from __future__ import annotations

import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
GBRAIN = Path(r"C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库")
RESEARCH = GBRAIN / r"reference-corpus\operations\gbrain-longform-spine-tension-v1-20260901"
OUT = ROOT / r"books\real-exp-book-engine-mutation-ab-20260901-v1"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
MULTI = ROOT / r"books\real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"
SINGLE = ROOT / r"books\real-exp-private-prototype-asymmetry-pace-ruler-20260827-v1"

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.character_prompts import generate_split_prompt


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def treatment_bundle() -> str:
    text = read(RESEARCH / r"synthesis\CROSS_BOOK_SOL_SYNTHESIS.md")
    start = text.index("## 8. Source-Blind Treatment Bundle for TGN A/B")
    body = text[start:].split("## 9. Failure Modes / Boundaries", 1)[0]
    return body.split("\n", 2)[2].strip()


def run_acp(prompt_path: Path, out_json: Path, model: str = "gpt-5.6-sol", effort: str = "high") -> dict:
    cp = subprocess.run(
        ["node", str(RUNNER), str(prompt_path), str(out_json), model, effort, str(ROOT), str(GBRAIN)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=10800,
    )
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr[-4000:])
    payload = json.loads(read(out_json))
    if not payload.get("ok"):
        raise RuntimeError(str(payload.get("error")))
    return payload


def multi_gbrain(start: int, end: int) -> str:
    data = json.loads(read(MULTI / "planning" / f"story-{start:02d}-{end:02d}" / "gbrain.json"))
    return str(data.get("result") or "")


def build_multi_prompt(start: int, extra: str) -> str:
    end = start + 9
    previous = "STORY_PROGRAM_11_20.md" if start == 21 else "STORY_PROGRAM_21_30.md"
    gbrain = multi_gbrain(start, end)
    if extra:
        gbrain = gbrain.rstrip() + "\n\n### Additional source-blind long-form craft\n" + extra.strip() + "\n"
    return generate_split_prompt(
        mode="story_refresh",
        book_content=read(MULTI / f"BOOK_AFTER_CH{start-1:02d}.md"),
        creative_direction=(
            f"《我身藏诸界》第{start}—{end}章 frozen-authority Story Refresh 回归。"
            "不改已批准 World / Character / Canon；只重新规划当前 Horizon，使局部故事成立并让已经发生的历史继续产生真实因果。"
        ),
        world_vision=read(MULTI / "WORLD_VISION.md"),
        world_expansions=read(MULTI / "WORLD_EXPANSIONS.md"),
        character_card=read(MULTI / "CHARACTER.md"),
        current_character=read(MULTI / "planning" / f"current-character-through-{start-1}.md"),
        creative_state={
            "world_vision": {"status": "author_approved"},
            "character_card": {"status": "author_approved"},
            "proposal": {"status": "author_approved"},
        },
        proposal_context=read(MULTI / previous),
        selected_references=[],
        gbrain_inspiration=gbrain,
        effective_from_chapter=start,
    )


def build_single_prompt(extra: str) -> str:
    gbrain = read(SINGLE / "STORY_GBRAIN.md")
    if extra:
        gbrain = gbrain.rstrip() + "\n\n### Additional source-blind long-form craft\n" + extra.strip() + "\n"
    return generate_split_prompt(
        mode="idea",
        creative_direction=read(SINGLE / "AUTHOR_DIRECTION.md"),
        world_vision=read(SINGLE / "WORLD_VISION.md"),
        character_card=read(SINGLE / "CHARACTER.md"),
        character_initial_state=read(SINGLE / "CHARACTER_INITIAL_STATE.md"),
        creative_state={
            "world_vision": {"status": "author_approved"},
            "character_card": {"status": "author_approved"},
        },
        selected_references=[],
        gbrain_inspiration=gbrain,
    )


def build_prompts() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    bundle = treatment_bundle()
    (OUT / "TREATMENT_BUNDLE.md").write_text(bundle + "\n", encoding="utf-8")
    cases = {
        "ning_21_30": (build_multi_prompt(21, ""), build_multi_prompt(21, bundle)),
        "ning_31_40": (build_multi_prompt(31, ""), build_multi_prompt(31, bundle)),
        "wen_singleworld": (build_single_prompt(""), build_single_prompt(bundle)),
    }
    for case, (a, b) in cases.items():
        folder = OUT / case
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "prompt_A.md").write_text(a, encoding="utf-8")
        (folder / "prompt_B.md").write_text(b, encoding="utf-8")


def run_pairs() -> None:
    build_prompts()
    jobs = []
    for case in ("ning_21_30", "ning_31_40", "wen_singleworld"):
        folder = OUT / case
        for label in ("A", "B"):
            jobs.append((case, label, folder / f"prompt_{label}.md", folder / f"response_{label}.json"))
    rows = []
    # Three simultaneous Codex ACP sessions can stall after initialization on this Windows host.
    # Two-way concurrency is the highest level already demonstrated to make forward progress.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(run_acp, p, j): (case, label, j) for case, label, p, j in jobs}
        for fut in concurrent.futures.as_completed(futures):
            case, label, out_json = futures[fut]
            payload = fut.result()
            text = str(payload["text"])
            folder = OUT / case
            (folder / f"response_{label}.md").write_text(text, encoding="utf-8")
            row = {
                "case": case,
                "label": label,
                "wall_seconds": payload.get("wall_seconds"),
                "chars": len(text),
            }
            rows.append(row)
            print(row, flush=True)
    (OUT / "PAIR_RUN_SUMMARY.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def judge_prompt(case: str) -> str:
    folder = OUT / case
    a = read(folder / "response_A.md")
    b = read(folder / "response_B.md")
    multi = case.startswith("ning_")
    subject = "《我身藏诸界》的当前新 Horizon" if multi else "闻野舟这部普通单世界玄幻的完整 Story Program"
    return f"""# ROLE
你是 TGN Long-form Book Engine 的匿名 A/B judge。A 与 B 来自同一 Frozen Authority；不要猜实验条件，只直接比较规划质量。

# 核心问题
哪个候选更能让{subject}既有局部故事满足，又明显属于同一本持续增厚的长篇，而不是一段独立中篇？

重点判断：
1. Character-specific decision tension：人物已有私人牵引发生真实不兼容时，选择是否改变路线/对象/暴露/机会成本；不能靠口癖、创伤倒推或无损第三解。
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
`PASS / DIRECTIONAL PASS / PARTIAL PASS / FAIL`：这里判断较优方案是否证明“额外 long-form craft”在这个 frozen sample 上有真实增益；若只有措辞更像原则、故事因果没变，不得给 PASS。
## What This Did Not Prove

=== CANDIDATE A ===
{a}

=== CANDIDATE B ===
{b}
"""


def run_judges() -> None:
    jobs = []
    for case in ("ning_21_30", "ning_31_40", "wen_singleworld"):
        folder = OUT / case
        p = folder / "judge_prompt.md"
        p.write_text(judge_prompt(case), encoding="utf-8")
        jobs.append((case, p, folder / "judge.json"))
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(run_acp, p, j, "gpt-5.6-luna", "high"): (case, j) for case, p, j in jobs}
        for fut in concurrent.futures.as_completed(futures):
            case, out_json = futures[fut]
            payload = fut.result()
            text = str(payload["text"])
            folder = OUT / case
            (folder / "JUDGE.md").write_text(text, encoding="utf-8")
            row = {"case": case, "wall_seconds": payload.get("wall_seconds"), "chars": len(text)}
            rows.append(row)
            print(row, flush=True)
    (OUT / "JUDGE_RUN_SUMMARY.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "pairs"
    if stage == "prompts":
        build_prompts()
    elif stage == "pairs":
        run_pairs()
    elif stage == "judges":
        run_judges()
    else:
        raise SystemExit("use prompts|pairs|judges")
