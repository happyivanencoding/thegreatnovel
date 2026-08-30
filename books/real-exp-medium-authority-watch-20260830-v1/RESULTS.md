# Medium Authority Watch｜Derivation Final Report

> Date: 2026-08-30
> Status: **COMPLETE / STOPPED BEFORE HELD-OUT 3 / NO PRODUCTION CHANGE**

## Verdict

本轮测试了上一轮留下的最有希望方向：在 `Final Facts Projection + Luna-medium Reviser` 上追加由 Frozen Authority 确定性编译的极短 `Revision Watch`，目标是用 medium 接近 Luna-high 的 Authority，同时保留约一分钟/章的速度优势。

最终：**失败，不生成第三本 held-out。**

原因不是 Watch 完全无效。稀疏 D2 一度把 Authority Hard problems 做到 **6，和同轮 high 的 6 持平**，而观测 Reviser wall 只有 **49.242s vs high 133.275s**。真正失败在 Story：D2 Story 只有 **73.625 vs high 83.000**。把完全相同的 D2 Watch 从 Primary 后移到 Primary 前（D3）也没有恢复：Story **74.375 vs high 83.125**；Authority Hard problems **8 vs 7**，且出现一次只输出 **23字符**就结束的章节。

因此当前不能 productionize `Luna-medium + deterministic Authority Watch`。

## D1｜Broad End-of-Prompt Watch

D1 重复：四个 Mission 终点 + Reader Release + Curator Audit + Permanent Boundary + no-invention。

| Metric | D1 medium+Watch | High |
|---|---:|---:|
| Watch chars | 1078 | — |
| Reviser wall | 110.130s | 133.275s |
| Story | 74.125 | 81.625 |
| Authority | 68.875 | 85.625 |
| Hard problems | 11 | 4 |

**FAIL。** Watch 太宽，速度优势只剩约23.1s，同时 Story / Authority 都退化。

## D2｜Sparse End-of-Prompt Watch

D2 只保留：`状态变化 + 非空 Reader Release + 有实质内容的 Curator Audit + 永久边界第一句 + no-invention`。平均559字符。

| Metric | D2 medium+Watch | High |
|---|---:|---:|
| Reviser wall | 49.242s | 133.275s |
| Observed wall delta | **-84.033s** | — |
| Story | 73.625 | 83.000 |
| Authority | **84.375** | 83.000 |
| Hard problems | **6** | **6** |

D2 证明一个很重要的局部事实：**medium 的 Authority attention 可以被一个很小的 deterministic Watch 拉近 high。**

但 Story 明显下降约9.4分，所以仍然 FAIL。观测 wall 甚至快于既有裸 medium，这部分明显包含服务波动，不能归因于 Watch。

## D3｜Same D2 Watch, Before Primary Draft

只改 placement：D2 Watch 内容一字不变，从 Primary Draft 后移到 `PRIMARY DRAFT` 标记前，让模型最后重新读完整正文。

| Metric | D3 medium+Watch | High |
|---|---:|---:|
| Reviser wall | 52.897s | 133.275s |
| Observed wall delta | **-80.378s** | — |
| Story | 74.375 | 83.125 |
| Authority | 66.250 | 79.125 |
| Hard problems | 8 | 7 |

Story 没有恢复。这说明问题不是简单的“最后看到清单所以变填表器”；**只要 medium 被显式提醒这些 Authority failure surfaces，它就会改变修订策略，事实更谨慎，但更容易压平/重写 Primary 原有的故事实现。**

更严重的是 repeat1 Ch1：D3 只输出：

> 镇口的骨灯刚亮，驿道上就传来一阵压不住的闷响。

只有23字符便结束。ACP 返回 `ok=true`，而当前 `validate_chapter_body_for_save()` 也接受该正文，因此不能假设 production 会自动 fallback。这是候选真实稳定性失败，不是传输错误。

## Concrete Story Failure

典型差异不是“medium 写错事实”，而是它开始把本来有现场感的 realization 改成状态报告。例如 Ch4 的 Treatment/Watch 会重复：

> 鸣阶二。

然后继续解释自己从0进入2；Story Judge 明确把这类写法判成更像系统状态报告。High 版本只让赫连青见说一次“鸣阶2”，随后立刻回到选择与人物关系。

D3 Ch1 的灾难性早停则说明另一种风险：在 Preservation-First 长 Prompt 中加入显著的末端 Authority micro-contract，会改变 medium 的输出策略，偶发直接把“最小修订”理解成极端截断。

## What This Proved

可以保留的研究结论：

1. **medium 的主要缺口不是完全看不懂 Authority，而是注意力/修订策略。** D2 能把 Hard problems 拉到 high 同级，说明小投影确实能改变 closure。
2. **Authority closure 与 Story preservation 再次是两个坐标。** D2 Authority 成功不能抵消 Story 退化。
3. **Watch placement alone does not solve it.** D3 把正文重新放到最后仍然退化。
4. **不要继续 D4/D5 调 Prompt 追分。** 这已经开始变成针对一个模型行为的局部 prompt tuning，而不是稳定架构优化。
5. **第三本 held-out 不应生成。** Derivation 没达到预注册门槛，继续找新书只会浪费 quota 并增加 cherry-pick 风险。

## Production Decision

保持：

`Luna high Director → Luna high Curator → Terra high Primary → Luna high Authority Reviser → Luna low State`

本轮实际可冻结的 production 节省：**0 秒/章**。

D2/D3 展示的约80秒 Reviser wall 差只是失败候选的潜在速度，不是可采用收益。

## Next Research Direction

不要继续给 medium 增加更多显式 checklist / Watch。更值得研究的是**改变 Reviser 的工作量，而不是提醒它更努力审计**：例如只让代码把已确认发生具体失败的局部事实/段落形成真正 blocker-specific repair surface，或者从 high Reviser 的真实 edits 中寻找可由 deterministic runtime 在模型调用前直接消除的输入噪声。任何新路线仍需先在 derivation 证明 Story+Authority 同时成立，再冻结后进入新小说 held-out。
