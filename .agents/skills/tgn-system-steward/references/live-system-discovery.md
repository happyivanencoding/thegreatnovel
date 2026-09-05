# Live System Discovery

本 Agent 不保存固定 production snapshot。每次 TGN 系统协作任务先全文读取项目根目录 `DEEP_CONTEXT_HANDOFF_FINAL.md`，再全文读取 `PROJECT_RULES.md`，在作出决定或修改前完成。可连续分段读取，截断处续读，不漏段；检索、摘要或其它 Agent 读过均不能替代本人阅读。

这两份必读完成后才使用 **bounded discovery**：默认预算为 `git status/log` + 2—4份任务相关 current docs + 用户指定 artifact。只有发生冲突或证据不足时才扩大范围。此协作入口不改变生产节点输入合同，不把交接历史送入 Writer / Curator。

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

系统改动后在同一任务同步相关 docs、审计技能与最终交接文件。docs 描述当前行为，技能保留方法与相关发现入口，交接记录决策依据、验证范围和未解决项；各自更新，不复制整套快照。

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

如果问题涉及“长任务为什么停住 / 必须回来问好了吗才继续”，把**进程宿主**与**小说 pipeline**分开审计。先确认现有 runner 是否已经包含正常的 validator / retry / error handling，再确认它是不是被当前 ChatGPT turn、AgentDock command session 或其它短生命周期父进程托管。若 runner 语义本身正确而只是父进程结束后被回收，最小修法是换成持久 Job Host；不要因此新增 Recovery Agent、Reviewer、Judge 或第二套 workflow。反过来，持久宿主只能保证 runner 活着，不能拿它掩盖真实的 Story / Outline / Authority transport 缺陷。

如果用户采用 **final-output-only / hands-off** 工作方式，区分**用户交互审批**与**内部 Authority Freeze checkpoint**。用户不逐项点击 World / Character / Story，不等于这些边界应该被删除；自动 Production Run 可以由已获任务授权的 TGN operator 完成选择、Save / Adopt / Freeze 和正常重试，随后继续下游。审计时检查的是每个下游 Agent 是否只读到已经冻结、验证通过的正确上游，而不是“页面上有没有作者批准按钮”。反过来，也不能因为 operator 被授权自动推进，就把任意模型 Response 直接当 Canon 或绕过现有 validator。手工 Author Workspace 应被视为高级检查 / 干预面，而不是默认生产路径。

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
