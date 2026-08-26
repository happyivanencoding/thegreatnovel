---
schema_version: reference-corpus-card-v1
card_id: prose-character-voice-pressure-routing-v1
card_type: prose-control
knowledge_level: CROSS_BOOK_CONTRAST
status: HOLD
source_book_ids:
- rcv0-20-gaowu-quanqiu-gaowu
- rcv0-03-dushi-xiuzhen-chatianqun
- rcv0-27-dushi-diyi-xulie
- rcv0-28-xuanhuan-jiangye
- rcv0-18-lingyi-daogui-yixian
- rcv0-29-xuanhuan-guimi-zhi-zhu
evidence_refs: []
evidence_scope: MULTI_BOOK
maturity: PILOT
active_inspiration: false
title: 人物声音压力路由：用不同压力处理方式区分声音（HOLD）
---

# Character Voice Pressure Routing v1 — HOLD

## Shared Creative Problem
同一压力进入多个角色后，模型容易把所有人写成冷静、聪明、边界清楚、短句谈条件的同一种声音。

## Mechanism
只从当前 Canon、关系位置、知识差和已存在的人物行为中选择不同的压力处理通道，例如计算、纠正、嘴硬、玩笑、礼貌、回避、命令、交易或继续行动。声音差异来自“人物注意什么、误判什么、拒答什么、保护什么、把什么当筹码”，而不是额外发明口癖或性格标签。

## Applicability
只有当前场景存在明显 voice merge 风险，且输入已经支持角色之间不同的知识、利益或反应方式时，才有候选价值。

## Guidance
Curator 若使用，只应把当前场景的差异编译成 1–2 条局部压力，不要求每个角色都展示独特动作，也不要求对白逐句改变筹码。

## Failure Modes
- 为区分声音凭空新增性格、过去或口癖。
- 把“更活泼/更冷”当作人物区分。
- 为制造人味强行加入停顿、手部动作或玩笑。
- 把所有场景都变成多人声音展示。

## Evidence Basis
全球高武、修真聊天群、第一序列、将夜、道诡异仙、诡秘之主的 bounded Selection DNA v2。

## Status
HOLD。暂不加入生产路由；需要独立 A/B 验证后才能考虑激活。
