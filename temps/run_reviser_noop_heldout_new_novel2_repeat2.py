from __future__ import annotations
import json,re,subprocess,time
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'books'/'real-exp-reviser-noop-upstream-heldout-20260830-v1'/'heldout-new-novel-2'
SOURCE=BASE/'runs'; OUT=BASE/'repeat2'
RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')

def clean(text:str)->str:
    return re.sub(r'(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$','',text).strip()

def call(prompt_path:Path,out_path:Path,model:str,effort:str,label:str)->dict:
    last=''
    for attempt in range(3):
        try:
            p=subprocess.run(['node',str(RUNNER),str(prompt_path),str(out_path),model,effort,str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace',timeout=1200)
        except subprocess.TimeoutExpired:
            last=f'timeout {label}';time.sleep(2+attempt*2);continue
        if p.returncode==0 and out_path.exists():
            data=json.loads(out_path.read_text(encoding='utf-8'))
            if data.get('ok'): return data
            last=str(data.get('error',''))
        else:last=(p.stderr+'\n'+p.stdout)[-4000:]
        time.sleep(2+attempt*2)
    raise RuntimeError(f'{label}: {last}')

def run_prompt(prompt:str,d:Path,name:str,model:str)->tuple[str,float]:
    d.mkdir(parents=True,exist_ok=True); pp=d/f'{name}_prompt.md'; ap=d/f'{name}_acp.json'; rp=d/f'{name}_response.md';pp.write_text(prompt,encoding='utf-8');data=call(pp,ap,model,'high',name);text=clean(str(data.get('text','')));rp.write_text(text+'\n',encoding='utf-8');return text,float(data.get('wall_seconds') or 0)

def extract_body(text:str)->str:
    return text.rsplit('# 正式正文',1)[-1].strip() if '# 正式正文' in text else text.strip()

def reviser_prompt_with_body(source_prompt:str,new_body:str)->str:
    marker='## PRIMARY DRAFT｜唯一待修订正文底稿'
    if marker not in source_prompt: raise RuntimeError('missing primary marker')
    prefix=source_prompt.split(marker,1)[0].rstrip()
    return prefix+'\n\n'+marker+'\n\n'+new_body.strip()+'\n'

def primary_one(ch:int,arm:str):
    src=SOURCE/f'chapter-{ch:04d}'; d=OUT/f'chapter-{ch:04d}'
    prompt=(src/f'{arm}_primary_prompt.md').read_text(encoding='utf-8')
    raw,wall=run_prompt(prompt,d,f'{arm}_primary','gpt-5.6-terra')
    body=extract_body(raw);(d/f'{arm}_primary_body.md').write_text(body+'\n',encoding='utf-8')
    return ch,arm,wall,body

def reviser_one(ch:int,arm:str,body:str):
    src=SOURCE/f'chapter-{ch:04d}';d=OUT/f'chapter-{ch:04d}'
    frozen=(src/f'{arm}_reviser_prompt.md').read_text(encoding='utf-8')
    prompt=reviser_prompt_with_body(frozen,body)
    raw,wall=run_prompt(prompt,d,f'{arm}_reviser','gpt-5.6-luna')
    final=extract_body(raw);(d/f'{arm}_final_body.md').write_text(final+'\n',encoding='utf-8')
    return ch,arm,wall,final

def main():
    OUT.mkdir(parents=True,exist_ok=True); primary={}; rows=[]
    with ThreadPoolExecutor(max_workers=8) as ex:
        fs=[ex.submit(primary_one,ch,arm) for ch in range(1,5) for arm in ('control','treatment')]
        for f in as_completed(fs):
            ch,arm,wall,body=f.result();primary[(ch,arm)]=(body,wall);print('PRIMARY',ch,arm,wall,flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex:
        fs=[ex.submit(reviser_one,ch,arm,primary[(ch,arm)][0]) for ch in range(1,5) for arm in ('control','treatment')]
        for f in as_completed(fs):
            ch,arm,rwall,final=f.result();body,pwall=primary[(ch,arm)];rows.append({'chapter':ch,'arm':arm,'primary_wall':pwall,'reviser_wall':rwall,'chain_wall':pwall+rwall});print('REVISER',ch,arm,rwall,flush=True)
    rows.sort(key=lambda x:(x['chapter'],x['arm']))
    (OUT/'summary.json').write_text(json.dumps({'schema_version':'final-facts-projection-heldout2-repeat2','rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
