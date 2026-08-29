from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import re
import sys


ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-premise-aperture-20260829-v1" / "fast_multiworld"
EXP = BASE / "downstream_S2"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "temps"))

from run_premise_aperture_downstream import (  # noqa: E402
    dump,
    numbered_blocks,
    read,
    retrieval_meta,
    run_acp,
)
from story_mvp.character_prompts import generate_split_prompt  # noqa: E402
from story_mvp.character_seeds import compose_character_card, split_human_seed_authorities  # noqa: E402
from story_mvp.gbrain_retrieval import retrieve_gbrain  # noqa: E402
from story_mvp.long_form_evolution import extract_world_horizon_handoff  # noqa: E402
from story_mvp.premise_aperture import (  # noqa: E402
    build_single_pass_lane_bundle,
    render_lane_direction,
)
from story_mvp.storage import validate_book_content_for_save  # noqa: E402


def assert_prompt_isolation(
    *, world_prompt: str, power_prompt: str, human_prompt: str, story_direction: str
) -> dict[str, object]:
    checks = {
        "world_has_selected_world": "万言城" in world_prompt and "语言不是比喻" in world_prompt,
        "world_hides_ontology": "会爬行的黑色字迹" not in world_prompt,
        "world_hides_privilege": "黑色字钉" not in world_prompt,
        "world_hides_story_interface": "重映在城墙" not in world_prompt,
        "power_has_ontology": "会爬行的黑色字迹" in power_prompt,
        "power_has_privilege": "黑色字钉" in power_prompt,
        "power_hides_story_interface": "重映在城墙" not in power_prompt,
        "human_has_ontology": "会爬行的黑色字迹" in human_prompt,
        "human_hides_privilege": "黑色字钉" not in human_prompt,
        "human_hides_story_interface": "重映在城墙" not in human_prompt,
        "story_has_full_premise": all(
            token in story_direction
            for token in ("万言城", "会爬行的黑色字迹", "黑色字钉", "重映在城墙")
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(f"single-pass lane isolation failed: {failed}")
    return {"passed": True, "checks": checks}


def main() -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    author = read(BASE / "AUTHOR_DIRECTION.md")
    selected = read(BASE / "single_pass" / "SELECTED_S2.md")
    bundle = build_single_pass_lane_bundle(selected)
    world_direction = render_lane_direction(bundle, lane="world")
    power_direction = render_lane_direction(bundle, lane="power")
    human_direction = render_lane_direction(bundle, lane="human")
    story_direction = render_lane_direction(bundle, lane="story")

    protocol = """# S2 Downstream Preservation Protocol

- Treatment was pre-registered before blind-panel results: `fast_multiworld / S2`.
- The selected complete Premise Card is compiled by code back into isolated lane directions.
- World receives only `World-only Direction`.
- Power receives only Ontology + Power directions; random Power Novelty/Lexique are disabled.
- Human receives only Ontology and remains Power/Story blind.
- Power candidate 2 and Human candidate 2 are pre-registered; no selector and no cherry-pick.
- Story Program first receives the complete selected Premise Card plus approved World/Character.
- Current production models remain: Luna-high World/Power/Human/Outline, Sol-high Story, Terra-high audit.
- Production default workflow is not modified.
"""
    (EXP / "PROTOCOL.md").write_text(protocol, encoding="utf-8")
    (EXP / "AUTHOR_DIRECTION.md").write_text(author + "\n", encoding="utf-8")
    (EXP / "SELECTED_PREMISE.md").write_text(selected + "\n", encoding="utf-8")
    lane_dir = EXP / "COMPILED_LANES"
    lane_dir.mkdir(exist_ok=True)
    for name, content in {
        "WORLD_DIRECTION.md": world_direction,
        "POWER_DIRECTION.md": power_direction,
        "HUMAN_DIRECTION.md": human_direction,
        "STORY_DIRECTION.md": story_direction,
    }.items():
        (lane_dir / name).write_text(content + "\n", encoding="utf-8")

    # World-only Authority.
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
    world = str(
        run_acp(
            EXP / "WORLD_PROMPT.md",
            EXP / "WORLD_ACP.json",
            EXP / "WORLD_VISION.md",
            model="gpt-5.6-luna",
            label="premise-downstream-S2-world",
        )["text"]
    )

    # Power/Human isolated from each other and Story.
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
The selected Ontology and Power-only Direction are mandatory search constraints, not optional inspiration. All three Power Candidates must preserve the protagonist as a living command, the need to truly defeat a real speaker, the use of a just-spoken command, literal wording, a real carrier, and carrier destruction. Candidates may vary only early applications, compound growth and high-tier expression. Do not invent Biography or Story events.
"""
    human_contract = """# EXPERIMENTAL AUTHOR DIRECTION CONTRACT
The selected Ontology is the literal T0 body, not symbolism or a temporary costume. All Human Candidates must be the same kind of living command while remaining completely blind to special Power, future Story, rewards and interface. Generate concrete desires, appetites, rivalries and relationships without restoring a standard human body.
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
    dump(
        EXP / "PROMPT_ISOLATION.json",
        assert_prompt_isolation(
            world_prompt=world_prompt,
            power_prompt=power_prompt,
            human_prompt=human_prompt,
            story_direction=story_direction,
        ),
    )
    (EXP / "POWER_PROMPT.md").write_text(power_prompt, encoding="utf-8")
    (EXP / "HUMAN_PROMPT.md").write_text(human_prompt, encoding="utf-8")

    with ThreadPoolExecutor(max_workers=2) as pool:
        power_future = pool.submit(
            run_acp,
            EXP / "POWER_PROMPT.md",
            EXP / "POWER_ACP.json",
            EXP / "POWER_CANDIDATES.md",
            model="gpt-5.6-luna",
            label="premise-downstream-S2-power",
        )
        human_future = pool.submit(
            run_acp,
            EXP / "HUMAN_PROMPT.md",
            EXP / "HUMAN_ACP.json",
            EXP / "HUMAN_CANDIDATES.md",
            model="gpt-5.6-luna",
            label="premise-downstream-S2-human",
        )
        power_candidates = str(power_future.result()["text"])
        human_candidates = str(human_future.result()["text"])

    power_blocks = numbered_blocks(power_candidates, "POWER CANDIDATE", 3)
    human_blocks = numbered_blocks(human_candidates, "HUMAN CANDIDATE", 4)
    power = re.sub(
        r"(?m)^# POWER CANDIDATE \d+｜", "# POWER SEED｜", power_blocks[1], count=1
    )
    human = re.sub(
        r"(?m)^# HUMAN CANDIDATE \d+｜", "# HUMAN SEED｜", human_blocks[1], count=1
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

    # First complete collision after World/Character approval.
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
    story = str(
        run_acp(
            EXP / "STORY_PROGRAM_PROMPT.md",
            EXP / "STORY_PROGRAM_ACP.json",
            EXP / "STORY_PROGRAM.md",
            model="gpt-5.6-sol",
            label="premise-downstream-S2-story",
        )["text"]
    )
    try:
        handoff = extract_world_horizon_handoff(story)
    except ValueError as error:
        handoff = f"Extraction failed: {error}"
    (EXP / "WORLD_HORIZON_HANDOFF.md").write_text(handoff + "\n", encoding="utf-8")

    # Outline.
    outline_state = {**story_state, "proposal": {"status": "author_approved"}}
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
    outline = str(
        run_acp(
            EXP / "OUTLINE_PROMPT.md",
            EXP / "OUTLINE_ACP.json",
            EXP / "OUTLINE_RAW.md",
            model="gpt-5.6-luna",
            label="premise-downstream-S2-outline",
        )["text"]
    )
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

    audit_prompt = f"""你是 TGN Premise Preservation 审计员。比较预注册的 Single-Agent S2 Premise Card 与它经过真实 production Authority 链后的 World / Character / Story / Outline。只审计，不改稿。

必须判断：
1. World-only / Ontology-only / Power-only / Interface 四个方向分别 PRESERVED / TRANSFORMED-BUT-PRESERVED / LOST / CONTRADICTED。
2. World 是否仍 protagonist-blind；Human 是否偷看 Power/Story；Power 是否发明 Biography。
3. 主角是否始终是一句活命令，而非普通人类修士或可恢复人形。
4. Power 是否仍要求“真正击败 + 对方刚说过 + 字面含义 + 真实载体 + 载体毁则消失”。
5. 回音塔公开重映是否改变关系/社会位置，还是装饰。
6. World、Ontology、Power、Story 是否过度同构为语言同一隐喻；具体指出这种统一是商业聚焦还是会造成百章重复。
7. 第一章/前五章是否主轴清楚，是否比 current fast-multiworld baseline 更 Click/Bold/Clear/Changed-Verbs/Payoff。
8. 对比 Orthogonal C2 下游：哪种编译更能保留 premise，哪种更容易语义坍缩。
9. 结论 PASS / CONDITIONAL PASS / FAIL；只给会改变冻结判断的一项最小修正，不建议再加代理。

严格格式：
# SINGLE-PASS DOWNSTREAM AUDIT
## Direction Preservation Table
## Lane Isolation
## Coherence vs Semantic Collapse
## Opening and Five-Chapter Readability
## Baseline and Orthogonal Delta
## Verdict

# SELECTED S2 PREMISE
{selected}

# CURRENT BASELINE
{read(BASE / 'CURRENT_BASELINE_PACKAGE.md')}

# ORTHOGONAL C2 SELECTED COLLISION
{read(BASE / 'orthogonal' / 'selected_C2_lane_projection' / 'SELECTED_COLLISION.md')}

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
        label="premise-downstream-S2-audit",
    )
    dump(
        EXP / "RUN_SUMMARY.json",
        {
            "case": "fast_multiworld/S2",
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
