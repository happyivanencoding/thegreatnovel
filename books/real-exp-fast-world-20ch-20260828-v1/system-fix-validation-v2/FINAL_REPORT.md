# Fast World 20ch — System Fix Validation v2

## Scope

修复两份审计共同指出的系统问题：Supporting Logic 重新抢 Story Engine、职业人格过强、奖励/欲望前景不足、Public Proof 过度克制、Plot Pace 与 Tier Pace 绑定、高速成长因果不足、Rival 反制无效、Mystery 过早资源化、Backstage Abstraction Leakage、World Horizon 缺少读者可见外缘钩子与 continuity 漂移。

## Root cause

旧规则并未消失；新旁路是：`Human 职业型责任偏好 × World 公共资源素材 → Story Collision 判断高度匹配 → 正式批准为长期 Story Grammar`。Primary 与 Reviser 只是后续展开/保留。Backstage Abstraction Leakage 例外：真实追源确认“身份入口”由旧 Reviser 自己新增。

## Production changes

- Human Occupational Trait Ceiling：责任/审计/边界/路线等大幅降为低权重局部习惯；主角不是协调员。
- Character relevance != Story Engine authorization。
- Major Reward Anchor / Big Direction First：阶段先锁真正值得馋的对象/胜负/关系/谜团；公共资源冲突只留大方向选择和直接后果。
- Plot Pace != Tier Pace；异常高速升级必须由 Core Asymmetry / Advantage Stack 承担因果。
- Mystery Before Settlement；长期 Rival 学到边界后至少一次反制真实奏效。
- Authority Reviser 激进压缩 process carrier；新增 Backstage Abstraction Translation 与 Named Entity Continuity Sweep。
- Public Proof：Collective Shock、Ruler Calibration、Behavioral Repricing 三路并列、无高低；大型节点允许一起吃满。
- World Horizon Handoff 可复用已批准外缘信号制造“山外有天”读者钩子，但不提前发明下一世界答案。

## Human A/B

同一九垂原、同一 Human GBrain：

- **Production strong**：候选主要由钱、胜负、远行、审美、享受、自由、偏袒、占有等私人牵引驱动；职业性责任不再占前景。
- **MAX**：进一步把职业型理性压到几乎只剩手段，候选第一辨识度集中在审美/享受/性欲/面子/好奇/亲密占有/报复/野心。

两档都保存；MAX 不自动 productionize，由作者判断是否过头。

## Story Program A/B

Baseline 的长期发动机大量围绕责任、损失、路线、矿权、粮道、迁徙协调。

Current production 变为：

`潮路生两身 → 百炉夺槊 → 深矿猎王 → 万井关系/生活兑现 → 裂潮关断矿 → 两身镇海`

明显把前景改为夺取、越阶、具体奖励、关系后果、Rival 与 World Mystery。

MAX 更激进：前10章可叠加反潮楔、名刀、永久行潮籍、奖金、百炉护印；中段越阶猎镇海目标；终段再拿炉心、矿脉开采份额、现金与自己的商队。Authority/因果边界未作为自动淘汰理由，强度交作者决定。

## Ch15 Reviser A/B

- Baseline final: ~4160 chars
- Production Reviser: ~4241 chars；更注意删协调解释，但 Frozen Mission 本身仍是井/粮道/迁徙冲突。
- MAX Reviser: ~3165 chars，约 -24%；保持大方向 Mission/结果，但显著压缩谁守哪里、谁撤哪里等 process carrier。

结论：Reviser 可以做强保险，但不能把已经冻结错误的 Story Engine 改成另一种故事；根修必须上游完成。

## Ch14 Public Proof A/B

MAX 在同一 Frozen Authority 下形成三段并列兑现：

1. 开炉场声音断掉/多人同时止声；
2. 懂行者说明普通成炉者只能稳住自身附近，而顾停舟把整段潮势送到四十丈外并改向；
3. 阮青蜃笑意消失并立刻重谈价格，周围人让位、重新看待回潮楔与顾停舟。

结论：Collective Shock + Ruler + Repricing 可以同时成立；不应把群众震动默认降级。

## Backstage language source trace

旧 Ch4 Primary 原句：`以后我能自己接案、合法带潮器，也能用自己的名字登记潮路结果。`

旧 Reviser 自己扩成：`对普通人来说，这是离开聚落的身份入口。`

新 Reviser 复验同一 Primary/Authority 后写成具体人话：`以后我能合法持有潮器，以自己的名字接案、登记路线结果，也得自己承担潮路上的风险。`

因此 Backstage Abstraction Leakage 确实有一部分来自第二审计；新增 Translation 规则真实有效。

## Continuity

已修：阮青蜃性别漂移、唐绾年龄/资历称谓冲突、镇潮军府正式名漂移。

## Verification

- Focused contracts: PASS
- Full suite: **358/358 PASS**
- `git diff --check`: PASS

## What this did not prove

- 没有证明 MAX Human / MAX Story 应直接成为默认强度；作者仍需比较真实输出。
- 没有重写原20章全文验证所有新上游规则的长期组合效果；当前验证是冻结样本的 Human/Story/Reviser/Public Proof 受控 A/B。
- Reviser 无权修掉已经冻结在 Chapter Mission 里的错误 Story Engine，因此不把它当上游修复替代品。
