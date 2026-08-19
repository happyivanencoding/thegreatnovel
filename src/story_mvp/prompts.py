from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any


PROMPT_MODES = {
    "idea": "男频爽文创意生成",
    "outline": "新书/总纲规划",
    "chapter_prep": "当前章执行小纲",
    "chapter": "当前章节写作",
    "review": "十章复盘与下一批十章",
    "context_curator": "Hybrid Context Curator",
    "primary_writer": "Hybrid Primary Writer",
    "specialist_opening": "Opening & Scene Entry Specialist",
    "specialist_dialogue": "Dialogue & Character Voice Specialist",
    "specialist_action": "Action & Spatial Logic Specialist",
    "specialist_emotion": "Emotion & Aftermath Specialist",
    "chapter_integrator": "Hybrid Revision Integrator",
    "state_delta": "State Delta 提案与 Canon Index 更新",
}

REQUIRED_OUTLINE_FIELDS = (
    "触发事件",
    "推动事件的人",
    "主角行动",
    "对手或世界反应",
    "直接结果",
    "状态变化",
    "叙事功能",
    "结尾推动力",
)

DEFAULT_PRODUCT_DIRECTION = """当前产品默认目标是成熟中文男频成长爽文。优先寻找具有主角主动性、非对称优势、可重复利用、复利增长、早期兑现和持续行动空间扩大的具体故事。创新应优先体现在玩法和成长路径上，而不是单纯通过悲剧代价、伦理折磨或反爽机制制造“高级感”。这是创作方向，不是机械模板；如果作者明确要求其他类型，以作者要求为准。"""

DEFAULT_COMPOSABLE_GROWTH_DIRECTION = """当前产品只提供主角成长型虚构世界男频长篇的启动方向。不要预设所有书都沿同一条力量链成长；优先寻找本书自己的非对称位置、成长对象、转换网络、可重复循环、阶段变异和核心不变量。成长可以来自力量、知识、职业、规则、身份、造物、组织、关系、世界通行能力或它们的组合；作者选定具体创意后，以本书成长基因为准。"""

CLASSIC_PATTERN_DIRECTION = """经典成长模式是一等公民：可组合只表示不强迫所有作品相同，不表示主动回避成熟主干。资源→成长→战斗→身份→更高级资源→更大世界，以及职业→技能→任务→身份、探索→机缘→成长→新区域、内容副本→战斗→战利品→构筑等，都可以成为本书主干。如果作者输入、GBrain证据或当前创意表明某条经典链最适合本书，应当保留它，创新放在新优势、世界机制、转换方式、关系反馈或阶段变异上。"""


WRITER_AUDIT_RULE = """Writer Audit 只报告实际存在的事项：
- 本次正式正文字符数；
- 实际发现的 CANON PROSE / BOOK CONTRACT / CANON INDEX / PLAN 冲突；
- 为承接前文而补入的必要桥接；
- 对当前章事件合同作出的实质调整及原因。
没有冲突、必要桥接或实质调整时，明确写：无需要报告的冲突或实质调整。
不要把正常的场景安排、遣词选择、句段变化或普通润色包装成问题。不要为了满足数量而制造发现。不要输出 chain-of-thought。"""


PROSE_REALIZATION_CONTRACT = f"""本合同只负责“how to say”，不重规划“what happens”。本次为单 Writer 直接写作：根据已批准的当前章事件合同直接写出可提交的正式正文，不模拟多 Writer 串行稿件，不输出内部推理。权威规则（按维度划分）与冲突处理以运行期上下文中的 AUTHORITY 最小权威规则为准，只注入一次，不在这里复述。

## Output boundary

最终返回必须使用三个一级标题：`# Writer Audit`、`# 正式正文`、`# 章节事实摘要`。`# 章节事实摘要` 只放 100—200 字事实摘要，不写入章节正文文件。

{WRITER_AUDIT_RULE}

`chapter-NNNN.md` 只保存正式小说正文；不把 audit、摘要或内部推理写进正文，不自动修改 BOOK、事实、资源、能力、线索、结果、状态变化或结尾。

## Continuity

承接 CANON PROSE 前文正文的最后状态（地点、时间、在场人物、身体状态、情绪、手中物品、最后动作、未完成即时目标）；章节边界不是场景边界，对话、追逐、战斗、调查、试炼和谈判可以跨章。连续性应通过自然动作和场景表现：不要为了证明物品归属、数量或交易完成而重复盘点已经清楚的事实。

## Prose profile 地位

BOOK 的 `## 7. 叙事结构`、`## 8. 文风与可操作参数`、`## 9. 对话特点`、`## 10. 节奏结构` 共同构成当前书的 prose profile。它们是作者可编辑的软控制：决定叙述距离、句段变化、说明进入方式、角色声音和场景压力，不是禁词表、固定句长或硬性风格评分。GBrain Inspiration Results 与 Reference Programs 只是 OPTIONAL INSPIRATION 可选参考，不能覆盖 BOOK CONTRACT、CANON PROSE、CANON INDEX、PLAN 或 PROSE PROFILE。"""

SINGLE_WRITER_RUNTIME_NOTE = "运行期声明：本次为单 Writer 直接写作；任何多 Writer 协议已被本运行合同取代。"

#: BOOK.md「当前状态、未兑现承诺与作者备注」一级标题受保护锚点；
#: chapter_prep 与 chapter_context（CANON_INDEX_STATUS_HEADING）都引用本常量。
CURRENT_STATE_HEADING = "# 当前状态、未兑现承诺与作者备注"


DEFAULT_PROMPT_TEMPLATES = {
    "idea": f"""你是透明协作的男频成长爽文创意助手。根据作者的粗方向、页面上完整可见的 GBrain Inspiration Results 和手动选择的 Reference Programs，生成 3—5 个明显不同的商业男频成长爽文核心创意。不评分、不排名、不替作者选择，不调用任何外部服务。

{DEFAULT_PRODUCT_DIRECTION}

{DEFAULT_COMPOSABLE_GROWTH_DIRECTION}

{CLASSIC_PATTERN_DIRECTION}

默认创作偏置：主角要有明显主动性；金手指要形成可重复、可放大的非对称优势；代价服务于策略，不负责抵消爽感；1—3 章出现核心异常或优势，3—10 章完成第一次明确利用，10—30 章形成稳定循环或公开证明；成长要打开新的行动空间，每次扩大都带来新的玩法。

核心优势或成长对象必须有纵向成长路线：早期能做什么，随后如何恢复、放大、反推或重新组合，进一步如何打开本书自己的新问题、新关系、新规则或新世界。每个候选说明本书最重要的读者满足和它如何变化，不要求套用直接/间接 payoff 分类。

每个候选还必须输出：
## 成长组合
说明本候选把哪些变量和循环组合在一起。
## 初始转换网络
用箭头说明主角最初怎样把一种优势转换成新的行动能力，允许分叉、反馈和条件转换。
## 长篇变异潜力
说明 100 章内成长对象、行动方式、主要循环或世界理解怎样发生至少几次本质变化，而不是只让敌人变强。
## 与其它候选的真正差异
说明转换网络或循环关系的不同，不能只换题材名、金手指名字、敌人或地图。候选可以共享同一个经典成长骨架，只要非对称优势、资源生成方式、验证玩法、世界结构、核心关系、长期变异或 reader promise 真正不同；不要为了差异强迫某个候选变成纯谜团、纯规则、纯建设或纯关系小说。

不要为了显得高级，默认使用失忆、寿命、感情、伦理诅咒或越成功越痛苦等抵消型代价。除非作者明确要求，否则优先寻找可以复利、早期兑现并自然扩大到 100 章的玩法。

每个候选必须完整使用以下结构：
## 候选N：书名/概念名
一句话创意：主角是谁 + 得到什么非对称优势 + 最直接要解决什么问题。
主角核心优势：它具体能做什么。
为什么这是优势：别人为什么无法轻易复制。
核心爽点循环：主角做什么 → 得到什么 → 怎样进一步放大优势 → 引来什么更高层机会或敌人。
开局1—3章：具体发生什么。
前10章：第一个完整小闭环是什么。
第一个公开证明：主角什么时候让别人第一次真正意识到他的价值、实力或异常。
100章扩张方向：小能力怎样扩大为资源、身份、组织、地域或世界行动能力。
关键关系：至少一个会随主角成长持续改变的人。
最大的重复风险：这个玩法写久以后最容易重复什么。""",
    "outline": f"""你是透明协作的 GBrain 故事规划助手。只根据下方作者输入、作者编辑过的 GBrain Inspiration Results 与参考程序，生成一份完整、具体、可编辑的故事规划提案，不调用任何外部服务。

{DEFAULT_PRODUCT_DIRECTION}

{DEFAULT_COMPOSABLE_GROWTH_DIRECTION}

{CLASSIC_PATTERN_DIRECTION}

作者已选择 / 编辑的规划种子规则：如果下方“作者已选择 / 编辑的规划种子”区域非空，它代表作者已经从 Idea Proposal 中选择并编辑过的创意。它的核心设定、成长优势和 Reader Promise 权威高于默认产品方向和 GBrain，Outline 必须展开这个创意，不得重新换一本书。可以补充世界、人物、成长机制、长期阶段和具体事件，但不得静默修改作者选择的核心创意。

生成 Outline 前，请把 Idea 生成的候选放入 Proposal 编辑区，只保留或编辑作者准备继续发展的候选；不要自动评分、排名或替作者选择。

先建立整本书的总体设计画像，再据此规划 100 章和第一批十章。最终返回内容必须按以下四个一级 Markdown 标题逐字输出，不能增加其它一级标题：

# 小说总体设计画像
# 未来100章大型剧情块
# 未来十章逐章小纲
# 当前状态、未兑现承诺与作者备注

在“小说总体设计画像”下，先完整输出以下开放的成长基因图，再输出 1—12 个总体画像区块。不生成 JSON/YAML，不评分，不把任何一项变成 Hard Gate：

## 0. 本书成长基因图
### 作者明确保留
如果作者明确输入了成长链、核心玩法、必须保留的元素或不希望被改掉的方向，原样或忠实压缩记录在这里；如果作者没有明确指定，写“作者暂未锁定具体成长主干”。这是普通作者内容，不是 Hard Gate。
用普通 Markdown 描述本书的核心组合、关键变量、转换网络、循环族、阶段变异、核心不变量和退化风险。变量名称、数量和循环名称由本书决定，不要复制产品示例。如果作者或证据明确支持资源→成长→战斗→身份等经典链，应把它作为本书主干，不要为了显得创新而回避。
核心组合：说明哪些机制被组合在一起。
关键变量：只列本书真正需要的成长对象。
转换网络：用箭头说明一对多、多对一、反馈、条件转换、延迟兑现、负反馈或中期失效。
循环族：生成本书真正需要的一个主循环和零到多个辅助循环，说明各自的阅读满足、阶段、互相供能和何时退居次要；不要为了多样性强行生成 2—4 个同等重要的循环。
阶段变异：说明成长对象、行动方式、冲突、验证场景、关系、时间尺度、世界认识或读者好奇心怎样换挡。
核心不变量：只写 1—3 条长期必须持续给读者的体验。
退化风险：只写本书最可能的 1—3 种退化。

## 1. 核心类型与读者承诺
说明本质类型、前中远期读者为什么继续追，以及类型升级由什么具体故事变化产生。
## 2. 世界观结构
只写真正决定剧情的核心坐标轴，并说明它们怎样咬合、每次成长打开什么行动空间。如果本书需要且对当前故事重要，再具体说明空间/层级、主要权力关系、力量或成长道路、成长阶梯和当前时代变化；不要求每本书都有多个势力、流派、等级、学院、猎团或遗迹。
## 3. 世界如何持续制造剧情压力
从境界压制、功法与传承、资源竞争、强敌、同辈竞争、宗门阶层、秘境、遗迹、妖兽、地域危险、身份暴露、大势力、市场/渠道和上层世界规则中选择合适来源；不要让市场、认证或制度天然占据主要位置。
## 4. 主角模型、人物弧与核心矛盾
优先写主角最强欲望、最喜欢采取的行动、如何利用优势、如何越来越主动、从弱者走向什么位置，以及哪类胜利最能让读者满足。只有自然存在时才写核心人物矛盾，不要为了显得深刻强制生成伦理困境。
## 5. 配角与关系系统
写长期角色、各自利益、关系变化与反转、情绪价值，以及关系系统最容易失败的地方。关系可以承担崇拜、友情、师徒、竞争、嫉妒、恐惧、爱慕、忠诚、背叛和旧日轻视后的重新评价；不要把所有角色都写成制度利益方，也不要让所有人只做同一种反应。
## 6. 核心情节发动机
根据成长基因图写本书真正需要的一个主循环和零到多个辅助循环，说明每个循环的阅读满足、适用阶段、互相供能方式、何时退居次要，以及第2/3/4次运行如何改变变量、风险、身份、规模或收益形式。成熟爽文可以长期运行一个强主循环，不要为了多样性强行改掉它。
## 7. 叙事结构
写主要叙述距离、主要视角、何时贴近或拉远、视角切换条件与切换功能，以及前后期场景叙事和总结叙事的变化；说明如何用他人反应展示主角地位变化。
### 第一章开篇策略
第一章开篇策略完全由作者和本书 BOOK 决定，可以是人物直接入场、强冲突入场、讲述者宏观开场、历史/传说开场、神秘事件、对手视角、倒叙、日常反差或其它方式。不要默认所有书相同；只有当 BOOK 选择讲述者宏观开场时，才用故事口吻建立当前需要的世界信息，再自然收束到主角。
## 8. 文风与可操作参数
写目标单章长度、段落、信息/描写/对话/内心/战斗密度、系统信息频率和每章推进台阶，并形成可执行的 prose profile：说明高低压力场景的句段变化、说明如何进入、内心与感官如何落到行动、最可能出现的机械表达及其规避方式；再说明名词具体度、动词的方向/接触/结果、修饰词使用倾向、不确定词使用边界、口语/庄重/专业语体边界；这些是创作目标，不是代码限制。
## 9. 对话特点
写核心角色在词汇、句长、礼貌、攻击性、避答和沉默方式上的差异，以及各自的节奏、信息量、身份、隐藏目的、直接或试探方式；说明对话怎样改变现场和博弈。
## 10. 节奏结构
分别说明 opening、ordinary、dialogue、action、payoff、aftermath、emotion、ending 等场景功能如何改变节奏，再说明单章、约10章、大型剧情块和100章推进什么，如何交替小爽点、中型兑现、阶段大兑现、afterward与新压力，并指出节奏重复风险。
## 11. 主题、价值观与长期问题
写故事赞赏什么、警惕什么、主角相信什么、世界迫使他面对什么反例，以及主题如何从实际机制中浮现。主题是长期运行后自然出现的东西，不得要求主角承受伦理惩罚；可以是普通人靠选择和积累逆袭、知识打破资源壁垒、实力带来选择权或弱小时别人定规则、强大后主角获得定义规则的资格。
## 12. 当前设计最强点与最弱点
写设计统一性、当前最弱处和写作时真正需要防止的 2—5 个问题，不生成风险清单。

画像必须是作者可修改的创作模型，而不是百科全书或机械模板。

未来 100 章写 4—8 个自然剧情块，不要套固定 5 × 20。每个剧情块必须使用以下顺序：

所有大型剧情块必须共同覆盖第1章到第100章：第一块从第1章开始，最后一块结束于第100章，相邻章节范围必须清楚衔接。必须完整输出所有剧情块，不能只展示第一个块，不能用“后续类似”“后面略”省略。越靠后的块可以稍粗，但仍必须明确核心人物、主要事件、主角行动、核心转折、高潮、得到什么、失去或承担什么，以及如何进入下一块。

## 第X—Y章：具体块名
具体发生：先写具体人物、具体地点、具体事件、主角行动、对手或世界反应、转折、高潮和新问题；不要只写“建立资源循环”或“敌人升级”。
阶段结果：说明主角获得或失去什么资源、能力、身份、关系或行动空间，以及下一块为什么必然发生。
叙事功能：说明这组具体事件完成了什么兑现、换挡或压力升级。
推向下一块：写出下一块从哪个具体问题开始。

每个大型剧情块还必须说明：当前使用成长基因图中的哪条循环、通过哪条转换路径产生变化、哪个旧变量被重新解释或失效、哪个新变量进入故事、下一块为什么必须换用另一条路径。不要强制每块使用不同 payoff 标签或固定阶段顺序。

未来十章必须是一个连续的小故事，而不是十个独立主题。每章使用：

## 第N章：具体标题
具体剧情：用 2—4 句写具体人物、事件和主角行动。
结果 / 状态变化：写直接结果和状态变化。
叙事功能：写本章在局部故事中的作用。
结尾推动：写下一章为什么发生。

每章都必须有具体人物、具体事件、主角具体行动、直接结果、状态变化、叙事功能和结尾推动。禁止用“主角继续调查”“危机升级”“爆发点”“关系深化”“敌人变强”代替剧情。

必须连续逐章列出完整的十章，不能合并章节，不能省略后几章。

第N章的结尾推动必须成为第N+1章具体剧情的直接因果起点；如果换地点、时间或主要人物，第N+1章必须写出桥接动作。章节边界不是场景边界，不要为每章强行重置到新场景。

最后在当前状态一级标题下写出故事开始前的初始状态、已经建立的远期承诺、当前未解决问题和作者备注。

不要把抽象主题当作事件链，不要自动替作者批准或保存任何内容。""",
    "chapter_prep": """你是透明协作的当前章执行小纲助手。只根据作者当前页面提供的 BOOK 执行相关画像、当前大型剧情块、当前章对应的十章计划条目、前一章或前两章正式正文、最近章节摘要和当前状态，生成当前章真正用于写正文的八字段合同，不调用任何外部服务。

当前章执行小纲只负责把已经批准的中期计划落实为本章可执行合同。正式正文是已发生事实的最高来源；如果正式正文与旧计划冲突，优先服从正式正文，并在八字段中做最小必要调整。不得重新规划整本书，不得重新选择题材或创意，不得把十章计划改写成另一条故事。

必须只输出以下八个字段，每项都必须填写具体内容：
触发事件：
推动事件的人：
主角行动：
对手或世界反应：
直接结果：
状态变化：
叙事功能：
结尾推动力：

不要输出正文，不要输出章节概述，不要增加其它字段、一级标题、解释、审计或内部推理。不要改变十章计划中的主要事件、预定结果、状态变化、叙事功能和下一章推动；只有正式正文已使旧计划局部不可执行时，才做最小必要调整。八项全部必填。""",
    "chapter": """你是透明协作的 GBrain 章节写作助手。本次为单 Writer 直接写作：根据已批准的当前章事件合同，直接写出可提交的正式正文，不模拟多 Writer 串行稿件。只依据页面上提供的章节运行期上下文（AUTHORITY / BOOK CONTRACT / CHAPTER MISSION / CANON PROSE / CANON INDEX / PLAN / PROSE PROFILE / OPTIONAL INSPIRATION）写作，不调用任何外部服务。

## 连续性优先

本章不是独立短篇。如果 CANON PROSE 区块提供了上一章或前两章正文，先承接其最后地点、时间、在场人物、身体状态、情绪、手中物品、最后动作、最后一句对话和未完成即时目标。本章开头必须直接继续该场景；如果确实需要换时间或地点，先用 1—3 段自然桥接写清因果。章节边界不是场景边界，对话、追逐、战斗、调查、试炼和谈判可以跨章。不要因为小纲换了场景就瞬移，也不要机械重复上一章结尾。

## 选择性展开

连续不等于所有过程都详细书写。优先展开会改变人物决定或关系、第一次展示重要世界规则、冲突或悬念真正变化、payoff发生、后面会复用的信息，以及空间本身参与冲突的动作。可以压缩没有新信息的普通路程、已明确的重复疼痛、相同担忧的重复表达、没有新博弈的讨价还价和已经理解的规则复述。重要桥接必须存在，但桥接不等于流水账。

前 3—10 章不要默认给所有功能角色正式名字。只有会复现、会形成关系、会影响后续或作者明确保留的角色才命名；已经建立的重要角色不得被机械改成身份称呼。

最终返回必须使用三个一级标题：# Writer Audit、# 正式正文、# 章节事实摘要；审计信息和事实摘要不得混入正式正文区块。

先遵守当前章事件合同，再在必要时做有明确原因的细节调整。作者最终主要阅读“# 正式正文”。

不要替作者写入文件，不要把未发生的结果说成既定事实。""",
    "review": f"""你是透明协作的 GBrain 故事复盘助手。只根据作者当前页面提供的原计划、实际十章摘要、当前状态、未兑现承诺、尚未发生的远期方向和作者编辑过的 GBrain Inspiration Results，生成一份可编辑 Proposal，不调用任何外部服务。

以页面提供的本书成长基因图、总体设计画像和已经发生的正文事实为优先，不重复注入产品默认方向，不把任何固定成长链当作本书规则。

请输出：
1. 实际完成内容；
2. 重复或未兑现的问题；
3. 对远期计划的有限建议；
4. 下一批十章逐章小纲。

先输出：

## 当前实际运行了什么成长循环

说明过去十章主要依靠了哪些变量和转换关系，提供了什么阅读满足。

## 实际产生了什么变化

说明主角能够做、理解、影响、控制或进入的范围发生了什么改变。

## 是否重复使用同一路径

如果过去两批依赖同一种转换方式，说明下一批怎样换另一个循环、改变关键变量、让旧循环失效、连接两个循环，或让之前的副循环成为主循环。

## 成长基因图是否需要更新

只有正文已经证明原设计不准确时才提出 Proposal；否则写“当前成长基因图暂不调整”。

如果实际写作已经证明总体画像需要变化，先输出：

## 总体画像需要调整的地方

只写被已发生事实支持的有限建议，不自动修改 BOOK；如果没有必要调整，明确写“暂不调整”。

在逐章小纲之前，先写：

## 下一批十章总体事件链

用 3—6 句话说明这一批十章从什么具体状态开始、出现什么问题、主角准备怎么解决、中途发生什么转折、第十章左右具体兑现什么，以及留下什么新问题。

下一批十章必须使用与 outline 完全相同的格式：

## 第N章：具体标题
具体剧情：用 2—4 句写具体人物、事件和主角行动。
结果 / 状态变化：写直接结果和状态变化。
叙事功能：写本章在局部故事中的作用。
结尾推动：写下一章为什么发生。

第N章的结尾推动必须成为第N+1章具体剧情的直接因果起点；如果换地点、时间或主要人物，第N+1章必须写出桥接动作。章节边界不是场景边界，不要为每章强行重置到新场景。

十章必须组成一个连续的局部故事。禁止只写“主角继续调查”“危机升级”“爆发点”“关系深化”或“敌人变强”，再让 Writer 自己补造剧情。

建议必须尊重已经发生的事实，不能自动采用、保存或重写 BOOK。""",
}


def _specialist_prompt_template(label: str, duties: str) -> str:
    return f"""你是透明协作的 {label} 专项 Agent。你是建议者，不是审判者：不评分、不拒绝 Primary Writer、不要求必须发现问题、不输出整章重写，也不触发上游重跑。只根据当前章事件合同、Primary Draft、分配给你的 Curated Context 和必要的前文章末衔接片段，提出真正有效的局部修改建议。

职责：
{duties}

固定输出格式：
# Specialist Audit
只写真实发现的问题；没有时必须写：未发现需要修改的事项。

# Proposed Patches
没有建议时写：无。
有建议时最多写 3 个局部 Patch，每个使用以下结构：
## Patch N
目标锚点：
操作：replace / insert_before / insert_after
建议文本：
理由：

Patch 不能改变主要事件、直接结果、人物决定、资源状态或章节结尾推动。不要给正文打分，不要输出 chain-of-thought。"""


HYBRID_PROMPT_TEMPLATES = {
    "context_curator": """你是透明协作的 Context Curator。只从较长设计输入中筛选本章真正相关的信息，压缩上下文，不重写 CANON PROSE，不重新规划本章，不创造新事实。BOOK CONTRACT、计划和 Inspiration 中尚未发生的内容不得写成既成事实；AUTHOR NOTES 不是 Canon。字符数只是观察值，不是门禁。

固定输出格式：
# Curator Audit
只报告输入中的明确冲突或无法判断是否相关的项目；没有时写：无需要报告的冲突或不确定项。

# Curated Chapter Context
必须使用以下二级标题，全部保留；无相关内容时写“无”：
## Relevant Book Contract
## Relevant Characters and Relationships
## Relevant World Rules
## Relevant Open Promises
## Relevant Plan
## Relevant Prose Controls
## Opening Strategy
## Relevant Inspiration

只选择当前章需要的信息，不复制完整 BOOK、完整十章计划或完整前文，不输出内部推理。""",
    "primary_writer": """你是透明协作的 Primary Writer。先独立写出一篇完整章节；四个专项 Agent 尚未提供任何修改，不要预先采用它们的意见。正文必须落实当前章事件合同，包含自然的叙事、对话、动作、内心、描写和结尾推动，而不是骨架或分镜。保持统一叙事声音，不为了连续性反复盘点已经清楚的物品、资源和交易。

Curated Context 为空时，明确把下方完整必要上下文作为 fallback 使用；这不是失败，也不自动重试。

固定输出格式：
# Primary Writer Audit
只报告实际冲突、必要桥接和实质调整；没有时写：无。
# Primary Draft
一篇完整的正式章节正文。
# Primary Fact Summary
只写本 Draft 已经成立的事实摘要，不写计划或内部推理。""",
    "specialist_opening": _specialist_prompt_template(
        "Opening & Scene Entry Agent",
        "检查 BOOK 已选择的开篇策略是否被执行；第一章若为讲述者宏观开场，检查世界远景→运行秩序/力量结构→当前压力→具体地域→主角现场→主角行动的收束；检查说明是否只服务未来约 30 章必要信息、是否仍像小说、镜头是否交给主角。非第一章检查章首承接和换景因果。不得把普通章节擅自改成宏观开场。",
    ),
    "specialist_dialogue": _specialist_prompt_template(
        "Dialogue & Character Voice Agent",
        "检查核心角色声音是否可区分；对话是否改变信息、关系、决定或行动；是否有同质化、纯说明式对白、缺乏潜台词/拒绝/回避/立场。不得改变主要事件和人物决定。",
    ),
    "specialist_action": _specialist_prompt_template(
        "Action & Spatial Logic Agent",
        "检查动作方向、位置、对象和结果；人物与物品是否无故出现或消失；调查、追逐、操作和空间移动是否连贯；世界规则是否通过行动产生后果；是否遗漏改变局面的关键动作。不得把正文改成战术说明书。",
    ),
    "specialist_emotion": _specialist_prompt_template(
        "Emotion & Aftermath Agent",
        "检查重大行动、胜利、失败和关系变化的真实余波；情绪是否通过动作、选择、沉默或感官进入；配角是否只有功能反应；payoff 后是否缺少确认与新压力；是否重复解释情绪。不得强制增加痛苦、悲剧代价或伦理惩罚。",
    ),
    "chapter_integrator": """你是透明协作的 Revision Integrator。Primary Draft 是唯一正文底稿。逐项判断四个专项 Agent 的局部 Patch 是否真正改善正文；冲突、重复、改变事件结果、破坏人物声音或重新规划章节的建议必须拒绝。四类建议不必全部采纳，全部不采纳也是正常结果。保持 Primary Writer 的主要叙事声音，不做第二轮自我审稿，不输出整章重写说明或内部推理。

固定输出格式：
# Writer Audit
报告正式正文字符数、实际采用的专项修改类型、未采用的冲突/无必要建议，以及实际 Canon / Plan 冲突或实质调整；没有时写：无。
# 正式正文
只输出最终整合后的正式小说正文；它必须以 Primary Draft 为底稿。
# 章节事实摘要
根据最终整合正文重新生成，只写最终正文已经成立的事实，不能机械复用 Primary Fact Summary。""",
}

DEFAULT_PROMPT_TEMPLATES.update(HYBRID_PROMPT_TEMPLATES)

HYBRID_PROMPT_MODES = frozenset(HYBRID_PROMPT_TEMPLATES)
SPECIALIST_PROMPT_MODES = frozenset(
    {f"specialist_{name}" for name in ("opening", "dialogue", "action", "emotion")}
)


#: state_delta 模式的内置模板（页面不提供可编辑模板；为空时由 generate_prompt 自动使用）。
#: 职责限定为书记员：只根据正式正文更新状态区提案；不检查 BOOK CONTRACT，不是章节门禁。
DEFAULT_STATE_DELTA_TEMPLATE = """你是透明协作的 State Delta 书记员。只根据下方当前章节编号、当前规范化 CANON INDEX、本次新提取的正式正文和 Writer 章节事实摘要，生成 BOOK 状态区的完整替换提案，不调用任何外部服务。

本次正式正文是 State Delta 的最高事实来源；Writer 章节事实摘要仅作辅助，冲突时以正式正文为准。AUTHOR NOTES 是作者元控制，不属于 Canon 事实，必须原样保留。

你不检查、也不报告 BOOK CONTRACT 或任何长期设计的状态；BOOK CONTRACT、完整百章计划、十章计划、prose profile、GBrain、Reference Programs 与前两章正文都不在本次输入中，不要猜测它们。

最终返回必须使用两个一级标题：

# State Delta Audit
只报告实际存在的事项：
- 本次正式正文与旧 CANON INDEX 的冲突；
- 无法从正式正文确定的状态。
没有时写：无需要报告的状态冲突或不确定项。

# Proposed Canon Index
完整状态区替换提案，必须使用以下格式：
当前已完成第N章。
最近章节摘要：（只保留当前产品实际需要的最近章节；新摘要必须来自正式正文；不复制 Writer Audit；不把计划写成事实）
当前状态：（只写当前确实成立的地点、人物、资源、物品、能力、知识、关系、伤势、即时目标和外部压力；只更新正文真实改变的项目）
未兑现承诺：（保留仍有效的旧承诺；新增正文真实建立的新承诺；删除或标记已兑现/失败/失效的承诺；不把普通悬念升级为长期承诺）
作者备注：（原样保留旧 AUTHOR NOTES，不得增删改写）

注意：各字段内容行不得以「最近章节摘要：」「当前状态：」「未兑现承诺：」「作者备注：」四个标签开头，否则会被确定性解析为新字段的开始。

禁止：输出 JSON/YAML；输出 chain-of-thought；修改 BOOK CONTRACT、PLAN 或正式章节正文；把 AUTHOR NOTES 当成 Canon 事实修改；替作者写入任何文件。"""


#: 规范化 CANON INDEX 的四个字段；只支持本项目真实使用的标签与格式。
CANON_INDEX_FIELDS = ("current_state", "recent_summaries", "open_promises", "author_notes")

_CANON_COMPLETED_CHAPTER_PATTERN = re.compile(r"^当前已完成第\s*(\d+)\s*章。?$")

_CANON_FIELD_LABELS = (
    ("最近章节摘要", "recent_summaries"),
    ("当前状态", "current_state"),
    ("未兑现承诺", "open_promises"),
    ("作者备注", "author_notes"),
)


def _match_canon_field_label(stripped: str) -> tuple[str, str] | None:
    """行以四个字段标签之一加冒号开头时返回（字段 key, 行内剩余内容），否则 None。"""
    for label, key in _CANON_FIELD_LABELS:
        if not stripped.startswith(label):
            continue
        rest = stripped[len(label):]
        if not rest or rest[0] not in "：:":
            continue
        return key, rest[1:].strip()
    return None


def parse_canon_index(status_text: str) -> dict[str, str]:
    """确定性解析 BOOK 状态区为规范化 CANON INDEX 四字段（纯函数）。

    只支持本项目真实使用的标签与格式：「当前已完成第N章。」「最近章节摘要：」
    「当前状态：」「未兑现承诺：」「作者备注：」。不调用 LLM，不写文件，
    不建通用 Markdown 框架。缺失字段返回空字符串。
    「当前已完成第N章。」计入 current_state（已发生事实的压缩状态）。

    边界约束（确定性行为）：
    - 首个字段标签出现前的无标签行并入 current_state（与「当前已完成第N章。」
      的归属一致），不静默丢弃；
    - 字段内容中一旦某行以四个标签之一加冒号开头，即整体切换到该字段；
      因此内容行不应以「最近章节摘要：」「当前状态：」「未兑现承诺：」
      「作者备注：」四个标签开头。
    """
    collected: dict[str, list[str]] = {key: [] for key in CANON_INDEX_FIELDS}
    completed: list[str] = []
    current_key: str | None = None
    for raw_line in status_text.splitlines():
        stripped = raw_line.strip()
        if current_key is None and _CANON_COMPLETED_CHAPTER_PATTERN.match(stripped):
            completed.append(stripped)
            continue
        matched = _match_canon_field_label(stripped)
        if matched is not None:
            current_key, inline = matched
            if inline:
                collected[current_key].append(inline)
            continue
        if current_key is not None:
            collected[current_key].append(raw_line)
        elif stripped:
            collected["current_state"].append(stripped)
    fields = {key: "\n".join(lines).strip() for key, lines in collected.items()}
    if completed:
        head = "\n".join(completed)
        body = fields["current_state"]
        fields["current_state"] = f"{head}\n{body}".strip() if body else head
    return fields


def canon_index_has_labels(status_text: str) -> bool:
    """状态区是否使用了本项目支持的 CANON INDEX 字段标签格式。

    收紧判定：至少命中一个字段标签（当前状态/最近章节摘要/未兑现承诺/作者备注）
    才算有标签；只含「当前已完成第N章。」与无标签自由文本时判定为无标签，
    调用方应原样注入，避免渲染出「（未填写）」占位块改变逐字注入行为。
    """
    return any(
        _match_canon_field_label(line.strip()) is not None
        for line in status_text.splitlines()
    )


def render_canon_index(
    fields: Mapping[str, str], *, page_recent_summaries: str = ""
) -> str:
    """渲染规范化 CANON INDEX 四段；最近摘要只注入一份。

    页面显式传入 recent_summaries 时用它，否则用解析出的 BOOK 内摘要；
    两者不会同时出现。AUTHOR NOTES 明确标注为作者元控制。
    """
    recent = page_recent_summaries.strip() or fields.get("recent_summaries", "").strip()
    blocks = (
        ("CURRENT STATE（已发生事实的压缩状态）", fields.get("current_state", "").strip()),
        ("RECENT SUMMARIES（最近章节事实摘要；本次只注入这一份）", recent),
        ("OPEN PROMISES（未兑现承诺；不等于已发生事实）", fields.get("open_promises", "").strip()),
        (
            "AUTHOR NOTES（作者元控制；不属于 Canon 事实；State Delta 不得自动修改或删除）",
            fields.get("author_notes", "").strip(),
        ),
    )
    return "\n\n".join(f"{title}：\n{body or '（未填写）'}" for title, body in blocks)


def _render_canon_status_without_summaries(status_block: str) -> str:
    """标签化状态区只渲染 current_state/open_promises/author_notes 三段。

    供 chapter_prep 在页面显式摘要非空时扣除内嵌最近章节摘要段，避免重复注入。
    """
    fields = parse_canon_index(status_block)
    blocks = (
        ("CURRENT STATE（已发生事实的压缩状态）", fields.get("current_state", "").strip()),
        ("OPEN PROMISES（未兑现承诺；不等于已发生事实）", fields.get("open_promises", "").strip()),
        (
            "AUTHOR NOTES（作者元控制；不属于 Canon 事实；State Delta 不得自动修改或删除）",
            fields.get("author_notes", "").strip(),
        ),
    )
    return "\n\n".join(f"{title}：\n{body or '（未填写）'}" for title, body in blocks)


class HardGateError(ValueError):
    def __init__(self, missing_fields: list[str]) -> None:
        self.missing_fields = missing_fields
        super().__init__("当前章小纲缺少非空字段：" + "、".join(missing_fields))


def parse_outline_fields(outline: str) -> dict[str, str]:
    """Parse the eight supported outline fields from individual lines."""
    values: dict[str, str] = {}
    for line in outline.splitlines():
        match = re.match(r"^\s*(?:[-*]\s*)?([^：:]+?)\s*[：:]\s*(.*?)\s*$", line)
        if not match:
            continue
        label = match.group(1).strip()
        value = match.group(2).strip()
        if label in REQUIRED_OUTLINE_FIELDS and value:
            values[label] = value
    return values


def validate_current_outline(outline: str) -> None:
    values = parse_outline_fields(outline)
    missing = [field for field in REQUIRED_OUTLINE_FIELDS if not values.get(field)]
    if missing:
        raise HardGateError(missing)


def _display_value(value: Any) -> str:
    if value is None:
        return "（未填写）"
    if isinstance(value, (list, tuple)):
        return "；".join(_display_value(item) for item in value)
    if isinstance(value, Mapping):
        return "；".join(f"{key}：{_display_value(item)}" for key, item in value.items())
    return str(value).strip() or "（未填写）"


def format_references(references: Iterable[Mapping[str, Any]]) -> str:
    lines: list[str] = []
    fields = (
        "program_id",
        "story_phase",
        "input_state",
        "central_pressure",
        "reusable_program",
        "applicable_conditions",
        "failure_modes",
        "anti_repetition_notes",
        "output_state",
    )
    for index, reference in enumerate(references, start=1):
        lines.append(f"Reference Program {index}")
        for field in fields:
            lines.append(f"{field}: {_display_value(reference.get(field))}")
        lines.append("")
    return "\n".join(lines).strip() or "（本次未选择 Reference Program）"


def _input_block(title: str, value: str) -> str:
    return f"## {title}\n\n{value.strip() or '（未填写）'}"


def _extract_markdown_block(content: str, heading: str) -> str:
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != heading:
            continue
        collected: list[str] = []
        for next_line in lines[index + 1:]:
            stripped = next_line.strip()
            if stripped.startswith("# ") or (heading.startswith("## ") and stripped.startswith("## ")):
                break
            collected.append(next_line)
        return "\n".join(collected).strip()
    return ""


def _chapter_book_context(book_content: str) -> str:
    blocks: list[str] = []
    growth_genome = _extract_markdown_block(book_content, "## 0. 本书成长基因图")
    if growth_genome:
        blocks.append(f"## 0. 本书成长基因图\n\n{growth_genome}")
    headings = (
        "## 1. 核心类型与读者承诺",
        "## 2. 世界观结构",
        "## 3. 世界如何持续制造剧情压力",
        "## 4. 主角模型、人物弧与核心矛盾",
        "## 5. 配角与关系系统",
        "## 7. 叙事结构",
        "## 8. 文风与可操作参数",
        "## 9. 对话特点",
        "## 10. 节奏结构",
    )
    blocks.extend([
        f"{heading}\n\n{_extract_markdown_block(book_content, heading)}"
        for heading in headings
        if _extract_markdown_block(book_content, heading)
    ])
    return "\n\n".join(blocks)


_MULTI_WRITER_HEADING_PATTERN = re.compile(
    r"^#{1,6}\s*(?:串行写作协议|Writer\s*[ABC](?![0-9A-Za-z]))"
)
#: 多 Writer 特征行：串行调度 Writer A、SUBAGENT_MODE 报告，或任何单独的 Writer A/B/C
#: 职责标记（lookahead 与测试守卫 _WRITER_ABC_PATTERN 口径一致，不误伤 Writer Audit）。
_MULTI_WRITER_LINE_PATTERN = re.compile(
    r"(?:串行(?:调用)?\s*Writer\s*A|SUBAGENT_MODE|Writer\s*[ABC](?![0-9A-Za-z]))"
)
#: sanitize 的 Audit 替换行只放一行短句；完整 WRITER_AUDIT_RULE 全文由
#: PROSE_REALIZATION_CONTRACT 只注入一次，避免旧模板路径双注入。
_SINGLE_WRITER_AUDIT_LINE = (
    "Writer Audit 只报告实际存在的事项；完整规则见本 Prompt 的 "
    "Story MVP Prose Realization Contract，没有冲突或实质调整时写："
    "无需要报告的冲突或实质调整。"
)
_SINGLE_WRITER_BODY_LINE = "只放本次直接写作的完整小说正文。"


#: BOOK CONTRACT 与 CANON INDEX 区块标签附带的语义说明（渲染时前置）。
BOOK_CONTRACT_BLOCK_NOTE = (
    "这里可以包含未来人物弧、未来关系变化、阶段方向和读者承诺。"
    "Writer 应让当前章节与其保持方向一致，但不得把其中尚未发生的内容写成当前事实，"
    "也不得因为局部计划调整就把它当作 Canon 冲突。"
    "已发生事实不能被 BOOK CONTRACT 覆盖；若正文证明旧设计已失效，保留已发生事实并在 Writer Audit 报告。"
)
CANON_INDEX_BLOCK_NOTE = "它低于正式正文；若与正式正文冲突，以正式正文为准。"


def _annotated_block(note: str, content: str) -> str:
    return f"{note}\n\n{content.strip()}" if content.strip() else note


#: 三标题输出合同中需要注入单 Writer 替换行的合同标题。
_SINGLE_WRITER_CONTRACT_HEADINGS = ("# Writer Audit", "# 正式正文")


def sanitize_chapter_template(template: str) -> tuple[str, bool]:
    """单 Writer 合同的确定性执行机制（组装期净化），不是数据/API 兼容层。

    chapter 组装时对提交模板做确定性净化，只影响 prompt 组装，不修改任何文件：

    - 「串行写作协议 / Writer A / Writer B / Writer C」标题区块内逐行判断：
      只丢弃命中多 Writer 特征的行（_MULTI_WRITER_LINE_PATTERN、以「只放 Writer」
      开头的行、多 Writer 子标题行），同区块内的普通作者内容（如命名规则、
      三标题输出合同引导句）原样保留；
    - 把三标题输出合同中引用 Writer A/B/C 中间稿的行替换为单 Writer 描述；
      注入依据「最近保留的输出合同标题」状态（last_contract_heading），
      不依赖该行与合同标题物理相邻；
    - 删除其余描述 Writer A/B/C 串行写作的行。
    """
    kept: list[str] = []
    changed = False
    skip_level = 0
    last_contract_heading: str | None = None
    for line in template.splitlines():
        stripped = line.strip()
        is_heading = stripped.startswith("#")
        heading_level = len(stripped) - len(stripped.lstrip("#")) if is_heading else 0
        if skip_level and is_heading and heading_level <= skip_level:
            skip_level = 0
        if is_heading and _MULTI_WRITER_HEADING_PATTERN.match(stripped):
            skip_level = heading_level
            changed = True
            continue
        if is_heading:
            last_contract_heading = (
                stripped if stripped in _SINGLE_WRITER_CONTRACT_HEADINGS else None
            )
            kept.append(line)
            continue
        if re.match(r"^只放\s*Writer\s*[ABC]", stripped):
            kept.append(_SINGLE_WRITER_BODY_LINE)
            changed = True
            continue
        if _MULTI_WRITER_LINE_PATTERN.search(line):
            if last_contract_heading == "# Writer Audit":
                kept.append(_SINGLE_WRITER_AUDIT_LINE)
            elif last_contract_heading == "# 正式正文":
                kept.append(_SINGLE_WRITER_BODY_LINE)
            changed = True
            continue
        if "A/B 中间稿、" in line:
            kept.append(line.replace("A/B 中间稿、", ""))
            changed = True
            continue
        kept.append(line)
    return "\n".join(kept).strip(), changed


def generate_prompt(
    *,
    mode: str,
    template: str,
    book_content: str,
    creative_direction: str = "",
    proposal_context: str = "",
    current_long_block: str = "",
    previous_chapter_text: str = "",
    current_outline: str = "",
    current_chapter_plan: str = "",
    recent_summaries: str = "",
    selected_references: list[Mapping[str, Any]] | None = None,
    gbrain_inspiration: str = "",
    actual_summaries: str = "",
    current_state: str = "",
    unfulfilled_promises: str = "",
    future_direction: str = "",
    chapter_number: int = 0,
    chapter_prose: str = "",
    chapter_fact_summary: str = "",
    writer_mode: str = "hybrid_full",
    curator_response: str = "",
    curated_context: str = "",
    primary_writer_response: str = "",
    primary_draft: str = "",
    primary_fact_summary: str = "",
    specialist_opening_response: str = "",
    specialist_dialogue_response: str = "",
    specialist_action_response: str = "",
    specialist_emotion_response: str = "",
    enabled_specialists: Mapping[str, bool] | None = None,
) -> str:
    if mode not in PROMPT_MODES:
        raise ValueError(f"未知 Prompt 模式：{mode}")
    if len(selected_references or []) > 3:
        raise ValueError("最多只能选择 3 个 Reference Program")
    if mode == "chapter" or mode in HYBRID_PROMPT_MODES:
        validate_current_outline(current_outline)

    if mode in SPECIALIST_PROMPT_MODES or mode == "chapter_integrator":
        if not primary_draft.strip():
            from .hybrid_runtime import extract_primary_draft

            primary_draft = extract_primary_draft(primary_writer_response)
        if not primary_draft.strip():
            raise ValueError("Primary Draft 为空，无法进入专项或 Integrator 阶段")

    prompt_template = template.strip()
    if mode in HYBRID_PROMPT_MODES and not prompt_template:
        prompt_template = DEFAULT_PROMPT_TEMPLATES[mode]
    stripped_legacy_writer = False
    if mode == "chapter":
        prompt_template, stripped_legacy_writer = sanitize_chapter_template(template)
    elif mode == "state_delta" and not prompt_template:
        prompt_template = DEFAULT_STATE_DELTA_TEMPLATE
    parts = [prompt_template, ""]
    if mode == "chapter":
        if stripped_legacy_writer:
            parts.append(SINGLE_WRITER_RUNTIME_NOTE)
        parts.extend(["# Story MVP Prose Realization Contract", PROSE_REALIZATION_CONTRACT])
        # 惰性导入：chapter_context 顶层依赖本模块，模块级互相导入会构成循环导入。
        from .chapter_context import build_chapter_context

        packet = build_chapter_context(
            book_content=book_content,
            current_long_block=current_long_block,
            previous_chapter_text=previous_chapter_text,
            current_outline=current_outline,
            recent_summaries=recent_summaries,
            gbrain_inspiration=gbrain_inspiration,
            selected_references=selected_references,
        )
        parts.append("# 页面当前输入（章节运行期上下文）")
        parts.append(_input_block(
            "AUTHORITY——权威规则（按维度划分）与冲突处理（最小权威规则，仅此一份）",
            packet.authority,
        ))
        parts.append(_input_block(
            "BOOK CONTRACT——长期设计与稳定方向，不等于已经发生",
            _annotated_block(BOOK_CONTRACT_BLOCK_NOTE, packet.book_contract),
        ))
        parts.append(_input_block("CHAPTER MISSION——本章事件合同（PLAN）", packet.chapter_mission))
        parts.append(_input_block("CANON PROSE——前文正文（已发生事实的最高来源）", packet.recent_prose))
        parts.append(_input_block(
            "CANON INDEX——已发生事实的压缩索引",
            _annotated_block(CANON_INDEX_BLOCK_NOTE, packet.canon_context),
        ))
        parts.append(_input_block("PLAN——滚动计划（尚未发生的当前意图）", packet.rolling_plan))
        parts.append(_input_block("PROSE PROFILE——BOOK §7—§10 软表达控制", packet.prose_profile))
        parts.append(_input_block(
            "OPTIONAL INSPIRATION——可选参考（不得覆盖以上任何层级）",
            packet.optional_inspiration,
        ))
    elif mode in HYBRID_PROMPT_MODES:
        from .chapter_context import build_chapter_context
        from .hybrid_runtime import (
            build_curator_context,
            build_integrator_context,
            build_specialist_context,
        )

        packet = build_chapter_context(
            book_content=book_content,
            current_long_block=current_long_block,
            previous_chapter_text=previous_chapter_text,
            current_outline=current_outline,
            recent_summaries=recent_summaries,
            gbrain_inspiration=gbrain_inspiration,
            selected_references=selected_references,
        )
        parts.append(f"# Hybrid Runtime\n\nwriter_mode: {writer_mode}")
        if mode == "context_curator":
            context = build_curator_context(packet)
            parts.extend(
                [
                    _input_block("AUTHORITY", context.authority),
                    _input_block("当前章事件合同", context.chapter_mission),
                    _input_block("BOOK CONTRACT", context.book_contract),
                    _input_block("规范化 CANON INDEX", context.canon_index),
                    _input_block("当前大型剧情块与十章计划", context.rolling_plan),
                    _input_block("PROSE PROFILE", context.prose_profile),
                    _input_block("OPTIONAL INSPIRATION", context.optional_inspiration),
                    _input_block("前文章末局部衔接片段", context.transition_context),
                ]
            )
        elif mode == "primary_writer":
            curated = curated_context.strip() or curator_response.strip()
            fallback = not curated
            parts.extend(
                [
                    _input_block("AUTHORITY", packet.authority),
                    _input_block("Chapter Mission——当前章事件合同", packet.chapter_mission),
                    _input_block("CANON PROSE——必要前文正文", packet.recent_prose),
                    _input_block("CANON INDEX——规范化已发生事实索引", packet.canon_context),
                    _input_block(
                        "Curated Chapter Context" if not fallback else "Curated Chapter Context（缺失时的显式 fallback）",
                        curated or "Curator 未提供，使用完整上下文 fallback：\n\n"
                        + packet.book_contract
                        + "\n\n"
                        + packet.rolling_plan
                        + "\n\n"
                        + packet.prose_profile,
                    ),
                ]
            )
        elif mode in SPECIALIST_PROMPT_MODES:
            specialist = mode.removeprefix("specialist_")
            context = build_specialist_context(
                packet,
                curated_context.strip() or curator_response.strip(),
                primary_draft,
                specialist,
            )
            parts.extend(
                [
                    _input_block("当前章事件合同", context.chapter_mission),
                    _input_block("Primary Draft——唯一待评议正文底稿", context.primary_draft),
                    _input_block("本专项相关 Curated Context", context.relevant_curated_context),
                    _input_block("必要的前文章末衔接片段", context.transition_context),
                ]
            )
        else:
            specialists = {
                "opening": specialist_opening_response,
                "dialogue": specialist_dialogue_response,
                "action": specialist_action_response,
                "emotion": specialist_emotion_response,
            }
            enabled = dict(enabled_specialists or {})
            specialists = {
                name: value if enabled.get(name, True) else "未提供（作者未启用）"
                for name, value in specialists.items()
            }
            context = build_integrator_context(
                packet,
                curated_context.strip() or curator_response.strip(),
                primary_draft,
                specialists,
            )
            parts.extend(
                [
                    _input_block("AUTHORITY", context.authority),
                    _input_block("当前章事件合同", context.chapter_mission),
                    _input_block("必要 CANON PROSE", context.canon_prose),
                    _input_block("CANON INDEX", context.canon_index),
                    _input_block("Curated Chapter Context", context.curated_context),
                    _input_block("Primary Draft——唯一正文底稿", context.primary_draft),
                    _input_block("Opening Specialist Response", context.specialist_responses["opening"]),
                    _input_block("Dialogue Specialist Response", context.specialist_responses["dialogue"]),
                    _input_block("Action Specialist Response", context.specialist_responses["action"]),
                    _input_block("Emotion Specialist Response", context.specialist_responses["emotion"]),
                ]
            )
    elif mode == "chapter_prep":
        parts.append("# 页面当前输入")
        parts.append(_input_block("本书执行相关画像", _chapter_book_context(book_content)))
        parts.append(_input_block("当前大型剧情块", current_long_block))
        parts.append(_input_block("当前章对应的十章计划条目", current_chapter_plan))
        parts.append(_input_block("前两章正文（连续性上下文）", previous_chapter_text))
        parts.append(_input_block("最近 1—3 章摘要", recent_summaries))
        status_block = _extract_markdown_block(book_content, CURRENT_STATE_HEADING)
        if recent_summaries.strip() and canon_index_has_labels(status_block):
            # 页面显式摘要非空时，扣除标签化状态区内嵌的最近章节摘要段，
            # 避免同一 Prompt 出现两份摘要；页面摘要为空时保持注入 BOOK 内摘要。
            status_display = _render_canon_status_without_summaries(status_block)
        else:
            status_display = status_block
        parts.append(_input_block("当前状态", status_display))
    elif mode == "state_delta":
        # State Delta 只注入四组输入；默认不注入完整 BOOK CONTRACT、完整百章计划、
        # GBrain、Reference Programs、prose profile 或前两章完整正文。
        status_block = _extract_markdown_block(book_content, CURRENT_STATE_HEADING)
        if canon_index_has_labels(status_block):
            canon_index = render_canon_index(
                parse_canon_index(status_block), page_recent_summaries=recent_summaries
            )
        else:
            # 无标签旧格式状态区原样注入，避免 parse_canon_index 静默清空旧状态；
            # 页面显式摘要此时单独注入一份（与 chapter 模式语义一致，不重复注入）。
            page_summaries = recent_summaries.strip()
            canon_index = status_block
            if page_summaries:
                summary_block = f"最近 1—3 章摘要\n\n{page_summaries}"
                canon_index = f"{canon_index}\n\n{summary_block}" if canon_index else summary_block
        parts.append("# 页面当前输入（State Delta 上下文）")
        parts.append(_input_block("当前章节编号", str(chapter_number) if chapter_number else ""))
        parts.append(_input_block(
            "CANON INDEX——当前规范化 Canon Index（已发生事实的压缩状态）",
            canon_index,
        ))
        parts.append(_input_block(
            "本次新正式章节正文（State Delta 的最高事实来源）",
            chapter_prose,
        ))
        parts.append(_input_block(
            "Writer 章节事实摘要（仅辅助；与正式正文冲突时以正式正文为准）",
            chapter_fact_summary,
        ))
    else:
        parts.append("# 页面当前输入")
        if mode == "idea":
            parts.append(_input_block("作者粗方向", creative_direction))
            parts.append(_input_block("当前 BOOK.md（如果作者已经填写）", book_content))
        elif mode == "review":
            parts.append(_input_block("原计划", book_content))
            parts.append(_input_block("创作方向", creative_direction))
        else:
            parts.append(_input_block("当前 BOOK.md", book_content))
            parts.append(_input_block("创作方向", creative_direction))
        if mode == "outline":
            parts.append(_input_block(
                "作者已选择 / 编辑的规划种子",
                proposal_context.strip() or "（未选择 Idea Proposal）",
            ))
        parts.append(_input_block("选中的 Reference Programs", format_references(selected_references or [])))
        parts.append(_input_block("GBrain Inspiration Results（作者可编辑原文）", gbrain_inspiration))
        if mode == "review":
            parts.append(_input_block("本书成长基因图", _extract_markdown_block(book_content, "## 0. 本书成长基因图")))
            parts.append(_input_block("实际十章摘要", actual_summaries))
            parts.append(_input_block("当前状态", current_state))
            parts.append(_input_block("未兑现承诺", unfulfilled_promises))
            parts.append(_input_block("尚未发生的 100 章方向", future_direction))

    return "\n\n".join(parts).strip() + "\n"
