from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
OLD = ROOT / "books" / "real-exp-multiverse-compound-asymmetry-10ch-20260831-v1"
OUT = ROOT / "books" / "real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"
ACP_RUNNER = ROOT / "temps" / "acp_text_runner.py"

sys.path.insert(0, str(ROOT / "src"))

from story_mvp.batch_runtime import (
    BatchWindow,
    apply_batch_delta,
    build_batch_delta_reviser_prompt,
    build_batch_primary_prompt,
    extract_batch_outline_plans,
    parse_batch_delta_response,
    parse_batch_primary_response,
)
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.long_form_evolution import compile_current_character
from story_mvp.power_ruler import validate_world_expansion_ruler
from story_mvp.prompts import generate_prompt, parse_canon_memory
from story_mvp.storage import (
    DESIGN_SECTION_TITLES,
    apply_state_delta_to_book,
    compose_book_content,
    compose_design_content,
    parse_book_sections,
    validate_book_content_for_save,
)
from story_mvp.story_event_obligations import validate_book_registry_against_story_program


CREATIVE_STATE = {
    "world_vision": {"status": "author_approved"},
    "character_card": {"status": "author_approved"},
    "proposal": {"status": "author_approved"},
}

HORIZONS = [
    {
        "start": 11,
        "end": 20,
        "shadow": "巨尸骨骼拼成大陆；入夜后，行走其上的人旧伤鼓起，裂开的肋骨长出新的肺叶，断掉的手臂生出带齿骨刃。",
        "author_direction": "作者已决定宁烬本轮进入黑门骨显示的巨尸骨陆。把它做成独立运行的东方玄幻异世界：旧伤会在特定夜相下长成新的身体器官/结构，但不要预先为未知主角设计奖励。世界自身要有会生活、会爱恨、会争夺自己命运的人。脑洞大胆，但规则第一次出现必须一眼能懂。",
    },
    {
        "start": 21,
        "end": 30,
        "shadow": "无边兵器荒原；无主长枪、断剑、巨斧自行拔起，拖着锈火与风沙，追杀那些早已逃远的旧主人仇敌。",
        "author_direction": "作者已决定宁烬本轮进入黑门骨显示的无主兵荒原。把它做成独立运行的东方玄幻异世界：兵器与未完成之事有真正因果，但不要预先为未知主角设计奖励。兵器不是装备商店，应该有主人、遗愿、背叛、继承、仇敌和会自己改变局面的活人。脑洞大胆，但底层规则用普通话即可复述。",
    },
    {
        "start": 31,
        "end": 40,
        "shadow": "一座没有外墙的无边宫殿；每一扇门后，都悬着另一轮太阳。",
        "author_direction": "作者已决定宁烬本轮进入黑门骨显示的无墙万门宫殿。把它做成独立运行的东方玄幻异世界：门、距离、内外或太阳之间存在一条真正改变生活与战争的简单规则，但不要预先为未知主角设计奖励。这里应像一个文明而不是迷宫关卡，有常住者、关系、欲望、城邦/家族/异族与自己的大事。脑洞尽量大，首读语义仍要直接。",
    },
]

CALL_LOG: list[dict[str, object]] = []


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def dump(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def extract_from_heading(text: str, heading: str) -> str:
    pos = text.find(heading)
    return text[pos:].strip() if pos >= 0 else text.strip()


def strip_top_heading(text: str, heading: str) -> str:
    clean = extract_from_heading(text, heading)
    if clean.startswith(heading):
        clean = clean[len(heading):].lstrip("\r\n ")
    return clean.strip()


def run_acp(*, label: str, model: str, effort: str, prompt: str, folder: Path, timeout: int = 7200) -> str:
    folder.mkdir(parents=True, exist_ok=True)
    prompt_path = folder / "prompt.md"
    output_path = folder / "response.md"
    write(prompt_path, prompt)
    if output_path.is_file() and output_path.stat().st_size > 20:
        text = read(output_path)
        CALL_LOG.append({"label": label, "model": model, "effort": effort, "reused": True, "wall_seconds": 0.0, "chars": len(text)})
        return text
    started = time.perf_counter()
    cmd = [
        sys.executable,
        str(ACP_RUNNER),
        "--model", model,
        "--effort", effort,
        "--prompt-file", str(prompt_path),
        "--output", str(output_path),
        "--timeout", str(timeout),
    ]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", timeout=timeout + 120)
    wall = time.perf_counter() - started
    write(folder / "runner_stdout.txt", proc.stdout)
    write(folder / "runner_stderr.txt", proc.stderr)
    if proc.returncode != 0:
        raise RuntimeError(f"{label} ACP failed: {proc.returncode}\n{proc.stdout}\n{proc.stderr}")
    text = read(output_path)
    CALL_LOG.append({"label": label, "model": model, "effort": effort, "reused": False, "wall_seconds": round(wall, 3), "chars": len(text)})
    print(json.dumps(CALL_LOG[-1], ensure_ascii=False), flush=True)
    return text


def safe_gbrain(mode: str, folder: Path, **kwargs: str) -> str:
    cache = folder / "gbrain.json"
    if cache.is_file():
        data = json.loads(read(cache))
        return str(data.get("result") or "")
    try:
        result = retrieve_gbrain(mode=mode, **kwargs)
        dump(cache, result)
        return str(result.get("result") or "")
    except Exception as exc:
        dump(cache, {"status": "unavailable", "error": str(exc), "result": "（本次 GBrain 检索不可用；允许空结果，不补位。）"})
        return "（本次 GBrain 检索不可用；允许空结果，不补位。）"


def root_world() -> str:
    return """# PROTAGONIST-BLIND WORLD VISION

玄曜大界由九重天、三十六天洲、数百王朝、宗门与古族构成。天洲间有跨洲天舟与天外商路；王境以上可横渡远空，圣境与帝境能把战斗影响扩到山河、天域。天外遗物与真实世界裂口极少见，但已经进入顶层强者和天外商会的争夺视野。

## 普通人的生活与上升
普通修士从锻体、通脉进入灵海后才真正具备独立远行与争夺天洲级机缘的资格。大多数人依靠宗门、古族、王朝、商会、武馆或天舟商路往上走；天外遗物、古代遗迹、跨洲宝会会把原本接触不到的强者与资源拉到同一场合。

## 力量体系与正常值
玄曜大界主流公开力量为九境九重：锻体、通脉、灵海、神台、天门、王、圣、帝、天外；每境一至九重。境界是公开位置尺，不是胜负公式，器物、技法、经验、环境与异常能力都能制造越级结果。

### 精确力量主尺｜Frozen Grammar
主尺类型：大境界+数字子级
主尺名称：玄曜九境九重
精确位置格式：{大境界}{N}重
数字精度规则：每境1—9
当前可见范围：灵海1—9；神台1—9；天门1—9；王境1—9；圣境1—9；帝境1—9；天外境1—9
当前大档位：锻体境、通脉境、灵海境、神台境、天门境、王境、圣境、帝境、天外境

## 社会现实与身份
天洲大城公开尊重力量、资产、出身与已经被见证的战绩，但高位人物不会因为一次奇观自动知道他人的隐藏机制。天外商会以宝物、路线和跨洲交易闻名；古族与王朝更看重长期力量、血统与可控制资源。公开重新估价可以直接改变报价、招揽、敌意与待遇。

## 世界里真正值钱、值得想要的东西
高阶功法、神兵、异兽、天外火种、跨洲坐骑、王境以上传承、天外遗物与能打开新世界/新空间的真实媒介都足以引发争夺。最稀有的天外遗物未必提供单纯力量，也可能改变一个人原本被天地限制的行动方式。

## 世界知识边界
玄曜修士知道天外存在不能完全用本界解释的遗物和裂口，但普通人不知道诸界数量、来源与完整规则。一个人通常只有一个真实身体、一个魂与一个真实坐标；幻术、傀儡和分身都被视为替代物，而不是第二个同等真身。

## 世界正在发生的大事
九环天都的天外珍宝拍卖刚因黑门骨与异界裂口引发大乱；天外商会、裴氏与其它高位势力都开始重新估价这件遗物与相关见证者。更远天洲仍有自己的战争、宝会、宗门竞争和古族冲突，不围绕某个单一人物运转。

## 值得进入的地点、奇观与未知
九环天都、跨洲天舟、天外遗迹与真实异界裂口仍是当前最直接的世界外缘。黑门骨曾映出三个完全不同的世界影子，但这些世界自身是什么、为何如此、里面的人怎么生活仍未被玄曜大界解释。
"""


def character_card() -> str:
    return """# CHARACTER AUTHORITY

## POWER CORE｜Frozen Authority

后台短名：余门。宁烬亲自进入一个独立真实世界、卷入真实冲突并在不可回头的选择中承担后果后，可以永久带走一条该世界原本允许、而玄曜大界原本不允许的核心可能性。它不是简单复制功法或拿到宝物：带回的是宁烬本人以后可以成立的一种新现实权限。

触发边界：必须亲身进入；必须有真实冲突与选择；不能靠旁观、偷听或单纯抢一件物品获得；每个独立世界最多带回一条核心可能性；它本身不直接免费提升玄曜主境界；观察者不能直接看见“余门”或知道永久性/内部触发。

开局精确力量位置｜主尺：玄曜九境九重｜精确位置：灵海3重

长期成长方向：新的世界可能性可以继续加入，并与旧可能性产生单项做不到的复合。连续获得并递归复合高价值 Asymmetry 是主角的长期叙事特权；普通 Rival 可以更强、拿走主角错失的宝物、拥有自己的绝技/神兵，但不自动复制一套并行的递归异常栈。

## HUMAN CORE｜Frozen Authority

宁烬，十七岁。稳定牵引是钱、赢、面子、稀奇罕见之物、危险又漂亮的人或东西，以及“既然有机会碰到，为什么只拿一半”的贪心。他敢押、反应快、讨厌被别人替自己决定价值，也不喜欢明明能争却先替自己找退路。

他不是责任/治理型主角。聪明不等于替所有人协调利益；他可以救人、结盟、讲条件或暂时退让，但这些必须来自具体欲望、关系、胜负和眼前代价。爱钱已经成立后，不靠“值多少钱 / 这才叫买卖 / 我不喜欢亏”反复刷同一口癖；让好胜、好奇、面子、身体危险感、具体关系与偶尔不理性的偏爱自然进入选择。

## Composition Boundary

Frozen Power 与 Frozen Human 不互相后验合理化。后续 Power/Asset/Relationship/Identity/Knowledge 只从已发生 Canon 向前追加；人物可以发展，但不能因为新世界最适合某种性格就反向重写宁烬。
"""


def starting_story_program() -> str:
    return """# STORY PROGRAM

## 当前 Re-Collision
前十章已经完成第一轮：宁烬从玄曜大界进入镜海界，并把“一人可以同时拥有两个同等真实位置”的世界可能性永久带回；返回天都后完成公开证明。后续不再证明“能不能带回”，而要证明不同世界的可能性会怎样真正复合。

## 当前 Power / Human / World 的长期张力
宁烬仍只有灵海境三重的公开主尺位置，却已经拥有两处真身、白昼火、黑门骨和再次找到镜海界的海眼碎片。裴照临仍在主尺上明显更强，并持有完整白昼心。宁烬想要更多世界、更多不可复制的东西，也会因为贪、好胜与不肯只拿一半进入更危险路线。

## 全书成长与核心幻想兑现脊柱（只写从当前点向前仍成立的部分）
每个真正独立世界先作为自己的世界成立；宁烬进入后只能从自己真实走到的路线取得一条世界可能性。新的可能性必须留下，并与“双真”以及后续旧积累发生可复述的复合，而不是换地图清零。玄曜境界继续正常修炼与提升，但不能用免费升境替代世界可能性的核心幻想。

## 不可替代的人与关系
裴照临：灵海九重的 Origin Rival，持完整白昼心，raw ruler 与资源仍高于宁烬；他可以正常成长并赢得真正奖励，但没有自动递归 Advantage Stack。
镜离 / 澜生：同一个人的两个真实位置，留在镜海界处理赫连枢与本界余波；海眼碎片使关系和世界都具备真实回访可能，但不是每个新世界都必须回去打卡。
赫连枢：坠入镜海错位深处，生死未确认。
天外商王：公开重新估价宁烬并给出三十万灵玉、赤曜灯芯、赤鳞云驹与下一次天洲级宝物会入口；他的兴趣是生意，不是无条件保护。

## World Horizon Handoff
前十章 Horizon 已结束。黑门骨已经向读者明确显示三个下一世界影子；后续每个独立 instance 必须先经过 protagonist-blind World Expansion，再做 fresh Story Refresh。

## 远期仍值得追的东西
裴照临与白昼心会怎样发展；镜离/澜生与赫连枢的后续；黑门骨为什么会选择/适配宁烬仍未知；三个已经看见的异世界；宁烬最终能把多少互不相容的世界可能性压进同一个人身上。
"""


def starting_book() -> str:
    design = {
        "growth_genome": """### 作者明确保留
《我身藏诸界》的核心卖点是：进入不同真实世界，永久带走那个世界独有的一种可能性，并让不同可能性继续复合成只有宁烬能走出的成长路线。
### 一级成长收益
玄曜公开境界正常成长 + 诸界可能性 Advantage Stack。当前已成立第一条：两处都是真身；后续新世界必须带来新的现实权限并产生复合，不写成库存技能列表。
### 二级成长收益
钱、稀有器物、坐骑、跨界媒介、关系与世界入口可以同时成为爽点，但不能长期替代“主角本人变得更不可能”。
### 核心不变量
独立世界先成立；Route-Bound Acquisition；Rival 可更强但不复制主角递归优势栈。""",
        "type_promise": "东方玄幻大世界 + 多世界探索 + 复合非对称能力成长。世界奇观、强欲望对象、快速因果和高频兑现优先；每个世界结束后至少留下一个会真正改变后文的东西。",
        "world_structure": "玄曜大界是长期 Origin；黑门骨连接独立 instance 世界。镜海界已完成第一轮，海眼碎片允许未来回访。下一步只使用正文第10章已经出现的三个世界影子，不凭空替换成别的地图。",
        "world_pressure": "外界强者争黑门骨与天外遗物；各 instance 有自己的活人、利益、关系与危机。世界压力不默认变成治理/维护任务。",
        "protagonist_model": "宁烬贪、敢押、好胜、爱面子、爱稀奇，不愿被别人替自己决定价值；但不把爱钱写成每章固定口癖。选择优先暴露他这个人，而不是长期成长最优算法。",
        "relationships": "裴照临是 raw-ruler 长期压力；镜离/澜生是可回访的真实关系；天外商王是利益型高位观察者。新世界人物必须有自己的欲望，不围绕宁烬排队。",
        "plot_engine": "进入独立世界 → 被该世界真正的人/欲望/冲突卷入 → 宁烬按自己性格选择路线并可能错失其它机会 → 赢下/承担一个只有该世界才能成立的结果 → 带回一条世界可能性 → 返回玄曜或进入下一世界后发生复合与社会重新估价。每轮 Story Engine 仍需变体，不机械重复。",
        "narrative_structure": "默认5章连续正文窗口。每个10章 instance 应有 World Entry、核心人物/欲望、至少一次只有该世界才能发生的高价值场景、真正的可能性取得、返回后的直接 consequence；不是固定模板税，若故事自然变化可以偏移。",
        "prose": "普通中文男频可读性优先；动作和欲望先发生，说明只到当前选择需要。Story-bearing detail > 修饰密度。禁止把漂亮二段论反复写成稳定章法；避免后台规划词进入旁白。",
        "dialogue": "对话传递现场条件与人物关系，宁烬可嘴硬、贪心、挑衅，但不持续重复同一种金钱口癖。不同世界人物说话方式由生活与关系区分。",
        "rhythm": "剧情推进快，主尺升级不按章缴税。高潮可以同时兑现战利品、关系/身份重新估价与新入口；真正的大胜不主动削成保守资格奖励。",
        "theme": "同一个人能够容纳多少互相冲突的世界可能性；当不同世界对‘人是什么、位置是什么、伤是什么、行动是否结束、距离是什么’给出不同答案时，宁烬会变成什么。主题靠故事与身体/选择体现，不写哲学说明会。",
        "strengths_risks": "优势：诸界可能性可形成强复合；风险：世界沦为关卡、宁烬只剩爱钱标签、每轮都变成同一寻宝模板、能力解释比故事多。",
    }
    status = """当前已完成第10章。

## ACTIVE SCENE STATE
地点：玄曜大界九环天都，天外拍卖场大乱刚结束。
宁烬：灵海境三重；经历镜海界重伤后仍在恢复，当前公开站在赤鳞云驹旁/其上，天外商王已终止现场继续围杀。
即时目标：消化刚得到的资源与双真公开后果；黑门骨正在显示三个新的世界影子。

## PERSISTENT CANON

### Power / Capability
Current Power Position｜主尺：玄曜九境九重｜精确位置：灵海3重
- 已永久带回镜海界可能性：同一个宁烬可同时占据两个同等真实的位置；两处都是真身，都能受伤、持物、施展当前境界力量并共享感知；总元力仍来自同一片灵海，不会凭空翻倍。
- 两处真身任一处遭到致命结果都对宁烬本人构成真实死亡风险；它不是安全替身。
- 白昼火已经进入宁烬掌中并淬过玄曜元力，可造成远高于普通火焰的灼烧；正文已出现白昼火在两处真实位置间被转移/汇聚的可见用法，但没有公开解释其完整机制。
- 黑门骨可打开/识别真实异界裂口；海眼碎片使其未来能够重新识别镜海界。更深来源与全部边界仍未知。

### Active Relationships
裴照临｜灵海境九重；持完整白昼心｜公开敌对 Rival｜第10章亲自出剑后第一次因宁烬双真+白昼火改剑并退一步｜仍明显强于宁烬，下一次不会默认有商王挡在中间。
镜离 / 澜生｜留在镜海界处理赫连枢与本界余波｜与宁烬形成共同生死后的真实关系与欠账/回访入口｜分别留在岸/海两处世界继续行动｜未承诺跟随宁烬离开。
赫连枢｜镜海王｜敌对｜两处身体被镜离/澜生同时重创并坠入错位深处｜生死未确认。
天外商王｜天门境七重的利益型高位商人｜重新估价宁烬｜当众终止围杀并支付高价资源｜做生意，不等于长期保护。

### Identity / Access
- 九环天都大量见证者已亲眼看到宁烬仍是灵海境三重，却能同时出现两个魂息、血气、元力都真实的身体；神台境九重首席鉴宝师完成公开校准。
- 天外商王已给宁烬下一次天洲级宝物会的进入承诺/邀请；具体未来时间与内容尚未发生。

### Knowledge / Enemy State
- 宁烬知道镜海界的双身不是幻影，并亲自把其核心可能性带回。
- 裴照临知道宁烬拥有两个真实位置和白昼火的可见战斗效果，但不知道余门的隐藏因果、永久取得规则或未来复合上限。
- 黑门骨显示三个尚未进入的世界：巨尸骨陆、无主兵荒原、无墙万门宫殿；除此之外的规则均未知。

### World State
- 九环天都已经出现公开异常战例：一个灵海境三重修士同时以两个真实位置行动，并迫使灵海境九重的裴照临改变剑势；天外商会对其公开报价与待遇已经上调。
- 黑门骨与真实异界已经从少数人的传闻变成天都高位势力亲眼见证的争夺对象，但诸界机制仍不是公共常识。

### Tracked Assets
黑门骨｜宁烬｜掌骨/随身｜仍可显示与识别异界裂口｜第一章拍卖场落入宁烬手中。
海眼碎片｜宁烬｜随身｜可帮助黑门骨重新识别镜海界｜镜离第9章交给宁烬。
白昼火｜宁烬｜掌中/体内｜已与玄曜元力发生可见呼应｜镜海界白昼心残留中取得。
赤曜灯芯｜宁烬｜随身｜天外火种；与白昼火存在可见呼应，尚未完全探索｜第10章天外商王给出。
赤鳞云驹｜宁烬｜九环天都｜可踏空的跨城坐骑｜第10章天外商王给出。
三十万灵玉｜宁烬｜储物戒｜已实际到账｜第10章天外商王给出。
完整白昼心｜裴照临｜随身｜可稳定镜海界双位生命，带回玄曜后的进一步效果尚未完全显现｜第6章裴照临夺得。

## RECENT SUMMARIES
第8章：宁烬跌入镜海界无光层，在只能二选一的双重危机中同时踏出两步，第一次让两个宁烬在不同真实位置同时成立，并救下镜离与澜生；赫连枢与裴照临都亲眼看见。
第9章：镜海界上下错位，宁烬以两个真身分别行动，镜离/澜生同时重创赫连枢；裴照临带白昼心先行返回。镜离给宁烬海眼碎片，宁烬把双真与白昼火带回玄曜。
第10章：宁烬仍以灵海三重公开同时出现两个真实位置，击破六名高境围杀者的包围并迫使裴照临亲自改剑退一步；神台九重鉴宝师确认两处都是真身，商王重新报价并给出灵玉、赤曜灯芯、赤鳞云驹。黑门骨随后显示三个新世界影子。

## OPEN PROMISES
- 裴照临持完整白昼心并明确下次不会让商王成为屏障。
- 镜离/澜生仍在镜海界；赫连枢生死未知；海眼碎片允许真实回访。
- 黑门骨显示的巨尸骨陆、无主兵荒原、无墙万门宫殿尚未进入。
- 双真只是第一条世界可能性；下一条能否与它产生真正复合，是全书当前最重要的类型承诺。
- 黑门骨来源、为什么适配宁烬、诸界数量与更深机制仍未知。

## AUTHOR NOTES
- 书名：《我身藏诸界》。
- 默认审美 AGGRESSIVE：因果成立时不要主动少给、晚给、降成资格。
- 宁烬长期应形成主角专属 Advantage Stack；裴照临等 Rival 可以更强、拿大奖励，但不自动同步获得递归异常栈。
- 避免治理/维护/流程作为主发动机；避免漂亮二段论重复成章法；避免宁烬只剩爱钱口癖。
"""
    sections = {
        "design": compose_design_content(design),
        "long_plan": "当前前十章已完成；下一 Horizon 必须先做 protagonist-blind World Expansion 与 Story Refresh，再由 Outline 写入本区。",
        "small_plan": "当前没有未执行 Future-10；下一 Horizon 规划后写入。",
        "status": status,
    }
    return compose_book_content(sections)


def split_old_chapters(full_text: str) -> dict[int, str]:
    matches = list(re.finditer(r"(?m)^第[一二三四五六七八九十]+章[^\r\n]*$", full_text))
    if len(matches) != 10:
        raise RuntimeError(f"expected 10 old chapter headings, got {len(matches)}")
    out: dict[int, str] = {}
    for idx, match in enumerate(matches, start=1):
        end = matches[idx].start() if idx < len(matches) else len(full_text)
        out[idx] = full_text[match.start():end].strip()
    return out


def make_expansion_collection(entries: list[tuple[int, int, int, str]]) -> str:
    chunks = []
    for index, start, end, content in entries:
        body = strip_top_heading(content, "# WORLD EXPANSION")
        chunks.append(
            f"# WORLD EXPANSION {index:04d}\nScope: instance\nEffective From Chapter: {start}\nEffective Until Chapter: {end}\n\n{body}"
        )
    return "\n\n".join(chunks).strip() + ("\n" if chunks else "")


def ensure_world_expansion(*, horizon: dict[str, object], index: int, book: str, world: str, previous_collection: str) -> str:
    start = int(horizon["start"]); end = int(horizon["end"])
    folder = OUT / "planning" / f"world-{start:02d}-{end:02d}"
    gbrain = safe_gbrain(
        "world_expansion", folder,
        creative_direction=str(horizon["author_direction"]),
        world_vision=world,
    )
    prompt = generate_split_prompt(
        mode="world_expansion",
        book_content=book,
        creative_direction=str(horizon["author_direction"]),
        world_vision=world,
        world_expansions=previous_collection,
        creative_state=CREATIVE_STATE,
        gbrain_inspiration=gbrain,
        evolution_scope="instance",
        effective_from_chapter=start,
        effective_until_chapter=end,
    )
    response = run_acp(label=f"world-{start}-{end}", model="gpt-5.6-luna", effort="high", prompt=prompt, folder=folder)
    clean = extract_from_heading(response, "# WORLD EXPANSION")
    try:
        validate_world_expansion_ruler(clean, world, scope="instance")
    except Exception as exc:
        repair_folder = folder / "repair"
        repair_prompt = f"""下面是已经生成的 TGN instance World Expansion。production validator 只发现一个必须修的结构/Authority问题：{exc}\n\n请保留世界创意、人物、欲望、地点与冲突，只修 validator 指出的错误；仍然严格输出完整 `# WORLD EXPANSION` 六个区块，不解释修改过程。\n\n原稿：\n{clean}\n"""
        response = run_acp(label=f"world-{start}-{end}-repair", model="gpt-5.6-luna", effort="high", prompt=repair_prompt, folder=repair_folder)
        clean = extract_from_heading(response, "# WORLD EXPANSION")
        validate_world_expansion_ruler(clean, world, scope="instance")
    write(folder / "FINAL_WORLD_EXPANSION.md", clean)
    return clean


def build_outline_book(*, response: str, current_book: str, story_program: str, start: int, end: int, folder: Path) -> str:
    clean = extract_from_heading(response, "# 小说总体设计画像")
    def compile_candidate(text: str) -> str:
        parsed = parse_book_sections(text)
        current_status = parse_book_sections(current_book)["status"]
        parsed["status"] = current_status
        candidate = compose_book_content(parsed)
        validate_book_content_for_save(candidate)
        small = parse_book_sections(candidate)["small_plan"]
        missing = [n for n in range(start, end + 1) if re.search(rf"(?m)^##\s*第\s*{n}\s*章", small) is None]
        if missing:
            raise ValueError(f"Future-10 缺少章节：{missing}")
        validate_book_registry_against_story_program(story_program, candidate)
        return candidate
    try:
        book = compile_candidate(clean)
    except Exception as exc:
        repair_prompt = f"""你是 TGN Outline 层的定点修复器。只修下面 Outline 的 production 编译错误，不重写已批准 Story Program，不新增能力/世界/奖励。\n错误：{exc}\n本轮必须只规划第{start}—{end}章，四个一级标题必须严格是：`# 小说总体设计画像`、`# 当前中期规划窗口`、`# 未来十章逐章小纲`、`# 当前状态、未兑现承诺与作者备注`。如果是 RSE registry/schedule 错误，逐字保留 Story Program 的 RSE 事件块并只修排章引用。\n\n已批准 Story Program：\n{story_program}\n\n待修 Outline：\n{clean}\n"""
        repaired = run_acp(label=f"outline-{start}-{end}-repair", model="gpt-5.6-luna", effort="high", prompt=repair_prompt, folder=folder / "repair")
        book = compile_candidate(extract_from_heading(repaired, "# 小说总体设计画像"))
    write(folder / "BOOK_PLANNED.md", book)
    return book


def generate_horizon_plan(*, horizon: dict[str, object], index: int, book: str, world: str, character: str, story_program: str, expansion_entries: list[tuple[int,int,int,str]]) -> tuple[str, str, str]:
    start = int(horizon["start"]); end = int(horizon["end"])
    collection = make_expansion_collection(expansion_entries)
    status = parse_book_sections(book)["status"]
    current_character = compile_current_character(character_card=character, status_text=status, human_development="", chapter_number=start)
    write(OUT / "planning" / f"current-character-through-{start-1:02d}.md", current_character)

    author_story_direction = f"""《我身藏诸界》继续写第{start}—{end}章。作者已经决定进入本轮刚批准的 instance 世界，不改成留在天都。世界先独立成立，Story Refresh 再让宁烬按自己的贪、好胜、好奇与关系选择路线。\n本轮必须在自然高潮前后让宁烬**亲自赢下一条该世界独有的永久可能性**，并让它至少一次与已有“双真”产生单项做不到的复合；不要只给宝物/资格。取得必须 route-bound、有真实冲突和不可回头选择，不从全世界挑最适合 Build 的礼包。\n主尺成长不要过度克制：30章总跨度足以正常升若干小重，只要资源/战斗/修炼因果成立就可以真升级；但世界可能性本身不免费送境界。裴照临可正常成长并继续做 raw-ruler 压力，却不自动获得平行递归异常栈。\n每个 instance 的 Story Engine、人物关系与核心高价值场景都要明显不同；世界规则要改变人物命运/关系，不只当战斗机关。结尾返回玄曜或形成清楚的下一世界因果，并保留已发生资产、伤势与关系。"""
    story_folder = OUT / "planning" / f"story-{start:02d}-{end:02d}"
    story_gbrain = safe_gbrain(
        "story_refresh", story_folder,
        book_content=book,
        creative_direction=author_story_direction,
        world_vision=world,
        character_card=character,
        proposal_context=story_program,
        recent_summaries=status,
    )
    story_prompt = generate_split_prompt(
        mode="story_refresh",
        book_content=book,
        creative_direction=author_story_direction,
        world_vision=world,
        world_expansions=collection,
        character_card=character,
        current_character=current_character,
        creative_state=CREATIVE_STATE,
        proposal_context=story_program,
        selected_references=[],
        gbrain_inspiration=story_gbrain,
        effective_from_chapter=start,
    )
    story_response = run_acp(label=f"story-refresh-{start}-{end}", model="gpt-5.6-sol", effort="high", prompt=story_prompt, folder=story_folder)
    new_story = extract_from_heading(story_response, "# STORY PROGRAM")
    write(story_folder / "FINAL_STORY_PROGRAM.md", new_story)

    outline_direction = f"""当前已完成第{start-1}章。本轮 Outline 只编译已批准 Story Program 的第{start}—{end}章，Future-10 章号必须连续写第{start}章到第{end}章，不重写旧正文。节奏可以激进，保证核心世界可能性取得、复合、Public Proof/关系后果与返回因果真正落到具体事件；避免流程 filler、固定爱钱口癖和漂亮二段论。"""
    outline_folder = OUT / "planning" / f"outline-{start:02d}-{end:02d}"
    outline_gbrain = safe_gbrain(
        "outline", outline_folder,
        book_content=book,
        creative_direction=outline_direction,
        world_vision=world,
        character_card=character,
        proposal_context=new_story,
        recent_summaries=status,
    )
    outline_prompt = generate_split_prompt(
        mode="outline",
        book_content=book,
        creative_direction=outline_direction,
        world_vision=world,
        world_expansions=collection,
        character_card=character,
        current_character=current_character,
        creative_state=CREATIVE_STATE,
        proposal_context=new_story,
        selected_references=[],
        gbrain_inspiration=outline_gbrain,
    )
    outline_response = run_acp(label=f"outline-{start}-{end}", model="gpt-5.6-luna", effort="high", prompt=outline_prompt, folder=outline_folder)
    new_book = build_outline_book(response=outline_response, current_book=book, story_program=new_story, start=start, end=end, folder=outline_folder)
    return new_story, new_book, collection


def run_batch(*, batch_start: int, book: str, world: str, character: str, story_program: str, world_expansions: str, chapters: dict[int,str]) -> tuple[str, dict[int,str]]:
    window = BatchWindow(batch_start, 5)
    folder = OUT / "batches" / f"batch-{window.start_chapter:04d}-{window.end_chapter:04d}"
    plans = extract_batch_outline_plans(book, window)
    prev = chapters[batch_start - 1]
    primary_prompt = build_batch_primary_prompt(
        window=window,
        batch_plans=plans,
        book_content=book,
        world_vision=world,
        world_expansions=world_expansions,
        character_card=character,
        previous_chapter_text=prev,
    )
    primary_response = run_acp(label=f"primary-{window.start_chapter}-{window.end_chapter}", model="gpt-5.6-terra", effort="high", prompt=primary_prompt, folder=folder / "primary")
    try:
        primary = parse_batch_primary_response(primary_response, window)
    except Exception as exc:
        repair_prompt = primary_prompt + f"\n\n# OUTPUT COMPLETENESS REPAIR\n上一次输出无法被 Batch parser 接受：{exc}。保持同一故事与 Authority，不做解释；重新完整输出5章，每章都使用 `# BATCH CHAPTER N` + `## 正式正文`，不得漏章或压成摘要。"
        primary_response = run_acp(label=f"primary-{window.start_chapter}-{window.end_chapter}-repair", model="gpt-5.6-terra", effort="high", prompt=repair_prompt, folder=folder / "primary-repair")
        primary = parse_batch_primary_response(primary_response, window)
    write(folder / "PRIMARY.md", "\n\n".join(primary[n] for n in window.chapter_numbers))

    delta_prompt = build_batch_delta_reviser_prompt(
        window=window,
        batch_plans=plans,
        primary_chapters=primary,
        book_content=book,
        world_vision=world,
        world_expansions=world_expansions,
        character_card=character,
        story_program=story_program,
    )
    delta_response = run_acp(label=f"delta-{window.start_chapter}-{window.end_chapter}", model="gpt-5.6-sol", effort="high", prompt=delta_prompt, folder=folder / "delta", timeout=9000)
    delta = parse_batch_delta_response(delta_response, window)
    dump(folder / "DELTA.json", {"patches": list(delta.patches), "upstream_conflicts": list(delta.upstream_conflicts)})
    if delta.upstream_conflicts:
        raise RuntimeError(f"Batch {batch_start}-{window.end_chapter} upstream conflicts: {delta.upstream_conflicts}")
    final = apply_batch_delta(primary, delta, window)
    write(folder / "FINAL.md", "\n\n".join(final[n] for n in window.chapter_numbers))

    for n in window.chapter_numbers:
        chapters[n] = final[n]
        write(OUT / "chapters" / f"chapter-{n:04d}.md", final[n])
        status = parse_book_sections(book)["status"]
        recent = parse_canon_memory(status).get("recent_summaries", "").strip()
        state_prompt = generate_prompt(
            mode="state_delta",
            template="",
            book_content=book,
            recent_summaries=recent,
            chapter_number=n,
            chapter_prose=final[n],
            chapter_fact_summary="",
        )
        state_response = run_acp(label=f"state-{n}", model="gpt-5.6-luna", effort="low", prompt=state_prompt, folder=folder / "state" / f"chapter-{n:04d}", timeout=2400)
        book = apply_state_delta_to_book(book, n, state_response)
        validate_book_content_for_save(book)
    write(folder / "BOOK_AFTER_BATCH.md", book)
    return book, chapters


def render_all(chapters: dict[int,str]) -> str:
    parts = []
    for n in range(1, 41):
        body = chapters[n].strip()
        if not re.match(r"^第.{0,8}章", body):
            body = f"第{n}章\n\n{body}"
        parts.append(body)
    return "\n\n".join(parts).strip() + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    chapters_dir = OUT / "chapters"; chapters_dir.mkdir(exist_ok=True)
    old_full = read(OLD / "FULL_10_CHAPTERS.md")
    chapters = split_old_chapters(old_full)
    for n, body in chapters.items():
        write(chapters_dir / f"chapter-{n:04d}.md", body)
    write(OUT / "CHAPTERS_0001_0010.md", old_full)

    world = root_world(); character = character_card(); story = starting_story_program(); book = starting_book()
    write(OUT / "WORLD_VISION.md", world)
    write(OUT / "CHARACTER.md", character)
    write(OUT / "STORY_PROGRAM_BASE.md", story)
    write(OUT / "BOOK_START_CH10.md", book)

    expansion_entries: list[tuple[int,int,int,str]] = []
    for index, horizon in enumerate(HORIZONS, start=1):
        start = int(horizon["start"]); end = int(horizon["end"])
        previous_collection = make_expansion_collection(expansion_entries)
        expansion = ensure_world_expansion(horizon=horizon, index=index, book=book, world=world, previous_collection=previous_collection)
        expansion_entries.append((index, start, end, expansion))
        collection = make_expansion_collection(expansion_entries)
        write(OUT / "WORLD_EXPANSIONS.md", collection)

        story, book, collection = generate_horizon_plan(
            horizon=horizon,
            index=index,
            book=book,
            world=world,
            character=character,
            story_program=story,
            expansion_entries=expansion_entries,
        )
        write(OUT / f"STORY_PROGRAM_{start:02d}_{end:02d}.md", story)
        write(OUT / f"BOOK_PLAN_{start:02d}_{end:02d}.md", book)

        for batch_start in (start, start + 5):
            book, chapters = run_batch(
                batch_start=batch_start,
                book=book,
                world=world,
                character=character,
                story_program=story,
                world_expansions=collection,
                chapters=chapters,
            )
        write(OUT / f"BOOK_AFTER_CH{end:02d}.md", book)
        print(json.dumps({"horizon_complete": [start, end], "current_power": parse_canon_memory(parse_book_sections(book)["status"]).get("persistent_canon", "")[:500]}, ensure_ascii=False), flush=True)

    full = render_all(chapters)
    write(OUT / "FULL_40_CHAPTERS.md", full)
    write(OUT / "FULL_40_CHAPTERS.txt", full)
    write(OUT / "BOOK_FINAL.md", book)
    write(OUT / "STORY_PROGRAM_FINAL.md", story)
    dump(OUT / "CALL_LOG.json", CALL_LOG)
    metrics = {
        "chapters": 40,
        "new_chapters": 30,
        "calls": len(CALL_LOG),
        "wall_seconds_sum": round(sum(float(x.get("wall_seconds", 0.0)) for x in CALL_LOG), 3),
        "primary_calls": sum(1 for x in CALL_LOG if str(x.get("label", "")).startswith("primary-")),
        "delta_calls": sum(1 for x in CALL_LOG if str(x.get("label", "")).startswith("delta-")),
        "state_calls": sum(1 for x in CALL_LOG if str(x.get("label", "")).startswith("state-")),
        "final_chars": len(full),
    }
    dump(OUT / "RUN_METRICS.json", metrics)
    print(json.dumps(metrics, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
