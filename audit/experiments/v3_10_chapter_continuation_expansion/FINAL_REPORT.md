# v3 Original 十章连续续写实验：最终审计

生成日期：2026-08-16
实验性质：一次性、隔离的 `creation_mode=ORIGINAL` 实验，不是生产书的 Canon。

## 结论

系统闭环已真实跑通；正文质量判定为 `PARTIAL`，不是“文学质量全通过”。

- Browser 创建 Original、确认 Reader Kernel、Core Innovation、Story Foundation、Development，并生成第一章候选均已完成。
- 第 1–10 章逐章经过 Candidate → Chapter Contract → Draft → 十项校验 → 明确作者批准；共 10 个 Canon commit。
- 浏览器工作台最终显示“原创项目 · 10 个正式章节”，左栏逐章列出 1–10，十章均标为“正史”。
- 当前隔离书状态为 `WRITING_READY`；保留了失败与重试的 handoff 轨迹，没有把失败路径删除或伪装成成功。
- 正式 Batch 没有宣称通过：隔离书没有 `ACTIVE Story Atlas + FAR` horizon，因此本实验采用逐章连续执行，不能替代 Batch contract 验证。

实验根目录：

`C:\dev\小说续写系统\audit\experiments\v3_10_chapter_continuation_expansion\browser_smoke_20260816`

隔离书：`original-e56a54687506`
浏览器验收页：`http://127.0.0.1:8065/books/original-e56a54687506/editions/base/workbench`

## Canon 结果

| 章 | 标题 | 正文字符数 |
|---:|---|---:|
| 1 | 第一章 墙还在，路没了 | 2408 |
| 2 | 窗缝之外 | 1871 |
| 3 | 没有地面的平台 | 1294 |
| 4 | 屋顶在墙后 | 1148 |
| 5 | 倒着写的门 | 810 |
| 6 | 没有回声的楼梯 | 742 |
| 7 | 风从屋顶下面来 | 738 |
| 8 | 风把脚印吹回去 | 523 |
| 9 | 第三次重排 | 552 |
| 10 | 塔顶没有答案 | 720 |

数据库核对：10 个 `CANON_COMMITTED` draft、10 个 Canon commit、100 个验证报告且 0 个验证失败；另有 2 个保留的非 Canon `DRAFT`（第一章重复草稿、第二章第一次修订失败稿）。

handoff 共 29 个：23 `COMPLETED`、5 `STALE`、1 `FAILED`。失败和未采用路径被保留为审计轨迹；没有待处理的 `READY_FOR_CODEX` handoff。

## 确定性诊断

- 十章的 Canon、Timeline、Knowledge、Economy / Power、Debt、Payoff、Repetition 等硬验证均通过。
- 警告不是硬失败：`CHARACTER_FIT_BELOW_MINIMUM` 10 次；`CONTRACT_EVIDENCE_EMPTY` 66 次；`REALIZED_KERNEL_EXCEEDS_VERIFIED_CONTRACT` 28 次；`SCENE_REALIZATION_THIN` 4 次；`KERNEL_TRACE_WITHOUT_EFFECTIVE_CONTRACT` 1 次。
- 节奏快照共 11 个。标题重复、精确重复、开头/结尾相似度和同功能连续段没有触发硬问题；但 `ending_mode=unknown` 连续到第 10 章，最终为 `STRONG_WARNING`。这说明短实验的章末模式没有被充分标注，不能当作已解决的节奏证据。

## Live Reference Corpus

最终 live diagnostic：`ENABLED`，`query_ready=true`，`bundle_seal_valid=true`，367 张卡片，无 warnings / knowledge gaps。机器包 hash：

`3120e088142f5d75ad3f2d1d18eca36f5b89251369228b4f73c7f63e796ff9f9`

本次复核的三个 query 均返回 `ENABLED`：规划（地图转场/探索）1 张 exact，规划（纯收益/新能力）5 张 fallback，动作 prose 3 张 exact。Reference Corpus 只作为 `REFERENCE_ONLY` 机制提示，没有写入 Canon。

## 两份盲读审阅的合并判断

两位独立盲读者都认为可以继续第 11 章，但不应直接把这十章当成完整成熟的连载开篇：一份给出 `READABLE`，一份给出 `PARTIAL`；综合判定为 `PARTIAL`，不是 `BLOCKED`。

共同优点：核心幻想没有被普通求生解释替代；第 1 章的测距带选择、第 9–10 章从记录转为外探构成可追踪的主因果；广播与真实空间的冲突形成了清楚的悬疑规则。

共同问题：

1. 第 5–8 章重复“测量—记录—不进入—回撤”，中段缺少资源、伤害、路线突破或人物交互的实质变化。
2. 测距带连续多章承担几乎全部推进，“每天只能选一件”的取舍逐渐变成固定选择，物品进化爽点变窄。
3. 已核实的正文连续性问题：第 1 章写手电“彻底暗下去”（`chapter-000001...md:101`），第 2 章却写“手电还亮着”（`chapter-000002...md:5`）；第 1 章明确只有“一块旧的铝制指示牌”（`chapter-000001...md:19`），第 9 章突然出现“三块铝牌”（`chapter-000009...md:3-5`），中间没有取得另外两块的事件。
4. 第 1–2 章都使用二点九四米作为不同空间关系的精确结果；文本虽试图解释为新缝隙关系，读者仍可能把它读成测量/设定重复。
5. 第 10 章留下楼外天光、相邻建筑、广播来源和脚印主体等悬念，但下一章的具体行动目标还不够硬。

建议的第 11 章方向：从已确认的楼外天光出发，设置一个带具体代价的资源或落脚点目标，首次让测距带以外的物品选择真正改变生存状态，并兑现一个明确结果后再打开新问题。不要继续复制“测距—记录—撤退”模板。

## 代码与验证交付

本次实验真实暴露并修复了两处生产路径问题：

- `src/novel_authoring/planning/candidates.py`：Creative Candidate output 导入不再先构造一个不满足最小候选数约束的空 `CandidateOutput`。
- `src/novel_authoring/web/routes/workflow.py`：PLAN_ONLY 的 workflow handoff 与候选任务 Operation Workspace 分离时，正确按候选 task id 回解任务 manifest。

代码提交并已推送：`e78e504 Fix creative candidate import and continuation task lookup`。

验证结果：

- 完整 pytest：538 passed，1 failed。唯一失败是工作树中预先删除的根目录 `AGENTS.md` 使 `test_agents_rejects_worktree_creation_instruction` 无法读取文件；没有发现本次修复导致的测试失败。
- mypy：`Success: no issues found in 200 source files`。
- Python compileall：通过。
- 全仓 ruff：188 条既有 lint 债务；本次两个修改文件的命中均在旧代码行，未对全仓做无关清理。

本实验只使用隔离 `library/original-e56a54687506`，没有向生产 `book/` 写入 Canon；工作树中原有删除、未跟踪素材和其他实验产物均未被回退或纳入本次提交。
