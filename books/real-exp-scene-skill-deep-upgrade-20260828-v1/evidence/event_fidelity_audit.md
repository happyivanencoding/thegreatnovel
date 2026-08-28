我会按“证据窗口逐条核原著”的标准做只读审计：确认章节、标题、行号、短锚点、核心事件和观察结论是否都没有越出窗口；不会修改任何文件。先定位 A 的输出格式与本批 evidence 清单。已确认审计范围为 9 份 evidence（其中 `relationship` 两份、`showcase` 两份），并找到了 A 的固定交付结构。接下来我会以每一条 Evidence Window 的 locator 为入口读取对应 TXT，不把跨窗后果当作当前窗口证据。训练组的逐窗复核已完成：`training_cangyuan` 的 19 个 locator 与锚点均可在原文窗口中确认；`training_wudao` 的 16 个 locator/章节与核心事件也成立。当前只发现一处需要收窄的表述：`TW-15` 把导师的风险判断写成了已被文本绝对证实的“即时致命”，但同窗主角随即保留了冰部可救场的反证。其余三组仍在逐段读取本地原文，而不是依据章节摘要判断。所有审计结论都会按 A 的五段结构合并，并且只报会实际改变 evidence 文本的条目。我已完成训练类的源文本复核，并在等待关系、离别/身份、牺牲/展示三组完成相同粒度的窗口核对；目前没有发现需要丢弃的训练窗口。已收回两组完整回核：关系类共确认 2 个窗口必须弃用、4 个需精确修订；离别/身份类确认 2 个身份窗口把核心亮相放在了 locator 外，不能保留。继续等待牺牲与展示组。牺牲与展示组覆盖的窗口数量最多，仍在逐一核对；我会等它完成后统一给出可直接回写 evidence 的最小修订清单，不会凭机械 locator 预检替代正文核验。# Verdict

需修订。共核验 129 个窗口：106 PASS、19 EDIT、4 DROP_WINDOW；未修改任何文件。

# File Audits

- `departure_zhuxian_evidence.md`：EDIT `ZX-D07`；其余 12 窗口 PASS。
- `identity_douluo_evidence.md`：FAIL `E04`、`E08`；其余 10 窗口 PASS。
- `relationship_jiangye_evidence.md`：FAIL `E06`；EDIT `E11`；其余 10 窗口 PASS。
- `relationship_zhuxian_evidence.md`：FAIL `ZX-M-05`；EDIT `ZHX-L6-24-01`、`ZHX-L7-14-01`、`ZHX-L8-12-01`；其余 11 窗口 PASS。
- `sacrifice_douluo_evidence.md`：EDIT `SE-DL-01/02/03/10/12`；其余 9 窗口 PASS。均为章节标签与实际跨章范围不一致。
- `showcase_doupo_evidence.md`：EDIT `DP-01/04/05/10/13/14/16`；其余 9 窗口 PASS。`DP-01` 的二长老初始质疑在窗外；`DP-10` 不应写成“改为年轻一辈赛事”；`DP-14` 漏列第1328章；`DP-16` 应止于第1569章。
- `showcase_quanqiu_evidence.md`：EDIT `GQG-SHOW-08`；其余 11 窗口 PASS。应把“敌人立刻撤离”收窄为“敌方被击杀/擒拿，失去行动能力”。
- `training_cangyuan_evidence.md`：PASS，19 窗口均成立。
- `training_wudao_evidence.md`：EDIT `TW-15`；其余 15 窗口 PASS。风险应表述为导师判断的“高温错误快且难救援”，不能写成文本已绝对证实的即时致命。

`OBSERVATION_NARROW`：

- `relationship_jiangye:E11`：恐惧表白与“回长安”均在该窗外，应移回 E10。
- `relationship_zhuxian:ZHX-L8-12-01`：空石台、绿衣角、昏倒均在 27042 后，不可保留。
- `showcase_quanqiu:GQG-SHOW-08`、`training_wudao:TW-15`：按上述收窄。

# Replacement Anchors

- `ZX-D07` → `带回大竹……峰`
- `relationship_jiangye:E11` → `陈某想要杀我`
- `ZHX-L6-24-01` → `抓的更紧`
- `ZHX-L7-14-01` → `不怪……她`
- `DP-04` → `三年之约，结束了`
- `DP-05` → `以一敌三`
- `DP-13` → `1395`

# Drop Windows

- `identity:E04`：亮出教皇令的关键动作在 14883–14892，当前窗从 14894 开始。
- `identity:E08`：红环显露与御之一族接受唐门都在当前窗外。
- `relationship_jiangye:E06`：范围跨入下一章，且“老人接受家务秩序”的依据在窗前。
- `relationship_zhuxian:ZX-M-05`：核心火化、安葬与称师父均属于下一章《化解》，当前 locator 不成立。

# Stats

- 总窗口：129
- PASS：106
- EDIT：19
- DROP_WINDOW：4
- ANCHOR_REPLACE：7
- DROP_ANCHOR：0
- OBSERVATION_NARROW：4
