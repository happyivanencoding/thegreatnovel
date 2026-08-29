from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
import json
import re
import sys


ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-premise-aperture-20260829-v1" / "fast_multiworld"
V1 = BASE / "downstream_S2"
EXP = BASE / "downstream_S2_frozen_v2"
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
    has_explicit_premise_conflict,
    render_lane_direction,
)
from story_mvp.storage import validate_book_content_for_save  # noqa: E402


WORLD_INTERFACE_V2 = """### World Interface-only Direction

万言城的回音塔会放大所有重大命令。谁在公开场合下令，整座城都可能听见；任何人被命令改变行动时，回音塔都会把那一刻重映在城墙上。这个公开重映规则不依赖未来主角，适用于所有达到塔网公开阈值的命令事件。
"""

ORIGIN_V2 = """### Initial Origin-only Direction

主角在开篇公开处刑现场才第一次诞生。叛军首领被处决、尸体已经失去声音后，最后一句“不要跪”从死者喉咙里掉出来，成为会爬行的黑色字迹。第一场事件之前，它没有训练、关系、职业、旧胜负或另一段 Biography。
"""

LEGACY_COMPILE_TRACE = """### Authority-Compilation Trace

这是预注册旧候选的回放占位，不构成合法性证明。该候选生成时还没有 compile-trace 输出合同；本实验故意不修它的开篇、尺或终局，只要求 frozen contract 保留 lane facts，并由 Story Program 对剩余冲突 fail loud。
"""


def normalize_selected_s2(selected_v1: str) -> str:
    """Split already-selected S2 facts into lane-specific frozen fields without inventing a new premise."""

    ontology_heading = "### Protagonist Ontology-only Direction"
    power_heading = "### Power-only Direction"
    if ontology_heading not in selected_v1 or power_heading not in selected_v1:
        raise ValueError("selected S2 lacks expected lane headings")
    selected_v2 = selected_v1
    if "### World Interface-only Direction" not in selected_v2:
        selected_v2 = selected_v2.replace(
            ontology_heading,
            f"{WORLD_INTERFACE_V2.strip()}\n\n{ontology_heading}",
            1,
        )
    if "### Initial Origin-only Direction" not in selected_v2:
        selected_v2 = selected_v2.replace(
            power_heading,
            f"{ORIGIN_V2.strip()}\n\n{power_heading}",
            1,
        )
    if "### Authority-Compilation Trace" not in selected_v2:
        opening_heading = "### 第一章标志性画面"
        if opening_heading not in selected_v2:
            raise ValueError("selected S2 lacks first-chapter heading")
        selected_v2 = selected_v2.replace(
            opening_heading,
            f"{LEGACY_COMPILE_TRACE.strip()}\n\n{opening_heading}",
            1,
        )
    return selected_v2.strip()


def assert_prompt_isolation(
    *, world_prompt: str, power_prompt: str, human_prompt: str, story_direction: str
) -> dict[str, object]:
    checks = {
        "world_has_world": "万言城" in world_prompt and "语言不是比喻" in world_prompt,
        "world_has_public_interface": "任何人被命令改变行动" in world_prompt
        and "重映在城墙" in world_prompt,
        "world_hides_ontology": "会爬行的黑色字迹" not in world_prompt,
        "world_hides_origin": "死者喉咙里掉出来" not in world_prompt,
        "world_hides_power": "黑色字钉" not in world_prompt,
        "power_has_ontology": "会爬行的黑色字迹" in power_prompt,
        "power_has_all_carrier_scope": "门、兵器、野兽或人的身体" in power_prompt,
        "power_hides_origin": "死者喉咙里掉出来" not in power_prompt,
        "power_hides_world_interface": "任何人被命令改变行动" not in power_prompt,
        "human_has_ontology": "会爬行的黑色字迹" in human_prompt,
        "human_has_exact_origin": "死者喉咙里掉出来" in human_prompt,
        "human_hides_power": "黑色字钉" not in human_prompt,
        "human_hides_world_interface": "任何人被命令改变行动" not in human_prompt,
        "story_has_full_contract": all(
            token in story_direction
            for token in (
                "万言城",
                "任何人被命令改变行动",
                "会爬行的黑色字迹",
                "死者喉咙里掉出来",
                "门、兵器、野兽或人的身体",
                "重映在城墙",
            )
        ),
        "story_requires_explicit_conflict": "PREMISE-AUTHORITY CONFLICT" in story_direction,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(f"frozen premise lane isolation failed: {failed}")
    return {"passed": True, "checks": checks}


def main() -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    author = read(BASE / "AUTHOR_DIRECTION.md")
    selected_v1 = read(V1 / "SELECTED_PREMISE.md")
    selected = normalize_selected_s2(selected_v1)
    bundle = build_single_pass_lane_bundle(selected)
    world_direction = render_lane_direction(bundle, lane="world")
    power_direction = render_lane_direction(bundle, lane="power")
    human_direction = render_lane_direction(bundle, lane="human")
    story_direction = render_lane_direction(bundle, lane="story")

    protocol = """# S2 Frozen Lane Contract V2 Protocol

- Near-single-variable repair of the pre-registered `fast_multiworld / S2` downstream failure.
- The premise itself is unchanged; existing S2 facts are split into two missing lane fields:
  - protagonist-blind World Interface: every qualifying changed action is publicly remapped;
  - exact T0 Origin: the living command is born from the dead rebel's throat at the opening execution, with no prior Biography.
- Author selection remains non-Canon until each existing Authority is generated and approved.
- After selection, each lane receives only its own frozen author constraints, not the full Premise Card.
- World receives World + protagonist-blind World Interface.
- Power receives Ontology + exact Power trigger/coverage/boundary; no Origin, Biography, World Interface or Story.
- Human receives Ontology + exact T0 Origin; no special Power, World Interface or future Story.
- Story first receives the full selected contract after World/Power/Human approval; conflict must be surfaced explicitly instead of silently rewritten.
- Power candidate 2 and Human candidate 2 remain pre-registered. No model selector or post-hoc cherry-pick.
- Outline receives approved World/Character/Story, not the raw Premise Card.
- Production default is not modified.
"""
    (EXP / "PROTOCOL.md").write_text(protocol, encoding="utf-8")
    (EXP / "AUTHOR_DIRECTION.md").write_text(author + "\n", encoding="utf-8")
    (EXP / "SELECTED_PREMISE_CONTRACT_V2.md").write_text(selected + "\n", encoding="utf-8")
    receipt = {
        "selected_candidate": "S2",
        "source": str(V1 / "SELECTED_PREMISE.md"),
        "contract_version": 2,
        "selected_sha256": sha256(selected.encode("utf-8")).hexdigest(),
        "world_sha256": sha256(world_direction.encode("utf-8")).hexdigest(),
        "power_sha256": sha256(power_direction.encode("utf-8")).hexdigest(),
        "human_sha256": sha256(human_direction.encode("utf-8")).hexdigest(),
        "story_sha256": sha256(story_direction.encode("utf-8")).hexdigest(),
        "power_candidate": 2,
        "human_candidate": 2,
    }
    dump(EXP / "PRE_REGISTERED_SELECTION.json", receipt)

    lane_dir = EXP / "COMPILED_LANES"
    lane_dir.mkdir(exist_ok=True)
    for name, content in {
        "WORLD_DIRECTION.md": world_direction,
        "POWER_DIRECTION.md": power_direction,
        "HUMAN_DIRECTION.md": human_direction,
        "STORY_DIRECTION.md": story_direction,
    }.items():
        (lane_dir / name).write_text(content + "\n", encoding="utf-8")

    # World Authority: protagonist-blind, but the selected public interface is a world rule.
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
    world_path = EXP / "WORLD_VISION.md"
    if world_path.exists():
        world = read(world_path)
        print("REUSE premise-frozen-v2-S2-world", flush=True)
    else:
        world = str(
            run_acp(
                EXP / "WORLD_PROMPT.md",
                EXP / "WORLD_ACP.json",
                world_path,
                model="gpt-5.6-luna",
                label="premise-frozen-v2-S2-world",
            )["text"]
        )

    # Power and Human stay mutually blind.
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
            power_direction.strip(),
            "# OUTPUT CONFLICT RULE\n"
            "若任一已批准 World 正常值真的使上述触发、目标类别或永久边界无法同时成立，不要自行缩窄或增强；输出 `PREMISE-AUTHORITY CONFLICT` 并指出精确冲突。否则三个候选都必须完整实现。",
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
            human_direction.strip(),
            "# OUTPUT CONFLICT RULE\n"
            "若已批准 World 真的无法容纳上述 literal Ontology 或 T0 Origin，不要搬移出生、补前传或恢复人形；输出 `PREMISE-AUTHORITY CONFLICT`。否则四个候选都必须从同一 T0 开始。",
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

    power_candidates_path = EXP / "POWER_CANDIDATES.md"
    human_candidates_path = EXP / "HUMAN_CANDIDATES.md"
    if power_candidates_path.exists() and human_candidates_path.exists():
        power_candidates = read(power_candidates_path)
        human_candidates = read(human_candidates_path)
        print("REUSE premise-frozen-v2-S2-power/human", flush=True)
    else:
        with ThreadPoolExecutor(max_workers=2) as pool:
            power_future = pool.submit(
                run_acp,
                EXP / "POWER_PROMPT.md",
                EXP / "POWER_ACP.json",
                power_candidates_path,
                model="gpt-5.6-luna",
                label="premise-frozen-v2-S2-power",
            )
            human_future = pool.submit(
                run_acp,
                EXP / "HUMAN_PROMPT.md",
                EXP / "HUMAN_ACP.json",
                human_candidates_path,
                model="gpt-5.6-luna",
                label="premise-frozen-v2-S2-human",
            )
            power_candidates = str(power_future.result()["text"])
            human_candidates = str(human_future.result()["text"])

    if has_explicit_premise_conflict(power_candidates) or has_explicit_premise_conflict(
        human_candidates
    ):
        raise RuntimeError("Power/Human surfaced a premise-authority conflict; inspect artifacts")

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

    character = compose_character_card(power_seed=power, human_seed=human)
    human_authority = split_human_seed_authorities(human)
    (EXP / "CHARACTER.md").write_text(character, encoding="utf-8")
    (EXP / "CHARACTER_INITIAL_STATE.md").write_text(
        human_authority["initial_state"], encoding="utf-8"
    )
    (EXP / "CHARACTER_AUDITION.md").write_text(
        human_authority["audition_metadata"], encoding="utf-8"
    )

    # Story sees the complete selected promise only after approved lane Authorities.
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
    story_path = EXP / "STORY_PROGRAM.md"
    if story_path.exists():
        story = read(story_path)
        print("REUSE premise-frozen-v2-S2-story", flush=True)
    else:
        story = str(
            run_acp(
                EXP / "STORY_PROGRAM_PROMPT.md",
                EXP / "STORY_PROGRAM_ACP.json",
                story_path,
                model="gpt-5.6-sol",
                label="premise-frozen-v2-S2-story",
            )["text"]
        )
    if has_explicit_premise_conflict(story):
        raise RuntimeError("Story surfaced a premise-authority conflict; inspect artifacts")
    try:
        handoff = extract_world_horizon_handoff(story)
    except ValueError as error:
        handoff = f"Extraction failed: {error}"
    (EXP / "WORLD_HORIZON_HANDOFF.md").write_text(handoff + "\n", encoding="utf-8")

    # Outline consumes only approved Authorities and Story Program, not the raw Premise Card.
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
    outline_path = EXP / "OUTLINE.md"
    if outline_path.exists():
        outline = read(outline_path)
        print("REUSE premise-frozen-v2-S2-outline", flush=True)
    else:
        outline = str(
            run_acp(
                EXP / "OUTLINE_PROMPT.md",
                EXP / "OUTLINE_ACP.json",
                EXP / "OUTLINE_RAW.md",
                model="gpt-5.6-luna",
                label="premise-frozen-v2-S2-outline",
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
    outline_path.write_text(outline + "\n", encoding="utf-8")

    audit_prompt = f"""你是 TGN Frozen Premise Contract V2 审计员。比较同一张预注册 S2 Premise 在 V1 direction-only 编译与 V2 lane-specific frozen contract 编译后的真实 World / Power / Human / Story / Outline。只审计，不改稿。

V1 已知失败：出生被移到旧训练场破旗；字钉从门/兵器/野兽/人缩窄成只能活人；公开重映从稳定 World Interface 降成偶发演出。

必须判断：
1. V2 World-only、World Interface、Ontology、T0 Origin、Power trigger/coverage/boundary、Story Promise 分别 PRESERVED / TRANSFORMED-BUT-PRESERVED / LOST / CONTRADICTED。
2. World 是否仍 protagonist-blind；Human 是否仍 Power/Story blind；Power 是否仍 Biography blind。
3. Human 是否严格从公开处刑、死者喉中诞生开始，没有之前的训练、关系、职业或旧胜负。
4. Power 是否保留“真正击败 + 刚刚说过 + 字面含义 + 可钉进门、兵器、野兽或人的任何真实载体 + 载体毁则消失”，不得只保留活人。
5. World 是否把任何符合阈值的行动改变公开重映为稳定公共规则；Story 是否让它持续改变追捕、价格、关系、战术和社会位置。
6. V2 是否仍避免旧 Fantasy Seed：World 有无主角也在推进；Human 是否有不服务语言主题的欲望/偏心/关系；Power 是否没有发明人生意义。
7. Outline 未读取 raw Premise Card，是否仍通过 approved Authorities / Story 保留第一章标志画面、Changed Verbs、第一次兑现和前五章换挡。
8. 对比 V1，Frozen lane contract 是否修复精确失败；是否引入新的语义同构、Prompt 负担或角色人格被概念吞噬。
9. 结论 PASS / CONDITIONAL PASS / FAIL。只给会改变冻结判断的最小后续动作；不建议新增 Agent、Judge、Reviewer、Scorer 或 Hard Gate。

严格格式：
# FROZEN PREMISE CONTRACT V2 AUDIT
## Preservation Table
## Lane Isolation
## V1 → V2 Delta
## Commercial Coherence vs Semantic Collapse
## Opening / Outline Preservation
## Verdict

# SELECTED S2 CONTRACT V2
{selected}

# V1 FAILURE AUDIT
{read(V1 / 'AUDIT.md')}

# V2 WORLD
{world}

# V2 POWER
{power}

# V2 HUMAN
{human}

# V2 STORY PROGRAM
{story}

# V2 OUTLINE
{outline}
"""
    (EXP / "AUDIT_PROMPT.md").write_text(audit_prompt, encoding="utf-8")
    audit_path = EXP / "AUDIT.md"
    if audit_path.exists():
        audit_text = read(audit_path)
        audit_result: dict[str, object] = {"chars": len(audit_text)}
        print("REUSE premise-frozen-v2-S2-audit", flush=True)
    else:
        audit_result = run_acp(
            EXP / "AUDIT_PROMPT.md",
            EXP / "AUDIT_ACP.json",
            audit_path,
            model="gpt-5.6-terra",
            label="premise-frozen-v2-S2-audit",
        )
    dump(
        EXP / "RUN_SUMMARY.json",
        {
            "case": "fast_multiworld/S2_frozen_v2",
            "prompt_isolation_passed": True,
            "contract_version": 2,
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
    print(
        json.dumps(
            {
                "outline_valid": outline_valid,
                "world_chars": len(world),
                "power_chars": len(power),
                "human_chars": len(human),
                "story_chars": len(story),
                "outline_chars": len(outline),
                "audit_chars": audit_result["chars"],
            },
            ensure_ascii=False,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
