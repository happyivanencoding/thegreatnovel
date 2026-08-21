# Parallel Execution Experiment · Browser Workflow Audit

## 页面/事件 1 · 初始工作台回读

- 时间：2026-08-21 Europe/Paris
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:18065/`
- 作用域：experiment=`real-exp-prose-execution-parallel-v1`; book_id=`UNKNOWN`; edition_id=`UNKNOWN`; chapter_id=`UNKNOWN`; draft_id=`UNKNOWN`; handoff_id=`UNKNOWN`
- 动作：启动实验副本工作台并读取可见 DOM；未读取 Candidate B。
- 输入：`STORY_MVP_WORKSPACE=C:\dev\tgn-story-mvp\books\real-exp-prose-execution-parallel-v1`
- 页面可见结果：工作区路径正确；页面显示 Fantasy Seed → World Vision → Story Program、当前章 Director、当前章执行小纲、单 Writer、State Delta、Run Ledger 等真实生产入口；初始未加载具体小说。
- 机器输出：页面标题为 `Transparent GBrain Story Studio`；DOM 可见 GBrain 开关区域和 `GBrain：未查询`。
- 一致性判断：通过。工作区边界与实验目录一致；没有可见 Candidate B 内容。由于当前 checkout 没有 Skill 文档所说的 workflow handoff/edition 页面，`book_id/edition_id/handoff_id` 保持 UNKNOWN，不从 URL 或 SQLite 推断。
- 调试/下一动作：使用当前生产 Python `generate_prompt` 函数渲染并保存实验 Prompt；不把不存在的 workflow 页面伪造为已执行。

## 页面/事件 2 · 端口基础设施失败

- 时间：2026-08-21 Europe/Paris
- 页面：无页面变化；工作台端口尝试
- 作用域：experiment=`real-exp-prose-execution-parallel-v1`
- 动作：尝试绑定 `127.0.0.1:8765`。
- 输入：同一应用与同一 `STORY_MVP_WORKSPACE`。
- 页面可见结果：服务器启动后因 WinError 10013 无法绑定 8765，随即退出。
- 机器输出：`[Errno 13] error while attempting to bind on address ('127.0.0.1', 8765): [winerror 10013]`。
- 一致性判断：UNKNOWN；这是本地端口权限/占用问题，不是生成链结果。
- 调试/下一动作：改用 `127.0.0.1:18065`，不重试任何内容调用。

## 页面/事件 3 · 实验工作台可见状态

- 时间：2026-08-21 Europe/Paris
- 页面：Transparent GBrain Story Studio；URL：`http://127.0.0.1:18065/`
- 作用域：experiment=`real-exp-prose-execution-parallel-v1`; book_id=`UNKNOWN`
- 动作：重新导航后读取 DOM。
- 输入：同一实验工作区配置。
- 页面可见结果：工作台成功加载；页面明确显示“作者保留判断权”，Prompt 与 Codex Return、Run Ledger、Director、Chapter Prep、单 Writer、State Delta 控件均可见；GBrain 显示未查询。
- 机器输出：HTTP 页面可见；当前下拉列表尚未选定 candidate book，故未提交任何保存、批准或 Canon 动作。
- 一致性判断：通过浏览器层回读；实验生成仍由保存后的生产 Prompt + 独立代理完成，正式书籍 Canon 未改变。
- 调试/下一动作：继续执行 C 的唯一 Outline 调用；所有 response 仍先落盘到实验目录。

## 页面/事件 4 · A Chapter 1 Writer 硬门投影失败

- 时间：2026-08-21 Europe/Paris
- 页面：无新增页面动作；生产 Prompt 渲染层
- 作用域：candidate=`candidate-a`; chapter=`1`; stage=`Writer`
- 动作：用生产 `generate_prompt(mode="chapter")` 渲染 Writer Prompt，输入为已落盘的 A Chapter 1 Prep response。
- 输入：原始 `chapter_prep_response.md` 保留八个字段名与内容，但字段名单独占行、内容在下一行。
- 页面可见结果：生产 `validate_current_outline` 拒绝，原始错误为 `当前章小纲缺少非空字段：触发事件、推动事件的人、主角行动、对手或世界反应、直接结果、状态变化、叙事功能、结尾推动力`；Writer 未调用。
- 机器输出：失败发生在 `src/story_mvp/prompts.py:1154-1158` 的现行解析器；`chapter_prep_prompt` 当前显示格式与该解析器接受的同一行格式不一致。
- 一致性判断：原始 response 未被覆盖，内容调用未重试；这是生产接口形状不一致，不能归因于正文质量。
- 调试/下一动作：在实验目录生成 `chapter_prep_for_writer.md`，只把每个标签与其紧随的原始内容行无损合并；再次调用同一生产渲染函数。该派生文件不写回生产代码、Prompt 或正式 Canon。

## 页面/事件 5 · 实验终态

- 时间：2026-08-21 Europe/Paris
- 页面：工作台仍位于 `http://127.0.0.1:18065/`；本事件同时核对实验文件状态
- 作用域：experiment=`real-exp-prose-execution-parallel-v1`; candidate=`A,C`; chapters=`1—3`
- 动作：读取实验最终产物与 Git 状态；未执行浏览器保存、批准或正史提交。
- 输入：A/C 各三章的已保存 Prompt、response、正文、事实摘要、State Delta 和实验 BOOK 副本。
- 页面可见结果：实验工作台入口可见；正式 Canon 未被页面操作改变。
- 机器输出：A/C 各 3 个正文目录；Chapter 4 不存在；A/C Reader、World Engine、Execution Fidelity、Cross-Candidate 与最终 verdict 文件均存在；`src/`、`tests/`、`pyproject.toml` 无 tracked diff。
- 一致性判断：通过。`Chapter → experiment-local State Delta/Canon snapshot` 链条闭合；正式书籍/生产 Canon 保持未写入。State/Canon 是否造成 recap 保持 UNKNOWN，未把 WARNING 升级为失败。
- 调试/下一动作：按任务要求停止，不生成 Chapter 4，不修改生产层。
