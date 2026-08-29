from __future__ import annotations
import hashlib,json,random,re,subprocess,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp')
SRC=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'/'runs'
BASE=ROOT/'books'/'real-exp-chapter-latency-optimization-20260829-v1'
EXP=BASE/'phase-h-curator-medium-contract-fixed'
J=BASE/'blind-judges-curator-medium-contract-fixed'
RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')
CHAPTERS=[2,3,10,13,14,16,19]
J.mkdir(parents=True,exist_ok=True)
def clean(t:str)->str:return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def body(t:str)->str:return clean(t).rsplit('# 正式正文',1)[-1].strip()
def h2(text:str,prefix:str)->str:
 ms=list(re.finditer(r'(?m)^##\s+(.+?)\s*$',text))
 for i,m in enumerate(ms):
  if m.group(1).strip().startswith(prefix):
   e=ms[i+1].start() if i+1<len(ms) else len(text);return text[m.end():e].strip()
 return ''
def call(pp:Path,out:Path,model:str,effort:str)->dict:
 last=''
 for attempt in range(3):
  cp=subprocess.run(['node',str(RUNNER),str(pp),str(out),model,effort,str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if cp.returncode==0 and out.exists():
   try:j=json.loads(out.read_text(encoding='utf-8'))
   except Exception as e:j={};last=str(e)
   if j.get('ok'):return j
   last=str(j.get('error',''))
  else:last=(cp.stderr+'\n'+cp.stdout)[-3000:]
  time.sleep(2+2*attempt)
 raise RuntimeError(last)
key={}
for ch in CHAPTERS:
 src=SRC/f'chapter-{ch:04d}'; tr=EXP/f'chapter-{ch:04d}'; d=J/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True)
 control=body((src/'authority_reviser_response.md').read_text(encoding='utf-8'))
 treatment=(tr/'final_treatment_body.md').read_text(encoding='utf-8').strip()
 order=['control','treatment'];random.Random(202608291500+ch).shuffle(order);texts={'control':control,'treatment':treatment}
 key[str(ch)]={'A':order[0],'B':order[1],'control_sha256':hashlib.sha256(control.encode()).hexdigest(),'treatment_sha256':hashlib.sha256(treatment.encode()).hexdigest()}
 rp=(src/'authority_reviser_prompt.md').read_text(encoding='utf-8')
 tail=h2(rp,'CANON TAIL')
 reader=f'''你是匿名盲读的中文男频长篇小说读者审稿人。下面两版来自同一个冻结剧情合同，但你不知道来源。只评最终阅读体验，不猜模型、不因篇幅长短偏爱任何一版。\n\n目标是顶级商业男频长篇：清楚、具体、推进快、人物有欲望与声音、能力/胜负/收益落地、高潮有重量，同时避免程序化实施、后台策划词、重复证明与 AI 式解释。\n\n逐项比较：动作/位置/因果与当前目标是否易懂；主角是否主动争取具体欲望而非协调员；配角是否有独立利益与声音；力量、获得、损失、身份和关系变化是否落地；是否重复、流程化、术语化或高潮后解释过多；章末是否自然推动下一章。若各有明显优劣可 MIXED，不要强行中立。\n\n严格输出：\nVERDICT: A / B / MIXED\nCONFIDENCE: high / medium / low\nREADABILITY: A / B / TIE\nCHARACTER_AND_RELATIONSHIP: A / B / TIE\nPAYOFF_AND_POWER: A / B / TIE\nANTI_PROCEDURAL_PROSE: A / B / TIE\nCONTINUATION_PULL: A / B / TIE\nHARD_PROBLEM_A: 无 或一句\nHARD_PROBLEM_B: 无 或一句\nREASON: 6—12句，引用具体事件或表达特征，不长引原文。\n\n# 上一章必要尾部\n{tail[-1800:] if tail else '未提供；只比较两版内部阅读质量。'}\n\n# OPTION A\n{texts[order[0]]}\n\n# OPTION B\n{texts[order[1]]}\n'''
 blocks=[]
 for label,prefix in [('FROZEN MISSION','FROZEN CHAPTER MISSION'),('WORLD AUTHORITY','WORLD REALITY AUTHORITY'),('READER RELEASE','READER RELEASE'),('POWER CORE','POWER CORE'),('HUMAN CORE','HUMAN CORE'),('CANON INDEX','CANON INDEX'),('CANON TAIL','CANON TAIL')]:
  val=h2(rp,prefix)
  if val:blocks.append(f'## {label}\n{val}')
 authority='\n\n'.join(blocks)
 auth=f'''你是匿名的 TGN Authority / Canon 盲审员。两版正文来自同一冻结上游。你不知道来源，也不能按篇幅或“改动更多”评分。\n\n先检查主要事件顺序、人物决定、胜负、资源得失、伤势、身份/力量结果、知识边界、Reader Release、Direct Result、State Change、Ending；再比较人物欲望、关系牵引、Public Proof/力量尺、收益代价，以及重复证明、程序化实施、协调员主角、后台抽象词或未授权事实。硬冲突不能凭文笔抵消。两版都合法时，选择更完整兑现 Mission、同时更像成熟男频正文的一版。\n\n严格输出：\nVERDICT: A / B / MIXED\nCONFIDENCE: high / medium / low\nHARD_VIOLATIONS_A: 无 或逐条短写\nHARD_VIOLATIONS_B: 无 或逐条短写\nMISSION_FIDELITY: A / B / TIE\nCANON_AND_AUTHORITY: A / B / TIE\nHUMAN_AND_RELATIONSHIP: A / B / TIE\nPAYOFF_RULER_RESULT: A / B / TIE\nANTI_REPETITION_PROCESS: A / B / TIE\nREASON: 6—12句，引用具体事件层证据，不长引正文。\n\n# FROZEN AUTHORITY\n{authority}\n\n# OPTION A\n{texts[order[0]]}\n\n# OPTION B\n{texts[order[1]]}\n'''
 (d/'reader_prompt.md').write_text(reader,encoding='utf-8');(d/'authority_prompt.md').write_text(auth,encoding='utf-8')
(J/'blind_key.json').write_text(json.dumps(key,ensure_ascii=False,indent=2),encoding='utf-8')
def one(ch:int):
 d=J/f'chapter-{ch:04d}'
 r=call(d/'reader_prompt.md',d/'reader_acp.json','gpt-5.6-terra','high');rt=clean(r.get('text',''));(d/'reader.md').write_text(rt+'\n',encoding='utf-8')
 a=call(d/'authority_prompt.md',d/'authority_acp.json','gpt-5.6-luna','high');at=clean(a.get('text',''));(d/'authority.md').write_text(at+'\n',encoding='utf-8')
 return {'chapter':ch,'reader_seconds':r.get('wall_seconds'),'authority_seconds':a.get('wall_seconds'),'reader':rt,'authority':at}
rows=[]
with ThreadPoolExecutor(max_workers=7) as ex:
 for f in as_completed([ex.submit(one,ch) for ch in CHAPTERS]):
  x=f.result();rows.append(x);print(json.dumps({'chapter':x['chapter'],'reader':x['reader'].splitlines()[:2],'authority':x['authority'].splitlines()[:2]},ensure_ascii=False),flush=True)
rows.sort(key=lambda x:x['chapter']);(J/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
