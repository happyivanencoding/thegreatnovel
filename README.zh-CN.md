# TGN — TheGreatNovel

简体中文 | [English](README.md)

**一个面向 AI 原生长篇小说的开源长时程叙事引擎。**

大多数 AI 写作工具优化的是下一段文字。**TGN 想优化的是整本书。**

TGN 把作者意图转化为可持续存在的故事权威，再让模型在这个边界内规划、写作、修订和扩展。目标不是让模型偶尔写出一章漂亮正文，而是让人物在几十章后仍然像同一个人，让世界始终比主角更大，让能力、关系、身份与旧选择能够长期复利，让真正未知的谜团可以继续未知，也让很久以前发生的事持续改变未来还能发生什么。

> TGN 仍处于活跃研发阶段。它不是一组 Prompt 的集合，而是在完整小说生成、失败分析和反复 production 实验中逐步建立起来的系统。

## 我们在解决什么

LLM 可以写出很漂亮的场景，却仍然很容易写坏一本小说。

长篇里真正难的通常不是语法，而是**结构漂移**：模型会悄悄改掉规则，把人物压缩成最近几章的行为，忘记旧关系为什么重要，把世界观写成布景，或者让每个新世界都围着主角量身定制，最后整个世界失去独立生命。

TGN 的核心判断是：

> **长篇 AI 小说需要的不是更长的 Prompt，而是一套 Story Authority Architecture。**

## TGN 如何理解一本小说

```text
作者意图
    ↓
可选 Premise Search
    ↓
World Authority + Character Authority
    ↓
Story Program
    ↓
Horizon Plan
    ↓
4–6 章 Batch Runtime
    ↓
Authority-Preserving Revision
    ↓
Canon + Story State
    ↺
World Expansion / Story Refresh
```

最重要的边界很简单：上游阶段可以决定故事，下游阶段负责把已经批准的故事真正写出来，而不是在写正文时悄悄重新设计整本书。

## TGN 的不同之处

### 先建立 Authority，再写正文

世界规则、人物身份、长期承诺、已发生 Canon 和已经批准的剧情决定，与正文分开保存。Writer 得到的是经过裁剪的当前 Authority，而不是被要求把整本小说全部塞进上下文里再“尽量别写错”。

### 世界不是为了主角才存在

TGN 在 Story Program 第一次碰撞之前，刻意把世界构建与主角优化分开。世界可以拥有自己的角色、机会、冲突和未来；即使主角选择另一条路线，这些东西仍然能够继续发生。

### 长篇需要纵向复利

换地图不应该等于重开游戏。TGN 会让能力、关系、身份、敌人、资产、知识、社会位置和未解问题跨越不同 Horizon 留下来，并在新的条件下重新获得意义和价格。

### 允许真正的未知存在

并不是所有 Mystery 都应该在大纲阶段被提前解释。TGN 可以明确保存“作者目前也不知道”的状态，只在下一段故事真的需要时决定最小的一层答案，再通过正文里的事件把它变成读者事实。

### Batch 写作，而不是逐章失忆

正文以短 Batch 连续生成，让 Writer 能够真正看到数章之间的叙事惯性。随后由独立 Authority pass 只修复局部事实漂移，而不是把 Revision 变成第二个可以重写故事的作者。

### Retrieval 负责扩大可能性，不负责制造事实

TGN 可以连接外部 Story Craft 知识库，但检索结果始终位于 Canon 之外。它可以帮助系统看到更多创作可能性，却不会因为“被检索到了”就自动成为小说世界里的事实。

## 当前公开仓库包含什么

- 本地 FastAPI 作者工作台
- Premise、World、Character、Story Program、Outline 等结构化工作流
- 持久 Canon 与 Story State
- 长篇 World Expansion 与 Story Refresh
- Batch 章节生成与 Authority-preserving Revision
- 可选外部 Story Craft Retrieval 接口
- 针对 Runtime 与 Authority 行为的回归测试

公开的 `main` 分支刻意保持为干净的 production surface。内部研究文档、私有语料、实验 provenance 和项目交接材料不会随 release 一起公开。

## Quick Start

需要 Python 3.11+。

```bash
python -m venv .venv
```

激活环境后安装：

```bash
pip install -e ".[test]"
```

启动本地作者工作台：

```bash
story-mvp
```

打开：

```text
http://127.0.0.1:8000
```

运行测试：

```bash
pytest
```

## 仓库结构

```text
src/story_mvp/   Engine、Runtime、Prompt、Storage 与作者工作台
books/           已随公开 release 保留的示例 / workspace artifact
tests/           Runtime 与回归测试
```

## Direction

TGN 最终想做的是一种 **book-scale generative system**：它既能保留一本小说长期的创作身份和因果记忆，又不会为了控制一致性而牺牲惊喜、扩张与作者真正的选择权。

目标不是做一个“完全可控的文本生成器”，而是让：

> **句子层面的自由，与整本小说尺度上的连续性，可以同时成立。**

## 第三方材料

TGN 的许可证只适用于本项目有权许可的材料。第三方库、参考作品、数据集、模型服务和受版权保护的源文本仍受各自许可证与条款约束。本仓库不会授予任何第三方版权小说或私有语料的权利。

## License

TGN Engine 使用 **GNU Affero General Public License v3.0 only**（`AGPL-3.0-only`）。

完整许可证见 [`LICENSE`](LICENSE)。
