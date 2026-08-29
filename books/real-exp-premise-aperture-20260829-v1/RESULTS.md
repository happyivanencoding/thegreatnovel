# Premise Aperture Controlled Experiment｜Final Results

日期：2026-08-29

状态：`EXPERIMENT COMPLETE / PARTIAL FREEZE RECOMMENDED / AUTHOR DECISION PENDING`

Production default：**未改变**

## 1. Executive Verdict

当前 TGN 想不出足够精彩、足够大胆设定的最早根因，不是 Writer、不只是 GBrain，也不是 World / Power Prompt 缺少更多“创新字段”，而是：

> 旧 Fantasy Seed 被正确移除后，系统保护了 World / Power / Human 的独立 Authority，却没有在任何 Authority 冻结前保留一个非 Canon 的完整 Premise 搜索空间。

结果是各 lane 都能给出完整、合理、可持续的答案，却在真正形成高风险核心幻想之前就收敛为安全的人类主角、职业性能力和可解释世界。

受控实验支持下面的**候选开书架构**：

```text
作者方向
  → Single-Agent Premise Forge：一次生成 S1 / S2 / S3 完整候选
  → Independent Premise Authority Compiler：只审可满足性
  → 作者选择 / 修复 / 放弃；不自动 selector
  → lane-specific frozen contract
       World：World-only + protagonist-blind public interface
       Power：literal Ontology + Initial Scale Position
              + trigger / target / action / carrier / root boundary
       Human：literal Ontology + exact T0 Origin + Initial Scale Position
       Story：Authorities 批准后第一次看完整 Promise
  → 现有 Split Authority production chain
  → Outline / chapters 只读 approved Authorities
```

它不是第四 Authority，也不是旧 Fantasy Seed 的复活；在作者明确冻结前，只是可回滚的开书实验路径。

## 2. 从四本扫榜素材得到的判断

四本书的共同优势不是“机制更复杂”，而是把以下内容早早绑成一个主押注：

- 《仙品从考入府学开始》：熟悉修仙世界 + 妖魔宴席反客为主 + 少年主角狠辣姿态 + 立即反杀与夺宝；
- 《不懂，我玩猿神的》：弱势南方古猿 + 现代知识和群体投掷新动词 + PVP 公频嘲讽／破防；
- 《天父》：主角直接成为远古巨蛇幼体 + 伏击、绞杀、吞食、蜕变等非人身体动作 + 生态地位变化；
- 《灵气复苏，我在荒岛肝属性》：熟悉属性成长 + 空难荒岛 + 网络直播与观众反馈 + 每次劳动立刻得到数值回报。

它们不是每个部分都陌生，而是：

> 熟悉商业类型 + 一处真正大胆的大偏离 + 第一章即可验证的新动词 + 立即兑现 + 社会／生态反馈。

旧 TGN baseline 更容易先完成世界合理性、职业位置和流程因果，最后只剩 Story Program 在安全 Authority 之间排列事件；此时再要求它发明非人本体、根能力或公共叙事界面已经太晚。

## 3. Hypotheses

### H1｜缺的是完整 premise search，而不是更多局部创新字段

若在 Authority 前增加一次完整 Premise Forge，应提高 Click / Bold / Changed Verbs / Payoff，同时保持一句话可懂。

### H2｜多 fresh-context 高电压轴不一定优于单代理完整 premise

若“独立代理越多越有创意”成立，四轴固定碰撞应至少不弱于 Single-pass；否则说明 isolation 是防泄漏工具，不是 composition optimizer。

### H3｜上游候选好看不等于可编译

候选必须先证明第一章动作、T0 尺位和远期复合能由明确字段推出，再进入昂贵 downstream；Forge 的自我 Trace 不能自动视为真。

### H4｜作者选择后的字段必须保真

World / Power / Human lane isolation 通过，仍可能静默搬移出生、缩窄能力或降格 Interface。需要 lane-specific frozen contract 与 fail-loud。

## 4. Protocol

### 4.1 Frozen Cases

- `generic_fantasy`：普通玄幻；
- `fast_multiworld`：20 章一个世界、快速升到当前世界顶层；
- `game_instance`：副本流 / 游戏副本。

Baseline 均使用既有 production artifacts，不重抽。

### 4.2 Treatments

- `B0`：Current production baseline；
- `S1 / S2 / S3`：一个 fresh Luna-high Agent 一次生成三张完整 premise cards；
- `C1 / C2 / C3`：World / Ontology / Privilege / Interface 四个 fresh-context 轴，各生成三项；代码预注册配对，再由 Collision Agent 补最小桥梁；
- `V1 / V2 / V3`：两押注 Voltage Budget；
- `Trace v2 / V3 / V4`：逐步加入 Authority-Compilation Trace、Initial Scale Position 与 independent compiler。

主实验未向模型提供四本扫榜作品的角色、专名、事件组合或具体能力，只提供“高风险押注、强画面、新动词、立即兑现”的抽象 craft。

### 4.3 Anti-Cherry-Pick

- C 配对由代码固定；
- S2 / C2 在看输出前预注册为 downstream 样本；
- V4 S2 在生成前预注册；
- 同时报告整个 candidate pool；
- 评审采用 3 case × 3 独立 casewise blind review；
- 跨 case batch panel 出现上下文串扰，已标为 `INVALID / SUPERSEDED`；
- 当预注册 S2 被 independent compiler 判 FAIL 时，停止 downstream，不换成更好的 S1 / S3 冒充成功。

## 5. Quantitative Evidence

### 5.1 Valid Casewise Blind Panel

| Case | B0 | S1 | S2 | S3 | C1 | C2 | C3 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Generic Fantasy | 76.3 | 86.3 | **88.7** | 83.7 | 69.7 | 71.3 | 76.7 |
| Fast Multiworld | 68.0 | 82.3 | 84.3 | **87.7** | 74.7 | 68.0 | 68.0 |
| Game Instance | 83.0 | 81.0 | 82.3 | **89.3** | 76.3 | 67.0 | 74.0 |

跨 case pool 平均：

| Pool | Overall |
|---|---:|
| Single-pass S pool | **85.1** |
| Current B0 | **75.8** |
| Four-axis C pool | **71.7** |

预注册同位比较：

| Case | S2 − C2 |
|---|---:|
| Generic Fantasy | +17.3 |
| Fast Multiworld | +16.3 |
| Game Instance | +15.3 |
| Pooled | **+16.3** |

边界：

- 不存在可冻结的“永远选 S2”：Generic ceiling 是 S2，Fast / Game ceiling 是 S3；
- Game Instance baseline 已有 83.0，S1 / S2 略低，只有 S3 明显提高；
- Premise Aperture 扩大搜索分布，不保证每张候选都胜过强 baseline；
- 分数不能代替 direct reading 与 downstream preservation。

### 5.2 Calls / Wall Evidence

Single-pass 每本只需 1 次 Luna-high 候选调用；四轴方案需要 5 次调用（四轴 + collision）。

| Path | Calls / Book | Mean Wall / Call | Mean Output Chars |
|---|---:|---:|---:|
| Single-pass | 1 | 261.9s | 6473 |
| Four independent axes | 4 | 86.9s | 1585 |
| Collision | 1 | 157.0s | 5274 |

四轴调用更多、总计算更高，质量反而更低。没有冻结理由。

## 6. Direct Reading Evidence

真正拉开差距的不是专名密度，而是 **Changed Verbs**：

- `活脏`：空器官主角击败目标后移植其最强器官；
- `死后开战`：清醒归尸预先标记尸体，把死亡变成移动、复活与适应；
- `人间秘境`：主角本身是一座成长中的移动秘境；
- `活令`：主角是一句会爬行的活命令，把败者刚说出的命令割成黑字钉入实体；
- `走城者`：主角是一座行走城市，把建筑、巨兽与战争机械并入自身；
- `死式`：谁故意杀死主角，谁就把那次致死结果送给他；
- `一城吞门`：主角是一间活房子，吞进真实建筑与人并长成移动城市；
- `镜外有人`：谁看见完整倒影并给主角命名，就为他建立一处出镜路线。

相比之下，旧 baseline 更容易让标准人形主角继续执行观察、分析、探路、修复、登记、路线优化或职业性竞争。

## 7. Why Four-Axis Collision Failed

四个轴单独看并不缺创意。失败发生在整体 composition：

1. **Premise Competition**：每一项都要求解释、首章兑现和长期成长；
2. **Cognitive Load**：第一章同时建立世界异常、非人形态、直接特权和异层界面；
3. **Engine Competition**：四个组件各自能长成一本书；
4. **Coherence Tax**：Collision Agent 为共存增加桥梁、统一主题或改变 locked core；
5. **False Inference**：fresh-context isolation 防止偷看，不代表组件天然适合组成一个商业 premise。

Two-Bet Voltage Budget 能降低过载，但 V pool 77.3，仍低于 S pool 86.7；保留 `RESEARCH_ONLY`。

## 8. Downstream Preservation and Compiler Evidence

### 8.1 Orthogonal C2｜CONDITIONAL PASS

World、非人铜像 Ontology 与明日证词 Interface 均保留，但 Power 把“意识进入宿主、铜像留在原地”静默增强成双躯并行。证明 lane-safe 不等于 semantic-safe。

### 8.2 Single-pass S2 V1｜Direction-only Compiler｜FAIL

同一预注册 `活令` 发生三项不可接受改写：

1. 从“公开处刑后死者喉中诞生”搬到旧训练场破旗，并补出出生前 Biography；
2. Power 从门／兵器／野兽／人四类载体缩窄成只作用于活人；
3. 稳定公开重映被降成终局偶发演出。

结论：柔性 Direction 不可冻结。

### 8.3 S2 V2｜Lane-specific Frozen Contract

同一候选、同一预选 Power / Human 编号重跑。World、Human、Power 均完整保留字段；Story 没有静默圆，而是返回 `PREMISE-AUTHORITY CONFLICT`：

- 开篇群体逆转发生在夺词 trigger 之前，也超出 T0 只能让自身“不跪”的权限；
- 全城开门依赖未批准的复制／共同载体；
- Human T0 声位 0 不在 World 的 1—100 公共尺中；
- 终局全城“醒来”依赖未定义共同载体与语义扩张。

结论分开：

- frozen contract / fail-loud：**PASS**；
- 旧 S2 整合：**FAIL**；
- production freeze：**NOT AUTHORIZED**。

### 8.4 Authority-Compilation Trace v2

加入 Forge 自检后，三张卡仍大胆，但独立审计发现 Trace 会把自己的隐含桥梁写成“已经合法”：未满足 trigger、Interface 偷放大、T0 尺位无公共语法、终局假设共同载体。三张均 FAIL。

结论：Trace 必须保留，但不能替代 independent compiler。

### 8.5 V3 Initial Scale Position

增加 `Initial Scale Position-only Direction` 后，Human 不再需要自行猜主角 T0 等级。它解决了字段缺失，却仍不能解决开篇动作与远期成长的假桥梁。

### 8.6 V4 Independent Premise Authority Compiler

三张新候选仍保持强货架电压：

| Candidate | Verdict | Exact result |
|---|---|---|
| S1《死式》 | CONDITIONAL PASS | 开篇合法；18—20 章到命火尺 9 与关闭死潮缺少已定义成长映射 |
| S2《一城吞门》 | FAIL | 棚屋未真实完整过门；后墙门不存在；五名见证者未建立；界壳核心不能自动推出 9 阶 |
| S3《镜外有人》 | CONDITIONAL PASS | 一次出镜只允许一次动作，却连续夺钥匙、割门绳；尺位与九锚点 runway 基本闭合 |

V4 S2 在生成前已预注册。Compiler 判 FAIL 后，实验在 World 生成前停止，没有换样本或强行下游。这证明它能用一次窄开书检查提前阻止昂贵的无效 Authority 链。

### 8.7 Selected Premise Repair V5｜FAIL

对预注册 S2 允许一次 Luna-high 定点修复，并由代码锁死标题、货架简介、非人 Ontology、Changed Verbs 与不可磨平项。修复补上了完整过门、同一真实门、五名见证者和逐级壳层结构，但漏掉了整个受保护 `主角反复会做的新动作` 字段，并把窄修复扩写成大范围重构。

确定性 protected-core validator 在独立 Compiler 复检前停止；没有事后把旧字段复制回来，也没有进入 downstream。结论：Selected Premise 自动修复当前 `FAIL / RESEARCH_ONLY`。Compiler 失败时应先把精确冲突交给作者。

## 9. Architecture Findings

1. **Premise search must precede Authority freeze.**
2. **One complete premise generator beats multiple equal-voltage components.**
3. **Forge self-consistency is not compiler correctness.**
4. **Independent compiler must audit satisfiability, not commercial taste.**
5. **Author choice remains the creative gate.**
6. **Selected premise becomes lane-specific binding constraints, not a fourth Authority.**
7. **Fail-loud is better than silent semantic smoothing.**
8. **Raw Premise Card must disappear before Outline / chapter runtime.**

## 10. Framework Decision Table

| ID | Candidate | Current Recommendation |
|---|---|---|
| F1 | Premise search before Authority freeze | **RECOMMEND FREEZE** |
| F2 | Single-Agent Forge produces S1 / S2 / S3 complete cards | **RECOMMEND FREEZE AS OPTIONAL OPENING STAGE** |
| F3 | Independent Premise Authority Compiler before author selection | **RECOMMEND FREEZE AS NARROW OPENING CHECK** |
| F4 | Author selects / manually resolves conflicts / rejects; no auto selector | **RECOMMEND FREEZE** |
| F5 | Lane-specific frozen contract + fail-loud + raw card not passed downstream | **RECOMMEND FREEZE** |
| F6 | Exact prompt wording, token budget, model configuration | **KEEP EXPERIMENTAL** |
| F7 | Selected Premise automatic repair | **TESTED FAIL / RESEARCH_ONLY** |
| F8 | Four-axis full collision | **REJECT** |
| F9 | Two-Bet Voltage Budget | **RESEARCH_ONLY** |
| F10 | Model/Judge automatic conservative or highest-score selector | **REJECT** |
| F11 | Restore old unified Fantasy Seed | **REJECT** |

Recommended freeze means freezing architecture boundaries, not silently enabling an unskippable production default. Before default-on, require at least two additional topics with `Compiler PASS → real downstream PASS`.

## 11. Implementation Status

Implemented, tested, but not wired into production default:

- `src/story_mvp/premise_aperture.py`
  - Single-pass Forge prompt;
  - four-axis and Two-Bet research paths;
  - Initial Scale Position;
  - Authority-Compilation Trace;
  - Independent Premise Compiler prompt builder;
  - Selected Premise repair prompt + protected-core validator (research-only; real test FAIL);
  - single-card response normalization + fail-closed parser;
  - code-fixed collision matrices and lock validation;
  - lane-specific frozen bundle and projections;
  - explicit conflict detection.
- `tests/test_premise_aperture.py`
  - non-Canon contract;
  - exact S1 / S2 / S3 compiler input;
  - parser fail-closed;
  - lock preservation;
  - lane isolation and frozen-field projection;
  - conflict detector;
  - compiler does not score, choose or repair.

## 12. What This Did Not Solve

- 哪一档候选适合所有题材；
- Compiler 失败后的正式边界已倾向“把精确冲突交给作者”；自动定点修复一次真实测试漏掉受保护字段，后续只作 research-only；
- 两个额外题材的 `Compiler PASS → downstream PASS`；
- 同一 Changed Verb 到百章后是否会变成一招放大；
- 正文 prose、章节 Runtime 或章节速度；
- Compiler 增加的一次开书调用的最终净成本。

## 13. Final Proposed Decision

建议作者批准以下组合：

- 冻结 F1—F5 的**架构边界**；
- F2 / F3 先作为可选、可跳过的开书入口；
- 暂不默认接入所有新书；
- 拒绝 F8 / F10 / F11；
- F9 保留 research-only；
- F6 / F7 继续实验。

在作者确认前，production 默认开书链保持不变。
