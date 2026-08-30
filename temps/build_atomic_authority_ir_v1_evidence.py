from __future__ import annotations
import csv,json,re
from pathlib import Path
BASE=Path(r'books/real-exp-atomic-authority-ir-20260829-v1')
def load(rel):return json.loads((BASE/rel).read_text(encoding='utf-8'))
static=load('phase-a-static-ir/summary.json')
verbose=load('phase-b-director-sidecar/summary.json')
compact=load('phase-c-compact-director-sidecar/summary.json')
micro=load('phase-d-micro-director-sidecar/summary.json')
schema=load('phase-f-schema-validation/summary.json')
key=load('phase-e-blind-compact-mission/blind_key.json');blind_rows=load('phase-e-blind-compact-mission/summary.json')
counts={'story':{},'authority':{}};decoded=[]
for row in blind_rows:
 name=row['sample'];item={'sample':name}
 for field in ('story','authority'):
  m=re.search(r'(?m)^VERDICT:\s*(A|B|MIXED)',row[field]);v=m.group(1);val='MIXED' if v=='MIXED' else key[name][v]
  counts[field][val]=counts[field].get(val,0)+1;item[field]=val
  item[field+'_hard']=[line.strip() for line in row[field].splitlines() if line.startswith('HARD_')]
 decoded.append(item)
blind={'counts':counts,'rows':decoded}
evidence={
 'schema_version':'atomic-authority-ir-v1-evidence-index',
 'final_question':'Can source-pure typed Authority IR + separate Primary Preservation Map replace post-hoc Chinese obligation parsing?',
 'static_source_pure_ir':static,
 'verbose_json_sidecar':verbose,
 'compact_json_sidecar':compact,
 'micro_dsl_sidecar':micro,
 'mission_blind':blind,
 'schema_validation':schema,
 'focused_tests':{'passed':57,'command':'python -m pytest -q temps/test_atomic_authority_ir_v1.py'},
 'architecture':'ARCHITECTURE.md',
 'protocol':'PROTOCOL.md',
 'schemas':[str(p.relative_to(BASE)) for p in sorted((BASE/'schemas').glob('*.json'))],
 'independent_audits':{
   'formal_pre_fix':'phase-g2-postfix-audits/formal.md',
   'story_post_fix':'phase-g2-postfix-audits/story.md',
   'formal_resolution':'phase-g2-postfix-audits/FORMAL_AUDIT_RESOLUTION.md',
 },
}
(BASE/'EVIDENCE_INDEX.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rows=[
 ['source_pure_static_ir',static['samples'],'n/a','4/4 source-pure; 4/4 preflight eligible',f"editable ratio avg {static['average_editable_ratio']*100:.2f}%",'PASS_ARCHITECTURE'],
 ['verbose_json_sidecar',verbose['samples'],verbose['sidecar_wall_change_percent'],f"parse {verbose['parse_ok']}/4",f"merged eligible {verbose['merged_contracts_preflight_eligible']}/4; coverage {verbose['average_expected_structural_coverage']*100:.2f}%",'FAIL_OUTPUT_PROTOCOL'],
 ['compact_json_sidecar',compact['samples'],compact['sidecar_wall_change_percent'],f"Story control3/treatment1",f"Authority treatment3/control1; parse {compact['parse_ok']}/4; merged eligible {compact['merged_contracts_preflight_eligible']}/4",'FAIL_OUTPUT_PROTOCOL'],
 ['micro_dsl_sidecar',micro['samples'],micro['sidecar_wall_change_percent'],f"8 fields {micro['all_eight_fields_present']}/4",f"parse {micro['parse_ok']}/4; merged eligible {micro['merged_contracts_preflight_eligible']}/4",'FAIL_OUTPUT_PROTOCOL'],
 ['native_structured_decision_schema',57,'not measured','single typed source dual projection unit pass',f"schema/runtime checks {schema['valid_checks']}/{schema['artifact_checks']}; no free human clause",'PASS_SCHEMA_ONLY'],
 ['primary_preservation_map',static['samples'],'0 LLM calls','outside locality blocked 4/4',f"avg editable {static['average_editable_ratio']*100:.2f}%",'PASS_EXPERIMENTAL'],
 ['cross_book_same_schema',2,'0 LLM calls','two books / four chapters','4/4 static source-pure contracts eligible','PASS_STATIC_ONLY'],
 ['production_route',0,'0','unchanged','unsupported chapters bypass Atomic','NO_CHANGE'],
]
with (BASE/'DECISION_TABLE.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['route_or_layer','samples','wall_change_percent','story_or_locality','authority_or_schema','decision']);w.writerows(rows)
source_rows=[
 ['Frozen Mission','YES','Hard facts / current chapter transitions','No prose preservation'],
 ['Canon','YES','Occurred states / current holders / preconditions','No realization preference'],
 ['World Authority','YES','World rules / resource semantics','No chapter creativity'],
 ['Power Authority','YES','Stable scale / ability conditions','No automatic chapter upgrade'],
 ['Human Authority','YES','Approved human constraints / named conditional trigger','No prose quota'],
 ['Reader Release','YES','Scheduled reader-knowledge fact','No unscheduled encyclopedia'],
 ['Curator','NO','Location/protection hints and non-binding diagnostics','Cannot create fact/conflict/entity/edit window'],
 ['Primary Draft','NO','Evidence location / protected fragment inside allowed window','Cannot define identity, fact, conflict or Authority'],
 ['Delta / Reviser / Judge','NO','Candidate text or experiment evaluation only','Cannot self-certify Hard Contract'],
]
with (BASE/'SOURCE_SEPARATION_MATRIX.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['source','may_create_hard_contract','allowed_contribution','forbidden_contribution']);w.writerows(source_rows)
print(json.dumps({'blind':blind,'decision_rows':len(rows),'source_rows':len(source_rows)},ensure_ascii=False,indent=2))
