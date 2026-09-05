"""Real Incident Snapshot regression evaluator.

This module belongs to TGN's experiment/regression layer.  It deliberately does not
sit on the production generation path and it is not a semantic safety classifier.
Each corpus case captures one real historical failure at the earliest useful
boundary, plus narrow case-specific assertions calibrated against a known-bad and a
known-good output.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORPUS_ROOT = PROJECT_ROOT / "evals" / "real_incident_snapshots"
SUPPORTED_ASSERTIONS = frozenset(
    {
        "contains_all",
        "contains_any",
        "not_contains_any",
        "ordered",
        "count",
    }
)


@dataclass(frozen=True)
class SnapshotCase:
    case_id: str
    title: str
    boundary: str
    failure_class: str
    detects: str
    on_failure: str
    source_evidence: tuple[str, ...]
    snapshot_path: Path
    known_bad_path: Path
    known_good_path: Path
    assertions: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class SnapshotResult:
    case_id: str
    passed: bool
    failures: tuple[str, ...]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Snapshot 文件不存在：{path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Snapshot JSON 无法解析：{path}") from error
    if not isinstance(value, dict):
        raise ValueError(f"Snapshot JSON 顶层必须是 object：{path}")
    return value


def load_case(case_directory: Path) -> SnapshotCase:
    metadata_path = case_directory / "case.json"
    value = _read_json(metadata_path)
    required = (
        "id",
        "title",
        "boundary",
        "failure_class",
        "detects",
        "on_failure",
        "source_evidence",
        "files",
        "assertions",
    )
    missing = [key for key in required if key not in value]
    if missing:
        raise ValueError(f"{metadata_path} 缺少字段：{'、'.join(missing)}")

    case_id = str(value["id"]).strip()
    if case_id != case_directory.name:
        raise ValueError(f"Snapshot ID 与目录名不一致：{case_id} != {case_directory.name}")

    files = value["files"]
    if not isinstance(files, dict):
        raise ValueError(f"{case_id} files 必须是 object")
    file_names = {name: str(files.get(name, "")).strip() for name in ("snapshot", "known_bad", "known_good")}
    if not all(file_names.values()):
        raise ValueError(f"{case_id} 必须声明 snapshot / known_bad / known_good")

    assertions = value["assertions"]
    if not isinstance(assertions, list) or not assertions:
        raise ValueError(f"{case_id} 至少需要一个 case-specific assertion")
    normalized: list[dict[str, Any]] = []
    for index, assertion in enumerate(assertions, start=1):
        if not isinstance(assertion, dict):
            raise ValueError(f"{case_id} assertion {index} 必须是 object")
        kind = str(assertion.get("kind", "")).strip()
        if kind not in SUPPORTED_ASSERTIONS:
            raise ValueError(f"{case_id} assertion {index} 不支持 kind={kind!r}")
        normalized.append(dict(assertion))

    source_evidence = value["source_evidence"]
    if not isinstance(source_evidence, list) or not source_evidence:
        raise ValueError(f"{case_id} 必须记录至少一个真实历史 evidence 路径")

    return SnapshotCase(
        case_id=case_id,
        title=str(value["title"]).strip(),
        boundary=str(value["boundary"]).strip(),
        failure_class=str(value["failure_class"]).strip(),
        detects=str(value["detects"]).strip(),
        on_failure=str(value["on_failure"]).strip(),
        source_evidence=tuple(str(item).strip() for item in source_evidence if str(item).strip()),
        snapshot_path=case_directory / file_names["snapshot"],
        known_bad_path=case_directory / file_names["known_bad"],
        known_good_path=case_directory / file_names["known_good"],
        assertions=tuple(normalized),
    )


def load_corpus(root: Path = DEFAULT_CORPUS_ROOT) -> tuple[SnapshotCase, ...]:
    manifest = _read_json(root / "manifest.json")
    if manifest.get("schema_version") != 1:
        raise ValueError("Real Incident Snapshot manifest 目前只支持 schema_version=1")
    case_ids = manifest.get("cases")
    if not isinstance(case_ids, list) or not case_ids:
        raise ValueError("Snapshot manifest cases 必须是非空数组")
    normalized_ids = tuple(str(case_id).strip() for case_id in case_ids)
    if len(normalized_ids) != len(set(normalized_ids)):
        raise ValueError("Snapshot manifest 含重复 case ID")
    return tuple(load_case(root / case_id) for case_id in normalized_ids)


def _values(assertion: Mapping[str, Any], case_id: str, kind: str) -> tuple[str, ...]:
    raw = assertion.get("values")
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"{case_id} {kind} assertion 需要非空 values")
    values = tuple(str(value) for value in raw if str(value))
    if not values:
        raise ValueError(f"{case_id} {kind} assertion values 不能为空")
    return values


def evaluate_text(case: SnapshotCase, text: str) -> SnapshotResult:
    failures: list[str] = []
    for index, assertion in enumerate(case.assertions, start=1):
        kind = str(assertion["kind"])
        label = str(assertion.get("label", f"assertion-{index}"))
        if kind == "contains_all":
            missing = [value for value in _values(assertion, case.case_id, kind) if value not in text]
            if missing:
                failures.append(f"{label}: 缺少 {missing!r}")
        elif kind == "contains_any":
            values = _values(assertion, case.case_id, kind)
            if not any(value in text for value in values):
                failures.append(f"{label}: 一个候选锚点都未出现 {list(values)!r}")
        elif kind == "not_contains_any":
            present = [value for value in _values(assertion, case.case_id, kind) if value in text]
            if present:
                failures.append(f"{label}: 出现已知回归锚点 {present!r}")
        elif kind == "ordered":
            cursor = -1
            for value in _values(assertion, case.case_id, kind):
                cursor = text.find(value, cursor + 1)
                if cursor < 0:
                    failures.append(f"{label}: 未按顺序找到 {value!r}")
                    break
        elif kind == "count":
            value = str(assertion.get("value", ""))
            if not value:
                raise ValueError(f"{case.case_id} count assertion 需要 value")
            actual = text.count(value)
            minimum = assertion.get("min")
            maximum = assertion.get("max")
            exact = assertion.get("exact")
            if exact is not None and actual != int(exact):
                failures.append(f"{label}: {value!r} 次数={actual}，要求 exact={int(exact)}")
            if minimum is not None and actual < int(minimum):
                failures.append(f"{label}: {value!r} 次数={actual}，要求 min={int(minimum)}")
            if maximum is not None and actual > int(maximum):
                failures.append(f"{label}: {value!r} 次数={actual}，要求 max={int(maximum)}")
    return SnapshotResult(case.case_id, not failures, tuple(failures))


def calibrate_case(case: SnapshotCase) -> tuple[SnapshotResult, SnapshotResult]:
    bad = evaluate_text(case, case.known_bad_path.read_text(encoding="utf-8"))
    good = evaluate_text(case, case.known_good_path.read_text(encoding="utf-8"))
    if bad.passed:
        raise ValueError(f"{case.case_id} 校准失败：known_bad 竟然 PASS；该 case 没有检测到历史事故")
    if not good.passed:
        raise ValueError(
            f"{case.case_id} 校准失败：known_good 仍 FAIL：{'；'.join(good.failures)}"
        )
    return bad, good


def validate_corpus(root: Path = DEFAULT_CORPUS_ROOT) -> tuple[SnapshotCase, ...]:
    cases = load_corpus(root)
    for case in cases:
        for path in (case.snapshot_path, case.known_bad_path, case.known_good_path):
            if not path.is_file() or not path.read_text(encoding="utf-8").strip():
                raise ValueError(f"{case.case_id} 缺少非空文件：{path.name}")
        for evidence in case.source_evidence:
            evidence_path = PROJECT_ROOT / evidence
            if not evidence_path.is_file():
                raise ValueError(f"{case.case_id} 历史 evidence 不存在：{evidence}")
        calibrate_case(case)
    return cases


def evaluate_file(case: SnapshotCase, response_path: Path) -> SnapshotResult:
    return evaluate_text(case, response_path.read_text(encoding="utf-8"))


def _find_case(cases: Iterable[SnapshotCase], case_id: str) -> SnapshotCase:
    for case in cases:
        if case.case_id == case_id:
            return case
    raise ValueError(f"未知 Snapshot case：{case_id}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TGN Real Incident Snapshot Eval Corpus")
    parser.add_argument("--root", type=Path, default=DEFAULT_CORPUS_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="校准全部历史 known-bad / known-good case")
    sub.add_parser("list", help="列出当前 corpus")
    check = sub.add_parser("check", help="用单个历史 case 检查一个候选输出")
    check.add_argument("case_id")
    check.add_argument("response", type=Path)
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    cases = load_corpus(args.root)
    if args.command == "validate":
        validate_corpus(args.root)
        print(f"PASS: {len(cases)} Real Incident Snapshot cases calibrated")
        return 0
    if args.command == "list":
        for case in cases:
            print(f"{case.case_id}\t{case.boundary}\t{case.title}")
        return 0
    case = _find_case(cases, args.case_id)
    result = evaluate_file(case, args.response)
    if result.passed:
        print(f"PASS: {case.case_id} — {case.title}")
        return 0
    print(f"FAIL: {case.case_id} — {case.title}")
    for failure in result.failures:
        print(f"- {failure}")
    print(f"下一步：{case.on_failure}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
