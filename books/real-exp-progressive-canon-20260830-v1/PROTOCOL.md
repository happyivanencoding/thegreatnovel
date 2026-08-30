# Progressive Canonization / Author-Open Mystery Experiment

状态：`EXPERIMENTAL / NOT PRODUCTION`

## Hypothesis

长篇 Mystery 不要求作者开书时知道终极答案。系统应显式区分：

1. `AUTHOR OPEN`：作者自己尚未决定；
2. `AUTHOR FIXED HIDDEN`：作者已批准一小层真相，但人物/读者尚未知；
3. 已正式 Reveal 的事实继续进入现有 Canon，不由本机制另建数据库。

作者未决定时不是缺陷。只有当前 Story Horizon 真正无法继续定义高质量冲突/入口/选择时才触发低频 Decision Surface；若仍可继续，必须 `DEFER`。

## Cases

- A `meta_instance`：正控；来源于现有“故乡突然被界签标成第一副本 / 落日隧道 / 携带成果”书型。下一独立副本并不需要解释玩家/NPC/系统终极来源。预期 `DEFER`；不允许为了 World Expansion 强迫作者解释 Meta。
- B `identity_archive`：身份/历史谜团；当前路线要进入只认某种旧印记的档案层，必须先决定这枚印记至少属于什么类别。若 `DECISION NEEDED`，预注册实验选择 `R2`。
- C `relationship_betrayal`：关系/背叛史谜团；当前路线马上进入旧友正面对质，必须至少决定当年的开门是否是她自主承担的一项私人承诺，还是外力强迫。若 `DECISION NEEDED`，预注册实验选择 `R3`。

不因候选质量改选；Compiler FAIL 即停止该 Case 的 Treatment downstream。

## Treatment

`Author Open Mystery → Decision Surface → (only if needed) Non-Canon Reframe R1/R2/R3 + D0 → pre-registered author-choice simulation → Independent Canonization Compiler → planning-only Hidden Fixed Point → Story Refresh`

- Reframe 不能自动选择；
- D0 不得新增真相；
- Compiler 只审 backward compatibility / hidden boundary / remaining-unknown boundary，不评分；
- Hidden Fixed Point 只进入规划，不直接进入章节 Writer；
- 本轮不修改当前小说，不修改 production runtime。

## Downstream comparison

同一冻结 Effective World / Current Character / Existing Canon / Previous Story 下比较：

- `B0`：当前 Story Refresh，无 Author Mystery Control；
- `T`：加入 `AUTHOR OPEN` 或经 Compiler PASS 的 `AUTHOR FIXED HIDDEN` planning projection。

盲评重点：

- 是否吃书 / retrospective rewrite；
- 是否过早解释 Mystery；
- 是否还能产生具体下一阶段故事；
- 新 Fixed Point 是否只定一层而非写完整终极 lore；
- 是否让旧锚点获得新含义而不是作废；
- Meta Case 是否能在不解释玩家/NPC的情况下仍然让第二副本值得追。

## What this experiment does not authorize

- 不新增 per-chapter Mystery Agent / Reviewer；
- 不要求每个 Mystery 都有固定答案；
- 不把 `AUTHOR NOTES` 直接当 Hidden Truth 存储：当前 Chapter Context 会把 Author Notes 送入章节上下文，存在提前泄漏风险；
- 不冻结任何字段名、模型或 UI；
- 不自动回写 World Root / Human Origin / 已完成正文。
