from pathlib import Path
from story_mvp.gbrain_retrieval import retrieve_gbrain
life = Path('books/real-exp-human-gbrain-v1-ab-20260826-v1/LIFE_CONTEXT.md').read_text(encoding='utf-8')
# Feed this as world_vision is wrong because function will project headings again; use original world vision.
world = Path('books/real-exp-human-gbrain-v1-ab-20260826-v1/WORLD_VISION.md').read_text(encoding='utf-8')
r = retrieve_gbrain(mode='human_seed', world_vision=world)
print('strategy', r['query_strategy'])
print('queries', r['query_texts'])
print('raw', r['raw_count'], 'accepted', r['accepted_count'], 'final_limit', r['final_limit'])
for i,x in enumerate(r['accepted'],1): print(i, x['slug'], x['score'], x.get('card_type'), x.get('title',''))
print('rejected human-ish')
for x in r['rejected']:
    if any(k in x['slug'] for k in ['human','appetite','character','relationship']): print(x)
