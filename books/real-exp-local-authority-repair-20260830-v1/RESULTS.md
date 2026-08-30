# Post-hoc Authority Repair Alternatives｜Final Report

> Date: 2026-08-30
> Status: **COMPLETE / STOP FAMILY / NO PRODUCTION CHANGE**

## Final Verdict

本轮按“换思路”要求，不再调整 medium Authority Watch，而是测试两个实质不同的后处理架构：

1. **Blocker-Local Repair**：模型只看极小局部，95%以上正文代码锁死；分别测试 Luna medium 与 Luna high。
2. **Transactional High Diff**：Luna high 看完整 Authority + 完整 Primary，但只输出全局一致的事务式段落 diff；做不到就 fallback Full-high。

最终三条都失败，因此没有生成第三部新 held-out 小说，也没有修改 production。

最重要的新结论：

> **Full Luna-high Reviser 的主要 latency 不是“重新输出完整正文”造成的，而是它必须对完整 Primary + 完整 Frozen Authority 做全章语义闭合。**
>
> 局部上下文很快，但失去全局判断；恢复完整上下文后，即使只输出 diff，reasoning wall 仍接近 Full Reviser，fallback 后反而更慢。

---

## 1. L1｜Luna-medium Blocker-Local Repair

冻结协议 SHA-256：`FA7381FC82824E5C221E81203145787E74487A9ABC0EE1B915D885C07C40A32E`。

结构：

```text
Frozen State / Reader Release / Curator Audit
        ↓ deterministic lexical locality selector
2—5 editable paragraphs + ±1 read-only context
        ↓ Luna medium
single-paragraph replacements only
        ↓ code locks all other paragraphs
```

这和 2026-08-29 被否决的 Patch-only 不同：旧 Patch 模型仍看完整 Primary 并自己选锚点；L1 由 Runtime 先选 locality，模型根本看不到其余约96%的正文。

### Engineering

- 8/8 selector supported；
- 平均 editable ratio：**4.09%**；
- 平均修改：**1.875 段/章**；
- L1 wall：**20.447s/章**；
- matched Full-high：**133.275s/章**；
- 名义差值：**112.828s/章**。

### Blind

| | Primary | L1 local | Full-high |
|---|---:|---:|---:|
| Story mean | 57.250 | **52.875** | 55.000 |
| Authority mean | 79.500 | **79.750** | 88.750 |
| Authority hard problems | 11 | **13** | 6 |

L1 不仅没逼近 Full-high，Hard problems 还从 Primary 的11变成13。

典型情况：

- repeat1 Ch1：局部 repair 成功补齐 Reader Release，Authority 甚至优于 matched Full-high；说明局部修理**可以**对某些明确 fact family 非常有效。
- repeat1 Ch3：成功删掉“残索在后腿附近”的未授权位置，Authority 99 / 0 hard problem。
- 但 repeat1 Ch2：为了强调永久骨痕，把结果提前到身体适配真正成立之前，制造新的因果时点错误。
- repeat2 Ch3：为修残索/关系，新增旧骨刀损伤与沉角感知能力。
- repeat2 Ch4：把 Curator 的“来源未知”审计语言直接写进正文。

**根因：active Authority lane ≠ Primary 真实 blocker。** 只缩 locality 不能让 medium 知道“该不该动”。

Verdict：**FAIL**。

---

## 2. L2｜Luna-high Blocker-Local Repair

冻结协议 SHA-256：`1F54FA24D1AAFAEBD31FA2BFEA8B942B093A53B866684D2101A84FC21A1A5870`。

唯一变量：L1 的 `Luna medium → Luna high`；locality selector、阈值、patch grammar、editable IDs 全部不变。

### Engineering

- 平均 editable ratio仍为 **4.09%**；
- 平均修改 **1.500 段/章**；
- local-high wall **29.696s/章**；
- Full-high **133.275s/章**；
- 名义差值 **103.579s/章**。

### Blind

| | Primary | L2 high-local | Full-high |
|---|---:|---:|---:|
| Story mean | 77.125 | **66.750** | 73.125 |
| Authority mean | 81.750 | **80.875** | 92.375 |
| Authority hard problems | 15 | **14** | 5 |

把模型升回 high 也没有解决。L2 Hard problems **14 vs Full-high 5**，Story 也明显更低。

代表性失败：

- repeat1 Ch4：局部 high 在真正行动发生前提前宣布“已经选定无声湖 / 沉角已成同行者 / 已进入鸣阶2”，把 Future Result 写成先验摘要；
- repeat2 Ch3：提前宣布沉角不再属于裴氏，同时保留未授权感知能力；
- repeat1 Ch2：因为真正需要修的永久骨痕落点不在 selector 选中的可编辑段，L2 返回0 patch，问题原样留下。

这证明第二个根因：

> **即使模型本身是 Luna-high，如果不给它全章，它仍无法可靠知道某个局部状态与前后全文的真实时点、依赖和未选中错误。**

Verdict：**FAIL**。

---

## 3. T1｜Full-context Transactional High Diff

冻结协议 SHA-256：`DEBC7FAD6B5E9E778B846B38523AD9761A7CD1F7947E269368060F1D84061688`。

这是专门解决旧 Patch-only “前文改了，后文仍矛盾”的版本：Luna-high 重新看到完整 Authority + 完整 Primary；但不输出完整正文，只输出按 fact domain 分组的原子 transaction。修改某个状态时必须把所有依赖段落一起返回，做不到就 `ESCALATE_FULL`。

### Timing

- T1 call wall：**110.624s/章**；
- fallback：**2/8**；
- fallback-adjusted route：**134.230s/章**；
- matched Full-high：**133.275s/章**；
- 实际差值：**-0.955s/章**。

也就是：

> **Transactional Diff 平均反而慢0.955秒/章。**

部分单章确实很快，例如 repeat2 Ch3 只改1段，35.166s vs Full-high 135.551s；但另外两章 patch 无法安全应用而 fallback，route 分别慢约109秒。还有一些复杂章 T1 自身已经达到122—175秒，与直接 Full-high 相当或更慢。

因此预先冻结的 timing gate 已经失败，没有必要再花16次 Judge 调用做质量盲评。

这个结果非常关键：

> **缩短输出 token 并没有稳定缩短 Luna-high 的核心思考时间。**
>
> Full Reviser 的 latency 主要来自“读完整 Authority + 完整正文并做全局语义闭合”，不是来自把最终正文再打印一遍。

Verdict：**FAIL_TIMING**。

---

## 4. Combined conclusion

三条路线形成一个清楚的 trade-off：

| Route | Context | Output | Wall | Authority |
|---|---|---|---:|---|
| L1 medium-local | 极小局部 | 极小 patch | **20.4s** | 不够，且会造新错 |
| L2 high-local | 极小局部 | 极小 patch | **29.7s** | 仍不够；缺全局依赖 |
| T1 high-transaction | 完整全章 | diff only | **134.2s route** | 有全局资格，但速度收益消失 |
| Production Full-high | 完整全章 | 完整正文 | **133.3s** | 当前基准 |

所以本轮排除了一个很大的搜索空间：

> **不要再把主要希望放在“让 Reviser 输出更少”或“只给它几个局部段落”。**

只要它仍承担完整 Authority closure，就需要完整上下文与高强度语义推理；把上下文截掉会伤正确性，把上下文恢复后 wall 又回来。

---

## 5. What This Did Not Prove

没有证明：

- 所有局部修复永远无用；Reader Release、单一未授权位置等 narrow family 已出现成功案例；
- Luna-high 永远必须输出完整正文；这里只证明当前 Transactional Diff 没有带来 aggregate wall gain；
- 不能继续优化 Reviser latency。

证明的是：**通用 post-hoc local/diff replacement 不是当前的速度突破口。**

---

## 6. Next Direction

下一步如果继续追速度，不建议再做 L3/T2 prompt 微调。更值得换层级：

1. **减少 Full-high 需要重新推理的 Authority 不确定性，而不是减少它输出多少字。**
2. 研究能否在 Primary 生成时形成可信、极窄的 realization evidence，使 Runtime 能确定哪些 Hard Facts 已闭合、哪些仍需要 high；不能靠 Primary 自报一句“已完成”，必须有可验证的对应关系。
3. 或寻找真正更快但仍具 high Authority reasoning 的模型/effort 配置，而不是用 Watch 强迫 medium 模拟 high。
4. 当前 `validate_chapter_body_for_save()` 另有已发现的23字正文仍可通过问题，应单独修复；它与本实验 route 无关，不在这里顺手混改。

第三本新 held-out 没有生成，因为 derivation acceptance gate 未通过。

---

## Production Decision

**No production change.**

继续：`Luna high Director → Luna high Curator → Terra high Primary → Luna high Authority Reviser → Luna low State`。

当前可冻结的真实节省仍是：**0 秒/章**。
