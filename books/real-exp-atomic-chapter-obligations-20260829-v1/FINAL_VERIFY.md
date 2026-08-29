# Verdict

NEEDS_FIX

# Unsupported Claims

- `EVIDENCE_INDEX.json`、`METRICS_SUMMARY.json`、`formal_audit.md`、`story_audit.md` 均不存在；依赖它们的指标、盲评与独立审计不能称为可独立复核。
- `RESULTS_DRAFT.md:274-282` 依赖未指定且口径冲突的 `story_audit_acp.json`；其“Authority 3:1、Reader 2:2”与报告 corrected phase-i 的 `2 Delta / 1 Control / 1 Mixed` 汇总矛盾。
- `:323`“Full Luna-high Authority Reviser 为 production 默认”不能由本实验边界文件证明；应改为“既有 production control／本实验建议继续保留”。

# Incorrect Numbers

- `RESULTS_DRAFT.md:80`：修正版历史 Full shadow 应为 `3 通过、4 阻止`，不是 `2、5`。
- `:87-94`：phase-g2 corrected 应为 eligible `10/20`、fail closed `10/20`、historical Full pass `5`、blocked `15`；不是 `9/20、11/20、4、16`。
- 已列速度百分比算术无误；phase-j 的 `57.485 + 95.865 = 153.350s`、相对 `120.371s` 为 `-27.4%`。

# Boundary Misstatements

- `:17-25` 的流程图遗漏“Full Reviser 后必须再次过 Atomic Gate；仍失败则停止”，会误导为 Full fallback 自动安全。
- `:55` 将 `source_conflict / diagnostic` 合并后直接 fail closed，过宽；良性 unknown/diagnostic 不等于真实 Authority conflict。
- `:110-122` 将所有路线称为 “fallback-adjusted wall” 不成立：C2、H、H2 都有 residual failure 且 `fallback_full=0`，不能当作含 Full fallback 成本的端到端 wall。
- 零漏报没有被明确泛化；`22/22`、`12/12`已限定为 known-bad／mutation 样本。该限制应保留。
- `commercial_value` 未被硬化为配额，当前表述正确。
- corrected phase-i 的 Reader/Authority 表内自洽，但必须解释或剔除与 story-audit ACP 的冲突汇总。

# Missing Material Risks

- 缺少各路线的 Delta、discard、Full fallback、residual repair、重试成本明细；无法确认 fallback 是否完整计入。
- phase-c0 的“1 Full fallback，1 residual failure”未给逐章链路，无法确认二者是否同一章的“fallback 后复闸失败”。
- formal audit 缺失，false negative、false positive、跨书泛化均未获独立审计。
- repeat consensus 与盲评没有在指定证据文件中给出原始票数、分母和 Mixed 处理规则。

# Required Edits

1. 更正 `:80` 与 `:87-94` 的覆盖率数字。
2. 改流程图：`Full Reviser → Atomic Gate again → pass / FULL_REVISER_RESIDUAL_FAILURE`。
3. 拆分 `source_conflict` 与 benign diagnostic。
4. 把无 Full fallback 的 wall 改称“实测 route wall”；补全每条路线的成本组成与公式。
5. 补齐四个指定文件；否则删除或降级相应盲评、审计和指标结论。
6. 说明 ACP 的 `3:1 / 2:2` 与 corrected phase-i 汇总为何不同；无法说明则不把 ACP 作为证据。
7. 将 Full Reviser 的 production 表述降为既有默认／实验建议，明确实验未证明其 production 安全或质量。

<oai-mem-citation>
<citation_entries>
MEMORY.md:995-998|note=[实验结论需保留原始证据并区分受控结果与生产状态]
</citation_entries>
<rollout_ids>
</rollout_ids>
</oai-mem-citation>
