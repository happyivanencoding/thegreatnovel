from __future__ import annotations
import json,re,subprocess,time,difflib
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r"C:\dev\tgn-story-mvp")
BOOK=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1';SOURCE=BOOK/'runs'
PRIMARY_STATE=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'speculative-state-from-primary-all20'
OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'full-reviser-fact-delta'
RUNNER=Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs");CHAPTERS=(1,2,3,6,10,14,19)
SUPPLEMENT="""# EXPERIMENTAL FACT DELTA OUTPUT CONTRACT｜替换前文单标题输出要求

本轮仍执行完全相同的 Full Luna-high Authority Revision；不要缩短审查、不要改成 Patch、不要减少 Preservation First / Authority Conflict Sweep / Value-Preserving Relocation。唯一新增的是：在完整最终正文后，报告这次修订是否改变了下一章 State Extraction 必须知道的事实。

最终严格输出两个一级标题：
# 正式正文
<完整最终正文>
# FACT DELTA
若 Primary Draft 与最终正文在下列事实维度完全相同，只写：NONE
若有变化，逐条写：
- DIMENSION: event / actor / object / result / state / resource / ownership / time / power / relationship / knowledge / open_promise / ending
  BEFORE: <Primary 中的事实；无则 NONE>
  AFTER: <最终正文事实；无则 NONE>

FACT DELTA 只报告客观语义变化：事件发生与否、行动者/对象、胜负/结果、状态、资源、持有人、时间、力量位置/机制、关系阶段、谁知道什么、未兑现承诺、Ending。纯措辞、删重复、压流程、句序、节奏、感官、比喻或不改变事实强度的更清楚表达不报告。不得为了让 FACT DELTA 更简单而少修正文，也不得把审计文字写进小说。
"""

def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def parse_output(t):
 t=clean(t);m=re.search(r'(?m)^# FACT DELTA\s*$',t)
 if not m:raise ValueError('missing FACT DELTA')
 before=t[:m.start()].strip();fact=t[m.end():].strip();body=before.rsplit('# 正式正文',1)[-1].strip();return body,fact
def call(pp,op,model='gpt-5.6-luna',effort='high'):
 last=''
 for a in range(3):
  cp=subprocess.run(['node',str(RUNNER),str(pp),str(op),model,effort,str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if cp.returncode==0 and op.exists():
   try:j=json.loads(op.read_text(encoding='utf-8'))
   except Exception as e:j={};last=str(e)
   if j.get('ok'):return j
   last=str(j.get('error',''))
  else:last=(cp.stderr+'\n'+cp.stdout)[-3000:]
  time.sleep(2+a*2)
 raise RuntimeError(last)
def one(ch):
 src=SOURCE/f'chapter-{ch:04d}';d=OUT/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True)
 prompt=(src/'authority_reviser_prompt.md').read_text(encoding='utf-8')+'\n\n'+SUPPLEMENT;pp=d/'fact_delta_reviser_prompt.md';op=d/'fact_delta_reviser_acp.json';pp.write_text(prompt,encoding='utf-8');data=call(pp,op);raw=clean(data.get('text',''));body,fact=parse_output(raw);(d/'response.md').write_text(raw+'\n',encoding='utf-8');(d/'final_body.md').write_text(body+'\n',encoding='utf-8');(d/'fact_delta.md').write_text(fact+'\n',encoding='utf-8')
 control=json.loads((src/'authority_reviser_acp.json').read_text(encoding='utf-8'));state=json.loads((src/'state_acp.json').read_text(encoding='utf-8'));primary_state=json.loads((PRIMARY_STATE/f'chapter-{ch:04d}'/'speculative_state_acp.json').read_text(encoding='utf-8')) if (PRIMARY_STATE/f'chapter-{ch:04d}'/'speculative_state_acp.json').exists() else {'wall_seconds':0};rw=float(data.get('wall_seconds') or 0);cw=float(control.get('wall_seconds') or 0);sw=float(state.get('wall_seconds') or 0);psw=float(primary_state.get('wall_seconds') or 0);none=fact.strip()=='NONE';route=max(rw,psw)+(0 if none else sw);current=cw+sw
 primary=clean((src/'primary_response.md').read_text(encoding='utf-8')).rsplit('# 正式正文',1)[-1].strip();control_body=(BOOK/'chapters'/f'chapter-{ch:04d}.md').read_text(encoding='utf-8').strip()
 return {'chapter':ch,'fact_delta_none':none,'fact_delta':fact,'reviser_wall_seconds':rw,'control_reviser_wall_seconds':cw,'control_state_wall_seconds':sw,'primary_state_wall_seconds':psw,'current_reviser_plus_state_seconds':round(current,3),'fact_delta_route_seconds':round(route,3),'route_speedup_percent':round((1-route/current)*100,2),'primary_treatment_similarity':round(difflib.SequenceMatcher(None,primary,body,autojunk=False).ratio(),5),'control_treatment_similarity':round(difflib.SequenceMatcher(None,control_body,body,autojunk=False).ratio(),5),'final_chars':len(body),'usage':data.get('result',{}).get('usage',{})}
def main():
 OUT.mkdir(parents=True,exist_ok=True);rows=[]
 with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as ex:
  fs=[ex.submit(one,ch) for ch in CHAPTERS]
  for f in as_completed(fs):r=f.result();rows.append(r);print(json.dumps({k:r[k] for k in ('chapter','fact_delta_none','reviser_wall_seconds','route_speedup_percent','primary_treatment_similarity')},ensure_ascii=False),flush=True)
 rows.sort(key=lambda x:x['chapter']);(OUT/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
