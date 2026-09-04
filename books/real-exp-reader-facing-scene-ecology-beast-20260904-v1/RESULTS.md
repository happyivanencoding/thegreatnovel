# Reader-Facing Scene Ecology — Beast Canyon Experiment

日期：2026-09-04

## Verdict

**PASS，冻结方法；不宣称本组六章已经等同顶级男频成品。**

本轮冻结的不是新的 Story Program，也不是新 Agent，而是 `Story Program → Outline/Future-10 → Batch Primary` 之间避免高价值 reader-facing 信息逐层压扁的最小 transport / realization 方法：

- Stable Scene Geography；
- Living Power Ecology；
- Important Actor / Active Interior Carry-Forward；
- Situation Re-anchor（`Action Advance ≠ Situation Memory`）；
- Earned Convergence（`Convergence is payoff, not simultaneous loading`）；
- 少量 Story-approved `Reader-Facing Actor Ruler Anchors` 结构化运输面。

已冻结的 `Power Growth Causality / Living Power Progression` 不改，本轮只处理第5—10章鸣骨峡暴露出的下一层问题。

## Controlled Experiment

Baseline：`books/real-exp-living-power-progression-beast-20260903-v2`

Treatment：`books/real-exp-reader-facing-scene-ecology-beast-20260904-v1`

冻结：

- Author Direction；
- World Vision；
- Power Seed；
- Human Seed；
- Character；
- Story Program 的创作事实与因果；
- GBrain 输入；
- 最终第1—4章正文。

Fresh：

- Outline（Luna high）；
- 第5—10章一个6章 Terra-high Batch Primary；
- 一个6章 Sol-high Batch Authority Delta；
- 第5—10章 Luna-low State。

没有手工 prose treatment，没有新 Agent / Reviewer / Scene Map 数据库 / 每章空间 Gate。

Production run：8 次模型调用；模型 wall 1063.826s；Sol Delta 7 个 exact local patches；`upstream_conflicts = 0`。

Steward 0.3.50 同步完成：`skill-authoring lint` 为 `portable=true / 0 errors / 0 warnings`；package validate + install/activate PASS；bounded read-only smoke 行为 PASS——它正确对旧 Baseline 判 FAIL，并把最早根因定位在 `Story Program → Outline/Future-10` representation transport，明确反对新增 Scene Graph、Reader State DB、Power Ecology Agent 或让 Primary 直接读取完整 Story Program。

## Root Cause Confirmed

### 1. Living Power Ecology 首先在 Story Program → Outline 丢失

冻结 Story Program 原本已经明确：

- 唐鹭会在鸣骨峡以 `共鸣级44` 展示“共载”；
- 韩狩会在前期鸣骨峡以 `共鸣级68` 维持返程线，展示“择风”。

Baseline Outline / Future-10 没有把这两个“具名人物 + 精确位置 + 当前现场展示”绑定送进第5—10章，因此 Baseline 正文第5—10章的共鸣尺只剩 `贺临川1 / 段阙26`。这不是 Primary 单独遗忘，而是上游 representation compression loss。

### 2. Important Character interior 也在 Story → Outline → Future-10 逐层压缩

Story Program 的唐鹭拥有苏渠、沉瓦、贺青禾、照雪自主选择等具体私人因果；Baseline Outline/Future-10 逐渐压成“拿航契和船位换照雪”，最终 Primary 很容易只写成功能性交易 NPC。

### 3. Spatial confusion 主要来自没有 Stable Scene Geography

Baseline Future-10 只给“交易台 / 旧风门 / 兽巢路线 / 副链”等局部对象，没有先确定稳定彼此关系。Primary 为每个动作继续生成窄道、石台、斜坡、交易台底部、岩台等局部空间，单句可成立但跨章 working map 漂移。

## Prompt-only Failures Before the Final Treatment

本轮先做了两次只生成 Outline 的停线实验，证明“多提醒一句”不足：

1. 第一版泛化 `Important Actor Carry-Forward / Living Power Ecology` 后，Stable Geography 已明显改善，但 Luna 仍把唐鹭44 / 韩狩68的当前绑定压掉；实验停止，没有生成正文。
2. 第二版进一步强调 actor-ruler carry-forward 后，Outline 保留了44/68，但把唐鹭44搬到后面的白脊阶段、韩狩68搬到后面的雷穹阶段；事实没丢，Story 已批准的演示时机却被重新调度，仍停止。

因此最终没有继续堆自由文本提醒，而是新增一个非常窄的结构化 transport surface：

`### Reader-Facing Actor Ruler Anchors`

只保存 Story Program **已经明确决定**的 0—6 条具名人物力量演示，格式：

`人物 + 精确位置 + 展示 + 时机/地点 + 现场意义`

Outline 在 `Reader-Facing Actor Ruler Anchor Schedule` 原样复制，不能换演员、数字、能力或把演示搬到更晚阶段。它不是第四 Authority，不给人物自动发等级，也不新增创作决策；只是防止自由文本编译把已经决定的 Story causality 丢绑定。

旧 V2 Story Program 生成于该 transport section 上线以前，所以本实验只把其原文里已明确存在的两条事实整理成同义 appendix；没有新增唐鹭/韩狩的等级、能力、地点或事件。

第三次 Outline 通过真正的当前 Future-10 stop-line：

- 第5章先进入鸣骨峡并建立唐鹭；
- 第6章建立叶朔 / 旧风门；
- 第7章韩狩 `共鸣级68 / 择风 / 返程线`；
- 第8章唐鹭 `共鸣级44 / 共载` + 航契/船位/照雪选择；
- 第9章主角真正放弃船位跟照雪；
- 第10章断副链 + 乌金回脊索。

这把旧版“唐鹭/叶朔/韩狩/段阙同时加载后立刻大汇流”改成了 reader-earned convergence。

## Final Prose Evidence

### A. Stable Scene Geography：PASS

第5章先把舞台立成可重复使用的关系：

- 外围旧停驻点 / 半圈石台；
- 峡谷中段的临时交易台；
- 交易台下三条粗副链；
- 更深处的旧风门 / 迁徙风道；
- 下方危险风隙。

第6章再次明确“三条副链横在风门外风道上”；后续段阙、唐鹭、韩狩、照雪都围绕同一交易台 / 风门 / 副链 / 返程线移动。正文仍会出现骨台、骨梁、骨脊、斜坡等局部动作点，但它们现在附着于稳定舞台，不再每段重新发明主地图。

### B. Situation / Causal Re-anchor：PASS

第6章直接让 POV 重报：

> “段阙要的是把照雪赶回交易台。唐鹭盯的是契纸和沉瓦的线索。叶朔只在乎兽群能不能过门。”

随后明确：

> “没人会替他把照雪带出来。”

第9章再次给行动地图：上方唐鹭返程线正在变窄，主角往右仍可能赶上；照雪被副链隔在左边。读者不用自己从前几页动作重建“现在到底是什么局面”。

### C. Living Power Ecology：PASS

Baseline 第5—10章没有唐鹭44 / 韩狩68。

Treatment Final：

- 韩狩入场直接写 `共鸣级六十八 / 越风`，并现场维持“择风”返程线；一个商盟伙计只靠近风线边缘就被侧风撞回交易台，主角明确知道自己1级连靠近都要找角度。
- 韩狩的高阶力量同时约束事件：段阙必须回应他的撤链命令；但韩狩明确“我查镇脉钉旧案”，他的力量用于军府查案和维持返程线，不替主角争照雪。强者不介入不再像作者忘记了他。
- 唐鹭在交易台坍塌时以 `共鸣级四十四` 现场展示“共载”，人、兽、货箱一起换落点；主角立刻拿自己的1级体验作比较。

共鸣级因此从“主角与段阙专用战斗数字”开始恢复成解释社会位置、行动资格和现场行为的共同语言。

### D. Active Interior Continuity / Dialogue Breathing：PASS

Treatment 唐鹭不再只有“给我照雪，我给你船”的功能句。她明确说完整航契来自苏渠、自己同时在找沉瓦和照雪；面对“你能保证照雪还能自己选路吗”，她先沉默，再承认只能保证不把照雪关进商盟笼子，不能替照雪保证选择。

这没有把 Story Program 的完整 Biography 倾倒给读者，却让“亡侣留下的活物 / 自己不愿承认照雪可能不选她”真实改变对白、停顿与交易方式。韩狩的对白仍短，因为他的现场身份/性格允许简短命令；因此改动不是统一把所有对白拉长，而是恢复人物间呼吸差异。

### E. Earned Convergence：PASS

旧版第5—6章几乎同时初始化唐鹭、叶朔、韩狩、商盟、交易、迁巢、军府旧钉、段阙与复杂空间。

Treatment 让主要 reader model 分步成立：唐鹭 → 叶朔/旧风门 → 韩狩/68级 → 唐鹭/44级与私人交易 → 主角选择 → 奖励结算。事件本身仍属于同一个鸣骨峡多方碰撞，没有把它拆成多个无关小任务。

## Sol Delta

Sol-high Batch Authority Delta 只做 7 个局部修复，主要是：

- 补回迁徙巢崖真实上移；
- 删除未授权的“明早”精确时间；
- 恢复贺临川亲手断副链的批准事件，并同步第10章链条状态；
- 删除同一连续威胁里的第二次“先见一瞬”；
- 恢复放弃船位的真实代价，不让交易失败后座位继续白送；
- 恢复韩狩真实取回镇脉钉并发现裂痕与公开记录不符。

关键的 Reader-Facing Scene Ecology 增益均被保留，没有被 Authority Delta 当作“多余解释”删除。

## Residual / What This Did Not Solve

- 鸣骨峡 Final 仍有少量骨台 / 骨梁 / 骨脊等微地形，这是动作需要，不再全部视为问题；若用户实读仍在某一段迷路，应修那段具体空间关系，不继续加全局空间框架。
- 叶朔仍比唐鹭薄，但他当前的迁巢欲望、旧风门职责和“不替主角停门”的行为因果已经清楚。本轮不为了人物厚度均匀给所有配角增加内心独白或 Biography。
- Actor Ruler Anchors 只保护 Story Program 已经明确决定的少量高价值具名演示；它不是“所有 NPC 都要等级”的清单，也不是第二个 Public Milestone Ladder。
- 本轮直接验证的是一个真实多方高负荷场景。方法应冻结为 current production default，但后续新世界若出现另一种复杂场景，仍按实际 reader failure 判断，不扩成通用 Scene Graph / Reader State DB。

## Freeze

冻结：

1. `Stable Scene Geography`；
2. `Action Advance ≠ Situation Memory`；
3. `Living Power Ecology`；
4. `Important Actor Carry-Forward / Active Interior Continuity`；
5. `Convergence is payoff, not simultaneous loading`；
6. Story Program `Reader-Facing Actor Ruler Anchors` → Outline 原样 Schedule → Future-10 当窗口兑现；
7. 对话长短按人物/压力变化，不再统一压成一句功能对白；
8. 有限 POV 在复杂多方场景承担最低充分的观察 / 判断 / 决定，帮助读者理解当前行动因果。
