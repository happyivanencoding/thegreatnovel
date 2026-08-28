我将严格只读这三类实验 Markdown 与其引用的本地原著 TXT，按原文逐窗核验；不会修改任何文件。已完成逐字锚点与行号的第一轮交叉检查：多数窗口定位可复现；目前发现少数锚点落在窗口外或缺失。接下来只对这些异常和跨窗归纳做原文复核。# Verdict

通过。81 个窗口的 locator 与核心事件均可由对应 TXT 复核；无 `DROP_WINDOW`。发现 36 个缺失、非 literal 或落在窗口外的 anchor，均已给出原文内 ≤12 字替换。

# File Audits

- `chase_xianni_evidence.md`：12/12 locator、章节与核心追逃状态成立。`XIANNI-CHASE-06`、`11` 的原 anchor 在窗外，改锚即可。
- `chase_yongye_evidence.md`：14/14 成立。`YY-EM-05` 的 `两道山岭之外` 在窗外；窗口内“沟壑—回身射击—追兵止步”核心事件成立。
- `stealth_guimi_evidence.md`：15/15 成立，但全部缺少 anchor 字段；文件开头“GB18030 会乱码、实际 UTF-8”的说明与本地 TXT 相反：GB18030 可正确还原正文，UTF-8 才乱码。
  - `OBSERVATION_NARROW`：E03、E08、E12、E13 是能力边界／身份方案／风险判断，能证明“决策条件”，不能单独证明伪装或反制已经成功兑现。
- `stealth_sirenjing_evidence.md`：12/12 成立，12 个 anchor 均为窗口内 literal。
- `survival_diyixulie_evidence.md`：13/13 成立。SE-DY-01、07、13 需改锚。
  - `OBSERVATION_NARROW`：SE-DY-01 只证明异常痕迹促成脱队边界，不证明营地已遭明确怪物威胁。
- `survival_quanqiu_evidence.md`：15/15 成立，但全部缺少 anchor 字段。
  - `OBSERVATION_NARROW`：SQ-01 是行动前职责与撤退阈值布置，证明的是预案结构，不是该预案已在战斗中生效。

# Replacement Anchors

- `XIANNI-CHASE-06` → `二话不说转身就逃`
- `XIANNI-CHASE-11` → `三人一直跟随`
- `YY-EM-05` → `数米宽的沟壑`
- `SE-DY-01` → `鱼肉鱼骨竟然全都不见了`
- `SE-DY-07` → `十块换一枚`
- `SE-DY-13` → `马车在营地外围成一圈`

`stealth_guimi`：

- E01 `公共盥洗室`
- E02 `密契仪式`
- E03 `只能是你自己`
- E04 `化妆改扮后`
- E05 `对哪些东西过敏`
- E06 `详细资料`
- E07 `识破身份`
- E08 `第三层身份`
- E09 `阳台滑落`
- E10 `没有不在场证人`
- E11 `表演得很好`
- E12 `乔装改扮`
- E13 `顶替某个人身份`
- E14 `留下了一些尾巴`
- E15 `还能再等一等`

`survival_quanqiu`：

- SQ-01 `不可抵抗`
- SQ-02 `打了两分钟`
- SQ-03 `灭了这座城`
- SQ-04 `伤痕累累`
- SQ-05 `战略性撤退`
- SQ-06 `16个精血合一`
- SQ-07 `围杀他们的武者近千人`
- SQ-08 `统计战损`
- SQ-09 `挡住30秒`
- SQ-10 `服用复神丹`
- SQ-11 `交不交`
- SQ-12 `搅乱人群`
- SQ-13 `带走他们就行`
- SQ-14 `守护那些重伤的同袍`
- SQ-15 `维持通道开启`

# Drop Windows

无。

# Stats

- 审核窗口：81
- locator／核心事件成立：81
- 保留原 literal anchor：45
- 需 replacement anchor：36
- `DROP_ANCHOR`：0
- `DROP_WINDOW`：0
