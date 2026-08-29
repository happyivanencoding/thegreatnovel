from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT=Path(r"C:\dev\tgn-story-mvp")
BOOK=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'
SOURCE=BOOK/'runs'
OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'ten-chapter-attention-kernel'
RUNNER=Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS=(2,3,10,14,19)
RANGES=((1,10),(11,20))

sys.path.insert(0,str(ROOT/'src'))
from story_mvp.hybrid_runtime import extract_unresolved_fact_boundary,strip_legacy_prose_controls  # noqa:E402
from story_mvp.scene_skills import render_selected_revision_watches,strip_scene_skill_selection  # noqa:E402

KERNEL_TEMPLATE="""你是 TGN 的 Ten-Chapter Attention Kernel Compiler，使用 GPT-5.6 Luna high。你只把十章内反复不变的 Book/Human/Prose/Scene Skill Authority 编译一次，供每章正式 Luna-high Curator 使用；不生成正文、不替代 Director、不决定当前 Canon，也不创造新事实。

规则：
- 只保留这十章会真实用到、能改变人物选择、关系、World/Power体验、Payoff、表达方式或重复风险的稳定材料。
- 人物必须保留具体欲望、competing motives、行为签名、关系触发；不要压成“负责、克制、成熟”。
- 保护男频价值：主角主动性、具体占有/收益、核心幻想、Public Proof三路、人物欲望、关系换位、惊喜、Named Opportunity价值。
- Prose 只编译高杠杆差异：叙述距离、人物声音、场景节奏、最常见AI/流程退化；不写通用口号。
- Scene Skill 只能从原 Catalog 选 ID，不重写技能，不要求每章用满。
- Future 10 只是计划，不是 Canon；不得把未来获得、出场、胜负或关系变化写成已发生。
- 每章映射只写静态可能相关项；正式 Curator 仍必须服从当章 Frozen Mission / Canon / Reader Release，不能因 Kernel 改行动者、对象、结果或 Ending。

严格输出：
# RANGE INVARIANTS
## Book / Fantasy
最多12条。
## Human / Relationships
最多12条。
## Prose / Anti-Regression
最多10条。
## Global Unknown / Do Not Infer
最多8条。

# CHAPTER STATIC MAP
对范围内每章逐章输出：
## 第N章
Book/Human Focus: 2—5条；无则 NONE
Prose Focus: 1—3条；无则 NONE
Scene Skill Shortlist: 1—5个原始 skill_id，用逗号分隔；无则 none
Do Not Infer: 0—3条；无则 NONE

不要输出 Audit、评分、正文、当前状态或内部推理。"""


def clean(text:str)->str:return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$","",text).strip()
def body(text:str)->str:return clean(text).rsplit('# 正式正文',1)[-1].strip()

def call(pp:Path,op:Path,model:str='gpt-5.6-luna',effort:str='high')->dict:
 last=''
 for attempt in range(3):
  proc=subprocess.run(['node',str(RUNNER),str(pp),str(op),model,effort,str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if proc.returncode==0 and op.exists():
   try:data=json.loads(op.read_text(encoding='utf-8'))
   except Exception as e:data={};last=str(e)
   if data.get('ok'):return data
   last=str(data.get('error',''))
  else:last=(proc.stderr+'\n'+proc.stdout)[-3000:]
  time.sleep(2+attempt*2)
 raise RuntimeError(last)

def h2_blocks(text:str)->list[tuple[str,str,int,int]]:
 starts=list(re.finditer(r'(?m)^##\s+(.+?)\s*$',text));out=[]
 for i,m in enumerate(starts):
  end=starts[i+1].start() if i+1<len(starts) else len(text)
  out.append((m.group(1).strip(),text[m.end():end].strip(),m.start(),end))
 return out

def get_h2(text:str,prefix:str)->str:
 for h,b,_,_ in h2_blocks(text):
  if h.startswith(prefix):return b
 return ''

def replace_h2(text:str,prefix:str,new_heading:str,new_body:str)->str:
 for h,b,start,end in h2_blocks(text):
  if h.startswith(prefix):
   return text[:start]+f'## {new_heading}\n\n{new_body}\n\n'+text[end:].lstrip()
 raise RuntimeError('missing h2 '+prefix)

def exact_between(text:str,start:str,end:str|None)->str:
 i=text.index(start)+len(start);j=text.index(end,i) if end else len(text);return text[i:j].strip()

def stable_inputs(representative:int)->dict[str,str]:
 p=(SOURCE/f'chapter-{representative:04d}'/'curator_prompt.md').read_text(encoding='utf-8')
 return {
  'human':exact_between(p,'## FROZEN HUMAN CORE——稳定人格权威，只用于本章相关选择与私人牵引','## 压缩 Growth Genome（本章相关固定小节）'),
  'genome':exact_between(p,'## 压缩 Growth Genome（本章相关固定小节）','## BOOK CONTRACT——本章确定性预取'),
  'book':exact_between(p,'## BOOK CONTRACT——本章确定性预取','## 本章成长收益短投影（规划提示，不是正文措辞）'),
  'prose':exact_between(p,'## PROSE PROFILE','## SCENE SKILL CATALOG——只用于选择 1 个 Primary 与可选 1 个 Secondary'),
  'catalog':exact_between(p,'## SCENE SKILL CATALOG——只用于选择 1 个 Primary 与可选 1 个 Secondary','## OPTIONAL INSPIRATION'),
 }

def plan_block(ch:int)->str:
 p=(SOURCE/f'chapter-{ch:04d}'/'director_prompt.md').read_text(encoding='utf-8')
 block=get_h2(p,f'第{ch}章')
 return f'## 第{ch}章\n\n{block}' if block else f'## 第{ch}章\n\n（历史 Prompt 未暴露独立条目。）'

def compile_kernel(start:int,end:int)->dict:
 directory=OUT/f'kernel-{start:04d}-{end:04d}';directory.mkdir(parents=True,exist_ok=True)
 inputs=stable_inputs(start if start==1 else 14)
 plans='\n\n'.join(plan_block(ch) for ch in range(start,end+1))
 prompt='\n\n'.join((KERNEL_TEMPLATE,'# FROZEN BOOK/HUMAN/PROSE INPUT', '## HUMAN CORE\n'+inputs['human'],'## GROWTH GENOME\n'+inputs['genome'],'## BOOK CONTRACT\n'+inputs['book'],'## PROSE PROFILE\n'+inputs['prose'],'## SCENE SKILL CATALOG\n'+inputs['catalog'],'# FUTURE 10 PLAN INPUT\n'+plans))
 pp=directory/'kernel_prompt.md';op=directory/'kernel_acp.json';pp.write_text(prompt,encoding='utf-8');data=call(pp,op);kernel=clean(data.get('text',''));(directory/'kernel.md').write_text(kernel+'\n',encoding='utf-8')
 return {'start':start,'end':end,'wall_seconds':float(data.get('wall_seconds') or 0),'prompt_chars':len(prompt),'kernel_chars':len(kernel),'usage':data.get('result',{}).get('usage',{})}

def kernel_for(ch:int)->tuple[str,float]:
 start,end=(1,10) if ch<=10 else (11,20);directory=OUT/f'kernel-{start:04d}-{end:04d}'
 kernel=(directory/'kernel.md').read_text(encoding='utf-8').strip();data=json.loads((directory/'kernel_acp.json').read_text(encoding='utf-8'))
 invariants=kernel.split('# CHAPTER STATIC MAP',1)[0].strip()
 chapter=''
 blocks=h2_blocks(kernel)
 for h,b,_,_ in blocks:
  if h.startswith(f'第{ch}章'):chapter=f'## {h}\n\n{b}';break
 return invariants+'\n\n# CURRENT CHAPTER STATIC MAP\n'+(chapter or 'NONE'),float(data.get('wall_seconds') or 0)

def skill_shortlist(kernel:str,catalog:str)->str:
 m=re.search(r'(?mi)^Scene Skill Shortlist:\s*(.*?)\s*$',kernel);ids=[]
 if m:
  ids=[x.strip() for x in re.split(r'[,，]',m.group(1)) if x.strip() and x.strip().lower()!='none']
 lines=[]
 for line in catalog.splitlines():
  if not line.strip().startswith('- '):continue
  sid=line.strip()[2:].split(':',1)[0].strip()
  if sid in ids:lines.append(line.strip())
 return '\n'.join(lines) or '（Kernel 未选择 Scene Skill；正式 Curator 可写 none。）'

def replace_once(text:str,old:str,new:str,label:str)->str:
 if text.count(old)!=1:raise RuntimeError(f'{label}: count={text.count(old)}')
 return text.replace(old,new,1)

def replace_revision_watch(prompt:str,old_curator:str,new_curator:str)->str:
 old=render_selected_revision_watches(old_curator);new=render_selected_revision_watches(new_curator);heading='## ACTIVE SCENE REVISION WATCH｜只在明确失败时局部使用';primary='## PRIMARY DRAFT｜唯一待修订正文底稿'
 if old:
  block=f'{heading}\n\n{old}'
  if new:return prompt.replace(block,f'{heading}\n\n{new}',1)
  return prompt.replace(block+'\n\n','',1)
 if new:return prompt.replace(primary,f'{heading}\n\n{new}\n\n{primary}',1)
 return prompt

def run_chapter(ch:int)->dict:
 source=SOURCE/f'chapter-{ch:04d}';directory=OUT/f'chapter-{ch:04d}';directory.mkdir(parents=True,exist_ok=True)
 full=(source/'curator_prompt.md').read_text(encoding='utf-8');kernel,kwall=kernel_for(ch);stable=stable_inputs(1 if ch<=10 else 14);short=skill_shortlist(kernel,stable['catalog'])
 prompt=full
 prompt=replace_h2(prompt,'FROZEN HUMAN CORE','STATIC ATTENTION KERNEL——Human/Book/Prose',kernel)
 prompt=replace_h2(prompt,'BOOK CONTRACT——本章确定性预取','BOOK CONTRACT——由十章 Kernel 编译','（见 STATIC ATTENTION KERNEL；当前 Mission/Canon 仍为动态最高相关输入。）')
 prompt=replace_h2(prompt,'PROSE PROFILE','PROSE PROFILE——由十章 Kernel 编译','（见 STATIC ATTENTION KERNEL。）')
 prompt=replace_h2(prompt,'SCENE SKILL CATALOG——只用于选择 1 个 Primary 与可选 1 个 Secondary','SCENE SKILL SHORTLIST——十章 Kernel 当前章候选',short)
 pp=directory/'kernel_curator_prompt.md';op=directory/'kernel_curator_acp.json';pp.write_text(prompt,encoding='utf-8');cdata=call(pp,op);curator=clean(cdata.get('text',''));(directory/'kernel_curator_response.md').write_text(curator+'\n',encoding='utf-8')
 old_curator=clean((source/'curator_response.md').read_text(encoding='utf-8'));old_visible=strip_legacy_prose_controls(strip_scene_skill_selection(old_curator));new_visible=strip_legacy_prose_controls(strip_scene_skill_selection(curator));old_un=extract_unresolved_fact_boundary(old_curator);new_un=extract_unresolved_fact_boundary(curator)
 primary_prompt=(source/'primary_prompt.md').read_text(encoding='utf-8');primary_prompt=replace_once(primary_prompt,old_visible,new_visible,f'ch{ch} curator')
 if old_un!=new_un:primary_prompt=replace_once(primary_prompt,old_un or '（Curator 未投影出额外未解事实；仍服从最高事实边界。）',new_un or '（Curator 未投影出额外未解事实；仍服从最高事实边界。）',f'ch{ch} unresolved')
 ppp=directory/'primary_prompt.md';pop=directory/'primary_acp.json';ppp.write_text(primary_prompt,encoding='utf-8');pdata=call(ppp,pop,'gpt-5.6-terra','high');pt=clean(pdata.get('text',''));pb=body(pt);(directory/'primary_response.md').write_text(pt+'\n',encoding='utf-8');(directory/'primary_body.md').write_text(pb+'\n',encoding='utf-8')
 old_primary=body((source/'primary_response.md').read_text(encoding='utf-8'));rp=(source/'authority_reviser_prompt.md').read_text(encoding='utf-8');rp=replace_once(rp,old_curator,curator,f'ch{ch} reviser curator');rp=replace_once(rp,old_primary,pb,f'ch{ch} reviser primary');rp=replace_revision_watch(rp,old_curator,curator);rpp=directory/'reviser_prompt.md';rop=directory/'reviser_acp.json';rpp.write_text(rp,encoding='utf-8');rdata=call(rpp,rop);rt=clean(rdata.get('text',''));fb=body(rt);(directory/'reviser_response.md').write_text(rt+'\n',encoding='utf-8');(directory/'final_body.md').write_text(fb+'\n',encoding='utf-8')
 control={s:json.loads((source/f'{s}_acp.json').read_text(encoding='utf-8')) for s in ('curator','primary','authority_reviser')};ct=sum(float(x.get('wall_seconds') or 0) for x in control.values());tt=float(cdata.get('wall_seconds') or 0)+float(pdata.get('wall_seconds') or 0)+float(rdata.get('wall_seconds') or 0);amortized=tt+kwall/10
 return {'chapter':ch,'kernel_wall_seconds':kwall,'kernel_amortized_seconds':round(kwall/10,3),'control_c_p_r_seconds':round(ct,3),'treatment_c_p_r_seconds':round(tt,3),'treatment_amortized_seconds':round(amortized,3),'critical_speedup_percent':round((1-tt/ct)*100,2),'amortized_speedup_percent':round((1-amortized/ct)*100,2),'curator_prompt_chars':len(prompt),'control_curator_prompt_chars':len(full),'curator_wall_seconds':float(cdata.get('wall_seconds') or 0),'primary_wall_seconds':float(pdata.get('wall_seconds') or 0),'reviser_wall_seconds':float(rdata.get('wall_seconds') or 0),'final_chars':len(fb)}

def main()->None:
 OUT.mkdir(parents=True,exist_ok=True)
 with ThreadPoolExecutor(max_workers=2) as ex: kernels=list(ex.map(lambda r:compile_kernel(*r),RANGES))
 (OUT/'kernel_summary.json').write_text(json.dumps(kernels,ensure_ascii=False,indent=2),encoding='utf-8')
 rows=[]
 with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as ex:
  futs=[ex.submit(run_chapter,ch) for ch in CHAPTERS]
  for fut in as_completed(futs):
   row=fut.result();rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
 rows.sort(key=lambda x:x['chapter']);(OUT/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
