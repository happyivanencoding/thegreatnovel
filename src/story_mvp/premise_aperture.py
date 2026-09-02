from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal, Mapping


AxisName = Literal["world", "ontology", "privilege", "interface"]
LaneName = Literal["world", "power", "human", "story"]


BOLD_PREMISE_CRAFT = """# PRE-AUTHORITY CREATIVE APERTURE｜非 Canon

这里不是 production Fantasy Seed，也不生成新的世界/人物/力量权威。它只在任何 Authority 冻结前扩大作者可选择的搜索空间。

大胆设定不是术语更多、机制更复杂，而是尽早押注一个会改变读者想象与主角动作的高风险事实：主角以什么存在形态开始、世界眼前有什么不可忽略的异常、主角拥有哪种直接且不公平的特权、行动怎样被别人看见并产生社会后果。好设定至少让主角反复做出普通“人类修士升级”不会自然拥有的新动作，并能在第一章形成一幅具体画面。

共同边界：
- 先寻找让人想点开第一章的画面、身体状态、危险、欲望、反客为主或尺度冲击，再补最少可信桥梁；不要先把五百章合理性解释完。
- Category Collision 必须改变因果和玩法，不是把两个类型词并排写在简介里。
- 允许非人、非标准身体、异常生命阶段、公开观看/记录、跨层叙事或其它强界面；也允许普通人形，只要起点关系本身足够特殊。
- 不能只给普通修士换职业、换能源名、换宗门名、换一套考试/资格/资源分配流程。
- 直接特权优先改变战斗、身体、移动、生存、探索、占有、召唤、学习、变形、支配或其它可感知动作；不默认落成分析、维护、审核、路线优化或工作效率。
- 每个候选只保留少量熟悉锚点，让读者能一句话听懂；大胆不等于难懂。
- 不复制任何来源作品的角色、专名、事件组合或具体能力，只迁移“高风险押注、强画面、玩法碰撞、立即兑现”的创作方法。
"""


@dataclass(frozen=True)
class CollisionSpec:
    candidate_id: str
    world_id: str
    ontology_id: str
    privilege_id: str
    interface_id: str


@dataclass(frozen=True)
class PremiseLaneBundle:
    world: str
    ontology: str
    privilege: str
    interface: str
    collision: str
    origin: str = ""
    world_interface: str = ""
    scale_position: str = ""


@dataclass(frozen=True)
class VoltageBudgetSpec:
    candidate_id: str
    first_id: str
    second_id: str
    primary_bet: str
    low_voltage_rule: str


DEFAULT_COLLISION_MATRIX: tuple[CollisionSpec, ...] = (
    CollisionSpec("C1", "W1", "O2", "P3", "I1"),
    CollisionSpec("C2", "W2", "O3", "P1", "I2"),
    CollisionSpec("C3", "W3", "O1", "P2", "I3"),
)


DEFAULT_VOLTAGE_BUDGET_MATRIX: tuple[VoltageBudgetSpec, ...] = (
    VoltageBudgetSpec(
        "V1",
        "W1",
        "P2",
        "World pressure is primary; Privilege is the single protagonist twist.",
        "主角使用普通人形；不新增特殊 Ontology 或 Narrative Interface。",
    ),
    VoltageBudgetSpec(
        "V2",
        "O3",
        "P1",
        "Protagonist ontology is primary; Privilege is the single action engine.",
        "世界只给熟悉、具体的生存／竞争场景；不新增世界级异常或 Narrative Interface。",
    ),
    VoltageBudgetSpec(
        "V3",
        "W3",
        "I3",
        "World pressure is primary; Interface is the single social complication.",
        "主角使用普通人形；特殊 Power 留给后续独立 Authority，不在前提阶段新增。",
    ),
)


_AXIS_PROMPTS: dict[AxisName, str] = {
    "world": """你是 World Voltage 发散者。你完全不知道未来主角、Power、Human、Story Program 与开篇事件。只创造即使换掉主角也值得写的世界级异常或现实押注。

生成 3 个互不换皮的 World Spark。每个只需要一个高电压世界事实，不做完整 World Vision，不填力量尺，不解释终极真相。三者必须改变不同的日常动作、危险和欲望；至少两个不能只是“新的修炼能源/宗门竞争/秘境出现”。

严格格式：
# WORLD AXIS SPARKS
## W1｜短标签
Core: 一句话写眼前已经成立、任何人都无法忽略的世界事实
### 三幅可见画面
### 普通生活与欲望怎样被改变
### 即使没有主角也会继续推进的人与冲突
### 最少熟悉锚点
### 暂时不要解释的边界
## W2｜短标签
（同结构）
## W3｜短标签
（同结构）
""",
    "ontology": """你是 Protagonist Ontology 发散者。你看不到未来世界规则、Power、Biography、Story Opportunity 或开篇安排。只创造主角“以什么身体、物种、生命阶段、存在方式或视角位置开始”。

生成 3 个互不换皮的 Ontology Spark。存在形态不是人格标签，也不是完整金手指；它首先改变呼吸、移动、进食、感知、交流、占有、战斗或被别人对待的方式。至少两个明显偏离标准人类少年修士，但仍能让普通读者一句话想象。不要自动补悲惨童年或使命。

严格格式：
# ONTOLOGY AXIS SPARKS
## O1｜短标签
Core: 一句话写主角开局是什么样的存在
### 天然拥有的新动作与受限动作
### 身体／生命最直接的欲望与麻烦
### 视角会看见的独特东西
### 这不是 Power 的部分
### 第一眼形象
## O2｜短标签
（同结构）
## O3｜短标签
（同结构）
""",
    "privilege": """你是 Direct Privilege 发散者。你看不到未来持有者、世界专名、Biography、Story Opportunity 或终局。只创造读者会直接想拥有的“别人必须服从什么，而我可以额外做什么”。

生成 3 个互不换皮的 Privilege Spark。每个最多一个主异常，先白话后标签；明显偏强，但只保留一条真正防万能的根边界。至少两个必须改变身体、战斗、移动、生存、探索、占有或其它直接动作，不能只是学习更快、分析更准、做事更有效率。

严格格式：
# PRIVILEGE AXIS SPARKS
## P1｜短标签
Core: 一句话写普通人做不到、持有者现在就多能做什么
### 第一次就很过分的用法
### 反复使用会长出的新动作
### 公开显露时别人为什么会失态
### 唯一根边界
## P2｜短标签
（同结构）
## P3｜短标签
（同结构）
""",
    "interface": """你是 Narrative Interface / Tone Voltage 发散者。你看不到未来世界、主角形态、Power 与具体剧情。只创造“行动怎样被看见、记录、误读、观看、传播、结算或跨越另一层现实”，以及这种界面带来的语气和即时压力。

生成 3 个互不换皮的 Interface Spark。它不是 UI 功能表，也不是必须有面板；可以是公开传播、异层观看、游戏／仪式／记录／叙述者关系、时间差、双重现场或其它具体介质。每个都要真正改变人物敢不敢做、别人如何反应或读者如何获得额外信息。至少一个允许强烈幽默、荒诞或低俗生命力，不全部写成庄严神秘。

严格格式：
# INTERFACE AXIS SPARKS
## I1｜短标签
Core: 一句话写行动通过什么具体界面产生第二层后果
### 第一章立刻施加的压力
### 谁能看见、谁会误解、谁能回应
### 反复使用后的关系／名声／风险复利
### 语气电压
### 不要膨胀成的系统
## I2｜短标签
（同结构）
## I3｜短标签
（同结构）
""",
}


SINGLE_PASS_PROMPT = """你是 Single-Agent Premise Forge。你一次同时设计世界异常、主角存在形态、直接特权与叙事界面，用来测试单代理在明确要求“大胆”时是否仍会过早自洽。

生成 3 个完整候选：S1 追求最强商业吸引力而非最安全；S2 主动再大胆一档；S3 可以极端，但必须一句话可懂。不要自动选择。三者不能只是同一个人类修士、同一种升级循环换世界名。

字段边界必须真实可拆：`World Interface-only Direction` 只写即使换掉主角也成立的观看／记录／传播规则，不提主角、Power 或开篇事件；`Initial Origin-only Direction` 只写第一场事件发生前已经成立的 T0 出生位置、诞生方式与零点经历，不补未来剧情；`Initial Scale Position-only Direction` 必须逐条写主角 T0 在 World 已定义每一条适用主尺／副尺上的精确位置，不适用也必须明确写 `不适用` 及原因，不能让 Human / Power 临时发明 `0级`、`尺外` 或默认一阶；`Power-only Direction` 必须把触发、目标类别、能做的动作与永久边界写清，不能靠 Story 再补。作者选择后，这些字段会被代码作为各 lane 的硬约束分别投影，所以不能把关键事实只藏在第一章画面、Compilation Trace 或最小桥梁里。

大胆不等于先写一个震撼镜头，再让下游临时发明机制把它圆上。每个候选必须 **Authority-compilable**：
- 第一章每个超常结果都要能从已经写明的 World / Interface / Ontology / T0 Origin / Power 直接推出；触发尚未满足时不得提前使用该能力，除非 `Power-only Direction` 明确写出一次性的 T0 例外及其边界。
- Interface 默认只能观看、记录、传播或改变社会后果，不能偷偷复制、放大或改写 Power 的因果覆盖；若它本身会路由因果，必须作为对所有相关行动者都成立的 protagonist-blind World 规则写清。
- 主角 T0 若落在公开力量尺之外，World-only 必须先定义一个不依赖主角的通用位置或类别；不能等 Human / Story 把 `0级`、`尺外` 或 `未登记` 临时解释出来。
- 20章与百章图景只能复合已经存在的规则，不得假设未写明的全城共同载体、无限复制、中央控制或新能力。
- `Authority-Compilation Trace` 不是自夸总结。逐项写出“具体动作／结果 → 精确来源字段 → 触发是否已满足 → 目标／载体 → 为什么合法”；发现无法闭合就修改候选本身，而不是写“后续解释”。

严格格式：
# SINGLE-PASS PREMISE CANDIDATES
## S1｜概念名
### 一句话货架简介
### World-only Direction
### World Interface-only Direction
### Protagonist Ontology-only Direction
### Initial Origin-only Direction
### Initial Scale Position-only Direction
### Power-only Direction
### Story Interface / Opening Promise
### Authority-Compilation Trace
### 第一章标志性画面
### 主角反复会做的新动作
### 第一次不公平兑现
### 20章玩法扩张
### 100章以上仍能长出的不同故事
### 最小可信桥梁
### 不可磨平的三点
## S2｜概念名
（同结构）
## S3｜概念名
（同结构）
"""


PREMISE_COMPILER_PROMPT = """你是 TGN 的 Premise Authority Compiler。你只检查候选能否被后续 World / Power / Human / Story Authority 精确实现；你不是创意 Judge、商业评分器、自动 selector 或改稿人。

对 S1 / S2 / S3 分别做约束可满足性审计。大胆、怪异、主角占便宜大、奖励多都不是错误；只有字段缺失、触发未满足、目标或载体不在覆盖内、精确尺位置无 World 公共语法、Interface 偷做 Power 因果、开篇或远期动作依赖未写明机制时，才判冲突。

必须逐项检查：
1. 第一章每个超常动作／结果，是否真的由 World / Interface / Ontology / Origin / Initial Scale Position / Power 明文推出；不能因为候选自己的 `Authority-Compilation Trace` 声称合法就放行。
2. 触发发生前是否已经满足；目标是否真的完成了规则要求的进入、接触、击败、死亡、命名、穿越或其它状态变化；载体、门、出口、身体、空间和见证者是否在当时真实存在。
3. Interface 是否只观看、记录、传播或改变社会后果；不能暗中复制、移动、放大、远程路由或改写 Power。
4. T0 精确位置是否被 protagonist-blind World 的公开主尺或已定义副尺容纳；不能让下游临时新增 0 级、尺外类别或主角专属尺度。
5. 第一次不公平兑现、20 章终局与百章 runway 是否只复合已经定义的操作；不能假设共同载体、无限复制、凭空多出的出口、未写明的等级跃迁或新能力。
6. 对 PASS / CONDITIONAL PASS 候选，也要说明 Changed Verbs、货架画面与激进度是否仍被保留；不得把“改保守”当默认修复方向。

严格输出：

# PREMISE AUTHORITY COMPILER
## S1
- Verdict: PASS / CONDITIONAL PASS / FAIL
- Opening legality:
- Scale legality:
- Long-form legality:
- Exact hidden bridges:
- Boldness preserved:
## S2
（同结构）
## S3
（同结构）
## Author-facing result
只列出每张卡的可编译状态与精确冲突。不得评分、排名、替作者选择、自动修复，或建议新增章节期 Reviewer / Gate。

# CANDIDATES
{CANDIDATES}
"""


SELECTED_PREMISE_COMPILER_PROMPT = """你是 TGN 的 Premise Authority Compiler。你只复核一张已经由作者选中的候选，判断它能否被后续 World / Power / Human / Story Authority 精确实现；你不是创意 Judge、商业评分器、自动 selector 或改稿人。

大胆、怪异、主角占便宜大、奖励多都不是错误。逐项检查：
1. 第一章每个超常动作／结果是否由已写 World / Interface / Ontology / Origin / Initial Scale Position / Power 直接推出；
2. 触发、目标、真实载体、出口、门、见证者和先后顺序在当时是否实际存在；
3. Interface 是否只记录／传播／改变社会后果，而没有偷做 Power；
4. T0 与后续等级跃迁是否被 protagonist-blind 的公共力量尺和已写成长规则容纳；
5. 第一次兑现、20 章终局与百章 runway 是否只复合既有操作，没有凭空新增出口、共同载体、复制、中央控制或等级跃迁；
6. 修复后的一句话货架承诺、非标准 Ontology、Changed Verbs 与不可磨平项是否仍然完整。

严格输出：

# SELECTED PREMISE AUTHORITY COMPILER
## {CANDIDATE_ID}
- Verdict: PASS / CONDITIONAL PASS / FAIL
- Opening legality:
- Scale legality:
- Long-form legality:
- Remaining hidden bridges:
- Protected creative core:

`PASS` 只允许用于所有动作已经明文闭合的候选。若仍需新增规则、出口、见证者、过门过程或等级映射，必须判 `CONDITIONAL PASS` 或 `FAIL`，并精确指出。

# SELECTED CANDIDATE
{CANDIDATE}
"""


PREMISE_REPAIR_PROMPT = """你是 TGN 的 Selected Premise Contract Repairer。你只修复一张作者已选候选中的因果不可编译点；你不是重新发散者、自动 selector、降风险编辑或下游 Story Writer。

这是一次 **最小约束修复**：
- 必须逐项解决 Compiler Report 中的所有 Opening / Scale / Long-form 冲突；不能写“后续解释”、不能把冲突移到 Story Program。
- 必须原样保留候选标题，以及 `一句话货架简介`、`Protagonist Ontology-only Direction`、`主角反复会做的新动作`、`不可磨平的三点` 四个受保护字段。
- 可以修改 World / World Interface / T0 Origin / Initial Scale Position / Power / Opening Promise / Compilation Trace / 第一章画面 / 第一次兑现 / 20章与百章展开，但只能为闭合已指出的因果；不得新增第二个同等高电压核心幻想。
- 不得把非人主角还原成人形，不得把核心动作改成分析、维护、管理、审核或效率优势，不得削弱第一次不公平兑现来换取可编译性。
- 修复后的每个超常结果都要写清真实触发、目标、载体、出口、见证者和当时已拥有的尺度位置；长期跃迁必须给出可复述的逐级组合，而不是从一次获得直接跳到顶级。
- 输出完整的单张 `## {CANDIDATE_ID}` 候选，不要写修订说明、评分或其它候选。

# LOCKED CREATIVE CORE｜必须逐字保留
{LOCKED_CORE}

# COMPILER REPORT｜必须逐项清零
{COMPILER_REPORT}

# ORIGINAL SELECTED CANDIDATE
{CANDIDATE}
"""


PREMISE_REPAIR_PROTECTED_HEADINGS: tuple[str, ...] = (
    "一句话货架简介",
    "Protagonist Ontology-only Direction",
    "主角反复会做的新动作",
    "不可磨平的三点",
)


COLLISION_PROMPT = """你是 Orthogonal Collision Forge。下方四组组件来自彼此隔离的 fresh context，并已由代码固定配对。你的任务不是选择更兼容的组件，也不是把它们统一成同一主题，而是寻找一个最小、具体、可读的碰撞方式。

强制规则：
- 每个候选必须逐字复制四条 `Core:` 内容到 `Locked Cores`；不得删除、替换、抽象化或降格成背景。
- 只能增加最多 3 条 Minimal Coherence Bridge。解释够主角在第一章行动即可，不建立百科、终极真相或统一 ontology。
- 碰撞后的简介必须让读者看见一幅具体场面、主角新增的动作、一次立即不公平的收益，以及别人/观众/关系的反应。
- 不要把非人形态偷偷改回普通人，不要把直接特权改成分析技能，不要把叙事界面改成可有可无的 UI。
- 候选之间不评分、不排名。

严格格式：
# ORTHOGONAL PREMISE COLLISIONS
## C1｜概念名
Source Lock: W1 + O2 + P3 + I1
### Locked Cores
World: <逐字复制>
Ontology: <逐字复制>
Privilege: <逐字复制>
Interface: <逐字复制>
### 一句话货架简介
### 第一章标志性画面
### 主角从此会反复做的新动作
### 第一次不公平兑现与现场反应
### 可持续 Story Engine
### 20章内怎样真正换挡
### 100章以上为什么不会只剩同一招放大
### Minimal Coherence Bridge（最多3条）
### 不可磨平的三点
## C2｜概念名
（严格使用 Source Lock: W2 + O3 + P1 + I2，同结构）
## C3｜概念名
（严格使用 Source Lock: W3 + O1 + P2 + I3，同结构）
"""


VOLTAGE_BUDGET_PROMPT = """你是 Asymmetric Voltage Budget Forge。下方组件仍来自彼此隔离的 fresh context，但这次每个候选只允许两个 premise-level 高电压押注：一个 Primary Bet，一个 Collision Friction。其余维度必须故意保持熟悉、低电压或留给后续独立 Authority。

这是对“四个好点同时说话”的纠偏，不是保守化：
- 一句话货架简介只能有一个主要幻想名词／动作，再加一个清楚的麻烦；不能连续列四套机制。
- 必须逐字复制两条 Locked Core；不得把它们磨平、互相解释成同一隐喻或合并成一个统一真相。
- 未锁定的轴不得再创造新的世界级异常、非人 Ontology、特殊 Power 或 Narrative Interface。
- 可以补最多 2 条 Minimal Coherence Bridge，只够第一章行动；不能建立百科、使命或终局。
- 主角必须有具体欲望、动作、首次不公平兑现或立即处境逆转；低电压不等于没有故事。
- 不评分、不排名。

严格格式：
# ASYMMETRIC VOLTAGE BUDGET CANDIDATES
## V1｜概念名
Source Lock: W1 + P2
Primary Bet: World pressure
### Locked Cores
World: <逐字复制 W1 Core>
Privilege: <逐字复制 P2 Core>
### 一句话货架简介
### 第一章标志性画面
### 主角反复会做的新动作
### 第一次兑现与现场反应
### 20章真实换挡
### 100章以上的不同故事姿态
### Low-voltage Support
### Minimal Coherence Bridge（最多2条）
### 最可能失败的地方
## V2｜概念名
（严格使用 Source Lock: O3 + P1；Ontology 为 Primary Bet；世界保持熟悉具体、无特殊 Interface，同结构）
## V3｜概念名
（严格使用 Source Lock: W3 + I3；World 为 Primary Bet；普通人形、特殊 Power 留给后续，同结构）
"""


def _input_block(label: str, content: str) -> str:
    return f"# {label}\n\n{content.strip() or '（无）'}"


def build_single_pass_prompt(*, author_direction: str) -> str:
    return "\n\n".join(
        (
            BOLD_PREMISE_CRAFT.strip(),
            SINGLE_PASS_PROMPT.strip(),
            _input_block("作者方向与硬约束", author_direction),
        )
    ).strip() + "\n"


def build_premise_compiler_prompt(*, candidates: str) -> str:
    """Build an author-facing satisfiability check, never an automatic selector."""

    sections = extract_sections(candidates, prefix="S")
    if tuple(sections) != ("S1", "S2", "S3"):
        raise ValueError(
            "Premise compiler 需要且只接受 `## S1` / `## S2` / `## S3` 三张候选"
        )
    return PREMISE_COMPILER_PROMPT.replace(
        "{CANDIDATES}", candidates.strip()
    ).strip() + "\n"


def _single_candidate_id(candidate: str) -> str:
    sections = extract_sections(candidate, prefix="S")
    if len(sections) != 1:
        raise ValueError("Selected premise compiler 需要且只接受一张 `## S#` 候选")
    return next(iter(sections))


def normalize_single_candidate_response(*, text: str, expected_id: str) -> str:
    """Drop a harmless ACP preamble while failing closed on extra candidates."""

    titled = list(re.finditer(r"## (S[1-9])｜[^\r\n]+", text))
    if not titled:
        raise ValueError(f"Premise response 缺少带标题的 `## {expected_id}｜...`")
    if len(titled) != 1 or titled[0].group(1) != expected_id:
        actual = tuple(match.group(1) for match in titled)
        raise ValueError(
            f"Premise response 必须且只包含 `## {expected_id}`，实际为 {actual}"
        )
    normalized = text[titled[0].start() :].strip()
    sections = extract_sections(normalized, prefix="S")
    if tuple(sections) != (expected_id,):
        raise ValueError(
            f"Premise response 必须且只包含 `## {expected_id}`，实际为 {tuple(sections)}"
        )
    return sections[expected_id].strip() + "\n"


def _single_candidate_heading(candidate: str) -> str:
    candidate_id = _single_candidate_id(candidate)
    match = re.search(
        rf"(?m)^## {re.escape(candidate_id)}(?:｜[^\n]*)?\s*$",
        candidate,
    )
    if not match:
        raise ValueError("Selected premise 缺少候选标题")
    return match.group(0).strip()


def build_selected_premise_compiler_prompt(*, candidate: str) -> str:
    """Build a strict satisfiability recheck for one author-selected card."""

    candidate_id = _single_candidate_id(candidate)
    build_single_pass_lane_bundle(candidate)
    return (
        SELECTED_PREMISE_COMPILER_PROMPT.replace("{CANDIDATE_ID}", candidate_id)
        .replace("{CANDIDATE}", candidate.strip())
        .strip()
        + "\n"
    )


def build_premise_repair_prompt(*, candidate: str, compiler_report: str) -> str:
    """Repair causality while code-locking the selected card's creative core."""

    candidate_id = _single_candidate_id(candidate)
    build_single_pass_lane_bundle(candidate)
    protected = [_single_candidate_heading(candidate)] + [
        extract_level3_section(candidate, heading=heading)
        for heading in PREMISE_REPAIR_PROTECTED_HEADINGS
    ]
    return (
        PREMISE_REPAIR_PROMPT.replace("{CANDIDATE_ID}", candidate_id)
        .replace("{LOCKED_CORE}", "\n\n".join(protected))
        .replace("{COMPILER_REPORT}", compiler_report.strip())
        .replace("{CANDIDATE}", candidate.strip())
        .strip()
        + "\n"
    )


def validate_premise_repair(*, original: str, repaired: str) -> dict[str, bool]:
    """Fail closed if a causal repair changes the author-selected creative core."""

    original_id = _single_candidate_id(original)
    repaired_id = _single_candidate_id(repaired)
    if repaired_id != original_id:
        raise ValueError(
            f"Premise repair 改变候选编号：{original_id} -> {repaired_id}"
        )
    if _single_candidate_heading(original) != _single_candidate_heading(repaired):
        raise ValueError("Premise repair 改写候选标题")
    build_single_pass_lane_bundle(repaired)
    checks: dict[str, bool] = {}
    changed: list[str] = []
    for heading in PREMISE_REPAIR_PROTECTED_HEADINGS:
        preserved = extract_level3_section(
            original, heading=heading
        ) == extract_level3_section(repaired, heading=heading)
        checks[heading] = preserved
        if not preserved:
            changed.append(heading)
    if changed:
        raise ValueError("Premise repair 改写受保护字段：" + "、".join(changed))
    return checks


def build_axis_prompt(*, axis: AxisName, author_direction: str) -> str:
    try:
        axis_prompt = _AXIS_PROMPTS[axis]
    except KeyError as error:
        raise ValueError(f"未知 Premise Aperture axis：{axis}") from error
    return "\n\n".join(
        (
            BOLD_PREMISE_CRAFT.strip(),
            axis_prompt.strip(),
            _input_block("作者方向与硬约束", author_direction),
        )
    ).strip() + "\n"


def extract_sections(text: str, *, prefix: str) -> dict[str, str]:
    """Extract stable `## XN` markdown sections from an aperture response."""

    pattern = re.compile(rf"(?m)^## ({re.escape(prefix)}[1-9])(?:｜[^\n]*)?\s*$")
    matches = list(pattern.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1)] = text[match.start() : end].strip()
    return sections


def extract_core(section: str) -> str:
    match = re.search(r"(?m)^Core:\s*(.+?)\s*$", section)
    if not match:
        raise ValueError("Premise axis section 缺少单行 Core")
    return match.group(1).strip()


def has_explicit_premise_conflict(text: str) -> bool:
    """Detect a fail-loud conflict declaration, not a prose mention of its token.

    Agents are allowed to say that a lane *does not* trigger the conflict.  A
    raw substring check would mistake that confirmation for a failure.  Prefer
    a standalone declaration; also accept the common ACP shape where a short
    reasoning preamble ends with the token and the next paragraph explicitly
    refuses generation.
    """

    standalone = re.search(
        r"(?mi)^\s*(?:#{1,6}\s*)?`?PREMISE-AUTHORITY CONFLICT`?(?:\s*[:：].*|\s*)$",
        text,
    )
    if standalone:
        return True

    token = re.search(r"`?PREMISE-AUTHORITY CONFLICT`?", text, flags=re.I)
    if not token:
        return False
    nearby = text[token.end() : token.end() + 500]
    return bool(
        re.search(
            r"当前不能(?:安全)?生成|不能安全生成|停止生成|无法继续|必须先由作者|故本轮停止",
            nearby,
        )
    )


def extract_level3_section(text: str, *, heading: str) -> str:
    """Extract one exact `###` section without leaking sibling premise fields."""

    pattern = re.compile(rf"(?m)^### {re.escape(heading)}\s*$")
    match = pattern.search(text)
    if not match:
        raise ValueError(f"Premise candidate 缺少字段：{heading}")
    sibling = re.search(r"(?m)^### \S", text[match.end() :])
    end = match.end() + sibling.start() if sibling else len(text)
    body = text[match.end() : end].strip()
    if not body:
        raise ValueError(f"Premise candidate 字段为空：{heading}")
    return f"### {heading}\n\n{body}"


def build_single_pass_lane_bundle(candidate_section: str) -> PremiseLaneBundle:
    """Compile an author-selected premise into isolated, lane-frozen directions."""

    if not re.search(r"(?m)^## S[1-9](?:｜[^\n]*)?\s*$", candidate_section):
        raise ValueError("Single-pass lane compiler 需要单个 `## S#` candidate section")
    world = extract_level3_section(candidate_section, heading="World-only Direction")
    world_interface = extract_level3_section(
        candidate_section, heading="World Interface-only Direction"
    )
    ontology = extract_level3_section(
        candidate_section, heading="Protagonist Ontology-only Direction"
    )
    origin = extract_level3_section(
        candidate_section, heading="Initial Origin-only Direction"
    )
    scale_position = extract_level3_section(
        candidate_section, heading="Initial Scale Position-only Direction"
    )
    privilege = extract_level3_section(candidate_section, heading="Power-only Direction")
    interface = extract_level3_section(
        candidate_section, heading="Story Interface / Opening Promise"
    )
    # The trace is discarded after selection, but its presence forces the
    # complete-premise generator to expose opening legality before lane split.
    extract_level3_section(candidate_section, heading="Authority-Compilation Trace")
    return PremiseLaneBundle(
        world=world,
        world_interface=world_interface,
        ontology=ontology,
        origin=origin,
        scale_position=scale_position,
        privilege=privilege,
        interface=interface,
        collision=candidate_section.strip(),
    )


def build_collision_prompt(
    *,
    author_direction: str,
    world_sparks: Mapping[str, str],
    ontology_sparks: Mapping[str, str],
    privilege_sparks: Mapping[str, str],
    interface_sparks: Mapping[str, str],
    matrix: tuple[CollisionSpec, ...] = DEFAULT_COLLISION_MATRIX,
) -> str:
    pools: dict[str, Mapping[str, str]] = {
        "W": world_sparks,
        "O": ontology_sparks,
        "P": privilege_sparks,
        "I": interface_sparks,
    }
    blocks: list[str] = [BOLD_PREMISE_CRAFT.strip(), COLLISION_PROMPT.strip()]
    for spec in matrix:
        ids = (spec.world_id, spec.ontology_id, spec.privilege_id, spec.interface_id)
        chosen: list[str] = []
        for spark_id in ids:
            pool = pools[spark_id[0]]
            if spark_id not in pool:
                raise ValueError(f"Collision 缺少 spark：{spark_id}")
            chosen.append(pool[spark_id])
        blocks.append(_input_block(f"{spec.candidate_id} FIXED COMPONENTS", "\n\n".join(chosen)))
    blocks.append(_input_block("作者方向与硬约束", author_direction))
    return "\n\n".join(blocks).strip() + "\n"


def build_voltage_budget_prompt(
    *,
    author_direction: str,
    world_sparks: Mapping[str, str],
    ontology_sparks: Mapping[str, str],
    privilege_sparks: Mapping[str, str],
    interface_sparks: Mapping[str, str],
    matrix: tuple[VoltageBudgetSpec, ...] = DEFAULT_VOLTAGE_BUDGET_MATRIX,
) -> str:
    pools: dict[str, Mapping[str, str]] = {
        "W": world_sparks,
        "O": ontology_sparks,
        "P": privilege_sparks,
        "I": interface_sparks,
    }
    blocks: list[str] = [BOLD_PREMISE_CRAFT.strip(), VOLTAGE_BUDGET_PROMPT.strip()]
    for spec in matrix:
        selected_sections: list[str] = []
        for spark_id in (spec.first_id, spec.second_id):
            pool = pools[spark_id[0]]
            if spark_id not in pool:
                raise ValueError(f"Voltage Budget 缺少 spark：{spark_id}")
            selected_sections.append(pool[spark_id])
        metadata = "\n".join(
            (
                f"Primary Bet: {spec.primary_bet}",
                f"Low-voltage Rule: {spec.low_voltage_rule}",
            )
        )
        blocks.append(
            _input_block(
                f"{spec.candidate_id} FIXED TWO-BET COMPONENTS",
                "\n\n".join((metadata, *selected_sections)),
            )
        )
    blocks.append(_input_block("作者方向与硬约束", author_direction))
    return "\n\n".join(blocks).strip() + "\n"


def validate_collision_locks(
    collision_text: str,
    *,
    world_sparks: Mapping[str, str],
    ontology_sparks: Mapping[str, str],
    privilege_sparks: Mapping[str, str],
    interface_sparks: Mapping[str, str],
    matrix: tuple[CollisionSpec, ...] = DEFAULT_COLLISION_MATRIX,
) -> dict[str, list[str]]:
    """Return missing locked core IDs per collision candidate; empty means preserved."""

    collision_sections = extract_sections(collision_text, prefix="C")
    pools: dict[str, Mapping[str, str]] = {
        "W": world_sparks,
        "O": ontology_sparks,
        "P": privilege_sparks,
        "I": interface_sparks,
    }
    missing: dict[str, list[str]] = {}
    for spec in matrix:
        section = collision_sections.get(spec.candidate_id, "")
        absent: list[str] = []
        for spark_id in (spec.world_id, spec.ontology_id, spec.privilege_id, spec.interface_id):
            core = extract_core(pools[spark_id[0]][spark_id])
            if core not in section:
                absent.append(spark_id)
        if absent:
            missing[spec.candidate_id] = absent
    return missing


def validate_voltage_budget_locks(
    budget_text: str,
    *,
    world_sparks: Mapping[str, str],
    ontology_sparks: Mapping[str, str],
    privilege_sparks: Mapping[str, str],
    interface_sparks: Mapping[str, str],
    matrix: tuple[VoltageBudgetSpec, ...] = DEFAULT_VOLTAGE_BUDGET_MATRIX,
) -> dict[str, list[str]]:
    budget_sections = extract_sections(budget_text, prefix="V")
    pools: dict[str, Mapping[str, str]] = {
        "W": world_sparks,
        "O": ontology_sparks,
        "P": privilege_sparks,
        "I": interface_sparks,
    }
    missing: dict[str, list[str]] = {}
    for spec in matrix:
        section = budget_sections.get(spec.candidate_id, "")
        absent: list[str] = []
        for spark_id in (spec.first_id, spec.second_id):
            core = extract_core(pools[spark_id[0]][spark_id])
            if core not in section:
                absent.append(spark_id)
        if absent:
            missing[spec.candidate_id] = absent
    return missing


def build_lane_bundle(
    *,
    selected: CollisionSpec,
    collision_text: str,
    world_sparks: Mapping[str, str],
    ontology_sparks: Mapping[str, str],
    privilege_sparks: Mapping[str, str],
    interface_sparks: Mapping[str, str],
) -> PremiseLaneBundle:
    collisions = extract_sections(collision_text, prefix="C")
    if selected.candidate_id not in collisions:
        raise ValueError(f"Collision response 缺少 {selected.candidate_id}")
    try:
        return PremiseLaneBundle(
            world=world_sparks[selected.world_id],
            ontology=ontology_sparks[selected.ontology_id],
            privilege=privilege_sparks[selected.privilege_id],
            interface=interface_sparks[selected.interface_id],
            collision=collisions[selected.candidate_id],
        )
    except KeyError as error:
        raise ValueError(f"Lane bundle 缺少 spark：{error.args[0]}") from error


def render_lane_direction(bundle: PremiseLaneBundle, *, lane: LaneName) -> str:
    """Project author-selected constraints without leaking the complete premise across lanes."""

    if lane == "world":
        parts = [
            "# AUTHOR-SELECTED WORLD PREMISE CONSTRAINTS｜批准前非 World Canon\n"
            "这些是作者已选择的 World-lane 硬约束，不是可被安全化、换义或删去的灵感。"
            "World Agent 仍不知道未来主角、Ontology、Power、Biography 与 Story；必须在 protagonist-blind 的前提下实现全部世界事实。",
            bundle.world,
        ]
        if bundle.world_interface:
            parts.extend(
                (
                    "# AUTHOR-SELECTED WORLD INTERFACE CONSTRAINTS｜仍保持 protagonist-blind\n"
                    "以下观看／记录／传播规则对世界中的所有相关行动成立；不得降格成偶尔使用的舞台效果，也不得偷接未来主角。",
                    bundle.world_interface,
                )
            )
        return "\n\n".join(parts).strip() + "\n"
    if lane == "power":
        return "\n\n".join(
            (
                "# AUTHOR-SELECTED ONTOLOGY BASELINE｜不是人格／故事\n"
                "这是作者已选择的 literal body / existence baseline。只用于判断普通动作与承载条件；不得恢复标准人形或发明 Biography。",
                bundle.ontology,
                "# AUTHOR-SELECTED INITIAL SCALE POSITION｜不是 Biography／Story\n"
                "这是作者已选择的 T0 精确尺位。Power Agent 必须让能力起始状态与它一致，"
                "不得补零级、默认一阶、擅自提升或把不适用的主尺强套给非人存在。",
                bundle.scale_position,
                "# AUTHOR-SELECTED POWER PREMISE CONSTRAINTS｜批准前非 Power Canon\n"
                "以下触发、目标类别、可执行动作、载体／消耗与永久边界全部是作者硬约束。"
                "所有 Power 候选都必须逐项保留；不得静默扩大、缩窄、替换或把直接动作改成分析能力。"
                "仍可独立设计早期用法、复合成长与高阶表现，但不得读取完整 Collision 或发明 Biography。",
                bundle.privilege,
            )
        ).strip() + "\n"
    if lane == "human":
        parts = [
            "# AUTHOR-SELECTED HUMAN PREMISE CONSTRAINTS｜不是 Power／Story\n"
            "Human 仍不知道未来特殊能力和 Story Opportunities。Ontology 是 literal T0 body，不是象征、临时服装或可恢复的人类状态。",
            bundle.ontology,
        ]
        if bundle.origin:
            parts.extend(
                (
                    "# AUTHOR-SELECTED T0 ORIGIN CONSTRAINTS\n"
                    "以下诞生位置、诞生方式与第一场事件前的零点事实不可搬移、提前或改写。"
                    "不得在这个 T0 之前补训练、关系、职业履历、旧选择或另一段 Biography。",
                    bundle.origin,
                )
            )
        if bundle.scale_position:
            parts.extend(
                (
                    "# AUTHOR-SELECTED INITIAL SCALE POSITION｜不是特殊 Power／Future Story\n"
                    "Human Agent 必须从这组精确 T0 尺位开始，不得自行补写更早训练、默认等级或尺外零位。",
                    bundle.scale_position,
                )
            )
        return "\n\n".join(parts).strip() + "\n"
    if lane == "story":
        return "\n\n".join(
            (
                "# AUTHOR-SELECTED FROZEN STORY PROMISE｜不新增第四 Authority\n"
                "Story Program 第一次看到完整碰撞。World / Human / Power 的分 lane 硬约束理应已在批准 Authority 中实现；"
                "必须保护标志性画面、核心新动作、第一次不公平兑现、Interface 与不可磨平项。"
                "若批准 Authority 仍与这些作者约束冲突，必须明确返回 `PREMISE-AUTHORITY CONFLICT`，不得静默删去、缩窄或用更安全的机制替代。",
                bundle.collision,
                "# SELECTED NARRATIVE INTERFACE",
                bundle.interface,
            )
        ).strip() + "\n"
    raise ValueError(f"未知 Premise Aperture lane：{lane}")
