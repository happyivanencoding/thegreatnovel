from pathlib import Path
import json
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.character_prompts import generate_split_prompt
root=Path(r"books/real-exp-private-prototype-upstream-20260826-traditional-v1")
direction=(root/'AUTHOR_DIRECTION.md').read_text(encoding='utf-8')
r=retrieve_gbrain(mode='world_vision',creative_direction=direction)
meta={k:v for k,v in r.items() if k not in {'raw_stdout','result','accepted','novel_candidates','raw_results','rejected'}}
meta['accepted']=[{'slug':x['slug'],'score':x['score']} for x in r['accepted']]
(root/'WORLD_RETRIEVAL_META.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'WORLD_GBRAIN.md').write_text(r['result'],encoding='utf-8')
p=generate_split_prompt(mode='world_vision',creative_direction=direction,gbrain_inspiration=r['result'])
(root/'WORLD_PROMPT.md').write_text(p,encoding='utf-8')
print('accepted',[(x['slug'],x['score']) for x in r['accepted']])
print('prompt chars',len(p))
