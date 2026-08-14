from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from novel_authoring.config import load_settings
from novel_authoring.contracts.draft import DraftOutput
from novel_authoring.domain.models import ContinuationMode, NarrativeFunction
from novel_authoring.original.genesis import build_genesis_apply_plan
from novel_authoring.original.models import (
    AuthorInnovationIntent,
    BookProfileDimensionDraft,
    BookProfileDraft,
    FirstChapterCandidate,
    FirstPhaseProposal,
    FoundationDevelopmentProposal,
    FoundationSetting,
    GenesisApplyPlan,
    OriginalBookRequest,
    OriginalFoundationConfirmation,
    RollingPlanning,
    SettingStrength,
    StoryFoundationCandidate,
    StoryRoute,
)
from novel_authoring.planning.models import CandidateProposal, ChapterContract
from novel_authoring.validation.validators import ValidationContext, validate_contract


def _profile() -> BookProfileDraft:
    return BookProfileDraft(
        **{
            dimension: BookProfileDimensionDraft(summary=dimension)
            for dimension in (
                "worldbuilding",
                "characters",
                "plot",
                "style",
                "narrative",
                "dialogue",
                "pacing",
                "themes",
                "continuity",
            )
        }
    )


def _chapter_candidate(index: int) -> FirstChapterCandidate:
    return FirstChapterCandidate(
        candidate_id=f"chapter-{index}",
        title=f"首章 {index}",
        opening_situation="异常能力在普通对象上第一次显形",
        hook="普通人无法解释结果",
        chapter_goal="让主角验证新行动可能",
        central_choice="是否立即使用能力",
        conflict="外部压力要求主角放弃验证",
        protagonist_action="主角主动选择并完成验证",
        cost="",
        irreversible_change="主角获得此前不存在的行动空间",
        ending_turn="新的更高能力问题出现",
        distinctiveness=f"候选差异 {index}",
    )


def _development_proposal(
    *, protagonist_cost: str = "", first_resource_bottleneck: str = ""
) -> FoundationDevelopmentProposal:
    foundation = StoryFoundationCandidate(
        candidate_id="foundation-one",
        title="异常能力承载",
        core_reading_promise="每次能力兑现都扩大可行动空间",
        protagonist="主角",
        protagonist_competence="能识别并使用已确认的特殊规则",
        protagonist_weakness="仍不知道能力的更高边界",
        protagonist_goal="证明能力可以改变处境",
        main_conflict="外部压力阻止能力验证",
        world_carrier="普通世界承载异常结果",
        first_stage_objective="完成第一次能力验证",
        risk_structure="对能力尺度的误判",
        social_configuration="普通人无法复制主角的结果",
        resource_structure="资源只影响执行条件，不定义能力上限",
        premise_relationship="直接展开已确认的核心机制",
        author_facing_pitch="主角让普通对象产生不可能的结果。",
        opening_situation="压力迫使主角立即选择一个普通对象",
        typical_choice="选择能力如何改变行动条件",
        innovation_fit="持续放大已确认核心，不增加第二套能力来源",
    )
    first_phase = FirstPhaseProposal(
        selected_foundation_id=foundation.candidate_id,
        opening_pressure="能力验证窗口正在关闭",
        first_concrete_goal="完成第一次验证",
        first_resource_bottleneck=first_resource_bottleneck,
        first_progression_opportunity="打开此前不可能的行动",
        first_payoff="得到普通人无法复制的结果",
        first_meaningful_escalation="更高能力边界被迫显形",
        stage_climax="主角公开完成能力验证",
        after_climax_change="世界开始按新的能力事实回应",
    )
    proposal = FoundationDevelopmentProposal.model_construct(
        schema_version="foundation-development-v1",
        information_status="PROPOSAL",
        core_innovation_intent=AuthorInnovationIntent(
            selected_primary_innovation_id="innovation-one"
        ),
        selected_foundation_id=foundation.candidate_id,
        selected_foundation=foundation,
        title_candidates=["书名一", "书名二", "书名三"],
        expanded_premise="特殊能力让普通对象产生超常结果。",
        protagonist="主角",
        protagonist_goal="证明能力可以改变处境",
        protagonist_conflict="外部压力阻止能力验证",
        protagonist_cost=protagonist_cost,
        protagonist_growth="从验证者扩大为改变环境的行动者",
        world_rules=["能力必须沿原功能连续发展"],
        foundation_settings=[
            FoundationSetting(
                setting_id="setting-one",
                category="WORLD_RULE",
                statement="能力结果可以超出普通工程上限",
                strength=SettingStrength.CORE,
            )
        ],
        characters=["主角"],
        factions=[],
        routes=[
            StoryRoute(
                route_id=f"route-{index}",
                title=f"路线 {index}",
                direction="沿能力验证打开新的行动空间",
                central_pressure="外部压力",
                opportunity="更高能力上限",
                risk="未知边界",
                commitments=["继续验证"],
            )
            for index in range(1, 4)
        ],
        recommended_route_id="route-1",
        recommendation_reason="最直接展示能力兑现",
        progression_grammar=["先扩大可能性，再打开更高 ceiling"],
        expansion_grammar=["让能力进入更大的异常环境"],
        payoff_grammar=["以不可复制的结果兑现当前能力"],
        first_phase=first_phase,
        first_phase_objective="完成第一次验证",
        rolling_planning=RollingPlanning(
            short=["完成能力验证"],
            mid=["探索更高能力上限"],
            long=["让能力改变更大范围的行动条件"],
        ),
        book_profile_draft=_profile(),
        first_chapter_candidates=[_chapter_candidate(index) for index in range(1, 4)],
        open_questions=[],
        hidden_truth_candidates=[],
        risks=[],
        avoid_cliches=[],
        kernel_contracts={},
        kernel_contract_proposals=None,
    )
    return proposal


def test_original_narrative_cost_fields_are_optional() -> None:
    assert not FirstPhaseProposal.model_fields["first_resource_bottleneck"].is_required()
    assert not FirstChapterCandidate.model_fields["cost"].is_required()
    assert not FoundationDevelopmentProposal.model_fields["protagonist_cost"].is_required()
    assert (
        not OriginalFoundationConfirmation.model_fields[
            "protagonist_cost_override"
        ].is_required()
    )
    assert FirstPhaseProposal.model_fields["first_resource_bottleneck"].default == ""
    assert FirstChapterCandidate.model_fields["cost"].default == ""
    assert FoundationDevelopmentProposal.model_fields["protagonist_cost"].default == ""
    assert (
        OriginalFoundationConfirmation.model_fields["protagonist_cost_override"].default
        is None
    )


def test_empty_costs_flow_through_genesis_and_contract_shapes() -> None:
    proposal = _development_proposal()
    confirmation = OriginalFoundationConfirmation(
        confirmed=True,
        selected_title="书名一",
        selected_foundation_id="foundation-one",
        selected_route_id="route-1",
        world_rules=["能力必须沿原功能连续发展"],
        first_phase_objective="完成第一次验证",
    )
    request = OriginalBookRequest(premise="特殊能力让普通对象产生超常结果。")

    plan = build_genesis_apply_plan(
        proposal_version_id="proposal-one",
        proposal=proposal,
        confirmation=confirmation,
        request=request,
    )

    assert all(item["title"] != "主角代价" for item in plan.author_truths)
    assert plan.first_phase["first_resource_bottleneck"] == ""
    for item in plan.first_chapter_candidates:
        assert item["cost"] == ""
        assert item["plan"]["opportunity_cost"] == ""
        assert item["plan"]["required_cost"] == ""
        CandidateProposal.model_validate(item["plan"])

    contract = ChapterContract(
        contract_id="contract-one",
        chapter=1,
        mode=ContinuationMode.CONSTRAINED_INNOVATION,
        boundary_packet_id="packet-one",
        continuation_boundary={},
        candidate_id=plan.first_chapter_candidates[0]["candidate_id"],
        primary_thread=plan.main_thread["thread_id"],
        primary_function=NarrativeFunction.SETUP,
        secondary_functions=[],
        reader_question="能力会打开什么新行动？",
        pressure={"before": 0, "target_after": 30},
        payoff_plan={},
        narrative_debt={"advance": [], "fully_pay": [], "new_major_hooks_allowed": 1},
        progress={"minimum_score": 25, "required_irreversible_change": "获得新行动空间"},
        required_irreversible_change="获得新行动空间",
        required_cost="",
        canon_constraints=[],
        knowledge_constraints=[],
        must_not_resolve=[],
        forbidden_repetitions=[],
        style_constraints={},
        ending_state="更高能力问题出现",
        commit_updates=["thread_status:thread-one"],
    )
    assert contract.required_cost == ""


def _confirmation(
    *,
    protagonist_cost_override: str | None = None,
    first_phase_overrides: dict[str, str] | None = None,
) -> OriginalFoundationConfirmation:
    return OriginalFoundationConfirmation(
        confirmed=True,
        selected_title="书名一",
        selected_foundation_id="foundation-one",
        selected_route_id="route-1",
        protagonist_cost_override=protagonist_cost_override,
        first_phase_overrides=first_phase_overrides or {},
        world_rules=["能力必须沿原功能连续发展"],
        first_phase_objective="完成第一次验证",
    )


def _genesis_plan(
    proposal: FoundationDevelopmentProposal,
    confirmation: OriginalFoundationConfirmation,
) -> GenesisApplyPlan:
    return build_genesis_apply_plan(
        proposal_version_id="proposal-one",
        proposal=proposal,
        confirmation=confirmation,
        request=OriginalBookRequest(premise="特殊能力让普通对象产生超常结果。"),
    )


def test_author_can_clear_protagonist_cost_and_first_resource_bottleneck() -> None:
    proposal = _development_proposal(
        protagonist_cost="AI 生成的代价",
        first_resource_bottleneck="AI 生成的资源瓶颈",
    )

    inherited = _genesis_plan(proposal, _confirmation())
    assert {
        item["statement"]
        for item in inherited.author_truths
        if item["title"] == "主角代价"
    } == {"AI 生成的代价"}
    assert inherited.first_phase["first_resource_bottleneck"] == "AI 生成的资源瓶颈"

    cleared = _genesis_plan(
        proposal,
        _confirmation(
            protagonist_cost_override="",
            first_phase_overrides={"first_resource_bottleneck": ""},
        ),
    )
    assert all(item["title"] != "主角代价" for item in cleared.author_truths)
    assert cleared.first_phase["first_resource_bottleneck"] == ""

    overridden = _genesis_plan(
        proposal,
        _confirmation(protagonist_cost_override="作者确认的代价"),
    )
    assert {
        item["statement"]
        for item in overridden.author_truths
        if item["title"] == "主角代价"
    } == {"作者确认的代价"}


def test_empty_mandatory_first_phase_override_keeps_proposal_value() -> None:
    proposal = _development_proposal()
    proposal.first_phase.first_payoff = "AI 生成的兑现"

    plan = _genesis_plan(
        proposal,
        _confirmation(
            first_phase_overrides={
                "first_resource_bottleneck": "",
                "first_payoff": "",
            }
        ),
    )

    assert plan.first_phase["first_resource_bottleneck"] == ""
    assert plan.first_phase["first_payoff"] == "AI 生成的兑现"


def _validation_context(
    *, required_cost: str, include_cost_evidence: bool
) -> ValidationContext:
    evidence = {
        "required_irreversible_change": ["不可逆改变"],
        "ending_state": ["结尾状态"],
        "commit:thread:main": ["线程证据"],
    }
    prose = "不可逆改变。结尾状态。线程证据。"
    if include_cost_evidence:
        evidence["required_cost"] = ["真实成本"]
        prose += "真实成本。"
    return ValidationContext(
        draft=DraftOutput.model_construct(
            task_id="task-cost",
            contract_id="contract-cost",
            chapter_title="成本校验",
            prose_markdown=prose,
            state_changes=[],
            contract_evidence=evidence,
            character_fit_inputs={},
            style_fit_inputs={},
            realized_kernel_trace=None,
        ),
        contract=ChapterContract.model_construct(
            contract_id="contract-cost",
            required_irreversible_change="不可逆改变",
            required_cost=required_cost,
            ending_state="结尾状态",
            commit_updates=["thread:main"],
            kernel_verification_status="LEGACY_NO_EFFECTIVE_CONTRACT",
        ),
        projection=cast(Any, None),
        settings=load_settings(),
    )


def test_empty_contract_cost_does_not_require_cost_evidence() -> None:
    report = validate_contract(
        _validation_context(required_cost="", include_cost_evidence=False)
    )

    assert report.passed
    assert all(
        finding.location != "contract_evidence:required_cost"
        for finding in report.findings
    )


def test_nonempty_contract_cost_still_requires_cost_evidence() -> None:
    report = validate_contract(
        _validation_context(required_cost="真实成本", include_cost_evidence=False)
    )

    assert not report.passed
    assert any(
        finding.code == "CONTRACT_REQUIREMENT_MISSING"
        and "required_cost" in finding.message
        for finding in report.findings
    )


def test_original_studio_preserves_explicit_empty_override_keys() -> None:
    javascript = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "novel_authoring"
        / "web"
        / "static"
        / "original.js"
    ).read_text(encoding="utf-8")

    assert (
        'protagonist_cost_override: String(form.get("protagonist_cost_override") || "").trim(),'
        in javascript
    )
    assert "firstPhaseOverrides[key.slice(13)] = String(value).trim();" in javascript
    assert "first_phase_overrides: firstPhaseOverrides," in javascript
