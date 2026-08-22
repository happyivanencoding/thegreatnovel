"""只为本隔离实验渲染冻结上下文和四个待调用 prompt。

脚本只读现有生产/实验输入，只写本目录；不导入或修改 Run Ledger、BOOK、Canon 或生产 Prompt。
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "books" / "real-exp-curator-primary-longform-v1" / "candidate-b"
OUT = ROOT / "books" / "real-exp-prologue-character-opening-v1"


def read(relative: str) -> str:
    return (SOURCE / relative).read_text(encoding="utf-8").strip()


def h2(text: str, title: str) -> str:
    pattern = rf"(?ms)^##\s+{re.escape(title)}\s*$\n(.*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text)
    return f"## {title}\n\n{match.group(1).strip()}" if match else ""


def h1(text: str, title: str) -> str:
    pattern = rf"(?ms)^#\s+{re.escape(title)}\s*$\n(.*?)(?=^#\s+|\Z)"
    match = re.search(pattern, text)
    return f"# {title}\n\n{match.group(1).strip()}" if match else ""


def write(name: str, content: str) -> None:
    (OUT / name).write_text(content.strip() + "\n", encoding="utf-8")


def artifact(name: str, pending: str) -> str:
    path = OUT / name
    return path.read_text(encoding="utf-8").strip() if path.is_file() else pending


fantasy = read("source/fantasy_seed.md")
world = read("source/world_vision.md")
program = read("source/story_program.md")
book = read("source/BOOK_after_old_experiment.md")
outline = read("source/frozen_outline.md")
fact_summary = read("_operation/chapter-0001/chapter_fact_summary.md")

book_design = book.split("\n# 当前中期规划窗口", 1)[0].strip()
outline_design = outline.split("\n# 当前中期规划窗口", 1)[0].strip()
outline_window = h1(outline, "当前中期规划窗口")
future10 = h1(outline, "未来十章逐章小纲")

world_context = "\n\n".join(
    block
    for block in (
        h2(world, "核心幻想不变量"),
        h2(world, "主角最强欲望"),
        h2(world, "主角身份与生命状态跃迁"),
        h2(world, "世界核心规则与力量来源"),
        h2(world, "力量带来的直接体验"),
        h2(world, "世界资源、利益与机会结构"),
        h2(world, "持续冲突来源"),
        h2(world, "第一次决定性兑现"),
        h2(world, "早期成长锚点与长期升格"),
    )
    if block
)

program_context = "\n\n".join(
    block
    for block in (
        h2(program, "世界观与故事主线"),
        h2(program, "主角与长期一级成长"),
        h2(program, "世界、力量与奇观"),
        h2(program, "核心优势与长期玩法"),
        h2(program, "第一次完整兑现"),
        h2(program, "世界结构与持续冲突"),
        h2(program, "关键关系"),
        h2(program, "早期锚点、中期里程碑与远期升格"),
    )
    if block
)

context = f"""# 冻结创作上下文（仅供本隔离实验）

以下材料来自 `SOURCE_MANIFEST.json` 指定的冻结树。它们是同一部作品的设计事实，不是本轮要重新设计的题目。

## Fantasy Seed

{fantasy}

## World Vision：本轮相关切片

{world_context}

## Story Program：本轮相关切片

{program_context}

## BOOK：设计画像（不读取旧实验运行状态）

{book_design}

## Outline：设计画像切片

{outline_design}

## Outline：当前中期规划窗口

{outline_window}

## Outline：Future 10

{future10}

## 冻结的 Chapter 1 现实结果

本轮不得减少或改写下列结果：

{fact_summary}

## 本轮表达实验边界

- 序章只把世界尺度收束到黑炉镇和三天倒计时，不兑现核心能力。
- Chapter 1 假定读者读过序章，不重新完整讲灵脉、玄烬仙宗或封炉制度。
- Chapter 1 必须从具体人物问题进入，并在本章内完成断镐开出生路的真实结果。
- 能力第一次使用时“操作清楚、原理神秘”：读者要明白断镐留下的一下被沈燧借来，帮助他把矿壁凿开；不要求解释来源、上限或终极规则。
- 不生成 Chapter 2—10，不提前兑现裂路器、炉窟完整体系或更远世界。
- 只允许使用既有事实、既有角色和既有名词；不添加新的体系、敌人、地图或能力。
"""
write("FROZEN_CONTEXT.md", context)

prologue_prompt = f"""你是《炉藏万象》“可选序章 → 人物型第一章”隔离实验的序章正文调用。

请先阅读本目录的 `FROZEN_CONTEXT.md`。它是冻结输入；不要重新设计故事，不要修改其中事实。

## 任务

只写一篇独立序章正文，不写章节编号，不写内部说明，不写作者评语。序章承担四个最低限度的读者认知任务：

1. 用具体景象和后果让读者知道这个世界为什么依赖灵脉 / 炉火；
2. 让读者看见玄烬仙宗为什么拥有决定矿镇生死的力量；
3. 让“封炉”落到一个普通矿镇的实际后果；
4. 把镜头收束到黑炉镇，并明确这里三天后要被封掉。

## 叙事边界

- 采用“世界尺度 → 当前大秩序 / 力量结构 → 地域 → 黑炉镇”的收束，但必须像小说，不像百科或设定说明。
- 优先写炉火熄灭、矿镇被列入废弃、令下达、人开始搬东西、已有炉子提前冷掉等可见后果。
- 可以点到裴照川和黑炉镇，但不要让沈燧承担本序章的主角建立任务。
- 只解释普通读者读完序章所需的最少规则；不要展开完整炼器体系、炉权职级、残器分类、核心能力来源、炉心 / 炉城 / 古战场体系。
- 不写塌方，不写断镐，不写核心能力兑现，不写 Chapter 1 的行动。
- 结尾停在黑炉镇三天后封炉的确定性上，然后停止，不追加追兵或新谜团。

## 表达方向

清楚 > 顺畅 > 有画面 > 文学感。使用朴素、直接、普通中文男频读者正常速度能够理解的句子；减少纯隐喻和连续排除式表达。具体景象、具体后果优先于完整解释。

输出只允许是序章正文。

## 冻结上下文

{context}
"""
write("prologue_prompt.md", prologue_prompt)

prologue = artifact("PROLOGUE.md", "（序章 response 尚未冻结；本阶段只渲染序章 prompt。）")

director_prompt = f"""你是《炉藏万象》隔离实验中的 Chapter 1 Director。

请阅读本目录的 `FROZEN_CONTEXT.md` 与 `PROLOGUE.md`。序章已经冻结；你现在只为人物型 Chapter 1 生成执行合同，不写正式正文。

## 实验目的

序章已经承担世界认知。Chapter 1 不再重新解释“为什么炉火重要、玄烬仙宗是什么、封炉总体意味着什么”，除非当前人物行动只需要一句局部提醒。请把第一章的读者认知顺序固定为：人 → 问题 → 后果 → 行动 → 异常 → 能力最简单的当前理解 → 主角利用它 → 结果。

## 必须保留的现实结果

本章仍需完成冻结事实摘要中的完整早兑现：沈燧面对矿镇最后一次开采 / 塌方造成的生死问题，正常办法无法救出人；他触到断镐，借到其中尚未完成的“凿开一条让人活着出去的路”，实际打开矿壁和生路；矿工与伤者活着撤出；沈燧留下黑铁锋片与身体痕迹；在场人重新按他的判断行动；裴照川把异常列入回收并把镜头推到被封存的废弃炼器窟。不要把这次结果推迟到 Chapter 2。

## 输出格式

只输出以下八个字段，字段必须具体；不要输出正文、评分或内部推理：

触发事件：
推动事件的人：
主角行动：
对手或世界反应：
直接结果：
状态变化：
叙事功能：
结尾推动力：

在“主角行动”和“直接结果”中，写清正常办法为什么不行、沈燧为什么作决定、断镐操作如何发生、风险是什么、谁因此活下来。不要安排新的核心能力、裂路器完成、炉窟体系展开或 Chapter 2—10 内容。

## 已冻结序章

{prologue}

## 冻结上下文

{context}
"""
if (OUT / "PROLOGUE.md").is_file():
    write("chapter-0001_director_prompt.md", director_prompt)

director_response = artifact("chapter-0001_director_response.md", "（Director response 尚未冻结；本阶段只渲染前置 prompt。）")
curator_prompt = f"""你是《炉藏万象》隔离实验中的 Chapter 1 Curator。

请阅读 `FROZEN_CONTEXT.md`、`PROLOGUE.md` 和 `chapter-0001_director_response.md`。Director 合同已经冻结；你只做一次受控的信息压缩，供 Primary Writer 使用，不重新规划故事，不写正式正文，不做文学评分。

## 压缩目标

把宏观世界认知留在序章，把第一章的写作上下文压缩到人物和行动：沈燧是谁、管事 / 矿工要求他做什么、失败后谁会死或被封在里面、为什么普通纳灵 / 搬运 / 主井不能解决、他看见了什么、断镐的一下如何操作、使用风险、实际逃生结果、社会反馈、黑铁锋片、裴照川的回收反应和废弃炼器窟钩子。

## 强制保留

- 不得把“感知残响”变成只有谜语或准备尝试；Chapter 1 必须真正完成开路。
- 读者第一次读完要大致明白：断掉的工具里还留着最后没完成的一下，沈燧能让这一下继续；不必知道原理和终极来源。
- 结果之后先有短暂落点：谁活下来、别人如何重新看沈燧、沈燧确认了什么、下一步为什么只能走向废窟。
- 压缩普通搬运、重复工程细节和已没有新信息的伤势复述。
- 不添加新人物、新能力、新术语、新地图、新制度，不提前写 Chapter 2—10。

## 输出格式

只输出以下分区，不写正文，不写评分：

### 人物与当前问题
### 最低必要世界信息
### 场景与因果顺序
### 能力第一次使用：操作清楚、原理神秘
### 需要详细展开
### 可以压缩
### 结果、反馈与短落点
### 必须避免的退化

## Director 合同

{director_response}

## 序章

{prologue}

## 冻结上下文

{context}
"""
if (OUT / "chapter-0001_director_response.md").is_file():
    write("chapter-0001_curator_prompt.md", curator_prompt)

curator_response = artifact("chapter-0001_curator_response.md", "（Curator response 尚未冻结；本阶段只渲染前置 prompt。）")
primary_prompt = f"""你是《炉藏万象》隔离实验中的 Chapter 1 Primary Writer。

请阅读 `FROZEN_CONTEXT.md`、`PROLOGUE.md`、`chapter-0001_director_response.md` 和 `chapter-0001_curator_response.md`。这些输入已经冻结；不要重新设计故事，不要把旧 Hybrid Chapter 1 正文当作改写底稿。

## 写作任务

在序章之后直接写一个人物型 Chapter 1。读者已经知道炉火、玄烬仙宗和封炉的宏观背景，所以正文尽快进入：沈燧是谁、别人现在要求他做什么、他为什么弱势、失败的具体后果、他必须作出的决定。

正文必须完整走完：具体人物 → 现实问题 → 失败后果 → 主角行动 → 异常 → 能力最简单的当前理解 → 主角利用 → 真实结果 → 人物 / 社会反馈 → 短暂落点 → 明确下一章推动。

## 必须兑现且不能推迟

这一章仍然必须让核心优势产生一次真实、不可替代的现实结果：沈燧触摸折断采矿镐，借到镐中尚未完成的凿路动作，把这一下送入封死的矿壁，打开让矿工和伤者活着通过的生路。不能停在感知、发现、准备尝试或“下章再试”。

第一次能力只需达到“操作清楚，原理神秘”：读者应自然理解刚才发生了什么、沈燧现在大概能做什么、为什么断镐帮助了这次凿路；不要解释它来自器物、旧主人、残魂或更高规则，也不要一次列出能力上限。

## 选择性展开

详细写：正常办法为什么不行；沈燧观察到的关键物件 / 空间限制；他为什么不抛下伤者；断镐动作如何进入身体和矿壁；使用风险与身体后果；石梁 / 裂口 / 人员通过的关键变化；矿工如何因结果改变对他的判断；沈燧确认掌心黑铁锋片；裴照川如何把异常列入回收；废弃炼器窟为什么成为下一步。

压缩：普通搬运的重复站位；每块石头移动；左右几尺的持续维护；每条裂纹发展；没有新信息的工程过程和伤势重复。

## 章末落点

开出生路后先让读者知道谁活下来了、现场的人怎么看沈燧、沈燧实际得到 / 确认了什么，再以既有的裴照川回收压力和废弃炼器窟作一个明确而克制的下一章入口。不要连续叠加新追兵、新阵法、新能力、新地图和新术语；不要提前结算裂路器或炉窟完整体系。

## 表达方向

清楚 > 顺畅 > 有画面 > 文学感。朴素、直接、普通中文男频读者正常速度能够理解；具体动作和后果优先；减少“它 / 那个东西 / 某种东西 / 没有完成的什么”等需要猜测的指代；减少连续排除式句法，但不机械禁用。不要百科式重复序章，不要炫技，不模仿任何来源作者。

## 输出格式

必须只输出以下三个一级标题：

# Writer Audit

只写少量结构性说明，不打分，不写内部推理。

# 正式正文

这里只写 Chapter 1 正文，不放事实摘要、prompt、审计或括号说明。

# 章节事实摘要

只列本章已经发生的事实、状态变化和结尾推动，不引入未来事实。

## Director 合同

{director_response}

## Curator 压缩上下文

{curator_response}

## 已冻结序章

{prologue}

## 冻结事实摘要

{fact_summary}

## 冻结创作上下文

{context}
"""
if (OUT / "chapter-0001_curator_response.md").is_file():
    write("chapter-0001_primary_prompt.md", primary_prompt)
