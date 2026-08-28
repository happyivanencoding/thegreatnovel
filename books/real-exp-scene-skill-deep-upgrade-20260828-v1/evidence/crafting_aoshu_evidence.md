我会只以本地《奥术神座》文本为依据，先核对编码、全书章节定位与现有 Scene Skill 的能力边界，再挑选分散的高信号实验/制作场景；不会把未被文本支持的推断写成证据。我正在使用 `distill-novels` 保证定位、证据与可迁移结论分层，并对照 `novel-scene-skills` 的 crafting / learning / insight / evaluation 边界，避免把已有能力换词重述为“新发现”。已完成全书编码与章节索引核对：文本以 GB18030 解码后共 56,648 行，并已从第一到第八部检索。现在正把“真正在现场改变方案或验证结论”的片段与仅有论文、讨论、结果转述的段落剥开，后者会作为反例边界，而不会混入证据窗口。# Source

- 《奥术神座》；本地 TXT 按 `GB18030` 解码，`splitlines()` 后共 56,648 行。
- 只使用该文本；所有 locator 为解码后本地行号。完成通知已发送至邮箱。

# Research Question

研究实验、制作、魔法研究中的创建场景：如何组织问题、材料/工具、关键控制、失败反馈与成果验证；技术细节如何服务幻想，而非变成工程日志。

# Evidence Windows

## AOSHU-CRAFT-01

**Evidence — 第一部·第四十五章《路西恩的魔法实验室》，2575–2593；anchor：`消除波动`**

- **scene posture/type**：研究基础设施的创建。
- **scene goal / pre-state**：已有器皿与材料，却没有可安全进行小型试验的场所。
- **expanded beats**：挖出狭小地下室→设置隔音→以银匕首刻阵→黑藤粉固定水银→启动遮掩波动的阵法→摆放器皿。
- **compressed/omitted beats**：此前数夜的陷阱与普通阵法直接压缩，不逐笔描写。
- **state-changing exchange**：粉末黏住水银、阵纹亮起并隐没，说明“隐蔽”从计划变为可用条件。
- **opponent/other-character reaction**：无；此处不需要旁观者。
- **body/space/detail selection**：只给地下室尺度、匕首、粉末、水银、精神疲惫；它们都直接解释空间为何可用且有时限。
- **ruler/reader model**：从外部看不出异常，且能承载后续“小动静”实验。
- **stop point**：入口封闭、器皿摆定、用途说清即止。
- **Interpretation — transfer observation**：基础设施戏的验证不必“性能大爆发”；把一个未来场景能否成立的条件变为可见事实即可。
- **anti-inference**：不能推出所有制作场景都需要秘密工坊或安全阵法。

## AOSHU-CRAFT-02

**Evidence — 第一部·第五十一章《消息》，2877–2894；anchor：`炽火胶`**

- **scene posture/type**：成熟配方的受控炼制。
- **scene goal / pre-state**：取得材料，要做可随身使用的爆燃药剂；此前失败曾造成轻伤，且没有足够防护。
- **expanded beats**：红液与黑液分次混合→搅拌与炼金阵共同压住爆炸趋势→改阵与降温→封管。
- **compressed/omitted beats**：此前多轮失败、成品威力测试、其他药剂的完整工序均被一句带过。
- **state-changing exchange**：每滴材料都诱发不稳定，人物以搅拌、阵法和温度三项控制回应；最终获得稳定成品。
- **opponent/other-character reaction**：无；紧张来自器皿内部的反应。
- **body/space/detail selection**：手、陶棒、滴管、白雾、收缩液体；细节只用于读者判断“为何会炸、为何没炸”。
- **ruler/reader model**：是否失控、是否形成可密封的成品。
- **stop point**：药剂入腰带，立刻转向下一项行动。
- **Interpretation — transfer observation**：熟练制作也可有悬念，但只需保留一个会改变成败的控制点。
- **anti-inference**：此前失败不是本场必须再演一遍的固定节拍。

## AOSHU-CRAFT-03

**Evidence — 第一部·第七十九章《哭泣灵魂》，4456–4504；anchor：`消音壁垒`**

- **scene posture/type**：高风险配方的失败—诊断—返工。
- **scene goal / pre-state**：在被监视的时段间隙炼成药剂；配方可用，但材料存在变异。
- **expanded beats**：称量、切分、调火、按顺序投料→异常声波与灵体反噬→判断不是配方整体错误，而是变异材料造成偏差→预设隔音与束缚→第二次完成。
- **compressed/omitted beats**：配方历史、常规辅料作用不展开。
- **state-changing exchange**：失败反馈不是“炸了”，而是特定声波与异常灵体；判断把下一轮控制从“照配方做”改为“防异常输出”。
- **opponent/other-character reaction**：无；人体反应承担危险读数。
- **body/space/detail selection**：恶心、后退、眩晕、器皿中人脸，只保留会迫使人物中止或修正的感官。
- **ruler/reader model**：第二次的声音被抵消、产物外观符合预期。
- **stop point**：产物出现且危险被控制，不再重复配方。
- **Interpretation — transfer observation**：失败反馈要指向“哪一类前提错了”，再让修正直接对应这一类错误。
- **anti-inference**：不能据此要求每次返工都加新防护；这里的防护来自第一次已经出现的具体威胁。

## AOSHU-CRAFT-04

**Evidence — 第二部·第二十三、二十四章《人工合成》《产物》，9274–9384；anchor：`亲自动手`**

- **scene posture/type**：争议性研究的公开可核验演示。
- **scene goal / pre-state**：证明非生命材料能合成一种被旧理论视为生命相关的物质；在场对手坚信不可能。
- **expanded beats**：让对手而非主角布置装置→分离气体、设定催化与高温高压→得到中间物→第二次反应→取样、鉴定、追加多轮实验。
- **compressed/omitted beats**：具体化学转化链只保留能让读者理解条件差异的温压与材料关系。
- **state-changing exchange**：产物出现后，先由对手鉴定，再由其自行追加验证；“做出来”转成“对方承认事实”。
- **opponent/other-character reaction**：围观者由笃定转为恐惧；对手承认产物，却重新界定其概念地位。
- **body/space/detail selection**：高台、可折叠实验室、反应炉、白色颗粒；空间把实验变成公开赌局。
- **ruler/reader model**：不是主角宣布成功，而是对手亲自操作、鉴定、复验。
- **stop point**：事实层面已成立，但概念争议重新打开；不强行把一次验证写成终局。
- **Interpretation — transfer observation**：若成果会改写既有立场，让质疑者控制或复核关键一环，比增加技术参数更有说服力。
- **anti-inference**：一次产物验证不等于整个理论已经被证实。

## AOSHU-CRAFT-05

**Evidence — 第三部·第五十一、五十二章《为什么》《魔鬼，真正的魔鬼！》，13601–13776；anchor：`淡红色物质`**

- **scene posture/type**：长周期模拟实验与集体验证。
- **scene goal / pre-state**：检验原始环境能否自然生成生命相关物质；读者与旁观者都认为装置过于简单。
- **expanded beats**：提出“模拟什么”→选择常见气体和纯水→从对照组确定比例→多方鉴定输入无杂质→循环高温、闪电、冷凝→一周无变化→颜色出现→多器皿取样、多人鉴定。
- **compressed/omitted beats**：一周内相同循环压缩成等待与观察，不逐日写日志。
- **state-changing exchange**：异常颜色出现后，撤保护、取样、多人鉴定；结果从视觉异常升级为可共享结论。
- **opponent/other-character reaction**：怀疑者因结果动摇；高阶研究者同时指出这只是生命研究的第一步。
- **body/space/detail selection**：玻璃瓶、导管、闪电、冷凝水、淡红色；反复出现的视觉循环承担“过程仍在发生”。
- **ruler/reader model**：输入已验证、循环未受干扰、产物可被多人识别。
- **stop point**：首次确认产物与其改变的研究方向；不把“生命如何完整形成”伪装成已解决。
- **Interpretation — transfer observation**：长期实验只展开三处：控制如何成立、等待为何不等于无事、异常出现后如何被确证。
- **anti-inference**：简单装置获得重大结果，不等于研究问题本身简单。

## AOSHU-CRAFT-06

**Evidence — 第三部·第五十六章《大陆的两边》，13928–13958；anchor：`红外光眼`**

- **scene posture/type**：新魔法的构造与最低用途验证。
- **scene goal / pre-state**：把已理解的成像原理转成可施放的二环探查法术；难点在原理如何映射为符文结构。
- **expanded beats**：组合阵法先成像→在黑暗中以活体目标复测→切换光照环境→确认可用于搜寻目标。
- **compressed/omitted beats**：完整法术模型、符文推导、材料消耗均不展开。
- **state-changing exchange**：模型形成后，目标与室外飞鸟提供两次不同尺度的验证。
- **opponent/other-character reaction**：无；这里的“他者”是可移动目标。
- **body/space/detail selection**：黑暗、红色影像、左眼变化、老鼠与飞鸟；全是功能的可见化。
- **ruler/reader model**：在无光处识别目标，且知道画面仍有层次限制。
- **stop point**：用途和限制清楚，转入后续法术规划。
- **Interpretation — transfer observation**：首次验证可用“一个贴身目标＋一个外部目标”完成，不必再上强敌试刀。
- **anti-inference**：不支持把所有新能力都写成两次测试；这里两次测试服务于“室内/室外”的功能边界。

## AOSHU-CRAFT-07

**Evidence — 第五部·第二十三至二十五章《规定》《万事俱备》《一种新粒子》，20424–20455、20521–20619；anchor：`阴极射线`**

- **scene posture/type**：团队发现后的分工验证。
- **scene goal / pre-state**：确认新辉光究竟是未知射线、电磁波，还是带电粒子；当前只有异常现象。
- **expanded beats**：抽稀气体、提高电压、复现绿色辉光→放入障碍物得到阴影→成员各自测不同性质→出现“持续偏转不足”的反例→发现低温木炭可改善真空→改阵、测轨迹与荷质比。
- **compressed/omitted beats**：一个月大量论文和大部分重复测量被概述。
- **state-changing exchange**：阴影先把“幻觉式异常”锁定为装置相关；后来的失败改变设备条件，而不是硬改结论。
- **opponent/other-character reaction**：助手先振奋、后困惑；导师不提前宣布答案，而是把解释降回待测假设。
- **body/space/detail selection**：绿色辉光、阴影、放电阵、真空条件、数据记录；每项都对应一个可排除的解释。
- **ruler/reader model**：可复现、可改变条件、可测得一致荷质比。
- **stop point**：新粒子结论足以写论文，并承认仍可继续改变材料条件复测。
- **Interpretation — transfer observation**：研究戏的推进单位可不是“操作步骤”，而是“排除一个解释／获得一个新控制条件”。
- **anti-inference**：多人分工并非自动更有戏；这里成立，是因为成员结果彼此冲突并改变下一步。

## AOSHU-CRAFT-08

**Evidence — 第五部·第一百二十七章《本质改变》，27165–27204；anchor：`寻找轨迹`**

- **scene posture/type**：由既有实验升级设备后的关键测量。
- **scene goal / pre-state**：在已有散射启发下，测出原子内部的带正电组分。
- **expanded beats**：申请改造阵法和炼金装置→从荧光点与轨迹中筛出目标→立即改阵测量→多项数据重合→从结果推出可继续检验的原子结构预测。
- **compressed/omitted beats**：长期观看光点、绝大多数无效轨迹、设备改造过程被压缩。
- **state-changing exchange**：找到预期轨迹后，不用旁白解释，立即切到测量；数据重合才允许命名与推论。
- **opponent/other-character reaction**：无现场对手；此前同行的实验提供进入本场的技术门槛。
- **body/space/detail selection**：观察器、闪烁荧光点、扭曲磁场、凌乱桌面；体现“发现来自筛选而非凭空显现”。
- **ruler/reader model**：电荷量、质量、荷质比三项一致。
- **stop point**：可命名的新对象和可证伪的后续预测出现后，转论文与理论。
- **Interpretation — transfer observation**：当发现来自复杂数据，正文只需让读者看见“发现什么信号、为何立刻切换测量、哪几项读数重合”。
- **anti-inference**：数据重合只支撑当前粒子结论，不自动证明其后所有理论延伸。

## AOSHU-CRAFT-09

**Evidence — 第六部·第六章《屋里屋外》，31028–31041；anchor：`共同来探讨`**

- **scene posture/type**：实验反例的共同诊断。
- **scene goal / pre-state**：回旋加速器在理论上应继续加速，实际却提前脱离加速场。
- **expanded beats**：学生报告反复验证过的偏差→导师先承认不知道原因→比较前后条件→把“高速状态下公式是否失效／粒子属性是否变化”明确为新问题。
- **compressed/omitted beats**：此前多次失败运行与具体数据没有逐条列示。
- **state-changing exchange**：学生带来可复现异常，导师没有用权威补答案，而是把失败转为共同可研究的条件差。
- **opponent/other-character reaction**：学生本能排斥“质量会随速度变化”的可能，这构成合理阻力。
- **body/space/detail selection**：没有额外奇观；此处靠问题的具体性而非感官放大。
- **ruler/reader model**：理论起始阶段有效，后段失效，且已反复验证。
- **stop point**：新问题已足以决定下一轮研究，不抢先解答。
- **Interpretation — transfer observation**：若结果尚未得到，场景可以在“可重复的矛盾被正确命名”处停下。
- **anti-inference**：不能把所有未知都留成悬念；必须先交代旧模型在哪个条件下仍然有效。

## AOSHU-CRAFT-10

**Evidence — 第八部·第六十三章《“考察者”》，45201–45224；anchor：`平缓可控`**

- **scene posture/type**：连续失败后的目标重定义。
- **scene goal / pre-state**：裂变反应堆多次爆炸；现有设计是从杀伤性魔法反向拆得。
- **expanded beats**：不重复描写爆炸→指出“能爆”不等于“可控供能”→将问题落到不同条件下粒子作用→决定重做长期轰击研究。
- **compressed/omitted beats**：多次事故现场完全不重演。
- **state-changing exchange**：失败不被归为单个阵纹损坏，而使成果目标从“能发生裂变”变为“平缓、稳定、可利用”。
- **opponent/other-character reaction**：师徒争论集中在问题归属；导师接受建议但坚持研究成本。
- **body/space/detail selection**：凌乱头发与褶皱法袍只标记事故余波，不把爆炸写成 spectacle。
- **ruler/reader model**：是否能长期稳定输出，而非瞬间威力。
- **stop point**：新的实验问题与成本成立，实际新一轮试验留给后续。
- **Interpretation — transfer observation**：制作失败若只证明“这次坏了”会空转；应让它重新定义成品真正要满足的性能。
- **anti-inference**：不支持把每一次原型事故都升级为大场面。

## AOSHU-CRAFT-11

**Evidence — 第七部·第八十六、八十七章《公开课》《观察改变世界？》，41119–41153；anchor：`单个电子`**

- **scene posture/type**：复杂仪器的公开实验与控制说明。
- **scene goal / pre-state**：验证电子是否具有波动性；观众知道理论争议，却未看到直接结果。
- **expanded beats**：以极细金属板、装置、感应屏建立平台→先出现干涉条纹→解释可能质疑→补充“单个电子”控制已做过，并公开可供他人申请复验。
- **compressed/omitted beats**：单电子长期累积的完整过程被明确压缩，因为现场演示会拖慢节奏。
- **state-changing exchange**：装置先给图像，人物才解释它排除了什么；控制条件改变的是“电子互相干扰”的替代解释。
- **opponent/other-character reaction**：高阶研究者到场，部分人接受现象但继续质疑解释边界。
- **body/space/detail selection**：极细缝、墙面投影、杂乱光点到条纹；视觉从混乱到模式即是验证。
- **ruler/reader model**：可见图案＋单电子控制＋开放复验。
- **stop point**：核心现象和可复核入口成立，立刻转向新一层理论争论。
- **Interpretation — transfer observation**：技术过程可压缩，但必须交代那个被压缩步骤排除了什么关键替代解释。
- **anti-inference**：一次漂亮图像不等于全部理论解释都已唯一成立。

## AOSHU-CRAFT-12

**Evidence — 第八部·第一百一十七章《一年后》，48146–48177；anchor：`误差叠加`**

- **scene posture/type**：高阶物品升级的精度控制。
- **scene goal / pre-state**：把“月时计”升阶；上一次因两处微小误差叠加而失败并受伤，材料不可轻易再得。
- **expanded beats**：隔绝干扰→以材料绘阵→放置残余材料→接入目标→检查每处连接的精度→启动供能→备用能量耗尽后投入自身精神力→功能出现。
- **compressed/omitted beats**：上次失败的全过程没有回放；阵纹的完整工程结构不展开。
- **state-changing exchange**：前两步完成后才允许人物认为风险下降；能量不足迫使投入自身资源，形成最后关口。
- **opponent/other-character reaction**：外部角色通过时钟异象感到变化；不进入实验室代替主角判断。
- **body/space/detail selection**：汗水、材料位置、连接误差、塔内熄灯、时钟异象；都服务“精度和供能”。
- **ruler/reader model**：新按钮与首次能力读取，且明确次数限制。
- **stop point**：新功能、代价与限制都清楚，不追加多轮试用。
- **Interpretation — transfer observation**：高端制作戏可把技术复杂度收束为一个读者能跟住的尺度：连接误差、能量缺口或材料不可再得。
- **anti-inference**：并非所有传奇制作都需要“前次失败”；这里的失败背景是本次精度紧张的来源。

## AOSHU-CRAFT-13

**Evidence — 第八部·第一百三十二章《擦除实验》，48980–49048；anchor：`等价变形`**

- **scene posture/type**：公开研究实验的对照、结果与可重复性。
- **scene goal / pre-state**：检验“记录后擦除”会否改变双缝结果；旧实验已给出观众共同基线。
- **expanded beats**：先重演旧实验→重布新装置并说明与旧机制等价→明确预测分歧→运行→结果与常识预期相反→同一实验重复五次→开放他人复现。
- **compressed/omitted beats**：真实装置细节被转换成易懂的“记录／报警／擦除”功能描述。
- **state-changing exchange**：新装置不是为了堆新名词，而是删除一个无关变量；重复把震撼结果从偶然变成暂时可信的事实。
- **opponent/other-character reaction**：普通观众、学生、权威者按各自认知承受结果；反应显出结论改变了哪些既有判断。
- **body/space/detail selection**：屏幕、安静、摔杯、手颤；身体细节只在结果冲击已被观众理解后出现。
- **ruler/reader model**：与旧实验的等价性、可见结果、五次重演、开放复验。
- **stop point**：可重复性已建立；转入“如何解释”而非再堆实验。
- **Interpretation — transfer observation**：当新实验难懂时，先给读者熟悉基线，再只替换一个会改变结论的变量。
- **anti-inference**：五次重复是此处主张冲击极高的写法，不构成每个小型制作场景的必要税。

# Cross-Window Findings

1. **技术细节的最小单位不是步骤，而是一个会缩小解释空间的控制。**材料比例、真空、障碍物、单电子、等价变形都因排除替代解释才被展开；普通装配与重复运行则压缩。`AOSHU-CRAFT-02/04/05/07/08/11/13`

2. **失败应改变“下一轮要控制什么”，而不是只增加危险感。**材料变异催生防护，连续爆炸改写成品目标，理论与实测的偏差被命名为高速条件问题，旧失败则为精度检查提供理由。`AOSHU-CRAFT-03/09/10/12`

3. **成果验证必须让读者看见“结果如何对应原目标”，而不止一句成功。**成品可用、图像出现、数据重合、对手复核、新按钮出现、重复实验，分别把不同类型的成果变成可判断的事实。`AOSHU-CRAFT-04/06/08/11/12/13`

4. **长时程研究靠“等待中的不变”蓄压，靠首次异常释放，不靠逐日记录。**一周循环、一个月的团队实验、长期炼废物品都被压缩；读者只在异常、诊断与检验时停留。`AOSHU-CRAFT-02/05/07/11/12`

5. **他者反应只在其能改变可信度或后续选择时进入现场。**对手亲自操作与复验、多人鉴定、学生提出反例、不同立场对实验结果的受冲击，均改变结论的社会含义；单人炼制则不强塞观众。`AOSHU-CRAFT-01/04/05/07/09/13`

# Counterexamples & Boundaries

- 成熟设施或成熟配方不必配置失败。实验室建成与炽火胶炼成靠时限、隐蔽和一个不稳定控制点已足够。`AOSHU-CRAFT-01/02`
- 研究场景可停在“可重复矛盾被准确命名”，不必当场给出答案。`AOSHU-CRAFT-09`
- 首次验证可非常简短：红外法术以两个可识别目标完成最低检验，而非强行安排战斗。`AOSHU-CRAFT-06`
- 结果成立仍可能不终结争议：尿素被反复验明，但其概念归属仍遭质疑；不能把“检测成功”写成“全领域定论”。`AOSHU-CRAFT-04`
- 复杂装置的创建过程可以不现场展开。宇宙观察站的文本重点是首次进入、用途与使用边界，而非建造；它适合做“完成后揭示”的反例，不应当作制作流程证据。第八部·第八十章《奥术研究的浪漫》，46111–46155。

# What Existing Skill Misses

对照当前 [crafting_creation.md](/C:/dev/tgn-story-mvp/.agents/skills/novel-scene-skills/scenes/crafting_creation.md:3)：

1. **缺“实物制造”与“待证命题”的双状态区分。**现有 Skill 能处理成品与设计目标的差距，但没有规定研究场景必须把“装置状态”与“解释状态”分开推进。阴极射线、回旋加速器、量子擦除都显示：装置可正常运行，解释仍未定案。`AOSHU-CRAFT-07/09/13`

2. **缺“关键控制如何叙事化”的选择法。**当前只要求依据反馈调整，未要求作者明确本轮删掉哪个替代解释、读者如何看懂这个变量变化。障碍物阴影、不同真空、单电子、等价变形正是这项缺口。`AOSHU-CRAFT-07/11/13`

3. **缺失败反馈的分类与切换。**“材料偏差”应导向配方/防护修正；“目标不等价”应导向性能重定义；“模型与数据冲突”应导向新问题，而不是立即返工。`AOSHU-CRAFT-03/09/10`

4. **缺过程内的可信度机制。**现有 `showcase_evaluation` 主要处理成果已成后的社会估值；本书的关键做法是让质疑者操作、复验、鉴定，先让过程本身获得可信度。`AOSHU-CRAFT-04/05/13`

5. **缺“技术细节的压缩理由”。**现有 Skill 说不要写教程，但尚未明确：可以压缩什么，前提是保留其所排除的解释与首次验证。`AOSHU-CRAFT-05/07/11`

# Candidate Transfer Rules

1. **规则：先判定本场是在做“成品”，还是在做“结论”。**

   - applicability：读者问题是“能不能造出来”或“这个现象意味着什么”之一，或两者并存。
   - stop rule：成品戏在首次用途成立后止；研究戏在当前假说获得最小现实反馈或明确反例后止。
   - failure pattern：把研究戏写成纯工序，导致结果看似来自作者宣布；或把制作戏写成抽象论文，导致成品没有可感知用途。

2. **规则：每一段技术动作都要对应一个唯一的叙事控制。**

   - applicability：场景存在多材料、多装置或多参数。
   - stop rule：读者已知道该控制排除了什么、改变了什么，就压缩其余同类操作。
   - failure pattern：罗列温度、阵纹、型号、比例，却没有任何一个细节改变成败、性能或解释空间。

3. **规则：失败后先定位“错的是材料、装置条件、性能目标，还是解释模型”。**

   - applicability：出现失控、异常读数、无法复现或结果与预期冲突。
   - stop rule：错误类别已决定下一次尝试的不同控制，即转入下一轮或转场。
   - failure pattern：失败只带来受伤、烧毁、惊叫，下一轮仍按原方案机械重做。

4. **规则：高认知负荷实验先建立共同基线，只替换一个影响结论的变量。**

   - applicability：实验本身陌生，或结果会颠覆读者/角色已有模型。
   - stop rule：旧方案、变形方案与唯一差异都清楚后，直接运行并展示结果。
   - failure pattern：先讲完整理论、再堆新装置，使读者不知道结果究竟由哪项变化造成。

5. **规则：验证优先选择能让角色立场改变的观察者。**

   - applicability：成果会被质疑，或其意义须超出主角自述。
   - stop rule：一位合适的质疑者、专家、助手或使用者完成有行动后果的判断即可。
   - failure pattern：多人轮流惊叹同一件事，或把反应留到成果已被旁白定义之后。

6. **规则：时间压缩围绕“不产生新信息的稳定运行”，而非围绕现实耗时。**

   - applicability：试验、等待、校准、重复炼制需要很长时间。
   - stop rule：第一次异常、首个可用结果或能改变方案的读数出现时恢复场景速度。
   - failure pattern：逐日实验日志拖慢阅读，或完全跳过等待，使结果像无代价掉落。

# Source Fidelity Audit

- 13 个入选窗口均已用 GB18030 解码后的 `splitlines()` 核对；未引用网络资料、模型记忆剧情或作者资料。
- `AOSHU-CRAFT-05` 的 locator 含一段并行情节，故只使用其中的装置设置、长期观察、取样与鉴定，不把并行情节当实验机制。
- 以下候选排除，不作为本次核心 evidence：

  - 第六部·第五章附近的超导成果：文本主要呈现成果展示与评价，未充分呈现发现时的创建/试验过程。
  - 第七部·第十五至十八章的电子波动论文争议：假设与审核反应充分，但缺少本窗口内实际验证，不能作为创建场景证据。
  - 第八部·第八十章《奥术研究的浪漫》，46111–46155：是完成后的研究基础设施揭示与首次使用，不是现场制作。
  - 第五部·第一百零七章《“发射”》，25983–26044：人造星球的具体制造过程被大幅压缩，只足以支持“最低验证目标”，不足以支撑制作步骤规则。
