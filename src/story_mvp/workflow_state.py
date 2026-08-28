"""主要 Story Artifact 的轻量依赖状态。

本模块只保存状态元数据，不复制 BOOK、创意产物或章节正文；单章内部节点仍由
``run_ledger`` 负责。本模块只处理主要持久产物之间的依赖、revision、stale 和 impact。
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any, Iterable


WORKFLOW_STATE_FILENAME = "WORKFLOW_STATE.json"
WORKFLOW_STATE_VERSION = 1

ARTIFACT_STATUSES = frozenset({"EMPTY", "DRAFT", "DONE", "STALE", "FAILED"})
FRESHNESS_VALUES = frozenset({"fresh", "stale"})

CREATIVE_ARTIFACT_KEYS = (
    "creative.world_vision",
    "creative.power_seed",
    "creative.human_seed",
    "creative.character_card",
    "creative.story_program",
)
BOOK_ARTIFACT_KEYS = (
    "book.design",
    "book.long_plan",
    "book.future_10",
    "book.canon_state",
)
STATIC_ARTIFACT_KEYS = CREATIVE_ARTIFACT_KEYS + BOOK_ARTIFACT_KEYS

CREATIVE_FILES = {
    "creative.world_vision": "WORLD_VISION.md",
    "creative.power_seed": "POWER_SEED.md",
    "creative.human_seed": "HUMAN_SEED.md",
    "creative.character_card": "CHARACTER.md",
    "creative.story_program": "PROPOSAL.md",
}
CREATIVE_STATE_KEYS = {
    "creative.world_vision": "world_vision",
    "creative.power_seed": "power_seed",
    "creative.human_seed": "human_seed",
    "creative.character_card": "character_card",
    "creative.story_program": "proposal",
}
BOOK_SECTIONS = {
    "book.design": "design",
    "book.long_plan": "long_plan",
    "book.future_10": "small_plan",
    "book.canon_state": "status",
}

ARTIFACT_LABELS = {
    "creative.world_vision": "世界幻想",
    "creative.power_seed": "力量种子",
    "creative.human_seed": "人物种子",
    "creative.character_card": "人物权威",
    "creative.story_program": "故事方案",
    "book.design": "总体设计",
    "book.long_plan": "中期规划",
    "book.future_10": "未来十章",
    "book.canon_state": "记忆状态",
}

_CHAPTER_ARTIFACT_PATTERN = re.compile(r"^chapter\.(\d+)\.(run|body|state_delta)$")
_CHAPTER_HEADING_PATTERN = re.compile(r"^##\s*第\s*(\d+)\s*章\s*[：:]")


def workflow_state_path(book_directory: Path) -> Path:
    return book_directory / WORKFLOW_STATE_FILENAME


def chapter_artifact_key(chapter_number: int, kind: str) -> str:
    if chapter_number < 1 or kind not in {"run", "body", "state_delta"}:
        raise ValueError("无效章节 Workflow Artifact")
    return f"chapter.{chapter_number}.{kind}"


def parse_chapter_artifact_key(artifact: str) -> tuple[int, str] | None:
    match = _CHAPTER_ARTIFACT_PATTERN.fullmatch(artifact)
    if not match:
        return None
    return int(match.group(1)), match.group(2)


def artifact_label(artifact: str) -> str:
    if artifact in ARTIFACT_LABELS:
        return ARTIFACT_LABELS[artifact]
    parsed = parse_chapter_artifact_key(artifact)
    if parsed:
        chapter, kind = parsed
        labels = {"run": "Run", "body": "正式正文", "state_delta": "State Delta"}
        return f"第{chapter}章 {labels[kind]}"
    return artifact


def _new_artifact(
    *,
    revision: int = 0,
    status: str = "EMPTY",
    source: str = "empty",
    freshness: str = "fresh",
) -> dict[str, Any]:
    return {
        "revision": revision,
        "status": status,
        "freshness": freshness,
        "last_source": source,
        "stale_from": [],
    }


def _new_state() -> dict[str, Any]:
    return {"version": WORKFLOW_STATE_VERSION, "artifacts": {}}


def _read_state(book_directory: Path) -> dict[str, Any] | None:
    path = workflow_state_path(book_directory)
    if not path.is_file():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"WORKFLOW_STATE.json 不是有效 JSON：{path}") from error
    if not isinstance(raw, dict) or raw.get("version") != WORKFLOW_STATE_VERSION:
        raise ValueError("WORKFLOW_STATE.json 版本不受支持")
    if not isinstance(raw.get("artifacts"), dict):
        raise ValueError("WORKFLOW_STATE.json 缺少 artifacts 对象")
    return raw


def _write_state(book_directory: Path, state: dict[str, Any]) -> None:
    workflow_state_path(book_directory).write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _creative_status(book_directory: Path, artifact: str, content: str) -> str:
    if not content.strip():
        return "EMPTY"
    state_path = book_directory / "CREATIVE_STATE.json"
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state_key = CREATIVE_STATE_KEYS.get(artifact, artifact.removeprefix("creative."))
            if state.get(state_key, {}).get("status") == "author_approved":
                return "DONE"
        except (OSError, json.JSONDecodeError):
            pass
    return "DRAFT"


def _content_status(content: str) -> str:
    return "DONE" if content.strip() else "EMPTY"


def _run_observation(manifest: dict[str, Any]) -> dict[str, Any]:
    """保存 Run 元数据观察值，不保存正文或 Prompt 内容。"""

    nodes = {}
    for node, info in sorted((manifest.get("nodes") or {}).items()):
        nodes[node] = {
            "status": info.get("status"),
            "attempts": info.get("attempts", 0),
            "prompt_file": info.get("prompt_file"),
            "response_file": info.get("response_file"),
        }
    return {
        "run_status": manifest.get("run_status"),
        "writer_mode": manifest.get("writer_mode"),
        "final_source": manifest.get("final_source"),
        "nodes": nodes,
    }


def _run_status(manifest: dict[str, Any]) -> tuple[str, str]:
    if manifest.get("run_status") == "failed":
        return "FAILED", "stale"
    statuses = [info.get("status") for info in (manifest.get("nodes") or {}).values()]
    if "stale" in statuses:
        return "STALE", "stale"
    if manifest.get("run_status") == "completed":
        return "DONE", "fresh"
    return "DRAFT", "fresh"


def _manifest_files(book_directory: Path) -> Iterable[tuple[int, Path, dict[str, Any]]]:
    runs = book_directory / "runs"
    if not runs.is_dir():
        return
    for manifest_path in sorted(runs.glob("chapter-*/manifest.json")):
        match = re.fullmatch(r"chapter-(\d+)", manifest_path.parent.name)
        if not match:
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(manifest, dict) and isinstance(manifest.get("nodes"), dict):
            yield int(match.group(1)), manifest_path, manifest


def _chapter_numbers(book_directory: Path) -> list[int]:
    result = []
    for path in (book_directory / "chapters").glob("chapter-*.md"):
        match = re.fullmatch(r"chapter-(\d+)\.md", path.name)
        if match:
            result.append(int(match.group(1)))
    return sorted(result)


def _future_chapter_entries(content: str) -> dict[int, str]:
    matches = list(_CHAPTER_HEADING_PATTERN.finditer(content))
    result: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        result[int(match.group(1))] = content[match.start() : end].strip()
    return result


def _changed_future_chapters(old_content: str, new_content: str) -> set[int]:
    old_entries = _future_chapter_entries(old_content)
    new_entries = _future_chapter_entries(new_content)
    return {
        number
        for number in set(old_entries) | set(new_entries)
        if old_entries.get(number) != new_entries.get(number)
    }


def _all_revision_inputs(state: dict[str, Any]) -> dict[str, int]:
    artifacts = state["artifacts"]
    return {key: int(artifacts.get(key, {}).get("revision", 0)) for key in STATIC_ARTIFACT_KEYS}


def _ensure_entry(
    state: dict[str, Any],
    artifact: str,
    *,
    revision: int = 0,
    status: str = "EMPTY",
    source: str = "empty",
) -> dict[str, Any]:
    entry = state["artifacts"].setdefault(
        artifact, _new_artifact(revision=revision, status=status, source=source)
    )
    entry.setdefault("revision", revision)
    entry.setdefault("status", status)
    entry.setdefault("freshness", "fresh")
    entry.setdefault("last_source", source)
    entry.setdefault("stale_from", [])
    return entry


def _mark_stale(state: dict[str, Any], artifact: str, cause: str) -> None:
    entry = state["artifacts"].get(artifact)
    if entry is None:
        return
    if artifact.endswith(".body") and entry.get("status") == "DONE":
        return
    entry["status"] = "STALE"
    entry["freshness"] = "stale"
    causes = entry.setdefault("stale_from", [])
    if cause not in causes:
        causes.append(cause)


def _protected_chapters(book_directory: Path) -> set[int]:
    return set(_chapter_numbers(book_directory))


def _mark_run_stale(book_directory: Path, chapter_number: int) -> None:
    manifest_path = book_directory / "runs" / f"chapter-{chapter_number:04d}" / "manifest.json"
    if not manifest_path.is_file():
        return
    try:
        from .run_ledger import mark_run_stale

        mark_run_stale(book_directory, chapter_number)
    except (FileNotFoundError, ValueError):
        # Workflow metadata remains authoritative for a manifest that is no longer loadable.
        return


def _existing_future_run_numbers(
    book_directory: Path,
    *,
    allowed: set[int] | None = None,
    after: int | None = None,
) -> list[int]:
    protected = _protected_chapters(book_directory)
    numbers = []
    for number, _, _ in _manifest_files(book_directory):
        if number in protected:
            continue
        if allowed is not None and number not in allowed:
            continue
        if after is not None and number <= after:
            continue
        numbers.append(number)
    return sorted(set(numbers))


def _mark_future_runs_stale(
    state: dict[str, Any],
    book_directory: Path,
    cause: str,
    *,
    allowed: set[int] | None = None,
    after: int | None = None,
) -> list[str]:
    affected: list[str] = []
    for number in _existing_future_run_numbers(book_directory, allowed=allowed):
        if after is not None and number <= after:
            continue
        run_key = chapter_artifact_key(number, "run")
        _mark_stale(state, run_key, cause)
        state_delta_key = chapter_artifact_key(number, "state_delta")
        if state_delta_key in state["artifacts"]:
            _mark_stale(state, state_delta_key, cause)
        _mark_run_stale(book_directory, number)
        affected.append(run_key)
    return affected


def _initialize_state(book_directory: Path) -> dict[str, Any]:
    from .storage import parse_book_sections

    state = _new_state()
    for artifact, filename in CREATIVE_FILES.items():
        content = _read_text(book_directory / filename)
        status = _creative_status(book_directory, artifact, content)
        _ensure_entry(
            state,
            artifact,
            revision=1 if content.strip() else 0,
            status=status,
            source="legacy" if content.strip() else "empty",
        )

    book_content = _read_text(book_directory / "BOOK.md")
    sections = parse_book_sections(book_content)
    for artifact, section in BOOK_SECTIONS.items():
        content = sections[section]
        _ensure_entry(
            state,
            artifact,
            revision=1 if content.strip() else 0,
            status=_content_status(content),
            source="legacy" if content.strip() else "empty",
        )

    revisions = _all_revision_inputs(state)
    for number, _, manifest in _manifest_files(book_directory):
        run_key = chapter_artifact_key(number, "run")
        status, freshness = _run_status(manifest)
        run_entry = _ensure_entry(state, run_key, revision=1, status=status, source="legacy")
        run_entry["freshness"] = freshness
        run_entry["observed"] = _run_observation(manifest)
        run_entry["source_revisions"] = dict(revisions)
        state_delta_key = chapter_artifact_key(number, "state_delta")
        node_status = (manifest.get("nodes") or {}).get("state_delta", {}).get("status")
        delta_status = {
            "completed": "DONE",
            "adopted": "DONE",
            "failed": "FAILED",
            "stale": "STALE",
        }.get(node_status, "DRAFT")
        delta_entry = _ensure_entry(state, state_delta_key, revision=1, status=delta_status, source="legacy")
        delta_entry["freshness"] = "stale" if delta_status == "STALE" else "fresh"

    for number in _chapter_numbers(book_directory):
        key = chapter_artifact_key(number, "body")
        _ensure_entry(state, key, revision=1, status="DONE", source="legacy")
    return state


def _refresh_state(state: dict[str, Any], book_directory: Path) -> bool:
    """同步真实文件/manifest 的存在与状态，不推断内容语义。"""

    from .storage import parse_book_sections

    before = copy.deepcopy(state)
    artifacts = state.setdefault("artifacts", {})
    supported_static = set(STATIC_ARTIFACT_KEYS)
    for artifact in list(artifacts):
        if artifact not in supported_static and parse_chapter_artifact_key(artifact) is None:
            artifacts.pop(artifact)
    for entry in artifacts.values():
        source_revisions = entry.get("source_revisions")
        if isinstance(source_revisions, dict):
            entry["source_revisions"] = {
                key: value for key, value in source_revisions.items() if key in supported_static
            }
    for artifact, filename in CREATIVE_FILES.items():
        content = _read_text(book_directory / filename)
        entry = _ensure_entry(state, artifact)
        if entry.get("status") != "STALE":
            entry["status"] = _creative_status(book_directory, artifact, content)
            entry["freshness"] = "fresh"
    sections = parse_book_sections(_read_text(book_directory / "BOOK.md"))
    for artifact, section in BOOK_SECTIONS.items():
        entry = _ensure_entry(state, artifact)
        if entry.get("status") != "STALE":
            entry["status"] = _content_status(sections[section])
            entry["freshness"] = "fresh"
    revisions = _all_revision_inputs(state)
    observed_runs = {number: manifest for number, _, manifest in _manifest_files(book_directory)}
    for number, manifest in observed_runs.items():
        run_key = chapter_artifact_key(number, "run")
        status, freshness = _run_status(manifest)
        entry = _ensure_entry(state, run_key, revision=1, status=status, source="legacy")
        observation = _run_observation(manifest)
        if entry.get("observed") != observation:
            entry["revision"] = max(1, int(entry.get("revision", 0)) + 1)
            entry["observed"] = observation
        entry["status"] = status
        entry["freshness"] = freshness
        entry.setdefault("source_revisions", dict(revisions))
        delta_key = chapter_artifact_key(number, "state_delta")
        node_status = (manifest.get("nodes") or {}).get("state_delta", {}).get("status")
        delta_status = {
            "completed": "DONE",
            "adopted": "DONE",
            "failed": "FAILED",
            "stale": "STALE",
        }.get(node_status, "DRAFT")
        delta_entry = _ensure_entry(state, delta_key, revision=1, status=delta_status, source="legacy")
        delta_entry["status"] = delta_status
        delta_entry["freshness"] = "stale" if delta_status == "STALE" else "fresh"

    for number in _chapter_numbers(book_directory):
        entry = _ensure_entry(state, chapter_artifact_key(number, "body"), revision=1, status="DONE", source="legacy")
        if entry.get("status") != "STALE":
            entry["status"] = "DONE"
            entry["freshness"] = "fresh"
    return state != before


def ensure_workflow_state(book_directory: Path) -> dict[str, Any]:
    state = _read_state(book_directory)
    if state is None:
        state = _initialize_state(book_directory)
        _write_state(book_directory, state)
        return state
    if _refresh_state(state, book_directory):
        _write_state(book_directory, state)
    return state


def _apply_content_change(
    state: dict[str, Any],
    book_directory: Path,
    artifact: str,
    old_content: str,
    new_content: str,
    source: str,
    *,
    changed_chapters: set[int] | None = None,
) -> list[str]:
    if old_content == new_content:
        return []
    entry = _ensure_entry(state, artifact)
    entry["revision"] = int(entry.get("revision", 0)) + 1
    if artifact in CREATIVE_FILES:
        entry["status"] = _creative_status(book_directory, artifact, new_content)
    else:
        entry["status"] = _content_status(new_content)
    entry["freshness"] = "fresh"
    entry["last_source"] = source
    entry["stale_from"] = []
    affected: list[str] = []

    if artifact == "creative.world_vision":
        for downstream in (
            "creative.power_seed",
            "creative.human_seed",
            "creative.character_card",
            "creative.story_program",
            "book.design",
            "book.long_plan",
            "book.future_10",
        ):
            _mark_stale(state, downstream, artifact)
        affected.extend(_mark_future_runs_stale(state, book_directory, artifact))
    elif artifact in {"creative.power_seed", "creative.human_seed"}:
        for downstream in (
            "creative.character_card",
            "creative.story_program",
            "book.design",
            "book.long_plan",
            "book.future_10",
        ):
            _mark_stale(state, downstream, artifact)
        affected.extend(_mark_future_runs_stale(state, book_directory, artifact))
    elif artifact == "creative.character_card":
        for downstream in ("creative.story_program", "book.design", "book.long_plan", "book.future_10"):
            _mark_stale(state, downstream, artifact)
        affected.extend(_mark_future_runs_stale(state, book_directory, artifact))
    elif artifact == "creative.story_program":
        for downstream in ("book.design", "book.long_plan", "book.future_10"):
            _mark_stale(state, downstream, artifact)
        affected.extend(_mark_future_runs_stale(state, book_directory, artifact))
    elif artifact == "book.design":
        for downstream in ("book.long_plan", "book.future_10"):
            _mark_stale(state, downstream, artifact)
        affected.extend(_mark_future_runs_stale(state, book_directory, artifact))
    elif artifact == "book.long_plan":
        for downstream in ("book.future_10",):
            _mark_stale(state, downstream, artifact)
        affected.extend(_mark_future_runs_stale(state, book_directory, artifact))
    elif artifact == "book.future_10":
        affected.extend(
            _mark_future_runs_stale(
                state,
                book_directory,
                artifact,
                allowed=changed_chapters or set(),
            )
        )
    elif artifact == "book.canon_state":
        current_revision = int(entry["revision"])
        for number, _, _ in _manifest_files(book_directory):
            if number in _protected_chapters(book_directory):
                continue
            run_key = chapter_artifact_key(number, "run")
            run_entry = state["artifacts"].get(run_key, {})
            source_revisions = run_entry.get("source_revisions", {})
            if int(source_revisions.get("book.canon_state", 0)) < current_revision:
                _mark_stale(state, run_key, artifact)
                delta_key = chapter_artifact_key(number, "state_delta")
                _mark_stale(state, delta_key, artifact)
                _mark_run_stale(book_directory, number)
                affected.append(run_key)
    return affected


def record_content_change(
    book_directory: Path,
    artifact: str,
    old_content: str,
    new_content: str,
    *,
    source: str = "author_edit",
) -> dict[str, Any]:
    if artifact not in STATIC_ARTIFACT_KEYS:
        raise ValueError(f"不是可直接保存的主要 Artifact：{artifact}")
    state = ensure_workflow_state(book_directory)
    _apply_content_change(state, book_directory, artifact, old_content, new_content, source)
    _write_state(book_directory, state)
    return state


def record_book_change(
    book_directory: Path,
    old_content: str,
    new_content: str,
    *,
    source: str = "author_edit",
) -> dict[str, Any]:
    from .storage import parse_book_sections

    old_sections = parse_book_sections(old_content)
    new_sections = parse_book_sections(new_content)
    state = ensure_workflow_state(book_directory)
    for artifact, section in BOOK_SECTIONS.items():
        changed = _changed_future_chapters(old_sections[section], new_sections[section]) if artifact == "book.future_10" else None
        _apply_content_change(
            state,
            book_directory,
            artifact,
            old_sections[section],
            new_sections[section],
            source,
            changed_chapters=changed,
        )
    _write_state(book_directory, state)
    return state


def record_chapter_body_change(
    book_directory: Path,
    chapter_number: int,
    old_content: str,
    new_content: str,
    *,
    source: str = "author_edit",
) -> dict[str, Any]:
    if old_content == new_content:
        return ensure_workflow_state(book_directory)
    state = ensure_workflow_state(book_directory)
    body_key = chapter_artifact_key(chapter_number, "body")
    entry = _ensure_entry(state, body_key)
    entry["revision"] = int(entry.get("revision", 0)) + 1
    entry["status"] = "DONE"
    entry["freshness"] = "fresh"
    entry["last_source"] = source
    entry["stale_from"] = []
    if old_content.strip():
        _mark_stale(state, chapter_artifact_key(chapter_number, "state_delta"), body_key)
        try:
            from .run_ledger import mark_node_stale

            mark_node_stale(book_directory, chapter_number, "state_delta")
        except (FileNotFoundError, ValueError):
            pass
        _mark_future_runs_stale(state, book_directory, body_key, after=chapter_number)
    _write_state(book_directory, state)
    return state


def sync_run_manifest(book_directory: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    chapter_number = int(manifest["chapter_number"])
    state = ensure_workflow_state(book_directory)
    key = chapter_artifact_key(chapter_number, "run")
    status, freshness = _run_status(manifest)
    entry = _ensure_entry(state, key, revision=1, status=status, source="run_ledger")
    observation = _run_observation(manifest)
    if entry.get("observed") != observation:
        entry["revision"] = max(1, int(entry.get("revision", 0)) + 1)
        entry["observed"] = observation
    entry["status"] = status
    entry["freshness"] = freshness
    entry["last_source"] = "run_ledger"
    entry.setdefault("source_revisions", _all_revision_inputs(state))
    delta_key = chapter_artifact_key(chapter_number, "state_delta")
    node_status = (manifest.get("nodes") or {}).get("state_delta", {}).get("status")
    delta_status = {
        "completed": "DONE",
        "adopted": "DONE",
        "failed": "FAILED",
        "stale": "STALE",
    }.get(node_status, "DRAFT")
    delta_entry = _ensure_entry(state, delta_key, revision=1, status=delta_status, source="run_ledger")
    delta_entry["status"] = delta_status
    delta_entry["freshness"] = "stale" if delta_status == "STALE" else "fresh"
    _write_state(book_directory, state)
    return state


def workflow_status(book_directory: Path) -> dict[str, Any]:
    state = ensure_workflow_state(book_directory)
    body_numbers = _chapter_numbers(book_directory)
    run_numbers = [number for number, _, _ in _manifest_files(book_directory)]
    if run_numbers:
        current = min(number for number in run_numbers if number > max(body_numbers, default=0)) if any(
            number > max(body_numbers, default=0) for number in run_numbers
        ) else max(body_numbers, default=1)
    else:
        current = max(body_numbers, default=0) + 1
    next_node = "director"
    manifest_path = book_directory / "runs" / f"chapter-{current:04d}" / "manifest.json"
    if manifest_path.is_file():
        try:
            from .run_ledger import next_actionable_node

            next_node = next_actionable_node(book_directory, current) or "完成"
        except (FileNotFoundError, ValueError):
            next_node = "未知"
    return {
        "version": WORKFLOW_STATE_VERSION,
        "artifacts": state["artifacts"],
        "current_chapter": current,
        "next_actionable_node": next_node,
        "protected_completed_chapters": body_numbers,
    }


def _dependents_for_impact(book_directory: Path, artifact: str) -> list[str]:
    state = ensure_workflow_state(book_directory)
    parsed = parse_chapter_artifact_key(artifact)
    if parsed:
        chapter_number, kind = parsed
        if kind == "body":
            result = [chapter_artifact_key(chapter_number, "state_delta")]
            result.extend(
                chapter_artifact_key(number, "run")
                for number in _existing_future_run_numbers(book_directory, after=chapter_number)
            )
            return [key for key in result if key in state["artifacts"]]
        if kind == "run":
            return []
        if kind == "state_delta":
            return []
    if artifact == "book.future_10":
        content = _read_text(book_directory / "BOOK.md")
        from .storage import parse_book_sections

        section = parse_book_sections(content)["small_plan"]
        allowed = set(_future_chapter_entries(section))
        return [chapter_artifact_key(number, "run") for number in _existing_future_run_numbers(book_directory, allowed=allowed)]
    if artifact == "book.canon_state":
        return [
            chapter_artifact_key(number, "run")
            for number in _existing_future_run_numbers(book_directory)
            if int(state["artifacts"].get(chapter_artifact_key(number, "run"), {}).get("source_revisions", {}).get("book.canon_state", 0))
            < int(state["artifacts"].get("book.canon_state", {}).get("revision", 0))
        ]
    static = {
        "creative.world_vision": ["creative.power_seed", "creative.human_seed"],
        "creative.power_seed": ["creative.character_card"],
        "creative.human_seed": ["creative.character_card"],
        "creative.character_card": ["creative.story_program"],
        "creative.story_program": ["book.design"],
        "book.design": ["book.long_plan"],
        "book.long_plan": ["book.future_10"],
    }
    return static.get(artifact, [])


def workflow_impact(book_directory: Path, artifact: str) -> dict[str, Any]:
    state = ensure_workflow_state(book_directory)
    known = set(state["artifacts"]) | set(STATIC_ARTIFACT_KEYS)
    if artifact not in known:
        raise ValueError(f"未知 Workflow Artifact：{artifact}")
    direct = _dependents_for_impact(book_directory, artifact)
    actual: list[str] = []
    queue = list(direct)
    visited: set[str] = set()
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        if current in state["artifacts"] and current not in _protected_body_keys(book_directory):
            actual.append(current)
        queue.extend(_dependents_for_impact(book_directory, current))
    protected = sorted(_protected_chapter_artifacts(book_directory))
    return {
        "artifact": artifact,
        "label": artifact_label(artifact),
        "direct_dependents": direct,
        "transitive_dependents": actual,
        "existing_nodes_affected": actual,
        "protected_completed_chapters": protected,
        "affected_count": len(actual),
        "stale_reason": state["artifacts"].get(artifact, {}).get("stale_from", []),
    }


def _protected_body_keys(book_directory: Path) -> set[str]:
    return {chapter_artifact_key(number, "body") for number in _protected_chapters(book_directory)}


def _protected_chapter_artifacts(book_directory: Path) -> set[str]:
    result: set[str] = set()
    for number in _protected_chapters(book_directory):
        result.update(
            {
                chapter_artifact_key(number, "body"),
                chapter_artifact_key(number, "run"),
                chapter_artifact_key(number, "state_delta"),
            }
        )
    return result
