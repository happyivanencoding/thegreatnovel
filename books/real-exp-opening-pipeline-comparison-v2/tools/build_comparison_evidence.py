"""Build non-production comparison evidence and blind-reading material."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SINGLE_ROOT = ROOT.parent / "real-exp-opening-three-chapter-hook-v1"
CANDIDATES = {"candidate-b": "《炉藏万象》", "candidate-c": "《掌中天工》"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def execution(candidate: str, chapter: int) -> dict:
    path = ROOT / candidate / "runs" / f"chapter-{chapter:04d}" / "execution.json"
    return json.loads(read(path))


def as_int(value: object) -> int:
    return value if isinstance(value, int) else 0


def build_efficiency() -> None:
    lines = [
        "# Efficiency report",
        "",
        "Hybrid token fields are actual runtime values when available; this run returned no token usage, so input/output/total tokens remain `UNKNOWN`. Character counts are observations and are not token estimates.",
        "",
        "| lane | chapter | calls | executed nodes | skipped nodes | actual tokens | prompt chars | response chars | final source |",
        "|---|---:|---:|---|---|---|---:|---:|---|",
    ]
    for candidate, title in CANDIDATES.items():
        for chapter in range(1, 4):
            record = execution(candidate, chapter)
            nodes = record["nodes"]
            executed = [name for name, item in nodes.items() if item["status"] not in {"skipped", "missing"}]
            skipped = [name for name, item in nodes.items() if item["status"] == "skipped"]
            prompt_chars = sum(as_int(item["prompt_chars"]) for item in nodes.values())
            response_chars = sum(as_int(item["response_chars"]) for item in nodes.values())
            lines.append(
                f"| Hybrid · {title} | {chapter} | {record['model_calls']} | {', '.join(executed)} | {', '.join(skipped) or '无'} | UNKNOWN | {prompt_chars} | {response_chars} | {record.get('final_source') or '—'} |"
            )
        single_dir = SINGLE_ROOT / candidate / "chapters"
        single_chars = sum(len(read(single_dir / f"chapter-{chapter:04d}.md")) for chapter in range(1, 4))
        lines.append(
            f"| Single Control · {title} | 1—3 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | {single_chars}（三章正文合计） | Single Control |"
        )
    lines.extend(
        [
            "",
            "Single Control 的旧实验没有可核验的真实 token/call manifest，因此 token、calls 和 prompt chars 严格写 `UNKNOWN`；没有把字符数换算成 token。",
        ]
    )
    write(ROOT / "efficiency-report.md", "\n".join(lines) + "\n")


def prompt_headings(text: str) -> list[str]:
    headings = []
    for line in text.splitlines():
        if re.match(r"^#{1,2} ", line) and line not in headings:
            headings.append(line)
    return headings


def build_context_audit() -> None:
    lines = [
        "# Chapter 3 context bloat audit",
        "",
        "本表只观察实际保存的 Chapter 3 Prompt，不做优化建议，不用字符数伪装 token。每个 Prompt 的上下文区块来自其真实标题；`Opening Contract` 是否出现按文本直接核对。",
        "",
    ]
    for candidate, title in CANDIDATES.items():
        record = execution(candidate, 3)
        run = ROOT / candidate / "runs" / "chapter-0003"
        names = ["director", "chapter_prep", "curator", "primary", *record["selected_specialists"], "integrator", "state_delta"]
        lines.append(f"## {title} / {candidate}")
        lines.append("")
        lines.append("| node | prompt chars | Opening Contract | key context blocks observed | previous prose | prior node output |")
        lines.append("|---|---:|---|---|---|---|")
        for name in names:
            prompt_name = "chapter_prep_prompt.md" if name == "chapter_prep" else f"{name}_prompt.md"
            path = run / prompt_name
            text = read(path)
            if not text:
                continue
            headings = prompt_headings(text)
            key = [
                heading.removeprefix("# ").removeprefix("## ")
                for heading in headings
                if any(token in heading for token in (
                    "Opening Three Chapter Contract", "AUTHORITY", "BOOK CONTRACT", "CANON PROSE",
                    "CANON INDEX", "PLAN", "Curated", "Primary Draft", "Specialist", "Reader-First",
                ))
            ]
            previous = any(token in text for token in ("CANON PROSE", "前文正文", "上一章", "前文章末"))
            prior = any(token in text for token in ("Curated Chapter Context", "Primary Draft", "Specialist Response", "当前返回"))
            lines.append(
                f"| {name} | {len(text)} | {'yes' if text.count('Opening Three Chapter Contract') else 'no'} | {'; '.join(key) or '—'} | {'yes' if previous else 'no'} | {'yes' if prior else 'no'} |"
            )
        lines.append("")
        lines.append("Prompt headings observed:")
        for name in names:
            prompt_name = "chapter_prep_prompt.md" if name == "chapter_prep" else f"{name}_prompt.md"
            headings = prompt_headings(read(run / prompt_name))
            if headings:
                lines.append(f"- `{name}`: " + " / ".join(headings))
        lines.append("")
    write(ROOT / "context-bloat-audit.md", "\n".join(lines) + "\n")


def join_chapters(directory: Path) -> str:
    return "\n\n---\n\n".join(
        read(directory / f"chapter-{chapter:04d}.md").strip() for chapter in range(1, 4)
    ) + "\n"


def build_blind_materials() -> None:
    blind = ROOT / "blind-reader-materials"
    write(
        blind / "book-a" / "option-a.md",
        join_chapters(ROOT / "candidate-b" / "chapters"),
    )
    write(
        blind / "book-a" / "option-b.md",
        join_chapters(SINGLE_ROOT / "candidate-b" / "chapters"),
    )
    write(
        blind / "book-c" / "option-a.md",
        join_chapters(SINGLE_ROOT / "candidate-c" / "chapters"),
    )
    write(
        blind / "book-c" / "option-b.md",
        join_chapters(ROOT / "candidate-c" / "chapters"),
    )
    write(
        blind / "blind-reader-instructions.md",
        """# Blind reader instructions

你只能读取同目录下 `book-a/option-a.md`、`book-a/option-b.md`、`book-c/option-a.md`、`book-c/option-b.md`。不要读取实验目录、文件名之外的任何 key、Prompt、manifest、模型名或上游资料。

每本只回答以下问题，不打分：

1. 第一章结束时哪版更想立刻点第二章？
2. 哪版核心异能更爽、更清楚，但没有透支？
3. 哪版主角更有具体人格和行为指纹？
4. 哪版 NPC 更像独立的人而不是功能角色？
5. 哪版对话更自然？
6. 哪版动作和空间更自然？
7. 哪版更少出现“动作后马上解释意义”？
8. 哪版更少出现过度工整 / 正确判断过密？
9. 哪版前三章的个人资产和复利更清楚？
10. 哪版第三章后更想继续看长期故事？
11. 哪版整体更接近顶级中文男频商业长篇？

每本最终从 `SINGLE_BETTER`、`HYBRID_BETTER`、`MIXED` 三选一，并引用具体章段现象，不输出数字分数。
""",
    )
    write(
        blind / "blind-key.md",
        """# Blind key (do not provide to blind reader)

- book-a: option-a = Hybrid Selective, option-b = Single Control, 《炉藏万象》
- book-c: option-a = Single Control, option-b = Hybrid Selective, 《掌中天工》
""",
    )


if __name__ == "__main__":
    build_efficiency()
    build_context_audit()
    build_blind_materials()
