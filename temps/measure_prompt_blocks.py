"""测量两份 chapter Prompt 的区块级字符占比，为对比报告提供确定性数据。

只读 temps/baseline_chapter_prompt.md 与 temps/after_chapter_prompt.md；不写其它文件。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def section_lengths(text: str, level: str) -> list[tuple[str, int]]:
    """按 Markdown 标题切分，返回 (标题, 含标题的区块字符数)。"""
    lines = text.splitlines(keepends=True)
    blocks: list[tuple[str, list[str]]] = []
    current: tuple[str, list[str]] | None = None
    for line in lines:
        if line.startswith(level + " ") and not line.startswith(level + "#"):
            if current:
                blocks.append(current)
            current = (line.strip(), [line])
        else:
            if current is None:
                current = ("(前置文本)", [line])
            current[1].append(line)
    if current:
        blocks.append(current)
    return [(title, len("".join(body))) for title, body in blocks]


def main() -> None:
    baseline = (ROOT / "temps" / "baseline_chapter_prompt.md").read_text(encoding="utf-8")
    after = (ROOT / "temps" / "after_chapter_prompt.md").read_text(encoding="utf-8")
    print(f"baseline len={len(baseline)}  after len={len(after)}  diff={len(baseline) - len(after)}")
    print("\n== baseline 二级区块 ==")
    for title, size in section_lengths(baseline, "##"):
        print(f"{size:>6}  {size / len(baseline) * 100:5.1f}%  {title}")
    print("\n== after 二级区块 ==")
    for title, size in section_lengths(after, "##"):
        print(f"{size:>6}  {size / len(after) * 100:5.1f}%  {title}")


if __name__ == "__main__":
    main()
