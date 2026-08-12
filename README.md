# Novel Studio

> **Author-first, local, auditable long-form webnovel authoring system.**
>
> 一个面向**中文长篇连载网文**的本地创作、续写、改写与世界管理系统。

---

# 为什么要做这个项目？

现有的大模型已经能够写出不错的小说片段。

但当目标从：

> “写一章”

变成：

> “连续写几百章、上百万字，并且仍然像同一本小说”

问题就完全不同了。

长篇创作中的 AI 往往会：

* 遗忘既有设定；
* 偷偷改变人物性格；
* 吃掉伏笔与承诺；
* 创造没有来源的能力和物品；
* 忘记谁知道什么；
* 忘记资源已经消耗；
* 忘记人物曾经受过的伤；
* 忘记世界规则；
* 让人物实力突然跳跃；
* 让剧情不断重复相同结构；
* 在几百章后逐渐失去原作的气质。

**Novel Studio 不是一个聊天机器人。**

它更接近：

> **一套专门为长篇小说作者设计的 IDE（Integrated Development Environment）。**

就像软件工程不会只依赖程序员“记住所有代码”，长篇小说也不应该要求作者或 AI 永远记住几百万字里的所有状态。

Novel Studio 尝试把小说中的：

* 世界状态；
* 人物；
* 势力；
* 能力；
* 装备；
* 背包；
* 资源；
* 知识边界；
* 作者隐藏设定；
* 长线剧情；
* 世界扩张；
* 爽点；
* 节奏；
* 成长体系；

逐渐变成：

> **可管理、可验证、可审计、可持续维护的创作状态。**

---

# 项目目标

Novel Studio 希望解决的不是：

> “怎样让 AI 写几章小说？”

而是：

> **怎样让 AI 真正参与一部几十万、几百万字长篇网文的长期创作，同时保持世界观、人物、成长体系和剧情连续性。**

系统支持：

* 导入已有小说继续创作；
* 改写已有小说；
* 从一句话开始原创；
* 长期维护世界状态；
* 长期维护人物成长；
* 管理资源、能力和装备；
* 管理人物知识边界；
* 管理伏笔与秘密；
* 管理爽点与 Narrative Debt；
* 管理世界扩张；
* 管理长期剧情方向；
* 在正式写入正文前自动验证候选内容。

最终希望形成：

```text
作者负责：

判断
审美
方向
选择
最终决定

AI负责：

理解
检索
提出方案
规划
写草稿
检查问题

系统负责：

记忆
状态
规则
证据
验证
历史
审计
```

---

# 产品定位

Novel Studio 主要面向：

# 中文长篇连载网文

尤其关注：

* 东方玄幻；
* 仙侠；
* 高武；
* 科幻玄幻；
* 神秘学成长；
* 末世进化；
* 求生；
* 世界扩张型长篇；
* 强成长、强资源、强能力体系的连载小说。

未来也希望支持：

* 都市；
* 历史；
* 游戏；
* 电竞；
* 商业；
* 文娱；
* 职业成长；
* 生存建设；
* 政治与国家建设；
* 灵异与谜团型长篇。

Novel Studio 不试图用同一个模板写所有小说。

不同作品可以拥有不同的：

```text
Reader Experience

Narrative Drive

Progression Model

Payoff Channels

Mystery Structure

World Expansion Model
```

---

# 设计原则

## Author First

作者永远拥有最终决定权。

AI 可以：

* 理解；
* 建议；
* 规划；
* 提供候选；
* 写草稿；
* 检查连续性；
* 找潜在问题。

AI 不能：

* 偷偷修改世界观；
* 偷偷改变人物；
* 偷偷改变正式版本；
* 自动批准章节；
* 将推测偷偷变成事实。

**AI 是创作伙伴，不是作品所有者。**

---

## Canon is Sacred

正式发生过的正文具有明确边界。

任何新内容必须经历：

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

AI 永远不能绕过作者批准直接进入正式正文。

---

## Python is the Authority

LLM 负责：

* 理解；
* 创意；
* 分析；
* 写作；
* 文学判断。

Python 负责：

* 状态；
* 数据；
* 规则；
* 校验；
* 工作流；
* 审计；
* Commit。

核心原则：

> **LLM at the edges; deterministic engine at the center.**

---

## Everything is Auditable

系统应该能够回答：

> 为什么生成这个方案？

> 它依据哪些事实？

> 它推进了哪些长期剧情？

> 它使用了哪些人物状态？

> 它修改了什么？

> 有没有违反成长规则？

> 有没有让角色知道不应该知道的信息？

> 有没有破坏已经建立的伏笔？

> 为什么最终选择了这个版本？

长篇 AI 创作不能只是：

> “模型觉得这样比较好。”

它应该逐渐成为：

> **可以理解、可以检查、可以回滚的创作过程。**

---

# 两种主要创作模式

## 导入已有小说

将已有小说导入 Novel Studio。

系统可以建立：

* Book Library；
* Source Manifest；
* Story Atlas；
* Chapter World State；
* Character State；
* Knowledge State；
* Distillation Package；
* Global Book Profile；
* Author Truth；
* Continuation Boundary；
* Progression State；
* Narrative Drive Proposal。

随后从：

```text
第 N 章
```

继续：

```text
第 N+1 章
```

而不是每次重新把几十万字塞进 Prompt。

---

## 从一句话开始原创

例如：

> 近未来体修成神。

或者：

> 一群人在移动巨兽背上建立文明。

系统会先理解：

```text
读者为什么会追这本书？
```

然后建立：

* Reader Experience；
* Story Foundation；
* Genre Contract；
* Narrative Drive；
* Progression Contract；
* 世界规则；
* 主角；
* 势力；
* 长线规划；
* 第一章候选。

作者确认后，才真正开始写第一章。

---

# Novel Studio

Novel Studio 是整个系统的作者工作台。

主要包括：

* 正文；
* 人物与关系；
* 世界与物品；
* 成长；
* 剧情规划；
* 创作任务；
* 作者幕后设定；
* Reveal；
* 九维画像；
* 连续性；
* Activity Center。

系统内部拥有大量工程状态，

但普通作者界面尽量只回答几个问题：

> **现在写到哪里？**

> **人物现在是什么状态？**

> **还有什么没有兑现？**

> **下一章最值得写什么？**

---

# Book Library

Book Library 管理所有作品。

支持：

* 导入已有小说；
* 原创新书；
* 多 Book；
* 多 Edition；
* 初始化；
* 归档；
* Developer Mode。

正式作品与：

* Test；
* Demo；
* Benchmark；

默认隔离。

技术实验不会污染作者书库。

---

# Edition

一本小说可以拥有不同正式路线。

例如：

```text
原始版本

正式修订版

平行路线

另一结局
```

但：

```text
Draft ≠ Edition

Experiment ≠ Edition

Benchmark ≠ Book
```

正式续写默认继续当前 Edition。

重大改写可以建立派生 Edition。

---

# Chapter World State

系统为每一章维护：

# Chapter World State

记录这一章结束以后：

* 人物在哪里；
* 有什么装备；
* 有什么能力；
* 拥有什么资源；
* 身体状态如何；
* 谁和谁是什么关系；
* 谁知道什么；
* 哪些势力发生变化；
* 哪些世界规则已经建立；
* 哪些剧情线程仍然活跃。

因此可以查询：

> **第 30 章结束时世界是什么样？**

也可以查询：

> **第 300 章结束时世界是什么样？**

而不会把第 300 章的信息倒灌到第 30 章。

---

# Author Truth

长篇小说存在大量：

> 作者知道，但角色和读者不知道的事情。

Novel Studio 将这些内容单独管理。

例如：

* 真正身份；
* 幕后目的；
* 世界秘密；
* 最终 Boss；
* 某个角色真正的立场；
* 某件物品真正的来源。

并严格区分：

```text
作者知道什么

读者知道什么

角色知道什么
```

---

# Reveal System

秘密并不是：

```text
不知道
→
突然全部知道
```

它可能经历：

```text
未知
→
暗示
→
怀疑
→
部分揭露
→
确认
```

Novel Studio 使用 Reveal Plan 管理这些变化，

避免：

* 提前泄密；
* 忘记揭露；
* 一次解释过多；
* 角色无依据突然知道真相。

---

# Progressive Initialization

已有长篇可以选择不同初始化深度。

## QUICK

快速建立：

* 全书结构；
* 当前边界；
* 基础画像。

适合：

快速体验和探索。

---

## BALANCED

推荐模式。

重点建立：

* 全书连续性索引；
* 当前人物；
* 当前资源；
* 当前剧情；
* 活跃伏笔；
* 最近章节完整状态。

适合：

正式续写。

---

## FULL

全书深度分析。

适合：

* 大规模改写；
* 全书审计；
* 世界状态研究；
* 长期大型项目。

系统的目标不是：

> “必须先分析完整本书才能开始写。”

而是：

> **尽快达到安全创作当前下一章所需要的状态。**

---

# Distillation

Novel Studio 集成文学蒸馏层。

它可以从小说中提取：

* 世界；
* 人物；
* 剧情；
* 文风；
* 叙事；
* 对话；
* 节奏；
* 主题；
* 连续性。

形成九维文学理解。

这些内容属于：

> **Soft Reference**

它们可以帮助 AI 理解小说，

但不能自动成为 Canon。

---

# Chinese Serialized Webnovel Kernel

Novel Studio 正在建立：

# Chinese Serialized Webnovel Kernel

即：

> **中文长篇连载网文内核。**

它试图理解的不是：

> “这本书属于玄幻还是都市？”

而是：

> **读者为什么还想看下一章？**

不同小说可能由不同 Narrative Drive 推动：

```text
力量成长

知识成长

谜团揭露

资源获取

世界探索

职业成长

财富与地位

势力建设

政治与国家

竞技排名

团队成长

生存与基地

人物关系
```

一本小说可以同时拥有多个 Drive。

---

# Progression Engine

Progression Engine 是当前最重要的专业引擎之一。

主要服务：

* 玄幻；
* 仙侠；
* 高武；
* 科幻玄幻；
* 末世进化；
* 神秘学晋升。

它关注：

```text
主角现在成长到哪里？

下一阶段是什么？

突破需要什么？

缺少什么资源？

刚获得什么新能力？

这个能力验证过了吗？

成长已经停滞多久？

什么时候应该让世界扩大？
```

Progression 不一定是：

```text
炼气
筑基
金丹
```

也可以是：

```text
等级

序列

生命层级

身体进化

能力槽

知识权限

职业能力

社会地位
```

---

# Narrative Debt

长篇小说中很多内容都会产生：

> **未来必须偿还的期待。**

例如：

得到新能力：

→ 读者期待看到它真正使用。

接近突破：

→ 读者期待突破兑现。

发现秘密：

→ 读者期待进一步揭露。

获得线索：

→ 读者期待它影响未来。

进入新的势力：

→ 读者期待它改变人物地位。

Novel Studio 将这些期待看作：

# Narrative Debt

并持续追踪：

```text
已经建立什么？

推进了什么？

兑现了什么？

拖得太久了吗？
```

---

# Payoff Engine

长篇小说的满足感并不只有：

> “主角升级。”

不同作品可能拥有不同的 Payoff Channels：

* 力量突破；
* 新能力；
* 新装备；
* 资源机缘；
* 越级胜利；
* 身份提升；
* 势力认可；
* 财富跃迁；
* 世界扩张；
* 谜团揭晓；
* 复仇兑现；
* 团队成长；
* 关系推进。

系统试图避免：

> 连续几十章只使用同一种爽点。

---

# Serial Scheduler

未来 Novel Studio 不只是回答：

> “下一章可以写什么？”

而是尝试回答：

> **“为什么现在最应该写这个？”**

Scheduler 会综合：

* 当前剧情；
* 人物状态；
* 成长状态；
* Narrative Debt；
* Payoff；
* Reveal；
* 世界扩张；
* 作者任务；
* 最近章节结构；
* 节奏疲劳；

生成多个候选方向。

最终决定仍然属于作者。

---

# 写作工作流

```text
Current Story State
        ↓
Narrative Scheduler
        ↓
3 Candidate Plans
        ↓
Author Selection
        ↓
Chapter Contract
        ↓
Draft
        ↓
Validation
        ↓
Author Approval
        ↓
Canon Commit
        ↓
World State Update
        ↓
下一章
```

---

# 对作者意味着什么？

Novel Studio 希望降低长篇创作中一种非常真实的成本：

# 认知负担

写几十章时，

作者可以记住大部分东西。

写几百章以后，

问题会越来越多：

* 这个人什么时候得到这个能力？
* 谁知道这个秘密？
* 这件装备是不是已经丢了？
* 这个伏笔什么时候埋的？
* 这个人物和另外一个人的关系现在是什么状态？
* 最近是不是很久没有真正的成长了？
* 这个地图是不是已经写太久？
* 这个秘密是不是拖了太久？
* 前面有没有已经建立过冲突设定？

Novel Studio 希望让作者不再需要：

> **把整部小说装在脑子里。**

作者可以把更多注意力留给：

* 想象；
* 人物；
* 审美；
* 情绪；
* 世界；
  -真正值得决定的东西。

---

# 对独立创作者意味着什么？

过去，一部长篇小说通常高度依赖：

> 一个人的记忆和长期稳定产出能力。

AI 出现以后，

个人作者理论上第一次拥有了一支：

```text
研究助手

设定管理员

连续性编辑

资料检索员

剧情规划师

草稿助手

质量检查员
```

组成的虚拟创作团队。

Novel Studio 希望为这种新的：

# AI-native Independent Creator

提供基础设施。

一个人不一定需要变成大型工作室，

也有可能长期管理：

* 百万字世界；
* 多人物；
* 多版本；
* 多条剧情线；
* 数百章历史。

---

# 对 AI 创作方式意味着什么？

今天很多 AI 小说系统的核心仍然是：

```text
Prompt
+
Context Window
+
Generate
```

Novel Studio 尝试探索另一种路径：

```text
Persistent State
+
Deterministic Workflow
+
LLM Reasoning
+
Human Approval
```

也就是说：

> **从 Prompt Engineering 走向 Creative Systems Engineering。**

模型本身很重要，

但模型外部的：

* 状态；
* Memory；
* Tooling；
* Validation；
* Workflow；
* Human Control；

可能同样决定长篇创作能否真正成立。

---

# 对创作者社群的潜在价值

如果 Novel Studio 最终发展成一个开放的创作系统，它的价值可能不仅属于单个作者。

它还可能逐渐形成一种新的：

# 可交流的小说工程语言

今天作者交流时经常说：

> “这里节奏有点慢。”

> “感觉最近不够爽。”

> “这个伏笔拖太久了。”

> “主角最近没成长。”

这些判断往往完全依赖经验和感觉。

Novel Studio 希望在不取代文学判断的前提下，提供一些可以共同讨论的结构：

```text
Progression Debt

Payoff Channel

World Expansion

Narrative Drive

Reveal Depth

Knowledge Boundary

Character State

Chapter Intent
```

它们不是文学公式，

而是：

> **作者之间讨论复杂长篇结构时可以共享的语言。**

---

# 可复现的小说研究

如果同一种结构分析可以应用于大量作品，

创作者社群就有可能开始回答过去很难系统研究的问题：

> 一部长篇玄幻通常怎样打开新地图？

> 成长、战斗和资源之间通常怎样形成循环？

> 一项新能力平均多久会获得第一次真正验证？

> 哪些小说依靠升级维持追读？

> 哪些小说实际上依靠谜团而不是升级？

> 长篇作品在什么时候最容易产生疲劳？

这些问题不应该变成：

> “写小说的唯一公式。”

但可以成为：

> **可观察、可比较、可讨论的创作知识。**

---

# 从“模仿小说”到“学习结构”

Novel Studio 不希望建立：

```text
复制某部小说
```

的系统。

更有价值的方向是：

> **理解为什么不同小说有效，然后把这种知识抽象成可重新组合的结构。**

例如：

不是保存：

> 某小说第多少章发生了什么。

而是研究：

```text
它怎样建立成长期待？

怎样安排资源？

怎样扩大世界？

怎样让新能力产生未来期待？

怎样控制谜团揭露？

怎样避免几百万字以后失去动力？
```

这样一个社群共享的 Reference Corpus，

最终可能成为：

> **中文网文结构研究的开放知识层。**

---

# 创作者拥有自己的数据

Novel Studio 默认采用：

# Local-first

小说正文、设定和创作状态首先属于作者自己。

这对于创作者非常重要。

因为小说不仅是一份文本，

其中还包括：

* 未发布剧情；
* 世界秘密；
* 人物设计；
* 商业计划；
* 创作习惯；
* 长期 IP 规划。

Novel Studio 希望让作者能够：

> **真正掌握自己的创作数据和历史。**

---

# AI 不应该取代作者

Novel Studio 的目标不是：

> 让 AI 自动生产无限小说。

真正想探索的是：

> **AI 能不能扩大一个作者能够掌控的创作复杂度？**

过去一个作者可能能够稳定管理：

```text
几十个人物
一条主线
几个重要伏笔
```

未来借助这种系统，

一个作者可能管理：

```text
数百人物
多个势力
多层世界
长期成长系统
几十条线程
不同 Edition
百万字历史
```

但：

# 决定什么值得写的人仍然是作者。

---

# 开放创作基础设施

长期来看，Novel Studio 希望能够形成：

```text
Core Engine

Genre Adapters

Narrative Engines

Analysis Skills

Validators

Benchmarks

Reference Corpus

Community Extensions
```

不同创作者可以贡献：

* 新的分析工具；
* 新的 Genre Adapter；
* 新的可视化；
* 新的 Validator；
* 新的结构研究；
* 新的 Benchmark。

于是项目不再只是：

> 一个小说生成程序。

而可能逐渐成为：

> **一套开放的 AI 长篇创作基础设施。**

---

# 项目结构

Novel Studio 采用 **Source / Runtime Library / Deterministic Engine / Codex Skills / Web Studio** 分层结构。

```text
thegreatnovel/
│
├── README.md
│   项目首页与产品说明
│
├── Novel_Authoring_System_Constitution_V2.md
│   系统最高层设计原则与不可破坏边界
│
├── AGENTS.md
│   Codex / Agent 在仓库中的工程规则
│
├── PLAN.md
├── progress.md
├── task_plan.md
├── findings.md
│   计划、阶段进展、任务与审计记录
│
├── pyproject.toml
├── uv.lock
│   Python 项目定义与锁定依赖
│
│
├── book/
│   └── 原始小说来源
│
│   用户放入或导入的 TXT / Markdown 等源正文。
│
│   原则：
│   - 原始 Source 永久只读
│   - 不由续写、改写或 AI Workflow 直接修改
│   - 导入后由 Library 建立自己的受控运行状态
│
│
├── library/
│   └── 正式 Book Library
│
│   Novel Studio 的主要运行数据目录。
│
│   每一本书拥有独立：
│   - Book metadata
│   - Edition
│   - SQLite state
│   - Source Manifest
│   - Analysis
│   - Distillation
│   - Runtime Baseline
│   - World State
│   - Author Truth
│   - Planning
│   - Draft
│   - Revision
│   - Handoff / Operation
│   - Snapshot
│
│   新的正式流程默认写入这里。
│
│
├── workspace/
│   └── Legacy workspace
│
│   旧版运行目录。
│
│   主要用于：
│   - 兼容读取
│   - 旧项目迁移
│
│   不再作为新项目默认运行位置。
│
│
├── src/
│   └── novel_authoring/
│       │
│       ├── atlas/
│       │   Story Atlas、长篇结构与剧情地图
│       │
│       ├── author_control/
│       │   作者控制层：
│       │   Author Truth、Book Profile、Reveal、
│       │   作者意图与长期约束
│       │
│       ├── canon/
│       │   Canon Event / Projection 与正式事实层
│       │
│       ├── context/
│       │   创作 Context 构建与路由
│       │
│       ├── contracts/
│       │   跨 Workflow 的严格数据合同
│       │
│       ├── db/
│       │   SQLite、数据库基础设施与持久化
│       │
│       ├── distill/
│       │   小说文学蒸馏与九维 Knowledge Layer
│       │
│       ├── domain/
│       │   核心领域模型
│       │
│       ├── drafting/
│       │   Draft 生命周期与正文草稿处理
│       │
│       ├── ingest/
│       │   原始正文导入、章节解析与 Source 建立
│       │
│       ├── initialization/
│       │   Existing Novel 初始化
│       │
│       │   支持渐进式分析、Coverage 与按需补齐
│       │
│       ├── metrics/
│       │   小说指标、观察与 Hard / Soft Gate
│       │
│       ├── original/
│       │   原创新书 Genesis
│       │
│       │   一句话创意 → 阅读体验 → Foundation →
│       │   第一章创作
│       │
│       ├── planning/
│       │   Candidate Planning、Narrative Portfolio、
│       │   Innovation Reward、Narrative Debt 与 Payoff
│       │
│       ├── progression/
│       │   Progression Webnovel Engine
│       │
│       │   ├── contracts.py
│       │   │   Reader / Genre / Progression 等成长合同
│       │   ├── adapters.py
│       │   │   可组合的成长题材 Adapter
│       │   ├── interpretation.py
│       │   │   阅读体验与成长体系理解
│       │   ├── inference.py
│       │   │   Existing Novel 的成长结构推断
│       │   ├── projections.py
│       │   │   章节级 Progression State Projection
│       │   ├── resources.py
│       │   │   成长资源与 Opportunity
│       │   ├── debt.py
│       │   │   Progression / Showcase 等成长债务
│       │   ├── anticipation.py
│       │   │   读者当前期待的 Anticipation Surface
│       │   ├── diagnostics.py
│       │   │   成长与 Genre Drift 诊断
│       │   ├── scheduler.py
│       │   │   Progression-aware Serial Scheduling
│       │   └── workspace.py
│       │       作者侧成长工作台 View
│       │
│       ├── serial_kernel/
│       │   Chinese Serialized Webnovel Kernel
│       │
│       │   中文长篇连载网文的通用叙事驱动力层：
│       │   ├── models.py
│       │   │   Narrative Drive 等通用模型
│       │   ├── classification.py
│       │   │   Drive / 类型识别
│       │   ├── engines.py
│       │   │   Specialized Narrative Engine 接口与注册
│       │   └── diagnostics.py
│       │       Narrative Drive Drift 等通用诊断
│       │
│       ├── revision/
│       │   Revision Campaign 与正式改写流程
│       │
│       ├── rhythm/
│       │   节奏、章节结构与疲劳诊断
│       │
│       ├── runtime_baseline/
│       │   Source-derived Runtime Baseline
│       │
│       │   保存经原文证据验证的当前有效状态
│       │
│       ├── storage/
│       │   Book Library、文件布局、Registry 与存储
│       │
│       ├── validation/
│       │   Draft / Continuity / Genre / Progression 校验
│       │
│       ├── web/
│       │   Novel Studio Web Workbench
│       │
│       │   作者书库、正文、世界状态、成长、
│       │   剧情规划、Activity Center 等界面
│       │
│       ├── workflows/
│       │   Continuation、Revision、Handoff 等工作流
│       │
│       ├── cli/
│       │   模块化 CLI
│       │
│       ├── readiness.py
│       │   Studio / Continuation / Revision Readiness
│       │
│       ├── pending_actions.py
│       │   可恢复的作者操作
│       │
│       └── edition.py
│           Edition 与正式叙事版本管理
│
│
├── .agents/
│   └── skills/
│
│   Codex Desktop 使用的小说创作 Skills。
│
│   当前包括：
│   - initialize-existing-novel
│   - bootstrap-original-novel
│   - continue-novel
│   - continue-novel-batch
│   - distill-novels
│   - process-novel-handoff
│   - bootstrap-story-atlas
│   - refresh-story-atlas
│   - render-story-atlas-assets
│   - analyze-novel-rhythm
│   - review-novel-metrics
│   - ...
│
│   LLM 主要通过这些受控 Skill 位于系统边缘工作，
│   而不是直接修改 Runtime Authority。
│
│
├── .codex/
│   Codex 项目级配置与本地开发辅助配置
│
│
├── config/
│   项目配置与运行参数
│
│
├── scripts/
│   Benchmark、迁移、验收与工程辅助脚本
│
│
├── benchmark/
│   ├── acceptance reports
│   ├── quality benchmarks
│   └── artifacts/
│
│   保存：
│   - Progression Kernel 验收
│   - Narrative Drive 验收
│   - Continuation Benchmark
│   - Innovation Benchmark
│   - 浏览器截图与可审计实验产物
│
│   Benchmark 与正式作者书库保持逻辑隔离。
│
│
├── audit/
│   历史审计材料与工程检查结果
│
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATA_MODEL.md
│   ├── EDITION_MODEL.md
│   ├── ORIGINAL_NOVEL_GENESIS.md
│   ├── CHINESE_SERIALIZED_WEBNOVEL_KERNEL.md
│   ├── PROGRESSION_WEBNOVEL_KERNEL_ARCHITECTURE.md
│   ├── STORY_ATLAS_WORKFLOW.md
│   ├── REVISION_WORKFLOW.md
│   ├── CODEX_CONTINUATION_WORKFLOW.md
│   ├── AUTHOR_WORKBENCH.md
│   ├── WINDOWS_QUICKSTART.md
│   ├── architecture/
│   ├── operations/
│   ├── audits/
│   ├── reference/
│   └── user/
│
│   产品、架构、数据模型、Workflow、
│   用户使用说明与设计决策的主要文档入口。
│
│
├── inspirations/
│   外部灵感、研究材料与架构参考
│
│
├── examples/
│   示例配置、输入与使用案例
│
│
└── tests/
    自动测试

    覆盖：
    - Unit
    - Integration
    - Workflow
    - Continuity
    - Revision
    - Initialization
    - Progression
    - Serial Kernel
    - Web / UX
    - Safety boundaries
```

---

## 核心运行边界

从目录结构上，可以把整个项目理解成五层：

```text
book/
原始来源
只读
        ↓
library/
正式运行状态
        ↓
src/novel_authoring/
确定性创作引擎
        ↓
.agents/skills/
LLM / Codex 创作能力
        ↓
web/
作者操作界面
```

其中最重要的原则是：

```text
Source ≠ Runtime

Runtime ≠ Draft

Draft ≠ Canon

AI Proposal ≠ Author Truth

Benchmark ≠ Author Project
```

---

## 当前叙事内核

当前核心架构已经从单纯的小说续写进一步演化为：

```text
Chinese Serialized Webnovel Kernel
        │
        ├── Narrative Drive
        │
        └── Specialized Narrative Engines
                │
                └── Progression Engine
                        │
                        ├── Reader Experience
                        ├── Genre Contract
                        ├── Progression Contract
                        ├── Progression State
                        ├── Resource Economy
                        ├── World Expansion
                        ├── Anticipation Surface
                        ├── Progression Debt
                        └── Serial Scheduler
```

其中：

**Chinese Serialized Webnovel Kernel** 负责理解：

> 这部长篇小说主要依靠什么持续产生下一章期待？

**Progression Engine** 则是目前最成熟的 Specialized Narrative Engine，重点处理：

* 玄幻；
* 仙侠；
* 高武；
* 科幻玄幻；
* 进化；
* 能力成长；
* 神秘学晋升；

等具有长期成长结构的作品。


---

# Roadmap

当前重点：

* Reader Experience Contract；
* Narrative Drive；
* Progression Engine；
* Genre Contract；
* World Expansion；
* Resource Economy；
* Payoff Engine；
* Narrative Debt；
* Serial Scheduler。

下一阶段：

* Mystery Engine；
* Career Engine；
* Strategy Engine；
* Competitive Engine；
* Survival Engine；
* Relationship Engine；
* Multi-Engine Scheduling；
* Structural Reference Corpus。

长期目标：

# 建立一个真正能够辅助作者创作数百万字中文长篇连载小说的专业创作系统。

不是：

> 一个更复杂的 Prompt。

也不是：

> 一个自动写小说的机器人。

而是一套：

# AI-native Creative Infrastructure

让作者拥有：

更大的世界，

更长的故事，

更复杂的人物，

更可靠的记忆，

以及对自己作品更强的控制力。
