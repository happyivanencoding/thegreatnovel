from __future__ import annotations

import pytest

from story_mvp.power_ruler import (
    extract_initial_power_position,
    parse_root_precise_power_ruler,
    validate_human_seed_start,
)


WORLD_WITHOUT_RULER_META_NAME = """# PROTAGONIST-BLIND WORLD VISION

## 力量体系与正常值
### 精确力量主尺｜Frozen Grammar
主尺类型：大境界+数字子级
主尺名称：NONE
精确位置格式：{大境界}{N}重
数字精度规则：每个大境界1—9重
当前可见范围：启泉1重—至尊9重
当前大档位：启泉、神藏、贯脊、识海、圣境、至尊
"""


def test_world_ruler_can_be_precise_without_a_second_public_name() -> None:
    ruler = parse_root_precise_power_ruler(WORLD_WITHOUT_RULER_META_NAME)

    assert ruler.name == "NONE"
    assert ruler.position_format == "{大境界}{N}重"


def test_human_position_omits_literal_none_when_world_has_no_ruler_meta_name() -> None:
    human = "开局精确力量位置｜精确位置：启泉3重"

    validate_human_seed_start(human, WORLD_WITHOUT_RULER_META_NAME)
    current = extract_initial_power_position(human)

    assert current == "Current Power Position｜精确位置：启泉3重"
    assert "NONE" not in current


def test_human_cannot_invent_a_ruler_name_when_world_uses_none() -> None:
    human = "开局精确力量位置｜主尺：身天尺｜精确位置：启泉3重"

    with pytest.raises(ValueError, match="不应另造主尺"):
        validate_human_seed_start(human, WORLD_WITHOUT_RULER_META_NAME)
