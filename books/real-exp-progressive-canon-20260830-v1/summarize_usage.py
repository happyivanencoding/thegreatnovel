from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import json


EXP = Path(__file__).resolve().parent


def phase(label: str) -> str:
    if "v2-blind" in label:
        return "v2_blind"
    if "authority-audit" in label:
        return "v2_authority_audit"
    if "progressive-canon-v2-" in label and label.endswith("-refresh"):
        return "v2_story_refresh"
    if "blind-" in label:
        return "v1_blind"
    if label.endswith("-decision"):
        return "decision_surface"
    if label.endswith("-reframe"):
        return "reframe_forge"
    if label.endswith("-compiler"):
        return "canonization_compiler"
    if label.endswith("-refresh"):
        return "v1_story_refresh"
    return "other"


rows = []
for path in EXP.rglob("*_ACP.json"):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("ok") or not data.get("label"):
        continue
    usage = (data.get("result") or {}).get("usage") or {}
    rows.append(
        {
            "path": str(path.relative_to(EXP)),
            "label": data["label"],
            "phase": phase(data["label"]),
            "model": data.get("model"),
            "wall_seconds": data.get("wall_seconds"),
            "total_tokens": usage.get("totalTokens"),
            "input_tokens": usage.get("inputTokens"),
            "cached_read_tokens": usage.get("cachedReadTokens"),
            "output_tokens": usage.get("outputTokens"),
            "thought_tokens": usage.get("thoughtTokens"),
        }
    )

by_model = defaultdict(lambda: defaultdict(float))
by_phase = defaultdict(lambda: defaultdict(float))
for row in rows:
    for bucket, key in ((by_model, row["model"]), (by_phase, row["phase"])):
        bucket[key]["calls"] += 1
        bucket[key]["wall_seconds_sum"] += float(row["wall_seconds"] or 0)
        for field in ("total_tokens", "input_tokens", "cached_read_tokens", "output_tokens", "thought_tokens"):
            bucket[key][field] += int(row[field] or 0)

phase_critical_seconds = sum(
    max((float(r["wall_seconds"] or 0) for r in rows if r["phase"] == p), default=0)
    for p in sorted(by_phase)
)

payload = {
    "calls": len(rows),
    "aggregate_call_wall_seconds": round(sum(float(r["wall_seconds"] or 0) for r in rows), 3),
    "parallel_phase_critical_path_estimate_seconds": round(phase_critical_seconds, 3),
    "tokens": {
        "total": sum(int(r["total_tokens"] or 0) for r in rows),
        "input": sum(int(r["input_tokens"] or 0) for r in rows),
        "cached_read": sum(int(r["cached_read_tokens"] or 0) for r in rows),
        "output": sum(int(r["output_tokens"] or 0) for r in rows),
        "thought": sum(int(r["thought_tokens"] or 0) for r in rows),
    },
    "by_model": {k: dict(v) for k, v in sorted(by_model.items())},
    "by_phase": {k: dict(v) for k, v in sorted(by_phase.items())},
    "credits_or_billed_cost": "N/A — ACP payload exposes token usage and wall-clock but not billed credits/cost; no estimate is fabricated.",
    "rows": sorted(rows, key=lambda x: x["label"]),
}
(EXP / "USAGE.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False, indent=2))
