"""把已经冻结的 raw responses 派生为实验正文 artifact；不重写、不调用模型。"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8").strip()


def write(name: str, text: str) -> None:
    (ROOT / name).write_text(text.strip() + "\n", encoding="utf-8")


def main() -> None:
    if (ROOT / "prologue_response.md").is_file():
        write("PROLOGUE.md", read("prologue_response.md"))

    primary_path = ROOT / "chapter-0001_primary_response.md"
    if not primary_path.is_file():
        return
    primary = read(primary_path.name)
    formal = re.search(r"(?ms)^#\s+正式正文\s*$\n(.*?)(?=^#\s+章节事实摘要\s*$|\Z)", primary)
    facts = re.search(r"(?ms)^#\s+章节事实摘要\s*$\n(.*)\Z", primary)
    if not formal or not formal.group(1).strip():
        raise SystemExit("Primary response 缺少非空 # 正式正文 区块；保留 raw，不派生 chapter-0001.md")
    if not facts or not facts.group(1).strip():
        raise SystemExit("Primary response 缺少非空 # 章节事实摘要 区块；保留 raw，不派生正文")
    write("chapter-0001.md", formal.group(1))
    write("chapter-0001_fact_summary.md", facts.group(1))


if __name__ == "__main__":
    main()
