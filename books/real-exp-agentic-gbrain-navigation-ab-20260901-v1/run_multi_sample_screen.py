from __future__ import annotations

import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
GBRAIN_ROOT = Path(r"C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库")
OUT = ROOT / r"books\real-exp-agentic-gbrain-navigation-ab-20260901-v1\multi-sample-terra-screen"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
SELF = Path(__file__).resolve()

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.gbrain import get_gbrain
from story_mvp.gbrain_retrieval import (
    MODE_ALLOWED_CATEGORIES,
    _has_surface_conflict,
    active_inspiration_allowed,
    build_retrieval_brief,
    extract_abstract_content,
    extract_hard_constraints,
    retrieve_gbrain,
    source_category,
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


GENERIC_MULTIWORLD_DIRECTION = (
    "成熟中文男频成长长篇。严格保持已冻结 World / Power / Human，不重写它们。"
    "让这个具体 Human 的私人欲望真实改变路线、对象与机会成本；Living Actors 在主角缺席时也继续行动。"
    "追求强 Fantasy、具体高价值获得、关系与长期因果复利，避免治理、工程、任务板和成长最优解。"
)


def case_defs() -> dict[str, dict[str, Path | str]]:
    game = ROOT / r"books\real-exp-game-instance-rse-5ch-20260829-v2"
    atl = ROOT / r"books\real-exp-atlantis-ocean-10ch-20260901-v1\artifacts"
    multi = ROOT / r"books\real-exp-multiworld-personality-advantage-20260831-v1"
    beast = multi / "w1_beast_ridges"
    star = multi / "w2_fallen_star_sea"
    return {
        "game_instance": {
            "direction": game / "AUTHOR_DIRECTION.md",
            "world": game / "WORLD_VISION.md",
            "character": game / "CHARACTER.md",
            "initial": game / "CHARACTER_INITIAL_STATE.md",
        },
        "atlantis": {
            "direction": atl / "AUTHOR_DIRECTION.md",
            "world": atl / "01C_WORLD.md",
            "character": atl / "CHARACTER.md",
            "initial": atl / "CHARACTER_INITIAL_STATE.md",
        },
        "beast_h1": {
            "direction_text": GENERIC_MULTIWORLD_DIRECTION,
            "world": beast / "WORLD_VISION.md",
            "character": beast / "human_1" / "CHARACTER.md",
            "initial": beast / "human_1" / "INITIAL_CHARACTER_STATE.md",
        },
        "beast_h2": {
            "direction_text": GENERIC_MULTIWORLD_DIRECTION,
            "world": beast / "WORLD_VISION.md",
            "character": beast / "human_2" / "CHARACTER.md",
            "initial": beast / "human_2" / "INITIAL_CHARACTER_STATE.md",
        },
        "beast_h3": {
            "direction_text": GENERIC_MULTIWORLD_DIRECTION,
            "world": beast / "WORLD_VISION.md",
            "character": beast / "human_3" / "CHARACTER.md",
            "initial": beast / "human_3" / "INITIAL_CHARACTER_STATE.md",
        },
        "fallen_star_h1": {
            "direction_text": GENERIC_MULTIWORLD_DIRECTION,
            "world": star / "WORLD_VISION.md",
            "character": star / "human_1" / "CHARACTER.md",
            "initial": star / "human_1" / "INITIAL_CHARACTER_STATE.md",
        },
    }


def case_data(case: str) -> dict[str, str]:
    spec = case_defs()[case]
    direction = str(spec.get("direction_text") or "")
    if not direction:
        direction = read(Path(spec["direction"]))
    return {
        "mode": "idea",
        "creative_direction": direction,
        "world_vision": read(Path(spec["world"])),
        "character_card": read(Path(spec["character"])),
        "character_initial_state": read(Path(spec["initial"])),
        "book_content": "",
        "proposal_context": "",
    }


def retrieval_kwargs(d: dict[str, str]) -> dict[str, str]:
    return {
        "mode": d["mode"],
        "book_content": d["book_content"],
        "creative_direction": d["creative_direction"],
        "world_vision": d["world_vision"],
        "character_card": d["character_card"],
        "proposal_context": d["proposal_context"],
    }


def run_acp(
    prompt_path: Path,
    out_json: Path,
    *,
    model: str,
    effort: str = "high",
    timeout: int = 3600,
) -> dict:
    cp = subprocess.run(
        ["node", str(RUNNER), str(prompt_path), str(out_json), model, effort, str(ROOT), str(GBRAIN_ROOT)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
    )
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr[-5000:] or cp.stdout[-5000:])
    payload = json.loads(read(out_json))
    if not payload.get("ok"):
        raise RuntimeError(str(payload.get("error")))
    return payload


def search_case(case: str, query: str) -> dict:
    d = case_data(case)
    result = retrieve_gbrain(**retrieval_kwargs(d), query_override=query)
    return {
        "case": case,
        "query": query,
        "accepted_count": result.get("accepted_count", 0),
        "accepted": [
            {
                "slug": item["slug"],
                "type": item.get("type", ""),
                "score": item.get("score"),
                "abstract": item.get("abstract", ""),
                "transfer_boundary": item.get("transfer_boundary", ""),
            }
            for item in result.get("accepted", [])
        ],
    }


def get_case_card(case: str, slug: str) -> dict:
    d = case_data(case)
    mode = d["mode"]
    category = source_category(slug)
    if category not in MODE_ALLOWED_CATEGORIES[mode]:
        raise ValueError(f"{mode} does not allow category {category}")
    page = get_gbrain(slug)
    if not active_inspiration_allowed(page):
        raise ValueError("inactive inspiration")
    abstract, boundary = extract_abstract_content(page)
    if not abstract:
        raise ValueError("no source-blind abstract")
    constraints = extract_hard_constraints(
        d["creative_direction"], d["world_vision"], d["character_card"], d["proposal_context"], d["book_content"]
    )
    if _has_surface_conflict(abstract, constraints):
        raise ValueError("surface conflict with frozen constraints")
    return {"slug": slug, "type": category, "abstract": abstract, "transfer_boundary": boundary}


def navigator_prompt(case: str) -> str:
    d = case_data(case)
    brief = build_retrieval_brief(**retrieval_kwargs(d))
    return f"""# ROLE
你是 TGN GBrain Retrieval Navigator。你不写 Story Program，只为当前冻结 World + Human 主动找最多 3 条 source-blind craft。

# CURRENT TASK
{brief}

# ONLY ALLOWED SEARCH TOOL
在仓库根目录用 shell：
python "{SELF}" nav-search {case} "你的查询"
python "{SELF}" nav-get {case} "slug"

# RULES
- 做 2—4 次 search；最多 6 次 get。
- 第一跳从你判断的“这个具体 World + Human 现在最缺什么 Story Craft”出发，不照抄固定 query aliases。
- 至少一次后续 query 必须来自上一跳新发现的概念，形成真实 multi-hop。
- 只通过以上工具读 GBrain；不直接读原始 GBrain 文件或来源证据。
- GBrain 只是 inspiration，Frozen World / Power / Human 更高。
- 不为凑数选卡；最多 3 张，也可以 0 张。
- 特别注意：如果不同 Human 的私人欲望排序不同，不要把他们都推成成长最优、关系最优或道德最优路线。

# FINAL
只输出 JSON：
{{"searches":[{{"query":"...","why":"...","discovered":"..."}}],"selected_slugs":["..."],"synthesis":"这些卡具体改变哪种 Story 判断；若无增益写无增益"}}
"""


def parse_json_object(text: str) -> dict:
    a, b = text.find("{"), text.rfind("}")
    if a < 0 or b < a:
        raise ValueError("no JSON object")
    return json.loads(text[a : b + 1])


def nav_bundle(case: str, nav: dict) -> tuple[str, list[dict]]:
    slugs = nav.get("selected_slugs") or []
    if not isinstance(slugs, list) or len(slugs) > 3:
        raise ValueError("selected_slugs invalid")
    items = [get_case_card(case, str(slug)) for slug in slugs]
    blocks = []
    for i, item in enumerate(items, 1):
        blocks.append(
            f"### Inspiration {i}\nsource: {item['slug']}\ntype: {item['type']}\n\n"
            f"可用抽象：{item['abstract']}\n\n"
            f"使用边界：{item.get('transfer_boundary') or '只迁移抽象机制，不迁移来源故事表层。'}"
        )
    return "\n\n".join(blocks), items


def story_prompt(case: str, inspiration: str) -> str:
    d = case_data(case)
    return generate_split_prompt(
        mode="idea",
        creative_direction=d["creative_direction"],
        world_vision=d["world_vision"],
        character_card=d["character_card"],
        character_initial_state=d["character_initial_state"],
        creative_state={
            "world_vision": {"status": "author_approved"},
            "character_card": {"status": "author_approved"},
        },
        selected_references=[],
        gbrain_inspiration=inspiration,
    )


def prepare_case(case: str) -> dict:
    folder = OUT / case
    folder.mkdir(parents=True, exist_ok=True)
    d = case_data(case)
    fixed = retrieve_gbrain(**retrieval_kwargs(d))
    write(folder / "fixed_retrieval.json", json.dumps(fixed, ensure_ascii=False, indent=2))
    write(folder / "navigator_prompt.md", navigator_prompt(case))
    return {
        "case": case,
        "fixed_slugs": [x["slug"] for x in fixed.get("accepted", [])],
        "fixed_count": fixed.get("accepted_count", 0),
    }


def run_navigator(case: str) -> dict:
    folder = OUT / case
    payload = run_acp(folder / "navigator_prompt.md", folder / "navigator.json", model="gpt-5.6-sol")
    nav = parse_json_object(str(payload["text"]))
    bundle, items = nav_bundle(case, nav)
    write(folder / "navigator.md", str(payload["text"]))
    write(folder / "navigator_selection.json", json.dumps(nav, ensure_ascii=False, indent=2))
    write(folder / "navigator_items.json", json.dumps(items, ensure_ascii=False, indent=2))
    write(folder / "navigator_bundle.md", bundle)
    return {
        "case": case,
        "wall_seconds": payload.get("wall_seconds"),
        "selected_slugs": nav.get("selected_slugs", []),
        "searches": nav.get("searches", []),
    }


def prepare_story_prompts(case: str) -> None:
    folder = OUT / case
    fixed = json.loads(read(folder / "fixed_retrieval.json"))
    nav_bundle_text = read(folder / "navigator_bundle.md")
    write(folder / "prompt_A_fixed.md", story_prompt(case, str(fixed.get("result") or "")))
    write(folder / "prompt_B_navigator.md", story_prompt(case, nav_bundle_text))


def run_story(case: str, label: str) -> dict:
    folder = OUT / case
    prompt = folder / ("prompt_A_fixed.md" if label == "A" else "prompt_B_navigator.md")
    out_json = folder / ("A_terra.json" if label == "A" else "B_terra.json")
    payload = run_acp(prompt, out_json, model="gpt-5.6-terra")
    text = str(payload["text"])
    write(folder / ("A_terra.md" if label == "A" else "B_terra.md"), text)
    return {"case": case, "label": label, "wall_seconds": payload.get("wall_seconds"), "chars": len(text)}


def judge_prompt(case: str) -> str:
    folder = OUT / case
    x, y = read(folder / "A_terra.md"), read(folder / "B_terra.md")
    d = case_data(case)
    char = d["character_card"]
    world = d["world_vision"]
    return f"""# ROLE
你是 TGN Retrieval Structure 的匿名 A/B Judge。X/Y 使用同一 Frozen World / Human、同一 Terra-high Story 模型；只比较 Story Program 成品，不猜实验条件。

# FROZEN WORLD AUTHORITY
{world}

# FROZEN CHARACTER AUTHORITY
{char}

# CURRENT STORY AUTHORITY RULE
Story Program / Story Refresh 可以在 World / Human / Canon 尚未定义的过去空白中补重要配角旧史、隐藏关系、亲缘/师徒/竞争/共同失败/债/失约/上一代选择，并把 Human 已成立的家庭关系与 World Living Actors 接成过去因果。只要不改写已发生/公开 Canon、不偷答 AUTHOR OPEN、不把未来伪造成过去，这类 Relationship-History Backfill 是合法创作权；不得仅因它不在 Frozen Human 原文里就判 Authority 越界。

# JUDGMENT
判断哪个更值得继续写，重点：
1. 具体欲望、Living Actors、强幻想、冲突、获得与结算是否更有小说牵引。
2. Plot Engine 是否会变化而非换皮重复；对手/配角是否有自主行动。
3. Character-specific Choice：是否真由这个 Frozen Human 的私人欲望排序改变路线/对象/机会成本；不能统一成成长最优/关系最优/道德最优。
4. 高价值 reward 是否扩大 action space，并继续产生关系/敌人/身份/新选择，而非只加库存。
5. 长篇因果是否有 Book State Mutation / recontextualization，但不为“长篇感”机械召回或维护旧线。
6. Authority safety：不得重写 World/Power/Human、偷答未知、发明已发生未来。
7. Complexity tax：更多术语、线程、解释若没有改变行动因果，算负增益。

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
说明胜者是否保住这个 Human 的独特选择逻辑。
## Verdict
`PASS / DIRECTIONAL PASS / PARTIAL PASS / FAIL`

=== X ===
{x}

=== Y ===
{y}
"""


def run_judge(case: str) -> dict:
    folder = OUT / case
    p = folder / "judge_prompt.md"
    write(p, judge_prompt(case))
    payload = run_acp(p, folder / "judge.json", model="gpt-5.6-luna")
    text = str(payload["text"])
    write(folder / "JUDGE.md", text)
    return {"case": case, "wall_seconds": payload.get("wall_seconds"), "judge": text}


def run_screen() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cases = list(case_defs())
    prep = [prepare_case(c) for c in cases]
    write(OUT / "PREP.json", json.dumps(prep, ensure_ascii=False, indent=2))
    print("PREP", json.dumps(prep, ensure_ascii=False), flush=True)

    nav_rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(run_navigator, c): c for c in cases}
        for fut in concurrent.futures.as_completed(futures):
            row = fut.result()
            nav_rows.append(row)
            print("NAV", json.dumps(row, ensure_ascii=False), flush=True)
    write(OUT / "NAV_SUMMARY.json", json.dumps(nav_rows, ensure_ascii=False, indent=2))

    for c in cases:
        prepare_story_prompts(c)

    story_rows = []
    jobs = [(c, label) for c in cases for label in ("A", "B")]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(run_story, c, label): (c, label) for c, label in jobs}
        for fut in concurrent.futures.as_completed(futures):
            row = fut.result()
            story_rows.append(row)
            print("STORY", json.dumps(row, ensure_ascii=False), flush=True)
    write(OUT / "STORY_SUMMARY.json", json.dumps(story_rows, ensure_ascii=False, indent=2))


def run_judges() -> None:
    cases = list(case_defs())
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(run_judge, c): c for c in cases}
        for fut in concurrent.futures.as_completed(futures):
            row = fut.result()
            rows.append(row)
            print("JUDGE", row["case"], flush=True)
    write(OUT / "JUDGE_SUMMARY.json", json.dumps(rows, ensure_ascii=False, indent=2))


def main() -> None:
    if len(sys.argv) >= 4 and sys.argv[1] == "nav-search":
        print(json.dumps(search_case(sys.argv[2], sys.argv[3]), ensure_ascii=False, indent=2))
        return
    if len(sys.argv) >= 4 and sys.argv[1] == "nav-get":
        print(json.dumps(get_case_card(sys.argv[2], sys.argv[3]), ensure_ascii=False, indent=2))
        return
    action = sys.argv[1] if len(sys.argv) > 1 else "screen"
    if action == "screen":
        run_screen()
    elif action == "judges":
        run_judges()
    else:
        raise SystemExit("screen|judges|nav-search CASE QUERY|nav-get CASE SLUG")


if __name__ == "__main__":
    main()
