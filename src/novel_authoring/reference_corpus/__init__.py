"""Deterministic foundation for the external Reference Corpus V0.

The package deliberately stops at filesystem inventory, proposal validation,
and source-aware card contracts.  It does not read or interpret a novel into
semantic findings and it never writes to the immutable raw corpus.
"""

from novel_authoring.reference_corpus.models import (
    CardKnowledgeLevel,
    CorpusCardFrontmatter,
    InventoryFile,
    InventoryManifest,
    PilotSelectionProposal,
)

__all__ = [
    "CardKnowledgeLevel",
    "CorpusCardFrontmatter",
    "InventoryFile",
    "InventoryManifest",
    "PilotSelectionProposal",
]
