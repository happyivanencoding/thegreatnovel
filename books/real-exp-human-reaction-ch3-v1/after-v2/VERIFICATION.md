# Frozen Chapter 3 After-v2 Verification

## 输入与边界

使用 `books/real-exp-opening-reader-first-fresh-v1/runs/chapter-0002/BOOK_after_state_delta.md` 作为 Chapter 3 起点；保留原 Chapter 1/2、`FIXED_CORE.md`、`CHAPTER_PLANS.md` 和 `READER_IMMEDIATE_UNDERSTANDING.md`。旧 `OLD_CHAPTER_3.md`、旧 `NEW_CHAPTER_3.md` 和旧 `runs/chapter-0003/` 没有覆盖。

固定事实是：台心合格牌；对手阻拦下取牌并带回自己的白线；周既明最终越过判定线；顾长川取得本轮公开升院合格但尚未正式入内门；真实进攻后只使用一次回身卸力步且使用后消失；许照确认守约；周既明成为公开竞争者。

## 节点证据

- Director：`director_prompt.md` / `director_response.md`，八字段齐全，无第九字段、身份漂移或结果漂移。
- Curator：`curator_prompt.md` / `curator_response.md`，固定 Curated sections 齐全；成长短投影未在 `Relevant Plan` 原样回显；未把 Director 策划总结改写成正文。
- Primary：`primary_prompt.md` / `primary_response.md` / `final_formal_prose.md`，三标题正确；正文保留全部冻结结果。
- State Delta：`state_delta_prompt.md` / `state_delta_response.md` / `BOOK_after_state_delta.md`，解析和应用成功；状态明确保留“本轮公开合格但尚未正式入内门”。
- Specialist、Integrator、Reviewer、自动重写和生产 BOOK 写入：均未运行。

## Before / After 代表片段

### 1. 开场与读者锚点

Before 旧稿先用演武场、规则和候考队列铺开，随后才落到顾长川的伤势与目标。

After 直接把顾长川放进点名动作：“宁秋禾揭开封存的考核名册，念到‘顾长川’时，他从队列里走了出来。”随后立即给出台心合格牌、两条白线和当前伤势。读者更早知道谁在场、要拿什么、身体有什么限制。

### 2. 规则先发生再解释

Before 虽然保留取牌回线，但规则说明较长，并在后文多次解释“不是击倒”。

After 用一次现场对白说明“取牌、带回自己的白线、越线判负”，随后马上进入周既明站在牌前的阻拦位置；规则服务于当前行动，没有先讲完整世界机制。

### 3. Human Reaction 进入因果

Before 主要由顾长川正确分析周既明的假动作和真实进攻，人物反应较多承担说明功能。

After 顾长川先不追假动作，明确等待真实进攻；用完唯一一次步法后，他再用普通脚步回线，而不是自动追加能力。周既明越线后说“你一直等到我真的压上来”，许照通过确认“守约”结束交易，宁秋禾用名册登记并要求“先归队”。这些反应改变了后续位置、关系和行动，而不是只增加情绪词。

### 4. Planning Language Leakage

Before 旧新版实验曾出现“已经经过了公开场面的验证”“第一道门打开”等作者总结式句子，且还把本轮合格写成取得内门弟子身份。

After 主要把意义交给具体结果：合格牌被取回、周既明越线、名册记下本轮公开合格、顾长川仍穿外门衣袍、内门报到尚未开始。正文未把“闭环、阶段推进、价值兑现、成长空间、建立优势”等后台标签扩写成作者旁白，也没有添加永久能力。

## 过度纠正检查

After 仍保留连续动作段、必要规则说明、伤势限制和简短对话；没有把每个事件拆成固定“观察—反应—行动”模板，没有连续堆叠“他顿了顿”，没有删除取牌规则，也没有把全文改成碎句或纯口语。速度仍由一次取牌竞争推动。

## 运行控制说明

本目录保存四个有效节点的 Prompt/Response 与 State Delta 应用结果。由于一次 Primary worker 只生成了 Prompt 未产出 response，后续单独 worker 生成并保存了唯一有效 Primary response；因此本产物可用于冻结事实和表达方向的最小验证，但不宣称是严格无中断的四调用 benchmark。生产环境没有增加节点、LLM call、Hard Gate、validator、blacklist 或自动 rewrite。
