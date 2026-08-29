from __future__ import annotations
import hashlib,json,re
from pathlib import Path
BASE=Path(r'books/real-exp-atomic-chapter-obligations-20260829-v1')
BLIND=BASE/'phase-i-blind-atomic-delta-corrected'
ROUTE=BASE/'phase-k-v03-revalidation'
key=json.loads((BLIND/'blind_key.json').read_text(encoding='utf-8'))
summary=json.loads((BLIND/'summary.json').read_text(encoding='utf-8'))
route_summary=json.loads((ROUTE/'summary.json').read_text(encoding='utf-8'))
rows=[];counts={'reader':{},'authority':{}}
for row in route_summary['rows']:
    if row['run']!='run1' or row['route_status']!='ADOPT_DELTA': continue
    chapter=int(row['chapter']); ch=str(chapter)
    blind_row=next(item for item in summary if int(item['chapter'])==chapter)
    route_body=(ROUTE/f'chapter-{chapter:04d}'/'run1_route_final_body.md').read_text(encoding='utf-8').strip()
    prompt=(BLIND/f'chapter-{chapter:04d}'/'reader_prompt.md').read_text(encoding='utf-8')
    option_a=prompt.split('# OPTION A',1)[1].split('# OPTION B',1)[0].strip()
    option_b=prompt.split('# OPTION B',1)[1].strip()
    atomic_option='A' if key[ch]['A']=='atomic_delta' else 'B'
    atomic_body=option_a if atomic_option=='A' else option_b
    if hashlib.sha256(route_body.encode()).hexdigest()!=hashlib.sha256(atomic_body.encode()).hexdigest():
        raise RuntimeError(f'ch{chapter}: current route body differs from judged atomic option')
    decoded={'chapter':chapter,'route_status':'ADOPT_DELTA','body_hash_verified':True}
    for judge in ('reader','authority'):
        match=re.search(r'(?m)^VERDICT:\s*(A|B|MIXED)',blind_row[judge])
        verdict=match.group(1)
        value='MIXED' if verdict=='MIXED' else key[ch][verdict]
        counts[judge][value]=counts[judge].get(value,0)+1
        decoded[judge]=value
    rows.append(decoded)
out={'version':'atomic-obligations-v0.3-boundary-calibrated','scope':'Only v0.3 ADOPT_DELTA rows whose exact final body was already anonymously judged','counts':counts,'rows':rows}
dir=BASE/'phase-l-v03-effective-blind';dir.mkdir(parents=True,exist_ok=True)
(dir/'summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
