我会只核对定位、锚点与观察是否被当前文本窗口支持，不改动任何文件；先按项目记忆确认原著与证据文件的既有约定。证据文件的格式分为两套（`evidence_id` 与标题式 ID），我会统一按每个窗口实际声明的行号和锚点取原著窗口，不以文件开头的研究过程文字作为证据。接下来先做全量的“锚点—窗口—章节标题”机械核验；它能发现定位或短锚点的具体失配，失配后才逐窗复读事件与 observation。机械核验已经定位到若干“概括式锚点”并非逐字原文；这些不影响相应窗口的行号本身。另有两条证据在文件中自认没有对手交换／对手尚未入场，按 combat lane 的纳入标准应剔除。现在我在做最后的章节标题邻域校验，以区分“标题未包含在截取行内”与“标题、行号确实错配”。# Verdict

需修订：9 个锚点替换，17 个窗口剔除；其余 149 个窗口定位、核心事件与 observation 可由当前窗口支持，未发现需 `OBSERVATION_NARROW` 的条目。

# File Audits

- `combat_dasheng_evidence.md`：EDIT — `DS-L01` `DROP_WINDOW`（文件自述无对手交换、非 combat）。
- `combat_doupo_evidence.md`：PASS — `CD-01` 至 `CD-12`。
- `combat_guimi_evidence.md`：EDIT — `CG-04` `ANCHOR_REPLACE`。
- `combat_jiangye_evidence.md`：EDIT — `M01`、`M02`、`M04`、`M05` `ANCHOR_REPLACE`。
- `combat_quanqiu_evidence.md`：EDIT — `CQ-07` `DROP_WINDOW`（行号止于 164579，未覆盖所报第805章《杀出通天大道！》，其标题在 164934）。
- `combat_quanzhi_evidence.md`：EDIT — `CQZ-11` `ANCHOR_REPLACE`。
- `combat_sirenjing_evidence.md`：PASS — `SE-01` 至 `SE-12`。
- `combat_tunshi_evidence.md`：FAIL — `CT-01` 至 `CT-13` `DROP_WINDOW`（对应 TXT 按指定 GB18030/GBK 解码为系统性乱码，章节标题、原文锚点与事件均无法按本审计规则复核）。
- `combat_wudao_evidence.md`：EDIT — `CWM-05` `ANCHOR_REPLACE`。
- `combat_xianni_evidence.md`：EDIT — `XI-CX-14` `DROP_WINDOW`（窗口明确写明对手尚未入场，属战前布置，不是 combat exchange）。
- `combat_yishizhizun_evidence.md`：EDIT — `E11` `DROP_WINDOW`（所报“第120章《各有收获》”与该行窗不一致；本地文本此处由第119章转至第121章）。
- `combat_yongye_evidence.md`：EDIT — `YY-E02`、`YY-M05` `ANCHOR_REPLACE`。
- `combat_zhetian_evidence.md`：PASS — `E01` 至 `E12`。

# Replacement Anchors

- `CG-04`：`孩子会提前降生`
- `M01`：`黑色桃花`
- `M02`：`钟声节奏里的间隙`
- `M04`：`短矛插进`
- `M05`：`红线一动`
- `CQZ-11`：`冲锋三步`
- `CWM-05`：`后退示弱`
- `YY-E02`：`三颗特制的纯银原力弹`
- `YY-M05`：`巨弩箭头`

# Drop Windows

- `DS-L01`：无对手、无 combat exchange。
- `CQ-07`：章节/标题与 line range 错配。
- `CT-01` 至 `CT-13`：指定解码规则下无法取得可核验原文。
- `XI-CX-14`：战前布置，对手未入场。
- `E11`：章节标题与 line range 错配。

# Stats

- 文件：13
- 窗口：175
- 原样通过：149
- 保留但需换锚：9
- 剔除：17
- `OBSERVATION_NARROW`：0
