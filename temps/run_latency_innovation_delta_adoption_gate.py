from __future__ import annotations

import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT=Path(r"C:\dev\tgn-story-mvp")
RUNNER=Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'delta-adoption-gate'
CASES=(
    ('fast20',ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1',ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'paragraph-delta-reviser',(2,3,10,14,19)),
    ('shadow10',ROOT/'books'/'real-exp-current-pipeline-authority-reviser-0010-20260828-v1',ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'paragraph-delta-reviser-crossbook',(1,4,6,8,10)),
)

TEMPLATE="""你是 TGN 的 Delta Adoption Gate，使用 GPT-5.6 Luna medium。你看不到 Full Reviser 输出，也不自己改正文；只决定一份 Luna-high Paragraph Delta 候选能否直接成为最终正文，还是必须回到现有 Full Luna-high Reviser。

这是高精度放行，不是平均打分。只有同时满足以下条件才 `ACCEPT_DELTA`：
1. 相比 Primary，Delta 已修复或没有新增 Frozen Mission / Canon / World / Power / Human / Reader Release 的硬问题；行动者、对象、完成时态、结果、状态变化、资源/持有、数字、人物称谓/性别、正式势力/地点名、能力边界与 Ending 全部正确。
2. Delta 没有遗漏 Primary 中仍有价值且 authority-safe 的人物欲望、关系反应、核心幻想、具体获得、Public Proof、社会重新定价、惊喜、节奏停顿或章末真实动作。
3. 若 Primary 本身存在明确问题，Delta 必须真的解决；`KEEP_ALL` 只有当 Primary 已足够安全时才能放行。
4. Delta 不能通过新造数字、制度、价格、支付方式、能力规则、旧史、人物到场或未来事件来“修好”。
5. 任何不确定、只凭文风偏好、或需要全文重新分配笔墨才能判断的情况，都输出 `FULL_REVISER`。

注意：Full Reviser 可能自身也会随机出错，但本 Gate 不能以此为理由放过 Delta 的硬问题。你的问题只是：Delta 是否已经足够安全、完整、有男频价值，可以跳过 Full Reviser。

严格输出：
DECISION: ACCEPT_DELTA / FULL_REVISER
CONFIDENCE: high / medium / low
PRIMARY_HARD_PROBLEMS: 无 或逐条短写
DELTA_HARD_PROBLEMS: 无 或逐条短写
DELTA_FIXED_PRIMARY: YES / NO / NOT_NEEDED
VALUE_PRESERVED: YES / NO / UNCERTAIN
GLOBAL_CLOSURE_SAFE: YES / NO / UNCERTAIN
REASON: 6—12句，引用具体正文。
"""

def clean(text:str)->str:return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$","",text).strip()
def body(text:str)->str:return clean(text).rsplit('# 正式正文',1)[-1].strip()

def call(pp:Path,op:Path)->dict:
 last=''
 for attempt in range(3):
  proc=subprocess.run(['node',str(RUNNER),str(pp),str(op),'gpt-5.6-luna','medium',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if proc.returncode==0 and op.exists():
   try:data=json.loads(op.read_text(encoding='utf-8'))
   except Exception as e:data={};last=str(e)
   if data.get('ok'):return data
   last=str(data.get('error',''))
  else:last=(proc.stderr+'\n'+proc.stdout)[-3000:]
  time.sleep(2+attempt*2)
 raise RuntimeError(last)

def one(label:str,book:Path,treatment:Path,ch:int)->dict:
 source=book/'runs'/f'chapter-{ch:04d}';directory=OUT/label/f'chapter-{ch:04d}';directory.mkdir(parents=True,exist_ok=True)
 primary=body((source/'primary_response.md').read_text(encoding='utf-8'))
 delta=(treatment/f'chapter-{ch:04d}'/'final_body.md').read_text(encoding='utf-8').strip()
 auth=(source/'authority_reviser_prompt.md').read_text(encoding='utf-8').split('## PRIMARY DRAFT｜唯一待修订正文底稿',1)[0].strip()
 prompt='\n\n'.join((TEMPLATE,'# FROZEN AUTHORITY\n'+auth,'# PRIMARY DRAFT\n'+primary,'# DELTA CANDIDATE\n'+delta))
 pp=directory/'gate_prompt.md';op=directory/'gate_acp.json';pp.write_text(prompt,encoding='utf-8');data=call(pp,op);resp=clean(data.get('text',''));(directory/'gate_response.md').write_text(resp+'\n',encoding='utf-8')
 m=re.search(r'(?m)^DECISION:\s*(ACCEPT_DELTA|FULL_REVISER)\s*$',resp);decision=m.group(1) if m else 'INVALID'
 delta_data=json.loads((treatment/f'chapter-{ch:04d}'/'paragraph_delta_acp.json').read_text(encoding='utf-8'))
 control_data=json.loads((source/'authority_reviser_acp.json').read_text(encoding='utf-8'))
 dw=float(delta_data.get('wall_seconds') or 0);gw=float(data.get('wall_seconds') or 0);cw=float(control_data.get('wall_seconds') or 0);route=dw+gw+(cw if decision!='ACCEPT_DELTA' else 0)
 return {'book':label,'chapter':ch,'decision':decision,'delta_wall_seconds':dw,'gate_wall_seconds':gw,'control_wall_seconds':cw,'effective_route_seconds':round(route,3),'effective_speedup_percent':round((1-route/cw)*100,2),'response':resp,'usage':data.get('result',{}).get('usage',{})}

def main()->None:
 OUT.mkdir(parents=True,exist_ok=True);jobs=[(label,b,t,ch) for label,b,t,chs in CASES for ch in chs];rows=[]
 with ThreadPoolExecutor(max_workers=len(jobs)) as ex:
  futs=[ex.submit(one,*job) for job in jobs]
  for fut in as_completed(futs):
   row=fut.result();rows.append(row);print(json.dumps({k:row[k] for k in ('book','chapter','decision','gate_wall_seconds','effective_speedup_percent')},ensure_ascii=False),flush=True)
 rows.sort(key=lambda r:(r['book'],r['chapter']));(OUT/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':main()
