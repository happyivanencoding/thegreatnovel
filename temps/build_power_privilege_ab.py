from __future__ import annotations
import json, shutil, sys
from pathlib import Path

ROOT=Path(r'C:\dev\tgn-story-mvp')
SRC=ROOT/'books'/'real-exp-private-prototype-fresh-novel-20260826-v1'
EXP=ROOT/'books'/'real-exp-power-spark-privilege-20260826-v1'
sys.path.insert(0,str(ROOT/'src'))

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.power_novelty import build_power_novelty_bundle

EXP.mkdir(parents=True,exist_ok=True)
world=(SRC/'WORLD_VISION.md').read_text(encoding='utf-8')
direction=(SRC/'AUTHOR_DIRECTION.md').read_text(encoding='utf-8')
(EXP/'WORLD_FROZEN.md').write_text(world,encoding='utf-8')
(EXP/'AUTHOR_DIRECTION_FROZEN.md').write_text(direction,encoding='utf-8')

novelty=build_power_novelty_bundle(seed=20260826)
(EXP/'POWER_NOVELTY_FIXED.md').write_text(novelty,encoding='utf-8')
ret=retrieve_gbrain(mode='power_seed',creative_direction=direction,world_vision=world)
(EXP/'POWER_GBRAIN.md').write_text(ret['result'],encoding='utf-8')
(EXP/'POWER_RETRIEVAL_META.json').write_text(json.dumps({
    'query_strategy':ret.get('query_strategy'),
    'query_texts':ret.get('query_texts'),
    'accepted_count':ret.get('accepted_count'),
    'accepted':[{'slug':x.get('slug'),'score':x.get('score')} for x in ret.get('accepted',[])],
    'final_limit':ret.get('final_limit'),
},ensure_ascii=False,indent=2),encoding='utf-8')

p=generate_split_prompt(
    mode='power_seed',
    creative_direction=direction,
    world_vision=world,
    creative_state={'world_vision':{'status':'author_approved'}},
    gbrain_inspiration=ret['result'],
    power_novelty=novelty,
)
(EXP/'PROMPT_B_PRIVILEGE.md').write_text(p,encoding='utf-8')

# Causal baseline: identical World / GBrain / Spark / schema/model; remove only the
# new Privilege Delta / cross-tier / compoundability guidance added in this change.
lines=[]
for line in p.splitlines():
    if line.startswith('- **Novelty ≠ Power Fantasy 强度。**'):
        continue
    if line.startswith('- 允许并鼓励有条件的越级威胁、'):
        continue
    if line.startswith('- 这是男频成长长篇：正常修炼必须真实增强持有者本身；Exception 的掌握同时继续质变，不是外挂替代修炼。核心异常还应能与后续功法、'):
        line='- 这是男频成长长篇：正常修炼必须真实增强持有者本身；Exception 的掌握同时继续质变，不是外挂替代修炼。'
    lines.append(line)
a='\n'.join(lines).strip()+'\n'
(EXP/'PROMPT_A_SPARK_ONLY.md').write_text(a,encoding='utf-8')
(EXP/'PROTOCOL.md').write_text('''# Power Spark × Privilege Delta A/B\n\n- Frozen World: fresh private-prototype World Vision from ec58672.\n- Same Power GBrain bundle for A/B.\n- Same deterministic Novelty Spark bundle, seed 20260826.\n- Same model: GPT-5.6 Luna high, fresh sessions.\n- A: current Spark mechanism without new Privilege Delta / cross-tier / compoundability guidance.\n- B: Spark + new Privilege Delta / conditional cross-tier / compoundability guidance.\n- No Human / Character / Story Program visible.\n- Compare all 3 candidates, no cherry-picking.\n''',encoding='utf-8')
print(json.dumps({
    'exp':str(EXP),
    'sparks':[line for line in novelty.splitlines() if line.startswith('内部标签：')],
    'accepted':[x.get('slug') for x in ret.get('accepted',[])],
    'a_chars':len(a),'b_chars':len(p)
},ensure_ascii=False,indent=2))
