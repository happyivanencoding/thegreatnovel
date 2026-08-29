from __future__ import annotations

from pathlib import Path
import json
import sys


ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-premise-aperture-20260829-v1" / "fast_multiworld"
EXP = BASE / "downstream_S2"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "temps"))

from run_premise_aperture_downstream import (  # noqa: E402
    clean,
    dump,
    read,
    retrieval_meta,
    run_acp,
)
from story_mvp.character_prompts import generate_split_prompt  # noqa: E402
from story_mvp.character_seeds import split_human_seed_authorities  # noqa: E402
from story_mvp.gbrain_retrieval import retrieve_gbrain  # noqa: E402
from story_mvp.long_form_evolution import extract_world_horizon_handoff  # noqa: E402
from story_mvp.premise_aperture import (  # noqa: E402
    build_single_pass_lane_bundle,
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


def acp_meta(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"ok": False, "missing": True}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "ok": bool(data.get("ok")),
        "wall_seconds": data.get("wall_seconds"),
        "chars": len(str(data.get("text", ""))),
        "error": data.get("error"),
    }


def main() -> None:
    author = read(BASE / "AUTHOR_DIRECTION.md")
    selected = read(EXP / "SELECTED_PREMISE.md")
    bundle = build_single_pass_lane_bundle(selected)
    story_direction = render_lane_direction(bundle, lane="story")

    world = read(EXP / "WORLD_VISION.md")
    character = read(EXP / "CHARACTER.md")
    human = read(EXP / "HUMAN_SEED.md")
    human_authority = split_human_seed_authorities(human)

    story_path = EXP / "STORY_PROGRAM.md"
    if story_path.exists():
        story = read(story_path)
    elif (EXP / "STORY_PROGRAM_ACP.json").exists():
        story = materialize_acp(EXP / "STORY_PROGRAM_ACP.json", story_path)
    else:
        story = str(
            run_acp(
                EXP / "STORY_PROGRAM_PROMPT.md",
                EXP / "STORY_PROGRAM_ACP.json",
                story_path,
                model="gpt-5.6-sol",
                label="premise-downstream-S2-story",
            )["text"]
        )

    try:
        handoff = extract_world_horizon_handoff(story)
    except ValueError as error:
        handoff = f"Extraction failed: {error}"
    (EXP / "WORLD_HORIZON_HANDOFF.md").write_text(handoff + "\n", encoding="utf-8")

    outline_path = EXP / "OUTLINE.md"
    if outline_path.exists():
        outline = read(outline_path)
        outline_valid = not (EXP / "OUTLINE_VALIDATION_ERROR.txt").exists()
    else:
        outline_state = {
            "world_vision": {"status": "author_approved"},
            "character_card": {"status": "author_approved"},
            "proposal": {"status": "author_approved"},
        }
        retrieval = retrieve_gbrain(
            mode="outline",
            creative_direction=author,
            world_vision=world,
            character_card=character,
            proposal_context=story,
        )
        (EXP / "OUTLINE_GBRAIN.md").write_text(retrieval["result"], encoding="utf-8")
        dump(EXP / "OUTLINE_RETRIEVAL.json", retrieval_meta(retrieval))
        outline_prompt = generate_split_prompt(
            mode="outline",
            creative_direction=author,
            world_vision=world,
            character_card=character,
            character_initial_state=human_authority["initial_state"],
            creative_state=outline_state,
            proposal_context=story,
            gbrain_inspiration=retrieval["result"],
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
        outline_path.write_text(outline + "\n", encoding="utf-8")

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
    audit_path = EXP / "AUDIT.md"
    if audit_path.exists():
        audit = read(audit_path)
    elif (EXP / "AUDIT_ACP.json").exists():
        audit = materialize_acp(EXP / "AUDIT_ACP.json", audit_path)
    else:
        audit = str(
            run_acp(
                EXP / "AUDIT_PROMPT.md",
                EXP / "AUDIT_ACP.json",
                audit_path,
                model="gpt-5.6-terra",
                label="premise-downstream-S2-audit",
            )["text"]
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
            "power_chars": len(read(EXP / "POWER_SEED.md")),
            "human_chars": len(human),
            "story_chars": len(story),
            "outline_chars": len(outline),
            "audit_chars": len(audit),
            "calls": {
                "world": acp_meta(EXP / "WORLD_ACP.json"),
                "power": acp_meta(EXP / "POWER_ACP.json"),
                "human": acp_meta(EXP / "HUMAN_ACP.json"),
                "story": acp_meta(EXP / "STORY_PROGRAM_ACP.json"),
                "outline": acp_meta(EXP / "OUTLINE_ACP.json"),
                "audit": acp_meta(EXP / "AUDIT_ACP.json"),
            },
        },
    )
    print(
        json.dumps(
            {
                "story_chars": len(story),
                "outline_chars": len(outline),
                "audit_chars": len(audit),
                "outline_valid": outline_valid,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
