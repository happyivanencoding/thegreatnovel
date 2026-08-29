from __future__ import annotations
import json, subprocess, time
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp')
OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'persistent-acp-probe'
EMPTY=Path(r'C:\dev\tgn-acp-text-runtime-empty')
RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')
BATCH=ROOT/'temps'/'run_latency_persistent_acp_batch.mjs'
OUT.mkdir(parents=True,exist_ok=True);EMPTY.mkdir(parents=True,exist_ok=True)
jobs=[]
for i in range(6):
    prompt=OUT/f'probe-{i+1}.md';prompt.write_text('严格只输出两个大写字母：OK\n',encoding='utf-8')
    jobs.append({'label':f'probe-{i+1}','prompt_path':str(prompt),'model':'gpt-5.6-luna','effort':'low'})
(OUT/'jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
control=[];start=time.time()
for job in jobs:
    out=OUT/f"control-{job['label']}.json"
    t=time.time()
    cp=subprocess.run(['node',str(RUNNER),job['prompt_path'],str(out),job['model'],job['effort'],str(EMPTY)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
    if cp.returncode: raise RuntimeError(cp.stderr[-2000:])
    data=json.loads(out.read_text(encoding='utf-8'))
    control.append({'label':job['label'],'external_elapsed':round(time.time()-t,3),'runner_wall_seconds':data.get('wall_seconds'),'text':data.get('text','').strip(),'usage':data.get('result',{}).get('usage',{})})
control_total=round(time.time()-start,3)
cp=subprocess.run(['node',str(BATCH),str(OUT/'jobs.json'),str(OUT/'persistent.json'),str(EMPTY)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
if cp.returncode: raise RuntimeError(cp.stderr[-3000:])
persistent=json.loads((OUT/'persistent.json').read_text(encoding='utf-8'))
summary={'control_total_external_seconds':control_total,'control':control,'persistent':persistent}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
