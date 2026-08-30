from pathlib import Path

import pytest

from story_mvp.chapter_context import build_chapter_context, build_director_context
from story_mvp.prompts import OUTLINE_TEMPLATE, STORY_PROGRAM_TEMPLATE, generate_prompt
from story_mvp.run_ledger import (
    create_or_load_run,
    load_node_prompt,
    retry_node,
    save_node_prompt,
    save_node_response,
)
from story_mvp.story_event_obligations import (
    BOOK_REGISTRY_HEADING,
    PROGRAM_REGISTRY_HEADING,
    RUNTIME_OBLIGATION_HEADING,
    chapter_story_event_ids,
    missing_story_events,
    parse_story_program_protected_events,
    validate_book_registry_against_story_program,
)


STORY_PROGRAM = f"""# STORY PROGRAM

## 核心碰撞
故乡与更高层规则第一次发生冲突。

{PROGRAM_REGISTRY_HEADING}
### RSE-01
事件原子：旧灼痕上的界签首次显现 → 北燧城被明确标记为第一副本 → 十二日期限与落日隧道合法归门同时进入裴骁认知 → 只有本地真实取得且确认归属的成果可携带离开
状态残留：界阶1成立；该 State 不能替代界签首次显现与副本规则进入读者认知的现场事件
排程边界：第1章
读者证明锚点：界签；第一副本；十二日；合法归门

## 全书成长与核心幻想兑现脊柱
后续继续。
"""


REGISTRY = f"""{BOOK_REGISTRY_HEADING}
#### RSE-01
事件原子：旧灼痕上的界签首次显现 → 北燧城被明确标记为第一副本 → 十二日期限与落日隧道合法归门同时进入裴骁认知 → 只有本地真实取得且确认归属的成果可携带离开
状态残留：界阶1成立；该 State 不能替代界签首次显现与副本规则进入读者认知的现场事件
排程边界：第1章
读者证明锚点：界签；第一副本；十二日；合法归门
"""


CHAPTER_PLAN = """## 第1章：明擂押上最后一把
具体剧情：裴骁押上试火钱参加明擂，兽袭时抢回真昼炭并点燃灯芯。
结果 / 状态变化：裴骁进入灯阶1，界阶1成立。
叙事功能：完成开篇第一次力量兑现。
结尾推动：主灯即将熄灭。
不可降格 Story Event：RSE-01"""


MISSION = """触发事件：熄行兽扑灭擂场外灯火。
推动事件的人：熄行兽。
主角行动：裴骁抢回真昼炭并点燃灯芯。
对手或世界反应：熄行兽扑向火源。
直接结果：裴骁正面撞退熄行兽。
状态变化：裴骁进入灯阶1。
叙事功能：完成开篇力量兑现。
结尾推动力：主灯继续熄灭。"""


BOOK = f"""# 小说总体设计画像

## 0. 本书成长基因图
### 核心不变量
越限完成后留下。

## 1. 核心类型与读者承诺
副本成长爽文。
{REGISTRY}

## 2. 世界观结构
北燧城依靠灯火生活。

## 3. 世界如何持续制造剧情压力
光带退潮。

## 4. 主角模型、人物弧与核心矛盾
裴骁要钱、面子和离城。

## 5. 配角与关系系统
裴禾会拆穿他的借口。

# 当前中期规划窗口

## 第1—2章：明擂
完成第一次公开胜负。

# 未来十章逐章小纲

{CHAPTER_PLAN}

## 第2章：第三次之后
具体剧情：裴骁完成第三次过烧。
结果 / 状态变化：第三次过烧留下。
叙事功能：兑现能力。
结尾推动：车队出城。

# 当前状态、未兑现承诺与作者备注

故事尚未开始。
"""


def test_story_program_event_registry_is_small_typed_authority() -> None:
    events = parse_story_program_protected_events(STORY_PROGRAM)
    assert tuple(events) == ("RSE-01",)
    event = events["RSE-01"]
    assert "第一副本" in event.event_atom
    assert event.state_residue.startswith("界阶1成立")
    assert event.reader_anchors == ("界签", "第一副本", "十二日", "合法归门")


def test_outline_must_copy_event_atom_exactly_and_schedule_exact_chapter() -> None:
    validate_book_registry_against_story_program(STORY_PROGRAM, BOOK)

    dropped = BOOK.replace(REGISTRY, "")
    with pytest.raises(ValueError, match="缺失 RSE-01"):
        validate_book_registry_against_story_program(STORY_PROGRAM, dropped)

    rewritten = BOOK.replace("北燧城被明确标记为第一副本", "北燧城发生异常")
    with pytest.raises(ValueError, match="被改写"):
        validate_book_registry_against_story_program(STORY_PROGRAM, rewritten)

    unscheduled = BOOK.replace("\n不可降格 Story Event：RSE-01", "")
    with pytest.raises(ValueError, match="第1章"):
        validate_book_registry_against_story_program(STORY_PROGRAM, unscheduled)


def test_scheduled_event_atom_enters_director_budget_and_frozen_mission() -> None:
    packet = build_chapter_context(
        book_content=BOOK,
        current_outline=MISSION,
        current_chapter_plan=CHAPTER_PLAN,
        chapter_number=1,
    )
    assert RUNTIME_OBLIGATION_HEADING in packet.protected_story_events
    assert "第一副本" in packet.chapter_mission
    assert "状态残留" in packet.chapter_mission
    assert "状态残留不能替代事件" in packet.chapter_mission

    director = build_director_context(packet)
    assert "不可降格 Reader-Facing Story Event" in director.current_chapter_plan
    assert "界签首次显现" in director.current_chapter_plan
    assert "十二日" in director.current_chapter_plan


def test_primary_and_reviser_receive_event_atom_without_full_story_program() -> None:
    primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content=BOOK,
        chapter_number=1,
        current_outline=MISSION,
        current_chapter_plan=CHAPTER_PLAN,
    )
    reviser = generate_prompt(
        mode="authority_reviser",
        template="",
        book_content=BOOK,
        chapter_number=1,
        current_outline=MISSION,
        current_chapter_plan=CHAPTER_PLAN,
        primary_draft="裴骁抢回真昼炭，胸口点亮灯火。",
    )
    for prompt in (primary, reviser):
        assert "界签首次显现" in prompt
        assert "第一副本" in prompt
        assert "合法归门" in prompt
        assert "# STORY PROGRAM" not in prompt


def test_anchor_closure_distinguishes_event_from_state_only() -> None:
    packet = build_chapter_context(
        book_content=BOOK,
        current_outline=MISSION,
        current_chapter_plan=CHAPTER_PLAN,
        chapter_number=1,
    )
    authority_prompt = f"AUTHORITY\n\n{packet.chapter_mission}"
    state_only = "# 正式正文\n裴骁点燃灯芯。商盟见证者说：界阶1。"
    missing = missing_story_events(authority_prompt, state_only)
    assert [event.event_id for event in missing] == ["RSE-01"]

    realized = """# 正式正文
旧灼痕浮出界签：第一副本，沉昼界·北燧城。剩余十二日。合法归门位于落日隧道。"""
    assert missing_story_events(authority_prompt, realized) == ()


def test_authority_reviser_gets_only_one_bounded_story_event_repair(tmp_path: Path) -> None:
    packet = build_chapter_context(
        book_content=BOOK,
        current_outline=MISSION,
        current_chapter_plan=CHAPTER_PLAN,
        chapter_number=1,
    )
    authority_prompt = f"AUTHORITY\n\n{packet.chapter_mission}"
    state_only = "# 正式正文\n裴骁跨过关口，正式进入灯阶1，界阶1成立。"
    realized = "# 正式正文\n裴骁正式进入灯阶1。旧灼痕浮出界签：第一副本，沉昼界·北燧城。只剩十二日，合法归门在落日隧道。"

    book_dir = tmp_path / "book"
    create_or_load_run(book_dir, 1, writer_mode="curator_primary")
    save_node_prompt(book_dir, 1, "authority_reviser", authority_prompt)

    first = save_node_response(book_dir, 1, "authority_reviser", state_only)
    node = first["nodes"]["authority_reviser"]
    assert node["status"] == "failed"
    assert node["repair_reason"] == "missing_protected_story_event"
    assert node["required_story_event_ids"] == ["RSE-01"]
    repair_prompt = load_node_prompt(book_dir, 1, "authority_reviser")
    assert "Protected Story Event Repair" in repair_prompt
    assert "状态残留（不能替代事件）" in repair_prompt

    retry_node(book_dir, 1, "authority_reviser")
    second = save_node_response(book_dir, 1, "authority_reviser", realized)
    node = second["nodes"]["authority_reviser"]
    assert node["status"] == "completed"
    assert "repair_reason" not in node
    assert "required_story_event_ids" not in node


def test_story_and_outline_prompts_explicitly_forbid_event_to_state_collapse() -> None:
    assert "## 不可降格的 Reader-Facing Story Events" in STORY_PROGRAM_TEMPLATE
    assert "某个 State 已成立" in STORY_PROGRAM_TEMPLATE
    assert "Reader-Facing Fact Language" in STORY_PROGRAM_TEMPLATE
    assert "Event Atom 是语义 Authority，不是要求正文逐字照抄" in STORY_PROGRAM_TEMPLATE
    assert "reader-safe literal" in STORY_PROGRAM_TEMPLATE
    assert "不要把后台策划词、状态标签、抽象规则概括" in STORY_PROGRAM_TEMPLATE
    assert "### 不可降格 Reader-Facing Story Event Registry" in OUTLINE_TEMPLATE
    assert "不能改写、缩写或补充事件原子" in OUTLINE_TEMPLATE
    assert "不可降格 Story Event" in OUTLINE_TEMPLATE


def test_future_protected_event_registry_does_not_leak_into_current_chapter_prompts() -> None:
    future_registry = """#### RSE-20
事件原子：第二十章才允许显现的远期秘密由旧物主动开口，迫使主角重新解释此前一段历史
状态残留：远期秘密已公开；该 State 不能替代现场显现
排程边界：第20章
读者证明锚点：远期秘密；旧物开口
"""
    book = BOOK.replace(
        "## 2. 世界观结构",
        future_registry + "\n## 2. 世界观结构",
        1,
    )
    primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content=book,
        chapter_number=1,
        current_outline=MISSION,
        current_chapter_plan=CHAPTER_PLAN,
    )
    curator = generate_prompt(
        mode="context_curator",
        template="",
        book_content=book,
        chapter_number=1,
        current_outline=MISSION,
        current_chapter_plan=CHAPTER_PLAN,
    )
    for prompt in (primary, curator):
        assert "界签首次显现" in prompt
        assert "远期秘密" not in prompt
        assert "旧物开口" not in prompt


def test_story_program_protected_event_registry_is_deliberately_small() -> None:
    blocks = []
    for index in range(1, 6):
        blocks.append(
            f"""### RSE-{index:02d}\n事件原子：事件{index}现场发生\n状态残留：状态{index}\n排程边界：第{index}章\n读者证明锚点：锚点{index}"""
        )
    oversized = PROGRAM_REGISTRY_HEADING + "\n" + "\n\n".join(blocks)
    with pytest.raises(ValueError, match="最多保护 4 个"):
        parse_story_program_protected_events(oversized)


def test_story_event_registry_rejects_unparsed_continuation_instead_of_truncating() -> None:
    malformed = STORY_PROGRAM.replace(
        "事件原子：旧灼痕上的界签首次显现 → 北燧城被明确标记为第一副本 → 十二日期限与落日隧道合法归门同时进入裴骁认知 → 只有本地真实取得且确认归属的成果可携带离开",
        "事件原子：旧灼痕上的界签首次显现 → 北燧城被明确标记为第一副本\n→ 十二日期限与落日隧道合法归门同时进入裴骁认知",
    )
    with pytest.raises(ValueError, match="不允许静默丢字段或续行"):
        parse_story_program_protected_events(malformed)


def test_future10_rejects_duplicate_story_event_fields_in_one_chapter() -> None:
    duplicated = CHAPTER_PLAN + "\n不可降格 Story Event：RSE-02"
    with pytest.raises(ValueError, match="只能有一行"):
        chapter_story_event_ids(duplicated)


def test_story_event_repair_preserves_semantics_without_phrase_locking_event_atom() -> None:
    packet = build_chapter_context(
        book_content=BOOK,
        current_outline=MISSION,
        current_chapter_plan=CHAPTER_PLAN,
        chapter_number=1,
    )
    authority_prompt = f"AUTHORITY\n\n{packet.chapter_mission}"
    missing = missing_story_events(authority_prompt, "# 正式正文\n裴骁进入灯阶1。")
    assert missing
    from story_mvp.story_event_obligations import build_protected_story_event_repair_prompt

    repair = build_protected_story_event_repair_prompt(
        authority_prompt,
        "# 正式正文\n裴骁进入灯阶1。",
        missing,
    )
    assert "Event Atom 要保真其事实与因果，不要求逐字复现原句" in repair
    assert "除 proof anchors 外" in repair


def test_story_event_repair_keeps_only_one_current_prose_draft() -> None:
    packet = build_chapter_context(
        book_content=BOOK,
        current_outline=MISSION,
        current_chapter_plan=CHAPTER_PLAN,
        chapter_number=1,
    )
    authority = (
        "AUTHORITY\n\n"
        + packet.chapter_mission
        + "\n\n## PRIMARY DRAFT｜唯一待修订正文底稿\n\nOLD PRIMARY UNIQUE"
    )
    current = "# 正式正文\nCURRENT REVISION UNIQUE"
    missing = missing_story_events(authority, current)
    assert missing
    from story_mvp.story_event_obligations import build_protected_story_event_repair_prompt

    repair = build_protected_story_event_repair_prompt(authority, current, missing)
    assert "OLD PRIMARY UNIQUE" not in repair
    assert repair.count("CURRENT REVISION UNIQUE") == 1
    assert repair.count("CURRENT AUTHORITY REVISION｜唯一待修订正文底稿") == 1
