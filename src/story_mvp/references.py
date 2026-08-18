from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


REFERENCE_ROOT = Path(
    r"C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\reference-corpus-program-deep-v1\reference-programs"
)

REFERENCE_FIELDS = (
    "program_id",
    "story_phase",
    "input_state",
    "central_pressure",
    "reusable_program",
    "applicable_conditions",
    "failure_modes",
    "anti_repetition_notes",
    "output_state",
)


def load_validated_references(root: Path = REFERENCE_ROOT) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    references: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.yaml")) + sorted(root.rglob("*.yml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError):
            continue
        if not isinstance(data, dict) or data.get("status") != "VALIDATED":
            continue
        references.append(
            {
                "status": "VALIDATED",
                **{field: data.get(field, "") for field in REFERENCE_FIELDS},
            }
        )
    return sorted(references, key=lambda item: str(item.get("program_id", "")))
