from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp-native-e2e")
sys.path.insert(0, str(ROOT / "temps"))

from atomic_authority_ir_v1 import DirectorStructuredDecision, EntityRegistry
from run_atomic_authority_ir_v1_static import sample_specs
from run_native_structured_e2e import NATIVE_CONFIG
from run_native_structured_e2e import (
    action_surfaces,
    augment_registry,
    narrative_surfaces,
    normalize_native_payload,
    validate_rendered_projection_scope,
)

BASE = ROOT / "books" / "real-exp-native-structured-e2e-20260830-v1"


def _spec(name: str):
    return next(item for item in sample_specs() if item["name"] == name)


def _render(name: str, run: str = "e2e-run4") -> str:
    spec = _spec(name)
    registry = augment_registry(name, EntityRegistry.from_dict(spec["registry"]))
    raw = json.loads(
        (BASE / run / name / "native_director_raw_decision.json").read_text(
            encoding="utf-8"
        )
    )
    payload, changes = normalize_native_payload(name, spec, raw)
    assert not changes
    decision = DirectorStructuredDecision.from_dict(payload)
    return decision.render_human_mission(
        registry=registry,
        surfaces=action_surfaces(name),
        narrative_functions=narrative_surfaces(name),
    )


def test_jiuchui_relationship_surface_never_mentions_shadow_book_entities():
    mission = _render("jiuchui_ch14")
    assert "分影" not in mission
    assert "陆绾" not in mission
    assert "少东家" in mission
    assert "旧主从关系" in mission


def test_all_final_v2_missions_pass_cross_book_projection_scope_guard():
    for run in ("e2e-run4", "e2e-run5"):
        for spec in sample_specs():
            name = spec["name"]
            registry = augment_registry(name, EntityRegistry.from_dict(spec["registry"]))
            mission = (BASE / run / name / "effective_director_mission.md").read_text(
                encoding="utf-8"
            )
            assert validate_rendered_projection_scope(name, mission, registry) == []


def test_human_mission_renderer_has_no_bad_multiclause_punctuation():
    for name in NATIVE_CONFIG:
        mission = _render(name)
        assert "。；" not in mission
        assert all(line.endswith("。") for line in mission.splitlines() if line.strip())


def test_v2_protocol_freeze_hashes_still_match_model_route_files():
    payload = json.loads((BASE / "PROTOCOL_FREEZE_V2.json").read_text(encoding="utf-8"))
    for relative, expected in payload["files"].items():
        path = ROOT / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == expected, relative


def test_final_v2_known_fact_coverage_and_no_fallback():
    for run in ("e2e-run4", "e2e-run5"):
        summary = json.loads((BASE / run / "summary.json").read_text(encoding="utf-8"))
        assert summary["native_director_accepted"] == 4
        assert summary["director_fallbacks"] == 0
        for row in summary["rows"]:
            coverage = row["native_structural_coverage"]
            assert coverage["matched"] == coverage["expected"]
            assert coverage["coverage"] == 1.0


def test_final_analysis_does_not_claim_time_savings_or_production_adoption():
    analysis = json.loads((BASE / "FINAL_ANALYSIS_V2.json").read_text(encoding="utf-8"))
    assert analysis["timing"]["mean_seconds_saved"] < 0
    evidence = json.loads((BASE / "EVIDENCE_INDEX.json").read_text(encoding="utf-8"))
    assert evidence["time_saved_seconds_per_chapter"] == 0
    assert evidence["production_changed"] is False
    validation = json.loads((BASE / "FINAL_VALIDATION.json").read_text(encoding="utf-8"))
    assert validation["production_adoption"] is False
