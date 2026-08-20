# Outline Eventization Fix v1 + Paired Blind Validation

## 1. 最终结论

- A：`A_EVENTIZATION_IMPROVED`。
- B：`B_HEALTH_PRESERVED`。
- Compounding：`COMPOUNDING_PRESERVED`。
- Outline 总判定：`OUTLINE_FIX_VALIDATED`。
- `LOCAL_FIX_GLOBAL_DAMAGE`：未发现。
- 正式保留当前 Outline 修改，并记录：`OUTLINE_FROZEN`。
- 最终上游冻结基线：`CREATIVE_CHAIN_FROZEN + OUTLINE_FROZEN`。
- 不进入正文，不修改其它 Prompt 或生产层。

Treatment 的改善不是增加资产名词，而是把已有的法则、仙域、文明记忆、锚群、器物和关系放回人物动作、对手反制、不可逆结果与下一块因果中。B 没有退化为科技树或工程说明书。

## 2. 仓库、生产修改与实验提交

- branch：`principal_dev_new_sys`
- v2 开始 HEAD：`2be35340b36aa05588c85324ffd5e2e1bfa6d951`
- Frozen Creative Prompt baseline：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`
- 生产修改 commit：`2be35340b36aa05588c85324ffd5e2e1bfa6d951`，`fix: strengthen outline eventization`。
- 实验 commit：由本目录提交的 `test: validate outline eventization fix`，最终 hash 在提交后冻结快照与交付消息中记录。
- 生产修改只涉及 `src/story_mvp/prompts.py` 的 `OUTLINE_TEMPLATE`；四个 Frozen Creative Prompt evaluated 内容与基线完全一致。
- 相关测试：`134 passed`（`tests/test_mvp.py` 与 `tests/test_reader_first_runtime.py`）；Outline/Prompt 定向测试 `5 passed`。

## 3. Outline 最小修改

只修改 `OUTLINE_TEMPLATE` 四处：

1. 强化已有 `具体发生：`，要求具体人物动机、主角动作、对手/竞争者/世界行动者的回应或反制、不可逆结果，并明确能力/资产/法则/关系升级必须通过事件发生。
2. 将已有 `二级收益结算：` 改为 `收益与反哺：`，要求写永久净新增及其接下来能让主角完成的具体新动作，并要求资产通过后续行动、人物反应或社会后果进入剧情。
3. 在已有 `## 5. 配角与关系系统` 下补充长期重要人物的关系连续性原则；允许人物退出，但退出必须有具体故事原因。
4. 在已有 10/30/100 说明处补充：每个节点除能力变化外，必须用一个具体、不可逆、可复述事件证明超越发生。

未新增 Agent、字段 Schema、Hard Gate、评分系统、角色模块、关系数值或事件检测器。

## 4. Frozen Creative Chain 与 Control/Treatment

### Creative Chain

v2 的 INPUT、Fantasy Seed、World Vision、Story Program 与上一轮逐字节一致：

- INPUT SHA-256：`c81f58f23d0f5ef457c5ef8294ed6c9a5868e313c7de2ff1635bee2be582ba96`。
- A Seed：`81923fbf33e8eff3c4f8ed9b4a84f1133eb56d4f412160f61a444722f07f49c1`。
- A World Vision：`69994c8727c1be9226eaa9651f2b622d80a32c720428eab2197a4afc4dc59560`。
- A Story Program：`16c10c8d23004213f3d67d6887a84543cd282e8d6fa684a4c13e39f62349cdf8`。
- B Seed：`2287e791e3e5a3545756f1c38fbc875f5de1e7443db989838bfa9e3df960bcf9`。
- B World Vision：`1414f5121143c8267e16fe2d1372f12d7d132947913d28310e07c29ce3704e76`。
- B Story Program：`78f2e3289169adf473aa1f25b6d1eac87cc1a31652844450fedab84e8f8e30ab`。

Creative Chain：零修改。

### Control

- A Control：[control_outline.md](../candidate-a/control_outline.md)，来源上一轮冻结 Outline，SHA-256 `6010208e2bc0310230dafd468d4a82af718b5a86bdf3df651f0cdfc07dbc91d0`。
- B Control：[control_outline.md](../candidate-b/control_outline.md)，来源上一轮冻结 Outline，SHA-256 `746a78a70791f2e66a308310452c3fa7a7d28957bae797f46ee99caef7cd81b8`。

### Treatment

- A Treatment：[treatment_outline.md](../candidate-a/treatment_outline.md)，SHA-256 `7c8b7a5c56f96c9aab4b6dc8b1f8771e2913ed4183722972902822718a84d230`。
- B Treatment：[treatment_outline.md](../candidate-b/treatment_outline.md)，SHA-256 `b8d5daeaec24252893d2f5684b93ea13c10ea71ad4b1afa78a6b8e4d43dc79d7`。
- A Treatment Prompt：[treatment_outline_prompt.md](../candidate-a/treatment_outline_prompt.md)，SHA-256 `c89abf968c0aaec40cbf47301dc2232e92311ee5e4ccf714f0cfa53479021ae0`；完整 rendered prompt 25,460 字符，生成前逐字校验通过。
- B Treatment Prompt：[treatment_outline_prompt.md](../candidate-b/treatment_outline_prompt.md)，SHA-256 `2cc24d3baadf23a95c8605a78c28564b37d19bcfc5d07ff1253064749088072a`；完整 rendered prompt 25,802 字符，生成前逐字校验通过。

模型/Agent 类型：两轮均使用 `luna_worker`；上一轮没有独立记录 temperature/sampling，本轮不猜测。

## 5. Blind Mapping

Blind Reviewer 只看到匿名 X/Y，两个盲审完成后才揭示映射：

- Candidate A：X = Treatment，Y = Control。
- Candidate B：X = Control，Y = Treatment。

盲审报告：

- [Candidate A Blind Pair Review](candidate-a-blind-pair-review.md)
- [Candidate B Blind Pair Review](candidate-b-blind-pair-review.md)
- [Cross-Candidate Attribution](cross-candidate-review.md)

## 6. Candidate A《偷走明天的人》归因

### 33—100 章主要差异

- 第 33—50 章：Control 是“比较生机分支—切法则—恢复区域”；Treatment 增加未来道基承受法则冲撞、真火烧壳、剑意切骨、乌弦守法则、顾观河封门、未来猎人追踪、许沉戈改道，随后法则按入山脉并改变灵脉、昼夜和势力兴衰。
- 第 51—66 章：Control 主要写“提供共同条件、固定仙域出生规则”；Treatment 把冲突落到城门出生资格、斩断单一终局门钥、沈寒枝接人、乌弦处理文明记忆、仙山实体化和第一道脚步。
- 第 67—84 章：Control 主要是留下生机、形成锚群、截取胜果；Treatment 保留这些资产，但明确敌方胜势、许沉戈切锚、门钥之果、文明记忆和人员接入，锚群承担供给与校正。
- 第 85—100 章：两版都有终点根系；Treatment 更清楚写出顾观河、乌弦、许沉戈的阻力、剑意切界、真火炼化、阵眼比较、回昼法则与锚群承接以及根系固定。

Treatment 减少了后段 `ABSTRACT_PROGRESS_BLOCK`，并让回昼法则、仙域锚地、文明记忆、锚群和新明天根系进入人物选择、争夺、接入和不可逆结果。它没有完全修复沈寒枝第 67—100 章的独立行动缺口，但没有恶化。

### A 对手、关系、社会反馈

- 对手：Treatment 更清楚呈现顾观河封门/封城、乌弦守法则/要求归返、许沉戈追火/切锚、未来猎人追踪等反制。
- 沈寒枝：Treatment 前两块与仙域块的合作、接人和共同选择更清楚；无昼、诸界和终点仍缺少足以改变下一块的独立行动。该共同缺口保留为局部 `RELATIONSHIP_FADEOUT`，不是 Treatment 新增损害。
- 社会反馈：Treatment 更具体呈现区域势力改位、出生资格变化、文明记忆和人员接入、终局资格变化。
- 主角选择：Treatment 更明确体现“不救整座灾界、不夺整座仙域、不让单一终局垄断出生资格、不把所有未来一并夺走”。

### A 10 / 30 / 100 与未来十章

- 10：两版均为取剑/真火/道果并斩黑河；Treatment 仍是 `EVENTIZED_MILESTONE`。
- 30：两版均为取阵眼、带回被抹去者、形成未来道基；Treatment 的动作链更连贯。
- 100：两版均为取法则、按入山脉、固定新明天；Treatment 对阻力、工具分工和不可逆区域后果更清楚。
- 未来十章：Control 的“剑意→真火→道果→斩河”顺序略稳定；Treatment 的先取剑意、后握完整未来剑是部分成果到完整兑现，略有回看，但没有低事件密度、延期 payoff 或 `LOCAL_FIX_GLOBAL_DAMAGE`。

A 结论：`A_EVENTIZATION_IMPROVED`。

## 7. Candidate B《掌中天工》保健结果

Treatment 保留并强化了健康结构：

- 沈砺仍然先读残构，再决定拆、留、接，最后亲自定形。
- 宁绾的弟弟线、受伤、卡闸、扩大救援、矿坑救人和后段探路更连续。
- 裴无铸仍主动封路、误判、追踪、带器阵入场、带走残术，并没有退化为“正统炼器观点”。
- 社会反馈增加了追兵误判、坐标争夺、玄衡宗与王朝暂时联合、玄律从关闭接口到有限承认。
- 护腕→逆灵炉/晶核→回澜炉心→解潮炉心→浮垣洞天的复利链保持；新增中间状态没有变成独立科技树。
- 没有出现无必要人物膨胀、机械塞高潮、`ISOLATED_TECH_TREE` 或 `ENGINEERING_BIAS_REGRESSION`。

B 未来十章 Treatment 更稳：断剑、护腕、黑晶、锁阵、铁火巨兽、宁绾救援和弟弟未救出等结果逐章进入下一章；没有 `LOW_EVENT_DENSITY`、`PAYOFF_TOO_DEFERRED` 或 `LOCAL_FIX_GLOBAL_DAMAGE`。

B 结论：`B_HEALTH_PRESERVED`。

## 8. Control vs Treatment 维度比较

### A

- 具体人物行动：Treatment 后段更强；Control 前十章顺序略稳。
- 对手反制：Treatment 后段更强；Control 前十章许沉戈抽火更集中。
- 不可逆结果：Treatment 更清楚，尤其法则入山、门钥斩断、人员/文明接入和根系固定。
- 资产事件化：Treatment 更强，资产不只在结算处出现。
- 关系连续性：前期 Control 略顺，后段两版共同缺沈寒枝独立选择。
- 社会反馈：Treatment 后段更有区域、文明和终局资格后果。
- 10/30/100：Treatment 更易复述。
- 未来十章：Control 略稳，但两版均通过。

### B

- 具体人物行动：Treatment 更强。
- 对手反制：Treatment 更强。
- 不可逆结果：Treatment 更清楚人物层和局部层结果。
- 资产事件化：Treatment 即时使用更显性，Control 跨块链条更紧；两版均通过。
- 关系连续性：Treatment 更强，尤其宁绾/裴无铸/玄律的中间状态。
- 社会反馈：Treatment 更具体。
- 10/30/100：Treatment 更容易复述。
- 未来十章：Treatment 更稳。

## 9. LOCAL_FIX_GLOBAL_DAMAGE

未发现：Treatment 没有破坏未来十章，没有膨胀人物，没有机械制造冲突/高潮，没有让人物戏抢走 Compounding，也没有损害 B 的健康结构。

## 10. 标签归因摘要

- A Control：主要问题是 `ABSTRACT_PROGRESS_BLOCK`（51—84 局部）、`RELATIONSHIP_NOT_EVENTIZED`/`RELATIONSHIP_FADEOUT`（沈寒枝后段），其它核心负向标签未形成全局问题。
- A Treatment：`ABSTRACT_PROGRESS_BLOCK` 明显减少但第 67—84 仍有局部抽象；`RELATIONSHIP_NOT_EVENTIZED`/`RELATIONSHIP_FADEOUT` 仍是共同局部缺口；未发现 `PROTAGONIST_DISSOLVES_IN_MECHANIC`、`MILESTONE_TOO_ABSTRACT`、`LOW_EVENT_DENSITY`、`PAYOFF_TOO_DEFERRED` 或 `ASSET_NARRATIVE_SEPARATION`。
- B Control/Treatment：均未发现 `ABSTRACT_PROGRESS_BLOCK`、`ASSET_NOT_EVENTIZED`、`GENERIC_POWER_GAIN`、`REACTION_ONLY`、`ISOLATED_TECH_TREE`、`ENGINEERING_BIAS_REGRESSION`、`ANTAGONIST_AS_IDEOLOGY_ONLY`、`MILESTONE_TOO_ABSTRACT`、`LOW_EVENT_DENSITY`、`THIN_SCENE_CAST`、`PAYOFF_TOO_DEFERRED`、`FIRST_ARC_STILL_DESIGN_DOC` 或 `ASSET_NARRATIVE_SEPARATION`。
- B 两版共同只有轻度“从逐章细化转为后段阶段块”的时间粒度变化，不构成全局 `TIME_ABSTRACTION_DRIFT`。

## 11. 接受决定

满足接受条件：

- `A_EVENTIZATION_IMPROVED`
- `B_HEALTH_PRESERVED`
- `COMPOUNDING_PRESERVED`
- `OUTLINE_FIX_VALIDATED`

因此正式保留修改后的 `OUTLINE_TEMPLATE`，记录 `OUTLINE_FROZEN`，与 `CREATIVE_CHAIN_FROZEN` 共同构成冻结基线。

不自动进入未来十章、Director、Chapter Prep 或正文；下一阶段由作者另行决定。

## 12. 审查产物

- [Candidate A Blind Pair Review](candidate-a-blind-pair-review.md)
- [Candidate B Blind Pair Review](candidate-b-blind-pair-review.md)
- [Cross-Candidate Review](cross-candidate-review.md)
