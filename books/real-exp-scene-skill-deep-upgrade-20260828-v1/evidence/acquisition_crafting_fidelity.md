我会严格只读本实验的三类 evidence 文件及其对应原著 TXT，逐窗回核章节、行号、锚点与观察，不改动任何文件。这里会使用“小说证据提炼”流程来保证引用可追溯；它不会引入额外资料。已确认“同 D”的交付为固定审计结构：Verdict、File Audits、Replacement Anchors、Drop Windows、Stats。接下来进行一次机械定位核验；它只会发现行号、章节边界或锚点的具体失配，命中项才进入逐窗原文复读并判断是否需收窄或剔除。定位与章节边界核验已完成：80 个窗口的行号均有效，章节序列与本地文本一致。现在只复读每窗的核心证据／解释字段，专门检查“叙述事实是否被误写成结论”；若发现结论超出窗口，我会只收窄 observation，不会误删仍成立的定位。# Verdict

需修订：6 个锚点替换；其余 74 个窗口的章节、标题、1-based 行号、核心事件与 observation 均由对应本地原著窗口支持。无需 `DROP_WINDOW` 或 `OBSERVATION_NARROW`。

# File Audits

- `crafting_aoshu_evidence.md`：EDIT — `AOSHU-CRAFT-08`、`11`、`12`、`13` `ANCHOR_REPLACE`。
- `crafting_doupo_evidence.md`：PASS — `DPC-01` 至 `DPC-12`。
- `hunt_doupo_evidence.md`：PASS — `H01` 至 `H12`。
- `hunt_zhetian_evidence.md`：EDIT — `ZHT-H09`、`ZHT-H11` `ANCHOR_REPLACE`。
- `resource_guimi_evidence.md`：PASS — 16 个窗口。
- `resource_quanqiu_evidence.md`：PASS — `RQ-01` 至 `RQ-15`。

# Replacement Anchors

- `AOSHU-CRAFT-08`：`预想之中的轨迹`
- `AOSHU-CRAFT-11`：`一个电子`
- `AOSHU-CRAFT-12`：`叠加在一起`
- `AOSHU-CRAFT-13`：`在原理上等价`
- `ZHT-H09`：`不怎么顺畅`
- `ZHT-H11`：`需要得到阵图才能收走`

# Drop Windows

无。

# Stats

- 文件：6
- 窗口：80
- 原样通过：74
- 保留但需换锚：6
- 剔除：0
- `OBSERVATION_NARROW`：0

未修改任何文件。
