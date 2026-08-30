from __future__ import annotations
import argparse,json,sys
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
WORKTREE=Path(r"C:\dev\tgn-story-mvp-native-e2e")
BASE=WORKTREE/"books"/"real-exp-native-structured-e2e-20260830-v1"
sys.path.insert(0,str(WORKTREE/"temps"))
from run_native_structured_e2e import (MODEL,body,call_acp,clean_model_text,replace_h2_block,replace_mission_values,replace_primary_curated_context,source_directory)
SAMPLES=("jiuchui_ch14","jiuchui_ch16","shadow_ch4","shadow_ch9")

def one(sample:str,run_label:str):
    src=source_directory(sample);out=BASE/run_label/sample;out.mkdir(parents=True,exist_ok=True)
    old_mission=(src/'director_response.md').read_text(encoding='utf-8').strip()
    # Director
    dp=out/'director_prompt.md';da=out/'director_acp.json';dp.write_text((src/'director_prompt.md').read_text(encoding='utf-8'),encoding='utf-8')
    data=call_acp(dp,da,model=MODEL['director'][0],effort=MODEL['director'][1]); mission=clean_model_text(str(data.get('text','')));(out/'director_response.md').write_text(mission+'\n',encoding='utf-8');dw=float(data.get('wall_seconds') or 0)
    # Curator sees the fresh Director mission everywhere the old mission appeared.
    cp=replace_mission_values((src/'curator_prompt.md').read_text(encoding='utf-8'),old_mission,mission)
    cpp=out/'curator_prompt.md';cpa=out/'curator_acp.json';cpp.write_text(cp,encoding='utf-8')
    data=call_acp(cpp,cpa,model=MODEL['curator'][0],effort=MODEL['curator'][1]);cur=clean_model_text(str(data.get('text','')));(out/'curator_response.md').write_text(cur+'\n',encoding='utf-8');cw=float(data.get('wall_seconds') or 0)
    # Primary sees the same fresh mission + fresh Curator.
    pp=replace_mission_values((src/'primary_prompt.md').read_text(encoding='utf-8'),old_mission,mission);pp=replace_primary_curated_context(pp,cur)
    ppp=out/'primary_prompt.md';ppa=out/'primary_acp.json';ppp.write_text(pp,encoding='utf-8')
    data=call_acp(ppp,ppa,model=MODEL['primary'][0],effort=MODEL['primary'][1]);pri=clean_model_text(str(data.get('text','')));(out/'primary_response.md').write_text(pri+'\n',encoding='utf-8');pw=float(data.get('wall_seconds') or 0)
    # Reviser sees fresh mission + fresh Curator + fresh Primary.
    rp=(src/'authority_reviser_prompt.md').read_text(encoding='utf-8');rp=replace_h2_block(rp,'FROZEN CHAPTER MISSION',mission);rp=replace_h2_block(rp,'CURATOR',cur);rp=replace_h2_block(rp,'PRIMARY DRAFT',pri)
    rpp=out/'reviser_prompt.md';rpa=out/'reviser_acp.json';rpp.write_text(rp,encoding='utf-8')
    data=call_acp(rpp,rpa,model=MODEL['reviser'][0],effort=MODEL['reviser'][1]);rev=clean_model_text(str(data.get('text','')));(out/'reviser_response.md').write_text(rev+'\n',encoding='utf-8');rw=float(data.get('wall_seconds') or 0)
    final=body(rev);(out/'final_body.md').write_text(final+'\n',encoding='utf-8')
    return {'sample':sample,'director_seconds':dw,'curator_seconds':cw,'primary_seconds':pw,'reviser_seconds':rw,'total_seconds':round(dw+cw+pw+rw,3),'mission_chars':len(mission),'final_chars':len(final)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run-label',required=True);ap.add_argument('--workers',type=int,default=4);a=ap.parse_args();rows=[]
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        fut=[ex.submit(one,s,a.run_label) for s in SAMPLES]
        for f in as_completed(fut):
            r=f.result();rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
    rows.sort(key=lambda x:x['sample']);by={n:round(sum(r[f'{n}_seconds'] for r in rows),3) for n in ('director','curator','primary','reviser')};summary={'schema_version':'fresh-control-chain-e2e-v1','run':a.run_label,'samples':4,'by_node_seconds':by,'total_seconds':round(sum(r['total_seconds'] for r in rows),3),'rows':rows};(BASE/a.run_label/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k!='rows'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
