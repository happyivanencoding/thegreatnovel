我会按 source-first 流程做：先读取现有 Scene Skill 的判断边界与记忆索引，再以 GB18030 解码整本《将夜》、跨段筛选可复核场景，最后输出带行号的 Markdown 证据稿；不把推断写成原文事实。我已按原著阶段并行分配只读取证；主线程会核对现有 `trial_challenge`、`training_learning`、`showcase_evaluation` 的边界，并独立建立全书章节—行号索引，避免把“考核”名词误判成有效场景。这项任务也匹配 `distill-novels`：它要求来源文本、定位器与可迁移边界分离。我会用它的证据规范约束整理，不会使用其来改写或仿写原著。当前工作树已有大量与本任务无关的未提交修改；我只读源 TXT 和 Scene Skill，不会触碰这些文件。已确认源文本共 86,127 行，章节标题在分卷处重置；下文会以“卷内章节名 + source line”作为唯一定位，不假装全书连续章号。我会把“同一段登山”拆成不同的状态交换（报名、公开规则、观察后入场、选择题、判定后的制度争执），但不会把连续的纯体力攀登拆成多条证据来凑数量；其余窗口将从入学、修行门槛、惩罚性闭关和外部宗门规则中补齐。# Source

- `SOURCE_BOOK`：`将夜`
- `SOURCE_PATH`：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\小说整理合集\01_玄幻\将夜.txt`
- `SOURCE_ID`：`trial_jiangye`
- 核对方式：`read_bytes().decode("gb18030").splitlines()`，以下均为 1-based source line。
- 边界：只将原著作为 `REFERENCE_ONLY` evidence；不迁移专名、情节或作者句式。

# Research Question

书院、修行与制度性门槛如何先成为真实障碍；人物如何以已建立的资源和选择跨越；考核何时推动状态变化，何时仅是资格税。

# Evidence Windows

## JY-E01｜入院资格并非军部回执

- **章节 / locator**：第一卷第四章《非典型唐人的前路探讨》；`264–285`
- **anchor**：`跑三个部堂去盖章`
- **Evidence**
  - **scene posture/type**：军营中的制度通路谈判。
  - **scene goal**：宁缺评估护送公主的风险，是否值得换取书院入口。
  - **pre-state**：已有军功、推荐函和回执，但回执仅代表可参加考试。
  - **expanded beats**：将军说明部堂、官阶与人情仍会卡住资格；宁缺算“拿命换资格”的账；得知队伍有修行者后重新衡量。
  - **compressed/omitted beats**：未展开部堂逐项办理，也未在本窗结算是否成行。
  - **state-changing exchange**：表面“已有回执”被改写为“仍缺真正通路”；修行机会使护送的价格发生变化。
  - **opponent/other-character reaction**：将军不耐烦地催促；宁缺由低头盘算转为抬头追问。
  - **body/space/detail selection**：泥地、鞋跟、低头、窗外星光，承载计算过程。
  - **ruler/reader model**：资格要先显示为资源、层级和风险的组合价格。
  - **stop point**：停在未决选择，不假装资格已到手。
- **Interpretation**
  - **transfer observation**：制度说明只有重定价人物下一步时才是戏。
  - **anti-inference**：不能推出所有考生都要走关系，或宁缺已决定接受护送。

## JY-E02｜盖章之后，门槛转成现金与德行

- **章节 / locator**：第一卷第三十一、三十二章《一文钱难死主仆俩》；`1478–1545`
- **anchor**：`三部盖章确认`
- **Evidence**
  - **scene posture/type**：行政准入后的生存门槛。
  - **scene goal**：取得准试凭证，并解决备考期间的食宿成本。
  - **pre-state**：公主照应令其未遭刁难；宁缺和桑桑现金有限。
  - **expanded beats**：三部盖章被压缩完成；书院食宿费用立刻构成新障碍；混帮派挣钱又受德行考察限制；二人转向卖字。
  - **compressed/omitted beats**：无逐个官员冲突，无制度制定史。
  - **state-changing exchange**：`能否参加` 变成 `能否负担且不触犯下一层规则`。
  - **opponent/other-character reaction**：路人轻视其不懂行情；桑桑算账；宁缺接受原本抗拒的卖字方案。
  - **body/space/detail selection**：汗、雨檐、水花、扳手指数银两、雨地写字。
  - **ruler/reader model**：手续本身不够；它必须导向可执行的下一道资源约束。
  - **stop point**：卖字路线成立即停，不提前写成录取。
- **Interpretation**
  - **transfer observation**：行政门槛后接一个会迫使人物选路的下游瓶颈。
  - **anti-inference**：文本明确官府并未敲诈；收费也不自动等于反派。

## JY-E03｜多科累计分数：先承认自己的得分路径

- **章节 / locator**：第一卷第七十三至七十五章《那年春，我把桃花切一斤》；`3276–3348`
- **anchor**：`不打算当白卷英雄`
- **Evidence**
  - **scene posture/type**：正式入院试的评分结构。
  - **scene goal**：宁缺在文科弱势下守住总分希望。
  - **pre-state**：六科累计；他只真正把握射、御，数科亦有优势。
  - **expanded beats**：数科迅速作答；礼、书仍写满试卷；乐科放弃；阅卷者识破漂亮字迹掩不住空泛内容；后续压力集中到射御。
  - **compressed/omitted beats**：题卷全文、精确权重、最终分数均未展开。
  - **state-changing exchange**：文科评分把他的可行路线压缩为后续身体项目。
  - **opponent/other-character reaction**：考生哀叹题难；教习先看字、后按内容判低分。
  - **body/space/detail selection**：考场、墨、卷面、围案阅卷。
  - **ruler/reader model**：读者应先知道总分结构，再理解人物为何放弃某项、押注某项。
  - **stop point**：文试劣势形成即停。
- **Interpretation**
  - **transfer observation**：多技能考核里，强项、弱项、补救空间须在动作前可见。
  - **anti-inference**：漂亮外观不能替代达标内容；本窗恰为反例。

## JY-E04｜边塞技能被制度识别

- **章节 / locator**：第一卷第七十五、七十六章《那年春，我把桃花切一斤》《黑色闪电以及弓弦的奏鸣》；`3349–3426`
- **anchor**：`大黑子，对我好点儿`
- **Evidence**
  - **scene posture/type**：骑射考核中的能力转译。
  - **scene goal**：用射御弥补文科失分。
  - **pre-state**：随机分马，烈马已使多人受伤。
  - **expanded beats**：宁缺判断驯马耗时，改用既有杀伐经验压住黑马；稳定完成骑行和射击；军官由旁观转为招揽。
  - **compressed/omitted beats**：不列全科分数或录取线。
  - **state-changing exchange**：过去的边塞生存技能变成考试中可读的高分证据。
  - **opponent/other-character reaction**：黑马由抗拒转为服从；考生追问；军官重估其价值。
  - **body/space/detail selection**：缰绳、额汗、箭靶、扳指、弓弦节奏。
  - **ruler/reader model**：考核成为故事，前提是考项真正匹配人物已建立的能力。
  - **stop point**：现场评价改变即可停，不把榜单直接写成终局。
- **Interpretation**
  - **transfer observation**：让既有劳动、习惯或生存技能进入一个公平可见的制度场。
  - **anti-inference**：不是“主角气场”通吃；技能与项目必须具体匹配。

## JY-MID-01｜开放藏书，不等于有能力读取

- **章节 / locator**：第一卷第八十二至八十四章《旧书楼》《且劈书山第一刀》《春已浓，人将残，书如故》；`3676–3832`
- **anchor**：`把山劈开`
- **Evidence**
  - **scene posture/type**：知识资源开放后的身体性门槛。
  - **scene goal**：宁缺决定是否继续承受修行书反噬。
  - **pre-state**：他已入书院，却无修行潜质；书可看，内容却不可承受。
  - **expanded beats**：规则说明；首次昏厥；调整饮食和身体后再入；连续失败被压缩；他仍继续上楼。
  - **compressed/omitted beats**：第三至第六日不逐次重演，只保留损耗和旁观反应。
  - **state-changing exchange**：教习提出退出理由；桑桑把障碍重述为需要面对的“山”；宁缺选择继续。
  - **opponent/other-character reaction**：女教授从观察转为劝止；同窗由嘲弄转为不理解的敬佩。
  - **body/space/detail selection**：二楼、书架、楼梯、眩晕、白沫、越来越虚浮的脚步。
  - **ruler/reader model**：重复尝试必须每次都留下成本或新信息，否则是资格税。
  - **stop point**：停在继续选择，不给即时突破。
- **Interpretation**
  - **transfer observation**：硬门槛应同时给出身体代价、退出选项和旁观者误读。
  - **anti-inference**：不能推出坚持必然得到资质；原文后续仍依赖特殊条件与新方法。

## JY-MID-02｜期考作为资格税的反例

- **章节 / locator**：第一卷第一百一十九、二十章《被遗忘的期考》《自幼杀蛮，故蛮不讲理》；`5586–5673`
- **anchor**：`问题就在于你请了假`
- **Evidence**
  - **scene posture/type**：考试余波中的共同体审判。
  - **scene goal**：呈现缺考如何被解释为怯懦。
  - **pre-state**：宁缺因重伤昏迷缺考，真实代价远高于校园考场。
  - **expanded beats**：异样目光；友人解释“参加”本身的共同体意义；同窗公开追问；宁缺承认赌局失败，却拒绝接受懦夫标签。
  - **compressed/omitted beats**：考题、答卷、评分被完全压缩。
  - **state-changing exchange**：制度只读取“缺席”，不能读取其真实经历；社会身份因此受损。
  - **opponent/other-character reaction**：谢承运凭成绩获声望；钟大俊借规则羞辱；友人相信他却无力扭转舆论。
  - **body/space/detail selection**：书舍目光、拦门者、长廊离场。
  - **ruler/reader model**：若考核只改变标签而不测它声称测量之物，它是资格税；但资格税仍会制造关系成本。
  - **stop point**：不替他正名，保留隔膜。
- **Interpretation**
  - **transfer observation**：同时写清“制度实际测了什么”与“共同体声称它测了什么”。
  - **anti-inference**：不代表所有考试无意义；同书中成绩确实会改变声望与机会预期。

## JY-MID-03｜不取消规则，只重编码读取方式

- **章节 / locator**：第一卷第一百二十八章《书院里的天才们》；`6047–6068`，后续抄本 `6140–6148`
- **anchor**：`只有洞玄上品`
- **Evidence**
  - **scene posture/type**：修行知识门槛与局部绕行。
  - **scene goal**：把“看不懂修行书”转成可实验的问题。
  - **pre-state**：规则要求洞玄上品才可直接读懂；宁缺已能感知，却不达标准。
  - **expanded beats**：陈皮皮解释机制；提出永字八法拆形、离楼重组的可能；明确不保证成功；宁缺立刻测试烛火与银锭。
  - **compressed/omitted beats**：长期训练与抄本过程不展开。
  - **state-changing exchange**：资格门槛仍在，但他以已有书法能力改变输入方式。
  - **opponent/other-character reaction**：陈皮皮先判烛火控制弱，后承认银锭反应异常。
  - **body/space/detail selection**：深夜旧书楼、烛火、银锭、眉心发闷。
  - **ruler/reader model**：绕行必须保留不确定性、实验成本和失败反馈。
  - **stop point**：局部反应成立即停，不升级为掌握功法。
- **Interpretation**
  - **transfer observation**：让人物改变读取规则的方式，而不是让世界规则突然失效。
  - **anti-inference**：不能泛化为创意必能跨境界；此法依赖角色既有专长和特定结构。

## JY-MID-04｜公开考核先把人放进同一把尺

- **章节 / locator**：第一卷第一百四十九至一百五十二章《开楼》《登山》《起步》《十四年，去年夏天，今日拾阶》；`7263–7575`
- **anchor**：`因为我想登山`
- **Evidence**
  - **scene posture/type**：二层楼公开资格试的起步。
  - **scene goal**：宁缺将个人愿望提交到公共判定。
  - **pre-state**：只招一人；隆庆等人被默认有资格，宁缺被视为局外人。
  - **expanded beats**：替代机会出现；他仍选择参加；规则公布；迟到入场；第一步剧痛；再度踩上山道；身体逐步适应。
  - **compressed/omitted beats**：其他登山者的大量失败压缩为速度、昏迷和结果。
  - **state-changing exchange**：教授以“想登山”认可其参赛资格；宁缺从被围观者变成竞争者。
  - **opponent/other-character reaction**：嘲讽、担忧、重新建立的唐人信心并存；隆庆仍未将他当对手。
  - **body/space/detail selection**：石径、脚掌针痛、竹叶无形割伤、雾山。
  - **ruler/reader model**：公开规则的价值在于同一环境下的不同身体反馈。
  - **stop point**：止于能继续，不提前写成获胜。
- **Interpretation**
  - **transfer observation**：先让读者看见所有人服从同一规则，再显示个体训练如何改变承受方式。
  - **anti-inference**：不是意志万能；文本将其适应性落在长期细微训练与特殊念力上。

## JY-MID-05｜阵法门允许的不是捷径，而是另一种操作

- **章节 / locator**：第一卷第一百五十四章《银道与柴门，入雾》；`7835–7998`
- **anchor**：`君子不器`
- **Evidence**
  - **scene posture/type**：循环阵法与文字门。
  - **scene goal**：低境界的宁缺通过山道与柴门。
  - **pre-state**：常规路径要求速度、高境界或更强感知；他均不占优。
  - **expanded beats**：发现回到原点；分析阵法；选取微弱而精细的控制；银箔试路；记忆受阻；挖石失败；掌心留字后补全柴门。
  - **compressed/omitted beats**：其他登山者的多次尝试被压缩；先前半年训练以少量生活物件带过。
  - **state-changing exchange**：谢承运说“过不去”；宁缺转向测试机制而非争辩；柴门打开。
  - **opponent/other-character reaction**：谢承运由轻蔑转为震惊；山顶观察者承认方法别出心裁。
  - **body/space/detail selection**：桥、重复石径、银箔、蹲伏、掌心红印、柴门烟气。
  - **ruler/reader model**：有效解题不是取消规则，而是用规则容许、却无人优先想到的操作。
  - **stop point**：柴门开、浓雾仍在。
- **Interpretation**
  - **transfer observation**：门槛应先失败、再显机制、再由旧能力组合出有代价的解法。
  - **anti-inference**：弱者并非总能投机胜强者；高境界仍是同一规则下的有效路径。

## JY-MID-06｜心理关用可核对的生活事实，而非口号

- **章节 / locator**：第一卷第一百五十六章《山顶的青树，压烂的糕点，一切都是幻觉……》；`8170–8323`
- **anchor**：`我杀给你们看`
- **Evidence**
  - **scene posture/type**：幻境记忆试炼。
  - **scene goal**：宁缺辨认真相，不让被优化的往事替代现实。
  - **pre-state**：已过阵法与柴门；隆庆境界更高，却同样被幻境阻住。
  - **expanded beats**：过往逐级重现；暴力反应失效；疲惫怀疑；理想化的桑桑出现；她的生活选择与真实习惯矛盾；宁缺据此斩开灰墙。
  - **compressed/omitted beats**：十七年经历以闪回压缩；只展开能改变判断的细节。
  - **state-changing exchange**：对桑桑的具体提问及回答，成为幻境可被证伪的证据。
  - **opponent/other-character reaction**：观察者追问判断依据；隆庆的受阻构成强反例。
  - **body/space/detail selection**：夜雾、湿衣、血、刀、石阶、假墙。
  - **ruler/reader model**：心理门槛要有可复核的关系细节，不能只用“相信自己”。
  - **stop point**：真实山道显现即停。
- **Interpretation**
  - **transfer observation**：重要的价值选择应落在角色长期生活中已建立的小事实。
  - **anti-inference**：不能写成创伤越重越强；高境界、压抑情绪皆不能替代判断。

## JY-P01｜通过不等于制度会立刻承认

- **章节 / locator**：第一卷第一百五十八、五十九章《咔嚓！咔嚓！》《大唐国师很了不起吗？》；`8680–8847`
- **anchor**：`我不服`
- **Evidence**
  - **scene posture/type**：考核结果后的制度争夺。
  - **scene goal**：确认“先登顶者入二层楼”的结果能否落地。
  - **pre-state**：宁缺已先登顶；朝廷、西陵、神符师与书院各有利益。
  - **expanded beats**：外界质疑；规则被重申；颜瑟欲争徒；亲王把压力转成“主动退出”；宁缺不接责任；书院内部仍争论。
  - **compressed/omitted beats**：不重演登山过程。
  - **state-changing exchange**：宁缺从胜者变为各方要交易的资格持有人；他的回话将选择压力抛回机构。
  - **opponent/other-character reaction**：外部不服；公主要求快刀斩乱麻；教授意见分裂。
  - **body/space/detail selection**：书舍争执、冷茶、官员等待、晨光中的宁缺。
  - **ruler/reader model**：结果的“社会承认”是另一场戏，尤其当通过会重分配资源与政治筹码。
  - **stop point**：争议仍在，不把资格写成自动稳定身份。
- **Interpretation**
  - **transfer observation**：重要通过后，可转写为“谁试图重定义结果、谁承担后果”。
  - **anti-inference**：不是所有通过都需政治余波；只有结果会改变多个利益方时适用。

## JY-P02｜惩罚性闭关：禁制先给出不可绕过的代价

- **章节 / locator**：第二卷第一百七十九至一百八十一章《后山的师生和金兰树》《山崖之上望长安》《崖洞囚徒的第一次越狱》；`25554–25717`
- **anchor**：`自由是很珍贵的`
- **Evidence**
  - **scene posture/type**：书院惩罚与修行禁制。
  - **scene goal**：宁缺面对被囚后崖，判断留下、逃离或寻找破关方式。
  - **pre-state**：刚入二层楼，仍珍视书院；自由被收走。
  - **expanded beats**：得知惩罚；本能想逃；明确逃离会失去多年积累；禁制第一次反震；他转向冥想和准备。
  - **compressed/omitted beats**：三月日常并未逐日描写。
  - **state-changing exchange**：夫子将囚禁定为惩罚、磨砺与考验；宁缺在确认无绕路后选择研究禁制。
  - **opponent/other-character reaction**：桑桑担忧；书院同人震惊；禁制以直接反震回答。
  - **body/space/detail selection**：崖壁、洞口、血迹、火把、浓稠元气。
  - **ruler/reader model**：禁制成立须有第一下真实、可感的失败；人物再行动才不是空喊自由。
  - **stop point**：首次越狱失败、方法转向即停。
- **Interpretation**
  - **transfer observation**：囚禁类门槛应把“代价—失败—新研究方向”连接起来。
  - **anti-inference**：不可把受困浪漫化；人物继续留下也与其现实利益和关系绑定。

## JY-L01｜知守观：口诀必须被译成身体操作

- **章节 / locator**：第五卷第三十一、三十二章《七进知守观》《清静的废人》；`64049–64142`
- **anchor**：`七进十三出`
- **Evidence**
  - **scene posture/type**：制度谜门与修行资格门。
  - **scene goal**：隆庆进入关闭的知守观，取得面见观主、继续修行的资格。
  - **pre-state**：只能走正门；触门受威压伤害；留下一句含义未明的提示。
  - **expanded beats**：触门失败；观察后墙、废墟、石阶；隔夜推算；将口诀译为倒退上下阶与倒退七步；入观跪见观主。
  - **compressed/omitted beats**：阵法全貌和多轮试错未逐项展开。
  - **state-changing exchange**：空间动作正确后，失败者转为被允许面见师父的人。
  - **opponent/other-character reaction**：阵法先伤人；师叔平静接纳；观主将更深的门槛转为内心敬畏。
  - **body/space/detail selection**：木门、六级石阶、崩山、鼻眼黑血、跪地。
  - **ruler/reader model**：读者看“动作是否触发空间变化”，不看境界名号。
  - **stop point**：进入后止于认错，不预支原谅或新功法。
- **Interpretation**
  - **transfer observation**：抽象规则可先以一句不完整提示出现，再由失败代价和现场几何让人物译解。
  - **anti-inference**：同窗此前可因改阵绕过，故不能说此门绝对、恒定、不可绕。

## JY-L02｜唐小棠闯桃山：过防线不等于完成救援

- **章节 / locator**：第五卷第四十六至四十九章《有人闯山》至《你想战，那便战（下）》；`64960–65182`
- **anchor**：`连破三关`
- **Evidence**
  - **scene posture/type**：多层防线与战斗型修行考核。
  - **scene goal**：闯至桃山前坪，救出陈皮皮。
  - **pre-state**：她停在洞玄巅峰；外有骑兵、神卫、阵法、高阶修行者。
  - **expanded beats**：突进骑兵；破清光阵；到达前坪；与勒布对战；连续冲锋；对手退步认输；仍无法带走陈皮皮。
  - **compressed/omitted beats**：不逐场描摹所有骑兵交手。
  - **state-changing exchange**：破阵、逼退对手使她取得到达前坪的资格证明，但救援目标未结。
  - **opponent/other-character reaction**：神官从轻蔑到震撼；勒布承认战意但保留实力优势。
  - **body/space/detail selection**：血、兽皮、铁棍、桃花、清光阵、歌声。
  - **ruler/reader model**：每层障碍必须改变判断、身体状态、关系或目标距离。
  - **stop point**：止于“带不走”，不把破境写成万能胜利。
- **Interpretation**
  - **transfer observation**：突破最好来自“必须做成某事”的承受，而非独立奖励动画。
  - **anti-inference**：战意不替代实力；取得一层资格不等于完成更高目标。

## JY-L03｜规则边界越过后，反制仍然有效

- **章节 / locator**：第五卷第七十六、七十七章《颤栗》；核心 `67243–67335`，标题 `67189`、`67279`
- **anchor**：`她的世界的边界`
- **Evidence**
  - **scene posture/type**：世界规则边界与越界选择。
  - **scene goal**：宁缺拒绝继续受控，尝试恢复行动自由。
  - **pre-state**：雪山气海被锁；正面突破空间边界会死。
  - **expanded beats**：重复扫雪压缩为受控生活；情感与臣服谈判；裂缝显出边界；正面不可破；借引力越界；获得短暂自由；规则反制；跳崖。
  - **compressed/omitted beats**：此前受刑和日常劳动只作蒙太奇。
  - **state-changing exchange**：从执行仆役转为公开拒绝；控制者未能预判他的跳崖选择。
  - **opponent/other-character reaction**：裂缝、神殿、人间震动构成规则回应；对方短暂失措后重设压制。
  - **body/space/detail selection**：扫帚、积雪、裂缝、颊伤、栏杆、深渊。
  - **ruler/reader model**：以边界可见性、身体代价和反制是否发生衡量突破。
  - **stop point**：共同坠入深渊，不结算关系或最终胜负。
- **Interpretation**
  - **transfer observation**：规则型门槛可让人物先学习反馈，再用低阶但可调用的规则作有代价选择。
  - **anti-inference**：短暂恢复不等于永久解锁；情感接触也非普遍破规则方案。

# Cross-Window Findings

1. **考核成为故事的最低条件，是规则先造成不可替代的代价，再迫使人物用既有资源作选择。** 单纯“有考试”不够。`JY-E02` 的盖章因为转化为现金与德行限制而成立；`JY-MID-04/05` 以身体、阵法和记忆问题不断改变操作；`JY-L01` 以受伤和空间反馈逼出推理。

2. **人物的跨越不是抽象意志升级，而是旧能力在新规则中的重新定价。** 边塞骑射被译为正式成绩，书法被译为读取方案，微弱念力被译为阵法操作。`JY-E04`、`JY-MID-03`、`JY-MID-05`。

3. **“通过”至少可分为：进入、资格确认、目标完成、社会承认四层；不得自动合并。** 入知守观不等于解决内心门槛；唐小棠破阵不等于救人；二层楼登顶后仍要处理承认与交易。`JY-L01`、`JY-L02`、`JY-P01`。

4. **资格税不一定无戏，但它只在暴露“制度能读取什么、不能读取什么”时有价值。** 期考未能读取宁缺的重伤经历，却真实改变共同体评价；题目和答卷本身被压缩。`JY-MID-02`，反证边界为 `JY-E03–E04`。

5. **重复失败只应展开到反馈发生变化为止。** 旧书楼保留首次昏厥、重新进入和身体恶化，省略中间同质失败；桃山省略多数交手，只保留破阵、公开对峙与对手退步。`JY-MID-01`、`JY-L02`、`JY-L03`。

# Counterexamples & Boundaries

- 行政手续若没有新成本、阻拦者、资源选择或关系变动，应压缩为过场；`JY-E02` 中真正被展开的是费用和谋生，不是盖章。
- 坚持不是成功证明。普通学生退出旧书楼，宁缺也并非立即破境。`JY-MID-01`。
- 高境界不是自动通关。隆庆可被幻境所困；弱者也不是必然靠巧思获胜。`JY-MID-05/06`。
- 通过外部判定后，不要擅自结算主目标。唐小棠到达前坪仍无法救人。`JY-L02`。
- 规则突破后，仍须保留反制与后果；否则门槛会退化成一次性钥匙。`JY-L03`。

# What Existing Skill Misses

现有 `trial_challenge`、`training_learning`、`showcase_evaluation` 已有“外部成功线、反馈、压缩重复”的基础。但这批证据新增了四项实际判断能力：

1. **资格税判别**：必须区分制度真正测量的东西，和共同体宣称它测量的东西；二者错位时，考试可保留其社会成本，但不应伪装成能力成长。
2. **门槛级联**：准入、现金、德行、知识能力、社会承认可能是连续门槛；只展开真正改变下一步选择的那一层。
3. **旧能力重编码**：不要用“突然更强”解门；先确认角色已有能力，再让新规则暴露其新的适配价值。
4. **结果分层停笔**：进入、判定、获得、目标完成、社会承认不是同一状态；应在本场主问题结算后停下，把后续冲突交给下一场。

# Candidate Transfer Rules

1. **规则—资源级联**

   - **applicability**：入学、晋升、任职、准入后紧接资源约束的场景。
   - **rule**：手续完成后，只补写第一个真正迫使人物重新选路的下游门槛。
   - **stop rule**：合规路线已确定，并改变下一场行动时停止。
   - **failure pattern**：反复盖章、排队、说明流程，没有成本或决定。
   - **evidence**：`JY-E01`、`JY-E02`。

2. **累计评分下的主动取舍**

   - **applicability**：多科、多项、可累积分数的考核。
   - **rule**：先让读者知道强项、弱项与总分关系；人物随后主动押注可得分项。
   - **stop rule**：强项得到可见评分或旁观者重估即可。
   - **failure pattern**：用漂亮话、伪装或未建立的万能能力直接换高分。
   - **evidence**：`JY-E03`、`JY-E04`。

3. **硬门槛的有效重复**

   - **applicability**：训练、阅读、修行、耐受类阻碍。
   - **rule**：每次展开的重试都必须带来新反馈、新方法、新关系判断或新的身体代价。
   - **stop rule**：出现方法变更、明确退出或硬性失败即压缩后续重复。
   - **failure pattern**：角色只是更痛苦地再来一次。
   - **evidence**：`JY-MID-01`、`JY-MID-03`。

4. **规则内绕行**

   - **applicability**：阵法、谜题、流程门、技巧型资格试。
   - **rule**：先让规则造成失败，再显出机制；解法必须来自先前建立的能力，且保留成本。
   - **stop rule**：阶段门打开，下一层未知立即接管时停止。
   - **failure pattern**：灵感无来源、规则失效、一次解释解决所有后果。
   - **evidence**：`JY-MID-05`、`JY-L01`。

5. **通过后的未结算结果**

   - **applicability**：通过会重分配身份、资源、归属或多方利益的考核。
   - **rule**：明确本次只结算哪一层：进入、资格、目标或承认；其余层保留为下一场冲突。
   - **stop rule**：本场状态交换已经落地。
   - **failure pattern**：一通过就同时获得身份、关系、资源、终极目标和全员认可。
   - **evidence**：`JY-P01`、`JY-L01`、`JY-L02`。

# Source Fidelity Audit

- 已排除仅有回顾性评价、没有完整现场交换的候选，如后山回顾登顶考验的段落；它们可说明主题，不能代替场景证据。
- 已排除“修行者无人可教”的纯讨论候选；虽涉及修行上限，但缺少外部判定线或当场跨越动作。
- 已排除仅有安检通过结果、未呈现完整门槛—选择—反馈链的潜入候选。
- `JY-E02` 的部堂流程本身接近资格税，保留它仅因原文立刻把资格转成现金与德行约束；不以它证明“行政流程天然有戏”。
- 全部保留窗口都有本地 `gb18030` 解码后的章节名与行号；未用模型记忆补足未写出的考试机制、人物动机或结果。
