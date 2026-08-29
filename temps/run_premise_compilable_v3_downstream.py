from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import re
import sys
from typing import Any


ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-premise-aperture-20260829-v1" / "fast_multiworld"
FORGE = BASE / "compilable_single_v3"
EXP = BASE / "downstream_S2_compilable_v3"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "temps"))

from run_premise_aperture_downstream import (  # noqa: E402
    clean,
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
    extract_sections,
    has_explicit_premise_conflict,
    render_lane_direction,
)
from story_mvp.storage import validate_book_content_for_save  # noqa: E402


def materialize_acp(json_path: Path, response_path: Path) -> str:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"{json_path.name}: {data.get('error')}")
    text = clean(str(data.get("text", "")))
    if not text:
        raise RuntimeError(f"{json_path.name}: empty text")
    response_path.write_text(text + "\n", encoding="utf-8")
    return text


def load_or_run(
    *,
    prompt_path: Path,
    json_path: Path,
    response_path: Path,
    model: str,
    label: str,
) -> str:
    if response_path.exists():
        print(f"REUSE {label}", flush=True)
        return read(response_path)
    if json_path.exists():
        print(f"MATERIALIZE {label}", flush=True)
        return materialize_acp(json_path, response_path)
    return str(
        run_acp(
            prompt_path,
            json_path,
            response_path,
            model=model,
            label=label,
        )["text"]
    )


def full_section_present(container: str, section: str) -> bool:
    return section.strip() in container


def assert_prompt_isolation(
    *,
    world_prompt: str,
    power_prompt: str,
    human_prompt: str,
    story_direction: str,
    bundle: Any,
) -> dict[str, object]:
    checks = {
        "world_has_world": full_section_present(world_prompt, bundle.world),
        "world_has_world_interface": full_section_present(
            world_prompt, bundle.world_interface
        ),
        "world_hides_ontology": not full_section_present(world_prompt, bundle.ontology),
        "world_hides_origin": not full_section_present(world_prompt, bundle.origin),
        "world_hides_scale_position": not full_section_present(
            world_prompt, bundle.scale_position
        ),
        "world_hides_power": not full_section_present(world_prompt, bundle.privilege),
        "world_hides_story_interface": not full_section_present(
            world_prompt, bundle.interface
        ),
        "power_has_ontology": full_section_present(power_prompt, bundle.ontology),
        "power_has_scale_position": full_section_present(
            power_prompt, bundle.scale_position
        ),
        "power_has_power": full_section_present(power_prompt, bundle.privilege),
        "power_hides_origin": not full_section_present(power_prompt, bundle.origin),
        "power_hides_world_interface": not full_section_present(
            power_prompt, bundle.world_interface
        ),
        "power_hides_story_interface": not full_section_present(
            power_prompt, bundle.interface
        ),
        "human_has_ontology": full_section_present(human_prompt, bundle.ontology),
        "human_has_origin": full_section_present(human_prompt, bundle.origin),
        "human_has_scale_position": full_section_present(
            human_prompt, bundle.scale_position
        ),
        "human_hides_power": not full_section_present(human_prompt, bundle.privilege),
        "human_hides_world_interface": not full_section_present(
            human_prompt, bundle.world_interface
        ),
        "human_hides_story_interface": not full_section_present(
            human_prompt, bundle.interface
        ),
        "story_has_full_candidate": bundle.collision.strip() in story_direction,
        "story_requires_fail_loud": "PREMISE-AUTHORITY CONFLICT" in story_direction,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(f"compilable-v3 lane isolation failed: {failed}")
    return {"passed": True, "checks": checks}


def stop_on_conflict(stage: str, text: str) -> None:
    if not has_explicit_premise_conflict(text):
        return
    path = EXP / f"{stage.upper()}_PREMISE_AUTHORITY_CONFLICT.md"
    path.write_text(text.strip() + "\n", encoding="utf-8")
    dump(
        EXP / "RUN_SUMMARY.json",
        {
            "case": "fast_multiworld/S2_compilable_v3",
            "status": "premise_authority_conflict",
            "conflict_stage": stage,
            "production_default_changed": False,
        },
    )
    raise RuntimeError(f"{stage}: explicit PREMISE-AUTHORITY CONFLICT")


def forge_response() -> str:
    response_path = FORGE / "RESPONSE.md"
    if response_path.exists():
        return read(response_path)
    json_path = FORGE / "ACP.json"
    if not json_path.exists():
        raise FileNotFoundError("compilable Forge ACP output is not ready")
    return materialize_acp(json_path, response_path)


def main() -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    author = read(BASE / "AUTHOR_DIRECTION.md")
    response = forge_response()
    sections = extract_sections(response, prefix="S")
    if tuple(sections) != ("S1", "S2", "S3"):
        raise RuntimeError(f"expected S1/S2/S3, got {tuple(sections)}")
    # All three must be compilable; selected S2 was registered before generation.
    for candidate_id, section in sections.items():
        try:
            build_single_pass_lane_bundle(section)
        except ValueError as error:
            raise RuntimeError(f"{candidate_id} is not authority-compilable: {error}") from error

    selected = sections["S2"]
    bundle = build_single_pass_lane_bundle(selected)
    world_direction = render_lane_direction(bundle, lane="world")
    power_direction = render_lane_direction(bundle, lane="power")
    human_direction = render_lane_direction(bundle, lane="human")
    story_direction = render_lane_direction(bundle, lane="story")

    protocol = """# Compilable Single-Pass S2 V3 Downstream Protocol

- The Forge prompt now requires an `Authority-Compilation Trace` inside the same non-Canon generation call.
- `S2` was pre-registered before the Forge response existed; no best-looking candidate was selected post hoc.
- All S1/S2/S3 cards must parse with World Interface, exact T0 Origin, Power trigger/coverage/boundary and Authority-Compilation Trace.
- The trace can expose causality but cannot authorize a missing rule.
- After author selection, code deterministically projects lane-specific frozen contracts.
- World sees World + protagonist-blind interface only.
- Power sees literal Ontology + exact Power only; no Origin/Biography/Story.
- Human sees literal Ontology + exact T0 Origin only; no special Power/Story.
- Story sees the complete selected card only after approved World/Power/Human.
- Every Authority stage must fail loudly with `PREMISE-AUTHORITY CONFLICT`; no later stage may start after a conflict.
- Power candidate 2 and Human candidate 2 are pre-registered.
- Outline consumes approved World/Character/Story and never receives the raw Premise Card.
- Production default is unchanged.
"""
    (EXP / "PROTOCOL.md").write_text(protocol, encoding="utf-8")
    (EXP / "AUTHOR_DIRECTION.md").write_text(author + "\n", encoding="utf-8")
    (EXP / "FORGE_RESPONSE.md").write_text(response + "\n", encoding="utf-8")
    (EXP / "SELECTED_PREMISE.md").write_text(selected + "\n", encoding="utf-8")
    dump(
        EXP / "PRE_REGISTERED_SELECTION.json",
        {
            "selected_candidate": "S2",
            "registered_before_generation": True,
            "power_candidate": 2,
            "human_candidate": 2,
        },
    )
    lane_dir = EXP / "COMPILED_LANES"
    lane_dir.mkdir(exist_ok=True)
    for name, content in {
        "WORLD_DIRECTION.md": world_direction,
        "POWER_DIRECTION.md": power_direction,
        "HUMAN_DIRECTION.md": human_direction,
        "STORY_DIRECTION.md": story_direction,
    }.items():
        (lane_dir / name).write_text(content + "\n", encoding="utf-8")

    # World Authority.
    world_author = "\n\n".join((author, world_direction))
    wr = retrieve_gbrain(mode="world_vision", creative_direction=world_author)
    (EXP / "WORLD_GBRAIN.md").write_text(wr["result"], encoding="utf-8")
    dump(EXP / "WORLD_RETRIEVAL.json", retrieval_meta(wr))
    world_prompt = "\n\n".join(
        (
            generate_split_prompt(
                mode="world_vision",
                creative_direction=world_author,
                gbrain_inspiration=wr["result"],
            ).strip(),
            "# FAIL-LOUD RULE\n"
            "若作者已选 World / public-interface 硬约束与作者方向无法同时成立，输出独立行 `PREMISE-AUTHORITY CONFLICT` 并停止；不得删改硬约束。",
        )
    ) + "\n"
    (EXP / "WORLD_PROMPT.md").write_text(world_prompt, encoding="utf-8")
    world = load_or_run(
        prompt_path=EXP / "WORLD_PROMPT.md",
        json_path=EXP / "WORLD_ACP.json",
        response_path=EXP / "WORLD_VISION.md",
        model="gpt-5.6-luna",
        label="premise-compilable-v3-S2-world",
    )
    stop_on_conflict("world", world)

    # Isolated Power / Human Authorities.
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
            "# FAIL-LOUD RULE\n"
            "三个候选都必须完整实现上述 trigger / target coverage / action / carrier / root boundary。"
            "若与已批准 World 冲突，输出独立行 `PREMISE-AUTHORITY CONFLICT` 并停止；不得静默增强、缩窄或换义。",
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
            "# FAIL-LOUD RULE\n"
            "四个候选都必须从上述 literal Ontology + exact T0 Origin 开始。"
            "若与已批准 World 冲突，输出独立行 `PREMISE-AUTHORITY CONFLICT` 并停止；不得搬移出生、补前传或恢复标准人形。",
        )
    ) + "\n"
    dump(
        EXP / "PROMPT_ISOLATION.json",
        assert_prompt_isolation(
            world_prompt=world_prompt,
            power_prompt=power_prompt,
            human_prompt=human_prompt,
            story_direction=story_direction,
            bundle=bundle,
        ),
    )
    (EXP / "POWER_PROMPT.md").write_text(power_prompt, encoding="utf-8")
    (EXP / "HUMAN_PROMPT.md").write_text(human_prompt, encoding="utf-8")

    power_path = EXP / "POWER_CANDIDATES.md"
    human_path = EXP / "HUMAN_CANDIDATES.md"
    if power_path.exists() and human_path.exists():
        power_candidates = read(power_path)
        human_candidates = read(human_path)
        print("REUSE premise-compilable-v3-S2-power/human", flush=True)
    else:
        with ThreadPoolExecutor(max_workers=2) as pool:
            power_future = pool.submit(
                load_or_run,
                prompt_path=EXP / "POWER_PROMPT.md",
                json_path=EXP / "POWER_ACP.json",
                response_path=power_path,
                model="gpt-5.6-luna",
                label="premise-compilable-v3-S2-power",
            )
            human_future = pool.submit(
                load_or_run,
                prompt_path=EXP / "HUMAN_PROMPT.md",
                json_path=EXP / "HUMAN_ACP.json",
                response_path=human_path,
                model="gpt-5.6-luna",
                label="premise-compilable-v3-S2-human",
            )
            power_candidates = power_future.result()
            human_candidates = human_future.result()
    stop_on_conflict("power", power_candidates)
    stop_on_conflict("human", human_candidates)

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

    # Complete Story collision after approval.
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
    story = load_or_run(
        prompt_path=EXP / "STORY_PROGRAM_PROMPT.md",
        json_path=EXP / "STORY_PROGRAM_ACP.json",
        response_path=EXP / "STORY_PROGRAM.md",
        model="gpt-5.6-sol",
        label="premise-compilable-v3-S2-story",
    )
    stop_on_conflict("story", story)
    try:
        handoff = extract_world_horizon_handoff(story)
    except ValueError as error:
        handoff = f"Extraction failed: {error}"
    (EXP / "WORLD_HORIZON_HANDOFF.md").write_text(handoff + "\n", encoding="utf-8")

    # Outline receives approved Authorities only.
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
    outline = load_or_run(
        prompt_path=EXP / "OUTLINE_PROMPT.md",
        json_path=EXP / "OUTLINE_ACP.json",
        response_path=EXP / "OUTLINE_RAW.md",
        model="gpt-5.6-luna",
        label="premise-compilable-v3-S2-outline",
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

    audit_prompt = f"""你是 TGN Authority-Compilable Premise 审计员。比较同一 fast-multiworld 作者方向下：原 S2 在 frozen V2 的真实 Story 层发生 Authority conflict；新 Forge 在同一次非 Canon 生成里加入 Authority-Compilation Trace，并预注册 S2 后走完整真实链。只审计，不改稿。

必须判断：
1. 新 S2 的 Authority-Compilation Trace 是否逐项真实，还是自称闭合但依赖未授权机制。
2. World-only / World Interface / Ontology / T0 Origin / Power trigger-coverage-boundary / Opening Promise 分别 PRESERVED / TRANSFORMED-BUT-PRESERVED / LOST / CONTRADICTED。
3. World 是否 protagonist-blind；Human 是否 Power/Story blind；Power 是否 Biography blind。
4. 第一章所有超常结果是否在发生时已经合法：不能提前使用未获得能力，不能让 Interface 偷偷复制 Power，不能让一个载体无 World 路由却产生全城效果。
5. 主角进入精确力量尺的位置是否已由 protagonist-blind World 预先定义。
6. 20章结算是否复合现有规则与真实载体，不依赖未写明中央控制、无限复制或改写命令字面。
7. 主角是否仍有大胆 Changed Verbs、清楚第一章图像、立即兑现与公共反应；可编译性修复有没有把 premise 修保守。
8. Human 是否拥有不服务核心概念的欲望、偏心、关系与具体快乐；World 是否无主角也继续推进，避免旧 Fantasy Seed 语义提纯。
9. Outline 没有读取 raw Premise Card，是否仍通过 approved Authorities / Story 保留前五章主轴和20章换挡。
10. 对比 current baseline、四轴 C2、旧 S2 V1/V2：结论 PASS / CONDITIONAL PASS / FAIL。只给一项会改变冻结判断的最小动作；不建议新增 Agent/Judge/Reviewer/Scorer/Hard Gate。

严格格式：
# AUTHORITY-COMPILABLE PREMISE V3 AUDIT
## Compilation Trace Truth Table
## Direction Preservation
## Lane Isolation
## Opening / Scale / Climax Legality
## Commercial Voltage vs Semantic Collapse
## Baseline / C2 / Old-S2 Delta
## Verdict

# NEW SELECTED S2
{selected}

# OLD S2 V2 STORY CONFLICT
{read(BASE / 'downstream_S2_frozen_v2' / 'STORY_PROGRAM.md')}

# CURRENT BASELINE
{read(BASE / 'CURRENT_BASELINE_PACKAGE.md')}

# ORTHOGONAL C2 AUDIT
{read(BASE / 'downstream_C2' / 'AUDIT.md')}

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
    audit = load_or_run(
        prompt_path=EXP / "AUDIT_PROMPT.md",
        json_path=EXP / "AUDIT_ACP.json",
        response_path=EXP / "AUDIT.md",
        model="gpt-5.6-terra",
        label="premise-compilable-v3-S2-audit",
    )
    dump(
        EXP / "RUN_SUMMARY.json",
        {
            "case": "fast_multiworld/S2_compilable_v3",
            "status": "complete",
            "selected_candidate": "S2",
            "registered_before_generation": True,
            "prompt_isolation_passed": True,
            "pre_registered_power_candidate": 2,
            "pre_registered_human_candidate": 2,
            "outline_valid": outline_valid,
            "world_chars": len(world),
            "power_chars": len(power),
            "human_chars": len(human),
            "story_chars": len(story),
            "outline_chars": len(outline),
            "audit_chars": len(audit),
            "production_default_changed": False,
        },
    )
    print(
        json.dumps(
            {
                "status": "complete",
                "outline_valid": outline_valid,
                "story_chars": len(story),
                "outline_chars": len(outline),
                "audit_chars": len(audit),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
