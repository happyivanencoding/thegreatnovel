# Clean 10-Chapter E2E — Ready for Codex Subagents

状态：**scaffold ready / generation not started**。

本目录已经冻结实验边界、作者输入、Scene Skill v1.1 基线与确定性 verifier；真正的新书生成和 Chapter 1—10 LLM 节点必须由 Codex subagent 执行。

执行前先读：

1. `INPUT.md`
2. `FREEZE_SNAPSHOT.md`
3. `EXPERIMENT.md`
4. `CODEX_SUBAGENT_RUNBOOK.md`

完成 10 章后运行：

```powershell
python books/real-exp-clean-e2e-scene-skill-v11-10ch/verify_experiment.py
```

它只生成确定性 trace / 合并稿 / 后台术语复核，不评价文学质量。
