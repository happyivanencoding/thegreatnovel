from __future__ import annotations

import concurrent.futures
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
GBRAIN = Path(r"C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库")
OUT = ROOT / r"books\real-exp-agentic-gbrain-navigation-ab-20260901-v1"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
MULTI = ROOT / r"books\real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"
SINGLE = ROOT / r"books\real-exp-private-prototype-asymmetry-pace-ruler-20260827-v1"
NAV_TOOL = OUT / "gbrain_nav_tool.py"

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.gbrain_retrieval import build_retrieval_brief, retrieve_gbrain


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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
        raise RuntimeError(cp.stderr[-5000:])
    payload = json.loads(read(out_json))
    if not payload.get("ok"):
        raise RuntimeError(str(payload.get("error")))
    return payload


def case_data(case: str) -> dict[str, str | int]:
    if case == "ning_21_30":
        return {
            "mode": "story_refresh",
            "start": 21,
            "book_content": read(MULTI / "BOOK_AFTER_CH20.md"),
            "creative_direction": (
                "《我身藏诸界》第21—30章 frozen-authority Story Refresh。"
                "不改已批准 World / Character / Canon；让当前 Horizon 本身好看，同时让已经发生的历史继续产生真实因果。"
            ),
            "world_vision": read(MULTI / "WORLD_VISION.md"),
            "world_expansions": read(MULTI / "WORLD_EXPANSIONS.md"),
            "character_card": read(MULTI / "CHARACTER.md"),
            "current_character": read(MULTI / "planning" / "current-character-through-20.md"),
            "proposal_context": read(MULTI / "STORY_PROGRAM_11_20.md"),
        }
    if case == "wen_singleworld":
        return {
            "mode": "idea",
            "start": 1,
            "book_content": "",
            "creative_direction": read(SINGLE / "AUTHOR_DIRECTION.md"),
            "world_vision": read(SINGLE / "WORLD_VISION.md"),
            "world_expansions": "",
            "character_card": read(SINGLE / "CHARACTER.md"),
            "current_character": "",
            "character_initial_state": read(SINGLE / "CHARACTER_INITIAL_STATE.md"),
            "proposal_context": "",
        }
    raise ValueError(case)


def retrieval_kwargs(data: dict[str, str | int]) -> dict[str, str]:
    return {
        "mode": str(data["mode"]),
        "book_content": str(data.get("book_content", "")),
        "creative_direction": str(data.get("creative_direction", "")),
        "world_vision": str(data.get("world_vision", "")),
        "character_card": str(data.get("character_card", "")),
        "proposal_context": str(data.get("proposal_context", "")),
    }


def build_story_prompt(case: str, gbrain_bundle: str) -> str:
    d = case_data(case)
    if d["mode"] == "story_refresh":
        return generate_split_prompt(
            mode="story_refresh",
            book_content=str(d["book_content"]),
            creative_direction=str(d["creative_direction"]),
            world_vision=str(d["world_vision"]),
            world_expansions=str(d["world_expansions"]),
            character_card=str(d["character_card"]),
            current_character=str(d["current_character"]),
            creative_state={
                "world_vision": {"status": "author_approved"},
                "character_card": {"status": "author_approved"},
                "proposal": {"status": "author_approved"},
            },
            proposal_context=str(d["proposal_context"]),
            selected_references=[],
            gbrain_inspiration=gbrain_bundle,
            effective_from_chapter=int(d["start"]),
        )
    return generate_split_prompt(
        mode="idea",
        creative_direction=str(d["creative_direction"]),
        world_vision=str(d["world_vision"]),
        character_card=str(d["character_card"]),
        character_initial_state=str(d.get("character_initial_state", "")),
        creative_state={
            "world_vision": {"status": "author_approved"},
            "character_card": {"status": "author_approved"},
        },
        selected_references=[],
        gbrain_inspiration=gbrain_bundle,
    )


def baseline_bundle(case: str) -> dict:
    return retrieve_gbrain(**retrieval_kwargs(case_data(case)))


def navigator_prompt(case: str) -> str:
    d = case_data(case)
    brief = build_retrieval_brief(**retrieval_kwargs(d))
    return f"""# ROLE
你是 TGN GBrain Retrieval Navigator。你不写 Story Program，只负责为一个已经冻结 Authority 的规划任务主动探索 source-blind craft。

# 当前任务
{brief}

# 允许使用的唯一检索工具
在仓库根目录通过 shell 调用：
python "{NAV_TOOL}" search --case {case} --query "你的查询"
python "{NAV_TOOL}" get --case {case} --slug "返回的slug"

# 实验约束
- 必须主动做 2—4 次 search；最多 6 次 get。
- 第一跳从你判断的当前真正缺口出发，不要照抄现有固定 alias 列表。
- 至少一次后续 search 必须来自上一跳结果里新发现的概念；这才算 multi-hop。
- 只允许通过上面的工具读取 GBrain；不要直接打开 GBrain 原始文件或 source evidence。
- GBrain 只是 Optional Inspiration，不得覆盖 Frozen World / Human / Power / Canon。
- 不为凑数选卡；最后最多 3 张，也允许少于 3 张。
- 优先选会改变“下一步 Story 决策”的知识，而不是同义原则。

# FINAL OUTPUT
只输出 JSON，不要 markdown fence：
{{
  "searches": [{{"query":"...","why":"...","discovered":"..."}}],
  "selected_slugs": ["..."],
  "synthesis": "说明这几张卡组合后具体改变什么规划判断；若没有真实增益就说明没有"
}}
"""


def parse_json_object(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("navigator did not return JSON")
    return json.loads(text[start : end + 1])


def navigator_bundle(case: str, nav_payload: dict) -> tuple[str, list[dict]]:
    slugs = nav_payload.get("selected_slugs") or []
    if not isinstance(slugs, list) or len(slugs) > 3:
        raise ValueError("navigator selected_slugs must be a list of at most 3")
    items: list[dict] = []
    for slug in slugs:
        cp = subprocess.run(
            [sys.executable, str(NAV_TOOL), "get", "--case", case, "--slug", str(slug)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=120,
        )
        if cp.returncode != 0:
            raise RuntimeError(cp.stderr or cp.stdout)
        items.append(json.loads(cp.stdout))
    blocks = []
    for i, item in enumerate(items, 1):
        blocks.append(
            "\n".join(
                [
                    f"### Inspiration {i}",
                    f"source: {item['slug']}",
                    f"type: {item['type']}",
                    "",
                    f"可用抽象：{item['abstract']}",
                    "",
                    f"使用边界：{item.get('transfer_boundary') or '只迁移抽象机制，不迁移来源故事表层。'}",
                ]
            )
        )
    return "\n\n".join(blocks), items


def jit_prompt(case: str) -> str:
    base = build_story_prompt(case, "")
    return f"""# EXPERIMENTAL JIT GBRAIN NAVIGATION
你仍然是下方正式 TGN Story Program / Story Refresh Agent，但这次没有上游预选 Inspiration。
在开始最终规划前，你可以把 GBrain 当作 JIT 搜索工具主动查询。

唯一允许的知识检索工具：
python "{NAV_TOOL}" search --case {case} --query "你的查询"
python "{NAV_TOOL}" get --case {case} --slug "返回的slug"

约束：
- 做 2—4 次 search，最多 6 次 get；至少一次 follow-up query 来自上一跳新发现的概念。
- 只通过该工具读取 source-blind active inspiration；不得直接读 GBrain 原始文件/source evidence。
- 搜索只是为了补当前规划缺口。够了就停，不需要覆盖所有知识。
- Frozen World / Character / Canon / Previous Story 高于 GBrain；GBrain 不能创建 Authority。
- 最终回答只输出正式 Story Program / Story Refresh，不要输出搜索日志、工具说明或检索分析。

# FORMAL STORY PROMPT
{base}
"""


def save_payload(folder: Path, label: str, payload: dict) -> None:
    write(folder / f"{label}.md", str(payload["text"]))
    write(folder / f"{label}.json", json.dumps(payload, ensure_ascii=False, indent=2))


def run_case(case: str) -> None:
    folder = OUT / case
    folder.mkdir(parents=True, exist_ok=True)

    fixed = baseline_bundle(case)
    write(folder / "fixed_retrieval.json", json.dumps(fixed, ensure_ascii=False, indent=2))
    fixed_slugs = [x["slug"] for x in fixed.get("accepted", [])]
    print({"case": case, "fixed_slugs": fixed_slugs}, flush=True)

    nav_p = folder / "navigator_prompt.md"
    jit_p = folder / "prompt_C_jit.md"
    write(nav_p, navigator_prompt(case))
    write(jit_p, jit_prompt(case))

    # Navigator and integrated JIT are independent and can run together.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        f_nav = ex.submit(run_acp, nav_p, folder / "navigator.json")
        f_jit = ex.submit(run_acp, jit_p, folder / "C_jit.json")
        nav_result = f_nav.result()
        jit_result = f_jit.result()

    write(folder / "navigator.md", str(nav_result["text"]))
    nav = parse_json_object(str(nav_result["text"]))
    write(folder / "navigator_selection.json", json.dumps(nav, ensure_ascii=False, indent=2))
    nav_bundle, nav_items = navigator_bundle(case, nav)
    write(folder / "navigator_bundle.md", nav_bundle)
    write(folder / "navigator_items.json", json.dumps(nav_items, ensure_ascii=False, indent=2))
    save_payload(folder, "C_jit", jit_result)

    prompt_a = build_story_prompt(case, str(fixed.get("result") or ""))
    prompt_b = build_story_prompt(case, nav_bundle)
    write(folder / "prompt_A_fixed.md", prompt_a)
    write(folder / "prompt_B_navigator.md", prompt_b)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        f_a = ex.submit(run_acp, folder / "prompt_A_fixed.md", folder / "A_fixed.json")
        f_b = ex.submit(run_acp, folder / "prompt_B_navigator.md", folder / "B_navigator.json")
        a = f_a.result()
        b = f_b.result()
    save_payload(folder, "A_fixed", a)
    save_payload(folder, "B_navigator", b)

    summary = {
        "case": case,
        "fixed_slugs": fixed_slugs,
        "navigator_searches": nav.get("searches", []),
        "navigator_slugs": nav.get("selected_slugs", []),
        "wall_seconds": {
            "navigator": nav_result.get("wall_seconds"),
            "A_fixed": a.get("wall_seconds"),
            "B_story_only": b.get("wall_seconds"),
            "B_total": (nav_result.get("wall_seconds") or 0) + (b.get("wall_seconds") or 0),
            "C_jit": jit_result.get("wall_seconds"),
        },
        "chars": {
            "A_fixed": len(str(a["text"])),
            "B_navigator": len(str(b["text"])),
            "C_jit": len(str(jit_result["text"])),
        },
    }
    write(folder / "run_summary.json", json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


def run_ab_from_completed_navigator(case: str) -> None:
    """Resume after a JIT stall without rerunning the completed Navigator."""
    folder = OUT / case
    fixed = json.loads(read(folder / "fixed_retrieval.json"))
    nav_wrapper = json.loads(read(folder / "navigator.json"))
    nav = parse_json_object(str(nav_wrapper["text"]))
    write(folder / "navigator.md", str(nav_wrapper["text"]))
    write(folder / "navigator_selection.json", json.dumps(nav, ensure_ascii=False, indent=2))
    nav_bundle, nav_items = navigator_bundle(case, nav)
    write(folder / "navigator_bundle.md", nav_bundle)
    write(folder / "navigator_items.json", json.dumps(nav_items, ensure_ascii=False, indent=2))

    write(folder / "prompt_A_fixed.md", build_story_prompt(case, str(fixed.get("result") or "")))
    write(folder / "prompt_B_navigator.md", build_story_prompt(case, nav_bundle))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        f_a = ex.submit(run_acp, folder / "prompt_A_fixed.md", folder / "A_fixed.json")
        f_b = ex.submit(run_acp, folder / "prompt_B_navigator.md", folder / "B_navigator.json")
        a = f_a.result()
        b = f_b.result()
    save_payload(folder, "A_fixed", a)
    save_payload(folder, "B_navigator", b)
    summary = {
        "case": case,
        "C_jit": "STALL_NO_FINAL_AFTER_~15_MIN",
        "fixed_slugs": [x["slug"] for x in fixed.get("accepted", [])],
        "navigator_searches": nav.get("searches", []),
        "navigator_slugs": nav.get("selected_slugs", []),
        "wall_seconds": {
            "navigator": nav_wrapper.get("wall_seconds"),
            "A_fixed": a.get("wall_seconds"),
            "B_story_only": b.get("wall_seconds"),
            "B_total": (nav_wrapper.get("wall_seconds") or 0) + (b.get("wall_seconds") or 0),
        },
        "chars": {"A_fixed": len(str(a["text"])), "B_navigator": len(str(b["text"]))},
    }
    write(folder / "run_summary.json", json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


def run_navigator_ab(case: str) -> None:
    """Run fixed retrieval vs Navigator->fresh Story without the failed integrated JIT shape."""
    folder = OUT / case
    folder.mkdir(parents=True, exist_ok=True)
    fixed = baseline_bundle(case)
    write(folder / "fixed_retrieval.json", json.dumps(fixed, ensure_ascii=False, indent=2))
    nav_prompt_path = folder / "navigator_prompt.md"
    write(nav_prompt_path, navigator_prompt(case))
    nav_wrapper = run_acp(nav_prompt_path, folder / "navigator.json")
    write(folder / "navigator.md", str(nav_wrapper["text"]))
    nav = parse_json_object(str(nav_wrapper["text"]))
    write(folder / "navigator_selection.json", json.dumps(nav, ensure_ascii=False, indent=2))
    nav_bundle, nav_items = navigator_bundle(case, nav)
    write(folder / "navigator_bundle.md", nav_bundle)
    write(folder / "navigator_items.json", json.dumps(nav_items, ensure_ascii=False, indent=2))

    write(folder / "prompt_A_fixed.md", build_story_prompt(case, str(fixed.get("result") or "")))
    write(folder / "prompt_B_navigator.md", build_story_prompt(case, nav_bundle))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        f_a = ex.submit(run_acp, folder / "prompt_A_fixed.md", folder / "A_fixed.json")
        f_b = ex.submit(run_acp, folder / "prompt_B_navigator.md", folder / "B_navigator.json")
        a = f_a.result()
        b = f_b.result()
    save_payload(folder, "A_fixed", a)
    save_payload(folder, "B_navigator", b)
    summary = {
        "case": case,
        "fixed_slugs": [x["slug"] for x in fixed.get("accepted", [])],
        "navigator_searches": nav.get("searches", []),
        "navigator_slugs": nav.get("selected_slugs", []),
        "wall_seconds": {
            "navigator": nav_wrapper.get("wall_seconds"),
            "A_fixed": a.get("wall_seconds"),
            "B_story_only": b.get("wall_seconds"),
            "B_total": (nav_wrapper.get("wall_seconds") or 0) + (b.get("wall_seconds") or 0),
        },
    }
    write(folder / "run_summary.json", json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


def pair_judge_prompt(case: str) -> str:
    folder = OUT / case
    a_payload = json.loads(read(folder / "A_fixed.json"))
    b_path = folder / "B_navigator.json"
    if not b_path.exists():
        b_path = folder / "B_navigator_retry.json"
    b_payload = json.loads(read(b_path))
    x = str(a_payload["text"])
    y = str(b_payload["text"])
    return f"""# ROLE
你是 TGN Long-form Story Engine 的匿名 A/B judge。X/Y 使用相同 Frozen Authority、相同 Sol-high Story 模型，只有进入 Story Agent 的 GBrain inspiration 选择方式不同。不要猜实验条件，只读成品。

# 判断问题
哪个候选更像真正值得继续写的同一本长篇，而不是把更多 Story Craft 术语塞进规划？

重点比较：
1. 当前 Horizon / Story Program 本身是否有具体欲望、Living Actors、强幻想、冲突和结算。
2. Book State Mutation 是否真实改变后来的人、关系、资产、敌人策略、价格、知识或行动窗口。
3. Historical Recontextualization / Character Afterlife 是否让旧东西在新条件下改变意义或用途，而非库存式回访。
4. Character-specific Choice 是否来自 Frozen Human，且保留真实机会成本，不统一成“最优成长解”。
5. 长篇牵引是否升压，但不预写未知未来世界、Mystery 真相或机械召回旧人。
6. 是否形成新的具体因果组合，而不是照抄原则。
7. Authority safety：不得新造未批准过去、世界规则、固定未来真相。
8. Complexity tax：更多线程/解释若没有改变行动因果，算负增益。

# OUTPUT
## X
优点 / 硬问题 / 软问题
## Y
优点 / 硬问题 / 软问题
## Winner
只允许 `X` / `Y` / `TIE`
## Meaningful Gain over X
只允许 `NONE / SMALL / MATERIAL`
## Verdict
`PASS / DIRECTIONAL PASS / PARTIAL PASS / FAIL`
## What This Did Not Prove

=== X ===
{x}

=== Y ===
{y}
"""


def run_pair_judge(case: str) -> None:
    folder = OUT / case
    p = folder / "judge_ab_prompt.md"
    write(p, pair_judge_prompt(case))
    payload = run_acp(p, folder / "judge_ab.json", model="gpt-5.6-luna", effort="high")
    write(folder / "JUDGE_AB.md", str(payload["text"]))
    print(str(payload["text"]), flush=True)


def judge_prompt(case: str) -> str:
    f = OUT / case
    x = read(f / "A_fixed.md")
    y = read(f / "B_navigator.md")
    z = read(f / "C_jit.md")
    return f"""# ROLE
你是 TGN Long-form Story Engine 的匿名三候选 judge。X/Y/Z 使用相同 Frozen Authority 与同一 Sol-high Story 模型，只是知识检索结构不同。不要猜结构，只读成品。

# 判断问题
哪一个最像真正值得继续写的同一本长篇，而不是把更多 Story Craft 术语塞进规划？

重点比较：
1. 当前 Horizon / Story Program 本身是否有具体欲望、Living Actors、强幻想、冲突和结算，不被“长篇维护”吞掉。
2. Book State Mutation：阶段结束后，是否真的有人/关系/资产/敌人策略/价格/知识/行动窗口从此不能按旧状态运作。
3. Historical Recontextualization / Character Afterlife：旧东西是否在新条件下改变用途、意义、风险或社会价格，而不是库存式回访。
4. Character-specific Choice：路线分叉是否来自这个 Frozen Human 的私人牵引，且有真实机会成本；不要奖励统一的“最优成长解”。
5. Long-form pull：长期问题是否升压但不预写未知未来世界、Mystery 真相或机械召回旧人。
6. Creative synthesis：是否形成单张卡没有直接写出的新组合，而不是照抄原则。
7. Authority safety：不得新造未批准过去、世界规则、固定未来真相；GBrain inspiration 不能变 Canon。
8. Complexity tax：如果只是措辞更复杂、线程更多、解释更多，却没有改变行动因果，判为负增益。

# OUTPUT
## X
优点 / 硬问题 / 软问题
## Y
优点 / 硬问题 / 软问题
## Z
优点 / 硬问题 / 软问题
## Ranking
明确写 `1 > 2 > 3`，用 X/Y/Z。
## Meaningful Gain?
说明第一名相对 X（现有基线）的增益是 `NONE / SMALL / MATERIAL`。
## Verdict
`PASS / DIRECTIONAL PASS / PARTIAL PASS / FAIL`
## What This Did Not Prove

=== X ===
{x}

=== Y ===
{y}

=== Z ===
{z}
"""


def run_judge(case: str) -> None:
    folder = OUT / case
    p = folder / "judge_prompt.md"
    write(p, judge_prompt(case))
    payload = run_acp(p, folder / "judge.json", model="gpt-5.6-luna", effort="high")
    write(folder / "JUDGE.md", str(payload["text"]))
    print(str(payload["text"]), flush=True)


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "run"
    case = sys.argv[2] if len(sys.argv) > 2 else "ning_21_30"
    if action == "run":
        run_case(case)
    elif action == "ab":
        run_ab_from_completed_navigator(case)
    elif action == "navab":
        run_navigator_ab(case)
    elif action == "judge_ab":
        run_pair_judge(case)
    elif action == "judge":
        run_judge(case)
    else:
        raise SystemExit("usage: run_agentic_ab.py run|ab|navab|judge_ab|judge [case]")
