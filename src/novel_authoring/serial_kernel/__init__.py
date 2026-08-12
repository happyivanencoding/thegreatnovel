"""Chinese Serialized Webnovel Kernel public surface."""

from novel_authoring.serial_kernel.classification import interpret_narrative_drives
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
    "EngineImplementationDepth",
    "MarketCategory",
    "MarketCategoryMetadata",
    "NarrativeDrive",
    "NarrativeDriveContract",
    "NarrativeDriveInterpretation",
    "NarrativeEngineType",
    "PROGRESSION_DRIVES",
    "interpret_narrative_drives",
]
