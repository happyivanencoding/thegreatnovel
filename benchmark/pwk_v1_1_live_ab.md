# PWK V1.1 Live A/B

日期：2026-08-12

## Evidence taxonomy

本报告严格区分：

- automated test：pytest/静态门禁；
- fixture：测试构造 JSON；
- live semantic output：本轮模型真实生成；
- browser：真实本地服务与浏览器；
- human review：人工盲评。

Fixture 与单测不能替代 Live；Live 也不能替代作者批准或人工文学判断。

## Original Novel A/B

### A：旧链

- book：`original-9f85ca12570b`
- authentic handoff：`handoff_db547c5caba91f6ff583ed97`
- 无 Kernel Contracts
- 0 chapters / 0 Canon

### B：PWK V1.1

- book：`pwk-v11-original-b-live`
- semantic bootstrap handoff：`handoff_0d9646742721bdfdbe980b46`
- 作者侧 Reader Experience 已确认
- 生成 Reader/Genre/Narrative Drive/Progression 等 proposal
- 0 chapters / 0 Canon
- 浏览器真实呈现三条成长型 Story Foundation，核心循环包括材料、代价、危险验证与世界扩张

模型生成的两章 A/B prose 位于：

- `benchmark/artifacts/pwk_v1_1_live_ab/original/variant-a/`
- `benchmark/artifacts/pwk_v1_1_live_ab/original/variant-b/`

限制：这些 prose 是 live semantic output，但不是正式 Chapter Contract → Draft artifact；不得描述为 Canon continuation。

## Existing Novel A/B

### A：既有 live baseline

复用已完成的真实 `benchmark/live_phase5/runs/live-v1/`：A=`DISTILL_ONLY`，两章候选与正文均通过旧十项 Validator，N+2 使用 N+1 provisional context；未获得作者批准，未写 Canon。

### B：PWK V1.1 production wiring

- book：`phase5-live-b-050`
- context：chapter 50 → target 51
- Formal handoff：`handoff_7d20458a61b76806c794921f`
- Aggregate：`planning-aggregate_667057dec2c81abe70d4c518`
- Candidate task：`plan_ffe0e06d113a1f02f1156d17`
- 3 live semantic candidates → Python verification → existing Hard Gate/Score/Innovation
- selected：`pwk-b-fog-bearing-mark`
- Chapter Contract：`contract_40141b35706e489cfe9c8041`
- Live Draft revision 2：`draft_8a313c3153f4b1558fe3a938`
- Validation：10/10 pass
- events/canon/chapters after validation：0 / 0 / 50

限制：新 B 目前只有 N+1 正式链，没有完成作者批准后的 N+2；因此不能把它称为完整 Existing Novel A/B 闭环。

## Browser evidence

- `browser/01-live-b-readiness-gate.png`：已有书 Live B 被真实初始化门禁拦截；没有伪造 READY 状态换取截图。
- `browser/02-original-live-b-reader-drive.png`：原创新书 Live B 的真实 Story Foundation 页面，显示 0 正式章节与三条成长方向。
- `server.stdout.log` / `server.stderr.log`：本地服务启动记录。

已有书 verified-evidence Workbench 截图仍未完成，因为 Live B 没有达到产品规定的初始化 readiness。该项保留为 P1 blocker。

## Anti-leak 与人工评审

- 生产 Prompt/Skill fixture entity scan：CLEAR
- Live Draft semantic policy leak：CLEAR
- semantic discovery future-chapter evidence：自动化拒绝
- human blind review：`PENDING`

由于没有独立人工评分，本报告不声称 B 的文学质量优于 A；只确认 B 的事实、边界、成本和状态变化更可审计。
