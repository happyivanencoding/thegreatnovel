from __future__ import annotations
import json,re,sys
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
WORKTREE=Path(r'C:\dev\tgn-story-mvp-atomic-gate-skip-reviser-20260830')
BASE=WORKTREE/'books'/'real-exp-free-text-atomic-gate-skip-reviser-20260830-v1'
sys.path.insert(0,str(WORKTREE/'temps'))
from run_free_text_atomic_gate_e2e import call,clean,body
RUNS=('fresh-gate-1','fresh-gate-2'); SAMPLES=('jiuchui_ch14','shadow_ch9')

def authority_from_reviser(prompt:str)->str:
    start=prompt.find('## AUTHORITY')
    if start<0: start=prompt.find('## FROZEN CHAPTER MISSION')
    end=prompt.find('## ACTIVE SCENE REVISION WATCH')
    if end<0: end=prompt.find('## PRIMARY DRAFT')
    if start<0 or end<0 or end<=start: raise ValueError('authority block')
    return prompt[start:end].strip()

def parse(raw:str):
    t=clean(raw);m=re.search(r'\{.*\}',t,re.S)
    if not m: raise ValueError(t[:500])
    v=json.loads(m.group(0))
    if v.get('decision') not in {'PASS_DIRECT_FINAL','FALLBACK_FULL'}: raise ValueError(v)
    return v

def one(run,sample,repeat):
    d=BASE/run/sample;out=BASE/'authority-oracle'/run/sample/f'repeat-{repeat}';out.mkdir(parents=True,exist_ok=True)
    authority=authority_from_reviser((d/'reviser_prompt.md').read_text(encoding='utf-8'))
    primary=(d/'primary_body.md').read_text(encoding='utf-8').strip()
    prompt=f'''你是 fresh-context TGN Frozen Authority 审计员。你不是改稿模型，也不评文笔。\n\n任务：判断下面这份 Primary Draft 能否**不经过 Full Authority Reviser，直接成为 Final Draft**。\n\nPASS 只允许在以下条件同时成立时给出：\n- Frozen Chapter Mission 中当前章必须发生的 actor/action/object、Direct Result、State Change、Ending 已经落实；\n- money/payment、ownership、power boundary、relationship、Reader Release、unknown boundary 与跨章 timing 没有会污染下一章 Canon 的错误；\n- 没有把未到账的回报写成已到账、把未知写成已知、把允许范围扩大成新能力；\n- 缺失只属于文风/可选细节，而不是当前章必须落地的事实。\n\n不要因为文本激进、爽、群众反应强或更简洁而扣分。不要因为“可能会错”而保守判 FAIL；只报具体已发生的 hard conflict / required missing。\n\n严格只输出 JSON：\n{{"decision":"PASS_DIRECT_FINAL|FALLBACK_FULL","hard_violations":[],"missing_required":[],"reason":"中文4-8句，指出具体事实"}}\n\n# FROZEN AUTHORITY AND CURRENT CONTEXT\n\n{authority}\n\n# PRIMARY DRAFT\n\n{primary}\n'''
    pp=out/'prompt.md';ap=out/'acp.json';pp.write_text(prompt,encoding='utf-8')
    data=call(pp,ap,'gpt-5.6-luna','high');raw=str(data.get('text',''));(out/'response.md').write_text(raw.strip()+'\n',encoding='utf-8');v=parse(raw)
    return {'run':run,'sample':sample,'repeat':repeat,'decision':v['decision'],'hard_violations':v.get('hard_violations',[]),'missing_required':v.get('missing_required',[]),'reason':v.get('reason',''),'wall_seconds':float(data.get('wall_seconds') or 0)}
rows=[]
with ThreadPoolExecutor(max_workers=8) as ex:
    fs=[ex.submit(one,r,s,k) for r in RUNS for s in SAMPLES for k in (1,2)]
    for f in as_completed(fs):
        row=f.result();rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
rows.sort(key=lambda x:(x['run'],x['sample'],x['repeat']))
summary={'schema_version':'free-text-atomic-bypass-authority-oracle-v1','supported_samples':list(SAMPLES),'calls':len(rows),'rows':rows}
for r in RUNS:
    summary[r]={}
    for s in SAMPLES:
        ds=[x['decision'] for x in rows if x['run']==r and x['sample']==s]
        summary[r][s]={'decisions':ds,'unanimous_pass':all(x=='PASS_DIRECT_FINAL' for x in ds),'unanimous_fallback':all(x=='FALLBACK_FULL' for x in ds)}
(BASE/'authority-oracle'/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='rows'},ensure_ascii=False,indent=2))
