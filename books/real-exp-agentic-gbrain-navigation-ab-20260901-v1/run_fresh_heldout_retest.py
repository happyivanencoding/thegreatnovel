from __future__ import annotations

import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
GBRAIN_ROOT = Path(r"C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库")
EXP = ROOT / r"books\real-exp-agentic-gbrain-navigation-ab-20260901-v1"
OUT = EXP / "post-fix-rerun" / "fresh-heldout"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
SELF = Path(__file__).resolve()

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.gbrain import get_gbrain
from story_mvp.gbrain_retrieval import (
    MODE_ALLOWED_CATEGORIES,
    _has_surface_conflict,
    active_inspiration_allowed,
    extract_abstract_content,
    extract_hard_constraints,
    retrieve_gbrain,
    source_category,
)


DIRECTIONS = {
    "sky_chain": (
        "成熟中文男频长篇。世界母题只限定为：悬空群岛、危险天空、真正值得追逐的飞行/坠落/高空奇观。"
        "不要照搬已有天空岛模板；从普通人生活、力量、活着的人、值钱东西和远方欲望重新发明。"
    ),
    "world_tree": (
        "成熟中文男频长篇。世界母题只限定为：人类与异族生活在一株不可测量的巨型活树内部与枝冠，"
        "树本身会生长、脱皮、结果、腐坏并改变道路。不要把它写成资源治理题，要有身体、异兽、奇物、探险和强者幻想。"
    ),
    "time_tide": (
        "成熟中文男频长篇。世界母题只限定为：古战场与城市会周期性遭遇可观察的时间潮汐，"
        "某些地点会短暂重现过去动作、伤痕或未完成事件，但世界仍是可生活的实体世界。"
        "重点是冒险、力量、遗物、人物旧选择与未知，不写时间管理或程序化解谜。"
    ),
    "star_ice": (
        "成熟中文男频长篇。世界母题只限定为：极寒夜海、漂移冰陆与会坠入海中的星体残骸。"
        "海下与冰层上必须都值得探索；不要写成航运管理，重点是异兽、星冰、身体变化、兵器、远方和活着的人。"
    ),
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_acp(prompt_path: Path, out_json: Path, *, model: str, effort: str = "high", timeout: int = 3600) -> dict:
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


def world_prompt(case: str) -> str:
    return f"""# ROLE
你是 TGN protagonist-blind World Vision Agent。生成一个全新的实验 Frozen World Authority；你完全不知道未来主角是谁，也不能为任何主角留钥匙孔。

# AUTHOR DIRECTION
{DIRECTIONS[case]}

# HARD REQUIREMENTS
- 只输出 Markdown World Vision，不写 Story Program，不写主角。
- 世界必须能独立运行：至少 5 个 Living Actors / 生物 / 小群体，各自明确“想要什么 → 马上准备做什么 → 主角永不存在也会改变谁/物/地点”。
- 少数 Living Actors 可以在故事开始前彼此活过真实关系史；旧选择要在今天留下债、遗物、误解、空位、身份或路线后果。
- 力量体系必须 Small Grammar / Large Variation，用普通话 1—3 句讲清底层；随后用身体、兵器、异兽、地点、环境、组合制造多样性。
- 必须冻结唯一精确公开主尺：连续数字或大境界+数字子级；给出 0/低阶/中阶/高阶/顶层的可感 benchmark。它是 Reader Ruler，不是总战力分。
- 明确普通人的生活、失败形状、上升入口、社会价格，但不要把治理/维护/资源分配写成故事发动机。
- 至少 6 个真正值得进去看的地点/奇观/未知；至少 5 种具体高价值对象（兵器、身体变化、异兽、遗物、传承、入口等可混合）。
- 至少一个强世界规则必须改变某个具体人物的生活或关系因果，不只服务战斗谜题。
- 允许 0—1 条成熟 Secondary Fantasy Road；不够好就不要造。
- AUTHOR OPEN 的谜团保持未知，不给隐藏真相。

# REQUIRED HEADINGS
# PROTAGONIST-BLIND WORLD VISION
## 普通人的生活与上升
## 力量体系与正常值
### 精确力量主尺｜Frozen Grammar
## 社会现实与身份
## 世界里真正值钱、值得想要的东西
## 世界正在发生的大事
## 已经活过的人与关系史
## 值得进入的地点、奇观与未知
## 世界知识边界

要求大胆、具体、reader-facing；不要解释你如何设计。
"""


def character_prompt(case: str) -> str:
    world = read(OUT / case / "WORLD_VISION.md")
    appetite_seed = {
        "sky_chain": "爱出风头、喜欢漂亮昂贵的飞行装备、享受被人记住，也真想拥有随时离开的自由；有一个会改变其选择的具体家人或旧关系。",
        "world_tree": "对稀奇活物与身体变化有强烈占有欲，喜欢舒服生活和钱，不天然愿意负责别人；又有一段具体亲密关系会让其偶尔放弃最值钱路线。",
        "time_tide": "非常好胜，讨厌别人替自己定义过去，喜欢公开胜负和稀有旧物；会被某个具体旧人/家族关系刺中，但不默认道德最优。",
        "star_ice": "好奇、虚荣、喜欢漂亮器物和远行，也贪图温暖舒适与钱；面对真正想要的东西会冒险，但不是无脑探险狂。",
    }[case]
    return f"""# ROLE
你是 TGN Split Character Fixture Agent。World 已冻结；你不能修改 World，也不能设计 Story Program。
为这个全新 World 生成一个可用于 Story Program A/B 的 Frozen Character Authority：Power 与 Human 独立成立，不做后验主题化调和。

# FROZEN WORLD
{world}

# HUMAN APPETITE SEED
{appetite_seed}

# POWER REQUIREMENTS
- 生成一个直接、强、可观察的 Core Power Asymmetry；必须明显值得同层人羡慕，且不是工作流/分析/管理能力。
- 它可以与世界正常力量不同源；World Normal 只是比较尺。
- 给出 Trigger / Observable Effect / Permanent Boundary / T0 precise position。
- 不把它做成万能；但不要用对称代价把强度抵消掉。

# HUMAN REQUIREMENTS
- 至少 4 个互相竞争的私人动机：钱、胜负、审美、身体吸引、舒服生活、自由、面子、好奇、偏心、具体关系等自由组合。
- 必须存在至少两样都真有价值、但不能总是同时完整取得的东西。
- Behavior Signature 是跨场景选择偏向，不是固定口癖/动作。
- 至少 2 个具体关系原点，其中至少 1 个会真实改变选择；不要靠新造惨死/背叛来证明人格。
- 初始位置必须在 World 主尺上给出精确数字，并符合普通人/年轻人可达范围。

# OUTPUT
只输出一个 JSON object，不要 markdown fence：
{{
  "character_markdown": "# CHARACTER\\n\\n## POWER CORE｜Frozen Authority\\n...\\n\\n## HUMAN CORE｜Frozen Authority\\n...\\n\\n### 持续牵引与互相竞争的动机\\n...\\n\\n### Behavior Signature\\n...\\n\\n### 重要关系原点\\n...\\n\\n## Composition Boundary\\n...",
  "initial_state_markdown": "# CHARACTER INITIAL STATE\\n\\n## Power / Capability\\nCurrent Power Position: ...\\n...\\n\\n## Life / Possession / Relationship\\n..."
}}
"""


def parse_json_object(text: str) -> dict:
    a, b = text.find("{"), text.rfind("}")
    if a < 0 or b < a:
        raise ValueError("no JSON object")
    return json.loads(text[a : b + 1])


def forge_world(case: str) -> dict:
    folder = OUT / case
    write(folder / "AUTHOR_DIRECTION.md", DIRECTIONS[case])
    p = folder / "forge_world_prompt.md"
    write(p, world_prompt(case))
    payload = run_acp(p, folder / "forge_world.json", model="gpt-5.6-luna")
    text = str(payload["text"])
    write(folder / "WORLD_VISION.md", text)
    return {"case": case, "world_wall": payload.get("wall_seconds"), "world_chars": len(text)}


def forge_character(case: str) -> dict:
    folder = OUT / case
    p = folder / "forge_character_prompt.md"
    write(p, character_prompt(case))
    payload = run_acp(p, folder / "forge_character.json", model="gpt-5.6-luna")
    obj = parse_json_object(str(payload["text"]))
    character = str(obj["character_markdown"])
    initial = str(obj["initial_state_markdown"])
    write(folder / "CHARACTER.md", character)
    write(folder / "CHARACTER_INITIAL_STATE.md", initial)
    return {"case": case, "character_wall": payload.get("wall_seconds"), "character_chars": len(character)}


def forge() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(forge_world, case): case for case in DIRECTIONS}
        for fut in concurrent.futures.as_completed(futures):
            row = fut.result(); rows.append(row); print("WORLD", json.dumps(row, ensure_ascii=False), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(forge_character, case): case for case in DIRECTIONS}
        for fut in concurrent.futures.as_completed(futures):
            row = fut.result(); rows.append(row); print("CHAR", json.dumps(row, ensure_ascii=False), flush=True)
    write(OUT / "FORGE_SUMMARY.json", json.dumps(rows, ensure_ascii=False, indent=2))


def case_data(case: str) -> dict[str, str]:
    folder = OUT / case
    return {
        "mode": "idea",
        "creative_direction": DIRECTIONS[case],
        "world_vision": read(folder / "WORLD_VISION.md"),
        "character_card": read(folder / "CHARACTER.md"),
        "character_initial_state": read(folder / "CHARACTER_INITIAL_STATE.md"),
        "book_content": "",
        "proposal_context": "",
    }


def retrieval_kwargs(d: dict[str, str]) -> dict[str, str]:
    return {
        "mode": "idea",
        "book_content": "",
        "creative_direction": d["creative_direction"],
        "world_vision": d["world_vision"],
        "character_card": d["character_card"],
        "proposal_context": "",
    }


def nav_search(case: str, query: str) -> dict:
    d = case_data(case)
    result = retrieve_gbrain(**retrieval_kwargs(d), query_override=query)
    return {
        "query": query,
        "accepted": [
            {"slug": x["slug"], "type": x.get("type", ""), "score": x.get("score"), "abstract": x.get("abstract", ""), "transfer_boundary": x.get("transfer_boundary", "")}
            for x in result.get("accepted", [])
        ],
    }


def nav_get(case: str, slug: str) -> dict:
    d = case_data(case)
    category = source_category(slug)
    if category not in MODE_ALLOWED_CATEGORIES["idea"]:
        raise ValueError("category not allowed")
    page = get_gbrain(slug)
    if not active_inspiration_allowed(page):
        raise ValueError("inactive inspiration")
    abstract, boundary = extract_abstract_content(page)
    constraints = extract_hard_constraints(d["creative_direction"], d["world_vision"], d["character_card"])
    if not abstract or _has_surface_conflict(abstract, constraints):
        raise ValueError("card unavailable for this frozen authority")
    return {"slug": slug, "type": category, "abstract": abstract, "transfer_boundary": boundary}


def navigator_prompt(case: str) -> str:
    d = case_data(case)
    return f"""# ROLE
你是 TGN GBrain Retrieval Navigator。你不写 Story Program，只为当前全新 Frozen World + Human 主动找最多 3 条 source-blind craft。

# AUTHOR DIRECTION
{d['creative_direction']}

# FROZEN WORLD
{d['world_vision']}

# FROZEN CHARACTER
{d['character_card']}

# ONLY ALLOWED SEARCH TOOL
在仓库根目录用 shell：
python "{SELF}" nav-search {case} "你的查询"
python "{SELF}" nav-get {case} "slug"

# RULES
- 做 2—4 次 search；最多 6 次 get。
- 第一跳从这个具体 World + Human 真正缺什么 Story Craft 出发，不照抄固定 query aliases。
- 至少一次后续 query 必须来自上一跳发现的新概念，形成真实 multi-hop。
- 只通过上面工具读 GBrain；不得直接读 GBrain 文件/source evidence。
- Frozen World / Power / Human 高于 GBrain；不为 craft 发明 World 事实。
- 保留这个 Human 的私人欲望排序；不要统一成成长最优/关系最优/道德最优。
- 最多 3 张，也可以少于 3 张。

# FINAL
只输出 JSON：
{{"searches":[{{"query":"...","why":"...","discovered":"..."}}],"selected_slugs":["..."],"synthesis":"..."}}
"""


def nav_bundle(case: str, nav: dict) -> tuple[str, list[dict]]:
    slugs = nav.get("selected_slugs") or []
    if not isinstance(slugs, list) or len(slugs) > 3:
        raise ValueError("bad selected_slugs")
    items = [nav_get(case, str(s)) for s in slugs]
    blocks = []
    for i, item in enumerate(items, 1):
        blocks.append(
            f"### Inspiration {i}\nsource: {item['slug']}\ntype: {item['type']}\n\n可用抽象：{item['abstract']}\n\n使用边界：{item.get('transfer_boundary') or '只迁移抽象机制，不迁移来源故事表层。'}"
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
        creative_state={"world_vision": {"status": "author_approved"}, "character_card": {"status": "author_approved"}},
        selected_references=[],
        gbrain_inspiration=inspiration,
    )


def prepare(case: str) -> dict:
    folder = OUT / case
    d = case_data(case)
    fixed = retrieve_gbrain(**retrieval_kwargs(d))
    write(folder / "fixed_retrieval.json", json.dumps(fixed, ensure_ascii=False, indent=2))
    write(folder / "navigator_prompt.md", navigator_prompt(case))
    return {"case": case, "fixed_slugs": [x["slug"] for x in fixed.get("accepted", [])]}


def run_nav(case: str) -> dict:
    folder = OUT / case
    payload = run_acp(folder / "navigator_prompt.md", folder / "navigator.json", model="gpt-5.6-sol")
    nav = parse_json_object(str(payload["text"]))
    bundle, items = nav_bundle(case, nav)
    write(folder / "navigator_selection.json", json.dumps(nav, ensure_ascii=False, indent=2))
    write(folder / "navigator_bundle.md", bundle)
    write(folder / "navigator_items.json", json.dumps(items, ensure_ascii=False, indent=2))
    return {"case": case, "wall_seconds": payload.get("wall_seconds"), "selected_slugs": nav.get("selected_slugs", [])}


def run_story(case: str, label: str) -> dict:
    folder = OUT / case
    fixed = json.loads(read(folder / "fixed_retrieval.json"))
    inspiration = str(fixed.get("result") or "") if label == "A" else read(folder / "navigator_bundle.md")
    p = folder / f"prompt_{label}.md"
    write(p, story_prompt(case, inspiration))
    payload = run_acp(p, folder / f"{label}_terra.json", model="gpt-5.6-terra")
    text = str(payload["text"])
    write(folder / f"{label}_terra.md", text)
    return {"case": case, "label": label, "wall_seconds": payload.get("wall_seconds"), "chars": len(text)}


def ab() -> None:
    prep = [prepare(c) for c in DIRECTIONS]
    print("PREP", json.dumps(prep, ensure_ascii=False), flush=True)
    nav_rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(run_nav, c): c for c in DIRECTIONS}
        for fut in concurrent.futures.as_completed(futures):
            row = fut.result(); nav_rows.append(row); print("NAV", json.dumps(row, ensure_ascii=False), flush=True)
    story_rows = []
    jobs = [(c, label) for c in DIRECTIONS for label in ("A", "B")]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(run_story, c, label): (c, label) for c, label in jobs}
        for fut in concurrent.futures.as_completed(futures):
            row = fut.result(); story_rows.append(row); print("STORY", json.dumps(row, ensure_ascii=False), flush=True)
    write(OUT / "AB_SUMMARY.json", json.dumps({"prep": prep, "nav": nav_rows, "story": story_rows}, ensure_ascii=False, indent=2))


def judge_prompt(case: str) -> str:
    folder = OUT / case
    d = case_data(case)
    a, b = read(folder / "A_terra.md"), read(folder / "B_terra.md")
    return f"""# ROLE
你是 TGN 全新 held-out 世界的匿名 A/B Judge。X/Y 使用同一 Frozen World / Power / Human 与同一 Terra-high Story 模型；只比较 Story Program 成品。

# FROZEN WORLD
{d['world_vision']}

# FROZEN CHARACTER
{d['character_card']}

# CURRENT STORY AUTHORITY RULE
Story Program 可以在尚未定义的过去空白中合法 backfill 重要配角旧史/关系史；不能改写已冻结事实、偷答 AUTHOR OPEN、或把未来伪造成过去。
**本实验没有预先冻结 Story Program、RSE、阶段顺序或候选奖励。X/Y 都是在同一 Frozen World / Power / Human 之上独立提出候选 Story Program。不得把 X 自己新写的 RSE、旧史、阶段、奖励或 Handoff 当成 Authority 去判 Y“改写冻结内容”，反之亦然。只能对照上面的 Frozen World / Character 判断 Authority。**

# JUDGMENT
比较：当前 Horizon 阅读牵引、Living Actors、Human-specific choice 与真实机会成本、Plot Engine 变化、高价值获得、Book State Mutation、历史重释、力量尺纵深、是否过早耗尽世界、Authority safety、complexity tax。
奖励更多本身不是缺陷；只有因果/Authority/牺牲被抹平才是硬问题。

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

=== X ===
{a}

=== Y ===
{b}
"""


def run_judge(case: str) -> dict:
    folder = OUT / case
    p = folder / "judge_prompt.md"
    write(p, judge_prompt(case))
    payload = run_acp(p, folder / "judge.json", model="gpt-5.6-luna")
    text = str(payload["text"])
    write(folder / "JUDGE.md", text)
    return {"case": case, "wall_seconds": payload.get("wall_seconds"), "judge": text}


def judges() -> None:
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {ex.submit(run_judge, c): c for c in DIRECTIONS}
        for fut in concurrent.futures.as_completed(futures):
            row = fut.result(); rows.append(row); print("JUDGE", row["case"], flush=True)
    write(OUT / "JUDGE_SUMMARY.json", json.dumps(rows, ensure_ascii=False, indent=2))


def main() -> None:
    if len(sys.argv) >= 4 and sys.argv[1] == "nav-search":
        print(json.dumps(nav_search(sys.argv[2], sys.argv[3]), ensure_ascii=False, indent=2)); return
    if len(sys.argv) >= 4 and sys.argv[1] == "nav-get":
        print(json.dumps(nav_get(sys.argv[2], sys.argv[3]), ensure_ascii=False, indent=2)); return
    action = sys.argv[1] if len(sys.argv) > 1 else "forge"
    if action == "forge": forge()
    elif action == "ab": ab()
    elif action == "judges": judges()
    else: raise SystemExit("forge|ab|judges|nav-search CASE QUERY|nav-get CASE SLUG")


if __name__ == "__main__":
    main()
