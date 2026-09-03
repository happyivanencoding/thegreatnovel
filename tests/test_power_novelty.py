from __future__ import annotations

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.power_novelty import build_power_lexique_bundle, build_power_novelty_bundle
from story_mvp.gbrain_retrieval import PLANNING_KEYWORD_QUERIES, PLANNING_KEYWORD_QUERY_BATCHES


WORLD = """# PROTAGONIST-BLIND WORLD VISION

## 力量体系与正常值
普通修士只能稳定维持一种主承载；御剑时很难同时施展另一套完整术式。
"""

STATE = {"world_vision": {"status": "author_approved"}}


def test_world_prompt_requires_reusable_social_power_rulers() -> None:
    prompt = generate_split_prompt(mode="world_vision", creative_direction="男频修仙")
    assert "力量尺必须能长期反复拿来比较" in prompt
    assert "精确力量主尺是强制 World Root Authority" in prompt
    assert "唯一精确当前位置" in prompt
    assert "主尺类型" in prompt
    assert "不要合成单一总战力分" in prompt
    assert "不是机械胜负公式，但也不能只是装饰数字" in prompt
    assert "不会被单一特殊机制凭空抹掉的**基础盘**" in prompt
    assert "不能因为废掉高阶者一招" in prompt
    assert "普通人怎样在聚落之间移动" in prompt
    assert "谁有能力跨越危险区域" in prompt
    assert "公开类别" in prompt
    assert "不把当前行动目的、隐藏关系、未解真相或未来 reveal" in prompt
    assert "创新落在事实与玩法，不落在词汇表" in prompt
    assert "不能让一个新词必须再靠两三个本书新词才能解释" in prompt
    assert "不要为了证明原创而回避境界、功法、兵器、异兽、血脉、火雷" in prompt
    assert "前台力量先给直接可感知的作用" in prompt
    assert "而不是先学习一套道路/路径概念" in prompt


def test_power_novelty_bundle_is_reproducible_and_diverse() -> None:
    first = build_power_novelty_bundle(seed=20260826)
    second = build_power_novelty_bundle(seed=20260826)

    assert first == second
    assert first.count("## Candidate ") == 3
    labels = [line for line in first.splitlines() if line.startswith("内部标签：")]
    assert len(labels) == 3
    assert len(set(labels)) == 3
    assert "seed: 20260826" in first
    assert "每个候选最多一个主异常" in first
    assert "单一异常只负责制造独特玩法，不是削弱预算" in first
    assert "Power Asymmetry 仍应明显超标" in first

    regression = build_power_novelty_bundle(seed=2026082716)
    assert "只能穿过自己能理解的障碍" not in regression
    assert "只能穿过自己正在亲手触碰的障碍" in regression


def test_power_lexique_bundle_is_reproducible_optional_and_authority_safe() -> None:
    first = build_power_lexique_bundle(seed=20260828)
    second = build_power_lexique_bundle(seed=20260828)

    assert first == second
    assert sum(line.startswith("- ") and " × " in line for line in first.splitlines()) == 6
    assert "全部不适合时必须全部忽略" in first
    assert "最多为每个 Candidate 借 0—1 个 primitive" in first
    assert "更具体的身体/器物/空间载体" in first
    assert "不得借 primitive 改写 POWER BASELINE / Novelty Spark 已有的触发、条件、覆盖对象、代价或 Permanent Boundary" in first
    assert "不得因此新建第二能源、法则树、概念权限或复杂触发链" in first
    assert "不要求进入一句话大白话或能力短名" in first


def test_power_prompt_auto_injects_noncanon_novelty_sparks() -> None:
    prompt = generate_split_prompt(
        mode="power_seed",
        world_vision=WORLD,
        creative_state=STATE,
        gbrain_inspiration="POWER CRAFT",
    )

    assert "Power Novelty Spark（随机扰动；非 Canon）" in prompt
    assert "Power Lexique Primitive Spark（可选；非 Canon；可完全忽略）" in prompt
    assert "OPTIONAL POWER LEXIQUE PRIMITIVE POOL" in prompt
    assert "熟悉幻想：" in prompt
    assert "单一异常：" in prompt
    assert "设定创新 ≠ 术语创新 ≠ 机制复杂化" in prompt
    assert "## 一句话大白话" in prompt
    assert "直接能力不要在成长时变回分析能力" in prompt
    assert "不要把它重新解释成结构分析、受力判断、材料诊断、路线计算或逐步验证" in prompt
    assert "如果读者明天醒来得到它" in prompt
    assert "World Power Normal → Power Asymmetry" in prompt
    assert "不必先被证明为世界内合法例外" in prompt
    assert "默认强度故意偏夸张" in prompt
    assert "宁可偏强一档" in prompt
    assert "不要做对称平衡" in prompt
    assert "Core Power 必须有明显纯收益区间" in prompt
    assert "Permanent Boundary 优先收束成一到少数根边界" in prompt
    assert "Boundary Stable, Privilege Expands" in prompt
    assert "Privilege Delta" in prompt
    assert "同层普通人通常只能做到什么" in prompt
    assert "不能靠删除 Novelty Spark 的“单一异常”换来" in prompt
    assert "允许并鼓励有条件的越级威胁" in prompt
    assert "局部高阶特权 ≠ 开局完整跨大档胜利" in prompt
    assert "输出尺度与可承载强度仍要和当前主尺发生真实耦合" in prompt
    assert "越级幅度本身也是成长结果" in prompt
    assert "不要为不同世界硬编码统一的 `+N级` 上限" in prompt
    assert "不要新增“超标坐标/比较表/评分”等输出字段" in prompt
    assert "不要让长期成长只剩数量、距离、持续时间越来越大" in prompt
    assert "不要逐步退化成互不相干的“技能背包”" in prompt
    assert "Future Legend Image 都不得放松、绕过或遗忘前面已经写明的 Permanent Boundary" in prompt
    assert "Power Seed 只定义**开局 Core Asymmetry**" in prompt
    assert "后续 Story Program 可以通过真实故事获得新的 Power Asymmetry" in prompt
    assert "POWER CRAFT" in prompt


def test_story_program_keeps_later_asymmetries_reader_facing() -> None:
    prompt = generate_split_prompt(
        mode="idea",
        creative_direction="男频修仙",
        world_vision=WORLD,
        character_card="# CHARACTER\n\n## POWER CORE\n能穿墙。\n\n## HUMAN CORE\n想赢。",
        creative_state={
            "world_vision": {"status": "author_approved"},
            "character_card": {"status": "author_approved"},
        },
    )

    assert "后续新 Asymmetry 继承 Power Seed 的“先白话、后命名”边界" in prompt
    assert "以前做不到什么、现在具体多能做什么" in prompt
    assert "不得靠两三个新造概念互相解释来制造高级感" in prompt
    assert "New Asymmetry ≠ New Power System" in prompt
    assert "Ruler 不是机械胜负公式，也不是可以被任一特殊机制绕开的装饰数字" in prompt
    assert "局部翻盘" in prompt
    assert "制造一次失误 / 存活 / 夺物 / 逼退 / 改变局面" in prompt
    assert "越级幅度本身也是纵向成长奖励" in prompt
    assert "Power Identity 要比技能清单更稳定" in prompt
    assert "外部兵器、法宝、坐骑等仍是外部资产" in prompt
    assert "Bonus Surprise is allowed" in prompt


def test_power_retrieval_aliases_include_power_dominance_and_verification() -> None:
    assert "power dominance" in PLANNING_KEYWORD_QUERIES["power_seed"]
    assert "power verification" in PLANNING_KEYWORD_QUERIES["power_seed"]
    assert "public proof" in PLANNING_KEYWORD_QUERY_BATCHES["power_seed"][1]


def test_power_novelty_can_be_disabled_for_control_experiments() -> None:
    prompt = generate_split_prompt(
        mode="power_seed",
        world_vision=WORLD,
        creative_state=STATE,
        power_novelty="",
    )

    assert "Power Novelty Spark（随机扰动；非 Canon）" not in prompt
    assert "## 一句话大白话" in prompt


def test_power_lexique_can_be_disabled_for_control_experiments() -> None:
    prompt = generate_split_prompt(
        mode="power_seed",
        world_vision=WORLD,
        creative_state=STATE,
        power_lexique="",
    )

    assert "Power Novelty Spark（随机扰动；非 Canon）" in prompt
    assert "Power Lexique Primitive Spark（可选；非 Canon；可完全忽略）" not in prompt
