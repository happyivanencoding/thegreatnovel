# Prompt / Context Cost Audit

字符数是 Python 字符数观察值，不转换为 token；所有实际 token 均为 `UNKNOWN`。Curator chain 的总输入为 `Curator prompt + Curated Primary prompt`，不把 Curator Response 再额外重复加一次，因为它已经包含在 Curated Primary prompt 字符数中。

| snapshot | arm | prompt chars | response chars | call count | prompt context |
|---|---|---:|---:|---:|---|
| 01 | Single | 14,210 | 4,127 | 1 | full Reader-First：Authority、Book Contract、Chapter Mission、Canon Prose/Index、Plan、Prose Profile、Opening Contract |
| 01 | Primary-Fallback | 9,662 | 4,584 | 1 | Primary context + explicit missing-Curator fallback |
| 01 | Curator | 10,096 | 4,670 | 1 | Curator projection input：Authority、事件合同、Book Contract、Canon、Plan、Prose Profile、transition |
| 01 | Curated Primary | 10,675 | 5,709 | 1 | Primary context + raw Curated Chapter Context |
| 02 | Single | 36,493 | 8,200 | 1 | full Reader-First + two chapters of prior prose |
| 02 | Primary-Fallback | 31,965 | 6,492 | 1 | Primary context + explicit fallback |
| 02 | Curator | 22,131 | 4,350 | 1 | Curator projection input + long prior context |
| 02 | Curated Primary | 22,624 | 6,886 | 1 | Primary context + raw Curated Chapter Context |
| 03 | Single | 29,805 | 8,130 | 1 | full Reader-First + prior prose |
| 03 | Primary-Fallback | 24,369 | 7,062 | 1 | Primary context + explicit fallback |
| 03 | Curator | 22,080 | 4,266 | 1 | Curator projection input + prior prose |
| 03 | Curated Primary | 14,985 | 6,902 | 1 | Primary context + raw Curated Chapter Context |

## Curator compression finding

Curated Primary prompt 相对 Primary-Fallback：

- snapshot-01：`+1,013` chars；Curator 没有带来最终 Prompt 压缩。
- snapshot-02：`-9,341` chars；最终 Primary Prompt 被明显压缩。
- snapshot-03：`-9,384` chars；最终 Primary Prompt 被明显压缩。

但完整 Curator chain 相对 Primary-Fallback 的总输入仍增加：

- snapshot-01：`10,096 + 10,675` vs `9,662`；
- snapshot-02：`22,131 + 22,624` vs `31,965`；
- snapshot-03：`22,080 + 14,985` vs `24,369`。

因此 Curator 确实在 2/3 snapshot 压缩了最终 Primary context，但额外一次调用使总输入/响应成本上升；是否值得由质量结果决定，而不是由压缩本身决定。
