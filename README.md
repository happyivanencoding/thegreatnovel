# Novel Studio

> **Author-first, local, auditable long-form webnovel authoring system.**
>
> 一个面向**中文长篇连载网文**的本地创作、续写、改写与世界管理系统。

---

# 为什么要做这个项目？

现有的大模型已经能够写出不错的小说片段。

但是，当目标变成一部几十万、上百万字的长篇网文时，它们通常会遇到：

- 遗忘既有设定；
- 偷偷修改人物状态；
- 吃掉伏笔与承诺；
- 创造没有来源的能力、物品或知识；
- 世界观逐渐崩坏；
- 几百章以后无法保持连续性；
- 很难长期维持成长节奏与读者期待。

**Novel Studio 不是一个聊天机器人。**

它更接近于：

> **一套专门为长篇网文作者设计的 IDE（Integrated Development Environment）。**

系统将小说中的：

- 世界状态
- 人物
- 势力
- 能力
- 背包
- 资源
- 知识边界
- 作者隐藏设定
- 长线剧情
- 世界扩张
- 爽点
- 节奏

全部变成：

> **可管理、可验证、可审计、可持续维护的数据。**

---

# 项目目标

Novel Studio 希望解决的不是：

> "让 AI 写几章小说。"

而是：

> **让 AI 能够长期参与一部数百万字中文长篇网文的创作，同时保持世界观、成长体系、人物关系和剧情连续性。**

支持：

- 导入已有小说继续创作
- 改写已有小说
- 从一句话开始原创
- 长期维护世界状态
- 长期维护人物成长
- 自动管理伏笔
- 自动管理秘密
- 自动管理节奏
- 自动管理爽点
- 自动管理世界扩张

---

# 产品定位

Novel Studio 面向的是：

**中文长篇连载网文。**

尤其适合：

- 东方玄幻
- 仙侠
- 高武
- 科幻玄幻
- 神秘学成长
- 末世成长
- 求生
- 长篇成长流

未来也支持：

- 都市
- 历史
- 游戏
- 电竞
- 商业
- 文娱
- 职业成长等长篇类型。

---

# 核心理念

## Author First

作者永远拥有最终决定权。

AI：

可以：

- 理解
- 建议
- 规划
- 写草稿
- 找 Bug
- 检查连续性

不能：

- 偷偷修改世界观
- 偷偷修改人物
- 偷偷修改正史
- 偷偷批准章节

---

## Canon is Sacred

正式正文永远需要：

```text
Candidate
    ↓
Chapter Contract
    ↓
Draft
    ↓
Validation
    ↓
Author Approval
    ↓
Canon
```

AI 永远不能直接写入 Canon。

---

## Python is the Authority

LLM：

负责：

- 创意
- 理解
- 写作
- 分析

Python：

负责：

- 状态
- 数据
- 校验
- 工作流
- 审计
- Commit

核心原则：

> **LLM at the edges; deterministic engine at the center.**

---

## Everything is Auditable

系统必须回答：

为什么会生成这一章？

依据哪些事实？

推进哪些剧情？

修改哪些状态？

违反哪些规则？

以后还能不能回滚？

---

# 两种创作模式

## 导入已有小说

例如：

- 《斗破苍穹》
- 《斗罗大陆》
- 《吞噬星空》
- 《诡秘之主》

系统会：

建立：

- Book Library
- Story Atlas
- Chapter World State
- Character State
- Distillation Package
- Author Truth
- Continuation Boundary
- 九维全书画像

然后继续：

第 N+1 章。

---

## 从一句话开始原创

例如：

> 近未来体修成神。

或者：

> 一群人在移动巨兽背上建立文明。

系统会：

建立：

- Reader Experience
- Story Foundation
- Genre Contract
- Progression Contract
- 世界规则
- 主角
- 势力
- 长线规划
- 第一章候选

然后正式开始创作。

---

# Novel Studio

Novel Studio 是整个系统的工作台。

包括：

- 正文
- 世界状态
- 人物
- 背包
- 能力
- 地点
- 势力
- 作者全知
- 长线规划
- 九维画像
- 连续性
- Activity Center

作者几乎所有工作都在这里完成。

---

# Book Library

Book Library 管理所有小说。

支持：

- 导入已有小说
- 新建原创小说
- Book
- Edition
- 初始化
- 分类
- Developer Mode

正式作品、测试、Demo 与 Benchmark 默认隔离。

---

# 世界状态

系统为每一章维护：

**Chapter World State**

记录：

- 人物
- 背包
- 能力
- 装备
- 地点
- 势力
- 世界规则
- 知识
- 作者隐藏设定

并能够查看：

> **第 N 章结束以后，世界真正是什么样。**

---

# Author Truth

作者知道：

角色不知道。

读者不知道。

包括：

- 真相
- 幕后计划
- 最终目标
- 世界秘密

这些不会直接进入正文。

---

# Progressive Initialization

已有小说支持：

## QUICK

快速进入工作台。

适合：

快速了解作品。

---

## BALANCED（推荐）

建立：

- 全书事实索引
- 当前边界
- 活跃人物
- 当前剧情

适合：

正式续写。

---

## FULL

完整深度分析。

适合：

- 大规模改写
- 全书审计
- 长期项目

---

# Distillation

Novel Studio 集成：

**distill-novels**

生成：

- 世界
- 人物
- 剧情
- 文风
- 对话
- 节奏
- 主题
- 连续性

形成九维文学理解层。

这些属于：

> **Soft Reference**

不会直接成为 Canon。

---

# Novel Studio Architecture

```text
Reader Experience
        ↓
Genre Contract
        ↓
Narrative Drive
        ↓
Specialized Narrative Engines
        ↓
Story Planning
        ↓
Candidate
        ↓
Draft
        ↓
Validation
        ↓
Author Approval
        ↓
Canon
        ↓
World State
```

---

# 核心能力

- 多版本 Edition
- 正式续写
- 正式改写
- 世界状态
- 作者全知
- Reveal Plan
- Story Atlas
- Distillation
- Progressive Initialization
- Activity Center
- Local Codex Workflow
- Browser Workbench

---

# 当前重点方向

Novel Studio 正在建设：

## Chinese Serialized Webnovel Kernel

它不是：

一个"修仙生成器"。

而是：

一个专门服务：

**中文长篇连载网文**

的创作内核。

目前重点完成：

- Progression Engine（成长）
- Reader Experience
- Genre Contract
- World Expansion
- Resource Economy
- Payoff Engine
- Narrative Debt
- Serial Scheduler

未来扩展：

- Mystery Engine
- Career Engine
- Strategy Engine
- Survival Engine
- Competition Engine
- Relationship Engine

---

# 项目目录

```text
book/
    原始正文（永久只读）

library/
    小说运行库

src/
    Python Engine

.agents/
    Codex Skills

docs/
    文档

benchmark/
    Benchmark

tests/
    自动测试
```

---

# Roadmap

未来重点：

- Reader Experience
- Narrative Drive
- Progression Engine
- Mystery Engine
- World Expansion
- Story Scheduler
- Automatic Long-form Planning

最终目标：

> **建立一个真正能够长期辅助作者创作中文长篇连载网文的专业创作系统，而不是一个只会生成几章小说的 AI。**
