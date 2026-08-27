from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-private-prototype-asymmetry-novel-20260826-v2"
EXP = ROOT / "books" / "real-exp-private-prototype-asymmetry-pace-ruler-20260827-v1"
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.hybrid_runtime import extract_primary_draft
from story_mvp.storage import validate_book_content_for_save, validate_chapter_body_for_save

spec = importlib.util.spec_from_file_location("asym_e2e", ROOT / "temps" / "run_private_asymmetry_e2e.py")
base_runner = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(base_runner)
base_runner.EXP = EXP

FROZEN = [
    "AUTHOR_DIRECTION.md",
    "WORLD_VISION.md",
    "POWER_SEED.md",
    "HUMAN_SEED.md",
    "CHARACTER.md",
    "CHARACTER_INITIAL_STATE.md",
    "CHARACTER_AUDITION.md",
    "WORLD_GBRAIN.md",
    "STORY_GBRAIN.md",
    "OUTLINE_GBRAIN.md",
]


def init() -> None:
    if EXP.exists():
        raise RuntimeError(f"experiment already exists: {EXP}")
    EXP.mkdir(parents=True)
    (EXP / "chapters").mkdir()
    (EXP / "runs").mkdir()
    for name in FROZEN:
        shutil.copy2(BASE / name, EXP / name)
    (EXP / "PROTOCOL.md").write_text(
        "# Protocol｜Pacing + Reader Ruler Regression\n\n"
        "- Baseline: `real-exp-private-prototype-asymmetry-novel-20260826-v2`.\n"
        "- Freeze: Author Direction / World / Power / Human / Character and Story/Outline GBrain bundles.\n"
        "- Treatment: production commit `4344ef1` — Ruler=Compression + World benchmarks, State Advance After Proof, Choice→Consequence, Discriminative Detail Only, Plot Pace≠Tier Pace.\n"
        "- Rerun: Sol high Story Program → Luna high Outline → 5 serial chapters via Luna Director / Luna Curator / Terra Primary / Luna low State.\n"
        "- Separate World-only smoke uses the same Author Direction + frozen World GBrain to verify reusable benchmark generation; it is not novel authority.\n"
        "- Integration A/B of one coherent pacing/ruler package, not a one-variable causal decomposition.\n",
        encoding="utf-8",
    )
    author = (EXP / "AUTHOR_DIRECTION.md").read_text(encoding="utf-8")
    world = (EXP / "WORLD_VISION.md").read_text(encoding="utf-8")
    character = (EXP / "CHARACTER.md").read_text(encoding="utf-8")
    initial = (EXP / "CHARACTER_INITIAL_STATE.md").read_text(encoding="utf-8")

    world_smoke = generate_split_prompt(
        mode="world_vision",
        creative_direction=author,
        gbrain_inspiration=(EXP / "WORLD_GBRAIN.md").read_text(encoding="utf-8"),
    )
    (EXP / "WORLD_BENCHMARK_SMOKE_PROMPT.md").write_text(world_smoke, encoding="utf-8")

    story_prompt = generate_split_prompt(
        mode="idea",
        creative_direction=author,
        world_vision=world,
        character_card=character,
        character_initial_state=initial,
        creative_state={
            "world_vision": {"status": "author_approved"},
            "character_card": {"status": "author_approved"},
        },
        gbrain_inspiration=(EXP / "STORY_GBRAIN.md").read_text(encoding="utf-8"),
    )
    (EXP / "STORY_PROGRAM_PROMPT.md").write_text(story_prompt, encoding="utf-8")
    print(json.dumps({"exp": str(EXP), "world_smoke_chars": len(world_smoke), "story_prompt_chars": len(story_prompt)}, ensure_ascii=False))


def mat_world_smoke() -> None:
    text = base_runner.save_model_text(EXP / "WORLD_BENCHMARK_SMOKE_ACP.json", EXP / "WORLD_BENCHMARK_SMOKE.md")
    lines = [
        line.strip()
        for line in text.splitlines()
        if any(k in line for k in ("一阶", "二阶", "三阶", "四阶", "五阶", "六阶", "七阶", "八阶", "九阶", "普通", "价值", "排名"))
    ]
    (EXP / "WORLD_BENCHMARK_SMOKE_LINES.md").write_text("\n".join(lines[:100]) + "\n", encoding="utf-8")
    print(json.dumps({"world_smoke_chars": len(text), "candidate_benchmark_lines": len(lines)}, ensure_ascii=False))


def mat_story_build_outline() -> None:
    source = EXP / "STORY_PROGRAM_POSTCHANGE_ACP.json"
    if not source.exists():
        raise RuntimeError("post-change Story Program result is not ready")
    story = base_runner.save_model_text(source, EXP / "STORY_PROGRAM.md")
    prompt = generate_split_prompt(
        mode="outline",
        creative_direction=(EXP / "AUTHOR_DIRECTION.md").read_text(encoding="utf-8"),
        world_vision=(EXP / "WORLD_VISION.md").read_text(encoding="utf-8"),
        character_card=(EXP / "CHARACTER.md").read_text(encoding="utf-8"),
        character_initial_state=(EXP / "CHARACTER_INITIAL_STATE.md").read_text(encoding="utf-8"),
        creative_state={
            "world_vision": {"status": "author_approved"},
            "character_card": {"status": "author_approved"},
            "proposal": {"status": "author_approved"},
        },
        proposal_context=story,
        gbrain_inspiration=(EXP / "OUTLINE_GBRAIN.md").read_text(encoding="utf-8"),
    )
    (EXP / "OUTLINE_PROMPT.md").write_text(prompt, encoding="utf-8")
    print(json.dumps({"story_chars": len(story), "outline_prompt_chars": len(prompt)}, ensure_ascii=False))


def mat_outline() -> None:
    d = base_runner.load_acp(EXP / "OUTLINE_ACP.json")
    text = base_runner.clean_model_text(d["text"])
    pos = text.find("# 小说总体设计画像")
    if pos >= 0:
        text = text[pos:]
    validate_book_content_for_save(text)
    (EXP / "OUTLINE.md").write_text(text + "\n", encoding="utf-8")
    (EXP / "BOOK.md").write_text(text + "\n", encoding="utf-8")
    print(json.dumps({"outline_chars": len(text)}, ensure_ascii=False))


def body(n: int) -> None:
    d = base_runner.load_acp(base_runner.rd(n) / "primary_acp.json")
    raw = base_runner.clean_model_text(d["text"])
    (base_runner.rd(n) / "primary_response.md").write_text(raw + "\n", encoding="utf-8")
    text = extract_primary_draft(raw).strip()
    validate_chapter_body_for_save(text)
    if len(text) < 1000:
        raise RuntimeError(f"chapter {n} too short to form a complete scene: {len(text)}")
    (EXP / "chapters" / f"chapter-{n:04d}.md").write_text(text + "\n", encoding="utf-8")
    print(json.dumps({"chapter": n, "body_chars": len(text)}, ensure_ascii=False))


def combine() -> None:
    outline = (EXP / "OUTLINE.md").read_text(encoding="utf-8")
    titles = {int(m.group(1)): m.group(2).strip() for m in re.finditer(r"(?m)^## 第(\d+)章：(.+)$", outline)}
    raw, titled = [], []
    for n in range(1, 6):
        text = (EXP / "chapters" / f"chapter-{n:04d}.md").read_text(encoding="utf-8").strip()
        raw.append(text)
        titled.append(f"第{n}章 {titles.get(n, '')}\n\n{text}")
    (EXP / "READER_COPY_0001_0005.txt").write_text("\n\n".join(raw) + "\n", encoding="utf-8")
    (EXP / "READER_COPY_0001_0005_TITLED.txt").write_text("\n\n".join(titled) + "\n", encoding="utf-8")
    print(json.dumps({"chars": [len(x) for x in raw], "total": sum(map(len, raw))}, ensure_ascii=False))


def metrics() -> None:
    old = [(BASE / "chapters" / f"chapter-{n:04d}.md").read_text(encoding="utf-8") for n in range(1, 6)]
    new = [(EXP / "chapters" / f"chapter-{n:04d}.md").read_text(encoding="utf-8") for n in range(1, 6)]
    keys = ["复测", "离镇", "病驮兽", "白角", "幼年王种", "王种", "号角", "硬化"]

    def first(chapters: list[str], key: str):
        for i, text in enumerate(chapters, 1):
            if key in text:
                return i
        return None

    data = {
        "old_chars": [len(x) for x in old],
        "new_chars": [len(x) for x in new],
        "old_total": sum(map(len, old)),
        "new_total": sum(map(len, new)),
        "milestones": {k: {"old": first(old, k), "new": first(new, k)} for k in keys},
    }
    (EXP / "METRICS.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "init":
        init()
    elif action == "mat-world-smoke":
        mat_world_smoke()
    elif action == "mat-story":
        mat_story_build_outline()
    elif action == "mat-outline":
        mat_outline()
    elif action == "combine":
        combine()
    elif action == "metrics":
        metrics()
    elif action in {"director", "curator", "primary", "body", "state", "apply", "materialize"}:
        n = int(sys.argv[2])
        if action == "materialize":
            base_runner.materialize(n, sys.argv[3])
        elif action == "body":
            body(n)
        elif action == "apply":
            base_runner.apply_state(n)
        else:
            getattr(base_runner, action)(n)
    else:
        raise SystemExit(action)
