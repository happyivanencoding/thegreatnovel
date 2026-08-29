from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(r"C:\dev\tgn-story-mvp")
sys.path.insert(0, str(ROOT / "temps"))

from atomic_chapter_obligations import (  # noqa: E402
    AtomicObligation,
    CheckStatus,
    GateSeverity,
    ObligationKind,
    ObligationMode,
    ObligationPack,
    body,
    compile_obligations,
    infer_diff_operations,
    validate_candidate,
)


def pack_with(*obligations: AtomicObligation) -> ObligationPack:
    return ObligationPack(
        chapter=1,
        protagonist="顾停舟",
        mission_fields={},
        obligations=list(obligations),
        source_conflicts=[],
        unsupported_clauses=[],
        diagnostics=[],
        primary_paragraph_count=1,
    )


def hard(
    obligation_id: str,
    kind: ObligationKind,
    mode: ObligationMode,
    validator: dict,
    *,
    source_text: str = "test",
    evidence: tuple[int, ...] = (),
) -> AtomicObligation:
    return AtomicObligation(
        id=obligation_id,
        kind=kind,
        mode=mode,
        severity=GateSeverity.HARD,
        source_field="test",
        source_text=source_text,
        boundary="test boundary",
        validator=validator,
        primary_evidence_paragraphs=evidence,
    )


def decision(obligation: AtomicObligation, text: str, *, primary: str = "原文。", operations=None):
    actual_operations = (
        [{"kind": "REPLACE", "start": 1, "end": 1}]
        if operations is None
        else operations
    )
    return validate_candidate(
        pack_with(obligation),
        primary_body=primary,
        final_body=text,
        operations=actual_operations,
    )


def mission_prompt(
    *,
    trigger="地潮提前冲入旧关。",
    action="顾停舟稳住粮道。",
    reaction="守将带居民撤离。",
    result="粮道保住。",
    state="地潮提前的原因仍未解决。",
    ending="下一轮潮势将冲向撤离队伍。",
    reader_release="（本章没有单独排程 Reader Release。）",
    human_core="顾停舟想拥有自己的钱和行潮资格。",
) -> str:
    return f"""## FROZEN CHAPTER MISSION｜不得改剧情

触发事件：{trigger}
主角行动：{action}
对手或世界反应：{reaction}
直接结果：{result}
状态变化：{state}
结尾推动力：{ending}

## READER RELEASE｜本章已批准首次释放事实；逐条核对

{reader_release}

## HUMAN CORE｜Frozen Authority

# HUMAN SEED｜顾停舟／测试角色

{human_core}

## CANON INDEX｜已发生事实压缩索引

当前无额外冲突。
"""


def curator(relationships="- 守将：当前在场。") -> str:
    return f"""# Curator Audit

无。

# Curated Chapter Context

## Relevant Characters and Relationships

{relationships}

## Relevant Open Promises

- 地潮提前的原因仍未知。

## Relevant Book Contract

主角欲望、奖励和关系只在正文已有时保护。

## Payoff and Promise Window

NONE
"""


def test_lost_reward_cannot_also_be_received():
    obligation = hard(
        "MONEY-LOST",
        ObligationKind.MONEY,
        ObligationMode.TERMINAL,
        {
            "type": "status",
            "object_terms": ["尾款"],
            "status": "lost",
            "status_terms": ["无法兑现", "放弃", "落空"],
        },
    )
    result = decision(
        obligation,
        "实测尾款已经明确放弃。\n\n矿队随后又把尾款交到顾停舟手里。",
    )
    assert result["decision"] == "FALLBACK_FULL_REVISER"
    assert "conflicts" in result["blocking_checks"][0]["reason"]


def test_entitlement_is_not_cash_received():
    obligation = hard(
        "MONEY-1",
        ObligationKind.MONEY,
        ObligationMode.MUST_HOLD,
        {
            "type": "status",
            "object_terms": ["个人矿利"],
            "status": "entitlement_confirmed",
            "status_terms": ["份额", "登记", "依据"],
        },
    )
    passed = decision(obligation, "个人矿利份额已经登记，具体兑现尚待首批矿料核定。")
    failed = decision(obligation, "个人矿利八百潮铢已经到账。")
    assert passed["decision"] == "ADOPT_DELTA"
    assert failed["decision"] == "FALLBACK_FULL_REVISER"
    assert any(
        marker in failed["blocking_checks"][0]["reason"]
        for marker in ("upgraded", "missing", "conflicts")
    )


def test_battle_scale_is_not_stable_power_tier():
    obligation = hard(
        "POWER-1",
        ObligationKind.POWER_BOUNDARY,
        ObligationMode.MUST_NOT_HOLD,
        {"type": "forbid_power_transition", "target": "镇海", "subject": "顾停舟"},
    )
    assert decision(obligation, "顾停舟承住了镇海冲击，并把潮兽压回远潮。")["decision"] == "ADOPT_DELTA"
    assert decision(obligation, "顾停舟正式进入镇海，力量完成稳定突破。")["decision"] == "FALLBACK_FULL_REVISER"


def test_current_canon_power_ceiling_forbids_unapproved_higher_tier():
    prompt = mission_prompt().replace(
        "当前无额外冲突。",
        """## PERSISTENT CANON：
### Power / Capability
照域潮谱已被顾停舟正式掌握，可维持局部潮路。

## OPEN PROMISES：
- 顾停舟未来可能进入镇海。""",
    )
    pack = compile_obligations(
        chapter=1,
        authority_prompt=prompt,
        curator_response=curator(),
        primary_body="顾停舟稳住粮道。\n\n粮道保住。",
    )
    guards = [
        item for item in pack.obligations
        if item.source_field == "CANON INDEX / current stable power"
    ]
    assert [item.object for item in guards] == ["镇海"]
    failed = validate_candidate(
        pack_with(guards[0]),
        primary_body="顾停舟稳住粮道。",
        final_body="顾停舟正式进入镇海。",
        operations=[{"kind": "REPLACE", "start": 1, "end": 1}],
    )
    assert failed["decision"] == "FALLBACK_FULL_REVISER"


def test_missing_current_tier_does_not_allow_any_unapproved_transition():
    pack = compile_obligations(
        chapter=1,
        authority_prompt=mission_prompt(),
        curator_response=curator(),
        primary_body="顾停舟稳住粮道。\n\n粮道保住。",
    )
    guards = [
        item for item in pack.obligations
        if item.source_field == "CANON INDEX / current stable power"
    ]
    assert {item.object for item in guards} == {"入潮", "成炉", "照域", "镇海"}


def test_negated_original_transfer_does_not_trigger_conflict():
    obligation = hard(
        "OWN-NEG",
        ObligationKind.OWNERSHIP,
        ObligationMode.TERMINAL,
        {
            "type": "ownership",
            "object_terms": ["原路线册", "路线册", "原册"],
            "owner_terms": ["顾停舟", "他"],
            "possession_terms": ["收进怀里", "持有", "保留"],
            "forbidden_transfer_terms": ["送入", "交出", "带着"],
            "forbidden_destination_terms": ["校路官", "校路台"],
        },
    )
    result = decision(
        obligation,
        "顾停舟没有把路线册交出去，校路官只记下副本。\n\n顾停舟把原册收进怀里。",
    )
    assert result["decision"] == "ADOPT_DELTA"


def test_negated_departure_does_not_count_as_departed():
    obligation = hard(
        "END-NEG",
        ObligationKind.ENDING,
        ObligationMode.TERMINAL,
        {
            "type": "departure",
            "protagonist": "顾停舟",
            "subject_terms": ["顾停舟", "他"],
            "terms": ["上车", "随队出发", "驶去"],
            "context_terms": ["粮车", "粮队", "旧关"],
        },
    )
    failed = decision(
        obligation,
        "第一批粮车还在巷口等着，顾停舟还没有上车。",
    )
    passed = decision(
        obligation,
        "顾停舟踩上粮车，车轮朝旧关驶去。",
    )
    assert failed["decision"] == "FALLBACK_FULL_REVISER"
    assert passed["decision"] == "ADOPT_DELTA"


def test_original_and_copy_are_different_objects():
    ownership = hard(
        "OWN-1",
        ObligationKind.OWNERSHIP,
        ObligationMode.TERMINAL,
        {
            "type": "ownership",
            "object_terms": ["原路线册", "原册"],
            "owner_terms": ["顾停舟", "我"],
            "possession_terms": ["持有", "保留", "仍在", "归我"],
        },
    )
    transfer = hard(
        "OWN-2",
        ObligationKind.OWNERSHIP,
        ObligationMode.MUST_HOLD,
        {
            "type": "transfer",
            "object_terms": ["事实副本", "副本"],
            "destination_terms": ["校路台"],
            "transfer_terms": ["送入", "送到"],
        },
    )
    pack = pack_with(ownership, transfer)
    good = validate_candidate(
        pack,
        primary_body="原文。",
        final_body="原路线册仍由顾停舟持有。\n\n校路官把事实副本送入校路台。",
        operations=[{"kind": "REPLACE", "start": 1, "end": 1}],
    )
    bad = validate_candidate(
        pack,
        primary_body="原文。",
        final_body="校路官把原路线册送入校路台。",
        operations=[{"kind": "REPLACE", "start": 1, "end": 1}],
    )
    assert good["decision"] == "ADOPT_DELTA"
    assert bad["decision"] == "FALLBACK_FULL_REVISER"


def test_possession_and_dispute_can_coexist():
    possession = hard(
        "OWN-1",
        ObligationKind.OWNERSHIP,
        ObligationMode.TERMINAL,
        {
            "type": "ownership",
            "object_terms": ["回潮楔", "楔子"],
            "owner_terms": ["顾停舟", "他"],
            "possession_terms": ["手里", "收回袖中", "持有"],
        },
    )
    dispute = hard(
        "OWN-2",
        ObligationKind.OWNERSHIP,
        ObligationMode.MUST_HOLD,
        {
            "type": "dispute",
            "object_terms": ["回潮楔", "楔子"],
            "dispute_terms": ["争议", "追索", "主张"],
        },
    )
    result = validate_candidate(
        pack_with(possession, dispute),
        primary_body="原文。",
        final_body="顾停舟把回潮楔收回袖中。\n\n阮青蜃仍对楔子的归属提出追索。",
        operations=[{"kind": "REPLACE", "start": 1, "end": 1}],
    )
    assert result["decision"] == "ADOPT_DELTA"


def test_actor_action_object_rejects_body_for_clone():
    obligation = hard(
        "ACT-1",
        ObligationKind.ACTOR_ACTION_OBJECT,
        ObligationMode.MUST_HOLD,
        {
            "type": "actor_action_object",
            "subject_terms": ["分身", "它"],
            "object_terms": ["回潮楔", "楔子"],
            "actions": ["fix"],
        },
    )
    good = decision(obligation, "分身把回潮楔钉进第二个潮压节点。")
    bad = decision(obligation, "分身按住地面。\n\n本体把回潮楔钉进第二个潮压节点。")
    assert good["decision"] == "ADOPT_DELTA"
    assert bad["decision"] == "FALLBACK_FULL_REVISER"


def test_unresolved_fact_does_not_require_repetition_but_forbids_answer():
    obligation = hard(
        "UNK-1",
        ObligationKind.UNRESOLVED_FACT,
        ObligationMode.MUST_REMAIN_UNKNOWN,
        {
            "type": "unresolved",
            "topic_terms": ["地潮提前"],
            "revelation_terms": ["原因是", "真相是", "查明"],
        },
    )
    assert decision(obligation, "顾停舟带着回潮楔进入观测点。", primary="原文。", operations=[])["decision"] == "ADOPT_DELTA"
    assert decision(obligation, "地潮提前的原因是照域潮谱被人改过。") ["decision"] == "FALLBACK_FULL_REVISER"


def test_deadline_word_does_not_match_dichao_tiqian():
    pack = compile_obligations(
        chapter=1,
        authority_prompt=mission_prompt(trigger="地潮提前冲入旧关。", ending="下一轮潮势将冲向撤离队伍。"),
        curator_response=curator(),
        primary_body="地潮比预期更早撞上旧关。\n\n顾停舟稳住粮道。\n\n守将带居民撤离。\n\n粮道保住。",
    )
    assert not [item for item in pack.obligations if item.kind == ObligationKind.TIME_WINDOW]


def test_explicit_low_tide_deadline_compiles():
    pack = compile_obligations(
        chapter=1,
        authority_prompt=mission_prompt(ending="下一次低潮前必须核查新裂槽。"),
        curator_response=curator(),
        primary_body="地潮撞上旧关。\n\n顾停舟稳住粮道。\n\n守将带居民撤离。\n\n下一次低潮前，他必须核查新裂槽。",
    )
    deadlines = [item for item in pack.obligations if item.kind == ObligationKind.TIME_WINDOW]
    assert len(deadlines) == 1
    assert "下一次低潮前" in deadlines[0].object


def test_cooldown_before_reuse_is_not_terminal_dissipation():
    pack = compile_obligations(
        chapter=1,
        authority_prompt=mission_prompt(
            action="顾停舟让回潮楔完成一次改向。",
            state="回潮楔再次使用前必须散尽残压，不能连续硬压。",
        ),
        curator_response=curator(),
        primary_body="回潮楔上的残压还在散，散尽之前不能再次硬压。\n\n粮道保住。",
    )
    cooldown = [
        item for item in pack.obligations
        if item.validator.get("type") == "residual_pressure"
    ]
    assert len(cooldown) == 1
    assert cooldown[0].validator["terminal"] is False
    result = validate_candidate(
        pack_with(cooldown[0]),
        primary_body="回潮楔上的残压还在散，散尽之前不能再次硬压。",
        final_body="回潮楔上的残压还在散，散尽之前不能再次硬压。",
        operations=[{"kind": "REPLACE", "start": 1, "end": 1}],
    )
    assert result["decision"] == "ADOPT_DELTA"


def test_explicit_chapter_end_dissipation_is_terminal():
    pack = compile_obligations(
        chapter=1,
        authority_prompt=mission_prompt(
            action="顾停舟让回潮楔完成一次改向。",
            state="本章结束时回潮楔残压已经散尽。",
        ),
        curator_response=curator(),
        primary_body="回潮楔残压已经散尽。\n\n粮道保住。",
    )
    terminal = [
        item for item in pack.obligations
        if item.validator.get("type") == "residual_pressure"
    ]
    assert len(terminal) == 1
    assert terminal[0].validator["terminal"] is True
    failed = validate_candidate(
        pack_with(terminal[0]),
        primary_body="回潮楔残压已经散尽。",
        final_body="回潮楔残压还在散。",
        operations=[{"kind": "REPLACE", "start": 1, "end": 1}],
    )
    assert failed["decision"] == "FALLBACK_FULL_REVISER"


def test_source_conflict_preflight_falls_back():
    pack = compile_obligations(
        chapter=1,
        authority_prompt=mission_prompt(
            state="个人矿利具体兑现尚待战后结算。",
            ending="个人矿利终于到账。",
        ),
        curator_response=curator(),
        primary_body="顾停舟完成战斗。",
    )
    assert not pack.preflight_eligible
    assert any("terminal conflict" in conflict for conflict in pack.source_conflicts)


def test_current_mission_actor_outranks_stale_remote_human_seed():
    prompt = mission_prompt(action="顾停舟稳住粮道。").replace(
        "HUMAN SEED｜顾停舟／测试角色",
        "HUMAN SEED｜顾临川／过期原型",
    )
    pack = compile_obligations(
        chapter=1,
        authority_prompt=prompt,
        curator_response=curator(),
        primary_body="顾停舟稳住粮道。\n\n粮道保住。",
    )
    assert pack.protagonist == "顾停舟"
    action = next(item for item in pack.obligations if item.source_field == "主角行动")
    assert action.subject == "顾停舟"


def test_full_settlement_cannot_be_satisfied_by_first_partial_payment():
    obligation = hard(
        "MONEY-FULL",
        ObligationKind.MONEY,
        ObligationMode.TERMINAL,
        {
            "type": "status",
            "object_terms": ["个人矿利"],
            "status": "received",
            "status_terms": ["到账", "交到手里"],
            "partial_authorized": False,
            "authorized_amounts": [],
        },
    )
    failed = decision(obligation, "战后首笔个人矿利已经到账。")
    passed = decision(obligation, "战后个人矿利已经全部结清，交到顾停舟手里。")
    assert failed["decision"] == "FALLBACK_FULL_REVISER"
    assert "partial" in failed["blocking_checks"][0]["reason"]
    assert passed["decision"] == "ADOPT_DELTA"


def test_explicit_partial_payment_accepts_first_payment_but_not_invented_amount():
    obligation = hard(
        "MONEY-PARTIAL",
        ObligationKind.MONEY,
        ObligationMode.TERMINAL,
        {
            "type": "status",
            "object_terms": ["个人矿利"],
            "status": "received",
            "status_terms": ["到账", "交到手里"],
            "partial_authorized": True,
            "authorized_amounts": ["八百潮铢"],
        },
    )
    passed = decision(obligation, "首笔个人矿利八百潮铢已经到账。")
    invented = decision(obligation, "首笔个人矿利一千潮铢已经到账。")
    assert passed["decision"] == "ADOPT_DELTA"
    assert invented["decision"] == "FALLBACK_FULL_REVISER"
    assert "unauthorized amount" in invented["blocking_checks"][0]["reason"]


def test_public_proof_requires_bound_performance_ruler_and_repricing():
    proof = hard(
        "PROOF-1",
        ObligationKind.PUBLIC_PROOF,
        ObligationMode.MUST_HOLD,
        {
            "type": "public_proof",
            "subject_terms": ["顾停舟", "他"],
            "topic_terms": ["回潮楔", "潮压"],
            "performance_terms": ["稳住", "改向"],
            "ruler_terms": ["守将", "懂行"],
            "repricing_terms": ["报价", "入册"],
        },
    )
    good = decision(
        proof,
        "顾停舟用回潮楔稳住潮压。\n\n守将看完改向，明确说这超过普通成炉手段。\n\n军府当场把他的战绩入册，并重新报价。",
    )
    unrelated = decision(
        proof,
        "顾停舟用回潮楔稳住潮压。\n\n守将看着远处的粮队。\n\n商人给一匹无关驮兽重新报价。",
    )
    assert good["decision"] == "ADOPT_DELTA"
    assert unrelated["decision"] == "FALLBACK_FULL_REVISER"


def test_relationship_transition_requires_the_named_counterpart():
    relationship = hard(
        "REL-1",
        ObligationKind.RELATIONSHIP_STATE,
        ObligationMode.TERMINAL,
        {
            "type": "relationship",
            "subject_terms": ["顾停舟", "他"],
            "counterpart_terms": ["少东家"],
            "terms": ["主从", "同行", "合作"],
            "transition_terms": ["不再", "转为", "各走自己的"],
        },
    )
    good = decision(
        relationship,
        "少东家看着顾停舟，说今后不再以雇主身份叫他回去，两人转为各自定价的同行者。",
    )
    unrelated = decision(
        relationship,
        "顾停舟与校路官谈成一份合作。\n\n少东家仍站在门外。",
    )
    assert good["decision"] == "ADOPT_DELTA"
    assert unrelated["decision"] == "FALLBACK_FULL_REVISER"


def test_surprise_is_protected_only_when_primary_already_contains_it():
    surprise = hard(
        "SURPRISE-1",
        ObligationKind.COMMERCIAL_VALUE,
        ObligationMode.PRESERVE_IF_PRESENT,
        {
            "type": "commercial_preserve",
            "category": "surprise",
            "markers": ["没想到", "竟然"],
            "source_paragraphs": [1],
            "key_terms": ["回潮楔"],
            "source_text": "谁也没想到，回潮楔里竟然还藏着第二层潮纹。",
        },
        evidence=(1,),
    )
    untouched = decision(
        surprise,
        "谁也没想到，回潮楔里竟然还藏着第二层潮纹。",
        primary="谁也没想到，回潮楔里竟然还藏着第二层潮纹。",
        operations=[],
    )
    erased = decision(
        surprise,
        "顾停舟检查了回潮楔。",
        primary="谁也没想到，回潮楔里竟然还藏着第二层潮纹。",
        operations=[{"kind": "REPLACE", "start": 1, "end": 1}],
    )
    assert untouched["decision"] == "ADOPT_DELTA"
    assert erased["decision"] == "FALLBACK_FULL_REVISER"


def test_unapproved_prior_dialogue_backreference_fails_whole_draft_gate():
    obligation = hard(
        "PRIOR-QUOTE-1",
        ObligationKind.SOURCE_CONFLICT,
        ObligationMode.MUST_NOT_HOLD,
        {
            "type": "prior_quote",
            "authorized_quotes": ["回去以后还有一堆烂账"],
        },
    )
    invented = decision(obligation, "这比少东家那句‘回去再算’更干脆。")
    authorized = decision(obligation, "这比少东家那句‘回去以后还有一堆烂账’更干脆。")
    current_dialogue = decision(obligation, "少东家说：‘回去再算。’")
    assert invented["decision"] == "FALLBACK_FULL_REVISER"
    assert "prior dialogue" in invented["blocking_checks"][0]["reason"]
    assert authorized["decision"] == "ADOPT_DELTA"
    assert current_dialogue["decision"] == "ADOPT_DELTA"


def test_human_cue_requires_named_person_and_contact():
    human = "陆绾身上的药粉气味在身体靠近时会牵动顾停舟的私人注意。"
    relationships = "- 陆绾：当前在场，与顾停舟发生近身治疗。"
    prompt = mission_prompt(human_core=human)
    with_contact = compile_obligations(
        chapter=1,
        authority_prompt=prompt,
        curator_response=curator(relationships),
        primary_body="陆绾抓住顾停舟的手臂替他包扎。\n\n粮道保住。",
    )
    cues = [item for item in with_contact.obligations if item.kind == ObligationKind.HUMAN_CUE]
    assert len(cues) == 1
    cue_pack = pack_with(cues[0])
    missing = validate_candidate(
        cue_pack,
        primary_body="陆绾抓住顾停舟的手臂替他包扎。\n\n粮道保住。",
        final_body="陆绾抓住顾停舟的手臂替他包扎。\n\n粮道保住。",
        operations=[{"kind": "REPLACE", "start": 1, "end": 1}],
    )
    present = validate_candidate(
        cue_pack,
        primary_body="陆绾抓住顾停舟的手臂替他包扎。\n\n粮道保住。",
        final_body="陆绾抓住顾停舟的手臂替他包扎，靠近时药粉气味压过血腥味。\n\n粮道保住。",
        operations=[{"kind": "REPLACE", "start": 1, "end": 1}],
    )
    assert missing["decision"] == "FALLBACK_FULL_REVISER"
    assert present["decision"] == "ADOPT_DELTA"

    without_contact = compile_obligations(
        chapter=1,
        authority_prompt=prompt,
        curator_response=curator(relationships),
        primary_body="陆绾站在另一边守住出口。\n\n粮道保住。",
    )
    assert not [item for item in without_contact.obligations if item.kind == ObligationKind.HUMAN_CUE]


def test_commercial_value_is_preserve_if_present_not_quota():
    obligation = hard(
        "VALUE-1",
        ObligationKind.COMMERCIAL_VALUE,
        ObligationMode.PRESERVE_IF_PRESENT,
        {
            "type": "commercial_preserve",
            "category": "desire",
            "markers": ["想要", "属于自己"],
            "source_paragraph": 1,
        },
        source_text="顾停舟想要一条真正属于自己的路。",
        evidence=(1,),
    )
    untouched = decision(
        obligation,
        "顾停舟想要一条真正属于自己的路。",
        primary="顾停舟想要一条真正属于自己的路。",
        operations=[],
    )
    deleted = decision(
        obligation,
        "顾停舟完成了任务。",
        primary="顾停舟想要一条真正属于自己的路。",
        operations=[{"kind": "DELETE", "start": 1, "end": 1}],
    )
    assert untouched["decision"] == "ADOPT_DELTA"
    assert deleted["decision"] == "FALLBACK_FULL_REVISER"


@pytest.mark.parametrize(
    ("chapter", "eligible"),
    [(2, True), (3, False), (9, True), (10, False), (14, True), (16, True), (19, False)],
)
def test_representative_preflight_boundaries(chapter: int, eligible: bool):
    directory = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs" / f"chapter-{chapter:04d}"
    pack = compile_obligations(
        chapter=chapter,
        authority_prompt=(directory / "authority_reviser_prompt.md").read_text(encoding="utf-8"),
        curator_response=(directory / "curator_response.md").read_text(encoding="utf-8"),
        primary_body=body((directory / "primary_response.md").read_text(encoding="utf-8")),
    )
    assert pack.preflight_eligible is eligible


def test_full_reviser_residual_failures_are_not_hidden():
    source = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
    expected = {
        2: "ADOPT_DELTA",
        9: "ADOPT_DELTA",
        14: "ADOPT_DELTA",  # bound performance → ruler → repricing sequence is present
        16: "FALLBACK_FULL_REVISER",  # body/clone artifact actor drift
    }
    for chapter, expected_decision in expected.items():
        directory = source / f"chapter-{chapter:04d}"
        primary = body((directory / "primary_response.md").read_text(encoding="utf-8"))
        final = body((directory / "authority_reviser_response.md").read_text(encoding="utf-8"))
        pack = compile_obligations(
            chapter=chapter,
            authority_prompt=(directory / "authority_reviser_prompt.md").read_text(encoding="utf-8"),
            curator_response=(directory / "curator_response.md").read_text(encoding="utf-8"),
            primary_body=primary,
        )
        result = validate_candidate(
            pack,
            primary_body=primary,
            final_body=final,
            operations=infer_diff_operations(primary, final),
        )
        assert result["decision"] == expected_decision
