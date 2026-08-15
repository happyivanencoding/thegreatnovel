"""Pydantic contracts for Reference Corpus V0.

These models describe deterministic metadata and provenance boundaries.  They
are intentionally not literary-analysis models: meaning remains in a future
Codex/LLM skill and is never promoted to Canon by these contracts.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class InventoryParseStatus(StrEnum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"
    UNSUPPORTED = "UNSUPPORTED"


class CardKnowledgeLevel(StrEnum):
    BOOK_OBSERVATION = "BOOK_OBSERVATION"
    CROSS_BOOK_CONTRAST = "CROSS_BOOK_CONTRAST"
    CORPUS_SYNTHESIS = "CORPUS_SYNTHESIS"
    AUTHOR_TASTE = "AUTHOR_TASTE"


class CorpusCardType(StrEnum):
    REFERENCE_BOOK = "reference-book"
    BOOK_DNA = "book-dna"
    PROSE_DNA = "prose-dna"
    ARC_OBSERVATION = "arc-observation"
    OBSERVATION = "observation"
    MECHANISM_CARD = "mechanism-card"
    CONTRAST_CARD = "contrast-card"
    CORPUS_SYNTHESIS = "corpus-synthesis"
    TASTE_NOTE = "taste-note"


class CategoryDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_id: str = Field(min_length=1)
    category_name: str = Field(min_length=1)


class InventoryFile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_id: str = Field(min_length=1)
    category_name: str = Field(min_length=1)
    relative_path: str = Field(min_length=1)
    file_name: str = Field(min_length=1)
    extension: str = Field(min_length=1)
    size_bytes: int = Field(ge=0)
    modified_at: str = Field(min_length=1)
    parse_status: InventoryParseStatus
    detected_encoding: str | None = None
    estimated_chapter_count: int = Field(ge=0)
    title: str = Field(min_length=1)
    normalized_title: str = Field(min_length=1)
    warnings: list[str] = Field(default_factory=list)


class InventoryCategory(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_id: str = Field(min_length=1)
    category_name: str = Field(min_length=1)
    file_count: int = Field(ge=0)
    supported_file_count: int = Field(ge=0)
    eligible_file_count: int = Field(ge=0)
    warnings: list[str] = Field(default_factory=list)


class InventoryManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["reference-corpus-inventory-v1"]
    created_at: str = Field(min_length=1)
    raw_root: str = Field(min_length=1)
    corpus_root: str = Field(min_length=1)
    expected_categories: list[CategoryDefinition]
    actual_categories: list[CategoryDefinition]
    categories: list[InventoryCategory]
    files: list[InventoryFile]
    warnings: list[str] = Field(default_factory=list)


class SelectionAlternative(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_path: str = Field(min_length=1)
    title: str = Field(min_length=1)
    known_warning: str = ""


class SelectionRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_path: str = Field(min_length=1)
    title: str = Field(min_length=1)
    category: str = Field(min_length=1)
    category_name: str = Field(min_length=1)
    selection_reason: str = Field(min_length=1)
    contrast_role: str = Field(min_length=1)
    known_warning: str = ""
    alternatives: list[SelectionAlternative] = Field(default_factory=list)


class SelectionCategory(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_id: str = Field(min_length=1)
    category_name: str = Field(min_length=1)
    status: Literal["PROPOSED", "BLOCKED"]
    recommendations: list[SelectionRecommendation] = Field(default_factory=list)
    blocker: str | None = None

    @model_validator(mode="after")
    def validate_category_shape(self) -> SelectionCategory:
        if self.status == "BLOCKED" and not self.blocker:
            raise ValueError("BLOCKED category 必须说明 blocker")
        if self.status == "PROPOSED" and self.blocker:
            raise ValueError("PROPOSED category 不应携带 blocker")
        return self


class PilotSelectionProposal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["reference-corpus-selection-v1"]
    status: Literal["PROPOSED", "CONFIRMED"]
    created_at: str = Field(min_length=1)
    raw_root: str = Field(min_length=1)
    corpus_root: str = Field(min_length=1)
    expected_categories: list[CategoryDefinition]
    actual_categories: list[CategoryDefinition]
    selection_basis: list[str] = Field(min_length=1)
    categories: list[SelectionCategory]
    supplemental_recommendations: list[SelectionRecommendation] = Field(default_factory=list)
    target_book_count: int = Field(default=26, ge=1)
    selected_book_count: int = Field(ge=0)
    blocking_issues: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_count(self) -> PilotSelectionProposal:
        count = sum(len(category.recommendations) for category in self.categories)
        count += len(self.supplemental_recommendations)
        if count != self.selected_book_count:
            raise ValueError("selected_book_count 必须等于所有推荐项数量")
        return self


class CorpusCardFrontmatter(BaseModel):
    """Small frontmatter contract for future derived cards.

    The source locator is required even for cards that later synthesize across
    books.  Cross-book cards should put the full evidence list in
    ``source_refs``; the singular fields keep every page locally auditable.
    """

    model_config = ConfigDict(extra="allow")

    card_id: str = Field(min_length=1)
    card_type: CorpusCardType
    knowledge_level: CardKnowledgeLevel
    source_book_id: str = Field(min_length=1)
    locator: str = Field(min_length=1)
    source_refs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_knowledge_boundary(self) -> CorpusCardFrontmatter:
        if self.knowledge_level is CardKnowledgeLevel.BOOK_OBSERVATION and self.card_type in {
            CorpusCardType.MECHANISM_CARD,
            CorpusCardType.CORPUS_SYNTHESIS,
        }:
            raise ValueError(
                "BOOK_OBSERVATION 不能标记为跨书 mechanism-card/corpus-synthesis"
            )
        if self.card_type is CorpusCardType.TASTE_NOTE and (
            self.knowledge_level is not CardKnowledgeLevel.AUTHOR_TASTE
        ):
            raise ValueError("taste-note 必须是 AUTHOR_TASTE")
        return self


__all__ = [
    "CardKnowledgeLevel",
    "CategoryDefinition",
    "CorpusCardFrontmatter",
    "CorpusCardType",
    "InventoryCategory",
    "InventoryFile",
    "InventoryManifest",
    "InventoryParseStatus",
    "PilotSelectionProposal",
    "SelectionAlternative",
    "SelectionCategory",
    "SelectionRecommendation",
]
