from __future__ import annotations
import json,re,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from typing import Any

ROOT=Path(r'C:\dev\tgn-story-mvp-local-repair-20260830')
SOURCE=Path(r'C:\dev\tgn-story-mvp-reviser-noop-20260830\books\real-exp-reviser-noop-upstream-heldout-20260830-v1\heldout-new-novel-2')
BASE=ROOT/'books'/'real-exp-local-authority-repair-20260830-v1'
OUT=BASE/'derivation-t1-transactional-high'
RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')
PROTOCOL=(BASE/'PROTOCOL_T1_SHA256.txt').read_text(encoding='utf-8').strip()

TRANSACTION_CONTRACT=r'''你是 TGN 的 Transactional High Authority Reviser。你仍使用 Luna-high 的全章判断能力，但不输出完整正文；你只输出全局一致的段落事务补丁。

原则：
- Frozen Mission / Canon / World / Power / Human / Reader Release 决定事实；Primary 是待修稿。
- Preservation First：正确段落逐字不动，不做同义润色。
- 发现事实/状态域需要修改时，必须在完整 Primary 中扫描该域所有依赖出现；若同一 ownership/resource/power/relationship/result 状态在多个段落都有依赖，必须把所有需要联动的段落放进同一个 transaction。
- 如果无法在最多8个单段替换、且不超过全文20%段落的范围内完成全局闭合，返回 ESCALATE_FULL。
- 只允许整段替换，不插入、删除、拆段、合段、重排。
- 不新增 Authority 未明确的伤势、数字、物品来源/持有关系、旧史、他人内心/认知或新能力。
- Reader Release 只补最短充分信息；状态/力量 milestone 只在批准时直称一次。
- 可以处理现有 Full Reviser 本来负责的明确问题：Authority冲突、必要Reader Release/结果/状态/Ending遗漏、Named Entity连续性、必要World/Power/Human realization，以及确定无新故事价值的重复/程序化展开。
- 不为了更顺、更漂亮而改正确段落。

严格只输出一个JSON对象，三种 disposition：
1. {"disposition":"NO_CHANGE","transactions":[]}
2. {"disposition":"ESCALATE_FULL","transactions":[],"reason":"..."}
3. {"disposition":"PATCH","transactions":[{"domain":"power:protagonist","reason":"具体失败","patches":[{"paragraph_id":12,"old_text":"逐字完整原段","new_text":"完整单段替换文本"}]}]}

PATCH 约束：
- old_text 必须逐字等于编号 Primary 中该 paragraph_id 的完整原段。
- 同一 paragraph_id 只能出现一次。
- new_text 必须是一个非空段落，不含空行。
- 一个 domain 一旦进入 PATCH，必须包含该 domain 所有需要同步修改的段落；不能只修第一处。
'''

def body(text:str)->str:return text.rsplit('# 正式正文',1)[-1].strip()
def paras(text:str)->list[str]:return [x.strip() for x in re.split(r'\n\s*\n',text.strip()) if x.strip()]
def call(prompt_path,out_path):
 p=subprocess.run(['node',str(RUNNER),str(prompt_path),str(out_path),'gpt-5.6-luna','high',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace',timeout=900)
 if p.returncode!=0:raise RuntimeError(p.stderr[-4000:])
 d=json.loads(out_path.read_text(encoding='utf-8'))
 if not d.get('ok'):raise RuntimeError(str(d.get('error')))
 return d

def parse_json(text:str):
 t=text.strip()
 if t.startswith('```'):
  t=re.sub(r'^```(?:json)?\s*','',t);t=re.sub(r'\s*```$','',t)
 return json.loads(t)

def build_prompt(full:str,primary:str)->str:
 marker='## PRIMARY DRAFT｜唯一待修订正文底稿'
 before=full.split(marker,1)[0]
 if '# Hybrid Runtime' in before:before='# Hybrid Runtime'+before.split('# Hybrid Runtime',1)[1]
 numbered='\n\n'.join(f'[P{i:03d}]\n{p}' for i,p in enumerate(paras(primary),1))
 return TRANSACTION_CONTRACT+'\n\n'+before.strip()+'\n\n## NUMBERED PRIMARY DRAFT\n'+numbered

def apply_transaction(raw:dict,primary:str):
 disposition=str(raw.get('disposition','')).upper(); ps=paras(primary)
 if disposition=='NO_CHANGE':return primary,[],disposition
 if disposition=='ESCALATE_FULL':return primary,[],disposition
 if disposition!='PATCH':raise ValueError('invalid disposition')
 txs=raw.get('transactions',[])
 if not isinstance(txs,list) or not txs:raise ValueError('PATCH without transactions')
 flat=[];seen=set();out=list(ps)
 for tx in txs:
  domain=str(tx.get('domain','')).strip();reason=str(tx.get('reason','')).strip()
  if not domain:raise ValueError('empty domain')
  patches=tx.get('patches',[])
  if not isinstance(patches,list) or not patches:raise ValueError('empty transaction patches')
  for patch in patches:
   idx=int(patch['paragraph_id']);old=str(patch['old_text']).strip();new=str(patch['new_text']).strip()
   if idx<1 or idx>len(ps):raise ValueError(f'bad paragraph id {idx}')
   if idx in seen:raise ValueError(f'duplicate paragraph {idx}')
   if ps[idx-1]!=old:raise ValueError(f'old_text mismatch P{idx}')
   if not new or '\n\n' in new:raise ValueError(f'paragraph structure change P{idx}')
   seen.add(idx);out[idx-1]=new;flat.append({'domain':domain,'paragraph_id':idx,'reason':reason,'old':old,'new':new})
 if len(flat)>8 or len(flat)>max(1,int(len(ps)*0.20)):raise ValueError(f'patch budget exceeded {len(flat)}/{len(ps)}')
 final='\n\n'.join(out)
 if len(paras(final))!=len(ps):raise ValueError('paragraph count changed')
 for idx,(a,b) in enumerate(zip(ps,paras(final)),1):
  if idx not in seen and a!=b:raise ValueError(f'unpatched paragraph changed P{idx}')
 return final,flat,disposition

def one(run,ch):
 src_run='runs' if run=='repeat1' else 'repeat2';d=SOURCE/src_run/f'chapter-{ch:04d}'
 full=(d/'treatment_reviser_prompt.md').read_text(encoding='utf-8');primary=body((d/'treatment_primary_response.md').read_text(encoding='utf-8'));high=body((d/'treatment_reviser_response.md').read_text(encoding='utf-8'))
 target=OUT/run/f'chapter-{ch:04d}';target.mkdir(parents=True,exist_ok=True);prompt=build_prompt(full,primary);pp=target/'t1_prompt.md';ap=target/'t1_acp.json';pp.write_text(prompt,encoding='utf-8')
 data=call(pp,ap);wall=float(data.get('wall_seconds') or 0);raw=parse_json(str(data.get('text','')));fallback_reason=''
 try:
  candidate,patches,disp=apply_transaction(raw,primary)
 except Exception as e:
  candidate=primary;patches=[];disp='PARSE_FALLBACK';fallback_reason=f'{type(e).__name__}: {e}'
 high_data=json.loads((d/'treatment_reviser_acp.json').read_text(encoding='utf-8'));high_wall=float(high_data.get('wall_seconds') or 0)
 fallback=disp in {'ESCALATE_FULL','PARSE_FALLBACK'}
 final=high if fallback else candidate;route_wall=wall+(high_wall if fallback else 0)
 (target/'t1_response.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(target/'route_final_body.md').write_text(final+'\n',encoding='utf-8');(target/'candidate_body.md').write_text(candidate+'\n',encoding='utf-8');(target/'primary_body.md').write_text(primary+'\n',encoding='utf-8');(target/'high_body.md').write_text(high+'\n',encoding='utf-8');(target/'patch_manifest.json').write_text(json.dumps({'protocol_sha256':PROTOCOL,'disposition':disp,'fallback':fallback,'fallback_reason':fallback_reason,'patches':patches},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 row={'run':run,'chapter':ch,'disposition':disp,'fallback':fallback,'patch_count':len(patches),'t1_wall':round(wall,3),'high_wall':round(high_wall,3),'route_wall':round(route_wall,3),'saved_vs_high':round(high_wall-route_wall,3)};print(row,flush=True);return row

def main():
 OUT.mkdir(parents=True,exist_ok=True);rows=[]
 with ThreadPoolExecutor(max_workers=8) as ex:
  fs=[ex.submit(one,r,c) for r in ['repeat1','repeat2'] for c in range(1,5)]
  for f in as_completed(fs):rows.append(f.result())
 rows.sort(key=lambda x:(x['run'],x['chapter']));summary={'schema_version':'transactional-high-diff-t1-derivation-v1','protocol_sha256':PROTOCOL,'rows':rows,'fallback_count':sum(r['fallback'] for r in rows),'mean_patch_count':round(sum(r['patch_count'] for r in rows)/len(rows),3),'mean_t1_wall':round(sum(r['t1_wall'] for r in rows)/len(rows),3),'mean_route_wall':round(sum(r['route_wall'] for r in rows)/len(rows),3),'mean_high_wall':round(sum(r['high_wall'] for r in rows)/len(rows),3),'mean_saved_vs_high':round(sum(r['saved_vs_high'] for r in rows)/len(rows),3)};(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
