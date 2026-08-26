from pathlib import Path
import json, hashlib
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.gbrain import get_gbrain

root = Path('books/real-exp-private-prototype-upstream-20260826-v1')
root.mkdir(parents=True, exist_ok=True)

direction = '''成熟中文男频幻想成长长篇。全新虚构世界，主角长期真正变强。世界先于主角成立，不围绕未来主角定制锁孔；优先具体力量、奇观、强敌、价值物、关系与可探索空间，避免工程化、制度化、项目管理化叙事成为主发动机。不要预设主角现实履历、现代职业或现实身份。'''

world_ret = retrieve_gbrain(mode='world_vision', creative_direction=direction)
world_prompt = generate_split_prompt(
    mode='world_vision',
    creative_direction=direction,
    gbrain_inspiration=world_ret['result'],
)
(root/'AUTHOR_DIRECTION.md').write_text(direction, encoding='utf-8')
(root/'WORLD_GBRAIN.md').write_text(world_ret['result'], encoding='utf-8')
(root/'WORLD_RETRIEVAL_META.json').write_text(json.dumps({
    k: world_ret[k] for k in ['query_strategy','query_texts','accepted_count','accepted','final_limit']
}, ensure_ascii=False, indent=2), encoding='utf-8')
(root/'WORLD_PROMPT.md').write_text(world_prompt, encoding='utf-8')

# Explicit prototype bundle; default retrieval is intentionally bypassed.
prototype_slugs = [
    'book-dna/private-prototype-pwaalpha-appetite-v1',
    'book-dna/private-prototype-pwaalpha-choice-bias-v1',
    'book-dna/private-prototype-pwaalpha-relationship-v1',
]
blocks=[]
for i,slug in enumerate(prototype_slugs,1):
    page=get_gbrain(slug)
    # Runtime explicit-selector experiment intentionally uses full abstract card body,
    # but no private source pages or opaque evidence resolution.
    blocks.append(f'### Prototype Inspiration {i}\nsource: {slug}\n\n{page}')
(root/'EXPLICIT_PROTOTYPE_GBRAIN.md').write_text('\n\n'.join(blocks), encoding='utf-8')
(root/'PROTOCOL.md').write_text('''# Protocol\n\n- Anonymous prototype: prism-wanderer-alpha\n- World: prototype OFF\n- Power: prototype OFF\n- Human: explicit prototype selector ON (Appetite/Behavior/Relationship, one each)\n- No real name/location/employer/private source text may enter artifacts.\n- Power/Human generated in fresh independent contexts.\n- No Character Composer.\n- No Sol until author chooses a Power candidate.\n''', encoding='utf-8')
print(root)
print('world prompt chars', len(world_prompt), 'gbrain accepted', world_ret['accepted_count'])
print('prototype slugs', prototype_slugs)
