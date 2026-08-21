# Clean End-to-End Novel Test v1

本实验只保存本轮生成、运行和审查产物，不修改生产 Prompt、runtime、GBrain、Schema、UI 或其它生产代码。

## 范围

- 唯一作者输入见 `INPUT.md`。
- Fantasy Seed 只调用一次；随后只用独立 Blind Selector 选择一个候选。
- World Vision、Story Program、Dynamic Outline 各调用一次。
- 只按当前正式 Director → Chapter Prep → Writer → State Delta / Canon 链完成前三章。
- 三章全部冻结后才启动 Reviewer。
- GBrain、Reference Programs、旧 BOOK、历史实验和其它小说正文均不属于本轮输入。
- 不生成 Chapter 4，不根据质量重生成，不在本轮修复生产系统。

## 下游门禁的实验夹具

本轮按任务文件用独立 Blind Selector 替代作者人工看候选后的选择。当前生产 `generate_prompt` 对 World Vision、Story Program、Outline 需要内存中的 `author_approved` 状态；后续 Prompt 渲染会使用仅存在于本轮渲染进程中的审批夹具，让已选候选沿生产模板继续跑通。该夹具不写入生产 Creative State，不把模型选择记录为真实作者批准。

## 调用规则

每次生成在调用前先保存完整 rendered Prompt；只有 API 中断、无 response、写入失败、明显截断或 provider error 才允许使用相同输入重试，并记录原因。质量问题不触发重试。

## 产物边界

本目录是唯一实验写入范围。根目录的 `BOOK.md`、`PROMPTS.md` 和 `chapters/` 若在运行中创建，均只服务于本轮实验，不替代生产数据模型。
