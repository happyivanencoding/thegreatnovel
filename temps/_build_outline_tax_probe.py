from pathlib import Path
import json
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.character_prompts import generate_split_prompt
root = Path(r'C:\dev\tgn-story-mvp')
exp = root/'books'/'real-exp-private-prototype-upstream-20260826-traditional-v1'
read = lambda name: (exp/name).read_text(encoding='utf-8')
author = read('AUTHOR_DIRECTION.md')
world = read('WORLD_VISION.md')
character = read('CHARACTER_EXPERIMENTAL.md')
initial = read('CHARACTER_INITIAL_STATE_EXPERIMENTAL.md')
story = read('STORY_PROGRAM_CURRENT_PRODUCTION.md')
ret = retrieve_gbrain(mode='outline', creative_direction=author, world_vision=world, character_card=character, proposal_context=story)
(exp/'OUTLINE_CURRENT_GBRAIN.md').write_text(ret['result'], encoding='utf-8')
meta = {k:v for k,v in ret.items() if k not in {'raw_stdout','novel_candidates','raw_results','accepted','rejected','result'}}
meta['accepted'] = [{k:v for k,v in x.items() if k in {'slug','score','type','is_genre_prior','transfer_boundary'}} for x in ret['accepted']]
meta['rejected'] = ret['rejected']
(exp/'OUTLINE_CURRENT_RETRIEVAL_META.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
prompt = generate_split_prompt(mode='outline', creative_direction=author, world_vision=world, character_card=character, character_initial_state=initial, proposal_context=story, book_content='', creative_state={'world_vision':{'status':'author_approved'},'character_card':{'status':'author_approved'},'proposal':{'status':'author_approved'}}, selected_references=[], gbrain_inspiration=ret['result'])
(exp/'OUTLINE_CURRENT_PROMPT.md').write_text(prompt, encoding='utf-8')
print(json.dumps({'accepted_count':ret['accepted_count'],'accepted_slugs':[x['slug'] for x in ret['accepted']], 'prompt_chars':len(prompt), 'gbrain_chars':len(ret['result'])}, ensure_ascii=False, indent=2))
