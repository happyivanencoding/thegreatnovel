from __future__ import annotations

import pytest
from pydantic import ValidationError

from novel_authoring.original.models import (
    CoreInnovationProposal,
    OriginalBookRequest,
    OriginalCreativeSemantics,
)


def semantics(
    *,
    existing_signature_mechanism: str,
    expected_scale: str,
) -> OriginalCreativeSemantics:
    return OriginalCreativeSemantics(
        signature_fantasy="主角把有限机会持续转化为更大的行动主动权",
        existing_signature_mechanism=existing_signature_mechanism,
        open_design_space=["如何保持选择新鲜", "已有成果如何组合回收"],
        payoff_texture=["具体选择带来的反差", "旧成果在新压力中的回收"],
        novelty_focus=["既有机制产生的新用途与组合"],
        realism_anchors=["人物判断、资源来源与行动后果保持可信"],
        complexity_boundaries=["不增加未经作者意图需要的竞争性第二核心"],
        repeatable_reader_loop=["压力出现", "作出有限选择", "兑现结果", "打开新局势"],
        anti_drift=[f"不把{expected_scale}作品改写成预制剧情模板"],
    )


def core_proposal(
    creative: OriginalCreativeSemantics,
    *,
    mechanisms: list[str],
) -> CoreInnovationProposal:
    candidates = []
    for index, mechanism in enumerate(mechanisms, start=1):
        candidates.append(
            {
                "innovation_id": f"core-{index}",
                "title": f"玩法 {index}",
                "plain_language_pitch": f"用方案 {index} 解决仍未决定的选择与组合问题。",
                "concrete_example": "一次具体压力下的选择示意，不是故事基础、Canon 或未来事件。",
                "reader_anticipation": f"期待下一次如何用已有成果完成变化 {index}。",
                "unresolved_design_choices": [
                    f"如何让第 {index} 种选择保持新鲜",
                    f"如何让第 {index} 种成果在后续回收",
                ],
                "core_mechanism": mechanism,
                "protagonist_special_rule": "主角只能按 Seed 已定义的规则行动。",
                "choice_generation": f"方案 {index} 让有限机会产生不同取舍。",
                "progression_generation": f"方案 {index} 让已获成果形成新组合。",
                "payoff_generation": f"方案 {index} 先兑现当前选择再打开下一局势。",
                "limitation": "有限机会不可撤销。",
                "expansion_grammar": "扩大问题尺度，不增加独立外挂。",
                "long_form_capacity": "容量由 expected_length 与语义需求决定。",
                "novelty_source": "来自既有机制的新用途和组合。",
                "repetition_risk": "只换物品名称会重复。",
                "fit_with_reader_promise": "增强已确认的可重复阅读循环。",
            }
        )
    return CoreInnovationProposal(
        innovation_candidates=candidates,
        kernel_contracts={"creative_semantics": creative.model_dump(mode="json")},
    )


def test_short_strong_mechanism_keeps_signature_and_only_varies_open_choices() -> None:
    signature = "每天只能升级一件自己的普通物品；每日一次、不可撤销"
    creative = semantics(
        existing_signature_mechanism=signature,
        expected_scale="较短闭环",
    )
    proposal = core_proposal(
        creative,
        mechanisms=[f"保留 {signature}；变化仅来自开放设计 {index}" for index in range(1, 4)],
    )

    assert all(signature in item.core_mechanism for item in proposal.innovation_candidates)
    assert len(
        {tuple(item.unresolved_design_choices) for item in proposal.innovation_candidates}
    ) == 3
    assert proposal.kernel_contracts["creative_semantics"] == creative.model_dump(mode="json")


def test_very_long_progression_keeps_open_grammar_without_fixed_outline() -> None:
    signature = "个人能力体系已有明确起点，并能通过选择持续成长"
    request = OriginalBookRequest(
        premise="年轻主角在大型幻想世界中长期成长，与伙伴和组织面对更高层次挑战。",
        expected_length="超长成长型连载",
    )
    creative = semantics(
        existing_signature_mechanism=signature,
        expected_scale=request.expected_length,
    ).model_copy(
        update={
            "realism_anchors": ["世界本身也是主要幻想来源"],
            "complexity_boundaries": ["只限制竞争性第二核心，不限制世界丰富度"],
        }
    )
    proposal = core_proposal(
        creative,
        mechanisms=[f"保留 {signature}；用开放语法扩展层次 {index}" for index in range(1, 4)],
    )
    serialized = proposal.model_dump_json()

    assert request.expected_length == "超长成长型连载"
    assert all(signature in item.core_mechanism for item in proposal.innovation_candidates)
    assert creative.realism_anchors == ["世界本身也是主要幻想来源"]
    assert creative.complexity_boundaries == ["只限制竞争性第二核心，不限制世界丰富度"]
    assert not any(token in serialized for token in ("第1000章", "20卷", "学院篇", "比赛篇"))
    assert proposal.kernel_contracts["creative_semantics"]["repeatable_reader_loop"] == (
        creative.repeatable_reader_loop
    )


def test_weak_seed_can_still_propose_three_distinct_generative_mechanisms() -> None:
    creative = semantics(existing_signature_mechanism="", expected_scale="开放篇幅")
    proposal = core_proposal(
        creative,
        mechanisms=["关系承诺制造选择", "线索交换改变局势", "资源建设扩大行动范围"],
    )

    assert creative.existing_signature_mechanism == ""
    assert len({item.core_mechanism for item in proposal.innovation_candidates}) == 3
    assert len(
        {tuple(item.unresolved_design_choices) for item in proposal.innovation_candidates}
    ) == 3


def test_creative_semantics_rejects_taxonomy_or_numeric_answers() -> None:
    payload = semantics(
        existing_signature_mechanism="",
        expected_scale="开放篇幅",
    ).model_dump(mode="json")
    payload["novelty_focus"] = 80

    with pytest.raises(ValidationError):
        OriginalCreativeSemantics.model_validate(payload)

    payload = semantics(
        existing_signature_mechanism="",
        expected_scale="开放篇幅",
    ).model_dump(mode="json")
    payload["creative_family"] = "PRESET"

    with pytest.raises(ValidationError):
        OriginalCreativeSemantics.model_validate(payload)


def test_creative_semantics_schema_contains_only_open_text_fields() -> None:
    schema = OriginalCreativeSemantics.model_json_schema()
    properties = schema["properties"]

    assert set(properties) == {
        "signature_fantasy",
        "existing_signature_mechanism",
        "open_design_space",
        "payoff_texture",
        "novelty_focus",
        "realism_anchors",
        "complexity_boundaries",
        "repeatable_reader_loop",
        "anti_drift",
    }
    assert properties["signature_fantasy"]["type"] == "string"
    assert properties["existing_signature_mechanism"]["type"] == "string"
    for field_name in set(properties) - {
        "signature_fantasy",
        "existing_signature_mechanism",
    }:
        assert properties[field_name]["type"] == "array"
        assert properties[field_name]["items"]["type"] == "string"
