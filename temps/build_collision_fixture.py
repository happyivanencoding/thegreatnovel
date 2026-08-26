from pathlib import Path
import json, re, sys

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.character_seeds import compose_character_card, split_human_seed_authorities
from story_mvp.gbrain_retrieval import retrieve_gbrain

root = Path(sys.argv[1])
world = (root / "WORLD_VISION.md").read_text(encoding="utf-8")
direction = (root / "AUTHOR_DIRECTION.md").read_text(encoding="utf-8")
powers = (root / "POWER_SEEDS.md").read_text(encoding="utf-8")
human = (root / "HUMAN_SEED.md").read_text(encoding="utf-8")

m = re.search(r"(?ms)# POWER CANDIDATE 1｜(.+?)\n(.*?)(?=^---\s*$|^# POWER CANDIDATE 2｜|\Z)", powers)
if not m:
    raise SystemExit("POWER CANDIDATE 1 not found")
name = m.group(1).strip()
body = m.group(2).strip()
selected = f"# POWER SEED｜{name}\n{body}\n"
(root / "POWER_SELECTED_EXPERIMENTAL.md").write_text(selected, encoding="utf-8")

human_parts = split_human_seed_authorities(human)
character = compose_character_card(power_seed=selected, human_seed=human)
(root / "CHARACTER_EXPERIMENTAL.md").write_text(character, encoding="utf-8")
(root / "CHARACTER_INITIAL_STATE_EXPERIMENTAL.md").write_text(human_parts["initial_state"], encoding="utf-8")

protocol = """# Collision Experimental Protocol

- This is an experiment fixture, NOT author approval and NOT production Canon.
- Power selection rule was fixed before reading downstream Collision quality: always choose ordinal POWER CANDIDATE 1.
- The same ordinal rule is used for both v3 and traditional-control worlds; no cherry-picking.
- Human Seed is the already-fixed explicit anonymous prototype projection.
- CHARACTER is deterministic composition; no Character Composer LLM.
- Story Program is the first stage allowed to see Full World + Full Character + T0 state.
- Story Program uses GPT-5.6 Sol high with normal Story GBrain retrieval (max 3).
"""
(root / "COLLISION_PROTOCOL.md").write_text(protocol, encoding="utf-8")

ret = retrieve_gbrain(
    mode="idea",
    creative_direction=direction,
    world_vision=world,
    character_card=character,
)
(root / "STORY_GBRAIN.md").write_text(ret["result"], encoding="utf-8")
(root / "STORY_RETRIEVAL_META.json").write_text(
    json.dumps(
        {
            "query_strategy": ret.get("query_strategy"),
            "query_texts": ret.get("query_texts"),
            "accepted_count": ret.get("accepted_count"),
            "accepted": [{"slug": x["slug"], "score": x["score"]} for x in ret.get("accepted", [])],
            "final_limit": ret.get("final_limit"),
        },
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)
state = {
    "world_vision": {"status": "author_approved"},
    "character_card": {"status": "author_approved"},
}
prompt = generate_split_prompt(
    mode="idea",
    creative_direction=direction,
    world_vision=world,
    character_card=character,
    character_initial_state=human_parts["initial_state"],
    creative_state=state,
    gbrain_inspiration=ret["result"],
)
(root / "STORY_PROGRAM_PROMPT.md").write_text(prompt, encoding="utf-8")
print(json.dumps({"root": str(root), "power_selected": name, "story_gbrain_accepted": ret.get("accepted_count"), "prompt_chars": len(prompt)}, ensure_ascii=False))
