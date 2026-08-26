from pathlib import Path
import json, re
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.gbrain_retrieval import retrieve_gbrain
root=Path('books/real-exp-private-prototype-upstream-20260826-v1')
world_json=json.loads((root/'WORLD_ACP.json').read_text(encoding='utf-8'))
world=world_json['text'].strip()
(root/'WORLD_VISION.md').write_text(world+'\n',encoding='utf-8')

direction=(root/'AUTHOR_DIRECTION.md').read_text(encoding='utf-8')
# Production Power retrieval only sees projected power baseline internally.
power_ret=retrieve_gbrain(mode='power_seed',creative_direction=direction,world_vision=world)
power_prompt=generate_split_prompt(mode='power_seed',creative_direction=direction,world_vision=world,creative_state={'world_vision':{'status':'author_approved'}},gbrain_inspiration=power_ret['result'])
(root/'POWER_GBRAIN.md').write_text(power_ret['result'],encoding='utf-8')
(root/'POWER_RETRIEVAL_META.json').write_text(json.dumps({k:power_ret[k] for k in ['query_strategy','query_texts','accepted_count','accepted','final_limit']},ensure_ascii=False,indent=2),encoding='utf-8')
(root/'POWER_PROMPT.md').write_text(power_prompt,encoding='utf-8')

# Human explicit-prototype bundle. Full private source text is never used; only the three anonymized cards.
proto=(root/'EXPLICIT_PROTOTYPE_GBRAIN.md').read_text(encoding='utf-8')
human_prompt=generate_split_prompt(mode='human_seed',creative_direction=direction,world_vision=world,creative_state={'world_vision':{'status':'author_approved'}},gbrain_inspiration=proto)
(root/'HUMAN_PROMPT.md').write_text(human_prompt,encoding='utf-8')

# hard isolation checks on prompts
proto_markers=['pwaalpha','prism-wanderer-alpha','情欲与肉体吸引','Stable Choice Bias']
checks={
 'world_proto_marker_hits':{m:world.count(m) for m in proto_markers},
 'power_prompt_proto_marker_hits':{m:power_prompt.count(m) for m in proto_markers},
 'human_prompt_has_three_selector_slugs':all(s in human_prompt for s in ['private-prototype-pwaalpha-appetite-v1','private-prototype-pwaalpha-choice-bias-v1','private-prototype-pwaalpha-relationship-v1']),
 'world_chars':len(world),'power_prompt_chars':len(power_prompt),'human_prompt_chars':len(human_prompt),
 'power_gbrain_accepted':power_ret['accepted_count'],
}
(root/'ISOLATION_CHECKS.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
print('\n--- WORLD HEADINGS ---')
for line in world.splitlines():
 if line.startswith('#'): print(line)
