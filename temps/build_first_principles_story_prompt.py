from pathlib import Path
import sys

root = Path(sys.argv[1])
blind_selected = len(sys.argv) > 2 and sys.argv[2] == "blind"
world = (root / "WORLD_VISION.md").read_text(encoding="utf-8")
character = (root / ("CHARACTER_BLIND_SELECTED.md" if blind_selected else "CHARACTER_EXPERIMENTAL.md")).read_text(encoding="utf-8")
state = (root / ("CHARACTER_INITIAL_STATE_BLIND.md" if blind_selected else "CHARACTER_INITIAL_STATE_EXPERIMENTAL.md")).read_text(encoding="utf-8")
gbrain = (root / ("STORY_GBRAIN_BLIND.md" if blind_selected else "STORY_GBRAIN.md")).read_text(encoding="utf-8")
direction = (root / "AUTHOR_DIRECTION.md").read_text(encoding="utf-8")

contract = r'''你是成熟中文男频成长长篇的 Story Program 设计者。这是 World 与 Character 第一次完整相遇。

## 冻结权威
World、Power Core、Human Core、T0 当前欲望已经冻结。不能为了让故事整齐而重写它们，也不能把人物过去解释成 Power 的隐喻。Counterplay 只能由真实碰撞后的学习产生。

## 第一性原则
**Story Program 是“长期因果如何继续”的编译，不是每个阶段都缴一次升级税的表单。**

这本书必须长期让主角本人真正变强，Core Fantasy 也必须反复得到有分量的兑现；但“持续成长”是全书级 spine，不等于每个大型阶段都必须同时出现新能力、新装备、新资源、新地图和一次能力演示。

一个大型阶段为什么值得存在，只看它有没有自己的主要发动因果：
- Life：主角私人欲望、具体关系、人生去留或自己造成的旧后果；
- Fantasy：力量、战斗、获得、探索或核心能力真正产生新玩法；
- World：世界里本来就在发生、即使主角不来仍会推进的人物行动与大事。

三者可以混合，但每个阶段可以明显偏一个。**不要为了“均衡”给每阶段都补齐三种发动机。** 如果本阶段没有新的标志性力量成长或获得，就让它没有；只要全书 progression spine 仍然成立。

Supporting Logic Must Not Automatically Become Story Engine：职业流程、材料处理、宗门行政、合同、运输、诊断、修复、任务分配等可以支撑因果，但除非人物的关键选择真的发生在那里，否则压到背景。

World 必须继续大于外挂：已有世界人物首先追自己的东西；世界事件不能被改造成“下一次 Power 用法的素材库”。同样，Human 不能只留在阶段开头和结尾做情绪装饰：如果一个具体的人、身体吸引、审美、胜负、享受、面子、亲密或私人承诺足以让主角放弃直接成长收益、改路、留下、回返或承担代价，这就是完整的 Story 因果，不需要再补一个升级理由替它辩护。

Behavior Signature 是稳定选择偏向，不是固定剧情动作。不要把人物写成“稳定就厌倦→离开；关系要失去→回头”的自动机。同一偏向应能在不同信息、关系、风险和欲望冲突下产生不同手段。

Plot Engine Diversity 只要求相邻阶段的核心问题与主角关键选择真的不同，不做打勾表。不要连续退化成：得到消息/任务 → 去危险地点 → 击败竞争者 → 获得资源 → 升级 → 更大地图。

## 输出合同
先写一个简洁总览，然后严格使用以下结构。不要生成第二版，不要重复任何一级/二级标题。

# STORY PROGRAM

## 核心碰撞
说明这个人进入这个世界以后，最自然产生的 3—5 个长期张力：
- 哪些欲望即使没有 Power 也会继续；
- Power 会怎样帮助、诱惑或误导他；
- 哪些世界人物/事件不会因主角而改变自己的目标；
- 哪些关系真的能改变他的选择。
不要把它们统一成一句主题。

## 全书一级成长脊柱
只写 4—6 次真正改变主角本人能力与行动方式的质变。它们可以跨越多个大型阶段；不需要一阶段对应一次。说明 Core Fantasy 怎样持续活着、怎样与正常修炼共同增长，以及最终仍受什么边界约束。

## 不可替代的人与关系
写少量具体人物。每个人先有自己的欲望；说明这个人为什么无法被“同等有用的另一个人”替代，以及关系会怎样真实改变主角的风险、去留、暴露、牺牲或时间分配。允许爱情、身体吸引、友情、竞争、依赖、嫉妒、背叛、效忠、敌意等，不把关系统一成安全合作。

## 长期故事主线
生成 5—7 个自然大型阶段。阶段长度不平均，也不为凑数拆分。

每阶段只使用下面六项：

### 阶段N｜阶段名
**为什么现在发生：** 上一阶段留下的事实、某个人主动做的事、世界事件、私人欲望或真正的 Fantasy 机会，为什么让这一段现在发生。不要写抽象“需要升级”。

**谁想要什么：** 只写本阶段真正推动事情的 2—5 个主体及其具体欲望。组织角色也要写人为什么这么做，而不是只有职位利益。

**主角的关键选择与行动：** 写 1—3 个会暴露这个人是谁的 Contestable Choice。明确他主动做了什么。不要自动选择长期最优，也不要让 Power 替他做价值判断。

**这一阶段真正的阅读满足：** 只选最主要的 1—2 个满足，允许主要来自 Life / Fantasy / World 任意一类。Core Fantasy 若不是主满足，只需自然活着，不得硬抢主线。

**结果：什么永久改变：** 写人物关系、世界事实、拥有物、身份、伤亡、秘密、地点归属或主角本人能力中真正发生的变化。只有实际发生显著成长/获得时才写，不需要机械掉宝或升级。

**下一阶段为何自然发生：** 只能从已经发生的选择、关系、世界行动、未完成欲望或旧谜团长出。下一阶段不要求更大，只要求更值得追。

## 远期仍值得追的东西
列出少量仍未完成的人、欲望、世界事件、地点或力量场面。不要汇总成终极哲学，也不要把所有未知并成同一个幕后真相。

## 边界
- 不逐章写 Outline。
- 不替 Writer 写正文。
- 不把世界 supporting reality 变成治理/工程主线。
- 不新增隐藏第11境界或更高力量层。
- 不输出第二套候选方案。
'''

prompt = (
    contract
    + "\n\n# 作者方向\n\n" + direction.strip()
    + "\n\n# 已冻结 WORLD VISION\n\n" + world.strip()
    + "\n\n# 已冻结 CHARACTER AUTHORITY\n\n" + character.strip()
    + "\n\n# T0 CHARACTER STATE\n\n" + state.strip()
    + "\n\n# Story GBrain（与 baseline 相同，只作可选抽象灵感）\n\n" + gbrain.strip()
    + "\n"
)
(root / ("STORY_PROGRAM_BLIND_FIRST_PRINCIPLES_PROMPT.md" if blind_selected else "STORY_PROGRAM_FIRST_PRINCIPLES_PROMPT.md")).write_text(prompt, encoding="utf-8")
print(f"prompt_chars={len(prompt)}")
