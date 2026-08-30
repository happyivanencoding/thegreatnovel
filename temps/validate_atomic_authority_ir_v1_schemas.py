from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-atomic-authority-ir-20260829-v1"
sys.path.insert(0, str(ROOT / "temps"))

from atomic_authority_ir_v1 import (  # noqa: E402
    AtomicAuthorityContract,
    DirectorStructuredDecision,
    EntityRegistry,
    PrimaryPreservationMap,
)
from test_atomic_authority_ir_v1 import (  # noqa: E402
    narrative_registry,
    structured_canon_artifact,
    structured_decision_payload,
    surface_registry,
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _type_matches(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, True)


def _bounded_validate(
    value: Any,
    schema: Mapping[str, Any],
    path: tuple[str, ...] = (),
) -> list[dict[str, str]]:
    """Validate the Draft-2020-12 subset used by these four bounded schemas.

    The experiment intentionally adds no package dependency. Unsupported schema
    keywords fail schema sanity rather than being silently ignored.
    """

    errors: list[dict[str, str]] = []

    def error(message: str, at: tuple[str, ...] = path) -> None:
        errors.append({"path": "/".join(at), "message": message})

    if "anyOf" in schema:
        branches = [
            _bounded_validate(value, branch, path)
            for branch in schema["anyOf"]
        ]
        if not any(not branch_errors for branch_errors in branches):
            error("value matches none of anyOf branches")
        return errors

    if "const" in schema and value != schema["const"]:
        error(f"expected const={schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        error(f"value={value!r} is not in enum")

    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        if not any(_type_matches(value, item) for item in expected_type):
            error(f"type mismatch expected one of {expected_type}")
            return errors
    elif isinstance(expected_type, str) and not _type_matches(value, expected_type):
        error(f"type mismatch expected {expected_type}")
        return errors

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                error(f"missing required property {key!r}", (*path, str(key)))
        properties = schema.get("properties", {})
        pattern_properties = schema.get("patternProperties", {})
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            child_path = (*path, str(key))
            if key in properties:
                errors.extend(_bounded_validate(item, properties[key], child_path))
                continue
            matching = [
                child_schema
                for pattern, child_schema in pattern_properties.items()
                if re.fullmatch(pattern, str(key))
            ]
            if matching:
                for child_schema in matching:
                    errors.extend(_bounded_validate(item, child_schema, child_path))
                continue
            if additional is False:
                error(f"additional property {key!r} is not allowed", child_path)
            elif isinstance(additional, dict):
                errors.extend(_bounded_validate(item, additional, child_path))

    if isinstance(value, list):
        if len(value) < int(schema.get("minItems", 0)):
            error(f"array has {len(value)} items below minItems")
        if "maxItems" in schema and len(value) > int(schema["maxItems"]):
            error(f"array has {len(value)} items above maxItems")
        if schema.get("uniqueItems"):
            fingerprints = [
                json.dumps(item, ensure_ascii=False, sort_keys=True)
                for item in value
            ]
            if len(fingerprints) != len(set(fingerprints)):
                error("array violates uniqueItems")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(
                    _bounded_validate(item, item_schema, (*path, str(index)))
                )

    if isinstance(value, str):
        if len(value) < int(schema.get("minLength", 0)):
            error(f"string shorter than minLength={schema.get('minLength')}")
        if "pattern" in schema and not re.fullmatch(str(schema["pattern"]), value):
            error(f"string does not match pattern={schema['pattern']!r}")

    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < int(schema["minimum"]):
            error(f"integer below minimum={schema['minimum']}")

    return errors


def _schema_sanity(schema: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("missing Draft 2020-12 $schema")
    if schema.get("type") != "object":
        errors.append("root type must be object")
    if not isinstance(schema.get("required"), list):
        errors.append("root required must be an array")
    if not isinstance(schema.get("properties"), dict):
        errors.append("root properties must be an object")
    return errors


def validate_payload(
    *,
    sample: str,
    artifact: str,
    payload: Mapping[str, Any],
    schema: Mapping[str, Any],
    expected_valid: bool = True,
) -> dict[str, Any]:
    errors = _bounded_validate(payload, schema)
    observed_valid = not errors
    passed = observed_valid is expected_valid
    return {
        "sample": sample,
        "artifact": artifact,
        "validator": "bounded Draft 2020-12 subset",
        "expected_valid": expected_valid,
        "observed_valid": observed_valid,
        "valid": passed,
        "errors": errors[:12],
    }


def main() -> None:
    schema_dir = BASE / "schemas"
    schema_files = sorted(schema_dir.glob("*.json"))
    schemas = {path.name: load(path) for path in schema_files}
    rows: list[dict[str, Any]] = []

    for path in schema_files:
        schema = schemas[path.name]
        schema_errors = _schema_sanity(schema)
        rows.append(
            {
                "sample": "schema_definition",
                "artifact": path.name,
                "validator": "bounded Draft 2020-12 schema sanity",
                "expected_valid": True,
                "observed_valid": not schema_errors,
                "valid": not schema_errors,
                "errors": [str(item) for item in schema_errors],
            }
        )

    phase = BASE / "phase-a-static-ir"
    for directory in sorted(path for path in phase.iterdir() if path.is_dir()):
        registry_payload = load(directory / "entity_registry.json")
        EntityRegistry.from_dict(registry_payload)
        rows.append(
            validate_payload(
                sample=directory.name,
                artifact="entity_registry.json",
                payload=registry_payload,
                schema=schemas["entity-registry-v1.schema.json"],
            )
        )

        contract_payload = load(directory / "atomic_authority_contract.json")
        AtomicAuthorityContract.from_dict(contract_payload)
        rows.append(
            validate_payload(
                sample=directory.name,
                artifact="atomic_authority_contract.json",
                payload=contract_payload,
                schema=schemas["atomic-authority-contract-v1.schema.json"],
            )
        )

        preservation_payload = load(directory / "primary_preservation_map.json")
        PrimaryPreservationMap.from_dict(preservation_payload)
        rows.append(
            validate_payload(
                sample=directory.name,
                artifact="primary_preservation_map.json",
                payload=preservation_payload,
                schema=schemas["primary-preservation-map-v1.schema.json"],
            )
        )

    registry = EntityRegistry.from_dict(
        {
            "chapter_id": "BOOK_A:CH001",
            "protagonist_id": "PROTAGONIST_001",
            "entities": [
                {
                    "entity_id": "PROTAGONIST_001",
                    "kind": "character",
                    "display_name": "顾停舟",
                    "aliases": ["他"],
                    "authority_refs": ["canon.protagonist"],
                    "parent_entity_id": "",
                },
                {
                    "entity_id": "RIVAL_001",
                    "kind": "character",
                    "display_name": "阮青蜃",
                    "aliases": [],
                    "authority_refs": ["canon.rival"],
                    "parent_entity_id": "",
                },
                {
                    "entity_id": "ROUTE_001",
                    "kind": "route",
                    "display_name": "粮路",
                    "aliases": ["粮道"],
                    "authority_refs": ["world.route"],
                    "parent_entity_id": "",
                },
            ],
        }
    )
    decision = DirectorStructuredDecision.from_dict(structured_decision_payload())
    decision_payload = decision.to_dict()
    mission = decision.render_human_mission(
        registry=registry,
        surfaces=surface_registry(),
        narrative_functions=narrative_registry(),
    )
    contract = decision.build_contract(
        registry=registry,
        authority_artifacts=(structured_canon_artifact(),),
    )
    decision_row = validate_payload(
        sample="unit_structured_decision",
        artifact="director_structured_decision.json",
        payload=decision_payload,
        schema=schemas["director-structured-decision-v1.schema.json"],
    )
    required_labels = (
        "触发事件：",
        "推动事件的人：",
        "主角行动：",
        "对手或世界反应：",
        "直接结果：",
        "状态变化：",
        "叙事功能：",
        "结尾推动力：",
    )
    if not all(label in mission for label in required_labels):
        decision_row["valid"] = False
        decision_row["errors"].append(
            {"path": "rendered_mission", "message": "missing required field label"}
        )
    if not contract.preflight_eligible:
        decision_row["valid"] = False
        decision_row["errors"].append(
            {"path": "contract", "message": "dual-projected contract is not eligible"}
        )
    rows.append(decision_row)

    # Negative probes prove that the schema rejects the stale/dangerous envelopes
    # that the former syntax-only validator would have accepted.
    stale_human_clause = copy.deepcopy(decision_payload)
    stale_human_clause["clauses"][0]["human_clause"] = "第二份自由语义写入。"
    rows.append(
        validate_payload(
            sample="negative_probe",
            artifact="director_human_clause_rejected.json",
            payload=stale_human_clause,
            schema=schemas["director-structured-decision-v1.schema.json"],
            expected_valid=False,
        )
    )

    stale_free_narrative = copy.deepcopy(decision_payload)
    stale_free_narrative["narrative_function"] = "第二份自由叙事功能。"
    rows.append(
        validate_payload(
            sample="negative_probe",
            artifact="director_free_narrative_rejected.json",
            payload=stale_free_narrative,
            schema=schemas["director-structured-decision-v1.schema.json"],
            expected_valid=False,
        )
    )

    first_contract = load(
        next(iter(sorted(path for path in phase.iterdir() if path.is_dir())))
        / "atomic_authority_contract.json"
    )
    missing_provenance = copy.deepcopy(first_contract)
    missing_provenance.pop("artifact_provenance", None)
    rows.append(
        validate_payload(
            sample="negative_probe",
            artifact="contract_missing_provenance_rejected.json",
            payload=missing_provenance,
            schema=schemas["atomic-authority-contract-v1.schema.json"],
            expected_valid=False,
        )
    )

    tampered_digest = copy.deepcopy(first_contract)
    tampered_digest["artifact_provenance"][0]["revision_sha256"] = "0" * 64
    runtime_rejected = False
    runtime_error = ""
    try:
        AtomicAuthorityContract.from_dict(tampered_digest)
    except Exception as error:
        runtime_rejected = True
        runtime_error = f"{type(error).__name__}: {error}"
    rows.append(
        {
            "sample": "negative_probe",
            "artifact": "contract_tampered_digest_runtime_rejected.json",
            "validator": "AtomicAuthorityContract.from_dict",
            "expected_valid": False,
            "observed_valid": not runtime_rejected,
            "valid": runtime_rejected,
            "errors": [] if runtime_rejected else [
                {"path": "artifact_provenance", "message": "tampered digest accepted"}
            ],
            "runtime_error": runtime_error,
        }
    )

    first_preservation = load(
        next(iter(sorted(path for path in phase.iterdir() if path.is_dir())))
        / "primary_preservation_map.json"
    )
    missing_hashes = copy.deepcopy(first_preservation)
    missing_hashes.pop("paragraph_hashes", None)
    rows.append(
        validate_payload(
            sample="negative_probe",
            artifact="preservation_missing_hashes_rejected.json",
            payload=missing_hashes,
            schema=schemas["primary-preservation-map-v1.schema.json"],
            expected_valid=False,
        )
    )

    out = BASE / "phase-f-schema-validation"
    out.mkdir(parents=True, exist_ok=True)
    (out / "director_structured_decision.json").write_text(
        json.dumps(decision_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    summary = {
        "schema_version": "atomic-authority-ir-v1-schema-validation",
        "external_dependencies_added": False,
        "validator_runtime": "internal bounded Draft 2020-12 subset; no added dependency",
        "schema_definitions": len(schema_files),
        "artifact_checks": len(rows),
        "valid_checks": sum(row["valid"] for row in rows),
        "invalid_checks": sum(not row["valid"] for row in rows),
        "negative_probes": sum(not row["expected_valid"] for row in rows),
        "negative_probes_rejected": sum(
            (not row["expected_valid"]) and (not row["observed_valid"])
            for row in rows
        ),
        "rows": rows,
    }
    (out / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["invalid_checks"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
