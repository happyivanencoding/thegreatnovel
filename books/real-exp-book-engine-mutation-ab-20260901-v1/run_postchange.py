from __future__ import annotations

import concurrent.futures
import json
from pathlib import Path

from run_ab import OUT, build_multi_prompt, build_single_prompt, run_acp

CASES = {
    "ning_21_30": build_multi_prompt(21, ""),
    "wen_singleworld": build_single_prompt(""),
}


def run_one(case: str, prompt_text: str) -> dict:
    folder = OUT / case
    prompt = folder / "prompt_POST_CHANGE.md"
    result = folder / "response_POST_CHANGE.json"
    prompt.write_text(prompt_text, encoding="utf-8")
    payload = run_acp(prompt, result, "gpt-5.6-sol", "high")
    text = str(payload["text"])
    (folder / "response_POST_CHANGE.md").write_text(text, encoding="utf-8")
    return {"case": case, "wall_seconds": payload.get("wall_seconds"), "chars": len(text)}


def main() -> None:
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(run_one, case, prompt): case for case, prompt in CASES.items()}
        for fut in concurrent.futures.as_completed(futures):
            row = fut.result()
            rows.append(row)
            print(row, flush=True)
    (OUT / "POST_CHANGE_RUN_SUMMARY.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
