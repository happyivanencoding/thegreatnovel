# Reader-facing ontology regression A/B

Baseline source: `books/real-exp-personality-advantage-tree-20260827-v1`.

目标失败：不是“出现任何新词”，而是读者必须先学习一串本书新词才能知道力量在做什么，或一个本来直接的力量在触发/成长时被改写成结构分析、材料诊断、路线计算、定义/权限等抽象过程。

受控阶段：

1. **World A/B**：同 Author Direction + 同已保存 World GBrain + Luna high；旧 Prompt 对比 Treatment。第一版各做多次复验，第二版只增加对第一版残余的“直接可感知作用”边界。
2. **Core Power A/B**：冻结同一旧 Approved World、同 Power GBrain、同 Novelty seed `2026082716` + Luna high；旧 Spark 的“理解障碍”对比可观察触发，并继续检查 mastery 是否重新分析化。
3. **Later Asymmetry**：冻结同一旧 World、两名不同 Human/Character、同 Story GBrain + Sol high；只增加后续新 Asymmetry 的“先白话、后命名”边界。
4. **Final generalization**：使用不含本轮术语要求的第二套作者方向生成 2 个新 World，并在其中 1 个 World 上重复问题 Spark 的 Power 生成。

成功条件：专名可以存在，但只压缩已经理解的对象；去掉专名仍能用短普通话说明核心作用；直接型能力的长期掌握不变回分析/验证流程；强度、可复合性与 Permanent Boundary 不被削弱。

记录：实际生成文本、Prompt、ACP payload、tokens 与 wall-clock；ChatGPT-login ACP payload 不提供 credits/cost，因此 `USAGE.json` 对该字段明确记为 N/A。
