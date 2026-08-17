# Browser Workflow Audit · original-d336a8f607cd

## 页面/事件 1 · 创建 Original

- 时间：2026-08-17 Europe/Paris（具体秒级时间由运行环境日志保留）
- 页面：书库；URL：`http://127.0.0.1:8877/`
- 作用域：book_id=UNKNOWN；edition_id=UNKNOWN；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：内部浏览器打开 `/library`，确认临时书库无既有项目；进入“新建原创小说”。
- 输入：运行库 `C:\Users\jingx\AppData\Local\Temp\thegreatnovel-original-e2e-20260817-a\library`；全新 Original 表单。
- 页面可见结果：书库显示“放入你的第一本小说”；没有复用旧实验项目。
- 机器输出：服务器 `/health` 返回 200，commit=`73a8fc1e42fb6f4b67e9a3f6542d39674e1447a2`。
- 一致性判断：通过；实验运行库与仓库既有 library 隔离。
- 调试/下一动作：填写作者 premise，提交创建。

## 页面/事件 2 · 提交 Original 作者输入

- 页面：新建原创小说；URL：`http://127.0.0.1:8877/library/original/new`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：填写并提交 Original 表单。
- 输入：一句话创意为“失去武者身份的边城少年，被迫在公开擂台上用一套被禁用的观星步法挑战垄断城池的冠军；每次胜利都会暴露他真正的出身，并把他推向下一层更强的对手。”；类型为“东方战力成长与身份竞争”；基调为“紧张、直接、人物行动先于解释，保留热血竞争感”；视角为“第三人称限知”；篇幅为“长篇连载，不锁定章数”；必须包含三项：主角必须通过公开竞争争回身份、每次胜利都要改变对手或社会目光、战力成长必须带来新的行动选择；禁止三项：复制旧实验建筑/生存资源/每日物品机制、正文旁白解释系统规则、预先固定十章剧情；抽象参考特征三项：竞争结果产生社会反馈、成长通过事件结果体现、章末保留具体新对手或新门槛。
- 页面可见结果：`原创项目 · 0 个正式章节`；`AI 正在理解阅读体验与叙事驱动力`；`Step 0 · Semantic First Read`；明确不会生成核心玩法、Foundation 或首章。
- 机器输出：URL 中确认全新 book_id=`original-d336a8f607cd`。
- 一致性判断：通过；主要 Reader Experience family 是战力/成长/身份/竞争，与旧 survival-resource 实验不同。
- 调试/下一动作：读取/执行 Semantic First Read handoff，等待页面回读。

## 页面/事件 3 · Reader Kernel Proposal 回读

- 页面：原创项目 Reader Kernel；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/original`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=handoff_86b47c6695787a804f7564da
- 动作：浏览器回读完成的 Proposal，未调整 AI 推荐值。
- 页面可见结果：状态为“等待确认阅读体验”；主驱动“排名与赛事晋级”；辅助驱动“力量与阶段成长 / 身份保存压力 / 身份与认可提升”；Progression Engine 为启用；页面显示完整创作语义、证据、不确定性和作者留意项；正式章节数仍为 0。
- 机器输出：workflow start=`RUNNING`；executor=`interpret-original-reader-kernel`；workflow complete=`COMPLETED`；artifact=`operations/handoff_86b47c6695787a804f7564da/artifacts/reader_kernel/proposal.json`；`canon_committed=false`。
- 一致性判断：通过；Proposal 与作者 premise 的战力/身份/竞争方向一致，尚未越级生成玩法或章节。
- 调试/下一动作：作者在浏览器点击“确认当前 Proposal 并继续”。

## 页面/事件 4 · Core Innovation Proposal 回读

- 页面：原创项目 Core Innovation；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/original`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=handoff_b59d9209dfc88bb201918e13
- 动作：Reader Kernel 确认后浏览器进入 Core 生成阶段；执行页面创建的 handoff 并回读结果。
- 页面可见结果：Reader Experience 已确认；页面显示正在生成三个核心玩法方案，仍为 0 个正式章节。
- 机器输出：workflow start=`RUNNING`；executor=`bootstrap-original-novel`；workflow complete=`COMPLETED`；Core artifact 含三个候选 `core-competition-reading`、`core-qualification-escalation`、`core-asymmetric-opponent`；Reference=`ZERO_RESULTS`；`canon_committed=false`。
- 一致性判断：通过；三个候选共享被禁用观星步法的竞争核心，只在能力展开、资格后果和对手压力的开放问题上差异化。
- 调试/下一动作：浏览器回读三个候选，默认采用系统推荐候选，不按文学偏好重新挑选。

## 页面/事件 5 · Story Foundation Proposal 回读

- 页面：原创项目 Story Foundation；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/original`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=handoff_7b84acd7881ee6d4f1a79bcb
- 动作：Core 确认后浏览器进入 Foundation 生成阶段；执行页面 handoff 并回读三个故事承载方案。
- 页面可见结果：状态为“等待选择故事基础”；三个方案共享 `让每次胜负重新解释观星步法`，分别呈现城市名籍擂台、跨城巡擂、禁步审判台；正式章节数仍为 0。
- 机器输出：workflow start=`RUNNING`；executor=`bootstrap-original-novel`；workflow complete=`COMPLETED`；Foundation IDs=`foundation-qualification-city`、`foundation-crosscity-circuit`、`foundation-banned-step-trial`；`canon_committed=false`。
- 一致性判断：通过；候选差异来自社会承载、舞台扩张和身份后果，不是新增第二核心机制。
- 调试/下一动作：浏览器默认采用第一个 Foundation 候选，生成 Development Proposal。

## 页面/事件 6 · Foundation Development 回读

- 页面：原创项目 Development；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/original`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=handoff_4b9e2af551ae2065e2ee6a5f
- 动作：选择默认 Foundation 后执行 Development handoff 并回读 Proposal。
- 页面可见结果：页面显示“正在针对已选故事基础生成成长长线与第一阶段”，正式章节数仍为 0。
- 机器输出：workflow start=`RUNNING`；executor=`bootstrap-original-novel`；workflow complete=`COMPLETED`；selected Foundation=`foundation-qualification-city`；推荐路线=`route-public-proof`；首章候选数=3；`canon_committed=false`。
- 一致性判断：通过；Development 继承 selected Core、Foundation 和 Reader Kernel，未写正文或 Canon。
- 调试/下一动作：浏览器回读 Development 完成状态，确认 Genesis，然后进入首章候选。

## 页面/事件 7 · Genesis 最终确认与首章候选

- 页面：原创项目 Genesis；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/original`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=UNKNOWN
- 动作：浏览器回读 Development/第一阶段/三条路线/三项首章候选，点击“确认故事基础并进入第一章候选”完成 Genesis 确认。
- 页面可见结果：标题默认“名籍之外的擂台”；状态“故事基础已确认”；正式章节数=0；展示三项首章候选，未生成正文。
- 机器输出：`canon_committed=false`；Genesis 确认后进入作者首章候选页面。
- 一致性判断：通过；确认动作只写幕后设定与路线，不创建正文或 Canon。
- 调试/下一动作：按实验规则采用第一项系统默认首章候选“名籍之外的第一场挑战”。

## 页面/事件 8 · 首章候选选择与 Draft handoff

- 页面：原创项目首章准备；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/original`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=UNKNOWN；draft_id=UNKNOWN；handoff_id=handoff_f53bd6dd77d55c4ae98315cb
- 动作：浏览器选择系统默认首章候选“名籍之外的第一场挑战”。
- 页面可见结果：页面显示“首章要求已冻结，等待生成与校验”；明确停在已校验，不自动写入正式正文；正式章节数=0。
- 机器输出：浏览器创建 `CONTINUATION / DRAFT_AND_VALIDATE` handoff=`handoff_f53bd6dd77d55c4ae98315cb`；首章候选 ID=`first-qualification-challenge`。
- 一致性判断：通过；作者可见选择通过页面完成，尚未生成、校验或批准正文。
- 调试/下一动作：执行同一页面提供的 handoff，必须写 creative output 与独立 publication review，再回到页面。

## 页面/事件 9 · Chapter 1 Validation 与浏览器批准

- 页面：Draft Review；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/editions/base/draft-review`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=canon-chapter_172c2f1dffc21ee79ed10c71；draft_id=draft_a74dcaafaf1a1fa99ad56f71；handoff_id=handoff_f53bd6dd77d55c4ae98315cb
- 动作：页面显示 `VALIDATED_DRAFT`、10 项 validator PASS、Hard errors=0；通过页面按钮点击一次“批准写入正史”。
- 页面可见结果：点击后 inline 状态变为“已写入正史”，没有 JS dialog、window.confirm 或 blocking modal。
- 机器输出：Canon commit=`canon-commit_9ccb975a8a997ba4d3fc56c4`；chapter=`canon-chapter_172c2f1dffc21ee79ed10c71`；event range=1–5；Canon content hash=`806b68f6bbde5e3c202f12adcd9109998f5c3170050e433e9bf35ffe7160aaa6`；snapshot=`snapshot_11796c4c2cb52b5ffd3f48c0`；projection hash=`f13b948fdeaab4923a11590e1747d3cf9c5e026589c55496e652c558080795f2`。
- 一致性判断：通过；刷新 Original 页面显示 `1 个正式章节`、首章标题和“继续写第二章”，Canon 与 Projection 已建立；旧失败 DRAFT 仍保留为审计记录。
- 调试/下一动作：继续通过浏览器点击“继续写第二章”，逐章重复 Candidate→Contract→Draft→独立 review→Validation→Approve。

## 页面/事件 10 · 第二章 handoff 创建（修复后）

- 页面：小说工作台续写第 2 章；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/editions/base/workbench?action=continue&chapter_id=canon-chapter_172c2f1dffc21ee79ed10c71`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=canon-chapter_172c2f1dffc21ee79ed10c71；draft_id=UNKNOWN；handoff_id=handoff_02d0c91f21869a54e69e6589
- 动作：服务器重启到 `b1c6f27` 后，浏览器再次点击“开始续写”。
- 页面可见结果：不再显示“尚未建立结构索引”；任务中心显示“第2章续写 · 等待 AI 处理 · 20%”。
- 机器输出：新 `CONTINUATION / DRAFT_AND_VALIDATE` handoff=`handoff_02d0c91f21869a54e69e6589`；旧失败点击没有生成可执行 handoff，未写 Canon。
- 一致性判断：通过；Original 无来源书使用空历史 context 直接进入现有 Boundary/Contract handoff，未伪造结构索引。
- 调试/下一动作：执行该 handoff，继续默认候选与独立 semantic review。

## 页面/事件 11 · Chapter 2 候选、Validation 与浏览器批准

- 页面：Draft Review / Workbench；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/editions/base/draft-review`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=canon-chapter_2d8343a86398504c96f256e5；draft_id=draft_278411fc6304b09107d4a9d3；handoff_id=handoff_cc63d405ca8cc7ae7b9dfb96
- 动作：浏览器 PLAN_ONLY 候选页默认选择 rank 1 “记录上的下一道门”；页面进入 Draft Review；点击第一项“批准写入正史”。
- 页面可见结果：Draft Review inline 显示“已写入正史”；无 JS dialog、window.confirm 或 blocking modal；Workbench 刷新显示 `正文 2` 与“记录上的下一道门 正史”。
- 机器输出：第2章 Canon commit=`canon-commit_af65d712e850921c56e6e480`；event range=6–11；chapter=`canon-chapter_2d8343a86398504c96f256e5`；最新 snapshot=`snapshot_1e905cdc56d7fbb36edd91cd`；projection state hash=`c2e07f8319774d6580dd2a30a3b21c36c0e5b7b56b78c6f12298be4c285f5bb5`；10 validator PASS；semantic review=`REVIEWED`；publication findings=[]。
- 一致性判断：通过；第 2 章使用不同白线/铜镜复核压力，未复制第 1 章同一解决动作；Canon 计数从 1 增至 2。
- 调试/下一动作：继续从 Workbench 通过浏览器开始第 3 章。

## 页面/事件 12 · Chapter 3 候选、独立 review、Validation 与浏览器批准

- 页面：Workbench → Draft Review；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/editions/base/draft-review`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=canon-chapter_5a4799f5a65c70ec80d8edf0；draft_id=draft_8eef86a3b857ee8ae165cba7；handoff_id=handoff_8db371c6d2a99d83e4762ca8
- 动作：浏览器生成第 3 章 PLAN_ONLY handoff，默认选择“被看见之后的邀请”；随后浏览器创建 DRAFT_AND_VALIDATE handoff。正文先写入 creative output，再独立重读生成 publication_review.json；浏览器 Draft Review 显示 `VALIDATED_DRAFT` 后点击批准。
- 页面可见结果：10 项 validator 全部 PASS、Hard errors=0；Workbench 刷新显示 `正文 3` 与“被看见之后的邀请 正史”；没有 JS dialog、window.confirm 或 blocking modal。
- 机器输出：PLAN handoff=`handoff_edee4dd15ab8dc110db4e4c3`；DRAFT handoff=`handoff_8db371c6d2a99d83e4762ca8`；contract=`contract_9e15bec120590b9b4915692f`；selected candidate=`candidate_d6b7a8911780750ef7890809`；draft=`draft_8eef86a3b857ee8ae165cba7`；validation=`validation_a5bd686436ba8dcf1cf4d2c1`；semantic review=`REVIEWED`；publication findings=[]。
- Canon 证据：commit=`canon-commit_f31950f27f0db74be2e10c29`；chapter=`canon-chapter_5a4799f5a65c70ec80d8edf0`；event range=12–17；Canon content hash=`d1bb9f3421bb95c07aac2ea8531c0e307507697b35f947f4f30f33f1a4c14c6d`；snapshot=`snapshot_9648150ee621b0224611411d`；projection state hash=`91711a5157a64abf2cf71d88deee3152bd904c68b1f53c6fac249da15b914aa9`。
- 一致性判断：通过；第 3 章把竞争从城内复核推进到城外、规则不同且可拒绝的公开挑战，正文不是第二章白线复核的同构重写。一次真实验证发现 `world/social state changes` 合同标签映射缺口，已补最小编译映射并用回归测试和新 draft 复验。
- 调试/下一动作：从第 3 章正史锚点继续逐章执行第 4–10 章，并保留失败 draft 作为审计输入，不把失败记录伪装成 Canon。

## 页面/事件 13 · Chapter 4 候选、独立 review、Validation 与浏览器批准

- 页面：Workbench → Draft Review；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/editions/base/draft-review`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=canon-chapter_08286d9715515203c3a5245c；draft_id=draft_f8d9fa01ca9d9dcb0412bdb7；handoff_id=handoff_7a753752d49ab7205182f92c
- 动作：浏览器生成第 4 章 PLAN_ONLY handoff，默认选择“渡口规则的第一道门”；正文在白河渡外场完成一次规则验证，并由独立 review 重新提取结果与下一条窄规则；页面显示 10/10 PASS 后批准。
- 页面可见结果：Draft Review inline 显示“已写入正史”；Workbench 刷新显示 `正文 4` 与“渡口规则的第一道门 正史”；无 JS dialog、window.confirm 或 blocking modal。
- 机器输出：PLAN handoff=`handoff_ec5b7792096e6f0b6ffe2ea3`；DRAFT handoff=`handoff_7a753752d49ab7205182f92c`；contract=`contract_08a1c857406c47c184b95e33`；selected candidate=`candidate_43179a6cbbbbf3dd570ba010`；draft=`draft_f8d9fa01ca9d9dcb0412bdb7`；validation=`validation_01ff15535c99cba946d8adc9`；semantic review=`REVIEWED`；publication findings=[]。
- Canon 证据：commit=`canon-commit_efa72a3c7830d57190394781`；chapter=`canon-chapter_08286d9715515203c3a5245c`；event range=18–23；Canon content hash=`b38bfd477756fc82cfb58b666a02b1532a2cf4139530182a421f55a06dd7392d`；snapshot=`snapshot_e4d54a3fb07900edd2b4ca01`；projection state hash=`a6069f0ae88af4631063a4ee6eaa8119544149c2d5e9a1e3d2a41dd75af4c5ce`。
- 一致性判断：通过；第 4 章把第 3 章的邀请兑现为有三名见证者的外场验证，新增“更窄的判定条件”，没有回到城内擂台模板。
- 调试/下一动作：继续从第 4 章正史锚点创建第 5 章规划 handoff。

## 页面/事件 14 · Chapter 5 候选、独立 review、Validation 与浏览器批准

- 页面：Workbench → Draft Review；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/editions/base/draft-review`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=canon-chapter_92688f62db7a5fc7f4409175；draft_id=draft_8db2135be157eed857948ad3；handoff_id=handoff_21a74e4d2d5e043bff425b47
- 动作：浏览器生成并确认第 5 章候选“黑石前的第二次判定”；独立 review 重新阅读正文，只提取连续记录与下一条更窄边界；Draft Review 显示 10/10 PASS 后批准。
- 页面可见结果：页面 inline 显示“已写入正史”；Workbench 刷新显示 `正文 5` 与“黑石前的第二次判定 正史”；无 JS dialog、window.confirm 或 blocking modal。
- 机器输出：PLAN handoff=`handoff_665c68633dc35389ff1ca703`；DRAFT handoff=`handoff_21a74e4d2d5e043bff425b47`；contract=`contract_80c06c932ed9a4e856259054`；selected candidate=`candidate_7f41a8b10eeead0d41776d3d`；draft=`draft_8db2135be157eed857948ad3`；validation=`validation_fbf6d2cd3e6213bae1ba7faa`；semantic review=`REVIEWED`；publication findings=[]。
- Canon 证据：commit=`canon-commit_a339bc7c6fb17abf09028eec`；chapter=`canon-chapter_92688f62db7a5fc7f4409175`；event range=24–29；Canon content hash=`d54119b8c57b3e8b530d7dfd2e519fb9d68957fdbd7d3551060552d7244344c3`；snapshot=`snapshot_1e33adeec813849a5b1b4b1c`；projection state hash=`64d2f52d3a783c3d239d9520c99540b5b3a5aaa2f4b74ef671d00980154985ff`。
- 一致性判断：通过；第 5 章将外场验证继续压缩成更窄的公开判定，正文没有回退到城内名籍复核。
- 调试/下一动作：继续从第 5 章正史锚点创建第 6 章规划 handoff。

## 页面/事件 15 · Chapter 5 候选、独立 review、Validation 与浏览器批准

- 页面：Workbench → Draft Review；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/editions/base/draft-review`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=canon-chapter_92688f62db7a5fc7f4409175；draft_id=draft_8db2135be157eed857948ad3；handoff_id=handoff_21a74e4d2d5e043bff425b47
- 动作：浏览器确认第 5 章候选“黑石前的第二次判定”；独立 review 只提取连续记录与下一条更窄边界；Draft Review 显示 10/10 PASS 后批准。
- 页面可见结果：inline 显示“已写入正史”；Workbench 刷新显示 `正文 5` 与“黑石前的第二次判定 正史”；无 JS dialog、window.confirm 或 blocking modal。
- 机器输出：PLAN handoff=`handoff_665c68633dc35389ff1ca703`；DRAFT handoff=`handoff_21a74e4d2d5e043bff425b47`；contract=`contract_80c06c932ed9a4e856259054`；selected candidate=`candidate_7f41a8b10eeead0d41776d3d`；draft=`draft_8db2135be157eed857948ad3`；validation=`validation_fbf6d2cd3e6213bae1ba7faa`；semantic review=`REVIEWED`；publication findings=[]。
- Canon 证据：commit=`canon-commit_a339bc7c6fb17abf09028eec`；chapter=`canon-chapter_92688f62db7a5fc7f4409175`；event range=24–29；Canon content hash=`d54119b8c57b3e8b530d7dfd2e519fb9d68957fdbd7d3551060552d7244344c3`；snapshot=`snapshot_1e33adeec813849a5b1b4b1c`；projection state hash=`64d2f52d3a783c3d239d9520c99540b5b3a5aaa2f4b74ef671d00980154985ff`。
- 一致性判断：通过；第 5 章把外场验证继续压缩成更窄的公开判定，正文没有回退到城内名籍复核。
- 调试/下一动作：继续从第 5 章正史锚点创建第 6 章规划 handoff。

## 页面/事件 16 · Chapter 6 候选、独立 review、Validation 与浏览器批准并停止

- 页面：Workbench → Draft Review；URL：`http://127.0.0.1:8877/books/original-d336a8f607cd/editions/base/draft-review`
- 作用域：book_id=original-d336a8f607cd；edition_id=base；chapter_id=canon-chapter_c491c59c99304f6ba14ad3b7；draft_id=draft_930c3197afbad2c6c5a27b61；handoff_id=handoff_18c548fb36b8428cb2b76c26
- 动作：浏览器确认第 6 章候选“见证者名单上的新名字”；独立 review 重新阅读正文，确认名字进入名单和记录主体变化；Draft Review 显示 10/10 PASS 后点击批准。用户随后明确要求停止，不再创建第 7 章。
- 页面可见结果：inline 显示“已写入正史”；Workbench 刷新显示 `正文 6` 与“见证者名单上的新名字 正史”；无 JS dialog、window.confirm 或 blocking modal。
- 机器输出：PLAN handoff=`handoff_f38d69f3782eba6668fb25b1`；DRAFT handoff=`handoff_18c548fb36b8428cb2b76c26`；contract=`contract_a44fb5d352054ff5ee91dfc3`；selected candidate=`candidate_a6ba2124bb278d282af586cc`；draft=`draft_930c3197afbad2c6c5a27b61`；validation=`validation_e7d1cde797dc6f198b5f46f9`；semantic review=`REVIEWED`；publication findings=[]。
- Canon 证据：commit=`canon-commit_205e3257fad8d9edffbaea79`；chapter=`canon-chapter_c491c59c99304f6ba14ad3b7`；event range=30–35；Canon content hash=`bc9ff09e550106b23229c7b6bcd559be42cc02dcef0ec3adfa46e8aedc54d4fc`；snapshot=`snapshot_2d4bbabe3c2c9a5001b2dd1a`；projection state hash=`d9100dbd89273a3cdf8b7e88546f087a17ad5aba01fd71820a522d7534608303`。
- 一致性判断：通过；第 6 章把连续能力验证推进成公开记录主体变化；停止边界由用户明确给出，未创建第 7 章 handoff。
- 调试/下一动作：关闭续写路径，整理本实验 6 章审计材料。



