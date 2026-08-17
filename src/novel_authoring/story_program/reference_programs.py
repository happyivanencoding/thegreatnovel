"""Small, explicit loader for the validated Reference Program YAML files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

DEFAULT_REFERENCE_ROOT = (
    Path(r"C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库")
    / "reference-corpus-program-deep-v1"
    / "reference-programs"
)
ALLOWED_STATUSES = {"VALIDATED", "PROVISIONAL"}


def _text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def _lines(value: object) -> list[str]:
    if isinstance(value, list):
        return [_text(item) for item in value if _text(item)]
    if value is None:
        return []
    item = _text(value)
    return [item] if item else []


@dataclass(frozen=True, slots=True)
class ReferenceProgram:
    program_id: str
    source_book_id: str
    status: str
    story_phase: str
    input_state: str
    reader_promise: str
    central_pressure: str
    reusable_program: str
    applicable_conditions: tuple[str, ...]
    failure_modes: tuple[str, ...]
    anti_repetition_notes: tuple[str, ...]
    output_state: str
    raw: dict[str, Any]

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> ReferenceProgram:
        program_id = _text(payload.get("program_id"))
        source_book_id = _text(payload.get("source_book_id"))
        status = _text(payload.get("status")).upper()
        if not program_id or not source_book_id or status not in ALLOWED_STATUSES:
            raise ValueError("Reference Program 缺少 program_id/source_book_id/status")
        return cls(
            program_id=program_id,
            source_book_id=source_book_id,
            status=status,
            story_phase=_text(payload.get("story_phase")),
            input_state=_text(payload.get("input_state")),
            reader_promise=_text(payload.get("reader_promise")),
            central_pressure=_text(payload.get("central_pressure")),
            reusable_program=_text(payload.get("reusable_program")),
            applicable_conditions=tuple(_lines(payload.get("applicable_conditions"))),
            failure_modes=tuple(_lines(payload.get("failure_modes"))),
            anti_repetition_notes=tuple(_lines(payload.get("anti_repetition_notes"))),
            output_state=_text(payload.get("output_state")),
            raw=dict(payload),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "program_id": self.program_id,
            "source_book_id": self.source_book_id,
            "status": self.status,
            "story_phase": self.story_phase,
            "input_state": self.input_state,
            "reader_promise": self.reader_promise,
            "central_pressure": self.central_pressure,
            "reusable_program": self.reusable_program,
            "applicable_conditions": list(self.applicable_conditions),
            "failure_modes": list(self.failure_modes),
            "anti_repetition_notes": list(self.anti_repetition_notes),
            "output_state": self.output_state,
        }

    def prompt_payload(self) -> str:
        """Return exactly the abstract fields that enter a generated prompt."""

        lines = [
            f"program_id: {self.program_id}",
            f"source_book_id: {self.source_book_id}",
            f"status: {self.status}",
            f"story_phase: {self.story_phase or '未填写'}",
            f"input_state: {self.input_state or '未填写'}",
            f"reader_promise: {self.reader_promise or '未填写'}",
            f"central_pressure: {self.central_pressure or '未填写'}",
            f"reusable_program: {self.reusable_program or '未填写'}",
            "applicable_conditions:",
            *[f"  - {item}" for item in self.applicable_conditions],
            "failure_modes:",
            *[f"  - {item}" for item in self.failure_modes],
            "anti_repetition_notes:",
            *[f"  - {item}" for item in self.anti_repetition_notes],
            f"output_state: {self.output_state or '未填写'}",
            "禁止复制：来源小说的人物、地名、修炼方法、物品、具体事件和句子。",
        ]
        return "\n".join(lines)


def _payloads_from_yaml(value: object) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        nested = value.get("programs")
        if isinstance(nested, list):
            return [item for item in nested if isinstance(item, dict)]
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def load_reference_programs(
    root: Path | None = None,
    *,
    include_provisional: bool = False,
    query: str = "",
) -> list[ReferenceProgram]:
    """Load only explicitly supported statuses, with deterministic filename order."""

    directory = Path(root or DEFAULT_REFERENCE_ROOT).expanduser().resolve()
    if not directory.is_dir():
        return []
    needle = query.strip().casefold()
    result: list[ReferenceProgram] = []
    for path in sorted((*directory.rglob("*.yaml"), *directory.rglob("*.yml"))):
        try:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError):
            continue
        for item in _payloads_from_yaml(payload):
            try:
                program = ReferenceProgram.from_mapping(item)
            except ValueError:
                continue
            if program.status == "PROVISIONAL" and not include_provisional:
                continue
            if needle:
                haystack = "\n".join(
                    [
                        program.program_id,
                        program.source_book_id,
                        program.story_phase,
                        program.reader_promise,
                        program.central_pressure,
                        program.reusable_program,
                        *program.applicable_conditions,
                        *program.failure_modes,
                        *program.anti_repetition_notes,
                        program.output_state,
                    ]
                ).casefold()
                if needle not in haystack:
                    continue
            result.append(program)
    return sorted(result, key=lambda item: (item.status != "VALIDATED", item.program_id))


def select_reference_programs(
    programs: list[ReferenceProgram],
    program_ids: list[str],
    *,
    allow_provisional: bool = False,
) -> list[ReferenceProgram]:
    selected_ids = [str(item).strip() for item in program_ids if str(item).strip()]
    if len(selected_ids) > 3:
        raise ValueError("每轮最多选择 3 个 Reference Program")
    by_id = {item.program_id: item for item in programs}
    selected: list[ReferenceProgram] = []
    for program_id in selected_ids:
        program = by_id.get(program_id)
        if program is None:
            raise ValueError(f"Reference Program 不存在或未加载：{program_id}")
        if program.status == "PROVISIONAL" and not allow_provisional:
            raise ValueError("PROVISIONAL Program 需要作者明确开启后才能使用")
        selected.append(program)
    return selected


__all__ = [
    "ALLOWED_STATUSES",
    "DEFAULT_REFERENCE_ROOT",
    "ReferenceProgram",
    "load_reference_programs",
    "select_reference_programs",
]
