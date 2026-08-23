from __future__ import annotations

import argparse
import json
from pathlib import Path

from story_mvp.chapter_context import ChapterContextPacket, project_event_contract_for_prose
from story_mvp.hybrid_runtime import (
    build_curator_context,
    extract_primary_prose_context,
)
from story_mvp.prompts import (
    DEFAULT_PROMPT_TEMPLATES,
    READER_FIRST_PROSE_CONTRACT,
    _input_block,
)
from story_mvp.scene_skills import (
    render_scene_skill_catalog,
    render_selected_scene_skills,
    strip_scene_skill_selection,
)

ROOT = Path(__file__).resolve().parents[1]

AUTHORITY = """已发生事实以 CANON PROSE > CANON INDEX；未来意图以 BOOK CONTRACT > PLAN；表达只由 PROSE PROFILE 控制。Curator 不得创造事实。"""

BOOK_CONTRACT = """## 1. 核心类型与读者承诺
成熟中文男频玄幻成长长篇。核心幻想是主角能看见被世界秩序隐藏的旧门与断路，并把一次进入变成以后可复用的行动优势。故事价值优先于流程完整。

## 2. 世界观结构
宗门、边城、遗迹和旧朝留下大量被封存的道路、身份与器物。道路可以连接地点，也可能连接旧身份、盟约和被掩埋的历史。

## 3. 世界压力
敌人会封门、换身份、转移证物、利用主角打开的入口反向追踪。支持逻辑不得自动成为 Story Engine。

## 4. 主角模型
江临厌恶别人替他决定能去哪里、能知道什么。他主动、记仇、护短，也愿意为了真正重要的人冒险。

## 5. 配角与关系系统
宁青梧、沈雪舟、顾槐生等角色都有离屏目标；旧角色回归必须改变当前选择，而不是只负责提供信息。

## 7. 叙事结构
第三人称限知，跟随江临。重要旧线回流时先让物件、动作和人物反应成立，再补最少解释。

## 8. 文风与可操作参数
清楚、直接、有画面；克制但不干，丰富但不腻。避免工程说明与 AI 修辞堆积。

## 9. 对话特点
人物说话有利益和关系位置，不背诵设定。

## 10. 节奏结构
关键回归、揭露和兑现允许短暂停留，让读者真正感到旧线重新有意义。"""

PROSE_PROFILE = """## 7. 叙事结构
第三人称限知，当前 POV 为江临。

## 8. 文风与可操作参数
Reader-First；Story-bearing Texture；具体动作和结果优先。

## 9. 对话特点
短、带立场，避免说明腔。

## 10. 节奏结构
重要旧线回流允许人物反应与一次确认，不重复总结。"""

GROWTH = """## 0. 本书成长基因图（章节压缩）
### 已批准幻想不变量
被封死的地方仍可能被江临亲自打开；每次真正进入都扩大他的未来行动空间。
### 核心不变量
旧线回流必须改变人物选择、世界入口或敌人策略。
### 退化风险
不要把开门能力写成巡检、维护、路线运营或数据库管理。"""

RELEVANT_FACTS = {
    30: [
        "第18章：宁青梧离开前把玄鹭玉牌交给江临。玉牌红绳缺了一结；她只说‘第三盏灯亮前别交给任何人’。只有江临与宁青梧知道这句话。",
        "OPEN-18：宁青梧为什么提前离开、玄鹭玉牌为何不能见第三盏灯，均未兑现。",
    ],
    120: [
        "第18章：宁青梧离开前把玄鹭玉牌交给江临。玉牌红绳缺了一结；她只说‘第三盏灯亮前别交给任何人’。只有江临与宁青梧知道这句话。",
        "第73章：边城旧市出现同样缺一结的红绳，江临没有取走，只记住摊主左手有烧伤。",
        "第119章末：失踪九十余章的宁青梧重新出现。她没有先叫江临名字，而是先看他腰间玄鹭玉牌，随后说‘第三盏灯已经有人点过一次了’。",
        "OPEN-18：玄鹭玉牌与第三盏灯的约定仍未解释；宁青梧回归使其进入兑现窗口。",
    ],
    300: [
        "第42章：沈雪舟替江临挡下旧朝追索后离队，留下半枚青铜镜。镜背只有沈雪舟知道的划痕顺序是‘二、一、三’；江临只知道这半枚镜不能照活人。",
        "第181章：北境死人铺出现另一半青铜镜的拓印，但划痕顺序被故意改成‘一、二、三’，江临判断有人冒用沈雪舟身份。",
        "第299章末：自称沈雪舟的人在白塔门外等江临，手里拿着另一半青铜镜，却主动把镜面对准自己。",
        "OPEN-42：沈雪舟真实去向、半枚青铜镜为何不能照活人尚未兑现；冒名者线与本人回归可能发生碰撞。",
    ],
    600: [
        "第18章：宁青梧把玄鹭玉牌交给江临，约定第三盏灯亮前不能交给任何人。",
        "第120章：宁青梧回归后确认第三盏灯已被点过一次，但她没有拿回玉牌；她改为让江临继续持有。",
        "第42章：沈雪舟留下半枚青铜镜，镜背划痕顺序‘二、一、三’只有本人知道。",
        "第300章：江临识破白塔门外的冒名者；真正的沈雪舟仍未现身，另一半镜被白塔收走。",
        "第411章：顾槐生与江临立下白塔誓约：如果白塔第七层重新开门，顾槐生负责让城中人撤离，江临负责进入第七层，不交换职责。",
        "第599章末：白塔第七层在无人触碰时自行开门。宁青梧带着缺一结的红绳出现；同时，塔内有人用沈雪舟独有的‘二、一、三’划痕敲门。顾槐生却要求江临留下守城，和第411章誓约直接冲突。",
        "OPEN-411：白塔誓约已经触发；顾槐生为何反悔、塔内沈雪舟信号真假、宁青梧此刻回归目的必须在当前阶段碰撞。",
    ],
}

MISSIONS = {
    30: """触发事件：江临在旧市第三盏灯即将点亮时发现玄鹭玉牌自行发热，宁青梧留下的红绳缺口与灯架上的旧结完全吻合。\n主角行动：江临必须决定是立刻带玉牌进入灯后旧门，还是先保住宁青梧留下的约定。\n直接结果：他确认旧门与玄鹭玉牌有关，但本章不解释宁青梧去向。\n结尾推动力：第三盏灯开始亮。""",
    120: """触发事件：失踪九十余章的宁青梧重新出现在江临面前，并第一眼看向玄鹭玉牌。\n主角行动：江临不先追问她去了哪里，而是拿出玉牌，要求她解释‘第三盏灯已经有人点过一次’意味着什么。\n直接结果：两人的旧约重新进入当前主线，宁青梧必须作出一个会改变下一步行动的回答。\n结尾推动力：她指出真正点灯的人就在回灯楼内。""",
    300: """触发事件：白塔门外自称沈雪舟的人拿着另一半青铜镜，却把镜面对准自己。\n主角行动：江临利用自己记得的半镜限制和沈雪舟留下的划痕信息判断真假，不允许对方用旧关系直接取得信任。\n直接结果：身份真假在本章出现可见证据；半枚青铜镜旧线重新改变当前选择。\n结尾推动力：塔内传来只有真正沈雪舟才可能留下的第二个信号。""",
    600: """触发事件：白塔第七层自行开门，宁青梧带着缺一结的红绳出现；塔内同时传出沈雪舟独有的‘二、一、三’敲击。顾槐生却要求江临留下守城。\n主角行动：江临必须在白塔誓约、宁青梧的第三盏灯旧线和沈雪舟的镜线同时回流时判断谁在改变约定、谁在发出真实求援，并决定是否进入第七层。\n直接结果：至少一条沉睡百章以上的关系或承诺在当前选择中产生不可逆变化。\n结尾推动力：第七层门开始关闭。""",
}


def distractor(i: int) -> str:
    return (
        f"支线记录{i:04d}：灰湾客卿季闻舟在第{i % 97 + 1}号渡口处理一件与当前主线无关的旧债；"
        f"持有青木票{i:04d}，与巡夜人关系为临时合作。该记录已经结清，与当前章旧线无关。"
    )


def canon_for(n: int) -> str:
    extras = "\n\n".join(distractor(i) for i in range(1, n + 1))
    facts = "\n\n".join(RELEVANT_FACTS[n])
    return f"""## ACTIVE SCENE STATE
当前地点：白塔/旧市对应阶段现场。江临在场，当前目标与本章事件合同一致。上一章留下的即时动作尚未完成。

## PERSISTENT CANON
江临的核心能力是识别被封存的旧门与断路，但必须亲自进入才能把它变成以后可复用的行动优势。

{extras}

{facts}

## RECENT SUMMARIES
第{max(1,n-2)}章：近期冲突推进，但没有改写本实验所需的旧事实。

第{max(1,n-1)}章：当前地点与敌人压力建立。

第{n-1}章末：{RELEVANT_FACTS[n][-2] if n > 30 else '第三盏灯相关旧物重新出现。'}

## OPEN PROMISES
普通近期承诺：当前敌人的追索仍在。

{RELEVANT_FACTS[n][-1]}
"""


def packet_for(n: int) -> ChapterContextPacket:
    recent = f"""上一章正文节选：夜里风很硬。江临停在门前，没有立刻伸手。与第{n}章事件直接相连的旧人物或旧物已经进入现场，但真正的选择尚未发生。"""
    return ChapterContextPacket(
        authority=AUTHORITY,
        book_contract=BOOK_CONTRACT,
        chapter_mission=MISSIONS[n],
        canon_context=canon_for(n),
        recent_prose=recent,
        rolling_plan=MISSIONS[n],
        chapter_plan_context=MISSIONS[n],
        current_long_block=f"第{n}章所在剧情块：旧线回流并改变当前选择。",
        current_chapter_plan=MISSIONS[n],
        prose_profile=PROSE_PROFILE,
        optional_inspiration="",
        growth_benefit_projection="本章一级成长：判断与行动空间；二级收益：旧关系/旧承诺重新可用；反哺：打开下一阶段入口。",
        growth_genome_compact=GROWTH,
        prologue_reader_knowledge="",
    )


def curator_prompt(packet: ChapterContextPacket, *, full: bool) -> str:
    ctx = build_curator_context(packet)
    book = packet.book_contract if full else ctx.book_contract
    canon = packet.canon_context if full else ctx.canon_index
    label = "FULL CONTEXT 对照组" if full else "CURRENT INDEX-FIRST"
    parts = [DEFAULT_PROMPT_TEMPLATES["context_curator"], "", f"# Scaling Experiment Variant\n\n{label}"]
    parts += [
        _input_block("AUTHORITY", ctx.authority),
        _input_block("当前章事件合同", ctx.chapter_mission),
        _input_block("CONTEXT INDEX——只含结构入口", ctx.context_index),
        _input_block("压缩 Growth Genome", ctx.growth_genome_compact),
        _input_block("BOOK CONTRACT——" + ("全量" if full else "本章确定性预取"), book),
        _input_block("本章成长收益短投影", ctx.growth_benefit_projection),
        _input_block("CANON INDEX——" + ("全量" if full else "本章确定性预取"), canon),
        _input_block("当前大型剧情块与十章计划", ctx.rolling_plan),
        _input_block("PROSE PROFILE", ctx.prose_profile),
        _input_block("SCENE SKILL CATALOG", render_scene_skill_catalog()),
        _input_block("OPTIONAL INSPIRATION", ctx.optional_inspiration),
        _input_block("前文章末局部衔接片段", ctx.transition_context),
    ]
    parts.append("# 实验执行边界\n只执行 Context Curator 职责。不得修改文件，不得读取额外项目资料。最终只输出 Curator 合同要求的内容，不讨论实验设计。")
    return "\n\n".join(parts)


def primary_prompt(packet: ChapterContextPacket, curated: str) -> str:
    active = render_selected_scene_skills(curated)
    curated_for_writer = strip_scene_skill_selection(curated)
    parts = [
        DEFAULT_PROMPT_TEMPLATES["primary_writer"],
        "",
        "# Reader-First Prose Contract",
        READER_FIRST_PROSE_CONTRACT,
        "# Hybrid Runtime\n\nwriter_mode: curator_primary",
        _input_block("AUTHORITY", packet.authority),
        _input_block("Chapter Mission——正文可见最小事件合同", project_event_contract_for_prose(packet.chapter_mission)),
        _input_block("CANON PROSE——上一章全文与上上章必要章末", extract_primary_prose_context(packet.recent_prose)),
    ]
    if active:
        parts.append(_input_block("ACTIVE SCENE SKILLS——只控制场景如何落成正文", active))
    parts.append(_input_block("Curated Chapter Context", curated_for_writer))
    parts.append("# 实验执行边界\n只执行 Primary Writer。不得修改文件、重规划或读取额外资料。最终只返回 `# 正式正文` 与正文。")
    return "\n\n".join(parts)


def generate_curators() -> None:
    manifest = []
    for n in (30, 120, 300, 600):
        d = ROOT / f"chapter-{n:04d}"
        d.mkdir(parents=True, exist_ok=True)
        packet = packet_for(n)
        packet_json = {
            k: getattr(packet, k)
            for k in packet.__dataclass_fields__
        }
        (d / "packet.json").write_text(json.dumps(packet_json, ensure_ascii=False, indent=2), encoding="utf-8")
        for variant, full in (("index", False), ("full", True)):
            prompt = curator_prompt(packet, full=full)
            p = d / f"{variant}_curator_prompt.md"
            p.write_text(prompt, encoding="utf-8")
            manifest.append({"chapter": n, "variant": variant, "prompt": str(p), "prompt_chars": len(prompt), "model": "gpt-5.6-luna", "reasoning": "high"})
    (ROOT / "CURATOR_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def generate_primaries() -> None:
    manifest = []
    for n in (30, 120, 300, 600):
        d = ROOT / f"chapter-{n:04d}"
        data = json.loads((d / "packet.json").read_text(encoding="utf-8"))
        packet = ChapterContextPacket(**data)
        for variant in ("index", "full"):
            response = d / f"{variant}_curator_response.md"
            if not response.exists():
                raise SystemExit(f"missing curator response: {response}")
            curated = response.read_text(encoding="utf-8")
            prompt = primary_prompt(packet, curated)
            p = d / f"{variant}_primary_prompt.md"
            p.write_text(prompt, encoding="utf-8")
            manifest.append({"chapter": n, "variant": variant, "prompt": str(p), "prompt_chars": len(prompt), "model": "gpt-5.6-terra", "reasoning": "high"})
    (ROOT / "PRIMARY_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["curator", "primary"], required=True)
    args = ap.parse_args()
    if args.phase == "curator":
        generate_curators()
    else:
        generate_primaries()
