from pathlib import Path
base=Path(r'books/real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1')
story=(base/'planning/story-11-20/response.md').read_text(encoding='utf-8')

def block(text, heading):
    s=text.find(heading)
    if s<0: raise RuntimeError(f'missing {heading}')
    tail=text[s+len(heading):]
    import re
    m=re.search(r'(?m)^##\s', tail)
    e=s+len(heading)+(m.start() if m else len(tail))
    return text[s:e].rstrip()

rse=block(story,'### RSE-03')
for rel in ['planning/outline-11-20/response.md','planning/outline-11-20/BOOK_PLANNED.md','BOOK_PLAN_11_20.md']:
    p=base/rel
    t=p.read_text(encoding='utf-8')
    old=block(t,'### RSE-03')
    t=t.replace(old,rse,1)
    p.write_text(t,encoding='utf-8')
    print('synced',rel,len(old),'->',len(rse))
