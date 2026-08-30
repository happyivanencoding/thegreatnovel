from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import random
import sys


ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(EXP))

from run_experiment import CASES, dump, judge_prompt, run_acp, story_refresh_prompt  # noqa: E402
from story_mvp.progressive_canon import (  # noqa: E402
    adopt_hidden_fixed_point,
    extract_reframe_candidates,
    render_planning_projection,
)


TARGETS = ("identity_archive", "relationship_betrayal")


def cases_by_id():
    return {case.case_id: case for case in CASES}


def run_t2() -> dict[str, dict]:
    by_id = cases_by_id()
    result: dict[str, dict] = {}
    jobs = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for case_id in TARGETS:
            case = by_id[case_id]
            d = EXP / case_id
            candidates = extract_reframe_candidates((d / "REFRAME.md").read_text(encoding="utf-8"))
            selected = candidates[case.preregistered_candidate]
            compiler = (d / "COMPILER.md").read_text(encoding="utf-8")
            fixed = adopt_hidden_fixed_point(
                thread=case.thread,
                selected_candidate=selected,
                compiler_report=compiler,
            )
            projection = render_planning_projection(fixed)
            (d / "V2_PLANNING_PROJECTION.md").write_text(projection + "\n", encoding="utf-8")
            prompt = story_refresh_prompt(case, projection)
            (d / "T2_STORY_REFRESH_PROMPT.md").write_text(prompt, encoding="utf-8")
            jobs.append(
                (
                    case,
                    pool.submit(
                        run_acp,
                        d / "T2_STORY_REFRESH_PROMPT.md",
                        d / "T2_STORY_REFRESH_ACP.json",
                        d / "T2_STORY_REFRESH.md",
                        model="gpt-5.6-sol",
                        effort="high",
                        label=f"progressive-canon-v2-{case_id}-refresh",
                    ),
                )
            )
        for case, future in jobs:
            run = future.result()
            result[case.case_id] = {"wall": run["wall"], "model": run["model"]}
    return result


def authority_audit_prompt(case_id: str) -> str:
    case = cases_by_id()[case_id]
    d = EXP / case_id
    selected = (d / "SELECTED_CANDIDATE.md").read_text(encoding="utf-8")
    t1 = (d / "T_STORY_REFRESH.md").read_text(encoding="utf-8")
    t2 = (d / "T2_STORY_REFRESH.md").read_text(encoding="utf-8")
    return f"""你是 TGN Progressive Canonization 的独立 Authority 审计员。比较同一已批准 Hidden Fixed Point 下的 V1 与 V2 Story Refresh。只审实际输出，不改稿。

V1 只拿到 Fixed Point + Still Open；V2 唯一新增的是保存并显式传入原候选的 Reveal Boundary，并要求规划必须使用 Fixed Point、在 Reveal Boundary 允许的当前阶段安排可观察的 future reveal，同时不得越界。

判断：
1. V1 是否出现 under-use：知道作者有 Hidden Truth，却没有让下一阶段的门、证据、行为或未来 reveal 真正受它约束；
2. V2 是否修复 under-use；
3. V2 是否反过来把 Author Hidden Truth 当作已发生 Reader Canon，造成 premature reveal；
4. V2 是否越过 What Remains Unknown；
5. 两版是否吃掉已发生 Canon；
6. 新增 Reveal Boundary 是否是必要的最小控制，还是多余字段。

严格输出：
# REVEAL BOUNDARY AUTHORITY AUDIT
Case: {case_id}
V1 Fixed-Point Use: PASS / UNDERUSED / OVERREVEALED
V2 Fixed-Point Use: PASS / UNDERUSED / OVERREVEALED
V2 Still-Open Boundary: PASS / FAIL
Backward Compatibility: PASS / FAIL
Reveal Boundary Necessary: YES / NO / UNCLEAR
Verdict: PASS / DIRECTIONAL PASS / FAIL
Reason: 6—12句

# EXISTING CANON / PLANNING NEED
{case.context}

{case.planning_need}

# AUTHOR-SELECTED REFRAME
{selected}

# V1 STORY REFRESH
{t1}

# V2 STORY REFRESH
{t2}
"""


def run_authority_audits(summary: dict[str, dict]) -> None:
    jobs = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for case_id in TARGETS:
            d = EXP / case_id
            prompt = authority_audit_prompt(case_id)
            pp = d / "V2_AUTHORITY_AUDIT_PROMPT.md"
            pp.write_text(prompt, encoding="utf-8")
            jobs.append(
                (
                    case_id,
                    pool.submit(
                        run_acp,
                        pp,
                        d / "V2_AUTHORITY_AUDIT_ACP.json",
                        d / "V2_AUTHORITY_AUDIT.md",
                        model="gpt-5.6-terra",
                        effort="high",
                        label=f"progressive-canon-v2-{case_id}-authority-audit",
                    ),
                )
            )
        for case_id, future in jobs:
            run = future.result()
            summary[case_id]["authority_audit_wall"] = run["wall"]


def build_blind_package() -> tuple[str, dict[str, dict[str, str]]]:
    rng = random.Random(2026083002)
    by_id = cases_by_id()
    mapping: dict[str, dict[str, str]] = {}
    blocks = []
    for case_id in TARGETS:
        case = by_id[case_id]
        d = EXP / case_id
        b0 = (d / "B0_STORY_REFRESH.md").read_text(encoding="utf-8")
        t2 = (d / "T2_STORY_REFRESH.md").read_text(encoding="utf-8")
        pair = [("B0", b0), ("T2", t2)]
        rng.shuffle(pair)
        mapping[case_id] = {"X": pair[0][0], "Y": pair[1][0]}
        blocks.append(
            "\n\n".join(
                (
                    f"# CASE {case_id}",
                    "## Frozen Known Facts\n" + case.context,
                    "## Planning Need\n" + case.planning_need,
                    "## Version X\n" + pair[0][1],
                    "## Version Y\n" + pair[1][1],
                )
            )
        )
    return "\n\n---\n\n".join(blocks), mapping


def run_blind(summary: dict[str, dict]) -> None:
    package, mapping = build_blind_package()
    (EXP / "V2_BLIND_PACKAGE.md").write_text(package + "\n", encoding="utf-8")
    dump(EXP / "V2_BLIND_MAPPING.json", mapping)
    prompts = {
        "cold_reader": judge_prompt(package, "商业冷读：优先看故事推进、人物选择、Mystery牵引与继续追读；解释完整本身不加分。"),
        "longform": judge_prompt(package, "长篇结构：优先看局部定真是否真正服务未来事件、是否保留更深未知、是否避免吃书和预制终局。"),
    }
    jobs = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for name, prompt in prompts.items():
            pp = EXP / f"V2_BLIND_{name.upper()}_PROMPT.md"
            pp.write_text(prompt, encoding="utf-8")
            jobs.append(
                (
                    name,
                    pool.submit(
                        run_acp,
                        pp,
                        EXP / f"V2_BLIND_{name.upper()}_ACP.json",
                        EXP / f"V2_BLIND_{name.upper()}.md",
                        model="gpt-5.6-terra" if name == "cold_reader" else "gpt-5.6-luna",
                        effort="high",
                        label=f"progressive-canon-v2-blind-{name}",
                    ),
                )
            )
        for name, future in jobs:
            run = future.result()
            summary.setdefault("judges", {})[name] = {"wall": run["wall"], "model": run["model"]}


def main() -> None:
    summary = {case_id: {} for case_id in TARGETS}
    runs = run_t2()
    for case_id, value in runs.items():
        summary[case_id].update(value)
    run_authority_audits(summary)
    run_blind(summary)
    summary["only_variable_after_selected_candidate"] = "Reveal Boundary retention + planning-use instruction"
    dump(EXP / "V2_RUN_SUMMARY.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
