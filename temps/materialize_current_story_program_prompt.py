from pathlib import Path
import sys

from story_mvp.character_prompts import generate_split_prompt

root = Path(sys.argv[1])
blind = len(sys.argv) > 2 and sys.argv[2] == "blind"
world = (root / "WORLD_VISION.md").read_text(encoding="utf-8")
direction = (root / "AUTHOR_DIRECTION.md").read_text(encoding="utf-8")
character = (root / ("CHARACTER_BLIND_SELECTED.md" if blind else "CHARACTER_EXPERIMENTAL.md")).read_text(encoding="utf-8")
state = (root / ("CHARACTER_INITIAL_STATE_BLIND.md" if blind else "CHARACTER_INITIAL_STATE_EXPERIMENTAL.md")).read_text(encoding="utf-8")
gbrain = (root / ("STORY_GBRAIN_BLIND.md" if blind else "STORY_GBRAIN.md")).read_text(encoding="utf-8")

prompt = generate_split_prompt(
    mode="idea",
    creative_direction=direction,
    world_vision=world,
    character_card=character,
    character_initial_state=state,
    creative_state={
        "world_vision": {"status": "author_approved"},
        "character_card": {"status": "author_approved"},
    },
    gbrain_inspiration=gbrain,
)
name = "STORY_PROGRAM_CURRENT_PRODUCTION_BLIND_PROMPT.md" if blind else "STORY_PROGRAM_CURRENT_PRODUCTION_PROMPT.md"
(root / name).write_text(prompt, encoding="utf-8")
print(f"{root} blind={blind} prompt_chars={len(prompt)}")
