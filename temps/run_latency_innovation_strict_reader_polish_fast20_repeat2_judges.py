from __future__ import annotations
import json,random,re,subprocess,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp');BOOK=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1';SOURCE=BOOK/'runs';T=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'strict-reader-polish-fast20-repeat2';OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'blind-strict-reader-polish-fast20-repeat2';RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs');CH=(8,13,16,18)
def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def call(pp,out,model):
 last=''
 for a in range(3):
  cp=subprocess.run(['node',str(RUNNER),str(pp),str(out),model,'high',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if cp.returncode==0 and out.exists():
   j=json.loads(out.read_text(encoding='utf-8'))
   if j.get('ok'):return j
   last=str(j.get('error',''))
  else:last=(cp.stderr+'\n'+cp.stdout)[-2000:]
  time.sleep(2+a*2)
 raise RuntimeError(last)
def auth(ch):return (SOURCE/f'chapter-{ch:04d}'/'authority_reviser_prompt.md').read_text(encoding='utf-8').split('## PRIMARY DRAFT｜唯一待修订正文底稿',1)[0]
OUT.mkdir(parents=True,exist_ok=True);key={}
for ch in CH:
 d=OUT/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True);control=(BOOK/'chapters'/f'chapter-{ch:04d}.md').read_text(encoding='utf-8').strip();polish=(T/f'chapter-{ch:04d}'/'final_body.md').read_text(encoding='utf-8').strip();order=['control','polish'];random.Random(20260829520+ch).shuffle(order);texts={'control':control,'polish':polish};key[str(ch)]={'A':order[0],'B':order[1]}
 reader=f'''你是匿名成熟中文男频正文盲读员。两版只差删除一句可能的重复总结。不要因更短自动判优。判断删除后是否更自然、更信任读者、更快进入动作，或反而损失人物判断、场景压力、节奏重音。\n严格输出：\nVERDICT: A / B / MIXED\nCONFIDENCE: high / medium / low\nNATURALNESS: A / B / TIE\nCHARACTER_VALUE: A / B / TIE\nSCENE_PRESSURE: A / B / TIE\nANTI_AI_EXPLANATION: A / B / TIE\nHARD_PROBLEM_A: 无 或一句\nHARD_PROBLEM_B: 无 或一句\nREASON: 6—10句。\n\n# OPTION A\n{texts[order[0]]}\n\n# OPTION B\n{texts[order[1]]}\n'''
 authority=f'''你是匿名 TGN Authority / Preservation 盲审员。两版只允许纯删除差异。检查删除是否改变事实、人物判断、关系、压力、Mission、State、Canon、Payoff或Ending；事实等价时再判断 Result Stop / Trust Reader。\n严格输出：\nVERDICT: A / B / MIXED\nCONFIDENCE: high / medium / low\nHARD_VIOLATIONS_A: 无 或一句\nHARD_VIOLATIONS_B: 无 或一句\nFACT_EQUIVALENCE: YES / NO\nHUMAN_SCENE_VALUE: A / B / TIE\nRESULT_STOP: A / B / TIE\nREASON: 6—10句。\n\n# FROZEN AUTHORITY\n{auth(ch)}\n\n# OPTION A\n{texts[order[0]]}\n\n# OPTION B\n{texts[order[1]]}\n'''
 (d/'reader_prompt.md').write_text(reader,encoding='utf-8');(d/'authority_prompt.md').write_text(authority,encoding='utf-8')
(OUT/'blind_key.json').write_text(json.dumps(key,ensure_ascii=False,indent=2),encoding='utf-8')
def one(ch):
 d=OUT/f'chapter-{ch:04d}';r=call(d/'reader_prompt.md',d/'reader_acp.json','gpt-5.6-terra');rt=clean(r['text']);(d/'reader.md').write_text(rt+'\n',encoding='utf-8');a=call(d/'authority_prompt.md',d/'authority_acp.json','gpt-5.6-luna');at=clean(a['text']);(d/'authority.md').write_text(at+'\n',encoding='utf-8');return {'chapter':ch,'reader':rt,'authority':at,'reader_wall':r['wall_seconds'],'authority_wall':a['wall_seconds']}
rows=[]
with ThreadPoolExecutor(max_workers=3) as ex:
 for f in as_completed([ex.submit(one,ch) for ch in CH]):
  x=f.result();rows.append(x);print(json.dumps({'chapter':x['chapter'],'reader':x['reader'].splitlines()[:2],'authority':x['authority'].splitlines()[:3]},ensure_ascii=False),flush=True)
rows.sort(key=lambda x:x['chapter']);(OUT/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
