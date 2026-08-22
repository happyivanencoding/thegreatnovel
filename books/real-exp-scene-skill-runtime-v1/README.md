# Scene Skill Runtime v1 — Deterministic Wiring Experiment

Base branch: `principal_dev_new_sys`
Runtime commit: `dd68a6d`
Growth projection fix: `a211bd7`

## 目的

只验证 Scene Skill v1 的运行期接线，不评价 prose 质量：Curator Prompt 能看到紧凑 Scene Skill Catalog；冻结选择后，Primary Writer 只按需得到 1 个 Primary 与可选 1 个 Secondary；原始选择控制区块不会重复泄漏到 Writer；Specialist 不接收 Active Scene Skill。

## 冻结样本

- Chapter 2：沿用 `real-exp-opening-reader-first-fresh-v1` 的冻结 Chapter 1 后状态、Chapter 2 Director/Curator 与计划；冻结选择 `social_bargain_decision`。
- Chapter 3：沿用 `real-exp-human-reaction-ch3-v1/after-v2` 的冻结 Director/Curator 与修正后的取牌回线事实；起点使用原实验 Chapter 2 State Delta；冻结选择 `trial_challenge + combat`。

## 结论边界

本机 Story MVP OpenAI executor 当前 `configured=False`，且没有独立 LLM worker，因此本目录不冒充“同模型 prose benchmark”。这里是生产 `generate_prompt()` 的真实 deterministic Prompt 对照。后续一旦 executor 有模型配置，只需基于这些冻结 Prompt 各执行一次 Primary，即可比较 prose；不需要新增 harness、Agent、Hard Gate 或 validator。

## 结果

Chapter 2：before 16453 chars → after 16935 chars，增量 482 chars，只注入 `social_bargain_decision`。
Chapter 3：before 19231 chars → after 19965 chars，增量 734 chars，只注入 `trial_challenge` 与 `combat`。

所有 wiring assertions 均通过，详见各目录 `verification.json` 与 `prompt_diff.patch`。
