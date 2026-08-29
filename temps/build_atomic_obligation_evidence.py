from __future__ import annotations
import difflib, hashlib, json, re
from pathlib import Path

ROOT=Path(r'C:\dev\tgn-story-mvp')
BASE=ROOT/'books'/'real-exp-atomic-chapter-obligations-20260829-v1'
SOURCE=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'/'runs'


def load(rel):
    p=BASE/rel
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None

def slim_summary(rel):
    d=load(rel)
    if not d:return None
    return {k:v for k,v in d.items() if k!='rows'}

def decode_blind(dirname):
    d=BASE/dirname
    if not (d/'blind_key.json').exists() or not (d/'summary.json').exists():return None
    key=json.loads((d/'blind_key.json').read_text(encoding='utf-8'))
    rows=json.loads((d/'summary.json').read_text(encoding='utf-8'))
    counts={}; decoded=[]
    for row in rows:
        ch=str(row['chapter']); item={'chapter':int(ch)}
        for field in ('reader','story','authority','state'):
            text=row.get(field)
            if not isinstance(text,str):continue
            m=re.search(r'(?mi)^VERDICT:\s*(A|B|C|MIXED)\s*$',text)
            if not m:continue
            v=m.group(1).upper(); val='MIXED' if v=='MIXED' else key.get(ch,{}).get(v,v)
            counts.setdefault(field,{})[val]=counts.setdefault(field,{}).get(val,0)+1
            item[field]=val
            item[field+'_hard']=[line.strip() for line in text.splitlines() if line.startswith('HARD_')]
        decoded.append(item)
    return {'counts':counts,'rows':decoded}

def exact_repeat(dir1,dir2,chapters=(2,9,14,16)):
    rows=[]
    for ch in chapters:
        candidates=[]
        for dirname in (dir1,dir2):
            d=BASE/dirname/f'chapter-{ch:04d}'
            for name in ('route_final_body.md','residual_candidate.md','delta_candidate.md','final_body.md'):
                p=d/name
                if p.exists():
                    candidates.append((dirname,name,p.read_text(encoding='utf-8').strip()));break
        if len(candidates)!=2:
            rows.append({'chapter':ch,'comparable':False,'found':[(x[0],x[1]) for x in candidates]});continue
        a,b=candidates
        rows.append({'chapter':ch,'comparable':True,'exact':a[2]==b[2], 'a_file':a[1],'b_file':b[1], 'a_sha256':hashlib.sha256(a[2].encode()).hexdigest(),'b_sha256':hashlib.sha256(b[2].encode()).hexdigest(),'similarity':round(difflib.SequenceMatcher(None,a[2],b[2],autojunk=False).ratio(),6)})
    return {'exact_count':sum(r.get('exact') for r in rows),'comparable_count':sum(r.get('comparable') for r in rows),'rows':rows}

cal=load('phase-b-calibration/summary.json')
full20=load('phase-f-full20-audit/summary.json')
cross=load('phase-e-crossbook-compile/summary.json')
first=load('phase-c-atomic-delta/summary.json')
repeat=load('phase-c2-atomic-delta-repeat2/summary.json')
gateonly=load('phase-c0-gate-only-delta/summary.json')
residual=load('phase-c3-residual-repair/summary.json')
residual2=load('phase-c4-residual-repair-repeat2/summary.json')

# Calibration confusion matrix, tolerant to historical key names.
cal_rows=cal.get('rows',[]) if cal else []
conf={'safe_total':0,'safe_admitted':0,'safe_blocked':0,'bad_total':0,'bad_blocked':0,'bad_missed':0}
for row in cal_rows:
    expected=row.get('expected','')
    decision=row.get('decision','')
    if expected=='KNOWN_SAFE':
        conf['safe_total']+=1
        conf['safe_admitted']+=decision=='ADOPT_DELTA'
        conf['safe_blocked']+=decision!='ADOPT_DELTA'
    elif expected=='KNOWN_BAD':
        conf['bad_total']+=1
        conf['bad_blocked']+=decision!='ADOPT_DELTA'
        conf['bad_missed']+=decision=='ADOPT_DELTA'

# Aggregate route metrics.
def aggregate(d):
    if not d:return None
    rows=d.get('rows',[])
    control=d.get('control_total_seconds')
    effective=d.get('effective_total_seconds')
    if control is None and rows: control=sum(float(r.get('full_reviser_wall_seconds',r.get('control_full_reviser_seconds',0))) for r in rows)
    if effective is None and rows: effective=sum(float(r.get('effective_route_seconds',0)) for r in rows)
    return {
        'samples':d.get('samples',len(rows)),
        'adopted':sum(str(r.get('route_status','')).startswith('ADOPT') for r in rows),
        'fallback':sum('FALLBACK' in str(r.get('route_status','')) or 'FAILURE' in str(r.get('route_status','')) for r in rows),
        'control_total_seconds':round(float(control or 0),3),
        'effective_total_seconds':round(float(effective or 0),3),
        'fallback_adjusted_speedup_percent':round((1-float(effective)/float(control))*100,2) if control and effective is not None else d.get('fallback_adjusted_speedup_percent'),
        'rows':rows,
    }

# Obligation kind coverage from saved packs.
kind_counts={}; mode_counts={}; severity_counts={}; eligible_packs=0; packs=0
for p in BASE.glob('phase-f-full20-audit/chapter-*/obligation_pack.json'):
    d=json.loads(p.read_text(encoding='utf-8')); packs+=1; eligible_packs+=bool(d.get('preflight_eligible'))
    for o in d.get('obligations',[]):
        kind_counts[o['kind']]=kind_counts.get(o['kind'],0)+1
        mode_counts[o['mode']]=mode_counts.get(o['mode'],0)+1
        severity_counts[o['severity']]=severity_counts.get(o['severity'],0)+1

# Diff snippets for known boundary cases.
def body(text):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',text).strip().rsplit('# 正式正文',1)[-1].strip()
def paragraphs(text):return [x.strip() for x in re.split(r'\n\s*\n',text) if x.strip()]
def changed_excerpt(ch, treatment_dir, keywords):
    control=body((SOURCE/f'chapter-{ch:04d}'/'authority_reviser_response.md').read_text(encoding='utf-8'))
    td=BASE/treatment_dir/f'chapter-{ch:04d}'
    tp=None
    for name in ('route_final_body.md','residual_candidate.md','delta_candidate.md','final_body.md'):
        p=td/name
        if p.exists():tp=p;break
    if not tp:return {'chapter':ch,'missing':True}
    treat=tp.read_text(encoding='utf-8').strip()
    cp=paragraphs(control);tpv=paragraphs(treat)
    selected=[]
    for side,label in ((cp,'control'),(tpv,'treatment')):
        hits=[p for p in side if any(k in p for k in keywords)]
        selected.append({'side':label,'paragraphs':hits[:4]})
    return {'chapter':ch,'file':str(tp.relative_to(BASE)),'exact_control':control==treat,'similarity':round(difflib.SequenceMatcher(None,control,treat,autojunk=False).ratio(),6),'excerpts':selected}

examples=[
 changed_excerpt(2,'phase-c-atomic-delta',('阮青蜃','裂槽','记录')),
 changed_excerpt(9,'phase-c-atomic-delta',('观日宗','遗物','异兽','药材')),
 changed_excerpt(14,'phase-c3-residual-repair',('车辕','货队','出发','回潮楔','残压')),
 changed_excerpt(16,'phase-c3-residual-repair',('分身','回潮楔','钉进','钉入')),
]

evidence={
 'version':'atomic-chapter-obligations-v0.1',
 'calibration_confusion_matrix':conf,
 'calibration_summary':{k:v for k,v in (cal or {}).items() if k!='rows'},
 'full20_audit':{k:v for k,v in (full20 or {}).items() if k!='rows'},
 'crossbook_compile':{k:v for k,v in (cross or {}).items() if k!='rows'},
 'obligation_coverage':{'packs':packs,'eligible_packs':eligible_packs,'kind_counts':kind_counts,'mode_counts':mode_counts,'severity_counts':severity_counts},
 'atomic_prompt_delta':aggregate(first),
 'atomic_prompt_delta_repeat2':aggregate(repeat),
 'gate_only_delta':aggregate(gateonly),
 'residual_only_repair':aggregate(residual),
 'residual_only_repair_repeat2':aggregate(residual2),
 'atomic_repeatability':exact_repeat('phase-c-atomic-delta','phase-c2-atomic-delta-repeat2'),
 'residual_repeatability':exact_repeat('phase-c3-residual-repair','phase-c4-residual-repair-repeat2'),
 'blind_atomic_prompt':decode_blind('phase-d-blind-atomic-delta'),
 'blind_residual_repair':decode_blind('phase-d3-blind-residual-repair'),
 'examples':examples,
 'independent_audits':{
  'formal':'phase-g-independent-audits/formal_audit.md',
  'story':'phase-g-independent-audits/story_audit.md',
 },
}
(BASE/'EVIDENCE_INDEX.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# compact machine decision data
(BASE/'METRICS_SUMMARY.json').write_text(json.dumps({
 'calibration':conf,
 'full20':evidence['full20_audit'],
 'crossbook':evidence['crossbook_compile'],
 'routes':{k:evidence[k] for k in ('atomic_prompt_delta','atomic_prompt_delta_repeat2','gate_only_delta','residual_only_repair','residual_only_repair_repeat2')},
 'repeatability':{'atomic':evidence['atomic_repeatability'],'residual':evidence['residual_repeatability']},
 'blind':{'atomic':evidence['blind_atomic_prompt'],'residual':evidence['blind_residual_repair']},
},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('wrote evidence',BASE/'EVIDENCE_INDEX.json')
