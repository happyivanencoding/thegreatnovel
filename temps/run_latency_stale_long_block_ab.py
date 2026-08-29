from __future__ import annotations
import json,re,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp'); SRC=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'/'runs'; EXP=ROOT/'books'/'real-exp-chapter-latency-optimization-20260829-v1'/'phase-e-stale-long-block'; RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs'); CHAPTERS=[11,14,19,20]; EXP.mkdir(parents=True,exist_ok=True)
def clean(t): return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def remove_stale_block(prompt:str)->tuple[str,int]:
    marker='## 当前大型剧情块与十章计划'
    s=prompt.index(marker)
    e=prompt.index('## PROSE PROFILE',s)
    block=prompt[s:e]
    split='当前章十章计划条目'
    if split not in block: raise RuntimeError('missing current chapter plan label')
    current=block.split(split,1)[1].strip()
    replacement=f'{marker}\n\n{split}\n\n{current}\n\n'
    return prompt[:s]+replacement+prompt[e:], len(block)-len(replacement)
def one(ch:int):
    src=SRC/f'chapter-{ch:04d}'/'curator_prompt.md';d=EXP/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True)
    treatment,removed=remove_stale_block(src.read_text(encoding='utf-8'));pp=d/'curator_no_stale_block_prompt.md';pp.write_text(treatment,encoding='utf-8');out=d/'curator_no_stale_block_acp.json'
    cp=subprocess.run(['node',str(RUNNER),str(pp),str(out),'gpt-5.6-luna','high',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
    if cp.returncode: raise RuntimeError(f'ch{ch}: {cp.stderr[-2500:]}')
    j=json.loads(out.read_text(encoding='utf-8'))
    if not j.get('ok'): raise RuntimeError(f'ch{ch}: {j.get("error")}')
    text=clean(j.get('text',''));(d/'curator_no_stale_block_response.md').write_text(text+'\n',encoding='utf-8')
    return {'chapter':ch,'removed_chars':removed,'prompt_chars':len(treatment),'wall_seconds':j.get('wall_seconds'),'usage':j.get('result',{}).get('usage',{}),'response_chars':len(text)}
rows=[]
with ThreadPoolExecutor(max_workers=4) as ex:
 for f in as_completed([ex.submit(one,ch) for ch in CHAPTERS]):
  r=f.result();rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
rows.sort(key=lambda x:x['chapter']);(EXP/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
