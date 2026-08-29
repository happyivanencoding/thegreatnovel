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
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "reviser-trust-reader-sweep"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (1, 3, 4, 5, 6, 10, 11, 12, 16, 17, 18)

MODULE = """## Trust Reader Final Sweep｜只删纯盖章，不磨人物

完成全部 Authority / Mission / Value-Preserving 修订后，做一次极窄的 Result Stop 检查。只有当一句旁白**完全没有新增事实或人物价值**，且它的同一意义已经被紧邻的动作、对白、物体变化或具体位置充分证明时，才允许直接删除该句或把同义结果句合并；不为此改写周围正文。

典型可删对象是“这句话/那些事/三件事/某人说得没错”等作者替读者再次盖章的纯总结，或一句抽象结果后紧跟同义具体结果。删除后 Mission、Canon、关系、情绪、压力、Payoff 与 Ending 必须逐字义等价。

下列内容即使看起来像说明，也一律保护，不删除、不合并、不改写：
- 人物直接的怕、不怕、想、不想、要、喜欢、舍不得、拒绝、决定、偏心、嫉妒、野心、占有欲与其它私人牵引；
- 人物说话姿态、语气、是否求人、克制、嘴硬、犹豫等关系信号；
- 群体等待、围观、沉默、震惊、压力与社会重新定价；
- 主角独特价值判断、行为签名、幽默、刻薄或世界观措辞；
- 独立停顿句，只要它承担欲望、关系、力量、爽点、情绪或节奏重音。

无法确定是否为纯重复时保持原文。这个 Sweep 只删除，不新增事实，不成为新的重写理由。"""


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


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    marker = "## 冻结边界"
    if prompt.count(marker) != 1:
        raise RuntimeError(f"ch{chapter}: marker count={prompt.count(marker)}")
    prompt = prompt.replace(marker, MODULE + "\n\n" + marker, 1)
    prompt_path = directory / "reviser_prompt.md"
    output_path = directory / "reviser_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    final_body = body(response)
    (directory / "reviser_response.md").write_text(response + "\n", encoding="utf-8")
    (directory / "final_body.md").write_text(final_body + "\n", encoding="utf-8")
    control = json.loads((source / "authority_reviser_acp.json").read_text(encoding="utf-8"))
    return {
        "chapter": chapter,
        "control_wall_seconds": float(control.get("wall_seconds") or 0),
        "treatment_wall_seconds": float(data.get("wall_seconds") or 0),
        "latency_change_percent": round((float(data.get("wall_seconds") or 0) / float(control.get("wall_seconds") or 1) - 1) * 100, 2),
        "control_chars": len((BOOK / "chapters" / f"chapter-{chapter:04d}.md").read_text(encoding="utf-8").strip()),
        "treatment_chars": len(final_body),
        "usage": data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
