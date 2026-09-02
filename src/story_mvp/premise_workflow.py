from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Literal

from .premise_aperture import (
    PremiseLaneBundle,
    build_single_pass_lane_bundle,
    extract_sections,
    render_lane_direction,
)


PREMISE_CANDIDATES_FILENAME = "PREMISE_CANDIDATES.md"
SELECTED_PREMISE_FILENAME = "SELECTED_PREMISE.md"
PREMISE_COMPILER_REPORT_FILENAME = "PREMISE_COMPILER_REPORT.md"
PREMISE_COMPILER_INPUT_FILENAME = "PREMISE_COMPILER_INPUT.md"
PREMISE_SKIPPED_FILENAME = "PREMISE_SKIPPED.md"
PREMISE_CONTRACT_FILENAME = "PREMISE_CONTRACT.md"
PREMISE_LANE_FILENAMES = {
    "world": "PREMISE_WORLD_CONTRACT.md",
    "power": "PREMISE_POWER_CONTRACT.md",
    "human": "PREMISE_HUMAN_CONTRACT.md",
    "story": "PREMISE_STORY_CONTRACT.md",
}

CompilerScope = Literal["candidates", "selected"]


def _read(directory: Path, filename: str) -> str:
    path = directory / filename
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _write(directory: Path, filename: str, content: str) -> None:
    (directory / filename).write_text(content.strip() + "\n", encoding="utf-8")


def _delete(directory: Path, *filenames: str) -> None:
    for filename in filenames:
        path = directory / filename
        if path.is_file():
            path.unlink()


def _candidate_sections(candidates: str) -> dict[str, str]:
    sections = extract_sections(candidates, prefix="S")
    if tuple(sections) != ("S1", "S2", "S3"):
        raise ValueError(
            "Premise Forge 结果必须且只能包含 `## S1` / `## S2` / `## S3` 三张完整候选"
        )
    for section in sections.values():
        build_single_pass_lane_bundle(section)
    return sections


def _normalize_selected(selected: str) -> tuple[str, str]:
    matches = list(re.finditer(r"(?m)^## (S[1-9])(?:｜[^\n]*)?\s*$", selected))
    if len(matches) != 1:
        raise ValueError("Selected Premise 必须且只能包含一张 `## S#｜...` 候选")
    normalized = selected[matches[0].start() :].strip()
    sections = extract_sections(normalized, prefix="S")
    candidate_id = matches[0].group(1)
    if tuple(sections) != (candidate_id,):
        raise ValueError("Selected Premise 包含多张候选或候选编号不一致")
    build_single_pass_lane_bundle(sections[candidate_id])
    return candidate_id, sections[candidate_id].strip()


def _compiler_verdicts(report: str) -> tuple[CompilerScope, dict[str, str]]:
    selected_scope = "# SELECTED PREMISE AUTHORITY COMPILER" in report
    batch_scope = "# PREMISE AUTHORITY COMPILER" in report and not selected_scope
    if selected_scope == batch_scope:
        raise ValueError(
            "Premise Compiler Report 必须来自 batch Compiler 或 selected-card Compiler，且只能属于一种 scope"
        )
    sections = extract_sections(report, prefix="S")
    expected_count = 1 if selected_scope else 3
    if len(sections) != expected_count:
        raise ValueError(
            f"Premise Compiler Report 的候选数量无效：期望 {expected_count}，实际 {len(sections)}"
        )
    if not selected_scope and tuple(sections) != ("S1", "S2", "S3"):
        raise ValueError("Batch Premise Compiler Report 必须依次包含 S1 / S2 / S3")
    verdicts: dict[str, str] = {}
    for candidate_id, section in sections.items():
        match = re.search(
            r"(?mi)^\s*-\s*Verdict:\s*(CONDITIONAL PASS|PASS|FAIL)\s*$",
            section,
        )
        if not match:
            raise ValueError(f"Premise Compiler Report 的 {candidate_id} 缺少严格 `- Verdict:`")
        verdicts[candidate_id] = match.group(1).upper()
    return ("selected" if selected_scope else "candidates"), verdicts


def _compiler_input_scope(content: str) -> CompilerScope:
    try:
        _candidate_sections(content)
    except ValueError:
        _normalize_selected(content)
        return "selected"
    return "candidates"


def _contract_files(directory: Path) -> dict[str, str]:
    return {
        lane: _read(directory, filename)
        for lane, filename in PREMISE_LANE_FILENAMES.items()
    }


def _combined_contract(
    *, candidate_id: str, compiler_scope: CompilerScope, contracts: dict[str, str]
) -> str:
    labels = {
        "world": "WORLD LANE CONTRACT",
        "power": "POWER LANE CONTRACT",
        "human": "HUMAN LANE CONTRACT",
        "story": "STORY LANE CONTRACT",
    }
    chunks = [
        "# FROZEN PREMISE CONTRACT",
        f"Selected Candidate: {candidate_id}",
        f"Compiler Scope: {compiler_scope}",
        "Compiler Verdict: PASS",
        "Raw Premise Card Runtime Policy: DISCARD AFTER AUTHORITY COMPILATION",
    ]
    for lane in ("world", "power", "human", "story"):
        chunks.extend(("", f"## {labels[lane]}", "", contracts[lane].strip()))
    return "\n".join(chunks).strip() + "\n"


def _clear_contract(directory: Path) -> str:
    old = _read(directory, PREMISE_CONTRACT_FILENAME)
    _delete(
        directory,
        PREMISE_CONTRACT_FILENAME,
        *PREMISE_LANE_FILENAMES.values(),
    )
    return old


def _record_contract_change(directory: Path, old: str, new: str) -> None:
    if old == new:
        return
    from .storage import invalidate_creative_authorities_for_premise_change
    from .workflow_state import record_content_change

    invalidate_creative_authorities_for_premise_change(directory)
    record_content_change(
        directory,
        "premise.contract",
        old,
        new,
        source="premise_author_decision",
    )


def _ensure_premise_mutable(directory: Path) -> None:
    state_path = directory / "CREATIVE_STATE.json"
    if not state_path.is_file():
        return
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"CREATIVE_STATE.json 无法解析：{error}") from error
    world = state.get("world_vision", {}) if isinstance(state, dict) else {}
    if isinstance(world, dict) and world.get("status") == "author_approved":
        raise ValueError("World Vision 已批准；Premise 决定已冻结，不能再修改或跳过")


def read_premise_payload(directory: Path) -> dict[str, Any]:
    candidates = _read(directory, PREMISE_CANDIDATES_FILENAME)
    selected = _read(directory, SELECTED_PREMISE_FILENAME)
    compiler_report = _read(directory, PREMISE_COMPILER_REPORT_FILENAME)
    compiler_input = _read(directory, PREMISE_COMPILER_INPUT_FILENAME)
    skipped = bool(_read(directory, PREMISE_SKIPPED_FILENAME).strip())
    combined_contract = _read(directory, PREMISE_CONTRACT_FILENAME)
    contracts = _contract_files(directory)

    active = any(
        value.strip()
        for value in (candidates, selected, compiler_report, compiler_input, combined_contract, *contracts.values())
    )
    if skipped and active:
        raise ValueError("Premise 状态无效：SKIPPED 与 active premise files 同时存在")

    contract_presence = [bool(combined_contract.strip()), *(bool(value.strip()) for value in contracts.values())]
    if any(contract_presence) and not all(contract_presence):
        raise ValueError("Premise 状态无效：lane contract 文件不完整")
    approved = all(contract_presence)

    selected_id = ""
    normalized_selected = ""
    if selected.strip():
        selected_id, normalized_selected = _normalize_selected(selected)

    compiler_scope = ""
    verdicts: dict[str, str] = {}
    if compiler_report.strip():
        compiler_scope, verdicts = _compiler_verdicts(compiler_report)
        if not compiler_input.strip():
            raise ValueError("Premise Compiler Report 缺少对应的 Compiler Input snapshot")

    selected_verdict = verdicts.get(selected_id, "") if selected_id else ""
    compiled_input_matches = False
    if normalized_selected and compiler_scope:
        if compiler_scope == "selected":
            _, compiled_selected = _normalize_selected(compiler_input)
            compiled_input_matches = compiled_selected == normalized_selected
        else:
            compiled_sections = _candidate_sections(compiler_input)
            compiled_input_matches = compiled_sections.get(selected_id, "").strip() == normalized_selected

    can_approve = (
        bool(normalized_selected)
        and selected_verdict == "PASS"
        and compiled_input_matches
        and not approved
    )
    if approved:
        status = "approved"
    elif skipped:
        status = "skipped"
    elif normalized_selected and compiler_report.strip():
        status = "compiler_pass" if can_approve else "compiler_blocked"
    elif compiler_report.strip():
        status = "compiled"
    elif normalized_selected:
        status = "selected"
    elif candidates.strip():
        status = "candidates_ready"
    else:
        status = "not_started"

    started_unapproved = status not in {"not_started", "skipped", "approved"}
    return {
        "optional": True,
        "status": status,
        "started_unapproved": started_unapproved,
        "ready_for_authority": not started_unapproved,
        "candidates": candidates,
        "selected": normalized_selected,
        "selected_id": selected_id,
        "compiler_report": compiler_report,
        "compiler_input": compiler_input,
        "compiler_scope": compiler_scope,
        "compiler_verdicts": verdicts,
        "selected_verdict": selected_verdict,
        "compiled_input_matches": compiled_input_matches,
        "can_approve": can_approve,
        "approved": approved,
        "skipped": skipped,
        "combined_contract": combined_contract,
        "contracts": contracts if approved else {lane: "" for lane in PREMISE_LANE_FILENAMES},
    }


def save_premise_candidates(directory: Path, content: str) -> dict[str, Any]:
    _ensure_premise_mutable(directory)
    _candidate_sections(content)
    old_contract = _clear_contract(directory)
    _write(directory, PREMISE_CANDIDATES_FILENAME, content)
    _delete(
        directory,
        SELECTED_PREMISE_FILENAME,
        PREMISE_COMPILER_REPORT_FILENAME,
        PREMISE_COMPILER_INPUT_FILENAME,
        PREMISE_SKIPPED_FILENAME,
    )
    _record_contract_change(directory, old_contract, "")
    return read_premise_payload(directory)


def save_selected_premise(directory: Path, content: str) -> dict[str, Any]:
    _ensure_premise_mutable(directory)
    candidates = _read(directory, PREMISE_CANDIDATES_FILENAME)
    candidate_sections = _candidate_sections(candidates)
    candidate_id, selected = _normalize_selected(content)
    if candidate_id not in candidate_sections:
        raise ValueError(f"Selected Premise 的 {candidate_id} 不存在于当前 Forge candidates")
    old_contract = _clear_contract(directory)
    _write(directory, SELECTED_PREMISE_FILENAME, selected)
    _delete(directory, PREMISE_SKIPPED_FILENAME)
    _record_contract_change(directory, old_contract, "")
    return read_premise_payload(directory)


def record_premise_compiler_input(
    directory: Path, *, scope: CompilerScope
) -> str:
    """Bind a future Compiler report to the exact text present at prompt generation."""

    _ensure_premise_mutable(directory)
    if scope == "selected":
        compiler_input = _read(directory, SELECTED_PREMISE_FILENAME)
        _normalize_selected(compiler_input)
    else:
        compiler_input = _read(directory, PREMISE_CANDIDATES_FILENAME)
        _candidate_sections(compiler_input)
    old_contract = _clear_contract(directory)
    _write(directory, PREMISE_COMPILER_INPUT_FILENAME, compiler_input)
    _delete(
        directory,
        PREMISE_COMPILER_REPORT_FILENAME,
        PREMISE_SKIPPED_FILENAME,
    )
    _record_contract_change(directory, old_contract, "")
    return compiler_input.strip()


def save_premise_compiler_report(directory: Path, content: str) -> dict[str, Any]:
    _ensure_premise_mutable(directory)
    scope, _ = _compiler_verdicts(content)
    compiler_input = _read(directory, PREMISE_COMPILER_INPUT_FILENAME)
    if not compiler_input.strip():
        raise ValueError(
            "Premise Compiler Report 缺少 Prompt 生成时的 Input snapshot；请重新生成 Compiler Prompt"
        )
    input_scope = _compiler_input_scope(compiler_input)
    if input_scope != scope:
        raise ValueError(
            f"Premise Compiler Report scope={scope} 与 Input snapshot scope={input_scope} 不一致"
        )
    old_contract = _clear_contract(directory)
    _write(directory, PREMISE_COMPILER_REPORT_FILENAME, content)
    _delete(directory, PREMISE_SKIPPED_FILENAME)
    _record_contract_change(directory, old_contract, "")
    return read_premise_payload(directory)


def approve_premise(directory: Path) -> dict[str, Any]:
    payload = read_premise_payload(directory)
    if payload["approved"]:
        return payload
    _ensure_premise_mutable(directory)
    if not payload["can_approve"]:
        if payload["selected_verdict"] != "PASS":
            raise ValueError(
                "Selected Premise 必须获得 strict PASS；CONDITIONAL PASS / FAIL 只能返回作者处理"
            )
        if not payload["compiled_input_matches"]:
            raise ValueError("Selected Premise 已在 Compiler 之后被编辑，必须重新独立编译")
        raise ValueError("Premise 尚未满足批准条件")

    candidate_id = str(payload["selected_id"])
    selected = str(payload["selected"])
    bundle: PremiseLaneBundle = build_single_pass_lane_bundle(selected)
    contracts = {
        lane: render_lane_direction(bundle, lane=lane)  # type: ignore[arg-type]
        for lane in ("world", "power", "human", "story")
    }
    combined = _combined_contract(
        candidate_id=candidate_id,
        compiler_scope=payload["compiler_scope"],
        contracts=contracts,
    )
    old_contract = _read(directory, PREMISE_CONTRACT_FILENAME)
    for lane, filename in PREMISE_LANE_FILENAMES.items():
        _write(directory, filename, contracts[lane])
    _write(directory, PREMISE_CONTRACT_FILENAME, combined)
    _delete(directory, PREMISE_SKIPPED_FILENAME)
    _record_contract_change(directory, old_contract, combined)
    return read_premise_payload(directory)


def skip_premise(directory: Path) -> dict[str, Any]:
    _ensure_premise_mutable(directory)
    old_contract = _clear_contract(directory)
    _delete(
        directory,
        PREMISE_CANDIDATES_FILENAME,
        SELECTED_PREMISE_FILENAME,
        PREMISE_COMPILER_REPORT_FILENAME,
        PREMISE_COMPILER_INPUT_FILENAME,
    )
    _write(
        directory,
        PREMISE_SKIPPED_FILENAME,
        "# PREMISE APERTURE DECISION\n\nSKIPPED BY AUTHOR\n",
    )
    _record_contract_change(directory, old_contract, "")
    return read_premise_payload(directory)
