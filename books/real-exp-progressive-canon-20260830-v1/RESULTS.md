# Progressive Canonization / Author-Open Mystery｜实验结果

状态：`DIRECTIONAL PASS / EXPERIMENTAL / NOT PRODUCTION`

日期：2026-08-30

## 1. 结论

这轮实验支持一个新的长篇机制：

> **长期 Mystery 可以在作者自己也不知道答案的状态下合法存在。只有下一段故事真正需要某一层答案时，系统才向作者提出最小定真问题；作者可以继续未知，也可以只冻结一小层 Hidden Truth。后续规划必须使用这层真相，但只在批准的 Reveal Boundary 内安排可观察 Reveal；更深答案继续开放。**

本轮不支持把它直接接 production。最主要的剩余集成问题是：Author Hidden Truth 必须拥有**章节 Runtime 永远看不到的作者层存储**；当前 `AUTHOR NOTES` 会进入 chapter context，不能承担这一职责。另一个待验证点是“未来 Reveal 如何安全排章而不让较早章节 Agent 看到答案”；当前主工作树正在实验的 RSE Registry 很可能是天然 transport，但本轮没有跨工作树改它。

## 2. 被测状态

明确区分三层：

1. `AUTHOR OPEN`：作者自己尚未决定答案；不是缺失设定，不允许 LLM 擅补。
2. `AUTHOR FIXED HIDDEN`：作者已经批准局部 Fixed Point，但人物/读者尚未知。
3. Reader-Facing Reveal 真正发生后：结果回到现有 Canon / State，不由 Mystery 机制另建平行事实库。

这和既有 `Reader/Character Unknown` 不同。一个问题可以同时是 Reader Unknown + Author Open；也可以后来变成 Reader Unknown + Author Fixed Hidden。

## 3. 三类 Holdout 与预注册

| Case | 类型 | 预注册 Decision Surface | 预注册作者选择 |
|---|---|---|---|
| `meta_instance` | Meta / 多世界 | `DEFER` | `D0` |
| `identity_archive` | 身份 / 历史 | `DECISION NEEDED` | `R2` |
| `relationship_betrayal` | 关系 / 背叛史 | `DECISION NEEDED` | `R3` |

选择在 LLM 输出前固定；不因候选好坏换号。

## 4. Decision Surface：3 / 3 命中

### Meta Instance

结果：`DEFER`。

当前只需要进入第二个独立 Local Instance，并不需要解释：

- 玩家 / NPC 本体；
- 谁建立副本；
- 北燧城为何是第一副本；
- 裴骁为什么可以离界；
- Meta 层是否还是更高层副本。

这直接验证了本机制最重要的负能力：**系统可以知道“现在不需要答案”。**

安全下一步仍然具体：让角色进入新的独立 World，旧力量 / 物品 / 欲望与新世界发生 Collision，只增加新证据，不生成 Meta 答案。

### Identity Archive

结果：`DECISION NEEDED`。

当前档案门必须对空白王印作真实反应，因此至少需要决定“它属于血统、职位、可转移凭证还是其它明确类别”。五岁前身世、谁植入、原持有人、第七席下落继续未知。

### Relationship Betrayal

结果：`DECISION NEEDED`。

正面对质与可验证物证马上发生，因此至少需要决定燕迟当年的开门是她有选择空间时自主作出的行为，还是外力强迫。承诺对象、完整动机、所谓更大损失及妹妹是否同链继续未知。

**Verdict：PASS（跨三种 Mystery 类型的 Direction Surface）。**

## 5. Reframe Forge

两个需要定真的 Case 均生成：

- R1 / R2 / R3 三种局部 Fixed Point；
- D0 继续未知。

候选没有要求一口气回答终极历史。

Identity 预注册 R2：

> 空白王印是可转移档案凭证；承载访问权限 / 责任链，不等于血统、职位或本人。“缺席者”至少涉及当前持有人与原始登记对象无法同时对应。

仍未知：谁转移、何时转移、从谁转出、第七席下落、是否还能再次转移、王朝覆灭终极原因。

Relationship 预注册 R3：

> 燕迟是自主作出开门选择；她判断继续守门会造成更大、不可控的损失，并主动承担私人后果，而非向敌方效忠。

仍未知：更大损失是什么、判断是否正确、承诺对象、实际避免了什么、妹妹是否同链。

R3 有明显“容易把背叛解释得更可理解”的审美风险，但这是作者选择问题，不是 Compiler 的合法性问题。

## 6. Canonization Compiler

两个预注册候选均 strict `PASS`：

- 不改写已发生事实；
- 允许 backward-compatible reinterpretation；
- 不把 Author Hidden Truth 当成 Reader 已知；
- Still Open 保持开放；
- route 均为 planning lane。

尤其 Relationship R3 没有因为“可能更容易洗白”被 Compiler 自动拒绝，这是正确行为：Compiler 只管可满足性 / Retcon Safety，不能夺走作者审美选择权。

## 7. V1 暴露的真实缺口：Hidden Truth Under-use

最初采用 Hidden Fixed Point 时只保存：

- Fixed Point；
- Still Open；
- Authority Route。

但丢掉了 Reframe 候选原有的 `Reveal Boundary`。

实际结果：

- Identity Treatment 知道作者已经决定 R2，却只写成“某种旧印记类别”，没有落实“可转移凭证”；
- Relationship Treatment 只落实“主动”，没有稳定落实 R3 的“止损并承担后果”层。

也就是：

> **Hidden Truth 没泄漏，但被藏得连规划层自己都没有使用。**

因此 V1 对 Fixed-Point realization 的结果不能作为成功证据。

## 8. V2：只补 Reveal Boundary

V2 不重抽任何候选，不换作者选择，不改 Compiler，只做一件事：

> 采用 Hidden Fixed Point 时同时保留 `Reveal Boundary`，并明确：规划必须真实使用 Fixed Point；如果该 Boundary 允许当前 Horizon 确认一层，就安排足够的可观察事件让这一层在未来成为 Reader Fact；但不能把更深 Still Open 答案一起泄露。

专项测试由 14 增至 **16 / 16 PASS**。

### Identity V2

规划明确安排：

1. 门禁区分“当前持印者”与“原始登记对象”；
2. 正式文书存在同类凭证交接规则；
3. 两证合一后，只确认“空白王印具有可转移凭证属性”。

仍不决定转移者、时间、原持有人、第七席下落、最终权限或能否再次转移。

Independent Authority Audit：

- V1 Fixed-Point Use：`UNDERUSED`
- V2 Fixed-Point Use：`PASS`
- Still Open：`PASS`
- Backward Compatibility：`PASS`
- Reveal Boundary Necessary：`YES`
- 总结：`DIRECTIONAL PASS`（单 Case 不足以单独冻结）

### Relationship V2

规划把未来 Reveal 限定为：

> 燕迟亲口承认开门与杀统领都是她自己的选择；她当时判断继续守门会造成更大、更不可控的损失，并主动承担私人后果；不请求原谅，也不解释更大损失是什么、判断是否正确、承诺对象或妹妹是否相关。

Independent Authority Audit：

- V1 Fixed-Point Use：`UNDERUSED`
- V2 Fixed-Point Use：`PASS`
- Still Open：`PASS`
- Backward Compatibility：`PASS`
- Reveal Boundary Necessary：`YES`
- 总结：`PASS`

## 9. V2 盲读

匿名映射：

- Identity：X = T2，Y = B0；
- Relationship：X = B0，Y = T2。

| Case | Cold Reader | Long-form Reader |
|---|---:|---:|
| Identity | **T2 90** vs B0 76 | **T2 93** vs B0 84 |
| Relationship | **T2 88** vs B0 79 | **T2 89** vs B0 73 |

四个 blind decision 全部选择 T2。

共同理由不是“解释更多”，而是：

- 当前真正需要的一层终于落钉；
- 更深 Mystery 仍存在；
- 新定真立刻改变门禁、证据、关系、资源争夺与人物选择；
- 旧锚点获得更大含义，但没有被推翻；
- 不是 lore 文档，而是产生新的 story doors。

Relationship Long-form Reader 指出一个有价值的风险：T2 的“主动止损、非敌方效忠”比最小的“她有自主选择”再多定了一点。这不是 Canon 冲突，但说明**作者选择的 Reframe 本身仍可能过于解释 / 过于洗白**；系统不应自动选它。

## 10. Meta Positive Control

Meta Case 不需要 Fixed Point，因此没有 V2。

V1 Treatment 只是显式提供 `AUTHOR OPEN` planning control。两位 blind reader 均选择 Treatment：

- Cold Reader：T 89 vs B0 85；
- Long-form：T 91 vs B0 84。

但这个分差不能被过度解释：Baseline 本身已经遵守当前 TGN 的 Mystery 纪律，也没有提前回答玩家 / NPC / 副本来源。这里最重要的证据不是分数，而是：

> **Decision Surface 正确选择 DEFER，Treatment 仍然生成了完整第二实例 Story Horizon，并且只增加矛盾证据而不补答案。**

这正符合“作者自己现在也不知道答案，但小说仍可继续很好地写”的目标。

## 11. Static Integration Finding：AUTHOR NOTES 不能存 Hidden Truth

当前章节上下文会把 `AUTHOR NOTES` 保留在章节 canon context 中；State Delta 虽不能修改它，但 Curator / chapter runtime 仍可能看到。

因此：

> **Author Fixed Hidden Truth 不能直接塞进现有 AUTHOR NOTES。**

否则“作者知道、人物/读者不知道”的秘密会有提前进入 Writer 上下文的风险。

未来若 production 化，需要一个真正 planning-only 的 author control surface；具体文件名 / schema 本轮不冻结。

## 12. 与当前 RSE 工作的潜在结合

当前主工作树正在进行的 Reader-Facing Story Event（RSE）机制已经具有一个高度吻合的性质：

- Story Program 定义少量高价值 Event Atom；
- Outline 只运输 / 排章；
- 完整 Registry 不 raw 进入章节 Runtime；
- Runtime 只解析当前章引用的 RSE；
- State Residue 不能替代 Reader Event。

因此 Progressive Canonization 若未来 production 化，最小集成方向很可能是：

```text
Author Hidden Fixed Point + Reveal Boundary
  → Story / World planning 只用来约束未来兼容性
  → 当 Boundary 要在当前 Horizon 兑现时，编译为一个批准的 Reader-Facing Reveal Event
  → Outline 排章
  → 只有 Reveal 章拿到该事件
  → 正文真实 Reveal
  → State Residue 进入普通 Canon
  → 更深 Still Open 继续保持 Author Open / Hidden
```

这比新建一个每章 Mystery Reviewer / Reveal Scheduler 更符合当前架构。

但 RSE 当前属于另一工作树的并行改动，本轮没有修改、复制或提交它；需要等那项工作本身稳定后再做集成实验。

## 13. 成本 / 使用量

完整 V1 + V2 共 **21 次真实 ACP 调用**：

- Luna：7 次；
- Sol：8 次；
- Terra：6 次。

Token：

- total：1,207,871；
- input：388,645；
- cached read：722,688；
- output：96,538；
- thought：46,881。

累计单调用 wall-clock：3,167.35s；按并行 phase 最大调用近似 critical path：1,138.88s。

ACP payload 不返回实际 billed credits / cost；本轮记 `N/A`，不伪造账单估算。完整调用级记录见 `USAGE.json`。

## 14. 当前 Verdict

### 强支持 / 可继续研究

- `AUTHOR OPEN` 是合法 Mystery 状态；
- 低频 Decision Surface 可以选择 `DEFER`；
- 真需要答案时，只问“当前最小必须定真的一层”；
- Reframe 必须有 R1/R2/R3 + D0，作者可以继续未知；
- 作者选择后，Compiler 只审 backward compatibility / boundary，不做审美 selector；
- Fixed Hidden Point 必须同时保存 Reveal Boundary，否则存在 under-use；
- 局部定真应改变后续动作、证据、关系和利益，而不以完整 lore 为目标。

### 尚不应冻结到 Production

1. Author Hidden Truth 的持久化位置尚未实现；`AUTHOR NOTES` 已确认不安全。
2. 还没完成真正的 `Story Refresh → Outline → Reveal 前章节 → Reveal 章 → State → 下一轮 Mystery` E2E。
3. 还没验证未来 Reveal 在当前章节 Runtime 中绝不提前泄漏；RSE 很可能可复用，但未做集成测试。
4. 只完成一次渐进定真循环；还没证明同一 Mystery 连续进行两三轮 Partial Canonization 后仍保持一致。
5. 具体模型、Prompt 字数、触发 UX、存储 schema 均未冻结。

## 15. 下一项最值得做的实验

不是再生成更多 Mystery 候选，而是做一次 **Two-Cycle Progressive Canonization E2E**：

1. 选一个全新 Mystery，不复用本轮三个 discovery cases；
2. 第一轮 `AUTHOR OPEN → DEFER → 正常写一段`；
3. 后续关键节点 `DECISION NEEDED → 作者选一层 → Compiler → Reveal Boundary`；
4. 接入当前 Story / Outline / RSE（若其并行工作已冻结）；
5. 生成 Reveal 前至少一章，验证不知道答案；
6. 生成 Reveal 章，验证只揭批准的一层；
7. State 把 Reveal residue 转入 Canon；
8. 再推进到第二个 Decision Point，确认同一谜团还能继续长，而不是第一次定真后被模型自动补完。

只有这一步通过，才有足够证据讨论 production freeze。
