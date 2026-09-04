from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SRC = ROOT / "books" / "real-exp-power-ruler-heldout-20260903-v1" / "B_beast_bond"
OUT = ROOT / "books" / "real-exp-living-power-progression-beast-20260903-v2"
ACP_RUNNER = ROOT / "temps" / "acp_text_runner.py"
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.batch_runtime import (
    BatchWindow,
    apply_batch_delta,
    build_batch_delta_reviser_prompt,
    build_batch_primary_prompt,
    extract_batch_outline_plans,
    parse_batch_delta_response,
    parse_batch_primary_response,
)
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.character_seeds import compose_character_card, split_human_seed_authorities
from story_mvp.power_ruler import parse_root_precise_power_ruler, validate_human_seed_start
from story_mvp.prompts import generate_prompt
from story_mvp.storage import apply_state_delta_to_book, validate_book_content_for_save
from story_mvp.story_event_obligations import validate_book_registry_against_story_program

AUTHOR_DIRECTION = (SRC / "AUTHOR_DIRECTION.md").read_text(encoding="utf-8").strip()
CREATIVE_WORLD = {"world_vision": {"status": "author_approved"}}
CREATIVE_CHARACTER = {
    "world_vision": {"status": "author_approved"},
    "character_card": {"status": "author_approved"},
}
CREATIVE_STORY = {
    "world_vision": {"status": "author_approved"},
    "character_card": {"status": "author_approved"},
    "proposal": {"status": "author_approved"},
}
CALL_LOG: list[dict[str, object]] = []


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def dump(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_tail(path: Path, heading: str) -> str:
    text = read(path)
    pos = text.find(heading)
    if pos < 0:
        raise RuntimeError(f"missing frozen inspiration heading: {heading} in {path}")
    return text[pos + len(heading):].strip()


def extract_between(path: Path, start_heading: str, end_heading: str) -> str:
    text = read(path)
    start = text.find(start_heading)
    end = text.find(end_heading, start + len(start_heading))
    if start < 0 or end < 0:
        raise RuntimeError(f"missing frozen block {start_heading} -> {end_heading}")
    return text[start + len(start_heading):end].strip()


def extract_from_heading(text: str, heading: str) -> str:
    pos = text.find(heading)
    if pos < 0:
        raise RuntimeError(f"model response missing heading: {heading}")
    return text[pos:].strip()


def extract_candidate(text: str, kind: str, index: int) -> str:
    pattern = re.compile(
        rf"(?ms)# {re.escape(kind)} CANDIDATE {index}｜(?P<title>.+?)\s*$\n(?P<body>.*?)(?=# {re.escape(kind)} CANDIDATE \d+｜|\Z)"
    )
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"missing {kind} candidate {index}")
    title = match.group("title").strip()
    body = match.group("body").strip()
    return f"# {kind} SEED｜{title}\n{body}\n"


def run_acp(*, label: str, model: str, effort: str, prompt: str, timeout: int = 5400) -> str:
    folder = OUT / "calls" / label
    folder.mkdir(parents=True, exist_ok=True)
    prompt_path = folder / "prompt.md"
    response_path = folder / "response.md"
    write(prompt_path, prompt)
    if response_path.is_file() and response_path.stat().st_size > 20:
        text = read(response_path)
        row = {"label": label, "model": model, "effort": effort, "reused": True, "wall_seconds": 0.0, "chars": len(text)}
        CALL_LOG.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
        return text
    started = time.perf_counter()
    proc = subprocess.run(
        [
            sys.executable,
            str(ACP_RUNNER),
            "--model", model,
            "--effort", effort,
            "--prompt-file", str(prompt_path),
            "--output", str(response_path),
            "--timeout", str(timeout),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout + 180,
    )
    wall = time.perf_counter() - started
    write(folder / "runner_stdout.txt", proc.stdout)
    write(folder / "runner_stderr.txt", proc.stderr)
    if proc.returncode != 0:
        raise RuntimeError(f"{label} ACP failed: {proc.returncode}\n{proc.stdout}\n{proc.stderr}")
    text = read(response_path)
    row = {"label": label, "model": model, "effort": effort, "reused": False, "wall_seconds": round(wall, 3), "chars": len(text)}
    CALL_LOG.append(row)
    print(json.dumps(row, ensure_ascii=False), flush=True)
    return text


def frozen_inputs() -> dict[str, str]:
    return {
        "world_gbrain": extract_tail(SRC / "world_prompt.md", "# World GBrain Inspiration（可选）"),
        "power_gbrain": extract_tail(SRC / "power_candidates_prompt.md", "# Power GBrain Craft（可选）"),
        "human_gbrain": extract_tail(SRC / "human_candidates_prompt.md", "# Human GBrain Craft（可选）"),
        "story_gbrain": extract_tail(SRC / "story_program_prompt.md", "# GBrain Inspiration Results（可选，只借鉴长期故事结构，不能覆盖已批准 Character / World）"),
        "outline_gbrain": extract_tail(SRC / "outline_prompt.md", "# GBrain Inspiration Results（可选，不能覆盖批准产物）"),
        "power_novelty": read(SRC / "POWER_NOVELTY.md").strip(),
        "power_lexique": extract_between(
            SRC / "power_candidates_prompt.md",
            "# Power Lexique Primitive Spark（可选；非 Canon；可完全忽略）",
            "# Power GBrain Craft（可选）",
        ),
    }


def generate_upstream(inputs: dict[str, str]) -> tuple[str, str, str, str, str, str, str]:
    world_prompt = generate_split_prompt(
        mode="world_vision",
        creative_direction=AUTHOR_DIRECTION,
        gbrain_inspiration=inputs["world_gbrain"],
    )
    write(OUT / "01_WORLD_PROMPT.md", world_prompt)
    world_resp = run_acp(label="world", model="gpt-5.6-luna", effort="high", prompt=world_prompt)
    world = extract_from_heading(world_resp, "# PROTAGONIST-BLIND WORLD VISION")
    parse_root_precise_power_ruler(world)
    if "### 公共力量里程碑｜Public Milestone Ladder" not in world:
        raise RuntimeError("WORLD_MILESTONE_MISSING: Luna output omitted current production Public Milestone Ladder")
    if "公共新动词" not in world or "世界开口" not in world or "少年为什么向往" not in world:
        raise RuntimeError("WORLD_MILESTONE_INCOMPLETE: Ladder exists but required public promise semantics are missing")
    write(OUT / "01_WORLD_VISION.md", world)

    power_prompt = generate_split_prompt(
        mode="power_seed",
        world_vision=world,
        creative_state=CREATIVE_WORLD,
        gbrain_inspiration=inputs["power_gbrain"],
        power_novelty=inputs["power_novelty"],
        power_lexique=inputs["power_lexique"],
    )
    human_prompt = generate_split_prompt(
        mode="human_seed",
        world_vision=world,
        creative_state=CREATIVE_WORLD,
        gbrain_inspiration=inputs["human_gbrain"],
    )
    write(OUT / "02_POWER_PROMPT.md", power_prompt)
    write(OUT / "03_HUMAN_PROMPT.md", human_prompt)

    # Keep the old B held-out pre-registration: Candidate 1 for Power, Candidate 1 for Human.
    # Calls are sequential here to avoid mixing ACP transport failures with the creative test.
    power_resp = run_acp(label="power", model="gpt-5.6-luna", effort="high", prompt=power_prompt)
    human_resp = run_acp(label="human", model="gpt-5.6-luna", effort="high", prompt=human_prompt)
    power_seed = extract_candidate(power_resp, "POWER", 1)
    human_seed = extract_candidate(human_resp, "HUMAN", 1)
    validate_human_seed_start(human_seed, world)
    human_parts = split_human_seed_authorities(human_seed)
    character = compose_character_card(power_seed=power_seed, human_seed=human_seed)
    write(OUT / "02_POWER_SEED.md", power_seed)
    write(OUT / "03_HUMAN_SEED.md", human_seed)
    write(OUT / "04_CHARACTER.md", character)
    write(OUT / "04_CHARACTER_INITIAL_STATE.md", human_parts["initial_state"])

    story_prompt = generate_split_prompt(
        mode="idea",
        creative_direction=AUTHOR_DIRECTION,
        world_vision=world,
        character_card=character,
        character_initial_state=human_parts["initial_state"],
        creative_state=CREATIVE_CHARACTER,
        gbrain_inspiration=inputs["story_gbrain"],
    )
    write(OUT / "05_STORY_PROMPT.md", story_prompt)
    story_resp = run_acp(label="story", model="gpt-5.6-sol", effort="high", prompt=story_prompt)
    story = extract_from_heading(story_resp, "# STORY PROGRAM")
    write(OUT / "05_STORY_PROGRAM.md", story)

    outline_prompt = generate_split_prompt(
        mode="outline",
        creative_direction=AUTHOR_DIRECTION,
        world_vision=world,
        character_card=character,
        character_initial_state=human_parts["initial_state"],
        creative_state=CREATIVE_STORY,
        proposal_context=story,
        book_content="",
        gbrain_inspiration=inputs["outline_gbrain"],
    )
    write(OUT / "06_OUTLINE_PROMPT.md", outline_prompt)
    outline_resp = run_acp(label="outline", model="gpt-5.6-luna", effort="high", prompt=outline_prompt)
    book = extract_from_heading(outline_resp, "# 小说总体设计画像")
    validate_book_content_for_save(book)
    validate_book_registry_against_story_program(book, story)
    write(OUT / "06_BOOK_OUTLINE.md", book)
    return world, power_seed, human_seed, character, human_parts["initial_state"], story, book


def generate_batch(
    *,
    start_chapter: int,
    world: str,
    character: str,
    story: str,
    book: str,
    previous_chapter_text: str = "",
) -> tuple[dict[int, str], object]:
    window = BatchWindow(start_chapter, 5)
    tag = f"{window.start_chapter:02d}_{window.end_chapter:02d}"
    plans = extract_batch_outline_plans(book, window)
    dump(OUT / f"07_BATCH_PLANS_{tag}.json", {str(k): v for k, v in plans.items()})
    primary_prompt = build_batch_primary_prompt(
        window=window,
        batch_plans=plans,
        book_content=book,
        world_vision=world,
        world_expansions="",
        character_card=character,
        previous_chapter_text=previous_chapter_text,
    )
    write(OUT / f"07_BATCH_PRIMARY_PROMPT_{tag}.md", primary_prompt)
    primary_resp = run_acp(
        label=f"batch-primary-{tag}",
        model="gpt-5.6-terra",
        effort="high",
        prompt=primary_prompt,
        timeout=7200,
    )
    try:
        chapters = parse_batch_primary_response(primary_resp, window)
    except Exception as exc:
        repair_prompt = primary_prompt + (
            f"\n\n# OUTPUT COMPLETENESS REPAIR\n上一次输出无法被 production Batch parser 接受：{exc}。"
            f"保持同一故事与 Authority，不解释；重新完整输出第{window.start_chapter}—{window.end_chapter}章，"
            "每章都用 `# BATCH CHAPTER N` + `## 正式正文`，不得漏章或压成摘要。"
        )
        write(OUT / f"07_BATCH_PRIMARY_REPAIR_PROMPT_{tag}.md", repair_prompt)
        primary_resp = run_acp(
            label=f"batch-primary-repair-{tag}",
            model="gpt-5.6-terra",
            effort="high",
            prompt=repair_prompt,
            timeout=7200,
        )
        chapters = parse_batch_primary_response(primary_resp, window)
    write(
        OUT / f"07_BATCH_PRIMARY_{tag}.md",
        "\n\n".join(f"# CHAPTER {n}\n{chapters[n]}" for n in window.chapter_numbers),
    )

    delta_prompt = build_batch_delta_reviser_prompt(
        window=window,
        batch_plans=plans,
        primary_chapters=chapters,
        book_content=book,
        world_vision=world,
        world_expansions="",
        character_card=character,
        story_program=story,
    )
    write(OUT / f"08_BATCH_DELTA_PROMPT_{tag}.md", delta_prompt)
    delta_resp = run_acp(
        label=f"batch-delta-{tag}",
        model="gpt-5.6-sol",
        effort="high",
        prompt=delta_prompt,
        timeout=7200,
    )
    delta = parse_batch_delta_response(delta_resp, window)
    dump(
        OUT / f"08_BATCH_DELTA_{tag}.json",
        {"patches": list(delta.patches), "upstream_conflicts": list(delta.upstream_conflicts)},
    )
    if delta.upstream_conflicts:
        raise RuntimeError("BATCH_UPSTREAM_CONFLICT: " + json.dumps(list(delta.upstream_conflicts), ensure_ascii=False))
    final = apply_batch_delta(chapters, delta, window)
    final_text = "\n\n".join(f"# 第{n}章\n\n{final[n]}" for n in window.chapter_numbers)
    write(OUT / f"09_FINAL_{tag}.md", final_text)
    write(OUT / f"09_FINAL_{tag}.txt", final_text)
    return final, delta


def run_state(final: dict[int, str], book: str, *, start_chapter: int) -> str:
    current = book
    for chapter in range(start_chapter, start_chapter + 5):
        state_prompt = generate_prompt(
            mode="state_delta",
            template="",
            book_content=current,
            recent_summaries="",
            chapter_number=chapter,
            chapter_prose=final[chapter],
            chapter_fact_summary="",
        )
        write(OUT / "state" / f"chapter-{chapter:04d}" / "prompt.md", state_prompt)
        state_resp = run_acp(
            label=f"state-{chapter}",
            model="gpt-5.6-luna",
            effort="low",
            prompt=state_prompt,
            timeout=3000,
        )
        write(OUT / "state" / f"chapter-{chapter:04d}" / "response.md", state_resp)
        current = apply_state_delta_to_book(current, chapter, state_resp)
        validate_book_content_for_save(current)
    write(OUT / f"10_BOOK_AFTER_CH{start_chapter + 4}.md", current)
    return current


def validate_upstream_growth(world: str, power: str, story: str, book: str) -> None:
    failures: list[str] = []
    if "### 正常成长因果｜Power Growth Causality" not in world:
        failures.append("World 缺 Power Growth Causality")
    if "正常成长耦合" not in power:
        failures.append("Power Seed 缺 Growth Coupling")
    if "鸣位19" in story and not any(token in story for token in ("9级", "10级", "11级", "12级", "13级", "14级", "15级", "16级", "17级", "18级")):
        failures.append("Story 仍只有8→19，没有任何中间精确位置")
    if "鸣位19" in book and not any(token in book for token in ("9级", "10级", "11级", "12级", "13级", "14级", "15级", "16级", "17级", "18级")):
        failures.append("Outline 仍只有8→19，没有任何中间精确位置")
    if failures:
        raise RuntimeError("UPSTREAM_GROWTH_SCREEN_FAILED: " + "；".join(failures))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write(OUT / "00_AUTHOR_DIRECTION.md", AUTHOR_DIRECTION)
    dump(
        OUT / "00_EXPERIMENT_CONTRACT.json",
        {
            "source_heldout": str(SRC),
            "frozen_author_direction": True,
            "frozen_gbrain_from_source_heldout": True,
            "power_candidate": 1,
            "human_candidate": 1,
            "premise": "skipped (same split-authority path as source held-out)",
            "models": {
                "world": "gpt-5.6-luna/high",
                "power": "gpt-5.6-luna/high",
                "human": "gpt-5.6-luna/high",
                "story": "gpt-5.6-sol/high",
                "outline": "gpt-5.6-luna/high",
                "batch_primary": "gpt-5.6-terra/high",
                "batch_delta": "gpt-5.6-sol/high",
                "state": "gpt-5.6-luna/low",
            },
            "batch_size": 5,
            "chapters": 10,
            "manual_prose_treatment": False,
            "treatment": "Living Power Progression / Reader-Explicit Growth / Frequent Ruler Refresh",
        },
    )
    inputs = frozen_inputs()
    world, power, human, character, initial, story, book = generate_upstream(inputs)
    validate_upstream_growth(world, power, story, book)
    dump(OUT / "CALL_LOG.json", CALL_LOG)
    if "--upstream-only" in sys.argv:
        print(json.dumps({"status": "upstream_complete", "calls": len(CALL_LOG)}, ensure_ascii=False), flush=True)
        return

    final_01_05, delta_01_05 = generate_batch(
        start_chapter=1,
        world=world,
        character=character,
        story=story,
        book=book,
    )
    book_after_ch5 = run_state(final_01_05, book, start_chapter=1)

    final_06_10, delta_06_10 = generate_batch(
        start_chapter=6,
        world=world,
        character=character,
        story=story,
        book=book_after_ch5,
        previous_chapter_text=final_01_05[5],
    )
    book_after_ch10 = run_state(final_06_10, book_after_ch5, start_chapter=6)
    write(OUT / "10_BOOK_AFTER_CH10.md", book_after_ch10)

    all_final = {**final_01_05, **final_06_10}
    full_text = "\n\n".join(f"# 第{n}章\n\n{all_final[n]}" for n in range(1, 11))
    write(OUT / "FULL_10_CHAPTERS.md", full_text)
    write(OUT / "FULL_10_CHAPTERS.txt", full_text)

    dump(OUT / "CALL_LOG.json", CALL_LOG)
    metrics = {
        "total_model_wall_seconds": round(sum(float(x.get("wall_seconds") or 0) for x in CALL_LOG), 3),
        "calls": len(CALL_LOG),
        "batch_primary_wall_seconds": round(sum(float(x.get("wall_seconds") or 0) for x in CALL_LOG if str(x.get("label", "")).startswith("batch-primary-") and "repair" not in str(x.get("label", ""))), 3),
        "batch_delta_wall_seconds": round(sum(float(x.get("wall_seconds") or 0) for x in CALL_LOG if str(x.get("label", "")).startswith("batch-delta-")), 3),
        "patch_count": len(delta_01_05.patches) + len(delta_06_10.patches),
        "upstream_conflicts": len(delta_01_05.upstream_conflicts) + len(delta_06_10.upstream_conflicts),
    }
    dump(OUT / "METRICS.json", metrics)
    print(json.dumps({"status": "complete", **metrics}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
