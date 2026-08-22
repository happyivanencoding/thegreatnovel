# Clean 10-Chapter E2E — Scene Skill v1.1

本实验验证当前 `principal_dev_new_sys` 的完整新书到连续十章生产链，而不是继续优化 Scene Skill 本身。

## 核心问题

1. 单场景质量改善后，连续十章是否仍像一本成熟中文男频长篇，而不是十个局部正确的片段。
2. Curator 是否能随剧情自然选择不同 Scene Skill，而不是机械重复或为了 Skill 改写剧情。
3. Reader-First、Human Reaction、Planning → Prose 边界能否跨十章稳定保持。
4. 主角的身份、关系、资源、主动目标、能力与行动舞台是否产生连续阶段变化。
5. 一级成长、二级收益与反哺是否真正改变后续行动，而不是只存在于规划标签。

## 生产链

新书阶段使用当前生产模板与当前生产默认能力：

`Fantasy Seed → World Vision → Story Program / Idea → Outline`

章节阶段每章使用：

`Director → Context Curator → Primary Writer → State Delta`

- 使用 `writer_mode=curator_primary`。
- 不运行 Specialist / Integrator，除非生产链本身因为用户显式修复要求而需要；本实验默认全部不启用。
- 不手工指定 Scene Skill；必须由 Curator 自己选择。
- 不运行 Chapter Prep 作为额外 LLM 节点；Director 的八字段合同是当前章 WHAT HAPPENS 的唯一执行合同。
- 每章 State Delta 成功应用后，再生成下一章。
- 连续运行 Chapter 1—10，不根据文学质量重生成。

## Clean 边界

- 唯一作者输入是 `INPUT.md`。
- 不读取旧实验正文、旧 BOOK、旧候选或《借我一招》《炉藏万象》作为内容参考。
- 当前生产流程若本来会读取 GBrain / Genre Prior / Reference Program，可按生产默认逻辑使用；不得人工把历史实验内容塞入上下文。
- 不为了覆盖 Scene Skill 类型人为设计章节。
- 不为了让十章“更好看”手工改 Director、Curator 或 Primary Response。

## 子代理规则

所有需要 LLM 生成的节点由 Codex 独立 subagent 执行；不调用外部 API，不使用 `openai_executor.py`。

成功返回但质量差、选错 Skill、剧情普通、文字不满意，都属于实验结果，不重试。只有执行级失败（调用报错、空返回、明显截断、写入失败）才允许以同一 Prompt 重试一次，并记录原因。

## 产物

新书阶段保存每个节点的 `prompt.md` / `response.md` 与最终批准/选择结果。

每章至少保存：

- `director_prompt.md`
- `director_response.md`
- `curator_prompt.md`
- `curator_response.md`
- `scene_skill_selection.json`
- `primary_prompt.md`
- `primary_response.md`
- `chapter.md`
- `chapter_fact_summary.md`
- `state_delta_prompt.md`
- `state_delta_response.md`
- `BOOK_after_state_delta.md`

根目录保存：

- `BOOK.md`
- `CALL_LOG.json`
- `SCENE_SKILL_TRACE.json`
- `TEN_CHAPTERS_COMBINED.md`
- `FINAL_REPORT.md`

## 评价边界

不做机械总分。报告真实问题，也允许结论是“某部分已经正确”。

重点判断：

- 十章是否形成连续故事阶段，而非重复局部循环；
- 主角是否越来越主动；
- Scene Skill 是否自然切换且真的服务当前场景；
- 关系和人物反应是否跨章累积；
- payoff 是否真实改变后续可做之事；
- Reader-First 是否稳定；
- 是否出现 Planning Language leakage；
- 是否出现 Scene Skill 模板化；
- 第十章结束时是否形成继续阅读欲望。
