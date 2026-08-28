我会按“只读指定材料、严格剔除 fidelity invalid windows”的边界执行：先读取当前三类 Primary、实验证据与 fidelity 文件，再逐个确认现有 ID 与有效窗口，最后只修改对应 skill 文档；不会新增同义 Primary，也不会把资源/制作流程抽象成故事发动机。此次使用 `novel-scene-skills`，因为任务本身要求深化既有 Scene Skill，并遵守其 source-blind 与投影边界。规范已确认：Scene Skill 只回答“这场戏读者持续追问什么、Writer 如何把它写成真实场景”，不能改章合同、Canon 或增加门禁。刚才环境没有 `rg`，因此改用等价的只读文件名筛选；这一步只用于定位用户明确允许的材料，若发现路径缺失我会据实处理。指定证据已读完。fidelity 审计明确为：80 个窗口中 74 个原样通过、6 个仅需替换 anchor、`DROP_WINDOW = 无`；因此本次没有 fidelity invalid window 可纳入剔除，但会遵守“修正后的定位才有效”的边界，并不把任何未经核实的候选补进来。当前最清晰的新增量是：猎取的“搜索/筛选/取得”分层与保有形态，资源戏的价格参照/稀缺类型/配置后果，制作戏的阶段门与继续—保全—报废选择。下一步写三份候选 v2，`showcase_evaluation` 只作为既有相邻 Primary 的 handoff 终点，不新增第四个同义能力。我会把结果写入本实验的 `synthesis/candidate_skills/`，作为待纳入候选，不覆盖当前生产 skill；这样能保留现有工作树中的其他修改与作者审阅边界。三份文档都会保持 source-blind：不带书名、窗口号、原文专名或证据引用，只保留可迁移的场景规则。`Revision Watch` 按要求写 `NONE`，因为本轮没有直接 A/B 文本可作为修订依据。三份候选 v2 已写入实验目录。现在做一次窄范围验收：检查每份是否都有八个规定字段、是否误带书名/窗口号/证据 ID、是否误生成新 Primary，以及是否明确了与 `showcase_evaluation`、`relationship`、`combat` 的交接。若检查命中具体缺陷，我只修该缺陷；不会为已经正确的内容再做重复审计。验收命令本身出现 PowerShell 管道语法错误，尚未产生验收结论；这是检查器问题，不是文档问题。我会修正为先收集结果再格式化，继续只检查上述具体条件。字段与 source-blind 检查已通过：三份文档均包含规定的八个字段，没有发现书名、窗口号、证据 ID 或新增 Primary，且三份都明确了到 `showcase_evaluation`、`relationship`、`combat` 的 handoff。第二个小检查器又因同样的 PowerShell `foreach |` 写法失败；我会改成结果数组后再跑一次，只确认 `Revision Watch = NONE` 与文件行数，不扩大检查范围。最后的路径/工作树检查再次只是 PowerShell 管道写法错误，未触碰文件。字段、source-blind 和 `Revision Watch` 检查已经有明确通过结果；我只补一个不使用 `foreach` 管道的存在性检查，确认三份文件确实落盘，并确认当前生产的 `showcase_evaluation.md` 没有被本次写入覆盖。已完成三份 source-blind v2 候选文档：

- [hunt_acquisition_v2_candidate.md](C:\dev\tgn-story-mvp\books\real-exp-scene-skill-deep-upgrade-20260828-v1\synthesis\candidate_skills\hunt_acquisition_v2_candidate.md)
- [resource_economy_v2_candidate.md](C:\dev\tgn-story-mvp\books\real-exp-scene-skill-deep-upgrade-20260828-v1\synthesis\candidate_skills\resource_economy_v2_candidate.md)
- [crafting_creation_v2_candidate.md](C:\dev\tgn-story-mvp\books\real-exp-scene-skill-deep-upgrade-20260828-v1\synthesis\candidate_skills\crafting_creation_v2_candidate.md)

已确认：

- 三份均包含规定的八个字段。
- `Revision Watch` 均为 `NONE`。
- 未新增同义 Primary。
- 已覆盖 search / selection / acquisition、机会成本、阶段门、继续/保全/报废、成果证明及到 showcase / relationship / combat 的 handoff。
- fidelity 审计中 `DROP_WINDOW = 无`；6 个问题仅为 anchor 替换，不构成剔除窗口。
- 当前生产版 `showcase_evaluation.md` 未被本次覆盖。
