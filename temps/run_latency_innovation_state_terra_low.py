from __future__ import annotations
import json,re,subprocess,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r"C:\dev\tgn-story-mvp");BOOK=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1';SOURCE=BOOK/'runs';OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'state-terra-low';RUNNER=Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs");CHAPTERS=(1,2,3,6,10,14,19,20)
HEADINGS=('Proposed Active Scene State','Proposed Persistent Canon','Proposed Chapter Summary','Proposed Open Promises')
def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def call(pp,op):
 last=''
 for a in range(3):
  cp=subprocess.run(['node',str(RUNNER),str(pp),str(op),'gpt-5.6-terra','low',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if cp.returncode==0 and op.exists():
   try:j=json.loads(op.read_text(encoding='utf-8'))
   except Exception as e:j={};last=str(e)
   if j.get('ok'):return j
   last=str(j.get('error',''))
  else:last=(cp.stderr+'\n'+cp.stdout)[-3000:]
  time.sleep(2+a*2)
 raise RuntimeError(last)
def parse(t):
 t=clean(t);out={}
 for i,h in enumerate(HEADINGS):
  m=re.search(rf'(?m)^# {re.escape(h)}\s*$',t)
  if not m:out[h]='';continue
  later=[x.start() for x in re.finditer(r'(?m)^# ',t[m.end():])];end=m.end()+(later[0] if later else len(t)-m.end());out[h]=re.sub(r'\s+',' ',t[m.end():end].strip())
 return out
def one(ch):
 src=SOURCE/f'chapter-{ch:04d}';d=OUT/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True);prompt=(src/'state_prompt.md').read_text(encoding='utf-8');pp=d/'terra_low_prompt.md';op=d/'terra_low_acp.json';pp.write_text(prompt,encoding='utf-8');td=call(pp,op);tr=clean(td.get('text',''));(d/'terra_low_response.md').write_text(tr+'\n',encoding='utf-8');ld=json.loads((src/'state_acp.json').read_text(encoding='utf-8'));lr=clean(ld.get('text',''));tf=parse(tr);lf=parse(lr);exact={h:tf[h]==lf[h] for h in HEADINGS};return {'chapter':ch,'terra_wall_seconds':float(td.get('wall_seconds') or 0),'luna_wall_seconds':float(ld.get('wall_seconds') or 0),'speedup_percent':round((1-float(td.get('wall_seconds') or 0)/float(ld.get('wall_seconds') or 1))*100,2),'field_exact':exact,'all_fields_exact':all(exact.values()),'terra_chars':len(tr),'luna_chars':len(lr),'terra_fields':tf,'luna_fields':lf,'usage':td.get('result',{}).get('usage',{})}
def main():
 OUT.mkdir(parents=True,exist_ok=True);rows=[]
 with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as ex:
  fs=[ex.submit(one,ch) for ch in CHAPTERS]
  for f in as_completed(fs):r=f.result();rows.append(r);print(json.dumps({k:r[k] for k in ('chapter','terra_wall_seconds','luna_wall_seconds','speedup_percent','all_fields_exact')},ensure_ascii=False),flush=True)
 rows.sort(key=lambda x:x['chapter']);(OUT/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
