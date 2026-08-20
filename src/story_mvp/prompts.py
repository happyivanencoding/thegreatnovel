from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any


PROMPT_MODES = {
    "idea": "Story Program / 商业化结构方案",
    "fantasy_seed": "Fantasy Seed / 核心幻想种子",
    "world_vision": "World Vision / 世界幻想画像",
    "outline": "新书/总纲规划",
    "director": "当前章 Director",
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

DEFAULT_PRODUCT_DIRECTION = """当前产品默认目标是成熟中文男频成长长篇。先让读者清楚感到主角获得了值得拥有的力量、自由、生命层次、身份逆转、探索机会或命运掌控，再让世界和长期故事承载它。创新优先体现在可感知的能力快感、主动行动和阶段升格，而不是用固定痛苦抵消高光。这是创作方向，不是机械模板；如果作者明确要求其他类型，以作者要求为准。"""

DEFAULT_COMPOSABLE_GROWTH_DIRECTION = """Growth Genome 是整理工具，不是创造世界的第一语言。它只负责在核心幻想、世界画像和长期故事方向已经批准后，整理一级成长、二级收益、阶段升格、主循环、反哺关系和重复风险，帮助故事运行到更长篇幅。它不选择核心幻想，不替主角决定欲望，不决定力量是否令人向往，也不要求所有故事制度化。"""

CLASSIC_PATTERN_DIRECTION = """经典成长模式是一等公民：可组合只表示不强迫所有作品相同，不表示主动回避成熟主干。资源→成长→战斗→身份→更高级资源→更大世界，以及职业→技能→任务→身份、探索→机缘→成长→新区域、内容副本→战斗→战利品→构筑等，都可以成为本书主干。如果作者输入、GBrain证据或当前创意表明某条经典链最适合本书，应当保留它，创新放在新优势、世界机制、转换方式、关系反馈或阶段变异上。"""

GROWTH_BENEFIT_HIERARCHY = """Growth Benefit Hierarchy：
一级成长收益是读者长期期待主角本人越来越能做什么，优先写力量、战斗、神通、技艺、生命层次、规则掌控、造物或其它个人能力；它是主轴，不是职位、权限或组织规模。
二级成长收益是一级能力运行后的外部结算，例如财富、资源、装备、身份、关系、势力、领地和世界入口；它们只在真实需要时出现，并服务于下一次一级成长。
Growth Genome 可以用一级能力 → 二级收益 → 新资源/场景/敌人/入口 → 下一轮一级成长整理长期因果，但不要求每本书都使用复杂网络。"""

INTERNAL_REALISM_DIRECTION = """内部因果必须可信，但可信不等于现代程序真实。玄幻、仙侠、奇幻、科幻和异世界优先使用本世界的力量、阶层、资源、信仰、血脉、地域、种族、宗门、王朝、神明、天道与超凡规则制造因果。只有作者明确选择现实职业或制度题材时，现代工业流程、项目管理、质量控制、学术实验、行政审批、合同责任、合规审查和数据留痕才可以成为主要发动机。"""

PAYOFF_FIRST_COST_RHYTHM = """Payoff-first 成本节奏：成熟不等于每次胜利立即受伤、负债、被审查或承担新责任。默认顺序是：胜利或突破真正发生 → 外界反应 → 主角获得实际收益 → 收益改变行动空间 → 再决定是否需要代价或余波。普通小胜允许明显净收益；阶段大胜通常应当收益明显大于当前成本。成本只在真实需要时限制选择、迫使策略或推动换挡，不作为每次 Payoff 的固定税。"""


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


READER_FIRST_PROSE_CONTRACT = """Reader-First Prose Contract：这是表达层合同，不重规划本章事实。

1. 动作先于术语：第一次出现本书独有概念时，先让读者看见对象、动作和结果，再由人物用普通话形成理解；只有反复使用确实能减少解释时才固定命名。
2. 常见题材词可以自然使用；本书新造的机制、部件、阵法和抽象关系必须先通过场景成立，不要为了显得原创而给普通动作换名字。
3. 普通语言优先：能用“借力、卡住、撞开、绕过去、压下来、黏住、看见、躲开、把力量送过去”说清楚时，不默认升级成工程或审计术语。
4. 已经通过动作成立的边界只在发生新变化时更新，不连续用“不是、没有、尚未、并不、不代表、还不能算”重复证明旧边界。
5. 段落要有真实节拍变化；连续动作、观察或判断保持自然段，单句段留给冲击、决定、翻转、停顿、强烈反应和章末钩子。
6. 重大首次兑现先写结果、外界反应、主角实际收益和行动空间，再写必要的限制或代价；不要用三种同义表述同时削弱兑现。
7. 主角的判断要带着自己的经历、习惯、偏见、欲望、幽默或刻薄，不把人物写成通用的冷静正确男主。

准确机制仍须保留，但优先通过可见动作、直接结果、人物理解和后续选择让读者理解。"""


READER_FIRST_PROSE_SHORT = """Reader-First 短投影：以可见对象、人物动作、现场结果和普通语言优先；新造术语先用场景成立，已通过动作成立的边界不重复解释；连续动作保持自然段，重大兑现先落地再写必要限制。"""

SINGLE_WRITER_RUNTIME_NOTE = "运行期声明：本次为单 Writer 直接写作；任何多 Writer 协议已被本运行合同取代。"

#: BOOK.md「当前状态、未兑现承诺与作者备注」一级标题受保护锚点；
#: chapter_prep 与 chapter_context（CANON_INDEX_STATUS_HEADING）都引用本常量。
CURRENT_STATE_HEADING = "# 当前状态、未兑现承诺与作者备注"


DEFAULT_DIRECTOR_TEMPLATE = """你是透明协作的当前章 Director。只根据当前大型剧情块的压缩摘要、当前章十章计划条目、压缩成长基因、当前 Canon Index、最近一章摘要、前文章末衔接和作者当前章意图，生成本章可执行的八字段事件合同。你不读取完整 BOOK、完整百章计划、完整十章计划、GBrain 原始结果、Genre Prior 或前两章完整正文，不重新规划整本书，不创造已发生事实。

必须输出以下八个字段，全部具体填写：
触发事件：
推动事件的人：
主角行动：
对手或世界反应：
直接结果：
状态变化：
叙事功能：
结尾推动力：

八字段之后可以输出一个非必填区块：
## 专项建议
Opening：启用 / 不启用；理由
Dialogue：启用 / 不启用；理由
Action：启用 / 不启用；理由
Emotion：启用 / 不启用；理由

专项建议只是作者可覆盖的运行建议，不是第九个 Hard Gate。通常只建议真正有价值的 0—2 个专项。不要输出正文、审计、评分、完整计划或内部推理。"""


DEFAULT_PROMPT_TEMPLATES = {
    "idea": f"""你是透明协作的男频成长爽文创意助手。根据作者的粗方向、页面上完整可见的 GBrain Inspiration Results 和手动选择的 Reference Programs，生成 3—5 个明显不同的商业男频成长爽文核心创意。不评分、不排名、不替作者选择，不调用任何外部服务。

{DEFAULT_PRODUCT_DIRECTION}

{DEFAULT_COMPOSABLE_GROWTH_DIRECTION}

{CLASSIC_PATTERN_DIRECTION}

{GROWTH_BENEFIT_HIERARCHY}

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
最大的重复风险：这个玩法写久以后最容易重复什么。
## 一级成长收益
说明读者长期最期待主角哪一项个人核心能力成长；写清当前亲自能做什么，而不是职位、信用或权限。
## 一级成长阶段
分别说明早期、中期和约100章时，主角具体多会了什么，至少写出三次玩法质变，不能只写数值、范围或声望扩大。
## 二级成长收益
说明财富、资源、装备、身份、关系、队伍、组织、领地或世界入口如何由一级能力运行产生；不要求每类都存在。
## 反哺关系
用箭头说明二级收益怎样提供资源、使用机会、新敌人、新问题或新入口，推动下一轮一级能力成长。
## 主次失衡风险
说明这个创意最可能怎样让二级收益吞掉一级能力主线，以及如何保持主次关系。""",
    "outline": f"""你是透明协作的 GBrain 故事规划助手。只根据下方作者输入、作者编辑过的 GBrain Inspiration Results 与参考程序，生成一份完整、具体、可编辑的故事规划提案，不调用任何外部服务。

{DEFAULT_PRODUCT_DIRECTION}

{DEFAULT_COMPOSABLE_GROWTH_DIRECTION}

{CLASSIC_PATTERN_DIRECTION}

{GROWTH_BENEFIT_HIERARCHY}

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
### 一级成长收益
必须写：核心成长对象、初始能力、当前限制、第一次质变、第二次质变、第三次质变、约100章能力状态，以及核心玩法如何变化。一级成长必须是主角本人越来越能做什么，不得只写职位、信用、权限、关系或组织规模。
### 二级成长收益
分别说明本书实际需要的资源/财富、身份/声望、关系/队伍、组织/领地、地图/世界入口；不需要的类别明确写“本书不使用”或省略，不强行补齐。
### 反哺关系
用箭头说明二级收益怎样为一级成长提供资源、使用机会、新敌人、新问题、新环境或更高世界入口。
### 主次关系
明确本书长期主要书写什么，哪些内容只是结算与放大器，二级收益何时可以阶段性成为焦点，以及如何防止它取代一级成长。
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
一级成长变化：主角本人的核心能力发生了什么可感知变化；没有变化时说明本块不推进一级成长。
二级收益结算：本块产生了什么资源、身份、关系、组织、领地或世界入口；没有时说明本块不结算。
反哺下一轮：这些收益怎样让下一块能够推进新的一级成长。

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

页面可能提供本章成长收益短投影：本章一级成长推进、本章二级收益结算、本章反哺。它们只是辅助规划信息，不是第九、第十或更多字段；普通承接章、情绪章和调查章可以写“本章不推进”或“本章不结算”。

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

## 一级成长实际发生了什么

说明主角相较十章前，亲自多能做了什么。若没有真实变化，直接写“没有真实的一级成长变化”，不要制造成长。

## 二级收益实际获得了什么

说明资源、财富、身份、声望、关系、队伍、组织、领地或世界入口发生了什么变化。

## 二级收益是否吞掉一级成长

检查过去十章是否主要只写权限、信用、职位、关系、组织、责任或外界评价，而主角核心能力没有新玩法或质变。没有时明确写“未发现二级收益吞掉一级成长”。

## 下一批如何反哺一级成长

只调整下一批计划：说明已经获得的二级收益如何提供资源、使用机会、新敌人、新问题、新环境或更高入口，推动下一轮一级能力成长。

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
其中必须额外写出：本批一级成长目标、本批二级收益目标、本批反哺关系。它们是规划说明，不是单章必填字段。

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

## Reader-Facing Language
只写本章需要的正文表达建议：内部机制用普通话如何落到对象、动作和结果；哪些题材常用词可以直接使用；哪些本书新造词必须先用动作解释；哪些策划术语不应直接进入正文。不得改写剧情。

## Already Established — Do Not Re-explain
列出最近正文已经通过动作清楚证明、且本章没有新变化的边界。它们仍然有效，但 Writer 不需要再次解释。

## Recent Repetition Risks
只列最近两章真实重复的主导场景、主要感官、动作方式、冲突方式、解决套路、否定式说明或章末钩子形式。它是提醒，不是失败判定。

## Payoff and Promise Window
明确区分已经拿到的收益对象、已经兑换或到账的收益、已经改变生活或行动空间的收益，以及仍未兑现的近期读者承诺。不得把待兑换物品写成已经到账。

只选择当前章需要的信息，不复制完整 BOOK、完整十章计划或完整前文；如果提供了本章成长收益短投影，只把三行短投影放在 `## Relevant Plan` 的末尾，不解释整套 Growth Benefit Hierarchy；不输出内部推理。""",
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
        "检查 BOOK 已选择的开篇策略是否被执行；第一章若为讲述者宏观开场，检查世界远景→运行秩序/力量结构→当前压力→具体地域→主角现场→主角行动的收束；检查说明是否只服务未来约 30 章必要信息、是否仍像小说、镜头是否交给主角。非第一章检查章首承接和换景因果。额外检查陌生世界信息是否通过故事和具体命运进入、是否连续堆出陌生名词、是否把已经成立的规则重新介绍。准确不等于术语化。不得把普通章节擅自改成宏观开场。",
    ),
    "specialist_dialogue": _specialist_prompt_template(
        "Dialogue & Character Voice Agent",
        "检查核心角色声音是否可区分；对话是否改变信息、关系、决定或行动；是否有同质化、纯说明式对白、缺乏潜台词/拒绝/回避/立场；人物是否说普通人会说的话，专业词是否有现场上下文，是否有人像策划文档一样背诵设定。不得改变主要事件和人物决定。",
    ),
    "specialist_action": _specialist_prompt_template(
        "Action & Spatial Logic Agent",
        "检查动作方向、位置、对象和结果；人物与物品是否无故出现或消失；调查、追逐、操作和空间移动是否连贯；世界规则是否通过行动产生后果；是否遗漏改变局面的关键动作。准确不等于术语化；能用方向词、接触词和结果词说清楚时，不建议新增机械名称。不得把正文改成战术说明书。",
    ),
    "specialist_emotion": _specialist_prompt_template(
        "Emotion & Aftermath Agent",
        "检查重大行动、胜利、失败和关系变化的真实余波；情绪是否通过动作、选择、沉默或感官进入；配角是否只有功能反应；payoff 后是否缺少确认与新压力；是否重复解释情绪或用否定句证明旧边界。不得强制增加痛苦、悲剧代价或伦理惩罚。",
    ),
    "chapter_integrator": """你是透明协作的 Revision Integrator。Primary Draft 是唯一正文底稿。只接收有效局部 Patch；逐项判断它们是否真正改善正文，冲突、重复、改变事件结果、破坏人物声音或重新规划章节的建议必须拒绝。四类建议不必全部采纳，全部不采纳也是正常结果。保持 Primary Writer 的主要叙事声音，删除策划语言泄漏、同义重复解释和没有节拍变化的微段；不做第二轮全面审稿，不输出整章重写说明或内部推理。

固定输出格式：
# Writer Audit
报告正式正文字符数、实际采用的专项修改类型、未采用的冲突/无必要建议，以及实际 Canon / Plan 冲突或实质调整；没有时写：无。
# 正式正文
只输出最终整合后的正式小说正文；它必须以 Primary Draft 为底稿。
# 章节事实摘要
根据最终整合正文重新生成，只写最终正文已经成立的事实，不能机械复用 Primary Fact Summary。""",
}

DEFAULT_PROMPT_TEMPLATES.update(HYBRID_PROMPT_TEMPLATES)


FANTASY_SEED_TEMPLATE = f"""你是透明协作的 Fantasy Seed 创作助手。当前创作目标是成熟中文男频玄幻/修仙成长长篇；作者明确指定其他类型时，以作者要求为准。只读取作者粗方向、作者明确题材、作者明确要求保留的内容和作者明确禁止的内容。不要读取或提及任何其它资料。你的唯一问题是：这本书实际上最值得让读者幻想什么？

生成 3—5 个真正不同的候选。不评分、不排名、不自动选择。先写能力快感、力量占有欲和世界吸引力，再写持续阻力与长期升格；不要把创意先写成运行手册。

每个候选严格使用：

## 候选N：概念名

### 核心幻想
读者代入主角后，最想亲自拥有的能力、生命状态、行动空间、世界位置或实现的核心欲望是什么？

### 主角最强欲望
主角最想获得、夺回、摆脱、改变或超越什么？写出他会主动怎样追逐它。

### 力量占有欲
为什么读者会直接产生“我也想拥有这种能力”的欲望？写这种能力或生命状态的直接体验，以及第一次使用时的具体、可感知收益。如果该设定自然存在限制、风险、消耗或后果，再写出它们怎样服务玩法和剧情；不为平衡收益机械添加。

### 第一次标志性奇观
写一幅具体场面，代表这项能力与世界的吸引力。不要写组织图、流程图或制度说明。

### 持续阻力与压力
写什么力量、人物、环境、竞争、世界规则或其它因素持续阻挡主角，并说明它如何随故事尺度升级；具体的冲突方式由作品自身决定。

### 非对称优势
主角怎样靠独有能力、信息差、特殊资源、身份、血脉、规则位置或机会，获得明显不成比例、具体且可感知的实际收益？说明这项优势在长篇中如何继续发展、组合、变异或改变玩法。

### 第一次情绪兑现
说明前面的欲望或压力如何通过主角主动行动获得第一次兑现，核心幻想落地后主角的能力、处境、世界位置或核心欲望发生了什么可感知变化，以及主要情绪如何释放。

### 10章超越
主角本人在修为、战斗、神通、核心技艺、生命层次、规则掌控、行动能力或其它个人能力上第一次跨过什么过去不可触碰的界限？

### 30章超越
主角本人获得什么新的力量、生命状态、行动能力或世界通行能力？

### 100章超越
主角本人已经能做到什么开局时完全不可能的事？这次升格怎样改变后续玩法或世界尺度？

### 世界扩张欲望
为什么读者想跟随主角进入更高层世界？

不要输出成长整理、变量图、复杂网络、长期章节规划或完整能力限制。"""


WORLD_VISION_TEMPLATE = f"""你是透明协作的 World Vision 创作助手。当前创作目标是为成熟中文男频玄幻/修仙成长长篇承载核心幻想；作者明确指定其他类型时，以作者要求为准。只有作者已经明确批准 Fantasy Seed 时，才执行本 Prompt。只读取作者粗方向、已批准 Fantasy Seed 全文和作者额外说明，不读取其它资料。你的职责是说明世界怎样承载已批准的核心幻想，不重新发明核心幻想，也不把未知提前还原成单一解释。

最终严格输出：

# 世界幻想画像

## 核心幻想不变量
用 3—6 句说明无论后续怎样规划，本书必须持续给读者什么体验。

## 主角最强欲望
写主角真正想得到、摆脱、夺回、摧毁或超越什么。

## 主角身份与生命状态跃迁
开局是什么人，长期将成为什么存在？写主角本人在力量、寿命、行动能力、世界位置、核心欲望或命运状态上怎样变化，具体终局形式由已批准幻想、世界和长期剧情自然决定。

## 世界最震撼的三幅画面
分别体现核心规则、主角力量上限以及值得继续探索或改变的世界层面；三幅画面不必承担同一种功能。

## 世界核心规则与力量来源
说明普通人如何获得力量，以及力量、资源、血脉、知识、环境、身份、规则或其它因素怎样影响身体、生命状态、战斗能力、社会位置、行动范围或命运。让规则制造具体故事，不写成操作手册。

## 力量带来的直接体验
主角使用或获得核心能力时看见什么、感到什么、能做什么、过去做不到什么、第一次产生什么明确收益，以及外界怎样反应。

## 力量的升格方向
说明核心能力怎样从小尺度用途逐渐触及本书适合的强敌、大阵、山河、世界、生死、时间、因果、天道、法则或世界边界；写主角本人在能力、生命层次、战斗方式、核心技艺、规则掌控或行动空间上发生的真正变化。如果该力量自然存在上限、限制、风险、消耗或后果，再写出它们怎样服务玩法和剧情；不为平衡收益机械添加。

## 世界阶层、利益与行动压力
写力量、资源、身份、环境、规则、竞争或其它利益如何形成世界结构，并如何在不同阶段持续推动主角行动；具体动机和结果由人物与世界的处境自然呈现。

## 持续冲突来源
写足以持续推动主角行动和成长的具体阻力、敌人或世界压力，并说明它如何随故事尺度升级。来源可以是人物、竞争、利益冲突、环境、自然灾害、世界法则或其它设定，组合与比例由故事自然决定。

## 第一次决定性兑现
写主角第一次通过具体行动让核心幻想或非对称优势产生明确收益，并说明主角的能力、处境、世界位置或核心欲望如何因此改变，以及主要情绪如何释放。

## 10 / 30 / 100章超越阶梯
忠实展开 Fantasy Seed 中的三次超越，具体写主角本人在能力、生命层次、行动范围或其它一级成长上分别达到什么阶段。

## 神秘、未知与世界入口
说明读者最想继续探索什么，以及世界怎样打开新的行动空间；不要把所有未知提前解释完。

## 核心情绪与读者体验
写本书希望反复兑现的 1—3 种主要情绪或读者体验，具体由 Fantasy Seed、主角欲望和世界冲突决定。

World Vision 不要求在本阶段穷尽长期主线、完整能力限制、所有成本、成长整理或正文。"""


STORY_PROGRAM_TEMPLATE = f"""你是透明协作的 Story Program / 故事主线设计助手。只有 World Vision 已经由作者明确批准时，才基于已批准 Fantasy Seed 与 World Vision 生成一条由 5—7 个自然大型阶段组成的长期故事主线。你不能重新决定核心幻想、主角最强欲望、力量上限、标志性奇观或 10/30/100章超越。只读取作者粗方向、已批准 Fantasy Seed、已批准 World Vision 和作者手动选择的 Reference Programs；本阶段不读取其它灵感结果。

本阶段回答“这本书实际上如何展开”：以已批准的欲望、力量、行动、结果与变化组织主线，具体的冲突走向和终局形式由作品自身生长。

{DEFAULT_PRODUCT_DIRECTION}

先写总览，再严格使用以下结构：

## 世界观与故事主线

### 已批准幻想怎样落地
说明主线怎样忠实保留 Fantasy Seed 与 World Vision，并让核心幻想在行动和结果中持续出现。

### 主角与长期一级成长
写主角的开局状态、最强欲望、主动行动方式，以及十章、三十章、一百章时主角本人分别多能做什么。一级成长可以体现在修为、战斗、神通、核心技艺、生命层次、规则掌控、世界通行能力或其它真正属于主角本人的升格。

### 世界、力量与奇观
说明普通人如何获得力量，力量如何改变身体、生命状态、战斗能力、社会位置或行动范围，主角为什么不同，力量上限是什么，以及世界最值得继续探索的视觉奇观。

### 核心优势与长期玩法
说明主角的非对称优势、第一次使用时的具体收益，以及这项优势如何在长篇中继续发展、组合、变异或改变玩法，至少发生三次真正的玩法升格。

### 第一次完整兑现
说明第一次核心幻想兑现时的能力结果、具体收益、行动空间变化和主要情绪释放；外界反应或其它后果只在故事自然需要时写出。

### 世界结构与持续冲突
写世界的阶层、利益、环境、规则和行动压力，以及足以持续推动主角行动和成长的具体阻力、敌人或世界压力。来源可以是人物、竞争、利益冲突、环境、自然灾害、世界法则或其它设定，具体组合与推进方式由主线决定。

### 关键关系（可选）
只写确实对长期主线重要、并且有自身欲望和行动的人；没有必要时省略。

### 长期故事主线
生成 5—7 个自然衔接的大型阶段；阶段数量由这本书的因果和世界尺度决定，不为凑数拆分。每个阶段使用：

#### 阶段N：阶段名
开局状态：
主要事件与具体阻力：
主角主动行动：
主角一级成长：
核心幻想兑现：
主要情绪释放：
二级收益：写本阶段自然获得的资源、身份、关系、势力或世界入口，以及它们如何服务后续一级成长（如果本阶段有）。
世界扩张：
自然产生的后果或余波（如果有）：
推向下一阶段的压力或欲望：

### 十章、三十章、一百章成长阶梯
分别写主角本人在这些节点的能力、生命层次、行动空间或世界位置如何发生实质性变化，并与大型阶段保持因果连续。

### 继续探索的世界与未来场面
说明世界为什么值得继续探索，以及后续最令人期待的具体场面、能力兑现或世界扩张。

限制、风险、消耗或后果只在设定和剧情自然产生时写入相关阶段；没有就不补，不为平衡收益机械添加。不要输出新的核心幻想、复杂变量图、长期章节逐章计划或章节正文。"""


OUTLINE_TEMPLATE = f"""你是透明协作的故事 Outline 助手。生成前必须确认 Fantasy Seed、World Vision 和 Story Program 都已由作者明确批准；模型生成、模型选择、作者编辑和 legacy_unknown 都不是批准。已批准的三份创意产物高于产品默认模板，不能被静默改写。

{DEFAULT_PRODUCT_DIRECTION}

{DEFAULT_COMPOSABLE_GROWTH_DIRECTION}

{INTERNAL_REALISM_DIRECTION}

{PAYOFF_FIRST_COST_RHYTHM}

先忠实复现已批准的核心幻想、力量占有欲、主角欲望、世界奇观、不可调和压迫、决定性反转与 10/30/100章超越。不得把力量、长生、反杀、探索、超越或世界奇观重新解释成专业能力、职业资格、行业标准、公开试验、制度责任或组织治理。

最终只能使用以下四个一级标题：

# 小说总体设计画像
# 未来100章大型剧情块
# 未来十章逐章小纲
# 当前状态、未兑现承诺与作者备注

在总体设计画像下，先输出以下新的成长整理小节，再输出 1—12 个画像区块。Growth Genome 只整理已经批准的幻想，不选择核心幻想，不决定主角欲望，不决定每次收益必须有成本，也不决定故事必须制度化。

## 0. 本书成长基因图
### 已批准幻想不变量
忠实压缩 Fantasy Seed 与 World Vision，保留长期读者体验。
### 主角核心欲望与超越
主角长期想摆脱、夺回、获得或成为的东西，以及 10/30/100章超越。
### 一级成长主轴
主角本人越来越能做什么，写个人力量、战斗、神通、技艺、生命层次或规则掌控，不以职位、权限、组织规模替代。
### 核心优势阶段升格
至少说明三次真正改变力量层级、行动方式、战斗方式或世界关系的升格。
### 二级收益与反哺
说明财富、资源、身份、关系、势力和世界入口怎样服务一级成长。
### 主循环
只要求一个主循环；确有必要时才补辅助循环。
### 成本节奏
说明哪些阶段允许明显净收益，哪些关键节点成本用于制造选择，怎样防止每次 Payoff 被等量抵消。
### 核心不变量
只写 1—3 项长期读者体验。
### 退化风险
只写 1—3 项最真实的退化风险。

以下 1—12 区块服务于已批准幻想：
## 1. 核心类型与读者承诺
优先写核心幻想、力量占有欲、主角最强欲望、第一次决定性反转、10/30/100章超越和前中远期情绪兑现。
## 2. 世界观结构
说明最震撼的景象、最向往或恐惧的区域、力量怎样改变生命状态、主角成长后能进入什么过去不可触碰的地方，以及哪些未知无法只靠技术验证解决；如果本书需要且对当前故事重要，再补充空间/层级、权力关系和力量道路。
## 3. 世界如何持续制造剧情压力
从境界压制、血脉阶层、资源争夺、宗门垄断、王朝、神明、天道、异族、妖兽、秘境、战争、强敌、身份暴露或世界毁灭中选择真实需要的来源，也可以使用作者明确选择的制度矛盾；不得默认市场、认证、合同和审计占据主要位置。
## 4. 主角模型、人物弧与核心矛盾
回答主角不能忍受什么、渴望什么、愿意为何主动冒险、哪种胜利最让读者痛快，以及最终从什么人变成什么存在。
## 5. 配角与关系系统
允许崇拜、友情、师徒、竞争、嫉妒、恐惧、爱慕、忠诚、背叛和重新评价，不要求所有对手都有公共利益理由，不要求所有冲突互相理解。
## 6. 核心情节发动机
主循环首先回答主角如何主动使用优势，获得力量、资源、地位和更大的自由。试验、记录、复盘和准入只有本书真实需要时才出现。
## 7. 叙事结构
写视角、第一章开篇策略、场景与总结的比例，以及如何用他人反应展示地位变化。
## 8. 文风与可操作参数
写可执行的表达目标，不把它变成禁词表、固定句长或评分器。
## 9. 对话特点
写角色声音、潜台词、拒绝、回避、立场和对话如何改变现场。
## 10. 节奏结构
安排小爽点、中型兑现、阶段大兑现、余波与新压力的节拍，不要求每次高光立即抵消。
## 11. 主题、价值观与长期问题
让主题从实际行动和世界规则中自然浮现，不强制伦理惩罚。
## 12. 当前设计最强点与最弱点
只写当前最真实的 1—3 项风险，不生成机械风险清单。

未来 100 章写 4—8 个自然剧情块，完整覆盖第1章到第100章。完整输出所有剧情块，不能省略后面区块。每块严格使用：

## 第X—Y章：具体块名
具体发生：写人物、地点、事件、主角行动、敌人反应、转折与高潮。
核心幻想推进：读者在本块获得什么力量、自由、反转、探索或升格体验？
一级成长变化：主角本人真正多能做了什么？
主要情绪兑现：本块压抑了什么，最后怎样释放？
二级收益结算：获得什么资源、身份、关系、势力、领地或世界入口？
世界扩张：进入什么过去无法进入的地图、层级、秘密或敌人范围？
代价或余波（可选）：只有本块真实需要时才写，不得为了显得成熟强制制造等量损失。
推向下一块：哪个具体事件、新敌人或新入口导致下一块发生？

同一强主循环可以多次运行，只要能力、敌人、结果、情绪或世界尺度发生真实变化。不强制每块失去或承担什么，不强制负反馈、变量失效、新变量、公开验证、资格变化或不同转换路径。

未来十章开头先写批次说明：
本批核心幻想兑现：
本批一级成长目标：
本批第一次决定性反转：
本批实际净收益：
本批打开的新行动空间：
本批主要情绪颜色：

随后保留现有单章格式，连续列出十章：
## 第N章：具体标题
具体剧情：用 2—4 句写具体人物、事件和主角行动。
结果 / 状态变化：写直接结果和状态变化。
叙事功能：写本章在局部故事中的作用。
结尾推动：写下一章为什么发生。

这些批次说明不成为每章必填字段，十章内不要求每章都成长或结算。整批结束时明确回答主角真正多能做了什么、得到什么实际净收益、谁重新评价了主角、行动自由扩大到哪里、下一个更大世界入口是什么。

最后写故事开始前的初始状态、已经建立的远期承诺、当前未解决问题和作者备注。"""


REVIEW_TEMPLATE = f"""你是透明协作的十章 Review 助手。只根据作者提供的已发生正文摘要、当前状态、未兑现承诺、远期方向和当前设计，调整未来计划；Review 只用于调整未来，不自动重写或否定已完成正文。

{PAYOFF_FIRST_COST_RHYTHM}

## 核心幻想是否仍在兑现
最近章节是否仍然提供最初承诺的力量、自由、长生、探索、反杀、夺取、升格、关系或身份反转。

## 一级成长是否仍是主轴
主角本人是否真正多能做了什么，还是只增加职位、资格、权限、责任、组织规模或外界评价。

## 幻想盈余是否为正
检查是否每次胜利都被等量成本抵消、每次资格都增加更重责任、每次高光都立即被三种限制削弱、长期净收益过低。

## 冲突是否过度理性化
检查是否所有反派都是合理利益方、所有高潮都靠公开验证、所有冲突都靠承认不足，以及是否仍有击败、夺取、逃脱、拒绝、摧毁或决定性反转。

## 世界是否被程序化
检查是否退化为行业认证、技术质检、项目管理、合规审查、行政协调、职业晋升或学术实验。

以上只用于调整未来计划，不自动改写已完成正文。

随后输出：
1. 实际完成内容；
2. 最近兑现与未兑现的问题；
3. 下一批十章总体事件链；
4. 下一批十章逐章小纲。

## 下一批十章总体事件链
用 3—6 句话说明起点、问题、主角行动、转折、第十章左右的具体兑现和新入口，并写出本批核心幻想兑现、本批一级成长目标、本批实际净收益、本批打开的新行动空间和本批主要情绪颜色。

逐章使用：
## 第N章：具体标题
具体剧情：用 2—4 句写具体人物、事件和主角行动。
结果 / 状态变化：写直接结果和状态变化。
叙事功能：写本章在局部故事中的作用。
结尾推动：写下一章为什么发生。

十章必须连续；第N章的结尾推动必须成为第N+1章具体剧情的直接因果起点；不要求每章都成长或结算。结尾补充：主角真正多能做了什么、得到什么实际净收益、谁重新评价了主角、行动自由扩大到哪里、下一个更大世界入口是什么。"""


DEFAULT_PROMPT_TEMPLATES.update({
    "fantasy_seed": FANTASY_SEED_TEMPLATE,
    "world_vision": WORLD_VISION_TEMPLATE,
    "idea": STORY_PROGRAM_TEMPLATE,
    "outline": OUTLINE_TEMPLATE,
    "review": REVIEW_TEMPLATE,
})

HYBRID_PROMPT_MODES = frozenset(HYBRID_PROMPT_TEMPLATES)
SPECIALIST_PROMPT_MODES = frozenset(
    {f"specialist_{name}" for name in ("opening", "dialogue", "action", "emotion")}
)


#: state_delta 模式的内置模板（页面不提供可编辑模板；为空时由 generate_prompt 自动使用）。
#: 职责限定为书记员：只根据正式正文更新状态区提案；不检查 BOOK CONTRACT，不是章节门禁。
DEFAULT_STATE_DELTA_TEMPLATE = """你是透明协作的 State Delta 书记员。只根据下方当前章节编号、当前规范化 CANON INDEX、本次新提取的正式正文和 Writer 章节事实摘要，生成 BOOK 状态区的完整替换提案，不调用任何外部服务。

本次正式正文是 State Delta 的最高事实来源；Writer 章节事实摘要仅作辅助，冲突时以正式正文为准。AUTHOR NOTES 是作者元控制，不属于 Canon 事实，必须原样保留。

你不检查、也不报告 BOOK CONTRACT 或任何长期设计的状态；BOOK CONTRACT、完整百章计划、十章计划、prose profile、GBrain、Reference Programs 与前两章正文都不在本次输入中，不要猜测它们。

最终返回必须使用以下五个一级标题；缺少任一标题只阻止 State Delta 应用，不阻止章节保存：

# State Delta Audit
只报告实际存在的事项：
- 本次正式正文与旧 CANON INDEX 的冲突；
- 无法从正式正文确定的状态。
没有时写：无需要报告的状态冲突或不确定项。

# Proposed Active Scene State
输出下一章立即需要的完整 Active Scene State：当前地点、在场人物、即时伤势、手中关键物品、当前敌人或追兵、当前倒计时、下一步直接目标。下一章可以整体替换旧 Active Scene State。

# Proposed Persistent Canon
输出更新后的、简短的长期 Persistent Canon：已证明能力、能力限制、关系阶段、持久资源、长期身份、确认知识、长期伤势和重要敌我状态。只保留仍会影响未来章节的信息。不要把本章暂时位置或追兵重复写成长期开关。

# Proposed Chapter Summary
只输出本章一个事实摘要；摘要必须来自正式正文，不复制 Writer Audit，不把计划写成事实。

# Proposed Open Promises
输出更新后的未兑现承诺列表：保留仍有效的旧承诺，新增正文真实建立的新承诺，删除或标记已兑现/失败/失效的承诺；不要把普通悬念升级为长期承诺。

不要输出 AUTHOR NOTES。AUTHOR NOTES 由代码逐字保留；如果模型返回任何 `# AUTHOR NOTES` 或 `## AUTHOR NOTES` 标题，应用时显示明确错误并完全不应用。
作者备注：（原样保留旧 AUTHOR NOTES，不得增删改写）。各字段内容行不得以旧格式标签开头；AUTHOR NOTES 仍由代码保留。

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


CANON_MEMORY_FIELDS = (
    "active_scene_state",
    "persistent_canon",
    "recent_summaries",
    "open_promises",
    "author_notes",
)

_CANON_MEMORY_HEADINGS = (
    ("## ACTIVE SCENE STATE", "active_scene_state"),
    ("## PERSISTENT CANON", "persistent_canon"),
    ("## RECENT SUMMARIES", "recent_summaries"),
    ("## OPEN PROMISES", "open_promises"),
    ("## AUTHOR NOTES", "author_notes"),
)


def canon_memory_has_labels(status_text: str) -> bool:
    """返回状态区是否已经使用 Canon Memory v2 的五个固定二级标题。"""

    headings = {heading for heading, _ in _CANON_MEMORY_HEADINGS}
    return any(line.strip() in headings for line in status_text.splitlines())


def parse_canon_memory(status_text: str) -> dict[str, str]:
    """解析 Canon Memory v2；旧状态区只把旧「当前状态」映射为 Persistent Canon。

    这是一次确定性读取投影，不创建迁移文件，也不修改输入。完成章节行单独保留在
    ``completed_chapter``，供调用方在写回时避免重复；它不是新的 Canon 字段。
    """

    fields = {key: "" for key in CANON_MEMORY_FIELDS}
    completed: list[str] = []
    heading_map = dict(_CANON_MEMORY_HEADINGS)
    current_key: str | None = None
    for raw_line in status_text.splitlines():
        stripped = raw_line.strip()
        if _CANON_COMPLETED_CHAPTER_PATTERN.match(stripped):
            completed.append(stripped)
            continue
        if stripped in heading_map:
            current_key = heading_map[stripped]
            continue
        if current_key is not None:
            fields[current_key] = (
                f"{fields[current_key]}\n{raw_line}" if fields[current_key] else raw_line
            ).strip()
    if canon_memory_has_labels(status_text):
        fields["completed_chapter"] = completed[-1] if completed else ""
        return fields

    legacy = parse_canon_index(status_text)
    fields["persistent_canon"] = legacy["current_state"]
    fields["recent_summaries"] = legacy["recent_summaries"]
    fields["open_promises"] = legacy["open_promises"]
    fields["author_notes"] = legacy["author_notes"]
    fields["completed_chapter"] = ""
    if legacy["current_state"]:
        match = _CANON_COMPLETED_CHAPTER_PATTERN.search(legacy["current_state"])
        if match:
            fields["completed_chapter"] = match.group(0)
            fields["persistent_canon"] = legacy["current_state"][match.end():].strip()
    return fields


def render_canon_memory(
    fields: Mapping[str, str], *, page_recent_summaries: str = ""
) -> str:
    """渲染给章节节点的 Canon Memory v2 轻量投影。"""

    recent = page_recent_summaries.strip() or fields.get("recent_summaries", "").strip()
    completed = fields.get("completed_chapter", "").strip()
    blocks = []
    if completed:
        blocks.append(completed)
    values = (
        ("ACTIVE SCENE STATE", fields.get("active_scene_state", "")),
        ("PERSISTENT CANON", fields.get("persistent_canon", "")),
        ("RECENT SUMMARIES", recent),
        ("OPEN PROMISES", fields.get("open_promises", "")),
        (
            "AUTHOR NOTES（作者元控制；不属于 Canon 事实；State Delta 不得自动修改或删除）",
            fields.get("author_notes", ""),
        ),
    )
    blocks.extend(
        f"## {heading}：\n{value.strip() or '（未填写）'}" for heading, value in values
    )
    return "\n\n".join(blocks)


STATE_DELTA_V2_HEADINGS = (
    "# State Delta Audit",
    "# Proposed Active Scene State",
    "# Proposed Persistent Canon",
    "# Proposed Chapter Summary",
    "# Proposed Open Promises",
)


def parse_state_delta_v2(response: str) -> dict[str, str]:
    """解析 State Delta v2 提案；缺标题或模型输出 AUTHOR NOTES 时直接失败。"""

    if re.search(r"^#{1,2}\s+AUTHOR NOTES\s*$", response, flags=re.MULTILINE):
        raise ValueError("State Delta 返回不得包含 AUTHOR NOTES；旧 AUTHOR NOTES 必须由代码保留")
    mapping = {
        "# State Delta Audit": "audit",
        "# Proposed Active Scene State": "active_scene_state",
        "# Proposed Persistent Canon": "persistent_canon",
        "# Proposed Chapter Summary": "chapter_summary",
        "# Proposed Open Promises": "open_promises",
    }
    lines = response.splitlines()
    result: dict[str, str] = {}
    for index, line in enumerate(lines):
        key = mapping.get(line.strip())
        if not key:
            continue
        collected: list[str] = []
        for next_line in lines[index + 1 :]:
            if next_line.startswith("# "):
                break
            collected.append(next_line)
        result[key] = "\n".join(collected).strip()
    missing = [key for key in mapping.values() if not result.get(key)]
    if missing:
        raise ValueError("State Delta 缺少必要标题或内容：" + "、".join(missing))
    return result


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
    def __init__(self, missing_fields: list[str], message: str | None = None) -> None:
        self.missing_fields = missing_fields
        super().__init__(message or ("当前章小纲缺少非空字段：" + "、".join(missing_fields)))


class CreativeApprovalError(HardGateError):
    def __init__(self, missing_artifacts: list[str]) -> None:
        self.missing_artifacts = missing_artifacts
        labels = {
            "fantasy_seed": "Fantasy Seed",
            "world_vision": "World Vision",
            "proposal": "Story Program",
        }
        detail = "、".join(labels[item] for item in missing_artifacts)
        message = (
            f"当前{detail}尚未由作者明确批准。模型生成或模型选择不等于作者批准。"
            if len(missing_artifacts) == 1
            else f"以下创意产物尚未由作者明确批准：{detail}。模型生成或模型选择不等于作者批准。"
        )
        super().__init__(
            missing_artifacts,
            message,
        )


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
    fantasy_seed: str = "",
    world_vision: str = "",
    creative_state: Mapping[str, Any] | None = None,
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
    writer_mode: str = "hybrid_selective",
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
    state = creative_state or {}
    required_approvals = {
        "world_vision": ["fantasy_seed"],
        "idea": ["world_vision"],
        "outline": ["fantasy_seed", "world_vision", "proposal"],
    }.get(mode, [])
    missing_approvals = [
        artifact
        for artifact in required_approvals
        if not isinstance(state.get(artifact), Mapping)
        or state[artifact].get("status") != "author_approved"
    ]
    if missing_approvals:
        raise CreativeApprovalError(missing_approvals)
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
    elif mode == "director" and not prompt_template:
        prompt_template = DEFAULT_DIRECTOR_TEMPLATE
    elif mode in {"fantasy_seed", "world_vision", "idea", "outline", "review"} and not prompt_template:
        prompt_template = DEFAULT_PROMPT_TEMPLATES[mode]
    stripped_legacy_writer = False
    if mode == "chapter":
        prompt_template, stripped_legacy_writer = sanitize_chapter_template(template)
    elif mode == "state_delta" and not prompt_template:
        prompt_template = DEFAULT_STATE_DELTA_TEMPLATE
    parts = [prompt_template, ""]
    if mode == "director":
        from .chapter_context import build_chapter_context, build_director_context

        packet = build_chapter_context(
            book_content=book_content,
            current_long_block=current_long_block,
            previous_chapter_text=previous_chapter_text,
            current_outline=current_outline,
            current_chapter_plan=current_chapter_plan,
            recent_summaries=recent_summaries,
            gbrain_inspiration="",
            selected_references=[],
        )
        context = build_director_context(
            packet,
            recent_summaries=recent_summaries,
            author_intent=creative_direction,
        )
        parts.append("# Director Context")
        parts.extend(
            [
                _input_block("当前大型剧情块（压缩摘要）", context.current_long_block),
                _input_block("当前章十章计划条目", context.current_chapter_plan),
                _input_block("compact Growth Genome", context.growth_genome_compact),
                _input_block("当前 Canon Index", context.canon_index),
                _input_block("最近一章摘要", context.recent_summary),
                _input_block("前文章末必要衔接", context.transition_context),
                _input_block("作者当前章意图", context.author_intent),
            ]
        )
    elif mode == "chapter":
        if stripped_legacy_writer:
            parts.append(SINGLE_WRITER_RUNTIME_NOTE)
        parts.extend(["# Story MVP Prose Realization Contract", PROSE_REALIZATION_CONTRACT])
        # 惰性导入：chapter_context 顶层依赖本模块，模块级互相导入会构成循环导入。
        from .chapter_context import build_chapter_context
        from .hybrid_runtime import compact_book_contract_for_chapter

        packet = build_chapter_context(
            book_content=book_content,
            current_long_block=current_long_block,
            previous_chapter_text=previous_chapter_text,
            current_outline=current_outline,
            current_chapter_plan=current_chapter_plan,
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
            _annotated_block(
                BOOK_CONTRACT_BLOCK_NOTE,
                compact_book_contract_for_chapter(
                    packet.book_contract, packet.growth_genome_compact
                ),
            ),
        ))
        parts.append(_input_block("CHAPTER MISSION——本章事件合同（PLAN）", packet.chapter_mission))
        parts.append(_input_block("本章成长收益短投影（非门禁）", packet.growth_benefit_projection))
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
            drop_growth_hierarchy,
            extract_primary_prose_context,
        )

        packet = build_chapter_context(
            book_content=book_content,
            current_long_block=current_long_block,
            previous_chapter_text=previous_chapter_text,
            current_outline=current_outline,
            current_chapter_plan=current_chapter_plan,
            recent_summaries=recent_summaries,
            gbrain_inspiration=gbrain_inspiration,
            selected_references=selected_references,
        )
        parts.append(f"# Hybrid Runtime\n\nwriter_mode: {writer_mode}")
        if mode in SPECIALIST_PROMPT_MODES or mode in {"primary_writer", "chapter_integrator"}:
            contract = READER_FIRST_PROSE_SHORT if mode == "chapter_integrator" else READER_FIRST_PROSE_CONTRACT
            parts.extend(["# Reader-First Prose Contract", contract])
        if mode == "context_curator":
            context = build_curator_context(packet)
            parts.extend(
                [
                    _input_block("AUTHORITY", context.authority),
                    _input_block("当前章事件合同", context.chapter_mission),
                    _input_block("压缩 Growth Genome（本章相关固定小节）", context.growth_genome_compact),
                    _input_block("BOOK CONTRACT", context.book_contract),
                    _input_block("本章成长收益短投影（非长期理论）", context.growth_benefit_projection),
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
            primary_prose = extract_primary_prose_context(packet.recent_prose)
            parts.extend(
                [
                    _input_block("AUTHORITY", packet.authority),
                    _input_block("Chapter Mission——当前章事件合同", packet.chapter_mission),
                    _input_block("CANON PROSE——上一章全文与上上章必要章末", primary_prose),
                    _input_block("CANON INDEX——规范化已发生事实索引", packet.canon_context),
                    _input_block("本章成长收益短投影（非长期理论）", packet.growth_benefit_projection),
                    _input_block(
                        "Curated Chapter Context" if not fallback else "Curated Chapter Context（缺失时的显式 fallback）",
                        curated or "Curator 未提供，使用完整上下文 fallback：\n\n"
                        + drop_growth_hierarchy(packet.book_contract)
                        + "\n\n"
                        + packet.chapter_plan_context
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
                    _input_block("本章成长收益短投影（非长期理论）", context.growth_benefit_projection),
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
                    _input_block("CANON INDEX", context.canon_index),
                    _input_block("Primary Draft——唯一正文底稿", context.primary_draft),
                    _input_block("本章成长收益短投影（非长期理论）", context.growth_benefit_projection),
                    _input_block("Opening Specialist Response", context.specialist_responses["opening"]),
                    _input_block("Dialogue Specialist Response", context.specialist_responses["dialogue"]),
                    _input_block("Action Specialist Response", context.specialist_responses["action"]),
                    _input_block("Emotion Specialist Response", context.specialist_responses["emotion"]),
                ]
            )
    elif mode == "chapter_prep":
        from .chapter_context import render_growth_benefit_projection

        parts.append("# 页面当前输入")
        parts.append(_input_block("本书执行相关画像", _chapter_book_context(book_content)))
        parts.append(_input_block("当前大型剧情块", current_long_block))
        parts.append(_input_block("当前章对应的十章计划条目", current_chapter_plan))
        parts.append(_input_block(
            "本章成长收益短投影（非第九字段）",
            render_growth_benefit_projection(
                current_long_block=current_long_block,
                current_chapter_plan=current_chapter_plan,
                current_outline=current_outline,
            ),
        ))
        parts.append(_input_block("前两章正文（连续性上下文）", previous_chapter_text))
        status_block = _extract_markdown_block(book_content, CURRENT_STATE_HEADING)
        if canon_memory_has_labels(status_block):
            status_display = render_canon_memory(
                parse_canon_memory(status_block), page_recent_summaries=recent_summaries
            )
            summary_rendered = True
        elif recent_summaries.strip() and canon_index_has_labels(status_block):
            # 页面显式摘要非空时，扣除标签化状态区内嵌的最近章节摘要段，
            # 避免同一 Prompt 出现两份摘要；页面摘要为空时保持注入 BOOK 内摘要。
            status_display = _render_canon_status_without_summaries(status_block)
            summary_rendered = False
        else:
            status_display = status_block
            summary_rendered = False
        if not summary_rendered:
            parts.append(_input_block("最近 1—3 章摘要", recent_summaries))
        parts.append(_input_block("当前状态", status_display))
    elif mode == "state_delta":
        # State Delta 只注入四组输入；默认不注入完整 BOOK CONTRACT、完整百章计划、
        # GBrain、Reference Programs、prose profile 或前两章完整正文。
        status_block = _extract_markdown_block(book_content, CURRENT_STATE_HEADING)
        if canon_memory_has_labels(status_block):
            canon_index = render_canon_memory(
                parse_canon_memory(status_block), page_recent_summaries=recent_summaries
            )
        elif canon_index_has_labels(status_block):
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
        if status_block and not canon_memory_has_labels(status_block):
            canon_index = (
                f"{canon_index}\n\n旧格式历史标题（仅用于识别旧状态区，不得输出或应用）："
                "# Proposed Canon Index"
            )
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
    elif mode in {"fantasy_seed", "world_vision", "idea", "outline", "review"}:
        parts.append("# 页面当前输入")
        if mode == "fantasy_seed":
            parts.append(_input_block("作者粗方向与明确约束", creative_direction))
        elif mode == "world_vision":
            parts.append(_input_block("作者粗方向与额外说明", creative_direction))
            parts.append(_input_block("已批准 Fantasy Seed", fantasy_seed))
        elif mode == "idea":
            parts.append(_input_block("作者粗方向", creative_direction))
            parts.append(_input_block("已批准 Fantasy Seed", fantasy_seed))
            parts.append(_input_block("已批准 World Vision", world_vision))
            parts.append(_input_block("手动选择的 Reference Programs", format_references(selected_references or [])))
        elif mode == "outline":
            parts.append(_input_block("作者粗方向", creative_direction))
            parts.append(_input_block("已批准 Fantasy Seed", fantasy_seed))
            parts.append(_input_block("已批准 World Vision", world_vision))
            parts.append(_input_block("作者已批准的 Story Program", proposal_context))
            parts.append(_input_block("当前 BOOK.md（只作为已批准创意的承载草稿）", book_content))
            parts.append(_input_block("手动选择的 Reference Programs", format_references(selected_references or [])))
            parts.append(_input_block("GBrain Inspiration Results（可选，不能覆盖批准产物）", gbrain_inspiration))
        else:
            parts.append(_input_block("当前设计与原计划", book_content))
            parts.append(_input_block("创作方向", creative_direction))
            parts.append(_input_block("实际十章摘要", actual_summaries))
            parts.append(_input_block("当前状态", current_state))
            parts.append(_input_block("未兑现承诺", unfulfilled_promises))
            parts.append(_input_block("尚未发生的远期方向", future_direction))
            parts.append(_input_block("当前成长整理", _extract_markdown_block(book_content, "## 0. 本书成长基因图")))
            parts.append(_input_block("GBrain Inspiration Results（可选）", gbrain_inspiration))
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
