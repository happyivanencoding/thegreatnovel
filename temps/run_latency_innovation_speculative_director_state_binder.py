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
SPEC = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "speculative-next-director"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "speculative-director-state-binder"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
TRANSITIONS = ((2, 3), (3, 4), (5, 6), (12, 13), (14, 15), (18, 19))

TEMPLATE = """你是 TGN 的 State → Director Binder，使用 Luna low。SPECULATIVE DIRECTOR CONTRACT 已在上一章 State Delta 并行期间生成；FINAL CURRENT STATE 是 State 完成后的最终权威。

你不是新的 Director，不重做创意，不把合同写得更丰富。只做一次**最小差异绑定**：
1. 若 Speculative Contract 与 FINAL CURRENT STATE 在地点、在场人物、伤势、物品持有、力量位置、已完成动作、已知/未知、关系、收益/损失、倒计时或未完成即时目标上冲突，修正对应字段；
2. 若 Speculative 重演上一章已完成事件，删掉重演并从新状态产生的下一个动作开始；
3. FINAL CURRENT STATE 没有改变的地方，尽量逐字保留 Speculative Contract 的人物主动性、具体欲望、冲突、结果和 Ending；
4. 不新增事实、数字、机制、奖励、人物、地点或剧情；不把 Future Plan 写成 Canon；不把未完成结果改成已完成；
5. 当前章执行边界与必须结果仍是唯一事件预算，章末 Handoff 不得提前执行下一章。

严格只输出八字段：
触发事件：
推动事件的人：
主角行动：
对手或世界反应：
直接结果：
状态变化：
叙事功能：
结尾推动力：

全部具体填写。不要输出 Audit、说明、评分、正文或思考过程。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def call(prompt_path: Path, output_path: Path) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-luna", "low", str(ROOT)],
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


def h2_block(text: str, prefix: str) -> str:
    starts = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(starts):
        if not match.group(1).strip().startswith(prefix):
            continue
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        return text[match.end():end].strip()
    return ""


def final_inputs(chapter: int) -> str:
    prompt = (SOURCE / f"chapter-{chapter:04d}" / "director_prompt.md").read_text(encoding="utf-8")
    blocks = []
    for label, prefix in (
        ("CURRENT CHAPTER EXECUTION BOUNDARY", "当前章执行边界"),
        ("CURRENT LONG BLOCK", "当前大型剧情块"),
        ("NAMED OPPORTUNITY", "当前具名机会权威"),
        ("FINAL CANON INDEX", "当前 Canon Index"),
        ("FINAL RECENT SUMMARIES", "最近 1—3 章摘要"),
        ("FINAL PREVIOUS TAIL", "前文章末必要衔接"),
        ("AUTHOR INTENT", "作者当前章意图"),
    ):
        value = h2_block(prompt, prefix)
        if value:
            blocks.append(f"## {label}\n\n{value}")
    return "\n\n".join(blocks)


def one(previous: int, chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    speculative = (SPEC / f"chapter-{chapter:04d}" / "speculative_director_response.md").read_text(encoding="utf-8").strip()
    prompt = TEMPLATE + "\n\n# FINAL INPUT\n\n" + final_inputs(chapter) + "\n\n# SPECULATIVE DIRECTOR CONTRACT\n\n" + speculative
    prompt_path = directory / "binder_prompt.md"
    output_path = directory / "binder_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    (directory / "bound_director_response.md").write_text(response + "\n", encoding="utf-8")

    state_data = json.loads((SOURCE / f"chapter-{previous:04d}" / "state_acp.json").read_text(encoding="utf-8"))
    control_data = json.loads((SOURCE / f"chapter-{chapter:04d}" / "director_acp.json").read_text(encoding="utf-8"))
    spec_data = json.loads((SPEC / f"chapter-{chapter:04d}" / "speculative_director_acp.json").read_text(encoding="utf-8"))
    state_wall = float(state_data.get("wall_seconds") or 0)
    control_wall = float(control_data.get("wall_seconds") or 0)
    speculative_wall = float(spec_data.get("wall_seconds") or 0)
    binder_wall = float(data.get("wall_seconds") or 0)
    serial = state_wall + control_wall
    treatment = max(state_wall, speculative_wall) + binder_wall
    fields = re.findall(r"(?m)^(触发事件|推动事件的人|主角行动|对手或世界反应|直接结果|状态变化|叙事功能|结尾推动力)：", response)
    return {
        "previous_chapter": previous,
        "chapter": chapter,
        "state_wall_seconds": state_wall,
        "control_director_wall_seconds": control_wall,
        "speculative_director_wall_seconds": speculative_wall,
        "binder_wall_seconds": binder_wall,
        "control_state_plus_director_seconds": round(serial, 3),
        "treatment_parallel_plus_binder_seconds": round(treatment, 3),
        "critical_path_speedup_percent": round((1 - treatment / serial) * 100, 2),
        "response_chars": len(response),
        "fields": fields,
        "usage": data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=len(TRANSITIONS)) as executor:
        futures = [executor.submit(one, previous, chapter) for previous, chapter in TRANSITIONS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
