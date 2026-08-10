"""Edition-aware Global Book Profile with a generated baseline and author overlay."""

from __future__ import annotations

import json
import sqlite3
import uuid
from enum import StrEnum
from pathlib import Path
from typing import Any

from novel_authoring.db.database import Database
from novel_authoring.storage.layout import BookLayout
from novel_authoring.utils import utc_now

PROFILE_DIMENSIONS: tuple[tuple[str, str, str], ...] = (
    ("worldbuilding", "世界观", "worldbuilding.md"),
    ("characters", "人物", "characters.md"),
    ("plot", "剧情", "plot.md"),
    ("style", "文风", "style.md"),
    ("narrative", "叙事", "narrative.md"),
    ("dialogue", "对话", "dialogue.md"),
    ("pacing", "节奏", "pacing.md"),
    ("themes", "主题 / 价值观", "themes.md"),
    ("continuity", "连续性", "continuity.md"),
)

_DIMENSION_MAP = {
    dimension: {"label": label, "filename": filename}
    for dimension, label, filename in PROFILE_DIMENSIONS
}


class ProfileEditOperation(StrEnum):
    ADD = "ADD"
    REPLACE = "REPLACE"
    REMOVE = "REMOVE"


class ProfileStrength(StrEnum):
    SUGGESTION = "SUGGESTION"
    PREFER = "PREFER"
    MUST = "MUST"
    MUST_NOT = "MUST_NOT"


STRENGTH_LABELS = {
    ProfileStrength.SUGGESTION.value: "建议",
    ProfileStrength.PREFER.value: "优先",
    ProfileStrength.MUST.value: "必须",
    ProfileStrength.MUST_NOT.value: "禁止",
}


def _loads(value: Any, fallback: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(str(value))
    except (TypeError, ValueError):
        return fallback


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _profile_root(connection: sqlite3.Connection, book_id: str) -> Path:
    row = connection.execute(
        "SELECT workspace_root FROM books WHERE book_id=?", (book_id,)
    ).fetchone()
    if row is None:
        raise ValueError("book 不存在")
    root = Path(str(row["workspace_root"])).expanduser().resolve()
    if (root / "book.yaml").is_file():
        return BookLayout(root.parent).for_book(book_id).book_profil
    return root / "book_profil"


def _generated_baseline(
    connection: sqlite3.Connection, book_id: str
) -> dict[str, dict[str, Any]]:
    root = _profile_root(connection, book_id)
    baseline: dict[str, dict[str, Any]] = {}
    for dimension, label, filename in PROFILE_DIMENSIONS:
        path = root / filename
        baseline[dimension] = {
            "dimension": dimension,
            "label": label,
            "filename": filename,
            "content": path.read_text(encoding="utf-8")[:500_000] if path.is_file() else "",
            "available": path.is_file(),
            "source": "INITIALIZATION_GENERATED",
        }
    return baseline


def _apply_edits(
    baseline: dict[str, dict[str, Any]], edits: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    effective = {key: dict(value) for key, value in baseline.items()}
    applied: dict[str, list[dict[str, Any]]] = {key: [] for key in effective}
    for edit in edits:
        dimension = str(edit.get("dimension") or "")
        if dimension not in effective:
            continue
        operation = str(edit.get("operation") or ProfileEditOperation.ADD.value)
        content = str(edit.get("content") or "").strip()
        if operation == ProfileEditOperation.REPLACE.value:
            effective[dimension]["content"] = content
        elif operation == ProfileEditOperation.REMOVE.value:
            effective[dimension]["content"] = ""
        elif content:
            current = str(effective[dimension].get("content") or "").rstrip()
            effective[dimension]["content"] = (
                f"{current}\n\n{content}" if current else content
            )
        applied[dimension].append(dict(edit))
    result: list[dict[str, Any]] = []
    for dimension, _, _ in PROFILE_DIMENSIONS:
        value = effective[dimension]
        dimension_edits = applied[dimension]
        result.append(
            {
                **value,
                "available": bool(str(value.get("content") or "").strip()),
                "author_edits": dimension_edits,
                "author_edit_count": len(dimension_edits),
                "effective_source": (
                    "GENERATED_BASELINE_PLUS_AUTHOR_OVERLAY"
                    if dimension_edits
                    else value.get("source", "INITIALIZATION_GENERATED")
                ),
            }
        )
    return result


def _profile_history(
    connection: sqlite3.Connection, book_id: str, edition_id: str
) -> list[dict[str, Any]]:
    rows = connection.execute(
        "SELECT * FROM book_profile_versions WHERE book_id=? AND edition_id=? "
        "ORDER BY version_number DESC",
        (book_id, edition_id),
    ).fetchall()
    history: list[dict[str, Any]] = []
    previous_count = 0
    for row in reversed(rows):
        edits = list(_loads(row["author_edits_json"], []))
        new_edits = edits[previous_count:]
        previous_count = len(edits)
        history.append(
            {
                "profile_version_id": str(row["profile_version_id"]),
                "version_number": int(row["version_number"]),
                "reason": str(row["reason"] or ""),
                "created_at": str(row["created_at"]),
                "changes": [
                    {
                        "dimension": edit.get("dimension"),
                        "dimension_label": _DIMENSION_MAP.get(
                            str(edit.get("dimension")), {}
                        ).get("label", edit.get("dimension")),
                        "operation": edit.get("operation"),
                        "strength": edit.get("strength"),
                        "strength_label": STRENGTH_LABELS.get(
                            str(edit.get("strength")), edit.get("strength")
                        ),
                        "content": edit.get("content"),
                        "reason": edit.get("reason"),
                    }
                    for edit in new_edits
                ],
            }
        )
    return list(reversed(history))


def _baseline_for_connection(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    *,
    visited: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    if edition_id in visited:
        raise ValueError("Edition Profile 继承链出现循环")
    row = connection.execute(
        "SELECT baseline_json FROM book_profile_versions "
        "WHERE book_id=? AND edition_id=? ORDER BY version_number DESC LIMIT 1",
        (book_id, edition_id),
    ).fetchone()
    if row is not None:
        return dict(_loads(row["baseline_json"], {}))
    edition = connection.execute(
        "SELECT parent_edition_id FROM editions WHERE book_id=? AND edition_id=?",
        (book_id, edition_id),
    ).fetchone()
    parent_id = (
        None
        if edition is None or edition["parent_edition_id"] is None
        else str(edition["parent_edition_id"])
    )
    if parent_id is not None:
        return _baseline_for_connection(
            connection,
            book_id,
            parent_id,
            visited=visited | {edition_id},
        )
    return _generated_baseline(connection, book_id)


def queue_book_profile_refresh_proposal_in_transaction(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    *,
    source_type: str,
    proposed_baseline: dict[str, Any] | None = None,
    summary: str = "",
) -> str:
    """Queue an author-reviewed refresh suggestion inside an existing commit."""

    proposal_id = f"profile-proposal-{uuid.uuid4().hex}"
    baseline = proposed_baseline or _baseline_for_connection(
        connection, book_id, edition_id
    )
    connection.execute(
        "INSERT INTO book_profile_refresh_proposals("
        "proposal_id, book_id, edition_id, source_type, status, "
        "proposed_baseline_json, summary, created_at, version"
        ") VALUES (?, ?, ?, ?, 'PENDING', ?, ?, ?, 1)",
        (
            proposal_id,
            book_id,
            edition_id,
            source_type.strip().upper() or "AUTHOR_REANALYSIS",
            _dumps(baseline),
            summary.strip(),
            utc_now(),
        ),
    )
    return proposal_id


def _invalidate_profile_consumers(
    connection: sqlite3.Connection, book_id: str, edition_id: str, reason: str
) -> None:
    now = utc_now()
    connection.execute(
        "UPDATE planning_aggregates SET status='STALE', stale_reason=?, "
        "invalidated_at=?, version=version+1 "
        "WHERE book_id=? AND edition_id=? AND status='ACTIVE'",
        (reason, now, book_id, edition_id),
    )
    connection.execute(
        "UPDATE candidate_plans SET status='STALE', stale_reason=?, version=version+1 "
        "WHERE book_id=? AND edition_id=? AND status<>'STALE'",
        (reason, book_id, edition_id),
    )
    connection.execute(
        "UPDATE chapter_contracts SET status='STALE', stale_reason=?, version=version+1 "
        "WHERE book_id=? AND edition_id=? AND status<>'STALE'",
        (reason, book_id, edition_id),
    )


def load_effective_book_profile(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    _visited: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    if edition_id in _visited:
        raise ValueError("Edition Profile 继承链出现循环")
    with database.connect() as connection:
        edition = connection.execute(
            "SELECT parent_edition_id FROM editions WHERE book_id=? AND edition_id=?",
            (book_id, edition_id),
        ).fetchone()
        if edition is None:
            if edition_id != "base":
                raise ValueError("edition 不存在")
            parent_edition_id: str | None = None
        else:
            parent_edition_id = (
                None
                if edition["parent_edition_id"] is None
                else str(edition["parent_edition_id"])
            )
        row = connection.execute(
            "SELECT * FROM book_profile_versions WHERE book_id=? AND edition_id=? "
            "ORDER BY version_number DESC LIMIT 1",
            (book_id, edition_id),
        ).fetchone()
        if row is not None:
            baseline = dict(_loads(row["baseline_json"], {}))
            edits = list(_loads(row["author_edits_json"], []))
            version_id = str(row["profile_version_id"])
            version_number = int(row["version_number"])
            inherited_from = None
        else:
            parent_id = parent_edition_id
            baseline = {}
            edits = []
            version_id = f"generated:{book_id}:{edition_id}"
            version_number = 0
            inherited_from = parent_id
            if parent_id is None:
                baseline = _generated_baseline(connection, book_id)
        proposals = [
            {
                **dict(proposal),
                "proposed_baseline": _loads(proposal["proposed_baseline_json"], {}),
            }
            for proposal in connection.execute(
                "SELECT * FROM book_profile_refresh_proposals "
                "WHERE book_id=? AND edition_id=? ORDER BY created_at DESC",
                (book_id, edition_id),
            ).fetchall()
        ]
        history = _profile_history(connection, book_id, edition_id)
    if inherited_from is not None:
        parent = load_effective_book_profile(
            database,
            book_id,
            inherited_from,
            _visited=_visited | {edition_id},
        )
        baseline = {
            str(item["dimension"]): {
                **dict(item),
                "author_edits": [],
                "author_edit_count": 0,
                "source": f"INHERITED_FROM:{inherited_from}",
            }
            for item in parent["dimensions"]
        }
    dimensions = _apply_edits(baseline, edits)
    active_edits = [
        dict(edit)
        for edit in edits
        if str(edit.get("operation")) != ProfileEditOperation.REMOVE.value
    ]
    return {
        "book_id": book_id,
        "edition_id": edition_id,
        "profile_version_id": version_id,
        "version_number": version_number,
        "inherited_from_edition_id": inherited_from,
        "baseline": baseline,
        "author_edits": edits,
        "dimensions": dimensions,
        "active_directives": active_edits,
        "hard_constraints": {
            "must": [
                edit for edit in active_edits if edit.get("strength") == ProfileStrength.MUST.value
            ],
            "must_not": [
                edit
                for edit in active_edits
                if edit.get("strength") == ProfileStrength.MUST_NOT.value
            ],
        },
        "history": history,
        "proposals": proposals,
    }


def edit_book_profile(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    dimension: str,
    operation: ProfileEditOperation | str,
    content: str = "",
    strength: ProfileStrength | str = ProfileStrength.SUGGESTION,
    reason: str = "作者编辑",
) -> dict[str, Any]:
    database.initialize()
    if dimension not in _DIMENSION_MAP:
        raise ValueError("未知 Profile 维度")
    selected_operation = ProfileEditOperation(str(operation).upper())
    selected_strength = ProfileStrength(str(strength).upper())
    clean_content = content.strip()
    if selected_operation is not ProfileEditOperation.REMOVE and not clean_content:
        raise ValueError("画像编辑内容不能为空")
    current = load_effective_book_profile(database, book_id, edition_id)
    edit = {
        "edit_id": f"profile-edit-{uuid.uuid4().hex}",
        "dimension": dimension,
        "operation": selected_operation.value,
        "content": clean_content,
        "strength": selected_strength.value,
        "strength_label": STRENGTH_LABELS[selected_strength.value],
        "reason": reason.strip() or "作者编辑",
        "created_at": utc_now(),
    }
    edits = [*current["author_edits"], edit]
    version_number = int(current["version_number"]) + 1
    version_id = f"book-profile-{uuid.uuid4().hex}"
    with database.connect() as connection:
        connection.execute(
            "INSERT INTO book_profile_versions("
            "profile_version_id, book_id, edition_id, version_number, baseline_json, "
            "author_edits_json, reason, created_at, version"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)",
            (
                version_id,
                book_id,
                edition_id,
                version_number,
                _dumps(current["baseline"]),
                _dumps(edits),
                edit["reason"],
                edit["created_at"],
            ),
        )
        _invalidate_profile_consumers(
            connection,
            book_id,
            edition_id,
            f"Effective Book Profile 已更新至版本 {version_number}",
        )
    return load_effective_book_profile(database, book_id, edition_id)


def create_book_profile_refresh_proposal(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    source_type: str,
    proposed_baseline: dict[str, Any] | None = None,
    summary: str = "",
) -> dict[str, Any]:
    database.initialize()
    with database.connect() as connection:
        proposal_id = queue_book_profile_refresh_proposal_in_transaction(
            connection,
            book_id,
            edition_id,
            source_type=source_type,
            proposed_baseline=proposed_baseline,
            summary=summary,
        )
    return {"proposal_id": proposal_id, "status": "PENDING"}


def resolve_book_profile_refresh_proposal(
    database: Database,
    book_id: str,
    edition_id: str,
    proposal_id: str,
    *,
    action: str,
    edited_baseline: dict[str, Any] | None = None,
) -> dict[str, Any]:
    database.initialize()
    selected_action = action.strip().upper()
    if selected_action not in {"ACCEPT", "ACCEPT_EDITED", "REJECT"}:
        raise ValueError("Profile proposal action 无效")
    current = load_effective_book_profile(database, book_id, edition_id)
    with database.connect() as connection:
        proposal = connection.execute(
            "SELECT * FROM book_profile_refresh_proposals "
            "WHERE proposal_id=? AND book_id=? AND edition_id=?",
            (proposal_id, book_id, edition_id),
        ).fetchone()
        if proposal is None:
            raise ValueError("Profile proposal 不存在")
        if str(proposal["status"]) != "PENDING":
            raise ValueError("Profile proposal 已处理")
        now = utc_now()
        if selected_action == "REJECT":
            connection.execute(
                "UPDATE book_profile_refresh_proposals "
                "SET status='REJECTED', resolved_at=?, version=version+1 "
                "WHERE proposal_id=?",
                (now, proposal_id),
            )
        else:
            baseline = edited_baseline or dict(
                _loads(proposal["proposed_baseline_json"], {})
            )
            version_number = int(current["version_number"]) + 1
            connection.execute(
                "INSERT INTO book_profile_versions("
                "profile_version_id, book_id, edition_id, version_number, baseline_json, "
                "author_edits_json, reason, created_at, version"
                ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)",
                (
                    f"book-profile-{uuid.uuid4().hex}",
                    book_id,
                    edition_id,
                    version_number,
                    _dumps(baseline),
                    _dumps(current["author_edits"]),
                    f"接受 Profile proposal {proposal_id}",
                    now,
                ),
            )
            _invalidate_profile_consumers(
                connection,
                book_id,
                edition_id,
                f"已接受 Book Profile proposal {proposal_id}",
            )
            connection.execute(
                "UPDATE book_profile_refresh_proposals SET status=?, resolved_at=?, "
                "proposed_baseline_json=?, version=version+1 WHERE proposal_id=?",
                (
                    "ACCEPTED_EDITED" if selected_action == "ACCEPT_EDITED" else "ACCEPTED",
                    now,
                    _dumps(baseline),
                    proposal_id,
                ),
            )
    return load_effective_book_profile(database, book_id, edition_id)


__all__ = [
    "PROFILE_DIMENSIONS",
    "ProfileEditOperation",
    "ProfileStrength",
    "STRENGTH_LABELS",
    "create_book_profile_refresh_proposal",
    "edit_book_profile",
    "load_effective_book_profile",
    "queue_book_profile_refresh_proposal_in_transaction",
    "resolve_book_profile_refresh_proposal",
]
