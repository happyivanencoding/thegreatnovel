"""确定性地采集修改后（Chapter Runtime Lite v1）chapter Prompt（real-exp-001，第4章）。

与 temps/gen_baseline_prompt.py 使用完全相同的 10 项固定输入（见 temps/baseline_inputs.md），
仅输出文件与脚本名不同；通过 storage 读取真实 BOOK/PROMPTS/章节/EXPERIMENT 数据；
不调用 LLM/网络；不写 BOOK、不写章节；产物只输出到 temps/。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.prompts import generate_prompt
from story_mvp.references import load_validated_references
from story_mvp.storage import read_book_payload, read_chapter

BOOK_ID = "real-exp-001"
WORKSPACE = ROOT / "books"
CHAPTER_NUMBER = 4
LONG_BLOCK_HEADING = "## 第1—15章：贫民区的失效术式"
REFERENCE_IDS = (
    "rcv0-02-foundation-bottleneck",
    "rcv0-02-opening-bottleneck",
    "rcv0-24-public-proof-rescue-loop",
)

# 八字段小纲是 chapter_prep 的 LLM 输出，实验中从未落盘；此常量是固定替代值，
# 由 BOOK 十章小纲“第4章：黑市余波”条目确定性拆解而来。
CURRENT_OUTLINE = """触发事件：林砚带米拉回到黑市，发现钉四已经查到火符来源，却没有立刻交出修复方法。
推动事件的人：铁钉帮的钉四。
主角行动：林砚用三息火留下的痕迹证明自己只能做一次性修复，并要求铁钉帮先让旧炉区恢复供热，换取继续接触废术式的机会。
对手或世界反应：铁钉帮没有立刻抢夺方法，改为观察他的下一次修复。
直接结果：主角保住能力秘密，获得一条可以重复接触失效术式的黑市渠道。
状态变化：铁钉帮从追问方法转为观察他的下一次修复；林砚在第七下层拥有第一条可持续行动渠道。
叙事功能：承接升降井逃生，把第一次战斗兑现转成可持续的低层行动空间。
结尾推动力：钉四拿出一枚停摆的炉芯，说明旧炉区今晚还会有人冻死。"""


def extract_block(section_text: str, heading: str) -> str:
    lines = section_text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index + 1
            break
    if start is None:
        raise SystemExit(f"未找到区块：{heading}")
    collected = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        collected.append(line)
    return "\n".join(collected).strip()


def extract_recent_summaries(status_text: str) -> str:
    lines = status_text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip().startswith("最近章节摘要："):
            start = index
            break
    if start is None:
        raise SystemExit("BOOK 当前状态中未找到最近章节摘要")
    collected = [lines[start].split("最近章节摘要：", 1)[1]]
    for line in lines[start + 1:]:
        if line.strip().startswith("未兑现承诺："):
            break
        collected.append(line)
    text = "\n".join(collected).strip()
    if not text:
        raise SystemExit("最近章节摘要为空")
    return text


def extract_gbrain_stdout(experiment_text: str) -> str:
    lines = experiment_text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == "### GBrain 实际返回":
            start = index + 1
            break
    if start is None:
        raise SystemExit("EXPERIMENT.md 中未找到 GBrain 实际返回")
    collected = []
    in_block = False
    for line in lines[start:]:
        if line.startswith("    "):
            collected.append(line)
            in_block = True
        elif in_block and line.strip() == "":
            collected.append(line)
        elif in_block:
            break
    text = "\n".join(collected).strip()
    if not text:
        raise SystemExit("GBrain 实际返回区块为空")
    return text

def main() -> None:
    payload = read_book_payload(BOOK_ID, WORKSPACE)
    template = payload["prompt_templates"]["chapter"]
    book_content = payload["book_content"]
    current_long_block = extract_block(
        payload["sections"]["long_plan"], LONG_BLOCK_HEADING
    )
    previous_parts = []
    for number in range(max(1, CHAPTER_NUMBER - 2), CHAPTER_NUMBER):
        text = read_chapter(BOOK_ID, number, WORKSPACE)
        if text:
            previous_parts.append(f"# {number}章正文\n\n{text}")
    previous_chapter_text = "\n\n".join(previous_parts)
    recent_summaries = extract_recent_summaries(payload["sections"]["status"])
    experiment_path = ROOT / "books" / BOOK_ID / "EXPERIMENT.md"
    experiment_text = experiment_path.read_text(encoding="utf-8")
    gbrain_inspiration = extract_gbrain_stdout(experiment_text)
    validated = {item["program_id"]: item for item in load_validated_references()}
    selected_references = []
    for ref_id in REFERENCE_IDS:
        if ref_id not in validated:
            raise SystemExit(f"REFERENCE_ROOT 缺少 VALIDATED 参考程序：{ref_id}")
        selected_references.append(validated[ref_id])
    prompt = generate_prompt(
        mode="chapter",
        template=template,
        book_content=book_content,
        current_long_block=current_long_block,
        previous_chapter_text=previous_chapter_text,
        current_outline=CURRENT_OUTLINE,
        recent_summaries=recent_summaries,
        selected_references=selected_references,
        gbrain_inspiration=gbrain_inspiration,
    )
    out_dir = ROOT / "temps"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "after_chapter_prompt.md"
    target.write_text(prompt, encoding="utf-8")
    print(f"after prompt chars: {len(prompt)}")
    print(f"saved: {target}")


if __name__ == "__main__":
    main()
