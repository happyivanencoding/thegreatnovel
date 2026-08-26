from pathlib import Path
from story_mvp.gbrain_retrieval import retrieve_gbrain, human_lane_for_page
world=Path('books/real-exp-human-gbrain-v1-ab-20260826-v1/WORLD_VISION.md').read_text(encoding='utf-8')
r=retrieve_gbrain(mode='human_seed',world_vision=world)
print('strategy',r['query_strategy'])
print('queries')
for q in r['query_texts']: print(' ',q)
print('raw',r['raw_count'],'accepted',r['accepted_count'],'lane_counts',r['human_lane_counts'])
for i,x in enumerate(r['accepted'],1): print(i,x.get('human_lane'),x['slug'],x['score'])
print('--- lane mismatch/relevant rejections ---')
for x in r['rejected']:
    if 'Human Craft' in x['reason'] or 'active inspiration' in x['reason']:
        print(x)
print('--- bundle ---')
print(r['result'])
