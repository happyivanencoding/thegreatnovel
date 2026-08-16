$process-novel-handoff

处理 handoff_id=handoff_c25a239f6da2eda278554290。

运行 deterministic workflow start；成功后信任其 RUNNING contract。
Python 已冻结 executor_skill=continue-novel；调用 $continue-novel Skill，严格执行该 Skill 的 requested_stage=PLAN_ONLY。
业务输入只读取 task.json 指定的 business_input_files=["metric_context.json", "kernel_context.json", "world_state_context.json", "boundary_packet.json", "rhythm_context.json"]。



不得修改 book；不得批准写入正史；不得批准改写 Campaign；不得启用 Edition。
完成后将 result.json 写到任务输出目标，并运行 deterministic workflow complete；需要作者决定时写 waiting_for_user.json 并进入 WAITING_FOR_USER。