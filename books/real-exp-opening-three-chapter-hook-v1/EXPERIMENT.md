# Opening Three Chapter Hook v1

## 实验目的

验证开书前三章专用执行合同在三本冻结作品上的真实生产效果：

- A《偷走明天的人》：核心幻想早期兑现压力样本；
- B《炉藏万象》：残器最后之愿与个人资产落袋压力样本；
- C《掌中天工》：既有 `STRONG_OPENING` 正向控制组。

本目录只新增实验产物，不覆盖旧实验、不修改冻结上游、不写入正式 Canon。Outline 可以基于冻结的 Fantasy Seed、World Vision、Story Program 重新生成；每本只运行 Chapter 1—3，禁止 Chapter 4。

## 真实运行边界

每个 Outline、Director、Chapter Prep、Writer、State Delta 都是一次独立真实子代理调用。主线程先保存完整生产 rendered Prompt，子代理再读取该 Prompt 并写入原始 Response；不使用 Reviewer 标准参与生成，不自动重试，不人工修正文，不换模型。当前环境未提供真实 token 计数时，所有 token 字段写 `UNKNOWN`，不以字符数代替。

本 Pilot 使用当前正式单 Writer `chapter` Prompt；不改变生产默认 Writer mode。章节正文只从 Writer response 的 `# 正式正文` 区块提取，Audit、事实摘要、状态 Delta 和来源信息分离保存。State Delta 只更新实验副本 BOOK 的状态区，失败时保留原始 response 与错误证据，不做格式修复或重试。

## 停止条件

三本均完成 Outline、Chapter 1—3 的 Director/Chapter Prep/Writer/State Delta 及实验副本状态承接后停止；随后只运行去标识的旧新前三章盲读与系统 Review。不得生成 Chapter 4、扩展到十章、重开上游或增加 Reviewer/评分器/Hard Gate。

