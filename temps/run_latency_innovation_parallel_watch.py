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
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "parallel-authority-watch"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

PLANNER_TEMPLATE = """你是 TGN 的 Pre-Draft Authority Watch Planner，使用 GPT-5.6 Luna high。你在 Primary Writer 开始写正文的同时独立运行，因此看不到 Primary Draft，也不得猜它会怎么写。

你的任务不是写正文、不是重新规划，而是把本章最容易在正文中被遗漏、弱化、越界或错误实现的少量高价值语义编译成一份可执行 Watchlist，供随后快速 Finalizer 使用。

原则：
- Frozen Mission 决定本章事件、行动者、对象、结果、状态变化与 Ending；不能降成准备/资格/以后再做。
- Canon/World/Power/Human 的未知边界不能被合理猜测补成事实。
- Reader Release、精确力量尺、Public Proof、私人欲望、具体奖励/持有关系只在 Authority 明确支持时进入。
- 同时保护男频价值：主角主动性、核心幻想、具体占有/收益、人物欲望、关系变化、群体震动/懂行校准/行为重估、章末真实动作。
- Supporting implementation、登记/报告/路线/协调/重复证明只保留支撑因果所需的最少量。
- 每条只能来自下方 Authority；不新增数字、制度、支付方式、能力规则、旧史或人物到场。

严格输出以下六个区块，总长尽量控制在 1200—2200 中文字符：
# MUST LAND
用 M1/M2… 列出必须在最终正文真实发生的行动、直接结果、状态变化和 Ending。尽量保留原文中的行动者、对象和完成时态。
# MUST NOT INVENT
用 N1/N2… 列出仍未知、未批准、不能扩写的事实边界。
# REALIZATION PRIORITIES
用 R1/R2… 列出本章若触发时必须让读者感到的 World/Power/Human/Payoff/Public Proof 体验；没有则写 NONE。
# GLOBAL CLOSURE WATCH
用 G1/G2… 列出需要全文一致的持有人、时间窗口、数字/档位、人物/势力名、能力条件与资源状态；没有则写 NONE。
# PRESERVE VALUE
用 P1/P2… 列出即使修事实也不能顺手磨掉的人物、关系、爽点、欲望或惊喜价值；没有则写 NONE。
# COMPRESS ONLY IF PRESENT
用 C1/C2… 列出若 Draft 真的出现才压缩的低价值流程/重复证明；不得要求正文凭空加入这些内容。

不要输出 Audit、评分、正文、修改建议句子或思考过程。"""

FINALIZER_TEMPLATE = """你是 TGN 的 Fast Authority Finalizer，使用 GPT-5.6 Terra high。Primary Draft 是唯一正文底稿；Pre-Draft Watchlist 由独立 Luna-high Authority Planner 在看不到 Draft 的情况下编译。

你不是第二个 Director，也不是自由重写者。先逐条检查 Watchlist 与 Frozen Mission：
- Draft 已经正确的句段尽量逐字保留；
- 只修明确遗漏、冲突、时态/行动者/对象/持有关系错误、未授权事实、Reader Release/力量/人物 realization 漏失，以及真实存在的流程膨胀；
- MUST LAND 必须在最终正文中真实完成，不得降成准备、依据、资格、以后结算或“即将”；
- GLOBAL CLOSURE 涉及的事实要全文一致，不能只改第一处；
- 修事实时保护 PRESERVE VALUE；不能把主角主动性、人物欲望、关系、Payoff、群体震动、懂行校准、行为重估或章末真实动作一起删掉；
- Watchlist 没授权的新数字、制度、价格、支付方式、能力规则、旧史或未来剧情不得补造；
- COMPRESS ONLY IF PRESENT 只有 Draft 真的出现对应低价值内容时才处理。

固定输出：
# 正式正文
<完整最终正文>

不要输出说明、Audit、评分、Patch、事实摘要或思考过程。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    text = clean(text)
    return text.rsplit("# 正式正文", 1)[-1].strip()


def call(prompt_path: Path, output_path: Path, model: str, effort: str) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), model, effort, str(ROOT)],
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


def h2_block(text: str, heading_prefix: str, *, end_prefix: str | None = None) -> str:
    starts = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(starts):
        heading = match.group(1).strip()
        if not heading.startswith(heading_prefix):
            continue
        if end_prefix:
            for later in starts[index + 1:]:
                if later.group(1).strip().startswith(end_prefix):
                    return text[match.end():later.start()].strip()
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        return text[match.end():end].strip()
    return ""


def planner_context(authority_prompt: str) -> str:
    blocks = []
    headings = (
        "AUTHORITY——",
        "FROZEN CHAPTER MISSION",
        "CURATOR｜",
        "WORLD REALITY AUTHORITY",
        "READER RELEASE",
        "POWER CORE",
        "HUMAN CORE",
        "CANON INDEX",
        "CANON TAIL",
        "ACTIVE SCENE REVISION WATCH",
    )
    for heading in headings:
        value = h2_block(authority_prompt, heading)
        if value:
            blocks.append(f"## {heading}\n\n{value}")
    return "\n\n".join(blocks)


def finalizer_context(authority_prompt: str, watchlist: str, primary: str) -> str:
    blocks = []
    for heading in (
        "AUTHORITY——",
        "FROZEN CHAPTER MISSION",
        "READER RELEASE",
        "CANON TAIL",
    ):
        value = h2_block(authority_prompt, heading)
        if value:
            blocks.append(f"## {heading}\n\n{value}")
    blocks.extend((f"# PRE-DRAFT AUTHORITY WATCHLIST\n\n{watchlist}", f"# PRIMARY DRAFT\n\n{primary}"))
    return "\n\n".join(blocks)


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    authority_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    primary = body((source / "primary_response.md").read_text(encoding="utf-8"))

    planner_prompt = PLANNER_TEMPLATE + "\n\n# AUTHORITY INPUT\n\n" + planner_context(authority_prompt)
    planner_prompt_path = directory / "watch_planner_prompt.md"
    planner_output_path = directory / "watch_planner_acp.json"
    planner_prompt_path.write_text(planner_prompt, encoding="utf-8")
    planner_data = call(planner_prompt_path, planner_output_path, "gpt-5.6-luna", "high")
    watchlist = clean(planner_data.get("text", ""))
    (directory / "watchlist.md").write_text(watchlist + "\n", encoding="utf-8")

    finalizer_prompt = FINALIZER_TEMPLATE + "\n\n" + finalizer_context(authority_prompt, watchlist, primary)
    finalizer_prompt_path = directory / "terra_finalizer_prompt.md"
    finalizer_output_path = directory / "terra_finalizer_acp.json"
    finalizer_prompt_path.write_text(finalizer_prompt, encoding="utf-8")
    finalizer_data = call(finalizer_prompt_path, finalizer_output_path, "gpt-5.6-terra", "high")
    finalizer_text = clean(finalizer_data.get("text", ""))
    final_body = body(finalizer_text)
    (directory / "terra_finalizer_response.md").write_text(finalizer_text + "\n", encoding="utf-8")
    (directory / "final_body.md").write_text(final_body + "\n", encoding="utf-8")

    primary_data = json.loads((source / "primary_acp.json").read_text(encoding="utf-8"))
    control_reviser_data = json.loads((source / "authority_reviser_acp.json").read_text(encoding="utf-8"))
    primary_wall = float(primary_data.get("wall_seconds") or 0)
    planner_wall = float(planner_data.get("wall_seconds") or 0)
    finalizer_wall = float(finalizer_data.get("wall_seconds") or 0)
    control_wall = primary_wall + float(control_reviser_data.get("wall_seconds") or 0)
    treatment_critical = max(primary_wall, planner_wall) + finalizer_wall
    return {
        "chapter": chapter,
        "primary_wall_seconds": primary_wall,
        "control_reviser_wall_seconds": float(control_reviser_data.get("wall_seconds") or 0),
        "planner_wall_seconds": planner_wall,
        "finalizer_wall_seconds": finalizer_wall,
        "control_primary_plus_reviser_seconds": round(control_wall, 3),
        "treatment_parallel_critical_seconds": round(treatment_critical, 3),
        "critical_path_speedup_percent": round((1 - treatment_critical / control_wall) * 100, 2),
        "planner_prompt_chars": len(planner_prompt),
        "watchlist_chars": len(watchlist),
        "finalizer_prompt_chars": len(finalizer_prompt),
        "final_chars": len(final_body),
        "planner_usage": planner_data.get("result", {}).get("usage", {}),
        "finalizer_usage": finalizer_data.get("result", {}).get("usage", {}),
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
