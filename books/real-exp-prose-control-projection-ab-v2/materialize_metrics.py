from pathlib import Path
import json,re
EXP=Path(r'C:\dev\tgn-story-mvp\books\real-exp-prose-control-projection-ab-v2')
rows=[]
ABSTRACT=['意味着','这意味着','说明','这说明','显然','可以看出','其实','换句话说','不代表','并不代表','这不是','而是','也就是说','证明了','足以说明']
EXPLICIT=['意味着','这说明','显然','可以看出','换句话说','也就是说','足以说明']
ACTION=['拿','按','退','挡','递','停','转身','踩','抓','推','拉','撞','绕','压','抬','落','冲','贴','扣','拨','跨','移','踏','收','放','伸','翻','拽','扯','撑','带']

def draft(text):
    m=re.search(r'# Primary Draft\s*\n(.*?)(?=\n# Primary Fact Summary|\Z)',text,re.S)
    return (m.group(1).strip() if m else text.strip())

def count_patterns(t, pats): return sum(t.count(p) for p in pats)
for case in ['action_retest','dialogue_projection','entry_projection']:
  for arm in ['OFF','ON']:
    p=EXP/case/f'{arm}.json'; o=json.loads(p.read_text(encoding='utf-8'))
    t=draft(o.get('text',''))
    (EXP/case/f'draft_{arm}.md').write_text(t+'\n',encoding='utf-8')
    paras=[x.strip() for x in re.split(r'\n\s*\n',t) if x.strip()]
    sents=[x for x in re.split(r'[。！？!?]+',t) if x.strip()]
    row={
      'case':case,'arm':arm,'ok':o.get('ok'),
      'stop':(((o.get('result') or {}).get('response') or {}).get('stopReason')),
      'sec':round(o.get('wall_seconds',0),1),'chars':len(t),'paras':len(paras),'sentences':len(sents),
      'avg_sent_chars':round(sum(len(x) for x in sents)/max(1,len(sents)),1),
      'abstract_broad':count_patterns(t,ABSTRACT),
      'abstract_explicit':count_patterns(t,EXPLICIT),
      'bu_shi_er_shi':len(re.findall(r'不是[^。！？\n]{0,50}而是',t)),
      'action_verbs':count_patterns(t,ACTION),
    }
    rows.append(row); print(row)
(EXP/'metrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
