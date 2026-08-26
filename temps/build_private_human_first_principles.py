from pathlib import Path

root = Path(r"books/real-exp-private-prototype-upstream-20260826-v3")
life = (root / "HUMAN_LIFE_CONTEXT.md").read_text(encoding="utf-8")
bundle = (root / "EXPLICIT_ANON_HUMAN_BUNDLE.md").read_text(encoding="utf-8")

prompt = r'''你是成熟中文男频成长长篇的 Human Seed 设计者。你完全不知道未来 Power Seed、金手指和 named Story Opportunities。

这是一次显式匿名 prototype 投影：Prototype 只提供三类长期选择倾向；表层身份、家庭、生活事件、关系对象和当前欲望必须在当前幻想世界重新出生。

第一性原则：**Human Seed 是一个人的权威快照，不是解释“为什么他必然成为这个人”的心理学论文。**

不要把 prototype 的 Appetite / Behavior / Relationship 三 lane 汇总成一句人生哲学，再反向发明刚好逐条证明它的童年。生活事实可以影响他，也可以只是发生过；同一个事实可能支持多种后来选择。

保持三件事：
1. 多股私人欲望真实并存并竞争，包括 prototype 中明确存在的身体吸引/情欲、审美感官、被看见、胜负/比较、新鲜与具体关系；不要净化成“追求鲜活”一个总词。
2. Stable Choice Bias + Variable Realization：稳定的是容易保护/拒绝/过量什么，手段因现场变化；不要固化成“稳定就离开、失去就回头”。
3. Relationship as choice variable：一个具体的人能真实改变去留、风险、时间、暴露或机会牺牲；这个人也有自己的欲望，不是主角的校正器。

只生成 1 个 fictionalized Human Seed，不评分、不提供备选。

严格输出：

# HUMAN SEED｜幻想姓名／短标签
## 世界中的初始位置与生活事实
写具体出身、家庭、教育、日常、接触修炼/工作的方式，以及 3—5 件真实发生过的生活事实。不要逐条写 Adaptation 或人格结论；允许弱相关、偶然甚至彼此矛盾的事实。

## 持续牵引与互相竞争的动机
保留 3—5 股私人牵引，明确至少两处“不能同时都要”的真实冲突。不要总结成唯一 Core Obsession。

## Behavior Signature
写稳定选择偏向和多种可能实现；不要固定剧情动作。

## 重要关系原点
写 1—2 个具体的人；至少一段关系真实包含身体吸引/情欲，但不要把全部亲密都性化。说明为什么换成同等有用的人不成立，以及双方各自想要什么。

## Initial State Seed
### 当前私人欲望
写现在具体牵着他行动的一件事；它不是永久身份。

## Audition Metadata（非 Canon）
### 人物钩子
给一个不知道未来 Power 仍能记住他的场面；不绑定前三章。

# LIFE CONTEXT

''' + life + "\n\n# Explicit Anonymous Human Prototype\n\n" + bundle + "\n"
(root / "HUMAN_FIRST_PRINCIPLES_PROMPT.md").write_text(prompt, encoding="utf-8")
print(f"prompt_chars={len(prompt)}")
