# Runtime Review

独立 Runtime Reviewer 原始报告保存在 `runtime-review-agent.md`。本报告补充旧 Full Hybrid 基线、恢复演示和第 4 章 State Delta 格式复核。

## 结论

- `hybrid_selective` 五章每章运行 2 个 Specialist，共 35 次章节链调用；旧 Full Hybrid 主链为 45 次，减少 10 次（22.2%）。
- 沈砚旧五章 Hybrid 主链 Prompt 总字符为 500,839；本轮为 282,036，减少 43.7%。若把旧第1章 single control 也计入旧实验总量 516,020，则减少 45.3%；single control 不属于旧 Hybrid 主链。本轮 Prompt 会随连续正文增长，不能声称跨章单调变短；正确结论是局部投影相对旧 Full Hybrid 明显变小，同时章节自然增长仍存在。
- Action Specialist 五章都被选中且都有采纳 Patch；Dialogue 在第 2、5 章有效；Opening 在第 1 章无 Patch、后续两章有效；Emotion 未在本盲测选择。
- 五章均有有效 Patch，因此 Integrator 5/5 有输入依据；无自然“无 Patch”样本，但 Ledger/API/单元测试已验证无有效 Patch 时可 skipped。
- `runs/recovery-demo/` 证明单节点恢复：第 3 章 Action 在实验副本中 failed → 复用原 Prompt retry → attempts 1→2；Director/Curator/Primary 保持 completed；Integrator/State Delta stale；正式正文和正式 manifest 未改。
- State Delta 内容推进有效；第 1、2、3、5 章原始 Response 通过当前 v2 标题校验。第 4 章原始 Response 缺少 `# State Delta Audit`，虽旧执行已应用，当前校验记录为失败并保留原始响应，没有自动重跑；这是本盲测的明确格式缺口。

## 生产建议

建议保留 `hybrid_selective` 作为默认：它减少了专项调用，并把最稳定的 Action 专项留给作者选择；`hybrid_full` 仍用于卷首、高潮和架构实验。正式上线前必须使用当前 State Delta v2 标题校验，缺标题只阻止 Delta 应用，不阻止正文保存。
