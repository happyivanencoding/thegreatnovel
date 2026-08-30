from __future__ import annotations

import json
import math
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT=Path(r'C:\dev\tgn-story-mvp-local-repair-20260830')
SOURCE=Path(r'C:\dev\tgn-story-mvp-reviser-noop-20260830\books\real-exp-reviser-noop-upstream-heldout-20260830-v1\heldout-new-novel-2')
OUT=ROOT/'books'/'real-exp-local-authority-repair-20260830-v1'/'derivation-l1'
RUNNER=Path(r'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs')
PROTOCOL_HASH=(ROOT/'books'/'real-exp-local-authority-repair-20260830-v1'/'PROTOCOL_L1_SHA256.txt').read_text(encoding='utf-8').strip()
PUNCT=re.compile(r'[\s\W_]+', re.UNICODE)


def body(text:str)->str:
    return text.rsplit('# 正式正文',1)[-1].strip()

def paragraphs(text:str)->list[str]:
    return [x.strip() for x in re.split(r'\n\s*\n',text.strip()) if x.strip()]

def exact_line(prompt:str,label:str)->str:
    m=re.search(rf'(?m)^{re.escape(label)}：(.*)$',prompt)
    return m.group(1).strip() if m else ''

def section(prompt:str,start_pattern:str,next_pattern:str)->str:
    m=re.search(rf'(?ms)^{start_pattern}\s*$\n(.*?)(?={next_pattern}|\Z)',prompt)
    return m.group(1).strip() if m else ''

def protagonist(prompt:str)->str:
    m=re.search(r'(?m)^# HUMAN SEED｜([^／\n]+)',prompt)
    return m.group(1).strip() if m else ''

def norm(text:str,drop:str='')->str:
    if drop:
        text=text.replace(drop,'')
    return PUNCT.sub('',text)

def grams(text:str,drop:str='')->set[str]:
    t=norm(text,drop)
    return {t[i:i+2] for i in range(max(0,len(t)-1))}

def similarity(query:str,para:str,drop:str='')->float:
    q=grams(query,drop); p=grams(para,drop)
    if not q or not p:return 0.0
    return len(q&p)/math.sqrt(len(q)*len(p))

def active_lanes(prompt:str)->dict[str,str]:
    state=' '.join(x for x in [exact_line(prompt,'直接结果'),exact_line(prompt,'状态变化')] if x)
    reader=section(prompt,r'## READER RELEASE｜本章已批准首次释放事实；逐条核对',r'^## ')
    if '没有排程 Reader Release' in reader or '（本章没有排程 Reader Release。）' in reader:
        reader=''
    audit=section(prompt,r'# Curator Audit',r'^# ')
    return {k:v for k,v in [('reader',reader),('audit',audit),('state',state)] if v}

def choose(prompt:str,ps:list[str])->tuple[list[int],dict[int,dict[str,float]],dict[str,str]]:
    person=protagonist(prompt)
    lanes=active_lanes(prompt)
    quotas={'reader':3,'audit':2,'state':2}
    lane_order=['reader','audit','state']
    selected_by_lane={}
    for lane in lane_order:
        query=lanes.get(lane,'')
        if not query:continue
        ranked=[]
        for idx,p in enumerate(ps,1):
            if len(norm(p,person))<8:continue
            sc=similarity(query,p,person)
            if sc>=0.04:
                ranked.append((sc,idx))
        ranked.sort(reverse=True)
        selected_by_lane[lane]=ranked[:quotas[lane]]
    meta={};order=[]
    for lane in lane_order:
        for sc,idx in selected_by_lane.get(lane,[]):
            meta.setdefault(idx,{})[lane]=round(sc,6)
            if idx not in order:order.append(idx)
    return order[:5],meta,lanes

def prompt_text(ps:list[str],editable:list[int],meta:dict[int,dict[str,float]],lanes:dict[str,str])->str:
    context_ids=set()
    for idx in editable:
        context_ids.update(range(max(1,idx-1),min(len(ps),idx+1)+1))
    lane_block='\n\n'.join(f'### {name.upper()}\n{text}' for name,text in lanes.items())
    windows=[]
    for idx in sorted(context_ids):
        tag='EDITABLE' if idx in editable else 'READ_ONLY'
        lane_note=''
        if idx in meta:
            lane_note=' lanes='+','.join(f'{k}:{v:.3f}' for k,v in meta[idx].items())
        windows.append(f'[P{idx:03d} {tag}{lane_note}]\n{ps[idx-1]}')
    return f'''你是 TGN 的 Blocker-Local Authority Repair。你不是全章 Reviser，也不是 Story 编辑。你只能在 Runtime 已选出的极少段落里修复下面明确的 Authority lane；你看不到整章，其它段落由代码锁死。

## AUTHORITY LANES
{lane_block}

## LOCAL WINDOWS
{chr(10).join(windows)}

## 规则
- 只能修改标记为 EDITABLE 的 paragraph_id；READ_ONLY 只帮助衔接。
- 已经满足 Authority 的 EDITABLE 段不要改。
- 每个 patch 只能把一个原段替换成一个新段；不得插入、删除、拆段、合段或重排。
- 不做一般润色，不改变人物决定、胜负、Reward、关系方向、Ending 或未知事实。
- 不新增 Authority 未明确给出的伤势、数字、物品来源/持有关系、旧史、他人内心/认知或新能力。
- Reader Release 只补到读者能直接复述，不扩成百科。
- 状态/力量 milestone 只在 Authority 明确要求时直称一次，不重复总结。
- 如果局部窗口不足以安全修复某个 lane，就不要猜；保持不改。
- 最多5个 patch。

只输出单个 JSON 对象，不要 Markdown：
{{"patches":[{{"paragraph_id":12,"new_text":"完整单段正文，不含空行","reason":"一句话说明修复的具体Authority"}}]}}
没有修改时输出 {{"patches":[]}}。
'''

def call(prompt_path:Path,out_path:Path)->dict[str,Any]:
    proc=subprocess.run(['node',str(RUNNER),str(prompt_path),str(out_path),'gpt-5.6-luna','medium',str(ROOT)],cwd=ROOT,text=True,capture_output=True,encoding='utf-8',errors='replace',timeout=900)
    if proc.returncode!=0: raise RuntimeError(proc.stderr[-4000:])
    data=json.loads(out_path.read_text(encoding='utf-8'))
    if not data.get('ok'): raise RuntimeError(str(data.get('error')))
    return data

def parse_json_text(text:str)->dict[str,Any]:
    text=text.strip()
    if text.startswith('```'):
        text=re.sub(r'^```(?:json)?\s*','',text)
        text=re.sub(r'\s*```$','',text)
    return json.loads(text)

def one(run:str,ch:int)->dict[str,Any]:
    src_run='runs' if run=='repeat1' else 'repeat2'
    d=SOURCE/src_run/f'chapter-{ch:04d}'
    authority=(d/'treatment_reviser_prompt.md').read_text(encoding='utf-8')
    primary=body((d/'treatment_primary_response.md').read_text(encoding='utf-8'))
    high=body((d/'treatment_reviser_response.md').read_text(encoding='utf-8'))
    ps=paragraphs(primary)
    editable,meta,lanes=choose(authority,ps)
    target=OUT/run/f'chapter-{ch:04d}';target.mkdir(parents=True,exist_ok=True)
    manifest={'protocol_sha256':PROTOCOL_HASH,'run':run,'chapter':ch,'paragraph_count':len(ps),'editable_paragraph_ids':editable,'scores':{str(k):v for k,v in meta.items()},'lanes':lanes}
    (target/'locality_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not editable:
        final=primary; wall=0.0; raw={'patches':[]}; supported=False
    else:
        ptext=prompt_text(ps,editable,meta,lanes)
        prompt_path=target/'repair_prompt.md'; out_path=target/'repair_acp.json'
        prompt_path.write_text(ptext,encoding='utf-8')
        data=call(prompt_path,out_path); wall=float(data.get('wall_seconds') or 0); supported=True
        raw=parse_json_text(str(data.get('text','')))
        patches=raw.get('patches',[])
        if not isinstance(patches,list) or len(patches)>5: raise ValueError('invalid patches list')
        seen=set();new_ps=list(ps)
        for patch in patches:
            idx=int(patch['paragraph_id']);new=str(patch['new_text']).strip()
            if idx not in editable: raise ValueError(f'patch outside editable P{idx}')
            if idx in seen: raise ValueError(f'duplicate patch P{idx}')
            if not new or '\n\n' in new: raise ValueError(f'patch P{idx} changes paragraph structure')
            seen.add(idx);new_ps[idx-1]=new
        final='\n\n'.join(new_ps)
        final_ps=paragraphs(final)
        if len(final_ps)!=len(ps): raise ValueError('paragraph count changed')
        for idx,(before,after) in enumerate(zip(ps,final_ps),1):
            if idx not in editable and before!=after: raise ValueError(f'locked paragraph changed P{idx}')
    (target/'patches.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (target/'final_body.md').write_text(final+'\n',encoding='utf-8')
    (target/'primary_body.md').write_text(primary+'\n',encoding='utf-8')
    (target/'high_body.md').write_text(high+'\n',encoding='utf-8')
    high_data=json.loads((d/'treatment_reviser_acp.json').read_text(encoding='utf-8'))
    row={'run':run,'chapter':ch,'supported':supported,'editable_count':len(editable),'editable_ratio':round(len(editable)/len(ps),4),'patch_count':len(raw.get('patches',[])),'repair_wall':round(wall,3),'high_wall':float(high_data.get('wall_seconds') or 0),'final_chars':len(final),'primary_chars':len(primary),'high_chars':len(high)}
    print(row,flush=True);return row

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[]
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures=[ex.submit(one,run,ch) for run in ['repeat1','repeat2'] for ch in range(1,5)]
        for fut in as_completed(futures):rows.append(fut.result())
    rows.sort(key=lambda x:(x['run'],x['chapter']))
    summary={'schema_version':'local-authority-repair-l1-derivation-v1','protocol_sha256':PROTOCOL_HASH,'rows':rows,'supported':sum(r['supported'] for r in rows),'mean_editable_ratio':round(sum(r['editable_ratio'] for r in rows)/len(rows),4),'mean_patch_count':round(sum(r['patch_count'] for r in rows)/len(rows),3),'mean_repair_wall':round(sum(r['repair_wall'] for r in rows)/len(rows),3),'mean_high_wall':round(sum(r['high_wall'] for r in rows)/len(rows),3)}
    (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
