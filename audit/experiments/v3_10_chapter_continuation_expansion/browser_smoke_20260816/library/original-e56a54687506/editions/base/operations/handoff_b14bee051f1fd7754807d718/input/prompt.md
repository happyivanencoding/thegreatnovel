$process-novel-handoff

处理 handoff_id=handoff_b14bee051f1fd7754807d718。

运行 deterministic workflow start；成功后信任其 RUNNING contract。
Python 已冻结 executor_skill=continue-novel；调用 $continue-novel Skill，严格执行该 Skill 的 requested_stage=DRAFT_AND_VALIDATE。
业务输入只读取 task.json 指定的 business_input_files=["metric_context.json", "rhythm_context.json"]。

 作者本次特别目标：这是原创小说 Genesis 首章。只使用已经选择的 candidate_id=genesis-candidate-proposal-e39fee0d664e4e06923df0f31beee8eb-foundation-folded-tower-chapter-measuring-tape、contract_id=contract_d1955693b3c1166033b242e9 与 draft task_id=draft-task_7ff942998af9bb352a54375b；完成正文导入和十项校验，停在 VALIDATED。。该目标只作为 Author Control Intent 与本次操作输入，不得直接写入 Canon。

不得修改 book；不得批准写入正史；不得批准改写 Campaign；不得启用 Edition。
完成后将 result.json 写到任务输出目标，并运行 deterministic workflow complete；需要作者决定时写 waiting_for_user.json 并进入 WAITING_FOR_USER。