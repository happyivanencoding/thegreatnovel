"""Author-only truth storage and retroactive compatibility checks.

Author Truth is deliberately separate from the Canon event store.  A truth may
constrain future behaviour without having been exposed to either readers or
characters.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.db.database import Database
from novel_authoring.edition import edition_chapters
from novel_authoring.utils import utc_now


class TruthType(StrEnum):
    CHARACTER_SECRET = "CHARACTER_SECRET"
    CHARACTER_GOAL = "CHARACTER_GOAL"
    CHARACTER_IDENTITY = "CHARACTER_IDENTITY"
    ITEM_SECRET = "ITEM_SECRET"
    ABILITY_SECRET = "ABILITY_SECRET"
    LOCATION_SECRET = "LOCATION_SECRET"
    FACTION_SECRET = "FACTION_SECRET"
    FACTION_GOAL = "FACTION_GOAL"
    FACTION_RELATIONSHIP = "FACTION_RELATIONSHIP"
    WORLD_RULE_SECRET = "WORLD_RULE_SECRET"
    RELATIONSHIP_SECRET = "RELATIONSHIP_SECRET"
    PLOT_TRUTH = "PLOT_TRUTH"
    CAUSE = "CAUSE"
    MOTIVE = "MOTIVE"
    FUTURE_EVENT_PRECONDITION = "FUTURE_EVENT_PRECONDITION"
    CUSTOM = "CUSTOM"


class TruthStatus(StrEnum):
    IDEA = "IDEA"
    ACTIVE_TRUTH = "ACTIVE_TRUTH"
    PROVISIONAL_TRUTH = "PROVISIONAL_TRUTH"
    CONFLICTING = "CONFLICTING"
    RETIRED = "RETIRED"
    REVEALED = "REVEALED"


class TruthSource(StrEnum):
    AUTHOR_MANUAL = "AUTHOR_MANUAL"
    INITIALIZATION_INFERRED = "INITIALIZATION_INFERRED"
    DISTILL_CANDIDATE = "DISTILL_CANDIDATE"
    CANON_DERIVED = "CANON_DERIVED"
    REVISION_DERIVED = "REVISION_DERIVED"
    AUTHOR_CONFIRMED = "AUTHOR_CONFIRMED"
    SOURCE_VERIFIED = "SOURCE_VERIFIED"


class CompatibilityStatus(StrEnum):
    COMPATIBLE = "COMPATIBLE"
    COMPATIBLE_WITH_GAPS = "COMPATIBLE_WITH_GAPS"
    CONFLICTING = "CONFLICTING"
    REQUIRES_REVISION = "REQUIRES_REVISION"
    UNKNOWN = "UNKNOWN"


class CompatibilityVerdict(StrEnum):
    SUPPORTING = "SUPPORTING"
    NO_CONTRADICTION = "NO_CONTRADICTION"
    CAUTION = "CAUTION"
    CONTRADICTION = "CONTRADICTION"
    REVISION_REQUIRED = "REVISION_REQUIRED"


SAFE_COMPATIBILITY = {
    CompatibilityStatus.COMPATIBLE,
    CompatibilityStatus.COMPATIBLE_WITH_GAPS,
}


class TruthCompatibilityEvidenceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    verdict: CompatibilityVerdict
    chapter_id: str | None = None
    chapter_ordinal: int | None = Field(default=None, ge=1)
    source_span_id: str | None = None
    evidence_quote: str = ""
    explanation: str = ""

    @model_validator(mode="after")
    def evidence_is_auditable(self) -> TruthCompatibilityEvidenceInput:
        if self.verdict in {
            CompatibilityVerdict.CONTRADICTION,
            CompatibilityVerdict.REVISION_REQUIRED,
        } and not (self.source_span_id and self.evidence_quote.strip()):
            raise ValueError("冲突或修订证据必须包含 source_span_id 与 evidence_quote")
        return self


class AuthorTruthInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    truth_type: TruthType
    subject_type: str = Field(min_length=1)
    subject_id: str | None = None
    object_type: str | None = None
    object_id: str | None = None
    title: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    description: str = ""
    status: TruthStatus = TruthStatus.ACTIVE_TRUTH
    confidence: float = Field(default=1.0, ge=0, le=1)
    introduced_by: TruthSource = TruthSource.AUTHOR_MANUAL
    effective_from_chapter: int = Field(ge=1)
    effective_until_chapter: int | None = Field(default=None, ge=1)
    must_remain_true: bool = True
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    compatibility_evidence: list[TruthCompatibilityEvidenceInput] = Field(
        default_factory=list
    )

    @model_validator(mode="after")
    def valid_window(self) -> AuthorTruthInput:
        if (
            self.effective_until_chapter is not None
            and self.effective_until_chapter < self.effective_from_chapter
        ):
            raise ValueError("effective_until_chapter 不得早于 effective_from_chapter")
        if (
            self.introduced_by
            in {TruthSource.INITIALIZATION_INFERRED, TruthSource.DISTILL_CANDIDATE}
            and self.status is TruthStatus.ACTIVE_TRUTH
        ):
            raise ValueError("推断或蒸馏候选必须先作为 Secret Candidate 由作者确认")
        return self


def _loads(value: Any, fallback: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(str(value))
    except (TypeError, ValueError):
        return fallback


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _current_chapter(connection: sqlite3.Connection, book_id: str, edition_id: str) -> int:
    return max(
        (int(chapter["ordinal"]) for chapter in edition_chapters(connection, book_id, edition_id)),
        default=0,
    )


def _validate_scope(
    connection: sqlite3.Connection, book_id: str, edition_id: str
) -> None:
    book = connection.execute(
        "SELECT 1 FROM books WHERE book_id=?", (book_id,)
    ).fetchone()
    if book is None:
        raise ValueError("book 不存在")
    if edition_id != "base":
        edition = connection.execute(
            "SELECT 1 FROM editions WHERE book_id=? AND edition_id=?",
            (book_id, edition_id),
        ).fetchone()
        if edition is None:
            raise ValueError("edition 不存在")


def _validate_evidence(
    connection: sqlite3.Connection,
    book_id: str,
    evidence: TruthCompatibilityEvidenceInput,
) -> tuple[str | None, int | None, str | None]:
    chapter_id = evidence.chapter_id
    chapter_ordinal = evidence.chapter_ordinal
    source_span_id = evidence.source_span_id
    if source_span_id:
        row = connection.execute(
            "SELECT s.chapter_id, c.ordinal, s.excerpt "
            "FROM source_spans s LEFT JOIN chapters c ON c.chapter_id=s.chapter_id "
            "WHERE s.book_id=? AND s.span_id=?",
            (book_id, source_span_id),
        ).fetchone()
        if row is None:
            raise ValueError(f"compatibility evidence source span 不存在：{source_span_id}")
        found_chapter = None if row["chapter_id"] is None else str(row["chapter_id"])
        found_ordinal = None if row["ordinal"] is None else int(row["ordinal"])
        if chapter_id and found_chapter != chapter_id:
            raise ValueError("compatibility evidence chapter_id 与 source span 不一致")
        if chapter_ordinal and found_ordinal != chapter_ordinal:
            raise ValueError("compatibility evidence chapter_ordinal 与 source span 不一致")
        chapter_id = found_chapter
        chapter_ordinal = found_ordinal
        if evidence.evidence_quote.strip() and evidence.evidence_quote not in str(
            row["excerpt"] or ""
        ):
            chapter = connection.execute(
                "SELECT content FROM chapters WHERE book_id=? AND chapter_id=?",
                (book_id, found_chapter),
            ).fetchone()
            if chapter is None or evidence.evidence_quote not in str(chapter["content"]):
                raise ValueError("compatibility evidence_quote 不在引用的 Source 章节中")
    elif chapter_id:
        row = connection.execute(
            "SELECT ordinal FROM chapters WHERE book_id=? AND chapter_id=?",
            (book_id, chapter_id),
        ).fetchone()
        if row is None:
            raise ValueError("compatibility evidence chapter 不存在")
        found_ordinal = int(row["ordinal"])
        if chapter_ordinal and chapter_ordinal != found_ordinal:
            raise ValueError("compatibility evidence chapter ordinal 不一致")
        chapter_ordinal = found_ordinal
    return chapter_id, chapter_ordinal, source_span_id


def _coverage_complete(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    start: int,
    end: int,
) -> bool:
    if end < start:
        return True
    expected = end - start + 1
    row = connection.execute(
        "SELECT COUNT(DISTINCT chapter_ordinal) FROM source_state_chapter_coverage "
        "WHERE book_id=? AND edition_id=? AND chapter_ordinal BETWEEN ? AND ? "
        "AND status IN ('COMPLETE_NO_CHANGE', 'COMPLETE_WITH_CHANGES')",
        (book_id, edition_id, start, end),
    ).fetchone()
    return row is not None and int(row[0]) == expected


def _compatibility_result(
    connection: sqlite3.Connection,
    book_id: str,
    edition_id: str,
    effective_from: int,
    current_chapter: int,
    evidence: list[TruthCompatibilityEvidenceInput],
) -> tuple[CompatibilityStatus, str, str]:
    if effective_from > current_chapter:
        return (
            CompatibilityStatus.COMPATIBLE,
            "设定从未来章节生效，不会倒写已经发生的章节。",
            "FORWARD_ONLY",
        )
    verdicts = {item.verdict for item in evidence}
    if CompatibilityVerdict.CONTRADICTION in verdicts:
        return (
            CompatibilityStatus.CONFLICTING,
            "已存在明确 Source 反证；该真相不能激活，必须修改设定或进入 Revision。",
            "HIDDEN_ONLY",
        )
    if CompatibilityVerdict.REVISION_REQUIRED in verdicts:
        return (
            CompatibilityStatus.REQUIRES_REVISION,
            "该设定需要改变既有正文，只能通过 Revision 实现。",
            "HIDDEN_ONLY",
        )
    if not evidence:
        if effective_from == current_chapter:
            return (
                CompatibilityStatus.COMPATIBLE_WITH_GAPS,
                "设定从当前章节边界开始隐藏生效；不声明读者或角色此前已经知道。",
                "RETROACTIVE_HIDDEN_COMPATIBLE",
            )
        return (
            CompatibilityStatus.UNKNOWN,
            "尚无可审计的兼容性证据；保持 provisional，不改旧正文或历史知识。",
            "HIDDEN_ONLY",
        )
    complete = _coverage_complete(
        connection, book_id, edition_id, effective_from, current_chapter
    )
    if complete and CompatibilityVerdict.CAUTION not in verdicts:
        return (
            CompatibilityStatus.COMPATIBLE,
            f"第{effective_from}–{current_chapter}章已有完整状态覆盖，未发现明确冲突。",
            "RETROACTIVE_HIDDEN_COMPATIBLE",
        )
    return (
        CompatibilityStatus.COMPATIBLE_WITH_GAPS,
        f"第{effective_from}–{current_chapter}章未发现明确冲突，但覆盖仍有空白或注意项。",
        "RETROACTIVE_HIDDEN_COMPATIBLE",
    )


def _insert_evidence(
    connection: sqlite3.Connection,
    *,
    truth_id: str,
    book_id: str,
    edition_id: str,
    evidence: TruthCompatibilityEvidenceInput,
) -> str:
    chapter_id, chapter_ordinal, source_span_id = _validate_evidence(
        connection, book_id, evidence
    )
    evidence_id = f"truth-evidence-{uuid.uuid4().hex}"
    connection.execute(
        "INSERT INTO truth_compatibility_evidence("
        "evidence_id, truth_id, book_id, edition_id, verdict, chapter_id, "
        "chapter_ordinal, source_span_id, evidence_quote, explanation, created_at, version"
        ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
        (
            evidence_id,
            truth_id,
            book_id,
            edition_id,
            evidence.verdict.value,
            chapter_id,
            chapter_ordinal,
            source_span_id,
            evidence.evidence_quote.strip(),
            evidence.explanation.strip(),
            utc_now(),
        ),
    )
    return evidence_id


def _invalidate_truth_consumers(
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


def _truth_from_row(row: sqlite3.Row | dict[str, Any]) -> dict[str, Any]:
    item = dict(row)
    item["confidence"] = float(item["confidence"])
    item["must_remain_true"] = bool(item["must_remain_true"])
    item["tags"] = list(_loads(item.pop("tags_json", "[]"), []))
    item["metadata"] = dict(_loads(item.pop("metadata_json", "{}"), {}))
    item["requires_revision"] = item["compatibility_status"] in {
        CompatibilityStatus.CONFLICTING.value,
        CompatibilityStatus.REQUIRES_REVISION.value,
    }
    item["author_layer"] = "AUTHOR_TRUTH"
    return item


def get_author_truth(
    database: Database, book_id: str, edition_id: str, truth_id: str
) -> dict[str, Any]:
    database.initialize()
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM author_truths WHERE truth_id=? AND book_id=? AND edition_id=?",
            (truth_id, book_id, edition_id),
        ).fetchone()
        if row is None:
            raise ValueError("Author Truth 不存在")
        evidence_rows = connection.execute(
            "SELECT * FROM truth_compatibility_evidence WHERE truth_id=? "
            "ORDER BY active DESC, chapter_ordinal, created_at, evidence_id",
            (truth_id,),
        ).fetchall()
    truth = _truth_from_row(row)
    truth["compatibility_evidence"] = [
        {**dict(item), "active": bool(item["active"])} for item in evidence_rows
    ]
    return truth


def list_author_truths(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    chapter_ordinal: int | None = None,
    include_future: bool = False,
    include_retired: bool = False,
) -> list[dict[str, Any]]:
    database.initialize()
    sql = "SELECT * FROM author_truths WHERE book_id=? AND edition_id=?"
    params: list[Any] = [book_id, edition_id]
    if not include_retired:
        sql += " AND status<>'RETIRED'"
    if chapter_ordinal is not None and not include_future:
        sql += " AND effective_from_chapter<=? AND "
        sql += "(effective_until_chapter IS NULL OR effective_until_chapter>=?)"
        params.extend([chapter_ordinal, chapter_ordinal])
    sql += " ORDER BY effective_from_chapter, created_at, truth_id"
    with database.connect() as connection:
        rows = connection.execute(sql, tuple(params)).fetchall()
    return [_truth_from_row(row) for row in rows]


def create_author_truth(
    database: Database,
    book_id: str,
    edition_id: str,
    payload: AuthorTruthInput | dict[str, Any],
) -> dict[str, Any]:
    database.initialize()
    data = (
        payload
        if isinstance(payload, AuthorTruthInput)
        else AuthorTruthInput.model_validate(payload)
    )
    truth_id = f"truth-{uuid.uuid4().hex}"
    now = utc_now()
    with database.connect() as connection:
        _validate_scope(connection, book_id, edition_id)
        current_chapter = _current_chapter(connection, book_id, edition_id)
        for item in data.compatibility_evidence:
            _validate_evidence(connection, book_id, item)
        compatibility, summary, retroactive_scope = _compatibility_result(
            connection,
            book_id,
            edition_id,
            data.effective_from_chapter,
            current_chapter,
            data.compatibility_evidence,
        )
        status = data.status
        if status in {TruthStatus.ACTIVE_TRUTH, TruthStatus.REVEALED}:
            if compatibility is CompatibilityStatus.CONFLICTING:
                status = TruthStatus.CONFLICTING
            elif compatibility is CompatibilityStatus.REQUIRES_REVISION or (
                status is TruthStatus.ACTIVE_TRUTH
                and compatibility not in SAFE_COMPATIBILITY
            ):
                status = TruthStatus.PROVISIONAL_TRUTH
        connection.execute(
            "INSERT INTO author_truths("
            "truth_id, book_id, edition_id, truth_type, subject_type, subject_id, "
            "object_type, object_id, title, statement, description, status, confidence, "
            "introduced_by, effective_from_chapter, effective_until_chapter, "
            "retroactive_scope, compatibility_status, compatibility_summary, "
            "must_remain_true, tags_json, metadata_json, created_at, updated_at, version"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
            (
                truth_id,
                book_id,
                edition_id,
                data.truth_type.value,
                data.subject_type.strip().upper(),
                data.subject_id,
                data.object_type,
                data.object_id,
                data.title.strip(),
                data.statement.strip(),
                data.description.strip(),
                status.value,
                data.confidence,
                data.introduced_by.value,
                data.effective_from_chapter,
                data.effective_until_chapter,
                retroactive_scope,
                compatibility.value,
                summary,
                int(data.must_remain_true),
                _dumps(data.tags),
                _dumps(data.metadata),
                now,
                now,
            ),
        )
        for item in data.compatibility_evidence:
            _insert_evidence(
                connection,
                truth_id=truth_id,
                book_id=book_id,
                edition_id=edition_id,
                evidence=item,
            )
        if status in {TruthStatus.ACTIVE_TRUTH, TruthStatus.REVEALED}:
            _invalidate_truth_consumers(
                connection,
                book_id,
                edition_id,
                f"Author Truth {truth_id} 已加入规划边界",
            )
    return get_author_truth(database, book_id, edition_id, truth_id)


def evaluate_truth_compatibility(
    database: Database,
    book_id: str,
    edition_id: str,
    truth_id: str,
    *,
    evidence: list[TruthCompatibilityEvidenceInput | dict[str, Any]] | None = None,
) -> dict[str, Any]:
    database.initialize()
    parsed = [
        item
        if isinstance(item, TruthCompatibilityEvidenceInput)
        else TruthCompatibilityEvidenceInput.model_validate(item)
        for item in (evidence or [])
    ]
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM author_truths WHERE truth_id=? AND book_id=? AND edition_id=?",
            (truth_id, book_id, edition_id),
        ).fetchone()
        if row is None:
            raise ValueError("Author Truth 不存在")
        for item in parsed:
            _insert_evidence(
                connection,
                truth_id=truth_id,
                book_id=book_id,
                edition_id=edition_id,
                evidence=item,
            )
        evidence_rows = connection.execute(
            "SELECT verdict, chapter_id, chapter_ordinal, source_span_id, "
            "evidence_quote, explanation FROM truth_compatibility_evidence "
            "WHERE truth_id=? AND active=1 ORDER BY created_at, evidence_id",
            (truth_id,),
        ).fetchall()
        all_evidence = [
            TruthCompatibilityEvidenceInput.model_validate(dict(item))
            for item in evidence_rows
        ]
        current_chapter = _current_chapter(connection, book_id, edition_id)
        compatibility, summary, retroactive_scope = _compatibility_result(
            connection,
            book_id,
            edition_id,
            int(row["effective_from_chapter"]),
            current_chapter,
            all_evidence,
        )
        old_status = TruthStatus(str(row["status"]))
        if old_status in {TruthStatus.IDEA, TruthStatus.RETIRED}:
            status = old_status
        elif compatibility is CompatibilityStatus.CONFLICTING:
            status = TruthStatus.CONFLICTING
        elif compatibility is CompatibilityStatus.REQUIRES_REVISION:
            status = TruthStatus.PROVISIONAL_TRUTH
        elif compatibility in SAFE_COMPATIBILITY and old_status in {
            TruthStatus.PROVISIONAL_TRUTH,
            TruthStatus.CONFLICTING,
        }:
            status = TruthStatus.ACTIVE_TRUTH
        else:
            status = old_status
        connection.execute(
            "UPDATE author_truths SET compatibility_status=?, compatibility_summary=?, "
            "retroactive_scope=?, status=?, updated_at=?, version=version+1 WHERE truth_id=?",
            (
                compatibility.value,
                summary,
                retroactive_scope,
                status.value,
                utc_now(),
                truth_id,
            ),
        )
        if status != old_status or parsed:
            _invalidate_truth_consumers(
                connection,
                book_id,
                edition_id,
                f"Author Truth {truth_id} 兼容性已重新评估",
            )
    return get_author_truth(database, book_id, edition_id, truth_id)


def update_author_truth(
    database: Database,
    book_id: str,
    edition_id: str,
    truth_id: str,
    changes: dict[str, Any],
) -> dict[str, Any]:
    current = get_author_truth(database, book_id, edition_id, truth_id)
    allowed = {
        "truth_type",
        "subject_type",
        "subject_id",
        "object_type",
        "object_id",
        "title",
        "statement",
        "description",
        "status",
        "confidence",
        "introduced_by",
        "effective_from_chapter",
        "effective_until_chapter",
        "must_remain_true",
        "tags",
        "metadata",
    }
    unknown = set(changes) - allowed
    if unknown:
        raise ValueError(f"不可修改的 Author Truth 字段：{sorted(unknown)}")
    semantic_fields = {
        "truth_type",
        "subject_type",
        "subject_id",
        "object_type",
        "object_id",
        "statement",
        "effective_from_chapter",
        "effective_until_chapter",
    }
    semantic_changed = any(
        key in changes and changes[key] != current.get(key) for key in semantic_fields
    )
    payload = {
        key: current[key]
        for key in allowed
        if key in current
    }
    payload.update(changes)
    payload["compatibility_evidence"] = [
        {
            key: item.get(key)
            for key in (
                "verdict",
                "chapter_id",
                "chapter_ordinal",
                "source_span_id",
                "evidence_quote",
                "explanation",
            )
        }
        for item in current.get("compatibility_evidence", [])
        if bool(item.get("active", True)) and not semantic_changed
    ]
    data = AuthorTruthInput.model_validate(payload)
    with database.connect() as connection:
        if semantic_changed:
            connection.execute(
                "UPDATE truth_compatibility_evidence SET active=0 "
                "WHERE truth_id=? AND active=1",
                (truth_id,),
            )
        current_chapter = _current_chapter(connection, book_id, edition_id)
        compatibility, summary, retroactive_scope = _compatibility_result(
            connection,
            book_id,
            edition_id,
            data.effective_from_chapter,
            current_chapter,
            data.compatibility_evidence,
        )
        status = data.status
        if status in {TruthStatus.ACTIVE_TRUTH, TruthStatus.REVEALED}:
            if compatibility is CompatibilityStatus.CONFLICTING:
                status = TruthStatus.CONFLICTING
            elif compatibility is CompatibilityStatus.REQUIRES_REVISION or (
                status is TruthStatus.ACTIVE_TRUTH
                and compatibility not in SAFE_COMPATIBILITY
            ):
                status = TruthStatus.PROVISIONAL_TRUTH
        connection.execute(
            "UPDATE author_truths SET truth_type=?, subject_type=?, subject_id=?, "
            "object_type=?, object_id=?, title=?, statement=?, description=?, status=?, "
            "confidence=?, introduced_by=?, effective_from_chapter=?, "
            "effective_until_chapter=?, retroactive_scope=?, compatibility_status=?, "
            "compatibility_summary=?, must_remain_true=?, tags_json=?, metadata_json=?, "
            "updated_at=?, version=version+1 WHERE truth_id=?",
            (
                data.truth_type.value,
                data.subject_type.strip().upper(),
                data.subject_id,
                data.object_type,
                data.object_id,
                data.title.strip(),
                data.statement.strip(),
                data.description.strip(),
                status.value,
                data.confidence,
                data.introduced_by.value,
                data.effective_from_chapter,
                data.effective_until_chapter,
                retroactive_scope,
                compatibility.value,
                summary,
                int(data.must_remain_true),
                _dumps(data.tags),
                _dumps(data.metadata),
                utc_now(),
                truth_id,
            ),
        )
        _invalidate_truth_consumers(
            connection, book_id, edition_id, f"Author Truth {truth_id} 已修改"
        )
    return get_author_truth(database, book_id, edition_id, truth_id)


def create_open_creative_question(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    title: str,
    question: str,
    subject_type: str | None = None,
    subject_id: str | None = None,
    horizon: str = "LONG",
) -> dict[str, Any]:
    database.initialize()
    if not title.strip() or not question.strip():
        raise ValueError("Open Creative Question 的标题和问题不能为空")
    question_id = f"open-question-{uuid.uuid4().hex}"
    now = utc_now()
    with database.connect() as connection:
        _validate_scope(connection, book_id, edition_id)
        connection.execute(
            "INSERT INTO open_creative_questions("
            "question_id, book_id, edition_id, title, question, subject_type, subject_id, "
            "horizon, status, created_at, updated_at, version"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'OPEN_QUESTION', ?, ?, 1)",
            (
                question_id,
                book_id,
                edition_id,
                title.strip(),
                question.strip(),
                subject_type,
                subject_id,
                horizon.upper(),
                now,
                now,
            ),
        )
    return {"question_id": question_id, "status": "OPEN_QUESTION"}


def list_open_creative_questions(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    include_resolved: bool = False,
) -> list[dict[str, Any]]:
    database.initialize()
    sql = (
        "SELECT * FROM open_creative_questions WHERE book_id=? AND edition_id=?"
    )
    if not include_resolved:
        sql += " AND status='OPEN_QUESTION'"
    sql += " ORDER BY created_at, question_id"
    with database.connect() as connection:
        return [
            dict(row)
            for row in connection.execute(sql, (book_id, edition_id)).fetchall()
        ]


def create_secret_candidate(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    title: str,
    statement: str,
    truth_type: TruthType | str = TruthType.CUSTOM,
    subject_type: str | None = None,
    subject_id: str | None = None,
    evidence: list[dict[str, Any]] | None = None,
    confidence: float = 0.5,
    source: TruthSource | str = TruthSource.INITIALIZATION_INFERRED,
) -> dict[str, Any]:
    database.initialize()
    if not title.strip() or not statement.strip():
        raise ValueError("Secret Candidate 的标题和候选陈述不能为空")
    candidate_id = f"secret-candidate-{uuid.uuid4().hex}"
    now = utc_now()
    selected_type = TruthType(str(truth_type).upper())
    selected_source = TruthSource(str(source).upper())
    if not 0 <= confidence <= 1:
        raise ValueError("confidence 必须在 0 到 1 之间")
    with database.connect() as connection:
        _validate_scope(connection, book_id, edition_id)
        connection.execute(
            "INSERT INTO secret_candidates("
            "candidate_id, book_id, edition_id, title, statement, truth_type, "
            "subject_type, subject_id, evidence_json, confidence, source, status, "
            "created_at, updated_at, version"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
            "'INFERRED_SECRET_CANDIDATE', ?, ?, 1)",
            (
                candidate_id,
                book_id,
                edition_id,
                title.strip(),
                statement.strip(),
                selected_type.value,
                subject_type,
                subject_id,
                _dumps(evidence or []),
                confidence,
                selected_source.value,
                now,
                now,
            ),
        )
    return {
        "candidate_id": candidate_id,
        "status": "INFERRED_SECRET_CANDIDATE",
        "planning_role": "SOFT_POSSIBILITY_ONLY",
    }


def list_secret_candidates(
    database: Database,
    book_id: str,
    edition_id: str,
    *,
    include_resolved: bool = False,
) -> list[dict[str, Any]]:
    database.initialize()
    sql = "SELECT * FROM secret_candidates WHERE book_id=? AND edition_id=?"
    if not include_resolved:
        sql += " AND status='INFERRED_SECRET_CANDIDATE'"
    sql += " ORDER BY created_at, candidate_id"
    with database.connect() as connection:
        rows = connection.execute(sql, (book_id, edition_id)).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["evidence"] = list(_loads(item.pop("evidence_json", "[]"), []))
        item["confidence"] = float(item["confidence"])
        item["planning_role"] = (
            "SOFT_POSSIBILITY_ONLY"
            if item["status"] == "INFERRED_SECRET_CANDIDATE"
            else "RESOLVED"
        )
        result.append(item)
    return result


def resolve_secret_candidate(
    database: Database,
    book_id: str,
    edition_id: str,
    candidate_id: str,
    *,
    action: str,
    effective_from_chapter: int | None = None,
    compatibility_evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    database.initialize()
    selected = action.strip().upper()
    if selected not in {"CONFIRM_TRUTH", "KEEP_OPEN", "REJECT"}:
        raise ValueError("Secret Candidate action 无效")
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM secret_candidates WHERE candidate_id=? AND book_id=? "
            "AND edition_id=?",
            (candidate_id, book_id, edition_id),
        ).fetchone()
        if row is None:
            raise ValueError("Secret Candidate 不存在")
        if str(row["status"]) != "INFERRED_SECRET_CANDIDATE":
            raise ValueError("Secret Candidate 已处理")
        current = _current_chapter(connection, book_id, edition_id)
    truth: dict[str, Any] | None = None
    question: dict[str, Any] | None = None
    if selected == "CONFIRM_TRUTH":
        truth = create_author_truth(
            database,
            book_id,
            edition_id,
            {
                "truth_type": str(row["truth_type"]),
                "subject_type": str(row["subject_type"] or "CUSTOM"),
                "subject_id": row["subject_id"],
                "title": str(row["title"]),
                "statement": str(row["statement"]),
                "description": "由作者确认的 Hidden Truth Candidate。",
                "status": "ACTIVE_TRUTH",
                "confidence": float(row["confidence"]),
                "introduced_by": "AUTHOR_CONFIRMED",
                "effective_from_chapter": effective_from_chapter or max(current, 1),
                "compatibility_evidence": compatibility_evidence or [],
            },
        )
    elif selected == "KEEP_OPEN":
        question = create_open_creative_question(
            database,
            book_id,
            edition_id,
            title=str(row["title"]),
            question=f"是否采用候选隐藏设定：{row['statement']}",
            subject_type=(
                None if row["subject_type"] is None else str(row["subject_type"])
            ),
            subject_id=(None if row["subject_id"] is None else str(row["subject_id"])),
        )
    status = {
        "CONFIRM_TRUTH": "AUTHOR_CONFIRMED",
        "KEEP_OPEN": "OPEN_QUESTION",
        "REJECT": "REJECTED",
    }[selected]
    with database.connect() as connection:
        connection.execute(
            "UPDATE secret_candidates SET status=?, resolved_truth_id=?, updated_at=?, "
            "version=version+1 WHERE candidate_id=?",
            (status, None if truth is None else truth["truth_id"], utc_now(), candidate_id),
        )
    return {
        "candidate_id": candidate_id,
        "status": status,
        "truth": truth,
        "open_question": question,
    }


__all__ = [
    "AuthorTruthInput",
    "CompatibilityStatus",
    "CompatibilityVerdict",
    "TruthCompatibilityEvidenceInput",
    "TruthSource",
    "TruthStatus",
    "TruthType",
    "create_author_truth",
    "create_open_creative_question",
    "create_secret_candidate",
    "evaluate_truth_compatibility",
    "get_author_truth",
    "list_author_truths",
    "list_open_creative_questions",
    "list_secret_candidates",
    "resolve_secret_candidate",
    "update_author_truth",
]
