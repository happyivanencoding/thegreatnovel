# Original 浏览器连续质量实验（截至第 6 章）

状态：STOPPED_AT_USER_REQUEST_AFTER_CHAPTER_6

这是隔离的 creation_mode=ORIGINAL 浏览器实验。用户在第 6 章批准写入正史后要求停止，因此本目录是 6/10 的审计包，不是完整十章实验，也不把未生成的第 7–10 章写成空白成功。

- book：original-d336a8f607cd
- edition：base
- 临时运行库：C:\Users\jingx\AppData\Local\Temp\thegreatnovel-original-e2e-20260817-a
- 浏览器工作台：http://127.0.0.1:8877/books/original-d336a8f607cd/editions/base/workbench
- 已批准 Canon：6 章；Canon commit：6；每章 10/10 validator PASS；每章独立 publication review 均为 REVIEWED
- 审批边界：每章均由内部浏览器 Draft Review 点击“批准写入正史”；没有 CLI approve、直接 SQLite 写入或手工 Canon 补写
- 未纳入：临时 SQLite、WAL/SHM、operations、server cache、未跟踪实验库

目录说明：

- canon/CHAPTER_01.md–CHAPTER_06.md：从当前 Canon 投影导出的正文
- SIX_CHAPTERS_COMBINED.md：六章合订正文
- TEN_CHAPTERS_COMBINED.md：诚实的停止标记，不是伪造的十章正文
- reports/per_chapter_quality.md：逐章机器证据
- deterministic_audit.md：事件连续性、验证、审批和保留失败轨迹
- blind_review_a.md、blind_review_b.md：两份独立盲读
- comparison_with_v3.md：与 v3 五项问题的状态对照
- inputs/：作者输入、停止边界和 workflow ID 索引

v3 对照基线位于仓库已有的 audit/experiments/v3_10_chapter_continuation_expansion/；本实验没有复制其完整运行库。
