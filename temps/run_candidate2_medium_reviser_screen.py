from __future__ import annotations

import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = (
    ROOT
    / "books"
    / "real-exp-reviser-noop-upstream-heldout-20260830-v1"
    / "heldout-new-novel-2"
)
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
OUT = BASE / "medium-reviser-screen"


def clean(text: str) -> str:
    return re.sub(
        r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$",
        "",
        text,
    ).strip()


def call(prompt_path: Path, out_path: Path, label: str) -> dict:
    last = ""
    for attempt in range(3):
        try:
            proc = subprocess.run(
                [
                    "node",
                    str(RUNNER),
                    str(prompt_path),
                    str(out_path),
                    "gpt-5.6-luna",
                    "medium",
                    str(ROOT),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=1200,
            )
        except subprocess.TimeoutExpired:
            last = f"timeout {label}"
            time.sleep(2 + attempt * 2)
            continue
        if proc.returncode == 0 and out_path.exists():
            data = json.loads(out_path.read_text(encoding="utf-8"))
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (proc.stderr + "\n" + proc.stdout)[-4000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(f"{label}: {last}")


def body(raw: str) -> str:
    raw = clean(raw)
    return raw.rsplit("# 正式正文", 1)[-1].strip() if "# 正式正文" in raw else raw


def one(run: str, chapter: int) -> dict:
    source = (
        BASE / "runs" / f"chapter-{chapter:04d}"
        if run == "repeat1"
        else BASE / "repeat2" / f"chapter-{chapter:04d}"
    )
    out = OUT / run / f"chapter-{chapter:04d}"
    out.mkdir(parents=True, exist_ok=True)
    prompt = (source / "treatment_reviser_prompt.md").read_text(encoding="utf-8")
    prompt_path = out / "medium_reviser_prompt.md"
    acp_path = out / "medium_reviser_acp.json"
    response_path = out / "medium_reviser_response.md"
    final_path = out / "medium_final_body.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, acp_path, f"{run}-{chapter}")
    raw = str(data.get("text", ""))
    response_path.write_text(raw.strip() + "\n", encoding="utf-8")
    final = body(raw)
    final_path.write_text(final + "\n", encoding="utf-8")
    high_data = json.loads((source / "treatment_reviser_acp.json").read_text(encoding="utf-8"))
    primary_data = json.loads((source / "treatment_primary_acp.json").read_text(encoding="utf-8"))
    return {
        "run": run,
        "chapter": chapter,
        "primary_wall": float(primary_data.get("wall_seconds") or 0),
        "high_reviser_wall": float(high_data.get("wall_seconds") or 0),
        "medium_reviser_wall": float(data.get("wall_seconds") or 0),
    }


def main() -> None:
    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(one, run, chapter)
            for run in ("repeat1", "repeat2")
            for chapter in range(1, 5)
        ]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(row, flush=True)
    rows.sort(key=lambda item: (item["run"], item["chapter"]))
    summary = {
        "schema_version": "candidate2-medium-reviser-screen-v1",
        "rows": rows,
        "mean_high_reviser_wall": round(
            sum(row["high_reviser_wall"] for row in rows) / len(rows), 3
        ),
        "mean_medium_reviser_wall": round(
            sum(row["medium_reviser_wall"] for row in rows) / len(rows), 3
        ),
    }
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
