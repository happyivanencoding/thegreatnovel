from __future__ import annotations
import hashlib,json,re,subprocess,time,sys
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'books'/'real-exp-reviser-noop-upstream-heldout-20260830-v1'
BOOK=BASE/'heldout-new-novel'; OUT=BASE/'repeat2'; RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')
sys.path.insert(0,str(ROOT/'src'))
from story_mvp.hybrid_runtime import extract_primary_draft
WATCH="""## FINAL-DRAFT READINESS WATCH｜只在写完正文前内部检查一次

不要重规划剧情，也不要输出审计。只用本 Prompt 已经给你的 Authority / Mission / Curated Context，对最终正文做一次很窄的提交前检查：

1. **精确事实不自己补全**：金额、价格、旧对白、伤势、身份、持有人、能力边界与历史状态，输入没明确就不补；输入已经给了具体对象/状态时，全章用同一个具体对象/状态，不把“资格/份额/承诺”升级成“已到账/已拥有”。
2. **关键边界只落一次**：若本章结果真实依赖一个已明确的持有/付款/力量/冷却/未知边界，在发生点让读者看懂一次即可；不要漏，也不要后面再解释一遍。
3. **已排程价值说具体一次**：Curated Context / Reader Release 已明确某个具名入口、契约、奖励、地点或身份为什么值，就用现成事实让读者知道一次；不要压成“一个机会 / 更大的入口”，也不要新增待遇。
4. **结果成立就停**：动作、对白、物体变化和人物反应已经把意义写出来后，删掉随后同义的作者解释、人物总结、能力复盘或“不是A也不是B”的裁断；让后果进入下一动作。
5. **私人动机别净化**：Curated Context 已明确钱、胜负、占有、虚荣、审美/身体吸引、嫉妒、报复或某个具体人的牵引，而且现场自然触发时，让它通过一次想法/对白/注意力/选择露出来；不要改写成中性职责或正确分析。

除此之外按原 Primary 合同正常写，不为了通过这五项而新增说明段。"""
PROTOCOL_HASH='56B6ECC21151811F21DDDF2B696B5052DF417AD0419103473D44A25435CE13F3'

def clean(t):return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',t).strip()
def call(pp,ap,model):
 last=''
 for attempt in range(3):
  try:p=subprocess.run(['node',str(RUNNER),str(pp),str(ap),model,'high',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace',timeout=1200)
  except subprocess.TimeoutExpired:last='timeout';continue
  if p.returncode==0 and ap.exists():
   d=json.loads(ap.read_text(encoding='utf-8'))
   if d.get('ok'):return d
   last=str(d.get('error'))
  else:last=(p.stderr+'\n'+p.stdout)[-3000:]
  time.sleep(2+attempt*2)
 raise RuntimeError(last)
def run_primary(ch,arm):
 src=BOOK/'runs'/f'chapter-{ch:04d}';d=OUT/f'chapter-{ch:04d}';d.mkdir(parents=True,exist_ok=True)
 base=(src/'primary_base_prompt.md').read_text(encoding='utf-8');prompt=base if arm=='control' else base.rstrip()+'\n\n'+WATCH+'\n';pp=d/f'{arm}_primary_prompt.md';ap=d/f'{arm}_primary_acp.json';pp.write_text(prompt,encoding='utf-8');data=call(pp,ap,'gpt-5.6-terra');raw=clean(data.get('text',''));body=extract_primary_draft(raw).strip();(d/f'{arm}_primary_response.md').write_text(raw+'\n',encoding='utf-8');(d/f'{arm}_primary_body.md').write_text(body+'\n',encoding='utf-8');return ch,arm,body,raw,float(data.get('wall_seconds') or 0)
def replace_primary(prompt,body):
 marker='## PRIMARY DRAFT｜唯一待修订正文底稿'
 i=prompt.index(marker);return prompt[:i]+marker+'\n\n'+body.strip()+'\n'
def run_reviser(ch,arm,body):
 src=BOOK/'runs'/f'chapter-{ch:04d}';d=OUT/f'chapter-{ch:04d}';base=(src/'control_reviser_prompt.md').read_text(encoding='utf-8');prompt=replace_primary(base,body);pp=d/f'{arm}_reviser_prompt.md';ap=d/f'{arm}_reviser_acp.json';pp.write_text(prompt,encoding='utf-8');data=call(pp,ap,'gpt-5.6-luna');raw=clean(data.get('text',''));final=extract_primary_draft(raw).strip();(d/f'{arm}_reviser_response.md').write_text(raw+'\n',encoding='utf-8');(d/f'{arm}_final_body.md').write_text(final+'\n',encoding='utf-8');return ch,arm,final,float(data.get('wall_seconds') or 0)
def main():
 actual=hashlib.sha256((BASE/'PROTOCOL.md').read_bytes()).hexdigest().upper();assert actual==PROTOCOL_HASH,(actual,PROTOCOL_HASH)
 OUT.mkdir(parents=True,exist_ok=True);prim={};rows=[]
 with ThreadPoolExecutor(max_workers=4) as ex:
  fs=[ex.submit(run_primary,ch,arm) for ch in range(1,5) for arm in ('control','treatment')]
  for f in as_completed(fs):
   ch,arm,body,raw,wall=f.result();prim[(ch,arm)]=(body,wall);print('PRIMARY',ch,arm,wall,flush=True)
 with ThreadPoolExecutor(max_workers=4) as ex:
  fs=[ex.submit(run_reviser,ch,arm,prim[(ch,arm)][0]) for ch in range(1,5) for arm in ('control','treatment')]
  for f in as_completed(fs):
   ch,arm,final,rwall=f.result();pwall=prim[(ch,arm)][1];rows.append({'chapter':ch,'arm':arm,'primary_wall':pwall,'reviser_wall':rwall,'chain_wall':pwall+rwall});print('REVISER',ch,arm,rwall,flush=True)
 rows.sort(key=lambda x:(x['chapter'],x['arm']));(OUT/'summary.json').write_text(json.dumps({'schema_version':'reviser-noop-heldout-repeat2','rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
