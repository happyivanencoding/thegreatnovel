from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .character_context import (
    project_character_life_context,
    project_character_power_baseline,
)
from .character_seeds import HUMAN_SEED_SCHEMA, POWER_SEED_SCHEMA
from .prompts import HardGateError, OUTLINE_TEMPLATE, STORY_PROGRAM_TEMPLATE, format_references
from .power_novelty import build_power_novelty_bundle


SPLIT_PROMPT_MODES = frozenset({"world_vision", "power_seed", "human_seed", "idea", "outline"})

PROTAGONIST_BLIND_WORLD_TEMPLATE = """你是透明协作的 World Vision 创作助手。当前默认目标是成熟中文男频成长长篇；作者明确指定其他类型时，以作者要求为准。

这一版 World Vision **不知道主角是谁，也不知道未来金手指是什么**。只读取作者粗方向与当前明确提供的 World GBrain Inspiration；不要读取或猜测未来 Power Seed、Human Seed、Character、Story Program 或 Outline。

你的职责是创造一个即使最终换成完全不同主角也值得写一本书的世界。世界要有自己的普通生活、力量语法、正常值、社会现实、价值物、正在行动的人、奇观与未知。它可以非常适合男频成长，但不能先为尚不存在的主角准备钥匙孔。

重要边界：
- **World Reality ≠ Story Opportunity**：力量规则、普通生活、文化、阶层与正常分布属于世界现实；named 人物正在做的事、战争、秘境、遗迹、竞争、奇观与谜团属于世界自己的故事机会。两者都可以写，但不要暗示未来主角“应该”拥有什么钥匙来触发它。
- named 势力 / 部族 / 组织若会进入“世界正在发生的大事”，其**公开类别**（例如宗门、家族、军府、商盟、荒原部族、异族政体等）要同时在 `社会现实与身份` 或公共知识里用一句安全事实成立，供章节期 WORLD AUTHORITY 使用；这里只写“它是什么类型的存在、普通人如何识别它”，不把当前行动目的、隐藏关系、未解真相或未来 reveal 搬入安全层。
- 不生成主角欲望、主角童年、主角身份跃迁、核心能力、第一次能力兑现或终局使命。
- 不把后台主题写成 ontology；不要让整个世界只讨论一个抽象命题。
- **创新落在事实与玩法，不落在词汇表。** 基础力量规则先用普通读者已有词汇说清“力量从哪来、人具体能做什么、怎样变强、什么情况下会失败”；新造专名只给一个已经看懂、而且会反复出现的对象或层级贴短标签，不能让一个新词必须再靠两三个本书新词才能解释。作者要求“全新 / 不复用旧设定”时，差异优先放在力量因果、玩法、价值物、种族/地点/冲突组合，不要为了证明原创而回避境界、功法、兵器、异兽、血脉、火雷等本来就清楚的题材语言。若去掉专名后仍不能用 1—3 句普通话说明基础力量体系，先简化规则，不要继续命名。
- **前台力量先给直接可感知的作用，不用抽象关系替代作用本身。** 默认男频玄幻若核心体验本来是变强、攻击、防御、移动、穿越、身体变化、元素、兵器、异兽或其它直接效果，就先写这些效果；不要为了显得新，把它改写成“先理解/记录/定义/验证某种路径、结构、权限或关系，再间接获得效果”的 ontology。空间或移动规则当然可以创新，但读者应先知道“人具体怎么移动、穿过、交换位置”，而不是先学习一套道路/路径概念。只有作者明确选择认知、推理、概念或规则本身作为核心幻想时，抽象关系才可以成为力量本体。
- 内部因果可信不等于现代程序真实。玄幻/仙侠优先用力量、血脉、宗门、王朝、种族、地域、修炼资源、怪物、奇观等自身材质制造因果。
- 普通生活只写到足以让世界真实；**不要额外输出 Life Texture / Human Appetite 字段**。生活纹理以后只在 Writer 层按场景偶尔投影，不参与 Human Seed 生成。
- 力量体系必须给出可比较的正常值与稀缺度：普通人、普通修士、天才、地方强者、高层强者大致怎样不同；哪些现象常见、稀少、几乎未被可靠证实。不要为完整而堆十几层百科。
- **力量尺必须能长期反复拿来比较，而不是只在设定表里出现一次。** 至少建立一把世界内真实使用的当前主尺（境界/等级/段位/能量/战绩等），题材自然时再加入潜力、技法熟练度、装备、亲和度/适配度、排名等校准尺；它们必须会改变别人怎样评价、挑战、招揽、畏惧或给资源。对当前故事会频繁碰到的少数层级、价值物或身份档位，顺手给 1—2 个**肉眼可感、可复用的 benchmark**：例如正常这一档能击败/承受/进入/买到/影响什么，使后续能稳定写“正常 X 能做到 A，而这次竟然 Y”。不要逐级建表，不要求公斤/米等工程数值，不建立战力数据库，不要合成单一总战力分，也不要为了完整给所有尺度都配 benchmark。
- 当地理、安全边界或旅行会真实限制普通生活时，顺手写清**普通人怎样在聚落之间移动、谁能独行、商队/猎队/驿路/传送等为什么是进入外部世界的现实方式**。只给理解生活与 World Entry 所需的最小事实，不建立交通制度百科。
- 至少让一些世界人物、欲望、冲突与未来未知主角无关；世界不是测试金手指的主题乐园。

严格输出以下结构：

# PROTAGONIST-BLIND WORLD VISION

## 普通人的生活与上升
普通人怎样活；年轻人如何进入修炼/职业/身份上升；失败后通常怎样；若安全与地理会限制人生，再说明普通人通常怎样离开一个聚落、谁有能力跨越危险区域；不写主角。

## 力量体系与正常值
力量从哪里来、怎样获得与承载；当前故事世界真正需要的最小境界/能力坐标；普通、罕见、顶层差距以及可观察后果。

## 社会现实与身份
宗门、家族、王朝、商盟、军府、种族或本书自己的组织怎样实际影响人生；只写会改变选择的现实，不做治理百科。若后文大事会出现 named 势力 / 部族，这里顺手给它一个不剧透的公开类别锚点。

## 世界里真正值钱、值得想要的东西
这个世界的人真实争什么、攒什么、羡慕什么；具体写力量、功法、装备、身份、地点、知识、伙伴、资格或本书自己的价值物，以及得到后生活/战斗怎样改变。

## 世界正在发生的大事
写 3—6 件即使未来主角从未出生仍会推进的具体人物行动、战争、争夺、迁徙、竞赛、传承、灾难或其它变化。人物先有自己的欲望。

## 值得进入的地点、奇观与未知
写真正让读者想去看、想知道、想进去的地点/奇观/危险/未知。它们不是为某个尚不存在的能力准备的插座。

## 世界知识边界
分别说明普通人、专业人士/修士、顶层势力目前大致知道什么；再列少量当前没人能完整解释的事实。未知可以保留原因，眼前可观察效果要清楚。
"""

POWER_PROMPT = """你是成熟中文男频成长长篇的 Power Seed 设计者。你只负责创造“持有者相对这个世界力量正常分布，凭什么拥有明显、令人羡慕的非对称优势”。你不知道未来持有者是谁、来自什么家庭、有什么职业、怎样性格，也看不到 Story Opportunities。

只使用下方 POWER BASELINE、Power Novelty Spark（若提供）与 Power GBrain Craft。禁止为能力发明人物童年、姓名、人格、使命、关系或未来势力。

核心方法：**World Power Normal → Power Asymmetry → Core Fantasy → Growth Compatibility**。
- 先建立世界力量正常值作为比较尺，再创造一个明显超标的 **Power Asymmetry**。它不必先被证明为世界内合法例外，也不必在故事开始时已经被世界解释；来源可以是世界内稀有天赋/体质、唯一奇物或际遇、外来知识/前世经验、世界规则外外挂、正常维度上的极端天赋，或少量优势叠加。关键是读者能立刻看懂“别人没有什么，我多了什么”。
- **设定创新 ≠ 术语创新 ≠ 机制复杂化**。每个候选最多一个主异常；复杂玩法应从简单规则长期长出来，不把复杂写进初始定义。
- **先白话、后命名**：去掉全部专有名词后，普通读者仍应在一句话内听懂“我具体多能做什么”。世界内短名可有可无，不能代替能力解释。
- **直接能力不要在成长时变回分析能力。** 如果熟悉幻想本身是战斗、身体、移动、穿越、操控等直接效果，触发与异常掌握优先成长为更强控制、更多可作用对象、更危险场景下的稳定使用、与功法/兵器/身体的复合；不要把它重新解释成结构分析、受力判断、材料诊断、路线计算或逐步验证。只有 Spark / 作者方向本来就是学习、预知、推理、知识类幻想时，认知过程才可以是核心玩法。
- “为什么读者会馋”必须回答：如果读者明天醒来得到它，最想立刻拿来做什么？禁止用“战略自由度、成长潜力、规则位置”等抽象价值替代具体欲望。
- **默认强度故意偏夸张。** LLM 会自然自我平衡，所以第一稿宁可偏强一档，也不要偏保守。一个合格候选应让同层人第一次看到时产生“这也太占便宜了”的反应；如果只觉得更方便、更灵活、效率更高，通常还不够。
- **Novelty ≠ Power Fantasy 强度。** 候选必须形成清楚的 `Privilege Delta`：同层普通人通常只能做到什么、同层天才能做到什么，而这个 Power Asymmetry 让持有者现在就独占、提前或低代价拥有哪一种本来做不到、通常要更高一大档甚至数档才可能取得的特权。至少一个维度要明显超标，但不要求全属性越级。
- `Privilege Delta` 不能靠删除 Novelty Spark 的“单一异常”换来。如果 Spark 给的是条件、代价或限制，它必须继续真实约束能力；强度来自**在这个限制仍成立时，熟悉幻想依然提供巨大的特权**，不是把限制反写成额外外挂。
- **不要做对称平衡。** Permanent Boundary 用来限制适用范围、触发条件、覆盖对象或万能性，不是给每一点爽感配一笔等价代价。Core Power 必须保留一块明显的纯收益区间。
- 允许并鼓励有条件的越级威胁、越级生存、越级学习/获得或越级特权；边界用于防止无条件万能，不要把优势削到最后和普通同层修士差不多。候选应在现有 `World Power Normal → Power Asymmetry` / `为什么读者会馋` 等段落里自然说明哪一把 World ruler 最能让这种超标被别人看懂，例如境界、等级、潜力、熟练度、亲和度、能量、战绩或排名；不要另造总战力分，也不要新增“超标坐标/比较表/评分”等输出字段。
- 优先产生读者会直接想拥有的力量、身体状态、战斗方式或探索自由；不要把职业效率、维修、诊断、运输、审核、合同解释做成默认金手指。
- 这是男频成长长篇：正常修炼必须真实增强持有者本身；Power Asymmetry 的掌握同时继续质变，不是外挂替代修炼。Power Seed 只定义**开局 Core Asymmetry**，不包办全书所有力量；它要有可复合性，但不要提前枚举未来新能力。后续 Story Program 可以通过真实故事获得新的 Power Asymmetry，并让新旧优势产生化学反应。核心优势本身也应能与功法、兵器/法宝、身体/血脉、环境、传承等自然复合；不要让长期成长只剩数量、距离、持续时间越来越大。
- High-Tier Mutation 问高阶玩法怎样质变，不允许默认升级成因果、命运、天道、世界定义等抽象终极词。
- Legendary Power State 只写力量体验上限，不写未来身份、组织、统治地位、使命或故事结局；它和 Future Legend Image 都不得放松、绕过或遗忘前面已经写明的 Permanent Boundary。
- Future Legend Image 只是 AUDIT_ONLY，不是未来 Canon。

生成 3 个独立候选，不评分、不排名。候选必须匿名；不要给未来持有者取名。若提供了 Power Novelty Spark，Candidate 1/2/3 分别从对应 Spark 起步：只借“熟悉幻想 + 单一异常”做偏离，再按当前 World Power Normal 重新发明具体能力；不得原样抄 Spark，也不得让三个候选重新收敛成同一机制换皮。每个候选使用：

# POWER CANDIDATE N｜能力短名（可选；必须建立在白话理解之后）
## 一句话大白话
只用普通人的既有认知说明：别人做不到什么，我具体多能做什么。
## World Power Normal → Power Asymmetry
## Core Fantasy
## 为什么读者会馋
## Growth Compatibility
### 正常修炼轴
### 异常掌握轴
### High-Tier Mutation
### 永久边界
## Legendary Power State
## Power Audit Metadata（非 Canon）
### Future Legend Image

作者选择时会把一个候选编辑成单独的 `# POWER SEED`；不要替作者选择。
"""

HUMAN_PROMPT = """你是成熟中文男频成长长篇的 Human Seed 设计者。你只负责创造“这个人原本是谁”。你完全不知道未来 Power Seed、金手指、特殊体质或特殊身份，也看不到 named Story Opportunities。

只使用下方 LIFE CONTEXT 与 Human GBrain Craft。不要猜未来 Power，也不要为了一个不存在的外挂预留主题化童年。

第一性原则：**Human Seed 是一个人的权威快照，不是解释“他为什么必然成为他”的心理学论文。** 人的过去可以塑造他，也可以只是生活；不要先决定一句人格命题，再反向发明几段恰好逐条证明它的童年。

核心原则：
- **受世界塑形、对能力盲、对未来故事盲**。
- **经历是背景，不是人格证明**：先让具体生活事实成立，不逐条附上人格结论；同一种经历本来就可能塑造出不同的人。
- **多重动机并存**：保留 2—4 股会长期进入选择的私人牵引。胜负、钱、审美、身体欲望、好奇、享受、面子、亲近、自由、责任、野心、报复、归属都可以真实存在并互相竞争；不要求被一个单一核心执念统一。
- 长篇性来自这些牵引会在更大人生中继续改变选择，不等于自动长成事业、资产、决策权、专业权威或组织规模。
- **行为签名 = 稳定选择偏向 + 具体实现随现场变化**：读者逐渐知道他保护什么、拒绝什么、会为何承担代价；具体手段由当下信息、风险、能力边界和关系重新生成。不要统一成理性、克制、公平、公共利益最大化代理人。
- 重要关系必须**真实改变选择**：因为是这个具体的人，去留、风险、时间、暴露或机会牺牲会真实改变；换成另一个同等有用的人未必成立。
- 当前私人欲望是开书状态，**只初始化可变状态，不属于永久人物核心**。
- 人物钩子只用于候选辨识，证明这个人本身有戏；**不绑定前三章真实事件，不进入正式故事事实**。

生成 4 个独立候选，不评分、不排名。先保证每个人自身成立；不要为了多样性机械分配人格类型。

每个候选使用：

# HUMAN CANDIDATE N｜姓名／短标签
## 世界中的初始位置与生活事实
写具体出身、家庭、教育、工作/修炼接触，以及 3—5 件真实发生过、足以让这个人有过去的事情。不要逐条写 Adaptation；允许有些事实与后面人格弱相关或留下矛盾。
## 持续牵引与互相竞争的动机
写 2—4 股私人牵引，以及至少一个不能同时都满足的真实冲突。人物可以在某些欲望上明显过量，但不要把全部人生总结成唯一哲学。
## Behavior Signature
## 重要关系原点
## Initial State Seed
### 当前私人欲望
## Audition Metadata（非 Canon）
### 人物钩子

作者选择时会把一个候选编辑成单独的 `# HUMAN SEED`；不要替作者选择。
"""

EXPLICIT_PROTOTYPE_HUMAN_CONTRACT = """# Explicit Anonymous Human Prototype Projection

这是作者显式选择的匿名私人原型实验。只生成 **1 个** fictionalized Human Seed，不生成 4 个候选，也不要替作者再做人格变体搜索。

- 原型卡只提供 Appetite / Behavior / Relationship 的结构性选择偏向；现实身份、履历、地点、机构、关系身份和身体特征都不可推断或复原。
- LIFE_CONTEXT 决定幻想世界里的家庭、阶层、教育、工作/修炼接触和生活事实。不要让这些背景逐条证明原型卡；允许经历与动机弱相关、错位甚至形成新的矛盾。
- 保留多个 competing motives，不用一句人生哲学统一人物。情欲、身体吸引、虚荣、好胜、享乐、好奇、依恋等只要原型 craft 支持就可以真实存在，不净化、不道德化。
- 完全不知道 Power Seed。不要为了未知能力安排童年、职业、创伤或象征性人格。
- 重要关系必须在幻想世界重新创造具体的人；不得迁移现实关系对象。
- 输出标题直接使用 `# HUMAN SEED｜幻想姓名／短标签`。

其余 Human Seed schema 与默认 Human Prompt 相同。
"""


COLLISION_CONTRACT = """# 分离权威碰撞合同

**不要把碰撞消解成命中注定的适配。**

你第一次同时看到一个已冻结的世界和一个已冻结的人物。**世界与人物之间的不协调本身就是故事材料，不需要被解释掉。**

- World 是事实：不能为了让主角更合适而重写世界规则、已有故事机会、人物欲望或历史。
- Character 是事实：Power Core 与 Human Core 都不能重写；不要把人物经历解释成能力隐喻，也不要把人物欲望改成世界主题的答案。
- 你的工作是发现：这个具体的人拿着这种独立力量进入这个独立世界后，具体会想碰谁、想拿什么、被什么吸引、得罪谁、依赖谁、误判什么，以及哪些原本存在的世界事件会因此改道。
- 反制只能是碰撞之后学习产生的结果，不能反过来成为敌人存在的理由。
- 允许不协调、绕路、偶然关系和无法被金手指直接转换的世界大事；不要为了主题整齐把它们重新解释成“本来就适合主角”。
- **可以补少量过去，但不要用过去证明整个人。** 为了让当前关系、局部性格反应或某次选择更自然，可以补充少量非奠基性的过去经历、共同往事或旧事件；它们只能解释局部质感，不能重写 Human Core，也不能把人物收束成一条整齐的创伤因果链。
- **不要为了人格合理化而自动悲情化。** 不因为需要一点来处，就默认制造父母惨死、被抛弃、背叛、虐待、重大失去等创伤；普通、愉快、尴尬、失败、欲望、争执、错过同样可以形成有重量的过去。
- **过去存在，不等于现在就要告诉读者。** 这类为人物与关系补充的历史不得自动成为小说主线或大型阶段发动机，也不得一次性倾倒；Story Program 可以知道它存在，Outline 只在当前故事真正需要时逐步安排读者看见其中一小部分。
- 这是男频成长长篇：主角会通过正常修炼与已批准的力量异常真正越来越强，但 Story Program 不把每个阶段都写成能力升级说明书。
"""


class SplitCreativeApprovalError(HardGateError):
    def __init__(self, missing_artifacts: list[str]) -> None:
        self.missing_artifacts = missing_artifacts
        labels = {
            "world_vision": "World Vision",
            "character_card": "Character Authority",
            "proposal": "Story Program",
        }
        detail = "、".join(labels.get(item, item) for item in missing_artifacts)
        message = (
            f"当前{detail}尚未由作者明确批准。模型生成或模型选择不等于作者批准。"
            if len(missing_artifacts) == 1
            else f"以下创意产物尚未由作者明确批准：{detail}。模型生成或模型选择不等于作者批准。"
        )
        super().__init__(missing_artifacts, message)


def _approved(state: Mapping[str, Any] | None, artifact: str) -> bool:
    value = (state or {}).get(artifact, {})
    return isinstance(value, Mapping) and value.get("status") == "author_approved"


def _require_approved(state: Mapping[str, Any] | None, *artifacts: str) -> None:
    missing = [artifact for artifact in artifacts if not _approved(state, artifact)]
    if missing:
        raise SplitCreativeApprovalError(missing)


def _block(label: str, content: str) -> str:
    return f"# {label}\n\n{content.strip() or '（无）'}"


def adapt_split_planning_template(template: str, *, mode: str) -> str:
    """Migrate planning language to split authority without destroying custom templates."""

    text = template.strip()
    if mode == "idea":
        if not text or text == STORY_PROGRAM_TEMPLATE.strip():
            return STORY_PROGRAM_TEMPLATE.strip()
        intro = (
            "你是透明协作的 Story Program / 故事主线设计助手。只有 World Vision 与 Character Authority "
            "都由作者明确批准时，才生成长期故事主线。World 与 Character 是冻结事实；本阶段第一次设计它们如何碰撞。"
            "你可以决定早期兑现、稳定循环、中期里程碑、关系发展与长期阶段，但不能重写 Power Core、Human Core、"
            "T0 当前欲望或 World Canon 来制造命中注定的适配。GBrain 只是 OPTIONAL INSPIRATION，不得覆盖已批准权威。"
        )
        old_default_prefix = "你是透明协作的 Story Program / 故事主线设计助手。只有 World Vision 已经由作者明确批准时"
    elif mode == "outline":
        intro = (
            "你是透明协作的故事 Outline 助手。生成前必须确认 World Vision、Character Authority 和 Story Program "
            "都已由作者明确批准；模型生成、模型选择和作者编辑都不是批准。已批准产物高于产品默认模板，不能被静默改写。"
        )
        old_default_prefix = "你是透明协作的故事 Outline 助手。生成前必须确认 Fantasy Seed、World Vision 和 Story Program"
    else:
        return text

    # Replace only the retired TGN default contract. A genuinely custom template is
    # preserved verbatim and receives the new authority contract as a prefix.
    if text.startswith(old_default_prefix):
        _, sep, rest = text.partition("\n\n")
        text = intro + (sep + rest if sep else "")
    elif text:
        text = intro + "\n\n" + text
    else:
        text = intro

    replacements = (
        ("Fantasy Seed 与 World Vision", "Character Authority 与 World Vision"),
        ("Fantasy Seed、World Vision 和 Story Program", "World Vision、Character Authority 和 Story Program"),
        ("Fantasy Seed", "Character Authority"),
        ("Seed / World Vision / Story Program", "Character Authority / World Vision / Story Program"),
        ("Seed / World Vision", "Character Authority / World Vision"),
        ("Seed 中有辨识度的人格", "Human Core 中有辨识度的人格"),
        ("已批准 Seed", "已批准 Character Authority"),
    )
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def _compile_planning_with_character_authority(
    *,
    mode: str,
    template: str,
    book_content: str,
    creative_direction: str,
    world_vision: str,
    character_card: str,
    character_initial_state: str,
    proposal_context: str,
    selected_references: list[Mapping[str, Any]] | None,
    gbrain_inspiration: str,
) -> str:
    if len(selected_references or []) > 3:
        raise ValueError("最多只能选择 3 个 Reference Program")

    base = template.strip() or (STORY_PROGRAM_TEMPLATE if mode == "idea" else OUTLINE_TEMPLATE)
    parts = [adapt_split_planning_template(base, mode=mode), "", "# 页面当前输入"]
    parts.append(_block("作者粗方向", creative_direction))
    parts.append(_block("已批准 Character Authority", character_card))
    if character_initial_state.strip():
        parts.append(_block("Character Initial State｜T0 only", character_initial_state))
    parts.append(_block("已批准 World Vision", world_vision))

    if mode == "outline":
        parts.append(_block("作者已批准的 Story Program", proposal_context))
        parts.append(_block("当前 BOOK.md（只作为已批准创意的承载草稿）", book_content))

    parts.append(_block("手动选择的 Reference Programs", format_references(selected_references or [])))
    label = (
        "GBrain Inspiration Results（可选，只借鉴长期故事结构，不能覆盖已批准 Character / World）"
        if mode == "idea"
        else "GBrain Inspiration Results（可选，不能覆盖批准产物）"
    )
    parts.append(_block(label, gbrain_inspiration))
    return "\n\n".join(parts).strip() + "\n"


def generate_split_prompt(
    *,
    mode: str,
    template: str = "",
    book_content: str = "",
    creative_direction: str = "",
    world_vision: str = "",
    power_seed: str = "",
    human_seed: str = "",
    character_card: str = "",
    character_initial_state: str = "",
    creative_state: Mapping[str, Any] | None = None,
    proposal_context: str = "",
    current_long_block: str = "",
    current_outline: str = "",
    recent_summaries: str = "",
    selected_references: list[Mapping[str, Any]] | None = None,
    gbrain_inspiration: str = "",
    power_novelty: str | None = None,
    prototype_id: str = "",
    **_: Any,
) -> str:
    if mode == "world_vision":
        return "\n\n".join(
            [
                PROTAGONIST_BLIND_WORLD_TEMPLATE.strip(),
                _block("作者粗方向", creative_direction),
                _block("World GBrain Inspiration（可选）", gbrain_inspiration),
            ]
        ).strip() + "\n"

    if mode == "power_seed":
        _require_approved(creative_state, "world_vision")
        if not world_vision.strip():
            raise ValueError("生成 Power Seed 需要已批准的 World Vision")
        baseline = project_character_power_baseline(world_vision)
        novelty = build_power_novelty_bundle() if power_novelty is None else power_novelty.strip()
        parts = [POWER_PROMPT.strip(), baseline.strip()]
        if novelty:
            parts.append(_block("Power Novelty Spark（随机扰动；非 Canon）", novelty))
        parts.append(_block("Power GBrain Craft（可选）", gbrain_inspiration))
        return "\n\n".join(parts).strip() + "\n"

    if mode == "human_seed":
        _require_approved(creative_state, "world_vision")
        if not world_vision.strip():
            raise ValueError("生成 Human Seed 需要已批准的 World Vision")
        life = project_character_life_context(world_vision)
        human_prompt = HUMAN_PROMPT.strip()
        if prototype_id.strip():
            human_prompt = human_prompt.replace(
                "生成 4 个独立候选，不评分、不排名。先保证每个人自身成立；不要为了多样性机械分配人格类型。",
                "只生成 1 个匿名幻想人物，不评分、不排名；不要生成多个原型变体。",
            ).replace(
                "# HUMAN CANDIDATE N｜姓名／短标签",
                "# HUMAN SEED｜幻想姓名／短标签",
            ).replace(
                "作者选择时会把一个候选编辑成单独的 `# HUMAN SEED`；不要替作者选择。",
                "直接输出单个 `# HUMAN SEED`；不要生成候选列表。",
            )
        parts = [human_prompt]
        if prototype_id.strip():
            parts.append(EXPLICIT_PROTOTYPE_HUMAN_CONTRACT.strip())
        parts.extend([life.strip(), _block("Human GBrain Craft（可选）", gbrain_inspiration)])
        return "\n\n".join(parts).strip() + "\n"

    if mode == "idea":
        _require_approved(creative_state, "world_vision", "character_card")
        if not character_card.strip():
            raise ValueError("生成 Story Program 需要已批准的 Character Authority")
        planning = _compile_planning_with_character_authority(
            mode="idea",
            template=template,
            book_content=book_content,
            creative_direction=creative_direction,
            world_vision=world_vision,
            character_card=character_card,
            character_initial_state=character_initial_state,
            proposal_context=proposal_context,
            selected_references=selected_references,
            gbrain_inspiration=gbrain_inspiration,
        )
        return "\n\n".join([COLLISION_CONTRACT.strip(), planning.strip()]).strip() + "\n"

    if mode == "outline":
        _require_approved(creative_state, "world_vision", "character_card", "proposal")
        planning = _compile_planning_with_character_authority(
            mode="outline",
            template=template,
            book_content=book_content,
            creative_direction=creative_direction,
            world_vision=world_vision,
            character_card=character_card,
            character_initial_state=character_initial_state,
            proposal_context=proposal_context,
            selected_references=selected_references,
            gbrain_inspiration=gbrain_inspiration,
        )
        return planning

    raise ValueError(f"未知 Split Character Prompt 模式：{mode}")
