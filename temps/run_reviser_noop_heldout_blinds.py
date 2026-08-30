from __future__ import annotations
import json,random,re,subprocess,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'books'/'real-exp-reviser-noop-upstream-heldout-20260830-v1';BOOK=BASE/'heldout-new-novel';RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')
RUNS={'repeat1':BOOK/'runs','repeat2':BASE/'repeat2'}

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
def parse(raw):
 m=re.search(r'\{.*\}',clean(raw),re.S)
 if not m:raise ValueError(raw[:600])
 return json.loads(m.group(0))
def authority(ch):
 p=(BOOK/'runs'/f'chapter-{ch:04d}'/'control_reviser_prompt.md').read_text(encoding='utf-8');st=p.find('# Hybrid Runtime');en=p.find('## PRIMARY DRAFT',st);return p[st:en].strip()
def one(run,ch,judge):
 src=RUNS[run]/f'chapter-{ch:04d}';out=BASE/'blind-fourway'/run/f'chapter-{ch:04d}';out.mkdir(parents=True,exist_ok=True)
 files={'control_primary':src/'control_primary_body.md','treatment_primary':src/'treatment_primary_body.md','control_reviser':src/'control_final_body.md','treatment_reviser':src/'treatment_final_body.md'}
 texts={k:v.read_text(encoding='utf-8').strip() for k,v in files.items()};items=list(texts);random.Random(f'heldout:{run}:{ch}:{judge}').shuffle(items);letters='ABCD';key={letters[i]:items[i] for i in range(4)}
 cand='\n\n'.join(f'# OPTION {letter}\n\n{texts[key[letter]]}' for letter in letters)
 if judge=='story':
  prompt=("你是 fresh-context 匿名成熟中文男频商业编辑。下面四个候选来自同一章同一冻结上游，其中有两份Primary和两份经过Full Authority Reviser的版本，但你不知道对应关系。只评普通男频读者的最终阅读体验：开篇/续读欲、主角欲望和主动选择、冲突与动作清晰度、Power Fantasy、Reward/Public Proof/Surprise、关系、节奏、AI总结味、重复证明、程序/报告味、漂亮二段论。不要因更长、更短、更像修订稿而偏爱。\n\n严格只输出JSON：{\"ranking\":[\"A\",\"B\",\"C\",\"D\"],\"scores\":{\"A\":0,\"B\":0,\"C\":0,\"D\":0},\"reason\":\"中文6-10句，必须指出真正决定排序的具体文本差异\"}\n\n"+cand);model='gpt-5.6-terra'
 else:
  a=authority(ch);prompt=("你是 fresh-context 匿名 TGN Frozen Authority 审计员。下面四个候选来自同一章同一冻结上游。只比较 actor/action/object、Direct Result、State Change、Ending、money/resource/ownership、power boundary、relationship、Reader Release、unknown/history 与跨章 timing。不要评文笔；激进、爽、群众反应强本身不是错。只有 required missing、未授权新增或明确冲突才是Hard problem。\n\n严格只输出JSON：{\"ranking\":[\"A\",\"B\",\"C\",\"D\"],\"scores\":{\"A\":0,\"B\":0,\"C\":0,\"D\":0},\"hard_problems\":{\"A\":[],\"B\":[],\"C\":[],\"D\":[]},\"reason\":\"中文6-10句，指出具体事实边界\"}\n\n# FROZEN AUTHORITY CONTEXT\n"+a+"\n\n"+cand);model='gpt-5.6-luna'
 pp=out/f'{judge}_prompt.md';ap=out/f'{judge}_acp.json';pp.write_text(prompt,encoding='utf-8');d=call(pp,ap,model);raw=str(d.get('text',''));(out/f'{judge}_response.md').write_text(raw.strip()+'\n',encoding='utf-8');v=parse(raw)
 scores={key[k]:float(x) for k,x in v['scores'].items()};ranking=[key[x] for x in v['ranking']];hard={key[k]:x for k,x in v.get('hard_problems',{}).items()};return {'run':run,'chapter':ch,'judge':judge,'blind_key':key,'ranking':ranking,'scores':scores,'hard_problems':hard,'reason':v.get('reason',''),'wall_seconds':float(d.get('wall_seconds') or 0)}
def main():
 rows=[]
 with ThreadPoolExecutor(max_workers=8) as ex:
  fs=[ex.submit(one,run,ch,j) for run in RUNS for ch in range(1,5) for j in ('story','authority')]
  for f in as_completed(fs):
   x=f.result();rows.append(x);print(json.dumps(x,ensure_ascii=False),flush=True)
 rows.sort(key=lambda x:(x['run'],x['chapter'],x['judge']));out=BASE/'blind-fourway';(out/'summary.json').write_text(json.dumps({'schema_version':'reviser-noop-heldout-fourway-blind-v1','rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
