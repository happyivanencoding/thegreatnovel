# Live System Discovery

本 Agent 不保存固定 production snapshot。每次严肃审计先确认当前系统实际状态，但默认使用 **bounded discovery**：动态读取是为了避免过时，不是为了每次遍历整个仓库。

默认预算：`git status/log` + 2—4份任务相关 current docs + 用户指定 artifact。只有发生冲突或证据不足时才扩大范围。

## 1. Worktree

优先检查：

```text
git status --short --branch
git log --oneline -8
```

目的：

- 识别并行 agent / 用户未提交修改；
- 知道最近刚冻结了什么；
- 防止把几小时前的架构当当前 production；
- 防止误 stage unrelated work。

## 2. Current Methodology

读取任务相关的最新文档，不假定文件名永远不变。

常见入口：

- product direction；
- pipeline methodology / values；
- current architecture freeze doc；
- GBrain methodology；
- scene / prose skills。

如果文档与代码冲突，以实际 production path 为事实，并指出文档需要同步。

## 3. Actual Production Path

不要仅凭 Prompt 文本推断 pipeline。

确认：

- storage artifacts；
- API modes；
- workflow dependency / stale graph；
- prompt dispatcher；
- retrieval routing；
- UI approvals；
- tests。

实验目录里的模块只有在实际 import / route 中被调用才算 production。

## 4. Experiment Status

用户说“这个实验完成了吗”时，不只看文件存在。

检查：

- 原始 model output 是否完整；
- materialized artifact；
- audit / results；
- tests；
- commit / push（如果要求）；
- GBrain import/embed（如果涉及）。

识别：

- staging；
- materialized but not imported；
- imported but not embedded；
- full PASS / COMPLETE。

## 5. GBrain Live State

涉及 GBrain 时优先检查：

```text
gbrain stats
gbrain list / query / get
```

关键区分：

- source-specific DNA；
- cross-book mechanisms；
- `active_inspiration: true/false`；
- `REFERENCE_ONLY / HOLD / PILOT`；
- lane metadata；
- selector-only private prototype。

Runtime accepted bundle 比“库里有这张卡”更重要。

## 6. Prompt Visibility vs Retrieval Visibility

Authority isolation 要同时检查两条路：

1. generation prompt 看见什么；
2. GBrain retrieval brief/query 看见什么。

Prompt 隔离而 retrieval brief 仍吃 full context = 侧漏。

## 7. Current Model Routing

模型路由会变化。不要把 Skill 内任何价格或型号当永久事实。

审计模型实验时动态确认当前项目 default 和用户最新指定。

判断至少分开：

- quality；
- wall-clock；
- cost。

不要把“更快”说成“更便宜”。

## 8. Production vs Historical Artifacts

历史目录中可能保留：

- Fantasy Seed；
-旧 Character schema；
-旧 100章固定窗口；
-旧 Writer A/B/C；
-被废弃 reviewer/scorer。

这些用于研究，不自动构成当前规范。

如果用户问“以前我们删了什么”，才主动查 git history / old prompts。

## 9. Personal Prototype Boundary

私人 Human Prototype：

- 默认 retrieval 必须 0；
- 只有显式 selector 才进入 Human Seed 实验；
- 不进入 World / Power；
- 不成为全局 Human prior；
- 不从匿名卡反推现实身份或原始私人 source。

对私人原型实验的质量审计可以讨论已匿名化的欲望/行为/关系结构，但不要扩大现实个人事实。

## 10. When Context Is Missing

如果当前代码/文件足以解析，不先问用户重复提供。

如果任务很大但可 best-effort：

- 先完成能确定的部分；
- 明确剩余不确定性；
- 不以“需要更多信息”为理由停住整个任务。
