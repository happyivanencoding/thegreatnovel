from __future__ import annotations
import json,re,subprocess,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import sys
ROOT=Path(r"C:\dev\tgn-story-mvp")
BOOK=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1';SOURCE=BOOK/'runs'
CUR=ROOT/'books'/'real-exp-chapter-latency-optimization-20260829-v1'/'phase-f-curator-model-route'
OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'full-curator-terra-high-downstream'
RUNNER=Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs");CHAPTERS=(2,10,14,19);VARIANTS=('luna_high','terra_high')
sys.path.insert(0,str(ROOT/'src'))
from story_mvp.hybrid_runtime import extract_unresolved_fact_boundary,strip_legacy_prose_controls  # noqa:E402
from story_mvp.scene_skills import render_selected_revision_watches,strip_scene_skill_selection  # noqa:E402

def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def body(t):return clean(t).rsplit('# 正式正文',1)[-1].strip()
def call(pp,op,model,effort):
 last=''
 for a in range(3):
  cp=subprocess.run(['node',str(RUNNER),str(pp),str(op),model,effort,str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if cp.returncode==0 and op.exists():
   try:j=json.loads(op.read_text(encoding='utf-8'))
   except Exception as e:j={};last=str(e)
   if j.get('ok'):return j
   last=str(j.get('error',''))
  else:last=(cp.stderr+'\n'+cp.stdout)[-3000:]
  time.sleep(2+a*2)
 raise RuntimeError(last)
def replace_once(t,old,new,label):
 if t.count(old)!=1:raise RuntimeError(f'{label}: count={t.count(old)}')
 return t.replace(old,new,1)
def replace_watch(prompt,old_cur,new_cur):
 old=render_selected_revision_watches(old_cur);new=render_selected_revision_watches(new_cur);heading='## ACTIVE SCENE REVISION WATCH｜只在明确失败时局部使用';primary='## PRIMARY DRAFT｜唯一待修订正文底稿'
 if old:
  block=f'{heading}\n\n{old}'
  if new:return prompt.replace(block,f'{heading}\n\n{new}',1)
  return prompt.replace(block+'\n\n','',1)
 if new:return prompt.replace(primary,f'{heading}\n\n{new}\n\n{primary}',1)
 return prompt
def one(ch,variant):
 src=SOURCE/f'chapter-{ch:04d}';d=OUT/f'chapter-{ch:04d}'/variant;d.mkdir(parents=True,exist_ok=True);old_cur=clean((src/'curator_response.md').read_text(encoding='utf-8'));new_cur=clean((CUR/f'chapter-{ch:04d}'/f'{variant}_response.md').read_text(encoding='utf-8'));old_vis=strip_legacy_prose_controls(strip_scene_skill_selection(old_cur));new_vis=strip_legacy_prose_controls(strip_scene_skill_selection(new_cur));old_un=extract_unresolved_fact_boundary(old_cur);new_un=extract_unresolved_fact_boundary(new_cur)
 pp=(src/'primary_prompt.md').read_text(encoding='utf-8');pp=replace_once(pp,old_vis,new_vis,f'ch{ch} {variant} curator')
 if old_un!=new_un:pp=replace_once(pp,old_un or '（Curator 未投影出额外未解事实；仍服从最高事实边界。）',new_un or '（Curator 未投影出额外未解事实；仍服从最高事实边界。）',f'ch{ch} {variant} unresolved')
 ppp=d/'primary_prompt.md';pop=d/'primary_acp.json';ppp.write_text(pp,encoding='utf-8');pd=call(ppp,pop,'gpt-5.6-terra','high');pt=clean(pd.get('text',''));pb=body(pt);(d/'primary_response.md').write_text(pt+'\n',encoding='utf-8');(d/'primary_body.md').write_text(pb+'\n',encoding='utf-8')
 old_primary=body((src/'primary_response.md').read_text(encoding='utf-8'));rp=(src/'authority_reviser_prompt.md').read_text(encoding='utf-8');rp=replace_once(rp,old_cur,new_cur,f'ch{ch} {variant} reviser curator');rp=replace_once(rp,old_primary,pb,f'ch{ch} {variant} reviser primary');rp=replace_watch(rp,old_cur,new_cur);rpp=d/'reviser_prompt.md';rop=d/'reviser_acp.json';rpp.write_text(rp,encoding='utf-8');rd=call(rpp,rop,'gpt-5.6-luna','high');rt=clean(rd.get('text',''));fb=body(rt);(d/'reviser_response.md').write_text(rt+'\n',encoding='utf-8');(d/'final_body.md').write_text(fb+'\n',encoding='utf-8')
 cd=json.loads((CUR/f'chapter-{ch:04d}'/f'{variant}_acp.json').read_text(encoding='utf-8'));return {'chapter':ch,'variant':variant,'curator_wall_seconds':float(cd.get('wall_seconds') or 0),'primary_wall_seconds':float(pd.get('wall_seconds') or 0),'reviser_wall_seconds':float(rd.get('wall_seconds') or 0),'total_seconds':round(float(cd.get('wall_seconds') or 0)+float(pd.get('wall_seconds') or 0)+float(rd.get('wall_seconds') or 0),3),'curator_chars':len(new_cur),'primary_chars':len(pb),'final_chars':len(fb)}
def main():
 OUT.mkdir(parents=True,exist_ok=True);rows=[]
 with ThreadPoolExecutor(max_workers=8) as ex:
  fs=[ex.submit(one,ch,v) for ch in CHAPTERS for v in VARIANTS]
  for f in as_completed(fs):r=f.result();rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
 rows.sort(key=lambda x:(x['chapter'],x['variant']));(OUT/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
