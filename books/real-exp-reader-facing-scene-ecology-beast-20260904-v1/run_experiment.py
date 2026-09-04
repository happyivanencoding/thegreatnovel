from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-living-power-progression-beast-20260903-v2"
OUT = ROOT / "books" / "real-exp-reader-facing-scene-ecology-beast-20260904-v1"
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
from story_mvp.prompts import generate_prompt
from story_mvp.storage import apply_state_delta_to_book, validate_book_content_for_save
from story_mvp.story_event_obligations import validate_book_registry_against_story_program
from story_mvp.character_prompts import generate_split_prompt

CALL_LOG: list[dict[str, object]] = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def dump(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_tail(text: str, heading: str) -> str:
    pos = text.find(heading)
    if pos < 0:
        raise RuntimeError(f"missing heading: {heading}")
    return text[pos + len(heading):].strip()


def extract_from_heading(text: str, heading: str) -> str:
    pos = text.find(heading)
    if pos < 0:
        raise RuntimeError(f"model response missing heading: {heading}")
    return text[pos:].strip()


def parse_final_chapters(text: str) -> dict[int, str]:
    pat = re.compile(r"(?ms)^# 第(?P<n>\d+)章\s*\n+(?P<body>.*?)(?=^# 第\d+章\s*$|\Z)")
    out = {int(m.group("n")): m.group("body").strip() for m in pat.finditer(text)}
    if not all(n in out for n in range(1, 11)):
        raise RuntimeError(f"baseline prose parse incomplete: {sorted(out)}")
    return out


def run_acp(*, label: str, model: str, effort: str, prompt: str, timeout: int = 7200) -> str:
    folder = OUT / "calls" / label
    folder.mkdir(parents=True, exist_ok=True)
    prompt_path = folder / "prompt.md"
    response_path = folder / "response.md"
    write(prompt_path, prompt)
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
    row = {
        "label": label,
        "model": model,
        "effort": effort,
        "wall_seconds": round(wall, 3),
        "chars": len(text),
    }
    CALL_LOG.append(row)
    print(json.dumps(row, ensure_ascii=False), flush=True)
    return text


def freeze_inputs() -> tuple[str, str, str, str, str, str]:
    author = read(BASE / "00_AUTHOR_DIRECTION.md").strip()
    world = read(BASE / "01_WORLD_VISION.md").strip()
    power = read(BASE / "02_POWER_SEED.md").strip()
    human = read(BASE / "03_HUMAN_SEED.md").strip()
    character = read(BASE / "04_CHARACTER.md").strip()
    initial = read(BASE / "04_CHARACTER_INITIAL_STATE.md").strip()
    story = read(BASE / "05_STORY_PROGRAM.md").strip()
    for src, name in [
        ("00_AUTHOR_DIRECTION.md", "00_AUTHOR_DIRECTION.md"),
        ("01_WORLD_VISION.md", "01_WORLD_VISION.md"),
        ("02_POWER_SEED.md", "02_POWER_SEED.md"),
        ("03_HUMAN_SEED.md", "03_HUMAN_SEED.md"),
        ("04_CHARACTER.md", "04_CHARACTER.md"),
        ("04_CHARACTER_INITIAL_STATE.md", "04_CHARACTER_INITIAL_STATE.md"),
        ("05_STORY_PROGRAM.md", "05_STORY_PROGRAM.md"),
    ]:
        write(OUT / name, read(BASE / src))
    return author, world, character, initial, story, power


def add_legacy_actor_ruler_transport(story: str) -> str:
    """Experiment-only bridge for a pre-anchor Story Program.

    Both lines below are already explicit facts in the frozen V2 Story Program;
    this appendix adds no new story content. Future production Story Programs
    emit the same transport section directly.
    """
    appendix = """
### Reader-Facing Actor Ruler Anchors
- ACTOR-RULER-01｜人物：唐鹭｜精确位置：共鸣级44｜展示：共载｜时机/地点：阶段2 / 鸣骨峡｜现场意义：让读者看见猛烈气流里人、兽与货物一起转身落点的公共承诺。
- ACTOR-RULER-02｜人物：韩狩｜精确位置：共鸣级68｜展示：择风｜时机/地点：前期 / 鸣骨峡｜现场意义：维持鸣骨峡的短暂返程线，提前证明“择风”意味着什么。
""".strip()
    bridged = story.rstrip() + "\n\n" + appendix + "\n"
    write(OUT / "05_STORY_PROGRAM_WITH_ACTOR_RULER_TRANSPORT.md", bridged)
    return bridged


def generate_outline(*, author: str, world: str, character: str, initial: str, story: str) -> str:
    old_outline_prompt = read(BASE / "06_OUTLINE_PROMPT.md")
    outline_gbrain = extract_tail(old_outline_prompt, "# GBrain Inspiration Results（可选，不能覆盖批准产物）")
    creative_state = {
        "world_vision": {"status": "author_approved"},
        "character_card": {"status": "author_approved"},
        "proposal": {"status": "author_approved"},
    }
    prompt = generate_split_prompt(
        mode="outline",
        creative_direction=author,
        world_vision=world,
        character_card=character,
        character_initial_state=initial,
        creative_state=creative_state,
        proposal_context=story,
        book_content="",
        gbrain_inspiration=outline_gbrain,
    )
    write(OUT / "06_OUTLINE_PROMPT.md", prompt)
    response = run_acp(label="outline", model="gpt-5.6-luna", effort="high", prompt=prompt)
    book = extract_from_heading(response, "# 小说总体设计画像")
    validate_book_content_for_save(book)
    validate_book_registry_against_story_program(book, story)
    write(OUT / "06_BOOK_OUTLINE.md", book)
    return book


def screen_outline(book: str) -> None:
    failures: list[str] = []
    # This is an experiment stop-line, not a production hard gate.
    future_start = book.find("# 未来十章逐章小纲")
    future_end = book.find("# 当前状态、未兑现承诺与作者备注", future_start)
    future = book[future_start:future_end] if future_start >= 0 and future_end > future_start else ""
    if not re.search(r"唐鹭.{0,160}共鸣级44.{0,160}共载|共鸣级44.{0,160}唐鹭.{0,160}共载", future, re.S):
        failures.append("唐鹭44 / 共载未进入当前 Future-10")
    if not re.search(r"韩狩.{0,160}共鸣级68.{0,160}择风|共鸣级68.{0,160}韩狩.{0,160}择风", future, re.S):
        failures.append("韩狩68 / 择风未进入当前 Future-10")
    if "苏渠" not in book or "唐鹭" not in book:
        failures.append("唐鹭当前私人因果未保留")
    # Stable geography should keep the main stage pieces instead of inventing only local names.
    geography_hits = sum(token in book for token in ("交易台", "旧风门", "副链", "风隙", "高台"))
    if geography_hits < 4:
        failures.append("鸣骨峡稳定空间锚点不足")
    if failures:
        raise RuntimeError("SCENE_ECOLOGY_OUTLINE_SCREEN_FAILED: " + "；".join(failures))


def rebuild_book_after_ch4(new_outline: str) -> str:
    current = new_outline
    for chapter in range(1, 5):
        response = read(BASE / "state" / f"chapter-{chapter:04d}" / "response.md")
        current = apply_state_delta_to_book(current, chapter, response)
        validate_book_content_for_save(current)
    write(OUT / "06_BOOK_AFTER_FROZEN_CH4.md", current)
    return current


def generate_batch_5_10(*, world: str, character: str, story: str, book_after_ch4: str, previous_chapter: str):
    window = BatchWindow(5, 6)
    plans = extract_batch_outline_plans(book_after_ch4, window)
    dump(OUT / "07_BATCH_PLANS_05_10.json", {str(k): v for k, v in plans.items()})
    primary_prompt = build_batch_primary_prompt(
        window=window,
        batch_plans=plans,
        book_content=book_after_ch4,
        world_vision=world,
        world_expansions="",
        character_card=character,
        previous_chapter_text=previous_chapter,
    )
    write(OUT / "07_BATCH_PRIMARY_PROMPT_05_10.md", primary_prompt)
    primary_response = run_acp(
        label="batch-primary-05_10",
        model="gpt-5.6-terra",
        effort="high",
        prompt=primary_prompt,
    )
    chapters = parse_batch_primary_response(primary_response, window)
    write(OUT / "07_BATCH_PRIMARY_05_10.md", "\n\n".join(f"# CHAPTER {n}\n{chapters[n]}" for n in window.chapter_numbers))

    delta_prompt = build_batch_delta_reviser_prompt(
        window=window,
        batch_plans=plans,
        primary_chapters=chapters,
        book_content=book_after_ch4,
        world_vision=world,
        world_expansions="",
        character_card=character,
        story_program=story,
    )
    write(OUT / "08_BATCH_DELTA_PROMPT_05_10.md", delta_prompt)
    delta_response = run_acp(
        label="batch-delta-05_10",
        model="gpt-5.6-sol",
        effort="high",
        prompt=delta_prompt,
    )
    delta = parse_batch_delta_response(delta_response, window)
    dump(OUT / "08_BATCH_DELTA_05_10.json", {"patches": list(delta.patches), "upstream_conflicts": list(delta.upstream_conflicts)})
    if delta.upstream_conflicts:
        raise RuntimeError("BATCH_UPSTREAM_CONFLICT: " + json.dumps(list(delta.upstream_conflicts), ensure_ascii=False))
    final = apply_batch_delta(chapters, delta, window)
    final_text = "\n\n".join(f"# 第{n}章\n\n{final[n]}" for n in window.chapter_numbers)
    write(OUT / "09_FINAL_05_10.md", final_text)
    write(OUT / "09_FINAL_05_10.txt", final_text)
    return final, delta


def run_state_5_10(final: dict[int, str], book_after_ch4: str) -> str:
    current = book_after_ch4
    for chapter in range(5, 11):
        prompt = generate_prompt(
            mode="state_delta",
            template="",
            book_content=current,
            recent_summaries="",
            chapter_number=chapter,
            chapter_prose=final[chapter],
            chapter_fact_summary="",
        )
        write(OUT / "state" / f"chapter-{chapter:04d}" / "prompt.md", prompt)
        response = run_acp(
            label=f"state-{chapter}",
            model="gpt-5.6-luna",
            effort="low",
            prompt=prompt,
            timeout=3000,
        )
        write(OUT / "state" / f"chapter-{chapter:04d}" / "response.md", response)
        current = apply_state_delta_to_book(current, chapter, response)
        validate_book_content_for_save(current)
    write(OUT / "10_BOOK_AFTER_CH10.md", current)
    return current


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    author, world, character, initial, story, power = freeze_inputs()
    story_for_outline = add_legacy_actor_ruler_transport(story)
    baseline_chapters = parse_final_chapters(read(BASE / "FULL_10_CHAPTERS.md"))
    write(OUT / "FROZEN_BASELINE_CH1_4.md", "\n\n".join(f"# 第{n}章\n\n{baseline_chapters[n]}" for n in range(1, 5)))
    dump(
        OUT / "00_EXPERIMENT_CONTRACT.json",
        {
            "baseline": str(BASE),
            "frozen": ["author_direction", "world", "power", "human", "character", "story_program", "gbrain", "final_chapters_1_4"],
            "fresh": ["outline", "batch_primary_5_10", "batch_delta_5_10", "state_5_10"],
            "treatment": "Reader-Facing Scene Ecology: Stable Scene Geography + Living Power Ecology + Active Interior Continuity + Situation Re-anchor + Earned Convergence",
            "models": {"outline": "gpt-5.6-luna/high", "batch_primary": "gpt-5.6-terra/high", "batch_delta": "gpt-5.6-sol/high", "state": "gpt-5.6-luna/low"},
            "batch_window": "chapters 5-10 (6 chapters)",
            "manual_prose_treatment": False,
        },
    )

    if "--reuse-outline" in sys.argv and (OUT / "06_BOOK_OUTLINE.md").exists():
        outline = read(OUT / "06_BOOK_OUTLINE.md")
        validate_book_content_for_save(outline)
        validate_book_registry_against_story_program(outline, story_for_outline)
        print(json.dumps({"label": "outline", "reused": True, "chars": len(outline)}, ensure_ascii=False), flush=True)
    else:
        outline = generate_outline(author=author, world=world, character=character, initial=initial, story=story_for_outline)
    screen_outline(outline)
    if "--outline-only" in sys.argv:
        dump(OUT / "CALL_LOG.json", CALL_LOG)
        print(json.dumps({"status": "outline_complete", "calls": len(CALL_LOG)}, ensure_ascii=False), flush=True)
        return

    book_after_ch4 = rebuild_book_after_ch4(outline)
    final, delta = generate_batch_5_10(
        world=world,
        character=character,
        story=story,
        book_after_ch4=book_after_ch4,
        previous_chapter=baseline_chapters[4],
    )
    run_state_5_10(final, book_after_ch4)

    full = {n: baseline_chapters[n] for n in range(1, 5)}
    full.update(final)
    full_text = "\n\n".join(f"# 第{n}章\n\n{full[n]}" for n in range(1, 11))
    write(OUT / "FULL_10_CHAPTERS.md", full_text)
    write(OUT / "FULL_10_CHAPTERS.txt", full_text)
    dump(OUT / "CALL_LOG.json", CALL_LOG)
    dump(
        OUT / "METRICS.json",
        {
            "calls": len(CALL_LOG),
            "model_wall_seconds": round(sum(float(x["wall_seconds"]) for x in CALL_LOG), 3),
            "patch_count": len(delta.patches),
            "upstream_conflicts": len(delta.upstream_conflicts),
        },
    )
    print(json.dumps({"status": "complete", "calls": len(CALL_LOG), "patches": len(delta.patches)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
