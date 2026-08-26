from pathlib import Path
import json,re
EXP=Path(r'C:\dev\tgn-story-mvp\books\real-exp-prose-control-projection-ab-v2')
DOC=Path(r'C:\dev\tgn-story-mvp\docs\GBRAIN_PROSE_CRAFT_V1.md')
metrics=json.loads((EXP/'metrics.json').read_text(encoding='utf-8'))
rows={(r['case'],r['arm']):r for r in metrics}
report=f'''# Prose Control Micro Projection A/B v2 — 2026-08-24

## Goal

在上一轮多场景 A/B 得出 `KEEP OPTIONAL` 后，验证三个更小的问题：

1. 给 Prose Controls 加入“动作/对白/结果已成立后停止抽象解释”的共享软规则是否有方向性效果；
2. `spatially-traceable-causality` 换一个完全不同的 Action 场景后能否复现正收益；
3. Dialogue / Entry 不再给完整 Control，只给 2–4 句 scene-specific projection，是否修复上一轮的过度执行。

所有 A/B 均固定同一 Chapter Mission / Canon / BOOK Prose Profile / Terra high Primary Writer；每对 prompt 在实验区块之前 SHA 一致。最终只用 1 次 Luna high 联合盲评，组内 X/Y 随机打乱。

## Shared abstract-explanation stop rule

7 张 Prose Controls 均加入同一条软规则：

> 动作、对白、物体变化或人物反应已经让意义成立时，不再追加“意味着、说明、显然、可以看出、这不是……而是……”式同义解释；只有当前 POV 必须据此做下一步选择时，才保留一条具体判断。

它不是禁词表：这些词在确实承担当前人物判断时仍可使用；重点是阻止“动作已经成立后又解释一次”。

## Experiment A — Action retest

Scene：公开考核中的近身取牌对抗。与上一轮“路线追逐”不同，空间天然简单、边界清楚。

Control：完整、更新后的 `spatially-traceable-causality-v1`。

| | OFF | ON |
|---|---:|---:|
| Blind score | **8.6** | 7.8 |
| Draft chars | {rows[('action_retest','OFF')]['chars']} | {rows[('action_retest','ON')]['chars']} |
| Broad abstract markers | {rows[('action_retest','OFF')]['abstract_broad']} | {rows[('action_retest','ON')]['abstract_broad']} |
| Explicit explanation markers | {rows[('action_retest','OFF')]['abstract_explicit']} | {rows[('action_retest','ON')]['abstract_explicit']} |
| Action-verb hits | {rows[('action_retest','OFF')]['action_verbs']} | {rows[('action_retest','ON')]['action_verbs']} |

Result：**ON -0.8**。

和上一轮复杂路线追逐的 **ON +0.4** 合并看，结论不是“Action Control 无效”，而是它高度依赖空间复杂度：追逐、多入口、移动地形、多人混战等容易丢方位的场景可能受益；简单一对一、单一场地反而会因为过度追踪和额外动作细节而变重。

因此已收窄 `spatially-traceable-causality` 的 Applicability：简单一对一、位置天然清楚时不默认启用。

## Experiment B — Dialogue short projection

沿用上一轮回灯集 Ch4 高压谈判，但把完整 Control 压成三句：只保留状态变化、潜台词和停止抽象解释，并明确禁止新增 Mission 外交易条件。

| | OFF | ON projection |
|---|---:|---:|
| Blind score | **8.6** | 8.3 |
| Draft chars | {rows[('dialogue_projection','OFF')]['chars']} | {rows[('dialogue_projection','ON')]['chars']} |
| Broad abstract markers | {rows[('dialogue_projection','OFF')]['abstract_broad']} | {rows[('dialogue_projection','ON')]['abstract_broad']} |
| Explicit explanation markers | {rows[('dialogue_projection','OFF')]['abstract_explicit']} | {rows[('dialogue_projection','ON')]['abstract_explicit']} |

Result：**ON -0.3**，与上一轮完整 Dialogue Control 的 **ON -0.3** 相同。

这说明 Dialogue 的问题不只是 Control 太长。当前 Reader-First / 对话基础规则已经能让自然对白承担大部分筹码与关系变化，额外 Control 容易重复方法论或让模型为了“更像谈判”增加结构。压短后抽象解释指标改善，但没有转换成整体阅读优势。

因此 `dialogue-state-pressure` 继续 `KEEP OPTIONAL`，并进一步收窄：只在多方、高压、隐含筹码确实难以从基础对白读清时使用；基础对白已经自然改变筹码时，不额外增加回合、报价或承诺。

## Experiment C — Entry short projection

沿用矿井 Ch1 开场，把完整 `action-anchored-grounding` 压成三句：动作/目标/限制先行；只允许一个真正改变判断的局部异常；禁止补造机制并停止动作后解释。

| | OFF | ON projection |
|---|---:|---:|
| Blind score | 8.1 | **8.5** |
| Draft chars | {rows[('entry_projection','OFF')]['chars']} | {rows[('entry_projection','ON')]['chars']} |
| Broad abstract markers | {rows[('entry_projection','OFF')]['abstract_broad']} | {rows[('entry_projection','ON')]['abstract_broad']} |
| Explicit explanation markers | {rows[('entry_projection','OFF')]['abstract_explicit']} | {rows[('entry_projection','ON')]['abstract_explicit']} |
| Action-verb hits | {rows[('entry_projection','OFF')]['action_verbs']} | {rows[('entry_projection','ON')]['action_verbs']} |

Result：**ON +0.4**。上一轮完整 Entry Control 是 **ON -0.3**，本轮短 projection 成功翻正。

因此短 projection 解决“研究卡太厚、Primary 认真执行方法论”的方向有真实证据。已把本轮三句版本写入 `action-anchored-grounding-v1` 的 `Writer Projection`，但仍不自动全局 ON；需要至少再用一个不同 Entry 场景复验后再考虑 promotion。

## Abstract explanation suppression result

方向性结果：

- Action：explicit marker **1 → 0**；
- Dialogue：broad marker **1 → 0**；
- Entry：**0 → 1**，说明软规则不能保证逐样本机械下降。

因此保留为“stop rule”，不升级成 banned-word checker / hard gate / rewrite pass。真正目标仍是：**意义已由现场成立后停止重复解释**，而不是让某些词永远不能出现。

## Product decision

- 全局 Prose Control：继续 **KEEP OPTIONAL**；
- `spatially-traceable-causality`：只对复杂空间 Action 保留强候选，不用于所有战斗；
- `dialogue-state-pressure`：OPTIONAL，且适用面进一步收窄；
- `action-anchored-grounding`：研究卡继续保留，生产时优先使用短 `Writer Projection`；
- Abstract Explanation Suppression：作为 7 张 Control 的共享软 stop rule 保留。

本轮不增加 Reviewer、禁词表、评分器或自动重写。
'''
(EXP/'AB_REPORT.md').write_text(report,encoding='utf-8')

doc=DOC.read_text(encoding='utf-8')
section='''\n## Micro Projection A/B v2（2026-08-24）\n\n在首轮 4 Scene A/B 的 `KEEP OPTIONAL` 基础上，进一步验证“抽象解释抑制 + 短 projection”：\n\n- 7 张 Prose Controls 均加入共享 stop rule：动作、对白、物体变化或人物反应已经让意义成立时，不追加“意味着 / 说明 / 显然 / 可以看出 / 这不是……而是……”式同义解释；只有当前 POV 必须据此选择时才保留具体判断。这不是禁词表。\n- Action 换成公开考核近身对抗复验：OFF 8.6 / ON 7.8；结合上一轮复杂路线追逐 ON +0.4，说明 `spatially-traceable-causality` 只应优先用于追逐、多人、移动地形、多入口等读者可能丢失方位/因果的 Action，不应覆盖简单一对一。\n- Dialogue 完整 Control 上轮 ON -0.3；本轮压成三句 scene projection 后仍 ON -0.3。说明问题不只在长度，当前基础 Writer 已能完成多数谈判；`dialogue-state-pressure` 继续 OPTIONAL，并禁止为执行控制新增交易条件/回合。\n- Entry 完整 Control 上轮 ON -0.3；本轮三句 projection 变为 OFF 8.1 / ON 8.5（+0.4）。因此 `action-anchored-grounding` 保留完整研究卡，但增加短 `Writer Projection` 作为生产候选；至少再跨一个 Entry 场景复验后才 promotion。\n- 抽象解释指标在 Action 1→0、Dialogue 1→0，但 Entry 0→1；因此 stop rule 有方向价值，但不能升级成机械禁词/重写门禁。\n\n当前产品判断仍是 **KEEP OPTIONAL**；短 projection 比“把完整研究卡压给 Primary”更值得继续验证。完整实验见 `books/real-exp-prose-control-projection-ab-v2/AB_REPORT.md`。\n'''
if '## Micro Projection A/B v2（2026-08-24）' not in doc:
    doc=doc.rstrip()+section+'\n'
DOC.write_text(doc,encoding='utf-8')
print(EXP/'AB_REPORT.md'); print(DOC)
