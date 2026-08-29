from __future__ import annotations

from pathlib import Path
import json
import sys


ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-premise-aperture-20260829-v1" / "fast_multiworld"
REPAIR = BASE / "compilable_single_v5_repair"
EXP = BASE / "downstream_S2_repaired_v5"
sys.path.insert(0, str(ROOT / "temps"))

import run_premise_compilable_v4_downstream as harness  # noqa: E402


def main() -> None:
    summary = json.loads((REPAIR / "RUN_SUMMARY.json").read_text(encoding="utf-8"))
    if summary.get("compiler_verdict") != "PASS":
        raise RuntimeError("selected repaired premise is not compiler PASS")
    synthetic = (REPAIR / "REPAIRED_FORGE_RESPONSE.md").read_text(encoding="utf-8")
    (REPAIR / "RESPONSE.md").write_text(synthetic, encoding="utf-8")

    harness.FORGE = REPAIR
    harness.EXP = EXP
    harness.main()


if __name__ == "__main__":
    main()
