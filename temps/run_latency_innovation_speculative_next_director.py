from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
SOURCE = BOOK / "runs"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "speculative-next-director"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
TRANSITIONS = ((2, 3), (3, 4), (5, 6), (12, 13), (14, 15), (18, 19))

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.chapter_context import _without_recent_summaries_for_director  # noqa: E402


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def call(prompt_path: Path, output_path: Path) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-luna", "high", str(ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        if process.returncode == 0 and output_path.exists():
            try:
                data = json.loads(output_path.read_text(encoding="utf-8"))
            except Exception as error:
                data = {}
                last = str(error)
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (process.stderr + "\n" + process.stdout)[-3000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(last)


def h2_span(text: str, prefix: str) -> tuple[int, int, str]:
    starts = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(starts):
        if not match.group(1).strip().startswith(prefix):
            continue
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        return match.start(), end, text[match.end():end].strip()
    raise ValueError(f"missing heading prefix: {prefix}")


def replace_h2(text: str, prefix: str, body: str) -> str:
    start, end, _ = h2_span(text, prefix)
    heading = re.match(r"(?m)^##\s+(.+?)\s*$", text[start:end]).group(1).strip()
    return text[:start] + f"## {heading}\n\n{body}\n\n" + text[end:].lstrip()


def old_state_inputs(previous_chapter: int) -> tuple[str, str]:
    text = (SOURCE / f"chapter-{previous_chapter:04d}" / "state_prompt.md").read_text(encoding="utf-8")
    start_marker = "## CANON INDEX——当前规范化 Canon Index（已发生事实的压缩状态）"
    end_marker = "## 本次新正式章节正文（State Delta 的最高事实来源）"
    if start_marker not in text or end_marker not in text:
        raise RuntimeError(f"ch{previous_chapter}: state markers missing")
    block = text.split(start_marker, 1)[1].split(end_marker, 1)[0].strip()
    canon_without_recent = _without_recent_summaries_for_director(block)
    recent_match = re.search(
        r"(?ms)^## RECENT SUMMARIES：\s*(.*?)(?=^## OPEN PROMISES：|\Z)",
        block,
    )
    recent = recent_match.group(1).strip() if recent_match else ""
    return canon_without_recent, recent


def one(previous_chapter: int, next_chapter: int) -> dict:
    source = SOURCE / f"chapter-{next_chapter:04d}"
    directory = OUT / f"chapter-{next_chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    prompt = (source / "director_prompt.md").read_text(encoding="utf-8")
    old_canon, old_recent = old_state_inputs(previous_chapter)
    prompt = replace_h2(prompt, "当前 Canon Index", old_canon or "（当前 Canon Index 为空。）")
    prompt = replace_h2(prompt, "最近 1—3 章摘要", old_recent or "（未提供最近 1—3 章摘要。）")
    prompt_path = directory / "speculative_director_prompt.md"
    output_path = directory / "speculative_director_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    (directory / "speculative_director_response.md").write_text(response + "\n", encoding="utf-8")

    state_data = json.loads((SOURCE / f"chapter-{previous_chapter:04d}" / "state_acp.json").read_text(encoding="utf-8"))
    director_data = json.loads((source / "director_acp.json").read_text(encoding="utf-8"))
    state_wall = float(state_data.get("wall_seconds") or 0)
    control_wall = float(director_data.get("wall_seconds") or 0)
    treatment_wall = float(data.get("wall_seconds") or 0)
    serial = state_wall + control_wall
    parallel = max(state_wall, treatment_wall)
    return {
        "previous_chapter": previous_chapter,
        "chapter": next_chapter,
        "state_wall_seconds": state_wall,
        "control_director_wall_seconds": control_wall,
        "speculative_director_wall_seconds": treatment_wall,
        "control_state_plus_director_seconds": round(serial, 3),
        "parallel_critical_seconds": round(parallel, 3),
        "critical_path_speedup_percent": round((1 - parallel / serial) * 100, 2),
        "prompt_chars": len(prompt),
        "response_chars": len(response),
        "usage": data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=len(TRANSITIONS)) as executor:
        futures = [executor.submit(one, previous, current) for previous, current in TRANSITIONS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
