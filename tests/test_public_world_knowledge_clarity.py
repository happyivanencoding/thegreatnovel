from __future__ import annotations

from story_mvp.chapter_context import (
    extract_reader_release_for_chapter,
    project_current_opportunity_authority,
)
from story_mvp.character_prompts import PROTAGONIST_BLIND_WORLD_TEMPLATE
from story_mvp.prompts import (
    DEFAULT_DIRECTOR_TEMPLATE,
    DEFAULT_PROMPT_TEMPLATES,
    DIRECTOR_PLAN_COMPRESSION_RECOVERY,
    generate_prompt,
    OPENING_THREE_CHAPTER_CONTRACT,
    OUTLINE_TEMPLATE,
    PUBLIC_WORLD_KNOWLEDGE_CLARITY,
    READER_FIRST_PROSE_CONTRACT,
)


def test_world_vision_explicitly_separates_public_clarity_from_mystery() -> None:
    assert "Public World Knowledge = Clarity" in PUBLIC_WORLD_KNOWLEDGE_CLARITY
    assert "Unknown World = Mystery" in PUBLIC_WORLD_KNOWLEDGE_CLARITY
    assert "环境细节、人物动作、隐喻或专名只负责让画面活，不能代替基础答案" in PUBLIC_WORLD_KNOWLEDGE_CLARITY
    assert "不要求先等 Action 提问" in PUBLIC_WORLD_KNOWLEDGE_CLARITY
    assert "PUBLIC_WORLD_KNOWLEDGE_CLARITY" not in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "Public World Knowledge = Clarity" in PROTAGONIST_BLIND_WORLD_TEMPLATE
    assert "未来 reveal" in PROTAGONIST_BLIND_WORLD_TEMPLATE


def test_outline_schedules_an_opening_public_common_knowledge_bundle() -> None:
    assert "明显陌生/架空世界的第1章是公共常识定向的例外" in OUTLINE_TEMPLATE
    assert "默认把其中不同功能的事实拆成 2—3 条 `公共常识` Reader Release" in OUTLINE_TEMPLATE
    assert "不是把“力量 + 生活 + 社会上升”全压成一条" in OUTLINE_TEMPLATE
    assert "力量/当前与下一档 ruler" in OUTLINE_TEMPLATE
    assert "能做什么 + 在社会上通常意味着什么/能获得什么位置" in OUTLINE_TEMPLATE
    assert "为什么值得争、成功参与通常能打开什么" in OUTLINE_TEMPLATE
    assert "通用的“以后会有更大机会 / 可以去宗门军府”不能代替眼前这个具名机会" in OUTLINE_TEMPLATE
    assert "当 Story Program / Approved World 已经**具名**一个试场、选拔、招募" in OUTLINE_TEMPLATE
    assert "不能把上游的“某商盟公开试场 / 某宗门招募 / 某份契约”降成“公开机会 / 一个资格 / 更大的机会”" in OUTLINE_TEMPLATE
    assert "具名机会 + 当前已知价值" in OUTLINE_TEMPLATE
    assert "只写“某试场前训练 / 争取公开机会”仍算信息丢失" in OUTLINE_TEMPLATE
    assert "未来 reveal" in OUTLINE_TEMPLATE


def test_opening_contract_says_public_world_is_not_a_reading_comprehension_puzzle() -> None:
    assert "明显陌生/架空世界的前三章不是阅读理解题" in OPENING_THREE_CHAPTER_CONTRACT
    assert "主角大致在哪" in OPENING_THREE_CHAPTER_CONTRACT
    assert "哪些危险/生活习惯是大家的常识" in OPENING_THREE_CHAPTER_CONTRACT
    assert "不要求先靠火盆、服装、动作或对白让读者自己猜" in OPENING_THREE_CHAPTER_CONTRACT


def test_primary_and_reviser_require_direct_realization_not_environmental_inference() -> None:
    assert "开篇 Public Common Knowledge 不必先等动作提问" in READER_FIRST_PROSE_CONTRACT
    assert "仅靠环境细节、人物动作、专名、暗示" in READER_FIRST_PROSE_CONTRACT
    assert "不算已经说明" in READER_FIRST_PROSE_CONTRACT
    assert "本章若真实跨过前文已说明的公开力量/身份档位" in READER_FIRST_PROSE_CONTRACT
    assert "结果处直接命名新档位一次" in READER_FIRST_PROSE_CONTRACT

    reviser = DEFAULT_PROMPT_TEMPLATES["authority_reviser"]
    assert "普通读者不用推理就能复述规则" in reviser
    assert "火盆、服装、动作、专名或氛围" in reviser
    assert "不算已经兑现" in reviser
    assert "该细节不能替代已排程的公共常识说明" in reviser


def test_director_recovers_named_opportunity_value_lost_by_chapter_plan_compression() -> None:
    assert "Future 10 的单章条目只是当前剧情块的压缩投影" in DIRECTOR_PLAN_COMPRESSION_RECOVERY
    assert "具体机会名 + 当前已知价值" in DIRECTOR_PLAN_COMPRESSION_RECOVERY
    assert "Long Block 补足 Chapter Plan 的压缩损失" in DIRECTOR_PLAN_COMPRESSION_RECOVERY
    assert "不能改变章事件、提前宣布结果或从未来章偷新事实" in DIRECTOR_PLAN_COMPRESSION_RECOVERY
    assert DIRECTOR_PLAN_COMPRESSION_RECOVERY in DEFAULT_DIRECTOR_TEMPLATE

    long_block = """## 第1—4章：一镇两份日子
- 客舍当天要交付商队账目，武馆又安排公开试场前的最后训练。
- 铜羽商盟公开试场成为他的现实选择：赢得名次，通常可以取得随队护送契约、预付款和离开本镇的机会。顾临川连续使用分影。
- 正式试场前，疲惫令他的影形险些失稳。
"""
    chapter_plan = """## 第1章：一影分成两边
具体剧情：父亲要求顾临川完成商队账目；武馆安排公开试场前训练。
"""
    recovered = project_current_opportunity_authority(long_block, chapter_plan)
    assert recovered == "铜羽商盟公开试场成为他的现实选择：赢得名次，通常可以取得随队护送契约、预付款和离开本镇的机会。"

    prompt = generate_prompt(
        mode="director",
        template="",
        book_content="# 小说总体设计画像\n# 当前状态、未兑现承诺与作者备注\n",
        current_long_block=long_block,
        current_chapter_plan=chapter_plan,
        chapter_number=1,
    )
    assert "当前具名机会权威（从当前剧情块确定性恢复；不是新事实）" in prompt
    assert recovered in prompt


def test_director_opportunity_projection_stays_empty_without_matching_chapter_trigger() -> None:
    long_block = "铜羽商盟公开试场：赢得名次通常可以取得随队护送契约和预付款。"
    chapter_plan = "顾临川在客舍整理旧账，与父亲争论是否离开本镇。"
    assert project_current_opportunity_authority(long_block, chapter_plan) == ""


def test_reader_release_map_keeps_multiple_public_common_knowledge_lines_for_chapter_one() -> None:
    book = """# 小说总体设计画像

## 2. 世界观结构

### Reader Release Map
- 第1章｜公共常识：这个世界的人通过影子修炼；一阶能凝出基础影刃。
- 第1章｜公共常识：二阶可以正式担任商队护卫；顾临川目前还没有站稳一阶。
- 第1章｜公共常识：夺影兽会利用人的影子贴近，因此聚落夜里依赖稳定灯火与完整阴影。
- 第2章｜触发：铜羽商盟是跨城商盟，公开试场是地方武馆进入商队体系的入口。

## 3. 世界如何持续制造剧情压力
略。
"""
    chapter_one = extract_reader_release_for_chapter(book, 1)
    assert chapter_one.count("第1章") == 3
    assert "影子修炼" in chapter_one
    assert "二阶可以正式担任商队护卫" in chapter_one
    assert "夺影兽" in chapter_one
    assert "第2章" not in chapter_one
