from __future__ import annotations
import json,re,subprocess,sys,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path

ROOT=Path(r'C:\dev\tgn-story-mvp')
SOURCE=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'/'runs'
DIRECTOR=ROOT/'books'/'real-exp-chapter-latency-optimization-20260829-v1'/'phase-3-conditional-director'
OUT=ROOT/'books'/'real-exp-chapter-latency-optimization-20260829-v1'/'phase-3-conditional-director-downstream'
RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')
CHAPTERS=(2,13,16,19,20)
FIELDS=('触发事件','推动事件的人','主角行动','对手或世界反应','直接结果','状态变化','叙事功能','结尾推动力')
FIELD_RE=re.compile(r'(?ms)^('+'|'.join(map(re.escape,FIELDS))+r')[：:]\s*(.*?)(?=^(?:'+'|'.join(map(re.escape,FIELDS))+r')[：:]|^##\s|\Z)')
OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'src'))
from story_mvp.hybrid_runtime import strip_legacy_prose_controls,extract_primary_draft
from story_mvp.scene_skills import strip_scene_skill_selection,render_selected_revision_watches

def clean(t:str)->str:
    return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def parse_fields(t:str)->dict[str,str]:
    out={}
    for m in FIELD_RE.finditer(t):out[m.group(1)]=re.sub(r'\s+',' ',m.group(2)).strip()
    if set(out)!=set(FIELDS):raise RuntimeError(f'field parse mismatch: {set(FIELDS)-set(out)}')
    return out
def replace_once_or_skip(text:str,old:str,new:str,label:str,allow_zero:bool=False)->str:
    n=text.count(old)
    if n==0 and allow_zero:return text
    if n!=1:raise RuntimeError(f'{label}: expected 1 match, got {n}')
    return text.replace(old,new,1)
def call(pp:Path,out:Path,model:str,effort:str)->dict:
    last=''
    for attempt in range(3):
        cp=subprocess.run(['node',str(RUNNER),str(pp),str(out),model,effort,str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
        if cp.returncode==0 and out.exists():
            try:j=json.loads(out.read_text(encoding='utf-8'))
            except Exception as e:j={};last=str(e)
            if j.get('ok'):return j
            last=str(j.get('error',''))
        else:last=(cp.stderr+'\n'+cp.stdout)[-3000:]
        time.sleep(2+attempt*2)
    raise RuntimeError(last)
def body(t:str)->str:
    extracted=extract_primary_draft(clean(t)).strip()
    return extracted or clean(t).rsplit('# 正式正文',1)[-1].strip()

def run_one(ch:int)->dict:
    src=SOURCE/f'chapter-{ch:04d}'; d=OUT/f'chapter-{ch:04d}'; d.mkdir(parents=True,exist_ok=True)
    old_director=clean((src/'director_response.md').read_text(encoding='utf-8'))
    new_director=clean((DIRECTOR/f'chapter-{ch:04d}'/'conditional_director_response.md').read_text(encoding='utf-8'))
    old_fields=parse_fields(old_director);new_fields=parse_fields(new_director)

    # Curator: change only the frozen event-contract values.
    cp=(src/'curator_prompt.md').read_text(encoding='utf-8')
    for f in FIELDS:cp=replace_once_or_skip(cp,old_fields[f],new_fields[f],f'ch{ch} curator {f}')
    cpp=d/'curator_prompt.md';cpp.write_text(cp,encoding='utf-8')
    cj=call(cpp,d/'curator_acp.json','gpt-5.6-luna','high')
    curator=clean(cj.get('text',''));(d/'curator_response.md').write_text(curator+'\n',encoding='utf-8')

    old_curator=clean((src/'curator_response.md').read_text(encoding='utf-8'))
    old_visible=strip_legacy_prose_controls(strip_scene_skill_selection(old_curator))
    new_visible=strip_legacy_prose_controls(strip_scene_skill_selection(curator))
    pp=(src/'primary_prompt.md').read_text(encoding='utf-8')
    pp=replace_once_or_skip(pp,old_visible,new_visible,f'ch{ch} primary curator')
    for f in FIELDS:
        pp=replace_once_or_skip(pp,old_fields[f],new_fields[f],f'ch{ch} primary {f}',allow_zero=(f=='叙事功能'))
    ppp=d/'primary_prompt.md';ppp.write_text(pp,encoding='utf-8')
    pj=call(ppp,d/'primary_acp.json','gpt-5.6-terra','high')
    primary_text=clean(pj.get('text',''));primary=body(primary_text)
    (d/'primary_response.md').write_text(primary_text+'\n',encoding='utf-8');(d/'primary_body.md').write_text(primary+'\n',encoding='utf-8')

    old_primary=body((src/'primary_response.md').read_text(encoding='utf-8'))
    rp=(src/'authority_reviser_prompt.md').read_text(encoding='utf-8')
    rp=replace_once_or_skip(rp,old_curator,curator,f'ch{ch} reviser curator')
    rp=replace_once_or_skip(rp,old_primary,primary,f'ch{ch} reviser primary')
    old_watch=render_selected_revision_watches(old_curator);new_watch=render_selected_revision_watches(curator)
    if old_watch and old_watch!=new_watch:
        rp=replace_once_or_skip(rp,old_watch,new_watch,f'ch{ch} reviser watch')
    for f in FIELDS:rp=replace_once_or_skip(rp,old_fields[f],new_fields[f],f'ch{ch} reviser {f}')
    rpp=d/'reviser_prompt.md';rpp.write_text(rp,encoding='utf-8')
    rj=call(rpp,d/'reviser_acp.json','gpt-5.6-luna','high')
    reviser_text=clean(rj.get('text',''));final=body(reviser_text)
    (d/'reviser_response.md').write_text(reviser_text+'\n',encoding='utf-8');(d/'final_body.md').write_text(final+'\n',encoding='utf-8')

    control={s:json.loads((src/f'{s}_acp.json').read_text(encoding='utf-8'))['wall_seconds'] for s in ('director','curator','primary','authority_reviser')}
    return {
      'chapter':ch,
      'conditional_director_seconds':json.loads((DIRECTOR/f'chapter-{ch:04d}'/'conditional_director_acp.json').read_text(encoding='utf-8'))['wall_seconds'],
      'control_seconds':control,
      'treatment_seconds':{'curator':cj.get('wall_seconds'),'primary':pj.get('wall_seconds'),'authority_reviser':rj.get('wall_seconds')},
      'treatment_chars':{'curator':len(curator),'primary':len(primary),'final':len(final)},
      'usage':{'curator':cj.get('result',{}).get('usage',{}),'primary':pj.get('result',{}).get('usage',{}),'authority_reviser':rj.get('result',{}).get('usage',{})}
    }

rows=[]
with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as ex:
    for fut in as_completed([ex.submit(run_one,ch) for ch in CHAPTERS]):
        row=fut.result();rows.append(row);print(json.dumps({'chapter':row['chapter'],'seconds':row['treatment_seconds'],'chars':row['treatment_chars']},ensure_ascii=False),flush=True)
rows.sort(key=lambda x:x['chapter']);(OUT/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
