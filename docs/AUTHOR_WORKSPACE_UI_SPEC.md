# Author Workspace UI V3

> 项目执行规则以根目录 `PROJECT_RULES.md` 为唯一长期权威。本文只记录当前 Author Workspace 的真实信息架构、视觉系统与交互语义。

## 产品定位

Author Workspace 是阅读优先的本地小说创作舱，不是后台管理系统，也不是逐阶段审批表。**默认产品路径是 ChatGPT-operated Automatic Production Run：用户给方向 / 冻结输入 / 目标章数，TGN operator 跑完整生产链，用户主要阅读最终正文。** 界面继续复用唯一的 BOOK / Workflow / Run Ledger / Response 真源，不为视觉便利复制第二份 Authority；World / Character / Story 等 Freeze checkpoint 保留为 Agent 间信息边界，但其手工按钮属于高级检查 / 干预模式。

视觉采用两套独立主题：

- Light：暖灰纸白、雾蓝灰、深海军蓝文字，低饱和靛青、暗金与冷紫作为强调；
- Dark：深蓝黑、石墨灰与柔和象牙白，保持相同的层级关系和品牌强调色，不做简单反色；
- 主要卡片使用 22—28px 圆角、细边框、半透明渐变和轻 blur；阴影只用于浮层关系；
- 正文使用中文 Serif 系统栈和舒适行高；导航、工具栏、状态与数据区域使用 Sans Serif；
- 动效只做轻微 scale / fade / progress pulse，并遵守 `prefers-reduced-motion`。

## 信息架构

桌面端为四层结构：

```text
浮动项目栏
  ↓
窄导航 Rail → Story Structure Tree → 中央 Manuscript / Planning Surface → AgentDock 创作中枢
```

- 导航 Rail：概览、创意、故事设计、章节写作、记忆、工具；每个实际 view 只有一个 active item。
- Story Structure Tree：World、Power / Human / Character、Story Program、Long Plan、Future-10、当前章、Canon 与 Run，全部来自真实 Workflow artifacts 与已解析内容。
- 中央区：正文与长时间阅读优先；Overview 首先显示 Automatic Production Runs，复杂 Prompt、Response、Authority freeze、调试与手工采用动作进入右侧中枢或显式高级区。
- AgentDock：桌面常驻；中屏 / 小屏作为覆盖 Drawer。关闭 Drawer 后，运行中的任务仍通过轻量 mini anchor 保持可见。
- 顶部 Manuscript / Structure / Memory 切换真实 view；Audit / Versions 定位真实右侧区域，不伪装成概览页。

小屏使用单列内容、横向紧凑导航和覆盖式 AgentDock；390×844 下页面不得出现水平溢出。

## 默认 Automatic Production Run

用户不需要依次审批 World、Character、Story Program、World Expansion 或每一批章节。ChatGPT-operated 长任务在初始方向明确后，由 TGN operator 按既有 validator / Authority / retrieval / model routing 完成内部选择、Freeze、Adopt、正常失败恢复与后续生成；`author_approved` 等旧状态值只作为兼容性的内部 Frozen Authority 状态，UI 显示 `frozen`。手工编辑器和批准 API 不删除，但默认折叠并标为高级干预。

Overview 的 `Automatic Production Runs` 读取 `story-mvp-background` 持久任务，只展示 `job_id / label / status / timestamps / exit_code / sanitized error`，不展示 cwd、command、PID、日志路径或模型私有活动。浏览器只能读取 / 取消已经由可信 TGN operator 发起的任务，**不能提交 executable、cwd 或任意 runner command**。

## 长任务进度与心理锚点

AgentDock ACP 可能持续数分钟甚至更久。V3 不显示虚假百分比或 ETA，而投影下列真实信号：

1. 等待执行；
2. 建立会话；
3. 锁定模型、推理强度与只读配置；
4. 理解与计划；
5. 读取上下文、调用工具与验证；
6. 组织最终输出；
7. 完整性收尾；
8. 完成 / 失败 / 取消。

运行面板同时显示：累计耗时、距最近可见信号的时间、通用化的计划步骤、工具完成数、最近十条安全活动、取消入口，以及“可以继续写别处”的低打扰提示。1、3、5、10、15、20、30、45 分钟会产生一次新的长任务提醒；提醒只说明已用时、最近信号和仍可取消，不推断剩余时间。

真实 ACP `plan`、`tool_call`、`tool_call_update`、`agent_thought_chunk` 和 message phase 只映射到有限的作者可读活动词汇。UI 不展示 private reasoning、模型 commentary 原文、原始命令、文件路径、凭据或本机用户名。最终 Response 只接收明确的 `final` / `final_answer` channel。

页面标题、右侧 notice 和 mini anchor 会同步运行状态；mini anchor 不使用每秒 `aria-live`，阶段变化与完成通知通过稳定的 `role=status` 区域播报。ACP 路径存在只显示“入口可用”，ChatGPT 登录在真实任务启动时才确认。

浏览器对作业 list / get / cancel / create 使用明确 deadline。短暂状态查询失败时保留 pending lock 与已有活动，自动退避重试，不能因一次网络失败解锁重复启动；只有明确 404 / 服务重启丢失才终止轮询并 fail loud。

## AgentDock Response 边界（手工高级执行面）

`agentdock_acp` 仍是本机、有界内存的 Response executor：

- 后端可信解析 ACP，固定 TGN project root、`mcpServers=[]`、`read-only`、模型 / effort 白名单；
- ACP stdio 由 `node.exe` 直接启动 `@agentclientprotocol/codex-acp/dist/index.js`，不用 PowerShell wrapper 承载 UTF-8 NDJSON；`fs/read_text_file` 只读 project root 内 UTF-8 文件；`execute` permission 只单次放行并继续受 read-only sandbox 约束，`edit` / file-write / permission escalation 拒绝；
- 短控制 RPC 与最长 60 分钟生成 job 分开计时；stdout / stderr 持续 drain；cancel / timeout / shutdown 使用 terminate → wait → kill；
- pending job queue、ACP stdout event queue、activity、plan、output、error 与 completed history 都有界；stdout burst 通过有界 FIFO 反压处理，RPC response / callback 不丢弃；status 不返回 ACP 绝对路径；
- 手工 AgentDock job completed 不等于 Workflow artifact completed，不自动 Save / Apply / Adopt / Freeze。Automatic Production Run 是另一条由 TGN operator 明确委托的执行模式，它仍经过同一 Authority checkpoint，而不是把模型 Response 直接写成 Canon。

每次启动冻结：

```text
book_id + chapter_number + workflow_mode + Batch window
+ launch_token + exact Prompt + exact upstream input snapshot
+ target editor value + monotonic editor version
```

只有全部仍匹配且该 target 仍是最新启动，结果才自动回填。切书 / 切章 / 切节点、修改 Prompt、修改上游规划、改变 Batch 窗口、作者编辑 Response、刷新恢复、旧 launch 或服务重启丢失时，只允许只读查看；作者仍可在身份匹配后显式确认载入。

## GBrain Curator

GBrain 在 Workspace 中是三段式 Optional Inspiration 工作流：

```text
BOOK-aware Retrieval Brief
→ semantic retrieval + full-page extraction + compatibility filtering
→ author compare / select / assemble
```

### 检索与抽取

- `GET /api/gbrain/status` 只报告 CLI、embedding、active modes 与 optional-inspiration 角色，不暴露 Key；
- GBrain ON 阶段必须同时有 CLI 与 embedding；不可用时 fail loud，不降级为 keyword-only；
- 后端返回 raw / unique / accepted / rejected、partial query failures、fixed references，以及每个 accepted candidate 的独立 `formatted_block`；
- Human Seed 按 Appetite / Behavior / Relationship 三条 lane 分组，某 lane 没有可靠结果时宁可为空，不补弱卡。

### 比较、选择与组装

- 每次新检索默认 `NONE`，不会自动勾选候选；
- fixed reference 与 creative candidate 分开呈现；fixed 不占候选名额；
- 作者可以逐项选择、通过 selection tray 快速移除、并排比较来源类型 / 抽象 / transfer boundary；相关性分数明确不是质量评分；
- 只有作者点击“组装所选 Inspiration”后，才生成可编辑 Bundle；也可以明确点击“本轮不注入 GBrain”；
- 作者可以在当前明确组装结果上继续编辑，但不能用未绑定的手工文本绕过检索与选择。

### Stale 与 Prompt 边界

GBrain 请求冻结发起时的 book、chapter、mode、query、BOOK、World、Character、Story、Long Block、Outline 与 recent summaries。请求返回前任一项变化，返回结果不载入。

检索后相关输入、模式、Human Prototype 或 BOOK 变化时，旧候选与 Bundle 可保留供阅读，但显示 stale banner、禁用选择 / 组装，并从 Prompt payload 中剔除。新检索保留旧 Bundle但标为 previous，作者必须重新选择和组装。

只有同时满足以下条件的 Bundle 才进入 GBrain ON Prompt：

- 当前 retrieval 存在且上下文快照匹配；
- Bundle 来源是本轮 assembled，或在本轮 assembled 基础上的作者编辑；
- 当前选择 signature 未变化；
- required fixed references 仍存在。

GBrain OFF 阶段由前端返回空字符串，后端 `/api/prompt` 与 `/api/prompt/state-delta` 再次清空，保证 Chapter / Primary / Authority Delta / State 等阶段不接收 raw GBrain。GBrain 不自动写 Canon，不成为 Hard Gate 或 Authority source。

## Batch 与其它不变边界

Production 默认章节链仍是：

```text
Approved Future-10
→ deterministic Batch Packet
→ Terra-high Batch Primary
→ Terra-high Prose Delta ┐
                         ├→ deterministic Authority-first composition
→ Sol-high Authority Delta ┘
→ exact-window / exact-response preflight
→ 作者显式整批采用
→ State 逐章处理
```

Primary、Prose Delta、Authority Delta 与 State 使用独立 Response；两个 Delta 都绑定同一 Primary。窗口、Primary 或任一 Delta Response 变化都会使 preflight stale；预检显示 Authority patch 数、成功叠加的 Prose patch 数与因 Authority 重叠而跳过的 Prose patch。旧单章 Director → Curator → Primary → Full Reviser 仅保留为 fallback / 专项实验。

所有正式保存继续走 `saveCreativeArtifact`、`saveBook`、`approveChapter`、`saveRunPromptForMode`、`saveRunResponseForMode`、`applyCanonIndexProposal` 与现有后端 API。V3 不自动保存、不自动批准、不自动重跑 stale。

## 浏览器证据

当前 V3 冻结截图：

- `docs/ui-audit/workspace-v3-agent-progress-light.png`
- `docs/ui-audit/workspace-v3-gbrain-dark.png`
- `docs/ui-audit/workspace-v3-gbrain-compare.png`
- `docs/ui-audit/workspace-v3-mobile-anchor.png`

验证覆盖 1440×900 Light / Dark、GBrain 比较浮层、390×844 mini anchor、单一 active nav、无水平溢出、真实 ACP final channel、GBrain 默认 NONE / 显式组装 / stale fail-closed，以及短暂作业状态失败仍保留 pending lock。
