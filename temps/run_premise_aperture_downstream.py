from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import re
import subprocess
import sys


ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-premise-aperture-20260829-v1" / "fast_multiworld"
EXP = BASE / "downstream_C2"
RUNNER = ROOT / "temps" / "acp_readonly_runner.mjs"
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.character_prompts import generate_split_prompt  # noqa: E402
from story_mvp.character_seeds import compose_character_card, split_human_seed_authorities  # noqa: E402
from story_mvp.gbrain_retrieval import retrieve_gbrain  # noqa: E402
from story_mvp.long_form_evolution import extract_world_horizon_handoff  # noqa: E402
from story_mvp.storage import validate_book_content_for_save  # noqa: E402


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def dump(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def retrieval_meta(result: dict) -> dict:
    return {
        "query_strategy": result.get("query_strategy"),
        "query_texts": result.get("query_texts"),
        "accepted_count": result.get("accepted_count"),
        "accepted": [
            {"slug": item.get("slug"), "score": item.get("score")}
            for item in result.get("accepted", [])
        ],
        "rejected_count": result.get("rejected_count"),
        "final_limit": result.get("final_limit"),
    }


def run_acp(
    prompt_path: Path,
    out_json: Path,
    response_path: Path,
    *,
    model: str,
    label: str,
    effort: str = "high",
) -> dict[str, object]:
    cp = subprocess.run(
        ["node", str(RUNNER), str(prompt_path), str(out_json), model, effort, label],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if cp.returncode:
        raise RuntimeError(f"{label}: {cp.stderr[-2500:]}")
    data = json.loads(out_json.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"{label}: {data.get('error')}")
    text = clean(str(data.get("text", "")))
    response_path.write_text(text + "\n", encoding="utf-8")
    print(
        "DONE",
        {"label": label, "model": model, "wall_seconds": data.get("wall_seconds"), "chars": len(text)},
        flush=True,
    )
    return {"text": text, "wall_seconds": data.get("wall_seconds"), "chars": len(text)}


def numbered_blocks(text: str, marker: str, count: int) -> list[str]:
    starts = [m.start() for m in re.finditer(rf"(?m)^# {re.escape(marker)} \d+", text)]
    if len(starts) != count:
        raise RuntimeError(f"Expected {count} {marker} blocks, got {len(starts)}")
    starts.append(len(text))
    return [text[starts[i] : starts[i + 1]].strip() for i in range(count)]


def assert_prompt_isolation(
    *, world_prompt: str, power_prompt: str, human_prompt: str, story_direction: str
) -> dict[str, object]:
    checks = {
        "world_has_selected_world": "每天正午" in world_prompt and "上涨一丈" in world_prompt,
        "world_hides_ontology": "空心铜像" not in world_prompt,
        "world_hides_privilege": "血契借壳" not in world_prompt,
        "world_hides_interface": "未来证词" not in world_prompt,
        "power_has_ontology": "空心铜像" in power_prompt,
        "power_has_privilege": "血契借壳" in power_prompt,
        "power_hides_interface": "未来证词" not in power_prompt,
        "human_has_ontology": "空心铜像" in human_prompt,
        "human_hides_privilege": "血契借壳" not in human_prompt,
        "human_hides_interface": "未来证词" not in human_prompt,
        "story_has_full_collision": all(
            token in story_direction
            for token in ("每天正午", "空心铜像", "血契借壳", "未来证词")
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(f"lane prompt isolation failed: {failed}")
    return {"passed": True, "checks": checks}


def main() -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    author = read(BASE / "AUTHOR_DIRECTION.md")
    lane = BASE / "orthogonal" / "selected_C2_lane_projection"
    world_direction = read(lane / "WORLD_DIRECTION.md")
    power_direction = read(lane / "POWER_DIRECTION.md")
    human_direction = read(lane / "HUMAN_DIRECTION.md")
    story_direction = read(lane / "STORY_DIRECTION.md")
    selected_collision = read(lane / "SELECTED_COLLISION.md")

    protocol = """# C2 Downstream Preservation Protocol

- Treatment was pre-registered before any downstream output: `fast_multiworld / C2`.
- No post-hoc premise selection.
- World receives only W2.
- Power receives only O3 + P1; Power Novelty and Lexique are disabled for causal isolation.
- Human receives only O3 and remains Power/Story blind.
- Power candidate 2 and Human candidate 2 are selected before generation; no selector call and no cherry-pick.
- Story Program first receives the full C2 collision plus newly approved World and Character.
- Current production models are retained: Luna-high for World/Power/Human/Outline, Sol-high for Story Program.
- Production default workflow is not modified.
"""
    (EXP / "PROTOCOL.md").write_text(protocol, encoding="utf-8")
    (EXP / "AUTHOR_DIRECTION.md").write_text(author + "\n", encoding="utf-8")
    (EXP / "SELECTED_COLLISION.md").write_text(selected_collision + "\n", encoding="utf-8")

    # 1. World-only Authority.
    world_author = "\n\n".join((author, world_direction))
    wr = retrieve_gbrain(mode="world_vision", creative_direction=world_author)
    (EXP / "WORLD_GBRAIN.md").write_text(wr["result"], encoding="utf-8")
    dump(EXP / "WORLD_RETRIEVAL.json", retrieval_meta(wr))
    world_prompt = generate_split_prompt(
        mode="world_vision",
        creative_direction=world_author,
        gbrain_inspiration=wr["result"],
    )
    (EXP / "WORLD_PROMPT.md").write_text(world_prompt, encoding="utf-8")
    world_result = run_acp(
        EXP / "WORLD_PROMPT.md",
        EXP / "WORLD_ACP.json",
        EXP / "WORLD_VISION.md",
        model="gpt-5.6-luna",
        label="premise-downstream-C2-world",
    )
    world = str(world_result["text"])

    # 2. Power/Human remain isolated from each other and Story.
    state = {"world_vision": {"status": "author_approved"}}
    pr = retrieve_gbrain(
        mode="power_seed", creative_direction=power_direction, world_vision=world
    )
    hr = retrieve_gbrain(
        mode="human_seed", creative_direction=human_direction, world_vision=world
    )
    (EXP / "POWER_GBRAIN.md").write_text(pr["result"], encoding="utf-8")
    (EXP / "HUMAN_GBRAIN.md").write_text(hr["result"], encoding="utf-8")
    dump(EXP / "POWER_RETRIEVAL.json", retrieval_meta(pr))
    dump(EXP / "HUMAN_RETRIEVAL.json", retrieval_meta(hr))

    power_contract = """# EXPERIMENTAL AUTHOR DIRECTION CONTRACT
The selected Ontology and Privilege are mandatory search constraints, not optional inspiration. All three Power Candidates must preserve both Core statements and the single root boundary. They may vary only implementation grammar, early applications, compound growth and high-tier expression. Do not invent personality, biography, World truth or Story events.
"""
    human_contract = """# EXPERIMENTAL AUTHOR DIRECTION CONTRACT
The selected Ontology is the protagonist's literal T0 body, not symbolism and not an optional costume. All four Human Candidates must inhabit it while remaining completely blind to special Power, future Story, rewards and interface. Generate different concrete people, desires, motives and relationships without changing the body back into a standard human.
"""
    power_prompt = "\n\n".join(
        (
            generate_split_prompt(
                mode="power_seed",
                world_vision=world,
                creative_state=state,
                gbrain_inspiration=pr["result"],
                power_novelty="",
                power_lexique="",
            ).strip(),
            power_contract.strip(),
            power_direction,
        )
    ) + "\n"
    human_prompt = "\n\n".join(
        (
            generate_split_prompt(
                mode="human_seed",
                world_vision=world,
                creative_state=state,
                gbrain_inspiration=hr["result"],
            ).strip(),
            human_contract.strip(),
            human_direction,
        )
    ) + "\n"
    isolation = assert_prompt_isolation(
        world_prompt=world_prompt,
        power_prompt=power_prompt,
        human_prompt=human_prompt,
        story_direction=story_direction,
    )
    dump(EXP / "PROMPT_ISOLATION.json", isolation)
    (EXP / "POWER_PROMPT.md").write_text(power_prompt, encoding="utf-8")
    (EXP / "HUMAN_PROMPT.md").write_text(human_prompt, encoding="utf-8")

    with ThreadPoolExecutor(max_workers=2) as pool:
        power_future = pool.submit(
            run_acp,
            EXP / "POWER_PROMPT.md",
            EXP / "POWER_ACP.json",
            EXP / "POWER_CANDIDATES.md",
            model="gpt-5.6-luna",
            label="premise-downstream-C2-power",
        )
        human_future = pool.submit(
            run_acp,
            EXP / "HUMAN_PROMPT.md",
            EXP / "HUMAN_ACP.json",
            EXP / "HUMAN_CANDIDATES.md",
            model="gpt-5.6-luna",
            label="premise-downstream-C2-human",
        )
        power_candidates = str(power_future.result()["text"])
        human_candidates = str(human_future.result()["text"])

    power_blocks = numbered_blocks(power_candidates, "POWER CANDIDATE", 3)
    human_blocks = numbered_blocks(human_candidates, "HUMAN CANDIDATE", 4)
    power = re.sub(
        r"(?m)^# POWER CANDIDATE \d+｜",
        "# POWER SEED｜",
        power_blocks[1],
        count=1,
    )
    human = re.sub(
        r"(?m)^# HUMAN CANDIDATE \d+｜",
        "# HUMAN SEED｜",
        human_blocks[1],
        count=1,
    )
    (EXP / "POWER_SEED.md").write_text(power + "\n", encoding="utf-8")
    (EXP / "HUMAN_SEED.md").write_text(human + "\n", encoding="utf-8")
    dump(EXP / "PRE_REGISTERED_SELECTION.json", {"power_candidate": 2, "human_candidate": 2})

    character = compose_character_card(power_seed=power, human_seed=human)
    human_authority = split_human_seed_authorities(human)
    (EXP / "CHARACTER.md").write_text(character, encoding="utf-8")
    (EXP / "CHARACTER_INITIAL_STATE.md").write_text(
        human_authority["initial_state"], encoding="utf-8"
    )
    (EXP / "CHARACTER_AUDITION.md").write_text(
        human_authority["audition_metadata"], encoding="utf-8"
    )

    # 3. First full collision occurs only after World and Character are approved.
    story_author = "\n\n".join((author, story_direction))
    story_state = {
        "world_vision": {"status": "author_approved"},
        "character_card": {"status": "author_approved"},
    }
    sr = retrieve_gbrain(
        mode="idea",
        creative_direction=story_author,
        world_vision=world,
        character_card=character,
    )
    (EXP / "STORY_GBRAIN.md").write_text(sr["result"], encoding="utf-8")
    dump(EXP / "STORY_RETRIEVAL.json", retrieval_meta(sr))
    story_prompt = generate_split_prompt(
        mode="idea",
        creative_direction=story_author,
        world_vision=world,
        character_card=character,
        character_initial_state=human_authority["initial_state"],
        creative_state=story_state,
        gbrain_inspiration=sr["result"],
    )
    (EXP / "STORY_PROGRAM_PROMPT.md").write_text(story_prompt, encoding="utf-8")
    story_result = run_acp(
        EXP / "STORY_PROGRAM_PROMPT.md",
        EXP / "STORY_PROGRAM_ACP.json",
        EXP / "STORY_PROGRAM.md",
        model="gpt-5.6-sol",
        label="premise-downstream-C2-story",
    )
    story = str(story_result["text"])
    try:
        handoff = extract_world_horizon_handoff(story)
    except ValueError as error:
        handoff = f"Extraction failed: {error}"
    (EXP / "WORLD_HORIZON_HANDOFF.md").write_text(handoff + "\n", encoding="utf-8")

    # 4. Outline tests whether planning immediately smooths the premise back to normal.
    outline_state = {
        **story_state,
        "proposal": {"status": "author_approved"},
    }
    orr = retrieve_gbrain(
        mode="outline",
        creative_direction=author,
        world_vision=world,
        character_card=character,
        proposal_context=story,
    )
    (EXP / "OUTLINE_GBRAIN.md").write_text(orr["result"], encoding="utf-8")
    dump(EXP / "OUTLINE_RETRIEVAL.json", retrieval_meta(orr))
    outline_prompt = generate_split_prompt(
        mode="outline",
        creative_direction=author,
        world_vision=world,
        character_card=character,
        character_initial_state=human_authority["initial_state"],
        creative_state=outline_state,
        proposal_context=story,
        gbrain_inspiration=orr["result"],
    )
    (EXP / "OUTLINE_PROMPT.md").write_text(outline_prompt, encoding="utf-8")
    outline_result = run_acp(
        EXP / "OUTLINE_PROMPT.md",
        EXP / "OUTLINE_ACP.json",
        EXP / "OUTLINE_RAW.md",
        model="gpt-5.6-luna",
        label="premise-downstream-C2-outline",
    )
    outline = str(outline_result["text"])
    marker = outline.find("# 小说总体设计画像")
    if marker >= 0:
        outline = outline[marker:]
    try:
        validate_book_content_for_save(outline)
        outline_valid = True
    except ValueError as error:
        outline_valid = False
        (EXP / "OUTLINE_VALIDATION_ERROR.txt").write_text(str(error), encoding="utf-8")
    (EXP / "OUTLINE.md").write_text(outline + "\n", encoding="utf-8")

    audit_prompt = f"""你是 TGN Premise Preservation 审计员。比较预注册的非 Canon C2 碰撞与它真实经过当前 production Authority 链后形成的 World / Character / Story / Outline。

只审计，不改稿。逐项引用实际证据，不因怪异就加分。

必须判断：
1. 四条 Locked Core 在最终 Authority 中分别是 PRESERVED / TRANSFORMED-BUT-PRESERVED / LOST / CONTRADICTED。
2. World 是否保持 protagonist-blind，是否偷偷为铜像/借壳定制锁孔。
3. Power/Human 是否保持隔离：Human 有没有偷看借壳，Power 有没有发明 Biography。
4. 主角是否仍是活铜像，还是被写回普通少年/可随时恢复人形。
5. 血契借壳是否仍是直接身体动作，还是被降格成侦察/分析/召唤。
6. 未来证词是否真实改变关系与行动，还是只做装饰悬念。
7. 第一章/前五章是否有清楚主轴，还是四套 gimmick 同时争抢注意力。
8. 与当前 fast-multiworld baseline 相比，Click / Bold / Clarity / Changed Verbs / Immediate Payoff / Long-form Runway 各自提升或下降在哪里。
9. 给出下游保持结论：PASS / CONDITIONAL PASS / FAIL；列出会改变冻结判断的唯一最小修正，不要建议再加一个代理。

严格格式：
# DOWNSTREAM PRESERVATION AUDIT
## Locked Core Table
## Lane Isolation
## Opening and Five-Chapter Readability
## Baseline Delta
## Verdict

# PRE-REGISTERED COLLISION
{selected_collision}

# CURRENT BASELINE
{read(BASE / 'CURRENT_BASELINE_PACKAGE.md')}

# GENERATED WORLD
{world}

# GENERATED CHARACTER
{character}

# GENERATED STORY PROGRAM
{story}

# GENERATED OUTLINE
{outline}
"""
    (EXP / "AUDIT_PROMPT.md").write_text(audit_prompt, encoding="utf-8")
    audit_result = run_acp(
        EXP / "AUDIT_PROMPT.md",
        EXP / "AUDIT_ACP.json",
        EXP / "AUDIT.md",
        model="gpt-5.6-terra",
        label="premise-downstream-C2-audit",
    )

    dump(
        EXP / "RUN_SUMMARY.json",
        {
            "case": "fast_multiworld/C2",
            "prompt_isolation_passed": True,
            "pre_registered_power_candidate": 2,
            "pre_registered_human_candidate": 2,
            "outline_valid": outline_valid,
            "world_chars": len(world),
            "power_chars": len(power),
            "human_chars": len(human),
            "story_chars": len(story),
            "outline_chars": len(outline),
            "audit_chars": audit_result["chars"],
        },
    )


if __name__ == "__main__":
    main()
