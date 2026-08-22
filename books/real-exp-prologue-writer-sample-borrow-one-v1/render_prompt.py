"""用生产 prologue Prompt Mode 渲染《借我一招》的一次性样本。"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "books" / "real-exp-opening-reader-first-fresh-v1"
OUT = ROOT / "books" / "real-exp-prologue-writer-sample-borrow-one-v1"
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.prompts import generate_prompt  # noqa: E402


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(text: str, heading: str, level: int = 1) -> str:
    marker = "#" * level
    match = re.search(
        rf"(?ms)^{re.escape(marker)}\s+{re.escape(heading)}\s*$\n(.*?)(?=^{re.escape(marker)}\s+|\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


book = read(SOURCE / "BOOK.md")
plans = read(SOURCE / "CHAPTER_PLANS.md")
chapter_one_plan = re.search(r"(?ms)^## 第1章：.*?\n(.*?)(?=^## 第2章：|\Z)", plans)
intent = """本次是《借我一招》的可选 Prologue 小样本，不是 Chapter 1。

请让一个普通、具体、熟悉日常训练或山间生活的人，现场看见一次远超普通人的武力事件；先写他熟悉的对象、异常动作、尝试理解或处理、普通办法为什么无效，再让读者在产生疑问后得到一小段直接解释，最后落到顾长川为什么想变强的可见向往。不要写顾长川的考核、借招能力或第一章事件，不要写完整宗门体系，不要创建新术语，结尾停在“有人想达到这种力量”这一清楚事实。"""

prompt = generate_prompt(
    mode="prologue",
    template="",
    book_content=book,
    current_long_block=section(book, "当前中期规划窗口"),
    current_chapter_plan=chapter_one_plan.group(0).strip() if chapter_one_plan else "",
    creative_direction=intent,
)
(OUT / "prompt.md").write_text(prompt, encoding="utf-8")
