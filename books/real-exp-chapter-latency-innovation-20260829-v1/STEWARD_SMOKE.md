# tgn-system-steward 0.3.11 Final Latency Smoke

> Bounded read-only smoke; no repository file was modified by the audit agent.

## Frozen Input

Full Curator was changed from Luna high to Terra high. Four complete Curator → Primary → Reviser chains were 26.92% faster on average; Reader and Authority blinds were both 2:2, while hard actor / power-boundary / ending violations remained in the Terra route.

VERDICT: PARTIAL

KNOWLEDGE_CLASS: Experimental Hypothesis

WHY: Terra-high 在四章完整链路上取得了明确的 wall-clock 优势，且商业 Reader 与 Authority 双盲结果与 Luna 持平，说明它是有价值的性能候选。但最终正文仍出现行动者漂移、未授权分身规则，以及把“残压已散尽”改回“仍在散”的 Authority/State 级错误。第10章和第14章的问题不是单纯文风差异，而是足以阻止整条路线冻结为 production 默认的事实越权。当前证据支持“Terra 更快、质量大体不降”，不支持“Terra-high Curator 已安全替代 Luna-high”。根因暂不能归为 Curator 单层，因为缺少各节点 artifact 与 token/执行账目，必须保留为端到端 semantic route 的实验性结论。按协议应分别记为质量 PARTIAL、wall-clock PASS、成本 UNKNOWN。

WHAT_CAN_FREEZE: Terra-high 作为后续受控实验候选；四章样本中的约26.92% wall-clock 改善；商业 Reader 与 Authority 双盲未显示总体偏好劣化。

WHAT_MUST_NOT_FREEZE: Terra-high Curator 作为 production 默认；“更具体”可抵消 Authority 越权的判断；未完成完整节点账目、输入冻结和更多跨书样本前的成本结论。

- wall_seconds: 57.693
- model: gpt-5.6-luna
- effort: high
