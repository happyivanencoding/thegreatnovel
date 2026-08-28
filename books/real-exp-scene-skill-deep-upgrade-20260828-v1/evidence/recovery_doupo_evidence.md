我会按 source-first 方式先读取本地原著并核验现有 Scene Skill 的边界；只输出可定位的证据窗口与由其支持的判断，不把推测写成原著事实。此任务会使用 `distill-novels` 来保证本地文本的编码、定位和来源边界，并使用当前 `novel-scene-skills` 的定义来做“现有能力缺口”对照；两者都只用于证据抽取与比较，不改动项目文件。先做一次解码与章节索引核验：它会检测“GB18030 解码是否可用、章节标题能否稳定定位”；若失败，我会改用 GBK 再逐行核对，避免把乱码或错误行号带入证据。章节索引已确认全书共 1,646 章。我正在按“受损→处理→可观察反馈→首次再用/明确残余限制”的闭环筛选；单纯提到丹药、疗伤或事后一句“痊愈”的段落不会入选。已完成跨早中后期的回读，最终保留 14 个窗口；其中包含“恢复后立即重返战斗/位置”的正例，也保留了断臂不可复原、伤好而人未醒、药力混杂反而加重等边界，避免把恢复误写成自动满状态。# Source

- 《斗破苍穹》
- 本地 TXT：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\小说整理合集\01_玄幻\斗破苍穹.txt`
- 以 GB18030 解码并按 `splitlines()` 计行；共 85,927 行、1,646 章。

# Research Question

疗伤、力量恢复、残损修复与重返战斗如何被写成有状态变化的场景；尤其关注恢复层级、时间压缩、药物/身体反馈、第一次重新使用能力，以及“恢复不等于自动完全”。

# Evidence Windows

## recovery_doupo_01

- **Evidence：**第230章《修补与强化》，L11661–11704。
- **Scene posture/type：**濒死后的内部修补。
- **Scene goal：**让已经炼化的力量从“没杀死他”变为“重新可用”。
- **Pre-state：**经脉扭曲、骨骼与肌肉受损，储能近乎见底。
- **Expanded beats：**新力量先沿受损经脉流动，再修补经脉、骨骼、肌肉与皮肤；随后补回能量储备；主角苏醒后完成最后收纳动作。
- **Compressed/omitted beats：**重复修复过程不逐段计时。
- **State-changing exchange：**无对白交易；“修补完成”由能量重新可储存、主角能完成最终控制来确认。
- **Other-character reaction：**旁观者从紧张转为确认成功。
- **Body/space/detail selection：**只选经脉、骨骼、皮肤裂口、空掉的储能核心。
- **Ruler/reader model：**恢复不是外伤消失，而是“传导—承载—调用”重新闭环。
- **Stop point：**能力被正式收纳后停止，不再重复描述皮肤恢复。
- **Interpretation / transfer observation：**若损伤同时阻断身体与能力，先让读者看见功能部件恢复，再给第一次主动调用。
- **Anti-inference：**不能推出所有重伤都应附带强化；本窗口的强化依赖特殊力量及其既有设定。

## recovery_doupo_02

- **Evidence：**第238–240章《深藏不露》《破解封印》《残图到手，聘请保镖》，L12034–12184。
- **Scene posture/type：**解除长期封印后的力量归还。
- **Scene goal：**验证药物能否解除封印，并决定恢复者是否履约。
- **Pre-state：**恢复者长期被封印，无法动用原有实力；药方首次尝试曾失败。
- **Expanded beats：**重新炼成药物→吞服后两股力量对抗→封印离体→气势回归→恢复者立刻重新评估关系。
- **Compressed/omitted beats：**炼制中没有新判断的常规火候被压缩。
- **State-changing exchange：**恢复者先显露强势与反悔可能，随后因对方仍具威慑而兑现报酬，并接受后续协作。
- **Other-character reaction：**狂喜、试探、克制，三次变化都由恢复后的力量重新定价触发。
- **Body/space/detail selection：**额前封印、冰室、能量冲击与裂开的冰层。
- **Ruler/reader model：**力量是否真正回来，不靠宣告，而靠它立刻改变谁能威胁谁、谁必须履约。
- **Stop point：**恢复后的新行动关系成立，转入新的目标。
- **Interpretation / transfer observation：**适用于“恢复会改变谈判筹码”的戏；第一次展示可由关系重估替代打一架。
- **Anti-inference：**不代表每次恢复后都要安排背叛试探；此处成立于双方原本就有交换张力。

## recovery_doupo_03

- **Evidence：**第263–265章《药老沉睡》《依靠自己》《休养与控火能力》，L13490–13606。
- **Scene posture/type：**严重创伤后的分层休养与有限复工。
- **Scene goal：**在失去保护者后，恢复到能自救、能维持关系与能继续做事。
- **Pre-state：**五日昏迷；经脉近乎残破；仅剩少量能量；关键保护者进入沉睡。
- **Expanded beats：**先用温和药物恢复一点力气→筹药并连续药浴三日→确认经脉能承受运转→恢复炼药与控火练习。
- **Compressed/omitted beats：**后续按既定程序的日常调养，压缩为“预计一月回到原状态”。
- **State-changing exchange：**主角用尚未完全恢复的能力安排药材与承诺，换取盟友继续保护。
- **Other-character reaction：**亲人因其苏醒而放松；盟友因未来收益与信任继续站队。
- **Body/space/detail selection：**脆弱经脉、药液褪色、运气时的抽痛、药鼎中的火焰。
- **Ruler/reader model：**恢复至少分为“醒来”“能运转”“能工作”“回到旧峰值”四层。
- **Stop point：**新能力已经能在炼药中被实际使用，但“完全恢复”仍留在未来。
- **Interpretation / transfer observation：**很适合主角不能停在床上的长篇：让第一次复工既证明恢复，也推进外部资源线。
- **Anti-inference：**不能将“能炼药”误认成“可承受战斗”；文本明确仍需约一月回归旧状态。

## recovery_doupo_04

- **Evidence：**第579–580章《养伤》《实力晋升》，L29500–29562。
- **Scene posture/type：**战后静养转化为恢复后的跃迁。
- **Scene goal：**把油尽灯枯后的存活，转成可见的阶段变化。
- **Pre-state：**大战后斗气耗尽、伤势极重，连续修炼数日未醒。
- **Expanded beats：**同伴先判断伤势与异常波动→第五日气息上升→醒来、排出浊气、活动身体→揭示体内残余药力参与恢复。
- **Compressed/omitted beats：**数日无新反馈的打坐。
- **State-changing exchange：**没有对手互动；同伴先担忧后确认其不仅没留暗伤，还跨过层级。
- **Other-character reaction：**守护者的判断先于主角自述，给读者外部标尺。
- **Body/space/detail selection：**苍白转红润、浊气、体内残余药力、骨节响动。
- **Ruler/reader model：**恢复中的升级必须先有“伤势已处理”的证据，再显示新增幅度；仍可留下另一种旧问题。
- **Stop point：**身体动作确认状态后即转出。
- **Interpretation / transfer observation：**适用于既有储备在极限消耗后被释放的情形。
- **Anti-inference：**不是“重伤必升级”；本章明确依赖此前积累的药力和极限战斗。

## recovery_doupo_05

- **Evidence：**第613章《缓慢的蜕变》，L31191–31231。
- **Scene posture/type：**失去主动性的濒死修复。
- **Scene goal：**保持“可能活下来”的悬念，而非立即兑现回归。
- **Pre-state：**肉体、经脉、器官濒临毁灭，意识进入假死。
- **Expanded beats：**破坏力量持续焚烧；偶然形成的药液持续修复；两者反复拉锯。
- **Compressed/omitted beats：**不计算每次拉锯，不给确定恢复时长。
- **State-changing exchange：**无人物交涉；唯一交换是破坏与修补的相互抵消。
- **Other-character reaction：**无有效旁观者判断，避免过早确认结果。
- **Body/space/detail selection：**血液、经脉、骨骼、伤口与药液流入路径。
- **Ruler/reader model：**当人物不能行动时，读者追问应是“修复能否压过损坏”，不是“他何时满血”。
- **Stop point：**停在“可能数月、数年”的未知，保留后续回归价值。
- **Interpretation / transfer observation：**适用于需要把恢复本身保持为悬念的灾难后段。
- **Anti-inference：**此处的偶然药液组合不可转成通用解决方案，更不能把巧合当角色可复制的策略。

## recovery_doupo_06

- **Evidence：**第700章《治疗》，L35399–35417。
- **Scene posture/type：**战前修复盟友战力。
- **Scene goal：**修复旧创伤，使一名关键战力能参与即将到来的决战。
- **Pre-state：**目标长期留有外伤与萎靡气息，无法恢复旧峰值。
- **Expanded beats：**药力被火焰展开→目标痛苦挣扎→外伤愈合→气息上升→药力耗尽后确认仍需休息。
- **Compressed/omitted beats：**无新增反馈的后续休养。
- **State-changing exchange：**治疗者不收即时报酬，要求对方在两日后的大战投入力量。
- **Other-character reaction：**守护者从焦急到激动；被治者以长啸展示恢复。
- **Body/space/detail selection：**旧伤、萎靡气息、湖面波动、药力缩减。
- **Ruler/reader model：**恢复的价值用“能否赶上下一场不可替代的事”衡量。
- **Stop point：**“大部痊愈、休息后到峰值”已足够，立刻转入战前局势。
- **Interpretation / transfer observation：**治疗戏可成为盟约兑现，而不是独立的医疗展示。
- **Anti-inference：**不代表所有盟友治疗都必须附政治交换；本章由决战临近决定其必要性。

## recovery_doupo_07

- **Evidence：**第725–726章《形势》《宗门大会》，L36654–36697。
- **Scene posture/type：**胜利后的残余伤状态。
- **Scene goal：**阻止大胜把人物写成无代价满状态。
- **Pre-state：**斗气、灵魂、手臂同时受损。
- **Expanded beats：**半月后可出面，但本人明确只“勉强治愈”；旁人看出接近新门槛；新的危机信息马上进入。
- **Compressed/omitted beats：**半月疗伤具体流程。
- **State-changing exchange：**家人劝其不要急于彻底回归，主角却必须开始处理新威胁。
- **Other-character reaction：**盟友惊讶其恢复速度，但其惊讶没有抹掉未回峰值的事实。
- **Body/space/detail selection：**苍白脸色、断臂、气息起伏。
- **Ruler/reader model：**“能见人、能决策”与“能全力战斗”是不同恢复层。
- **Stop point：**新威胁被提出，恢复戏不再滞留。
- **Interpretation / transfer observation：**适用于战后主角必须重新接管事务、但不能无伤进入下一战。
- **Anti-inference：**不能把“已可行动”写成“可立即高强度再战”。

## recovery_doupo_08

- **Evidence：**第944–950章《韩冲》至《洪家》，L46718–47007。
- **Scene posture/type：**陌生地域中的受限自救。
- **Scene goal：**从“死在荒野的风险”恢复到最基本的行动与自保。
- **Pre-state：**空间冲击后躺倒近一日，不能站立，身处陌生且有野兽风险的环境。
- **Expanded beats：**先吞药、只争取一缕斗气→被外人救入车队→一天后可走路→数日调养恢复七八成→仍主动索取药材，为三日内回峰值准备。
- **Compressed/omitted beats：**车队行路与无变化的调息。
- **State-changing exchange：**外人提供庇护与基础药物；主角不夸耀实力，只把恢复变成当下的生存优先级。
- **Other-character reaction：**救助者由“他活不下来”转为惊讶其能走；仍提醒后遗症风险。
- **Body/space/detail selection：**沙漠、微弱呼吸、颠簸带来的疼、踉跄却站稳。
- **Ruler/reader model：**第一步不是恢复战力，而是把“不能动”变成“能活过下一天”。
- **Stop point：**明确三日恢复目标与所需药材后，转入外部冲突。
- **Interpretation / transfer observation：**适合把恢复嵌入陌生环境的生存压力中。
- **Anti-inference：**七八成恢复不等于安全；文本仍保留药材、期限与陌生地域三个约束。

## recovery_doupo_09

- **Evidence：**第1073–1074章《疗伤》《天毒蝎龙兽踪迹》，L53443–53531。
- **Scene posture/type：**先解除阻断性伤害，再处理普通损伤。
- **Scene goal：**驱逐持续冻结身体的特殊劲力，使后续疗伤终于有效。
- **Pre-state：**目标体内多处受伤，且隐性寒劲持续侵蚀血液与经脉；单纯休养无效。
- **Expanded beats：**探查找不到伤源→判断其特性→配火性药浴→痛感与双向寒热反应→多日、近百种药材后逼出寒劲→再给出两三日恢复旧峰值的药物方案。
- **Compressed/omitted beats：**四日内重复换药，仅以“材料增加、状态推进”概述。
- **State-changing exchange：**治疗完成后，双方把“先养伤”明确接到下一项高风险目标。
- **Other-character reaction：**旁观者先见脸色转红润而确认有效；受治者信任后续方案。
- **Body/space/detail selection：**寒气排出、脸色、药浴水色、热与冷同时出现。
- **Ruler/reader model：**先解决那个会让所有普通疗法失效的核心阻断，再谈恢复速度。
- **Stop point：**特殊伤害离体、后续恢复期限明确，转入下一目标。
- **Interpretation / transfer observation：**复杂伤势不应靠“加大药量”；要先找出改变治疗逻辑的异常机制。
- **Anti-inference：**本章并未让角色彻底解决长期体质问题；它只解决了本次可定位的寒劲与创伤。

## recovery_doupo_10

- **Evidence：**第1226–1230章《重伤》至《苏醒》，L62114–62340。
- **Scene posture/type：**长期昏迷恢复与延迟重返。
- **Scene goal：**把一次近乎致命的代价延伸为整个势力的等待与重组，而不是一句跳过。
- **Pre-state：**重击本应断绝生机；仅靠体质与火焰守住性命。
- **Expanded beats：**封闭山门保护治疗→两月、三月、半年、一年依次压缩→脸色与呼吸先恢复→伤势已愈但人仍不醒→苏醒征兆引起全体反应。
- **Compressed/omitted beats：**平稳期只以季节、势力变化和身体外观的节点展示。
- **State-changing exchange：**外部群体为其停留、结盟、调整防御；主角尚不能回应。
- **Other-character reaction：**从守候、担忧到全山被苏醒异动惊动。
- **Body/space/detail selection：**石塔、火焰、生机、由苍白转红润的脸色、手指微动。
- **Ruler/reader model：**“伤势痊愈”不等于“人物已回来”；意识、行动权与社会位置可各自滞后。
- **Stop point：**强烈苏醒信号出现后转入回归展示。
- **Interpretation / transfer observation：**长时间压缩必须让外部世界发生可见变化，否则只是删掉代价。
- **Anti-inference：**不能把一年休养机械复制为“养伤必升级”；本窗口另有既存资源与突破条件。

## recovery_doupo_11

- **Evidence：**第1272、1274、1282章《天阶斗技》《完美躯体》《药圣，药尘》，L64700–64816、L65265–65329。
- **Scene posture/type：**灵魂、骨骼、精血与药物共同完成的身体重建。
- **Scene goal：**让失去肉身的强者重新拥有可承担旧实力的身体。
- **Pre-state：**灵魂本源已补回，但没有合适躯体就不能恢复原有层级。
- **Expanded beats：**先确认本源恢复→摆出骨骼、精血、丹药三类材料→明确“可回旧峰值但更高层未知”→封闭重建→新身体在敌方袭击中以实战展示结果。
- **Compressed/omitted beats：**封闭炼制与融合过程本身不逐步直播。
- **State-changing exchange：**恢复后的首次行动不是报数，而是单手停住敌方杀招、迫使敌方撤退。
- **Other-character reaction：**敌人从预判“恢复峰值已很难”变为震骇；己方立即将其视为势力级转折。
- **Body/space/detail selection：**骨骼等级、精血品质、封闭石塔、恢复者伸手的动作。
- **Ruler/reader model：**重建身体要同时满足“能承载什么”“能否马上在压力下证明什么”。
- **Stop point：**首个不可逆的战场结果出现，恢复已被证实。
- **Interpretation / transfer observation：**对于大修复，第一次再用最好改变当前危机的力量结构，而不只是恢复者说自己回来了。
- **Anti-inference：**本窗口的超额突破被文本明确当作意外；不可将“换身体”普遍写成必然越级。

## recovery_doupo_12

- **Evidence：**第1344–1345章《追逃》《九星能量体》，L68838–68868。
- **Scene posture/type：**反例：可疗伤，不可复原的残损。
- **Scene goal：**保留敌方威胁，同时确认其永久战损改变了之后的战力结构。
- **Pre-state：**角色断臂、脸色苍白，只能借环境能量疗伤。
- **Expanded beats：**先用环境资源稳定伤势→十余日后恢复一般伤势→明确断臂无法复原、战力下降。
- **Compressed/omitted beats：**十余日的具体吸收过程。
- **State-changing exchange：**同伴要求先养伤、避开强敌；追击方以其战损评估可用战力。
- **Other-character reaction：**双方都不再把他当成原先完整战力。
- **Body/space/detail selection：**独臂、苍白脸色、可吸收的能量环境。
- **Ruler/reader model：**恢复应精确到部位与功能；“伤好了”不覆盖永久损失。
- **Stop point：**永久边界一经确认，即转向下一轮追逐。
- **Interpretation / transfer observation：**若要让伤势留下长期后果，必须让之后的战术、关系或评价真的随之改变。
- **Anti-inference：**这不是说每次重伤都该致残；它是针对已经明确失去身体部位的情形。

## recovery_doupo_13

- **Evidence：**第1481–1482章《大战落幕》《二星斗圣！！》，L76372–76444。
- **Scene posture/type：**战后先修补、后转化的延迟型恢复。
- **Scene goal：**先确认两名胜者都无法继续硬撑，再让恢复成为下一阶段变化的入口。
- **Pre-state：**一人消耗超出单纯斗气层面；另一人经脉损坏、接近无法行动。
- **Expanded beats：**先服药与搀扶→明确敌方即使治疗也会战力下降→主角闭关十日，伤势逐步愈合→特殊血脉持续洗刷身体→三个月后才显出突破。
- **Compressed/omitted beats：**十日后到百日之间的重复洗刷，只保留时间与气息节点。
- **State-changing exchange：**战后指挥先决定敌方残损将改变战争节奏；主角自身随后退出现场修养。
- **Other-character reaction：**同伴担忧三个月无动静，最终从担忧转为确认其进入突破。
- **Body/space/detail selection：**经脉抽痛、被搀扶、心脏血脉、皮肤颜色变化。
- **Ruler/reader model：**先把“恢复到能活、能站”与“后续突破”分成两个节拍。
- **Stop point：**他从治疗状态明确转入突破状态。
- **Interpretation / transfer observation：**大收益可从恢复中长出，但应先让原有创伤结算完成，再切换为 advancement。
- **Anti-inference：**不能把三个月闭关直接等同于疗伤；后段的主要问题已经变成力量跃迁。

# Cross-Window Findings

1. **恢复至少要区分伤势、能量、能力调用、意识/行动权与社会位置；它们不会同步归零。**
   支持：`recovery_doupo_01`、`03`、`07`、`08`、`10`、`12`。

2. **先找“使普通治疗无效”的核心阻断，再写一般疗伤；否则药物只是重复消耗。**
   支持：`recovery_doupo_02`（封印）、`09`（寒劲）、`11`（无躯体）、`12`（断臂边界）。

3. **可压缩的是重复过程，不是恢复判断。每次展开都要带来新诊断、功能回归、时间尺度变化或新选择。**
   支持：`recovery_doupo_03`、`04`、`08`、`10`、`13`。

4. **第一次重新使用能力应证明新的行动空间，而非重复一句“恢复了”。它可以是实战、履约、复工、部署或重新承担责任。**
   支持：`recovery_doupo_01`、`02`、`03`、`06`、`11`。

5. **“恢复不自动完全”应留下能改变后续决策的残余，而不是装饰性的疼痛。**
   支持：`recovery_doupo_03`、`07`、`08`、`10`；反证边界：`recovery_doupo_12`。

6. **恢复与突破可以相连，但必须先完成恢复的可观察结算，再切换到突破场景。**
   支持：`recovery_doupo_04`、`10`、`13`；反证：`recovery_doupo_03`、`07`。

# Counterexamples & Boundaries

- **永久残损不被普通恢复抹平。**断臂角色能借环境恢复伤势，但断臂不可复原，战力随之下降：`recovery_doupo_12`。
- **伤势痊愈不等于人物归来。**第1229章已明确身体状况比旧峰值更好，但人物仍未苏醒：`recovery_doupo_10`。
- **恢复后仍可能不能全力战斗。**半月治疗后仅勉强治愈，旧峰值另需时间：`recovery_doupo_07`。
- **特殊恢复不能被泛化为标准配方。**濒死药液拉锯来自意外组合，文本本身不给可控复现路径：`recovery_doupo_05`。
- **当核心问题已切换为突破时，不应继续按疗伤戏写。**第580、1229、1482章后段的主问题均已转为跃迁：`recovery_doupo_04`、`10`、`13`。

# What Existing Skill Misses

现有 `recovery_restoration` 已覆盖具体缺损、有效处理、首次功能回归与时间压缩。新增判断能力应是：

1. **恢复层级图。**区分“伤口”“能量”“调用能力”“意识/行动权”“社会位置”，避免用单一“恢复了”覆盖不同状态。
2. **核心阻断诊断。**先判断是否存在封印、异劲、无躯体、永久残损等使常规疗法无效的结构性问题。
3. **压缩的锚点。**时间跳跃必须留下身体、关系、世界或行动空间的变化节点；不能只写“数日后痊愈”。
4. **首次再用的场景选择。**恢复后的验证不必总是战斗，可是履约、生产、接管事务、获得保护或改变他人风险判断。
5. **残余限制的后续义务。**若保留未满状态，必须让它约束下一步；否则属于假代价。
6. **恢复→突破的切场规则。**当读者主要追问已变成“能跨到哪里”，应停止继续堆治疗反馈，转给 `breakthrough_advancement`。

# Candidate Transfer Rules

1. **分层确诊规则**
   - Applicability：人物同时有身体伤、能量空缺或行动失能。
   - Rule：先明确本场只解决哪一层，并让每个治疗动作对应那一层的可见反馈。
   - Stop rule：目标层已通过动作确认后停止；未解决层作为下一步约束。
   - Failure pattern：把止血、回气、醒来、恢复旧实力写成同一句。

2. **核心阻断优先规则**
   - Applicability：休养或普通药物不能解释为何角色仍无法恢复。
   - Rule：先暴露并处理封印、异物、异常力量、承载条件或永久残损。
   - Stop rule：阻断解除且后续普通恢复已有明确路径。
   - Failure pattern：不断换药、加痛感，却没有改变恢复逻辑。

3. **恢复时间压缩规则**
   - Applicability：恢复跨度超过当前场景应承受的重复过程。
   - Rule：只保留“诊断确认、方法有效、功能首次回来、外界因此变化”四类节点。
   - Stop rule：连续时间不再产生新的状态信息时直接跳转。
   - Failure pattern：逐日打坐或反复服药，却没有新的判断或代价。

4. **首次再用规则**
   - Applicability：恢复已达到可行动阈值。
   - Rule：选择最能改变当前行动空间的一次使用：逃生、履约、生产、保护、谈判或出手。
   - Stop rule：他人与局势已据此重新估价。
   - Failure pattern：角色起身说“我好了”，但后续所有人仍按旧状态行动。

5. **残余限制兑现规则**
   - Applicability：恢复不是完全，或作者需要保留代价。
   - Rule：残余限制必须影响下一次目标、风险或角色选择。
   - Stop rule：限制已在一次后续行动中实际造成成本，或被新的明确机制解除。
   - Failure pattern：只留一句“尚未痊愈”，下一场却全力无损作战。

6. **恢复与跃迁分场规则**
   - Applicability：恢复过程中积累的新资源开始主导读者期待。
   - Rule：先用一个可观察动作结算“原缺损已恢复到何层”，再转入突破场景。
   - Stop rule：读者主要问题从“能不能回来”变成“会到什么高度”。
   - Failure pattern：在同一节拍里把伤势、升级、战斗力、社会反馈全部一次性报完。

# Source Fidelity Audit

以下候选未纳入 Evidence Windows：

- 第132章《旖旎的疗伤》：未在本次最终复核中取得足够完整的机制窗口与可靠行段，排除。
- 第656章《修复药液》：主要是为灵魂修复准备材料，不是恢复实际发生并被验证的场景，排除。
- 第876章《三千焱炎火》：是能力说明，不是已发生的恢复场景，排除。
- 第1118章《苦修炼丹》：是消耗型恢复药物的说明，缺少人物受损、处理与结果闭环，排除。
- 第1509章《抢妖火本源！》：只给出临战“恢复伤势/斗气”的指令，缺少完成反馈与重返行动闭环，排除。
- 第1632章《失手》：瞬间痊愈服务于反派局势翻转，未形成可供本研究拆解的恢复层级与过程窗口，排除。

本报告未把上述排除项补为“弱证据”，也未用书外记忆补章节机制。
