# Original Novel Genesis

原创小说与导入小说共用同一套 Authoring Kernel。差异只发生在创作起点：原创项目没有不可变
来源正文，因此不运行 Source Coverage、Arc Extraction 或已有小说 Story Atlas 初始化，也不制造
假“第 0 章”。

## 状态

`ORIGINAL_SEED → BOOTSTRAP_READY → FOUNDATION_ACCEPTED →
FIRST_CHAPTER_DRAFTING → FIRST_CHAPTER_VALIDATED → WRITING`

- `ORIGINAL_SEED`：只保存 premise 与可选作者约束。
- `BOOTSTRAP_READY`：Codex 桌面端已生成 Proposal，仍没有 Author Truth、章节或 Canon。
- `FOUNDATION_ACCEPTED`：作者明确确认后，系统建立 Author Truth、持久指令、九维 Book Profile、
  SHORT/MID/LONG Rolling Planning、Genesis Boundary 和三个首章候选；仍没有正式章节。
- `FIRST_CHAPTER_DRAFTING` / `FIRST_CHAPTER_VALIDATED`：复用 Chapter Contract、Draft 和十项
  Validator，草稿停在批准门前。
- `WRITING`：作者逐字确认“批准写入正史”后，第 1 章成为正式 Canon；后续复用标准续写工作流。

## Proposal 合同

`ORIGINAL_BOOK_BOOTSTRAP` handoff 必须输出恰好三个书名、三个结构上不同的 Story
Foundation、三条未来路线和三个首章候选，并包含主角、目标、冲突、代价、成长、世界规则、
人物/势力、第一阶段目标、Rolling Planning、开放问题、风险与避免陈词滥调。LONG 只描述方向
和可能性，不能固定结局或生成逐章 FAR 大纲。

三条路线始终属于同一本 Book/base Edition。重新生成只产生新的 handoff 与 Proposal，不创建
Book、Edition 或 Canon 分支。

## 作者批准边界

“确认基础框架”和“批准写入正史”是两道不同的显式批准：

1. 确认基础框架只把 Proposal 转为作者控制层和 Genesis State。
2. 选择首章候选后才建立 Chapter Contract 与 Draft handoff。
3. 十项 Validator 全部通过后，草稿停在 `VALIDATED`。
4. 只有作者当前明确提供“批准写入正史”，系统才创建第 1 章与 Canon Commit。

原创项目不检查不存在的导入 Source Manifest；它仍校验当前投影、Edition、合同、Draft 内容、
Validator 和作者批准。已有导入小说的 Source 校验保持不变。
