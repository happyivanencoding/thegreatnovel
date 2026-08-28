# TGN — TheGreatNovel

简体中文 | [English](README.md)

TGN 是一个实验性的长篇 AI 小说创作系统，重点解决长期规划、章节可控执行、连续性记忆，以及可复用的故事创作知识。

> 当前状态：持续开发中。系统架构与 Prompt 仍会根据真实生成实验继续迭代。

## TGN 做什么

TGN 不让一个模型从设定一路包办到正文，而是把不同尺度的问题拆成职责明确的阶段：

```text
作者方向
→ Fantasy Seed
→ World Vision
→ Story Program
→ Outline
→ Director
→ Context Curator
→ Primary Writer
→ State Extraction
```

核心目标是：让上游明确决定“这本书是什么、接下来发生什么”，让下游专注执行，而不是在写章时偷偷重做整本书。

## 核心设计原则

- **Fantasy First**：先保证读者真正想拥有、进入或成为的幻想，以及主角主动性，再考虑系统与程序完整性。
- **Few Deep Rules > Many Hard Gates**：优先少量深规则和清晰职责，不堆 Reviewer、评分器与门禁。
- **Supporting Logic Must Not Automatically Become Story Engine**：合理性、机制、治理、验证、运营等可以支撑故事，但除非题材明确需要，否则不能反客为主。
- **Story-bearing Texture > Decorative Density**：正文的丰富感来自承载故事的具体细节，而不是形容词、比喻和五感堆积。
- **Planning 与 Prose 分责**：Director 决定发生什么，Writer 负责把已经批准的事件写成小说。
- **记忆保持轻量且事实化**：State Extraction 只记录正文真正发生的事，不替未来剧情做推测。

## GBrain

TGN 可以选择性接入本地 GBrain 知识库，用于 World Vision、Story Program、Outline，以及离线蒸馏后的 Scene Skills。

GBrain 是 **Optional Inspiration**，不是 Canon，也不是创意权威。原始参考材料不应直接进入 Primary Writer。

本仓库不要求、也不包含私人或本地原著语料库。

## 项目结构

```text
src/story_mvp/   应用、Prompt、Runtime 与存储逻辑
books/           小说工作区与生成实验
tests/           回归与 Runtime 测试
```

公开 `main` 分支只发布 production/runtime 代码，不包含内部架构、审计与交接文档。

## 快速开始

需要 Python 3.11+。

```bash
python -m venv .venv
```

激活虚拟环境后安装项目：

```bash
pip install -e ".[test]"
```

启动本地应用：

```bash
story-mvp
```

然后访问：

```text
http://127.0.0.1:8000
```

运行测试：

```bash
pytest
```

## 第三方材料

TGN 的许可证只覆盖项目有权授权的内容。第三方依赖、参考作品、数据集、模型服务和受版权保护的原始文本，仍分别受其自身许可证、版权和服务条款约束。本仓库的开源许可证不授予任何第三方小说原文或私人语料库的权利。

## License

TGN Engine 采用 **GNU Affero General Public License v3.0 only**（`AGPL-3.0-only`）授权。

完整许可证见 [`LICENSE`](LICENSE)。
