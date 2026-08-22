from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from story_mvp.scene_skills import parse_scene_skill_selection  # noqa: E402

REQUIRED = (
    "director_prompt.md",
    "director_response.md",
    "curator_prompt.md",
    "curator_response.md",
    "primary_prompt.md",
    "primary_response.md",
    "chapter.md",
    "chapter_fact_summary.md",
    "state_delta_prompt.md",
    "state_delta_response.md",
    "BOOK_after_state_delta.md",
)

PLANNING_LEAK_MARKERS = (
    "验证",
    "闭环",
    "阶段推进",
    "价值兑现",
    "成长空间",
    "建立优势",
    "事件合同",
    "Scene Skill",
    "Primary Writer",
    "Context Curator",
    "Curator",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def chapter_dir(number: int) -> Path:
    return ROOT / f"chapter-{number:04d}"


def main() -> int:
    missing: list[str] = []
    trace: list[dict[str, object]] = []
    combined: list[str] = []
    primary_counts: Counter[str] = Counter()
    secondary_counts: Counter[str] = Counter()
    leakage: dict[str, list[str]] = {}

    for number in range(1, 11):
        folder = chapter_dir(number)
        if not folder.is_dir():
            missing.append(str(folder.relative_to(ROOT)))
            continue
        for name in REQUIRED:
            if not (folder / name).is_file():
                missing.append(str((folder / name).relative_to(ROOT)))

        curator = read(folder / "curator_response.md")
        primary, secondary = parse_scene_skill_selection(curator)
        body = read(folder / "chapter.md").strip()
        if primary:
            primary_counts[primary] += 1
        if secondary:
            secondary_counts[secondary] += 1

        hits = [marker for marker in PLANNING_LEAK_MARKERS if marker in body]
        if hits:
            leakage[f"chapter-{number:04d}"] = hits

        trace.append(
            {
                "chapter": number,
                "primary_scene_skill": primary or None,
                "secondary_scene_skill": secondary or None,
                "chapter_chars": len(body),
                "planning_language_hits": hits,
            }
        )
        if body:
            combined.append(f"# 第{number}章\n\n{body}")

    (ROOT / "SCENE_SKILL_TRACE.json").write_text(
        json.dumps(trace, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (ROOT / "TEN_CHAPTERS_COMBINED.md").write_text(
        "\n\n".join(combined).strip() + ("\n" if combined else ""),
        encoding="utf-8",
    )

    report = [
        "# Deterministic Verification",
        "",
        f"- 完整章节目录：{10 - sum(1 for n in range(1, 11) if not chapter_dir(n).is_dir())}/10",
        f"- 缺失产物：{len(missing)}",
        f"- Primary Scene Skill 分布：{dict(primary_counts)}",
        f"- Secondary Scene Skill 分布：{dict(secondary_counts)}",
        f"- 正文后台术语命中章节：{len(leakage)}",
        "",
        "## Missing Artifacts",
        "",
        *(f"- {item}" for item in missing),
        "" if missing else "- 无",
        "",
        "## Planning-Language Hits",
        "",
    ]
    if leakage:
        report.extend(f"- {chapter}: {', '.join(hits)}" for chapter, hits in leakage.items())
    else:
        report.append("- 无")
    report.extend(
        [
            "",
            "说明：术语命中只用于人工复核，不自动判定正文失败；例如角色世界内自然使用同形词时可以是正常文本。",
        ]
    )
    (ROOT / "DETERMINISTIC_VERIFICATION.md").write_text(
        "\n".join(report).strip() + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "missing": missing,
        "primary_scene_skill_counts": dict(primary_counts),
        "secondary_scene_skill_counts": dict(secondary_counts),
        "planning_language_hits": leakage,
    }, ensure_ascii=False, indent=2))
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
