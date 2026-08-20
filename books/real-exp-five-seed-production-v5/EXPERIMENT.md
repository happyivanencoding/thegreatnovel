# Clean Compounding Seed Test v1

## 目的

只验证 Compounding Growth Engine v1 对 Fantasy Seed 的影响，不进入 World Vision、Story Program、Outline、章节生成、Canon 或 State Delta。

## 生产边界

- 生产 Prompt commit：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`
- 生产基线至少包含：`b6828961e9e4939577e66264cc0b9a62de1ade95`
- 输入唯一来源：本目录 `INPUT.md`
- 只调用一次 Fantasy Seed 生成：一个 Agent、一个 request、一个 response、一次生成五个候选
- 不调用 GBrain，不读取历史候选、v1/v2/v3/v4、reviewer、任务诊断或 Reference Programs
- 不自动重生成；生成失败时保留失败证据并停止
- 五个 Seed 冻结后才进行 blind reviewer 与跨候选审查

## 输出边界

唯一生成 response 保存为 `fantasy_seed_response.md`；其中标注的五个冻结 Seed、冻结快照和审查记录只作为本次实验产物，不回写生产 Prompt 或其它生产模块。

## 执行结果

- 有效模型调用：1 次；一个 Agent、一个 request、一个 response、五个候选。
- 模型：`gpt-5.6-luna`
- response：`chatcmpl-EEz0gQ0Jx2JHXDabXmdH1jQUdLTRA`
- 生成结果：成功，`finish_reason=stop`
- CLI 预检：一次 400 参数拒绝，发生在模型生成前；未产生 response，未改变输入或生成内容。
- 冻结与审查：已完成；审查只读冻结 response。
