from pathlib import Path
import json

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.gbrain_retrieval import retrieve_gbrain

root = Path(r"books/real-exp-private-prototype-upstream-20260826-traditional-v1")
world = (root / "WORLD_VISION.md").read_text(encoding="utf-8")
ret = retrieve_gbrain(mode="human_seed", world_vision=world)
prompt = generate_split_prompt(
    mode="human_seed",
    world_vision=world,
    creative_state={"world_vision": {"status": "author_approved"}},
    gbrain_inspiration=ret["result"],
)
(root / "HUMAN_STANDARD_GBRAIN.md").write_text(ret["result"], encoding="utf-8")
(root / "HUMAN_STANDARD_PROMPT.md").write_text(prompt, encoding="utf-8")
(root / "HUMAN_STANDARD_RETRIEVAL_META.json").write_text(
    json.dumps({
        "query_strategy": ret.get("query_strategy"),
        "query_texts": ret.get("query_texts"),
        "accepted_count": ret.get("accepted_count"),
        "accepted": [
            {"slug": x["slug"], "score": x["score"], "human_lane": x.get("human_lane")}
            for x in ret.get("accepted", [])
        ],
        "final_limit": ret.get("final_limit"),
    }, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(json.dumps({"accepted": ret.get("accepted_count"), "prompt_chars": len(prompt)}, ensure_ascii=False))
