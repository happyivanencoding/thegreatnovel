# Long-Form Pacing Window v1 + Dynamic Outline Validation

## 实验性质

本轮验证 Long-Form Pacing 是否能把固定章节 deadline 改成：早期商业锚点、稳定循环、动态中期里程碑和远期升格方向；同时把固定未来100章改成按故事密度选择的当前中期规划窗口。

本轮只重新解释旧版 Creative Chain 中的章节绑定，不重抽 Fantasy Seed，不重新优化 Compounding、Narrative、Eventization、Cost、Payoff、GBrain、Character、Canon、State Delta、Director、Writer 或 prose。

## 生产基线

- 用户指定开始 HEAD：`90b05697e94e2d70e5a57dd5ce7a0ea6434049ab`。
- Long-Form Pacing 生产修改 commit：`2c1e3434b6d68043ba0aac556e63d7912ba23368`。
- Creative Chain baseline：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`。
- Outline Eventization Fix：`2be35340b36aa05588c85324ffd5e2e1bfa6d951`。
- Outline paired validation：`90b05697e94e2d70e5a57dd5ce7a0ea6434049ab`。
- 当前生产 `src/story_mvp/prompts.py` blob SHA-1：`06ce9e78d9c4753b56bc7550129f54828763e7df`。

## 允许重新打开的范围

只重新打开并修改了 Long-Form Pacing 相关的 Fantasy Seed、World Vision、Story Program、Outline 语义，以及旧 BOOK long-plan 标题的最小读取兼容。其它生产层没有修改。

新增共享方向：`LONG_FORM_PACING_DIRECTION`。

## 候选与 Control

- Candidate A：`《偷走明天的人》`，过快尺度升格压力样本。
- Candidate B：`《掌中天工》`，健康速度保护样本。

Legacy Seed、World Vision、Story Program 和作者方向均来自 `books/real-exp-outline-eventization-v1/`，Control Outline 直接复制上一轮冻结 `outline_response.md`，均未重新生成。

## 逐层生成边界

每个候选独立执行：

Legacy Seed → 新 World Vision → freeze → 新 Story Program → freeze → 新 Dynamic Outline。

每层只生成一次，不自动重生成，不读取另一候选、不读取 reviewer、不使用 GBrain、Reference Programs 或历史实验。

每个 rendered prompt 先由主 Agent保存并逐字校验，再启动对应真实 Agent；校验失败时停止该层，不调用模型。每层 response 生成后立即冻结。

## Blind Comparison

最终匿名比较旧 Frozen Outline 与新 Dynamic Outline：长期上限是否保留、同层玩法是否横向展开、旧资产寿命、世界生态、B 的健康速度、Filler、Compounding、Narrative、Eventization、窗口边界和未来十章质量。盲审完成后才揭示 X/Y mapping。

## 最终判定

只有同时满足 A pacing 明显改善、B 健康节奏保留、Compounding/Narrative/Eventization 保留、无 filler、远期上限未损伤、窗口边界自然，才记录 `PACING_FIX_VALIDATED`，并正式记录 `CREATIVE_CHAIN_FROZEN_V2` 与 `OUTLINE_FROZEN_V2`。

本轮结束后停止，不生成 Chapter，不修改 Director/Writer/角色系统。

## 执行结果

- Legacy A/B Seed、World Vision、Story Program、Control：全部逐字复制，hash 校验通过。
- A/B 新 World Vision、Story Program、Dynamic Outline：各层独立 Agent 各生成一次；每层 prompt 均先保存并逐字校验。
- Dynamic Outline 窗口：A `N=60`；B `N=96`。
- Blind mapping：A X=Treatment/Y=Control；B X=Control/Y=Treatment。
- A：`A_PACING_IMPROVED`。
- B：`B_HEALTHY_PACE_PRESERVED`。
- 全局：`COMPOUNDING_PRESERVED`、`NARRATIVE_PRESERVED`、`EVENTIZATION_PRESERVED`、`LONG_TERM_RUNWAY_PRESERVED`。
- 最终：`PACING_FIX_VALIDATED`。
- 正式冻结建议：`CREATIVE_CHAIN_FROZEN_V2` + `OUTLINE_FROZEN_V2`。
- `FILLER_BLOAT`、`CEILING_DAMAGED`、`ARBITRARY_WINDOW_BOUNDARY`、`LOCAL_FIX_GLOBAL_DAMAGE`：未发现。
- 本轮不进入正文。
