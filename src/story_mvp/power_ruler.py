"""Precise reader-facing power ruler helpers.

TGN keeps one exact public main ruler for long-form growth.  The ruler is a
reader coordinate, not a combat formula: levels / stars / ranks tell readers
where somebody is, while skills, equipment, matchup and asymmetry still decide
what actually happens.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


ROOT_RULER_HEADING = "### 精确力量主尺｜Frozen Grammar"
MACRO_RULER_HEADING = "### 精确力量主尺延展｜Macro"
INSTANCE_RULER_HEADING = "### 本地精确力量主尺｜Instance Grammar"
INITIAL_POWER_POSITION_PREFIX = "开局精确力量位置｜"
CURRENT_POWER_POSITION_PREFIX = "Current Power Position｜"

_ALLOWED_TYPES = {"连续数字", "大境界+数字子级", "数字序列"}
_NUMERIC_RANGE_RE = re.compile(r"\d+\s*[—–-]\s*\d+")
_DIGIT_RE = re.compile(r"\d")
_LEVEL3_END_RE = re.compile(r"(?m)^#{1,3} .+$")
_LEVEL2_END_RE = re.compile(r"(?m)^#{1,2} .+$")
_KNOWN_FIELD_LABELS = {
    "主尺类型",
    "主尺名称",
    "精确位置格式",
    "数字精度规则",
    "当前可见范围",
    "当前大档位",
    "沿用主尺",
    "主尺语法改动",
    "新增可见范围",
    "与全局主尺关系",
}


@dataclass(frozen=True)
class PrecisePowerRuler:
    ruler_type: str
    name: str
    position_format: str
    numeric_rule: str
    visible_range: str
    major_tiers: str


def _section(text: str, heading: str, *, level: int = 3) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    after_start = start + len(heading)
    after = text[after_start:]
    regex = _LEVEL3_END_RE if level == 3 else _LEVEL2_END_RE
    match = regex.search(after)
    end = after_start + (match.start() if match else len(after))
    return text[start:end].strip()


def _fields(section: str) -> dict[str, str]:
    result: dict[str, str] = {}
    current_label = ""
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_label, current_lines
        if current_label:
            result[current_label] = "\n".join(current_lines).strip()
        current_label = ""
        current_lines = []

    for raw in section.splitlines()[1:]:
        line = raw.strip()
        if not line:
            continue
        if current_label == "当前大档位" and current_lines and not line.startswith(("-", "*")):
            flush()
            break
        normalized = line.lstrip("-* ").strip()
        label_match = re.match(r"^([^：:\n]+)[：:]\s*(.*?)\s*$", normalized)
        if label_match and label_match.group(1).strip() in _KNOWN_FIELD_LABELS:
            flush()
            current_label = label_match.group(1).strip()
            inline = label_match.group(2).strip()
            if inline:
                current_lines.append(inline)
            continue
        if current_label:
            current_lines.append(line)
    flush()
    return result


def parse_root_precise_power_ruler(world_text: str) -> PrecisePowerRuler:
    section = _section(world_text, ROOT_RULER_HEADING)
    if not section:
        raise ValueError(
            f"World Vision 缺少 `{ROOT_RULER_HEADING}`；当前 production 强制使用精确力量主尺"
        )
    values = _fields(section)
    required = ("主尺类型", "主尺名称", "精确位置格式", "数字精度规则", "当前可见范围", "当前大档位")
    missing = [label for label in required if not values.get(label)]
    if missing:
        raise ValueError("精确力量主尺缺少字段：" + "、".join(missing))

    ruler_type = values["主尺类型"]
    if ruler_type not in _ALLOWED_TYPES:
        raise ValueError("主尺类型只能是：连续数字 / 大境界+数字子级 / 数字序列")
    if "{N}" not in values["精确位置格式"]:
        raise ValueError("精确位置格式必须包含 `{N}` 数字占位，例如 `魂力{N}级`、`{大境界}{N}星`、`序列{N}`")
    if not _NUMERIC_RANGE_RE.search(values["数字精度规则"]):
        raise ValueError("数字精度规则必须给出明确数字范围，例如 `1—100`、`每境1—9` 或 `9—0`")
    if len(_DIGIT_RE.findall(values["当前可见范围"])) < 2:
        raise ValueError("当前可见范围必须给出至少两个数字端点，不能只写模糊的低/中/高阶")

    return PrecisePowerRuler(
        ruler_type=ruler_type,
        name=values["主尺名称"],
        position_format=values["精确位置格式"],
        numeric_rule=values["数字精度规则"],
        visible_range=values["当前可见范围"],
        major_tiers=values["当前大档位"],
    )


def project_root_precise_power_ruler(world_text: str) -> str:
    """Return the frozen root ruler section after validating it."""

    parse_root_precise_power_ruler(world_text)
    return _section(world_text, ROOT_RULER_HEADING)


def _parse_position_line(text: str, prefix: str) -> tuple[str, str] | None:
    for raw in text.splitlines():
        line = raw.strip().lstrip("-* ").strip()
        if not line.startswith(prefix):
            continue
        ruler_match = re.search(r"主尺[：:]\s*([^｜|]+)", line)
        position_match = re.search(r"精确位置[：:]\s*(.+?)\s*$", line)
        if ruler_match and position_match:
            return ruler_match.group(1).strip(), position_match.group(1).strip()
    return None


def validate_human_seed_start(human_seed: str, world_text: str) -> None:
    """Require the world-shaped Human seed to freeze an exact opening ruler position."""

    ruler = parse_root_precise_power_ruler(world_text)
    parsed = _parse_position_line(human_seed, INITIAL_POWER_POSITION_PREFIX)
    if parsed is None:
        raise ValueError(
            "HUMAN_SEED.md 缺少 `开局精确力量位置｜主尺：...｜精确位置：...`，无法冻结开局精确力量位置"
        )
    ruler_name, position = parsed
    if ruler_name != ruler.name:
        raise ValueError(f"Human Seed 主尺 `{ruler_name}` 与 World Root 主尺 `{ruler.name}` 不一致")
    if not _DIGIT_RE.search(position):
        raise ValueError("开局精确力量位置必须包含明确数字；未入门角色使用世界定义的 `0级/0段` 等精确零位")


def extract_initial_power_position(human_seed_or_human_core: str) -> str:
    parsed = _parse_position_line(human_seed_or_human_core, INITIAL_POWER_POSITION_PREFIX)
    if parsed is None:
        return ""
    ruler, position = parsed
    return f"{CURRENT_POWER_POSITION_PREFIX}主尺：{ruler}｜精确位置：{position}"


def validate_world_expansion_ruler(content: str, world_root: str, *, scope: str) -> None:
    """Macro expansions preserve root grammar; instance worlds get their own exact local ruler."""

    root = parse_root_precise_power_ruler(world_root)
    if scope == "macro":
        section = _section(content, MACRO_RULER_HEADING)
        if not section:
            raise ValueError(f"macro World Expansion 缺少 `{MACRO_RULER_HEADING}`")
        values = _fields(section)
        required = ("沿用主尺", "主尺语法改动", "新增可见范围")
        missing = [label for label in required if not values.get(label)]
        if missing:
            raise ValueError("macro 精确力量尺延展缺少字段：" + "、".join(missing))
        if values["沿用主尺"] != root.name:
            raise ValueError(f"macro Expansion 必须沿用 World Root 主尺 `{root.name}`")
        if values["主尺语法改动"].upper() != "NONE":
            raise ValueError("macro World Expansion 只能延展 Scale Range，`主尺语法改动` 必须为 NONE")
        visible = values["新增可见范围"]
        if visible.upper() != "NONE" and len(_DIGIT_RE.findall(visible)) < 2:
            raise ValueError("macro 新增可见范围必须给出明确数字端点；若本轮不扩力量上限就写 NONE")
        return

    if scope != "instance":
        raise ValueError("World Expansion scope 必须是 macro 或 instance")
    section = _section(content, INSTANCE_RULER_HEADING)
    if not section:
        raise ValueError(f"instance World Expansion 缺少 `{INSTANCE_RULER_HEADING}`")
    values = _fields(section)
    required = ("主尺类型", "主尺名称", "精确位置格式", "数字精度规则", "当前可见范围", "与全局主尺关系")
    missing = [label for label in required if not values.get(label)]
    if missing:
        raise ValueError("instance 本地精确力量主尺缺少字段：" + "、".join(missing))
    if values["主尺类型"] not in _ALLOWED_TYPES:
        raise ValueError("instance 主尺类型只能是：连续数字 / 大境界+数字子级 / 数字序列")
    if "{N}" not in values["精确位置格式"]:
        raise ValueError("instance 精确位置格式必须包含 `{N}` 数字占位")
    if not _NUMERIC_RANGE_RE.search(values["数字精度规则"]):
        raise ValueError("instance 数字精度规则必须给出明确数字范围")
    if len(_DIGIT_RE.findall(values["当前可见范围"])) < 2:
        raise ValueError("instance 当前可见范围必须给出至少两个数字端点")
    if "不改写" not in values["与全局主尺关系"] and "独立" not in values["与全局主尺关系"]:
        raise ValueError("instance 必须明确本地尺独立存在且不改写全局主尺")


def project_expansion_precise_ruler(content: str, *, scope: str) -> str:
    heading = MACRO_RULER_HEADING if scope == "macro" else INSTANCE_RULER_HEADING
    return _section(content, heading)


def extract_current_power_position(persistent_canon: str) -> str:
    for raw in persistent_canon.splitlines():
        line = raw.strip().lstrip("-* ").strip()
        if line.startswith(CURRENT_POWER_POSITION_PREFIX):
            return line
    return ""


def current_power_position_from_sources(persistent_canon: str, human_origin: str) -> str:
    return extract_current_power_position(persistent_canon) or extract_initial_power_position(human_origin)


def preserve_or_require_current_power_position(
    proposed_persistent_canon: str,
    previous_persistent_canon: str,
) -> str:
    """Preserve the exact public ruler position across State extraction omissions.

    A later State pass is allowed to omit the line, but that omission must not erase a
    long-form coordinate.  Chapter 1 still needs one explicit position because there is
    no prior Canon value to inherit.
    """

    current = extract_current_power_position(proposed_persistent_canon)
    if current:
        if not _DIGIT_RE.search(current):
            raise ValueError("Current Power Position 必须包含明确数字")
        return proposed_persistent_canon.strip()

    previous = extract_current_power_position(previous_persistent_canon)
    if not previous:
        # Low-level/legacy State helpers may not have a Character/World authority at all.
        # New production books are protected earlier by World + Character approval gates;
        # when a position already exists, omission here can never erase it.
        return proposed_persistent_canon.strip()

    heading = "### Power / Capability"
    if heading in proposed_persistent_canon:
        return proposed_persistent_canon.replace(
            heading,
            f"{heading}\n{previous}",
            1,
        ).strip()
    body = proposed_persistent_canon.strip()
    return f"{heading}\n{previous}\n{body}".strip()
