from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
RUNNER = ROOT / "temps" / "acp_readonly_runner.mjs"
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.chapter_context import (
    parse_chapter_plan_fields,
    project_current_long_block_for_chapter,
)
from story_mvp.hybrid_runtime import extract_primary_draft
from story_mvp.progressive_canon import (
    MysteryThread,
    adopt_hidden_fixed_point,
    advance_after_reveal,
    build_canonization_compiler_prompt,
    build_decision_surface_prompt,
    build_reframe_prompt,
    compile_runtime_mystery_projection,
    extract_reframe_candidates,
    parse_compiler_verdict,
    parse_decision_surface,
    parse_reveal_contract,
    render_planning_projection,
    render_thread,
)
from story_mvp.prompts import generate_prompt, parse_canon_memory
from story_mvp.storage import (
    apply_state_delta_to_book,
    compose_book_content,
    default_book_content,
    parse_book_sections,
)


CREATIVE_DIRECTION = """成熟中文男频玄幻悬疑成长长篇。主角的私人欲望、占有、胜负和具体关系必须真正改变路线；长期 Mystery 允许作者自己暂时不知道答案。每次 Reveal 只回答当前必须的一层，并立刻改变下一步行动、敌我、物品价值或关系，不用 lore 说明替代故事。"""

WORLD = """# PROTAGONIST-BLIND WORLD VISION

听雨城建在黑岩丘陵之间，常年阴雨，城下有许多旧井、废渠和早于现王朝的石层。城市本身不是围绕任何未来主角建立的。

## 普通人的生活与上升
普通人靠铸刀、药草、运盐、旧物交易和城外雨兽狩猎生活。想离开底层，最常见的路是进入护街队、雨猎队、兵坊或商行；有钱人会购买纹师教习和更好的兵器。

## 力量体系与正常值
人以身体承载“雨纹”，能强化速度、力量、感知或兵器控制。能力仍服从具体身体、兵器和经验，不是单一战力公式。

### 精确力量主尺｜Frozen Grammar
主尺类型：连续数字
主尺名称：纹阶
精确位置格式：纹阶{N}
数字精度规则：1—36
当前可见范围：1—36
当前大档位：1—6普通成年练家；7—12护街/雨猎骨干；13—20地方强者；21—28城级名手；29—36听雨城顶层。

普通成年练家多在纹阶2—5；护街队骨干约7—10；能独自猎杀大型雨兽通常要12以上；城里最强的几个人在30上下。

## 社会现实与身份
城主府、三大兵坊、旧物市和护街队彼此有利益往来，但没有谁完全控制听雨城。旧井区因多次坍塌被封了一半，仍住着大量穷人和旧物贩子。

## 世界里真正值钱、值得想要的东西
高阶雨纹术、能承载多重纹路的兵器、雨兽骨核、旧朝兵库钥物、完整旧井地图都很值钱。真正能证明来源的古物会被兵坊、收藏家和城主府同时出高价。

## 世界正在发生的大事
一场持续三个月的异常长雨让旧井区不断塌陷；三大兵坊正在争一批从地下冲出的旧朝兵器；城主府准备彻底封死最深的几口井。

## 值得进入的地点、奇观与未知
旧井区深处有一口被陆家旧院墙体包住的“回影井”。它偶尔会吐出无法解释的旧物，但几十年来没有形成可靠规律，也没有人知道井下究竟通向哪里。

## 世界知识边界
普通人知道旧井危险、旧朝遗物值钱、地下有早于听雨城的石层；不知道任何所谓平行城市、时间回流、复制世界或幕后系统。
当前没人能完整解释的事实包括：回影井为什么偶尔吐出与城中物件高度相似的东西；这些东西是否真有共同来源；井下最深处是否存在可通行空间。
"""

CHAR_A = """# CHARACTER

## POWER CORE
主角陆昭，18岁，当前纹阶4。
开局精确力量位置｜主尺：纹阶｜精确位置：4
核心能力“钉影”：一天最多三次，他可以把自己亲眼看见的一个移动物体的影子钉在地面约两息；目标若力量远高于他会迅速挣脱。它能制造抢先手、夺物和逃跑机会，但不能读取记忆、判断真伪或解释回影井。

## HUMAN CORE
陆昭从旧物市和兵坊废料里长大，穷过，因此对“真正属于自己的值钱东西”有明显占有欲。他好胜、爱面子、喜欢赌别人不敢赌的高赔率机会；看到稀有物第一反应是它值多少钱、能不能先归自己，而不是替世界查明真相。
他对失踪两年的哥哥陆峥仍有复杂牵引：嘴上认定人已经没了，但任何明确属于哥哥的东西都会让他改变一次纯收益最优解。
稳定选择偏向：钱/独占稀有物 > 赢过看不起自己的人 > 好奇 > 普通安全；但哥哥相关事实可以突然提高他的风险阈值。

## Composition Boundary
职业经验只能帮助他认旧物、估价和在市场里谈价，不能把故事变成鉴定流程或档案工作。
"""

CHAR_B = """# CHARACTER

## POWER CORE
主角陆昭，18岁，当前纹阶4。
开局精确力量位置｜主尺：纹阶｜精确位置：4
核心能力“钉影”：一天最多三次，他可以把自己亲眼看见的一个移动物体的影子钉在地面约两息；目标若力量远高于他会迅速挣脱。它能制造抢先手、夺物和逃跑机会，但不能读取记忆、判断真伪或解释回影井。

## HUMAN CORE
陆昭同样在旧物市长大，但两年前哥哥失踪后，他实际上承担起照顾十二岁妹妹陆葵的生活。钱很重要，却主要意味着妹妹可以离开旧井区；他最厌恶把不可控危险带回家。
他仍然好胜，也想知道哥哥下落，但面对“高价值未知物”和“妹妹立刻暴露于风险”时，会先牺牲先手和钱，把妹妹从风险里移走，再回来追答案。
稳定选择偏向：妹妹安全 > 保住自己的选择权 > 钱 > 赢 > 好奇。哥哥线能让他冒险，但不会让他把妹妹当代价。

## Composition Boundary
保护具体家人不等于公共责任；他不会因此自动承担整座城的安全或最优调查路线。
"""

BASE_CURRENT = """# CURRENT CHARACTER
Compiled Through Chapter: {chapter}
主角：陆昭
Current Power Position｜主尺：纹阶｜精确位置：纹阶4
当前 Power：钉影，一天最多三次，目标明显强于自己时只能短暂生效。
{human}

## Current Canon Snapshot
{canon}
"""

INITIAL_THREAD = MysteryThread(
    mystery_id="M-WELL-01",
    question="回影井为什么会吐出与城中现存物件高度同源、却经历不同的第二份实物？",
    state="OPEN",
    known_anchors="""- 回影井几十年来偶尔吐出无法解释的旧物，但从未有可靠来源答案。
- 听雨城公共知识不存在平行城市、时间回流或复制世界等定论。
- 陆昭的哥哥陆峥两年前失踪，与井是否有关尚无证据。""",
    decision_trigger="只有下一段具体行动必须依赖这些物件的来源类别时，才决定最小一层；否则继续未知。",
    remains_unknown="物件来自哪里；是否存在另一处现实来源；两份物件是什么关系；陆峥是否与井有关；井为什么产生这种现象。",
    route="story",
)

APPROVED = {
    "world_vision": {"status": "author_approved"},
    "character_card": {"status": "author_approved"},
    "proposal": {"status": "author_approved"},
}

PREVIOUS_STORY = """# STORY PROGRAM
## 当前 Re-Collision
陆昭仍住在听雨城旧井区，以旧物交易和小规模雨猎赚钱。回影井只是一个已知但未解释的异常，当前故事只允许通过真实物件增加证据，不预设来源答案。
## 当前 Power / Human / World 的长期张力
陆昭想把值钱的异常物先变成自己的；世界各方会按物品价值而非主角命运行动。
## 本阶段核心情节发动机与变化后的主要 Reading Question
如果井里吐出一件不可能存在的第二份实物，陆昭会先抢到、保住、卖掉还是追来源？
## 全书成长与核心幻想兑现脊柱（只写从当前点向前仍成立的部分）
纹阶成长与钉影继续独立存在；Mystery 不替代力量成长。
## 不可替代的人与关系
哥哥陆峥的失踪只在出现具体证据时改变陆昭选择；妹妹陆葵按 Human Authority 生效。
## 未来大型阶段
先让回影井吐出第一件足够具体的异常实物，并让它改变现实利益。
## World Horizon Handoff
NOT YET
## 仍值得追的旧承诺与新欲望
回影井来源保持未知。
"""


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def run_acp(prompt_text: str, directory: Path, name: str, *, model: str, effort: str) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    prompt_path = directory / f"{name}_PROMPT.md"
    json_path = directory / f"{name}_ACP.json"
    md_path = directory / f"{name}.md"
    if json_path.is_file() and md_path.is_file():
        try:
            cached = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cached = {}
        prompt_matches = prompt_path.is_file() and prompt_path.read_text(encoding="utf-8") == prompt_text
        if prompt_matches and cached.get("ok") and cached.get("model") == model and cached.get("effort") == effort:
            return {
                "text": md_path.read_text(encoding="utf-8").strip(),
                "wall": 0.0,
                "agent_wall": cached.get("wall_seconds"),
                "usage": (cached.get("result") or {}).get("usage") or {},
                "model": model,
                "effort": effort,
                "reused": True,
            }
    prompt_path.write_text(prompt_text, encoding="utf-8")
    started = time.perf_counter()
    proc = subprocess.run(
        ["node", str(RUNNER), str(prompt_path), str(json_path), model, effort, name],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ACP {name} failed: {proc.stderr[-3000:]}\n{proc.stdout[-3000:]}")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if not payload.get("ok"):
        raise RuntimeError(f"ACP {name} failed: {payload.get('error')}")
    text = str(payload.get("text", "")).strip()
    md_path.write_text(text + "\n", encoding="utf-8")
    return {
        "text": text,
        "wall": round(time.perf_counter() - started, 3),
        "agent_wall": payload.get("wall_seconds"),
        "usage": (payload.get("result") or {}).get("usage") or {},
        "model": model,
        "effort": effort,
    }


def initial_status() -> str:
    return """当前已完成第0章。

## ACTIVE SCENE STATE
当前地点：听雨城陆家旧院，回影井就在封墙后。
在场：陆昭；陆葵是否在场由 Human 版本决定。
当前主动目标：靠旧物生意和雨猎赚钱，不主动替任何势力调查回影井。

## PERSISTENT CANON
### Power / Capability
Current Power Position｜主尺：纹阶｜精确位置：纹阶4
钉影：一天最多三次，可短暂钉住一个移动物体的影子；明显高阶目标会快速挣脱。
### Knowledge / Enemy State
回影井偶尔吐出异常旧物，但来源未知；陆峥两年前失踪，是否与井有关未知。
### Tracked Assets
陆昭自己的黑柄短刀｜陆昭｜腰间｜完好｜一直由本人持有

## RECENT SUMMARIES
当前尚无已完成正文或已批准章节摘要。

## OPEN PROMISES
- 回影井为何会吐出异常旧物仍未知。
- 陆峥失踪原因仍未知。

## AUTHOR NOTES
（无）"""


def make_base_book() -> str:
    sections = parse_book_sections(default_book_content())
    sections["status"] = initial_status()
    return compose_book_content(sections)


def current_character(book: str, char: str, chapter: int) -> str:
    status = parse_book_sections(book)["status"]
    human = re.search(r"(?ms)^## HUMAN CORE\s*(.*?)(?=^## Composition Boundary|\Z)", char)
    return BASE_CURRENT.format(
        chapter=chapter,
        human=(human.group(1).strip() if human else ""),
        canon=status,
    )


def recent_summaries(book: str) -> str:
    memory = parse_canon_memory(parse_book_sections(book)["status"])
    return memory.get("recent_summaries", "")


def extract_chapter_plan(outline_book: str, chapter: int) -> str:
    small = parse_book_sections(outline_book)["small_plan"]
    headings = list(re.finditer(r"(?m)^##\s+第\s*(\d+)\s*章(?:[：:].*)?$", small))
    for index, match in enumerate(headings):
        if int(match.group(1)) != chapter:
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(small)
        block = small[match.start():end].strip()
        if re.search(r"(?m)^##\s+第\s*\d+\s*章", block[len(match.group(0)):]):
            raise ValueError(f"第{chapter}章提取结果错误包含其它章节")
        return block
    raise ValueError(f"Outline 缺少第{chapter}章计划")


def strip_reveal_contract(story: str) -> str:
    return re.sub(r"(?ms)^# MYSTERY REVEAL CONTRACT\s*$.*\Z", "", story).strip()


def story_refresh_prompt(
    *,
    book: str,
    char: str,
    current: str,
    previous_story: str,
    thread: MysteryThread,
    reveal_chapter: int | None,
) -> str:
    base = generate_split_prompt(
        mode="story_refresh",
        book_content=book,
        creative_direction=CREATIVE_DIRECTION,
        world_vision=WORLD,
        character_card=char,
        current_character=current,
        creative_state=APPROVED,
        proposal_context=previous_story,
        selected_references=[],
        gbrain_inspiration="",
        effective_from_chapter=max(1, int(re.search(r"Compiled Through Chapter:\s*(\d+)", current).group(1)) + 1),
    )
    control = render_planning_projection(thread)
    if thread.state == "OPEN":
        extra = """# EXPERIMENTAL AUTHOR MYSTERY CONTROL｜PLANNING ONLY
{control}

本轮不得替作者决定答案。正常输出 Story Program；不要输出 `# MYSTERY REVEAL CONTRACT`。可以制造新的可观察证据、利益冲突和更具体问题，但不能把任何来源解释升级为事实。
""".format(control=control)
    else:
        assert reveal_chapter is not None
        extra = f"""# EXPERIMENTAL AUTHOR MYSTERY CONTROL｜PLANNING ONLY
{control}

这是 planning-only Hidden Truth。正常 Story Program 可以围绕它安排现实利益、证据和人物选择，但**不得在普通 Story Program 段落直接写出 Fixed Point 的答案**。只在全文最后额外输出下面唯一的 reader-facing transport：

# MYSTERY REVEAL CONTRACT
Mystery ID: {thread.mystery_id}
Reveal Chapter: {reveal_chapter}
Event Atom: 用一句具体现场事件，让人物/读者在第{reveal_chapter}章亲眼确认 Reveal Boundary 允许的这一层；不能靠旁白宣布答案。
State Residue: 只写事件发生后可以进入 Canon 的 1—2 个确定事实，不越过 Still Open。
Reader Anchors: 1—4 个 reader-safe 专名/物件/地点/短事实，用 `；` 分隔。
Still Open After Reveal: 明确列出揭晓后仍未回答的更深问题。

Contract 之外不要写原始 Fixed Point 答案；Contract 本身也只能写 Reveal Boundary 允许的 reader-facing 事实，不写更深原因。
"""
    return base + "\n\n" + extra


def outline_prompt(*, book: str, char: str, current: str, story: str, reveal_id: str = "", reveal_chapter: int = 0) -> str:
    safe_story = strip_reveal_contract(story)
    base = generate_split_prompt(
        mode="outline",
        book_content=book,
        creative_direction=CREATIVE_DIRECTION,
        world_vision=WORLD,
        character_card=char,
        current_character=current,
        creative_state=APPROVED,
        proposal_context=safe_story,
        selected_references=[],
        gbrain_inspiration="",
    )
    base += "\n# Approval Status｜already satisfied by production code\nWorld Vision、Character Authority、Story Program 均已由作者批准。CURRENT CHARACTER 是由已批准 Character Authority + 已发生 Canon 确定性编译出的 forward snapshot，不是新的 Character proposal，不产生第二次批准点。请直接执行 Outline 编译，不再次请求作者批准。\n"
    if not reveal_id:
        return base + "\n\n# Mystery Scheduling Boundary\n当前没有已批准 Reveal Event；所有 Mystery 答案继续按 Story Program 未知边界处理。\n"
    return base + f"""

# Mystery Scheduling Boundary｜只排时机，不提供答案
- 在 Future 10 的**第{reveal_chapter}章** `叙事功能` 中逐字加入标记 `[MYSTERY-REVEAL:{reveal_id}]`。
- 标记本身不包含答案。第{reveal_chapter}章之前的 Future 10、Reader Release Map 和覆盖前置章节的中期剧情块不得写这个 Reveal 的 State Residue、答案或等价解释。
- 不要为了规划完整而猜 Reveal 内容；真实 Event Atom 由 deterministic runtime transport 在 Reveal 当章注入。
"""


def inject_reveal_into_plan(plan: str, reveal) -> str:
    marker = f"[MYSTERY-REVEAL:{reveal.mystery_id}]"
    if marker not in plan:
        raise ValueError(f"Reveal 章计划缺少 scheduling marker：{marker}")
    values = parse_chapter_plan_fields(plan)
    needed = ("具体剧情", "结果 / 状态变化", "叙事功能", "结尾推动")
    missing = [key for key in needed if not values.get(key)]
    if missing:
        raise ValueError("Reveal 章计划缺少字段：" + "、".join(missing))
    values["具体剧情"] = values["具体剧情"].rstrip() + " " + reveal.event_atom
    values["结果 / 状态变化"] = (
        values["结果 / 状态变化"].rstrip()
        + " "
        + reveal.state_residue
        + " 更深未知继续保留："
        + reveal.still_open_after_reveal
    )
    return "\n".join(
        [
            re.match(r"^##.*$", plan.strip().splitlines()[0]).group(0),
            f"具体剧情：{values['具体剧情']}",
            f"结果 / 状态变化：{values['结果 / 状态变化']}",
            f"叙事功能：{values['叙事功能']}",
            f"结尾推动：{values['结尾推动']}",
        ]
    )


def make_runtime_plan(outline_book: str, chapter: int, reveal=None) -> tuple[str, str]:
    sections = parse_book_sections(outline_book)
    long_plan = sections["long_plan"]
    plan = extract_chapter_plan(outline_book, chapter)
    if reveal is not None and chapter == reveal.reveal_chapter:
        plan = inject_reveal_into_plan(plan, reveal)
    return long_plan, plan


def chapter_chain(
    *,
    chapter: int,
    runtime_book: str,
    outline_book: str,
    char: str,
    previous_prose: str,
    reveal=None,
    directory: Path,
) -> dict:
    long_plan, plan = make_runtime_plan(outline_book, chapter, reveal)
    recents = recent_summaries(runtime_book)

    director_prompt = generate_prompt(
        mode="director",
        template="",
        book_content=runtime_book,
        creative_direction=CREATIVE_DIRECTION,
        world_vision=WORLD,
        character_card=char,
        current_long_block=long_plan,
        previous_chapter_text=previous_prose,
        current_outline="",
        current_chapter_plan=plan,
        recent_summaries=recents,
        chapter_number=chapter,
    )
    director = run_acp(director_prompt, directory, "DIRECTOR", model="gpt-5.6-luna", effort="high")

    curator_prompt = generate_prompt(
        mode="context_curator",
        template="",
        book_content=runtime_book,
        creative_direction=CREATIVE_DIRECTION,
        world_vision=WORLD,
        character_card=char,
        current_long_block=long_plan,
        previous_chapter_text=previous_prose,
        current_outline=director["text"],
        current_chapter_plan=plan,
        recent_summaries=recents,
        chapter_number=chapter,
        writer_mode="curator_primary",
    )
    curator = run_acp(curator_prompt, directory, "CURATOR", model="gpt-5.6-luna", effort="high")

    primary_prompt = generate_prompt(
        mode="primary_writer",
        template="",
        book_content=runtime_book,
        creative_direction=CREATIVE_DIRECTION,
        world_vision=WORLD,
        character_card=char,
        current_long_block=long_plan,
        previous_chapter_text=previous_prose,
        current_outline=director["text"],
        current_chapter_plan=plan,
        recent_summaries=recents,
        chapter_number=chapter,
        writer_mode="curator_primary",
        curator_response=curator["text"],
    )
    primary = run_acp(primary_prompt, directory, "PRIMARY", model="gpt-5.6-terra", effort="high")
    primary_draft = extract_primary_draft(primary["text"]) or primary["text"]

    reviser_prompt = generate_prompt(
        mode="authority_reviser",
        template="",
        book_content=runtime_book,
        creative_direction=CREATIVE_DIRECTION,
        world_vision=WORLD,
        character_card=char,
        current_long_block=long_plan,
        previous_chapter_text=previous_prose,
        current_outline=director["text"],
        current_chapter_plan=plan,
        recent_summaries=recents,
        chapter_number=chapter,
        writer_mode="curator_primary",
        curator_response=curator["text"],
        primary_draft=primary_draft,
    )
    reviser = run_acp(reviser_prompt, directory, "AUTHORITY_REVISER", model="gpt-5.6-luna", effort="high")
    final_prose = extract_primary_draft(reviser["text"]) or reviser["text"]
    (directory / "FINAL_PROSE.md").write_text(final_prose + "\n", encoding="utf-8")

    state_prompt = generate_prompt(
        mode="state_delta",
        template="",
        book_content=runtime_book,
        creative_direction=CREATIVE_DIRECTION,
        world_vision=WORLD,
        character_card=char,
        chapter_number=chapter,
        chapter_prose=final_prose,
        recent_summaries=recents,
    )
    state = run_acp(state_prompt, directory, "STATE_DELTA", model="gpt-5.6-luna", effort="low")
    updated_book = apply_state_delta_to_book(runtime_book, chapter, state["text"])
    (directory / "BOOK_AFTER_STATE.md").write_text(updated_book, encoding="utf-8")

    return {
        "book": updated_book,
        "prose": final_prose,
        "plan": plan,
        "long_plan": long_plan,
        "prompts": {
            "director": director_prompt,
            "curator": curator_prompt,
            "primary": primary_prompt,
            "reviser": reviser_prompt,
            "state": state_prompt,
        },
        "runs": [director, curator, primary, reviser, state],
    }


def boundary_audit_prompt(*, mode: str, thread: MysteryThread, reveal, prompts: dict[str, str], prose: str, state_text: str = "") -> str:
    prompt_blob = "\n\n".join(f"## {k.upper()} PROMPT\n{v}" for k, v in prompts.items() if k != "state")
    if mode == "pre":
        task = """这是 Reveal 前章。判断任何 Prompt 或最终正文是否语义上泄露了作者 Hidden Fixed Point，或让读者/人物提前知道只有 Reveal 章才允许确认的 State Residue。仅仅知道‘问题仍未知’是允许的。"""
    elif mode == "reveal":
        task = """这是 Reveal 章。判断最终正文是否通过现场事件真正让读者确认允许的这一层 State Residue，同时是否越过 Still Open；不能因为读者能推测就算越界，只有文本把更深答案升级为确定事实才算。"""
    else:
        task = """这是 AUTHOR OPEN 章。作者自己尚未决定答案。判断 Prompt/正文是否擅自把任何来源解释升级成确定事实。"""
    return f"""你是独立 Mystery Boundary Auditor。只审泄漏与 Reveal Fidelity，不评分文风，不改稿。

{task}

# AUTHOR MYSTERY THREAD
{render_thread(thread)}

# REVEAL CONTRACT
{json.dumps(reveal.__dict__, ensure_ascii=False, indent=2) if reveal else 'NONE'}

# NODE PROMPTS
{prompt_blob}

# FINAL PROSE
{prose}

# STATE RESPONSE
{state_text or 'NONE'}

严格输出：
# MYSTERY BOUNDARY AUDIT
Verdict: PASS / FAIL
Raw Hidden Truth Exposed Before Authority: YES / NO
Allowed Reveal Realized: YES / NO / N-A
Still-Open Boundary Preserved: YES / NO
Reason: 5—10句
"""


def human_invariance_prompt(*, fixed: MysteryThread, story_a: str, story_b: str) -> str:
    return f"""你是独立 Character Authority Invariance 审计员。两个 Story Refresh 拿到同一个 World、同一个 Mystery Fixed Point、同一个 Reveal Boundary，唯一主要人物差异是 Frozen Human A/B。

Human A：好胜、贪钱、收藏欲强，异常首先被看作可占有的高价值机会。
Human B：妹妹安全优先，宁可错失高价值先手，也不把未知风险带回家。

判断两个 Story Refresh 是否真的在至少一个主要选择/机会成本上分叉；若都变成同一种‘理性调查最优解’，判 FAIL。Mystery Reveal 本身可以相同，人物围绕它怎么行动必须保留差异。

# FIXED MYSTERY
{render_thread(fixed)}

# STORY A
{story_a}

# STORY B
{story_b}

严格输出：
# HUMAN INVARIANCE AUDIT
Verdict: PASS / FAIL
A Main Choice: 一句
B Main Choice: 一句
Meaningful Divergence: YES / NO
Reason: 5—10句
"""


def decision(directory: Path, name: str, thread: MysteryThread, planning_need: str, context: str, expected: str) -> dict:
    p = build_decision_surface_prompt(thread=thread, planning_need=planning_need, current_context=context)
    run = run_acp(p, directory, name, model="gpt-5.6-luna", effort="high")
    status = parse_decision_surface(run["text"])
    if status != expected:
        raise RuntimeError(f"{name}: expected {expected}, got {status}")
    return {**run, "status": status}


def reframe_and_compile(directory: Path, label: str, thread: MysteryThread, surface_text: str, context: str, selected_id: str) -> tuple[MysteryThread, str, dict]:
    rp = build_reframe_prompt(thread=thread, decision_surface=surface_text, current_context=context)
    rr = run_acp(rp, directory, f"{label}_REFRAME", model="gpt-5.6-luna", effort="high")
    candidates = extract_reframe_candidates(rr["text"])
    selected = candidates[selected_id]
    (directory / f"{label}_SELECTED_{selected_id}.md").write_text(selected + "\n", encoding="utf-8")
    cp = build_canonization_compiler_prompt(thread=thread, selected_candidate=selected, current_context=context)
    cr = run_acp(cp, directory, f"{label}_COMPILER", model="gpt-5.6-terra", effort="high")
    verdict = parse_compiler_verdict(cr["text"])
    if verdict != "PASS":
        raise RuntimeError(f"{label} compiler={verdict}; preregistered candidate not replaced")
    fixed = adopt_hidden_fixed_point(thread=thread, selected_candidate=selected, compiler_report=cr["text"])
    (directory / f"{label}_FIXED.md").write_text(render_thread(fixed), encoding="utf-8")
    return fixed, selected, {"reframe": rr, "compiler": cr}


def state_context(book: str) -> str:
    return parse_book_sections(book)["status"]


def story_pair_for_humans(*, book: str, fixed: MysteryThread, previous_story: str, reveal_chapter: int, chapter: int, directory: Path):
    jobs = []
    chars = {"A": CHAR_A, "B": CHAR_B}
    with ThreadPoolExecutor(max_workers=2) as pool:
        for key, char in chars.items():
            current = current_character(book, char, chapter)
            prompt = story_refresh_prompt(
                book=book,
                char=char,
                current=current,
                previous_story=previous_story,
                thread=fixed,
                reveal_chapter=reveal_chapter,
            )
            jobs.append((key, prompt, pool.submit(run_acp, prompt, directory / key, "STORY_REFRESH", model="gpt-5.6-sol", effort="high")))
        results = {}
        for key, prompt, future in jobs:
            results[key] = {"prompt": prompt, "run": future.result()}
    return results


def main() -> None:
    if not RUNNER.is_file():
        raise RuntimeError(f"missing ACP runner: {RUNNER}")
    summary: dict[str, object] = {"pre_registration": {"cycle1_selected": "R2", "cycle2_selected": "R3", "reveal1": 3, "reveal2": 4}}
    book = make_base_book()
    (EXP / "INITIAL_BOOK.md").write_text(book, encoding="utf-8")
    (EXP / "WORLD.md").write_text(WORLD, encoding="utf-8")
    (EXP / "CHAR_A.md").write_text(CHAR_A, encoding="utf-8")
    (EXP / "CHAR_B.md").write_text(CHAR_B, encoding="utf-8")
    (EXP / "MYSTERY_INITIAL.md").write_text(render_thread(INITIAL_THREAD), encoding="utf-8")

    # 0) Author Open must be allowed to continue.
    d0_need = "今晚回影井第一次吐出一件足够具体的异常实物。当前只需要陆昭抢到、保住、验证它确实同时存在两份，并让别人因此行动；不需要决定来源。"
    d0 = decision(EXP / "decision0", "DECISION0", INITIAL_THREAD, d0_need, state_context(book), "DEFER")
    summary["decision0"] = d0["status"]

    # Initial open Story Refresh + Outline.
    current0 = current_character(book, CHAR_A, 0)
    sr0_prompt = story_refresh_prompt(book=book, char=CHAR_A, current=current0, previous_story=PREVIOUS_STORY, thread=INITIAL_THREAD, reveal_chapter=None)
    sr0 = run_acp(sr0_prompt, EXP / "open_phase", "STORY_REFRESH_OPEN", model="gpt-5.6-sol", effort="high")
    if "# MYSTERY REVEAL CONTRACT" in sr0["text"]:
        raise RuntimeError("AUTHOR OPEN Story Refresh illegally emitted reveal contract")
    out0_prompt = outline_prompt(book=book, char=CHAR_A, current=current0, story=sr0["text"])
    out0 = run_acp(out0_prompt, EXP / "open_phase", "OUTLINE_OPEN", model="gpt-5.6-luna", effort="high")
    runtime_sections = parse_book_sections(out0["text"])
    runtime_sections["status"] = initial_status()
    runtime_book = compose_book_content(runtime_sections)
    (EXP / "open_phase" / "RUNTIME_BOOK.md").write_text(runtime_book, encoding="utf-8")

    # Chapter 1 establishes anomaly but cannot answer it.
    ch1 = chapter_chain(chapter=1, runtime_book=runtime_book, outline_book=out0["text"], char=CHAR_A, previous_prose="", directory=EXP / "chapter1")
    audit1_prompt = boundary_audit_prompt(mode="open", thread=INITIAL_THREAD, reveal=None, prompts=ch1["prompts"], prose=ch1["prose"])
    audit1 = run_acp(audit1_prompt, EXP / "chapter1", "OPEN_BOUNDARY_AUDIT", model="gpt-5.6-terra", effort="high")
    if not re.search(r"(?mi)^Verdict:\s*PASS\s*$", audit1["text"]):
        raise RuntimeError("Chapter1 author-open boundary audit failed")
    runtime_book = ch1["book"]

    # 1) The next route now requires a minimum source category.
    d1_need = "第一章已经把回影井吐出的第二份同源实物推入公开验证，并建立了‘两份都能对同一旧井入口产生有效反应’这一事实。下一阶段要让入口后的证据继续发生可重复反应；若连第二份实物至少来自何种现实来源都不定，后续证据会变成 Writer 临时发明。只决定最小来源类别，不决定终极原因。"
    d1 = decision(EXP / "cycle1", "DECISION1", INITIAL_THREAD, d1_need, state_context(runtime_book), "DECISION NEEDED")
    fixed1, selected1, rc1 = reframe_and_compile(EXP / "cycle1", "CYCLE1", INITIAL_THREAD, d1["text"], state_context(runtime_book), "R2")
    summary["cycle1_selected"] = "R2"

    # Same Fixed Point, two Humans: must preserve different choice routes.
    pair = story_pair_for_humans(book=runtime_book, fixed=fixed1, previous_story=sr0["text"], reveal_chapter=3, chapter=1, directory=EXP / "cycle1" / "human_pair")
    human_a_story = pair["A"]["run"]["text"]
    human_b_story = pair["B"]["run"]["text"]
    h_audit = run_acp(human_invariance_prompt(fixed=fixed1, story_a=human_a_story, story_b=human_b_story), EXP / "cycle1", "HUMAN_INVARIANCE_AUDIT", model="gpt-5.6-terra", effort="high")
    if not re.search(r"(?mi)^Verdict:\s*PASS\s*$", h_audit["text"]):
        raise RuntimeError("Character Authority Invariance failed")

    reveal1 = parse_reveal_contract(human_a_story)
    if reveal1.reveal_chapter != 3 or reveal1.mystery_id != fixed1.mystery_id:
        raise RuntimeError("Cycle1 reveal contract violates preregistration")
    (EXP / "cycle1" / "REVEAL1_CONTRACT.json").write_text(json.dumps(reveal1.__dict__, ensure_ascii=False, indent=2), encoding="utf-8")

    current1 = current_character(runtime_book, CHAR_A, 1)
    o1_prompt = outline_prompt(book=runtime_book, char=CHAR_A, current=current1, story=human_a_story, reveal_id=reveal1.mystery_id, reveal_chapter=3)
    o1 = run_acp(o1_prompt, EXP / "cycle1", "OUTLINE1", model="gpt-5.6-luna", effort="high")

    # Chapter 2: pre-reveal full chain. Full hidden truth must remain absent.
    ch2_plan = extract_chapter_plan(o1["text"], 2)
    ch2_long = project_current_long_block_for_chapter(parse_book_sections(o1["text"])["long_plan"], 2)
    marker1 = f"[MYSTERY-REVEAL:{reveal1.mystery_id}]"
    if marker1 in ch2_plan or reveal1.state_residue in ch2_plan or reveal1.state_residue in ch2_long:
        raise RuntimeError("Cycle1 Outline leaked reveal into Chapter2 planning")
    ch2 = chapter_chain(chapter=2, runtime_book=runtime_book, outline_book=o1["text"], char=CHAR_A, previous_prose=ch1["prose"], directory=EXP / "chapter2")
    pre_proj1 = compile_runtime_mystery_projection(fixed1, reveal1, chapter_number=2)
    (EXP / "chapter2" / "MYSTERY_RUNTIME_PROJECTION.md").write_text(pre_proj1 + "\n", encoding="utf-8")
    pre_audit1 = run_acp(boundary_audit_prompt(mode="pre", thread=fixed1, reveal=reveal1, prompts=ch2["prompts"], prose=ch2["prose"]), EXP / "chapter2", "PRE_REVEAL_AUDIT", model="gpt-5.6-terra", effort="high")
    if not re.search(r"(?mi)^Verdict:\s*PASS\s*$", pre_audit1["text"]):
        raise RuntimeError("Cycle1 pre-reveal leak audit failed")
    runtime_book = ch2["book"]

    # Chapter 3: reveal event injected only now.
    ch3 = chapter_chain(chapter=3, runtime_book=runtime_book, outline_book=o1["text"], char=CHAR_A, previous_prose=ch2["prose"], reveal=reveal1, directory=EXP / "chapter3")
    reveal_proj1 = compile_runtime_mystery_projection(fixed1, reveal1, chapter_number=3)
    (EXP / "chapter3" / "MYSTERY_RUNTIME_PROJECTION.md").write_text(reveal_proj1 + "\n", encoding="utf-8")
    rev_audit1 = run_acp(boundary_audit_prompt(mode="reveal", thread=fixed1, reveal=reveal1, prompts=ch3["prompts"], prose=ch3["prose"], state_text=(EXP / "chapter3" / "STATE_DELTA.md").read_text(encoding="utf-8")), EXP / "chapter3", "REVEAL1_AUDIT", model="gpt-5.6-terra", effort="high")
    if not re.search(r"(?mi)^Verdict:\s*PASS\s*$", rev_audit1["text"]):
        raise RuntimeError("Cycle1 reveal audit failed")
    runtime_book = ch3["book"]

    # Reveal residue becomes an anchor; deeper question reopens.
    open2 = advance_after_reveal(fixed1, reveal1, next_decision_trigger="进入新的来源通道前，如果两处现实的关系会直接改变谁能跨越、什么能带回，就只决定这一层关系；其它来源继续未知。")
    (EXP / "cycle2" / "MYSTERY_AFTER_REVEAL1.md").parent.mkdir(parents=True, exist_ok=True)
    (EXP / "cycle2" / "MYSTERY_AFTER_REVEAL1.md").write_text(render_thread(open2), encoding="utf-8")

    d2_need = "第3章的 Reveal 已成为 Canon。下一章已经出现一个只能在‘来源地与听雨城究竟属于哪一种现实关系’明确后才能稳定表现的跨越现象；现在只决定这两处现实之间的最小关系，不解释它们为何产生，也不决定是否还有第三处。"
    d2 = decision(EXP / "cycle2", "DECISION2", open2, d2_need, state_context(runtime_book), "DECISION NEEDED")
    fixed2, selected2, rc2 = reframe_and_compile(EXP / "cycle2", "CYCLE2", open2, d2["text"], state_context(runtime_book), "R3")
    summary["cycle2_selected"] = "R3"

    # Second partial canonization, reveal immediately in Chapter 4.
    current3 = current_character(runtime_book, CHAR_A, 3)
    sr2_prompt = story_refresh_prompt(book=runtime_book, char=CHAR_A, current=current3, previous_story=strip_reveal_contract(human_a_story), thread=fixed2, reveal_chapter=4)
    sr2 = run_acp(sr2_prompt, EXP / "cycle2", "STORY_REFRESH2", model="gpt-5.6-sol", effort="high")
    reveal2 = parse_reveal_contract(sr2["text"])
    if reveal2.reveal_chapter != 4 or reveal2.mystery_id != fixed2.mystery_id:
        raise RuntimeError("Cycle2 reveal contract violates preregistration")
    (EXP / "cycle2" / "REVEAL2_CONTRACT.json").write_text(json.dumps(reveal2.__dict__, ensure_ascii=False, indent=2), encoding="utf-8")
    o2_prompt = outline_prompt(book=runtime_book, char=CHAR_A, current=current3, story=sr2["text"], reveal_id=reveal2.mystery_id, reveal_chapter=4)
    o2 = run_acp(o2_prompt, EXP / "cycle2", "OUTLINE2", model="gpt-5.6-luna", effort="high")

    ch4 = chapter_chain(chapter=4, runtime_book=runtime_book, outline_book=o2["text"], char=CHAR_A, previous_prose=ch3["prose"], reveal=reveal2, directory=EXP / "chapter4")
    rev_audit2 = run_acp(boundary_audit_prompt(mode="reveal", thread=fixed2, reveal=reveal2, prompts=ch4["prompts"], prose=ch4["prose"], state_text=(EXP / "chapter4" / "STATE_DELTA.md").read_text(encoding="utf-8")), EXP / "chapter4", "REVEAL2_AUDIT", model="gpt-5.6-terra", effort="high")
    if not re.search(r"(?mi)^Verdict:\s*PASS\s*$", rev_audit2["text"]):
        raise RuntimeError("Cycle2 reveal audit failed")
    runtime_book = ch4["book"]

    open3 = advance_after_reveal(fixed2, reveal2, next_decision_trigger="只有下一阶段真的必须解释更深来源时才继续定真。")
    (EXP / "MYSTERY_AFTER_REVEAL2.md").write_text(render_thread(open3), encoding="utf-8")

    d3_need = "下一阶段先处理第4章 Reveal 造成的现实后果：有人抢夺跨越机会、兵坊和城主府重新定价陆昭、陆昭必须决定先拿钱还是先保住家人。所有这些都可以在不解释终极来源的情况下成立。"
    d3 = decision(EXP / "final_defer", "DECISION3", open3, d3_need, state_context(runtime_book), "DEFER")
    summary["decision3"] = d3["status"]

    (EXP / "FINAL_BOOK.md").write_text(runtime_book, encoding="utf-8")
    summary.update({
        "decision0": "DEFER",
        "decision1": "DECISION NEEDED",
        "decision2": "DECISION NEEDED",
        "final_decision": "DEFER",
        "cycle1_compiler": "PASS",
        "cycle2_compiler": "PASS",
        "human_invariance": "PASS",
        "chapter1_open_boundary": "PASS",
        "chapter2_pre_reveal_boundary": "PASS",
        "chapter3_reveal_boundary": "PASS",
        "chapter4_reveal_boundary": "PASS",
        "production_modified": False,
        "current_user_novel_modified": False,
    })
    dump(EXP / "RUN_SUMMARY.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
