from __future__ import annotations
import json,re,subprocess,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r"C:\dev\tgn-story-mvp")
BOOK=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1';SOURCE=BOOK/'runs'
WATCH=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'parallel-authority-watch'
OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'watch-original-contract-reviser'
RUNNER=Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs");CHAPTERS=(2,3,10,14,19)

def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def body(t):return clean(t).rsplit('# 正式正文',1)[-1].strip()
def call(pp,op):
 last=''
 for a in range(3):
  cp=subprocess.run(['node',str(RUNNER),str(pp),str(op),'gpt-5.6-luna','high',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if cp.returncode==0 and op.exists():
   try:j=json.loads(op.read_text(encoding='utf-8'))
   except Exception as e:j={};last=str(e)
   if j.get('ok'):return j
   last=str(j.get('error',''))
  else:last=(cp.stderr+'\n'+cp.stdout)[-3000:]
  time.sleep(2+a*2)
 raise RuntimeError(last)
def h2(text,prefix):
 starts=list(re.finditer(r'(?m)^##\s+(.+?)\s*$',text))
 for i,m in enumerate(starts):
  if m.group(1).strip().startswith(prefix):
   end=starts[i+1].start() if i+1<len(starts) else len(text);return text[m.end():end].strip()
 return ''
def one(ch):
 src=SOURCE/f'chapter-{ch:04d}';d=OUT/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True)
 full=(src/'authority_reviser_prompt.md').read_text(encoding='utf-8');watch=(WATCH/f'chapter-{ch:04d}'/'watchlist.md').read_text(encoding='utf-8').strip();primary=body((src/'primary_response.md').read_text(encoding='utf-8'))
 prefix=full.split('# Hybrid Runtime',1)[0].rstrip()
 curator=h2(full,'CURATOR｜');authority=h2(full,'AUTHORITY——');mission=h2(full,'FROZEN CHAPTER MISSION');release=h2(full,'READER RELEASE');tail=h2(full,'CANON TAIL');revision=h2(full,'ACTIVE SCENE REVISION WATCH')
 parts=[prefix,'# Hybrid Runtime\n\nwriter_mode: curator_primary',f'## AUTHORITY——按维度划分的事实与计划边界\n\n{authority}',f'## FROZEN CHAPTER MISSION｜不得改剧情\n\n{mission}',f'## CURATOR｜本章近端注意力与实现要求\n\n{curator}',f'## PRE-DRAFT AUTHORITY WATCHLIST｜远端 Authority 的高精度覆盖编译\n\n{watch}',f'## READER RELEASE｜本章已批准首次释放事实；逐条核对\n\n{release}',f'## CANON TAIL｜上一章必要衔接\n\n{tail}']
 if revision:parts.append(f'## ACTIVE SCENE REVISION WATCH｜只在明确失败时局部使用\n\n{revision}')
 parts.append(f'## PRIMARY DRAFT｜唯一待修订正文底稿\n\n{primary}')
 prompt='\n\n'.join(parts);pp=d/'compact_original_reviser_prompt.md';op=d/'compact_original_reviser_acp.json';pp.write_text(prompt,encoding='utf-8');data=call(pp,op);resp=clean(data.get('text',''));fb=body(resp);(d/'response.md').write_text(resp+'\n',encoding='utf-8');(d/'final_body.md').write_text(fb+'\n',encoding='utf-8')
 pd=json.loads((src/'primary_acp.json').read_text(encoding='utf-8'));cd=json.loads((src/'authority_reviser_acp.json').read_text(encoding='utf-8'));wd=json.loads((WATCH/f'chapter-{ch:04d}'/'watch_planner_acp.json').read_text(encoding='utf-8'));pw=float(pd.get('wall_seconds') or 0);cw=float(cd.get('wall_seconds') or 0);ww=float(wd.get('wall_seconds') or 0);rw=float(data.get('wall_seconds') or 0);control=pw+cw;treatment=max(pw,ww)+rw
 return {'chapter':ch,'primary_wall_seconds':pw,'planner_wall_seconds':ww,'control_reviser_wall_seconds':cw,'compact_reviser_wall_seconds':rw,'control_primary_plus_reviser_seconds':round(control,3),'treatment_parallel_critical_seconds':round(treatment,3),'speedup_percent':round((1-treatment/control)*100,2),'full_prompt_chars':len(full),'compact_prompt_chars':len(prompt),'prompt_reduction_percent':round((1-len(prompt)/len(full))*100,2),'final_chars':len(fb),'usage':data.get('result',{}).get('usage',{})}
def main():
 OUT.mkdir(parents=True,exist_ok=True);rows=[]
 with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as ex:
  fs=[ex.submit(one,ch) for ch in CHAPTERS]
  for f in as_completed(fs):r=f.result();rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
 rows.sort(key=lambda x:x['chapter']);(OUT/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
