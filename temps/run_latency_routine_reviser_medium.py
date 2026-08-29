from __future__ import annotations
import json,subprocess,re
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp');SRC=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'/'runs';EXP=ROOT/'books'/'real-exp-chapter-latency-optimization-20260829-v1'/'phase-d-routine-reviser-medium';RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs');CHAPTERS=[2,13,16];EXP.mkdir(parents=True,exist_ok=True)
def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def body(t):return clean(t).rsplit('# 正式正文',1)[-1].strip()
def one(ch):
 d=EXP/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True);pp=d/'reviser_prompt.md';pp.write_text((SRC/f'chapter-{ch:04d}'/'authority_reviser_prompt.md').read_text(encoding='utf-8'),encoding='utf-8');out=d/'reviser_medium_acp.json'
 cp=subprocess.run(['node',str(RUNNER),str(pp),str(out),'gpt-5.6-luna','medium',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
 if cp.returncode:raise RuntimeError(f'ch{ch}: {cp.stderr[-2500:]}')
 j=json.loads(out.read_text(encoding='utf-8'))
 if not j.get('ok'):raise RuntimeError(f'ch{ch}: {j.get("error")}')
 text=clean(j.get('text',''));final=body(text);(d/'reviser_medium_response.md').write_text(text+'\n',encoding='utf-8');(d/'final_medium_body.md').write_text(final+'\n',encoding='utf-8')
 return {'chapter':ch,'wall_seconds':j.get('wall_seconds'),'usage':j.get('result',{}).get('usage',{}),'body_chars':len(final)}
rows=[]
with ThreadPoolExecutor(max_workers=3) as ex:
 for f in as_completed([ex.submit(one,ch) for ch in CHAPTERS]):
  r=f.result();rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
rows.sort(key=lambda x:x['chapter']);(EXP/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
