from __future__ import annotations

import pytest

from story_mvp.premise_aperture import (
    DEFAULT_COLLISION_MATRIX,
    DEFAULT_VOLTAGE_BUDGET_MATRIX,
    build_axis_prompt,
    build_collision_prompt,
    build_lane_bundle,
    build_premise_compiler_prompt,
    build_premise_repair_prompt,
    build_selected_premise_compiler_prompt,
    build_single_pass_prompt,
    build_single_pass_lane_bundle,
    build_voltage_budget_prompt,
    extract_core,
    extract_sections,
    has_explicit_premise_conflict,
    normalize_single_candidate_response,
    render_lane_direction,
    validate_collision_locks,
    validate_premise_repair,
    validate_voltage_budget_locks,
)


WORLD = """# WORLD AXIS SPARKS
## W1｜一
Core: 世界一
### 三幅可见画面
画面一
## W2｜二
Core: 世界二
### 三幅可见画面
画面二
## W3｜三
Core: 世界三
### 三幅可见画面
画面三
"""

ONTOLOGY = """# ONTOLOGY AXIS SPARKS
## O1｜一
Core: 形态一
### 第一眼形象
形象一
## O2｜二
Core: 形态二
### 第一眼形象
形象二
## O3｜三
Core: 形态三
### 第一眼形象
形象三
"""

PRIVILEGE = """# PRIVILEGE AXIS SPARKS
## P1｜一
Core: 特权一
### 唯一根边界
边界一
## P2｜二
Core: 特权二
### 唯一根边界
边界二
## P3｜三
Core: 特权三
### 唯一根边界
边界三
"""

INTERFACE = """# INTERFACE AXIS SPARKS
## I1｜一
Core: 界面一
### 语气电压
语气一
## I2｜二
Core: 界面二
### 语气电压
语气二
## I3｜三
Core: 界面三
### 语气电压
语气三
"""

COLLISION = """# ORTHOGONAL PREMISE COLLISIONS
## C1｜一
Source Lock: W1 + O2 + P3 + I1
### Locked Cores
World: 世界一
Ontology: 形态二
Privilege: 特权三
Interface: 界面一
## C2｜二
Source Lock: W2 + O3 + P1 + I2
### Locked Cores
World: 世界二
Ontology: 形态三
Privilege: 特权一
Interface: 界面二
## C3｜三
Source Lock: W3 + O1 + P2 + I3
### Locked Cores
World: 世界三
Ontology: 形态一
Privilege: 特权二
Interface: 界面三
"""


def _pools() -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]:
    return (
        extract_sections(WORLD, prefix="W"),
        extract_sections(ONTOLOGY, prefix="O"),
        extract_sections(PRIVILEGE, prefix="P"),
        extract_sections(INTERFACE, prefix="I"),
    )


def test_single_pass_and_axis_prompts_are_explicitly_non_canon() -> None:
    single = build_single_pass_prompt(author_direction="快节奏玄幻")
    world = build_axis_prompt(axis="world", author_direction="快节奏玄幻")

    assert "PRE-AUTHORITY CREATIVE APERTURE｜非 Canon" in single
    assert "SINGLE-PASS PREMISE CANDIDATES" in single
    assert "World Voltage 发散者" in world
    assert "完全不知道未来主角" in world


def test_premise_compiler_is_author_facing_satisfiability_not_selector() -> None:
    candidates = """# SINGLE-PASS PREMISE CANDIDATES
## S1｜一
S1_TOKEN
## S2｜二
S2_TOKEN
## S3｜三
S3_TOKEN
"""
    prompt = build_premise_compiler_prompt(candidates=candidates)

    assert all(token in prompt for token in ("S1_TOKEN", "S2_TOKEN", "S3_TOKEN"))
    assert "不能因为候选自己的 `Authority-Compilation Trace` 声称合法就放行" in prompt
    assert "不得评分、排名、替作者选择、自动修复" in prompt
    assert "大胆、怪异、主角占便宜大、奖励多都不是错误" in prompt


def test_premise_compiler_requires_exactly_three_candidates() -> None:
    with pytest.raises(ValueError, match="S1.*S2.*S3"):
        build_premise_compiler_prompt(
            candidates="""## S1｜一
只有一张
"""
        )


def test_unknown_axis_fails_closed() -> None:
    with pytest.raises(ValueError, match="未知 Premise Aperture axis"):
        build_axis_prompt(axis="missing", author_direction="")  # type: ignore[arg-type]


def test_extract_sections_and_core() -> None:
    sections = extract_sections(WORLD, prefix="W")

    assert tuple(sections) == ("W1", "W2", "W3")
    assert extract_core(sections["W2"]) == "世界二"
    assert "画面三" in sections["W3"]


def test_collision_prompt_uses_code_fixed_matrix() -> None:
    world, ontology, privilege, interface = _pools()
    prompt = build_collision_prompt(
        author_direction="方向",
        world_sparks=world,
        ontology_sparks=ontology,
        privilege_sparks=privilege,
        interface_sparks=interface,
    )

    assert "C1 FIXED COMPONENTS" in prompt
    assert "## W1｜一" in prompt
    assert "## O2｜二" in prompt
    assert "## P3｜三" in prompt
    assert "## I1｜一" in prompt
    assert "Source Lock: W2 + O3 + P1 + I2" in prompt


def test_collision_prompt_rejects_missing_spark() -> None:
    world, ontology, privilege, interface = _pools()
    del world["W2"]

    with pytest.raises(ValueError, match="Collision 缺少 spark：W2"):
        build_collision_prompt(
            author_direction="方向",
            world_sparks=world,
            ontology_sparks=ontology,
            privilege_sparks=privilege,
            interface_sparks=interface,
        )


def test_collision_lock_validator_detects_semantic_smoothing() -> None:
    world, ontology, privilege, interface = _pools()

    assert validate_collision_locks(
        COLLISION,
        world_sparks=world,
        ontology_sparks=ontology,
        privilege_sparks=privilege,
        interface_sparks=interface,
    ) == {}

    smoothed = COLLISION.replace("Privilege: 特权一", "Privilege: 一个更方便的能力", 1)
    assert validate_collision_locks(
        smoothed,
        world_sparks=world,
        ontology_sparks=ontology,
        privilege_sparks=privilege,
        interface_sparks=interface,
    ) == {"C2": ["P1"]}


def test_lane_projection_preserves_authority_isolation() -> None:
    world, ontology, privilege, interface = _pools()
    selected = DEFAULT_COLLISION_MATRIX[1]
    bundle = build_lane_bundle(
        selected=selected,
        collision_text=COLLISION,
        world_sparks=world,
        ontology_sparks=ontology,
        privilege_sparks=privilege,
        interface_sparks=interface,
    )

    world_direction = render_lane_direction(bundle, lane="world")
    power_direction = render_lane_direction(bundle, lane="power")
    human_direction = render_lane_direction(bundle, lane="human")
    story_direction = render_lane_direction(bundle, lane="story")

    assert "世界二" in world_direction
    assert "形态三" not in world_direction
    assert "特权一" not in world_direction
    assert "界面二" not in world_direction

    assert "形态三" in power_direction
    assert "特权一" in power_direction
    assert "世界二" not in power_direction
    assert "界面二" not in power_direction

    assert "形态三" in human_direction
    assert "特权一" not in human_direction
    assert "世界二" not in human_direction
    assert "界面二" not in human_direction

    assert "世界二" in story_direction
    assert "形态三" in story_direction
    assert "特权一" in story_direction
    assert "界面二" in story_direction


def test_unknown_lane_fails_closed() -> None:
    world, ontology, privilege, interface = _pools()
    bundle = build_lane_bundle(
        selected=DEFAULT_COLLISION_MATRIX[0],
        collision_text=COLLISION,
        world_sparks=world,
        ontology_sparks=ontology,
        privilege_sparks=privilege,
        interface_sparks=interface,
    )

    with pytest.raises(ValueError, match="未知 Premise Aperture lane"):
        render_lane_direction(bundle, lane="missing")  # type: ignore[arg-type]


def test_conflict_detector_ignores_negative_prose_but_accepts_fail_loud_line() -> None:
    assert not has_explicit_premise_conflict(
        "世界能够容纳这些约束，因此不触发 `PREMISE-AUTHORITY CONFLICT`。"
    )
    assert has_explicit_premise_conflict(
        "# PREMISE-AUTHORITY CONFLICT：World 禁止任何物体承载命令"
    )
    assert has_explicit_premise_conflict("PREMISE-AUTHORITY CONFLICT")
    assert has_explicit_premise_conflict("`PREMISE-AUTHORITY CONFLICT`：边界冲突")


def test_voltage_budget_uses_exactly_two_fixed_high_voltage_sparks() -> None:
    world, ontology, privilege, interface = _pools()
    prompt = build_voltage_budget_prompt(
        author_direction="方向",
        world_sparks=world,
        ontology_sparks=ontology,
        privilege_sparks=privilege,
        interface_sparks=interface,
    )

    assert "V1 FIXED TWO-BET COMPONENTS" in prompt
    assert "## W1｜一" in prompt
    assert "## P2｜二" in prompt
    v1_block = prompt.split("# V1 FIXED TWO-BET COMPONENTS", 1)[1].split(
        "# V2 FIXED TWO-BET COMPONENTS", 1
    )[0]
    assert "## O2｜二" not in v1_block
    assert "## I1｜一" not in v1_block
    assert len(DEFAULT_VOLTAGE_BUDGET_MATRIX) == 3


def test_voltage_budget_rejects_missing_component_and_checks_locks() -> None:
    world, ontology, privilege, interface = _pools()
    with pytest.raises(ValueError, match="Voltage Budget 缺少 spark：P2"):
        build_voltage_budget_prompt(
            author_direction="方向",
            world_sparks=world,
            ontology_sparks=ontology,
            privilege_sparks={"P1": privilege["P1"], "P3": privilege["P3"]},
            interface_sparks=interface,
        )

    response = """# ASYMMETRIC VOLTAGE BUDGET CANDIDATES
## V1｜一
World: 世界一
Privilege: 特权二
## V2｜二
Ontology: 形态三
Privilege: 特权一
## V3｜三
World: 世界三
Interface: 界面三
"""
    assert validate_voltage_budget_locks(
        response,
        world_sparks=world,
        ontology_sparks=ontology,
        privilege_sparks=privilege,
        interface_sparks=interface,
    ) == {}

    smoothed = response.replace("Interface: 界面三", "Interface: 一点传闻", 1)
    assert validate_voltage_budget_locks(
        smoothed,
        world_sparks=world,
        ontology_sparks=ontology,
        privilege_sparks=privilege,
        interface_sparks=interface,
    ) == {"V3": ["I3"]}


def test_single_pass_candidate_compiles_back_into_isolated_lanes() -> None:
    candidate = """## S2｜测试
### 一句话货架简介
完整概念
### World-only Direction
世界独有事实 WORLD_TOKEN
### World Interface-only Direction
世界公开界面 WORLD_PUBLIC_MARKER
### Protagonist Ontology-only Direction
身体独有事实 ONTOLOGY_TOKEN
### Initial Origin-only Direction
零点出生事实 ORIGIN_TOKEN
### Initial Scale Position-only Direction
精确尺位 SCALE_TOKEN
### Power-only Direction
能力独有事实 POWER_TOKEN
### Story Interface / Opening Promise
界面独有事实 INTERFACE_TOKEN
### Authority-Compilation Trace
开篇动作均由已写字段推出 TRACE_TOKEN
### 第一章标志性画面
完整碰撞 STORY_TOKEN
"""
    bundle = build_single_pass_lane_bundle(candidate)

    world = render_lane_direction(bundle, lane="world")
    power = render_lane_direction(bundle, lane="power")
    human = render_lane_direction(bundle, lane="human")
    story = render_lane_direction(bundle, lane="story")

    assert "WORLD_TOKEN" in world
    assert "WORLD_PUBLIC_MARKER" in world
    assert "ONTOLOGY_TOKEN" not in world
    assert "ORIGIN_TOKEN" not in world
    assert "SCALE_TOKEN" not in world
    assert "POWER_TOKEN" not in world
    assert "INTERFACE_TOKEN" not in world
    assert "TRACE_TOKEN" not in world

    assert "ONTOLOGY_TOKEN" in power
    assert "POWER_TOKEN" in power
    assert "WORLD_TOKEN" not in power
    assert "WORLD_PUBLIC_MARKER" not in power
    assert "ORIGIN_TOKEN" not in power
    assert "SCALE_TOKEN" in power
    assert "INTERFACE_TOKEN" not in power
    assert "TRACE_TOKEN" not in power

    assert "ONTOLOGY_TOKEN" in human
    assert "ORIGIN_TOKEN" in human
    assert "SCALE_TOKEN" in human
    assert "POWER_TOKEN" not in human
    assert "WORLD_PUBLIC_MARKER" not in human
    assert "INTERFACE_TOKEN" not in human
    assert "TRACE_TOKEN" not in human

    assert all(
        token in story
        for token in (
            "WORLD_TOKEN",
            "WORLD_PUBLIC_MARKER",
            "ONTOLOGY_TOKEN",
            "ORIGIN_TOKEN",
            "SCALE_TOKEN",
            "POWER_TOKEN",
            "INTERFACE_TOKEN",
            "TRACE_TOKEN",
            "STORY_TOKEN",
        )
    )


def test_single_pass_lane_compiler_fails_closed_on_missing_field() -> None:
    with pytest.raises(ValueError, match="Power-only Direction"):
        build_single_pass_lane_bundle(
            """## S1｜坏候选
### World-only Direction
世界
### World Interface-only Direction
界面规则
### Protagonist Ontology-only Direction
形态
### Initial Origin-only Direction
零点
### Initial Scale Position-only Direction
精确尺位
### Story Interface / Opening Promise
界面
### Authority-Compilation Trace
追踪
"""
        )


def test_single_pass_lane_compiler_requires_origin_and_world_interface() -> None:
    base = """## S1｜坏候选
### World-only Direction
世界
### Protagonist Ontology-only Direction
形态
### Power-only Direction
能力
### Story Interface / Opening Promise
故事界面
### Authority-Compilation Trace
追踪
"""
    with pytest.raises(ValueError, match="World Interface-only Direction"):
        build_single_pass_lane_bundle(base)

    with_world_interface = base.replace(
        "### Protagonist Ontology-only Direction",
        "### World Interface-only Direction\n公开规则\n### Protagonist Ontology-only Direction",
    )
    with pytest.raises(ValueError, match="Initial Origin-only Direction"):
        build_single_pass_lane_bundle(with_world_interface)

    with_origin = with_world_interface.replace(
        "### Power-only Direction",
        "### Initial Origin-only Direction\n零点\n### Power-only Direction",
    )
    with pytest.raises(ValueError, match="Initial Scale Position-only Direction"):
        build_single_pass_lane_bundle(with_origin)


def test_single_pass_render_marks_lane_payload_as_hard_constraints() -> None:
    candidate = """## S1｜硬约束
### World-only Direction
世界事实
### World Interface-only Direction
公开重映
### Protagonist Ontology-only Direction
非人本体
### Initial Origin-only Direction
死者喉中诞生
### Initial Scale Position-only Direction
主尺不适用；副尺一阶
### Power-only Direction
任何真实载体
### Story Interface / Opening Promise
公开开篇
### Authority-Compilation Trace
全部闭合
"""
    bundle = build_single_pass_lane_bundle(candidate)

    assert "硬约束" in render_lane_direction(bundle, lane="world")
    assert "不得降格成偶尔使用的舞台效果" in render_lane_direction(
        bundle, lane="world"
    )
    assert "目标类别" in render_lane_direction(bundle, lane="power")
    assert "不得静默扩大、缩窄" in render_lane_direction(bundle, lane="power")
    assert "不得在这个 T0 之前补训练" in render_lane_direction(
        bundle, lane="human"
    )
    assert "PREMISE-AUTHORITY CONFLICT" in render_lane_direction(
        bundle, lane="story"
    )


def test_single_pass_lane_compiler_requires_authority_compilation_trace() -> None:
    candidate = """## S1｜缺少预编译追踪
### World-only Direction
世界
### World Interface-only Direction
公开规则
### Protagonist Ontology-only Direction
形态
### Initial Origin-only Direction
零点
### Initial Scale Position-only Direction
精确尺位
### Power-only Direction
能力
### Story Interface / Opening Promise
故事界面
"""
    with pytest.raises(ValueError, match="Authority-Compilation Trace"):
        build_single_pass_lane_bundle(candidate)


def test_explicit_conflict_detector_accepts_acp_preamble_shape() -> None:
    assert has_explicit_premise_conflict(
        "子代理正在复核是否必须上返作者。`PREMISE-AUTHORITY CONFLICT`\n\n"
        "当前不能安全生成 # STORY PROGRAM。"
    )
    assert not has_explicit_premise_conflict(
        "所有字段一致，因此不触发 `PREMISE-AUTHORITY CONFLICT`。"
    )


REPAIRABLE_CANDIDATE = """## S2｜活门
### 一句话货架简介
他就是一扇会吞下房间的活门。
### World-only Direction
原世界规则
### World Interface-only Direction
五名见证者留下门影
### Protagonist Ontology-only Direction
主角是一扇真实活门，不能变成人。
### Initial Origin-only Direction
从旧门槛出生，只有一扇门。
### Initial Scale Position-only Direction
城壳尺1｜室壳。
### Power-only Direction
完整穿门后才能吞入。
### Story Interface / Opening Promise
第一章吞下一间棚屋。
### Authority-Compilation Trace
棚屋完整过门。
### 第一章标志性画面
棚屋从门中消失。
### 主角反复会做的新动作
- 吞下真实房间；
- 把门变成战场边界。
### 第一次不公平兑现
从同一扇门吐回棚屋。
### 20章玩法扩张
逐级接入完整壳体。
### 100章以上仍能长出的不同故事
不同世界争夺谁能进入他。
### 最小可信桥梁
目标必须真实完整过门。
### 不可磨平的三点
- 主角不是人；
- 穿门就是战斗；
- 身体成长改变关系。
"""


def test_selected_compiler_checks_one_card_without_selecting() -> None:
    prompt = build_selected_premise_compiler_prompt(candidate=REPAIRABLE_CANDIDATE)

    assert "## S2" in prompt
    assert "PASS / CONDITIONAL PASS / FAIL" in prompt
    assert "自动 selector" in prompt
    assert "他就是一扇会吞下房间的活门" in prompt


def test_selected_compiler_rejects_multiple_cards() -> None:
    with pytest.raises(ValueError, match="只接受一张"):
        build_selected_premise_compiler_prompt(
            candidate=REPAIRABLE_CANDIDATE + "\n## S3｜另一张\n内容"
        )


def test_repair_prompt_code_locks_creative_core() -> None:
    prompt = build_premise_repair_prompt(
        candidate=REPAIRABLE_CANDIDATE,
        compiler_report="棚屋没有完整过门。",
    )

    assert "LOCKED CREATIVE CORE" in prompt
    assert "## S2｜活门" in prompt
    assert "他就是一扇会吞下房间的活门" in prompt
    assert "主角是一扇真实活门，不能变成人" in prompt
    assert "吞下真实房间" in prompt
    assert "主角不是人" in prompt
    assert "棚屋没有完整过门" in prompt
    assert "不得削弱第一次不公平兑现" in prompt


def test_repair_validator_allows_causal_edits_but_rejects_core_drift() -> None:
    repaired = REPAIRABLE_CANDIDATE.replace(
        "完整穿门后才能吞入。",
        "当主角成为一座封闭空间的唯一真实门时，关门会让整座空间沿门槛完整折入。",
    ).replace(
        "棚屋完整过门。",
        "棚屋其余出口先被封死，主角成为唯一真实门，关门后整座棚屋完整折过门槛。",
    )

    checks = validate_premise_repair(
        original=REPAIRABLE_CANDIDATE,
        repaired=repaired,
    )
    assert all(checks.values())

    weakened = repaired.replace(
        "他就是一扇会吞下房间的活门。",
        "他是住在门里的少年。",
    )
    with pytest.raises(ValueError, match="一句话货架简介"):
        validate_premise_repair(
            original=REPAIRABLE_CANDIDATE,
            repaired=weakened,
        )

    renamed = repaired.replace("## S2｜活门", "## S2｜门中少年", 1)
    with pytest.raises(ValueError, match="改写候选标题"):
        validate_premise_repair(
            original=REPAIRABLE_CANDIDATE,
            repaired=renamed,
        )


def test_single_candidate_normalizer_drops_preamble_but_rejects_extra_card() -> None:
    normalized = normalize_single_candidate_response(
        text="先核对 `## S2` 约束。## S2｜活门\n正文\n",
        expected_id="S2",
    )
    assert normalized == "## S2｜活门\n正文\n"

    with pytest.raises(ValueError, match="必须且只包含"):
        normalize_single_candidate_response(
            text="## S2｜活门\n正文\n## S3｜另一张\n内容\n",
            expected_id="S2",
        )
