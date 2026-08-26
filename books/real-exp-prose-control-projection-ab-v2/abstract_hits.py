from pathlib import Path
import re
exp=Path(r'C:\dev\tgn-story-mvp\books\real-exp-prose-control-projection-ab-v2')
terms=['意味着','这说明','显然','可以看出','其实','换句话说','也就是说','足以说明']
for case in ['action_retest','dialogue_projection','entry_projection']:
  print('\n###',case)
  for arm in ['OFF','ON']:
    t=(exp/case/f'draft_{arm}.md').read_text(encoding='utf-8')
    hits=[]
    for sent in re.split(r'(?<=[。！？])',t):
      if any(x in sent for x in terms): hits.append(sent.strip())
    print(arm, hits)
