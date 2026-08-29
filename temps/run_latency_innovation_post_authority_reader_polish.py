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
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "post-authority-reader-polish"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

PROMPT = """你是 TGN 的 Post-Authority Reader Polish Patch Agent，使用 Terra medium。输入正文已经完成完整 Authority Revision；事实、事件、力量、持有关系、结果与 Ending 均冻结。

你只寻找最多 3 个**纯表达层、局部、可证明不改变 State**的高价值修复：
- 删除一句已经由动作/对白证明的后台总结、报告腔、身份入口/行动空间式抽象解释；
- 压缩同一结果的重复证明或无新选择的流程句；
- 在不新增信息的前提下，把一句角色不自然的系统说明改成同一个角色会说的普通话；
- 调整一个局部句段，让已有的主角欲望、人物反应、核心幻想或 Payoff 更直接，但只能使用 OLD 本身已经包含的事实和动作。

绝对禁止：新增或删除事件、动作结果、人物、物件、数字、价格、地点、制度、能力、境界、伤势、持有人、时间、承诺、关系变化、奖励、信息、因果或章末推动；不得改变代词、人物称谓、专名、否定/肯定、完成/未完成、已经/尚未、能/不能、必须/可以等事实强度；不得把暗示变成确定事实；不得重写战斗或整段场景。

宁可 `NO_CHANGE`，不要为了有产出而润色。不要做同义改写，不追求“更文学”。每个 Patch 的 OLD 必须是正文中唯一出现的连续原文，NEW 只改同一个局部，通常不超过 OLD 字数的 110%。

严格只输出：
NO_CHANGE

或：
# PATCH SET
## PATCH 1
OLD:
<唯一连续原文>
NEW:
<替换文本>
REASON:
<一句说明 Reader 价值；不得声称改事实>

最多 3 个 Patch。不要输出完整正文、Audit、评分或思考过程。"""

PATCH_PATTERN = re.compile(
    r"(?ms)^## PATCH\s+\d+\s*$\nOLD:\s*\n(?P<old>.*?)\nNEW:\s*\n(?P<new>.*?)\nREASON:\s*\n(?P<reason>.*?)(?=^## PATCH\s+\d+\s*$|\Z)"
)
FACT_STRENGTH = (
    "已经", "尚未", "仍未", "不能", "不得", "必须", "只能", "可以", "不再",
    "归", "持有", "交给", "收下", "到账", "突破", "成炉", "照域", "镇海",
    "死", "伤", "离开", "进入", "出发", "完成", "失败", "赢", "输",
)


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def call(prompt_path: Path, output_path: Path) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-terra", "medium", str(ROOT)],
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


def fact_tokens(text: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    numbers = tuple(sorted(re.findall(r"\d+(?:\.\d+)?", text)))
    strengths = tuple(term for term in FACT_STRENGTH if term in text)
    return numbers, strengths


def apply_patch(response: str, original: str) -> tuple[str, list[dict], str]:
    text = clean(response)
    if text == "NO_CHANGE":
        return original, [], "no_change"
    if not text.startswith("# PATCH SET"):
        raise ValueError("invalid output contract")
    result = original
    patches = []
    for match in PATCH_PATTERN.finditer(text):
        old = match.group("old").strip()
        new = match.group("new").strip()
        reason = match.group("reason").strip()
        if not old or result.count(old) != 1:
            raise ValueError(f"OLD occurrence count={result.count(old)}")
        if "..." in old or "……" in old:
            raise ValueError("ellipsis anchor")
        if len(new) > len(old) * 1.10 + 20:
            raise ValueError("patch expands too much")
        if fact_tokens(old) != fact_tokens(new):
            raise ValueError("numeric or fact-strength tokens changed")
        if old.count("\n\n") > 1 or new.count("\n\n") > 1:
            raise ValueError("patch spans too many paragraphs")
        result = result.replace(old, new, 1)
        patches.append({"old": old, "new": new, "reason": reason})
    if not patches or len(patches) > 3:
        raise ValueError(f"patch count={len(patches)}")
    return result.strip(), patches, "patched"


def one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    original = (BOOK / "chapters" / f"chapter-{chapter:04d}.md").read_text(encoding="utf-8").strip()
    prompt = PROMPT + "\n\n# FINAL AUTHORITY-CLEAN BODY\n\n" + original
    prompt_path = directory / "polish_prompt.md"
    output_path = directory / "polish_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    (directory / "polish_response.md").write_text(response + "\n", encoding="utf-8")
    fallback = False
    error = ""
    try:
        final, patches, mode = apply_patch(response, original)
    except Exception as exc:
        fallback = True
        error = str(exc)
        final, patches, mode = original, [], "invalid_fallback"
    (directory / "final_body.md").write_text(final + "\n", encoding="utf-8")
    state_data = json.loads((SOURCE / f"chapter-{chapter:04d}" / "state_acp.json").read_text(encoding="utf-8"))
    polish_wall = float(data.get("wall_seconds") or 0)
    state_wall = float(state_data.get("wall_seconds") or 0)
    return {
        "chapter": chapter,
        "state_wall_seconds": state_wall,
        "polish_wall_seconds": polish_wall,
        "parallel_critical_seconds": round(max(state_wall, polish_wall), 3),
        "added_wall_over_state_seconds": round(max(0.0, polish_wall - state_wall), 3),
        "hidden_by_state": polish_wall <= state_wall,
        "mode": mode,
        "fallback": fallback,
        "error": error,
        "patch_count": len(patches),
        "patches": patches,
        "original_chars": len(original),
        "final_chars": len(final),
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
