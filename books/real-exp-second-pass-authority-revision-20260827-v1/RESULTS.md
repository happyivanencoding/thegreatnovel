# Second-Pass Authority Revision A/B｜2026-08-27

## 目的

验证在 `Director → Curator → Primary` 之后、`State Extraction` 之前加入一个 **Second-Pass Authority Reviser** 是否有价值。

它不是第二个 Director，也不是重新写一章；目标是在冻结 Chapter Mission 的前提下：

- 删除/压缩重复确认、重复能力证明、工程化/程序化实施、Competence Filler；
- 修复 Primary 漏掉的 Reader Release；
- 从远端但更高权威的 World / Frozen Human / Frozen Power 中恢复少量准确 realization；
- 保留正确正文，不做全章同义重写。

## 实验输入

冻结历史书：`real-exp-private-prototype-reader-facing-20260827-v1`。

每个 Treatment 使用完全相同的已生成 Primary Draft，不重跑 Director / Curator / Primary。

Second Agent 输入：

1. Frozen Chapter Mission：历史 `director_response.md`；
2. 近端 Attention：历史 `curator_response.md`；
3. Safe World Reality：由批准的 `WORLD_VISION.md` 确定性投影普通生活、力量正常值、社会现实、价值结构、公开知识边界；
4. Reader Release：`BOOK.md` 当前章已排程条目；
5. Frozen Power Core：`CHARACTER.md` 原样 authority；
6. Frozen Human Core：`CHARACTER.md` 原样 authority；
7. 上一章 Canon Tail；
8. 当前 Primary Draft。

不输入 raw GBrain，不授权修改剧情合同。

## 最终 Revision Contract

### Preservation First

默认不动已经正确的正文。只有存在可指出的具体失败才允许修改；一句有问题只改一句，一个短段有问题只改短段。未修改部分尽可能逐字复制 Primary Draft。

### Authority Fact Discipline

远端资料只能按明确陈述的强度进入正文。人物偏好不等于当前物品客观属性；角色特定动机不能泛化成世界规则；可能性不能升级成确定事实。

### Human Trigger

Frozen Human 不是每章配额。只有 Frozen Human 明确写了当前具体人物的身体/气味/姿态牵引，并且 Primary Draft **已经存在两人直接身体接触或近身治疗**，却完全漏掉私人注意时，才补恰好一个 cue。同场协作、共同搬第三人、隔物递东西不算。

### Reader Release

Reader Release 是既定 timing decision。逐条核对，每一条第一版漏掉的明确事实都补一次；无排程不自行开百科。

### Attention Reallocation

Supporting implementation 连续占据笔墨、却没有产生新选择/失败/关系变化/不可逆结果时，可以压缩，把笔墨还给 World Entry / Rival / Relationship / Core Fantasy / Choice / Payoff 等本章高价值功能。但不得删除 Mission 要求的结果或章末推动。

## 场景覆盖

- Ch5：强动作章 / 正样本保护。测试 Second Agent 会不会把本来好的章节改坏。
- Ch6：World Entry + Reader Orientation 缺失 + 路线实施偏多。
- Ch9：Core Fantasy + 近身关系场景。测试 Frozen Human 还原。
- Ch10：阶段结算 / 程序化压力。测试“删流程”会不会误删真实 Consequence。

## Condition A

历史 Primary 正文，不做 Second Pass。

## Condition B｜Luna medium

模型：GPT-5.6 Luna，reasoning medium。

### Ch5

最终版不再为了 Human Core 强塞陆绾气味 cue。主事件、选择、两路分流、反噬、未知影术痕迹和章末推动保持不变。整体与原稿高度接近；强章没有被重新规划。

判定：**PASS / preservation baseline**。

### Ch6

原稿漏掉的 Reader Release 被补：

- 观日宗是公开传授影术的宗门；进入折日峡寻找失落传承；顾斜阳与宗门大比 / 继承资格有关；
- 古代石城有珍稀药材、遗物与异兽，说明它为什么值得人靠近。

没有把银鞘刀擅自升级为稀有兵器，也没有把药车错误改成能通过只容伤员的窄坡。路线实施仍保留不少，因此对 Attention Misallocation 的修复是部分而非彻底。

判定：**PASS on missing orientation / PARTIAL on attention reallocation**。

### Ch9

Primary 原稿本来已有“陆绾回身抓住顾临川胳膊、顾临川几乎压在她手上”的直接身体接触。Treatment 只在这里补一个 Frozen Human cue：陆绾身上的药粉、风尘和晒热布料气味靠近。

没有改关系阶段、没有表白、没有改变影身回流事件；后续大部分正文原样保留。

判定：**PASS**。

### Ch10

保留了阮青缨读报告、正式高报酬招募与“两条路”章末推动，没有把它误判成报告流程删掉。只能局部压缩说明，因为“统一说明 / 责任追问”本身已经被 Director 写进冻结 Mission；Second Agent 无权改变这个上游 story anchor。

判定：**PARTIAL**。证明 Second Agent 只能阻止低价值实现继续膨胀，不能替代 Outline / Director 根因修复。

## Preservation 观察

在加入 Preservation First 后，Luna medium 各章大部分段落可逐字保留。不同随机运行有波动；最终目标不是追求某个百分比，而是确认模型不再默认全章换词。

具有代表性的受控运行中：

- Ch9：约 98% Treatment 段落可在原稿中逐字找到；
- Ch10：约 97% 量级；
- Ch6 因必须补两个 Reader Release 并压缩部分路线实现，改动更大，但仍保持同一事件、结果和空间边界。

这证明 **Preservation First 是必要合同，不是可选 prose 偏好**。

## Terra 对比

### Terra high

更敢删、更紧，但出现过两次 authority 越界：

- Ch5 把“施术者未知”的影术痕迹直接断言成观日宗痕迹；
- Ch6 曾把“药车过不去、只有伤员能走”的窄坡改写为药车也可通过。

不适合该 bounded revision 角色。

### Terra medium

比 Terra high 明显更忠实，Ch5/6/9 的 preservation 与压缩能力都不错；但在**最终同一 Revision Contract**下仍出现两个决定性失败：

- Ch6 只补观日宗/传承 Reader Release，仍漏古代石城的珍稀药材/遗物/异兽价值条目；
- Ch10 再次把阮青缨正式招募整个结尾删除，正文停在“统一说明送往沉昼城”，直接丢失冻结 Mission 的结尾推动力。

因此 Terra medium 不作为默认 Second Agent。

## Luna reasoning effort 完整对比

最终同一 Revision Contract 下，用同一冻结 Ch5 / Ch6 / Ch9 / Ch10 Primary Draft 比较 Luna `low / medium / high / xhigh / max`。

| Effort | 平均 wall-clock | 平均 reasoning tokens | 平均原段逐字保留率 | 关键观察 |
|---|---:|---:|---:|---|
| low | 48.1s | 254 | 94.3% | Ch6 漏石城价值 Reader Release；Ch9 漏 Frozen Human cue |
| medium | 54.3s | 563 | **97.0%** | Ch9 / Ch10 最克制；本次公平批次 Ch6 漏第二条 Reader Release；此前独立复验曾补全，存在稳定性边界 |
| high | 93.7s | 2,656 | 93.1% | 四章关键合同全部满足；开始明显改写更多正确段落 |
| xhigh | 186.2s | 4,908 | 91.8% | 无新增关键质量收益；更频繁重措辞，约 high 的 2 倍耗时 |
| max | 379.0s | 6,947 | 90.0% | 四章关键合同可满足，但强章和正确结算也被更多重写；最慢章约 499s，无可见净收益 |

关键合同检查：

- low：Ch5 未知边界、Ch10 Consequence 能守住，但 Ch6 第二条 Reader Release 和 Ch9 Human cue 失败。
- medium：Preservation 最好；Ch9 cue、Ch10 Consequence 正确，但本轮 Ch6 只补“观日宗 / 传承 / 顾斜阳”，漏“珍稀药材 / 遗物 / 异兽”价值条目。
- high：本轮首次同时稳定通过 Ch5 未知边界、Ch6 两条 Reader Release + 空间事实、Ch9 Human cue、Ch10 阮青缨 Consequence。
- xhigh / max：同样通过上述关键检查，但没有比 high 增加新的可见价值，反而 Preservation 更差。

人工阅读也支持这一趋势：high 的 Ch9 会比 medium 多写“呼吸乱了一拍”等更显式的人物反应；xhigh / max 能把 cue 放到更贴近治疗的位置，但同时会改写更多本来正确的措辞。max 在 Ch10 甚至新增“责任自负”式记录措辞，属于更深思考带来的额外加工，不是本任务需要的收益。

### Effort recommendation

- 若**当前合同不再增加任何 deterministic coverage 机制**，质量优先选 **Luna high**：它是本轮第一个 4/4 压力章都完成关键要求的档位。
- 若把 Reader Release 的“逐条缺失项”在调用前确定性标成 explicit missing list，让模型不再自己判断有没有漏，推荐 **Luna medium**：它的 Preservation 明显最好，平均只比 low 慢约 6 秒，却比 high 快约 40 秒/章。
- `xhigh / max` 不推荐用于常驻 Second Agent。

## 结论

### Overall: DIRECTIONAL PASS

Second-Pass Authority Reviser 这个架构方向成立，尤其适合解决：

1. Primary 因近端压缩漏掉远端但高权威的人物/世界/Power realization；
2. Reader Release 已经排程但最终正文没有兑现；
3. Primary 把 Supporting Logic 展开成不必要流程；
4. 正确人物关系被默认成熟化、功能化时，在真正自然触发点恢复一个准确私人 cue。

但它**不是上游剧情修复器**：如果 Director 已把报告、考核、路线任务本身写成 Chapter Mission，Second Agent 不能合法删除整个事件，只能压缩 realization。

## 推荐形态

若后续 production 化，建议链条：

当前实验形态：`Luna Director → Luna Curator → Terra Primary Draft → Luna high Authority Reviser → Luna low State`。若后续把 Reader Release 缺失项在调用前确定性标注出来，则优先回落到 `Luna medium Authority Reviser`。

其中 Reviser：

- raw GBrain OFF；
- 输入 safe Authority Refresh Pack，而不是全量远端文件；
- Preservation First；
- 只输出最终正文；
- 正确段落默认不动；
- 所有新增事实必须来自 Authority / Reader Release / Curator / Canon；
- 不改变 Mission / Result / State Change / Ending。

## 关于“当地房屋 / 当地人的仪态 / 世界小细节”

Second Agent 可以补，但只能补 **上游批准世界已经真实提供** 的细节。它不能因为作者希望“更生动”就现场发明一个地区的屋顶、服饰、礼节或风俗。

如果未来希望稳定拥有这种 texture，应让 World Vision / safe World projection 本身保留少量可复用的 lived-world facts（建筑、衣着、日常姿态、食物、公共空间等），Second Agent 再按当前场景选择性 realization；不要让 Revision Agent 兼任 World Designer。

## What This Did Not Solve

- Ch10 一类上游 Mission 本身程序化的问题；
- Story Program / Outline 的奖励结构、Personal Myth 等长线问题；
- World Vision 本身没有提供的生活材质；
- 不能保证每个合理 Human cue 都由 Second Agent 独立识别，当前更可靠的做法仍是让 Curator 先决定本章 attention，再由 Reviser 用 Frozen Authority 校正遗漏。
