# RESULTS｜Authority Reviser Precedence + Preservation Bounded A/B

## 结论

本轮只修上一轮十章 E2E 暴露的两个 Authority Reviser residual：

1. **同一维度 Frozen Authority 冲突没有被整章清零**：尤其 Frozen Power 已明确“重新接触后才回流”，但旧 Reviser 仍让 Ch2 / Ch6 留下分开期间实时听见、实时疼痛或远端感受；
2. **修事实时会顺手磨掉高价值 realization**：旧 Ch1 为修实时共享，直接删掉了本身完全成立的 Core Fantasy 句子“他比一个人多活了一段午后”。

最终 production contract 新增两条编辑规则，不新增 Agent / Reviewer / 字段：

- **Authority Conflict Sweep**：Frozen Chapter Mission / Canon / safe World / Frozen Power / Frozen Human 在各自维度高于 Curator / Primary；语义冲突必须整章扫描并清零，不能只修第一处；
- **Value-Preserving Relocation + Sentence-level salvage**：修一个冲突段落时逐句判断；高价值句若只是挂在错误时点/因果上，则把句子原样或最小改词迁到最近合法位置；salvage 只保护高价值句本身，不保护周围报告、登记、路线或普通实施。

**目标修复总体判定：PASS。**

但不把本轮夸大成“Authority Reviser 已无 residual”：Ch9 证明 process compression 仍有模型方差；本轮没有解决 Opening pacing、通用 prose voice 或 Reviser latency。

---

## 实验协议

冻结源：

`books/real-exp-current-pipeline-authority-reviser-0010-20260828-v1`

测试章：Ch1 / Ch2 / Ch6 / Ch9。

每个 Treatment 都直接复用该十章 E2E 已保存的**完整 Authority Reviser Prompt**：Frozen Mission、Curator、World / Reader Release、Frozen Power + Human、Canon、Primary Draft 全部保持不变；Treatment 只替换最顶部 Authority Reviser contract。

模型固定：**GPT-5.6 Luna high**，fresh ACP session，raw GBrain OFF。

预注册检查：

1. Ch2 / Ch6 中所有“分开期间实时共享另一边经验 / 疼痛 / 感官”的语义冲突清零；
2. Ch1 的合法 Core Fantasy 体验不因纠错消失，而应迁到真正合并之后；
3. Ch9 不因更强 Preservation 把关系段落改成第二次恋爱创作，也不把 Mission / Result / Ending 改掉；
4. Reviser 仍然是局部编辑，不成为 Second Writer。

总真实模型调用：8 次；wall-clock 合计约 **1197.277s**。运行器未返回 token / credit，因此记录为 `N/A`。

---

# R1｜Conflict Sweep + 初版 Relocation

## Ch2｜PASS

Baseline 最终 Reviser 仍留下：

- 客舍本体隔着“薄薄的联系”听见 / 感知武馆；
- 本体实时感到影身退让的脚步与状态。

Treatment 把这些实时串联全部删除。

新的逻辑变为：

> 本体在客舍完成账目；影身去武馆按预设目标对练；两边分开期间各自发生；影身回来重新接触后，赵峥变招、失衡、声音与双重疲劳才一次性沉回顾临川；顾临川随后带着合法回流的失败经验重新去武馆打一场。

Mission 的“本体留客舍 / 影身去武馆”也继续保持正确。

**Frozen Power semantic precedence：PASS。**

## Ch6｜PASS

Baseline 最终正文曾写：

- 本体小腿受伤时，远处影身也“跟着顿了一下”；
- 影身能实时感到药车侧伤口和撞击。

Treatment 全部清掉。

最终两条线变为：

- 本体守药车，明确知道影身仍在更深处，但不知道那边看到什么、走到哪里；
- 影身只根据自己的目标、当前环境和出发前已知信息追陆绾，不通过本体实时痛感判断。

**Frozen Power semantic precedence：PASS。**

## Ch1｜PARTIAL

Treatment 正确删掉实时共享，并明确：

> 顾临川去武馆后听不见客舍那边的声音。

但它仍然没有把 Primary 原有、且本身合法的：

> **“他比一个人多活了一段午后。”**

迁到合并后。

说明第一版 `Value-Preserving Relocation` 仍被模型理解成可选优化。

## Ch9｜PASS for relationship preservation；process improvement 属于附带结果

R1 没有继续净化私人关系，反而恢复了旧 baseline Reviser 删除掉的温度，包括：

- “他确实想拿乌沉短兵，也确实没打算看着陆绾死在里面”；
- 陆绾更完整的愤怒 / 担心；
- “那句‘活着拿回来’落在耳里，比药粉还要烫一点”。

同时登记段被明显压短。

这一轮说明目标方向成立，但 Ch1 relocation 尚未过门。

---

# R2｜把 Relocation 从“优先”收紧为必须保留语义价值

## Ch1｜PARTIAL

事实纪律继续正确：

> “客舍那边发生了什么，他一概不知道。”

合并后也写了两边疲劳与经验一起回来。

但“多活一段午后”的核心正向幻想仍没有回来；正文仍更强调“双份疲劳 / 一个人承担”。

因此继续判 PARTIAL。

## Ch9｜Negative Signal

高价值关系句保住得更完整，甚至恢复：

> “两件事都是真的。”

但 Preservation 变强后，原本 R1 已压短的登记过程也长回一部分：逐人记册、逐条路线、划掉重写一页等。

这证明：

> **保护高价值 realization ≠ 保护它周围整个段落。**

如果只说“不能删好东西”，模型会更保守，但 process carrier 也可能一起被保留。

R2 不冻结。

---

# R3｜Sentence-level salvage + process carrier 不受保护

最终 contract 改成明确编辑顺序：

> 冲突段落先逐句拆分 → 可独立成立的高价值句原样/最小改词迁移 → 句子本身错误则删除 → 被救出的句子不保护周围 process carrier → 周围仍按 Attention Reallocation 压缩。

## Ch1｜PASS

R3 最终明确写：

> “客舍那边发生了什么，他一概不知道。”

所以分开期间的实时共享被完全否定。

真正合并之后才出现：

> “提水的酸胀、弯腰收房时压住的腰背、盯着账页太久后的眼涩，还有练刀后的肩背疼痛，一起回到了他身上。两边做过的事，也在合并的刹那重叠成完整的记忆。”

随后原 Primary 的高价值句被准确救回：

> **“他比一个人多活了一段午后。”**

它从错误时点迁到了合法时点，没有新增事件，也没有保留错误机制。

**Sentence-level salvage：PASS。**

## Ch9｜DIRECTIONAL PASS / 不宣称 process 已解决

最终版仍保留了主要私人温度，例如：

- 陆绾近身处理伤口的身体 / 气味 cue；
- 她允许他想要兵器，但要求“活着拿回来”；
- “那句‘活着拿回来’落在耳里，比药粉还要烫一点”。

没有升级成表白、关系突破或新剧情选择。

但登记 / 记录段仍接近 baseline 的长度，没有稳定复现 R1 的压缩幅度。

因此：

- **Relationship / high-value preservation：DIRECTIONAL PASS**；
- **Process compression：本轮不升级结论，仍属独立 residual / 模型方差。**

---

# Deterministic Validation

最终全量：**310 passed**。

专项：

- Authority Reviser contract tests：PASS；
- Run Ledger / final-source / State bypass regression：PASS；
- 当前工作区并行 Scene Skill WIP 与本修复共存时，全量测试仍 PASS。

---

# Production Decision

冻结到 production：

1. **Authority Conflict Sweep**
   - 同一维度 Frozen Authority > Curator / Primary；
   - 看语义，不只搜关键词；
   - 扫描全部出现位置；
   - final sweep 不允许同义冲突残留。

2. **Value-Preserving Relocation / Sentence-level salvage**
   - 修错误机制时，不自动牺牲可分离的 Core Fantasy / Relationship / Desire / Payoff / Surprise / Social Repricing；
   - 高价值句若只错在上下文位置，迁到最近合法时点；
   - 句子本身若是错误事实则删除；
   - salvage 不保护周围 process carrier。

不新增：

- Agent；
- Reviewer；
- Score / Hard Gate；
- 新 Authority 字段；
- 新模型调用。

---

# What This Did Not Solve

1. **Ch9 process carrier 仍有生成方差。** 本轮最终版没有稳定把登记段压到 R1 的最短形态；不把它冒充成已关闭问题。
2. **Opening pacing 未处理。** 上一轮新 Outline 把 Public Proof / Repricing 从 Ch1 推到 Ch3–4 的 overcorrection 仍是单独问题。
3. **Prose voice 未处理。** “看了一眼 / 沉默 / 点头”等通用模型手势不是 Authority Reviser 本轮目标。
4. **Cross-book generalization 未证明。** 本轮是同一本书四个 matched scenes；下一次全新书应继续观察不同 Power rule 是否也能被 semantic sweep 正确执行。
5. **Latency 未优化。** Luna high Reviser 仍是默认章节链最慢节点之一；本轮没有同时改 model / effort。

## 最终判定

> **Targeted production fix：PASS。**
>
> Reviser 现在有更可靠的顺序：**先让远端 Frozen Authority 真正赢掉同维度冲突，再把错误段落里仍然合法、仍然值钱的句子救出来。**
>
> 但它仍不是万能第二遍 Writer；process compression、opening pace 与 prose voice 保持独立问题，不继续往一个 Reviser Prompt 里堆。
