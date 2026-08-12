"""Explainable serial chapter intent recommendations and author overrides."""

from __future__ import annotations

import json
import uuid
from collections.abc import Mapping, Sequence
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from novel_authoring.db.database import Database
from novel_authoring.planning.innovation import NarrativeDebt, NarrativeDebtType
from novel_authoring.progression.anticipation import AnticipationSurfaceView
from novel_authoring.progression.models import PayoffChannel
from novel_authoring.utils import json_dumps, utc_now


class ChapterIntent(StrEnum):
    CONTINUITY_ADVANCE = "CONTINUITY_ADVANCE"
    PROGRESSION_SETUP = "PROGRESSION_SETUP"
    BREAKTHROUGH = "BREAKTHROUGH"
    POWER_VERIFICATION = "POWER_VERIFICATION"
    RESOURCE_OPPORTUNITY = "RESOURCE_OPPORTUNITY"
    RESOURCE_CONVERSION = "RESOURCE_CONVERSION"
    WORLD_EXPANSION = "WORLD_EXPANSION"
    MYSTERY_ADVANCE = "MYSTERY_ADVANCE"
    MYSTERY_PAYOFF = "MYSTERY_PAYOFF"
    FACTION_CONFLICT = "FACTION_CONFLICT"
    STATUS_RISE = "STATUS_RISE"
    TEAM_GROWTH = "TEAM_GROWTH"
    RELATIONSHIP_ADVANCE = "RELATIONSHIP_ADVANCE"
    RECOVERY = "RECOVERY"
    AFTERMATH = "AFTERMATH"
    TRANSITION = "TRANSITION"
    EXPLORATION = "EXPLORATION"
    CUSTOM = "CUSTOM"


class ChapterIntentRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_intent: ChapterIntent
    secondary_intents: list[ChapterIntent] = Field(default_factory=list, max_length=2)
    why_now: list[str] = Field(min_length=1)
    supporting_debt_ids: list[str] = Field(default_factory=list)
    supporting_anticipation_ids: list[str] = Field(default_factory=list)
    supporting_thread_ids: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    alternatives: list[ChapterIntent] = Field(default_factory=list)
    author_override_applied: bool = False

    @model_validator(mode="after")
    def validate_distinct_intents(self) -> ChapterIntentRecommendation:
        if self.primary_intent in self.secondary_intents:
            raise ValueError("primary intent 不得重复出现在 secondary intents")
        return self


class SchedulerOverride(BaseModel):
    model_config = ConfigDict(extra="forbid")

    override_id: str
    book_id: str
    edition_id: str
    chapter_ordinal: int = Field(ge=0)
    primary_intent: ChapterIntent
    secondary_intents: list[ChapterIntent] = Field(default_factory=list, max_length=2)
    reason: str = Field(min_length=1)
    created_at: str
    updated_at: str


_DEBT_INTENTS: dict[NarrativeDebtType, ChapterIntent] = {
    NarrativeDebtType.PLOT: ChapterIntent.CONTINUITY_ADVANCE,
    NarrativeDebtType.MYSTERY: ChapterIntent.MYSTERY_PAYOFF,
    NarrativeDebtType.RELATIONSHIP: ChapterIntent.RELATIONSHIP_ADVANCE,
    NarrativeDebtType.PROGRESSION: ChapterIntent.PROGRESSION_SETUP,
    NarrativeDebtType.POWER_SHOWCASE: ChapterIntent.POWER_VERIFICATION,
    NarrativeDebtType.RESOURCE: ChapterIntent.RESOURCE_CONVERSION,
    NarrativeDebtType.WORLD_EXPANSION: ChapterIntent.WORLD_EXPANSION,
    NarrativeDebtType.STATUS: ChapterIntent.STATUS_RISE,
    NarrativeDebtType.TEAM: ChapterIntent.TEAM_GROWTH,
    NarrativeDebtType.ANTICIPATION: ChapterIntent.CONTINUITY_ADVANCE,
}

_PAYOFF_INTENTS: dict[PayoffChannel, ChapterIntent] = {
    PayoffChannel.POWER_BREAKTHROUGH: ChapterIntent.BREAKTHROUGH,
    PayoffChannel.NEW_ABILITY: ChapterIntent.POWER_VERIFICATION,
    PayoffChannel.RESOURCE_GAIN: ChapterIntent.RESOURCE_OPPORTUNITY,
    PayoffChannel.MYSTERY_REVEAL: ChapterIntent.MYSTERY_PAYOFF,
    PayoffChannel.WORLD_EXPANSION: ChapterIntent.WORLD_EXPANSION,
    PayoffChannel.FACTION_ADVANCE: ChapterIntent.FACTION_CONFLICT,
    PayoffChannel.TEAM_GROWTH: ChapterIntent.TEAM_GROWTH,
    PayoffChannel.RELATIONSHIP_ADVANCE: ChapterIntent.RELATIONSHIP_ADVANCE,
    PayoffChannel.KNOWLEDGE_GAIN: ChapterIntent.MYSTERY_ADVANCE,
    PayoffChannel.DISCOVERY: ChapterIntent.EXPLORATION,
    PayoffChannel.TRANSFORMATION: ChapterIntent.PROGRESSION_SETUP,
    PayoffChannel.MASTERY: ChapterIntent.POWER_VERIFICATION,
    PayoffChannel.STRATEGIC_ADVANTAGE: ChapterIntent.CONTINUITY_ADVANCE,
    PayoffChannel.CUSTOM: ChapterIntent.CUSTOM,
}


def _intent_from_task(tasks: Sequence[Mapping[str, Any]]) -> ChapterIntent | None:
    intent_values = {item.value for item in ChapterIntent}
    for task in tasks:
        raw = task.get("chapter_intent") or task.get("intent")
        if raw and str(raw) in intent_values:
            return ChapterIntent(str(raw))
    return None


def recommend_chapter_intent(
    *,
    debts: Sequence[NarrativeDebt],
    anticipation: AnticipationSurfaceView,
    author_tasks: Sequence[Mapping[str, Any]] = (),
    active_thread_ids: Sequence[str] = (),
    immediate_aftermath: bool = False,
    recovery_needed: bool = False,
    override: SchedulerOverride | None = None,
) -> ChapterIntentRecommendation:
    """Recommend a function without creating a plot event or a mandatory schedule."""

    if override is not None:
        return ChapterIntentRecommendation(
            primary_intent=override.primary_intent,
            secondary_intents=override.secondary_intents,
            why_now=[f"作者 Override：{override.reason}"],
            supporting_thread_ids=list(active_thread_ids),
            author_override_applied=True,
        )
    author_intent = _intent_from_task(author_tasks)
    if author_intent is not None:
        return ChapterIntentRecommendation(
            primary_intent=author_intent,
            why_now=["当前有效 Author Task 指定了章节功能"],
            supporting_thread_ids=list(active_thread_ids),
            alternatives=[ChapterIntent.CONTINUITY_ADVANCE],
        )
    if immediate_aftermath:
        primary = ChapterIntent.AFTERMATH
        reasons = ["上一事件存在必须承接的即时余波"]
    elif recovery_needed:
        primary = ChapterIntent.RECOVERY
        reasons = ["当前压力与消耗支持恢复章节"]
    else:
        prioritized_debts = sorted(
            debts,
            key=lambda item: (item.debt_score or 0, item.opened_chapter),
            reverse=True,
        )
        top_anticipation = anticipation.items[0] if anticipation.items else None
        if prioritized_debts and (prioritized_debts[0].debt_score or 0) >= 40:
            primary = _DEBT_INTENTS[prioritized_debts[0].debt_type]
            reasons = [
                f"{prioritized_debts[0].debt_type.value} Debt 已进入近期推进区间"
            ]
        elif top_anticipation is not None:
            primary = _PAYOFF_INTENTS.get(
                top_anticipation.expected_payoff_channel,
                ChapterIntent.CONTINUITY_ADVANCE,
            )
            reasons = [f"当前最高读者期待来自 {top_anticipation.source.value}"]
        else:
            primary = ChapterIntent.CONTINUITY_ADVANCE
            reasons = ["没有成熟债务或强期待，优先承接当前活跃线程"]
    secondary: list[ChapterIntent] = []
    if anticipation.items:
        secondary_candidate = _PAYOFF_INTENTS.get(
            anticipation.items[0].expected_payoff_channel
        )
        if secondary_candidate is not None and secondary_candidate is not primary:
            secondary.append(secondary_candidate)
    return ChapterIntentRecommendation(
        primary_intent=primary,
        secondary_intents=secondary[:2],
        why_now=reasons,
        supporting_debt_ids=[
            debt.debt_id for debt in debts if (debt.debt_score or 0) >= 40
        ],
        supporting_anticipation_ids=[item.anticipation_id for item in anticipation.items[:3]],
        supporting_thread_ids=list(active_thread_ids),
        risks=(
            ["期待项持续增加；本建议不代表必须立即兑现"]
            if len(anticipation.items) > 5
            else []
        ),
        alternatives=[
            intent
            for intent in (ChapterIntent.CONTINUITY_ADVANCE, ChapterIntent.TRANSITION)
            if intent is not primary
        ],
    )


def save_scheduler_override(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
    chapter_ordinal: int,
    primary_intent: ChapterIntent,
    secondary_intents: Sequence[ChapterIntent] = (),
    reason: str,
) -> SchedulerOverride:
    database.initialize()
    now = utc_now()
    override_id = f"scheduler-override-{uuid.uuid4().hex}"
    with database.connect() as connection:
        connection.execute(
            """
            INSERT INTO serial_scheduler_overrides(
                override_id, book_id, edition_id, chapter_ordinal, primary_intent,
                secondary_intents_json, reason, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(book_id, edition_id, chapter_ordinal) DO UPDATE SET
                primary_intent=excluded.primary_intent,
                secondary_intents_json=excluded.secondary_intents_json,
                reason=excluded.reason,
                updated_at=excluded.updated_at,
                version=serial_scheduler_overrides.version+1
            """,
            (
                override_id,
                book_id,
                edition_id,
                chapter_ordinal,
                primary_intent.value,
                json_dumps([item.value for item in secondary_intents]),
                reason,
                now,
                now,
            ),
        )
    saved = load_scheduler_override(
        database,
        book_id=book_id,
        edition_id=edition_id,
        chapter_ordinal=chapter_ordinal,
    )
    if saved is None:
        raise RuntimeError("Scheduler Override 持久化失败")
    return saved


def load_scheduler_override(
    database: Database,
    *,
    book_id: str,
    edition_id: str,
    chapter_ordinal: int,
) -> SchedulerOverride | None:
    database.initialize()
    with database.connect() as connection:
        row = connection.execute(
            """
            SELECT * FROM serial_scheduler_overrides
            WHERE book_id=? AND edition_id=? AND chapter_ordinal=?
            """,
            (book_id, edition_id, chapter_ordinal),
        ).fetchone()
    if row is None:
        return None
    return SchedulerOverride(
        override_id=str(row["override_id"]),
        book_id=str(row["book_id"]),
        edition_id=str(row["edition_id"]),
        chapter_ordinal=int(row["chapter_ordinal"]),
        primary_intent=ChapterIntent(str(row["primary_intent"])),
        secondary_intents=[
            ChapterIntent(str(value))
            for value in json.loads(str(row["secondary_intents_json"]))
        ],
        reason=str(row["reason"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


__all__ = [
    "ChapterIntent",
    "ChapterIntentRecommendation",
    "SchedulerOverride",
    "load_scheduler_override",
    "recommend_chapter_intent",
    "save_scheduler_override",
]
