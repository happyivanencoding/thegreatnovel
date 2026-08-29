from __future__ import annotations

import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
SOURCE = BOOK / "runs"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "combined-reviser-state"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

OLD_OUTPUT = """固定输出只允许：
# 正式正文
<完整修订后的章节正文>
不要输出 Audit、修改说明、评分、差异列表、事实摘要或思考过程。"""

COMBINED_OUTPUT = """固定输出只允许以下五个一级标题，顺序不能改变：

# 正式正文
<完整修订后的章节正文>

# Proposed Active Scene State
根据你刚刚输出的最终正文，记录下一章立即需要的完整状态：地点、在场人物、即时伤势、手中关键物品、当前敌人或追兵、当前倒计时、下一步直接目标；主角已有明确主动目标时写“当前主动目标：……”。只写会影响下一章行动的内容。

# Proposed Persistent Canon
根据最终正文更新简短长期 Canon。保留仍有效的已证明能力/边界、关系阶段、身份/准入、确认知识、重要世界状态与持久资产；只在本章正文明确改变时更新。需要时使用：
### Power / Capability
### Active Relationships
### Identity / Access
### Knowledge / Enemy State
### World State
### Tracked Assets
不得从胜负、评价或高阶战绩反推力量等级变化；不得生成 Human Development；物品持有人、位置与转移必须服从最终正文。

# Proposed Chapter Summary
只写80—160字事实摘要，只写最终正文已经发生的事。

# Proposed Open Promises
最多12条，每条一行。合并重复；删除已兑现、失败、失效或只剩普通悬念的项目；新增必须由最终正文真实建立。近期影响选择/行动的优先，再保留少量真正长期承诺。

State 区块只是对你自己刚生成的最终正文做书记员式提取，不得反过来修改、补造或解释正文。旧 Canon 只提供此前状态；最终正文是本章唯一新事实来源。不得输出 AUTHOR NOTES、Audit、修改说明、评分、差异列表、JSON/YAML或思考过程。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def split_output(text: str) -> tuple[str, str]:
    clean_text = clean(text)
    marker = "# Proposed Active Scene State"
    if marker not in clean_text:
        raise ValueError("combined output missing Proposed Active Scene State")
    body_part, state_tail = clean_text.split(marker, 1)
    body = body_part.rsplit("# 正式正文", 1)[-1].strip()
    state = marker + state_tail
    for heading in (
        "# Proposed Persistent Canon",
        "# Proposed Chapter Summary",
        "# Proposed Open Promises",
    ):
        if heading not in state:
            raise ValueError(f"combined output missing {heading}")
    if len(body) < 1500:
        raise ValueError(f"combined body too short: {len(body)}")
    return body, state.strip()


def call(prompt_path: Path, output_path: Path) -> dict:
    last = ""
    for attempt in range(3):
        try:
            process = subprocess.run(
                ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-luna", "high", str(ROOT)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=1200,
            )
        except subprocess.TimeoutExpired:
            last = f"timeout after 1200s: {prompt_path}"
            time.sleep(2 + attempt * 2)
            continue
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


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    if prompt.count(OLD_OUTPUT) != 1:
        raise RuntimeError(f"ch{chapter}: output contract count={prompt.count(OLD_OUTPUT)}")
    prompt = prompt.replace(OLD_OUTPUT, COMBINED_OUTPUT, 1)
    prompt_path = directory / "combined_reviser_state_prompt.md"
    output_path = directory / "combined_reviser_state_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    body, state = split_output(response)
    (directory / "combined_response.md").write_text(response + "\n", encoding="utf-8")
    (directory / "final_body.md").write_text(body + "\n", encoding="utf-8")
    (directory / "state_delta.md").write_text(state + "\n", encoding="utf-8")

    reviser_data = json.loads((source / "authority_reviser_acp.json").read_text(encoding="utf-8"))
    state_data = json.loads((source / "state_acp.json").read_text(encoding="utf-8"))
    control = float(reviser_data.get("wall_seconds") or 0) + float(state_data.get("wall_seconds") or 0)
    treatment = float(data.get("wall_seconds") or 0)
    return {
        "chapter": chapter,
        "control_reviser_seconds": float(reviser_data.get("wall_seconds") or 0),
        "control_state_seconds": float(state_data.get("wall_seconds") or 0),
        "control_serial_seconds": round(control, 3),
        "combined_seconds": treatment,
        "speedup_percent": round((1 - treatment / control) * 100, 2),
        "body_chars": len(body),
        "state_chars": len(state),
        "usage": data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
