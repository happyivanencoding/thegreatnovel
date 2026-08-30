from __future__ import annotations
import json, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

WORKTREE=Path(r'C:\dev\tgn-story-mvp-atomic-gate-skip-reviser-20260830')
OLD=Path(r'C:\dev\tgn-story-mvp-native-e2e\books\real-exp-native-structured-e2e-20260830-v1')
BASE=WORKTREE/'books'/'real-exp-free-text-atomic-gate-skip-reviser-20260830-v1'/'feasibility-oracle'
sys.path.insert(0,str(WORKTREE/'temps'))
from run_native_structured_e2e import call_acp, clean_model_text
SAMPLES=('jiuchui_ch14','jiuchui_ch16','shadow_ch4','shadow_ch9')
RUNS=('fresh-control-3','fresh-control-4')

def body(text:str)->str:
    t=clean_model_text(text).strip()
    if '# 正式正文' in t:
        t=t.rsplit('# 正式正文',1)[-1].strip()
    return t

def parse_json(text:str):
    clean=clean_model_text(text).strip()
    m=re.search(r'\{.*\}',clean,re.S)
    if not m: raise ValueError('no json')
    v=json.loads(m.group(0))
    if v.get('decision') not in {'PASS_DIRECT_FINAL','FALLBACK_FULL'}: raise ValueError(v)
    return v

def make_prompt(sample:str, run:str)->str:
    template=(OLD/'primary-oracle-gate-v2'/'e2e-run4'/sample/'prompt.md').read_text(encoding='utf-8')
    prefix=template.split('PRIMARY DRAFT:',1)[0]
    primary=body((OLD/run/sample/'primary_response.md').read_text(encoding='utf-8'))
    return prefix+'PRIMARY DRAFT:\n'+primary+'\n\n严格只输出JSON：{"decision":"PASS_DIRECT_FINAL|FALLBACK_FULL","hard_violations":[],"missing_required":[],"reason":"4-8句"}\n'

def one(sample:str,run:str):
    out=BASE/run/sample; out.mkdir(parents=True,exist_ok=True)
    prompt=make_prompt(sample,run); pp=out/'prompt.md'; ap=out/'acp.json'; pp.write_text(prompt,encoding='utf-8')
    data=call_acp(pp,ap,model='gpt-5.6-luna',effort='high')
    raw=str(data.get('text','')); (out/'response.md').write_text(raw.strip()+'\n',encoding='utf-8')
    val=parse_json(raw)
    return {'run':run,'sample':sample,'decision':val['decision'],'hard_violations':val.get('hard_violations',[]),'missing_required':val.get('missing_required',[]),'reason':val.get('reason',''),'wall_seconds':float(data.get('wall_seconds') or 0)}

rows=[]
with ThreadPoolExecutor(max_workers=8) as ex:
    fs=[ex.submit(one,s,r) for r in RUNS for s in SAMPLES]
    for f in as_completed(fs):
        row=f.result();rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
rows.sort(key=lambda x:(x['run'],x['sample']))
summary={'schema_version':'free-text-primary-feasibility-oracle-v1','runs':list(RUNS),'samples':list(SAMPLES),'attempts':len(rows),'pass_direct_final':sum(r['decision']=='PASS_DIRECT_FINAL' for r in rows),'fallback_full':sum(r['decision']=='FALLBACK_FULL' for r in rows),'rows':rows}
BASE.mkdir(parents=True,exist_ok=True);(BASE/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='rows'},ensure_ascii=False,indent=2))
