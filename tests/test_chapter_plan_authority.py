from story_mvp.chapter_context import (
    PLAN_OUTCOME_ADJUSTMENT_MARKER,
    build_chapter_context,
    parse_chapter_plan_fields,
    project_chapter_plan_execution_boundary,
)
from story_mvp.prompts import generate_prompt


PLAN = """## 第19章：镇海关上
具体剧情：顾停舟以照域正面承受镇海潮兽冲击，分身把回潮楔送到第二个潮眼。
结果 / 状态变化：顾停舟本人进入镇海，镇海潮兽被压回远潮；回潮楔新增裂痕。
叙事功能：完成第一世界最高战局。
结尾推动：战后矿利与护粮结算到账，下一章顾停舟决定是否买潮舟。"""


MISSION_WITH_SILENT_TIER_LOSS = """触发事件：镇海潮兽撞向旧关。
推动事件的人：镇海潮兽。
主角行动：顾停舟以照域承压，分身钉住第二潮眼。
对手或世界反应：潮兽被改向的潮水推回远潮。
直接结果：居民、粮道与三座新井保住。
状态变化：顾停舟重伤，回潮楔新增裂痕。
叙事功能：完成最高战局。
结尾推动力：战后开始结算。"""


def test_future10_plan_is_split_into_execute_now_and_handoff_reservation() -> None:
    values = parse_chapter_plan_fields(PLAN)
    assert values["结果 / 状态变化"].startswith("顾停舟本人进入镇海")

    projection = project_chapter_plan_execution_boundary(PLAN)
    assert "本章唯一可执行事件预算" in projection
    assert "必须兑现的计划结果 / 状态变化：顾停舟本人进入镇海" in projection
    assert "章末 Handoff Reservation" in projection
    assert "不得在本章完成其下一步事件或结算" in projection
    assert "下一章顾停舟决定是否买潮舟" in projection


def test_director_receives_current_plan_as_unique_event_budget_and_long_block_as_context_only() -> None:
    prompt = generate_prompt(
        mode="director",
        template="",
        book_content="BOOK",
        chapter_number=19,
        current_long_block="阶段背景：最高战局后还会有战后买船与远行。",
        current_chapter_plan=PLAN,
    )
    assert "当前章执行边界（确定性拆分；唯一事件预算）" in prompt
    assert "当前大型剧情块（仅阶段背景；不能授权本章追加事件/结果）" in prompt
    assert "必须兑现的计划结果 / 状态变化：顾停舟本人进入镇海" in prompt
    assert "章末 Handoff Reservation" in prompt
    assert "当前大型剧情块只提供阶段背景" in prompt


def test_chapter_mission_deterministically_freezes_plan_outcome_even_when_director_drops_it() -> None:
    packet = build_chapter_context(
        current_outline=MISSION_WITH_SILENT_TIER_LOSS,
        current_chapter_plan=PLAN,
    )
    assert "上游计划已批准结果" in packet.chapter_mission
    assert "状态变化：" in packet.chapter_mission
    assert "顾停舟本人进入镇海" in packet.chapter_mission
    assert "Canon 优先" in packet.chapter_mission


def test_primary_and_reviser_inherit_plan_outcome_only_through_frozen_mission() -> None:
    primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="BOOK",
        chapter_number=19,
        current_outline=MISSION_WITH_SILENT_TIER_LOSS,
        current_chapter_plan=PLAN,
    )
    reviser = generate_prompt(
        mode="authority_reviser",
        template="",
        book_content="BOOK",
        chapter_number=19,
        current_outline=MISSION_WITH_SILENT_TIER_LOSS,
        current_chapter_plan=PLAN,
        primary_draft="顾停舟以照域承住潮兽冲击，最终将潮兽压回远潮。",
    )
    for prompt in (primary, reviser):
        assert "上游计划已批准结果" in prompt
        assert "顾停舟本人进入镇海" in prompt
        assert "CURRENT PLAN OUTCOME AUTHORITY" not in prompt


def test_canon_conflict_can_explicitly_adjust_plan_outcome_without_silent_cancellation() -> None:
    adjusted = MISSION_WITH_SILENT_TIER_LOSS.replace(
        "状态变化：顾停舟重伤，回潮楔新增裂痕。",
        f"状态变化：{PLAN_OUTCOME_ADJUSTMENT_MARKER} 前章 Canon 已确认潮炉破损，本章不能进入镇海；改为保住照域。",
    )
    packet = build_chapter_context(
        current_outline=adjusted,
        current_chapter_plan=PLAN,
    )
    assert PLAN_OUTCOME_ADJUSTMENT_MARKER in packet.chapter_mission
    assert "前章 Canon 已确认潮炉破损" in packet.chapter_mission
    assert "上游计划已批准结果" not in packet.chapter_mission
    assert "顾停舟本人进入镇海" not in packet.chapter_mission


def test_director_contract_requires_explicit_adjustment_marker_only_for_real_canon_conflict() -> None:
    prompt = generate_prompt(
        mode="director",
        template="",
        book_content="BOOK",
        chapter_number=19,
        current_long_block="阶段背景",
        current_chapter_plan=PLAN,
    )
    assert PLAN_OUTCOME_ADJUSTMENT_MARKER in prompt
    assert "该标记只处理事实冲突" in prompt
    assert "不授权因为节奏、审美或方便取消结果" in prompt
