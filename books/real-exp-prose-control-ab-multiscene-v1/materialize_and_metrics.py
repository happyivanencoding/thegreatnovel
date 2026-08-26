from pathlib import Path
import json,re,statistics
root=Path(r'C:\dev\tgn-story-mvp\books\real-exp-prose-control-ab-multiscene-v1')
abstract_terms=['意识到','意味着','显然','某种','复杂','仿佛','似乎','显得','说明了','证明了','这意味着','可以看出','因此','于是他明白','并非','不是','而是']
generic_reactions=['众人震惊','全场震惊','所有人都','一片哗然','目光一变','神色一变','微微一愣','心中一紧']
action_verbs=['抓','按','推','拉','挡','退','踩','转身','抬手','收回','递','站起','坐下','让开','扣住','撞','划','落下','停住','抬头','低头','迈','扑','绕','压住','放下']

def body_from(text:str)->str:
    m=re.search(r'# Primary Draft\s*\n([\s\S]*?)(?:\n# Primary Fact Summary|\Z)',text)
    if m:return m.group(1).strip()
    return text.strip()

def metrics(text:str):
    paras=[p.strip() for p in re.split(r'\n\s*\n',text) if p.strip()]
    sent=[s.strip() for s in re.split(r'(?<=[。！？!?])',text) if s.strip()]
    single=sum(1 for p in paras if len(re.findall(r'[。！？!?]',p))<=1)
    return {
      'chars':len(text),'paras':len(paras),'sentences':len(sent),
      'avg_sent_chars':round(sum(len(s) for s in sent)/max(1,len(sent)),1),
      'single_para_ratio':round(single/max(1,len(paras)),3),
      'abstract_terms':sum(text.count(t) for t in abstract_terms),
      'generic_reactions':sum(text.count(t) for t in generic_reactions),
      'action_verbs':sum(text.count(t) for t in action_verbs),
      'dialogue_marks':text.count('“')+text.count('”'),
    }
rows=[]
for case in ['dialogue','action','payoff','entry']:
  for arm in ['OFF','ON']:
    p=root/case/f'{arm}.json'
    o=json.loads(p.read_text(encoding='utf-8'))
    text=o.get('text','')
    body=body_from(text)
    (root/case/f'{arm}_response.md').write_text(text,encoding='utf-8')
    (root/case/f'{arm}_body.md').write_text(body+'\n',encoding='utf-8')
    stop=o.get('result',{}).get('response',{}).get('stopReason')
    m=metrics(body)
    row={'case':case,'arm':arm,'ok':o.get('ok'),'stop':stop,'sec':round(o.get('wall_seconds',0),1),'total_chars':len(text),**m}
    rows.append(row)
for r in rows: print(r)
(root/'metrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
