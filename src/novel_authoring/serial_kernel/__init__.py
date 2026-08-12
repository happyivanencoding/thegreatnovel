"""Chinese Serialized Webnovel Kernel public surface."""

from novel_authoring.serial_kernel.classification import interpret_narrative_drives
from novel_authoring.serial_kernel.diagnostics import (
    NarrativeDriveDriftDiagnostic,
    NarrativeDriveDriftStatus,
    NarrativeDriveStructureEvidence,
    diagnose_narrative_drive_drift,
)
from novel_authoring.serial_kernel.engines import (
    NARRATIVE_ENGINE_REGISTRY,
    EngineCandidateEvaluation,
    EngineIntentRecommendation,
    EngineValidationResult,
    NarrativeEngineAdapter,
    NarrativeEngineRegistry,
    ProgressionNarrativeEngineAdapter,
)
from novel_authoring.serial_kernel.models import (
    PROGRESSION_DRIVES,
    DrivePayoffChannel,
    DriveState,
    EngineImplementationDepth,
    MarketCategory,
    MarketCategoryMetadata,
    NarrativeDrive,
    NarrativeDriveContract,
    NarrativeDriveInterpretation,
    NarrativeEngineType,
)

__all__ = [
    "DrivePayoffChannel",
    "DriveState",
    "EngineCandidateEvaluation",
    "EngineImplementationDepth",
    "EngineIntentRecommendation",
    "EngineValidationResult",
    "MarketCategory",
    "MarketCategoryMetadata",
    "NarrativeDrive",
    "NarrativeDriveContract",
    "NarrativeDriveDriftDiagnostic",
    "NarrativeDriveDriftStatus",
    "NarrativeDriveInterpretation",
    "NARRATIVE_ENGINE_REGISTRY",
    "NarrativeEngineAdapter",
    "NarrativeEngineRegistry",
    "NarrativeEngineType",
    "NarrativeDriveStructureEvidence",
    "PROGRESSION_DRIVES",
    "ProgressionNarrativeEngineAdapter",
    "interpret_narrative_drives",
    "diagnose_narrative_drive_drift",
]
