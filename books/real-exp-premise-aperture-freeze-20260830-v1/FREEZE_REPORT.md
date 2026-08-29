# Premise Aperture F1–F5 Production Freeze Report

日期：2026-08-30

状态：`FROZEN / OPTIONAL / AUTHOR-GATED / PRODUCTION WIRED`

基线提交：`origin/principal_dev_new_sys@5654730f`

研究证据：`books/real-exp-premise-aperture-20260829-v1/RESULTS.md`

## 1. 冻结决定

作者明确批准冻结以下五项：

1. **F1｜Authority 冻结前的 Non-Canon Premise Search**；
2. **F2｜Single-Agent Premise Forge 一次生成 S1 / S2 / S3 三张完整候选**；
3. **F3｜fresh-context Independent Premise Authority Compiler**；
4. **F4｜作者选择、手动处理冲突或显式跳过；不自动 selector**；
5. **F5｜deterministic lane-specific frozen contracts + fail loud + raw card runtime cutoff**。

正式开书链：

```text
作者方向
  →（可选）Premise Forge S1/S2/S3
  → Independent Compiler
  → 作者批准 / 显式跳过
  → World / Power / Human / Story 四条确定性合同
  → 现有 Split Authority 链
  → Outline / chapter 不读取 raw Premise
```

没有恢复旧统一 Fantasy Seed，没有 Character Composer LLM，没有自动 selector、Repair Loop、章节期 Reviewer / Scorer 或 Premise Agent。

## 2. Production State Machine

| 状态 | 下游 Authority |
|---|---|
| `not_started` | 允许原 Split Authority 路径 |
| `skipped` | 允许原路径；跳过是作者显式决定 |
| `candidates_ready / selected / compiled / compiler_blocked` | 阻止 World / Power / Human / Story 的生成、保存与批准 |
| selected strict `PASS` + exact snapshot match | 可以由作者批准 |
| `approved` | 生成四条 frozen lane contract，继续现有链 |
| World Vision 已作者批准 | Premise 决定冻结，不能再改候选、重编或跳过 |

`CONDITIONAL PASS / FAIL` 只能返回作者；系统不自动换候选或修复。

## 3. Compiler Input Binding

冻结过程中发现并修复一个真实可达的版本绑定问题：若 snapshot 只在 Report 保存时生成，作者可以在 Compiler Prompt 发出后编辑候选，导致旧报告错误绑定到新文本。

当前实现：

- batch / selected Compiler Prompt 生成时立即写入 `PREMISE_COMPILER_INPUT.md`；
- Report 保存只验证 scope，不重写 snapshot；
- 当前 selected card 与 snapshot 不一致时，即使旧 Report 为 strict `PASS`，也不能批准；
- 必须重新执行 selected-card Compiler；
- 直接比较文本，不引入哈希、指纹或额外兼容层。

## 4. Authority Visibility

| Lane | 输入 |
|---|---|
| World | World-only + protagonist-blind public Interface |
| Power | literal Ontology + Initial Scale Position + trigger / target coverage / action / carrier / root boundary |
| Human | literal Ontology + exact T0 Origin + Initial Scale Position；看不到特殊 Power / Future Story |
| Story | Authorities 批准后第一次读取完整 Promise / Interface / immutable points |

Story Program 后，Outline、Director、Curator、Primary、Authority Reviser、State 与章节 Runtime 不再读取 raw Premise Card。

Workflow 中唯一正式节点是 `premise.contract`。候选、Selected Card、Compiler Input 与 Compiler Report 是作者工作区文件，不成为第四 Authority。

## 5. Author Workspace

UI 已加入最小 Premise 工作区：

- 生成 Forge Prompt；
- 应用并保存 S1 / S2 / S3；
- batch Compiler；
- 作者按钮选择 S1 / S2 / S3；
- 编辑并保存 selected card；
- selected-card Compiler；
- 保存 Compiler Report；
- 作者批准或显式跳过；
- 批准后查看四条只读 lane contract。

UI 没有自动 selector 或 Repair 按钮。World 批准后编辑与操作控件冻结；后端也独立拒绝绕过。

## 6. Implementation

核心代码：

- `src/story_mvp/premise_aperture.py`：Forge / Compiler Prompt、解析与 deterministic lane projection；
- `src/story_mvp/premise_workflow.py`：状态机、持久文件、snapshot、批准/跳过与合同写入；
- `src/story_mvp/app.py`：API / Prompt 路由与 author gate；
- `src/story_mvp/character_prompts.py`：World / Power / Human / Story lane injection；
- `src/story_mvp/storage.py`：Authority 保存/批准门禁与 creative state invalidation；
- `src/story_mvp/workflow_state.py`：`premise.contract` 与 stale graph；
- `src/story_mvp/templates/index.html`、`src/story_mvp/static/app.js`：作者工作区。

持久文件：

```text
PREMISE_CANDIDATES.md
SELECTED_PREMISE.md
PREMISE_COMPILER_INPUT.md
PREMISE_COMPILER_REPORT.md
PREMISE_SKIPPED.md
PREMISE_CONTRACT.md
PREMISE_WORLD_CONTRACT.md
PREMISE_POWER_CONTRACT.md
PREMISE_HUMAN_CONTRACT.md
PREMISE_STORY_CONTRACT.md
```

## 7. Documentation / Skill

已同步：

- `PROJECT_RULES.md`；
- `README.md`、`README.zh-CN.md`；
- `docs/PREMISE_APERTURE.md`；
- `docs/PIPELINE_METHODOLOGY_AND_VALUES.md`；
- `docs/MVP_PRODUCT_DIRECTION.md`；
- `docs/SPLIT_CHARACTER_AUTHORITY.md`；
- `docs/AUTHOR_WORKSPACE_UI_SPEC.md`；
- `DEEP_CONTEXT_HANDOFF_FINAL.md`；
- `tgn-system-steward` **v0.3.20**。

Steward 新增长期审计能力：Optional Premise 状态机、Prompt-time Compiler snapshot、strict PASS、lane visibility、Workflow authority、raw-card runtime cutoff 与 no-repair-loop 边界。

## 8. Verification

- JavaScript syntax：PASS；
- Python compile：PASS；
- Premise / Workflow / UI focused regression：**62 passed**；
- 全仓测试：**409 passed**；
- 真实 Chapter Prompt raw-card cutoff 回归：PASS；
- Skill authoring lint：PASS，0 errors / 0 warnings；
- Skill package validation：PASS；
- Skill v0.3.20 install + activate：PASS；
- Independent Steward smoke：**PASS**，见 `STEWARD_SMOKE.md`。

## 9. 仍为 Research-only / Rejected

- 四轴完整正交碰撞：拒绝；
- Two-Bet Voltage Budget：research-only；
- 模型/Judge 自动 selector：拒绝；
- Selected Premise 自动 Repair：一次真实测试漏掉 Changed Verbs，research-only；
- 旧统一 Fantasy Seed：拒绝恢复。

## 10. Residual Boundary

这次冻结解决的是**大胆完整前提的搜索、选择、可编译性与 Authority 保真**。它不自动保证每一张候选都优于强 baseline，也不解决正文 prose、章节速度或百章后玩法是否重复；这些仍由作者选择、Story Program、Outline 与章节 Runtime 承担。
