from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from story_mvp.app import app
from story_mvp.chapter_context import build_chapter_context, extract_reader_release_for_chapter
from story_mvp.hybrid_runtime import (
    build_specialist_context,
    extract_specialist_patches,
    extract_unresolved_fact_boundary,
)
from story_mvp.prompts import (
    DEFAULT_PROMPT_TEMPLATES,
    DEFAULT_STATE_DELTA_TEMPLATE,
    REQUIRED_OUTLINE_FIELDS,
    READER_FIRST_PROSE_CONTRACT,
    READER_FIRST_PROSE_SHORT,
    generate_prompt,
    parse_canon_memory,
    parse_state_delta_v2,
    render_canon_memory,
)
from story_mvp.gbrain_retrieval import genre_prior_matches_query, is_genre_prior_page, retrieve_gbrain
from story_mvp.scene_skills import parse_scene_skill_selection, render_selected_scene_skills
from story_mvp.run_ledger import (
    create_or_load_run,
    load_run,
    mark_node_failed,
    next_actionable_node,
    retry_node,
    save_node_prompt,
    save_node_response,
    skip_integrator_if_no_patches,
)
from story_mvp.storage import apply_state_delta_to_book, save_chapter, validate_chapter_body_for_save


def test_curator_gets_frozen_human_core_without_repeating_power_core() -> None:
    character = """# CHARACTER CARD 1｜Split Authority

## POWER CORE｜Frozen Authority

POWER_ONLY_MARKER

## HUMAN CORE｜Frozen Authority

# HUMAN SEED｜真实嵌套结构

## 持续牵引与互相竞争的动机

他会被具体人的身体、气味和靠近感吸引，也在意自己的钱与被有分量的人看见。

## Behavior Signature

不把安全与责任永远放在第一。

## Composition Boundary

不做后验合理化。
"""
    prompt = generate_prompt(
        mode="context_curator",
        template="",
        book_content="# 小说总体设计画像\n\n## 1. 核心类型与读者承诺\n\n成长",
        character_card=character,
        current_outline=OUTLINE,
    )
    assert "FROZEN HUMAN CORE——稳定人格权威" in prompt
    assert "身体、气味和靠近感" in prompt
    assert "POWER_ONLY_MARKER" not in prompt


def test_prompt_api_preserves_character_card_for_chapter_curator() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/prompt",
        json={
            "mode": "context_curator",
            "template": "",
            "book_content": "# 小说总体设计画像\n\n## 1. 核心类型与读者承诺\n\n成长",
            "character_card": (
                "# CHARACTER CARD 1｜Split Authority\n\n"
                "## POWER CORE｜Frozen Authority\n\nPOWER_API_ONLY\n\n"
                "## HUMAN CORE｜Frozen Authority\n\n# HUMAN SEED｜API\n\n## 持续牵引与互相竞争的动机\n\nHUMAN_API_PRIVATE_DESIRE\n\n## Behavior Signature\n\nHUMAN_API_BEHAVIOR\n\n"
                "## Composition Boundary\n\nEND"
            ),
            "current_outline": OUTLINE,
        },
    )
    assert response.status_code == 200
    prompt = response.json()["prompt"]
    assert "HUMAN_API_PRIVATE_DESIRE" in prompt
    assert "POWER_API_ONLY" not in prompt


OUTLINE = "\n".join(
    f"{field}：内容"
    for field in (
        "触发事件",
        "推动事件的人",
        "主角行动",
        "对手或世界反应",
        "直接结果",
        "状态变化",
        "叙事功能",
        "结尾推动力",
    )
)


def test_reader_first_contract_and_curator_sections_are_scoped() -> None:
    curator = generate_prompt(
        mode="context_curator",
        template="",
        book_content="# 小说总体设计画像\n\n## 7. 叙事结构\n贴近主角",
        current_outline=OUTLINE,
    )
    for heading in (
        "## Reader-Facing Language",
        "## Already Established — Do Not Re-explain",
        "## Recent Repetition Risks",
        "## Payoff and Promise Window",
    ):
        assert heading in curator

    # The explicit fixed-output list must contain every required section.  A prior
    # contract listed only the first nine headings while defining four more later,
    # which made otherwise valid Curators stop early after Relevant Inspiration.
    fixed_output_contract = curator.split("`## Scene Prose Projection`", 1)[0]
    for heading in (
        "## Relevant Book Contract",
        "## Relevant Characters and Relationships",
        "## Relevant World Rules",
        "## Relevant Open Promises",
        "## Relevant Plan",
        "## Scene Prose Projection",
        "## Opening Strategy",
        "## Scene Skill Selection",
        "## Relevant Inspiration",
        "## Reader-Facing Language",
        "## Already Established — Do Not Re-explain",
        "## Recent Repetition Risks",
        "## Payoff and Promise Window",
    ):
        assert heading in fixed_output_contract

    assert "Reader-First Prose Contract" not in curator
    for marker in (
        "当前最在意的事",
        "自尊/恐惧/欲望",
        "行为习惯或说话声音",
        "不要生成 Character Card",
    ):
        assert marker in curator
    assert "单 Writer 职责" not in curator
    assert "## Character Card" not in curator
    for marker in (
        "关系阶段、状态变化、社会评价、收益结算等抽象内容属于 Writer 的内部理解",
        "不能直接复制总结",
        "Curator 不必自行把这些内容改写成正文句子",
        "操作步骤重新列成 Writer 必须演示的场景说明",
        "具体性优先落在谁想得到什么、谁在阻止",
        "不在 `## Relevant Plan` 中原样回显",
        "1—3 个可感知锚点",
        "人物差异化反应",
        "不为凑丰富度罗列五感",
        "不要替 Writer 预写修辞句",
    ):
        assert marker in curator

    primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="",
        current_outline=OUTLINE,
        curated_context="# Curated Chapter Context\n\n## Reader-Facing Language\n动作优先",
    )
    assert primary.count(READER_FIRST_PROSE_CONTRACT) == 1
    for marker in (
        "清楚 > 顺畅 > 有画面 > 文学感",
        "普通中文男频网文读者",
        "明确写人物、对象、动作、原因和结果",
        "绝对禁令｜“漂亮二段论”不得重复成章法",
        "事实已经成立 → 短句总结 → 再解释这意味着什么",
        "一章一旦已经自然出现一处明显的这种收束",
        "后文绝对不要再主动制造第二处同构收束",
        "已经 show 出来的东西，不再为了“漂亮”补一个 tell 的尾巴",
        "重要能力、物品和规则第一次出现时",
        "少连续使用“不是……”",
        "对话有呼吸，不是每个人都用一句话完成一个剧情功能",
        "有限 POV 要帮助读者理解局势",
        "观察 → 判断/猜测 → 必要时发现自己判断不全 → 决定",
        "世界观和空间信息只解释当前故事与开篇定向需要的最小部分",
        "公共常识要直接讲清",
        "复杂场景先建立 Stable Scene Geography，再让人物移动",
        "Action Advance ≠ Situation Memory",
        "不要只摆出火盆、服装、站位、专名或异常现象让读者自己推",
        "动态成长因果不随之衰减",
        "Tell clearly → Show repeatedly → Tell the new delta",
        "关键后果的前提要在不可逆选择之前建立",
        "简单不等于空泛",
        "当前读者主问题",
        "具名的重要物品一旦明确换了持有人或位置",
        "关键因果节点",
        "第一息 / 第二息 / 第三息",
        "新章不要原样或近似复述上一章最后一句",
        "朴素、直接不等于情绪中性",
        "人物不是状态更新器",
        "有反应后选择压住",
        "重大胜利、失败、羞辱、翻盘",
        "不必每句高效",
        "核心欲望、自尊、恐惧或期待",
        "不要只用疼痛、战术判断、看一眼或状态确认代替它",
        "Active Interior Continuity",
        "重要配角带着自己的人生进入现场，不只带着任务",
        "Living Power Ecology 要在正文里真正约束行为",
        "一个明显高阶人物在场却不介入",
        "Planning → Prose 边界",
        "验证、闭环、阶段推进、价值兑现、成长空间、建立优势",
        "不要把后台标签原样扩写成作者总结",
        "动作、对白或结果已经成立后，不再追加同义的抽象解释",
        "Story-bearing Texture：丰富不是修饰堆积",
        "正文的丰富感优先来自承载故事的具体细节",
        "力量造成的可见后果",
        "不机械覆盖视觉、听觉、嗅觉、触觉",
        "不要为了“写得丰富”延长章节",
        "长期历史未知边界",
        "仍然是**未知**",
        "事实上限",
        "只授权地点，就不能顺手补身份、原因或机制",
        "对白不是补 Canon 的逃生口",
        "足以被 State Extraction 写进 Persistent Canon 的新陈述",
        "后续张力优先转向信不信、去不去、跟不跟、交不交、谁承担什么",
        "把合理猜测扩写成几十 / 几百章前已经发生过的秘密经历",
        "本章当下的动作、对白措辞、即时感官、现场证据与人物暂时判断",
        "后台章节编号和 pipeline 距离也不属于人物世界",
    ):
        assert marker in primary
    assert primary.count("人物不是状态更新器") == 1
    specialist = generate_prompt(
        mode="specialist_action",
        template="",
        book_content="",
        current_outline=OUTLINE,
        primary_draft="正文底稿",
    )
    assert specialist.count(READER_FIRST_PROSE_CONTRACT) == 0
    assert specialist.count(READER_FIRST_PROSE_SHORT) == 1
    assert "验证、闭环、阶段推进、价值兑现、成长空间、建立优势" in specialist


def test_unresolved_fact_boundary_is_deterministic_and_primary_visible() -> None:
    curated = """# Curator Audit

- 当前地点未确认；不要默认已进入塔内。

# Curated Chapter Context

## Relevant World Rules

- 已知规则：门会打开。
- 第三盏灯与玉牌的关系尚未解释；不要补造规则。

## Relevant Open Promises

- 宁青梧为何回来仍未解决。
- 点灯者身份未知。

## Payoff and Promise Window

- 已到账：玉牌。
- 仍未兑现：第三盏灯机制。
"""
    boundary = extract_unresolved_fact_boundary(curated)
    assert "当前地点未确认" in boundary
    assert "宁青梧为何回来仍未解决" in boundary
    assert "点灯者身份未知" in boundary
    assert "第三盏灯与玉牌的关系尚未解释" in boundary
    assert "仍未兑现：第三盏灯机制" in boundary
    assert "已知规则：门会打开" not in boundary
    assert "已到账：玉牌" not in boundary

    primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="",
        current_outline=OUTLINE,
        curated_context=curated,
    )
    marker = "UNRESOLVED FACT BOUNDARY——仍未知/未兑现，不得由 Writer 补成旧史"
    assert marker in primary
    assert primary.index(marker) < primary.index("CANON PROSE——上一章全文与上上章必要章末")
    assert "宁青梧为何回来仍未解决" in primary
    assert "第三盏灯与玉牌的关系尚未解释" in primary


def test_supporting_logic_does_not_become_story_engine() -> None:
    markers = (
        "支撑性逻辑不得自动成为故事发动机",
        "不自动成为叙事前景、主角职业、长期职责或作品认可的公共答案",
        "不从力量规模自动推出",
        "能力可信性优先在有真实目标和利害关系的行动中证明",
        "观察、分析、测试、验证、调整和实施",
        "不因能力可重复使用就自然职业化成维护、检测、生产、搬运或运营流程",
    )
    for mode in ("world_vision", "outline", "review"):
        for marker in markers:
            assert marker in DEFAULT_PROMPT_TEMPLATES[mode]

    idea = DEFAULT_PROMPT_TEMPLATES["idea"]
    assert "支撑性逻辑不得自动成为故事发动机" in idea
    assert "职业流程、材料处理、宗门行政、运输、诊断、修复、合同、任务分配" in idea
    assert "除非人物的关键选择真的发生在那里，否则压到背景" in idea
    assert "世界仍然大于外挂" in idea

    fantasy_seed = DEFAULT_PROMPT_TEMPLATES["fantasy_seed"]
    assert "Seed Supporting Logic Boundary" in fantasy_seed
    assert "不负责把可信性问题完整解决" in fantasy_seed
    assert "检测、维护、运输、生产、运营或其它职业流程" in fantasy_seed

    director = generate_prompt(
        mode="director",
        template="",
        book_content="",
        current_outline=OUTLINE,
    )
    for marker in markers:
        assert marker in director


def test_fantasy_salience_rules_are_scoped_to_planning_layers() -> None:
    shared_markers = (
        "核心幻想不变量",
        "幻想复利优先于操作流程复利",
        "Plot Engine Diversity",
        "经营文 Decision > Implementation",
    )
    for mode in ("outline", "review"):
        for marker in shared_markers:
            assert marker in DEFAULT_PROMPT_TEMPLATES[mode]

    idea = DEFAULT_PROMPT_TEMPLATES["idea"]
    assert "核心幻想也必须在多个自然阶段反复得到有分量、可观察的兑现" in idea
    assert "纵向复利是历史持续生效，不是阶段流水线" in idea
    assert "相邻阶段避免长期退化为" in idea
    assert "支撑性逻辑不得自动成为故事发动机" in idea

    for mode in ("outline", "review"):
        assert "Outline Fantasy Proof" in DEFAULT_PROMPT_TEMPLATES[mode]

    assert "经营文 Decision > Implementation" in DEFAULT_PROMPT_TEMPLATES["world_vision"]
    assert "经营文 Decision > Implementation" not in DEFAULT_PROMPT_TEMPLATES["fantasy_seed"]
    assert "Seed Long-form Compounding" in DEFAULT_PROMPT_TEMPLATES["fantasy_seed"]
    assert "Seed Long-form Pacing" in DEFAULT_PROMPT_TEMPLATES["fantasy_seed"]

    director = generate_prompt(
        mode="director",
        template="",
        book_content=(
            "# 小说总体设计画像\n"
            "## 0. 本书成长基因图\n"
            "### 已批准幻想不变量\n"
            "FANTASY_INVARIANT_MARKER\n"
            "### 核心不变量\n"
            "持续让主角获得超凡主动权"
        ),
        current_outline=OUTLINE,
    )
    assert "FANTASY_INVARIANT_MARKER" in director
    assert "核心幻想不变量" in director
    assert "Director Narrative Salience" in director
    assert "经营文 Decision > Implementation" in director
    assert "Plot Engine Diversity" not in director

    primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="",
        current_outline=OUTLINE,
        curated_context="# Curated Chapter Context\n\n## Relevant Plan\n只保留本章事实",
    )
    for marker in (
        "核心幻想不变量",
        "幻想复利优先于操作流程复利",
        "Outline Fantasy Proof",
        "Plot Engine Diversity",
        "Director Narrative Salience",
        "经营文 Decision > Implementation",
    ):
        assert marker not in primary


def test_scene_skill_runtime_is_curator_selected_and_primary_only() -> None:
    curator = generate_prompt(
        mode="context_curator",
        template="",
        book_content="",
        current_outline=OUTLINE,
    )
    assert "## Scene Skill Selection" in curator
    assert "SCENE SKILL CATALOG" in curator
    assert "- trial_challenge:" in curator
    assert "- combat:" in curator
    for skill_id in ("identity_reveal", "departure_vacancy", "sacrifice_convergence", "reunion_reentry"):
        assert f"- {skill_id}:" in curator
    assert "Projection Guidance:" in curator
    assert "trial_challenge" in curator

    curated = """# Curated Chapter Context

## Scene Skill Selection
Primary: trial_challenge
Secondary: combat

## Reader-Facing Language
动作优先
"""
    assert parse_scene_skill_selection(curated) == ("trial_challenge", "combat")
    active = render_selected_scene_skills(curated)
    assert "## Primary: trial_challenge" in active
    assert "## Secondary: combat" in active
    assert "只在其关键 beat 上提高细节密度" in active
    assert "不把整章都提高修饰密度" in active
    assert "# investigation" not in active

    primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="",
        current_outline=OUTLINE,
        curated_context=curated,
    )
    assert "ACTIVE SCENE SKILLS——只控制场景如何落成正文" not in primary
    assert "## Primary: trial_challenge" not in primary
    assert "## Secondary: combat" not in primary
    assert "# investigation" not in primary
    assert "## Scene Skill Selection" not in primary

    invalid_primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="",
        current_outline=OUTLINE,
        curated_context="# Curated Chapter Context\n\n## Scene Skill Selection\nPrimary: unknown_skill\nSecondary: combat",
    )
    assert "ACTIVE SCENE SKILLS——只控制场景如何落成正文" not in invalid_primary
    assert "unknown_skill" not in invalid_primary

    specialist = generate_prompt(
        mode="specialist_action",
        template="",
        book_content="",
        current_outline=OUTLINE,
        curated_context=curated,
        primary_draft="正文底稿",
    )
    assert "ACTIVE SCENE SKILLS——只控制场景如何落成正文" not in specialist
    assert "## Primary: trial_challenge" not in specialist


def test_scene_skill_v2_catalog_projects_guidance_and_reviser_only_gets_short_watch() -> None:
    curator_prompt = generate_prompt(
        mode="context_curator",
        template="",
        book_content="",
        current_outline=OUTLINE,
    )
    assert "Projection Guidance:" in curator_prompt
    assert "胜负尺" in curator_prompt
    assert "## Generation Lens" not in curator_prompt
    assert "## Revision Lens" not in curator_prompt

    curated = """# Curated Chapter Context

## Scene Prose Projection
只让这一轮对白改变一个真实条件；条件成立后停。

## Scene Skill Selection
Primary: social_bargain_decision
Secondary: relationship

## Reader-Facing Language
直接写人。
"""
    primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="",
        current_outline=OUTLINE,
        curated_context=curated,
    )
    assert "只让这一轮对白改变一个真实条件" in primary
    assert "## Generation Lens" not in primary
    assert "Revision Watch" not in primary

    reviser = generate_prompt(
        mode="authority_reviser",
        template="",
        book_content="",
        current_outline=OUTLINE,
        curator_response=curated,
        primary_draft="# 正式正文\n\n原稿。",
    )
    assert "ACTIVE SCENE REVISION WATCH" in reviser
    assert "social_bargain_decision" in reviser
    assert "relationship" in reviser
    assert "连续对白无结算" in reviser
    assert "单方付出被写成双向确认" in reviser
    assert "## Generation Lens" not in reviser
    assert "## Revision Lens" not in reviser


def test_opening_contract_is_scoped_to_planning_and_opening_nodes() -> None:
    primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="",
        current_outline=OUTLINE,
        current_chapter_plan="当前章计划",
        chapter_number=3,
    )
    opening = generate_prompt(
        mode="specialist_opening",
        template="",
        book_content="",
        current_outline=OUTLINE,
        primary_draft="正文底稿",
        chapter_number=3,
    )
    assert primary.count("# Opening Three Chapter Contract") == 1
    assert "World fact 的选择权在 World + Outline" in primary
    assert opening.count("# Opening Three Chapter Contract") == 1

    for mode in (
        "context_curator",
        "specialist_dialogue",
        "specialist_action",
        "specialist_emotion",
    ):
        prompt = generate_prompt(
            mode=mode,
            template="",
            book_content="",
            current_outline=OUTLINE,
            primary_draft="正文底稿" if mode != "context_curator" else "",
            chapter_number=3,
        )
        assert "# Opening Three Chapter Contract" not in prompt

    integrator = generate_prompt(
        mode="chapter_integrator",
        template="",
        book_content="",
        current_outline=OUTLINE,
        primary_draft="正文底稿",
        chapter_number=3,
    )
    assert "# Opening Three Chapter Contract" not in integrator


def test_specialist_patch_projection_excludes_audit_and_context_is_cropped() -> None:
    response = "# Specialist Audit\nSECRET_AUDIT\n# Proposed Patches\n## Patch 1\n目标锚点：开头\n操作：replace\n建议文本：保留动作。"
    assert "SECRET_AUDIT" not in extract_specialist_patches(response)
    assert "## Patch 1" in extract_specialist_patches(response)

    packet = build_chapter_context(
        book_content="# 小说总体设计画像\n## 0. 本书成长基因图\n### 核心不变量\n持续行动\n## 1. 核心类型与读者承诺\n成长",
        current_outline=OUTLINE,
        current_chapter_plan="## 第2章：当前条目\nCURRENT_CHAPTER_PLAN",
        current_long_block="CURRENT_BLOCK",
    )
    primary = "\n\n".join([f"前部{i}" + ("x" * 400) for i in range(8)]) + "\n\nTAIL_MARKER"
    opening = build_specialist_context(packet, "# Curated Chapter Context", primary, "opening")
    assert len(opening.primary_draft) <= 1800
    assert "CURRENT_CHAPTER_PLAN" in packet.chapter_plan_context
    assert packet.current_long_block == "CURRENT_BLOCK"


def test_director_prompt_uses_only_light_projection_and_selective_default() -> None:
    prompt = generate_prompt(
        mode="director",
        template="",
        book_content="# 小说总体设计画像\n## 0. 本书成长基因图\n### 核心不变量\nGENOME",
        current_long_block="CURRENT_BLOCK",
        current_chapter_plan="CURRENT_CHAPTER_PLAN",
        previous_chapter_text="PREVIOUS_TAIL",
        recent_summaries="RECENT_SUMMARY",
        creative_direction="AUTHOR_INTENT",
    )
    for marker in ("CURRENT_BLOCK", "CURRENT_CHAPTER_PLAN", "GENOME", "PREVIOUS_TAIL", "RECENT_SUMMARY", "AUTHOR_INTENT"):
        assert marker in prompt
    assert "writer_mode" not in prompt
    assert "专项建议" in prompt
    director_contract = prompt.split("# Director Context", 1)[0]
    for field in REQUIRED_OUTLINE_FIELDS:
        assert f"{field}：" in director_contract
    assert "八个字段仍是唯一事件合同字段" in director_contract
    assert "情绪字段：" not in director_contract
    for marker in (
        "长期旧线本章新事实具体化",
        "哪一个具体事实第一次成为确定事实",
        "仍未解决",
        "不要只写“至少一条旧线发生不可逆变化”",
        "不为填满事件合同补造几十 / 几百章前发生过的秘密经历",
    ):
        assert marker in director_contract

    hybrid = generate_prompt(
        mode="context_curator",
        template="",
        book_content="",
        current_outline=OUTLINE,
    )
    assert "writer_mode: hybrid_selective" in hybrid


def test_canon_memory_v2_and_state_delta_parser() -> None:
    status = """当前已完成第3章。

## ACTIVE SCENE STATE
废井；沈砚在场；左臂受伤。

## PERSISTENT CANON
砾角能在湿壁上短暂借力；关系阶段：容忍同行。
### Active Relationships
沈禾｜寻找失踪弟弟｜与主角暂时合作｜主角救过她一次｜答应提供旧矿图
### Tracked Assets
黑炉钥匙｜沈砚｜废井腰包｜可开旧炉门｜刚从主角转交

## RECENT SUMMARIES
第3章：主角打开闸门。

## OPEN PROMISES
沈禾的去向。

## AUTHOR NOTES
逐字保留这句。"""
    fields = parse_canon_memory(status)
    assert fields["active_scene_state"].startswith("废井")
    assert "短暂借力" in fields["persistent_canon"]
    assert "Active Relationships" in fields["persistent_canon"]
    assert "Tracked Assets" in fields["persistent_canon"]
    assert fields["author_notes"] == "逐字保留这句。"
    rendered = render_canon_memory(fields)
    assert "## ACTIVE SCENE STATE" in rendered
    assert "## PERSISTENT CANON" in rendered
    assert "沈禾｜寻找失踪弟弟" in rendered
    assert "黑炉钥匙｜沈砚" in rendered
    assert "当前主动目标" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "### Active Relationships" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "当前 Growth State" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "没有正文直接证据就不要推理" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "### Tracked Assets" in DEFAULT_STATE_DELTA_TEMPLATE

    proposal = parse_state_delta_v2(
        """# State Delta Audit
无。

# Proposed Active Scene State
新地点；无追兵。

# Proposed Persistent Canon
能力限制仍为短暂借力。

# Proposed Chapter Summary
主角拿到一枚钥匙。

# Proposed Open Promises
钥匙来自谁。"""
    )
    assert proposal["chapter_summary"] == "主角拿到一枚钥匙。"
    assert "# Proposed Canon Index" not in DEFAULT_STATE_DELTA_TEMPLATE

    updated = apply_state_delta_to_book(
        """# 小说总体设计画像
内容

# 当前状态、未兑现承诺与作者备注
当前已完成第0章。

## ACTIVE SCENE STATE
旧场景

## PERSISTENT CANON
### Power / Capability
Current Power Position｜主尺：测试阶｜精确位置：3级
旧长期事实

## RECENT SUMMARIES
当前尚无已完成正文或已批准章节摘要。

## OPEN PROMISES
旧承诺

## AUTHOR NOTES
作者原话。""",
        1,
        """# State Delta Audit
无。
# Proposed Active Scene State
新场景
# Proposed Persistent Canon
新能力限制
### Active Relationships
沈禾｜寻找弟弟｜暂时合作｜主角救援｜提供旧矿图
### Tracked Assets
黑炉钥匙｜沈禾｜回收册｜已转交｜刚从主角转出
# Proposed Chapter Summary
第一章事实
# Proposed Open Promises
新承诺""",
    )
    assert "当前已完成第1章。" in updated
    assert "第1章：第一章事实" in updated
    assert "作者原话。" in updated
    assert "沈禾｜寻找弟弟" in updated
    assert "黑炉钥匙｜沈禾" in updated
    assert "旧场景" not in updated

    preserved_prefix = """# 小说总体设计画像
## 0. 本书成长基因图
必须逐字保留。

# 当前中期规划窗口
PLAN

# 未来十章逐章小纲
FUTURE
"""
    source = preserved_prefix + "\n# 当前状态、未兑现承诺与作者备注\n\n## ACTIVE SCENE STATE\n旧\n"
    preserved = apply_state_delta_to_book(
        source,
        1,
        """# State Delta Audit
无。
# Proposed Active Scene State
新
# Proposed Persistent Canon
### Power / Capability
Current Power Position｜主尺：测试阶｜精确位置：1级
长期
# Proposed Chapter Summary
事实
# Proposed Open Promises
承诺""",
    )
    assert preserved.startswith(preserved_prefix.rstrip() + "\n\n# 当前状态、未兑现承诺与作者备注")
    assert "必须逐字保留。" in preserved

    prefixed = apply_state_delta_to_book(
        """# 小说总体设计画像
内容
# 当前状态、未兑现承诺与作者备注
## ACTIVE SCENE STATE
旧
## PERSISTENT CANON
### Power / Capability
Current Power Position｜主尺：测试阶｜精确位置：2级
旧
## RECENT SUMMARIES
旧
## OPEN PROMISES
旧
## AUTHOR NOTES
原话""",
        3,
        """# State Delta Audit
无。
# Proposed Active Scene State
新
# Proposed Persistent Canon
新
# Proposed Chapter Summary
第3章：已经发生。
# Proposed Open Promises
新""",
    )
    assert "第3章：第3章：" not in prefixed


def test_chapter_save_rejects_internal_sections_without_mutating_input(tmp_path: Path) -> None:
    body = "第一段正文。\n\n# Writer Audit\n不应保存。"
    try:
        validate_chapter_body_for_save(body)
    except ValueError as error:
        assert "Writer Audit" in str(error)
    else:
        raise AssertionError("internal chapter sections must be rejected")
    assert body.endswith("不应保存。")

    book_dir = tmp_path / "books" / "demo"
    (book_dir / "chapters").mkdir(parents=True)
    (book_dir / "BOOK.md").write_text("# book", encoding="utf-8")
    try:
        save_chapter("demo", 1, "---FACT_SUMMARY---\n摘要", tmp_path / "books")
    except ValueError as error:
        assert "FACT_SUMMARY" in str(error)
    else:
        raise AssertionError("fact summary must not be saved")
    assert not (book_dir / "chapters" / "chapter-0001.md").exists()


def test_run_ledger_retries_one_failed_node_and_keeps_upstream(tmp_path: Path) -> None:
    book_dir = tmp_path / "demo"
    (book_dir / "BOOK.md").parent.mkdir(parents=True)
    (book_dir / "BOOK.md").write_text("# book", encoding="utf-8")
    manifest = create_or_load_run(
        book_dir,
        1,
        writer_mode="hybrid_selective",
        selected_specialists=["opening"],
    )
    assert manifest["nodes"]["dialogue"]["status"] == "skipped"
    save_node_prompt(book_dir, 1, "director", "DIRECTOR_PROMPT")
    save_node_response(book_dir, 1, "director", "DIRECTOR_RESPONSE")
    save_node_prompt(book_dir, 1, "primary", "PRIMARY_PROMPT")
    save_node_response(book_dir, 1, "primary", "PRIMARY_RESPONSE")
    save_node_prompt(book_dir, 1, "opening", "OPENING_PROMPT")
    mark_node_failed(book_dir, 1, "opening")
    before = load_run(book_dir, 1)
    retried = retry_node(book_dir, 1, "opening")
    assert retried["nodes"]["opening"]["attempts"] == 2
    assert retried["nodes"]["director"]["status"] == "completed"
    assert retried["nodes"]["primary"]["status"] == "completed"
    save_node_response(book_dir, 1, "opening", "OPENING_RESPONSE")
    completed = load_run(book_dir, 1)
    assert completed["nodes"]["opening"]["response_file"].endswith("attempt-2.md")
    assert completed["nodes"]["integrator"]["status"] == "stale"
    assert next_actionable_node(book_dir, 1) == "curator"
    assert before["nodes"]["director"]["response_file"] == "director_response.md"
    skipped = skip_integrator_if_no_patches(book_dir, 1, {"opening": "# Proposed Patches\n无"})
    assert skipped["nodes"]["integrator"]["status"] == "skipped"


def test_genre_prior_is_capped_for_planning_and_excluded_from_chapter() -> None:
    genre = """---
creative_problem_tags:
- genre-prior
- idea
title: 题材先验｜玄幻修仙
---
## Reader Promise
题材先验内容。
## Failure Risks
风险。
"""
    mechanism = """---
creative_problem_tags:
- mechanism
---
## Mechanism
具体机制内容。
"""
    assert is_genre_prior_page(genre)
    pages = {
        "syntheses/genre-priors/a": genre,
        "syntheses/genre-priors/b": genre,
        "syntheses/genre-priors/c": genre,
        "mechanisms/concrete": mechanism,
    }
    raw = "\n".join(
        [
            "[0.99] syntheses/genre-priors/a -- prior",
            "[0.98] syntheses/genre-priors/b -- prior",
            "[0.97] syntheses/genre-priors/c -- prior",
            "[0.96] mechanisms/concrete -- mechanism",
        ]
    )
    idea = retrieve_gbrain(
        mode="idea", book_content="玄幻成长", query_override="玄幻修仙", query_func=lambda *_args, **_kwargs: raw, page_func=pages.__getitem__
    )
    assert idea["genre_prior_count"] == 2
    assert any(item["reason"] == "超过 Genre Prior 接受上限" for item in idea["rejected"])
    chapter = retrieve_gbrain(
        mode="chapter", book_content="玄幻成长", query_override="玄幻修仙", query_func=lambda *_args, **_kwargs: raw, page_func=pages.__getitem__
    )
    assert all(not item.get("is_genre_prior") for item in chapter["accepted"])
    assert any(item["reason"] == "章节节点不自动使用 Genre Prior" for item in chapter["rejected"])
    prompt = generate_prompt(
        mode="chapter",
        template="CHAPTER",
        book_content="",
        current_outline=OUTLINE,
        gbrain_inspiration="### Inspiration 1\nsource: syntheses/genre-priors/a\n可用抽象：题材先验",
    )
    assert "genre-priors/a" not in prompt
    assert not genre_prior_matches_query("---\ntitle: 题材先验｜宫斗宅斗\ncreative_problem_tags:\n- genre-prior\n---", "高武个人战斗", "syntheses/genre-priors/宫斗宅斗")


def test_run_ledger_api_persists_prompt_response_and_retry(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "ledger-api"}).status_code == 201
    created = client.post(
        "/api/books/ledger-api/runs/1",
        json={"writer_mode": "hybrid_selective", "selected_specialists": ["opening"]},
    )
    assert created.status_code == 200
    assert created.json()["nodes"]["dialogue"]["status"] == "skipped"
    prompt = client.put(
        "/api/books/ledger-api/runs/1/nodes/director/prompt",
        json={"content": "director prompt"},
    )
    assert prompt.status_code == 200
    response = client.put(
        "/api/books/ledger-api/runs/1/nodes/director/response",
        json={"content": "director response"},
    )
    assert response.status_code == 200
    loaded_response = client.get(
        "/api/books/ledger-api/runs/1/nodes/director/response"
    )
    assert loaded_response.status_code == 200
    assert loaded_response.json() == {"content": "director response"}
    failed = client.post("/api/books/ledger-api/runs/1/nodes/director/failed")
    assert failed.status_code == 200
    retried = client.post("/api/books/ledger-api/runs/1/nodes/director/retry")
    assert retried.status_code == 200
    assert retried.json()["nodes"]["director"]["attempts"] == 2
    assert (tmp_path / "ledger-api" / "runs" / "chapter-0001" / "director_prompt.md").is_file()

def test_approved_world_is_first_class_curator_authority_and_plan_schedules_release() -> None:
    world = """# PROTAGONIST-BLIND WORLD VISION

## 普通人的生活与上升
普通人住在猎墙内，离城通常跟随商队或猎队。

## 力量体系与正常值
一阶是正式猎手，二阶能独自处理大型异兽。

## 社会现实与身份
荒原部族有独立训练法，也会与城镇交易或冲突。

## 世界里真正值钱、值得想要的东西
高阶心核很值钱。

## 世界正在发生的大事
白角部正在追一头被掳走的幼年王种。

## 世界知识边界
普通人知道荒原部族存在，但不知道各部族当前目的。
当前没人能完整解释的事实：白角部为何改变旧路线。
"""
    plan = "## 第4章：封路\n具体剧情：白角部第一次挡住商队去路；此处让读者知道：荒原部族有独立训练法，也会与城镇交易或冲突。"
    packet = build_chapter_context(
        book_content="# 小说总体设计画像\n## 1. 核心类型与读者承诺\n成长",
        world_vision=world,
        current_chapter_plan=plan,
    )
    assert "WORLD REALITY AUTHORITY" in packet.world_authority
    assert "荒原部族有独立训练法" in packet.world_authority
    assert "白角部正在追一头" not in packet.world_authority
    assert "当前没人能完整解释的事实" not in packet.world_authority

    from story_mvp.hybrid_runtime import build_curator_context

    curator = build_curator_context(packet)
    assert "WORLD AUTHORITY" in curator.context_index
    assert "荒原部族有独立训练法，也会与城镇交易或冲突" in curator.world_authority
    assert "高阶心核很值钱" not in curator.world_authority


def test_curator_prompt_receives_world_authority_without_api_side_channel() -> None:
    world = """# PROTAGONIST-BLIND WORLD VISION

## 普通人的生活与上升
普通人住在猎墙内，离城通常跟随商队或猎队。

## 力量体系与正常值
一阶是正式猎手。

## 社会现实与身份
荒原部族有独立训练法，也会与城镇交易或冲突。

## 世界里真正值钱、值得想要的东西
高阶心核很值钱。

## 世界知识边界
普通人知道荒原部族存在。
"""
    prompt = generate_prompt(
        mode="context_curator",
        template="",
        book_content="# 小说总体设计画像\n## 1. 核心类型与读者承诺\n成长",
        world_vision=world,
        current_outline=OUTLINE,
        current_chapter_plan="## 第4章：封路\n具体剧情：此处告诉读者荒原部族有独立训练法，也会与城镇交易或冲突。",
        chapter_number=4,
    )
    assert "WORLD AUTHORITY——本章确定性预取" in prompt
    assert "荒原部族有独立训练法，也会与城镇交易或冲突" in prompt
    assert "Optional Reader Orientation Reference" not in prompt

def test_reader_release_map_is_optional_and_chapter_scoped() -> None:
    book = """# 小说总体设计画像
## 2. 世界观结构
世界摘要。
### Reader Release Map
- 第1章｜猎市起乱：城镇外有猎墙，普通人首先学会避开异兽。
- 第4章｜白角部挡路：荒原部族拥有不同于宗门的身体训练与驯兽传统。
## 3. 世界如何持续制造剧情压力
压力。
# 当前中期规划窗口
块。
# 未来十章逐章小纲
计划。
# 当前状态、未兑现承诺与作者备注
状态。
"""
    assert "城镇外有猎墙" in extract_reader_release_for_chapter(book, 1)
    assert "荒原部族" not in extract_reader_release_for_chapter(book, 1)
    assert "荒原部族" in extract_reader_release_for_chapter(book, 4)
    assert extract_reader_release_for_chapter(book, 2) == ""


def test_authority_reviser_receives_remote_authority_without_raw_gbrain_and_preserves_fixed_contract() -> None:
    character = """# CHARACTER CARD 1｜Split Authority

## POWER CORE｜Frozen Authority

POWER_CORE_MARKER：可以把一个自己分成两个并行行动的身体。

## HUMAN CORE｜Frozen Authority

HUMAN_CORE_MARKER：会被具体人的气味、姿态和身体靠近牵动，也在意自由钱和被看见。

## Composition Boundary

不做后验合理化。
"""
    world = """# PROTAGONIST-BLIND WORLD VISION

## 普通人的生活与上升

WORLD_LIFE_MARKER：本地石屋沿山壁层叠，居民常穿窄袖短袍。

## 力量体系与正常值

WORLD_POWER_MARKER：影子可以炼成实体用于攻防。

## 世界里真正值钱、值得想要的东西

WORLD_VALUE_MARKER：古城遗物和珍稀药材价格很高。
"""
    book = """# 小说总体设计画像

## 2. 世界观结构

世界结构。

### Reader Release Map
- 第5章｜READER_RELEASE_A：观日宗公开传授影术。
- 第5章｜READER_RELEASE_B：古城遗物、珍稀药材和异兽让各方争抢。
"""
    prompt = generate_prompt(
        mode="authority_reviser",
        template="CUSTOM_TEMPLATE_MUST_NOT_OVERRIDE_FIXED_REVISER",
        writer_mode="curator_primary",
        book_content=book,
        world_vision=world,
        character_card=character,
        current_outline=OUTLINE,
        chapter_number=5,
        curator_response="CURATOR_ATTENTION_MARKER",
        primary_draft="# 正式正文\n\nPRIMARY_DRAFT_MARKER",
        previous_chapter_text="CANON_TAIL_MARKER",
        gbrain_inspiration="RAW_GBRAIN_MARKER",
    )
    assert "Preservation First" in prompt
    assert "CUSTOM_TEMPLATE_MUST_NOT_OVERRIDE_FIXED_REVISER" not in prompt
    assert "FROZEN CHAPTER MISSION" in prompt
    assert "CURATOR_ATTENTION_MARKER" in prompt
    assert "WORLD_LIFE_MARKER" in prompt
    assert "WORLD_POWER_MARKER" in prompt
    assert "WORLD_VALUE_MARKER" in prompt
    assert "READER_RELEASE_A" in prompt and "READER_RELEASE_B" in prompt
    assert "POWER_CORE_MARKER" in prompt
    assert "HUMAN_CORE_MARKER" in prompt
    assert "CANON_TAIL_MARKER" in prompt
    assert "PRIMARY_DRAFT_MARKER" in prompt
    assert "RAW_GBRAIN_MARKER" not in prompt
    assert "逐条检查" in prompt
    assert "地方风俗、建筑样式或制度不得" in prompt
    assert "State Change / Social Repricing / Reward / Relationship Change / New Desire / Next Opportunity" in prompt


def test_authority_reviser_requires_primary_draft() -> None:
    try:
        generate_prompt(
            mode="authority_reviser",
            template="",
            book_content="",
            current_outline=OUTLINE,
            chapter_number=5,
            primary_draft="",
            primary_writer_response="",
        )
    except ValueError as error:
        assert "Primary Draft" in str(error)
    else:
        raise AssertionError("Authority Reviser must require a Primary Draft")
