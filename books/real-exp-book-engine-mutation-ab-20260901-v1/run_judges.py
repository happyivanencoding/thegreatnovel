from __future__ import annotations

import concurrent.futures
import json
import subprocess
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
GBRAIN = Path(r"C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库")
OUT = ROOT / r"books\real-exp-book-engine-mutation-ab-20260901-v1"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CASES = ("ning_21_30", "wen_singleworld")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_md(case: str) -> None:
    folder = OUT / case
    for label in ("A", "B"):
        md = folder / f"response_{label}.md"
        if md.exists():
            continue
        payload = json.loads(read(folder / f"response_{label}.json"))
        md.write_text(str(payload["text"]), encoding="utf-8")


def build_prompt(case: str) -> str:
    ensure_md(case)
    folder = OUT / case
    a = read(folder / "response_A.md")
    b = read(folder / "response_B.md")
    subject = "《我身藏诸界》21—30 的当前新 Horizon" if case == "ning_21_30" else "闻野舟这部普通单世界玄幻的完整 Story Program"
    return f"""# ROLE
你是 TGN Long-form Book Engine 的匿名 A/B judge。A 与 B 来自同一 Frozen Authority；不要猜实验条件，只直接比较规划质量。

# 核心问题
哪个候选更能让{subject}既有局部故事满足，又明显属于同一本持续增厚的长篇，而不是一段独立中篇？

重点判断：
1. Character-specific decision tension：人物已有私人牵引发生真实不兼容时，选择是否改变路线、对象、暴露、关系或机会成本；不能靠口癖、创伤倒推或无损第三解。
2. Local Closure → Book State Mutation：局部结算后，是否至少一个已有主体不能再按旧身份、旧关系、旧价格、旧策略或旧选择空间行动；纯保留 Canon、名单或获得新能力不算。
3. Historical Recontextualization：旧能力、关系、身份、资产、损失或知识是否在新语境里改变意义并进入当前因果，而非库存式复用。
4. Long-form pull：长期问题是否因新事实升压，同时不预写未知未来世界、Mystery 真相或固定回访税。
5. Payoff pressure：高价值结算是否把已建立欲望、差距/风险、旧积累与即时 consequence/repricing 连起来，而不是只有聪明解法或状态表。
6. Local story quality：当前 Horizon / Program 本身仍然具体、有欲望、有 Living Actors、有强 Fantasy；不能为了 Book Engine 把局部故事变成旧线维护。
7. Authority safety：不得新造未批准过去、世界规则、固定未来答案；不得任务板化、KPI化、关系数据库化。

# OUTPUT
## Candidate A
优点 / 硬问题 / 软问题
## Candidate B
优点 / 硬问题 / 软问题
## Comparative Findings
按上面核心问题说明差异，不打机械总分。
## Winner
只允许 `A` / `B` / `TIE`
## Verdict
`PASS / DIRECTIONAL PASS / PARTIAL PASS / FAIL`：这里判断较优方案是否证明额外 long-form craft 在这个 frozen sample 上有真实增益；若只有措辞更像原则、故事因果没变，不得给 PASS。
## What This Did Not Prove

=== CANDIDATE A ===
{a}

=== CANDIDATE B ===
{b}
"""


def run_one(case: str) -> dict:
    folder = OUT / case
    prompt = folder / "judge_prompt.md"
    result_path = folder / "judge.json"
    prompt.write_text(build_prompt(case), encoding="utf-8")
    cp = subprocess.run(
        ["node", str(RUNNER), str(prompt), str(result_path), "gpt-5.6-luna", "high", str(ROOT), str(GBRAIN)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=7200,
    )
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr[-4000:])
    payload = json.loads(read(result_path))
    if not payload.get("ok"):
        raise RuntimeError(str(payload.get("error")))
    text = str(payload["text"])
    (folder / "JUDGE.md").write_text(text, encoding="utf-8")
    return {"case": case, "wall_seconds": payload.get("wall_seconds"), "chars": len(text)}


def main() -> None:
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(run_one, case): case for case in CASES}
        for fut in concurrent.futures.as_completed(futures):
            row = fut.result()
            rows.append(row)
            print(row, flush=True)
    (OUT / "JUDGE_RUN_SUMMARY.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
