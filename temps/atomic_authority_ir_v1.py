"""Experimental Atomic Authority IR v1.

This module deliberately separates two products:

1. AtomicAuthorityContract: hard facts compiled only from Frozen Authority IR.
2. PrimaryPreservationMap: edit-locality and exact-fragment protection derived from
   Primary realization plus optional Curator location hints.

Curator and Primary cannot create hard facts, source conflicts, entity identity, or
chapter obligations. The module is experimental and is not wired into production.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field, replace
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence


ENTITY_ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9_:-]{2,127}$")
FACT_ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9_:-]{2,127}$")
SLOT_ID_PATTERN = re.compile(
    r"^[a-z][a-z0-9_]*(?::[A-Za-z0-9_.-]+)+$"
)
NARRATIVE_FUNCTION_ID_PATTERN = re.compile(
    r"^[a-z][a-z0-9_.:-]{2,127}$"
)
ENTITY_AUTHORITY_REF_PATTERN = re.compile(
    r"^(?:canon|world|power|human|mission|reader_release|character|authority|book_[a-z0-9]+)\."
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {str(key): _deep_freeze(item) for key, item in value.items()}
        )
    if isinstance(value, (list, tuple)):
        return tuple(_deep_freeze(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(_deep_freeze(item) for item in value)
    return value


def _deep_thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _deep_thaw(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_deep_thaw(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted(_deep_thaw(item) for item in value)
    return value


class IRValidationError(ValueError):
    """The typed Authority IR is invalid or unsupported."""


class SourcePurityError(IRValidationError):
    """A realization-layer source attempted to create hard Authority."""


class EntityKind(str, Enum):
    CHARACTER = "character"
    MANIFESTATION = "manifestation"
    FACTION = "faction"
    ORGANIZATION = "organization"
    LOCATION = "location"
    ITEM = "item"
    RESOURCE = "resource"
    CONTRACT = "contract"
    ROUTE = "route"
    POWER_TIER = "power_tier"
    ABILITY = "ability"
    GROUP = "group"
    MYSTERY = "mystery"
    EVENT = "event"


class AuthoritySource(str, Enum):
    FROZEN_MISSION = "frozen_mission"
    CANON = "canon"
    WORLD_AUTHORITY = "world_authority"
    POWER_AUTHORITY = "power_authority"
    HUMAN_AUTHORITY = "human_authority"
    READER_RELEASE = "reader_release"


ALLOWED_HARD_SOURCES = frozenset(AuthoritySource)
FORBIDDEN_HARD_SOURCE_NAMES = frozenset(
    {
        "primary",
        "primary_draft",
        "curator",
        "curator_audit",
        "curator_realization",
        "writer",
        "reviser",
        "judge",
    }
)

AUTHORITY_ARTIFACT_PREFIX = {
    AuthoritySource.FROZEN_MISSION: "mission:",
    AuthoritySource.CANON: "canon:",
    AuthoritySource.WORLD_AUTHORITY: "world:",
    AuthoritySource.POWER_AUTHORITY: "power:",
    AuthoritySource.HUMAN_AUTHORITY: "human:",
    AuthoritySource.READER_RELEASE: "reader_release:",
}


class FactKind(str, Enum):
    EVENT = "event"
    ACTION = "action"
    DIRECT_RESULT = "direct_result"
    STATE_TRANSITION = "state_transition"
    ENDING = "ending"
    POWER_TRANSITION = "power_transition"
    RESOURCE_TRANSITION = "resource_transition"
    OWNERSHIP_TRANSITION = "ownership_transition"
    RELATIONSHIP_TRANSITION = "relationship_transition"
    DEADLINE = "deadline"
    PUBLIC_PROOF = "public_proof"
    READER_RELEASE = "reader_release"
    UNKNOWN_BOUNDARY = "unknown_boundary"
    ABILITY_BOUNDARY = "ability_boundary"
    HISTORICAL_CLAIM_BOUNDARY = "historical_claim_boundary"


class FactMode(str, Enum):
    MUST_HOLD = "must_hold"
    TERMINAL = "terminal"
    MUST_NOT_HOLD = "must_not_hold"
    MUST_REMAIN_UNKNOWN = "must_remain_unknown"
    CONDITIONAL = "conditional"


class FactPhase(str, Enum):
    PRE_CHAPTER = "pre_chapter"
    DURING_CHAPTER = "during_chapter"
    CHAPTER_END = "chapter_end"
    POST_CHAPTER = "post_chapter"
    READER_KNOWLEDGE = "reader_knowledge"


HISTORICAL_CLAIM_DOMAINS = frozenset(
    {
        "money",
        "resource",
        "relationship_promise",
        "mystery",
        "action_basis",
        "ownership",
        "threat",
    }
)

ALLOWED_METADATA_KEYS: dict[FactKind, frozenset[str]] = {
    FactKind.EVENT: frozenset(),
    FactKind.ACTION: frozenset(),
    FactKind.DIRECT_RESULT: frozenset(),
    FactKind.STATE_TRANSITION: frozenset(),
    FactKind.ENDING: frozenset(),
    FactKind.POWER_TRANSITION: frozenset(),
    FactKind.RESOURCE_TRANSITION: frozenset(
        {"payment_state", "fulfillment", "amount"}
    ),
    FactKind.OWNERSHIP_TRANSITION: frozenset(),
    FactKind.RELATIONSHIP_TRANSITION: frozenset(),
    FactKind.DEADLINE: frozenset(
        {"relation", "timing", "not_current_terminal_departure"}
    ),
    FactKind.PUBLIC_PROOF: frozenset(
        {"performance_fact_id", "ruler", "required_consequence"}
    ),
    FactKind.READER_RELEASE: frozenset(),
    FactKind.UNKNOWN_BOUNDARY: frozenset(),
    FactKind.ABILITY_BOUNDARY: frozenset(),
    FactKind.HISTORICAL_CLAIM_BOUNDARY: frozenset(
        {"domain", "criticality", "allowed_claim_ids"}
    ),
}

ALLOWED_VALUE_KEYS: dict[FactKind, frozenset[str]] = {
    FactKind.STATE_TRANSITION: frozenset(
        {"enables", "not_purified_into_selfless_rescue"}
    ),
    FactKind.RESOURCE_TRANSITION: frozenset({"fulfillment", "amount"}),
    FactKind.ABILITY_BOUNDARY: frozenset(
        {
            "max_cycles_this_chapter",
            "requires_cooldown_after",
            "allowed",
            "full_body_power",
            "damage_is_real",
        }
    ),
}


class PreservationProvenance(str, Enum):
    PRIMARY_REALIZATION = "primary_realization"
    CURATOR_LOCATION_HINT = "curator_location_hint"
    MANUAL_EXPERIMENT = "manual_experiment"


class PatchKind(str, Enum):
    REPLACE = "replace"
    DELETE = "delete"
    INSERT_BEFORE = "insert_before"
    INSERT_AFTER = "insert_after"


class PreflightRoute(str, Enum):
    CURRENT_FULL_REVISER_UNGATED = "current_full_reviser_ungated"
    ATOMIC_FAST_ROUTE = "atomic_fast_route"


class FinalRoute(str, Enum):
    ADOPT_DELTA = "adopt_delta"
    FULL_REVISER_THEN_SUPPORTED_GATE = "full_reviser_then_supported_gate"
    FULL_REVISER_UNGATED = "full_reviser_ungated"
    CURRENT_FULL_REVISER_FINAL_UNGATED = "current_full_reviser_final_ungated"
    FINAL_AFTER_SUPPORTED_FULL = "final_after_supported_full"
    FULL_REVISER_RESIDUAL_FAILURE = "full_reviser_residual_failure"


class DirectorField(str, Enum):
    TRIGGER_EVENT = "trigger_event"
    EVENT_DRIVER = "event_driver"
    PROTAGONIST_ACTION = "protagonist_action"
    WORLD_REACTION = "world_reaction"
    DIRECT_RESULT = "direct_result"
    STATE_CHANGE = "state_change"
    ENDING_DRIVE = "ending_drive"


@dataclass(frozen=True)
class EntityRecord:
    entity_id: str
    kind: EntityKind
    display_name: str
    aliases: tuple[str, ...] = ()
    authority_refs: tuple[str, ...] = ()
    parent_entity_id: str = ""

    def __post_init__(self) -> None:
        if not ENTITY_ID_PATTERN.fullmatch(self.entity_id):
            raise IRValidationError(f"invalid entity_id={self.entity_id!r}")
        if not self.display_name.strip():
            raise IRValidationError(f"empty display_name for {self.entity_id}")
        if not self.authority_refs:
            raise IRValidationError(f"entity {self.entity_id} lacks Authority provenance")
        invalid_refs = [
            ref for ref in self.authority_refs
            if not ENTITY_AUTHORITY_REF_PATTERN.match(ref)
        ]
        if invalid_refs:
            raise SourcePurityError(
                f"entity {self.entity_id} has non-Authority provenance refs={invalid_refs}"
            )

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["kind"] = self.kind.value
        value["aliases"] = list(self.aliases)
        value["authority_refs"] = list(self.authority_refs)
        return value


@dataclass(frozen=True)
class EntityRegistry:
    chapter_id: str
    protagonist_id: str
    entities: Mapping[str, EntityRecord]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "entities",
            MappingProxyType(dict(self.entities)),
        )
        if self.protagonist_id not in self.entities:
            raise IRValidationError(
                f"protagonist_id={self.protagonist_id!r} is not in Entity Registry"
            )
        if self.entities[self.protagonist_id].kind != EntityKind.CHARACTER:
            raise IRValidationError("protagonist_id must reference a character entity")
        for entity in self.entities.values():
            if entity.parent_entity_id and entity.parent_entity_id not in self.entities:
                raise IRValidationError(
                    f"entity {entity.entity_id} references unknown parent {entity.parent_entity_id}"
                )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "EntityRegistry":
        records: dict[str, EntityRecord] = {}
        for raw in payload.get("entities", []):
            record = EntityRecord(
                entity_id=str(raw["entity_id"]),
                kind=EntityKind(str(raw["kind"])),
                display_name=str(raw["display_name"]),
                aliases=tuple(str(item) for item in raw.get("aliases", [])),
                authority_refs=tuple(
                    str(item) for item in raw.get("authority_refs", [])
                ),
                parent_entity_id=str(raw.get("parent_entity_id", "")),
            )
            if record.entity_id in records:
                raise IRValidationError(f"duplicate entity_id={record.entity_id}")
            records[record.entity_id] = record
        return cls(
            chapter_id=str(payload["chapter_id"]),
            protagonist_id=str(payload["protagonist_id"]),
            entities=records,
        )

    def require(self, entity_id: str) -> EntityRecord:
        try:
            return self.entities[entity_id]
        except KeyError as exc:
            raise IRValidationError(f"unknown entity_id={entity_id}") from exc

    def resolve_surface(self, text: str) -> set[str]:
        """Resolve explicit names/aliases for realization evidence only.

        This method never creates or changes entity identity in the hard contract.
        Ambiguous aliases return all matching IDs so the caller can fail closed.
        """

        found: set[str] = set()
        for entity_id, entity in self.entities.items():
            surfaces = (entity.display_name, *entity.aliases)
            if any(surface and surface in text for surface in surfaces):
                found.add(entity_id)
        return found

    def resolve_unique_surface(self, text: str) -> str:
        """Resolve exactly one entity or fail closed for realization mapping."""

        matches = self.resolve_surface(text)
        if len(matches) != 1:
            raise IRValidationError(
                f"surface must resolve to exactly one entity; matches={sorted(matches)}"
            )
        return next(iter(matches))

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "entity-registry-v1",
            "chapter_id": self.chapter_id,
            "protagonist_id": self.protagonist_id,
            "entities": [
                self.entities[key].to_dict() for key in sorted(self.entities)
            ],
        }


@dataclass(frozen=True)
class AuthorityFact:
    fact_id: str
    slot_id: str
    source: AuthoritySource
    source_ref: str
    kind: FactKind
    mode: FactMode
    phase: FactPhase
    actor_id: str = ""
    action_id: str = ""
    object_ids: tuple[str, ...] = ()
    counterparty_ids: tuple[str, ...] = ()
    from_state: str = ""
    to_state: str = ""
    value: Any = None
    terminal: bool = False
    condition_fact_ids: tuple[str, ...] = ()
    depends_on_fact_ids: tuple[str, ...] = ()
    condition_slots: tuple[str, ...] = ()
    depends_on_slots: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not FACT_ID_PATTERN.fullmatch(self.fact_id):
            raise IRValidationError(f"invalid fact_id={self.fact_id!r}")
        if not SLOT_ID_PATTERN.fullmatch(self.slot_id):
            raise IRValidationError(
                f"fact {self.fact_id} has invalid stable slot_id={self.slot_id!r}"
            )
        if not self.source_ref.strip():
            raise IRValidationError(f"fact {self.fact_id} lacks source_ref")
        if self.kind in {
            FactKind.ACTION,
            FactKind.DIRECT_RESULT,
            FactKind.ENDING,
            FactKind.POWER_TRANSITION,
            FactKind.RESOURCE_TRANSITION,
            FactKind.OWNERSHIP_TRANSITION,
            FactKind.RELATIONSHIP_TRANSITION,
        } and not self.actor_id:
            raise IRValidationError(f"fact {self.fact_id} requires actor_id")
        if self.kind in {
            FactKind.ACTION,
            FactKind.DIRECT_RESULT,
            FactKind.ENDING,
        } and not self.action_id:
            raise IRValidationError(f"fact {self.fact_id} requires action_id")

        if self.terminal != (self.mode == FactMode.TERMINAL):
            raise IRValidationError(
                f"fact {self.fact_id} terminal flag/mode mismatch: "
                f"terminal={self.terminal} mode={self.mode.value}"
            )
        if self.kind == FactKind.UNKNOWN_BOUNDARY:
            if self.mode != FactMode.MUST_REMAIN_UNKNOWN or self.terminal:
                raise IRValidationError(
                    f"unknown boundary {self.fact_id} must be nonterminal must_remain_unknown"
                )
        if self.kind == FactKind.ENDING:
            if (
                self.mode != FactMode.TERMINAL
                or self.phase != FactPhase.CHAPTER_END
                or not self.terminal
            ):
                raise IRValidationError(
                    f"ending {self.fact_id} must be terminal at chapter_end"
                )
        if self.kind == FactKind.DEADLINE:
            if (
                self.mode != FactMode.MUST_HOLD
                or self.phase != FactPhase.POST_CHAPTER
                or self.terminal
            ):
                raise IRValidationError(
                    f"deadline {self.fact_id} must remain nonterminal post_chapter"
                )
        if self.kind == FactKind.READER_RELEASE:
            if self.phase != FactPhase.READER_KNOWLEDGE or self.terminal:
                raise IRValidationError(
                    f"reader release {self.fact_id} must be nonterminal reader_knowledge"
                )
        if self.kind == FactKind.POWER_TRANSITION:
            if (
                self.mode != FactMode.TERMINAL
                or self.phase != FactPhase.CHAPTER_END
                or not self.from_state
                or not self.to_state
            ):
                raise IRValidationError(
                    f"power transition {self.fact_id} requires terminal chapter_end from/to state"
                )
        if self.kind == FactKind.HISTORICAL_CLAIM_BOUNDARY:
            domain = str(self.metadata.get("domain", ""))
            criticality = str(self.metadata.get("criticality", ""))
            if (
                self.mode != FactMode.MUST_NOT_HOLD
                or self.terminal
                or domain not in HISTORICAL_CLAIM_DOMAINS
                or criticality != "state_bearing"
            ):
                raise IRValidationError(
                    f"historical boundary {self.fact_id} must be nonterminal must_not_hold "
                    "with an allowed state-bearing domain"
                )

        try:
            json.dumps(self.value, ensure_ascii=False, sort_keys=True)
            json.dumps(dict(self.metadata), ensure_ascii=False, sort_keys=True)
        except (TypeError, ValueError) as exc:
            raise IRValidationError(
                f"fact {self.fact_id} contains non-JSON-safe value/metadata"
            ) from exc
        allowed_metadata = ALLOWED_METADATA_KEYS[self.kind]
        unknown_metadata = set(self.metadata) - allowed_metadata
        if unknown_metadata:
            raise IRValidationError(
                f"fact {self.fact_id} has unsupported metadata keys={sorted(unknown_metadata)}"
            )
        if isinstance(self.value, Mapping):
            allowed_value = ALLOWED_VALUE_KEYS.get(self.kind, frozenset())
            unknown_value = set(self.value) - allowed_value
            if unknown_value:
                raise IRValidationError(
                    f"fact {self.fact_id} has unsupported value keys={sorted(unknown_value)}"
                )
        object.__setattr__(self, "value", _deep_freeze(self.value))
        object.__setattr__(self, "metadata", _deep_freeze(self.metadata))

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "AuthorityFact":
        raw_source = str(payload["source"]).strip().lower()
        if raw_source in FORBIDDEN_HARD_SOURCE_NAMES:
            raise SourcePurityError(
                f"realization source {raw_source!r} cannot create Hard Authority"
            )
        try:
            source = AuthoritySource(raw_source)
        except ValueError as exc:
            raise SourcePurityError(
                f"source {raw_source!r} is not an allowed Frozen Authority source"
            ) from exc
        return cls(
            fact_id=str(payload["fact_id"]),
            slot_id=str(payload["slot_id"]),
            source=source,
            source_ref=str(payload["source_ref"]),
            kind=FactKind(str(payload["kind"])),
            mode=FactMode(str(payload["mode"])),
            phase=FactPhase(str(payload["phase"])),
            actor_id=str(payload.get("actor_id", "")),
            action_id=str(payload.get("action_id", "")),
            object_ids=tuple(str(item) for item in payload.get("object_ids", [])),
            counterparty_ids=tuple(
                str(item) for item in payload.get("counterparty_ids", [])
            ),
            from_state=str(payload.get("from_state", "")),
            to_state=str(payload.get("to_state", "")),
            value=payload.get("value"),
            terminal=bool(payload.get("terminal", False)),
            condition_fact_ids=tuple(
                str(item) for item in payload.get("condition_fact_ids", [])
            ),
            depends_on_fact_ids=tuple(
                str(item) for item in payload.get("depends_on_fact_ids", [])
            ),
            condition_slots=tuple(
                str(item) for item in payload.get("condition_slots", [])
            ),
            depends_on_slots=tuple(
                str(item) for item in payload.get("depends_on_slots", [])
            ),
            metadata=dict(payload.get("metadata", {})),
        )

    def canonical_signature(self) -> tuple[Any, ...]:
        return (
            self.kind.value,
            self.mode.value,
            self.actor_id,
            self.action_id,
            self.object_ids,
            self.counterparty_ids,
            self.from_state,
            self.to_state,
            json.dumps(_deep_thaw(self.value), ensure_ascii=False, sort_keys=True),
            self.terminal,
            self.condition_slots,
            self.depends_on_slots,
            json.dumps(_deep_thaw(self.metadata), ensure_ascii=False, sort_keys=True),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "fact_id": self.fact_id,
            "slot_id": self.slot_id,
            "source": self.source.value,
            "source_ref": self.source_ref,
            "kind": self.kind.value,
            "mode": self.mode.value,
            "phase": self.phase.value,
            "actor_id": self.actor_id,
            "action_id": self.action_id,
            "object_ids": list(self.object_ids),
            "counterparty_ids": list(self.counterparty_ids),
            "from_state": self.from_state,
            "to_state": self.to_state,
            "value": _deep_thaw(self.value),
            "terminal": self.terminal,
            "condition_fact_ids": list(self.condition_fact_ids),
            "depends_on_fact_ids": list(self.depends_on_fact_ids),
            "condition_slots": list(self.condition_slots),
            "depends_on_slots": list(self.depends_on_slots),
            "metadata": _deep_thaw(self.metadata),
        }


_TRUSTED_ARTIFACT_ISSUER = object()


def _authority_artifact_digest(facts: Sequence[AuthorityFact]) -> str:
    return hashlib.sha256(
        json.dumps(
            [fact.to_dict() for fact in facts],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


@dataclass(frozen=True)
class FrozenAuthorityArtifact:
    """A source-specific frozen artifact issued by a trusted Runtime path."""

    source: AuthoritySource
    artifact_id: str
    revision_sha256: str
    facts: tuple[AuthorityFact, ...]
    _issuer: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._issuer is not _TRUSTED_ARTIFACT_ISSUER:
            raise SourcePurityError(
                "FrozenAuthorityArtifact must be issued by a trusted source-specific freezer"
            )
        prefix = AUTHORITY_ARTIFACT_PREFIX[self.source]
        if not self.artifact_id.startswith(prefix):
            raise SourcePurityError(
                f"artifact_id={self.artifact_id!r} must start with {prefix!r}"
            )
        if not SHA256_PATTERN.fullmatch(self.revision_sha256):
            raise SourcePurityError(
                f"artifact {self.artifact_id} has invalid revision_sha256"
            )
        if any(fact.source != self.source for fact in self.facts):
            raise SourcePurityError(
                f"artifact {self.artifact_id} contains mismatched fact source"
            )
        expected_digest = _authority_artifact_digest(self.facts)
        if self.revision_sha256 != expected_digest:
            raise SourcePurityError(
                f"artifact {self.artifact_id} revision digest does not match facts"
            )


def _freeze_authority_artifact(
    source: AuthoritySource,
    artifact_id: str,
    raw_facts: Sequence[Mapping[str, Any] | AuthorityFact],
) -> FrozenAuthorityArtifact:
    """Internal source-specific constructor; raw payload source labels are ignored."""

    normalized: list[AuthorityFact] = []
    for index, raw in enumerate(raw_facts, 1):
        if isinstance(raw, AuthorityFact):
            payload = raw.to_dict()
        else:
            payload = dict(raw)
        payload["source"] = source.value
        payload["source_ref"] = f"{artifact_id}#fact:{index}"
        normalized.append(AuthorityFact.from_dict(payload))
    digest = _authority_artifact_digest(normalized)
    return FrozenAuthorityArtifact(
        source=source,
        artifact_id=artifact_id,
        revision_sha256=digest,
        facts=tuple(normalized),
        _issuer=_TRUSTED_ARTIFACT_ISSUER,
    )


def freeze_mission_artifact(
    artifact_id: str,
    facts: Sequence[Mapping[str, Any] | AuthorityFact],
) -> FrozenAuthorityArtifact:
    return _freeze_authority_artifact(
        AuthoritySource.FROZEN_MISSION, artifact_id, facts
    )


def freeze_canon_artifact(
    artifact_id: str,
    facts: Sequence[Mapping[str, Any] | AuthorityFact],
) -> FrozenAuthorityArtifact:
    return _freeze_authority_artifact(AuthoritySource.CANON, artifact_id, facts)


def freeze_world_artifact(
    artifact_id: str,
    facts: Sequence[Mapping[str, Any] | AuthorityFact],
) -> FrozenAuthorityArtifact:
    return _freeze_authority_artifact(
        AuthoritySource.WORLD_AUTHORITY, artifact_id, facts
    )


def freeze_power_artifact(
    artifact_id: str,
    facts: Sequence[Mapping[str, Any] | AuthorityFact],
) -> FrozenAuthorityArtifact:
    return _freeze_authority_artifact(
        AuthoritySource.POWER_AUTHORITY, artifact_id, facts
    )


def freeze_human_artifact(
    artifact_id: str,
    facts: Sequence[Mapping[str, Any] | AuthorityFact],
) -> FrozenAuthorityArtifact:
    return _freeze_authority_artifact(
        AuthoritySource.HUMAN_AUTHORITY, artifact_id, facts
    )


def freeze_reader_release_artifact(
    artifact_id: str,
    facts: Sequence[Mapping[str, Any] | AuthorityFact],
) -> FrozenAuthorityArtifact:
    return _freeze_authority_artifact(
        AuthoritySource.READER_RELEASE, artifact_id, facts
    )


@dataclass(frozen=True)
class AtomicAuthorityContract:
    chapter_id: str
    registry: EntityRegistry
    facts: Mapping[str, AuthorityFact]
    artifacts: tuple[FrozenAuthorityArtifact, ...]
    conflicts: tuple[str, ...]
    unsupported: tuple[str, ...]
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "facts", MappingProxyType(dict(self.facts)))
        object.__setattr__(self, "artifacts", tuple(self.artifacts))
        object.__setattr__(self, "conflicts", tuple(self.conflicts))
        object.__setattr__(self, "unsupported", tuple(self.unsupported))
        object.__setattr__(self, "diagnostics", tuple(self.diagnostics))

    @property
    def preflight_eligible(self) -> bool:
        return not self.conflicts and not self.unsupported

    @property
    def contract_hash(self) -> str:
        payload = {
            "chapter_id": self.chapter_id,
            "registry": self.registry.to_dict(),
            "artifacts": [
                {
                    "source": artifact.source.value,
                    "artifact_id": artifact.artifact_id,
                    "revision_sha256": artifact.revision_sha256,
                }
                for artifact in self.artifacts
            ],
            "facts": [self.facts[key].to_dict() for key in sorted(self.facts)],
            "conflicts": sorted(self.conflicts),
            "unsupported": sorted(self.unsupported),
        }
        raw = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def require_fact(self, fact_id: str) -> AuthorityFact:
        try:
            return self.facts[fact_id]
        except KeyError as exc:
            raise IRValidationError(f"unknown fact_id={fact_id}") from exc

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "atomic-authority-contract-v1",
            "chapter_id": self.chapter_id,
            "protagonist_id": self.registry.protagonist_id,
            "contract_hash": self.contract_hash,
            "preflight_eligible": self.preflight_eligible,
            "hard_sources": sorted({fact.source.value for fact in self.facts.values()}),
            "artifact_provenance": [
                {
                    "source": artifact.source.value,
                    "artifact_id": artifact.artifact_id,
                    "revision_sha256": artifact.revision_sha256,
                    "fact_ids": [fact.fact_id for fact in artifact.facts],
                }
                for artifact in self.artifacts
            ],
            "registry": self.registry.to_dict(),
            "facts": [self.facts[key].to_dict() for key in sorted(self.facts)],
            "conflicts": list(self.conflicts),
            "unsupported": list(self.unsupported),
            "diagnostics": list(self.diagnostics),
        }


    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "AtomicAuthorityContract":
        """Reload and re-verify a serialized Contract snapshot.

        This is distinct from `load_contract_payload()`, which loads a trusted
        pre-merge Runtime envelope. Snapshot loading reconstructs every source
        artifact, rechecks its digest, rebuilds conflicts/unsupported state, and
        compares the final Contract hash.
        """

        if str(payload.get("schema_version", "")) != "atomic-authority-contract-v1":
            raise IRValidationError(
                "Atomic Authority Contract requires schema_version=atomic-authority-contract-v1"
            )
        registry = EntityRegistry.from_dict(payload["registry"])
        if str(payload.get("chapter_id", "")) != registry.chapter_id:
            raise IRValidationError("Contract chapter_id does not match Registry")
        if str(payload.get("protagonist_id", "")) != registry.protagonist_id:
            raise IRValidationError("Contract protagonist_id does not match Registry")

        fact_rows = list(payload.get("facts", []))
        facts: dict[str, AuthorityFact] = {}
        for raw in fact_rows:
            current = AuthorityFact.from_dict(raw)
            if current.fact_id in facts:
                raise IRValidationError(
                    f"duplicate fact_id in Contract snapshot={current.fact_id}"
                )
            facts[current.fact_id] = current

        freezers = {
            AuthoritySource.FROZEN_MISSION: freeze_mission_artifact,
            AuthoritySource.CANON: freeze_canon_artifact,
            AuthoritySource.WORLD_AUTHORITY: freeze_world_artifact,
            AuthoritySource.POWER_AUTHORITY: freeze_power_artifact,
            AuthoritySource.HUMAN_AUTHORITY: freeze_human_artifact,
            AuthoritySource.READER_RELEASE: freeze_reader_release_artifact,
        }
        assigned: set[str] = set()
        builder = AtomicAuthorityContractBuilder(registry)
        for row in payload.get("artifact_provenance", []):
            source = AuthoritySource(str(row["source"]))
            fact_ids = tuple(str(item) for item in row.get("fact_ids", []))
            if not fact_ids:
                raise IRValidationError(
                    f"artifact {row.get('artifact_id')} has no fact_ids"
                )
            repeated = assigned.intersection(fact_ids)
            if repeated:
                raise IRValidationError(
                    f"facts assigned to multiple artifacts={sorted(repeated)}"
                )
            missing = [fact_id for fact_id in fact_ids if fact_id not in facts]
            if missing:
                raise IRValidationError(
                    f"artifact references unknown fact_ids={missing}"
                )
            current_facts = [facts[fact_id] for fact_id in fact_ids]
            if any(fact.source != source for fact in current_facts):
                raise SourcePurityError(
                    f"artifact {row.get('artifact_id')} source does not match assigned facts"
                )
            artifact = freezers[source](str(row["artifact_id"]), current_facts)
            if artifact.revision_sha256 != str(row["revision_sha256"]):
                raise SourcePurityError(
                    f"artifact {artifact.artifact_id} snapshot digest mismatch"
                )
            builder.add_artifact(artifact)
            assigned.update(fact_ids)

        unassigned = set(facts) - assigned
        if unassigned:
            raise IRValidationError(
                f"Contract facts lack artifact provenance={sorted(unassigned)}"
            )
        for diagnostic in payload.get("diagnostics", []):
            builder.add_diagnostic(str(diagnostic))
        contract = builder.build()
        if contract.contract_hash != str(payload.get("contract_hash", "")):
            raise SourcePurityError("Atomic Authority Contract snapshot hash mismatch")
        if list(contract.conflicts) != list(payload.get("conflicts", [])):
            raise IRValidationError("Contract conflict snapshot mismatch")
        if list(contract.unsupported) != list(payload.get("unsupported", [])):
            raise IRValidationError("Contract unsupported snapshot mismatch")
        if contract.preflight_eligible != bool(payload.get("preflight_eligible")):
            raise IRValidationError("Contract preflight_eligible snapshot mismatch")
        return contract


class AtomicAuthorityContractBuilder:
    """Merge typed Frozen Authority fragments without Curator/Primary input."""

    def __init__(self, registry: EntityRegistry) -> None:
        self.registry = registry
        self._artifacts: list[FrozenAuthorityArtifact] = []
        self._diagnostics: list[str] = []

    def add_artifact(self, artifact: FrozenAuthorityArtifact) -> None:
        if not isinstance(artifact, FrozenAuthorityArtifact):
            raise SourcePurityError(
                "Hard Authority must arrive as a source-specific FrozenAuthorityArtifact"
            )
        expected_digest = _authority_artifact_digest(artifact.facts)
        if artifact.revision_sha256 != expected_digest:
            raise SourcePurityError(
                f"artifact {artifact.artifact_id} digest no longer matches its facts"
            )
        self._artifacts.append(artifact)

    def add_fact(self, fact: AuthorityFact) -> None:
        raise SourcePurityError(
            "raw AuthorityFact injection is forbidden; use a source-specific frozen artifact"
        )

    def add_fragment(self, payload: Mapping[str, Any]) -> None:
        raise SourcePurityError(
            "self-labelled fragment injection is forbidden; use a source-specific frozen artifact"
        )

    def add_diagnostic(self, note: str) -> None:
        """Diagnostics may be recorded, but never become hard conflict/fact."""
        if note.strip():
            self._diagnostics.append(note.strip())

    def build(self) -> AtomicAuthorityContract:
        facts: dict[str, AuthorityFact] = {}
        conflicts: list[str] = []
        unsupported: list[str] = []

        if not self._artifacts:
            unsupported.append("Atomic Authority Contract has no frozen artifacts")

        artifact_ids: set[str] = set()
        for artifact in self._artifacts:
            if artifact.artifact_id in artifact_ids:
                conflicts.append(
                    f"duplicate Authority artifact_id={artifact.artifact_id}"
                )
            artifact_ids.add(artifact.artifact_id)

        for artifact in self._artifacts:
            for fact in artifact.facts:
                if fact.fact_id in facts:
                    conflicts.append(f"duplicate fact_id={fact.fact_id}")
                    continue
                facts[fact.fact_id] = fact

        if not facts:
            unsupported.append("Atomic Authority Contract has no hard facts")

        for fact in facts.values():
            if (
                fact.kind
                in {
                    FactKind.STATE_TRANSITION,
                    FactKind.POWER_TRANSITION,
                    FactKind.RESOURCE_TRANSITION,
                    FactKind.OWNERSHIP_TRANSITION,
                    FactKind.RELATIONSHIP_TRANSITION,
                }
                and fact.mode == FactMode.TERMINAL
                and fact.phase == FactPhase.CHAPTER_END
                and not fact.from_state
            ):
                unsupported.append(
                    f"terminal transition {fact.fact_id} lacks explicit from_state"
                )
            referenced_entities = [
                fact.actor_id,
                *fact.object_ids,
                *fact.counterparty_ids,
            ]
            for entity_id in referenced_entities:
                if entity_id and entity_id not in self.registry.entities:
                    unsupported.append(
                        f"fact {fact.fact_id} references unknown entity_id={entity_id}"
                    )
            for dependency in (*fact.condition_fact_ids, *fact.depends_on_fact_ids):
                if dependency not in facts:
                    unsupported.append(
                        f"fact {fact.fact_id} references unknown dependency={dependency}"
                    )

        known_slots = {fact.slot_id for fact in facts.values()}
        facts_by_slot: dict[str, set[str]] = {}
        for fact in facts.values():
            facts_by_slot.setdefault(fact.slot_id, set()).add(fact.fact_id)
        for fact in facts.values():
            for slot in (*fact.condition_slots, *fact.depends_on_slots):
                if slot not in known_slots:
                    unsupported.append(
                        f"fact {fact.fact_id} references unknown stable slot={slot}"
                    )

        dependency_graph: dict[str, set[str]] = {
            fact_id: set() for fact_id in facts
        }
        for fact in facts.values():
            dependency_graph[fact.fact_id].update(fact.condition_fact_ids)
            dependency_graph[fact.fact_id].update(fact.depends_on_fact_ids)
            for slot in (*fact.condition_slots, *fact.depends_on_slots):
                dependency_graph[fact.fact_id].update(
                    facts_by_slot.get(slot, set())
                )
            dependency_graph[fact.fact_id].discard(fact.fact_id)
            if fact.fact_id in fact.condition_fact_ids or fact.fact_id in fact.depends_on_fact_ids:
                conflicts.append(
                    f"fact {fact.fact_id} cannot depend on itself"
                )
            if fact.slot_id in (*fact.condition_slots, *fact.depends_on_slots):
                conflicts.append(
                    f"fact {fact.fact_id} cannot depend on its own stable slot={fact.slot_id}"
                )

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(fact_id: str, path: tuple[str, ...]) -> None:
            if fact_id in visiting:
                cycle = " -> ".join((*path, fact_id))
                conflicts.append(f"Authority dependency cycle: {cycle}")
                return
            if fact_id in visited or fact_id not in dependency_graph:
                return
            visiting.add(fact_id)
            for dependency in sorted(dependency_graph[fact_id]):
                visit(dependency, (*path, fact_id))
            visiting.remove(fact_id)
            visited.add(fact_id)

        for fact_id in sorted(dependency_graph):
            visit(fact_id, ())

        if self.registry.protagonist_id not in self.registry.entities:
            unsupported.append("registry protagonist_id is unresolved")

        by_slot_phase: dict[tuple[str, FactPhase], list[AuthorityFact]] = {}
        for fact in facts.values():
            by_slot_phase.setdefault((fact.slot_id, fact.phase), []).append(fact)
        for (slot_id, phase), group in by_slot_phase.items():
            signatures = {fact.canonical_signature() for fact in group}
            if len(signatures) > 1:
                refs = ", ".join(
                    f"{fact.fact_id}@{fact.source.value}:{fact.source_ref}"
                    for fact in group
                )
                conflicts.append(
                    f"incompatible Authority facts for slot={slot_id} phase={phase.value}: {refs}"
                )

        # Validate typed transitions against an explicit pre-chapter state when one
        # exists. No source priority is used to guess a winner.
        pre_states: dict[str, str] = {}
        for fact in facts.values():
            if fact.phase != FactPhase.PRE_CHAPTER:
                continue
            state = fact.to_state or (
                str(fact.value) if fact.value is not None else ""
            )
            if state:
                existing = pre_states.get(fact.slot_id)
                if existing and existing != state:
                    conflicts.append(
                        f"pre-chapter state conflict slot={fact.slot_id}: {existing!r} vs {state!r}"
                    )
                pre_states[fact.slot_id] = state
        for fact in facts.values():
            if not fact.from_state:
                continue
            current = pre_states.get(fact.slot_id)
            if current is None:
                unsupported.append(
                    f"transition {fact.fact_id} declares from_state={fact.from_state!r} "
                    f"but no pre-chapter state exists for slot={fact.slot_id}"
                )
            elif current != fact.from_state:
                conflicts.append(
                    f"transition {fact.fact_id} expects from_state={fact.from_state!r} "
                    f"but Canon has {current!r} for slot={fact.slot_id}"
                )

        return AtomicAuthorityContract(
            chapter_id=self.registry.chapter_id,
            registry=self.registry,
            facts=facts,
            artifacts=tuple(self._artifacts),
            conflicts=tuple(sorted(set(conflicts))),
            unsupported=tuple(sorted(set(unsupported))),
            diagnostics=tuple(self._diagnostics),
        )


_PRIMARY_EVIDENCE_ISSUER = object()


@dataclass(frozen=True)
class FactEvidenceBinding:
    fact_id: str
    paragraph_ids: tuple[int, ...]
    provenance: PreservationProvenance
    primary_sha256: str
    note: str = ""
    _issuer: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._issuer is not _PRIMARY_EVIDENCE_ISSUER:
            raise IRValidationError(
                "FactEvidenceBinding must be issued by bind_primary_realization()"
            )
        if self.provenance != PreservationProvenance.PRIMARY_REALIZATION:
            raise IRValidationError(
                "FactEvidenceBinding can only represent Primary realization evidence"
            )
        if not self.paragraph_ids or any(item < 1 for item in self.paragraph_ids):
            raise IRValidationError(
                "FactEvidenceBinding requires positive paragraph_ids"
            )
        if not SHA256_PATTERN.fullmatch(self.primary_sha256):
            raise IRValidationError(
                "FactEvidenceBinding requires primary_sha256"
            )


def bind_primary_realization(
    *,
    fact_id: str,
    paragraph_ids: Sequence[int],
    primary_body: str,
    note: str = "",
) -> FactEvidenceBinding:
    return FactEvidenceBinding(
        fact_id=fact_id,
        paragraph_ids=tuple(sorted(set(int(item) for item in paragraph_ids))),
        provenance=PreservationProvenance.PRIMARY_REALIZATION,
        primary_sha256=hashlib.sha256(primary_body.encode("utf-8")).hexdigest(),
        note=note,
        _issuer=_PRIMARY_EVIDENCE_ISSUER,
    )


@dataclass(frozen=True)
class ProtectionHint:
    paragraph_id: int
    exact_fragment: str
    provenance: PreservationProvenance
    note: str = ""

    def __post_init__(self) -> None:
        if self.paragraph_id < 1:
            raise IRValidationError("ProtectionHint paragraph_id must be positive")
        if not self.exact_fragment.strip():
            raise IRValidationError("ProtectionHint exact_fragment cannot be empty")


@dataclass(frozen=True)
class RepairTarget:
    fact_ids: tuple[str, ...]
    locality_radius: int = 0

    def __post_init__(self) -> None:
        if not self.fact_ids:
            raise IRValidationError("RepairTarget requires at least one blocker fact_id")
        if self.locality_radius not in {0, 1}:
            raise IRValidationError(
                "RepairTarget locality_radius must be 0 or 1; arbitrary window expansion is forbidden"
            )


@dataclass(frozen=True)
class PatchOperation:
    kind: PatchKind
    start: int
    end: int
    payload: str = ""

    def __post_init__(self) -> None:
        if self.start < 1 or self.end < self.start:
            raise IRValidationError(
                f"invalid patch range start={self.start} end={self.end}"
            )
        if self.kind in {PatchKind.REPLACE, PatchKind.INSERT_BEFORE, PatchKind.INSERT_AFTER} and not self.payload.strip():
            raise IRValidationError(f"{self.kind.value} requires payload")
        if self.kind == PatchKind.DELETE and self.payload:
            raise IRValidationError("delete operation cannot carry payload")


@dataclass(frozen=True)
class PrimaryPreservationMap:
    chapter_id: str
    contract_hash: str
    paragraph_hashes: Mapping[int, str]
    fact_evidence: Mapping[str, tuple[int, ...]]
    editable_paragraph_ids: frozenset[int]
    locked_paragraph_ids: frozenset[int]
    protection_hints: tuple[ProtectionHint, ...]
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "paragraph_hashes",
            MappingProxyType(dict(self.paragraph_hashes)),
        )
        object.__setattr__(
            self,
            "fact_evidence",
            MappingProxyType(
                {
                    str(key): tuple(value)
                    for key, value in self.fact_evidence.items()
                }
            ),
        )
        object.__setattr__(
            self,
            "editable_paragraph_ids",
            frozenset(self.editable_paragraph_ids),
        )
        object.__setattr__(
            self,
            "locked_paragraph_ids",
            frozenset(self.locked_paragraph_ids),
        )
        object.__setattr__(self, "protection_hints", tuple(self.protection_hints))
        object.__setattr__(self, "diagnostics", tuple(self.diagnostics))

    @property
    def paragraph_count(self) -> int:
        return len(self.paragraph_hashes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "primary-preservation-map-v1",
            "chapter_id": self.chapter_id,
            "contract_hash": self.contract_hash,
            "paragraph_count": self.paragraph_count,
            "paragraph_hashes": {
                str(key): value
                for key, value in sorted(self.paragraph_hashes.items())
            },
            "fact_evidence": {
                key: list(value) for key, value in sorted(self.fact_evidence.items())
            },
            "editable_paragraph_ids": sorted(self.editable_paragraph_ids),
            "locked_paragraph_ids": sorted(self.locked_paragraph_ids),
            "protection_hints": [asdict(item) | {"provenance": item.provenance.value} for item in self.protection_hints],
            "diagnostics": list(self.diagnostics),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "PrimaryPreservationMap":
        if str(payload.get("schema_version", "")) != "primary-preservation-map-v1":
            raise IRValidationError(
                "Primary Preservation Map requires schema_version=primary-preservation-map-v1"
            )
        paragraph_hashes = {
            int(key): str(value)
            for key, value in dict(payload.get("paragraph_hashes", {})).items()
        }
        paragraph_count = int(payload.get("paragraph_count", 0))
        if set(paragraph_hashes) != set(range(1, paragraph_count + 1)):
            raise IRValidationError(
                "Primary Preservation Map paragraph_hashes do not cover 1..paragraph_count"
            )
        editable = {int(item) for item in payload.get("editable_paragraph_ids", [])}
        locked = {int(item) for item in payload.get("locked_paragraph_ids", [])}
        if editable & locked or editable | locked != set(range(1, paragraph_count + 1)):
            raise IRValidationError(
                "Primary Preservation Map editable/locked partition is invalid"
            )
        return cls(
            chapter_id=str(payload["chapter_id"]),
            contract_hash=str(payload["contract_hash"]),
            paragraph_hashes=paragraph_hashes,
            fact_evidence={
                str(key): tuple(int(item) for item in value)
                for key, value in dict(payload.get("fact_evidence", {})).items()
            },
            editable_paragraph_ids=editable,
            locked_paragraph_ids=locked,
            protection_hints=tuple(
                ProtectionHint(
                    paragraph_id=int(item["paragraph_id"]),
                    exact_fragment=str(item["exact_fragment"]),
                    provenance=PreservationProvenance(str(item["provenance"])),
                    note=str(item.get("note", "")),
                )
                for item in payload.get("protection_hints", [])
            ),
            diagnostics=[str(item) for item in payload.get("diagnostics", [])],
        )



def split_paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]


def paragraph_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_primary_preservation_map(
    *,
    contract: AtomicAuthorityContract,
    primary_body: str,
    evidence_bindings: Sequence[FactEvidenceBinding],
    repair_target: RepairTarget,
    protection_hints: Sequence[ProtectionHint] = (),
) -> PrimaryPreservationMap:
    """Build edit locality from Primary/Curator realization, never hard facts."""

    paragraphs = split_paragraphs(primary_body)
    valid_ids = set(range(1, len(paragraphs) + 1))
    fact_evidence: dict[str, tuple[int, ...]] = {}
    diagnostics: list[str] = []
    primary_sha256 = hashlib.sha256(primary_body.encode("utf-8")).hexdigest()

    for binding in evidence_bindings:
        if binding._issuer is not _PRIMARY_EVIDENCE_ISSUER:
            raise IRValidationError(
                "untrusted Primary evidence binding"
            )
        if binding.primary_sha256 != primary_sha256:
            raise IRValidationError(
                f"Primary evidence binding for {binding.fact_id} targets a stale/different Primary"
            )
        contract.require_fact(binding.fact_id)
        paragraph_ids = tuple(sorted(set(binding.paragraph_ids)))
        unknown = set(paragraph_ids) - valid_ids
        if unknown:
            raise IRValidationError(
                f"evidence for {binding.fact_id} references unknown paragraphs={sorted(unknown)}"
            )
        existing = set(fact_evidence.get(binding.fact_id, ()))
        fact_evidence[binding.fact_id] = tuple(
            sorted(existing | set(paragraph_ids))
        )
        if binding.note:
            diagnostics.append(
                f"{binding.provenance.value}:{binding.fact_id}:{binding.note}"
            )

    editable: set[int] = set()
    for fact_id in repair_target.fact_ids:
        contract.require_fact(fact_id)
        locations = fact_evidence.get(fact_id, ())
        if not locations:
            raise IRValidationError(
                f"repair target fact {fact_id} has no Primary realization location"
            )
        editable.update(locations)
    radius = repair_target.locality_radius
    expanded: set[int] = set()
    for paragraph_id in editable:
        expanded.update(
            range(
                max(1, paragraph_id - radius),
                min(len(paragraphs), paragraph_id + radius) + 1,
            )
        )
    editable = expanded
    locked = valid_ids - editable

    clean_hints: list[ProtectionHint] = []
    for hint in protection_hints:
        if hint.paragraph_id not in valid_ids:
            raise IRValidationError(
                f"protection hint references unknown paragraph={hint.paragraph_id}"
            )
        if hint.exact_fragment not in paragraphs[hint.paragraph_id - 1]:
            raise IRValidationError(
                f"protected fragment is not present in P{hint.paragraph_id:03d}"
            )
        clean_hints.append(hint)
        if hint.paragraph_id not in editable:
            diagnostics.append(
                f"hint P{hint.paragraph_id:03d} remains safe through paragraph lock; it did not expand edit authority"
            )

    return PrimaryPreservationMap(
        chapter_id=contract.chapter_id,
        contract_hash=contract.contract_hash,
        paragraph_hashes={
            index: paragraph_hash(paragraph)
            for index, paragraph in enumerate(paragraphs, 1)
        },
        fact_evidence=fact_evidence,
        editable_paragraph_ids=editable,
        locked_paragraph_ids=locked,
        protection_hints=tuple(clean_hints),
        diagnostics=diagnostics,
    )


def validate_edit_locality(
    preservation: PrimaryPreservationMap,
    operations: Sequence[PatchOperation],
) -> list[str]:
    violations: list[str] = []
    for operation in operations:
        if operation.kind in {PatchKind.REPLACE, PatchKind.DELETE}:
            touched = set(range(operation.start, operation.end + 1))
        else:
            touched = {operation.start}
        forbidden = touched - preservation.editable_paragraph_ids
        if forbidden:
            violations.append(
                f"{operation.kind.value} touches locked paragraphs={sorted(forbidden)}"
            )
    return violations


def apply_patch_operations(
    primary_body: str,
    operations: Sequence[PatchOperation],
) -> str:
    paragraphs = split_paragraphs(primary_body)
    for operation in sorted(operations, key=lambda item: (item.start, item.end), reverse=True):
        start = operation.start - 1
        end = operation.end
        payload_parts = split_paragraphs(operation.payload) if operation.payload else []
        if operation.kind == PatchKind.REPLACE:
            paragraphs[start:end] = payload_parts
        elif operation.kind == PatchKind.DELETE:
            paragraphs[start:end] = []
        elif operation.kind == PatchKind.INSERT_BEFORE:
            paragraphs[start:start] = payload_parts
        elif operation.kind == PatchKind.INSERT_AFTER:
            paragraphs[end:end] = payload_parts
        else:  # pragma: no cover - exhaustive enum guard
            raise IRValidationError(f"unsupported patch kind={operation.kind}")
    return "\n\n".join(paragraphs)


def validate_primary_preservation(
    *,
    contract: AtomicAuthorityContract,
    preservation: PrimaryPreservationMap,
    primary_body: str,
    operations: Sequence[PatchOperation],
) -> dict[str, Any]:
    violations: list[str] = []
    if preservation.chapter_id != contract.chapter_id:
        violations.append(
            "Preservation Map chapter_id does not match current Contract"
        )
    if preservation.contract_hash != contract.contract_hash:
        violations.append(
            "Preservation Map contract_hash does not match current Contract"
        )
    current_paragraphs = split_paragraphs(primary_body)
    if len(current_paragraphs) != preservation.paragraph_count:
        violations.append(
            f"Primary paragraph count changed: expected={preservation.paragraph_count} "
            f"actual={len(current_paragraphs)}"
        )
    else:
        for index, paragraph in enumerate(current_paragraphs, 1):
            expected_hash = preservation.paragraph_hashes.get(index)
            actual_hash = paragraph_hash(paragraph)
            if expected_hash != actual_hash:
                violations.append(
                    f"Primary paragraph hash mismatch at P{index:03d}"
                )
    violations.extend(validate_edit_locality(preservation, operations))
    candidate = apply_patch_operations(primary_body, operations) if not violations else primary_body
    if not violations:
        candidate_paragraphs = split_paragraphs(candidate)
        if len(candidate_paragraphs) != preservation.paragraph_count:
            violations.append(
                "patch changed paragraph structure: "
                f"expected={preservation.paragraph_count} actual={len(candidate_paragraphs)}"
            )
        else:
            for paragraph_id in preservation.locked_paragraph_ids:
                expected_hash = preservation.paragraph_hashes[paragraph_id]
                actual_hash = paragraph_hash(
                    candidate_paragraphs[paragraph_id - 1]
                )
                if actual_hash != expected_hash:
                    violations.append(
                        f"patch changed locked paragraph P{paragraph_id:03d}"
                    )
        for hint in preservation.protection_hints:
            if hint.paragraph_id not in preservation.editable_paragraph_ids:
                continue
            touching = [
                operation
                for operation in operations
                if operation.kind in {PatchKind.REPLACE, PatchKind.DELETE}
                and operation.start <= hint.paragraph_id <= operation.end
            ]
            if not touching:
                continue
            replacement_payload = "\n\n".join(
                operation.payload
                for operation in touching
                if operation.kind == PatchKind.REPLACE
            )
            if hint.exact_fragment not in replacement_payload:
                violations.append(
                    f"edited locality erased or moved protected fragment from P{hint.paragraph_id:03d}: {hint.note or hint.exact_fragment}"
                )
    return {
        "schema_version": "primary-preservation-check-v1",
        "chapter_id": preservation.chapter_id,
        "pass": not violations,
        "violations": violations,
        "candidate_body": candidate,
        "editable_paragraph_ids": sorted(preservation.editable_paragraph_ids),
        "locked_paragraph_ids": sorted(preservation.locked_paragraph_ids),
    }


@dataclass(frozen=True)
class ContractGateResult:
    supported: bool
    pass_: bool
    blocker_fact_ids: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()


class AtomicRoutingPolicy:
    """Atomic is an acceleration layer, never a new global hard gate."""

    @staticmethod
    def preflight(contract: AtomicAuthorityContract) -> PreflightRoute:
        return (
            PreflightRoute.ATOMIC_FAST_ROUTE
            if contract.preflight_eligible
            else PreflightRoute.CURRENT_FULL_REVISER_UNGATED
        )

    @staticmethod
    def after_delta(
        contract: AtomicAuthorityContract,
        gate: ContractGateResult,
    ) -> FinalRoute:
        if not contract.preflight_eligible:
            return FinalRoute.CURRENT_FULL_REVISER_FINAL_UNGATED
        if not gate.supported:
            return FinalRoute.FULL_REVISER_UNGATED
        return (
            FinalRoute.ADOPT_DELTA
            if gate.pass_
            else FinalRoute.FULL_REVISER_THEN_SUPPORTED_GATE
        )

    @staticmethod
    def after_full(
        contract: AtomicAuthorityContract,
        gate: ContractGateResult,
    ) -> FinalRoute:
        if not contract.preflight_eligible:
            return FinalRoute.CURRENT_FULL_REVISER_FINAL_UNGATED
        if not gate.supported:
            return FinalRoute.CURRENT_FULL_REVISER_FINAL_UNGATED
        return (
            FinalRoute.FINAL_AFTER_SUPPORTED_FULL
            if gate.pass_
            else FinalRoute.FULL_REVISER_RESIDUAL_FAILURE
        )


COMPACT_CATEGORY_LIMITS = {
    "actions": 3,
    "results": 5,
    "states": 5,
    "ending": 2,
    "boundaries": 4,
}


def deterministic_mission_fact_id(
    chapter_id: str,
    category: str,
    index: int,
) -> str:
    chapter_slug = re.sub(r"[^A-Z0-9]+", "_", chapter_id.upper()).strip("_")
    category_slug = re.sub(r"[^A-Z0-9]+", "_", category.upper()).strip("_")
    return f"MISSION_{chapter_slug}_{category_slug}_{index:02d}"


def expand_compact_mission_sidecar(
    payload: Mapping[str, Any],
    registry: EntityRegistry,
) -> list[AuthorityFact]:
    """Expand a short Director sidecar into deterministic Mission facts.

    The Director chooses typed content and stable slots. Runtime owns fact IDs,
    source provenance, default modes/phases, and cross-source slot references.
    """

    if str(payload.get("v", "")) != "AAIR1":
        raise IRValidationError("compact sidecar requires v=AAIR1")
    if str(payload.get("chapter", "")) != registry.chapter_id:
        raise IRValidationError("compact sidecar chapter does not match Registry")
    if str(payload.get("protagonist", "")) != registry.protagonist_id:
        raise IRValidationError(
            "compact sidecar protagonist_id does not match Registry"
        )

    allowed_top = {
        "v",
        "chapter",
        "protagonist",
        *COMPACT_CATEGORY_LIMITS,
    }
    extra_top = set(payload) - allowed_top
    if extra_top:
        raise IRValidationError(
            f"compact sidecar contains unsupported top-level keys={sorted(extra_top)}"
        )

    facts: list[AuthorityFact] = []
    seen_slots: set[str] = set()
    allowed_kinds = {
        "actions": {FactKind.ACTION},
        "results": {
            FactKind.DIRECT_RESULT,
            FactKind.RESOURCE_TRANSITION,
            FactKind.OWNERSHIP_TRANSITION,
            FactKind.PUBLIC_PROOF,
        },
        "states": {
            FactKind.STATE_TRANSITION,
            FactKind.POWER_TRANSITION,
            FactKind.RELATIONSHIP_TRANSITION,
            FactKind.ABILITY_BOUNDARY,
        },
        "ending": {FactKind.ENDING, FactKind.DEADLINE},
        "boundaries": {
            FactKind.UNKNOWN_BOUNDARY,
            FactKind.ABILITY_BOUNDARY,
            FactKind.HISTORICAL_CLAIM_BOUNDARY,
        },
    }

    for category, limit in COMPACT_CATEGORY_LIMITS.items():
        raw_rows = payload.get(category, [])
        if not isinstance(raw_rows, list):
            raise IRValidationError(f"{category} must be a list")
        if len(raw_rows) > limit:
            raise IRValidationError(
                f"{category} exceeds compact limit {limit}: {len(raw_rows)}"
            )
        for index, raw in enumerate(raw_rows, 1):
            if not isinstance(raw, Mapping):
                raise IRValidationError(f"{category}[{index}] must be an object")
            slot = str(raw.get("slot", "")).strip()
            if not slot:
                raise IRValidationError(f"{category}[{index}] lacks stable slot")
            if slot in seen_slots:
                raise IRValidationError(f"duplicate compact slot={slot}")
            seen_slots.add(slot)

            if category == "actions":
                kind = FactKind.ACTION
                mode = FactMode.MUST_HOLD
                phase = FactPhase.DURING_CHAPTER
                terminal = False
            else:
                try:
                    kind = FactKind(str(raw.get("kind", "")))
                except ValueError as exc:
                    raise IRValidationError(
                        f"{category}[{index}] has invalid kind={raw.get('kind')!r}"
                    ) from exc
                if kind not in allowed_kinds[category]:
                    raise IRValidationError(
                        f"kind={kind.value} is not allowed in compact category={category}"
                    )
                terminal = bool(
                    raw.get(
                        "terminal",
                        category in {"results", "states"}
                        or (category == "ending" and kind == FactKind.ENDING),
                    )
                )
                if category == "boundaries":
                    default_mode = (
                        FactMode.MUST_REMAIN_UNKNOWN
                        if kind == FactKind.UNKNOWN_BOUNDARY
                        else FactMode.MUST_HOLD
                    )
                    mode = FactMode(str(raw.get("mode", default_mode.value)))
                    phase = FactPhase(
                        str(raw.get("phase", FactPhase.CHAPTER_END.value))
                    )
                elif category == "ending":
                    mode = FactMode.TERMINAL if terminal else FactMode.MUST_HOLD
                    phase = (
                        FactPhase.CHAPTER_END
                        if terminal
                        else FactPhase.POST_CHAPTER
                    )
                else:
                    mode = FactMode.TERMINAL if terminal else FactMode.MUST_HOLD
                    phase = FactPhase.CHAPTER_END

            fact_payload = {
                "fact_id": deterministic_mission_fact_id(
                    registry.chapter_id, category, index
                ),
                "slot_id": slot,
                "source": AuthoritySource.FROZEN_MISSION.value,
                "source_ref": f"director_ir.{category}.{index}",
                "kind": kind.value,
                "mode": mode.value,
                "phase": phase.value,
                "actor_id": str(raw.get("actor", "")),
                "action_id": str(raw.get("verb", "")),
                "object_ids": [str(item) for item in raw.get("objects", [])],
                "counterparty_ids": [
                    str(item) for item in raw.get("counterparties", [])
                ],
                "from_state": str(raw.get("from", "")),
                "to_state": str(raw.get("to", "")),
                "value": raw.get("value"),
                "terminal": terminal,
                "condition_slots": [
                    str(item) for item in raw.get("conditions", [])
                ],
                "depends_on_slots": [
                    str(item) for item in raw.get("depends", [])
                ],
                "metadata": dict(raw.get("meta", {})),
            }
            facts.append(AuthorityFact.from_dict(fact_payload))
    return facts




MICRO_LINE_LIMITS = {"A": 3, "R": 5, "S": 5, "E": 2, "B": 4}


def _micro_entity_list(raw: str, handles: Mapping[str, str]) -> list[str]:
    if not raw or raw == "-":
        return []
    result: list[str] = []
    for token in raw.split(","):
        key = token.strip()
        if not key:
            continue
        if key not in handles:
            raise IRValidationError(f"unknown micro entity handle={key}")
        entity_id = handles[key]
        if entity_id not in result:
            result.append(entity_id)
    return result


def _micro_kind(raw: str, allowed: set[FactKind]) -> FactKind:
    aliases = {
        "direct": FactKind.DIRECT_RESULT,
        "resource": FactKind.RESOURCE_TRANSITION,
        "ownership": FactKind.OWNERSHIP_TRANSITION,
        "relationship": FactKind.RELATIONSHIP_TRANSITION,
        "state": FactKind.STATE_TRANSITION,
        "power": FactKind.POWER_TRANSITION,
        "proof": FactKind.PUBLIC_PROOF,
        "ending": FactKind.ENDING,
        "deadline": FactKind.DEADLINE,
        "unknown": FactKind.UNKNOWN_BOUNDARY,
        "ability": FactKind.ABILITY_BOUNDARY,
        "history": FactKind.HISTORICAL_CLAIM_BOUNDARY,
    }
    try:
        kind = aliases[raw]
    except KeyError as exc:
        raise IRValidationError(f"unknown micro kind={raw!r}") from exc
    if kind not in allowed:
        raise IRValidationError(
            f"micro kind={kind.value} is not allowed in this line category"
        )
    return kind


def _derived_slot(
    *,
    chapter_id: str,
    category: str,
    index: int,
    kind: FactKind,
    actor_id: str,
    object_ids: Sequence[str],
    counterparty_ids: Sequence[str],
) -> str:
    object_id = object_ids[0] if object_ids else "NONE"
    counterpart_id = counterparty_ids[0] if counterparty_ids else "NONE"
    if kind == FactKind.RESOURCE_TRANSITION:
        return f"resource:{object_id}"
    if kind == FactKind.OWNERSHIP_TRANSITION:
        return f"ownership:{object_id}"
    if kind == FactKind.RELATIONSHIP_TRANSITION:
        return f"relationship:{actor_id}:{counterpart_id}"
    if kind == FactKind.POWER_TRANSITION:
        return f"power:{actor_id}"
    if kind == FactKind.ABILITY_BOUNDARY:
        return f"ability:{object_id}"
    if kind == FactKind.UNKNOWN_BOUNDARY:
        return f"mystery:{object_id}"
    if kind == FactKind.HISTORICAL_CLAIM_BOUNDARY:
        return f"history:{object_id}"
    if kind == FactKind.PUBLIC_PROOF:
        return f"public_proof:{chapter_id}:{object_id}"
    if kind == FactKind.DEADLINE:
        return f"deadline:{chapter_id}:{index:02d}"
    if kind == FactKind.ENDING:
        return f"ending:{chapter_id}:{index:02d}"
    if kind == FactKind.DIRECT_RESULT:
        return f"result:{chapter_id}:{index:02d}"
    if kind == FactKind.STATE_TRANSITION:
        return f"state:{object_id if object_ids else actor_id}"
    return f"event:{chapter_id}:{category}:{index:02d}"


def expand_micro_mission_sidecar(
    text: str,
    registry: EntityRegistry,
    handles: Mapping[str, str],
) -> list[AuthorityFact]:
    """Expand a tiny Director DSL; Runtime owns all persistent identifiers.

    Grammar (pipe-delimited; '-' means empty):

    A|actor|verb|objects|counterparties
    R|kind|actor|verb|objects|counterparties|from|to|value_json
    S|kind|actor|verb|objects|counterparties|from|to|value_json
    E|kind|actor|verb|objects|counterparties|from|to|value_json
    B|kind|actor|verb|objects|counterparties|mode|to|value_json
    """

    if handles.get("P") != registry.protagonist_id:
        raise IRValidationError(
            "micro handle P must map to Registry protagonist_id"
        )

    facts: list[AuthorityFact] = []
    counts = {key: 0 for key in MICRO_LINE_LIMITS}
    allowed = {
        "R": {
            FactKind.DIRECT_RESULT,
            FactKind.RESOURCE_TRANSITION,
            FactKind.OWNERSHIP_TRANSITION,
            FactKind.PUBLIC_PROOF,
        },
        "S": {
            FactKind.STATE_TRANSITION,
            FactKind.POWER_TRANSITION,
            FactKind.RELATIONSHIP_TRANSITION,
            FactKind.ABILITY_BOUNDARY,
        },
        "E": {FactKind.ENDING, FactKind.DEADLINE},
        "B": {
            FactKind.UNKNOWN_BOUNDARY,
            FactKind.ABILITY_BOUNDARY,
            FactKind.HISTORICAL_CLAIM_BOUNDARY,
        },
    }
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("|")]
        category = parts[0]
        if category not in MICRO_LINE_LIMITS:
            raise IRValidationError(f"unknown micro category={category!r}")
        counts[category] += 1
        if counts[category] > MICRO_LINE_LIMITS[category]:
            raise IRValidationError(
                f"micro category={category} exceeds limit={MICRO_LINE_LIMITS[category]}"
            )

        if category == "A":
            if len(parts) != 5:
                raise IRValidationError(f"A line requires 5 fields: {line}")
            _, actor_handle, verb, object_raw, counterparty_raw = parts
            kind = FactKind.ACTION
            mode = FactMode.MUST_HOLD
            phase = FactPhase.DURING_CHAPTER
            from_state = ""
            to_state = ""
            value = None
        elif category in {"R", "S", "E"}:
            if len(parts) != 9:
                raise IRValidationError(
                    f"{category} line requires 9 fields: {line}"
                )
            (
                _,
                kind_raw,
                actor_handle,
                verb,
                object_raw,
                counterparty_raw,
                from_state,
                to_state,
                value_raw,
            ) = parts
            kind = _micro_kind(kind_raw, allowed[category])
            terminal = category in {"R", "S"} or kind == FactKind.ENDING
            mode = FactMode.TERMINAL if terminal else FactMode.MUST_HOLD
            phase = (
                FactPhase.CHAPTER_END if terminal else FactPhase.POST_CHAPTER
            )
            value = None if value_raw in {"", "-", "null"} else json.loads(value_raw)
        else:
            if len(parts) != 9:
                raise IRValidationError(f"B line requires 9 fields: {line}")
            (
                _,
                kind_raw,
                actor_handle,
                verb,
                object_raw,
                counterparty_raw,
                mode_raw,
                to_state,
                value_raw,
            ) = parts
            kind = _micro_kind(kind_raw, allowed[category])
            mode = FactMode(mode_raw)
            phase = FactPhase.CHAPTER_END
            from_state = ""
            value = None if value_raw in {"", "-", "null"} else json.loads(value_raw)

        actor_id = ""
        if actor_handle not in {"", "-"}:
            if actor_handle not in handles:
                raise IRValidationError(
                    f"unknown micro actor handle={actor_handle}"
                )
            actor_id = handles[actor_handle]
        object_ids = _micro_entity_list(object_raw, handles)
        counterparty_ids = _micro_entity_list(counterparty_raw, handles)
        for entity_id in [actor_id, *object_ids, *counterparty_ids]:
            if entity_id:
                registry.require(entity_id)
        index = counts[category]
        slot_id = _derived_slot(
            chapter_id=registry.chapter_id,
            category=category,
            index=index,
            kind=kind,
            actor_id=actor_id,
            object_ids=object_ids,
            counterparty_ids=counterparty_ids,
        )
        facts.append(
            AuthorityFact(
                fact_id=deterministic_mission_fact_id(
                    registry.chapter_id, category, index
                ),
                slot_id=slot_id,
                source=AuthoritySource.FROZEN_MISSION,
                source_ref=f"director_micro_ir.{category}.{index}",
                kind=kind,
                mode=mode,
                phase=phase,
                actor_id=actor_id,
                action_id=verb,
                object_ids=tuple(object_ids),
                counterparty_ids=tuple(counterparty_ids),
                from_state=from_state,
                to_state=to_state,
                value=value,
                terminal=mode == FactMode.TERMINAL,
            )
        )
    return facts




DIRECTOR_FIELD_LABELS = {
    DirectorField.TRIGGER_EVENT: "触发事件",
    DirectorField.EVENT_DRIVER: "推动事件的人",
    DirectorField.PROTAGONIST_ACTION: "主角行动",
    DirectorField.WORLD_REACTION: "对手或世界反应",
    DirectorField.DIRECT_RESULT: "直接结果",
    DirectorField.STATE_CHANGE: "状态变化",
    DirectorField.ENDING_DRIVE: "结尾推动力",
}

DIRECTOR_FIELD_LIMITS: dict[DirectorField, tuple[int, int]] = {
    DirectorField.TRIGGER_EVENT: (1, 1),
    DirectorField.EVENT_DRIVER: (1, 3),
    DirectorField.PROTAGONIST_ACTION: (1, 3),
    DirectorField.WORLD_REACTION: (1, 4),
    DirectorField.DIRECT_RESULT: (1, 5),
    DirectorField.STATE_CHANGE: (1, 5),
    DirectorField.ENDING_DRIVE: (1, 2),
}

DIRECTOR_FIELD_ALLOWED_KINDS = {
    DirectorField.TRIGGER_EVENT: {FactKind.EVENT},
    DirectorField.EVENT_DRIVER: {FactKind.EVENT, FactKind.ACTION},
    DirectorField.PROTAGONIST_ACTION: {FactKind.ACTION},
    DirectorField.WORLD_REACTION: {
        FactKind.EVENT,
        FactKind.DIRECT_RESULT,
        FactKind.STATE_TRANSITION,
        FactKind.PUBLIC_PROOF,
    },
    DirectorField.DIRECT_RESULT: {
        FactKind.DIRECT_RESULT,
        FactKind.RESOURCE_TRANSITION,
        FactKind.OWNERSHIP_TRANSITION,
        FactKind.PUBLIC_PROOF,
    },
    DirectorField.STATE_CHANGE: {
        FactKind.STATE_TRANSITION,
        FactKind.POWER_TRANSITION,
        FactKind.RESOURCE_TRANSITION,
        FactKind.OWNERSHIP_TRANSITION,
        FactKind.RELATIONSHIP_TRANSITION,
        FactKind.ABILITY_BOUNDARY,
        FactKind.UNKNOWN_BOUNDARY,
    },
    DirectorField.ENDING_DRIVE: {FactKind.ENDING, FactKind.DEADLINE},
}


@dataclass(frozen=True)
class ActionSurfaceTemplate:
    action_id: str
    template: str

    def render(
        self,
        *,
        registry: EntityRegistry,
        actor_id: str,
        object_ids: Sequence[str],
        counterparty_ids: Sequence[str],
        from_state: str,
        to_state: str,
        value: Any,
    ) -> str:
        actor = (
            registry.require(actor_id).display_name if actor_id else "世界"
        )
        objects = "、".join(
            registry.require(entity_id).display_name for entity_id in object_ids
        )
        counterparties = "、".join(
            registry.require(entity_id).display_name
            for entity_id in counterparty_ids
        )
        rendered = self.template.format(
            actor=actor,
            objects=objects,
            counterparties=counterparties,
            from_state=from_state,
            to_state=to_state,
            value=(
                json.dumps(value, ensure_ascii=False, sort_keys=True)
                if value is not None
                else ""
            ),
        ).strip()
        if not rendered:
            raise IRValidationError(
                f"surface template for action_id={self.action_id} rendered empty"
            )
        return rendered


@dataclass(frozen=True)
class ActionSurfaceRegistry:
    templates: Mapping[str, ActionSurfaceTemplate]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "templates",
            MappingProxyType(dict(self.templates)),
        )

    @classmethod
    def from_dict(cls, payload: Mapping[str, str]) -> "ActionSurfaceRegistry":
        return cls(
            templates={
                action_id: ActionSurfaceTemplate(
                    action_id=action_id,
                    template=str(template),
                )
                for action_id, template in payload.items()
            }
        )

    def render(
        self,
        clause: "DirectorStructuredClause",
        registry: EntityRegistry,
    ) -> str:
        try:
            template = self.templates[clause.action_id]
        except KeyError as exc:
            raise IRValidationError(
                f"missing action surface template for action_id={clause.action_id}"
            ) from exc
        return template.render(
            registry=registry,
            actor_id=clause.actor_id,
            object_ids=clause.object_ids,
            counterparty_ids=clause.counterparty_ids,
            from_state=clause.from_state,
            to_state=clause.to_state,
            value=clause.value,
        )


@dataclass(frozen=True)
class NarrativeFunctionRegistry:
    surfaces: Mapping[str, str]

    def __post_init__(self) -> None:
        snapshot = {str(key): str(value).strip() for key, value in self.surfaces.items()}
        for function_id, surface in snapshot.items():
            if not NARRATIVE_FUNCTION_ID_PATTERN.fullmatch(function_id):
                raise IRValidationError(
                    f"invalid narrative_function_id={function_id!r}"
                )
            if not surface:
                raise IRValidationError(
                    f"empty narrative function surface for {function_id}"
                )
        object.__setattr__(self, "surfaces", MappingProxyType(snapshot))

    @classmethod
    def from_dict(cls, payload: Mapping[str, str]) -> "NarrativeFunctionRegistry":
        return cls(surfaces=dict(payload))

    def render(self, function_id: str) -> str:
        try:
            return self.surfaces[function_id]
        except KeyError as exc:
            raise IRValidationError(
                f"missing narrative function surface for id={function_id}"
            ) from exc


@dataclass(frozen=True)
class DirectorStructuredClause:
    field: DirectorField
    kind: FactKind
    actor_id: str = ""
    action_id: str = ""
    object_ids: tuple[str, ...] = ()
    counterparty_ids: tuple[str, ...] = ()
    from_state: str = ""
    to_state: str = ""
    value: Any = None
    terminal: bool | None = None
    mode: FactMode | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    surface_note: str = ""

    def __post_init__(self) -> None:
        if self.kind not in DIRECTOR_FIELD_ALLOWED_KINDS[self.field]:
            raise IRValidationError(
                f"kind={self.kind.value} is not allowed in Director field={self.field.value}"
            )
        if not self.action_id.strip():
            raise IRValidationError(
                f"Director structured clause field={self.field.value} lacks action_id"
            )
        object.__setattr__(self, "value", _deep_freeze(self.value))
        object.__setattr__(self, "metadata", _deep_freeze(self.metadata))

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "DirectorStructuredClause":
        allowed_keys = {
            "field", "kind", "actor_id", "action_id", "object_ids",
            "counterparty_ids", "from_state", "to_state", "value",
            "metadata", "surface_note",
        }
        unknown_keys = set(payload) - allowed_keys
        if unknown_keys:
            raise IRValidationError(
                "Director structured clause contains unsupported keys="
                + ", ".join(sorted(unknown_keys))
            )
        if "human_clause" in payload:
            raise IRValidationError(
                "human_clause is a second semantic write; use typed clause + Runtime surface registry"
            )
        return cls(
            field=DirectorField(str(payload["field"])),
            kind=FactKind(str(payload["kind"])),
            actor_id=str(payload.get("actor_id", "")),
            action_id=str(payload.get("action_id", "")),
            object_ids=tuple(str(item) for item in payload.get("object_ids", [])),
            counterparty_ids=tuple(
                str(item) for item in payload.get("counterparty_ids", [])
            ),
            from_state=str(payload.get("from_state", "")),
            to_state=str(payload.get("to_state", "")),
            value=payload.get("value"),
            terminal=None,
            mode=None,
            metadata=dict(payload.get("metadata", {})),
            surface_note=str(payload.get("surface_note", "")),
        )

    def _defaults(self) -> tuple[FactMode, FactPhase, bool]:
        if self.field in {
            DirectorField.TRIGGER_EVENT,
            DirectorField.EVENT_DRIVER,
            DirectorField.PROTAGONIST_ACTION,
            DirectorField.WORLD_REACTION,
        }:
            return FactMode.MUST_HOLD, FactPhase.DURING_CHAPTER, False
        if self.field == DirectorField.ENDING_DRIVE:
            if self.kind == FactKind.DEADLINE:
                return FactMode.MUST_HOLD, FactPhase.POST_CHAPTER, False
            return FactMode.TERMINAL, FactPhase.CHAPTER_END, True
        if self.kind == FactKind.UNKNOWN_BOUNDARY:
            return FactMode.MUST_REMAIN_UNKNOWN, FactPhase.CHAPTER_END, False
        if self.kind == FactKind.ABILITY_BOUNDARY:
            return FactMode.MUST_HOLD, FactPhase.CHAPTER_END, False
        return FactMode.TERMINAL, FactPhase.CHAPTER_END, True

    def to_fact(
        self,
        *,
        registry: EntityRegistry,
        index: int,
    ) -> AuthorityFact:
        for entity_id in (
            [self.actor_id]
            + list(self.object_ids)
            + list(self.counterparty_ids)
        ):
            if entity_id:
                registry.require(entity_id)
        default_mode, phase, default_terminal = self._defaults()
        mode = self.mode or default_mode
        terminal = default_terminal if self.terminal is None else self.terminal
        category = self.field.value
        slot_id = _derived_slot(
            chapter_id=registry.chapter_id,
            category=category,
            index=index,
            kind=self.kind,
            actor_id=self.actor_id,
            object_ids=self.object_ids,
            counterparty_ids=self.counterparty_ids,
        )
        return AuthorityFact(
            fact_id=deterministic_mission_fact_id(
                registry.chapter_id, category, index
            ),
            slot_id=slot_id,
            source=AuthoritySource.FROZEN_MISSION,
            source_ref=f"director_structured.{category}.{index}",
            kind=self.kind,
            mode=mode,
            phase=phase,
            actor_id=self.actor_id,
            action_id=self.action_id,
            object_ids=self.object_ids,
            counterparty_ids=self.counterparty_ids,
            from_state=self.from_state,
            to_state=self.to_state,
            value=_deep_thaw(self.value),
            terminal=terminal,
            metadata=_deep_thaw(self.metadata),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "field": self.field.value,
            "kind": self.kind.value,
            "actor_id": self.actor_id,
            "action_id": self.action_id,
            "object_ids": list(self.object_ids),
            "counterparty_ids": list(self.counterparty_ids),
            "from_state": self.from_state,
            "to_state": self.to_state,
            "value": _deep_thaw(self.value),
            "terminal": self.terminal,
            "mode": self.mode.value if self.mode else None,
            "metadata": _deep_thaw(self.metadata),
            "surface_note": self.surface_note,
        }


@dataclass(frozen=True)
class DirectorStructuredDecision:
    chapter_id: str
    protagonist_id: str
    clauses: tuple[DirectorStructuredClause, ...]
    narrative_function_id: str

    def __post_init__(self) -> None:
        if not NARRATIVE_FUNCTION_ID_PATTERN.fullmatch(
            self.narrative_function_id
        ):
            raise IRValidationError(
                "Director decision has invalid narrative_function_id"
            )
        counts = {field: 0 for field in DirectorField}
        for clause in self.clauses:
            counts[clause.field] += 1
        violations = []
        for field, (minimum, maximum) in DIRECTOR_FIELD_LIMITS.items():
            count = counts[field]
            if count < minimum or count > maximum:
                violations.append(
                    f"{field.value} count={count} expected={minimum}..{maximum}"
                )
        if violations:
            raise IRValidationError(
                "Director structured decision field limits: "
                + "; ".join(violations)
            )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "DirectorStructuredDecision":
        if str(payload.get("schema_version", "")) != "director-structured-decision-v1":
            raise IRValidationError(
                "Director decision requires schema_version=director-structured-decision-v1"
            )
        allowed_keys = {
            "schema_version", "chapter_id", "protagonist_id", "clauses",
            "narrative_function_id",
        }
        unknown_keys = set(payload) - allowed_keys
        if unknown_keys:
            raise IRValidationError(
                "Director decision contains unsupported keys="
                + ", ".join(sorted(unknown_keys))
            )
        forbidden_free_semantics = {
            key for key in ("narrative_function", "specialty_suggestions")
            if key in payload
        }
        if forbidden_free_semantics:
            raise IRValidationError(
                "Director decision contains a second free semantic source: "
                + ", ".join(sorted(forbidden_free_semantics))
            )
        return cls(
            chapter_id=str(payload["chapter_id"]),
            protagonist_id=str(payload["protagonist_id"]),
            clauses=tuple(
                DirectorStructuredClause.from_dict(item)
                for item in payload.get("clauses", [])
            ),
            narrative_function_id=str(payload["narrative_function_id"]),
        )

    def mission_facts(self, registry: EntityRegistry) -> list[AuthorityFact]:
        if self.chapter_id != registry.chapter_id:
            raise IRValidationError(
                "Director structured decision chapter_id does not match Registry"
            )
        if self.protagonist_id != registry.protagonist_id:
            raise IRValidationError(
                "Director structured decision protagonist_id does not match Registry"
            )
        counters: dict[DirectorField, int] = {}
        facts: list[AuthorityFact] = []
        slot_phase: set[tuple[str, FactPhase]] = set()
        signatures: set[tuple[Any, ...]] = set()
        for clause in self.clauses:
            if (
                clause.field == DirectorField.PROTAGONIST_ACTION
                and clause.actor_id != registry.protagonist_id
                and registry.require(clause.actor_id).parent_entity_id
                != registry.protagonist_id
            ):
                raise IRValidationError(
                    "protagonist_action actor_id must be the protagonist or a registered protagonist manifestation"
                )
            counters[clause.field] = counters.get(clause.field, 0) + 1
            fact = clause.to_fact(
                registry=registry,
                index=counters[clause.field],
            )
            key = (fact.slot_id, fact.phase)
            if key in slot_phase:
                raise IRValidationError(
                    f"Director decision duplicates slot/phase={key}"
                )
            signature = fact.canonical_signature()
            if signature in signatures:
                raise IRValidationError(
                    f"Director decision repeats a canonical fact at {fact.source_ref}"
                )
            slot_phase.add(key)
            signatures.add(signature)
            facts.append(fact)
        return facts

    def build_contract(
        self,
        *,
        registry: EntityRegistry,
        authority_artifacts: Sequence[FrozenAuthorityArtifact] = (),
    ) -> AtomicAuthorityContract:
        builder = AtomicAuthorityContractBuilder(registry)
        for artifact in authority_artifacts:
            if artifact.source == AuthoritySource.FROZEN_MISSION:
                raise IRValidationError(
                    "external artifacts cannot add a second Frozen Mission to a Director decision"
                )
            builder.add_artifact(artifact)
        builder.add_artifact(
            freeze_mission_artifact(
                f"mission:{self.chapter_id}:director_structured_v1",
                self.mission_facts(registry),
            )
        )
        return builder.build()

    def render_human_mission(
        self,
        *,
        registry: EntityRegistry,
        surfaces: ActionSurfaceRegistry,
        narrative_functions: NarrativeFunctionRegistry,
    ) -> str:
        grouped: dict[DirectorField, list[str]] = {
            field: [] for field in DirectorField
        }
        for clause in self.clauses:
            grouped[clause.field].append(
                surfaces.render(clause, registry).strip()
            )
        lines = []
        for field in DirectorField:
            clean_clauses = [
                clause.rstrip("。；; ") for clause in grouped[field]
            ]
            lines.append(
                f"{DIRECTOR_FIELD_LABELS[field]}："
                + "；".join(clean_clauses)
                + "。"
            )
            if field == DirectorField.STATE_CHANGE:
                lines.append(
                    "叙事功能："
                    + narrative_functions.render(self.narrative_function_id)
                )
        return "\n".join(lines).strip()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "director-structured-decision-v1",
            "chapter_id": self.chapter_id,
            "protagonist_id": self.protagonist_id,
            "clauses": [clause.to_dict() for clause in self.clauses],
            "narrative_function_id": self.narrative_function_id,
        }

def load_contract_payload(path: Path) -> AtomicAuthorityContract:
    """Load a trusted Runtime envelope with source-specific artifact fields.

    The envelope deliberately has no generic `source` key that content may spoof.
    """

    payload = json.loads(path.read_text(encoding="utf-8"))
    registry = EntityRegistry.from_dict(payload["registry"])
    builder = AtomicAuthorityContractBuilder(registry)
    loaders = {
        "frozen_mission_artifacts": freeze_mission_artifact,
        "canon_artifacts": freeze_canon_artifact,
        "world_artifacts": freeze_world_artifact,
        "power_artifacts": freeze_power_artifact,
        "human_artifacts": freeze_human_artifact,
        "reader_release_artifacts": freeze_reader_release_artifact,
    }
    allowed_top = {"registry", "diagnostics", *loaders}
    unknown_top = set(payload) - allowed_top
    if unknown_top:
        raise SourcePurityError(
            f"trusted Authority envelope contains unsupported keys={sorted(unknown_top)}"
        )
    for field_name, loader in loaders.items():
        for artifact_payload in payload.get(field_name, []):
            builder.add_artifact(
                loader(
                    str(artifact_payload["artifact_id"]),
                    artifact_payload.get("facts", []),
                )
            )
    for diagnostic in payload.get("diagnostics", []):
        builder.add_diagnostic(str(diagnostic))
    return builder.build()


def save_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
