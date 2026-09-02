from __future__ import annotations

import re
from dataclasses import dataclass


PROGRAM_REGISTRY_HEADING = "## 不可降格的 Reader-Facing Story Events"
BOOK_REGISTRY_HEADING = "### 不可降格 Reader-Facing Story Event Registry"
RUNTIME_OBLIGATION_HEADING = "## 不可降格 Reader-Facing Story Event Obligations"
CHAPTER_PLAN_FIELD = "不可降格 Story Event"


@dataclass(frozen=True)
class ProtectedStoryEvent:
    event_id: str
    event_atom: str
    state_residue: str
    timing_boundary: str
    reader_anchors: tuple[str, ...]


_ID_HEADING = re.compile(r"^#{3,5}\s+(RSE-\d{2,})\s*$")
_FIELD = re.compile(
    r"^(事件原子|状态残留|排程边界|读者证明锚点)\s*[：:]\s*(.*?)\s*$"
)
_CHAPTER_HEADING = re.compile(r"^##\s+第\s*(\d+)\s*章(?:[：:].*)?$", re.M)
_EXACT_CHAPTER = re.compile(r"第\s*(\d+)\s*章")
_ID_TOKEN = re.compile(r"RSE-\d{2,}")


def _section(text: str, heading: str) -> str:
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    except StopIteration:
        return ""
    level = len(heading) - len(heading.lstrip("#"))
    out: list[str] = []
    for line in lines[start + 1 :]:
        stripped = line.strip()
        match = re.match(r"^(#+)\s+", stripped)
        if match and len(match.group(1)) <= level:
            break
        out.append(line)
    return "\n".join(out).strip()


def _split_anchors(value: str, event_id: str) -> tuple[str, ...]:
    anchors = tuple(
        part.strip()
        for part in re.split(r"[；;]", value)
        if part.strip()
    )
    if not anchors:
        raise ValueError(f"{event_id} 缺少读者证明锚点")
    if len(anchors) > 6:
        raise ValueError(f"{event_id} 读者证明锚点最多 6 个")
    return anchors


def parse_protected_story_events(
    text: str, *, heading: str, strict_rows: bool = True
) -> dict[str, ProtectedStoryEvent]:
    """Parse the small author-approved protected-event registry.

    The registry is deliberately strict: it is an authority transport format, not prose.
    Old Story Programs without the heading remain valid and simply return an empty map.
    """

    body = _section(text, heading)
    if not body or body.strip() == "NONE":
        return {}
    lines = body.splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = _ID_HEADING.match(line.strip())
        if match:
            starts.append((index, match.group(1)))
    if not starts:
        raise ValueError(f"{heading} 必须使用 `RSE-01` 形式的事件块，或明确写 NONE")
    if len(starts) > 4:
        raise ValueError(f"{heading} 最多保护 4 个非替代性 Story Event；普通转折不得进入 Registry")

    events: dict[str, ProtectedStoryEvent] = {}
    for pos, (start, event_id) in enumerate(starts):
        if event_id in events:
            raise ValueError(f"重复的 Protected Story Event：{event_id}")
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        values: dict[str, str] = {}
        for raw in lines[start + 1 : end]:
            stripped = raw.strip()
            if not stripped:
                continue
            match = _FIELD.match(stripped)
            if not match:
                if strict_rows:
                    raise ValueError(
                        f"{event_id} 存在无法解析的行：{stripped}；Story Event Authority 不允许静默丢字段或续行"
                    )
                continue
            key, value = match.group(1), match.group(2).strip()
            if key in values:
                raise ValueError(f"{event_id} 重复字段：{key}")
            values[key] = value
        missing = [
            key
            for key in ("事件原子", "状态残留", "排程边界", "读者证明锚点")
            if not values.get(key)
        ]
        if missing:
            raise ValueError(f"{event_id} 缺少字段：{'、'.join(missing)}")
        events[event_id] = ProtectedStoryEvent(
            event_id=event_id,
            event_atom=values["事件原子"],
            state_residue=values["状态残留"],
            timing_boundary=values["排程边界"],
            reader_anchors=_split_anchors(values["读者证明锚点"], event_id),
        )
    return events


def parse_story_program_protected_events(story_program: str) -> dict[str, ProtectedStoryEvent]:
    return parse_protected_story_events(story_program, heading=PROGRAM_REGISTRY_HEADING)


def parse_book_protected_events(book_content: str) -> dict[str, ProtectedStoryEvent]:
    return parse_protected_story_events(book_content, heading=BOOK_REGISTRY_HEADING)


def render_book_registry(events: dict[str, ProtectedStoryEvent]) -> str:
    if not events:
        return BOOK_REGISTRY_HEADING + "\nNONE"
    parts = [BOOK_REGISTRY_HEADING]
    for event in events.values():
        parts.extend(
            [
                f"#### {event.event_id}",
                f"事件原子：{event.event_atom}",
                f"状态残留：{event.state_residue}",
                f"排程边界：{event.timing_boundary}",
                f"读者证明锚点：{'；'.join(event.reader_anchors)}",
            ]
        )
    return "\n".join(parts)


def validate_book_registry_against_story_program(story_program: str, book_content: str) -> None:
    """Fail loud if Outline drops or rewrites an approved high-value event atom."""

    approved = parse_story_program_protected_events(story_program)
    compiled = parse_book_protected_events(book_content)
    if not approved and not compiled:
        return
    if set(approved) != set(compiled):
        missing = sorted(set(approved) - set(compiled))
        extra = sorted(set(compiled) - set(approved))
        details: list[str] = []
        if missing:
            details.append("缺失 " + "、".join(missing))
        if extra:
            details.append("未批准 " + "、".join(extra))
        raise ValueError("Protected Story Event Registry 与已批准 Story Program 不一致：" + "；".join(details))
    for event_id, event in approved.items():
        if compiled[event_id] != event:
            raise ValueError(
                f"{event_id} 在 Story Program → Outline 编译中被改写；Outline 只能排章，不能重述事件原子"
            )
    validate_chapter_story_event_schedule(book_content)


def _chapter_blocks(small_plan: str) -> dict[int, str]:
    matches = list(_CHAPTER_HEADING.finditer(small_plan))
    blocks: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(small_plan)
        blocks[int(match.group(1))] = small_plan[match.start() : end].strip()
    return blocks


def _small_plan(book_content: str) -> str:
    marker = "# 未来十章逐章小纲"
    start = book_content.find(marker)
    if start < 0:
        return ""
    tail = book_content[start + len(marker) :]
    next_heading = re.search(r"(?m)^# (?!#)", tail)
    return tail[: next_heading.start()].strip() if next_heading else tail.strip()


def chapter_story_event_ids(chapter_plan: str) -> tuple[str, ...]:
    matched_values: list[str] = []
    for raw in chapter_plan.splitlines():
        stripped = raw.strip()
        match = re.match(
            rf"^(?:[-*]\s*)?{re.escape(CHAPTER_PLAN_FIELD)}\s*[：:]\s*(.*?)\s*$",
            stripped,
        )
        if not match:
            continue
        matched_values.append(match.group(1).strip())
    if not matched_values:
        return ()
    if len(matched_values) > 1:
        raise ValueError(f"每个 Future-10 章节只能有一行 `{CHAPTER_PLAN_FIELD}`")
    value = matched_values[0]
    if not value or value.upper() == "NONE":
        return ()
    ids = tuple(_ID_TOKEN.findall(value))
    if not ids:
        raise ValueError(f"{CHAPTER_PLAN_FIELD} 只能引用 `RSE-01` 形式的已批准 ID")
    return ids


def validate_chapter_story_event_schedule(book_content: str) -> None:
    """Validate IDs and exact chapter boundaries that are already in the current Future-10."""

    events = parse_book_protected_events(book_content)
    if not events:
        return
    blocks = _chapter_blocks(_small_plan(book_content))
    scheduled: dict[str, int] = {}
    for chapter, block in blocks.items():
        for event_id in chapter_story_event_ids(block):
            if event_id not in events:
                raise ValueError(f"第{chapter}章引用了未批准 Protected Story Event：{event_id}")
            if event_id in scheduled:
                raise ValueError(
                    f"Protected Story Event {event_id} 被重复排入第{scheduled[event_id]}章和第{chapter}章"
                )
            scheduled[event_id] = chapter
    for event_id, event in events.items():
        exact = _EXACT_CHAPTER.fullmatch(event.timing_boundary.strip())
        if not exact:
            continue
        chapter = int(exact.group(1))
        if chapter in blocks and scheduled.get(event_id) != chapter:
            raise ValueError(
                f"{event_id} 的已批准排程边界是第{chapter}章，但 Future-10 没有在该章引用它"
            )


def resolve_chapter_story_events(book_content: str, chapter_plan: str) -> tuple[ProtectedStoryEvent, ...]:
    ids = chapter_story_event_ids(chapter_plan)
    if not ids:
        return ()
    registry = parse_book_protected_events(book_content)
    resolved: list[ProtectedStoryEvent] = []
    for event_id in ids:
        try:
            resolved.append(registry[event_id])
        except KeyError as error:
            raise ValueError(f"当前章引用了未批准 Protected Story Event：{event_id}") from error
    return tuple(resolved)


def render_chapter_story_event_obligations(events: tuple[ProtectedStoryEvent, ...]) -> str:
    if not events:
        return ""
    lines = [RUNTIME_OBLIGATION_HEADING]
    for event in events:
        lines.extend(
            [
                f"### {event.event_id}",
                f"事件原子：{event.event_atom}",
                f"状态残留：{event.state_residue}",
                f"排程边界：{event.timing_boundary}",
                f"读者证明锚点：{'；'.join(event.reader_anchors)}",
            ]
        )
    return "\n".join(lines)



def strip_book_registry_from_section(section_text: str) -> str:
    """Keep the registry as deterministic scheduler metadata, never raw chapter context."""

    pattern = re.compile(
        rf"(?ms)^{re.escape(BOOK_REGISTRY_HEADING)}\s*$.*?(?=^###\s+|\Z)"
    )
    return pattern.sub("", section_text).strip()

def parse_runtime_story_event_obligations(authority_prompt: str) -> tuple[ProtectedStoryEvent, ...]:
    parsed = parse_protected_story_events(
        authority_prompt, heading=RUNTIME_OBLIGATION_HEADING, strict_rows=False
    )
    return tuple(parsed.values())


def story_event_realized(final_response: str, event: ProtectedStoryEvent) -> bool:
    """Catch total premise/event demotion using only author-approved literal proof anchors.

    This is intentionally narrower than semantic judging: the full event remains in Frozen
    Mission for the Reviser; anchors only decide whether the rare bounded repair is needed.
    """

    compact = re.sub(r"\s+", "", final_response)
    return all(re.sub(r"\s+", "", anchor) in compact for anchor in event.reader_anchors)


def missing_story_events(
    authority_prompt: str, final_response: str
) -> tuple[ProtectedStoryEvent, ...]:
    return tuple(
        event
        for event in parse_runtime_story_event_obligations(authority_prompt)
        if not story_event_realized(final_response, event)
    )


def _repair_authority_with_single_current_draft(
    authority_prompt: str, final_response: str
) -> str:
    """Keep frozen authority but expose exactly one prose draft to the bounded retry."""

    if "# CURRENT AUTHORITY REVISION" in authority_prompt:
        # A prior narrow repair prompt (for example explicit milestone repair) already
        # carries the current revision as its only prose draft. Do not duplicate it.
        return authority_prompt.strip()

    marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    start = authority_prompt.find(marker)
    if start >= 0:
        authority_only = authority_prompt[:start].rstrip()
        return (
            authority_only
            + "\n\n## CURRENT AUTHORITY REVISION｜唯一待修订正文底稿\n\n"
            + final_response.strip()
        )

    return (
        authority_prompt.strip()
        + "\n\n## CURRENT AUTHORITY REVISION｜唯一待修订正文底稿\n\n"
        + final_response.strip()
    )


def build_protected_story_event_repair_prompt(
    authority_prompt: str,
    final_response: str,
    missing: tuple[ProtectedStoryEvent, ...],
) -> str:
    """Build one narrow Preservation-First retry for a dropped reader-facing event."""

    if not missing:
        raise ValueError("Protected Story Event repair 至少需要一个缺失事件")
    requirements = []
    for event in missing:
        requirements.append(
            "\n".join(
                (
                    f"### {event.event_id}",
                    f"事件原子：{event.event_atom}",
                    f"状态残留（不能替代事件）：{event.state_residue}",
                    f"正文必须实际出现的读者证明锚点：{'；'.join(event.reader_anchors)}",
                )
            )
        )
    repair_base = _repair_authority_with_single_current_draft(
        authority_prompt, final_response
    )
    return f"""# 条件性 Protected Story Event Repair｜仅一次窄修复

你仍是同一个 Authority Reviser。这不是第二次创作，只修复已经批准、却在最终稿里被压成 State / 摘要而消失的 Reader-Facing Story Event。

Preservation First：
- 已经正确的段落默认逐字不动。
- 只在 Frozen Chapter Mission 已经授权的最近合法位置补回下面缺失事件的**最小现场因果**。
- 不能只补一个名词或 State；读者必须真正经历事件原子，并能看到列出的 proof anchors。**Event Atom 要保真其事实与因果，不要求逐字复现原句；除 proof anchors 外，若原子里含后台抽象词，优先用人物/读者一眼能懂的同义事实表达。**
- 不新增战斗、考核、资源、奖励、伤势、关系变化、人物选择、未知事实、机制解释或下一章事件。
- 不改主要事件顺序、胜负、Direct Result、State Change、Ending；如果原稿已有支撑句，优先 salvage / 移位，而不是重写周围正文。
- 本地人物不得替 Meta Authority 说自己不可能知道的话；谁能感知该事件继续服从 Frozen Authority。

# 缺失的 Protected Story Event

{chr(10).join(requirements)}

# FROZEN AUTHORITY + CURRENT REVISION｜只保留一份当前正文底稿

{repair_base}

严格只输出修复后的完整正式正文，不输出说明、补丁报告或审计。
""".strip() + "\n"
