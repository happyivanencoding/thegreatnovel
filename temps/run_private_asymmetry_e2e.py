from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
EXP = ROOT / "books" / "real-exp-private-prototype-asymmetry-novel-20260826-v2"
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.character_seeds import compose_character_card, split_human_seed_authorities
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.hybrid_runtime import extract_primary_draft
from story_mvp.power_novelty import build_power_novelty_bundle
from story_mvp.prompts import generate_prompt, parse_canon_memory
from story_mvp.storage import (
    apply_state_delta_to_book,
    parse_book_sections,
    validate_book_content_for_save,
    validate_chapter_body_for_save,
)

AUTHOR_DIRECTION = """成熟中文男频玄幻/武道成长长篇。生成一本真正全新的书：不复用近期实验中的九垣界、景息/天景、霜钟泽、澜照界、万灯河、赤脉山、黑日岛、分流真元、落景，也不复用上一 rejected attempt 的衡阶、承骨、重泉、坠铁、压潮、九折峡等指纹。世界的主要欲望与大事件优先落在人本身的力量与战斗、武技/功法、神兵奇物、身体/血脉/体质、怪物与狩猎、秘境遗迹、宗派/强者竞争、公开排名/试炼和真正高价值获得；道路、桥梁、运输、迁城、矿务、生产、维护、治理、资源分配只能是背景，不得成为世界的主要价值重心或长期故事发动机。世界与力量可以创新，但不要靠生造抽象名词制造新鲜感；读者第一次遇到规则时应先看懂它具体能做什么。力量体系要有世界内真实使用、可长期反复比较的主尺，并有值得羡慕的天才、高阶强者与高价值力量/物品/地点。Core Power 默认宁强勿弱，要让同层普通人/天才明显羡慕，并允许有条件的越级优势。World 阶段完全不知道未来主角是谁。"""

RECENT_FINGERPRINTS = (
    "九垣界", "景息", "天景", "霜钟泽", "澜照界", "万灯河", "赤脉山", "黑日岛", "分流真元", "落景",
    "衡阶", "承骨", "重泉", "坠铁", "压潮", "九折峡", "悬河古道", "白石盐海"
)
PROTOTYPE_MARKERS = ("prism-wanderer-alpha", "pwaalpha", "private-prototype")
NOVELTY_SEED = 2026082607


def dump_meta(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_acp(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not payload.get("ok"):
        raise RuntimeError(payload.get("error", "ACP failed"))
    return payload


def clean_model_text(text: str) -> str:
    text = re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text)
    return text.strip()


def save_model_text(acp_path: Path, out_path: Path) -> str:
    payload = load_acp(acp_path)
    text = clean_model_text(payload["text"])
    out_path.write_text(text + "\n", encoding="utf-8")
    dump_meta(out_path.with_suffix(".meta.json"), {k: payload.get(k) for k in ("model", "effort", "wall_seconds", "sessionId")})
    return text


def retrieval_meta(result: dict) -> dict:
    return {
        "query_strategy": result.get("query_strategy"),
        "query_texts": result.get("query_texts"),
        "accepted_count": result.get("accepted_count"),
        "accepted": [{"slug": x.get("slug"), "score": x.get("score")} for x in result.get("accepted", [])],
        "rejected_count": result.get("rejected_count"),
        "final_limit": result.get("final_limit"),
        "prototype_id": result.get("prototype_id", ""),
        "prototype_selected": result.get("prototype_selected", False),
    }


def init() -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    (EXP / "chapters").mkdir(exist_ok=True)
    (EXP / "runs").mkdir(exist_ok=True)
    (EXP / "AUTHOR_DIRECTION.md").write_text(AUTHOR_DIRECTION + "\n", encoding="utf-8")
    (EXP / "PROTOCOL.md").write_text(
        "# Protocol\n\n"
        "- Fresh protagonist-blind World; no reuse of prior book authority.\n"
        "- Power and Human run in fresh independent contexts.\n"
        "- Power receives deterministic 3-candidate Novelty Spark bundle plus current Power Asymmetry production rules.\n"
        "- Human uses explicit anonymous prototype selector `prism-wanderer-alpha`; no real identity/source details enter artifacts.\n"
        "- Power selection is blind to Human and precommitted to reader appetite + comparative privilege + simplicity + long-form compoundability.\n"
        "- Deterministic Character composition; Sol Story Program; Luna Outline; 5 serial chapters with State after each chapter.\n"
        "- Default chapter route: Luna Director -> Luna Curator -> Terra Primary -> Luna low State.\n",
        encoding="utf-8",
    )
    ret = retrieve_gbrain(mode="world_vision", creative_direction=AUTHOR_DIRECTION)
    (EXP / "WORLD_GBRAIN.md").write_text(ret["result"], encoding="utf-8")
    dump_meta(EXP / "WORLD_RETRIEVAL_META.json", retrieval_meta(ret))
    prompt = generate_split_prompt(mode="world_vision", creative_direction=AUTHOR_DIRECTION, gbrain_inspiration=ret["result"])
    (EXP / "WORLD_PROMPT.md").write_text(prompt, encoding="utf-8")
    print(json.dumps({"exp": str(EXP), "world_prompt_chars": len(prompt), "world_gbrain": [x.get("slug") for x in ret.get("accepted", [])]}, ensure_ascii=False))


def mat_world() -> None:
    text = save_model_text(EXP / "WORLD_ACP.json", EXP / "WORLD_VISION.md")
    hits = [x for x in RECENT_FINGERPRINTS if x in text]
    dump_meta(EXP / "WORLD_FINGERPRINT_CHECK.json", {"hits": hits, "pass": not hits})
    if hits:
        raise RuntimeError(f"World reused recent fingerprints: {hits}")
    print(json.dumps({"world_chars": len(text), "fingerprint_pass": True}, ensure_ascii=False))


def build_split() -> None:
    world = (EXP / "WORLD_VISION.md").read_text(encoding="utf-8")
    state = {"world_vision": {"status": "author_approved"}}
    novelty = build_power_novelty_bundle(seed=NOVELTY_SEED)
    (EXP / "POWER_NOVELTY.md").write_text(novelty, encoding="utf-8")

    pret = retrieve_gbrain(mode="power_seed", creative_direction=AUTHOR_DIRECTION, world_vision=world)
    (EXP / "POWER_GBRAIN.md").write_text(pret["result"], encoding="utf-8")
    dump_meta(EXP / "POWER_RETRIEVAL_META.json", retrieval_meta(pret))
    pp = generate_split_prompt(
        mode="power_seed", world_vision=world, creative_state=state,
        gbrain_inspiration=pret["result"], power_novelty=novelty,
    )
    if any(marker in pp for marker in PROTOTYPE_MARKERS):
        raise RuntimeError("Power prompt leaked prototype")
    (EXP / "POWER_PROMPT.md").write_text(pp, encoding="utf-8")

    hret = retrieve_gbrain(
        mode="human_seed", creative_direction=AUTHOR_DIRECTION, world_vision=world,
        prototype_id="prism-wanderer-alpha",
    )
    (EXP / "HUMAN_GBRAIN.md").write_text(hret["result"], encoding="utf-8")
    dump_meta(EXP / "HUMAN_RETRIEVAL_META.json", retrieval_meta(hret))
    hp = generate_split_prompt(
        mode="human_seed", world_vision=world, creative_state=state,
        gbrain_inspiration=hret["result"], prototype_id="prism-wanderer-alpha",
    )
    (EXP / "HUMAN_PROMPT.md").write_text(hp, encoding="utf-8")
    print(json.dumps({
        "novelty_seed": NOVELTY_SEED,
        "sparks": [line for line in novelty.splitlines() if line.startswith("熟悉幻想：") or line.startswith("单一异常：")],
        "power_gbrain": [x.get("slug") for x in pret.get("accepted", [])],
        "human_gbrain": [x.get("slug") for x in hret.get("accepted", [])],
    }, ensure_ascii=False))


def mat_power_human() -> None:
    power = save_model_text(EXP / "POWER_ACP.json", EXP / "POWER_CANDIDATES.md")
    human = save_model_text(EXP / "HUMAN_ACP.json", EXP / "HUMAN_SEED.md")
    if power.count("# POWER CANDIDATE") != 3:
        raise RuntimeError(f"Expected 3 Power candidates, got {power.count('# POWER CANDIDATE')}")
    if "# HUMAN SEED" not in human:
        raise RuntimeError("Human output missing HUMAN SEED")
    if any(marker in human for marker in PROTOTYPE_MARKERS):
        raise RuntimeError("Human output leaked prototype id")
    print(json.dumps({"power_chars": len(power), "human_chars": len(human)}, ensure_ascii=False))


def build_selector() -> None:
    world = (EXP / "WORLD_VISION.md").read_text(encoding="utf-8")
    power = (EXP / "POWER_CANDIDATES.md").read_text(encoding="utf-8")
    prompt = f"""你是匿名 Power Selector。你完全看不到 Human Seed、主角人格、Biography、Story Program 或未来剧情，只根据已批准 World 与 3 个 Power Candidate 做一次预先承诺的盲选。

选择目标按优先级：
1. Primitive reader pull：普通男频读者会不会立刻想拥有；
2. Comparative privilege：相对同层普通人/天才，是否有清楚、明显、值得羡慕的超标特权，最好存在有条件越级窗口；
3. Simplicity：一句大白话能懂，不能靠术语或复杂机制才显得厉害；
4. Long-form compoundability：以后能否与功法、兵器/法宝、身体/血脉、环境、传承等产生新化学反应，而不只是数字变大；
5. Spark fidelity / boundary：强度不能靠删除候选自己的单一异常或边界取得。

不要为了多样性平均照顾三个候选，也不要因为“更平衡”偏爱较弱能力。默认成熟中文男频成长幻想，宁可明显偏强，也不要只是方便或灵活。

严格输出：
SELECT: 1/2/3
REASON: 3—6 句，分别说明最直接欲望、同层/越级优势、简单度、长期复合性；不得新增或改写能力事实。

# WORLD
{world}

# POWER CANDIDATES
{power}
"""
    (EXP / "POWER_SELECTOR_PROMPT.md").write_text(prompt, encoding="utf-8")
    print(json.dumps({"selector_prompt_chars": len(prompt)}, ensure_ascii=False))


def candidate_blocks(text: str) -> list[str]:
    starts = [m.start() for m in re.finditer(r"(?m)^# POWER CANDIDATE \d+", text)]
    if len(starts) != 3:
        raise RuntimeError("Cannot parse 3 power candidates")
    starts.append(len(text))
    return [text[starts[i]:starts[i+1]].strip() for i in range(3)]


def apply_selector() -> None:
    sel = save_model_text(EXP / "POWER_SELECTOR_ACP.json", EXP / "POWER_SELECTOR_RESPONSE.md")
    m = re.search(r"(?m)^SELECT:\s*([123])\s*$", sel)
    if not m:
        raise RuntimeError(f"Invalid selector output: {sel[:300]}")
    idx = int(m.group(1))
    blocks = candidate_blocks((EXP / "POWER_CANDIDATES.md").read_text(encoding="utf-8"))
    chosen = blocks[idx - 1]
    chosen = re.sub(r"^# POWER CANDIDATE \d+｜.*$", "# POWER SEED", chosen, count=1, flags=re.M)
    (EXP / "POWER_SEED.md").write_text(chosen.strip() + "\n", encoding="utf-8")
    dump_meta(EXP / "SELECTION.json", {"selected": idx})
    print(json.dumps({"selected": idx, "power_seed_chars": len(chosen)}, ensure_ascii=False))


def build_character_story() -> None:
    world = (EXP / "WORLD_VISION.md").read_text(encoding="utf-8")
    power = (EXP / "POWER_SEED.md").read_text(encoding="utf-8")
    human = (EXP / "HUMAN_SEED.md").read_text(encoding="utf-8")
    character = compose_character_card(power_seed=power, human_seed=human)
    parts = split_human_seed_authorities(human)
    (EXP / "CHARACTER.md").write_text(character, encoding="utf-8")
    (EXP / "CHARACTER_INITIAL_STATE.md").write_text(parts["initial_state"], encoding="utf-8")
    (EXP / "CHARACTER_AUDITION.md").write_text(parts["audition_metadata"], encoding="utf-8")
    state = {"world_vision": {"status": "author_approved"}, "character_card": {"status": "author_approved"}}
    ret = retrieve_gbrain(
        mode="idea", creative_direction=AUTHOR_DIRECTION, world_vision=world,
        character_card=character, proposal_context="",
    )
    (EXP / "STORY_GBRAIN.md").write_text(ret["result"], encoding="utf-8")
    dump_meta(EXP / "STORY_RETRIEVAL_META.json", retrieval_meta(ret))
    prompt = generate_split_prompt(
        mode="idea", creative_direction=AUTHOR_DIRECTION, world_vision=world,
        character_card=character, character_initial_state=parts["initial_state"],
        creative_state=state, gbrain_inspiration=ret["result"],
    )
    (EXP / "STORY_PROGRAM_PROMPT.md").write_text(prompt, encoding="utf-8")
    print(json.dumps({"character_chars": len(character), "story_gbrain": [x.get("slug") for x in ret.get("accepted", [])], "story_prompt_chars": len(prompt)}, ensure_ascii=False))


def mat_story_build_outline() -> None:
    story = save_model_text(EXP / "STORY_PROGRAM_ACP.json", EXP / "STORY_PROGRAM.md")
    world = (EXP / "WORLD_VISION.md").read_text(encoding="utf-8")
    character = (EXP / "CHARACTER.md").read_text(encoding="utf-8")
    initial = (EXP / "CHARACTER_INITIAL_STATE.md").read_text(encoding="utf-8")
    state = {
        "world_vision": {"status": "author_approved"},
        "character_card": {"status": "author_approved"},
        "proposal": {"status": "author_approved"},
    }
    ret = retrieve_gbrain(
        mode="outline", creative_direction=AUTHOR_DIRECTION, world_vision=world,
        character_card=character, proposal_context=story,
    )
    (EXP / "OUTLINE_GBRAIN.md").write_text(ret["result"], encoding="utf-8")
    dump_meta(EXP / "OUTLINE_RETRIEVAL_META.json", retrieval_meta(ret))
    prompt = generate_split_prompt(
        mode="outline", creative_direction=AUTHOR_DIRECTION, world_vision=world,
        character_card=character, character_initial_state=initial,
        creative_state=state, proposal_context=story, gbrain_inspiration=ret["result"],
    )
    (EXP / "OUTLINE_PROMPT.md").write_text(prompt, encoding="utf-8")
    print(json.dumps({"story_chars": len(story), "outline_gbrain": [x.get("slug") for x in ret.get("accepted", [])], "outline_prompt_chars": len(prompt)}, ensure_ascii=False))


def mat_outline() -> None:
    payload = load_acp(EXP / "OUTLINE_ACP.json")
    text = clean_model_text(payload["text"])
    p = text.find("# 小说总体设计画像")
    if p >= 0:
        text = text[p:]
    validate_book_content_for_save(text)
    (EXP / "OUTLINE.md").write_text(text + "\n", encoding="utf-8")
    (EXP / "BOOK.md").write_text(text + "\n", encoding="utf-8")
    dump_meta(EXP / "OUTLINE.meta.json", {k: payload.get(k) for k in ("model", "effort", "wall_seconds", "sessionId")})
    print(json.dumps({"outline_chars": len(text), "book_valid": True}, ensure_ascii=False))


def book() -> str:
    return (EXP / "BOOK.md").read_text(encoding="utf-8")


def sections() -> dict:
    return parse_book_sections(book())


def recent() -> str:
    return parse_canon_memory(sections()["status"]).get("recent_summaries", "").strip()


def previous(n: int) -> str:
    if n <= 1:
        return ""
    return (EXP / "chapters" / f"chapter-{n-1:04d}.md").read_text(encoding="utf-8")


def chapter_plan(n: int) -> str:
    s = sections()["small_plan"]
    pat = rf"(?ms)^## 第{n}章：.*?(?=^## 第{n+1}章：|\Z)"
    m = re.search(pat, s)
    if not m:
        raise RuntimeError(f"missing chapter {n} plan")
    return m.group(0).strip()


def long_block(n: int) -> str:
    s = sections()["long_plan"]
    blocks = list(re.finditer(r"(?ms)^## 第(\d+)[—-](\d+)章：.*?(?=^## 第\d+[—-]\d+章：|\Z)", s))
    for m in blocks:
        if int(m.group(1)) <= n <= int(m.group(2)):
            return m.group(0).strip()
    return s[:7000].strip()


def rd(n: int) -> Path:
    path = EXP / "runs" / f"chapter-{n:04d}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_prompt(n: int, stage: str, text: str) -> None:
    (rd(n) / f"{stage}_prompt.md").write_text(text, encoding="utf-8")


def materialize(n: int, stage: str) -> None:
    payload = load_acp(rd(n) / f"{stage}_acp.json")
    text = clean_model_text(payload["text"])
    (rd(n) / f"{stage}_response.md").write_text(text + "\n", encoding="utf-8")
    dump_meta(rd(n) / f"{stage}_meta.json", {k: payload.get(k) for k in ("model", "effort", "wall_seconds", "sessionId")})
    print(json.dumps({"chapter": n, "stage": stage, "chars": len(payload["text"])}, ensure_ascii=False))


def director(n: int) -> None:
    prompt = generate_prompt(
        mode="director", template="", book_content=book(), current_long_block=long_block(n),
        previous_chapter_text=previous(n), current_outline="", current_chapter_plan=chapter_plan(n),
        recent_summaries=recent(), chapter_number=n,
        creative_direction="严格执行已批准的新 private-prototype / Power Asymmetry 小说与当前 Outline。优先真实人物欲望、强金手指兑现和世界内力量尺比较；规则先白话后命名，Supporting Logic 不得成为 Story Engine。不要让等级比较变成报表，但关键突破/越级/新强敌后读者必须知道主角在哪档、哪里超标。",
    )
    save_prompt(n, "director", prompt)


def curator(n: int) -> None:
    dr = (rd(n) / "director_response.md").read_text(encoding="utf-8")
    ret = retrieve_gbrain(mode="context_curator", book_content=book(), current_long_block=long_block(n), current_outline=dr, recent_summaries=recent())
    dump_meta(rd(n) / "curator_retrieval.json", {k: v for k, v in ret.items() if k not in {"raw_stdout", "result"}})
    (rd(n) / "scene_skill.md").write_text(ret["result"], encoding="utf-8")
    prompt = generate_prompt(
        mode="context_curator", template="", book_content=book(), current_long_block=long_block(n),
        previous_chapter_text=previous(n), current_outline=dr, current_chapter_plan=chapter_plan(n),
        recent_summaries=recent(), gbrain_inspiration=ret["result"], chapter_number=n,
    )
    save_prompt(n, "curator", prompt)
    print(json.dumps({"accepted": [x.get("slug") for x in ret.get("accepted", [])]}, ensure_ascii=False))


def primary(n: int) -> None:
    dr = (rd(n) / "director_response.md").read_text(encoding="utf-8")
    cu = (rd(n) / "curator_response.md").read_text(encoding="utf-8")
    sk = (rd(n) / "scene_skill.md").read_text(encoding="utf-8")
    prompt = generate_prompt(
        mode="primary_writer", template="", book_content=book(), current_long_block=long_block(n),
        previous_chapter_text=previous(n), current_outline=dr, current_chapter_plan=chapter_plan(n),
        recent_summaries=recent(), gbrain_inspiration=sk, curated_context=cu, chapter_number=n,
    )
    save_prompt(n, "primary", prompt)


def body(n: int) -> None:
    payload = load_acp(rd(n) / "primary_acp.json")
    raw = clean_model_text(payload["text"])
    (rd(n) / "primary_response.md").write_text(raw + "\n", encoding="utf-8")
    b = extract_primary_draft(raw).strip()
    validate_chapter_body_for_save(b)
    if len(b) < 1800:
        raise RuntimeError(f"chapter {n} too short: {len(b)}")
    (EXP / "chapters" / f"chapter-{n:04d}.md").write_text(b + "\n", encoding="utf-8")
    dump_meta(rd(n) / "primary_meta.json", {k: payload.get(k) for k in ("model", "effort", "wall_seconds", "sessionId")})
    print(json.dumps({"chapter": n, "body_chars": len(b)}, ensure_ascii=False))


def state(n: int) -> None:
    prose = (EXP / "chapters" / f"chapter-{n:04d}.md").read_text(encoding="utf-8")
    prompt = generate_prompt(mode="state_delta", template="", book_content=book(), recent_summaries=recent(), chapter_number=n, chapter_prose=prose)
    save_prompt(n, "state", prompt)


def apply_state(n: int) -> None:
    payload = load_acp(rd(n) / "state_acp.json")
    text = clean_model_text(payload["text"])
    (rd(n) / "state_response.md").write_text(text + "\n", encoding="utf-8")
    updated = apply_state_delta_to_book(book(), n, text)
    validate_book_content_for_save(updated)
    (EXP / "BOOK.md").write_text(updated, encoding="utf-8")
    dump_meta(rd(n) / "state_meta.json", {k: payload.get(k) for k in ("model", "effort", "wall_seconds", "sessionId")})
    print(json.dumps({"chapter": n, "book_chars": len(updated)}, ensure_ascii=False))


def combine() -> None:
    chunks = []
    for n in range(1, 6):
        chunks.append((EXP / "chapters" / f"chapter-{n:04d}.md").read_text(encoding="utf-8").strip())
    text = "\n\n".join(chunks) + "\n"
    (EXP / "READER_COPY_0001_0005.md").write_text(text, encoding="utf-8")
    (EXP / "READER_COPY_0001_0005.txt").write_text(text, encoding="utf-8")
    print(json.dumps({"combined_chars": len(text)}, ensure_ascii=False))


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "init": init()
    elif action == "mat-world": mat_world()
    elif action == "build-split": build_split()
    elif action == "mat-power-human": mat_power_human()
    elif action == "build-selector": build_selector()
    elif action == "apply-selector": apply_selector()
    elif action == "build-character-story": build_character_story()
    elif action == "mat-story-build-outline": mat_story_build_outline()
    elif action == "mat-outline": mat_outline()
    elif action == "combine": combine()
    elif action in {"director", "curator", "primary", "body", "state", "apply", "materialize"}:
        n = int(sys.argv[2])
        if action == "director": director(n)
        elif action == "curator": curator(n)
        elif action == "primary": primary(n)
        elif action == "body": body(n)
        elif action == "state": state(n)
        elif action == "apply": apply_state(n)
        else: materialize(n, sys.argv[3])
    else:
        raise SystemExit(f"unknown action {action}")
