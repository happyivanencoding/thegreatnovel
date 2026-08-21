# Parallel 3-Chapter Execution Stress Test v1 · Final Verdict

## 冻结基线

- repository：`C:\dev\tgn-story-mvp`
- branch：`principal_dev_new_sys`
- HEAD：`5992f62d11e8014c3cf783bf993589e1cb881585`
- Long-Form Pacing baseline：`2c1e3434b6d68043ba0aac556e63d7912ba23368`
- frozen state：`CREATIVE_CHAIN_FROZEN_V2` + `OUTLINE_FROZEN_V2`
- GBrain：OFF；Reference Programs：OFF；Candidate B：未读取

## 两本结果

| Candidate | Reader | World Engine | Execution Pipeline | Nearest Failure Layer |
|---|---|---|---|---|
| A《偷走明天的人》 | `A_PROMISING_BUT_TOO_ABSTRACT` | `EARLY_WORLD_ENGINE_HEALTHY` | `EXECUTION_PIPELINE_MIXED` | `Chapter-03 Writer / formal_prose.md` |
| C《吞界行舟》 | `C_PROMISING_BUT_GOVERNANCE_THIN` | `EARLY_WORLD_ENGINE_HEALTHY` | `EXECUTION_PIPELINE_HEALTHY` | `NONE_OBSERVED` |

## 跨类型判断

已确认的共同 execution 纹理：

- 两本主角都先诊断/核对/测量再施用能力；A 因此明显延迟资产兑现，C 目前仍把判断嵌入现场动作。
- 两本 Writer 都出现规律化 AI 文风家族：否定一个解释后立即给出正确解释、因果链过度整齐、正确判断过密、NPC 对话承担功能、章末钩子节拍相似。
- NPC 在局部场景中都容易承担流程或主题功能；A 偏制度/主题代理，C 偏人口与物流单位。
- 两本都有表层机制 recap，但 State/Canon 是否造成 recap 属于 `UNKNOWN`，本轮证据不足以归因。

没有确认的共同生产失败：

- 解释过量不是同等强度的共同问题：A 明确成立，C 只有局部规则密集。
- `PREP_OVERLOAD` 两本均为 `NO`。
- `DIRECTOR_AS_EXPANDER_ONLY` 两本均为 YES 的结构纹理，但没有被证实为质量回归。
- 世界只围绕主角转、资产都没有拥有感、领地取代个人成长，均没有作为共同失败成立。

## 是否重新打开 Frozen 层

结论：`NO_REOPEN_SUPPORTED`。

A 的时间机制、占有感、主角可替代性和第 3 章 Writer 设计语言泄漏是高概念候选的局部 execution 问题；C 的资产规模与治理薄弱是类型专项风险，且 C 的 execution verdict 健康。两本没有出现足够同质、同层、同机制的共同失败证据，不支持修改全局 Director、Prep、Writer、State/Canon、GBrain 或 Frozen Creative Chain。

## 生成与正史边界

- A/C 各完成 Chapter 1—3，共六章；没有 Chapter 4。
- 每章均有 Director Prompt/response、Chapter Prep Prompt/response、Writer Prompt/response、正式正文、事实摘要、State Delta Prompt/response 与实验 BOOK 状态快照。
- C 仅补生成一次当前 Outline；不重生成、不优化。
- State/Canon 更新只应用到本实验副本，不写正式书籍。
- 本轮只新增实验产物；生产代码、生产 Prompt、既有 Canon 未修改。

## 最终停止点

实验已完成，按任务要求停止；不生成第 4 章，不修改 Prompt，不重写正文，不添加 World Engine、角色卡或 prose checker。
