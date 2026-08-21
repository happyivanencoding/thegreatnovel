# Cost Audit

所有 token/sampling 字段均为 `UNKNOWN`；chars 只是字符观察值。

| clean snapshot | Single prompt | Primary-Fallback prompt | Curator prompt | Curated Primary prompt | Curator chain input | Single response | Primary response | Curated response |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| b2 replacement | 31,145 | 26,593 | 23,332 | 18,210 | 41,542 | 7,044 | 8,326 | 6,826 |
| b3 reused | 36,493 | 31,965 | 22,131 | 22,624 | 44,755 | 8,200 | 6,492 | 6,886 |
| c2 reused | 29,805 | 24,369 | 22,080 | 14,985 | 37,065 | 8,130 | 7,062 | 6,902 |

Curator chain input = Curator prompt + Curated Primary prompt. Curator 在 b3/c2 压缩最终 Primary prompt，但始终增加一次独立 content call；最终判断使用完整 chain cost，而不是只看 Curated Primary 是否更短。

新增调用：4 content calls；corrected Reader calls：3；Specialist/Integrator/Director/Chapter Prep/State Delta：0。
