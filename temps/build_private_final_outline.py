from pathlib import Path
import json,sys
ROOT=Path(r'C:\dev\tgn-story-mvp')
EXP=ROOT/'books'/'real-exp-private-prototype-final-novel-20260826-v1'
sys.path.insert(0,str(ROOT/'src'))
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.gbrain_retrieval import retrieve_gbrain
read=lambda n:(EXP/n).read_text(encoding='utf-8')
ret=retrieve_gbrain(mode='outline', creative_direction=read('AUTHOR_DIRECTION.md'), world_vision=read('WORLD_VISION.md'), character_card=read('CHARACTER.md'), proposal_context=read('STORY_PROGRAM.md'))
(EXP/'OUTLINE_GBRAIN.md').write_text(ret['result'],encoding='utf-8')
(EXP/'OUTLINE_RETRIEVAL_META.json').write_text(json.dumps({k:v for k,v in ret.items() if k not in {'raw_stdout','result'}},ensure_ascii=False,indent=2),encoding='utf-8')
prompt=generate_split_prompt(mode='outline', template='', creative_direction=read('AUTHOR_DIRECTION.md'), world_vision=read('WORLD_VISION.md'), character_card=read('CHARACTER.md'), character_initial_state=read('CHARACTER_INITIAL_STATE.md'), proposal_context=read('STORY_PROGRAM.md'), book_content='', creative_state={'world_vision':{'status':'author_approved'},'character_card':{'status':'author_approved'},'proposal':{'status':'author_approved'}}, selected_references=[], gbrain_inspiration=ret['result'])
(EXP/'OUTLINE_PROMPT.md').write_text(prompt,encoding='utf-8')
print(json.dumps({'prompt_chars':len(prompt),'accepted':[x['slug'] for x in ret['accepted']], 'strategy':ret['query_strategy']},ensure_ascii=False))
