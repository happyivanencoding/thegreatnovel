# CONTINUATION REVIEW｜第6—10章

## Verdict

- **Chapter continuity / State advance：PASS after bounded repair**
- **Reader-facing Power concreteness：PASS**
- **Supporting Logic 不成为 Story Engine：PASS**
- **Personality → Choice / Route：PASS**
- **Personality → sensual / bodily prose projection：DIRECTIONAL PASS，残余仍在**

## 第6—10章发生了什么

- 第6章：顾临川一行抵达古代石城外墙，第一次遇到观日宗、陆问山与顾斜阳；他没有为了靠近传承把药车和伤员带进交战区，先把撤离位置留出来，同时与顾斜阳发生第一次公开利益冲突。
- 第7章：分影第一次真正承担互相看不见的两条路线。本体护送陆绾、药车和伤员，影身跟随顾斜阳与观日宗弟子进入另一条石城路线。
- 第8章：影身已经看见可能通向传承的影光，但异兽即将堵死被困弟子。顾临川放弃继续追传承，让影身主动暴露引走异兽；影身被严重撕裂，传承机会没有被隐藏补偿回来。
- 第9章：残缺影身回返并与本体合并，石城记忆、战斗手感、恐惧和伤势一并回流。陆绾处理影伤；顾临川与顾斜阳都承认自己曾追逐传承，不替彼此改写责任。
- 第10章：统一说明不再重复证明分影机制，而把既有选择兑换成新的故事状态：顾临川获得一次观日宗外围试学资格，顾斜阳成为公开竞争者，阮青缨依据报告准备以正式高报酬商盟契约招募顾临川参与沉昼城古代影兵行动。

## Reader-facing Power

直接检索第6—10章 `结构 / 受力 / 路线计算 / 验证 / 诊断 / 流程 / 权限 / 分析`，命中为 0。

更重要的是直接阅读没有发现换词后的同类回归。第6章与第7章虽包含撤离路线选择，但它们只服务人物当前生死与利益冲突；没有把“找路”扩成顾临川的新专业能力。分影的长期变化仍然是：两具身体能分处不同现场、失去彼此视野、分别行动，并最终共同承担经验与伤势。

## Opportunity Cost

第8章是这五章最重要的选择点。顾临川确实想要石楼下的传承，而且入口已经在眼前；他选择引开异兽后，传承路线被留在塌楼与异兽之后。系统没有立即补一个同等级隐藏奖励抵消机会成本。

这让 Human 的“会被新鲜、漂亮、值得赢的东西吸引”与“具体的人会改变风险阈值”同时成立，而不是把他改写成从不动心的标准救人型主角。

## Personality prose residual

第9章比前五章更接近私人关系：陆绾扶住顾临川、处理影伤、按伤口、上药，并明确告诉他不要把影身当替死品。这让关系从纯工作边界向共同承担推进。

但 Human Seed 已批准的身体吸引与感官注意仍然很少进入 Primary prose。即使是第9章这种自然允许身体距离与感官注意出现的场景，Writer 仍主要选择医疗动作和责任语言，而不是顾临川对“这个具体的人”的身体/气味/靠近方式产生注意。

因此此前结论继续成立：**Personality → Choice 已经稳定；Personality → prose 的私人/身体性投影仍偏弱。** 当前证据不足以直接修改 production Prompt，应另做一次冻结场景的 Curator / Primary 投影定位实验。

## Bounded repairs

### Chapter 6

Raw Primary 有两个 continuity realization 错误：

1. 首次见顾斜阳却写成 `顾临川认出了顾斜阳`；正式正文改为先由观日宗弟子喊出顾斜阳的名字。
2. 上游未规定顾斜阳性别，Chapter 6 raw 临时写成女性，但 Chapters 8–9 连续实现为男性；正式 Chapter 6 统一为后续连续两章的男性实现。

两项都未改变剧情、人物欲望、结果或 State。修复记录见 `runs/chapter-0006/continuity_repair.md`。

### Chapter 10

Raw Director 把 Chapter 9 已经成立的“影身严重受损后，经验/恐惧/伤势回归本体”误写为 Chapter 10 `首次确定`。在 Curator / Primary 前按 Proof-after-State 原则修正：第10章只可在报告中引用既有事实，不得重新证明；本章新增状态仅是试学资格、竞争关系、招募理由与阶段结算。修复记录见 `runs/chapter-0010/director_repair.md`。

## Validation / Runtime

- Chapter 1—10 全部通过 production chapter validator。
- 最终 `BOOK.md` 通过保存校验。
- `READER_COPY_0001_0010.txt`：22,125 个文本字符。
- `READER_COPY_0006_0010.txt`：11,193 个文本字符。
- `USAGE.json` 已重建为全部 **46 次**真实 ACP 调用；ACP ChatGPT 登录不返回 credits，继续明确记录 `N/A`。

## What This Did Not Solve

本轮是既有已批准 Story Program / Outline 的连续续写，不是新的系统 A/B。因此不能仅凭第6—10章把“私人/身体性人格投影不足”升级为 production 根因结论，也不应在本轮给 Curator / Writer 新增规则。
