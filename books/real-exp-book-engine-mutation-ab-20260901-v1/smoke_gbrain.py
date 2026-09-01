from __future__ import annotations

import sys
sys.path.insert(0, r"C:\dev\tgn-story-mvp\src")

from story_mvp.gbrain_retrieval import retrieve_gbrain
from pathlib import Path

QUERIES = (
    '"thread ecology" OR "plot advancing"',
    '"story state compounding" OR "Local Closure"',
    '"plot engine variation" OR "Decision Vector"',
    '"reward afterlife" OR "reward recontextualization"',
)

for query in QUERIES:
    result = retrieve_gbrain(
        mode="story_refresh",
        creative_direction="长篇人物选择与历史复利",
        world_vision="玄幻世界",
        character_card="人物有多个私人欲望",
        query_override=query,
    )
    slugs = [item["slug"] for item in result["accepted"]]
    print(f"=== {query} ===")
    print(slugs)
    assert not any("gbrain-longform-spine-tension" in slug for slug in slugs)

book = Path(r"C:\dev\tgn-story-mvp\books\real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1")
default_result = retrieve_gbrain(
    mode="story_refresh",
    book_content=(book / "BOOK_AFTER_CH20.md").read_text(encoding="utf-8"),
    creative_direction="《我身藏诸界》第21—30章继续无主兵荒原；保留人物选择、跨世界复利与主世界后果。",
    world_vision=(book / "WORLD_VISION.md").read_text(encoding="utf-8"),
    character_card=(book / "CHARACTER.md").read_text(encoding="utf-8"),
    proposal_context=(book / "STORY_PROGRAM_11_20.md").read_text(encoding="utf-8"),
)
default_slugs = [item["slug"] for item in default_result["accepted"]]
print("=== production-default story_refresh ===")
print(default_slugs)
assert len(default_slugs) == 3
assert "mechanisms/plot-engine-variation-v3" in default_slugs
assert any(slug in default_slugs for slug in ("mechanisms/thread-collision-v3", "mechanisms/longitudinal-thread-dormancy-collision-afterlife-v3", "mechanisms/thread-ecology-v3"))
