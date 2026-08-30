from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

WORKTREE = Path(r"C:\dev\tgn-story-mvp-native-e2e")
BASE = WORKTREE / "books" / "real-exp-native-structured-e2e-20260830-v1"
sys.path.insert(0, str(WORKTREE / "temps"))
from run_native_structured_e2e import MODEL, call_acp, source_directory  # noqa: E402

NODE_FILES = (
    ("director", "director_prompt.md"),
    ("curator", "curator_prompt.md"),
    ("primary", "primary_prompt.md"),
    ("reviser", "authority_reviser_prompt.md"),
)


def one(sample: str, run_label: str):
    source = source_directory(sample)
    out = BASE / run_label / sample
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for node, filename in NODE_FILES:
        prompt = out / f"{node}_prompt.md"
        acp = out / f"{node}_acp.json"
        prompt.write_text((source / filename).read_text(encoding="utf-8"), encoding="utf-8")
        model, effort = MODEL[node]
        data = call_acp(prompt, acp, model=model, effort=effort)
        response = str(data.get("text", "")).strip()
        (out / f"{node}_response.md").write_text(response + "\n", encoding="utf-8")
        rows.append({
            "node": node,
            "wall_seconds": float(data.get("wall_seconds") or 0),
            "model": data.get("model"),
            "usage": data.get("result", {}).get("usage", {}),
        })
    return {
        "sample": sample,
        "nodes": rows,
        "total_seconds": round(sum(item["wall_seconds"] for item in rows), 3),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-label", required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    samples = ["jiuchui_ch14", "jiuchui_ch16", "shadow_ch4", "shadow_ch9"]
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(one, sample, args.run_label) for sample in samples]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["sample"])
    by_node = {
        node: round(sum(next(x["wall_seconds"] for x in row["nodes"] if x["node"] == node) for row in rows), 3)
        for node, _ in NODE_FILES
    }
    summary = {
        "schema_version": "fresh-control-timing-v1",
        "run": args.run_label,
        "samples": len(rows),
        "by_node_seconds": by_node,
        "total_seconds": round(sum(row["total_seconds"] for row in rows), 3),
        "rows": rows,
    }
    out = BASE / args.run_label
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
