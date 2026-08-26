from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp')
EXP=ROOT/'books'/'real-exp-private-prototype-final-novel-20260826-v1'
sys.path.insert(0,str(ROOT/'src'))
from story_mvp.prompts import generate_prompt, parse_canon_memory
from story_mvp.storage import parse_book_sections, apply_state_delta_to_book, validate_book_content_for_save, validate_chapter_body_for_save
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.hybrid_runtime import extract_primary_draft

def load_acp(path:Path)->dict:
    d=json.loads(path.read_text(encoding='utf-8'))
    if not d.get('ok'): raise RuntimeError(d.get('error','ACP failed'))
    return d

def materialize_outline():
    d=load_acp(EXP/'OUTLINE_ACP.json'); text=d['text'].strip()
    p=text.find('# 小说总体设计画像')
    if p>=0: text=text[p:]
    validate_book_content_for_save(text)
    (EXP/'OUTLINE.md').write_text(text,encoding='utf-8')
    (EXP/'BOOK.md').write_text(text,encoding='utf-8')
    (EXP/'OUTLINE_META.json').write_text(json.dumps({k:d.get(k) for k in ['model','effort','wall_seconds','sessionId']},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'outline_chars':len(text),'book_valid':True},ensure_ascii=False))

def book()->str: return (EXP/'BOOK.md').read_text(encoding='utf-8')
def sections(): return parse_book_sections(book())
def recent()->str: return parse_canon_memory(sections()['status']).get('recent_summaries','').strip()
def previous(n:int)->str:
    if n<=1: return ''
    return (EXP/'chapters'/f'chapter-{n-1:04d}.md').read_text(encoding='utf-8')
def chapter_plan(n:int)->str:
    s=sections()['small_plan']
    pat=rf'(?ms)^## 第{n}章：.*?(?=^## 第{n+1}章：|\Z)'
    m=re.search(pat,s)
    if not m: raise RuntimeError(f'missing chapter {n} plan')
    return m.group(0).strip()
def long_block(n:int)->str:
    s=sections()['long_plan']
    blocks=list(re.finditer(r'(?ms)^## 第(\d+)[—-](\d+)章：.*?(?=^## 第\d+[—-]\d+章：|\Z)',s))
    for m in blocks:
        if int(m.group(1))<=n<=int(m.group(2)): return m.group(0).strip()
    return s[:6000].strip()
def rd(n:int)->Path:
    p=EXP/'runs'/f'chapter-{n:04d}'; p.mkdir(parents=True,exist_ok=True); return p

def save_prompt(n:int,stage:str,text:str):
    p=rd(n)/f'{stage}_prompt.md'; p.write_text(text,encoding='utf-8'); print(p)

def materialize_response(n:int,stage:str):
    d=load_acp(rd(n)/f'{stage}_acp.json')
    (rd(n)/f'{stage}_response.md').write_text(d['text'].strip(),encoding='utf-8')
    (rd(n)/f'{stage}_meta.json').write_text(json.dumps({k:d.get(k) for k in ['model','effort','wall_seconds','sessionId']},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'chapter':n,'stage':stage,'chars':len(d['text'])},ensure_ascii=False))

def director(n:int):
    prompt=generate_prompt(mode='director',template='',book_content=book(),current_long_block=long_block(n),previous_chapter_text=previous(n),current_outline='',current_chapter_plan=chapter_plan(n),recent_summaries=recent(),chapter_number=n,creative_direction='严格执行已批准的最终 private-prototype 小说基线与当前 Outline。人物的私人欲望、胜负心、审美/身体吸引和具体关系可以真实改变选择；不要净化成人格正确答案。Supporting Logic 不得成为 Story Engine。')
    save_prompt(n,'director',prompt)
def curator(n:int):
    dr=(rd(n)/'director_response.md').read_text(encoding='utf-8')
    g=retrieve_gbrain(mode='context_curator',book_content=book(),current_long_block=long_block(n),current_outline=dr,recent_summaries=recent())
    (rd(n)/'curator_retrieval.json').write_text(json.dumps({k:v for k,v in g.items() if k not in {'raw_stdout','result'}},ensure_ascii=False,indent=2),encoding='utf-8')
    (rd(n)/'scene_skill.md').write_text(g['result'],encoding='utf-8')
    prompt=generate_prompt(mode='context_curator',template='',book_content=book(),current_long_block=long_block(n),previous_chapter_text=previous(n),current_outline=dr,current_chapter_plan=chapter_plan(n),recent_summaries=recent(),gbrain_inspiration=g['result'],chapter_number=n)
    save_prompt(n,'curator',prompt); print(json.dumps({'accepted':[x['slug'] for x in g['accepted']]},ensure_ascii=False))
def primary(n:int):
    dr=(rd(n)/'director_response.md').read_text(encoding='utf-8'); cu=(rd(n)/'curator_response.md').read_text(encoding='utf-8'); sk=(rd(n)/'scene_skill.md').read_text(encoding='utf-8')
    prompt=generate_prompt(mode='primary_writer',template='',book_content=book(),current_long_block=long_block(n),previous_chapter_text=previous(n),current_outline=dr,current_chapter_plan=chapter_plan(n),recent_summaries=recent(),gbrain_inspiration=sk,curated_context=cu,chapter_number=n)
    save_prompt(n,'primary',prompt)
def body(n:int):
    d=load_acp(rd(n)/'primary_acp.json'); text=d['text'].strip(); (rd(n)/'primary_response.md').write_text(text,encoding='utf-8')
    b=extract_primary_draft(text).strip(); validate_chapter_body_for_save(b)
    if len(b)<1800: raise RuntimeError(f'chapter {n} too short: {len(b)}')
    (EXP/'chapters'/f'chapter-{n:04d}.md').write_text(b,encoding='utf-8')
    (rd(n)/'primary_meta.json').write_text(json.dumps({k:d.get(k) for k in ['model','effort','wall_seconds','sessionId']},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'chapter':n,'body_chars':len(b)},ensure_ascii=False))
def state(n:int):
    b=(EXP/'chapters'/f'chapter-{n:04d}.md').read_text(encoding='utf-8')
    prompt=generate_prompt(mode='state_delta',template='',book_content=book(),recent_summaries=recent(),chapter_number=n,chapter_prose=b)
    save_prompt(n,'state',prompt)
def apply(n:int):
    d=load_acp(rd(n)/'state_acp.json'); text=d['text'].strip(); (rd(n)/'state_response.md').write_text(text,encoding='utf-8')
    updated=apply_state_delta_to_book(book(),n,text); validate_book_content_for_save(updated); (EXP/'BOOK.md').write_text(updated,encoding='utf-8')
    (rd(n)/'state_meta.json').write_text(json.dumps({k:d.get(k) for k in ['model','effort','wall_seconds','sessionId']},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'chapter':n,'book_chars':len(updated)},ensure_ascii=False))
def combine():
    chunks=[]
    for n in range(1,6):
        p=EXP/'chapters'/f'chapter-{n:04d}.md'
        if not p.exists(): raise RuntimeError(f'missing {p}')
        chunks.append(p.read_text(encoding='utf-8').strip())
    text='\n\n'.join(chunks)+'\n'; (EXP/'CHAPTERS_0001_0005.md').write_text(text,encoding='utf-8'); (EXP/'CHAPTERS_0001_0005.txt').write_text(text,encoding='utf-8')
    print(json.dumps({'combined_chars':len(text)},ensure_ascii=False))

if __name__=='__main__':
    a=sys.argv[1]
    if a=='outline': materialize_outline()
    elif a=='combine': combine()
    else:
        n=int(sys.argv[2]); {'director':director,'curator':curator,'primary':primary,'body':body,'state':state,'apply':apply,'materialize':materialize_response}[a](n,sys.argv[3]) if a=='materialize' else {'director':director,'curator':curator,'primary':primary,'body':body,'state':state,'apply':apply}[a](n)
