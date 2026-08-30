from __future__ import annotations
import json,random,re,sys
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
WORKTREE=Path(r'C:\dev\tgn-story-mvp-atomic-gate-skip-reviser-20260830')
BASE=WORKTREE/'books'/'real-exp-free-text-atomic-gate-skip-reviser-20260830-v1'
sys.path.insert(0,str(WORKTREE/'temps'))
from run_free_text_atomic_gate_e2e import call,clean
SAFE={('fresh-gate-1','jiuchui_ch16'),('fresh-gate-1','shadow_ch4'),('fresh-gate-1','shadow_ch9'),('fresh-gate-2','jiuchui_ch14'),('fresh-gate-2','jiuchui_ch16'),('fresh-gate-2','shadow_ch4'),('fresh-gate-2','shadow_ch9')}
def authority(prompt:str)->str:
 starts=[prompt.find('## AUTHORITY'),prompt.find('## FROZEN CHAPTER MISSION')];starts=[x for x in starts if x>=0];ends=[prompt.find('## ACTIVE SCENE REVISION WATCH'),prompt.find('## PRIMARY DRAFT')];ends=[x for x in ends if x>=0];st=min(starts);en=min(x for x in ends if x>st);return prompt[st:en].strip()
def parse(raw):
 m=re.search(r'\{.*\}',clean(raw),re.S)
 if not m: raise ValueError(raw[:400])
 return json.loads(m.group(0))
def one(run,sample,judge):
 d=BASE/run/sample;out=BASE/'oracle-safe-pair-blind-repeat2'/run/sample;out.mkdir(parents=True,exist_ok=True);p=(d/'primary_body.md').read_text(encoding='utf-8').strip();r=(d/'control_final_body.md').read_text(encoding='utf-8').strip();order=['primary','reviser'];random.Random(f'repeat2:{run}:{sample}:{judge}').shuffle(order);key={'A':order[0],'B':order[1]};texts={'primary':p,'reviser':r};cand=f"# A\n\n{texts[key['A']]}\n\n# B\n\n{texts[key['B']]}"
 if judge=='story':
  prompt=f'''你是 fresh-context 匿名成熟中文男频商业编辑。只评A/B最终读者体验，不知道哪个是Primary或Reviser。重点：续读欲、主角欲望与主动选择、冲突动作、Reward/Public Proof/Surprise、关系、节奏、AI总结味、程序/报告味、漂亮二段论。不要因更长/更短/更克制自动偏爱。严格只输出JSON：{{"winner":"A|B|TIE","scores":{{"A":0,"B":0}},"reason":"中文5-8句具体比较"}}\n\n{cand}''';model='gpt-5.6-terra'
 else:
  a=authority((d/'reviser_prompt.md').read_text(encoding='utf-8'));prompt=f'''你是 fresh-context 匿名TGN Frozen Authority审计员。只比较A/B的actor/action/object、Direct Result、State Change、Ending、money/ownership、power boundary、relationship、Reader Release、unknown与跨章timing，不评文笔。只有具体Hard conflict或required missing才扣分；激进/爽不是错。严格只输出JSON：{{"winner":"A|B|TIE","scores":{{"A":0,"B":0}},"hard_problems":{{"A":[],"B":[]}},"reason":"中文5-8句具体比较"}}\n\n# AUTHORITY\n{a}\n\n{cand}''';model='gpt-5.6-luna'
 pp=out/f'{judge}_prompt.md';ap=out/f'{judge}_acp.json';pp.write_text(prompt,encoding='utf-8');data=call(pp,ap,model,'high');raw=str(data.get('text',''));(out/f'{judge}_response.md').write_text(raw.strip()+'\n',encoding='utf-8');v=parse(raw);w=v.get('winner');decoded='tie' if w=='TIE' else key[w];return {'run':run,'sample':sample,'judge':judge,'winner':decoded,'blind_key':key,'scores':{key[k]:float(x) for k,x in v.get('scores',{}).items()},'hard_problems':{key[k]:x for k,x in v.get('hard_problems',{}).items()} if judge=='authority' else {},'reason':v.get('reason','')}
rows=[]
with ThreadPoolExecutor(max_workers=10) as ex:
 for f in as_completed([ex.submit(one,r,s,j) for r,s in sorted(SAFE) for j in ('story','authority')]):
  x=f.result();rows.append(x);print(json.dumps(x,ensure_ascii=False),flush=True)
rows.sort(key=lambda x:(x['run'],x['sample'],x['judge']));agg={}
for j in ('story','authority'):
 g=[x for x in rows if x['judge']==j];agg[j]={'primary_wins':sum(x['winner']=='primary' for x in g),'reviser_wins':sum(x['winner']=='reviser' for x in g),'ties':sum(x['winner']=='tie' for x in g),'primary_mean':round(sum(x['scores']['primary'] for x in g)/len(g),3),'reviser_mean':round(sum(x['scores']['reviser'] for x in g)/len(g),3)}
(BASE/'oracle-safe-pair-blind-repeat2'/'summary.json').write_text(json.dumps({'schema_version':'free-text-bypass-pair-blind-repeat2','pairs':7,'aggregates':agg,'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(agg,ensure_ascii=False,indent=2))
