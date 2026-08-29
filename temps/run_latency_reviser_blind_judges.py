from __future__ import annotations
import json,random,re,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp');SRC=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'/'runs';BASE=ROOT/'books'/'real-exp-chapter-latency-optimization-20260829-v1';EXP=BASE/'phase-d-routine-reviser-medium';J=BASE/'blind-judges-reviser-medium';RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs');CHAPTERS=[2,13,16];J.mkdir(parents=True,exist_ok=True)
def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def body(t):return clean(t).rsplit('# 正式正文',1)[-1].strip()
def h2(t,prefix):
 ms=list(re.finditer(r'(?m)^##\s+(.+?)\s*$',t))
 for i,m in enumerate(ms):
  if m.group(1).strip().startswith(prefix):
   e=ms[i+1].start() if i+1<len(ms) else len(t);return t[m.end():e].strip()
 return ''
key={}
for ch in CHAPTERS:
 src=SRC/f'chapter-{ch:04d}';tr=EXP/f'chapter-{ch:04d}';d=J/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True);high=body((src/'authority_reviser_response.md').read_text(encoding='utf-8'));med=(tr/'final_medium_body.md').read_text(encoding='utf-8').strip();texts={'high':high,'medium':med};order=['high','medium'];random.Random(2026082920+ch).shuffle(order);key[str(ch)]={'A':order[0],'B':order[1]};rp=(src/'authority_reviser_prompt.md').read_text(encoding='utf-8');tail=h2(rp,'CANON TAIL')
 reader=f'''你是匿名盲读的成熟中文男频长篇审稿人。两版共享同一 Primary Draft 和冻结上游，只是经过两种匿名后处理。不要猜来源，不按篇幅评分。比较清晰、具体、人物欲望与关系、payoff/力量/损失落地、去重复与去流程、章末牵引；事实错误必须指出。允许 MIXED，但不要机械中立。\n严格输出：\nVERDICT: A / B / MIXED\nCONFIDENCE: high / medium / low\nREADABILITY: A / B / TIE\nCHARACTER_AND_RELATIONSHIP: A / B / TIE\nPAYOFF_AND_POWER: A / B / TIE\nANTI_PROCEDURAL_PROSE: A / B / TIE\nCONTINUATION_PULL: A / B / TIE\nHARD_PROBLEM_A: 无 或一句\nHARD_PROBLEM_B: 无 或一句\nREASON: 6—12句。\n\n# 上一章必要尾部\n{tail[-1800:] if tail else '未提供'}\n\n# OPTION A\n{texts[order[0]]}\n\n# OPTION B\n{texts[order[1]]}\n''';(d/'reader_prompt.md').write_text(reader,encoding='utf-8')
 blocks=[]
 for label,prefix in [('FROZEN MISSION','FROZEN CHAPTER MISSION'),('WORLD AUTHORITY','WORLD REALITY AUTHORITY'),('READER RELEASE','READER RELEASE'),('POWER CORE','POWER CORE'),('HUMAN CORE','HUMAN CORE'),('CANON INDEX','CANON INDEX'),('CANON TAIL','CANON TAIL')]:
  v=h2(rp,prefix)
  if v:blocks.append(f'## {label}\n{v}')
 auth='\n\n'.join(blocks)
 authority=f'''你是匿名 TGN Authority / Canon 盲审员。两版共享同一冻结 Mission、Curator 与 Primary Draft。先查主要事件、人物决定、资源得失、力量/身份、Reader Release、未知边界、Direct Result、State Change、Ending，再比较人物、payoff、去重复/去流程。硬冲突不能凭文笔获胜。\n严格输出：\nVERDICT: A / B / MIXED\nCONFIDENCE: high / medium / low\nHARD_VIOLATIONS_A: 无 或逐条短写\nHARD_VIOLATIONS_B: 无 或逐条短写\nMISSION_FIDELITY: A / B / TIE\nCANON_AND_AUTHORITY: A / B / TIE\nHUMAN_AND_RELATIONSHIP: A / B / TIE\nPAYOFF_RULER_RESULT: A / B / TIE\nANTI_REPETITION_PROCESS: A / B / TIE\nREASON: 6—12句。\n\n# FROZEN AUTHORITY\n{auth}\n\n# OPTION A\n{texts[order[0]]}\n\n# OPTION B\n{texts[order[1]]}\n''';(d/'authority_prompt.md').write_text(authority,encoding='utf-8')
(J/'blind_key.json').write_text(json.dumps(key,ensure_ascii=False,indent=2),encoding='utf-8')
def run(pp,out,model):
 cp=subprocess.run(['node',str(RUNNER),str(pp),str(out),model,'high',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
 if cp.returncode:raise RuntimeError(cp.stderr[-2000:])
 j=json.loads(out.read_text(encoding='utf-8'))
 if not j.get('ok'):raise RuntimeError(j.get('error'))
 return j,clean(j.get('text',''))
def one(ch):
 d=J/f'chapter-{ch:04d}';rj,rt=run(d/'reader_prompt.md',d/'reader_acp.json','gpt-5.6-terra');(d/'reader.md').write_text(rt+'\n',encoding='utf-8');aj,at=run(d/'authority_prompt.md',d/'authority_acp.json','gpt-5.6-luna');(d/'authority.md').write_text(at+'\n',encoding='utf-8');return {'chapter':ch,'reader_seconds':rj.get('wall_seconds'),'reader':rt,'authority_seconds':aj.get('wall_seconds'),'authority':at}
rows=[]
with ThreadPoolExecutor(max_workers=3) as ex:
 for f in as_completed([ex.submit(one,ch) for ch in CHAPTERS]):
  r=f.result();rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
rows.sort(key=lambda x:x['chapter']);(J/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
