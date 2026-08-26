from pathlib import Path
p=Path('docs/PIPELINE_METHODOLOGY_AND_VALUES.md')
s=p.read_text(encoding='utf-8')
old='''- Future 10 的逐章具体事件；
- 故事开写前的 **T0 Initial State**：只记录 Chapter 1 第一场事件发生前已经成立的事实；Future 10 / 剧情块中规划出的能力使用、奖励、物品、关系变化、伤亡和其它未来结果只能留在 Plan / Open Promises，不能提前进入 Current State / Canon；
- 每个阶段的 Fantasy Proof、一级成长、收益与反哺、下一块推动；
- **World Model Release**：作者知道 World Vision 不等于读者知道。开书前三章在相关冲突或爽点需要之前，通过事件让读者获得当前需要的强弱、身份、价值与能力边界；新造概念第一次影响选择时，先让读者看到触发、可见结果和行动含义，再允许名称或深层解释进入，不把正文写成设定说明；
- **Core Gameplay Variation**：第一次高光以后，尽快把“它能不能做到”推进成“为什么选这个对象/时机/用法、别人怎样反制、同一优势还能产生什么不同结果”；尤其不要让上一轮已经证明有效的解法自动解决下一轮主要问题，下一轮冲突优先攻击它尚未解决的对象、关系、资源、目标或条件，或迫使主角换一种用法。这样实现换挡，不要求机械让主角失败或每轮加新代价；
- **Reader Experience Projection**：继续使用 Action Space / Expectation Ladder / Mystery Depth / Impact，但只投影到现有 Outline 字段：一级成长/本批打开的新行动空间写具体新行动，收益与推向下一块写下一层可欲望目标，旧物/旧人/旧事实承担 Mystery 锚点，结果/状态变化/余波写实际影响对象和范围；
- **Theme Is Derived**：`## 11. 主题、价值观与长期问题` 只后验总结已经由人物、欲望、世界与事件自然形成的主题；没有稳定主题时允许“暂不预设”，不得反向决定世界 ontology、资源、敌人、能力升格或终局。'''
new='''- Future 10 的逐章具体事件；
- 故事开写前的 **T0 Initial State**：只记录 Chapter 1 第一场事件发生前已经成立的事实；Future 10 / 剧情块中规划出的能力使用、奖励、物品、关系变化、伤亡和其它未来结果只能留在 Plan / Open Promises，不能提前进入 Current State / Canon；
- **Story Program execution, not rescheduling**：Power Seed 决定 growth grammar，Story Program 决定长期 realization，Outline 只把已批准变化落进当前窗口。某个剧情块可以完全没有 Power / Acquisition / 新地图；已经安排在当前窗口的真实成长又不能被省略；
- **Block Delta**：每块只记录相对本块开始真实改变的 Power/Capability、Possession、Relationship、Identity/Access、Knowledge、Enemy State、World State，没变化的维度省略，上一块已经发生的变化不能重复包装成新 Delta；
- **World Model Release**：作者知道 World Vision 不等于读者知道。开书前三章在相关冲突或爽点需要之前，通过事件让读者获得当前需要的强弱、身份、价值与能力边界；新造概念第一次影响选择时，先让读者看到触发、可见结果和行动含义，再允许名称或深层解释进入，不把正文写成设定说明；
- **Core Gameplay Variation**：第一次高光以后，尽快把“它能不能做到”推进成“为什么选这个对象/时机/用法、别人怎样反制、同一优势还能产生什么不同结果”；尤其不要让上一轮已经证明有效的解法自动解决下一轮主要问题，下一轮冲突优先攻击它尚未解决的对象、关系、资源、目标或条件，或迫使主角换一种用法。这样实现换挡，不要求机械让主角失败或每轮加新代价；
- **Reader Experience Projection**：Action Space / Expectation Ladder / Mystery Depth / Impact 仍作为后台阅读体验坐标，但通过具体故事锚点和实际 Delta 自然显现，不再要求每块或每十章分别填写“一级成长 / 净收益 / 新行动空间 / 世界扩张”；
- **Theme Is Derived**：`## 11. 主题、价值观与长期问题` 只后验总结已经由人物、欲望、世界与事件自然形成的主题；没有稳定主题时允许“暂不预设”，不得反向决定世界 ontology、资源、敌人、能力升格或终局。'''
assert s.count(old)==1, s.count(old)
p.write_text(s.replace(old,new),encoding='utf-8')
