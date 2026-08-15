# revise-novel

用于在 `Novel_Authoring_System_Constitution_V2.md` 约束下执行版本化改写。改写不是续写重试，也不得把 `drafts.revision` 当作改写版本号。

## Handoff Fast Path

如果 `workflow start` 已返回 `status=RUNNING` 且 `executor_skill=revise-novel`，只读取
`task.json` 指定的业务输入，复用已冻结且有效的 Edition、Impact inputs、Rhythm、Metrics
和 Atlas。不要再次运行 edition list、source preflight、完整 features rebuild 或重复 hash
校验；只有被修改章节实际改变且业务输入明确失效时，才重建受影响 feature。Approval 与
Edition activation 边界保持不变，并由 Python 的 complete/approval 路径负责。

## 硬边界

1. Direct Maintenance 模式先运行 `novel edition list`，确认 base、父版本锚点、源文件
   manifest SHA-256 和当前 ACTIVE edition；Handoff Mode 直接使用 START 冻结的 Edition。
2. 改写必须在派生 edition 中完成：`novel edition create --edition-id <id> ...`。base 永远保留，不删除、不覆盖、不把变体追加到 base 正文。
3. `RevisionSpec` 必须通过 `extra=forbid` 校验并持久化到 `library/<book>/editions/<edition>/revision_campaigns/<campaign>/`。
4. 先 deterministic source/FTS scan，再完成 Codex 语义影响审计；任何 `MUST_REVIEW` 只能 HANDLED 或提供理由的 `EXPLICITLY_WAIVED`，不能把“扫描完成”当作“影响已处理”。
5. 只接受 `task_type=REVISION_DRAFT` 的输出；导入前核对 task/campaign/unit/edition、章节 preimage SHA-256、schema 和文件哈希。
6. 依次执行 impact → plan → draft-task/import → validate → preview。批准改写必须逐字输入 `批准改写版本`；批准只提交目标 edition，不自动启用。
7. 只有作者明确输入 `启用改写版本` 才能调用 edition activate。激活前确认目标 edition 为 VALIDATED，且 base projection/source hash 未漂移。
8. 失败事务必须回滚事件、投影、variant、物化表和快照文件；discard 只将改写草稿标记为 REJECTED，不创建 variant。
9. Direct Maintenance 模式或被修改章节实际改变时，才按目标 edition 重建
   `chapter_features` 并运行 rhythm/hooks 诊断；旧 content hash 的特征失效但保留历史。节奏
   诊断只作为 Repetition Fatigue、Pressure Curve、Narrative Debt/Thread Priority 的证据，
   不新增总分，也不能绕过十项改写校验。Handoff Mode 复用已冻结且有效的输入。
10. Workbench 改写任务只能使用 Local File Handoff Protocol：先运行
    `novel workflow start`，按 `requested_stage` 执行并写回 result，最后运行
    `novel workflow complete`；Web 不启动 Codex、不批准 Campaign、也不激活 Edition。
11. 改写读取当前 edition 的 Story Atlas 仅作为带 hash 的软上下文；Atlas 的未来路线、
    INFERENCE 和 CANDIDATE 不能被改写当作 CANON，Atlas refresh 必须生成新的 child 版本，
    不覆盖 base 或旧 edition artifact。

## Reference Corpus 与共享 Prose Realization

Impact Audit 只分析作品内部事实，不调用 Reference Corpus。Impact Packet 完成后，
`build_revision_plan` 通过唯一的 `query_reference_corpus(purpose="PLANNING")` gateway
冻结 `reference_planning_context`；它只提供可迁移的机制、对照和知识缺口，不能决定
哪些事实必须改、选择 RevisionUnit 或覆盖 RevisionSpec。

`prepare_revision_draft_task` 再通过同一 gateway 以 `purpose="PROSE"` 冻结
`reference_prose_context`，并写入 `reference_context_snapshot.json` 与 `input.md`。
Revision Draft 必须读取并遵循 `.agents/skills/novel-prose-realization/SKILL.md`，
与普通 Draft 共用 Novel Prose Realization、Naturalness Audit 和有界 Targeted Repair
协议；不得创建第二套 revision humanizer 或正文生成逻辑。Prose Controls 只能改变句法、
段落节奏、信息呈现、对话自然度、描写和场景收束，不能改变 RevisionUnit、required
changes、must preserve、事件顺序、人物选择、资源、知识边界或 expected_after_state。

所有 Reference Context 都是 `REFERENCE_ONLY`，并在 task/plan artifact 中保留 status、
snapshot/package identity、card count、selected card ids、warnings 和 knowledge gaps。

## 推荐命令

```text
novel edition create --book-id <book> --edition-id <edition> --display-name <name>
novel revision create --book-id <book> --edition-id <edition> --spec revision_spec.yaml
novel revision impact --book-id <book> --campaign-id <campaign>
novel revision impact-complete --book-id <book> --campaign-id <campaign> --decisions decisions.json
novel revision plan --book-id <book> --campaign-id <campaign>
novel revision draft-task --book-id <book> --campaign-id <campaign> --unit-id <unit>
novel revision import --book-id <book> --output output.json
novel revision validate --book-id <book> --campaign-id <campaign>
novel revision preview --book-id <book> --campaign-id <campaign>
novel features rebuild --book-id <book> --edition-id <edition>
novel rhythm diagnose --book-id <book> --edition-id <edition>
novel hooks diagnose --book-id <book> --edition-id <edition>
novel revision approve --book-id <book> --campaign-id <campaign> --confirm "批准改写版本"
novel edition activate --book-id <book> --edition-id <edition> --confirm "启用改写版本"
novel export --book-id <book> --edition-id <edition>
```

真实 `book/` 只允许做源文件校验、影响分析、投影重建和导出 dry-run；未经作者明确批准，不得产生任何 revision commit 或 chapter variant。
