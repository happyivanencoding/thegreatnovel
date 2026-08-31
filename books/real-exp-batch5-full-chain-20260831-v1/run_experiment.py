from __future__ import annotations

import difflib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.hybrid_runtime import extract_primary_draft, extract_primary_fact_summary
from story_mvp.prompts import DEFAULT_PROMPT_TEMPLATES, generate_prompt, parse_canon_memory
from story_mvp.storage import (
    apply_state_delta_to_book,
    compose_book_content,
    compose_design_content,
    parse_book_sections,
    validate_book_content_for_save,
    validate_chapter_body_for_save,
)

RUNNER = ROOT / "temps" / "acp_readonly_runner.mjs"
CONTROL = EXP / "control_sequential"
TREATMENT = EXP / "treatment_batch5_primary"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def dump(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_model_text(text: str) -> str:
    text = re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text)
    return text.strip()


def run_acp(prompt: Path, out_json: Path, out_md: Path, *, model: str, effort: str, label: str, call_log: list[dict]) -> str:
    if out_md.is_file() and out_json.is_file():
        data = json.loads(out_json.read_text(encoding="utf-8"))
        text = out_md.read_text(encoding="utf-8").strip()
        call_log.append({
            "label": label,
            "model": model,
            "effort": effort,
            "reused": True,
            "wall_seconds": data.get("wall_seconds"),
            "usage": data.get("usage"),
            "chars": len(text),
        })
        return text
    started = time.perf_counter()
    proc = subprocess.run(
        ["node", str(RUNNER), str(prompt), str(out_json), model, effort, label],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    elapsed = time.perf_counter() - started
    if proc.returncode != 0:
        raise RuntimeError(f"ACP {label} failed:\n{proc.stderr[-5000:]}\n{proc.stdout[-5000:]}")
    data = json.loads(out_json.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"ACP {label}: {data.get('error')}")
    text = clean_model_text(str(data.get("text", "")))
    if not text:
        raise RuntimeError(f"ACP {label}: empty response")
    write(out_md, text)
    row = {
        "label": label,
        "model": model,
        "effort": effort,
        "reused": False,
        "outer_wall_seconds": round(elapsed, 3),
        "wall_seconds": data.get("wall_seconds", round(elapsed, 3)),
        "usage": data.get("usage"),
        "chars": len(text),
    }
    call_log.append(row)
    print(json.dumps(row, ensure_ascii=False), flush=True)
    return text


WORLD = r"""# PROTAGONIST-BLIND WORLD VISION

玄曜大界由九重天、三十六天洲、数百王朝、宗门与古族组成。天洲之间有跨洲天舟，王境能横渡远空，圣境与帝境的战斗可以改变山河与天象。

## 普通人的生活与上升

九环天都是玄曜大界著名天城，九座巨大城环悬在云海上方，跨洲天舟在城环之间往来。普通修士依靠宗门、古族、商会、武府、拍卖与远行机会接触更大的世界；灵玉是修士最常见的大额交易货币。

## 力量体系与正常值

玄曜修炼分九个大境界，每境一至九重：锻体、通脉、灵海、神台、天门、王、圣、帝、天外。大境界差距通常显著，但不是绝对胜负公式，功法、兵器、经验、环境和特殊能力都可能制造越级结果。

### 精确力量主尺｜Frozen Grammar

主尺类型：大境界+数字子级
主尺名称：玄曜九境
精确位置格式：{大境界}{N}重
数字精度规则：每境1—9重；未入当前境者按前一境精确位置记录
当前可见范围：锻体1重—帝9重
当前大档位：
- 锻体 / 通脉：基础修士。
- 灵海 / 神台：年轻修士与地方中坚常见活动层。
- 天门 / 王：天都高手与一洲霸主层。
- 圣 / 帝：能够改变大片疆域与天象的高位层。

宁烬开局是灵海境3重；同龄普通天才常见灵海境6—8重；裴照临是灵海境9重；天都真正高位护卫可到天门境；帝境战斗足以让整座天幕中的山河改色。

镜海界是与玄曜大界不同的独立世界。大海悬在天空，陆地在下方；本地人出生后通常同时拥有岸身与海身，两处都是真实身体，共享记忆却可以有不同即时行为与性格表现。杀死一处并不等于杀死这个人，只有两处都死才算真正死亡。镜海界常用“照数”描述能稳定维持多少真实位置；普通居民最常见就是岸、海二照。

## 社会现实与身份

玄曜大界里，一个人正常只有一个真实身体和一个真实位置；幻身、傀儡与分身都被视为替代物，不会被天地当作第二个同等真实的本人。九环天都的天外商会能举行让古族、王侯与高阶修士参加的拍卖；裴氏是天都有分量的古族，裴照临作为同代灵海境9重天才，公开实力远高于宁烬。

镜海界的城市同时向陆地与天海展开，追杀、战争、交易都可能在上下两个方向发生。王女镜离拥有岸身；她的海身澜生是同一个人的另一处真实位置。镜海王赫连枢公开要求镜离服从王命，但其更深私人目的只有在故事依法揭示后才能成为读者事实。

## 世界里真正值钱、值得想要的东西

黑门骨是能撕开真实世界裂口的天外遗物，价值足以引来高阶势力争夺。镜海界的白昼火屑可以短时强化力量爆发；能在天海辨向的骨舟与通往昼皇宫的真实航线都是可直接争夺的高价值对象。白昼心是镜海界百年级重宝，能够影响真实位置的稳定，各方都会为它付出极高代价。

## 世界知识边界

玄曜大界公开知道“天外可能存在别的真实天地”，但普通修士并不知道镜海界具体规则，更不知道宁烬是否拥有任何跨世界永久能力。镜海界居民知道岸身/海身、照数、白昼火屑与白昼心等公共常识，但不知道玄曜大界的余门机制。

任何 NPC 都不能仅凭看见宁烬异常表现，就知道他可以永久带走世界可能性、以后递归复合，或知道私有触发条件。"""

CHARACTER = r"""# CHARACTER CARD 1｜Split Authority

## POWER CORE｜Frozen Authority

核心跨界非对称能力短名：余门。

宁烬可以亲自进入独立世界；当他真实卷入冲突、在不可回头的选择中承担后果，并亲手让该世界核心规则相关的一种“不属于玄曜大界的可能性”在自己身上成立后，离开时有机会永久保留这一条可能性。

边界：不能坐在原地隔空获得；不能只旁观、偷听或抢一件宝物就获得；每个独立世界最多带回一条核心可能性；它不会直接提升玄曜境界；必须按原世界逻辑使用；NPC 不会自动知道余门的隐藏永久性与触发条件。

前5章严格边界：余门尚未完成第一次永久带回。镜海界的“双真/双在”只能作为世界诱惑和后续可能性存在，不能在第1—5章让宁烬提前获得两个真实身体，也不能让旁人宣布他以后必然得到。

## HUMAN CORE｜Frozen Authority

宁烬，17岁。

开局精确力量位置｜主尺：玄曜九境｜精确位置：灵海3重

稳定牵引：爱钱、好胜、要面子、敢押注；对漂亮、危险、稀奇的人和物天然多看一眼；极度不喜欢已经抓到手里的高价值东西被别人拿走。他会合作，但不是责任型协调员，也不会因为“大家都需要”就自动承担公共治理责任。

他判断买卖很快，但不是永远理性最优。一个东西只要足够稀奇、足够值钱，或者能证明自己押对了，他会愿意把风险压得很高。面对镜离/澜生，他最初的合作理由是她们知道白昼心和镜海界的高价值对象，不是救世大义。

## Composition Boundary
Power Core 与 Human Core 原样并列。不要用悲惨身世证明人格；不要把贪钱自动解释成贫穷创伤；不要把余门写成系统UI、任务列表或职业流程。"""


def make_design() -> str:
    sections = {
        "growth_genome": "宁烬从灵海3重、只想拿黑门骨翻身开始；前5章不升级境界，主要增长是世界入口、实物奖励、关系与对异界规则的可利用理解。余门首次永久带回留到后续，不提前兑现。",
        "type_promise": "东方玄幻大世界 + 多世界探索 + 复合非对称能力成长。第一世界必须先让读者想去、想拿、想看两处真实身体怎样战斗；主角长期优势来自以后能把不同世界独有可能性永久复合。",
        "world_structure": "玄曜大界是主世界；第一异世界为镜海界。\n\n### Reader Release Map\n- 第1章｜触发：玄曜九境九重是公开主尺；宁烬灵海3重，裴照临灵海9重，天幕中的帝境能隔洲改变山河。\n- 第1章｜触发：黑门骨能打开的是真实异世界裂口，不是普通秘境。\n- 第3章｜触发：镜海界大海在天上；本地人通常有岸身与海身，两处都是真身，必须两处都死才算真正死亡。\n- 第4章｜触发：双身生命共享部分感知/意图，但两处真实身体的具体动作并非机械同步，因此战斗会形成上下两个独立位置。\n- 第5章｜触发：倒悬城的赌局和城市空间会同时使用岸厅/海厅，骨舟与真实航线都是进入昼皇宫的实物入口。",
        "world_pressure": "黑门骨争夺把玄曜高位势力、裴照临和镜海追兵同时拉进同一事件。进入镜海后，赫连枢的舰队追捕镜离/澜生，白昼心三日窗口让合作无法无限拖延。",
        "protagonist_model": "宁烬想赚钱、赢、拿稀奇东西，不爱把到手物让人。裴照临以真实数值优势压住他，镜离/澜生以不同脾气不断改变合作现场。",
        "relationships": "裴照临：灵海9重的长期Rival，本阶段真实强于宁烬。镜离：冷、骄傲、爱掌控。澜生：冲、爱冒险、会拆镜离台。两者是同一个生命的两处真实位置。",
        "plot_engine": "拍卖夺物 → 追杀跨界 → 世界规则冲击 → 上下双战场 → 倒悬城赌命夺取。事件推动优先靠抢、逃、打、赌、选择和实物结果。",
        "narrative_structure": "前5章是一个完整小故事：得到门 → 进世界 → 建立世界欲望 → 第一次利用世界规则赢 → 用规则赚钱并拿到通向更大争夺的入口。",
        "prose": "成熟中文男频玄幻；画面清、动作因果明确、对白自然、允许强奇观。避免工程/治理/登记语言，避免一章反复使用事实→短句总结→意义升华的漂亮二段论。",
        "dialogue": "宁烬说话带交易感但不能每句都谈价格；镜离短冷；澜生更冲、更爱拆台；裴照临少说、靠实力和实际选择形成压力。",
        "rhythm": "每章有可见事件与结果；普通路程压缩。章末可以切场景，但不能删除即时因果。",
        "theme": "人是否只能活成一个版本不是前5章要讲道理的主题；先让世界规则通过活人、战斗和争夺变得可欲望。",
        "strengths_risks": "强点：天上海、岸身/海身、主角长期可带走世界可能性。风险：为聪明翻盘临时发明方便规则；裴照临被降智；宁烬的贪钱口癖过度重复。",
    }
    return compose_design_content(sections)


LONG_PLAN = r"""## 第1—5章：黑门骨到倒悬城

具体发生：宁烬在九环天都拍卖场意外拿到黑门骨，被裴照临和高阶势力追杀；他拒绝低价交出，带镜离冲进正在合拢的门。进入镜海界后，他见到镜离/澜生这对同一生命的岸身与海身，与她们因白昼心和高价值对象临时合作。黑舰追杀中，他利用双身妖兽两处动作不同步的弱点，以灵海3重赢下第一场本地战并拿到白昼火屑。裴照临在倒悬城外断桥堵路；下一章必须从同一现场用既有追兵、倒悬建筑地形与镜离/澜生两处动作完成脱身，再进入赌命宴。宁烬利用城主两处真身作弊的事实反制赌局，拿到白昼火屑、骨舟和通往昼皇宫的真实航线；章末白昼心提前出世。

阶段结果：宁烬仍是玄曜九境的灵海3重；持有黑门骨、白昼火屑、骨舟、真实航线；与镜离/澜生形成利益合作；裴照临仍是灵海9重且真实更强。余门第一次永久可能性尚未结算。

叙事功能：让多世界核心卖点通过一个可记住的真实异世界成立，并证明主角能把陌生世界规则转成自己的胜负/收益，但不提前拿到最终“双真”。

推向下一块：白昼心提前出世，所有势力冲向昼皇宫。"""

PLANS = {
1: r"""## 第1章：天都上空的黑门骨
具体剧情：九环天都的天外珍宝拍卖中，街心天幕同时映着帝境战场。天外商会拍出能打开真实异世界裂口的黑门骨，灵海9重的裴照临准备以家势与修为压住竞价；帝境级巨掌突然从天幕裂口探入争夺，黑门骨却在混乱中钉进灵海3重的宁烬掌心。宁烬明知所有人都会来抢仍不松手，黑骨裂开后让他第一次看见门后悬在天空的白海。
结果 / 状态变化：宁烬取得并实际持有黑门骨；全场见证黑门骨落入他手，裴照临把他从可忽略的穷修士重新估价为必须亲自夺回黑门骨的人。宁烬仍是灵海3重，余门未完成任何永久带回。
叙事功能：一章内建立主世界尺度、精确力量差、黑门骨价值与主角敢拿不放的性格。
结尾推动：黑缝中伸出镜离的手，她要求宁烬把门还给她，并说可以带他去一个“死人也能继续活”的地方。""",
2: r"""## 第2章：追进正在合拢的门
具体剧情：宁烬带着黑门骨在九环天都的悬街、天舟与城环间逃亡，高阶护卫与裴照临追来；裴照临提出十万灵玉和上等洞府换门骨。宁烬不是不爱钱，而是判断这价格远低于一整座真实异界，因此拒绝。镜离从裂缝中出来，后方三名镜海黑甲骑士追到；门正在合拢，宁烬主动抓住机会冲进门内，裴照临也追向裂缝但被门的异力阻挡/甩开，不能无因果与宁烬并肩进入。
结果 / 状态变化：宁烬成功跨入镜海界，黑门骨仍在他手；裴照临确认宁烬与门之间存在自己没有的特殊适配，但不知道余门机制。宁烬仍是灵海3重。
叙事功能：把“我拿到异界之门”迅速兑现成真正跨世界，而不是任务说明。
结尾推动：宁烬发现海水在天上，白海里有一个与自己一模一样的倒影/位置正在看他，但此时不能把它写成他已经获得第二真身。""",
3: r"""## 第3章：镜海界的两个自己
具体剧情：宁烬进入镜海界，被本地人当成只有一处真实身体的“单身者”。镜离的海身澜生从天海出现；镜离冷、澜生冲，两人共享生命与记忆却会互相拆台。通过守卫/铜镜/现场动作让读者直接看懂：本地人的岸身和海身都是真的，杀一处不算死。镜离说明白昼心三日后出现、赫连枢的黑舰正在封锁相关区域；宁烬因为她们知道白昼心和高价值对象的位置，选择合作，不是因为救世责任。
结果 / 状态变化：宁烬与镜离/澜生建立有条件的利益合作；读者与宁烬明确理解镜海界最核心的“双处真实”规则，但宁烬自己仍只有一处真实身体，没有获得双真。
叙事功能：让异世界本身产生强烈阅读欲望，并让两个性格不同的“同一个人”成为活角色而非设定说明器。
结尾推动：天海与陆地同时出现赫连枢的黑色舰队，公开命令镜离留下海身，并要求活捉这个没有第二条命的外界人。""",
4: r"""## 第4章：上下两场战斗
具体剧情：黑舰从地面与天海同时追杀。宁烬被一头岸身/海身同时存在的双身妖兽夹击；他发现两处共享感知与杀意，但真实身体的动作并非机械同步。宁烬利用倒影判断上方落点，故意诱使岸身扑杀，让妖兽自己的两处力量在同一薄弱位置互相制造破口，再以石矛完成击杀；不要临时发明只有这场战斗才有的万能“照线”。镜离/澜生与追兵也在上下两处同时行动。
结果 / 状态变化：宁烬以灵海3重击杀本地二照妖兽并取得一枚白昼火屑；镜离第一次把部分背后交给他，本地见证者对这个“单身者”重新估价。宁烬仍是灵海3重，也仍没有第二真身。
叙事功能：把镜海规则第一次转成具体战斗爽点，并保持裴照临的数值压迫。
结尾推动：通向倒悬城的浮桥被裴照临一剑斩断；裴照临以灵海9重亲自堵住城门方向，剑指宁烬索要黑门骨，后方追兵仍在逼近。""",
5: r"""## 第5章：倒悬城的赌命宴
具体剧情：必须从第4章裴照临堵断桥、追兵逼近的同一即时现场开始。宁烬不能靠临时“城内禁杀”获救；他利用已经存在的后方追兵、倒悬城外墙/石檐/城门空间以及镜离/澜生上下两个真实位置的动作，完成一个具体可见的脱身并进入倒悬城，裴照临仍保持明显更强且继续形成压力。城内赌命宴上下各有一厅，宁烬通过镜离/澜生合席观察城主岸身/海身作弊；他故意输几轮让城主放松，在最后关键局把作弊事实公开反制，不新增“正好只为这一次翻盘”的神秘判负规则。
结果 / 状态变化：宁烬赢得通往昼皇宫的真实航线、一枚更大的白昼火屑和能在天海辨向的骨舟；裴照临亲眼看到宁烬不是只靠运气。镜离/澜生与宁烬的合作加深但仍以各自欲望为先。宁烬仍是灵海3重，余门第一次永久带回仍未结算。
叙事功能：修复章间即时连续性，并把镜海双身规则从“能打”扩成“能赌、能骗、能赚钱”的世界玩法。
结尾推动：白昼心提前出世，两轮太阳同时出现，倒悬城/所有势力被迫立即转向昼皇宫。""",
}


def initial_status() -> str:
    return r"""当前已完成第0章。

## ACTIVE SCENE STATE

地点：九环天都天外珍宝拍卖场。
在场人物：宁烬；裴照临；天外商会拍卖者与各方来客。
即时伤势：无。
手中关键物品：旧宅契与少量灵玉；黑门骨尚未落入任何人手。
当前敌人或追兵：无明确个人追兵；拍卖尚未失控。
当前倒计时：无。
当前主动目标：宁烬想从天外珍宝拍卖里找到一个足以翻身的高价值机会。

## PERSISTENT CANON

### Power / Capability

Current Power Position｜主尺：玄曜九境｜精确位置：灵海3重
- 余门尚未完成任何跨世界永久获得。

### Active Relationships

裴照临｜只知道宁烬是场中不起眼的低阶修士｜同代强者/潜在竞争者｜尚未形成私人关系｜灵海9重，真实实力显著高于宁烬。

### Identity / Access

- 宁烬是17岁灵海3重年轻修士，没有高位宗门/古族身份可替他压住拍卖场。

### Knowledge / Enemy State

- 宁烬知道天外遗物可能极值钱，但不知道镜海界规则。
- 没有人公开知道宁烬拥有“余门”这项私有能力结构。

### World State

- 九环天都正在举行天外珍宝拍卖；天幕可映照远方高位战场。

### Tracked Assets

旧宅契｜宁烬｜随身｜可变卖但远不足以参与高阶宝物竞价｜开局已有。

## RECENT SUMMARIES

NONE

## OPEN PROMISES

- 黑门骨将成为第一个真实跨世界入口。
- 镜海界会让“一人两处都是真的”成为可见世界规则，但宁烬前5章不能提前永久获得双真。"""


def base_book() -> str:
    return compose_book_content({
        "design": make_design(),
        "long_plan": LONG_PLAN,
        "small_plan": "\n\n".join(PLANS[n] for n in range(1, 6)),
        "status": initial_status(),
    })


def book_path(root: Path) -> Path:
    return root / "BOOK.md"


def book(root: Path) -> str:
    return read(book_path(root))


def sections(root: Path) -> dict[str, str]:
    return parse_book_sections(book(root))


def recent(root: Path) -> str:
    mem = parse_canon_memory(sections(root)["status"])
    return mem.get("recent_summaries", "").strip()


def previous(root: Path, n: int) -> str:
    if n <= 1:
        return ""
    return read(root / "chapters" / f"chapter-{n-1:04d}.md").strip()


def run_dir(root: Path, n: int) -> Path:
    d = root / "runs" / f"chapter-{n:04d}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_snapshot(root: Path, n: int, label: str) -> None:
    write(run_dir(root, n) / f"BOOK_{label}.md", book(root))


def generate_control(call_log: list[dict]) -> None:
    CONTROL.mkdir(parents=True, exist_ok=True)
    (CONTROL / "chapters").mkdir(exist_ok=True)
    if not book_path(CONTROL).is_file():
        write(book_path(CONTROL), base_book())
    for n in range(1, 6):
        d = run_dir(CONTROL, n)
        save_snapshot(CONTROL, n, "before")
        common = dict(
            book_content=book(CONTROL),
            world_vision=WORLD,
            world_expansions="",
            character_card=CHARACTER,
            current_long_block=LONG_PLAN,
            previous_chapter_text=previous(CONTROL, n),
            current_chapter_plan=PLANS[n],
            recent_summaries=recent(CONTROL),
            chapter_number=n,
            creative_direction="冻结同一《我身藏诸界》前五章 Authority；当前 production sequential full-chain control。不得新增未批准机制。",
        )
        dp = generate_prompt(mode="director", template="", current_outline="", **common)
        write(d / "director_prompt.md", dp)
        dr = run_acp(d / "director_prompt.md", d / "director_acp.json", d / "director_response.md", model="gpt-5.6-luna", effort="high", label=f"batch5-full-control-ch{n:02d}-director", call_log=call_log)

        cp = generate_prompt(mode="context_curator", template="", current_outline=dr, gbrain_inspiration="", **common)
        write(d / "curator_prompt.md", cp)
        cu = run_acp(d / "curator_prompt.md", d / "curator_acp.json", d / "curator_response.md", model="gpt-5.6-luna", effort="high", label=f"batch5-full-control-ch{n:02d}-curator", call_log=call_log)

        pp = generate_prompt(mode="primary_writer", template="", current_outline=dr, gbrain_inspiration="", curated_context=cu, curator_response=cu, **common)
        write(d / "primary_prompt.md", pp)
        pr = run_acp(d / "primary_prompt.md", d / "primary_acp.json", d / "primary_response.md", model="gpt-5.6-terra", effort="high", label=f"batch5-full-control-ch{n:02d}-primary", call_log=call_log)
        pbody = extract_primary_draft(pr).strip()
        validate_chapter_body_for_save(pbody)
        write(d / "primary_body.md", pbody)

        rp = generate_prompt(mode="authority_reviser", template="", current_outline=dr, curated_context=cu, curator_response=cu, primary_draft=pbody, primary_writer_response=pr, **common)
        write(d / "reviser_prompt.md", rp)
        rr = run_acp(d / "reviser_prompt.md", d / "reviser_acp.json", d / "reviser_response.md", model="gpt-5.6-luna", effort="high", label=f"batch5-full-control-ch{n:02d}-reviser", call_log=call_log)
        final = extract_primary_draft(rr).strip()
        validate_chapter_body_for_save(final)
        write(d / "final_body.md", final)
        write(CONTROL / "chapters" / f"chapter-{n:04d}.md", final)

        final_fact = extract_primary_fact_summary(rr).strip()
        sp = generate_prompt(mode="state_delta", template="", book_content=book(CONTROL), recent_summaries=recent(CONTROL), chapter_number=n, chapter_prose=final, chapter_fact_summary=final_fact)
        write(d / "state_prompt.md", sp)
        sr = run_acp(d / "state_prompt.md", d / "state_acp.json", d / "state_response.md", model="gpt-5.6-luna", effort="low", label=f"batch5-full-control-ch{n:02d}-state", call_log=call_log)
        updated = apply_state_delta_to_book(book(CONTROL), n, sr)
        validate_book_content_for_save(updated)
        write(book_path(CONTROL), updated)
        save_snapshot(CONTROL, n, "after")
        print(f"CONTROL CH{n} DONE final_chars={len(final)}", flush=True)

    combined = "\n\n".join(read(CONTROL / "chapters" / f"chapter-{n:04d}.md").strip() for n in range(1, 6))
    write(CONTROL / "CHAPTERS_01_05.md", combined)


def control_packets_for_batch() -> list[str]:
    packets = []
    for n in range(1, 6):
        d = run_dir(CONTROL, n)
        dr = read(d / "director_response.md").strip()
        cu = read(d / "curator_response.md").strip()
        # Build a current production Primary prompt without Control prose. We keep the
        # exact Director/Curator authority packet but remove previous-chapter prose so
        # the batch writer must continue from its own immediately preceding chapter.
        pp = generate_prompt(
            mode="primary_writer",
            template="",
            book_content=base_book(),
            world_vision=WORLD,
            world_expansions="",
            character_card=CHARACTER,
            current_long_block=LONG_PLAN,
            previous_chapter_text="",
            current_outline=dr,
            current_chapter_plan=PLANS[n],
            recent_summaries="",
            chapter_number=n,
            creative_direction="冻结 Control 的 Director/Curator Authority Packet；Batch Primary 只改变五章连续写作窗口。",
            gbrain_inspiration="",
            curated_context=cu,
            curator_response=cu,
        )
        marker = "# 页面当前输入（章节运行期上下文）"
        idx = pp.find(marker)
        runtime_inputs = pp[idx:] if idx >= 0 else pp
        packets.append(f"# CHAPTER {n} FROZEN RUNTIME PACKET\n\n{runtime_inputs}")
    return packets


def parse_batch_primary(text: str) -> dict[int, tuple[str, str]]:
    result: dict[int, tuple[str, str]] = {}
    pat = re.compile(r"(?ms)^# BATCH CHAPTER ([1-5])\s*$\n(.*?)(?=^# BATCH CHAPTER [1-5]\s*$|\Z)")
    for m in pat.finditer(text):
        n = int(m.group(1))
        block = m.group(2)
        prose = re.search(r"(?ms)^## 正式正文\s*$\n(.*?)(?=^## 章节事实摘要\s*$|\Z)", block)
        facts = re.search(r"(?ms)^## 章节事实摘要\s*$\n(.*)$", block)
        if not prose or not facts:
            raise RuntimeError(f"Batch Primary chapter {n} missing prose/facts")
        body = prose.group(1).strip()
        fact = facts.group(1).strip()
        validate_chapter_body_for_save(body)
        result[n] = (body, fact)
    if set(result) != set(range(1, 6)):
        raise RuntimeError(f"Batch Primary chapters parsed: {sorted(result)}")
    return result


def generate_batch_primary(call_log: list[dict]) -> dict[int, tuple[str, str]]:
    TREATMENT.mkdir(parents=True, exist_ok=True)
    packets = control_packets_for_batch()
    prompt = DEFAULT_PROMPT_TEMPLATES["primary_writer"].strip() + r"""

# FORMAL BATCH-5 PRIMARY EXPERIMENT

你现在不是分别执行五次，而是在**一次连续写作会话中**完成第1—5章 Primary Draft。五份 FROZEN RUNTIME PACKET 都来自当前 production 的 Luna Director + Luna Curator；它们的事件、结果、Authority、Reader Release、未知边界仍逐章有效。Batch 只改变 Writer 的短中程视野，不授权你重规划。

严格规则：
1. 按 1→5 顺序写。写完第N章后，你刚写出的正式正文就是第N+1章最新 CANON PROSE；未来 Packet 不是已发生事实。
2. 每章只能完成自己的 Chapter Mission / Plan；绝不因为你看得到后面的 Packet 就提前兑现下一章事件、奖励、揭晓或能力。
3. 第4→5章尤其遵守 Chapter Handoff Continuity：第4章若以裴照临堵断桥/追兵逼近结束，第5章必须从同一即时现场以已有角色、追兵、地形、镜海双身动作完成具体 bridge；不得临时发明“城内禁杀/强敌忽然放行/传送”等方便规则。
4. 如果后一个 Packet 中存在只能由 Control 版本前文成立、但你自己的前文并未成立的具体实现细节，不要为了对齐 Control 补造事实；服从你已经写出的正文 + Frozen Mission，走最近合法因果。
5. 宁烬第1—5章始终是玄曜九境的灵海3重；不能提前获得双真/双在永久能力。裴照临灵海9重，真实更强。
6. 保留成熟中文男频正文的连续感；不要在章与章之间重新介绍同一规则，也不要把五章写成五篇独立短篇。

固定输出格式，恰好五个一级标题：
# BATCH CHAPTER 1
## 正式正文
...
## 章节事实摘要
...
# BATCH CHAPTER 2
...
一直到 # BATCH CHAPTER 5。
不要输出总审计、总总结或写作说明。

""" + "\n\n".join(packets)
    write(TREATMENT / "batch_primary_prompt.md", prompt)
    resp = run_acp(TREATMENT / "batch_primary_prompt.md", TREATMENT / "batch_primary_acp.json", TREATMENT / "batch_primary_response.md", model="gpt-5.6-terra", effort="high", label="batch5-full-treatment-primary-batch5", call_log=call_log)
    parsed = parse_batch_primary(resp)
    for n, (body, fact) in parsed.items():
        d = run_dir(TREATMENT, n)
        write(d / "batch_primary_body.md", body)
        write(d / "batch_primary_fact.md", fact)
    return parsed


def generate_treatment(call_log: list[dict]) -> None:
    TREATMENT.mkdir(parents=True, exist_ok=True)
    (TREATMENT / "chapters").mkdir(exist_ok=True)
    if not book_path(TREATMENT).is_file():
        write(book_path(TREATMENT), base_book())
    batch = generate_batch_primary(call_log)
    for n in range(1, 6):
        d = run_dir(TREATMENT, n)
        save_snapshot(TREATMENT, n, "before")
        dr = read(run_dir(CONTROL, n) / "director_response.md").strip()
        cu = read(run_dir(CONTROL, n) / "curator_response.md").strip()
        primary_body, primary_fact = batch[n]
        common = dict(
            book_content=book(TREATMENT),
            world_vision=WORLD,
            world_expansions="",
            character_card=CHARACTER,
            current_long_block=LONG_PLAN,
            previous_chapter_text=previous(TREATMENT, n),
            current_outline=dr,
            current_chapter_plan=PLANS[n],
            recent_summaries=recent(TREATMENT),
            chapter_number=n,
            creative_direction="Formal Batch-5 Primary treatment；Director/Curator packets frozen from Control，Reviser/State use Treatment rolling Canon。不得新增未批准机制。",
        )
        rp = generate_prompt(mode="authority_reviser", template="", curated_context=cu, curator_response=cu, primary_draft=primary_body, primary_writer_response=f"# 正式正文\n\n{primary_body}\n\n# 章节事实摘要\n\n{primary_fact}", **common)
        write(d / "reviser_prompt.md", rp)
        rr = run_acp(d / "reviser_prompt.md", d / "reviser_acp.json", d / "reviser_response.md", model="gpt-5.6-luna", effort="high", label=f"batch5-full-treatment-ch{n:02d}-reviser", call_log=call_log)
        final = extract_primary_draft(rr).strip()
        validate_chapter_body_for_save(final)
        write(d / "final_body.md", final)
        write(TREATMENT / "chapters" / f"chapter-{n:04d}.md", final)
        final_fact = extract_primary_fact_summary(rr).strip()
        sp = generate_prompt(mode="state_delta", template="", book_content=book(TREATMENT), recent_summaries=recent(TREATMENT), chapter_number=n, chapter_prose=final, chapter_fact_summary=final_fact)
        write(d / "state_prompt.md", sp)
        sr = run_acp(d / "state_prompt.md", d / "state_acp.json", d / "state_response.md", model="gpt-5.6-luna", effort="low", label=f"batch5-full-treatment-ch{n:02d}-state", call_log=call_log)
        updated = apply_state_delta_to_book(book(TREATMENT), n, sr)
        validate_book_content_for_save(updated)
        write(book_path(TREATMENT), updated)
        save_snapshot(TREATMENT, n, "after")
        print(f"TREATMENT CH{n} DONE final_chars={len(final)}", flush=True)
    combined = "\n\n".join(read(TREATMENT / "chapters" / f"chapter-{n:04d}.md").strip() for n in range(1, 6))
    write(TREATMENT / "CHAPTERS_01_05.md", combined)


def diff_metrics(a: str, b: str) -> dict:
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    opcodes = sm.get_opcodes()
    changed = [op for op in opcodes if op[0] != "equal"]
    changed_a = sum(i2-i1 for tag, i1, i2, j1, j2 in changed)
    changed_b = sum(j2-j1 for tag, i1, i2, j1, j2 in changed)
    return {
        "similarity": round(sm.ratio(), 4),
        "edit_blocks": len(changed),
        "changed_chars_primary": changed_a,
        "changed_chars_final": changed_b,
    }


def stage_sum(log: list[dict], contains: str) -> float:
    total = 0.0
    for row in log:
        if contains in row["label"]:
            val = row.get("wall_seconds") or row.get("outer_wall_seconds") or 0
            total += float(val or 0)
    return total


def analyze_metrics(call_log: list[dict]) -> dict:
    revisions = {"control": {}, "treatment": {}}
    for n in range(1, 6):
        cpri = read(run_dir(CONTROL, n) / "primary_body.md").strip()
        cfin = read(run_dir(CONTROL, n) / "final_body.md").strip()
        tpri = read(run_dir(TREATMENT, n) / "batch_primary_body.md").strip()
        tfin = read(run_dir(TREATMENT, n) / "final_body.md").strip()
        revisions["control"][str(n)] = diff_metrics(cpri, cfin)
        revisions["treatment"][str(n)] = diff_metrics(tpri, tfin)
    control_primary = stage_sum(call_log, "control-ch") - stage_sum(call_log, "control-ch")  # overwritten below
    sums = {
        "control_director": sum(float(r.get("wall_seconds") or 0) for r in call_log if "control-ch" in r["label"] and r["label"].endswith("-director")),
        "control_curator": sum(float(r.get("wall_seconds") or 0) for r in call_log if "control-ch" in r["label"] and r["label"].endswith("-curator")),
        "control_primary": sum(float(r.get("wall_seconds") or 0) for r in call_log if "control-ch" in r["label"] and r["label"].endswith("-primary")),
        "control_reviser": sum(float(r.get("wall_seconds") or 0) for r in call_log if "control-ch" in r["label"] and r["label"].endswith("-reviser")),
        "control_state": sum(float(r.get("wall_seconds") or 0) for r in call_log if "control-ch" in r["label"] and r["label"].endswith("-state")),
        "treatment_batch_primary": sum(float(r.get("wall_seconds") or 0) for r in call_log if r["label"] == "batch5-full-treatment-primary-batch5"),
        "treatment_reviser": sum(float(r.get("wall_seconds") or 0) for r in call_log if "treatment-ch" in r["label"] and r["label"].endswith("-reviser")),
        "treatment_state": sum(float(r.get("wall_seconds") or 0) for r in call_log if "treatment-ch" in r["label"] and r["label"].endswith("-state")),
    }
    sums["control_stage_sum"] = sum(sums[k] for k in ("control_director","control_curator","control_primary","control_reviser","control_state"))
    # For causal isolation Treatment reuses frozen D/C packets. A real implementation
    # would still owe their cost somehow, so report a comparable stage-cost-equivalent
    # sum without pretending this is a proven live critical path.
    sums["treatment_observed_after_frozen_packets"] = sums["treatment_batch_primary"] + sums["treatment_reviser"] + sums["treatment_state"]
    sums["treatment_stage_cost_equivalent_with_same_DC"] = sums["control_director"] + sums["control_curator"] + sums["treatment_batch_primary"] + sums["treatment_reviser"] + sums["treatment_state"]
    return {"stage_sums_seconds": {k: round(v,3) for k,v in sums.items()}, "reviser_edit_metrics": revisions}


def blind_judges(call_log: list[dict]) -> None:
    control_text = read(CONTROL / "CHAPTERS_01_05.md")
    treatment_text = read(TREATMENT / "CHAPTERS_01_05.md")
    story_prompt = f"""你是独立中文男频正文盲评员。下面版本A/B来自同一世界、同一人物、同一前5章计划；不知道生成拓扑。只比较最终正式正文，不根据长度奖励任何一方。\n\n重点判断：连续读下去的欲望、章间因果、宁烬是否像具体的人、镜海界奇观与规则是否一眼可懂、动作因果、对白、爽点/Reward落地、裴照临是否保持真实压迫、临时方便规则/AI式总结、作为100章以上长篇底稿的潜力。\n\n必须明确总冠军 A/B/TIE，并列出最关键的3—6条证据；没有差异就说TIE。不要猜哪版是Batch。\n\n# VERSION A\n\n{control_text}\n\n# VERSION B\n\n{treatment_text}\n"""
    write(EXP / "judge_story_prompt.md", story_prompt)
    run_acp(EXP / "judge_story_prompt.md", EXP / "judge_story_acp.json", EXP / "JUDGE_STORY.md", model="gpt-5.6-luna", effort="high", label="batch5-full-judge-story", call_log=call_log)

    authority_prompt = f"""你是独立 TGN Authority / Continuity 盲审。版本A/B标签与生成方式无关；只依据冻结 World、Character、前5章 Plan 审最终正文。\n\n逐版检查实际存在的硬问题：\n- 是否改变第1—5章主要事件/Reward/胜负；\n- 宁烬是否始终灵海3重、未提前获得双真永久能力；\n- 裴照临是否仍灵海9重且真实更强；\n- NPC 是否偷知余门隐藏永久机制；\n- 第4→5章即时堵路是否有具体因果 bridge；\n- 是否为翻盘临时发明只服务当前局面的世界规则；\n- State/持有物/伤势/关系是否跨章互相矛盾；\n- 是否出现后章事实提前泄漏。\n\n不要制造问题。分别给 HARD PROBLEMS 数量与证据，再给 Authority 更可靠的一版 A/B/TIE。最后单独回答：如果版本存在“预写后续章节导致前一章最终 Reviser 修改后，后文仍引用旧事实”的 stale 痕迹，具体指出；没有就写 NONE。\n\n# FROZEN WORLD\n{WORLD}\n\n# FROZEN CHARACTER\n{CHARACTER}\n\n# FROZEN PLANS\n{"\n\n".join(PLANS[n] for n in range(1,6))}\n\n# VERSION A\n{treatment_text}\n\n# VERSION B\n{control_text}\n"""
    write(EXP / "judge_authority_prompt.md", authority_prompt)
    run_acp(EXP / "judge_authority_prompt.md", EXP / "judge_authority_acp.json", EXP / "JUDGE_AUTHORITY.md", model="gpt-5.6-terra", effort="high", label="batch5-full-judge-authority", call_log=call_log)


def main() -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    write(EXP / "FROZEN_WORLD.md", WORLD)
    write(EXP / "FROZEN_CHARACTER.md", CHARACTER)
    write(EXP / "BOOK_BASE.md", base_book())
    write(EXP / "FROZEN_PLANS.md", "\n\n".join(PLANS[n] for n in range(1,6)))
    validate_book_content_for_save(base_book())
    call_log: list[dict] = []
    generate_control(call_log)
    generate_treatment(call_log)
    blind_judges(call_log)
    dump(EXP / "CALL_LOG.json", call_log)
    metrics = analyze_metrics(call_log)
    dump(EXP / "METRICS.json", metrics)
    print(json.dumps(metrics["stage_sums_seconds"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
