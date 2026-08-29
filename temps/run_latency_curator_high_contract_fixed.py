from __future__ import annotations
import json,subprocess,re,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp'); SRC=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'/'runs'; EXP=ROOT/'books'/'real-exp-chapter-latency-optimization-20260829-v1'/'phase-i-curator-high-contract-fixed'; RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs'); CH=[2,3,10,13,14,16,19]; EXP.mkdir(parents=True,exist_ok=True)
OLD='''## Relevant Inspiration\n\n`## Scene Prose Projection`'''; NEW='''## Relevant Inspiration\n## Reader-Facing Language\n## Already Established — Do Not Re-explain\n## Recent Repetition Risks\n## Payoff and Promise Window\n\n`## Scene Prose Projection`'''
def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def one(ch):
 d=EXP/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True);t=(SRC/f'chapter-{ch:04d}'/'curator_prompt.md').read_text(encoding='utf-8');assert t.count(OLD)==1;t=t.replace(OLD,NEW,1);pp=d/'prompt.md';pp.write_text(t,encoding='utf-8');out=d/'acp.json'
 for a in range(3):
  cp=subprocess.run(['node',str(RUNNER),str(pp),str(out),'gpt-5.6-luna','high',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if cp.returncode==0 and out.exists():
   j=json.loads(out.read_text(encoding='utf-8'))
   if j.get('ok'):
    text=clean(j['text']);(d/'response.md').write_text(text+'\n',encoding='utf-8');return {'chapter':ch,'wall_seconds':j['wall_seconds'],'usage':j.get('result',{}).get('usage',{}),'chars':len(text),'headings':re.findall(r'(?m)^##\s+(.+?)\s*$',text)}
  time.sleep(2+a*2)
 raise RuntimeError(f'ch{ch} failed')
rows=[]
with ThreadPoolExecutor(max_workers=7) as ex:
 for f in as_completed([ex.submit(one,ch) for ch in CH]):
  r=f.result();rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
rows.sort(key=lambda x:x['chapter']);(EXP/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
