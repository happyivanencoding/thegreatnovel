from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
EXP = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.character_context import project_character_life_context, project_character_power_baseline
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.character_seeds import compose_character_card, split_human_seed_authorities
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.hybrid_runtime import extract_primary_draft
from story_mvp.long_form_evolution import extract_world_horizon_handoff
from story_mvp.power_novelty import build_power_novelty_bundle
from story_mvp.prompts import generate_prompt, parse_canon_memory
from story_mvp.storage import (
    apply_state_delta_to_book,
    parse_book_sections,
    validate_book_content_for_save,
    validate_chapter_body_for_save,
)

AUTHOR_DIRECTION = """成熟中文男频高强度多世界成长爽文。整本书的长期形式是：一个稳定的跨世界 Meta Grammar + 一个个真正独立、生活自洽的 Local World；每个主要世界约 20 章完成一季，主角从刚进入时的外来者/低位者，经过真实选择、战斗、获得、关系与世界事件，在第 20 章前后成长到该 Local World 的顶层或成为决定该世界最高局势的人，然后进入下一独立世界。第一轮只设计和具体规划第一个 World Horizon，禁止提前设计第二世界的具体社会、力量、宝物、敌人或针对主角 Build 的答案。

节奏明确偏快、剧情必须跌宕：平均每 2—4 章至少出现一次真正改变“现在故事是什么”的 State Change / 关系换位 / 新目标 / 世界理解变化 / 大胜大失 / 新竞争结构；但不要用连续幕后黑手、连续假反转、每章升级或 Boss 逐级排队冒充跌宕。第一世界 20 章内部优先让 Story Engine 至少发生数次真实换挡，例如 Survival / Hunt / Acquisition / Competition / Relationship Choice / Identity / War / World Reveal 中按世界自然组合，而不是固定模板。

主角成长极快但不 Reset：第 20 章必须真正达到第一 Local World 的顶层尺度；后续世界会保留全部已获得能力、身体变化、装备、关系、知识与代价，只让 Problem / World Ruler / Social Reality / Victory Condition 改变。Power Asymmetry 宁强勿弱，允许明显越级特权；大胜按 AGGRESSIVE Payoff 真正结算。快速不等于省略人物：重要关系必须能改变主角选择，Human 可以有钱、胜负、虚荣、身体欲望、审美、享受、好奇、偏心、报复、野心与舍不得，不净化成成长最优人格。

世界与力量要具体、好懂、可视觉化；Small Grammar, Large Variation。不要靠抽象哲学、概念术语、治理、资源分配、维护、项目管理、测试验证或工程实施制造复杂感。第一世界应该让读者在第 1—2 章就知道普通人的生活、力量粗尺、什么真正值钱、最危险的东西和主角当前位置。World 阶段完全不知道未来主角是谁。

Story Program 必须把第一 World Horizon 的交接自然准备到第 20 章：最后阶段要让当前世界的最高局势真实结算，并输出 World Horizon Handoff；Handoff 只能说明触发条件、为什么该扩、carry-forward 与 orchestration，不能预写第二世界答案。Outline 先规划第 1—10 章；第 10 章后根据真实 Canon Review，再规划第 11—20 章。"""

NOVELTY_SEED = 202608282203
LOG = EXP / "RUN_LOG.txt"


def log(msg: str) -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def dump(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def clean(text: str) -> str:
    text = re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text)
    return text.strip()


def run_acp(prompt_path: Path, out_path: Path, model: str, effort: str, label: str) -> dict:
    log(f"ACP START {label} {model}/{effort}")
    proc = subprocess.run(
        ["node", str(RUNNER), str(prompt_path), str(out_path), model, effort, str(ROOT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ACP failed {label}: {proc.stderr[-3000:]}\n{proc.stdout[-3000:]}")
    data = json.loads(out_path.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"ACP failed {label}: {data.get('error')}")
    log(f"ACP DONE {label} wall={data.get('wall_seconds')} chars={len(data.get('text',''))}")
    return data


def model_text(data: dict, path: Path) -> str:
    text = clean(data.get("text", ""))
    path.write_text(text + "\n", encoding="utf-8")
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
    return [text[starts[i]:starts[i + 1]].strip() for i in range(count)]


def select_index(text: str, count: int) -> int:
    m = re.search(r"(?mi)^SELECT\s*:\s*(\d+)\s*$", text)
    if not m:
        raise RuntimeError(f"selector missing SELECT: {text[:500]}")
    idx = int(m.group(1))
    if not (1 <= idx <= count):
        raise RuntimeError(f"selector out of range: {idx}")
    return idx


def init_dirs() -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    (EXP / "chapters").mkdir(exist_ok=True)
    (EXP / "runs").mkdir(exist_ok=True)
    (EXP / "AUTHOR_DIRECTION.md").write_text(AUTHOR_DIRECTION + "\n", encoding="utf-8")


def generate_upstream() -> None:
    init_dirs()
    log("UPSTREAM world retrieval")
    wr = retrieve_gbrain(mode="world_vision", creative_direction=AUTHOR_DIRECTION)
    (EXP / "WORLD_GBRAIN.md").write_text(wr["result"], encoding="utf-8")
    dump(EXP / "WORLD_RETRIEVAL.json", retrieval_meta(wr))
    wp = generate_split_prompt(mode="world_vision", creative_direction=AUTHOR_DIRECTION, gbrain_inspiration=wr["result"])
    (EXP / "WORLD_PROMPT.md").write_text(wp, encoding="utf-8")
    world_data = run_acp(EXP / "WORLD_PROMPT.md", EXP / "WORLD_ACP.json", "gpt-5.6-luna", "high", "fast20-world")
    world = model_text(world_data, EXP / "WORLD_VISION.md")

    state = {"world_vision": {"status": "author_approved"}}
    novelty = build_power_novelty_bundle(seed=NOVELTY_SEED)
    (EXP / "POWER_NOVELTY.md").write_text(novelty, encoding="utf-8")
    pr = retrieve_gbrain(mode="power_seed", creative_direction=AUTHOR_DIRECTION, world_vision=world)
    hr = retrieve_gbrain(mode="human_seed", creative_direction=AUTHOR_DIRECTION, world_vision=world)
    (EXP / "POWER_GBRAIN.md").write_text(pr["result"], encoding="utf-8")
    (EXP / "HUMAN_GBRAIN.md").write_text(hr["result"], encoding="utf-8")
    dump(EXP / "POWER_RETRIEVAL.json", retrieval_meta(pr))
    dump(EXP / "HUMAN_RETRIEVAL.json", retrieval_meta(hr))
    pp = generate_split_prompt(mode="power_seed", world_vision=world, creative_state=state, gbrain_inspiration=pr["result"], power_novelty=novelty)
    hp = generate_split_prompt(mode="human_seed", world_vision=world, creative_state=state, gbrain_inspiration=hr["result"])
    (EXP / "POWER_PROMPT.md").write_text(pp, encoding="utf-8")
    (EXP / "HUMAN_PROMPT.md").write_text(hp, encoding="utf-8")
    with ThreadPoolExecutor(max_workers=2) as ex:
        fp = ex.submit(run_acp, EXP / "POWER_PROMPT.md", EXP / "POWER_ACP.json", "gpt-5.6-luna", "high", "fast20-power")
        fh = ex.submit(run_acp, EXP / "HUMAN_PROMPT.md", EXP / "HUMAN_ACP.json", "gpt-5.6-luna", "high", "fast20-human")
        pd, hd = fp.result(), fh.result()
    powers = model_text(pd, EXP / "POWER_CANDIDATES.md")
    humans = model_text(hd, EXP / "HUMAN_CANDIDATES.md")
    pblocks = numbered_blocks(powers, "POWER CANDIDATE", 3)
    hblocks = numbered_blocks(humans, "HUMAN CANDIDATE", 4)

    psel = f"""你是匿名 Power Selector。完全看不到 Human、Biography、Story 或未来世界。只根据当前世界力量正常值与三个 Power Candidate 盲选一个最适合高强度男频长篇的开局 Core Asymmetry。\n\n优先级：1) 普通读者立刻想拥有；2) 相对同层明显不公平，最好有条件越级；3) 一句话能懂；4) 能跨不同世界与兵器/身体/环境/传承产生复合；5) Permanent Boundary 仍成立。不要因为平衡而选弱的，也不要为第二世界做任何定制。\n\n严格输出：\nSELECT: 1/2/3\nREASON: 3—6句，不新增机制。\n\n# POWER BASELINE\n{project_character_power_baseline(world)}\n\n# CANDIDATES\n{powers}\n"""
    hsel = f"""你是匿名 Human Selector。完全看不到 Power、Story、未来奖励或未来世界。只根据当前普通生活背景与四个 Human Candidate，盲选一个最适合高强度长篇、但仍然像具体人的主角。\n\n优先级：1) 有直接私人欲望和行动性；2) competing motives 真会冲突，不是正确人格；3) 稳定选择偏向清楚但实现方式可变化；4) 至少一个具体关系能真正改变取舍；5) 能承受快速世界切换而不退化成成长最优算法。钱、胜负、虚荣、性欲、审美、享受、自利、报复、偏心、野心都合法。不要按道德评分。\n\n严格输出：\nSELECT: 1/2/3/4\nREASON: 3—6句，不新增人物事实。\n\n# LIFE CONTEXT\n{project_character_life_context(world)}\n\n# CANDIDATES\n{humans}\n"""
    (EXP / "POWER_SELECTOR_PROMPT.md").write_text(psel, encoding="utf-8")
    (EXP / "HUMAN_SELECTOR_PROMPT.md").write_text(hsel, encoding="utf-8")
    with ThreadPoolExecutor(max_workers=2) as ex:
        fp = ex.submit(run_acp, EXP / "POWER_SELECTOR_PROMPT.md", EXP / "POWER_SELECTOR_ACP.json", "gpt-5.6-luna", "high", "fast20-power-select")
        fh = ex.submit(run_acp, EXP / "HUMAN_SELECTOR_PROMPT.md", EXP / "HUMAN_SELECTOR_ACP.json", "gpt-5.6-luna", "high", "fast20-human-select")
        psd, hsd = fp.result(), fh.result()
    pst = model_text(psd, EXP / "POWER_SELECTOR.md")
    hst = model_text(hsd, EXP / "HUMAN_SELECTOR.md")
    pi = select_index(pst, 3)
    hi = select_index(hst, 4)
    power = re.sub(r"(?m)^# POWER CANDIDATE \d+｜", "# POWER SEED｜", pblocks[pi - 1], count=1)
    human = re.sub(r"(?m)^# HUMAN CANDIDATE \d+｜", "# HUMAN SEED｜", hblocks[hi - 1], count=1)
    (EXP / "POWER_SEED.md").write_text(power + "\n", encoding="utf-8")
    (EXP / "HUMAN_SEED.md").write_text(human + "\n", encoding="utf-8")
    dump(EXP / "SELECTION.json", {"power": pi, "human": hi})

    character = compose_character_card(power_seed=power, human_seed=human)
    ha = split_human_seed_authorities(human)
    (EXP / "CHARACTER.md").write_text(character, encoding="utf-8")
    (EXP / "CHARACTER_INITIAL_STATE.md").write_text(ha["initial_state"], encoding="utf-8")
    (EXP / "CHARACTER_AUDITION.md").write_text(ha["audition_metadata"], encoding="utf-8")

    cs = {"world_vision": {"status": "author_approved"}, "character_card": {"status": "author_approved"}}
    sr = retrieve_gbrain(mode="idea", creative_direction=AUTHOR_DIRECTION, world_vision=world, character_card=character)
    (EXP / "STORY_GBRAIN.md").write_text(sr["result"], encoding="utf-8")
    dump(EXP / "STORY_RETRIEVAL.json", retrieval_meta(sr))
    sp = generate_split_prompt(mode="idea", creative_direction=AUTHOR_DIRECTION, world_vision=world, character_card=character, character_initial_state=ha["initial_state"], creative_state=cs, gbrain_inspiration=sr["result"])
    (EXP / "STORY_PROGRAM_PROMPT.md").write_text(sp, encoding="utf-8")
    sd = run_acp(EXP / "STORY_PROGRAM_PROMPT.md", EXP / "STORY_PROGRAM_ACP.json", "gpt-5.6-sol", "high", "fast20-story")
    story = model_text(sd, EXP / "STORY_PROGRAM.md")
    handoff = extract_world_horizon_handoff(story)
    (EXP / "WORLD_HORIZON_HANDOFF.md").write_text(handoff + "\n", encoding="utf-8")

    os = {"world_vision": {"status": "author_approved"}, "character_card": {"status": "author_approved"}, "proposal": {"status": "author_approved"}}
    orr = retrieve_gbrain(mode="outline", creative_direction=AUTHOR_DIRECTION, world_vision=world, character_card=character, proposal_context=story)
    (EXP / "OUTLINE_GBRAIN.md").write_text(orr["result"], encoding="utf-8")
    dump(EXP / "OUTLINE_RETRIEVAL.json", retrieval_meta(orr))
    op = generate_split_prompt(mode="outline", creative_direction=AUTHOR_DIRECTION, world_vision=world, character_card=character, character_initial_state=ha["initial_state"], creative_state=os, proposal_context=story, gbrain_inspiration=orr["result"])
    (EXP / "OUTLINE_PROMPT.md").write_text(op, encoding="utf-8")
    od = run_acp(EXP / "OUTLINE_PROMPT.md", EXP / "OUTLINE_ACP.json", "gpt-5.6-luna", "high", "fast20-outline")
    outline = clean(od["text"])
    p = outline.find("# 小说总体设计画像")
    if p >= 0:
        outline = outline[p:]
    validate_book_content_for_save(outline)
    (EXP / "OUTLINE.md").write_text(outline + "\n", encoding="utf-8")
    (EXP / "BOOK.md").write_text(outline + "\n", encoding="utf-8")
    log(f"UPSTREAM COMPLETE power={pi} human={hi} handoff_chars={len(handoff)}")


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


def plan_source(n: int) -> str:
    if n <= 10:
        replan = EXP / "REPLAN_AFTER_CH1.md"
        if n >= 2 and replan.exists():
            return replan.read_text(encoding="utf-8")
        return sections()["small_plan"]
    return (EXP / "REVIEW_0010.md").read_text(encoding="utf-8")


def chapter_plan(n: int) -> str:
    src = plan_source(n)
    next_n = n + 1
    pat = rf"(?ms)^## 第{n}章：.*?(?=^## 第{next_n}章：|\Z)"
    m = re.search(pat, src)
    if not m:
        raise RuntimeError(f"missing chapter {n} plan")
    return m.group(0).strip()


def long_block(n: int) -> str:
    """Return only a long block that explicitly covers this chapter.

    A missing post-review block is not permission to fall back to the entire old
    long plan: that would re-inject stale Chapter 1—10 authority into later chapters.
    The production runtime also filters explicit stale ranges, but the batch runner
    fails closed here so the dirty context is never generated in the first place.
    """

    src = sections()["long_plan"]
    blocks = list(
        re.finditer(
            r"(?ms)^## 第(\d+)[—-](\d+)章：.*?(?=^## 第\d+[—-]\d+章：|\Z)",
            src,
        )
    )
    for match in blocks:
        if int(match.group(1)) <= n <= int(match.group(2)):
            return match.group(0).strip()
    return ""


def rd(n: int) -> Path:
    d = EXP / "runs" / f"chapter-{n:04d}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def run_stage(n: int, stage: str, prompt: str, model: str, effort: str) -> str:
    pp = rd(n) / f"{stage}_prompt.md"
    ap = rd(n) / f"{stage}_acp.json"
    rp = rd(n) / f"{stage}_response.md"
    pp.write_text(prompt, encoding="utf-8")
    data = run_acp(pp, ap, model, effort, f"fast20-ch{n:02d}-{stage}")
    return model_text(data, rp)


def make_review() -> None:
    mem = memory()
    story = (EXP / "STORY_PROGRAM.md").read_text(encoding="utf-8")
    handoff = (EXP / "WORLD_HORIZON_HANDOFF.md").read_text(encoding="utf-8")
    future = sections()["long_plan"] + "\n\n# WORLD HORIZON HANDOFF\n" + handoff
    rp = generate_prompt(
        mode="review",
        template="",
        book_content=book(),
        creative_direction=AUTHOR_DIRECTION + "\n\n本次 Review 的唯一范围是第11—20章；第20章必须完成第一 Local World 顶层结算并停在已批准 Handoff，不得越界写第二世界。",
        actual_summaries=mem.get("recent_summaries", ""),
        current_state=mem.get("active_scene_state", "") + "\n\n" + mem.get("persistent_canon", ""),
        unfulfilled_promises=mem.get("open_promises", ""),
        future_direction=future,
        gbrain_inspiration="",
    )
    (EXP / "REVIEW_0010_PROMPT.md").write_text(rp, encoding="utf-8")
    data = run_acp(EXP / "REVIEW_0010_PROMPT.md", EXP / "REVIEW_0010_ACP.json", "gpt-5.6-luna", "high", "fast20-review10")
    text = model_text(data, EXP / "REVIEW_0010.md")
    for n in range(11, 21):
        if not re.search(rf"(?m)^## 第{n}章：", text):
            raise RuntimeError(f"Review missing chapter {n}")
    log("REVIEW 10 COMPLETE")


def generate_chapter(n: int) -> None:
    world = (EXP / "WORLD_VISION.md").read_text(encoding="utf-8")
    character = (EXP / "CHARACTER.md").read_text(encoding="utf-8")
    plan = chapter_plan(n)
    block = long_block(n)
    base_direction = "严格执行当前批准的高强度20章第一世界计划。节奏快=高密度不可逆 State Change，不等于每章升级；每章必须让目标、关系、力量、身份、知识、敌人或世界局面至少有一项真正向前。避免程序化实施与重复证明。当前章 Plan 是本章事件上限：结尾只能制造下一章为什么必须发生，不能提前执行下一章的首个事件、结算或 payoff；Canon 已经完成的事实不得在本章重新表演。第20章必须完成当前 Local World 顶层结算并停在 Handoff，不越界创造第二世界。"

    dp = generate_prompt(
        mode="director", template="", book_content=book(), world_vision=world, world_expansions="", character_card=character,
        current_long_block=block, previous_chapter_text=previous(n), current_outline="", current_chapter_plan=plan,
        recent_summaries=recent(), chapter_number=n, creative_direction=base_direction,
    )
    dr = run_stage(n, "director", dp, "gpt-5.6-luna", "high")

    cp = generate_prompt(
        mode="context_curator", template="", book_content=book(), world_vision=world, world_expansions="", character_card=character,
        current_long_block=block, previous_chapter_text=previous(n), current_outline=dr, current_chapter_plan=plan,
        recent_summaries=recent(), gbrain_inspiration="", chapter_number=n,
    )
    cu = run_stage(n, "curator", cp, "gpt-5.6-luna", "high")

    pp = generate_prompt(
        mode="primary_writer", template="", book_content=book(), world_vision=world, world_expansions="", character_card=character,
        current_long_block=block, previous_chapter_text=previous(n), current_outline=dr, current_chapter_plan=plan,
        recent_summaries=recent(), gbrain_inspiration="", curated_context=cu, curator_response=cu, chapter_number=n,
    )
    pr = run_stage(n, "primary", pp, "gpt-5.6-terra", "high")
    primary_body = extract_primary_draft(pr).strip()
    validate_chapter_body_for_save(primary_body)

    arp = generate_prompt(
        mode="authority_reviser", template="", book_content=book(), world_vision=world, world_expansions="", character_card=character,
        current_long_block=block, previous_chapter_text=previous(n), current_outline=dr, current_chapter_plan=plan,
        recent_summaries=recent(), curated_context=cu, curator_response=cu, primary_draft=primary_body, primary_writer_response=pr,
        chapter_number=n,
    )
    ar = run_stage(n, "authority_reviser", arp, "gpt-5.6-luna", "high")
    final_body = extract_primary_draft(ar).strip()
    validate_chapter_body_for_save(final_body)
    if len(final_body) < 1800:
        raise RuntimeError(f"chapter {n} too short: {len(final_body)}")
    (EXP / "chapters" / f"chapter-{n:04d}.md").write_text(final_body + "\n", encoding="utf-8")

    sp = generate_prompt(mode="state_delta", template="", book_content=book(), recent_summaries=recent(), chapter_number=n, chapter_prose=final_body)
    st = run_stage(n, "state", sp, "gpt-5.6-luna", "low")
    updated = apply_state_delta_to_book(book(), n, st)
    validate_book_content_for_save(updated)
    (EXP / "BOOK.md").write_text(updated, encoding="utf-8")
    log(f"CHAPTER {n} COMPLETE chars={len(final_body)}")


def finalize() -> None:
    chapters = []
    for n in range(1, 21):
        p = EXP / "chapters" / f"chapter-{n:04d}.md"
        if not p.exists():
            raise RuntimeError(f"missing {p}")
        chapters.append(p.read_text(encoding="utf-8").strip())
    combined = "\n\n".join(chapters) + "\n"
    (EXP / "CHAPTERS_0001_0020.md").write_text(combined, encoding="utf-8")
    (EXP / "CHAPTERS_0001_0020.txt").write_text(combined, encoding="utf-8")
    src = "\n\n".join([
        "# WORLD\n" + (EXP / "WORLD_VISION.md").read_text(encoding="utf-8"),
        "# POWER\n" + (EXP / "POWER_SEED.md").read_text(encoding="utf-8"),
        "# HUMAN\n" + (EXP / "HUMAN_SEED.md").read_text(encoding="utf-8"),
        "# CHARACTER\n" + (EXP / "CHARACTER.md").read_text(encoding="utf-8"),
        "# STORY PROGRAM\n" + (EXP / "STORY_PROGRAM.md").read_text(encoding="utf-8"),
        "# FINAL BOOK STATE\n" + book(),
    ])
    (EXP / "SUMMARY_SOURCE.md").write_text(src, encoding="utf-8")
    dump(EXP / "RUN_COMPLETE.json", {"chapters": 20, "combined_chars": len(combined), "completed": True})
    log(f"ALL COMPLETE combined_chars={len(combined)}")


def main() -> None:
    if not RUNNER.exists():
        raise RuntimeError(f"missing ACP runner: {RUNNER}")
    generate_upstream()
    for n in range(1, 21):
        generate_chapter(n)
        if n == 10:
            make_review()
    finalize()


if __name__ == "__main__":
    main()

