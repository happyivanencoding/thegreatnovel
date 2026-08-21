# Patch Attribution：Primary Draft → Integrator Final

## 判定规则

Patch 只有在该 Patch 的建议文本或其可识别的局部改写确实出现在 `Integrator Final`、而 `Primary Draft` 中不存在时才记为 `ADOPTED`。Integrator Audit 的“已采用”只作为线索，最终以 `diffs/chapter-XX-primary-to-final.diff` 与 Specialist 原始 Response 的实际文本对比为准。

`accepted_patch_count` 只统计真实发生的 Specialist Patch，不把 Integrator 自己的错别字或换行微调计入。

## Chapter 1

实际 Specialist：`opening`、`action`；实际 Integrator：1 次；Primary→Final 字符差异：71；变化段落：1；Primary/Final 均不是完全相同。

| Specialist | Patch | 是否采用 | 实际 Final 变化 | 类型 | 归因判断 |
|---|---:|---|---|---|---|
| Opening | — | N/A | Opening Response 明确无有效 Patch | — | 不产生变化 |
| Action | 1 | ADOPTED | 在三名矿奴脱险后增加唐鹭从车架下脱身、滚出塌口的路径 | action/spatial、continuity | 确实补齐“第四个人”前的空间链，但 Final 随后仍保留“四个人一个接一个滚出”的总括句；Reader 因此认为 Primary 更紧凑，形成局部节奏退化 |

本章是 `B_LOCAL_REPAIR_WITH_RHYTHM_REGRESSION`：Integrator 不是 copy，但只完成一个局部空间修补，并引入可见动作回叠。

## Chapter 2

实际 Specialist：`dialogue`、`action`；实际 Integrator：1 次；Primary→Final 字符差异：130；变化段落：8；Primary/Final 均不是完全相同。

| Specialist | Patch | 是否采用 | 实际 Final 变化 | 类型 | 归因判断 |
|---|---:|---|---|---|---|
| Action | — | N/A | Action Response 明确无有效 Patch | — | 不产生变化 |
| Dialogue | 1 | REJECTED | Final 没有替换 Primary 的“推到它卡 / 我先接住车”对白 | dialogue/character、continuity | Integrator Audit 说明该替换会删掉推车、阵盘受压和车身下沉的动作承接；Final 保留原链，拒绝是有证据支持的 |
| Dialogue | 2 | ADOPTED | 增加“下面有人在喘”“成片的，气都在往下沉”、唐鹭质问和“我跟你去/先告诉我”的协作边界 | dialogue/character、continuity、explanation | Final 确实包含该局部对话；Reader 认为它增强线索闭合、NPC 主动选择与下一章牵引，但也使解释更显性 |

另有一句“只剩习惯”→“只剩下习惯”的微调，不属于 Specialist Patch，记为 `other`，不计入 accepted patch。

本章是 `C_DIALOGUE_AND_CHARACTER_REPAIR`：Integrator 对局部对白/关系有真实价值，但不是所有建议都应采用。

## Chapter 3

实际 Specialist：`action`；实际 Integrator：1 次；Primary→Final 字符差异：81；变化段落：4；Primary/Final 均不是完全相同。

| Specialist | Patch | 是否采用 | 实际 Final 变化 | 类型 | 归因判断 |
|---|---:|---|---|---|---|
| Action | 1 | ADOPTED | 霍沉交付空白记录片，沈砚收起；章末伪造维修记录的物件来源成立 | continuity、other | 形成前置—回收，增强章末计划的可执行性 |
| Action | 2 | ADOPTED | 沈砚从散落工具中取得短锤，后续敲平滑轮/处理工具有来源 | action/spatial、continuity | 具体补齐行动准备，不增加新能力或资源 |
| Action | 3 | ADOPTED | 将“穿过他们脚下的门框”改为“沿门框穿回窄门外” | action/spatial、explanation | 修正站位与线路方向，降低空间歧义 |

本章是 `C_ACTION_CONTINUITY_AND_SPATIAL_REPAIR`：三项 Patch 都能在 Final diff 中定位，Reader 认为它们增强前置准备、空间清晰度和章末回收；对白项没有稳定改善。

## 汇总

| 章节 | Specialist calls | Integrator calls | proposed patches | accepted patches | Primary→Final diff | change class |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 2 | 1 | 1 | 1 | 71 chars / 1 paragraph | B：局部修补但节奏退化 |
| 2 | 2 | 1 | 2 | 1 | 130 chars / 8 paragraphs | C：对白与人物协作修补 |
| 3 | 1 | 1 | 3 | 3 | 81 chars / 4 paragraphs | C：动作连续性与空间修补 |

Integrator 不是昂贵 copy：三章均发生真实文本变化；但变化规模都局部，没有证据表明它进行了广泛 scene realization 重写。价值集中在可定位的 repair，而不是“多一个节点就整体更好”。
