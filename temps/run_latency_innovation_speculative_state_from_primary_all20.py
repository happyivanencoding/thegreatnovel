from __future__ import annotations
import json,re,subprocess,time,difflib
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r"C:\dev\tgn-story-mvp")
BOOK=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1';SOURCE=BOOK/'runs'
OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'speculative-state-from-primary-all20'
RUNNER=Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs");CHAPTERS=tuple(range(1,21))
SENSITIVE=(
 '取得','获得','失去','放弃','归','交给','交回','交付','收下','推回','拿走','持有','所有权','使用权','原件','副本','登记','签下','到账','付款','尾款','赔付','预付款','矿利','潮铢',
 '低潮','地潮','下一次','之前','之后','当场','已经','尚未','仍未','开始','即将','完成','中止','进入','离开','抵达','撤离','死亡','受伤','咳血',
 '入潮','成炉','照域','镇海','分身','回潮楔','锁潮','改向','释放','行潮籍','升级','突破','战绩','身份','资格','入口',
 '不能','不得','必须','只能','不再','仍能','没有','并非','不是','未知','未明','真相','根源','他','她'
)
ENTITY_SUFFIXES=('军府','商盟','商号','宗','盟','会','台','部','城','关','峡','原','楔','潮髓','潮谱','行潮籍')

def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def body(t):return clean(t).rsplit('# 正式正文',1)[-1].strip()
def call(pp,op):
 last=''
 for a in range(3):
  cp=subprocess.run(['node',str(RUNNER),str(pp),str(op),'gpt-5.6-luna','low',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if cp.returncode==0 and op.exists():
   try:j=json.loads(op.read_text(encoding='utf-8'))
   except Exception as e:j={};last=str(e)
   if j.get('ok'):return j
   last=str(j.get('error',''))
  else:last=(cp.stderr+'\n'+cp.stdout)[-3000:]
  time.sleep(2+a*2)
 raise RuntimeError(last)
def paragraphs(t):return [p.strip() for p in re.split(r'\n\s*\n',t.strip()) if p.strip()]
def changed_spans(a,b):
 aa=paragraphs(a);bb=paragraphs(b);sm=difflib.SequenceMatcher(None,aa,bb,autojunk=False);out=[]
 for tag,i1,i2,j1,j2 in sm.get_opcodes():
  if tag!='equal':out.append({'tag':tag,'old':'\n\n'.join(aa[i1:i2]),'new':'\n\n'.join(bb[j1:j2])})
 return out
def entity_tokens(t):
 result=set()
 for suffix in ENTITY_SUFFIXES:
  for m in re.finditer(re.escape(suffix),t):
   for width in range(len(suffix)+1,min(len(suffix)+5,m.end()+1)):
    start=m.end()-width
    if start>=0:
     x=t[start:m.end()]
     if re.fullmatch(r'[\u4e00-\u9fff]+',x):result.add(x)
 return result
def conservative_gate(primary,final):
 spans=changed_spans(primary,final);reasons=[]
 if not spans:return True,['exact']
 ratio=sum(max(len(s['old']),len(s['new'])) for s in spans)/max(1,len(primary))
 if ratio>0.16:reasons.append(f'changed_ratio={ratio:.3f}')
 if paragraphs(primary)[-2:]!=paragraphs(final)[-2:]:reasons.append('ending_tail_changed')
 for index,s in enumerate(spans,1):
  combined=s['old']+'\n'+s['new']
  nums=set(re.findall(r'\d+(?:\.\d+)?',s['old']))^set(re.findall(r'\d+(?:\.\d+)?',s['new']))
  if nums:reasons.append(f'span{index}:numbers')
  if entity_tokens(s['old'])!=entity_tokens(s['new']):reasons.append(f'span{index}:entities')
  hits=sorted({x for x in SENSITIVE if x in combined})
  if hits:reasons.append(f'span{index}:sensitive={"/".join(hits[:8])}')
 return not reasons,reasons
def state_block(prompt):
 marker='## 本次新正式章节正文（State Delta 的最高事实来源）'
 if marker not in prompt:raise RuntimeError('state body marker missing')
 return prompt.split(marker,1)[1].strip()
def parse_state(text):
 headings=('Proposed Active Scene State','Proposed Persistent Canon','Proposed Chapter Summary','Proposed Open Promises')
 result={}
 for i,h in enumerate(headings):
  m=re.search(rf'(?m)^# {re.escape(h)}\s*$',text)
  if not m:result[h]='';continue
  ends=[x.start() for x in re.finditer(r'(?m)^# ',text[m.end():])]
  end=m.end()+(ends[0] if ends else len(text)-m.end())
  result[h]=re.sub(r'\s+',' ',text[m.end():end].strip())
 return result
def one(ch):
 src=SOURCE/f'chapter-{ch:04d}';d=OUT/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True)
 primary=body((src/'primary_response.md').read_text(encoding='utf-8'));final=(BOOK/'chapters'/f'chapter-{ch:04d}.md').read_text(encoding='utf-8').strip();prompt=(src/'state_prompt.md').read_text(encoding='utf-8');control_body=state_block(prompt)
 if prompt.count(control_body)!=1:raise RuntimeError(f'ch{ch}: control body count')
 speculative_prompt=prompt.replace(control_body,primary,1);pp=d/'speculative_state_prompt.md';op=d/'speculative_state_acp.json';pp.write_text(speculative_prompt,encoding='utf-8');data=call(pp,op);resp=clean(data.get('text',''));(d/'speculative_state_response.md').write_text(resp+'\n',encoding='utf-8')
 control_data=json.loads((src/'state_acp.json').read_text(encoding='utf-8'));control_resp=clean(control_data.get('text',''));gate,reasons=conservative_gate(primary,final);sp=parse_state(resp);cp=parse_state(control_resp);equal={k:sp[k]==cp[k] for k in sp};all_equal=all(equal.values())
 rw=float(json.loads((src/'authority_reviser_acp.json').read_text(encoding='utf-8')).get('wall_seconds') or 0);sw=float(control_data.get('wall_seconds') or 0);pw=float(data.get('wall_seconds') or 0);current=rw+sw;route=max(rw,pw)+(0 if gate else sw)
 return {'chapter':ch,'gate_accept':gate,'gate_reasons':reasons,'state_all_fields_exact':all_equal,'state_field_exact':equal,'reviser_wall_seconds':rw,'control_state_wall_seconds':sw,'speculative_state_wall_seconds':pw,'control_reviser_plus_state_seconds':round(current,3),'route_critical_seconds':round(route,3),'route_speedup_percent':round((1-route/current)*100,2),'primary_final_similarity':round(difflib.SequenceMatcher(None,primary,final,autojunk=False).ratio(),5),'changed_spans':changed_spans(primary,final),'speculative_response_chars':len(resp)}
def main():
 OUT.mkdir(parents=True,exist_ok=True);rows=[]
 with ThreadPoolExecutor(max_workers=8) as ex:
  fs=[ex.submit(one,ch) for ch in CHAPTERS]
  for f in as_completed(fs):r=f.result();rows.append(r);print(json.dumps({k:r[k] for k in ('chapter','gate_accept','state_all_fields_exact','route_speedup_percent','primary_final_similarity')},ensure_ascii=False),flush=True)
 rows.sort(key=lambda x:x['chapter']);(OUT/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
