# Validity Audit

## Old snapshot-01

状态：`INVALID_CONTEXT_CONTAMINATION`

目标是《炉藏万象》Chapter 1，但上一轮 `snapshot-01/frozen-input/BOOK.md` 已含 Chapter 1—3 Recent Summaries、裂路器、火鳞胚、五名获救炉工以及 Chapter 3 结束后的岔口/窟心目标。Primary-Fallback 生成“第四章 火线尽头”是该错误 Canon 的可解释响应，不是单纯 presentation format 错误。

该 snapshot 的三 Arm、旧 blind body、旧 Reader 结论全部排除，不进入最终 Architecture Verdict；旧 raw evidence 不删除、不覆盖。

## Old snapshot-02 → clean b3

状态：`CLEAN`

目标是《炉藏万象》Chapter 3；BOOK 来自 Chapter 2 后 State Delta，Previous Prose 是 Chapter 1—2，Current Outline/Plan 是 Chapter 3。三 Arm 正文事件范围符合目标章节；旧正文标题差异属于 `PRESENTATION_FORMAT_ONLY`，本轮 blind packaging 统一剥离单个外层标题。

## Old snapshot-03 → clean c2

状态：`CLEAN`

目标是《掌中天工》Chapter 2；BOOK 来自 Chapter 1 后 State Delta，Previous Prose 是 Chapter 1，Current Outline/Plan 是 Chapter 2。三 Arm 正文事件范围符合目标章节；标题文字不同属于 `PRESENTATION_FORMAT_ONLY`，已在 blind packaging 中统一剥离。

## Replacement b2

状态：`CLEAN`

目标是《炉藏万象》Chapter 2；BOOK 为 Chapter 1 后 State Delta，Previous Prose 为 Chapter 1，Current Outline/Plan 为 Chapter 2。Single、Primary-Fallback、Curator-Primary 三份 raw body 均从 Chapter 2 当前合同开始，没有把 Chapter 3 的火鳞胚/窟心状态作为已发生事实，也没有完成 Chapter 2 之外的后续主体事件。

Primary-Fallback 的 `## 第二章：断镐铸成裂路器` 只属于 `PRESENTATION_FORMAT_ONLY`，blind option 去除该外层标题；Raw body 保留完整。

## Final clean set

最终 Architecture Verdict 只使用：

1. replacement b2：《炉藏万象》Chapter 2；
2. clean b3：《炉藏万象》Chapter 3；
3. clean c2：《掌中天工》Chapter 2。

旧 snapshot-01 不参与任何最终计数或门槛判断。
