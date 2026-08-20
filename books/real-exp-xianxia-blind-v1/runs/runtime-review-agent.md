# 全新玄幻修仙盲测 Runtime Review

审查范围：仅使用 `chapter-0001` 至 `chapter-0005` 下的 `manifest.json`、manifest 中记录的节点 Prompt/Response 字符数、`selected_specialists`、Integrator 的 Patch/运行审计、State Delta 输出与 approval，以及目录文件名层面的恢复记录检查。

未对文笔、正文质量或读者接受度评分；以下只判断运行时上下文、调用选择、Patch 合并、状态推进和恢复证据。

## 结论

- 上下文没有缩小。五章总 Prompt 字符数从 37,640 增至 70,595；`primary` 从 5,445 增至 16,359，Integrator 从 6,253 增至 10,568，State Delta 从 5,436 增至 9,236。所选 Specialist 的 Prompt 合计也从 10,212 增至 19,578。
- `hybrid_selective` 确实减少了 Specialist 调用：每章只选 2 个、跳过 2 个，五章共 10 次 Specialist 调用。相对每章运行全部 4 个 Specialist 的上限，少 2 次/章、共少 10 次；但本批没有另一种 writer mode 作为控制组，所以不能据此证明相对其他真实模式的因果节省。
- 最有价值的是 Action Specialist。五章均选中，且每章都有被 Integrator 采用的 Action 内容。Dialogue Specialist 在第 2、5 章被选中，提出的 Patch 均被采用；Opening Specialist 的价值不稳定，第 1 章虽被选中但没有有效 Patch，第 3、4 章的 Patch 有效；Emotion Specialist 五章均未调用，当前没有价值证据。
- Integrator 没有显示为不必要调用。五章均有至少一个有效专项 Patch，`final_source=integrator`，Integrator 每次一次运行并为 `adopted`。但系统也没有展示“无有效 Patch 时跳过 Integrator”的路径，因此只能判定本批调用有输入依据，不能判定它具备按需跳过能力。
- Ledger/单节点恢复无法验收。五个 run 目录没有名为 recovery、restore、resume 或 ledger 的记录文件；所有节点均为一次尝试，没有重试或恢复事件。现有 manifest 的逐节点状态只能证明节点被拆开记录，不能证明 Ledger 支持从单个节点恢复。
- State Delta v2 在内容层面基本消除了旧状态尾巴：Active Scene State 与 Persistent Canon 随章节推进，且第 5 章明确覆盖第 4 章的旧地点、未使用回火环、无独立炉心/接单资格和无敌人等旧状态。但第 4 章的 State Delta Response 缺少规定的 `# State Delta Audit` 标题；同章 approval 仍写“应用本次 State Delta v2”。因此语义更新有效，格式门禁与 approval 不一致，不能判定五章 State Delta 全部完整通过。

## 每章运行与字符数证据

记法为 `Prompt/Response` 字符数。`D`=director，`C`=curator，`P`=primary，`O`=opening，`Di`=dialogue，`A`=action，`E`=emotion，`I`=integrator，`SD`=state_delta。

| 章节 | mode | selected_specialists | 实际节点调用 | 总 Prompt / Response | 节点 Prompt/Response |
|---|---|---|---:|---:|---|
| 1 | hybrid_selective | opening, action | 7 | 37,640 / 10,720 | D 2,944/800；C 7,350/1,772；P 5,445/2,923；O 4,645/54；Di 0/0；A 5,567/332；E 0/0；I 6,253/3,142；SD 5,436/1,697 |
| 2 | hybrid_selective | dialogue, action | 7 | 54,595 / 13,829 | D 5,258/943；C 9,663/3,815；P 10,577/2,985；O 0/0；Di 7,598/660；A 8,131/596；E 0/0；I 7,398/3,189；SD 5,970/1,641 |
| 3 | hybrid_selective | opening, action | 7 | 57,556 / 14,926 | D 4,985/1,000；C 9,858/2,816；P 12,398/3,778；O 6,605/532；Di 0/0；A 8,269/818；E 0/0；I 8,400/4,231；SD 7,041/1,751 |
| 4 | hybrid_selective | opening, action | 7 | 61,650 / 16,667 | D 5,128/748；C 9,520/3,967；P 14,189/4,428；O 7,184/455；Di 0/0；A 9,232/1,033；E 0/0；I 8,790/4,592；SD 7,607/1,444 |
| 5 | hybrid_selective | dialogue, action | 7 | 70,595 / 21,358 | D 5,195/855；C 9,659/4,790；P 16,359/5,994；O 0/0；Di 8,843/860；A 10,735/807；E 0/0；I 10,568/5,901；SD 9,236/2,151 |

每章 7 次调用由 director、curator、primary、2 个选中的 Specialist、Integrator、State Delta 组成；另外两个 Specialist 的 Prompt/Response 均为 0/0、attempts 为 0、status 为 `skipped`。

## 上下文是否缩小

没有。总 Prompt 字符数在五章中逐章上升，只有 director 在第 3 章比第 2 章略低，不能改变整体趋势。增长最明显的是 `primary`：5,445 → 10,577 → 12,398 → 14,189 → 16,359；这说明随着章节推进，主写作上下文仍在累积。Integrator 与 State Delta 的输入也同步增长，而不是变成固定的局部上下文。

因此，本批可以确认 Specialist 选择层变窄，但不能确认整个 Runtime 上下文变窄；目前更准确的描述是“少调用 Specialist，但保留的主链上下文持续增大”。

## Specialist 价值

### Action Specialist

Action 是唯一五章全选的 Specialist，也是五章均有采用记录的 Specialist：

- 第 1 章：Action Patch 1 被采用，补齐物件从退回箱边角到相邻木台的空间移动。
- 第 2 章：Action Patch 1、2 均被采用，补足复验中的空间指代和裂口停止位置。
- 第 3 章：Action Patch 1 的有效内容与 Opening Patch 2 合并，Action Patch 2、3 也被采用，重点是先后淬冷、保留材料和风门边界。
- 第 4 章：Action Patch 1、2、3 均被采用，重点是冷却位置、落锤站位/接钳动作以及回弹期间的裂损阶段。
- 第 5 章：Action Patch 1、2 均被采用，重点是首次受力定位和宁枝借车辕卸力。

从 Patch 采用记录看，Action 对“现场可执行动作、空间关系、受力/冷却顺序”持续产生可验收的局部收益，是当前最稳定的 Specialist。

### Dialogue Specialist

只在第 2、5 章调用。第 2 章 Dialogue Patch 1、2 均采用；第 5 章 Dialogue Patch 1–3 均采用。其贡献集中在把制度边界、现场指令、结算边界和邀约压成可执行的对白信息。样本少于 Action，但在被选择的两章中命中率高。

### Opening Specialist

第 1、3、4 章调用。第 1 章 Integrator 明确记录“Opening 无 Patch”，且该节点 Response 仅 54 字符；这是一次没有产生有效 Patch 的调用。第 3 章的有限时间与先后淬冷信息有效，第 4 章的可见材料替换与延后命名有效。因此 Opening 有条件价值，但选择器在第 1 章没有命中需求。

### Emotion Specialist

五章均为 `skipped`、attempts=0、Prompt/Response=0/0，没有本批价值证据。不能据此证明它永远无价值，只能说当前选择策略没有让它进入盲测运行。

## Integrator 是否被不必要调用

没有发现本批存在“无有效 Patch 仍调用 Integrator”的实例：

- 第 1 章有 1 个 Action Patch；
- 第 2 章有 4 个局部 Dialogue/Action Patch；
- 第 3 章有 Opening/Action 的有效内容，部分合并而非重复采用；
- 第 4 章有 Opening/Action 的多个动作与材料 Patch；
- 第 5 章有 3 个 Dialogue Patch 与 2 个 Action Patch。

五章的 manifest 均记录 Integrator `attempts=1`、`status=adopted`、`final_source=integrator`，没有失败重跑。Integrator 的实际作用是对有效局部 Patch 做合并、去重并产出最终来源；第 3 章明确展示了把 Opening Patch 2 与 Action Patch 1 合并，而不是机械重复写入。

边界是：本批没有“所有 Specialist 都无 Patch”的样本，所以不能证明运行时会在这种情况下跳过 Integrator，也不能量化 Integrator 相对于直接采用单个 Patch 的额外成本。

## Ledger 与单节点恢复

在五个 run 目录的文件名层面，没有发现 recovery、restore、resume 或 ledger 记录。五个 manifest 只显示正常完成、每个已执行节点 attempts=1；没有节点失败、重试、恢复起点、恢复后续节点或 Ledger checkpoint 字段。

结论不是“代码一定不支持恢复”，而是：在被允许读取的运行工件中，没有足够证据证明 Ledger 支持单节点恢复。当前只能确认节点产物按文件分开保存，不能确认从某个失败节点开始恢复时会跳过已完成节点、重建正确上下文并继续 Integrator/State Delta 链。

## State Delta v2 与旧状态尾巴

### 内容推进

State Delta 的 Active Scene State 和 Persistent Canon 在五章中有明确的阶段推进：

1. 第 1 章把旧的“Outline Proposal、尚未生成正文”推进为炉场公炉前、携带异常短刀等待复验，并把“受力记忆”保留为待复验观察。
2. 第 2 章把复验结果写入状态，同时将下一步目标改为从退回废料中找至少两件材料做对照，避免把单刀结果误存为普遍能力。
3. 第 3 章记录对照试验没有证明跨材料稳定复现，并把未入火的完整车环作为下一步真实受力验证对象，同时更新手指麻木状态。
4. 第 4 章把一次性回火环、其受力/裂损边界和押运出发状态写入 Persistent Canon 与 Active Scene State。
5. 第 5 章的 State Delta Audit 明确覆盖第 4 章旧地点、回火环“尚未再次使用”、无独立炉心/接单资格以及“无明确敌人”等旧状态，并写入灰渡登记处、退役独立炉心、临时接单牌、回火环报废和断脊匪已出现等新状态。

这些是状态替换而不是单纯追加；长期未解决的短刀来源、组织立场和合作关系等内容被保留在 Open Promises，属于未决事实，不应当误判为旧状态尾巴。

### 格式与应用门禁问题

每个 `state_delta_prompt.md` 都规定必须返回五个一级标题，缺少任一标题会阻止 State Delta 应用。第 1、2、3、5 章的 Response 含有五个标题；第 4 章只有：

- `# Proposed Active Scene State`
- `# Proposed Persistent Canon`
- `# Proposed Chapter Summary`
- `# Proposed Open Promises`

第 4 章缺少 `# State Delta Audit`，但 `state_delta_approval.md` 仍记录“应用本次 State Delta v2”。所以：

- 语义层面：State Delta v2 能清理旧 Active Scene/Persistent Canon 尾巴，且第 5 章继续修正上一章状态。
- 运行门禁层面：第 4 章存在“响应格式不满足自身合同、approval 却声称已应用”的不一致；必须把该章视为格式验收缺口，不能给出五章全量无条件通过。

## 仍未解决的问题

- 全局上下文仍随章节增长，`hybrid_selective` 只减少 Specialist 调用，没有证据表明主链上下文被压缩。
- 没有恢复记录或 Ledger checkpoint，单节点恢复能力不可验收。
- 第 4 章 State Delta 缺少 `State Delta Audit` 标题，manifest 的 `completed` 与 approval 文案不能替代格式门禁。
- 没有 full-specialist 或非 hybrid 控制组，无法把调用减少量与另一种真实运行模式做实验性比较。
