from pathlib import Path
import json,re,csv
R=Path('books/real-exp-chapter-latency-innovation-20260829-v1')
rows=json.loads((R/'speculative-next-director-canonless-downstream/summary.json').read_text(encoding='utf-8'))
c=sum(float(x['control_state_through_reviser_seconds']) for x in rows)
t=sum(float(x['treatment_parallel_state_through_reviser_seconds']) for x in rows)
metric={'samples':len(rows),'control_avg_seconds':round(c/len(rows),3),'treatment_avg_seconds':round(t/len(rows),3),'aggregate_speedup_percent':round((1-t/c)*100,2),'average_seconds_saved':round((c-t)/len(rows),3),'per_sample_speedup_percent':[round((1-float(x['treatment_parallel_state_through_reviser_seconds'])/float(x['control_state_through_reviser_seconds']))*100,2) for x in rows]}
D=R/'blind-speculative-next-director-canonless-downstream'
key=json.loads((D/'blind_key.json').read_text(encoding='utf-8'))
judges=json.loads((D/'summary.json').read_text(encoding='utf-8'))
counts={}; decoded=[]
for row in judges:
    ch=str(row['chapter']); item={'chapter':int(ch)}
    for field in ('reader','authority'):
        m=re.search(r'(?mi)^VERDICT:\s*(A|B|MIXED)\s*$',row[field]); v=m.group(1).upper()
        val='MIXED' if v=='MIXED' else key[ch][v]
        counts.setdefault(field,{})[val]=counts.setdefault(field,{}).get(val,0)+1
        item[field]=val
    decoded.append(item)
blind={'counts':counts,'rows':decoded}
p=R/'EVIDENCE_INDEX.json'; data=json.loads(p.read_text(encoding='utf-8'))
data['speculative_director_canonless_full_downstream']=metric
data['blind-speculative-next-director-canonless-downstream']=blind
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
validation={'report':'RESULTS.md','decision_table':'DECISION_TABLE.csv','evidence_index':'EVIDENCE_INDEX.json','full_pytest':'386 passed','skill_version':'0.3.11','skill_package_digest':'sha256:e4306ea15aefec69da466130328bd9e7cf583bda702b81bf90faeb7c43c119eb','canonless_speculative':{'speed':metric,'blind':blind,'production_decision':'FAIL_DEFAULT'}}
(R/'FINAL_EVIDENCE_VALIDATION.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
# decision table
p=R/'DECISION_TABLE.csv'
with p.open(encoding='utf-8-sig',newline='') as f: table=list(csv.reader(f))
head, body=table[0],table[1:]
if not any(r and r[0]=='speculative_director_canonless_full' for r in body):
    idx=next(i for i,r in enumerate(body) if r and r[0]=='speculative_director_full')+1
    body.insert(idx,['speculative_director_canonless_full','6',str(metric['aggregate_speedup_percent']),'reader treatment3/control3','authority treatment2/control3/mixed1','FAIL_DEFAULT'])
with p.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(head);w.writerows(body)
print(json.dumps({'metric':metric,'blind':blind},ensure_ascii=False,indent=2))
