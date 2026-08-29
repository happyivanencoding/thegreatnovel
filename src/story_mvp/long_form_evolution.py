"""Forward-only long-form authority evolution helpers.

The opening World/Power/Human origins stay stable.  This module only handles
later world expansions, stable Human development deltas, and deterministic
current-character snapshots used by periodic Story re-collision.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .power_ruler import current_power_position_from_sources


WORLD_EXPANSION_DIR = "world_expansions"
HUMAN_DEVELOPMENT_DIR = "human_development"
CURRENT_CHARACTER_FILENAME = "CURRENT_CHARACTER.md"

_WORLD_ENTRY_RE = re.compile(r"(?m)^# WORLD EXPANSION\s+(\d+)\s*$")
_HUMAN_ENTRY_RE = re.compile(r"(?m)^# HUMAN DEVELOPMENT DELTA\s+(\d+)\s*$")
_LEVEL2_RE = re.compile(r"(?m)^## .+$")
_LEVEL3_RE = re.compile(r"(?m)^### .+$")


def extract_world_horizon_handoff(story_program: str) -> str:
    """Return the Story Program's explicit forward handoff without interpreting it.

    The handoff is orchestration metadata for the author/planner.  It is
    intentionally *not* an input to protagonist-blind World Expansion; otherwise
    Character-aware Story planning could leak a tailored keyhole into World design.
    """

    heading = "## World Horizon Handoff"
    start = story_program.find(heading)
    if start < 0:
        return ""
    after_start = start + len(heading)
    after = story_program[after_start:]
    next_heading = _LEVEL2_RE.search(after)
    end = after_start + (next_heading.start() if next_heading else len(after))
    return story_program[start:end].strip()


@dataclass(frozen=True)
class WorldExpansionEntry:
    index: int
    scope: str
    effective_from: int
    effective_until: int
    body: str

    def active_at(self, chapter_number: int) -> bool:
        if chapter_number < self.effective_from:
            return False
        return self.effective_until <= 0 or chapter_number <= self.effective_until


@dataclass(frozen=True)
class HumanDevelopmentEntry:
    index: int
    evidence_through: int
    effective_from: int
    body: str

    def active_at(self, chapter_number: int) -> bool:
        return chapter_number >= self.effective_from


def _split_numbered_entries(text: str, pattern: re.Pattern[str]) -> list[tuple[int, str]]:
    matches = list(pattern.finditer(text))
    result: list[tuple[int, str]] = []
    for pos, match in enumerate(matches):
        end = matches[pos + 1].start() if pos + 1 < len(matches) else len(text)
        result.append((int(match.group(1)), text[match.end() : end].strip()))
    return result


def _metadata_int(block: str, label: str, default: int = 0) -> int:
    match = re.search(rf"(?mi)^{re.escape(label)}\s*:\s*(\d+)\s*$", block)
    return int(match.group(1)) if match else default


def _metadata_text(block: str, label: str, default: str = "") -> str:
    match = re.search(rf"(?mi)^{re.escape(label)}\s*:\s*([^\n]+?)\s*$", block)
    return match.group(1).strip() if match else default


def _strip_metadata(block: str, labels: tuple[str, ...]) -> str:
    lines = block.splitlines()
    kept: list[str] = []
    for line in lines:
        if any(re.match(rf"(?i)^{re.escape(label)}\s*:", line.strip()) for label in labels):
            continue
        kept.append(line)
    return "\n".join(kept).strip()


def parse_world_expansions(text: str) -> list[WorldExpansionEntry]:
    result: list[WorldExpansionEntry] = []
    for index, block in _split_numbered_entries(text, _WORLD_ENTRY_RE):
        scope = _metadata_text(block, "Scope", "macro").casefold()
        if scope not in {"macro", "instance"}:
            raise ValueError(f"World Expansion {index} 的 Scope 必须是 macro 或 instance")
        effective_from = _metadata_int(block, "Effective From Chapter")
        effective_until = _metadata_int(block, "Effective Until Chapter")
        if effective_from < 1:
            raise ValueError(f"World Expansion {index} 缺少有效 Effective From Chapter")
        if effective_until and effective_until < effective_from:
            raise ValueError(f"World Expansion {index} 的结束章节早于开始章节")
        body = _strip_metadata(
            block,
            ("Scope", "Effective From Chapter", "Effective Until Chapter"),
        )
        result.append(
            WorldExpansionEntry(
                index=index,
                scope=scope,
                effective_from=effective_from,
                effective_until=effective_until,
                body=body,
            )
        )
    return result


def parse_human_development(text: str) -> list[HumanDevelopmentEntry]:
    result: list[HumanDevelopmentEntry] = []
    for index, block in _split_numbered_entries(text, _HUMAN_ENTRY_RE):
        evidence_through = _metadata_int(block, "Evidence Through Chapter")
        effective_from = _metadata_int(block, "Effective From Chapter")
        if evidence_through < 0 or effective_from < 1:
            raise ValueError(f"Human Development Delta {index} 元数据无效")
        body = _strip_metadata(block, ("Evidence Through Chapter", "Effective From Chapter"))
        result.append(
            HumanDevelopmentEntry(
                index=index,
                evidence_through=evidence_through,
                effective_from=effective_from,
                body=body,
            )
        )
    return result


def effective_world_expansions(text: str, chapter_number: int) -> list[WorldExpansionEntry]:
    if chapter_number < 1:
        return []
    return [entry for entry in parse_world_expansions(text) if entry.active_at(chapter_number)]


def effective_human_development(text: str, chapter_number: int) -> list[HumanDevelopmentEntry]:
    if chapter_number < 1:
        return []
    return [entry for entry in parse_human_development(text) if entry.active_at(chapter_number)]


def compose_effective_world(world_root: str, world_expansions: str, chapter_number: int) -> str:
    """Compose root + only the forward authorities active for this chapter."""

    parts = [world_root.strip()]
    for entry in effective_world_expansions(world_expansions, chapter_number):
        parts.append(
            "\n".join(
                (
                    f"# ACTIVE WORLD EXPANSION {entry.index}",
                    f"Scope: {entry.scope}",
                    f"Effective From Chapter: {entry.effective_from}",
                    *(
                        (f"Effective Until Chapter: {entry.effective_until}",)
                        if entry.effective_until
                        else ()
                    ),
                    "",
                    entry.body,
                )
            ).strip()
        )
    return "\n\n".join(part for part in parts if part).strip() + "\n"


def _section(text: str, heading: str, *, level3: bool = False) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    after = text[start + len(heading) :]
    regex = _LEVEL3_RE if level3 else _LEVEL2_RE
    match = regex.search(after)
    end = start + len(heading) + (match.start() if match else len(after))
    return text[start:end].strip()


def _character_core(character_card: str, start_heading: str, end_heading: str) -> str:
    start = character_card.find(start_heading)
    if start < 0:
        return ""
    start += len(start_heading)
    end = character_card.find(end_heading, start)
    if end < 0:
        end = len(character_card)
    return character_card[start:end].strip()


def _canon_memory_sections(status_text: str) -> tuple[str, str]:
    active = _section(status_text, "## ACTIVE SCENE STATE")
    persistent = _section(status_text, "## PERSISTENT CANON")
    if not persistent:
        persistent = status_text.strip()
    return active, persistent


def project_world_state_from_status(status_text: str) -> str:
    """Expose only the explicit current World State to the protagonist-blind expander."""

    _, persistent = _canon_memory_sections(status_text)
    world = _section(persistent, "### World State", level3=True)
    if not world:
        return "（当前 Canon 尚未单独维护 World State；不得从人物状态反推未来世界。）"
    return world


def _canon_subsection(persistent: str, heading: str) -> str:
    return _section(persistent, heading, level3=True)


def compile_current_character(
    *,
    character_card: str,
    status_text: str,
    human_development: str,
    chapter_number: int,
) -> str:
    """Deterministically compile current Character authority from origins + happened facts."""

    power_origin = _character_core(
        character_card,
        "## POWER CORE｜Frozen Authority",
        "## HUMAN CORE｜Frozen Authority",
    )
    human_origin = _character_core(
        character_card,
        "## HUMAN CORE｜Frozen Authority",
        "## Composition Boundary",
    )
    active, persistent = _canon_memory_sections(status_text)
    power = _canon_subsection(persistent, "### Power / Capability")
    current_power_position = current_power_position_from_sources(persistent, human_origin)
    relationships = _canon_subsection(persistent, "### Active Relationships")
    identity = _canon_subsection(persistent, "### Identity / Access")
    knowledge = _canon_subsection(persistent, "### Knowledge / Enemy State")
    assets = _canon_subsection(persistent, "### Tracked Assets")
    development_entries = effective_human_development(human_development, chapter_number)
    development = "\n\n".join(
        "\n".join(
            (
                f"### Human Development Delta {entry.index}｜Effective From Chapter {entry.effective_from}",
                entry.body,
            )
        ).strip()
        for entry in development_entries
        if entry.body.strip()
    )

    parts = [
        "# CURRENT CHARACTER AUTHORITY｜Forward Snapshot",
        f"Compiled Through Chapter: {max(0, chapter_number - 1)}",
        "",
        "## Power Origin Core｜Frozen",
        power_origin or "（未提供 Frozen Power Core。）",
        "",
        "## Current Power Position｜Exact Public Ruler",
        current_power_position or "（当前精确力量位置尚未进入 Canon；不得用战绩或模糊强弱替代。）",
        "",
        "## Current Power Portfolio｜Canonical Additions",
        power or "（Canon 尚未单独维护 Power / Capability；以下 Current Canon Facts 仍为权威。）",
        "",
        "## Human Origin Core｜Frozen",
        human_origin or "（未提供 Frozen Human Core。）",
        "",
        "## Human Development｜Forward-only Stable Deltas",
        development or "NONE",
        "",
        "## Current Human State",
        "\n\n".join(part for part in (active, relationships) if part).strip() or "（当前没有额外人物状态。）",
        "",
        "## Current Identity / Knowledge / Assets",
        "\n\n".join(part for part in (identity, knowledge, assets) if part).strip() or "（由 Current Canon Facts 继续承载。）",
        "",
        "## Current Canon Facts｜Already Happened",
        persistent or "（当前 Persistent Canon 为空。）",
        "",
        "## Compilation Boundary",
        "这是确定性当前态，不重写 Origin，不创造新能力/新欲望/新关系。Human Development 按生效章节顺序读取；若后期 Delta 明确细化或改变早期稳定偏向，以后期已经发生的 Delta 约束未来，但旧 Delta 仍作为人物历史保留。未来 World Expansion 不参与本编译；Story Refresh 只能让独立世界与这份已发生人物事实重新碰撞。",
    ]
    return "\n".join(parts).strip() + "\n"
