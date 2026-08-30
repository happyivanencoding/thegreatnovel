from __future__ import annotations
import json,random,re,sys
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
WORKTREE=Path(r'C:\dev\tgn-story-mvp-atomic-gate-skip-reviser-20260830')
BASE=WORKTREE/'books'/'real-exp-free-text-atomic-gate-skip-reviser-20260830-v1'
sys.path.insert(0,str(WORKTREE/'temps'))
from run_free_text_atomic_gate_e2e import call,clean
# Oracle-safe set: supported requires unanimous 2/2; unsupported has one strict oracle and will receive another independent Authority blind here.
SAFE={('fresh-gate-1','jiuchui_ch16'),('fresh-gate-1','shadow_ch4'),('fresh-gate-1','shadow_ch9'),('fresh-gate-2','jiuchui_ch14'),('fresh-gate-2','jiuchui_ch16'),('fresh-gate-2','shadow_ch4'),('fresh-gate-2','shadow_ch9')}

def authority(prompt:str)->str:
    starts=[prompt.find('## AUTHORITY'),prompt.find('## FROZEN CHAPTER MISSION')];starts=[x for x in starts if x>=0]
    ends=[prompt.find('## ACTIVE SCENE REVISION WATCH'),prompt.find('## PRIMARY DRAFT')];ends=[x for x in ends if x>=0]
    st=min(starts);en=min(x for x in ends if x>st);return prompt[st:en].strip()
def parse(raw):
    m=re.search(r'\{.*\}',clean(raw),re.S)
    if not m:raise ValueError(raw[:500])
    v=json.loads(m.group(0));return v

def one(run,sample,judge):
    d=BASE/run/sample;out=BASE/'oracle-safe-pair-blind'/run/sample;out.mkdir(parents=True,exist_ok=True)
    p=(d/'primary_body.md').read_text(encoding='utf-8').strip();r=(d/'control_final_body.md').read_text(encoding='utf-8').strip()
    order=['primary','reviser'];random.Random(f'{run}:{sample}:{judge}:oracle-safe').shuffle(order);key={'A':order[0],'B':order[1]};texts={'primary':p,'reviser':r}
    candidates=f"# A\n\n{texts[key['A']]}\n\n# B\n\n{texts[key['B']]}"
    if judge=='story':
        prompt=f'''你是匿名成熟中文男频商业编辑。A/B来自同一章、同一上游；一个是Primary，一个是Full Authority Reviser，但你不知道哪个。只评最终读者体验：续读欲、主角欲望与主动选择、冲突/动作、Reward/Public Proof/Surprise、关系、节奏、AI总结味、程序/报告味、漂亮二段论。不要因更长、更克制或看起来更“修订过”而偏爱。\n\n严格只输出JSON：{{"winner":"A|B|TIE","scores":{{"A":0,"B":0}},"reason":"中文5-8句具体比较"}}\n\n{candidates}\n'''
        model='gpt-5.6-terra'
    else:
        a=authority((d/'reviser_prompt.md').read_text(encoding='utf-8'))
        prompt=f'''你是匿名 TGN Frozen Authority 审计员。A/B来自同一章同一Authority。只比较 actor/action/object、Direct Result、State Change、Ending、money/ownership、power boundary、relationship、Reader Release、unknown 与跨章timing。不要评文笔。只有具体Hard conflict或required missing才扣。激进、爽、群众反应强本身不是错。\n\n严格只输出JSON：{{"winner":"A|B|TIE","scores":{{"A":0,"B":0}},"hard_problems":{{"A":[],"B":[]}},"reason":"中文5-8句具体比较"}}\n\n# AUTHORITY\n{a}\n\n{candidates}\n'''
        model='gpt-5.6-luna'
    pp=out/f'{judge}_prompt.md';ap=out/f'{judge}_acp.json';pp.write_text(prompt,encoding='utf-8');data=call(pp,ap,model,'high');raw=str(data.get('text',''));(out/f'{judge}_response.md').write_text(raw.strip()+'\n',encoding='utf-8');v=parse(raw)
    winner=v.get('winner');decoded='tie' if winner=='TIE' else key[winner]
    return {'run':run,'sample':sample,'judge':judge,'blind_key':key,'winner':decoded,'scores':{key[k]:float(val) for k,val in v.get('scores',{}).items()},'hard_problems':{key[k]:val for k,val in v.get('hard_problems',{}).items()} if judge=='authority' else {},'reason':v.get('reason',''),'wall_seconds':float(data.get('wall_seconds') or 0)}
rows=[]
with ThreadPoolExecutor(max_workers=10) as ex:
    fs=[ex.submit(one,r,s,j) for r,s in sorted(SAFE) for j in ('story','authority')]
    for f in as_completed(fs):
        x=f.result();rows.append(x);print(json.dumps(x,ensure_ascii=False),flush=True)
rows.sort(key=lambda x:(x['run'],x['sample'],x['judge']))
agg={}
for j in ('story','authority'):
    g=[x for x in rows if x['judge']==j];agg[j]={'primary_wins':sum(x['winner']=='primary' for x in g),'reviser_wins':sum(x['winner']=='reviser' for x in g),'ties':sum(x['winner']=='tie' for x in g),'primary_mean':round(sum(x['scores']['primary'] for x in g)/len(g),3),'reviser_mean':round(sum(x['scores']['reviser'] for x in g)/len(g),3)}
summary={'schema_version':'free-text-bypass-oracle-safe-pair-blind-v1','pairs':len(SAFE),'aggregates':agg,'rows':rows};(BASE/'oracle-safe-pair-blind'/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'pairs':len(SAFE),'aggregates':agg},ensure_ascii=False,indent=2))
