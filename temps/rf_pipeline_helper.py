from __future__ import annotations
import json,re,sys
from pathlib import Path

ROOT=Path(r'C:\dev\tgn-story-mvp')
EXP=ROOT/'books'/'reader-feedback-prose-v1'
sys.path.insert(0,str(ROOT/'src'))
from story_mvp.prompts import generate_prompt, parse_canon_memory
from story_mvp.storage import parse_book_sections, compose_book_content, apply_state_delta_to_book
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.hybrid_runtime import extract_primary_draft


def clean_model_text(text:str, heading:str|None=None)->str:
    text=text.strip()
    if heading:
        i=text.find(heading)
        if i>=0: text=text[i:]
    return text.strip()

def load_json_text(path:Path)->str:
    data=json.loads(path.read_text(encoding='utf-8'))
    if not data.get('ok'): raise RuntimeError(f'ACP failed {path}: {data.get("error")}')
    return data.get('text','').strip()

def plan_text()->str:
    return (EXP/'CONTINUATION_PLAN.md').read_text(encoding='utf-8')

def chapter_plan(n:int)->str:
    text=plan_text()
    m=re.search(rf'(?ms)^## Chapter {n}:.*?(?=^## Chapter {n+1}:|^# Window Checks|\Z)',text)
    if not m: raise RuntimeError(f'chapter {n} plan not found')
    return m.group(0).strip()

def long_block()->str:
    text=plan_text()
    m=re.search(r'(?ms)^# Continuation Window\s*\n(.*?)(?=^## Chapter 4:)',text)
    return (m.group(1).strip() if m else 'Chapter 4—8: 内门新阶段连续窗口。')

def book()->str:
    return (EXP/'BOOK.md').read_text(encoding='utf-8')

def recent_summaries(book_text:str)->str:
    sections=parse_book_sections(book_text)
    status=sections['status']
    fields=parse_canon_memory(status)
    return fields.get('recent_summaries','').strip()

def prev_body(n:int)->str:
    if n==4: return (EXP/'SOURCE_CHAPTER_3.md').read_text(encoding='utf-8')
    return (EXP/'chapters'/f'chapter-{n-1:04d}.md').read_text(encoding='utf-8')

def run_dir(n:int)->Path:
    p=EXP/'runs'/f'chapter-{n:04d}'; p.mkdir(parents=True,exist_ok=True); return p

def prepare():
    raw=load_json_text(EXP/'continuation_plan_acp.json')
    text=clean_model_text(raw,'# Continuation Window')
    if '# Window Checks' not in text: raise RuntimeError('continuation plan missing Window Checks')
    for n in range(4,9):
        if f'## Chapter {n}:' not in text: raise RuntimeError(f'missing chapter {n}')
    (EXP/'CONTINUATION_PLAN.md').write_text(text,encoding='utf-8')
    src=(EXP/'SOURCE_BOOK_CH3.md').read_text(encoding='utf-8')
    sections=parse_book_sections(src)
    sections['long_plan']=long_block()
    sections['small_plan']='\n\n'.join(chapter_plan(n) for n in range(4,9))
    st=sections['status']
    # Remove only experiment-stop meta promises; keep all story canon/open promises.
    lines=[]
    for line in st.splitlines():
        s=line.strip()
        if ('隔离实验' in s and ('Chapter 1—3' in s or 'Chapter 3' in s or 'Chapter 4' in s)):
            continue
        if ('不生成 Chapter 4' in s or '不写 Chapter 4' in s):
            continue
        lines.append(line)
    st='\n'.join(lines).rstrip()
    note='- Reader Feedback Continuation v1：用户已明确授权在新实验中继续生成 Chapter 4—8；此授权只解除旧隔离实验的停止标记，不改写 Chapter 1—3 已发生 Canon。'
    if '## AUTHOR NOTES' in st:
        st += '\n' + note
    else:
        st += '\n\n## AUTHOR NOTES\n\n' + note
    sections['status']=st.strip()
    (EXP/'BOOK.md').write_text(compose_book_content(sections),encoding='utf-8')
    print('prepared plan/book',len(text),len((EXP/'BOOK.md').read_text(encoding='utf-8')))

def make_director(n:int):
    b=book(); recent=recent_summaries(b); prev=prev_body(n)
    prompt=generate_prompt(mode='director',template='',book_content=b,current_long_block=long_block(),previous_chapter_text=prev,current_outline='',current_chapter_plan=chapter_plan(n),recent_summaries=recent,chapter_number=n,creative_direction='按已批准 Chapter 4—8 continuation plan 执行当前章。优先人物欲望、力量选择、关系/对手反应与行动空间变化；Supporting Logic 不得成为 Story Engine，不把内门流程、训练程序或武技分析写成主要故事。')
    p=run_dir(n)/'director_prompt.md'; p.write_text(prompt,encoding='utf-8'); print(p)

def materialize(n:int,stage:str):
    rd=run_dir(n); text=load_json_text(rd/f'{stage}_acp.json')
    (rd/f'{stage}_response.md').write_text(text,encoding='utf-8')
    print(stage,'chars',len(text))

def make_curator(n:int):
    b=book(); recent=recent_summaries(b); prev=prev_body(n); rd=run_dir(n)
    director=(rd/'director_response.md').read_text(encoding='utf-8')
    g=retrieve_gbrain(mode='context_curator',book_content=b,current_long_block=long_block(),current_outline=director,recent_summaries=recent)
    (rd/'gbrain.json').write_text(json.dumps({k:v for k,v in g.items() if k not in {'raw_stdout'}},ensure_ascii=False,indent=2),encoding='utf-8')
    (rd/'gbrain_result.md').write_text(g['result'],encoding='utf-8')
    prompt=generate_prompt(mode='context_curator',template='',book_content=b,current_long_block=long_block(),previous_chapter_text=prev,current_outline=director,current_chapter_plan=chapter_plan(n),recent_summaries=recent,gbrain_inspiration=g['result'],chapter_number=n)
    p=rd/'curator_prompt.md'; p.write_text(prompt,encoding='utf-8'); print(p,'gbrain',g['query_strategy'],[x['slug'] for x in g['accepted']])

def make_primary(n:int):
    b=book(); recent=recent_summaries(b); prev=prev_body(n); rd=run_dir(n)
    director=(rd/'director_response.md').read_text(encoding='utf-8'); curator=(rd/'curator_response.md').read_text(encoding='utf-8')
    g=(rd/'gbrain_result.md').read_text(encoding='utf-8') if (rd/'gbrain_result.md').exists() else ''
    prompt=generate_prompt(mode='primary_writer',template='',book_content=b,current_long_block=long_block(),previous_chapter_text=prev,current_outline=director,current_chapter_plan=chapter_plan(n),recent_summaries=recent,gbrain_inspiration=g,curated_context=curator,chapter_number=n)
    p=rd/'primary_prompt.md'; p.write_text(prompt,encoding='utf-8'); print(p)

def extract_body(n:int):
    rd=run_dir(n); text=load_json_text(rd/'primary_acp.json'); (rd/'primary_response.md').write_text(text,encoding='utf-8')
    body=extract_primary_draft(text).strip()
    if len(body)<1800: raise RuntimeError(f'chapter {n} body too short {len(body)}')
    bad=['# Curator Audit','# Curated Chapter Context','# Writer Audit','# 章节事实摘要']
    if any(x in body for x in bad): raise RuntimeError(f'chapter {n} body has pipeline leakage')
    path=EXP/'chapters'/f'chapter-{n:04d}.md'; path.write_text(body,encoding='utf-8')
    print('body',n,'chars',len(body),path)

def make_state(n:int):
    b=book(); recent=recent_summaries(b); body=(EXP/'chapters'/f'chapter-{n:04d}.md').read_text(encoding='utf-8')
    prompt=generate_prompt(mode='state_delta',template='',book_content=b,recent_summaries=recent,chapter_number=n,chapter_prose=body)
    p=run_dir(n)/'state_prompt.md'; p.write_text(prompt,encoding='utf-8'); print(p)

def apply_state(n:int):
    rd=run_dir(n); text=load_json_text(rd/'state_acp.json'); (rd/'state_response.md').write_text(text,encoding='utf-8')
    b=book(); updated=apply_state_delta_to_book(b,n,text); (EXP/'BOOK.md').write_text(updated,encoding='utf-8')
    print('state applied',n,'book chars',len(updated))

if __name__=='__main__':
    action=sys.argv[1]
    if action=='prepare': prepare()
    else:
        n=int(sys.argv[2])
        {'director':make_director,'curator':make_curator,'primary':make_primary,'body':extract_body,'state':make_state,'apply':apply_state,'materialize':None}.get(action,lambda *_:None)(n) if action!='materialize' else materialize(n,sys.argv[3])
