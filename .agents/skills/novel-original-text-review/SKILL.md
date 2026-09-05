---
name: novel-original-text-review
version: 0.1.0
description: TGN 小说读感与经典对照的原文证据 Skill；从本地完整小说库直接读取经典原著连续窗口，再与 TGN 正文做 source-first 对照，禁止用 GBrain/蒸馏卡/梗概冒充原文阅读。
---

# Mission

当任务涉及以下任一目标时使用本 Skill：

- “这段和《遮天》/《斗罗》/其它经典相比差在哪里”；
- “为什么这一段不像成熟网文 / 顶级男频”；
- 战斗、对白、关系、探索、成长、Public Proof、世界介绍、长篇结构等读感对照；
- 为 TGN 的 Prompt / Runtime / Scene Skill / Story Program 改进寻找经典原文证据。

本 Skill 的第一原则：

> **没有实际读到原文，就没有完成经典原文对照。**

GBrain、蒸馏库、剧情梗概、模型记忆可以帮助提出“去哪里找”的假设，但不能作为“我已经读过经典原文”的证据。

# Original Library

默认从本机完整小说库动态发现可用 `.txt` 原著，而不是维护三本书白名单。默认 roots：

- `C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\400+本高质量完本合集`
- `C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\起点精选小说合集`
- `C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\小说整理合集`

可用 `TGN_CLASSIC_LIBRARY_ROOTS`（Windows `;` 分隔）覆盖/扩展 roots。当前主合集本身已有约 410 个 `.txt` 原著；**所有能被工具定位和直接读取的完整原著都可成为参考，不限于预设书单。**

少量经典路由建议见 `references/classic-routing.md`。它只是 search prior，不是排名，不是配额；当前任务若有更合适的其它原著，直接使用其它书。

# Tool

脚本：`scripts/classic_text.py`

常用调用：

```powershell
python scripts/classic_text.py catalog --query 遮天
python scripts/classic_text.py resolve --title 遮天
python scripts/classic_text.py search --title 遮天 --query "多人 战斗 空间" --limit 8
python scripts/classic_text.py window --title 遮天 --chapter 38 --before 1 --after 1 --out C:\dev\tgn-story-mvp\.local\classic-review\zhetian-ch38.txt
# 若同一本书不同卷会重复“第一章”等编号，使用 search 返回的唯一 ordinal：
python scripts/classic_text.py window --title 将夜 --ordinal 496 --out C:\dev\tgn-story-mvp\.local\classic-review\jiangye-o496.txt
```

工具只做确定性工作：发现完整原著、识别编码、解析章节、搜索候选章节、截取连续原文窗口、记录 locator。它不做文学判断，也不调用 LLM。

# Required Workflow

## 1. 先明确比较问题

不要先找“最有名”的书。先把当前读感问题压成一个具体阅读问题，例如：

- 多人战斗为什么空间混乱？
- 对白为什么像一句一句功能指令？
- 力量等级为什么存在但读者没有期待感？
- 世界介绍为什么只有设定，没有生活坐标？
- Public Proof 为什么只有“震惊”，没有社会重新定价？
- 长篇人物为什么离开当前章后就像不存在？

## 2. 选择 1—3 本真正相关的经典

- 用户明确点名某本书：必须优先直接读那本；本地找不到时明确说“未完成该书原文对照”，不能拿 GBrain 顶替。
- 用户未点名：从动态 catalog 中选 1—3 本最适合当前问题的经典。优先互补证据，而不是三本风格相同的书。
- 不需要每次都用《遮天》《斗罗》《斗破》。其它经典只要更适合当前问题，应优先其它经典。

## 3. 先定位，再读连续窗口

先用 `search` 找候选章节，再用 `window` 导出**完整场景或足够连续的章节窗口**。不要只摘一句金句证明观点。

每个实际阅读窗口至少记录：

- 书名；
- 本地 source path；
- 实际读取的章节号/标题；
- source line range；
- 是否为连续窗口；
- 为什么这个窗口与当前问题同位。

工具生成的窗口默认放 `.local/classic-review/`；不要把原著全文、窗口文件或长摘录提交到 Git。

## 4. 必须直接读原文

Agent 必须实际打开 `window` 生成的文本并阅读。只运行 `search`、看章节标题、读 GBrain 卡、读别人的摘要，都不算完成这一步。

如果窗口太大，可以继续缩窄到场景前后仍连续的范围；但不能只保留支持自己观点的孤立句子。

## 5. 再读 TGN 同位文本

冻结待比较的 TGN artifact。不要在读经典途中悄悄改 TGN 文本，再把修改后版本当 baseline。

## 6. Evidence → Interpretation → Generalization

输出判断时严格分三层：

1. **Original Evidence**：原文窗口里实际可观察的结构；只做短引用或位置描述，不复制大段原著。
2. **TGN Contrast**：TGN 同位文本具体少了什么 / 多了什么 / 顺序哪里不同。
3. **Transferable Principle**：抽象成 source-blind 的可迁移机制，不能变成模仿某作者声音、专名、句法或情节。

不要从“经典这样写”直接跳成“所有小说必须这样写”。至少说明当前问题为什么适用。

# Reading Receipt

任何声称“我读了经典原文并做了对比”的结论，正文前或报告中必须包含一个简短 `Original Text Reading Receipt`：

```text
Original Text Reading Receipt
- 《书A》：第X—Y章 / 标题；source lines A—B；已直接阅读连续窗口
- 《书B》：第M章；source lines C—D；已直接阅读完整场景
- GBrain used as original evidence: NO
```

如果没有 receipt，就不能写“对比经典原文后”。

# Failure Rules

以下情况必须停止 reference-specific 结论，而不是猜：

- 本地找不到用户点名的原著；
- 文件无法正常解码；
- 章节结构无法可靠定位，且无法建立足够连续窗口；
- 只找到摘要、蒸馏卡、二手剧情介绍；
- 实际只读了局部，却准备声称“通读全书”。

允许继续做一般读感分析，但必须明确：**本轮没有完成该经典的原文对照。**

# Copyright / Runtime Boundary

- 原著用于本地开发评审和 craft 学习，不进入 Production Writer / Reviser / Story Prompt。
- 不把完整原文窗口提交 Git，不把原著大段复制到 docs / GBrain / Skill。
- 对用户展示时优先章节 locator + 自己的分析；必要引用保持很短。
- 不模仿作者声音，不要求 Writer 仿写原著。

# Relationship to Other TGN Skills

- `tgn-system-steward`：负责 root-cause / architecture 判断；涉及经典读感证据时调用本 Skill 的原文流程。
- `novel-scene-skills`：可以由本 Skill 的 source-first 阅读结果提出新的研究证据，但只有经过 Fidelity / cross-book promotion 后才能升级 Deep Craft。
- GBrain：可以帮助导航、蒸馏和 source-blind synthesis，**不能替代本 Skill 的 Original Evidence**。
