from __future__ import annotations
import json, random, re, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp')
BOOK=ROOT/'books'/'real-exp-fast-world-20ch-20260828-v1'
SOURCE=BOOK/'runs'/'chapter-0003'
TREAT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'post-authority-reader-polish'/'chapter-0003'
OUT=ROOT/'books'/'real-exp-chapter-latency-innovation-20260829-v1'/'blind-post-authority-reader-polish'/'chapter-0003'
RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs');OUT.mkdir(parents=True,exist_ok=True)
control=(BOOK/'chapters'/'chapter-0003.md').read_text(encoding='utf-8').strip(); treatment=(TREAT/'final_body.md').read_text(encoding='utf-8').strip()
order=['control','polish'];random.Random(20260829190).shuffle(order);texts={'control':control,'polish':treatment}
key={'3':{'A':order[0],'B':order[1]}};(OUT.parent/'blind_key.json').write_text(json.dumps(key,ensure_ascii=False,indent=2),encoding='utf-8')
auth=(SOURCE/'authority_reviser_prompt.md').read_text(encoding='utf-8').split('## PRIMARY DRAFT｜唯一待修订正文底稿',1)[0]
reader=f'''你是匿名的成熟中文男频正文盲读员。两版只存在极小局部差异。比较哪版更自然、更像人物现场、更少 AI 式抽象总结，同时不能因为少一句就自动获胜。\n严格输出：\nVERDICT: A / B / MIXED\nCONFIDENCE: high / medium / low\nNATURALNESS: A / B / TIE\nCHARACTER_IMMEDIACY: A / B / TIE\nANTI_AI_EXPLANATION: A / B / TIE\nCONTINUITY: A / B / TIE\nHARD_PROBLEM_A: 无 或一句\nHARD_PROBLEM_B: 无 或一句\nREASON: 5—9句。\n\n# OPTION A\n{texts[order[0]]}\n\n# OPTION B\n{texts[order[1]]}\n'''
authority=f'''你是匿名 TGN Authority 审稿人。两版只允许纯表达差异。检查删除或改写是否损失人物关系、情绪事实、State、Mission、Canon、Payoff或章末推动；事实等价时再判断哪版更符合 Result Stop / Trust Reader。\n严格输出：\nVERDICT: A / B / MIXED\nCONFIDENCE: high / medium / low\nHARD_VIOLATIONS_A: 无 或一句\nHARD_VIOLATIONS_B: 无 或一句\nFACT_EQUIVALENCE: YES / NO\nRELATIONSHIP_VALUE: A / B / TIE\nRESULT_STOP: A / B / TIE\nREASON: 5—9句。\n\n# FROZEN AUTHORITY\n{auth}\n\n# OPTION A\n{texts[order[0]]}\n\n# OPTION B\n{texts[order[1]]}\n'''
(OUT/'reader_prompt.md').write_text(reader,encoding='utf-8');(OUT/'authority_prompt.md').write_text(authority,encoding='utf-8')
def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def call(kind,model):
 pp=OUT/f'{kind}_prompt.md';out=OUT/f'{kind}_acp.json'
 for attempt in range(3):
  cp=subprocess.run(['node',str(RUNNER),str(pp),str(out),model,'high',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace')
  if cp.returncode==0:
   j=json.loads(out.read_text(encoding='utf-8'))
   if j.get('ok'):
    text=clean(j['text']);(OUT/f'{kind}.md').write_text(text+'\n',encoding='utf-8');return kind,text,j.get('wall_seconds')
  time.sleep(2+attempt*2)
 raise RuntimeError(kind)
rows=[]
with ThreadPoolExecutor(max_workers=2) as ex:
 for f in as_completed([ex.submit(call,'reader','gpt-5.6-terra'),ex.submit(call,'authority','gpt-5.6-luna')]):
  rows.append(f.result());print(f.result() if False else '')
summary={kind:{'text':text,'wall_seconds':wall} for kind,text,wall in rows};(OUT.parent/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(summary,ensure_ascii=False,indent=2))
