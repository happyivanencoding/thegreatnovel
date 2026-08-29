from __future__ import annotations
import json,re,subprocess,time,difflib
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r"C:\dev\tgn-story-mvp")
BOOK=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1';SOURCE=BOOK/'runs'
OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'paragraph-manifest-reviser'
RUNNER=Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs");CHAPTERS=(2,3,10,14,19)
OVERRIDE="""# EXPERIMENTAL PARAGRAPH MANIFEST OUTPUT CONTRACT｜替换前文完整正文输出要求

你仍是同一个 Luna-high Full Authority Reviser：完整执行 Preservation First、Frozen Outcome Fidelity、Authority Conflict Sweep、Named Entity Sweep、Value-Preserving Relocation、Reader Release、Human/Power/Public Proof 与 Ending 检查。不要减少审查，也不要把任务改成摘要。

下方 PRIMARY DRAFT 已编号。最终不重复输出所有未改正文，而是输出一个**覆盖每个原段落的完整 Manifest**。每个原段落 P001…PNNN 必须恰好出现一次、严格按编号顺序：

# PARAGRAPH MANIFEST
## P001 KEEP
## P002 REPLACE
<替换后的完整段落；可包含原段落最小改动>
## P003 DELETE
## AFTER P003 INSERT
<新增的完整段落>
...
# CLOSURE CERTIFICATE
MUST_LAND: PASS / FAIL
GLOBAL_FACT_CLOSURE: PASS / FAIL
ENDING_PRESERVED: PASS / FAIL

规则：
- KEEP 不写正文；REPLACE 必须输出完整替换段；DELETE 只用于纯重复/流程载体，不能删人物、关系、Payoff、Public Proof、必要因果或 Ending。
- INSERT 只用于 Authority 明确支持而 Primary 漏掉的必要内容；锚在最近合法段落后。
- 每个原 P 编号必须恰好一条 KEEP/REPLACE/DELETE；不得漏号、重号、乱序。
- 未改部分由代码逐字恢复，因此不要为了文风统一改相邻正确段落。
- 所有新增数字、正式人物/势力/地点/器物名必须逐字来自 Authority；未知仍未知。
- Certificate 有任何 FAIL，说明你无法安全完成；仍输出 Manifest，但运行时会回退完整 Reviser。

不要输出完整正文、Audit、评分、理由、Patch编号或思考过程。"""
ENTITY_SUFFIXES=('军府','商盟','商号','宗','盟','会','台','部','城','关','峡','原','楔','潮髓','潮谱','行潮籍')
SENSITIVE_DELETE=('已经','尚未','仍未','没有','不能','不得','必须','只能','归','持有','交给','收下','到账','突破','升级','死','伤','离开','进入','出发','完成','失败','赢','输','第一次','最后','立刻','终于','想','不想','要','喜欢','舍不得','拒绝','决定','害怕','怕','震惊','沉默')

def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def body(t):return clean(t).rsplit('# 正式正文',1)[-1].strip()
def paras(t):return [p.strip() for p in re.split(r'\n\s*\n',t.strip()) if p.strip()]
def call(pp,op):
 last=''
 for a in range(3):
  cp=subprocess.run(['node',str(RUNNER),str(pp),str(op),'gpt-5.6-luna','high',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if cp.returncode==0 and op.exists():
   try:j=json.loads(op.read_text(encoding='utf-8'))
   except Exception as e:j={};last=str(e)
   if j.get('ok'):return j
   last=str(j.get('error',''))
  else:last=(cp.stderr+'\n'+cp.stdout)[-3000:]
  time.sleep(2+a*2)
 raise RuntimeError(last)
def entities(t):
 out=set()
 for suffix in ENTITY_SUFFIXES:
  for m in re.finditer(re.escape(suffix),t):
   for width in range(len(suffix)+1,min(len(suffix)+6,m.end()+1)):
    st=m.end()-width
    if st>=0:
     x=t[st:m.end()]
     if re.fullmatch(r'[\u4e00-\u9fff]+',x):out.add(x)
 return out
def guard_new(old,new,authority):
 nums=set(re.findall(r'\d+(?:\.\d+)?',new))-set(re.findall(r'\d+(?:\.\d+)?',old))
 if any(n not in authority for n in nums):raise ValueError('unauthorized number '+','.join(nums))
 ents=entities(new)-entities(old)
 if any(e not in authority for e in ents):raise ValueError('unauthorized entity '+','.join(sorted(e for e in ents if e not in authority)))
def parse_manifest(resp,original,authority):
 text=clean(resp);start=re.search(r'(?m)^# PARAGRAPH MANIFEST\s*$',text);cert=re.search(r'(?m)^# CLOSURE CERTIFICATE\s*$',text)
 if not start or not cert or cert.start()<=start.end():raise ValueError('missing manifest/certificate')
 certificate=text[cert.end():].strip()
 for key in ('MUST_LAND','GLOBAL_FACT_CLOSURE','ENDING_PRESERVED'):
  if not re.search(rf'(?m)^{key}:\s*PASS\s*$',certificate):raise ValueError('certificate '+key)
 manifest=text[start.end():cert.start()].strip();heads=list(re.finditer(r'(?m)^##\s+(.+?)\s*$',manifest));records=[]
 for i,m in enumerate(heads):
  end=heads[i+1].start() if i+1<len(heads) else len(manifest);records.append((m.group(1).strip(),manifest[m.end():end].strip()))
 original_parts=paras(original);actions={};inserts={}
 for head,payload in records:
  mm=re.fullmatch(r'P(\d{3})\s+(KEEP|REPLACE|DELETE)',head)
  mi=re.fullmatch(r'AFTER\s+P(\d{3})\s+INSERT',head)
  if mm:
   idx=int(mm.group(1));kind=mm.group(2)
   if idx in actions:raise ValueError('duplicate P')
   actions[idx]=(kind,payload)
  elif mi:
   idx=int(mi.group(1));inserts.setdefault(idx,[]).append(payload)
  else:raise ValueError('invalid heading '+head)
 expected=set(range(1,len(original_parts)+1))
 if set(actions)!=expected:raise ValueError(f'coverage missing={sorted(expected-set(actions))[:8]} extra={sorted(set(actions)-expected)[:8]}')
 result=[];changed=0
 for idx,old in enumerate(original_parts,1):
  kind,payload=actions[idx]
  if kind=='KEEP':
   if payload:raise ValueError('KEEP payload');result.append(old)
  elif kind=='REPLACE':
   if not payload:raise ValueError('empty replacement');guard_new(old,payload,authority);result.append(payload);changed+=1
  else:
   if payload:raise ValueError('DELETE payload')
   if re.search(r'[“”「」『』]',old) or re.search(r'\d',old) or entities(old) or any(x in old for x in SENSITIVE_DELETE):raise ValueError('unsafe delete P%03d'%idx)
   changed+=1
  for ins in inserts.get(idx,[]):
   if not ins:raise ValueError('empty insert');guard_new('',ins,authority);result.append(ins);changed+=1
 final='\n\n'.join(result).strip()
 if paras(final)[-2:]!=original_parts[-2:]:raise ValueError('ending tail changed')
 return final,changed

def one(ch):
 src=SOURCE/f'chapter-{ch:04d}';d=OUT/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True);full=(src/'authority_reviser_prompt.md').read_text(encoding='utf-8');primary=body((src/'primary_response.md').read_text(encoding='utf-8'));parts=paras(primary);numbered='\n\n'.join(f'[P{i:03d}]\n{p}' for i,p in enumerate(parts,1));prompt=full.replace(primary,numbered,1)+'\n\n'+OVERRIDE;authority=full.split('## PRIMARY DRAFT｜唯一待修订正文底稿',1)[0]
 pp=d/'manifest_prompt.md';op=d/'manifest_acp.json';pp.write_text(prompt,encoding='utf-8');data=call(pp,op);resp=clean(data.get('text',''));(d/'manifest_response.md').write_text(resp+'\n',encoding='utf-8');fallback=False;error=''
 try:final,changed=parse_manifest(resp,primary,authority)
 except Exception as e:fallback=True;error=str(e);final=(BOOK/'chapters'/f'chapter-{ch:04d}.md').read_text(encoding='utf-8').strip();changed=0
 (d/'final_body.md').write_text(final+'\n',encoding='utf-8');control=json.loads((src/'authority_reviser_acp.json').read_text(encoding='utf-8'));cw=float(control.get('wall_seconds') or 0);mw=float(data.get('wall_seconds') or 0);route=mw+(cw if fallback else 0)
 return {'chapter':ch,'paragraphs':len(parts),'fallback':fallback,'error':error,'changed_actions':changed,'manifest_wall_seconds':mw,'control_wall_seconds':cw,'effective_route_seconds':round(route,3),'effective_speedup_percent':round((1-route/cw)*100,2),'response_chars':len(resp),'final_chars':len(final),'control_similarity':round(difflib.SequenceMatcher(None,(BOOK/'chapters'/f'chapter-{ch:04d}.md').read_text(encoding='utf-8').strip(),final,autojunk=False).ratio(),5),'usage':data.get('result',{}).get('usage',{})}
def main():
 OUT.mkdir(parents=True,exist_ok=True);rows=[]
 with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as ex:
  fs=[ex.submit(one,ch) for ch in CHAPTERS]
  for f in as_completed(fs):r=f.result();rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
 rows.sort(key=lambda x:x['chapter']);(OUT/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
