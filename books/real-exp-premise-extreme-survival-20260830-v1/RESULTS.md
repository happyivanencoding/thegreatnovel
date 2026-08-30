# Extreme / Aggressive Premise Experiments｜Results

日期：2026-08-30  
状态：RESEARCH ONLY；production 未修改  
基线：`origin/principal_dev_new_sys@70df4ac4`，其中 F1–F5 Premise Aperture 已由 `986a6c55` 冻结。  
执行环境：独立 detached worktree `C:\dev\tgn-story-mvp-extreme-20260830`，未触碰主工作树中的 Atomic / latency 并行改动。

## 1. 本轮问题

本轮不是继续证明“Premise Forge 能不能想出怪设定”，而是测试两件更右尾的问题：

1. **E7 Extreme Premise Survival**：明确要求 S3 进入 extreme right-tail 后，它能否 strict Compiler PASS，并继续活过真实 `World → Power/Human → Story → Outline → Chapter 1–5`，而不是被下游磨回普通修士。
2. **E1 Matched Mutation Ladder**：同一个 premise DNA 做 M0→M4，作者能否直接看见 conservative / commercial / aggressive / extreme / overdrive 的真实差异，而不是拿五个不同点子误判“强度”。

E7 第一轮被 Compiler 挡住后，又做了一次**独立 fresh Treatment**：

3. **E7b Extreme + Primitive Closure**：不是修原 S3，而是重新生成；要求 20/100 章所有玩法只能由少量开局原语复合，禁止单点能力静默长成网络、远程路由、新 target class 或新出口。

预注册纪律：E7 与 E7b 都在生成前固定 `S3`；只有 strict `PASS` 才继续 downstream；`CONDITIONAL PASS / FAIL` 都停止；不换 S1/S2、不自动 Repair、不 sample-until-success。

## 2. E7｜Extreme Right-Tail

### 真实 S3

`《天下第一道伤口》`

> 主角不是受伤的人，而是一道刚刚长出意识的伤口；谁制造了这道伤，他就能沿着伤口留下的因果线钻进对方身体，从内部把伤口还回去。

真实 Changed Verbs：

- 沿创线钻进制造者体内；
- 把旧伤撕成新出口；
- 并入敌人的伤口边缘；
- 借伤者穿过封锁；
- 从刀口 / 箭孔 / 裂甲中出现；
- 拖动物体穿过开放伤口。

这证明 Extreme Treatment 没有把“大胆”降成更高数值、更多奖励或更专业技能。它直接改变了 Protagonist Ontology 与故事基本动词；一句话仍然可懂。

### Independent Compiler

Verdict：`CONDITIONAL PASS`。因此 E7 downstream **未授权、未运行**。

开篇核心“伤口反咬制造者”基本可编译，但存在一个触发语义缺口：原伤口本身是否能作为触发伤口、行刑者伸手时主角边缘与创线究竟怎样完成接触没有写严。

真正严重的坍缩发生在长线：

- “拖行刑者进入胸腔”超出小型物体权限；
- 从原伤转移到囚徒 / 医者移动锚点没有合法路径；
- “进入某强者旧伤”混淆了伤者端与制造者端；
- 兵器 / 铠甲 / 城墙 / 战争伤痕是否属于合法伤口未定义；
- 多条创线被静默升级为共同网络；
- 肢隙→门隙的几何增长没有映射到能力作用尺度；
- 跨 Local World 出口没有来源。

**关键结论：Extreme Forge 的第一章想象力已经强于它的 20 章因果纪律。** 新瓶颈不是“敢不敢想”，而是“怎样用同一组合法 Changed Verbs 长出很多不同故事”。

## 3. E1｜Matched Mutation Ladder

同一《天下第一道伤口》生成：

| 档位 | 主要变化 |
|---|---|
| M0 | 单目标 / 单出口 / 单城追捕 |
| M1 | 同一制造者体内多开放旧伤短链折返 |
| M2 | 人体 → 兵器 / 铠甲 / 建筑战争伤痕 |
| M3 | 全城开放伤口串成连续身体 |
| M4 | 整场战争伤口串成主角身体 |

这次 Ladder 成功证明“同一 DNA 也能明显看见电压梯度”，但它同时暴露两项失败信号：

1. **LLM 把 aggressive 主要理解成空间 / 网络规模升级。** M2→M4 的主要变化是个人→建筑→城市→战争，新的基本动作没有同比增加。
2. **Matched DNA 从 M2 开始出现 carrier 漂移。** 母 premise 没有批准“建筑也属于伤口载体”，M2 却把建筑战争伤痕直接纳入。因此这份 Ladder 目前适合作者看“电压”，不适合当 Authority-ready 版本梯度。

此外，M4 文本自己评价“M3 更像商业甜点”。该意见不是实验结论；Creative Intensity 仍只能由作者决定。后续若继续 Ladder，应明确禁止模型推荐某一档。

结论：`DIRECTIONAL PASS`。值得继续，但下一版应测试 **Lateral Aggression**：固定 carrier / reach，不允许只靠变大，强迫更激进来自不同动作组合、身体后果、关系/占有后果与反制，而不是城市尺度。

## 4. E7b｜Extreme + Primitive Closure

### 真实 S3

`《门胚：把敌人的攻击翻回去》`

> 只要有两面，世界就会长出门；主角是一枚刚出生的门胚，能贴上盾牌、铠甲和城墙，把穿门而过的攻击翻到敌人那一面，二十章内长成能倒扣整座天门的活门。

Power 明确压成五个 Legal Primitives：

`贴 / 开 / 翻 / 锁 / 移`

并限制 carrier 为：建筑墙体/门体、盾牌/铠甲等刚性防具、棺材/箱体等刚性容器。20 章动作全部显式写为这些 primitives 的 composition。

### 相对 E7 的真实改善

上一轮最严重的问题是：一个单一伤口—制造者通道在长线静默长成移动锚点、建筑伤口、多伤网络与跨世界出口。

E7b 的 Compiler 明确确认：从盾牌、城墙、攻城槌到天门的**动作形态原则上可以继续复用同一组原语**。Primitive Closure 因而是实质改善，不只是 Prompt 看起来更整齐。

### 仍未 strict PASS

Verdict：`CONDITIONAL PASS`。因此仍然没有启动真实 downstream。

最早剩余冲突收缩为两类核心语义：

1. **运动几何没有闭合。** `翻`只写“交换出口面”，不能自动推出枪尖会从持枪者胸口内部穿出；持枪者本人也没有穿门，不能被 `锁` 当目标。
2. **载体尺度 / 门阶绑定没有闭合。** T0 门胚只允许空气与光通过，却第一章让长矛通过；“贴上更大载体”究竟是否借用载体门幅没有规则。若贴上就完全借尺度，T0 贴天门即可七阶；若不能，第一章与 20 章都缺成长机制。

其次仍需明确：跨载体接触顺序、何时真实进入门缝、天门被锁如何等于关闭，以及百章中不得把未批准的身体载体预当既有事实。

结论：`DIRECTIONAL PASS`。Primitive Closure 把失败从“长线不断偷加新机制”压缩成“开局核心 Power 的 scale-binding / motion semantics 没写清”。这是更早、更窄、可定位的根因。

## 5. 本轮总判断

### 已经证明

- Extreme right-tail 可以显著改变 Ontology 与 Changed Verbs，同时保持一句话可懂。
- 当前 Extreme Forge **不是过度保守**；它甚至能自然产出《天下第一道伤口》《门胚》这种明显偏离标准人形修士的货架前提。
- Independent Compiler 没有惩罚怪异或强度；两次都保留 bold core，只因真实因果缺口拒绝 strict PASS。
- Primitive Closure 是有效方向：它减少了 long-form mechanism creep。
- Matched Mutation Ladder 有价值，但 LLM 会把 aggressive 退化成 `bigger reach / bigger network`。

### 尚未证明

- **尚无 strict PASS 的 Extreme S3，因此本轮没有合法进入 World / Power / Human / Story / Outline / Chapter 1–5。**
- 因此“Extreme premise 会不会被下游磨平”这个原始 E7 问题仍然未被真正回答。
- 尚未证明哪一档 M0–M4 是作者要冻结的电压；本轮也不应由模型替作者选。
- 尚未证明 Primitive Closure 应进入 production Forge；目前只是一轮 `DIRECTIONAL PASS`。

## 6. 下一批最有信息量的实验

不是继续抽 S3 直到 PASS。

更合理的下一步是：

1. **Conditional Scale-Binding Treatment**：只对“核心特权会借用载体 / 身体 / 器物尺度”的 premise，要求一句明确的 `effect scale source + growth mapping`；同时把运动结果写成可观察几何，而不是靠画面补因果。目标仍是 Extreme，不是加一张通用表。
2. **Lateral Mutation Ladder**：固定 carrier class、最大 reach 与核心原语，M0→M4 不许靠城市/战争尺度变大；只允许通过原语组合、身体改变、占有关系、Public Repricing、敌人反制与玩法选择提高电压。
3. 若上述 fresh Treatment 首次得到 strict PASS，再恢复原 E7：真实跑到 Chapter 1–5，定位 downstream 的第一处电压损失。

不要做：自动 Repair、自动 selector、第三次无上限重抽、per-chapter Premise Reviewer。

## 7. 调用记录

| 调用 | 模型 | Agent wall |
|---|---|---:|
| E7 Extreme Forge | Luna high | 389.588s |
| E7 Independent Compiler | Terra high | 145.148s |
| E1 Mutation Ladder | Luna high | 193.205s |
| E7b Primitive Closure Forge | Luna high | 422.007s |
| E7b Independent Compiler | Terra high | 194.016s |

顺序 wall-clock 合计约 22.6 分钟。没有为了拿 PASS 改模型、降 effort、换候选或进入自动修复。
