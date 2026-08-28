# Progressive Long-form Authority Architecture A/B

日期：2026-08-28
状态：**production architecture adopted；Human Development 的独立质量增益仍属 bounded evidence**

## 1. 问题

旧 production 把 `WORLD_VISION.md` 当成全书单一世界权威；World 修改只有 Rewrite 语义，会 stale Power/Human/Character。Story Program 主要是开书一次 Collision，几百章后没有 `Expanded World × Current Character` 的正式 Re-Collision。

这会造成四个长期问题：

1. 开书 World 被迫过早承担 500 章具体世界；
2. 后期新能力散落 Canon，没有显式 Current Power planning authority；
3. Frozen Human 能防短期漂移，但没有合法的长期人物发展；
4. 真正多世界副本没有 instance-local World Authority。

同时需要验证一个用户明确指出的风险：**单 Agent 同时创造未来世界、人物发展与未来 Story，会在内部自洽掉真正的 Surprise / Collision。**

## 2. A/B

两个冻结 Case：

- `xuanhuan_ch120`：普通玄幻，青州层已经基本活透，需要进入更大世界；
- `multiworld_ch80`：已完成三个独立世界，需要第四个真正不同的 Local World。

比较：

- **X｜Monolithic Sol**：同一个 Sol high 同时看 World Root + Frozen Human + Current Canon，一次完成 World Expansion / Human Development / Current Character / Future Story；
- **Y｜Split World**：Luna high protagonist-blind World Expansion → 已发生人物事实 → Sol high Re-Collision；不新增 Human Development Agent；
- **Z｜Split World + Human**：Luna high protagonist-blind World Expansion ∥ Luna high Human Development（只看 Frozen Human + Canon）→ Current Character → Sol high Re-Collision。

## 3. 结果

两组 blind judge 均没有选择 X 为首选。核心失败不是“写得不连贯”，恰恰相反：**它太会连贯**。

单 Agent 最常见的问题：

- 新世界资源/职业/冲突明显针对当前主角能力缺口；
- 人物成长与未来世界主题互相证明；
- 新奖励过早形成“刚好补 Build”的钥匙孔；
- 世界人物更像教学/验证主角的新组件，而不是自己已经在活的人；
- Surprise 被预先消化成漂亮的因果闭环。

Split World 的主要增益：

- 新世界先作为独立现实成立；
- NPC / 组织可以拒绝、误价、损害主角计划；
- 旧 Power 在陌生世界产生未预先设计的用途；
- Story Engine 更容易换挡，而不是同一玩法换皮；
- Re-Collision 才决定主角实际追什么、错过什么、获得什么。

最终跨 Case synthesis 选择的 production topology：

`protagonist-blind World Expansion → optional independent Human Development → deterministic Current Character → Sol Story Refresh / Re-Collision`

## 4. Human Development 的证据边界

两个测试 Case 中 Human Development Agent 都返回了 `NONE`。因此：

- **已证实**：它能守住“不因短期行为强行改人格”的边界；
- **未证实**：额外 Human Agent 在“人物真的已经稳定改变”的 Case 上是否显著优于其它最小实现。

Production 仍保留它，但作为**更慢、可选的 correctness clock**：不是每次 World Expansion 必跑，不是每个副本必跑；只有长历史已经可能让 Frozen Human 单独使用失真时才调用。`NONE` 不创建 Delta。

## 5. Production 决策

### Stable Origins, Evolving Authorities

- World Root：开书根语法 + 当前 World Horizon；
- World Expansion：forward-only，`macro / instance`；
- Power：Frozen Origin Core + Canon Current Power Portfolio；
- Human：Frozen Origin Core + Current State + chronological Human Development Deltas；
- Current Character：纯确定性编译，不调用 LLM；
- Story Refresh：新 Effective World 与 Current Character 的 fresh Re-Collision；
- Outline：刷新后读取 Effective World + Current Character，不回到 T0。

### Story Program Handoff

开书 Story Program 不再具体预写所有未来世界。当前 World Horizon 接近末尾时输出 `World Horizon Handoff`：

- 可观察触发条件；
- `macro / instance` scope；
- 为什么当前世界层已经需要扩；
- 必须 carry forward 的已批准/已发生事实；
- orchestration：`World Expansion → Current Character → Story Refresh`。

**Handoff 不注入 World Agent。** 它只负责告诉系统“什么时候该扩”，不告诉独立 World Agent“为了当前主角应该扩成什么”。

Outline / Review 也不能越过未执行 Handoff 自己补未来十章/百章。

## 6. 多世界副本

`scope=instance` 支持独立 Local World 的生效窗口：

- 进入前不污染旧章节；
- 当前副本期间进入 safe `WORLD AUTHORITY`；
- 离开后 Local World 自动退场；
- 真正带走的 Power / Asset / Relationship / Identity / Knowledge / Meta consequence 继续留在 Canon。

因此不需要一个巨大 `dungeon_scene_skill`，也不需要把几十个未来世界预塞进开书 World Vision。

## 7. 测试

新增 `tests/test_long_form_evolution.py`，覆盖：

- World Rewrite / Expansion stale 区分；
- expansion forward-only；
- bounded instance window；
- Writer 只拿 safe expansion facts；
- World Prompt 与 GBrain brief 均 protagonist-blind；
- Human Development 不看 Future World，`NONE` 不制造人格变化；
- Current Character 两层 Power / 三层 Human 编译；
- Story Program Handoff 与 Outline stop boundary；
- refreshed Outline 读取 Effective World + Current Character；
- Story Refresh 在 Current Character stale 时被阻止。

最终专项 `tests/test_long_form_evolution.py` 为 `12/12 PASS`；全量 `python -m pytest -q` 为 **336/336 PASS**。

## 8. What This Did Not Solve

- 没有证明“每约100章扩一次”是最佳频率；production 是 Story-boundary trigger，不是章数税；
- 没有证明 Human Development 在真实长期人物变化 Case 上的净质量增益；
- 没有做 500 章真实小说 E2E；
- 没有证明连续 10—20 个副本的 Macro Variation 已经稳定；副本流 source-first Deep Distillation 仍可继续补这一层 craft；
- 没有新增 deterministic RPG 数值模拟 / 大库存数据库；这不是本架构目标；
- 没有让 World Expansion / Story Refresh 变成每章节点，也没有新增 Reviewer / Scorer / Coordinator。

## 9. 最终判断

这次不是“为副本流加补丁”，而是把 TGN 从：

`Frozen Origins + Canon + One-shot Story Program`

升级为：

`Frozen Origins + Forward World / Power / Human Evolution + Deterministic Current Character + Periodic Fresh Re-Collision`

最重要的质量保护不是更多 Prompt，而是**创造未来的 Authority 彼此先保持独立，惊喜留到 Collision 才发生。**
