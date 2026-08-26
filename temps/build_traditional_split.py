from pathlib import Path
import json, re

from story_mvp.character_context import project_character_life_context, project_character_power_baseline
from story_mvp.character_prompts import HUMAN_PROMPT, generate_split_prompt
from story_mvp.gbrain_retrieval import retrieve_gbrain

root = Path(r"books/real-exp-private-prototype-upstream-20260826-traditional-v1")
world = (root / "WORLD_VISION.md").read_text(encoding="utf-8")
source_bundle = Path(r"books/real-exp-private-prototype-upstream-20260826-v3/EXPLICIT_ANON_HUMAN_BUNDLE.md")
bundle = source_bundle.read_text(encoding="utf-8")
(root / "EXPLICIT_ANON_HUMAN_BUNDLE.md").write_text(bundle, encoding="utf-8")

state = {"world_vision": {"status": "author_approved"}}
power_ret = retrieve_gbrain(mode="power_seed", world_vision=world)
power_prompt = generate_split_prompt(
    mode="power_seed",
    world_vision=world,
    creative_state=state,
    gbrain_inspiration=power_ret["result"],
)
(root / "POWER_BASELINE.md").write_text(project_character_power_baseline(world), encoding="utf-8")
(root / "POWER_GBRAIN.md").write_text(power_ret["result"], encoding="utf-8")
(root / "POWER_PROMPT.md").write_text(power_prompt, encoding="utf-8")
(root / "POWER_RETRIEVAL_META.json").write_text(
    json.dumps(
        {
            "query_strategy": power_ret.get("query_strategy"),
            "query_texts": power_ret.get("query_texts"),
            "accepted_count": power_ret.get("accepted_count"),
            "accepted": [{"slug": x["slug"], "score": x["score"]} for x in power_ret.get("accepted", [])],
            "final_limit": power_ret.get("final_limit"),
        },
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

life = project_character_life_context(world)
(root / "HUMAN_LIFE_CONTEXT.md").write_text(life, encoding="utf-8")
old = "生成 4 个独立候选，不评分、不排名。先保证每个人自身成立，再避免明显心理运动坍缩；不要为了多样性机械分配人格类型。\n\n每个候选使用：\n\n# HUMAN CANDIDATE N｜姓名／短标签"
new = "这是显式匿名原型实验，不再搜索人物分布。只生成 **1 个** fictionalized Human Seed：三条匿名 prototype lane 是人物内核权威，但表层身份、家庭、职业、关系对象与具体欲望对象必须在当前幻想世界重新出生。不要生成多个版本，不评分，不替未来 Power 做适配。\n\n严格使用：\n\n# HUMAN SEED｜幻想姓名／短标签"
human_contract = HUMAN_PROMPT.replace(old, new).replace(
    "作者选择时会把一个候选编辑成单独的 `# HUMAN SEED`；不要替作者选择。",
    "这是已显式选择的匿名 prototype；直接输出一份 `# HUMAN SEED`，不要再让作者从多个 Human 候选中选择。",
)
human_prompt = "\n\n".join(
    [human_contract.strip(), life.strip(), "# Explicit Anonymous Human Prototype Selector\n\n" + bundle.strip()]
) + "\n"
(root / "HUMAN_PROMPT.md").write_text(human_prompt, encoding="utf-8")

prototype_terms = ["prism-wanderer-alpha", "pwaalpha", "情欲与肉体吸引", "Stable Choice Bias"]
story_names = ["赤脉山", "白骨雪原", "太玄宗", "黑日岛", "西州灵雨", "九檐仙山", "万灯河", "断天门"]
checks = {
    "power_prompt_prototype_hits": {t: power_prompt.count(t) for t in prototype_terms},
    "human_prompt_expected_bundle_hits": {t: human_prompt.count(t) for t in prototype_terms},
    "life_context_named_story_hits": {t: life.count(t) for t in story_names},
    "power_prompt_named_human_seed_hits": 0,
    "power_gbrain_accepted": power_ret.get("accepted_count", 0),
    "power_prompt_chars": len(power_prompt),
    "human_prompt_chars": len(human_prompt),
    "life_context_chars": len(life),
}
(root / "PRE_RUN_ISOLATION_CHECKS.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding="utf-8")

bad = {k: v for k, v in checks["power_prompt_prototype_hits"].items() if v}
bad_story = {k: v for k, v in checks["life_context_named_story_hits"].items() if v}
print(json.dumps(checks, ensure_ascii=False, indent=2))
if bad:
    raise SystemExit(f"Power prompt leaked Human prototype terms: {bad}")
if bad_story:
    raise SystemExit(f"LIFE_CONTEXT leaked named Story Opportunities: {bad_story}")
print("PRE_RUN_ISOLATION_PASS")
