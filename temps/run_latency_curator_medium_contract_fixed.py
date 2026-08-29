from __future__ import annotations
import json,re,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp')
SRC=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'/'runs'
EXP=ROOT/'books'/'real-exp-chapter-latency-optimization-20260829-v1'/'phase-h-curator-medium-contract-fixed'
RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')
CHAPTERS=[2,3,10,13,14,16,19]
EXP.mkdir(parents=True,exist_ok=True)
OLD='''## Relevant Inspiration\n\n`## Scene Prose Projection`'''
NEW='''## Relevant Inspiration\n## Reader-Facing Language\n## Already Established — Do Not Re-explain\n## Recent Repetition Risks\n## Payoff and Promise Window\n\n`## Scene Prose Projection`'''

def clean(t:str)->str:
    return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()

def one(ch:int):
    d=EXP/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True)
    source=(SRC/f'chapter-{ch:04d}'/'curator_prompt.md').read_text(encoding='utf-8')
    if source.count(OLD)!=1: raise RuntimeError(f'ch{ch}: format block count={source.count(OLD)}')
    prompt=source.replace(OLD,NEW,1)
    pp=d/'curator_contract_fixed_prompt.md';pp.write_text(prompt,encoding='utf-8')
    out=d/'curator_contract_fixed_acp.json'
    cp=subprocess.run(['node',str(RUNNER),str(pp),str(out),'gpt-5.6-luna','medium',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
    if cp.returncode: raise RuntimeError(f'ch{ch}: {cp.stderr[-2500:]}')
    j=json.loads(out.read_text(encoding='utf-8'))
    if not j.get('ok'): raise RuntimeError(f'ch{ch}: {j.get("error")}')
    text=clean(j.get('text',''));(d/'curator_contract_fixed_response.md').write_text(text+'\n',encoding='utf-8')
    heads=re.findall(r'(?m)^##\s+(.+?)\s*$',text)
    return {'chapter':ch,'wall_seconds':j.get('wall_seconds'),'usage':j.get('result',{}).get('usage',{}),'chars':len(text),'headings':heads}
rows=[]
with ThreadPoolExecutor(max_workers=7) as ex:
    for f in as_completed([ex.submit(one,ch) for ch in CHAPTERS]):
        r=f.result();rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
rows.sort(key=lambda x:x['chapter']);(EXP/'curator_summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
