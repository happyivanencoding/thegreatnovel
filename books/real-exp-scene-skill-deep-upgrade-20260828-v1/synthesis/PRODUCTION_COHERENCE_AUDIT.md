我会按只读审计执行，先读取 `novel-scene-skills` 的完整规范，再限定在你列出的 production 文件内检查；不会读取 candidate 或 A/B mapping，也不会修改任何文件。此次检查会重点验证实际运行时传入的上下文，而不是只看静态文档。适用 Skill 已读取完毕。它明确要求：Deep Craft 与 Runtime 投影分层、Primary 只消费短问题/指导、Reviser 只消费短 Watch，且 source-specific evidence 不得进入 production；我将按这些硬边界审计。现在补做一次与本仓库相关的记忆索引快查，然后进入文件检查。当前静态目录确认有 24 个已注册 scene 文件、3 个 shared references，且每个 Primary 都有 Reading Question / Projection Guidance / Revision Watch 字段。初步看不到不存在的 combat 变体引用；接下来我会把“是否只是字段齐全”与“内容是否实际工程化/过长”分开核对，并追到 prompt/runtime/test 的真实传递路径。静态审计到这里的判断是：24 个 Reading Question 没有需要合并的明显同义项；`investigation`/`deduction`、`training`/`comprehension`/`breakthrough`、`hunt`/`resource`/`crafting` 的边界是不同阅读问题而非换名重复。非 `NONE` 的 Revision Watch 只有 `social_bargain_decision` 与 `relationship` 两张，符合“极少数”要求。下一步只跑 Scene Skill v2 定向测试：它能具体发现注册目录、Primary 隔离、Projection 下传或 Watch 下传是否回归；失败时我会据失败位置判断是 production 还是测试环境问题。定向测试尚未进入断言：pytest 在启动捕获阶段找不到可用临时目录（`FileNotFoundError`），这是环境准备失败，不是 Scene Skill 失败。下一步只检查一个已有的 `C:\tmp` 是否可用；若可用，就把 pytest 临时目录显式指向它，以实际执行同一组断言。即使显式指定 `C:\tmp`，pytest 仍无法创建临时文件，说明当前受限执行环境没有可写临时目录；断言仍未执行。测试本身是有价值的（会验证本次审计关注的 runtime 隔离），我将请求一次仅用于运行这组只读测试的受限外部权限；不改仓库文件。定向 Scene Skill v2 测试已通过：`2 passed, 19 deselected`。这确认了当前测试覆盖到的 Catalog→Curator、Projection→Primary 隔离、以及短 Watch→Reviser 传递均成立。为避免仅凭印象判断“短”，我再做一次只读的字段长度/内容异常检查，并检查 24 个文件的 Handoff 引用是否都落在注册表内；这一步若发现异常，我会只报告会改变运行行为的项。项目规则还要求“说审计时”独立使用当前 `tgn-system-steward` 做一次只读审计，再与主线程复核合并。我现在补执行这一项；它不会读取 candidate/A-B，也不会修改生产，只会按系统根因/层级边界复核当前结论。Steward 规范要求审计前确认工作树与最近冻结状态。我只读取 `git status` 和最近提交元数据，不打开其它文件、不触碰 candidate/A-B；这只用于判断当前 production 是否可能被未提交改动遮蔽，不会改变审计范围。Steward 的具体复核仍以你列出的 production 文件为证据。复核结果已收敛：目录字段完整、24 个 Handoff 引用均已注册、shared references 没有进入 `SCENE_SKILL_IDS` 或 Catalog；指定六类 Deep Craft 虽有较深的步骤化 Generation Lens，但其工程化风险被限制在研究层，未下传 Writer/Reviser。工作树本身有大量既有未提交改动，我未读取 candidate/A-B，也未修改任何内容。现在整理最终五段结论。# Verdict

PASS。当前 Scene Skill v2 production 自洽，无需阻断性修复；只读完成，未修改文件。

# Findings

- 24 个 Primary 均已注册，Reading Question 区分清楚；`investigation/deduction`、`training/comprehension/breakthrough`、`hunt/resource/crafting` 不构成重复合并项。
- Combat 变体均作为 posture/条件存在，没有发现未注册 skill 引用。
- Projection Guidance 均为短句，明确允许 `NONE`，没有下沉成 checklist。
- 非 `NONE` 的 Revision Watch 只有 `social_bargain_decision` 与 `relationship` 两项，且是 failure-triggered 短观察点。
- Combat、training、trial、resource、crafting、recovery 的 Deep Craft 虽有步骤化内容，但仍停留在研究层，并明确要求压缩流程、停止重复；未进入 Writer/Reviser。
- 未发现书名、作者、locator、evidence id 或 source-specific 内容泄漏。
- Shared references 明确未进入 Primary Router。

# Must Fix

无。

# Nice To Have

可补充覆盖全部 24 个 skill 的结构化测试；当前测试通过了代表性 `trial+combat` 与 `social+relationship` 路径，但这只是测试覆盖增强，不是 production 缺陷。

# Runtime Closure

- Curator 接收的是 `ID + Reading Question + Projection Guidance` 紧凑目录：`scene_skills.py:93`、`prompts.py:1993`。
- Primary 会移除 `Scene Skill Selection`，不直接接收完整 Skill：`scene_skills.py:186`、`prompts.py:2000`。
- Reviser 只接收已选 skill 的短 Revision Watch：`scene_skills.py:163`、`prompts.py:2063`。
- 指定 Scene Skill v2 测试通过：`2 passed, 19 deselected`。
- 仍保留的 `render_selected_scene_skills` 已明确标注为 legacy/research renderer，未接入当前 Primary runtime：`scene_skills.py:147`。
