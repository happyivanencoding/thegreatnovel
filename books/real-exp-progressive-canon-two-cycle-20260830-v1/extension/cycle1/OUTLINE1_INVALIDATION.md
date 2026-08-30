# Invalid Outline1｜Model self-gate

`extension/cycle1/OUTLINE1.*` 不计入实验成绩。

原因：production code 的 `creative_state` 已通过 World Vision / Character Authority / Story Program 作者批准门禁，但模型在 Prompt 中只看到 `CURRENT CHARACTER｜Forward Authority`，误把 deterministic forward snapshot 当成一个新的待批准 Character，主动停止并要求作者再次批准。

这不是用户缺少批准，也不是 Mystery 候选失败。V2 只增加一条已有架构事实：`Character Authority 已批准；CURRENT_CHARACTER 只是 deterministic forward snapshot，不产生第二个批准点。` 其它输入不变。
