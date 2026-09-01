from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"
OUT = ROOT / "books" / "real-exp-longitudinal-story-engine-20260901-v1"
ACP = ROOT / "temps" / "acp_text_runner.py"
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.character_prompts import generate_split_prompt


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def gbrain_result(start: int, end: int) -> str:
    path = BOOK / "planning" / f"story-{start:02d}-{end:02d}" / "gbrain.json"
    data = json.loads(read(path))
    return str(data.get("result") or "")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("start", type=int, choices=(21, 31))
    args = parser.parse_args()
    start = args.start
    end = start + 9
    previous = "STORY_PROGRAM_11_20.md" if start == 21 else "STORY_PROGRAM_21_30.md"
    folder = OUT / f"treatment-{start:02d}-{end:02d}"
    folder.mkdir(parents=True, exist_ok=True)

    prompt = generate_split_prompt(
        mode="story_refresh",
        book_content=read(BOOK / f"BOOK_AFTER_CH{start-1:02d}.md"),
        creative_direction=(
            f"《我身藏诸界》第{start}—{end}章重新做一次 frozen-authority Story Refresh 回归。"
            "不改已批准 World / Character / Canon；只测试当前 production Story Refresh 是否能让跨 Horizon 长线真正推进、"
            "让回归主世界反哺长篇，并让多个机会通过人物行动碰撞而非任务菜单出现。"
        ),
        world_vision=read(BOOK / "WORLD_VISION.md"),
        world_expansions=read(BOOK / "WORLD_EXPANSIONS.md"),
        character_card=read(BOOK / "CHARACTER.md"),
        current_character=read(BOOK / "planning" / f"current-character-through-{start-1}.md"),
        creative_state={
            "world_vision": {"status": "author_approved"},
            "character_card": {"status": "author_approved"},
            "proposal": {"status": "author_approved"},
        },
        proposal_context=read(BOOK / previous),
        selected_references=[],
        gbrain_inspiration=gbrain_result(start, end),
        effective_from_chapter=start,
    )
    prompt_path = folder / "prompt.md"
    response_path = folder / "response.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    cmd = [
        sys.executable,
        str(ACP),
        "--model", "gpt-5.6-sol",
        "--effort", "high",
        "--prompt-file", str(prompt_path),
        "--output", str(response_path),
        "--timeout", "9000",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=9300)
    (folder / "runner_stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (folder / "runner_stderr.txt").write_text(proc.stderr, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    print(f"TREATMENT_READY {start}-{end} {response_path.stat().st_size}")


if __name__ == "__main__":
    main()
