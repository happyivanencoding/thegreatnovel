from __future__ import annotations

import json
import concurrent.futures
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
EXP = ROOT / r"books\real-exp-agentic-gbrain-navigation-ab-20260901-v1"
OUT = EXP / "post-fix-rerun"
sys.path.insert(0, str(EXP))

import run_multi_sample_screen as multi
import run_agentic_ab as ning

multi.OUT = OUT / "multi-sample-terra"
ning.OUT = OUT / "ning-sol"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_terra() -> None:
    multi.run_screen()


def resume_terra() -> None:
    cases = list(multi.case_defs())
    nav_rows = []
    for case in cases:
        folder = multi.OUT / case
        if not (folder / "navigator_selection.json").exists():
            row = multi.run_navigator(case)
            nav_rows.append(row)
            print("NAV-RETRY", json.dumps(row, ensure_ascii=False), flush=True)

    for case in cases:
        multi.prepare_story_prompts(case)

    jobs = []
    for case in cases:
        folder = multi.OUT / case
        if not (folder / "A_terra.md").exists():
            jobs.append((case, "A"))
        if not (folder / "B_terra.md").exists():
            jobs.append((case, "B"))

    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(multi.run_story, case, label): (case, label) for case, label in jobs}
        for fut in concurrent.futures.as_completed(futures):
            row = fut.result()
            rows.append(row)
            print("STORY", json.dumps(row, ensure_ascii=False), flush=True)
    write(multi.OUT / "STORY_SUMMARY.json", json.dumps(rows, ensure_ascii=False, indent=2))


def run_terra_judges() -> None:
    multi.run_judges()


def run_ning() -> None:
    ning.run_navigator_ab("ning_21_30")


def ning_judge_prompt() -> str:
    case = "ning_21_30"
    folder = ning.OUT / case
    d = ning.case_data(case)
    a = read(folder / "A_fixed.md")
    b = read(folder / "B_navigator.md")
    return f"""# ROLE
你是 TGN post-fix Retrieval Structure 的匿名 A/B Judge。X/Y 使用完全相同 Frozen Authority 与同一 Sol-high Story Refresh 模型；只比较成品，不猜检索结构。

# FROZEN ROOT WORLD
{d['world_vision']}

# APPROVED FORWARD WORLD EXPANSIONS
{d['world_expansions']}

# FROZEN CHARACTER ORIGIN
{d['character_card']}

# CURRENT CHARACTER THROUGH CH20
{d['current_character']}

# BOOK / CANON THROUGH CH20
{d['book_content']}

# PREVIOUS APPROVED STORY PROGRAM
{d['proposal_context']}

# CURRENT STORY AUTHORITY RULE
Story Program / Story Refresh 可以在 World / Human / Canon 尚未定义的过去空白中补重要配角旧史、隐藏关系、亲缘/师徒/竞争/共同失败/债/失约/上一代选择，并把 Human 已成立的家庭关系与 World Living Actors 接成过去因果。只要不改写已发生/公开 Canon、不偷答 AUTHOR OPEN、不把未来伪造成过去，这类 Relationship-History Backfill 是合法创作权；不得仅因它不在 Frozen Human 原文里就判 Authority 越界。
**第21—30章的刷新 Story Program、RSE、阶段细节与新候选奖励并未预先冻结。X/Y 都是在同一已批准 Root World / Forward Expansions / Character / Canon-through-20 / Previous Story Authority 之上独立提出新的 Refresh。不得把 X 自己新写的 RSE、Backfill、阶段、奖励或 Handoff 当成 Authority 去判 Y“改写冻结内容”，反之亦然；只对照上面的真实 Frozen/Approved Authority。**

# JUDGMENT
哪个更值得继续作为第21—30章及后续长篇的 Story Refresh：
1. 当前 Horizon 本身是否有具体欲望、Living Actors、强幻想、冲突、获得与结算。
2. Book State Mutation 是否真实改变后续人、关系、资产、敌人策略、身份、价格、知识或行动窗口。
3. Historical Recontextualization / Character Afterlife 是否由旧事实在新条件下改变意义，而非库存回访。
4. Character-specific Choice 是否来自当前 Human，并保留真实机会成本，不统一成成长最优/关系最优/道德最优。
5. Local Closure 与长篇牵引是否同时成立；不机械召回旧人、不预写未知下一世界或 Mystery 真相。
6. Power ruler / Public Proof / Reward 是否遵守 Frozen Authority 与因果，不为 craft 好看而偷升阶、偷造世界对象或省略关键 acquisition/provenance 铰链。
7. Complexity tax：更多线程、术语、关系史若没有改变行动因果，算负增益。

# OUTPUT
## X
优点 / 硬问题 / 软问题
## Y
优点 / 硬问题 / 软问题
## Winner
`X` / `Y` / `TIE`
## Gain over X
`NONE` / `SMALL` / `MATERIAL`
## Human-specificity
## Verdict
`PASS / DIRECTIONAL PASS / PARTIAL PASS / FAIL`
## What This Did Not Prove

=== X ===
{a}

=== Y ===
{b}
"""


def run_ning_judge() -> None:
    folder = ning.OUT / "ning_21_30"
    p = folder / "judge_postfix_prompt.md"
    write(p, ning_judge_prompt())
    payload = ning.run_acp(p, folder / "judge_postfix.json", model="gpt-5.6-luna", effort="high")
    write(folder / "JUDGE_POSTFIX.md", str(payload["text"]))
    print(str(payload["text"]), flush=True)


def collect() -> None:
    data: dict[str, object] = {"terra": {}, "ning": {}}
    for case in multi.case_defs():
        folder = multi.OUT / case
        row: dict[str, object] = {}
        for name in ("fixed_retrieval.json", "navigator_selection.json", "STORY_SUMMARY.json", "JUDGE.md"):
            path = folder / name
            if path.exists():
                if path.suffix == ".json":
                    row[name] = json.loads(read(path))
                else:
                    row[name] = read(path)
        data["terra"][case] = row
    nfolder = ning.OUT / "ning_21_30"
    for name in ("fixed_retrieval.json", "navigator_selection.json", "run_summary.json", "JUDGE_POSTFIX.md"):
        path = nfolder / name
        if path.exists():
            data["ning"][name] = json.loads(read(path)) if path.suffix == ".json" else read(path)
    write(OUT / "COLLECTED.json", json.dumps(data, ensure_ascii=False, indent=2))


def main() -> None:
    action = sys.argv[1] if len(sys.argv) > 1 else "terra"
    if action == "terra":
        run_terra()
    elif action == "terra_resume":
        resume_terra()
    elif action == "terra_judges":
        run_terra_judges()
    elif action == "ning":
        run_ning()
    elif action == "ning_judge":
        run_ning_judge()
    elif action == "collect":
        collect()
    else:
        raise SystemExit("terra|terra_resume|terra_judges|ning|ning_judge|collect")


if __name__ == "__main__":
    main()
