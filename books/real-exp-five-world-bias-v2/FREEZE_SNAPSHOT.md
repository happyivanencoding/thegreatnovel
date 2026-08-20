# Generation Freeze Snapshot

冻结时间：2026-08-20T13:24:07.0049603+02:00

## Git

- TheGreatNovel 分支：`principal_dev_new_sys`
- TheGreatNovel commit：`a6e551460f1f13a8d42c44d43e8961b4f552958e`
- 实际生产 Prompt commit：`a6e551460f1f13a8d42c44d43e8961b4f552958e`
- 冻结时 tracked diff：无。
- 冻结时工作树新增范围：仅 `books/real-exp-five-world-bias-v2/`。

## Frozen candidate artifacts

以下是初次冻结时五个正式候选的原始响应与机械合并结果。初次合并后来发现终端大文件输出截断，污染版 Final 已另行留档；修复后的最终冻结见下方“Corrected Final Artifact Freeze”。

| Candidate | Fantasy Seed | World Vision | Mainline | Final |
|---|---:|---:|---:|---:|
| 01 · 未生之身 | 9,619 | 23,059 | 55,326 | 63,132 |
| 02 · 借万古一刹 | 11,705 | 22,610 | 44,223 | 62,685 |
| 03 · 死人簿外 | 9,435 | 15,839 | 50,428 | 55,916 |
| 04 · 败相归我 | 8,888 | 16,669 | 42,552 | 56,743 |
| 05 · 借败成仙 | 9,008 | 18,362 | 42,296 | 58,436 |

数字为冻结时文件字节数，不是质量指标。

## Independent generation records

### Fantasy Seed

- 01：`01a01ed5-ec68-7383-a08e-6b047fc88851`
- 02：`01a01ed5-ed8f-78f2-afe4-4c89a7a8ac87`
- 03：`01a01ed5-ef72-7091-bafd-e34258828b81`
- 04：`01a01ed5-f150-7670-bd21-915c042708b1`
- 05：`01a01ed5-f334-73b1-9535-1d420e89af1f`

### World Vision

- 01 正式最终写入：`01a01ed9-f2bc-7070-90b7-6e9204c43cc8`
- 01 另一次完成写入并已恢复留档：`01a01eda-3a1c-78e1-830e-f1445ffddf38`
- 02：`01a01eda-3b41-78f1-8c2d-e62b0c5990fb`
- 03：`01a01eda-3cf3-7502-8c82-c0ab139a7919`
- 04：`01a01eda-3ea7-70b2-af1d-2ad4c1d1b4e5`
- 05：`01a01eda-405c-7200-8fe3-ca8ec217a1d4`

### Story Mainline

- 01：`01a01ee0-4342-7f92-b4bc-ef1a509f04d3`
- 02：`01a01ee0-445c-7293-a1e8-1448c651091f`
- 03：`01a01ee0-4621-7460-894a-c980b2694953`
- 04：`01a01ee0-47d4-71a0-aa34-d5d21fa31d3a`
- 05：`01a01ee0-4975-7b61-b429-019a937622cc`

## Operational incident

Candidate 01 的 World Vision 阶段出现一个线程清理/延迟完成竞争：同一路径曾先写入 17,616 字节版本，后有另一个已启动的独立线程写入 23,059 字节版本。17,616 字节原始响应已从该线程运行日志恢复为 `candidates/candidate-01/world_vision_response_attempt-17616.md`；正式 `world_vision_response.md` 保留后写入版本，后续 Mainline 只读取正式文件。没有依据内容评分或人工选择版本，没有重生成；该事件作为实验运行事实保留。

## Freeze boundary

冻结后才允许读取五份 `final_world_and_mainline.md` 启动 Reviewer。Reviewer 不能修改任何候选；本快照和原始 Prompt/Response 一并作为生成阶段边界证据。

## Corrected Final Artifact Freeze

2026-08-20T14:07:46.2109074+02:00，使用本地文件流直接从五份原始 World Vision 与 Mainline Response 重建 Final；原始 Response 未改变，五份正式 Final 均确认不含 `tokens truncated` 占位符。修复后的正式 Final 字节数为：

| Candidate | Corrected Final |
|---|---:|
| 01 | 78,456 |
| 02 | 66,904 |
| 03 | 66,338 |
| 04 | 59,292 |
| 05 | 60,729 |

初次污染版 Final、三份受污染盲审和初次受污染 Meta 均保存在 `reviews/incident-truncated-final/`，不作为最终审查依据。

修复后重新启动的正式 Reviewer 线程：

- Blind A：`01a01f00-2d95-7611-9e21-c2e7206acc59`
- Blind B：`01a01f00-2ec7-79f0-bf7b-ed7eb68c70ac`
- Blind C：`01a01f00-3099-7192-be51-a02438ec3342`
- Meta：`01a01f09-247e-77d1-ae8a-5008f80cf2da`
