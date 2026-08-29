from __future__ import annotations

import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT=Path(r"C:\dev\tgn-story-mvp")
BOOK=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'
SOURCE=BOOK/'runs'
SPEC=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'speculative-next-director'
OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'speculative-next-director-rebase-low'
RUNNER=Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
TRANSITIONS=((2,3),(3,4),(5,6),(12,13),(14,15),(18,19))
FIELDS=("触发事件","推动事件的人","主角行动","对手或世界反应","直接结果","状态变化","叙事功能","结尾推动力")

TEMPLATE="""你是 TGN 的 Next-Director State Rebase Clerk，使用 GPT-5.6 Luna low。你不重新规划，不追求文采，只在上一章 State Delta 已完成后核对一份并行生成的下一章 Director 合同。

权威：上一章正式 State Delta 是新事实；NEXT FUTURE-10 PLAN 是下一章唯一事件预算；SPECULATIVE DIRECTOR 是待校正合同。

只做三件事：
1. 若 State 新事实使 speculative 某字段过时、缺少刚刚完成/未完成的直接承接、错写持有人/地点/人物状态，做最小修正；
2. 确保计划规定的直接结果、状态变化与 Ending 没有被降成准备、资格、依据或以后再做；
3. 保留 speculative 已有的主角主动性、人物冲突、具体奖励/损失和商业拉力，不把它压成 State 摘要。

不得新增 State / Plan 未给出的数字、制度、支付方式、能力规则、旧史、人物到场或下一章之后的事件。不得把 State Delta 的记录语言复制进小说策划；要保持可写的故事合同。

若完全无需改，输出：
KEEP

否则严格只输出八字段：
触发事件：
推动事件的人：
主角行动：
对手或世界反应：
直接结果：
状态变化：
叙事功能：
结尾推动力：

不要输出 Audit、理由、评分或思考过程。"""


def clean(text:str)->str:
 return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$","",text).strip()


def call(prompt_path:Path,output_path:Path)->dict:
 last=''
 for attempt in range(3):
  proc=subprocess.run(['node',str(RUNNER),str(prompt_path),str(output_path),'gpt-5.6-luna','low',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if proc.returncode==0 and output_path.exists():
   try:data=json.loads(output_path.read_text(encoding='utf-8'))
   except Exception as e:data={};last=str(e)
   if data.get('ok'):return data
   last=str(data.get('error',''))
  else:last=(proc.stderr+'\n'+proc.stdout)[-3000:]
  time.sleep(2+attempt*2)
 raise RuntimeError(last)


def h2_blocks(text:str)->list[tuple[str,str]]:
 starts=list(re.finditer(r'(?m)^##\s+(.+?)\s*$',text))
 out=[]
 for i,m in enumerate(starts):
  end=starts[i+1].start() if i+1<len(starts) else len(text)
  out.append((m.group(1).strip(),text[m.end():end].strip()))
 return out


def next_plan(chapter:int)->str:
 prompt=(SOURCE/f'chapter-{chapter:04d}'/'director_prompt.md').read_text(encoding='utf-8')
 prefix=f'第{chapter}章'
 for heading,body in h2_blocks(prompt):
  if heading.startswith(prefix):return f'## {heading}\n\n{body}'
 raise RuntimeError(f'ch{chapter}: plan block missing')


def state_response(previous:int)->str:
 p=SOURCE/f'chapter-{previous:04d}'/'state_response.md'
 if not p.exists():p=SOURCE/f'chapter-{previous:04d}'/'state_response.txt'
 if not p.exists():
  # Historical runs use state_response.md; fallback to ACP text only for compatibility.
  data=json.loads((SOURCE/f'chapter-{previous:04d}'/'state_acp.json').read_text(encoding='utf-8'))
  return clean(data.get('text',''))
 return clean(p.read_text(encoding='utf-8'))


def valid_contract(text:str)->bool:
 return all(re.search(rf'(?m)^{re.escape(field)}：',text) for field in FIELDS)


def one(previous:int,chapter:int)->dict:
 directory=OUT/f'chapter-{chapter:04d}';directory.mkdir(parents=True,exist_ok=True)
 speculative=clean((SPEC/f'chapter-{chapter:04d}'/'speculative_director_response.md').read_text(encoding='utf-8'))
 prompt='\n\n'.join((TEMPLATE,'# PREVIOUS STATE DELTA\n'+state_response(previous),'# NEXT FUTURE-10 PLAN\n'+next_plan(chapter),'# SPECULATIVE DIRECTOR\n'+speculative))
 pp=directory/'rebase_prompt.md';op=directory/'rebase_acp.json';pp.write_text(prompt,encoding='utf-8')
 data=call(pp,op);response=clean(data.get('text',''))
 if response=='KEEP':final=speculative;mode='keep'
 elif valid_contract(response):final=response;mode='rebased'
 else:final=clean((SOURCE/f'chapter-{chapter:04d}'/'director_response.md').read_text(encoding='utf-8'));mode='invalid_fallback_control'
 (directory/'rebase_response.md').write_text(response+'\n',encoding='utf-8')
 (directory/'final_director.md').write_text(final+'\n',encoding='utf-8')
 state_data=json.loads((SOURCE/f'chapter-{previous:04d}'/'state_acp.json').read_text(encoding='utf-8'))
 control_data=json.loads((SOURCE/f'chapter-{chapter:04d}'/'director_acp.json').read_text(encoding='utf-8'))
 spec_data=json.loads((SPEC/f'chapter-{chapter:04d}'/'speculative_director_acp.json').read_text(encoding='utf-8'))
 state_wall=float(state_data.get('wall_seconds') or 0);control=float(control_data.get('wall_seconds') or 0);spec_wall=float(spec_data.get('wall_seconds') or 0);rebase=float(data.get('wall_seconds') or 0)
 serial=state_wall+control;critical=max(state_wall,spec_wall)+rebase
 return {'previous_chapter':previous,'chapter':chapter,'mode':mode,'state_wall_seconds':state_wall,'speculative_wall_seconds':spec_wall,'rebase_wall_seconds':rebase,'control_state_plus_director_seconds':round(serial,3),'treatment_critical_seconds':round(critical,3),'speedup_percent':round((1-critical/serial)*100,2),'response_chars':len(response),'final_chars':len(final),'usage':data.get('result',{}).get('usage',{})}


def main()->None:
 OUT.mkdir(parents=True,exist_ok=True);rows=[]
 with ThreadPoolExecutor(max_workers=len(TRANSITIONS)) as ex:
  futs=[ex.submit(one,p,c) for p,c in TRANSITIONS]
  for fut in as_completed(futs):
   row=fut.result();rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
 rows.sort(key=lambda x:x['chapter']);(OUT/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':main()
