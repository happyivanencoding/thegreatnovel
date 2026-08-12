---
name: review-story-atlas
description: 审核 Story Atlas 的证据、冲突、就绪度、未知和 review queue；不把诊断或推断批准为 Canon。
---

# Review Story Atlas

Handoff Mode 只读取 `task.json` 指定的业务输入和已绑定 Atlas artifact；不要重新判断
task type 或重复校验 source/projection/registry/config hash。读取当前 Atlas manifest、全部
图谱、Narrative DNA、World Model、rules、assumptions、coverage/entity/contradiction/readiness
reports 和 Rolling Horizon。检查 CANON source span、INFERENCE reasoning/confidence/
counter-evidence、主角/当前线程/续写边界和远期未知；把问题写入 review queue，不修改正文、
Canon 或 Edition。
