# Scene Skill v1.1 真实章节 A/B/C 实验报告

## 执行边界

本次有效实验使用 8 次独立 Codex `luna_worker` 子代理调用：

- Chapter 2：1 次 Curator + A/B/C 各 1 次 Primary；
- Chapter 3：1 次 Curator + A/B/C 各 1 次 Primary。

每个 Primary 子代理只收到自己的 Primary Prompt，不知道其它实验组；A/B/C 的 Prompt 在去掉 `ACTIVE SCENE SKILLS` 区块后完全相同。没有运行 Director、Specialist、Integrator、State Delta 或 Review，没有写入 BOOK、正式章节 Canon 或生产源码。6 份 Primary Response 全部被当前确定性 parser 成功提取。

子代理角色统一为 `luna_worker`；当前实验环境没有独立暴露可核验的底层模型名，因此不猜测具体模型。

## Curator Selection

### Chapter 2

实际选择：

```text
Primary: social_bargain_decision
Secondary: hunt_acquisition
```

这是合理选择，不记为 Selection Failure：本章既有条件谈判，也有主角主动寻找并取得适合伤势的临时招式。它与参考答案的差异只在 Secondary，不改变事件合同。

### Chapter 3

实际选择：

```text
Primary: trial_challenge
Secondary: combat
```

选择合理，准确对应公开取牌门槛和周既明的阻拦动作。

## Chapter 2 判断

### A — No Scene Skill

事件完整，谈判、半步试探、一次完整示范、守约和章末公开考核入口都成立。它的优点是直接、具体，并用练功袋把回身卸力步落到可见动作上；不足是谈判中的条件变化和许照重新估值相对线性。

### B — Scene Skill v1

比 A 更明确地写出“拒绝 → 条件 → 试探 → 信息重新变得有用 → 示范成立”的顺序。谈判已经不是轮流交换台词，但中段仍较快地把条件收束为同意。

### C — Scene Skill v1.1

本章最佳。许照先用半步和假转身测试，顾长川拒绝把半招当完整招；她继续追问“如果已经被周既明带住”，顾长川用具体站位和受力回答，信息因此真正改变了她的决定位置，随后才完成一次完整示范。周既明听见交易后也改变明日出招安排。C 没有增加战斗、第二次示范或其它剧情，只把谈判的局部动力写得更清楚。

结论：Chapter 2 保留 v1.1；A 本身可读，B 已有效，C 的增益是实际的但属于场景执行增益，不是事件增益。

## Chapter 3 判断

### A — No Scene Skill

规则、取牌、回线、越线判定和身份边界都清楚，事件没有漂移；但公开考核和回线压力被压缩得更快，周既明的动作反馈层次少一些。

### B — Scene Skill v1

明显改善了考核的连续动力：假动作不触发主角行动，真实进攻才触发回身卸力步；取牌后立即切换为普通脚步回线，周既明改为封路并最终越线。它没有强制增加“先失败一次再重试”。

### C — Scene Skill v1.1

本章略优，B 很接近。C 更稳定地保持“公开规则与当前成功线 → 假动作 → 真实进攻 → 位置改变 → 取得合格牌 → 能力消失 → 普通脚步回线 → 现场判定”的因果链，并保留了许照确认守约、周既明承认公开竞争关系等短暂社会反馈。C 没有添加计划外失败轮次、永久掌握或正式入内门。

结论：Chapter 3 保留 v1.1；增益存在，但幅度比 Chapter 2 更克制，当前没有理由继续扩写 Scene Skill 或新增框架。

## 跨组副作用检查

- 事件漂移：未发现。Chapter 2 没有提前使用回身卸力步；Chapter 3 都只在周既明真实进攻后使用一次，并完成取牌回线；正式入内门和 Chapter 4 均未提前发生。
- Reader-First：六版都能读懂人物、目标和结果；B/C 在关键动作的因果可见度更好。
- Human Reaction：B/C 都让许照因信息和守约改变行为，也让周既明改变公开竞争策略；没有只靠微表情占位。
- Planning Language leakage：在六份 `chapter.md` 中未检出“验证、闭环、阶段推进、价值兑现、成长空间、建立优势、事件合同、Scene Skill、Primary Writer、Curator”等后台术语。
- 固定模板：没有观察到 v1.1 新增强制失败、固定 reversal 或固定 beat。半步试探和一次示范是冻结事件合同要求，不归因给 Scene Skill 副作用。

## 最终结论

`f15190b` 的 Scene Skill Content Deepening 应保留并冻结。当前两章证据支持它改善谈判和考核动作的局部表达，且没有改变 Canon 或增加运行期复杂度；证据还不足以证明每一种场景都同样受益，因此下一步如继续，应做更广的冻结输入正文实验，而不是继续增加 Skill 数量、Utility、Modifier、评分器或 Hard Gate。

## 证据索引

- `CALL_LOG.json`：8 个有效 Codex subagent 调用；
- `PARSER_STATUS.json`：6/6 Primary parser 成功；
- `SOURCE_MANIFEST.json`：冻结输入与 A/B/C 结构；
- `chapter-0002/*/primary_response.md`、`chapter-0003/*/primary_response.md`：8 份原始 Curator/Primary Response；
- `chapter-0002/*/chapter.md`、`chapter-0003/*/chapter.md`：6 份 parser 提取正文；
- `EXTERNAL_API_ATTEMPTS.json`：收到本轮子代理规则前误触发的外部 API 失败记录，不计入实验；
- `EXCLUDED_EXECUTION_FAILURES.json`、`EXCLUDED_UNASSIGNED_AGENTS.json`：未纳入 A/B/C 的执行级事件。
