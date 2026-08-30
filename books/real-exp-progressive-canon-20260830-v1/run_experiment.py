from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
import json
import random
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
RUNNER = ROOT / "temps" / "acp_readonly_runner.mjs"
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.character_prompts import STORY_REFRESH_PROMPT  # noqa: E402
from story_mvp.progressive_canon import (  # noqa: E402
    MysteryThread,
    adopt_hidden_fixed_point,
    build_canonization_compiler_prompt,
    build_decision_surface_prompt,
    build_reframe_prompt,
    extract_reframe_candidates,
    parse_compiler_verdict,
    parse_decision_surface,
    render_planning_projection,
    render_thread,
)


@dataclass(frozen=True)
class Case:
    case_id: str
    thread: MysteryThread
    planning_need: str
    context: str
    author_direction: str
    effective_world: str
    current_character: str
    canon_memory: str
    previous_story: str
    expected_surface: str
    preregistered_candidate: str


CASES = (
    Case(
        case_id="meta_instance",
        thread=MysteryThread(
            mystery_id="M-META-01",
            question="故乡为什么会被标记为副本，所谓玩家/NPC究竟是什么，裴骁为什么拥有正常副本居民不该拥有的离界可能？",
            state="OPEN",
            known_anchors="""- 裴骁从小在北燧城生活，父母、妹妹、旧街道、受伤与得失都以连续人生方式真实发生。
- 界签突然把北燧城标成“第一副本”，给出十二日期限、落日隧道合法归门，以及“只有本地真实取得并确认归属的成果可携带”的规则。
- 界签从未说明玩家/NPC的本体差异、谁建立副本、北燧城是否后来被副本化，或裴骁为何能离界。
- 已批准 World Horizon Handoff 只确认归门通向跨副本候场，下一目的地保持空白。""",
            decision_trigger="只有下一阶段的具体故事无法在不确定玩家/NPC/Meta关系的情况下成立时才定真；仅进入第二个独立副本不触发。",
            remains_unknown="玩家是什么；NPC是否只是权限标签；谁建立/维护副本；北燧城为何成为第一副本；裴骁为何能离界；Meta层是否仍是更高层副本。",
            route="story",
        ),
        planning_need="""第一副本已经完成主要结算。现在只需要让裴骁进入第二个真正独立的 Local Instance World，并让第一副本带出的能力、器物、欲望继续产生新碰撞。可以出现一个身份不明的跨副本行动者，但本阶段不要求确认对方是不是“真实玩家”，也不要求解释副本来源。""",
        context="""第一副本的核心承诺已经兑现：故乡被重新标成副本；裴骁为了钱、胜负、家人与离界机会行动；返照环等成果真正属于他并可携带；落日隧道归门开启。当前唯一 Meta 确认事实是“存在跨副本候场/下一实例”；玩家/NPC/系统来源仍无答案。""",
        author_direction="成熟中文男频多世界副本成长爽文。第二副本必须像独立真实世界，不是任务房；Meta Mystery 保持强牵引，但不要为了显示深度提前解释终极答案。",
        effective_world="""# EFFECTIVE WORLD｜第二实例：雾钟群岛
群岛每天黄昏会随巨钟声重新排列，普通居民靠记潮图、灯船和浮桥在岛间生活。当地力量主尺为潮纹{N}，1—40；普通成年护航者约5—8，岛卫精锐12—18，能独自横渡夜雾者20以上，群岛顶层约35—40。岛上最值钱的是能在重排后仍指向旧位置的“定响骨”、可抵抗夜雾的灯盐和被各岛争抢的浮钟控制权。三座大岛正在为一口失声巨钟争夺航路，且完全不知道裴骁或北燧城。""",
        current_character="""裴骁｜界阶2；保留越限成常、返照环、灯阶2基础与已取得物。核心欲望仍是钱、胜负、离开旧生活并掌控自己的去留；爱面子、愿赌、会为家人和具体关系改变一次最优收益，但不是救世主。第一次离开故乡后，他最想知道外面到底有多少世界，同时本能地想把每个世界真正值钱的东西变成自己的。""",
        canon_memory="""第一副本已结束：北燧城确实被界签称为第一副本；裴骁从落日隧道离界；返照环、真昼炭髓和已完成的越限成果可携带。未知：玩家、NPC、副本来源、离界Bug原因、Meta层本体。""",
        previous_story="""旧 Story Program 的跨世界承诺：每个实例有独立生活与力量规则；真实取得的成果持续携带；下一实例必须换 Story Engine。没有任何已批准终极 Meta 答案。""",
        expected_surface="DEFER",
        preregistered_candidate="D0",
    ),
    Case(
        case_id="identity_archive",
        thread=MysteryThread(
            mystery_id="M-ID-01",
            question="沈砚胸骨里的空白王印究竟属于什么，他为什么会被旧档案称为‘缺席者’？",
            state="OPEN",
            known_anchors="""- 沈砚五岁时被商队从边境战场外捡到，此前记忆缺失；商队收养与之后十多年生活都已明确发生。
- 胸骨空白王印会让旧王朝档案门回应；守门老人只认出它与被刮去姓名的“第七席”记录相同。
- 已通过公开验血确认沈砚与现王族没有血缘匹配。
- 没有证据证明他是转世、王族私生子、实验体或第七席本人。
- 沈砚本人厌恶别人用身世替他决定道路，他进档案馆首先是为了拿到能换钱和力量的旧王兵谱。""",
            decision_trigger="当下一大型阶段必须定义旧档案门为什么允许/拒绝他，以及哪类历史材料会对他的印记产生可验证反应时，只决定印记至少属于哪一类历史关系。",
            remains_unknown="沈砚五岁前是谁；谁把印记放进他身体；第七席本人去了哪里；旧王朝覆灭终极原因；印记是否还能转移。",
            route="story",
        ),
        planning_need="""作者已批准下一大型阶段发生在‘缺席档案馆’内部：第一道门必须根据空白王印作出真实反应，馆内第一批证据也必须围绕这枚印记展开。如果连印记属于血统、职位、可转移凭证还是别的类别都不定，门的反应与证据链都会变成 Writer 临时发明。现在只需要决定这一层类别，不需要决定沈砚五岁前完整身世。""",
        context="""当前已发生事实只有：战场弃儿、空白王印、旧档案响应、第七席记录同形、与现王族无血缘。下一阶段固定进入缺席档案馆，但终极身世仍开放。""",
        author_direction="成熟中文男频玄幻成长。身份谜团要扩大行动与敌我关系，不把主角写成命定救世主；即使身份特殊，也要保留他对钱、兵器、胜负和自主选择的直接欲望。",
        effective_world="""# EFFECTIVE WORLD｜旧都缺席档案馆
旧都以印阶{N}衡量能承载多少王印压力，1—30。档案馆是旧王朝留下的封闭机构，门禁会读取已经存在的印记类别，但不会创造身份。馆内保存军械谱、失踪席位记录和旧都封城前最后七日的文书。现王庭、兵器商会和三名旧臣后人都想先拿到第七席留下的兵谱，却各自只掌握部分事实。""",
        current_character="""沈砚｜印阶7；边境商队长大，擅长近战与拆解旧兵器。最强牵引是把值钱的旧王兵器与兵谱变成自己的力量和钱；对‘你是谁所以你应该做什么’极度反感。养母仍是他最明确的关系软肋。""",
        canon_memory="""已确认：空白王印存在；与第七席旧记录同形；无现王族血缘；第一道档案门尚未开启。未知：印记来源、沈砚五岁前历史、第七席下落。""",
        previous_story="""下一阶段已批准进入缺席档案馆，争夺旧王兵谱并第一次获得关于空白王印的可验证历史证据；不得一次揭开完整身世。""",
        expected_surface="DECISION NEEDED",
        preregistered_candidate="R2",
    ),
    Case(
        case_id="relationship_betrayal",
        thread=MysteryThread(
            mystery_id="M-REL-01",
            question="燕迟当年为什么亲手打开鹤鸣城门，又为什么三年后暗中救走江野的妹妹？",
            state="OPEN",
            known_anchors="""- 鹤鸣夜，燕迟在众目睽睽下亲手打开城门；她行动清醒，没有已知控制或幻术痕迹。
- 开门前她先杀死了阻止她的本阵统领，这是已经发生的事实，不能改成‘其实没有背叛’。
- 三年后，她用假名从敌营里救出江野妹妹，并拒绝说明原因。
- 残信只有一句‘我答应的不是他们’，无法确定她答应了谁、什么事或代价。
- 江野既想报当年的仇，也仍会因为燕迟本人改变选择；两人的旧关系不能被洗成单纯误会。""",
            decision_trigger="当两人下一次正面对质、敌方同时拿出可验证的鹤鸣夜证据时，至少要决定她当年的开门是自主承担的一项私人承诺，还是被外力强迫；否则所有证据和她的当前选择都只能继续绕圈。",
            remains_unknown="她具体答应了谁；承诺的完整内容；她是否预料城破规模；她后来救妹妹是否出于同一承诺；更大的敌方计划。",
            route="story",
        ),
        planning_need="""下一大型阶段已经批准为江野与燕迟第一次无法逃避的正面对质。敌人会拿出一件能证明‘燕迟当晚有选择空间’的真实物证，因此本阶段必须至少确定她是自主做出开门选择，还是实际上失去选择。只决定这一层；她究竟答应谁、为什么值得城破、后来为什么救妹妹仍可以继续未知。""",
        context="""已发生：燕迟清醒开门并杀本阵统领；城破造成真实死亡；三年后她又救出江野妹妹；残信‘我答应的不是他们’。不能把背叛抹成幻术或假开门。""",
        author_direction="成熟中文男频关系冲突。保留背叛的真实重量、吸引与怨恨并存；不要用一个秘密把燕迟洗成纯牺牲圣人，也不要让江野自动选择原谅。",
        effective_world="""# EFFECTIVE WORLD｜鹤鸣边州
剑阶{N} 1—24。三年前鹤鸣城破后，旧守军、占城军与逃民势力仍互相追杀。当前最大的公开利益是城下新开的赤髓矿与旧军械库；谁控制两者，谁就能重建一支边军。鹤鸣夜的责任仍是活人之间的现实仇债，不是抽象历史。""",
        current_character="""江野｜剑阶11；想变强、拿回旧军械库，也想亲口问燕迟为什么。好胜、记仇、对燕迟仍有强烈偏心但绝不愿承认；妹妹的安全会直接改变他的冒险阈值。""",
        canon_memory="""燕迟开门与杀统领为已发生事实；妹妹后来被她救走也为已发生事实；双方尚未完成对质。未知是动机与承诺对象，不是行为本身。""",
        previous_story="""下一阶段固定包含公开物证、第一次正面对质、旧军械库争夺和关系重新定价；不要求本阶段解决更大的敌方幕后。""",
        expected_surface="DECISION NEEDED",
        preregistered_candidate="R3",
    ),
)


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def run_acp(prompt: Path, out_json: Path, out_md: Path, *, model: str, effort: str, label: str) -> dict:
    started = time.perf_counter()
    proc = subprocess.run(
        ["node", str(RUNNER), str(prompt), str(out_json), model, effort, label],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ACP {label} failed: {proc.stderr[-3000:]}\n{proc.stdout[-3000:]}")
    payload = json.loads(out_json.read_text(encoding="utf-8"))
    if not payload.get("ok"):
        raise RuntimeError(f"ACP {label} failed: {payload.get('error')}")
    text = str(payload.get("text", "")).strip()
    out_md.write_text(text + "\n", encoding="utf-8")
    return {
        "text": text,
        "wall": round(time.perf_counter() - started, 3),
        "agent_wall": payload.get("wall_seconds"),
        "model": model,
        "effort": effort,
    }


def write_case_fixture(case: Case, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "MYSTERY_THREAD.md").write_text(render_thread(case.thread), encoding="utf-8")
    (directory / "PLANNING_NEED.md").write_text(case.planning_need + "\n", encoding="utf-8")
    (directory / "CURRENT_CONTEXT.md").write_text(case.context + "\n", encoding="utf-8")
    dump(
        directory / "PRE_REGISTERED.json",
        {
            "expected_surface": case.expected_surface,
            "candidate": case.preregistered_candidate,
            "registered_before_llm": True,
        },
    )


def story_refresh_prompt(case: Case, mystery_control: str = "") -> str:
    blocks = [
        STORY_REFRESH_PROMPT.strip(),
        "# 作者粗方向\n" + case.author_direction.strip(),
        "# EFFECTIVE WORLD｜Independent Authority\n" + case.effective_world.strip(),
        "# CURRENT CHARACTER｜Deterministic Forward Snapshot\n" + case.current_character.strip(),
        "# ALREADY-HAPPENED CANON MEMORY\n" + case.canon_memory.strip(),
        "# PREVIOUS STORY PROGRAM｜Only unresolved future obligations survive\n" + case.previous_story.strip(),
    ]
    if mystery_control.strip():
        blocks.append(
            "# AUTHOR MYSTERY PLANNING CONTROL｜PLANNING ONLY / NEVER READER CANON\n"
            + mystery_control.strip()
        )
    return "\n\n".join(blocks) + "\n"


def phase_decision_surfaces() -> dict[str, dict]:
    results: dict[str, dict] = {}
    jobs = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        for case in CASES:
            d = EXP / case.case_id
            write_case_fixture(case, d)
            prompt_text = build_decision_surface_prompt(
                thread=case.thread,
                planning_need=case.planning_need,
                current_context=case.context,
            )
            pp = d / "DECISION_SURFACE_PROMPT.md"
            pp.write_text(prompt_text, encoding="utf-8")
            jobs.append(
                (
                    case,
                    pool.submit(
                        run_acp,
                        pp,
                        d / "DECISION_SURFACE_ACP.json",
                        d / "DECISION_SURFACE.md",
                        model="gpt-5.6-luna",
                        effort="high",
                        label=f"progressive-canon-{case.case_id}-decision",
                    ),
                )
            )
        for case, future in jobs:
            run = future.result()
            status = parse_decision_surface(run["text"])
            results[case.case_id] = {
                "surface": status,
                "expected": case.expected_surface,
                "surface_match": status == case.expected_surface,
                "decision_wall": run["wall"],
            }
    return results


def phase_reframes_and_compilers(summary: dict[str, dict]) -> dict[str, MysteryThread]:
    adopted: dict[str, MysteryThread] = {}
    reframe_jobs = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for case in CASES:
            if summary[case.case_id]["surface"] != "DECISION NEEDED":
                continue
            d = EXP / case.case_id
            surface = (d / "DECISION_SURFACE.md").read_text(encoding="utf-8")
            prompt = build_reframe_prompt(
                thread=case.thread,
                decision_surface=surface,
                current_context=case.context,
            )
            pp = d / "REFRAME_PROMPT.md"
            pp.write_text(prompt, encoding="utf-8")
            reframe_jobs.append(
                (
                    case,
                    pool.submit(
                        run_acp,
                        pp,
                        d / "REFRAME_ACP.json",
                        d / "REFRAME.md",
                        model="gpt-5.6-luna",
                        effort="high",
                        label=f"progressive-canon-{case.case_id}-reframe",
                    ),
                )
            )
        reframe_runs = [(case, future.result()) for case, future in reframe_jobs]

    compiler_jobs = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for case, run in reframe_runs:
            d = EXP / case.case_id
            candidates = extract_reframe_candidates(run["text"])
            selected_id = case.preregistered_candidate
            if selected_id == "D0":
                summary[case.case_id]["selected"] = "D0"
                summary[case.case_id]["compiler"] = "SKIPPED"
                continue
            selected = candidates[selected_id]
            (d / "SELECTED_CANDIDATE.md").write_text(selected + "\n", encoding="utf-8")
            cp = build_canonization_compiler_prompt(
                thread=case.thread,
                selected_candidate=selected,
                current_context=case.context,
            )
            cpp = d / "COMPILER_PROMPT.md"
            cpp.write_text(cp, encoding="utf-8")
            compiler_jobs.append(
                (
                    case,
                    selected,
                    pool.submit(
                        run_acp,
                        cpp,
                        d / "COMPILER_ACP.json",
                        d / "COMPILER.md",
                        model="gpt-5.6-terra",
                        effort="high",
                        label=f"progressive-canon-{case.case_id}-compiler",
                    ),
                )
            )
        for case, selected, future in compiler_jobs:
            run = future.result()
            verdict = parse_compiler_verdict(run["text"])
            summary[case.case_id]["selected"] = case.preregistered_candidate
            summary[case.case_id]["compiler"] = verdict
            summary[case.case_id]["compiler_wall"] = run["wall"]
            if verdict != "PASS":
                continue
            fixed = adopt_hidden_fixed_point(
                thread=case.thread,
                selected_candidate=selected,
                compiler_report=run["text"],
            )
            adopted[case.case_id] = fixed
            (EXP / case.case_id / "ADOPTED_HIDDEN_FIXED_POINT.md").write_text(
                render_thread(fixed), encoding="utf-8"
            )
            (EXP / case.case_id / "PLANNING_PROJECTION.md").write_text(
                render_planning_projection(fixed) + "\n", encoding="utf-8"
            )
    return adopted


def phase_story_refresh(summary: dict[str, dict], adopted: dict[str, MysteryThread]) -> list[str]:
    comparable: list[str] = []
    jobs = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        for case in CASES:
            d = EXP / case.case_id
            baseline = story_refresh_prompt(case)
            (d / "B0_STORY_REFRESH_PROMPT.md").write_text(baseline, encoding="utf-8")

            control = ""
            if case.case_id == "meta_instance":
                # The author explicitly chooses to keep this mystery open for the next instance.
                control = render_planning_projection(case.thread)
                if summary[case.case_id]["surface"] != "DEFER":
                    summary[case.case_id]["treatment_downstream"] = "SKIPPED_SURFACE_MISMATCH"
                    continue
            elif case.case_id in adopted:
                control = render_planning_projection(adopted[case.case_id])
            else:
                summary[case.case_id]["treatment_downstream"] = "SKIPPED_NO_COMPILER_PASS"
                continue

            treatment = story_refresh_prompt(case, control)
            (d / "T_STORY_REFRESH_PROMPT.md").write_text(treatment, encoding="utf-8")
            jobs.append(
                (
                    case,
                    "B0",
                    pool.submit(
                        run_acp,
                        d / "B0_STORY_REFRESH_PROMPT.md",
                        d / "B0_STORY_REFRESH_ACP.json",
                        d / "B0_STORY_REFRESH.md",
                        model="gpt-5.6-sol",
                        effort="high",
                        label=f"progressive-canon-{case.case_id}-b0-refresh",
                    ),
                )
            )
            jobs.append(
                (
                    case,
                    "T",
                    pool.submit(
                        run_acp,
                        d / "T_STORY_REFRESH_PROMPT.md",
                        d / "T_STORY_REFRESH_ACP.json",
                        d / "T_STORY_REFRESH.md",
                        model="gpt-5.6-sol",
                        effort="high",
                        label=f"progressive-canon-{case.case_id}-t-refresh",
                    ),
                )
            )
            comparable.append(case.case_id)
        for case, arm, future in jobs:
            run = future.result()
            summary[case.case_id][f"{arm.lower()}_refresh_wall"] = run["wall"]
            summary[case.case_id]["treatment_downstream"] = "COMPLETE"
    return comparable


def build_blind_package(comparable: list[str]) -> tuple[str, dict[str, dict[str, str]]]:
    rng = random.Random(20260830)
    mapping: dict[str, dict[str, str]] = {}
    blocks = []
    by_id = {case.case_id: case for case in CASES}
    for case_id in comparable:
        case = by_id[case_id]
        d = EXP / case_id
        b0 = (d / "B0_STORY_REFRESH.md").read_text(encoding="utf-8")
        treatment = (d / "T_STORY_REFRESH.md").read_text(encoding="utf-8")
        pair = [("B0", b0), ("T", treatment)]
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


def judge_prompt(package: str, lens: str) -> str:
    return f"""你是独立盲评员。下面每个 Case 有冻结事实、当前规划需要和两个匿名 Story Refresh。你不知道哪个是 baseline / treatment。

你的镜头：{lens}

逐 Case 判断：
- Retcon Safety：有没有把已发生事实改掉；
- Mystery Discipline：有没有把仍不该知道的答案提前写死；
- Story Momentum：即使保留未知，下一阶段是否仍然具体、想追；
- Layered Canonization：若出现新定真，是否只定一层、留下更深未知；
- Reinterpretation Value：旧锚点是否获得新意义而非作废；
- Commercial Pull：是否让人更想继续看，而不是更像 lore 文档。

不要因为版本解释更多就加分；不要因为版本保留 Mystery 就默认加分，如果它因此变得空泛也要扣分。

严格输出：
# BLIND MYSTERY PANEL
## CASE <id>
Winner: X / Y / TIE
X Overall: 0-100
Y Overall: 0-100
Retcon / Mystery / Momentum / Layering / Reinterpretation / Pull: 分别简短比较
Reason: 4—8句

{package}
"""


def phase_blind_judges(comparable: list[str], summary: dict[str, dict]) -> None:
    if not comparable:
        return
    package, mapping = build_blind_package(comparable)
    (EXP / "BLIND_PACKAGE.md").write_text(package + "\n", encoding="utf-8")
    dump(EXP / "BLIND_MAPPING.json", mapping)
    prompts = {
        "cold_reader": judge_prompt(package, "商业冷读：优先看会不会继续追、故事是否具体、解释是否抢走神秘感。"),
        "longform": judge_prompt(package, "长篇结构：优先看可持续 Mystery、向后兼容重释、未来故事门与作者自由度。"),
    }
    jobs = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for name, prompt in prompts.items():
            pp = EXP / f"BLIND_{name.upper()}_PROMPT.md"
            pp.write_text(prompt, encoding="utf-8")
            jobs.append(
                (
                    name,
                    pool.submit(
                        run_acp,
                        pp,
                        EXP / f"BLIND_{name.upper()}_ACP.json",
                        EXP / f"BLIND_{name.upper()}.md",
                        model="gpt-5.6-terra" if name == "cold_reader" else "gpt-5.6-luna",
                        effort="high",
                        label=f"progressive-canon-blind-{name}",
                    ),
                )
            )
        for name, future in jobs:
            run = future.result()
            summary.setdefault("judges", {})[name] = {"wall": run["wall"], "model": run["model"]}


def main() -> None:
    if not RUNNER.is_file():
        raise RuntimeError(f"missing ACP runner: {RUNNER}")
    summary = phase_decision_surfaces()
    adopted = phase_reframes_and_compilers(summary)
    comparable = phase_story_refresh(summary, adopted)
    phase_blind_judges(comparable, summary)
    summary["comparable_cases"] = comparable
    summary["production_modified"] = False
    summary["current_novel_modified"] = False
    dump(EXP / "RUN_SUMMARY.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
