from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from .character_context import (
    project_character_life_context,
    project_character_power_baseline,
)
from .character_seeds import HUMAN_SEED_SCHEMA, POWER_SEED_SCHEMA
from .long_form_evolution import compose_effective_world, project_world_state_from_status
from .prompts import (
    HardGateError,
    OUTLINE_TEMPLATE,
    PUBLIC_WORLD_KNOWLEDGE_CLARITY,
    STORY_PROGRAM_TEMPLATE,
    format_references,
)
from .power_novelty import build_power_lexique_bundle, build_power_novelty_bundle
from .power_ruler import project_root_precise_power_ruler


SPLIT_PROMPT_MODES = frozenset(
    {
        "world_vision",
        "power_seed",
        "human_seed",
        "idea",
        "outline",
        "world_expansion",
        "human_development",
        "story_refresh",
    }
)

PROTAGONIST_BLIND_WORLD_TEMPLATE = f"""你是透明协作的 World Vision 创作助手。当前默认目标是成熟中文男频成长长篇；作者明确指定其他类型时，以作者要求为准。

这一版 World Vision **不知道主角是谁，也不知道未来金手指是什么**。只读取作者粗方向与当前明确提供的 World GBrain Inspiration；不要读取或猜测未来 Power Seed、Human Seed、Character、Story Program 或 Outline。

你的职责是创造一个即使最终换成完全不同主角也值得写一本书的世界。世界要有自己的普通生活、力量语法、正常值、社会现实、价值物、正在行动的人、奇观与未知。它可以非常适合男频成长，但不能先为尚不存在的主角准备钥匙孔。

{PUBLIC_WORLD_KNOWLEDGE_CLARITY}

重要边界：
- **World Reality ≠ Story Opportunity**：力量规则、普通生活、文化、阶层与正常分布属于世界现实；named 人物正在做的事、战争、秘境、遗迹、竞争、奇观与谜团属于世界自己的故事机会。两者都可以写，但不要暗示未来主角“应该”拥有什么钥匙来触发它。
- named 势力 / 部族 / 组织若会进入“世界正在发生的大事”，其**公开类别**（例如宗门、家族、军府、商盟、荒原部族、异族政体等）要同时在 `社会现实与身份` 或公共知识里用一句安全事实成立，供章节期 WORLD AUTHORITY 使用；这里只写“它是什么类型的存在、普通人如何识别它”，不把当前行动目的、隐藏关系、未解真相或未来 reveal 搬入安全层。
- 不生成主角欲望、主角童年、主角身份跃迁、核心能力、第一次能力兑现或终局使命。
- 不把后台主题写成 ontology；不要让整个世界只讨论一个抽象命题。
- **创新落在事实与玩法，不落在词汇表。** 基础力量规则先用普通读者已有词汇说清“力量从哪来、人具体能做什么、怎样变强、什么情况下会失败”；新造专名只给一个已经看懂、而且会反复出现的对象或层级贴短标签，不能让一个新词必须再靠两三个本书新词才能解释。作者要求“全新 / 不复用旧设定”时，差异优先放在力量因果、玩法、价值物、种族/地点/冲突组合，不要为了证明原创而回避境界、功法、兵器、异兽、血脉、火雷等本来就清楚的题材语言。若去掉专名后仍不能用 1—3 句普通话说明基础力量体系，先简化规则，不要继续命名。
- **Small Grammar, Large Variation / Reader Knowledge Compounding。** 如果主流力量已经能用 1—3 句普通话讲清，且现有一到少数互补操作轴已经有自己的辨识度，就保护它，不要为了“更统一”上提成泛化元能量、材性或总机制。后续丰富优先让读者已经学会的规则作用于新的招式、身体、兵器、异兽、环境、组合、强度与稀有例外，让旧知识越来越值钱；只有现有语法确实无法承载一种有长期价值的新幻想时，才新增新的底层机制。少规则/少系统不等于少内容，Variation 可以很大胆；世界谜团、历史、种族和社会也不要求全部服从同一个终极解释。
- **Fantasy Surface 要主动丰富，不要把 Small Grammar 误写成 Small World。** 基础因果已经清楚后，积极让同一 Grammar 长出真正不同的战斗姿态、标志性兵器/奇物、身体或物种差异、异兽/伴生物、会改变用法的天气/光线/地形、稀有高价值例外；不逐项填表，但也不要因为害怕增加设定，让几百章的新鲜感只剩“境界更高、同一招更大”。一个新表层至少应增加新的动作、欲望、比较或组合价值，而不是只增加一个需要解释的新名词。
- **主动寻找 0—1 条 Optional Secondary Fantasy Road。** 若本世界自然能长出一条即使不增强正面战力，读者仍可能想看某个人一路练到顶的强者道路——有可理解的强弱、真正顶层人物、可见作品/胜负、稀有高价值成果与社会价格——就把它作为世界既有事实分散写进当前结构的合适位置，不新增必填章节；它可以共享主力量的材料/器物/部分 Grammar，也可以是少量互补副轴，不为证明独立再造第二套宇宙能量。没有足够好的创意就不要硬造，也不预设未来主角一定会走。
- **前台力量先给直接可感知的作用，不用抽象关系替代作用本身。** 默认男频玄幻若核心体验本来是变强、攻击、防御、移动、穿越、身体变化、元素、兵器、异兽或其它直接效果，就先写这些效果；不要为了显得新，把它改写成“先理解/记录/定义/验证某种路径、结构、权限或关系，再间接获得效果”的 ontology。空间或移动规则当然可以创新，但读者应先知道“人具体怎么移动、穿过、交换位置”，而不是先学习一套道路/路径概念。只有作者明确选择认知、推理、概念或规则本身作为核心幻想时，抽象关系才可以成为力量本体。
- 内部因果可信不等于现代程序真实。玄幻/仙侠优先用力量、血脉、宗门、王朝、种族、地域、修炼资源、怪物、奇观等自身材质制造因果。
- 普通生活只写到足以让世界真实；**不要额外输出 Life Texture / Human Appetite 字段**。生活纹理以后只在 Writer 层按场景偶尔投影，不参与 Human Seed 生成。
- 力量体系必须给出可比较的正常值与稀缺度：普通人、普通修士、天才、地方强者、高层强者大致怎样不同；哪些现象常见、稀少、几乎未被可靠证实。不要为完整而堆十几层百科。
- **精确力量主尺是强制 World Root Authority。** 每个 production World 必须建立一把能给任何主要修炼者写出**唯一精确当前位置**的公开主尺，不能只有“低阶/中阶/高阶”或四五个粗境界。主尺只允许三种简单语法：`连续数字`（如 1—100 级）、`大境界+数字子级`（如每境 1—9 星/重/层）、`数字序列`（如序列 9—0）；具体名称由世界决定。严格在 `## 力量体系与正常值` 下输出 `### 精确力量主尺｜Frozen Grammar`，逐行填写：`主尺类型`、`主尺名称`、`精确位置格式`（必须含 `{{N}}`）、`数字精度规则`（必须给阿拉伯数字范围）、`当前可见范围`、`当前大档位`。这套 Grammar 一旦批准就是 World Root：普通 macro World Expansion 只能向上延展可见范围，不能改成另一套计数法；真正独立 instance 可以拥有自己的本地精确尺，但不得改写全局主尺。**精确尺是 Reader Ruler，不是战斗公式**：技能、装备、经验、环境、克制和 Power Asymmetry 仍可造成越级；不要因此建立总战力分、属性面板或逐项数值数据库。
- **力量尺必须能长期反复拿来比较，而不是只在设定表里出现一次。** 除精确主尺外，题材自然时再加入潜力、技法熟练度、装备、亲和度/适配度、排名等校准尺；它们必须会改变别人怎样评价、挑战、招揽、畏惧或给资源。对当前故事会频繁碰到的少数层级、价值物或身份档位，顺手给 1—2 个**肉眼可感、可复用的 benchmark**：例如正常这一档能击败/承受/进入/买到/影响什么，使后续能稳定写“正常 X 能做到 A，而这次竟然 Y”。不要逐级写战斗参数，不要求公斤/米等工程数值，不建立战力数据库，不要合成单一总战力分，也不要为了完整给所有尺度都配 benchmark。
- 当地理、安全边界或旅行会真实限制普通生活时，顺手写清**普通人怎样在聚落之间移动、谁能独行、商队/猎队/驿路/传送等为什么是进入外部世界的现实方式**。只给理解生活与 World Entry 所需的最小事实，不建立交通制度百科。
- 至少让一些世界人物、欲望、冲突与未来未知主角无关；世界不是测试金手指的主题乐园。

严格输出以下结构：

# PROTAGONIST-BLIND WORLD VISION

## 普通人的生活与上升
普通人怎样活；年轻人如何进入修炼/职业/身份上升；失败后通常怎样；若安全与地理会限制人生，再说明普通人通常怎样离开一个聚落、谁有能力跨越危险区域；不写主角。

## 力量体系与正常值
力量从哪里来、怎样获得与承载；当前故事世界真正需要的境界/能力坐标；普通、罕见、顶层差距以及可观察后果。必须包含下面这个固定子区块，并给出真实数字而不是占位说明：

### 精确力量主尺｜Frozen Grammar
主尺类型：连续数字 / 大境界+数字子级 / 数字序列（三选一，输出时只保留实际选择）
主尺名称：世界内长期公开使用的主尺名
精确位置格式：必须含 `{{N}}`，例如 `魂力{{N}}级` / `{{大境界}}{{N}}星` / `序列{{N}}`
数字精度规则：给出明确阿拉伯数字范围，例如 `1—100，每1级都是可记录位置` / `每个大境界1—9星` / `9—0，数字越小越高`
当前可见范围：只展开当前 World Horizon 真正需要的上下限，但必须写成精确数字端点
当前大档位：列出当前可见范围内读者会反复使用的少量大境界/社会称谓；连续数字型没有必要时可写 `NONE`

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
- **不要做对称平衡；Permanent Boundary 优先收束成一到少数根边界。** 它只负责限制真正会吞掉主要冲突的适用范围、触发条件、覆盖对象或万能性，不给每一点爽感配等价代价。只有 POWER BASELINE / Novelty Spark 已经存在、而且会真实改变“能不能做 / 对谁能做 / 何时能做”的限制才继续保留；不要把“不会额外治疗、不会复制天赋、不能替代正常修炼”这类本来就没有承诺的东西逐条写成限制，也不要自动再补疲劳、反噬、冷却、寿命、暴露等平账条款。Core Power 必须有明显纯收益区间；长期默认 **Boundary Stable, Privilege Expands**——成长主要扩大控制、对象、可靠性、组合、越级窗口与生活特权，而不是优势每扩大一步就同步长出一个新副作用。
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
- **多重动机并存，但职业化责任倾向必须大幅降权**：优先保留 2—4 股真正会让读者看见“这个人想要什么”的私人牵引，例如胜负、钱、审美、身体欲望、好奇、享受、面子、亲近、自由、野心、报复、归属。责任、精确、审计、边界、路线、损失归因、职业伦理等可以是局部习惯或现场判断，但除非作者明确选择职业/制度/经营题材，默认不得成为人物最强牵引、核心人格解释或长期反复证明的行为主题。
- 长篇性来自这些私人牵引会在更大人生中继续改变选择，不等于自动长成事业、资产、决策权、专业权威或组织规模。**主角永远不是协调员**：不要把聪明、成熟、负责写成替多方协调利益、分配责任、优化公共资源、安排所有人位置或替世界收拾残局。
- **行为签名 = 稳定选择偏向 + 具体实现随现场变化**：读者逐渐知道他想赢什么、想拿什么、舍不得什么、会为谁或为什么付代价；具体手段由当下信息、风险、能力边界和关系重新生成。职业经验只能改变局部观察与手段，不能垄断全书解题语法。不要统一成理性、克制、公平、公共利益最大化代理人。
- 重要关系必须**真实改变选择**：因为是这个具体的人，去留、风险、时间、暴露或机会牺牲会真实改变；换成另一个同等有用的人未必成立。
- 当前私人欲望是开书状态，**只初始化可变状态，不属于永久人物核心**。
- 人物钩子只用于候选辨识，证明这个人本身有戏；**不绑定前三章真实事件，不进入正式故事事实**。

生成 4 个独立候选，不评分、不排名。先保证每个人自身成立；不要为了多样性机械分配人格类型。

每个候选使用：

# HUMAN CANDIDATE N｜姓名／短标签
## 世界中的初始位置与生活事实
第一行固定写：`开局精确力量位置｜主尺：<World Root 主尺名称>｜精确位置：<符合 Frozen Grammar 的明确数字位置>`。即使尚未正式修炼，也使用 World 定义的 `0级/0段` 等精确零位，不写“普通人/未入门”这种无法长期比较的模糊位置。随后写具体出身、家庭、教育、工作/修炼接触，以及 3—5 件真实发生过、足以让这个人有过去的事情。不要逐条写 Adaptation；允许有些事实与后面人格弱相关或留下矛盾。
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


WORLD_EXPANSION_PROMPT = """你是 TGN 的周期性 World Expansion 设计者。你负责**向前扩世界**，不是回头重写开书 World，也不是替当前主角安排下一份礼包。

最重要的信息边界：**你看不到 Current Character、Power Stack、Human、关系、当前 Story Program 或未来 Outline。这个盲区是故意的。** 新世界必须先作为一个独立世界成立，惊喜来自它以后与人物碰撞，而不是你提前把世界做成主角的钥匙孔。

- 已批准 World Root 与此前 World Expansions 都是事实；不得改写旧力量规则、旧历史、旧公共常识或已存在地点。
- 只向 effective_from 之后增加过去尚未详细展开的世界层。`macro` 用于普通长篇进入更大大陆/圈层/文明/力量层；`instance` 用于多世界副本流的一次独立 Local World。
- Expansion 不是固定百章税；调用它意味着当前故事已经真正来到新 World Horizon。
- `macro` 优先做到“旧 Grammar 仍有效，但世界尺度、人物、价值物、危险、奇观或新幻想表面明显扩大”，不要为了扩世界就换一套宇宙底层物理。**Root 的精确力量主尺 Grammar 永远冻结**：必须在 `## 新力量 / 威胁 / 身份 / 价值尺度` 内输出 `### 精确力量主尺延展｜Macro`，写 `沿用主尺`、`主尺语法改动：NONE`、`新增可见范围`。如果本轮只扩地理/社会而不抬高力量上限，`新增可见范围：NONE`；绝不能借 Expansion 把 1—9 星改成初/中/后期，或另造第二套全局等级。
- `instance` 必须像一个原本就在运行的小世界：有普通生活、当地力量/危险、社会关系、价值物、人物欲望、正在发生的冲突与自己的未知；不是任务房、Boss 房或为某能力准备的谜题。独立副本可以有不同的本地力量语言，但也**强制拥有自己的精确本地主尺**：在 `## 新力量 / 威胁 / 身份 / 价值尺度` 内输出 `### 本地精确力量主尺｜Instance Grammar`，至少写三选一的 `主尺类型`、`主尺名称`、含 `{N}` 的 `精确位置格式`、明确数字范围的 `数字精度规则`、`当前可见范围`、`与全局主尺关系`；本地尺只帮助读者理解该世界，不回写全局主尺。
- 可以出现令人眼馋的兵器、传承、资源、伙伴、身份、地点和机会，但它们属于世界，不知道未来主角会不会得到；不得写“特别适合主角现有能力”“正好补足当前 Build”。
- 世界扩张应制造新的可追欲望与 Story Engine 可能性，而不是只把同一比赛/遗迹/争夺换地图放大。
- 只保留当前世界层真正需要的 reader-facing ruler；不要一次设计到全书终局。
- 未知仍是未知。不要因为你负责 World 就提前回答未来 mystery。

严格输出：

# WORLD EXPANSION

## 新增公共现实与普通生活
## 新力量 / 威胁 / 身份 / 价值尺度
按 Expansion Metadata 的 scope 严格包含一个精确尺子区块：
- `macro`：`### 精确力量主尺延展｜Macro`，逐行写 `沿用主尺` / `主尺语法改动：NONE` / `新增可见范围`。
- `instance`：`### 本地精确力量主尺｜Instance Grammar`，逐行写 `主尺类型` / `主尺名称` / `精确位置格式` / `数字精度规则` / `当前可见范围` / `与全局主尺关系`。
## 新地点、势力与公共识别
## 世界人物欲望与正在发生的事
## 真正值得想要或进入的东西
## 仍未知的边界
"""


HUMAN_DEVELOPMENT_PROMPT = """你是 TGN 的周期性 Human Development 审阅者。你只判断：这个人经过已经发生的长期故事以后，稳定选择偏向是否真的发生了**可进入未来 Authority 的发展**。

最重要的信息边界：**你看不到任何未来 World Expansion、未来奖励、未来 Story Program 或未来 Outline。** 不允许为了适配未来剧情提前改变人物。

- Frozen Human Core 是起源，不因为最近几章行为就失效。
- 当前目标、恋爱进度、愤怒、一次救人、连续几章负责/克制等，通常只是 Current State，不是 Stable Human Development。
- 只有已经发生的高代价选择、长期关系事实、反复且跨情境的选择，已经让继续只用旧 Stable Choice Bias 会明显写错这个人时，才新增 Development Delta。
- Development 是 forward-only：可以增加具体关系例外、调整某个 motive 的相对权重、形成新的稳定牵引或让旧偏向出现明确的新边界；不要把过去的自己删除成“原来其实不是这样”。
- 发展可以让人物更依恋、更野心、更享乐、更狠、更怕失去、更愿意停留，也可以没有变化；不要默认成长等于成熟、负责、善良或公共利益。
- 没有足够证据就输出 NONE。宁可不改，不做人格漂移。
- 不发明正文没有发生过的心理领悟、旧对话或隐藏动机。

严格输出：

# HUMAN DEVELOPMENT DELTA

若没有稳定变化，只写 `NONE`。
若有，只写少量已经被历史证明的 stable delta，并明确哪些 Origin 仍然成立、哪一种未来选择判断需要从此更新，以及证据边界是什么。
"""


STORY_REFRESH_PROMPT = """你是 TGN 的 Periodic Re-Collision / Story Refresh。当前不是开书第一次 Collision，而是一个已经活过很多章的人第一次面对**独立生成并已冻结的新 World Horizon**。

Authority：
- Effective World = World Root + 已生效 Forward World Expansions；你只能使用，不能重写。
- Current Character = Frozen Origins + 已发生 Power/Asset/Relationship/Identity/Knowledge + 已批准 Human Development；你只能使用，不能把人物重新优化成最适合新世界的人。
- Existing Canon 已发生不可回滚；旧 Story Program 只保留仍未兑现且仍成立的长期因果，不强迫未来继续照旧计划演。

核心方法：**Independent World × Current Character → Fresh Collision。**

- 不要把新世界重新解释成“原来一直为主角准备”。真正好的结果允许不协调、绕路、错失和意外偏好。
- Current Power Portfolio 是两层 Power 的当前态：开局 Core 继续存在，已获得 Power / 武器 / 身体变化继续有用。可以通过新世界真实事件再获得新的 Power Asymmetry，并与旧优势复合，但不能反向给 World 新造一件刚好补 Build 的东西。
- Human 决定选择，不用“长期成长最优解”覆盖人物。新世界出现多个高价值机会时，允许人物因钱、赢、好奇、爱情、兄弟、虚荣、报复、享受、自由等走不同路线。
- 新阶段应真正换 Story Engine / Reading Question；不要只把旧阶段的“接任务→危险地点→胜利→奖励”换皮。
- 旧获得要继续改变新阶段；新获得以后也必须留下，而不是阶段结束 reset。
- 世界扩张后重新校准 Reader Ruler、Social Repricing 与新 World Entry，但不把说明写成百科。
- 普通长篇规划一个自然大型阶段；多世界 instance 则规划当前副本 + 回归后真正留下的 consequence。都不要逐章。
- 只刷新未来，不重写已完成章节，不发明旧历史。
- **本次 Refresh 仍然只具体规划当前新 World Horizon。** 如果这一轮世界层会在未来被真正活透，最后 1—2 个自然阶段就开始形成下一次交接条件；到边界后停止替未知未来世界规划具体内容，再次等待独立 World Expansion。不要因为已经进入第二/第三轮 Refresh，就把后面所有世界重新一次性写死。

严格输出与 production Story Program 兼容的单一结构：

# STORY PROGRAM

## 当前 Re-Collision
## 当前 Power / Human / World 的长期张力
## 本阶段核心情节发动机与变化后的主要 Reading Question
## 全书成长与核心幻想兑现脊柱（只写从当前点向前仍成立的部分）
## 不可替代的人与关系
## 未来大型阶段
只规划当前已批准 World Horizon 内真正需要的阶段。每个阶段写：具体世界问题、主要推动者、主角关键选择、最主要阅读满足、真实 Power/Asset/Relationship/Identity/Knowledge/World Delta、旧积累怎样继续生效、下一阶段为何自然发生。
## World Horizon Handoff
若本轮 World Horizon 会在这些阶段后自然结束，写清：触发条件、`macro`/`instance` scope、为什么当前层已需要扩、必须 carry forward 的已发生事实，以及固定 orchestration：`protagonist-blind World Expansion → deterministic Current Character → Story Refresh`。若 Effective World / Canon 已经存在能让读者具体感到“当前层之外还有东西”的外缘信号，安排它在 Handoff 前最后 1—2 章露面一次；只允许使用已批准旧事实/旧未知，不得为钩子预写下一世界宝物、能力、势力或针对当前 Build 的答案。若尚未到边界，写 `NOT YET` + 仍缺的真实边界事件。
## 仍值得追的旧承诺与新欲望
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


def _book_status(book_content: str) -> str:
    heading = "# 当前状态、未兑现承诺与作者备注"
    start = book_content.find(heading)
    return book_content[start + len(heading) :].strip() if start >= 0 else ""


def _frozen_human_core(character_card: str) -> str:
    start_heading = "## HUMAN CORE｜Frozen Authority"
    end_heading = "## Composition Boundary"
    start = character_card.find(start_heading)
    if start < 0:
        return ""
    start += len(start_heading)
    end = character_card.find(end_heading, start)
    if end < 0:
        end = len(character_card)
    return character_card[start:end].strip()


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
    world_expansions: str,
    character_card: str,
    character_initial_state: str,
    current_character: str,
    proposal_context: str,
    selected_references: list[Mapping[str, Any]] | None,
    gbrain_inspiration: str,
) -> str:
    if len(selected_references or []) > 3:
        raise ValueError("最多只能选择 3 个 Reference Program")

    base = template.strip() or (STORY_PROGRAM_TEMPLATE if mode == "idea" else OUTLINE_TEMPLATE)
    parts = [adapt_split_planning_template(base, mode=mode), "", "# 页面当前输入"]
    parts.append(_block("作者粗方向", creative_direction))
    planning_character = (
        current_character.strip()
        if mode == "outline" and current_character.strip()
        else character_card
    )
    parts.append(
        _block(
            "CURRENT CHARACTER｜Forward Authority"
            if mode == "outline" and current_character.strip()
            else "已批准 Character Authority",
            planning_character,
        )
    )
    if character_initial_state.strip() and not (mode == "outline" and current_character.strip()):
        parts.append(_block("Character Initial State｜T0 only", character_initial_state))
    planning_world = world_vision
    if mode == "outline" and world_expansions.strip():
        match = re.search(r"Compiled Through Chapter:\s*(\d+)", current_character)
        boundary = int(match.group(1)) + 1 if match else 1
        planning_world = compose_effective_world(world_vision, world_expansions, boundary)
    parts.append(
        _block(
            "EFFECTIVE WORLD｜Root + Approved Forward Expansions"
            if mode == "outline" and world_expansions.strip()
            else "已批准 World Vision",
            planning_world,
        )
    )

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
    world_expansions: str = "",
    power_seed: str = "",
    human_seed: str = "",
    character_card: str = "",
    character_initial_state: str = "",
    human_development: str = "",
    current_character: str = "",
    creative_state: Mapping[str, Any] | None = None,
    proposal_context: str = "",
    current_long_block: str = "",
    current_outline: str = "",
    recent_summaries: str = "",
    selected_references: list[Mapping[str, Any]] | None = None,
    gbrain_inspiration: str = "",
    power_novelty: str | None = None,
    power_lexique: str | None = None,
    prototype_id: str = "",
    evolution_scope: str = "macro",
    effective_from_chapter: int = 0,
    effective_until_chapter: int = 0,
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
        lexique = build_power_lexique_bundle() if power_lexique is None else power_lexique.strip()
        parts = [POWER_PROMPT.strip(), baseline.strip()]
        if novelty:
            parts.append(_block("Power Novelty Spark（随机扰动；非 Canon）", novelty))
        if lexique:
            parts.append(_block("Power Lexique Primitive Spark（可选；非 Canon；可完全忽略）", lexique))
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
        parts.extend([
            life.strip(),
            _block("FROZEN PRECISE POWER RULER GRAMMAR｜只用于人物 T0 精确位置", project_root_precise_power_ruler(world_vision)),
            _block("Human GBrain Craft（可选）", gbrain_inspiration),
        ])
        return "\n\n".join(parts).strip() + "\n"

    if mode == "world_expansion":
        _require_approved(creative_state, "world_vision")
        if evolution_scope not in {"macro", "instance"}:
            raise ValueError("World Expansion scope 必须是 macro 或 instance")
        if effective_from_chapter < 1:
            raise ValueError("World Expansion 需要正整数 effective_from_chapter")
        if effective_until_chapter and effective_until_chapter < effective_from_chapter:
            raise ValueError("effective_until_chapter 不能早于 effective_from_chapter")
        world_state = project_world_state_from_status(_book_status(book_content))
        return "\n\n".join(
            [
                WORLD_EXPANSION_PROMPT.strip(),
                _block("作者粗方向", creative_direction),
                _block("WORLD ROOT｜Frozen Opening Authority", world_vision),
                _block("FROZEN PRECISE POWER RULER GRAMMAR｜不得改写", project_root_precise_power_ruler(world_vision)),
                _block("PREVIOUS APPROVED WORLD EXPANSIONS｜World-only", world_expansions),
                _block("CURRENT WORLD STATE｜Only explicit Canon World State", world_state),
                _block(
                    "Expansion Metadata",
                    "\n".join(
                        (
                            f"scope: {evolution_scope}",
                            f"effective_from_chapter: {effective_from_chapter}",
                            f"effective_until_chapter: {effective_until_chapter}",
                        )
                    ),
                ),
                _block("World GBrain Inspiration（可选；不能借主角反向塑形）", gbrain_inspiration),
            ]
        ).strip() + "\n"

    if mode == "human_development":
        _require_approved(creative_state, "character_card")
        human_core = _frozen_human_core(character_card)
        if not human_core:
            raise ValueError("Human Development 需要 Frozen Human Core")
        return "\n\n".join(
            [
                HUMAN_DEVELOPMENT_PROMPT.strip(),
                _block("FROZEN HUMAN CORE｜Origin Authority", human_core),
                _block("PREVIOUS APPROVED HUMAN DEVELOPMENT", human_development),
                _block("ALREADY-HAPPENED CANON MEMORY", _book_status(book_content)),
            ]
        ).strip() + "\n"

    if mode == "story_refresh":
        _require_approved(creative_state, "world_vision", "character_card", "proposal")
        if not current_character.strip():
            raise ValueError("Story Refresh 前必须先确定性刷新 CURRENT_CHARACTER.md")
        boundary = effective_from_chapter
        if boundary < 1:
            match = re.search(r"Compiled Through Chapter:\s*(\d+)", current_character)
            boundary = int(match.group(1)) + 1 if match else 1
        effective_world = compose_effective_world(world_vision, world_expansions, boundary)
        if len(selected_references or []) > 3:
            raise ValueError("Story Refresh 最多只能选择 3 个 Reference Program")
        return "\n\n".join(
            [
                STORY_REFRESH_PROMPT.strip(),
                _block("作者粗方向", creative_direction),
                _block("EFFECTIVE WORLD｜Independent Authority", effective_world),
                _block("CURRENT CHARACTER｜Deterministic Forward Snapshot", current_character),
                _block("ALREADY-HAPPENED CANON MEMORY", _book_status(book_content)),
                _block("PREVIOUS STORY PROGRAM｜Only unresolved future obligations survive", proposal_context),
                _block("Reference Programs（可选）", format_references(selected_references or [])),
                _block("GBrain Inspiration（可选；不能覆盖 World / Current Character）", gbrain_inspiration),
            ]
        ).strip() + "\n"

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
            world_expansions=world_expansions,
            character_card=character_card,
            character_initial_state=character_initial_state,
            current_character=current_character,
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
            world_expansions=world_expansions,
            character_card=character_card,
            character_initial_state=character_initial_state,
            current_character=current_character,
            proposal_context=proposal_context,
            selected_references=selected_references,
            gbrain_inspiration=gbrain_inspiration,
        )
        return planning

    raise ValueError(f"未知 Split Character Prompt 模式：{mode}")
