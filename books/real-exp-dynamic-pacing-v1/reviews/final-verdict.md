# Long-Form Pacing Window v1 + Dynamic Outline Validation

## 1. 最终判定

- A：`A_PACING_IMPROVED`
- B：`B_HEALTHY_PACE_PRESERVED`
- Compounding：`COMPOUNDING_PRESERVED`
- Narrative：`NARRATIVE_PRESERVED`
- Eventization：`EVENTIZATION_PRESERVED`
- Long-term runway：`LONG_TERM_RUNWAY_PRESERVED`
- 总判定：`PACING_FIX_VALIDATED`
- `LOCAL_FIX_GLOBAL_DAMAGE`：未发现
- 正式记录：`CREATIVE_CHAIN_FROZEN_V2` + `OUTLINE_FROZEN_V2`
- 本轮不进入正文，不修改 Director、Writer、Chapter、Canon、State Delta 或角色系统。

结论不是“把100改成另一个数字”。A Treatment 把原先前100章内的区域法则、仙域、终局和仙道终点重新放回远期路线，在当前层级增加城市、关系、资源、记录、遗迹和社会生态玩法；B Treatment 没有被强行拖慢，而是在约百章完成移动洞天，同时增加有效的公共生活、维护和迁移玩法。

## 2. 仓库与生产修改

- branch：`principal_dev_new_sys`
- 用户指定开始 HEAD：`90b05697e94e2d70e5a57dd5ce7a0ea6434049ab`
- 生产修改 commit：`2c1e3434b6d68043ba0aac556e63d7912ba23368`，`fix: decouple long-form pacing from fixed chapter milestones`
- Dynamic Pacing 实验 commit：由本目录最终提交，commit hash 在 Git 交付记录中。
- Creative Chain baseline：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`
- Outline Eventization Fix：`2be35340b36aa05588c85324ffd5e2e1bfa6d951`
- Paired Outline Validation：`90b05697e94e2d70e5a57dd5ce7a0ea6434049ab`

生产修改只重新打开 Long-Form Pacing 相关语义：

- 新增共享 `LONG_FORM_PACING_DIRECTION`；
- Fantasy Seed：固定 10/30/100 改为早期兑现、稳定循环、中期里程碑、远期升格方向；
- World Vision：同步四层节奏，并兼容旧版 10/30/100 字段；
- Story Program：继续作为 5—7 阶段全书地图，取消阶段平均章节额度，增加横向开发优先原则；
- Outline：`# 未来100章大型剧情块` 改为 `# 当前中期规划窗口`，要求 `规划范围：预计第1—N章` 和 `窗口终点`；
- storage/UI：新标题为 canonical，旧标题可读取；旧 BOOK 不需要迁移即可继续加载。

本轮没有重新优化 Fantasy Seed 多样性、Compounding、Narrative、Eventization、Cost、Payoff、GBrain、Character、Canon、State Delta、Director、Writer 或 prose。

## 3. 新节奏语义

### Fantasy Seed

- `早期兑现（约10章）`：核心优势早期成立并产生正向、可感知结果；约10章是软锚点。
- `稳定循环（约30章）`：核心优势经历多次使用，已有积累开始反哺，玩法从第一次奇观变成可持续循环。
- `中期里程碑`：第一个自然大型阶段充分展开后，主角完成开局不可能完成的事，并由具体不可逆事件证明；不绑定100，不等于长期上限。
- `远期升格方向`：只写长期玩法、生命层次、行动空间和世界关系的上限方向，不绑定章节。

### World Vision / Story Program

两层均使用早期兑现、稳定循环、中期里程碑、远期升格四层。旧版 approved Seed 的 10/30/100 被兼容解释为 10→早期兑现、30→稳定循环、100→旧版中期参考；作者明确锁定的具体章数仍优先。

Story Program 仍是全书 5—7 个自然阶段的地图，但不为阶段分配固定章节额度，也不默认平均分配篇幅。

### Dynamic Outline

Outline 只展开当前中期规划窗口：

- 当前窗口先声明 `规划范围：预计第1—N章`；
- 用 `窗口终点` 解释自然阶段完成、不可逆事件和下一玩法入口；
- 只展开当前自然需要执行的一个阶段或相邻阶段的一部分；
- 仍保留事件化大型剧情块和固定十章近期窗口。

## 4. A《偷走明天的人》

### Control / Treatment

- Control：旧版 N=100，前100章从完整区域法则推进到未来仙域、诸界终局、仙道终点和“新明天”根系。
- Treatment：N=60，窗口终点是照骨城脱离必死命册、本命法宝成形、剑意/真火/阵眼进入构筑并显出昼律入口。

### 主要差异

- Control 在第33—100章连续消耗区域法则、仙域和终局级内容；Treatment 把这些移到后续，未削平远期上限。
- Treatment 在同一城市—区域层横向开发未来剑意、真火、道果、阵眼：战斗、命册、迁城、资源分配、关系、遗迹、器火和机构冲突各自产生不同结果。
- Treatment 让照骨城成为可生活生态：居民、商路、登记、岁库、资源争执、外来宗门、定岁宫和见证网络持续行动。
- Treatment 让旧资产停留更久并换用：剑意从斩河转为切路径，真火从杀器转为炼器/破法，道果从个人机缘转为城市锚点，阵眼转为见证/生产/入口。
- Treatment 的远期昼律、古代遗城、未来仙域、归墟终局和最终选择仍存在；未发现 `CEILING_DAMAGED`。

### A 风险标签

- Control：`PREMATURE_SCALE_ESCALATION_REMAINS`、`CEILING_DAMAGED`。
- Treatment：未发现 `PREMATURE_SCALE_ESCALATION_REMAINS`、`CEILING_DAMAGED`、`FILLER_BLOAT`、`ARBITRARY_WINDOW_BOUNDARY`、`LOCAL_FIX_GLOBAL_DAMAGE`。
- Treatment 仍有局部：A 当前窗口没有展开第61—100章，不对未规划章节作虚构保证；这不是缺陷，而是动态窗口边界。

### A 未来十章

两版都保留固定十章、具体人物、行动、结果和直接因果。Control 第10章更早完成斩河/救城；Treatment 把首十章的战斗收益继续转入城市、关系和制度后果，仍有多个 payoff，没有 filler 或低事件密度。

## 5. B《掌中天工》

### Control / Treatment

- Control：N=100，约第100章完成移动微型洞天，下一入口是天外裂口与界锚。
- Treatment：N=96，第96章带着居民、药田、炉室和维修循环穿过断潮带，在九垣界脊稳定停驻；第97章以后自然进入九垣改脉。

### 健康速度保护

- 移动洞天仍然保持百章左右的自然尺度，没有被动态语义拖到200章。
- Treatment 增加了有效横向玩法：雨埋城水权/聚灵、逆潮离城、残骸登记、敌我识别、行炉补给/疗伤/居住、洞天维护/分配、断潮迁移。
- 这些不是无结果重复炼器；每个新层都改变人物、资源、社会反馈或下一行动。
- 沈砺行为指纹、宁绾关系、裴无铸竞争、玄律边界、法宝/工坊复利均保留。
- 未发现 `FILLER_BLOAT`、`CEILING_DAMAGED`、`ARBITRARY_WINDOW_BOUNDARY` 或 `LOCAL_FIX_GLOBAL_DAMAGE`。

### B 未来十章

Treatment 在第8章高光后用第9—10章继续处理食物、水、晶核、路线、追踪和雨埋城入口；Control 的十章更紧凑，但 Treatment 没有破坏事件密度或 payoff。

## 6. Blind Mapping

盲审完成后才揭示：

- Candidate A：X = Treatment，Y = Control。
- Candidate B：X = Control，Y = Treatment。

Blind reports：

- [Candidate A Pacing Review](candidate-a-pacing-review.md)
- [Candidate B Pacing Review](candidate-b-pacing-review.md)
- [Cross-Candidate Attribution](cross-candidate-review.md)

## 7. 全局判定与重新冻结

- A：`A_PACING_IMPROVED`
- B：`B_HEALTHY_PACE_PRESERVED`
- `COMPOUNDING_PRESERVED`
- `NARRATIVE_PRESERVED`
- `EVENTIZATION_PRESERVED`
- `LONG_TERM_RUNWAY_PRESERVED`
- `PACING_FIX_VALIDATED`
- 已记录 `CREATIVE_CHAIN_FROZEN_V2`
- 已记录 `OUTLINE_FROZEN_V2`

后续没有真实跨作品失败，不再因为单作品的 N 应为60、96、100或其它数字而修改全局 Prompt。本轮完成后停止，不进入正文。
