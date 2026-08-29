from __future__ import annotations
import json,re,subprocess,sys,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp')
SRC=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'/'runs'
EXP=ROOT/'books'/'real-exp-chapter-latency-optimization-20260829-v1'/'phase-h-curator-medium-contract-fixed'
RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')
CHAPTERS=[2,3,10,13,14,16,19]
sys.path.insert(0,str(ROOT/'src'))
from story_mvp.hybrid_runtime import strip_legacy_prose_controls
from story_mvp.scene_skills import strip_scene_skill_selection,render_selected_revision_watches

def clean(t:str)->str:
    return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def body(t:str)->str:
    return clean(t).rsplit('# 正式正文',1)[-1].strip()
def call(prompt_path:Path,out:Path,model:str,effort:str)->dict:
    last=''
    for attempt in range(3):
        cp=subprocess.run(['node',str(RUNNER),str(prompt_path),str(out),model,effort,str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
        if cp.returncode==0 and out.exists():
            try:j=json.loads(out.read_text(encoding='utf-8'))
            except Exception as e:j={};last=str(e)
            if j.get('ok'):return j
            last=str(j.get('error',''))
        else:last=(cp.stderr+'\n'+cp.stdout)[-3000:]
        time.sleep(2+attempt*2)
    raise RuntimeError(last)

def one(ch:int):
    src=SRC/f'chapter-{ch:04d}'; dst=EXP/f'chapter-{ch:04d}'
    old_cur=clean((src/'curator_response.md').read_text(encoding='utf-8'))
    new_cur=clean((dst/'curator_contract_fixed_response.md').read_text(encoding='utf-8'))
    old_visible=strip_legacy_prose_controls(strip_scene_skill_selection(old_cur))
    new_visible=strip_legacy_prose_controls(strip_scene_skill_selection(new_cur))
    p_prompt=(src/'primary_prompt.md').read_text(encoding='utf-8')
    if p_prompt.count(old_visible)!=1: raise RuntimeError(f'ch{ch}: old visible count={p_prompt.count(old_visible)}')
    p_prompt=p_prompt.replace(old_visible,new_visible,1)
    pp=dst/'primary_treatment_prompt.md'; pp.write_text(p_prompt,encoding='utf-8')
    pj=call(pp,dst/'primary_treatment_acp.json','gpt-5.6-terra','high')
    p_text=clean(pj.get('text','')); p_body=body(p_text)
    (dst/'primary_treatment_response.md').write_text(p_text+'\n',encoding='utf-8')
    (dst/'primary_treatment_body.md').write_text(p_body+'\n',encoding='utf-8')

    old_primary=body((src/'primary_response.md').read_text(encoding='utf-8'))
    r_prompt=(src/'authority_reviser_prompt.md').read_text(encoding='utf-8')
    if r_prompt.count(old_cur)!=1: raise RuntimeError(f'ch{ch}: old curator count in reviser={r_prompt.count(old_cur)}')
    if r_prompt.count(old_primary)!=1: raise RuntimeError(f'ch{ch}: old primary count in reviser={r_prompt.count(old_primary)}')
    r_prompt=r_prompt.replace(old_cur,new_cur,1).replace(old_primary,p_body,1)
    old_watch=render_selected_revision_watches(old_cur); new_watch=render_selected_revision_watches(new_cur)
    if old_watch and old_watch!=new_watch:
        if r_prompt.count(old_watch)!=1: raise RuntimeError(f'ch{ch}: old watch count={r_prompt.count(old_watch)}')
        r_prompt=r_prompt.replace(old_watch,new_watch,1)
    rp=dst/'reviser_treatment_prompt.md';rp.write_text(r_prompt,encoding='utf-8')
    rj=call(rp,dst/'reviser_treatment_acp.json','gpt-5.6-luna','high')
    r_text=clean(rj.get('text','')); final=body(r_text)
    (dst/'reviser_treatment_response.md').write_text(r_text+'\n',encoding='utf-8')
    (dst/'final_treatment_body.md').write_text(final+'\n',encoding='utf-8')
    return {'chapter':ch,'primary_seconds':pj.get('wall_seconds'),'reviser_seconds':rj.get('wall_seconds'),'primary_usage':pj.get('result',{}).get('usage',{}),'reviser_usage':rj.get('result',{}).get('usage',{}),'primary_chars':len(p_body),'final_chars':len(final)}
rows=[]
with ThreadPoolExecutor(max_workers=7) as ex:
    for f in as_completed([ex.submit(one,ch) for ch in CHAPTERS]):
        r=f.result();rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
rows.sort(key=lambda x:x['chapter']);(EXP/'downstream_summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
