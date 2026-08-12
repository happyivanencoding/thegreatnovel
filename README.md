下面是我建议作为**项目门面**的 README，它不是开发日志，也不是设计宪法，而是第一次进入仓库的人（包括未来的你）能够在 5 分钟内理解：

> **这是什么？为什么存在？怎么开始？和其他 AI 小说工具有什么区别？**

---

# Novel Studio

> **Author-first, local, auditable long-form webnovel authoring system.**
>
> 一个面向**中文长篇连载网文**的本地创作、续写、改写与世界管理系统。

---

# 为什么要做这个项目？

现有的大模型可以写小说。

但是：

* 它们会遗忘设定；
* 会偷偷修改人物；
* 会吃掉伏笔；
* 会创造不存在的能力；
* 很难连续写几百章；
* 很难保持一本小说十万、百万字后的连续性。

**Novel Studio 不是一个聊天机器人。**

它更像：

> **一套给小说作者使用的 IDE（集成创作环境）。**

它把：

* 世界状态
* 人物
* 势力
* 能力
* 背包
* 知识边界
* 作者隐藏设定
* 长线剧情
* 爽点
* 节奏
* 世界扩张

全部变成可以管理、可以验证、可以审计的数据。

---

# 目标

Novel Studio 希望最终做到：

> **让 AI 能够参与创作一本几百万字的长篇网文，而不是只能写几章 Demo。**

支持：

* 导入已有小说继续写
* 改写已有小说
* 从一句话开始原创
* 长期维护世界观
* 长期维护人物成长
* 自动管理伏笔
* 自动管理秘密
* 自动管理爽点
* 自动管理节奏
* 自动管理世界状态

---

# 设计原则

## 1. Author First

作者永远拥有最终决定权。

AI：

* 可以建议；
* 可以规划；
* 可以写草稿；

不能：

* 偷偷修改世界观；
* 偷偷修改人物；
* 偷偷批准正史。

---

## 2. Canon is Sacred

已经发生的正文：

永远不能被 AI 默默修改。

所有变化必须：

Draft

↓

Validation

↓

Author Approval

↓

Canon

---

## 3. Python is the Authority

LLM：

负责理解、规划、创意。

Python：

负责：

* 状态
* 数据
* 校验
* 工作流
* 审计
* Commit

---

## 4. Everything is Auditable

任何一句正文都必须回答：

为什么会写这句话？

它依据哪些事实？

违反了哪些规则？

修改了哪些状态？

以后还能回滚。

---

# 支持两种创作模式

## 导入已有小说

例如：

《斗破苍穹》

《斗罗大陆》

《吞噬星空》

《诡秘之主》

系统会：

* 建立 Book Library
* 初始化
* 建立 Story Atlas
* 建立 World State
* 建立 Character State
* 建立九维画像
* 建立 Author Truth
* 建立续写边界

然后继续第 N+1 章。

---

## 从一句话开始

例如：

> 一个普通人在移动巨兽背上建立文明。

或者：

> 近未来体修成神。

系统会：

建立：

* Reader Experience
* Story Foundation
* 世界观
* 主角
* 势力
* 长线剧情
* 第一章候选

然后进入正式创作。

---

# Novel Studio

Novel Studio 是整个系统的工作台。

包括：

* 正文
* 世界状态
* 人物
* 背包
* 能力
* 势力
* 地点
* 作者全知
* 长线规划
* 九维画像
* 连续性
* Activity Center

所有工作都在这里完成。

---

# Book Library

Book Library 管理所有小说。

支持：

* 导入已有小说
* 原创新书
* 多 Edition
* 版本管理
* 初始化
* 分类
* Developer Mode

测试、Benchmark 与正式作品默认隔离。

---

# 世界状态

每一章都有：

Chapter World State。

系统知道：

这一章结束以后：

* 人物状态
* 背包
* 能力
* 地点
* 势力
* 世界规则
* 知识
* 作者隐藏设定

发生了什么。

---

# Author Truth

作者知道，

角色不知道，

读者不知道。

例如：

幕后真相

最终 Boss

未来路线

真正目的

全部单独维护。

不会直接写进正文。

---

# Progressive Initialization

已有长篇支持三种初始化。

## QUICK

最快进入工作台。

适合：

快速了解作品。

---

## BALANCED（推荐）

重点分析：

* 当前剧情
* 当前人物
* 当前 Arc
* 活跃伏笔

适合：

正式续写。

---

## FULL

全书深度分析。

适合：

* 大规模改写
* 全书审计
* 长期项目

---

# Distill Integration

系统集成：

distill-novels。

它负责：

把一本小说提炼成：

* 世界
* 人物
* 剧情
* 文风
* 对话
* 节奏
* 主题
* 连续性

等九维知识。

这些属于：

**软理解层。**

不会直接变成 Canon。

---

# 续写流程

```
读取 Source
↓

建立 Boundary

↓

三个 Candidate

↓

Chapter Contract

↓

Draft

↓

十项 Validation

↓

Author Approval

↓

Canon Commit
```

---

# 改写流程

```
选择章节

↓

Revision Campaign

↓

派生 Edition

↓

Draft

↓

Validation

↓

Author Approval

↓

是否设为正式版本
```

---

# 项目结构

```
book/
    原始正文（永久只读）

library/
    Book Library

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

# 信息层级

系统严格区分：

```
Source

↓

Canon

↓

Author Truth

↓

Reader Knowledge

↓

Character Knowledge

↓

Inference

↓

Candidate

↓

Draft
```

任何推断：

都不能自动升级为 Canon。

---

# 本项目最大的特点

Novel Studio 并不是：

> "让 AI 写小说。"

它真正想解决的是：

> **如何让 AI 连续写几百万字，而仍然保持世界观一致。**

因此：

本项目更关注：

* 世界状态
* 长期成长
* 世界扩张
* 长线剧情
* 爽点管理
* 资源系统
* 能力系统
* 作者控制

而不是：

单章 Prompt Engineering。

---

# 当前定位

当前默认配置最适合：

* 东方玄幻
* 仙侠
* 科幻玄幻
* 高武
* 成长型爽文
* 求生
* 长篇连载

其他类型：

例如：

* 都市
* 历史
* 电竞
* 商业
* 文娱

也可以使用当前系统，

后续将进一步扩展对应的叙事内核。

---

# Roadmap

下一阶段重点：

* Reader Experience Contract
* Narrative Drive Kernel
* Progression Kernel
* Mystery Kernel
* Career Kernel
* Strategy Kernel
* World Expansion
* Automatic Narrative Scheduler
* Progressive World Simulation

最终目标：

> **建立一个真正能够长期辅助作者创作中文长篇网文的专业创作系统，而不是一个只会生成几章小说的 AI。**

```
```
