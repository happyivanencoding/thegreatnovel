from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import json,subprocess,time,re
ROOT=Path(r'C:\dev\tgn-story-mvp');D=ROOT/r'books/real-exp-atomic-authority-ir-20260829-v1/phase-g-independent-audits';RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')
def call(name,model):
 prompt=D/f'{name}_prompt.md';out=D/f'{name}_acp.json';last=''
 for attempt in range(3):
  try:r=subprocess.run(['node',str(RUNNER),str(prompt),str(out),model,'high',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace',timeout=1200)
  except subprocess.TimeoutExpired:last='timeout';continue
  if r.returncode==0 and out.exists():
   d=json.loads(out.read_text(encoding='utf-8'))
   if d.get('ok'):
    text=re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',d.get('text','')).strip();(D/f'{name}.md').write_text(text+'\n',encoding='utf-8');return {'name':name,'wall_seconds':d.get('wall_seconds'),'model':model}
   last=str(d.get('error'))
  else:last=(r.stderr+'\n'+r.stdout)[-3000:]
  time.sleep(2)
 raise RuntimeError(last)
with ThreadPoolExecutor(max_workers=2) as ex:
 fs=[ex.submit(call,'formal','gpt-5.6-luna'),ex.submit(call,'story','gpt-5.6-terra')]
 for f in as_completed(fs):print(json.dumps(f.result(),ensure_ascii=False),flush=True)
