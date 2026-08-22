"""用当前生产 prologue mode 渲染《借我一招》Prologue 重写 prompt。"""

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
old = read(OUT / "PROLOGUE_v1.md")
chapter_one_plan = re.search(r"(?ms)^## 第1章：.*?\n(.*?)(?=^## 第2章：|\Z)", plans)
intent = f"""本次重写《借我一招》的既有 Prologue，不是 Chapter 1，也不是重新设计故事。

请保留既有事件事实：青崖宗后山水渠出现异常；顾长川和附近普通人先用扁担、绳子、木桩等普通办法处理但失败；上游瀑布出现异常；远处强者一剑分开山瀑并改变水流；水渠、青苗、灶房等生活对象受到具体损失；顾长川因此明确想拥有那种力量。

重写目标：让事件更早发生，减少开头解释；让每个动作、失败、人物反应和后果直接可见；把最低限度的“修炼者能把力量送到身外”放在人物已经产生疑问之后；减少抽象总结、连续排除式句法和替代事实的比喻。可以让一个普通现场见证者承担更多观察，但不要建立完整配角卡。不要新增宗门历史、境界体系、术语、Chapter 1 考核、顾长川借招能力或后期敌人。

现有草稿只作为事实参考，不能逐句改写或保留原有句法：

{old}"""

prompt = generate_prompt(
    mode="prologue",
    template="",
    book_content=book,
    current_long_block=section(book, "当前中期规划窗口"),
    current_chapter_plan=chapter_one_plan.group(0).strip() if chapter_one_plan else "",
    creative_direction=intent,
)
(OUT / "rewrite_prompt.md").write_text(prompt, encoding="utf-8")
