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
WATCH = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "parallel-authority-watch"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "parallel-watch-luna-finalizer"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

FINALIZER_TEMPLATE = """你是 TGN 的 Compact Luna Authority Finalizer，使用 GPT-5.6 Luna high。Primary Draft 是唯一正文底稿；PRE-DRAFT WATCHLIST 由另一个 Luna-high Agent 在看不到 Draft 时从同一冻结 Authority 编译。

你不是第二个 Director，也不是自由重写者。你的唯一任务是用最小跨度把 Draft 修到可直接保存：
- 先逐条核对 Frozen Mission 与 Watchlist；MUST LAND 的行动者、对象、直接结果、状态变化与 Ending 必须真实完成，不能降成准备、资格、依据、以后结算或“即将”。
- Canon / World / Power / Human / Reader Release 决定事实边界；未授权的数字、制度、支付方式、外观、旧史、力量机制、人物到场或未来结果必须删除或降回未知。
- GLOBAL CLOSURE 涉及的持有人、时间窗口、数字/档位、人物/势力名、能力条件和资源状态必须全文一致，不能只修第一处。
- Preservation First：Draft 已经正确的句段尽量逐字保留；只改明确失败处。修事实时不得顺手磨掉主角主动性、人物欲望、关系、核心幻想、奖励占有、Public Proof、社会重新定价、惊喜或章末真实动作。
- 只有 Draft 真实出现无新选择的登记、报告、路线、协调、重复证明或后台抽象时才压缩；不要把正常场景、谈判、人物反应或 payoff 误删成摘要。
- 如果 Watchlist 与 Frozen Authority 冲突，以 Frozen Authority 为准；Watchlist 不能创造新事实。

固定输出：
# 正式正文
<完整最终正文>

不要输出 Audit、说明、Patch、评分、事实摘要或思考过程。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


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


def h2_block(text: str, heading_prefix: str) -> str:
    starts = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(starts):
        if not match.group(1).strip().startswith(heading_prefix):
            continue
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        return text[match.end():end].strip()
    return ""


def compact_context(authority_prompt: str, watchlist: str, primary: str) -> str:
    blocks = []
    for label, heading in (
        ("AUTHORITY", "AUTHORITY——"),
        ("FROZEN MISSION", "FROZEN CHAPTER MISSION"),
        ("CURATOR ATTENTION", "CURATOR｜"),
        ("WORLD AUTHORITY", "WORLD REALITY AUTHORITY"),
        ("READER RELEASE", "READER RELEASE"),
        ("POWER CORE", "POWER CORE"),
        ("HUMAN CORE", "HUMAN CORE"),
        ("CANON INDEX", "CANON INDEX"),
        ("CANON TAIL", "CANON TAIL"),
        ("ACTIVE REVISION WATCH", "ACTIVE SCENE REVISION WATCH"),
    ):
        value = h2_block(authority_prompt, heading)
        if value:
            blocks.append(f"## {label}\n\n{value}")
    blocks.extend((f"# PRE-DRAFT WATCHLIST\n\n{watchlist}", f"# PRIMARY DRAFT\n\n{primary}"))
    return "\n\n".join(blocks)


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    authority_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    primary = body((source / "primary_response.md").read_text(encoding="utf-8"))
    watchlist = (WATCH / f"chapter-{chapter:04d}" / "watchlist.md").read_text(encoding="utf-8").strip()
    prompt = FINALIZER_TEMPLATE + "\n\n" + compact_context(authority_prompt, watchlist, primary)
    prompt_path = directory / "luna_finalizer_prompt.md"
    output_path = directory / "luna_finalizer_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    final_body = body(response)
    (directory / "luna_finalizer_response.md").write_text(response + "\n", encoding="utf-8")
    (directory / "final_body.md").write_text(final_body + "\n", encoding="utf-8")

    primary_data = json.loads((source / "primary_acp.json").read_text(encoding="utf-8"))
    control_reviser = json.loads((source / "authority_reviser_acp.json").read_text(encoding="utf-8"))
    planner_data = json.loads((WATCH / f"chapter-{chapter:04d}" / "watch_planner_acp.json").read_text(encoding="utf-8"))
    primary_wall = float(primary_data.get("wall_seconds") or 0)
    planner_wall = float(planner_data.get("wall_seconds") or 0)
    finalizer_wall = float(data.get("wall_seconds") or 0)
    control_wall = primary_wall + float(control_reviser.get("wall_seconds") or 0)
    treatment_critical = max(primary_wall, planner_wall) + finalizer_wall
    return {
        "chapter": chapter,
        "primary_wall_seconds": primary_wall,
        "planner_wall_seconds": planner_wall,
        "luna_finalizer_wall_seconds": finalizer_wall,
        "control_primary_plus_reviser_seconds": round(control_wall, 3),
        "treatment_parallel_critical_seconds": round(treatment_critical, 3),
        "critical_path_speedup_percent": round((1 - treatment_critical / control_wall) * 100, 2),
        "full_reviser_prompt_chars": len(authority_prompt),
        "compact_finalizer_prompt_chars": len(prompt),
        "prompt_reduction_percent": round((1 - len(prompt) / len(authority_prompt)) * 100, 2),
        "watchlist_chars": len(watchlist),
        "final_chars": len(final_body),
        "usage": data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
