from __future__ import annotations
import argparse,json,re,subprocess,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from typing import Any

WORKTREE=Path(r'C:\dev\tgn-story-mvp-atomic-gate-skip-reviser-20260830')
BASE=WORKTREE/'books'/'real-exp-free-text-atomic-gate-skip-reviser-20260830-v1'
INPUTS=BASE/'frozen-inputs'
RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')
MODEL={'director':('gpt-5.6-luna','high'),'curator':('gpt-5.6-luna','high'),'primary':('gpt-5.6-terra','high'),'reviser':('gpt-5.6-luna','high')}
SAMPLES=('jiuchui_ch14','jiuchui_ch16','shadow_ch4','shadow_ch9')
MISSION_LABELS=('触发事件','推动事件的人','主角行动','对手或世界反应','直接结果','状态变化','叙事功能','结尾推动力')
import sys
sys.path.insert(0,str(WORKTREE/'temps'))
from atomic_primary_bypass_gate import evaluate

def clean(text:str)->str:
    return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',text).strip()
def body(text:str)->str:
    t=clean(text)
    if '# 正式正文' in t:t=t.rsplit('# 正式正文',1)[-1].strip()
    return t
def call(prompt:Path,out:Path,model:str,effort:str)->dict[str,Any]:
    last=''
    for attempt in range(3):
        try:
            cp=subprocess.run(['node',str(RUNNER),str(prompt),str(out),model,effort,str(WORKTREE)],cwd=WORKTREE,text=True,capture_output=True,encoding='utf-8',errors='replace',timeout=1200)
        except subprocess.TimeoutExpired:
            last='timeout';time.sleep(2+attempt*2);continue
        if cp.returncode==0 and out.exists():
            try:d=json.loads(out.read_text(encoding='utf-8'))
            except Exception as e:d={};last=str(e)
            if d.get('ok'):return d
            last=str(d.get('error',''))
        else:last=(cp.stderr+'\n'+cp.stdout)[-3000:]
        time.sleep(2+attempt*2)
    raise RuntimeError(last)
def parse_mission_fields(text:str)->dict[str,str]:
    result={}
    for i,label in enumerate(MISSION_LABELS):
        nxt='|'.join(re.escape(x) for x in MISSION_LABELS[i+1:])
        pat=rf'(?ms)^{re.escape(label)}：\s*(.*?)(?=^(?:{nxt})：|^## |\Z)' if nxt else rf'(?ms)^{re.escape(label)}：\s*(.*?)(?=^## |\Z)'
        m=re.search(pat,text)
        if m:result[label]=m.group(1).strip()
    return result
def replace_mission_values(prompt:str,old_mission:str,new_mission:str)->str:
    old=parse_mission_fields(old_mission);new=parse_mission_fields(new_mission)
    for label in MISSION_LABELS:
        if old.get(label) and new.get(label):prompt=prompt.replace(old[label],new[label])
    return prompt
def replace_h2_block(text:str,heading_prefix:str,replacement:str)->str:
    hs=list(re.finditer(r'(?m)^##\s+(.+?)\s*$',text))
    for i,m in enumerate(hs):
        if m.group(1).strip().startswith(heading_prefix):
            end=hs[i+1].start() if i+1<len(hs) else len(text)
            return text[:m.end()]+'\n\n'+replacement.strip()+'\n\n'+text[end:]
    raise ValueError(heading_prefix)
def replace_primary_curated_context(prompt:str,curator:str)->str:
    marker='## Curated Chapter Context';start=prompt.find(marker)
    if start<0:raise ValueError(marker)
    return prompt[:start]+marker+'\n\n'+curator.strip()+'\n'

def one(sample:str,run_label:str):
    src=INPUTS/sample;out=BASE/run_label/sample;out.mkdir(parents=True,exist_ok=True)
    old_mission=(src/'director_response.md').read_text(encoding='utf-8').strip()
    # rich free-text Director
    dp=out/'director_prompt.md';dp.write_text((src/'director_prompt.md').read_text(encoding='utf-8'),encoding='utf-8')
    d=call(dp,out/'director_acp.json',*MODEL['director']); mission=clean(str(d.get('text','')));(out/'director_response.md').write_text(mission+'\n',encoding='utf-8');dw=float(d.get('wall_seconds') or 0)
    # Curator
    cp=replace_mission_values((src/'curator_prompt.md').read_text(encoding='utf-8'),old_mission,mission);cpp=out/'curator_prompt.md';cpp.write_text(cp,encoding='utf-8')
    d=call(cpp,out/'curator_acp.json',*MODEL['curator']);cur=clean(str(d.get('text','')));(out/'curator_response.md').write_text(cur+'\n',encoding='utf-8');cw=float(d.get('wall_seconds') or 0)
    # Primary
    pp=replace_mission_values((src/'primary_prompt.md').read_text(encoding='utf-8'),old_mission,mission);pp=replace_primary_curated_context(pp,cur);ppp=out/'primary_prompt.md';ppp.write_text(pp,encoding='utf-8')
    d=call(ppp,out/'primary_acp.json',*MODEL['primary']);pri_raw=clean(str(d.get('text','')));pri=body(pri_raw);(out/'primary_response.md').write_text(pri_raw+'\n',encoding='utf-8');(out/'primary_body.md').write_text(pri+'\n',encoding='utf-8');pw=float(d.get('wall_seconds') or 0)
    # deterministic background gate
    g=evaluate(sample,pri)
    gate={'supported':g.supported,'pass':g.pass_,'decision':'PASS_DIRECT_FINAL' if g.supported and g.pass_ else 'FALLBACK_FULL','blockers':list(g.blockers),'evidence':list(g.evidence),'wall_ms':g.elapsed_ms}
    (out/'gate_result.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Always run the current Full Reviser as fallback or shadow control. Shadow time is excluded from treatment critical path on PASS.
    rp=(src/'authority_reviser_prompt.md').read_text(encoding='utf-8');rp=replace_h2_block(rp,'FROZEN CHAPTER MISSION',mission);rp=replace_h2_block(rp,'CURATOR',cur);rp=replace_h2_block(rp,'PRIMARY DRAFT',pri_raw);rpp=out/'reviser_prompt.md';rpp.write_text(rp,encoding='utf-8')
    d=call(rpp,out/'reviser_acp.json',*MODEL['reviser']);rev_raw=clean(str(d.get('text','')));rev=body(rev_raw);(out/'reviser_response.md').write_text(rev_raw+'\n',encoding='utf-8');(out/'control_final_body.md').write_text(rev+'\n',encoding='utf-8');rw=float(d.get('wall_seconds') or 0)
    gate_pass=gate['decision']=='PASS_DIRECT_FINAL';final=pri if gate_pass else rev;(out/'treatment_final_body.md').write_text(final+'\n',encoding='utf-8')
    gate_s=g.elapsed_ms/1000.0
    common=dw+cw+pw
    control=common+rw
    treatment=common+gate_s+(0 if gate_pass else rw)
    return {'sample':sample,'gate':gate['decision'],'supported':g.supported,'director_seconds':dw,'curator_seconds':cw,'primary_seconds':pw,'gate_seconds':round(gate_s,6),'reviser_seconds':rw,'control_total_seconds':round(control,3),'treatment_total_seconds':round(treatment,3),'seconds_saved':round(control-treatment,3),'percent_saved':round((1-treatment/control)*100,2),'primary_chars':len(pri),'reviser_chars':len(rev),'final_source':'primary' if gate_pass else 'reviser','blockers':list(g.blockers)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run-label',required=True);ap.add_argument('--workers',type=int,default=4);a=ap.parse_args()
    start=time.perf_counter();rows=[]
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        fs=[ex.submit(one,s,a.run_label) for s in SAMPLES]
        for f in as_completed(fs):
            r=f.result();rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
    rows.sort(key=lambda x:x['sample']);
    control=sum(r['control_total_seconds'] for r in rows);treatment=sum(r['treatment_total_seconds'] for r in rows)
    summary={'schema_version':'free-text-atomic-bypass-e2e-v1','run':a.run_label,'samples':4,'gate_supported':sum(r['supported'] for r in rows),'gate_pass':sum(r['gate']=='PASS_DIRECT_FINAL' for r in rows),'gate_fallback':sum(r['gate']!='PASS_DIRECT_FINAL' for r in rows),'control_total_seconds':round(control,3),'treatment_total_seconds':round(treatment,3),'seconds_saved':round(control-treatment,3),'percent_saved':round((1-treatment/control)*100,2),'seconds_saved_per_chapter':round((control-treatment)/4,3),'batch_elapsed_seconds':round(time.perf_counter()-start,3),'rows':rows}
    (BASE/a.run_label/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k!='rows'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
