from pathlib import Path
import json, re, sys

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.character_seeds import compose_character_card, split_human_seed_authorities
from story_mvp.gbrain_retrieval import retrieve_gbrain

root = Path(sys.argv[1])
index = int(sys.argv[2])
world = (root / "WORLD_VISION.md").read_text(encoding="utf-8")
direction = (root / "AUTHOR_DIRECTION.md").read_text(encoding="utf-8")
powers = (root / "POWER_SEEDS.md").read_text(encoding="utf-8")
human = (root / "HUMAN_SEED.md").read_text(encoding="utf-8")

next_index = index + 1
pat = rf"(?ms)# POWER CANDIDATE {index}｜(.+?)\n(.*?)(?=^---\s*$|^# POWER CANDIDATE {next_index}｜|\Z)"
m = re.search(pat, powers)
if not m:
    raise SystemExit(f"POWER CANDIDATE {index} not found")
name = m.group(1).strip()
body = m.group(2).strip()
selected = f"# POWER SEED｜{name}\n{body}\n"
human_parts = split_human_seed_authorities(human)
character = compose_character_card(power_seed=selected, human_seed=human)

(root / "POWER_SELECTED_BLIND.md").write_text(selected, encoding="utf-8")
(root / "CHARACTER_BLIND_SELECTED.md").write_text(character, encoding="utf-8")
(root / "CHARACTER_INITIAL_STATE_BLIND.md").write_text(human_parts["initial_state"], encoding="utf-8")

ret = retrieve_gbrain(
    mode="idea",
    creative_direction=direction,
    world_vision=world,
    character_card=character,
)
(root / "STORY_GBRAIN_BLIND.md").write_text(ret["result"], encoding="utf-8")
(root / "STORY_RETRIEVAL_META_BLIND.json").write_text(
    json.dumps({
        "selection_index": index,
        "selection_name": name,
        "query_strategy": ret.get("query_strategy"),
        "query_texts": ret.get("query_texts"),
        "accepted_count": ret.get("accepted_count"),
        "accepted": [{"slug": x["slug"], "score": x["score"]} for x in ret.get("accepted", [])],
        "final_limit": ret.get("final_limit"),
    }, ensure_ascii=False, indent=2),
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
(root / "STORY_PROGRAM_BLIND_SELECTED_PROMPT.md").write_text(prompt, encoding="utf-8")
(root / "COLLISION_BLIND_PROTOCOL.md").write_text(
    "# Blind-selected Collision Protocol\n\n"
    f"- Independent Power selector chose candidate {index}: {name}.\n"
    "- Selector saw World Power Baseline + anonymous Power candidates only; it did not see Human or Story Opportunities.\n"
    "- Character is deterministic Power/Human composition; no Character Composer.\n"
    "- Story Program is the first full collision and uses Sol high + normal Story GBrain.\n"
    "- This is an experiment fixture, not production Canon or author approval.\n",
    encoding="utf-8",
)
print(json.dumps({"root": str(root), "selected": f"{index}|{name}", "accepted": ret.get("accepted_count"), "prompt_chars": len(prompt)}, ensure_ascii=False))
