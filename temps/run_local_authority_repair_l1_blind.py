from __future__ import annotations
import json, random, re, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT=Path(r'C:\dev\tgn-story-mvp-local-repair-20260830')
SOURCE=Path(r'C:\dev\tgn-story-mvp-reviser-noop-20260830\books\real-exp-reviser-noop-upstream-heldout-20260830-v1\heldout-new-novel-2')
BASE=ROOT/'books'/'real-exp-local-authority-repair-20260830-v1'
DER=BASE/'derivation-l1'
OUT=BASE/'derivation-l1-blind'
RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')

def clean(text):return text.strip()
def call(prompt_path,out_path,model='gpt-5.6-luna'):
 proc=subprocess.run(['node',str(RUNNER),str(prompt_path),str(out_path),model,'high',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace',timeout=900)
 if proc.returncode!=0:raise RuntimeError(proc.stderr[-4000:])
 d=json.loads(out_path.read_text(encoding='utf-8'))
 if not d.get('ok'):raise RuntimeError(str(d.get('error')))
 return d

def parse(text):
 text=text.strip()
 if text.startswith('```'):
  text=re.sub(r'^```(?:json)?\s*','',text);text=re.sub(r'\s*```$','',text)
 return json.loads(text)

def one(run,ch,judge):
 d=DER/run/f'chapter-{ch:04d}'
 candidates={'primary':clean((d/'primary_body.md').read_text(encoding='utf-8')),'local':clean((d/'final_body.md').read_text(encoding='utf-8')),'high':clean((d/'high_body.md').read_text(encoding='utf-8'))}
 labels=['A','B','C']; names=list(candidates)
 rnd=random.Random(f'L1-{run}-{ch}-{judge}');rnd.shuffle(names)
 key={label:name for label,name in zip(labels,names)}
 blocks='\n\n'.join(f'## OPTION {label}\n{candidates[key[label]]}' for label in labels)
 outdir=OUT/run/f'chapter-{ch:04d}';outdir.mkdir(parents=True,exist_ok=True)
 if judge=='story':
  prompt='''你是 fresh-context 匿名成熟中文男频商业编辑。A/B/C是同一冻结章节的三种最终正文，但你不知道各自来自哪里。只比较读者最终体验：续读欲、主角主动性和私人欲望、动作/冲突、Power Fantasy、Reward/Public Proof、关系张力、节奏、AI总结/报告味。不要因为更长、更短或更像“修订稿”偏爱。

严格只输出JSON：{"ranking":["A","B","C"],"scores":{"A":0,"B":0,"C":0},"reason":"中文5-8句具体比较"}

'''+blocks
  model='gpt-5.6-luna'
 else:
  src_run='runs' if run=='repeat1' else 'repeat2'
  authority=(SOURCE/src_run/f'chapter-{ch:04d}'/'treatment_reviser_prompt.md').read_text(encoding='utf-8').split('## PRIMARY DRAFT',1)[0]
  prompt='''你是 fresh-context 匿名 TGN Authority Judge。下面给你冻结 Authority 与三个匿名最终正文。只审事实/计划忠实度，不因为文风更漂亮或更保守加分。逐个检查 actor/action/object、Direct Result、State Change、Ending、Reader Release、Power/永久边界、关系/ownership/resource状态、Unknown/旧史/伤势/数字/来源是否越权。

严格只输出JSON：{"ranking":["A","B","C"],"scores":{"A":0,"B":0,"C":0},"hard_problems":{"A":[],"B":[],"C":[]},"reason":"中文5-10句具体比较"}

## FROZEN AUTHORITY
'''+authority+'\n\n'+blocks
  model='gpt-5.6-terra'
 prompt_path=outdir/f'{judge}_prompt.md';out_path=outdir/f'{judge}_acp.json';prompt_path.write_text(prompt,encoding='utf-8')
 data=call(prompt_path,out_path,model); res=parse(str(data['text']))
 decoded={}
 for label in labels:
  name=key[label];decoded[name]={'score':float(res['scores'][label]),'hard_problems':list(res.get('hard_problems',{}).get(label,[]))}
 ranking=[key[x] for x in res['ranking']]
 row={'run':run,'chapter':ch,'judge':judge,'ranking':ranking,'decoded':decoded,'reason':res.get('reason',''),'key':key}
 (outdir/f'{judge}_decoded.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(run,ch,judge,ranking[0],flush=True);return row

def main():
 OUT.mkdir(parents=True,exist_ok=True);rows=[]
 with ThreadPoolExecutor(max_workers=16) as ex:
  fs=[ex.submit(one,r,c,j) for r in ['repeat1','repeat2'] for c in range(1,5) for j in ['story','authority']]
  for f in as_completed(fs):rows.append(f.result())
 agg={}
 for judge in ['story','authority']:
  agg[judge]={}
  subset=[r for r in rows if r['judge']==judge]
  for name in ['primary','local','high']:
   scores=[r['decoded'][name]['score'] for r in subset]; hard=sum(len(r['decoded'][name]['hard_problems']) for r in subset); first=sum(r['ranking'][0]==name for r in subset); ranks=[r['ranking'].index(name)+1 for r in subset]
   agg[judge][name]={'mean_score':round(sum(scores)/len(scores),3),'first_place':first,'mean_rank':round(sum(ranks)/len(ranks),3),'hard_problems':hard}
 summary={'schema_version':'local-authority-repair-l1-blind-v1','aggregates':agg,'rows':sorted(rows,key=lambda r:(r['run'],r['chapter'],r['judge']))}
 (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(agg,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
