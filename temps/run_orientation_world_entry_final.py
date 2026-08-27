from __future__ import annotations
import importlib.util, json, re, sys
from pathlib import Path
ROOT=Path(r'C:\dev\tgn-story-mvp')
EXP=ROOT/'books'/'real-exp-private-prototype-orientation-world-entry-final-20260827-v1'
BASELINE=ROOT/'books'/'real-exp-private-prototype-asymmetry-pace-ruler-20260827-v1'
sys.path.insert(0,str(ROOT/'src'))
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.hybrid_runtime import extract_primary_draft
from story_mvp.storage import validate_book_content_for_save, validate_chapter_body_for_save
spec=importlib.util.spec_from_file_location('base',ROOT/'temps'/'run_private_asymmetry_e2e.py')
base=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(base); base.EXP=EXP

def world(): return (EXP/'WORLD_VISION.md').read_text(encoding='utf-8')
def book(): return (EXP/'BOOK.md').read_text(encoding='utf-8')
def sections(): return base.parse_book_sections(book())
def recent(): return base.parse_canon_memory(sections()['status']).get('recent_summaries','').strip()
def prev(n): return '' if n<=1 else (EXP/'chapters'/f'chapter-{n-1:04d}.md').read_text(encoding='utf-8')
def chapter_plan(n):
 s=sections()['small_plan']; m=re.search(rf'(?ms)^## 第{n}章：.*?(?=^## 第{n+1}章：|\Z)',s)
 if not m:
  raise RuntimeError(f'missing ch {n}')
 return m.group(0).strip()
def long_block(n):
 s=sections()['long_plan']
 for m in re.finditer(r'(?ms)^## 第(\d+)[—-](\d+)章：.*?(?=^## 第\d+[—-]\d+章：|\Z)',s):
  if int(m.group(1))<=n<=int(m.group(2)): return m.group(0).strip()
 return s[:7000].strip()
def rd(n):
 p=EXP/'runs'/f'chapter-{n:04d}'; p.mkdir(parents=True,exist_ok=True); return p
def save(n,stage,text): (rd(n)/f'{stage}_prompt.md').write_text(text,encoding='utf-8')

def outline_prompt():
 p=generate_split_prompt(mode='outline',creative_direction=(EXP/'AUTHOR_DIRECTION.md').read_text(encoding='utf-8'),world_vision=world(),character_card=(EXP/'CHARACTER.md').read_text(encoding='utf-8'),character_initial_state=(EXP/'CHARACTER_INITIAL_STATE.md').read_text(encoding='utf-8'),creative_state={'world_vision':{'status':'author_approved'},'character_card':{'status':'author_approved'},'proposal':{'status':'author_approved'}},proposal_context=(EXP/'STORY_PROGRAM.md').read_text(encoding='utf-8'),gbrain_inspiration=(EXP/'OUTLINE_GBRAIN.md').read_text(encoding='utf-8'))
 (EXP/'OUTLINE_PROMPT.md').write_text(p,encoding='utf-8'); print(json.dumps({'chars':len(p)},ensure_ascii=False))
def mat_outline():
 d=base.load_acp(EXP/'OUTLINE_ACP.json'); t=base.clean_model_text(d['text']); pos=t.find('# 小说总体设计画像'); t=t[pos:] if pos>=0 else t; validate_book_content_for_save(t); (EXP/'OUTLINE.md').write_text(t+'\n',encoding='utf-8'); (EXP/'BOOK.md').write_text(t+'\n',encoding='utf-8'); print(json.dumps({'chars':len(t)},ensure_ascii=False))
def director(n):
 p=base.generate_prompt(mode='director',template='',book_content=book(),world_vision=world(),current_long_block=long_block(n),previous_chapter_text=prev(n),current_outline='',current_chapter_plan=chapter_plan(n),recent_summaries=recent(),chapter_number=n,creative_direction='严格执行当前批准 World/Character/Story Program/Outline。WORLD AUTHORITY 是世界事实权威；Reader Release Map 决定首次释放。保留 State Advance、Ruler Compression、Choice→Consequence、主人公连续升格。决定后的普通实施默认压缩。')
 save(n,'director',p)
def curator(n):
 dr=(rd(n)/'director_response.md').read_text(encoding='utf-8'); ret=base.retrieve_gbrain(mode='context_curator',book_content=book(),current_long_block=long_block(n),current_outline=dr,recent_summaries=recent()); base.dump_meta(rd(n)/'curator_retrieval.json',{k:v for k,v in ret.items() if k not in {'raw_stdout','result'}}); (rd(n)/'scene_skill.md').write_text(ret['result'],encoding='utf-8'); p=base.generate_prompt(mode='context_curator',template='',book_content=book(),world_vision=world(),current_long_block=long_block(n),previous_chapter_text=prev(n),current_outline=dr,current_chapter_plan=chapter_plan(n),recent_summaries=recent(),gbrain_inspiration=ret['result'],chapter_number=n); save(n,'curator',p); print(json.dumps({'accepted':[x.get('slug') for x in ret.get('accepted',[])]},ensure_ascii=False))
def primary(n):
 dr=(rd(n)/'director_response.md').read_text(encoding='utf-8'); cu=(rd(n)/'curator_response.md').read_text(encoding='utf-8'); sk=(rd(n)/'scene_skill.md').read_text(encoding='utf-8'); p=base.generate_prompt(mode='primary_writer',template='',book_content=book(),world_vision=world(),current_long_block=long_block(n),previous_chapter_text=prev(n),current_outline=dr,current_chapter_plan=chapter_plan(n),recent_summaries=recent(),gbrain_inspiration=sk,curated_context=cu,chapter_number=n); save(n,'primary',p)
def mat(n,stage): base.materialize(n,stage)
def body(n):
 d=base.load_acp(rd(n)/'primary_acp.json'); raw=base.clean_model_text(d['text']); (rd(n)/'primary_response.md').write_text(raw+'\n',encoding='utf-8'); t=extract_primary_draft(raw).strip(); validate_chapter_body_for_save(t);
 if len(t)<1000: raise RuntimeError(f'too short {n}: {len(t)}')
 (EXP/'chapters'/f'chapter-{n:04d}.md').write_text(t+'\n',encoding='utf-8'); print(json.dumps({'chapter':n,'chars':len(t)},ensure_ascii=False))
def state(n): base.state(n)
def apply(n): base.apply_state(n)
def combine():
 out=[]; titled=[]; outline=(EXP/'OUTLINE.md').read_text(encoding='utf-8'); titles={int(m.group(1)):m.group(2).strip() for m in re.finditer(r'(?m)^## 第(\d+)章：(.+)$',outline)}
 for n in range(1,6):
  t=(EXP/'chapters'/f'chapter-{n:04d}.md').read_text(encoding='utf-8').strip(); out.append(t); titled.append(f'第{n}章 {titles.get(n,"")}\n\n{t}')
 (EXP/'READER_COPY_0001_0005.txt').write_text('\n\n'.join(out)+'\n',encoding='utf-8'); (EXP/'READER_COPY_0001_0005_TITLED.txt').write_text('\n\n'.join(titled)+'\n',encoding='utf-8'); print(json.dumps({'chars':[len(x) for x in out],'total':sum(map(len,out))},ensure_ascii=False))
def metrics():
 old=[(BASELINE/'chapters'/f'chapter-{n:04d}.md').read_text(encoding='utf-8') for n in range(1,6)]; new=[(EXP/'chapters'/f'chapter-{n:04d}.md').read_text(encoding='utf-8') for n in range(1,6)]
 terms=['猎墙','普通人','商队','独行','外面','荒原部族','部族','白角部','三排','药车','缰绳','推车','二阶','无阶','王种']
 d={'old_chars':[len(x) for x in old],'new_chars':[len(x) for x in new],'old_total':sum(map(len,old)),'new_total':sum(map(len,new)),'term_counts':{term:{'old':sum(x.count(term) for x in old),'new':sum(x.count(term) for x in new)} for term in terms}}
 (EXP/'METRICS.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(d,ensure_ascii=False,indent=2))
a=sys.argv[1]
if a=='outline-prompt': outline_prompt()
elif a=='mat-outline': mat_outline()
elif a=='director': director(int(sys.argv[2]))
elif a=='curator': curator(int(sys.argv[2]))
elif a=='primary': primary(int(sys.argv[2]))
elif a=='mat': mat(int(sys.argv[2]),sys.argv[3])
elif a=='body': body(int(sys.argv[2]))
elif a=='state': state(int(sys.argv[2]))
elif a=='apply': apply(int(sys.argv[2]))
elif a=='combine': combine()
elif a=='metrics': metrics()
else: raise SystemExit(a)
