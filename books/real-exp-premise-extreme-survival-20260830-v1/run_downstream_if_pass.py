from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.character_seeds import compose_character_card, split_human_seed_authorities
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.hybrid_runtime import extract_primary_draft
from story_mvp.long_form_evolution import extract_world_horizon_handoff
from story_mvp.premise_aperture import build_single_pass_lane_bundle, has_explicit_premise_conflict, render_lane_direction
from story_mvp.prompts import generate_prompt, parse_canon_memory
from story_mvp.storage import apply_state_delta_to_book, parse_book_sections, validate_book_content_for_save, validate_chapter_body_for_save

RUNNER = ROOT / "temps" / "acp_readonly_runner.mjs"


def dump(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def run_acp(prompt_path: Path, out_json: Path, out_md: Path, *, model: str, effort: str, label: str) -> str:
    if out_md.exists():
        return out_md.read_text(encoding="utf-8").strip()
    started = time.time()
    proc = subprocess.run(["node", str(RUNNER), str(prompt_path), str(out_json), model, effort, label], cwd=ROOT, text=True, capture_output=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f"ACP {label} failed: {proc.stderr[-4000:]}\n{proc.stdout[-4000:]}")
    data = json.loads(out_json.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"ACP {label}: {data.get('error')}")
    text = clean(str(data.get("text", "")))
    if not text:
        raise RuntimeError(f"ACP {label}: empty")
    out_md.write_text(text + "\n", encoding="utf-8")
    print(json.dumps({"label": label, "wall": round(time.time()-started,2), "agent_wall": data.get("wall_seconds"), "chars": len(text)}, ensure_ascii=False), flush=True)
    return text


def retrieval_meta(result: dict) -> dict:
    return {
        "query_strategy": result.get("query_strategy"),
        "query_texts": result.get("query_texts"),
        "accepted_count": result.get("accepted_count"),
        "accepted": [{"slug": x.get("slug"), "score": x.get("score")} for x in result.get("accepted", [])],
        "rejected_count": result.get("rejected_count"),
        "final_limit": result.get("final_limit"),
    }


def numbered_blocks(text: str, marker: str, count: int) -> list[str]:
    starts = [m.start() for m in re.finditer(rf"(?m)^# {re.escape(marker)} \d+", text)]
    if len(starts) != count:
        raise RuntimeError(f"Expected {count} {marker} blocks, got {len(starts)}")
    starts.append(len(text))
    return [text[starts[i]:starts[i+1]].strip() for i in range(count)]


def stop_on_conflict(stage: str, text: str) -> None:
    if has_explicit_premise_conflict(text):
        (EXP / f"{stage.upper()}_PREMISE_AUTHORITY_CONFLICT.md").write_text(text + "\n", encoding="utf-8")
        raise RuntimeError(f"{stage}: PREMISE-AUTHORITY CONFLICT")


def book() -> str:
    return (EXP / "BOOK.md").read_text(encoding="utf-8")


def sections() -> dict:
    return parse_book_sections(book())


def memory() -> dict:
    return parse_canon_memory(sections()["status"])


def recent() -> str:
    return memory().get("recent_summaries", "").strip()


def previous(n: int) -> str:
    if n <= 1:
        return ""
    return (EXP / "chapters" / f"chapter-{n-1:04d}.md").read_text(encoding="utf-8")


def chapter_plan(n: int) -> str:
    src = sections()["small_plan"]
    m = re.search(rf"(?ms)^## 第{n}章：.*?(?=^## 第{n+1}章：|\Z)", src)
    if not m:
        raise RuntimeError(f"missing chapter {n} plan")
    return m.group(0).strip()


def long_block(n: int) -> str:
    src = sections()["long_plan"]
    for m in re.finditer(r"(?ms)^## 第(\d+)[—-](\d+)章：.*?(?=^## 第\d+[—-]\d+章：|\Z)", src):
        if int(m.group(1)) <= n <= int(m.group(2)):
            return m.group(0).strip()
    return ""


def run_stage(n: int, stage: str, prompt: str, model: str, effort: str) -> str:
    d = EXP / "runs" / f"chapter-{n:04d}"
    d.mkdir(parents=True, exist_ok=True)
    pp = d / f"{stage}_prompt.md"
    pp.write_text(prompt, encoding="utf-8")
    return run_acp(pp, d / f"{stage}_acp.json", d / f"{stage}_response.md", model=model, effort=effort, label=f"extreme-survival-ch{n:02d}-{stage}")


def main() -> None:
    summary = json.loads((EXP / "PHASE1_SUMMARY.json").read_text(encoding="utf-8"))
    if summary.get("compiler_verdict") != "PASS":
        raise RuntimeError(f"E7 downstream forbidden: compiler={summary.get('compiler_verdict')}")
    author = (EXP / "AUTHOR_DIRECTION.md").read_text(encoding="utf-8")
    selected = (EXP / "SELECTED_S3.md").read_text(encoding="utf-8")
    bundle = build_single_pass_lane_bundle(selected)
    world_direction = render_lane_direction(bundle, lane="world")
    power_direction = render_lane_direction(bundle, lane="power")
    human_direction = render_lane_direction(bundle, lane="human")
    story_direction = render_lane_direction(bundle, lane="story")

    lanes = EXP / "COMPILED_LANES"
    lanes.mkdir(exist_ok=True)
    for name, text in {"WORLD_DIRECTION.md": world_direction, "POWER_DIRECTION.md": power_direction, "HUMAN_DIRECTION.md": human_direction, "STORY_DIRECTION.md": story_direction}.items():
        (lanes / name).write_text(text + "\n", encoding="utf-8")

    # World sees only its frozen lane plus author genre direction.
    world_author = author + "\n\n" + world_direction
    wr = retrieve_gbrain(mode="world_vision", creative_direction=world_author)
    (EXP / "WORLD_GBRAIN.md").write_text(wr["result"], encoding="utf-8")
    dump(EXP / "WORLD_RETRIEVAL.json", retrieval_meta(wr))
    wp = generate_split_prompt(mode="world_vision", creative_direction=world_author, gbrain_inspiration=wr["result"]).strip() + "\n\n# PREMISE FAIL-LOUD\n若 World-only / public-interface 硬约束无法与作者方向同时成立，只输出 `PREMISE-AUTHORITY CONFLICT`；不得为了合理化恢复普通世界。\n"
    (EXP / "WORLD_PROMPT.md").write_text(wp, encoding="utf-8")
    world = run_acp(EXP / "WORLD_PROMPT.md", EXP / "WORLD_ACP.json", EXP / "WORLD_VISION.md", model="gpt-5.6-luna", effort="high", label="extreme-survival-world")
    stop_on_conflict("world", world)

    state = {"world_vision": {"status": "author_approved"}}
    pr = retrieve_gbrain(mode="power_seed", creative_direction=power_direction, world_vision=world)
    hr = retrieve_gbrain(mode="human_seed", creative_direction=human_direction, world_vision=world)
    (EXP / "POWER_GBRAIN.md").write_text(pr["result"], encoding="utf-8")
    (EXP / "HUMAN_GBRAIN.md").write_text(hr["result"], encoding="utf-8")
    dump(EXP / "POWER_RETRIEVAL.json", retrieval_meta(pr)); dump(EXP / "HUMAN_RETRIEVAL.json", retrieval_meta(hr))
    pp = "\n\n".join((generate_split_prompt(mode="power_seed", world_vision=world, creative_state=state, gbrain_inspiration=pr["result"], power_novelty="", power_lexique="").strip(), power_direction.strip(), "# PREMISE FAIL-LOUD\n三个候选都必须精确保留 literal Ontology、Initial Scale Position、trigger/target/action/carrier/root boundary；冲突只输出 `PREMISE-AUTHORITY CONFLICT`，不得静默缩窄、增强或换义。")) + "\n"
    hp = "\n\n".join((generate_split_prompt(mode="human_seed", world_vision=world, creative_state=state, gbrain_inspiration=hr["result"]).strip(), human_direction.strip(), "# PREMISE FAIL-LOUD\n四个候选都必须从 literal Ontology + exact T0 Origin + Initial Scale Position 开始；冲突只输出 `PREMISE-AUTHORITY CONFLICT`，不得搬出生、补前传或恢复普通人形。")) + "\n"
    (EXP / "POWER_PROMPT.md").write_text(pp, encoding="utf-8"); (EXP / "HUMAN_PROMPT.md").write_text(hp, encoding="utf-8")
    with ThreadPoolExecutor(max_workers=2) as pool:
        fp = pool.submit(run_acp, EXP / "POWER_PROMPT.md", EXP / "POWER_ACP.json", EXP / "POWER_CANDIDATES.md", model="gpt-5.6-luna", effort="high", label="extreme-survival-power")
        fh = pool.submit(run_acp, EXP / "HUMAN_PROMPT.md", EXP / "HUMAN_ACP.json", EXP / "HUMAN_CANDIDATES.md", model="gpt-5.6-luna", effort="high", label="extreme-survival-human")
        powers, humans = fp.result(), fh.result()
    stop_on_conflict("power", powers); stop_on_conflict("human", humans)
    pblocks = numbered_blocks(powers, "POWER CANDIDATE", 3); hblocks = numbered_blocks(humans, "HUMAN CANDIDATE", 4)
    power = re.sub(r"(?m)^# POWER CANDIDATE \d+｜", "# POWER SEED｜", pblocks[1], count=1)
    human = re.sub(r"(?m)^# HUMAN CANDIDATE \d+｜", "# HUMAN SEED｜", hblocks[1], count=1)
    (EXP / "POWER_SEED.md").write_text(power + "\n", encoding="utf-8"); (EXP / "HUMAN_SEED.md").write_text(human + "\n", encoding="utf-8")
    character = compose_character_card(power_seed=power, human_seed=human)
    ha = split_human_seed_authorities(human)
    (EXP / "CHARACTER.md").write_text(character, encoding="utf-8"); (EXP / "CHARACTER_INITIAL_STATE.md").write_text(ha["initial_state"], encoding="utf-8"); (EXP / "CHARACTER_AUDITION.md").write_text(ha["audition_metadata"], encoding="utf-8")

    story_author = author + "\n\n" + story_direction
    story_state = {"world_vision": {"status": "author_approved"}, "character_card": {"status": "author_approved"}}
    sr = retrieve_gbrain(mode="idea", creative_direction=story_author, world_vision=world, character_card=character)
    (EXP / "STORY_GBRAIN.md").write_text(sr["result"], encoding="utf-8"); dump(EXP / "STORY_RETRIEVAL.json", retrieval_meta(sr))
    sp = generate_split_prompt(mode="idea", creative_direction=story_author, world_vision=world, character_card=character, character_initial_state=ha["initial_state"], creative_state=story_state, gbrain_inspiration=sr["result"])
    (EXP / "STORY_PROGRAM_PROMPT.md").write_text(sp, encoding="utf-8")
    story = run_acp(EXP / "STORY_PROGRAM_PROMPT.md", EXP / "STORY_PROGRAM_ACP.json", EXP / "STORY_PROGRAM.md", model="gpt-5.6-sol", effort="high", label="extreme-survival-story")
    stop_on_conflict("story", story)
    (EXP / "WORLD_HORIZON_HANDOFF.md").write_text(extract_world_horizon_handoff(story) + "\n", encoding="utf-8")

    outline_state = {**story_state, "proposal": {"status": "author_approved"}}
    orr = retrieve_gbrain(mode="outline", creative_direction=author, world_vision=world, character_card=character, proposal_context=story)
    (EXP / "OUTLINE_GBRAIN.md").write_text(orr["result"], encoding="utf-8"); dump(EXP / "OUTLINE_RETRIEVAL.json", retrieval_meta(orr))
    op = generate_split_prompt(mode="outline", creative_direction=author, world_vision=world, character_card=character, character_initial_state=ha["initial_state"], creative_state=outline_state, proposal_context=story, gbrain_inspiration=orr["result"])
    (EXP / "OUTLINE_PROMPT.md").write_text(op, encoding="utf-8")
    outline_raw = run_acp(EXP / "OUTLINE_PROMPT.md", EXP / "OUTLINE_ACP.json", EXP / "OUTLINE_RAW.md", model="gpt-5.6-luna", effort="high", label="extreme-survival-outline")
    marker = outline_raw.find("# 小说总体设计画像"); outline = outline_raw[marker:] if marker >= 0 else outline_raw
    validate_book_content_for_save(outline)
    (EXP / "OUTLINE.md").write_text(outline + "\n", encoding="utf-8"); (EXP / "BOOK.md").write_text(outline + "\n", encoding="utf-8")

    (EXP / "chapters").mkdir(exist_ok=True); (EXP / "runs").mkdir(exist_ok=True)
    direction = "严格执行当前批准 Authority 与前5章计划。核心 Premise 已经在上游冻结，但 raw Premise Card 不提供给章节 Runtime；不要为了成熟/合理把非标准 Ontology、Changed Verbs、第一次 unfair payoff 或真实社会/生态后果改回普通修士叙事。不得新增未批准机制。"
    for n in range(1, 6):
        plan = chapter_plan(n); block = long_block(n)
        dp = generate_prompt(mode="director", template="", book_content=book(), world_vision=world, world_expansions="", character_card=character, current_long_block=block, previous_chapter_text=previous(n), current_outline="", current_chapter_plan=plan, recent_summaries=recent(), chapter_number=n, creative_direction=direction)
        dr = run_stage(n, "director", dp, "gpt-5.6-luna", "high")
        cp = generate_prompt(mode="context_curator", template="", book_content=book(), world_vision=world, world_expansions="", character_card=character, current_long_block=block, previous_chapter_text=previous(n), current_outline=dr, current_chapter_plan=plan, recent_summaries=recent(), gbrain_inspiration="", chapter_number=n)
        cu = run_stage(n, "curator", cp, "gpt-5.6-luna", "high")
        pwp = generate_prompt(mode="primary_writer", template="", book_content=book(), world_vision=world, world_expansions="", character_card=character, current_long_block=block, previous_chapter_text=previous(n), current_outline=dr, current_chapter_plan=plan, recent_summaries=recent(), gbrain_inspiration="", curated_context=cu, curator_response=cu, chapter_number=n)
        prsp = run_stage(n, "primary", pwp, "gpt-5.6-terra", "high"); primary_body = extract_primary_draft(prsp).strip(); validate_chapter_body_for_save(primary_body)
        arp = generate_prompt(mode="authority_reviser", template="", book_content=book(), world_vision=world, world_expansions="", character_card=character, current_long_block=block, previous_chapter_text=previous(n), current_outline=dr, current_chapter_plan=plan, recent_summaries=recent(), curated_context=cu, curator_response=cu, primary_draft=primary_body, primary_writer_response=prsp, chapter_number=n)
        ar = run_stage(n, "authority_reviser", arp, "gpt-5.6-luna", "high"); body = extract_primary_draft(ar).strip(); validate_chapter_body_for_save(body)
        (EXP / "chapters" / f"chapter-{n:04d}.md").write_text(body + "\n", encoding="utf-8")
        stp = generate_prompt(mode="state_delta", template="", book_content=book(), recent_summaries=recent(), chapter_number=n, chapter_prose=body)
        st = run_stage(n, "state", stp, "gpt-5.6-luna", "low"); updated = apply_state_delta_to_book(book(), n, st); validate_book_content_for_save(updated); (EXP / "BOOK.md").write_text(updated, encoding="utf-8")
        print(f"CHAPTER {n} COMPLETE chars={len(body)}", flush=True)

    combined = "\n\n".join((EXP / "chapters" / f"chapter-{n:04d}.md").read_text(encoding="utf-8").strip() for n in range(1,6)) + "\n"
    (EXP / "CHAPTERS_0001_0005.md").write_text(combined, encoding="utf-8"); (EXP / "CHAPTERS_0001_0005.txt").write_text(combined, encoding="utf-8")

    audit_prompt = f"""你是独立 Extreme Premise Survival 审计员。只回答：这张 Compiler PASS 的极端 premise 从冻结卡进入真实 World→Power/Human→Story→Outline→前5章后，在哪一层第一次被普通化、抽象化、职业化或换回旧动词；如果没有，就明确说保真。不要改稿，不因为设定怪/强而扣分。\n\n逐层检查：一句话货架承诺、literal Ontology、Changed Verbs、第一章标志画面、第一次 unfair payoff、Public/Social/Ecological Repricing、root boundary、Human-specific appetite。区分 PRESERVED / TRANSFORMED-BUT-PRESERVED / LOST / CONTRADICTED，并指出最早 collapse node。特别检查正文是否真的持续出现只有这本书才能发生的动作，而不是变回修炼→接任务→分析→胜利。\n\n严格输出：\n# EXTREME PREMISE SURVIVAL AUDIT\n## Stage Preservation Table\n## Earliest Collapse Node\n## Chapter 1-5 Unique Verbs\n## Commercial Voltage Survived?\n## Authority Legality\n## Verdict: PASS / DIRECTIONAL PASS / FAIL\n## What This Did Not Solve\n\n# PREMISE\n{selected}\n\n# WORLD\n{world}\n\n# POWER\n{power}\n\n# HUMAN\n{human}\n\n# STORY\n{story}\n\n# OUTLINE\n{outline}\n\n# CHAPTERS 1-5\n{combined}\n"""
    (EXP / "SURVIVAL_AUDIT_PROMPT.md").write_text(audit_prompt, encoding="utf-8")
    audit = run_acp(EXP / "SURVIVAL_AUDIT_PROMPT.md", EXP / "SURVIVAL_AUDIT_ACP.json", EXP / "SURVIVAL_AUDIT.md", model="gpt-5.6-terra", effort="high", label="extreme-survival-audit")
    dump(EXP / "DOWNSTREAM_SUMMARY.json", {"status":"complete", "chapters":5, "world_chars":len(world), "power_chars":len(power), "human_chars":len(human), "story_chars":len(story), "outline_chars":len(outline), "chapter_chars":len(combined), "audit_chars":len(audit), "production_modified":False})


if __name__ == "__main__":
    main()
