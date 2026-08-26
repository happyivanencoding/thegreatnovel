from pathlib import Path
p=Path('docs/MVP_PRODUCT_DIRECTION.md')
s=p.read_text(encoding='utf-8')
old='''## Growth Genome 的位置

Growth Genome 仍然存在，但只整理已经批准的 Character / World / Story Program 与 Outline 所需信息：

- 一级成长主轴；
- 二级收益与反哺；
- 主循环与阶段升格；
- 核心不变量与退化风险。

它不选择核心幻想，不创建人物欲望，不重新规划 Story Program，也不进入 State Delta 成为第二套状态系统。'''
new='''## Growth Genome / Outline 的位置

BOOK 中保留 `## 0. 本书成长基因图` 主要为了兼容现有 BOOK / Chapter Runtime，但它现在是**已批准上游的短投影**，不是第二个故事设计器：

- 压缩已批准幻想不变量；
- 复述 Story Program 已经安排的长期 Power / Capability 真实质变，不新增数量要求或升级节点；
- 记录会跨阶段继续生效的重要获得、关系、身份、知识或世界后果；
- 保留少量核心不变量与真实退化风险。

Outline 的职责是把 Story Program 编译成当前窗口的具体 Story Anchors。每个剧情块使用 `Block Delta`，只记录相对本块开始真实改变的 Power/Capability、Possession、Relationship、Identity/Access、Knowledge、Enemy State、World State；没有变化的维度直接省略。**Growth is longitudinal, not a per-block or ten-chapter tax.** Outline 不重新规划 Story Program，也不为了填表补微升级、小奖励、新权限或新地图。'''
assert s.count(old)==1
p.write_text(s.replace(old,new),encoding='utf-8')
