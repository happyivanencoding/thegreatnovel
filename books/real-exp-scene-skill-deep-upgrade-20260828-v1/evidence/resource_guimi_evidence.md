我会严格以本地《诡秘之主》TXT 为唯一证据，按 GB18030 解码与解码后行号定位；同时对照仓库现有 Scene Skill，提炼可迁移但不模仿文风的规则。先读取相关研究与场景技能约束，再分段检索原著。我已启用 `distill-novels`（它要求证据、解释、可迁移原则分层）并读取现有场景库总则；接下来会把全书按前中后段交叉取样，同时以现有 `resource_economy` 条目为基线判断新增能力。全书共有 118,560 行、章节标题在 TXT 中存在分卷重置；我会把“章号+标题”和绝对行号并列，避免仅凭重复章号误定位。已核验的强信号包括：租房预算如何转成谈判、优厚工资仍受材料配额限制、额外收入如何分裂为家庭可见收益与隐秘学习储备。另一个关键核验是：数字并非都要解释。有效窗口都让数额立刻承担一个场景动作——压价、留存、拒买、换币种、拆分预付与绩效、或把高薪改写成“仍无法练习”的制度缺口；纯粹报报价而没有后续选择的候选将被剔除。证据已收束为 14 个可复核窗口，覆盖家庭日常、机构配额、配方与材料估值、海上资产压力、消耗品、以及分段委托；我已排除只有报价、没有选择/反应/状态变化的片段。# Source

- SOURCE BOOK：`诡秘之主`
- SOURCE PATH：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\小说整理合集\01_玄幻\诡秘之主.txt`
- RESEARCH LANE：`resource_guimi`
- 定位方式：读取原始 bytes，以 GB18030 解码后 `splitlines()` 计数。TXT 有分卷后章号重置，故以“章号/标题 + 绝对行号”共同定位。
- 方法边界：仅使用上述本地文本；以下均为意译，anchor 仅供复核。

# Research Question

研究日常价格、材料、仪式/配方成本与身份收入：什么数字值得写，如何让资源稀缺改变选择，并避免账本化。

# Evidence Windows

## RES-01

- 定位：第三十章《新的开始》，2756–2768；anchor：`不是谁都能`
- Scene posture/type：搬家看房后的家庭资源决策。
- Scene goal：决定是否租下新居，并把“想拥有房子”落到可执行选择。
- Evidence：
  - pre-state：三兄妹已有更高周薪，但仍在找合适住处。
  - expanded beats：房东报出售价与租赁条件；主角将家庭收入、房租、食物、交通、婚育等放进一次心算；结论是买房不可达，立刻把行动交给更会谈价的哥哥。
  - compressed/omitted beats：没有逐项展开每一餐或每件衣服的账。
  - state-changing exchange：哥哥以采光、家具、壁炉等具体缺点压价，租金、家具费和押金均下降。
  - reaction：妹妹对新家发亮；房东被谈判说服。
  - body/space/detail：走廊、阳台、旧家具、钥匙与剩余现金，将住房价格落到能住、能晒衣、能否安家的体验。
  - ruler/reader model：数字的作用不是证明主角穷，而是让读者理解“有收入”与“拥有资产”之间仍隔着多年。
  - stop point：签约、付款、拿到钥匙后停止。
- Interpretation：适合写的不是完整预算，而是一个足以否决错误目标、并立刻改变谈判角色分工的估算。
- transfer observation：让一个大额价格撞上人物的稳定收入与可见生活成本，再把结论变成下一句行动。
- anti-inference：不能据此推出所有住房戏都必须详列预算；此处计算服务于“放弃购买、转入租赁谈判”。

## RES-02

- 定位：第四十七章《缺钱的老尼尔》，4361–4396；anchor：`薪水总是不够`
- Scene posture/type：师徒闲谈转为资源渠道揭示。
- Scene goal：解释高薪角色为何仍缺钱，并让主角获得材料来源的新行动入口。
- Evidence：
  - pre-state：主角刚接到高价值委托，误以为资深同事不会缺钱。
  - expanded beats：同事给出薪酬量级及社会参照；随即说明练习、实验和仪式受机构领用额度与正当理由约束；私人购买、地下市场因此成为必要渠道。
  - compressed/omitted beats：未列出每种材料的单价与库存。
  - state-changing exchange：主角从“材料可申请”改为请求被带去交易市场；同事却因债务暂时无法带路。
  - reaction：主角兴奋后受阻，提出借钱。
  - body/space/detail：沙发上的后仰、手腕吊坠、为难表情，让“材料短缺”先显为人际迟滞。
  - ruler/reader model：高工资不是资源充足；真正的缺口是可自由支配的试错额度与合法取得路径。
  - stop point：主角转而使用手头报酬解决另一项学习入口。
- Interpretation：把“稀缺”设置为配额、审批和渠道限制，比单纯设定穷更能逼出选择。
- transfer observation：当人物理论上有钱却无法推进时，优先写出# Source

- SOURCE BOOK：诡秘之主
- SOURCE PATH：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\小说整理合集\01_玄幻\诡秘之主.txt`
- RESEARCH LANE：`resource_guimi`
- 定位方法：`read_bytes()` → `gb18030` 解码 → 解码后 `splitlines()` 计行号。章节号在 TXT 中会分卷重置，故以“章节标题 + 绝对行号”共同定位。
- 范围：仅此 TXT；不以模型记忆补剧情。

# Research Question

日常价格、材料、仪式/配方成本与身份收入中，什么数字值得进入场景；资源稀缺如何改变人物选择，而不把戏写成账本。

# Evidence Windows

## RES-GM-01

- evidence_id：RES-GM-01
- chapter：第三十章《新的开始》
- source lines：2756–2768
- anchor：`不是谁都能`
- scene posture/type：看房后的家庭决策。
- scene goal：确认新住处是否可负担，并落定租约。
- pre-state：三兄妹有较高的新收入预期，但没有一次性购房能力。
- Evidence：房主报出长期地契与完全购买的两个数额；主角把收入、吃住、交通、婚育等压缩为“年储蓄速度”，立刻放弃买房念头，转而示意哥哥压租。谈判后，租金、家具费与押金均下降；交款后余额被报出。
- expanded beats：只展开能改变“买/租”“接受/压价”的数额、余额和居住条件。
- compressed/omitted beats：没有逐项展开每餐、每件衣物的消费记录。
- state-changing exchange：购买不可达 → 租赁成为现实路径；看房 → 压价并签约。
- opponent/other-character reaction：妹妹和哥哥被购房念头惊到；房东被具体缺点与再出租收益说服。
- body/space/detail selection：狭小阳台、采光、旧家具、钥匙与门口停顿，把抽象住房成本落为可住与不可住。
- ruler/reader model：数字值得写，因为它决定人物能否拥有稳定空间，而不是因为金融设定完整。
- stop point：交押金、拿钥匙、明确剩余现金后停。
- Interpretation：大额价格先用“普通收入需要多久”翻译，再让人物改用可行动的次优方案。
- transfer observation：价格应把远大愿望压缩成一个当下动作。
- anti-inference：不能据此推出每次买房戏都必须计算年限；这里的计算服务于“从买到租”的即时转向。

## RES-GM-02

- evidence_id：RES-GM-02
- chapter：第四十七章《缺钱的老尼尔》
- source lines：4361–4396
- anchor：`薪水总是不够`
- scene posture/type：同事闲谈转资源入口。
- scene goal：解释高薪者为何仍缺钱，并打开材料市场线索。
- pre-state：主角刚获高额委托报酬，误以为资深同事的高收入足够覆盖需求。
- Evidence：资深者的收入被与律师、经理等身份比较，先建立“丰厚”的共同认知；随后由练习、尝试仪式的材料配额与申请理由推翻“高薪=富足”。谈话进一步给出地下市场、材料来源与管制边界，主角立刻请求进入该渠道。
- expanded beats：收入比较、配额限制、市场存在的制度原因。
- compressed/omitted beats：未列出每次练习的材料清单或日常支出账。
- state-changing exchange：高薪的误读 → 材料渠道成为主角新需求；同事的欠账又暂时阻断带路。
- opponent/other-character reaction：同事先笑后为难；主角从诧异转为急切。
- body/space/detail selection：沙发靠背、搓弄吊坠、为难表情，使制度解释仍留在人际对话中。
- ruler/reader model：稀缺不必等于“没钱”；配额、正当性与渠道同样能把资源变成行动瓶颈。
- stop point：主角提出带路请求、被债务暂缓后停。
- Interpretation：这场戏的价格单位不是材料标价，而是“可获得性”。
- transfer observation：优先写让角色无法取得资源的门槛，再写金额。
- anti-inference：不能把所有机构写成压制资源流通；本窗口同时证明受控市场也能因治理成本而被容忍。

## RES-GM-03

- evidence_id：RES-GM-03
- chapter：第五十章《老尼尔的还钱办法》
- source lines：4562–4592
- anchor：`真正有了积蓄`
- scene posture/type：家庭晚餐中的收入分配。
- scene goal：让一笔额外报酬同时改变家庭关系与主角的隐秘资源计划。
- pre-state：家庭收入紧，主角需维持普通职业身份，同时准备神秘学材料。
- Evidence：一笔额外收入被用兄长近四周工资作比例；主角公开交出其中一部分，私下把另一笔经费留作材料储备。兄妹没有围绕账目争执，而是分别提出衣物、储蓄、学习投资等不同用途。
- expanded beats：一笔钱对家庭而言有多重、互相冲突的用途。
- compressed/omitted beats：没有计算衣物、书籍、裙子的精确价格。
- state-changing exchange：收入使家庭第一次有“积蓄”感，也让主角获得不公开的学习本金。
- opponent/other-character reaction：兄妹先惊讶后相信；妹妹偏向储蓄，哥哥把钱转成提升职业能力的计划。
- body/space/detail selection：餐桌、钞票被反复查看、刀叉停顿，令金额先成为关系事件。
- ruler/reader model：值得写的收入，是能迫使不同人物暴露“钱该为谁服务”的收入。
- stop point：家庭对衣物与存钱达成暂时安排后停。
- Interpretation：资源戏可同时保留公共账本与私人账本，张力来自两者不能互相解释。
- transfer observation：若资源涉及秘密身份，至少让一次配置在亲密关系中留下可见后果。
- anti-inference：并非每笔隐秘资金都该制造猜疑；此处亲属信任反而压低冲突，保留了后续负担。

## RES-GM-04

- evidence_id：RES-GM-04
- chapter：第五十一章《接地气的仪式魔法》
- source lines：4670–4708
- anchor：`必须牢记`
- scene posture/type：仪式教学与现场布置。
- scene goal：把仪式成本从“材料罗列”变为成功条件与风险选择。
- pre-state：学徒首次系统学习仪式，拥有危险的既往经验。
- Evidence：导师只取与目标象征相关的蜡烛、油、容器、盐和刀具；强调日期、环境、能力与辅助器具会影响成败，并明确低阶者不可为追求效果向未知对象求助。材料随后被摆入圆桌的空间关系中。
- expanded beats：象征为何对应目标、什么能力可减少辅助品、什么环境不可省。
- compressed/omitted beats：不报材料单价，不逐一介绍无关库存。
- state-changing exchange：普通“能否照做”的理解 → 学徒知道成本包含风险边界、环境与能力门槛。
- opponent/other-character reaction：导师在关键禁令处严肃，学徒因自身经历心虚。
- body/space/detail selection：清空圆桌、蜡烛位置、银箱和器物的取放，使准备过程可见。
- ruler/reader model：仪式材料值得写，前提是其缺失、替代或错误组合会改变结果。
- stop point：器物与规则齐备、正式仪式即将开始时停。
- Interpretation：仪式成本不等于货币；它还包括时间窗口、安静空间、能力要求与不可触碰的风险。
- transfer observation：每件被展开的仪式物应回答“它替哪项风险付费”。
- anti-inference：不适用于纯装饰性仪式；若材料不改变成功率、代价或选择，应压缩。

## RES-GM-05

- evidence_id：RES-GM-05
- chapter：第一百三十二章《再见“怪物”》
- source lines：12032–12042
- anchor：`只能看一看`
- scene posture/type：离开交易市场后的个人资源重估。
- scene goal：把现金不足转成两条收入路线，而非停在贫穷感叹。
- pre-state：主角刚恢复少量私房钱，仍背负预支工资的还款压力。
- Evidence：他面对非凡材料只能旁观；高息借款是可选但不优的路径。随即他区分家庭可见收入、私房钱与可通过配方/占卜取得的收益，并反思自己此前低价定位带来的改价困难。
- expanded beats：只展开会改变资金来源、身份暴露或收费权的数额。
- compressed/omitted beats：市场上具体有哪些材料、各自标价没有展开。
- state-changing exchange：无力购买 → 调整收入规划与经营策略。
- opponent/other-character reaction：无直接交易对手；既有客户与自己已建立的形象构成“不能随意涨价”的社会反作用。
- body/space/detail selection：从地下市场走到马车、再到俱乐部，空间切换对应资源路径切换。
- ruler/reader model：稀缺有效的信号不是“余额很低”，而是已有资源只能看、不能拿。
- stop point：确定下一步收入计划并进入职业场景后停。
- Interpretation：身份经营本身会锁住价格调整空间。
- transfer observation：当角色缺钱时，至少呈现一种可借、可赚、可卖或可等的路线，并让他拒绝其中一条。
- anti-inference：不能把借钱一律写成愚蠢；这里拒绝的是高息且会伤害后续选择的借款。

## RES-GM-06

- evidence_id：RES-GM-06
- chapter：第一百五十八章《有备无患》
- source lines：14113–14120
- anchor：`合理的交易`
- scene posture/type：知识/配方的定价谈判。
- scene goal：确定信息服务的报酬，并展示买卖双方不同的估值锚点。
- pre-state：买方刚获得配方校验与补全，卖方必须维持超然身份。
- Evidence：买方用低价购得的日记、同层级配方的市价与服务价值三项比较，提出折中支付；卖方压下个人对大额现金的震动，只确认交易合理。
- expanded beats：只给支撑“报价是否心虚、是否划算”的两个参照物。
- compressed/omitted beats：不解释完整市场价格体系。
- state-changing exchange：知识帮助 → 形成可兑现的报酬与后续账户安排。
- opponent/other-character reaction：买方因报价低于自己推算值而心虚；卖方外在淡然、内在被数额触动。
- body/space/detail selection：长桌、反复查看配方、轻敲桌缘，让抽象知识先落为可交割物。
- ruler/reader model：配方价格应配一个角色熟悉的比较基准，否则数字只有规模没有意义。
- stop point：报酬被确认、交付路径明确即停。
- Interpretation：同一金额可同时表达买方的占便宜感与卖方的身份压力。
- transfer observation：知识交易至少给出一个“市场价/取得成本/角色心理价”的对照。
- anti-inference：不能把所有隐秘知识都强行标成固定市价；本窗口中价格正因信息不对称而可谈。

## RES-GM-07

- evidence_id：RES-GM-07
- chapter：第二十七章《赌运气？》
- source lines：21160–21189
- anchor：`400镑能买到`
- scene posture/type：黑市估价转生存抉择。
- scene goal：让材料价格立刻暴露主角无法靠购买解决的危险。
- pre-state：主角持有可交易物，急需应对远强于自己的敌人。
- Evidence：鉴定者用低阶魔药两份主材的常见成本判断 400 镑报价合理；交易成交后，主角立即问这笔钱能买到什么自保手段。回答是否定的，并有人推销同价但高概率致死的物品。
- expanded beats：材料市价、购买力上限、风险概率。
- compressed/omitted beats：不列出全部可买物品。
- state-changing exchange：卖出材料 → 获得现金；现金仍不足以购买安全 → 自救路线不能靠消费完成。
- opponent/other-character reaction：聚会成员对其敌人等级嘲笑、回避；有人借绝境推销风险货。
- body/space/detail selection：面具、沉默的起居室、审视目光，令报价带有试探与暴露风险。
- ruler/reader model：价格不是奖励结算，而是让读者看见“可购买的解决方案仍不够”。
- stop point：高风险替代品被完整说明，主角尚未接受时停。
- Interpretation：合理报价不等于可行方案；购买力必须与问题等级匹配。
- transfer observation：若资源无法解题，应尽快让卖方、旁观者或效果边界把“不够”说清。
- anti-inference：不能为制造绝望而让所有市场物品无效；这里仍给出危险但真实的替代路线。

## RES-GM-08

- evidence_id：RES-GM-08
- chapter：第一百六十八章《猜测》
- source lines：33701–33721
- anchor：`难度和报酬`
- scene posture/type：以任务兑换材料的契约。
- scene goal：把晋升材料变成角色要主动承担或拒绝的工作条件。
- pre-state：角色正为兑换对应材料攒钱。
- Evidence：中间人先给现金报酬，再提出以对应材料作为高价值报酬；角色听到任务与厌恶对象有关后立即拒绝，直到得知对象已死才重新进入信息获取。
- expanded beats：风险未定、初期钱、材料回报与任务对象。
- compressed/omitted beats：材料实际市价、角色总资产不展开。
- state-changing exchange：材料承诺不能直接买到服从；任务的道德/危险信息重写接不接的选择。
- opponent/other-character reaction：中间人先保留风险描述；角色的即时拒绝迫使其补充事实。
- body/space/detail selection：偏僻巷道、先观察再现身，说明资源交换伴随信任与暴露成本。
- ruler/reader model：资源奖励只有在角色愿为它做什么、又不愿为它做什么时才有重量。
- stop point：任务真实对象与下一步情报目标被明确后停。
- Interpretation：材料可作为报酬，但不该自动压过角色底线。
- transfer observation：以稀缺资源发布任务时，先让接单者问风险与报酬，再允许新信息反转选择。
- anti-inference：不能推出角色面对材料都应拒绝；拒绝在此依赖既有价值判断。

## RES-GM-09

- evidence_id：RES-GM-09
- chapter：第二百三十六章《更好的选择》
- source lines：39698–39723
- anchor：`两天筹集资金`
- scene posture/type：高阶配方的多资产配置。
- scene goal：面对高价目标，决定保留、出售还是调动已有资产。
- pre-state：买方已积累战利品，却发现目标价格高于可自由支配现金。
- Evidence：角色先把获得战利品与高价目标放在同一尺度，再逐件排除不可卖物：主材料、身份风险物、联络物、补短板物、消耗品均各有用途或代价。最终不是立刻付款，而是承诺价格并争取筹资时间。
- expanded beats：仅展开真正可被出售、且每一件都带不同后果的资产。
- compressed/omitted beats：不对所有库存逐一估价。
- state-changing exchange：想买配方 → 发现现金不足 → 形成两日筹资承诺。
- opponent/other-character reaction：对方给出高价；角色的内部筛选替代了冗长讨价还价。
- body/space/detail selection：贴身口袋、面具、长桌上被具现的物品，帮助读者跟住“可卖/不可卖”。
- ruler/reader model：资产盘点应只展示会改变决策的保留理由。
- stop point：筹资期限确认后停，不提前解决钱从哪里来。
- Interpretation：资源稀缺能把“拥有很多”改写成“没有可动用的”。
- transfer observation：高价目标戏应让至少两种资产因不同理由被排除，最后才给出筹资动作。
- anti-inference：不适用于角色资产本就单一的场景；那时直接写一条主要取舍更有效。

## RES-GM-10

- evidence_id：RES-GM-10
- chapter：第一百一十五章《克莱恩的方案》
- source lines：52602–52611
- anchor：`不能这么自大`
- scene posture/type：材料目标的期限与路线规划。
- scene goal：将“钱不够”转为受边界约束的获取计划。
- pre-state：角色距晋升目标有数月，持有不少资产，也有危险但可获利的环境。
- Evidence：他估算现有资产、补齐主材的时间和出售特性的可能，却马上排除把高风险目标当作“移动赏金”的自大想法；随后转向借用、购买情报和委托第三方的方案。
- expanded beats：只保留资产、期限、主材缺口与风险排除。
- compressed/omitted beats：不计算每一笔海上收益。
- state-changing exchange：有资产但钱不够 → 不莽撞猎取 → 转为多步、低暴露的渠道调查。
- opponent/other-character reaction：无现场对手；既有危险认知构成对主角乐观估价的反制。
- body/space/detail selection：身体前倾、腰背微弓后再次思索，使计划不是轻松的数值推演。
- ruler/reader model：资金充足与安全可得是两件事；资源规划要把风险上限写进计划。
- stop point：第一条可执行路线出现后，转入下一场。
- Interpretation：数字在这里负责限制“可以做什么”，不是证明主角多富。
- transfer observation：当角色用总资产判断可行性时，紧接一个不可碰的风险边界。
- anti-inference：不意味着每个材料缺口都要拆成五步计划；只有替代路径本身构成悬念时才展开。

## RES-GM-11

- evidence_id：RES-GM-11
- chapter：第十二章《卖出》
- source lines：64682–64704
- anchor：`沉重财政压力`
- scene posture/type：大额跨币种交易。
- scene goal：用一次出售缓解身份维持与债务压力。
- pre-state：卖方需要筹集特定货币履约，同时维持高消费伪装身份。
- Evidence：卖方先报现金价，再为不吓退买方改为“现金+硬通货”的折价组合；买方依据组织用途与自身筹资能力还价，双方成交。成交后，叙事只点出债务、雇员、马车、礼物、舞会等持续身份成本，而不列明全部账目。
- expanded beats：报价变化、买方筹资能力、卖方持续支出压力。
- compressed/omitted beats：具体仆役工资、礼物和酒水逐项金额均省略。
- state-changing exchange：单一高价 → 混合支付成交；资产入账 → 暂缓但未消除身份成本。
- opponent/other-character reaction：买方默算、承认筹资不轻松，但因组织收益接受。
- body/space/detail selection：沉默数秒、成交后的松气、克制揉额头的动作。
- ruler/reader model：大额数字需要用“为何此人仍觉得不够”的持续义务校准。
- stop point：现金压力被暂时缓解、第二件货物开始展示时停。
- Interpretation：货币形式、流动性与身份成本，能让“有钱”仍保持紧迫。
- transfer observation：大额交易可只写一项付款结构变化和一串用途类别，不必写全账。
- anti-inference：不适用于一次性、无后续义务的纯奖励；那类场景不应强塞财政焦虑。

## RES-GM-12

- evidence_id：RES-GM-12
- chapter：第十三章《知识等于金钱》
- source lines：64707–64728
- anchor：`没有必要`
- scene posture/type：神奇物品的适配性筛选。
- scene goal：证明价格高低不能替代“是否适合我”。
- pre-state：卖方急需现金；多位潜在买家刚经历大额交易。
- Evidence：买方先按预警能力、攻击需求、负面作用与自身路线判断物品不合适，再听到价格后正式拒绝；其他人的复述与停顿放大金额，却没有改变她的决定。卖方随即改卖较低价、与买方知识需求匹配的物品，才激发购买意愿。
- expanded beats：功能、负面、角色需求、价格和群体反应。
- compressed/omitted beats：不展开物品全部历史或买家所有财产。
- state-changing exchange：高价物品无人购买 → 卖方换品；较低价且适配的知识得到回应。
- opponent/other-character reaction：旁观者被数额震住；买方拒绝后，另一件更匹配的物品形成新交易。
- body/space/detail selection：咬唇、短暂停顿、寒意等身体反应，让价格具备现场压力。
- ruler/reader model：价格应推高“值不值”的判断，不能取代它。
- stop point：买方明确想要更匹配的物品后停。
- Interpretation：一个昂贵资源被拒绝，往往比顺利成交更能显示价值体系。
- transfer observation：每次报价前先给角色一条具体适配/不适配理由；只报价格的拒绝不够。
- anti-inference：并非价格越低越会成交；此处成交来自需求匹配，不是降价本身。

## RES-GM-13

- evidence_id：RES-GM-13
- chapter：第五十章《周六晚上》
- source lines：67697–67708
- anchor：`只剩最后五片`
- scene posture/type：危险行动前的消耗品配置。
- scene goal：让有限工具决定行动窗口与隐蔽安排。
- pre-state：角色已用多次符咒定位目标，剩余次数有限，准备秘密调制魔药。
- Evidence：先写符咒已接近用尽及需补货，再写 130 镑购得的麻醉气体；该气体并未用来展示价格，而被用于安排夜间值守、逐舱释放、排除旁观者，然后才进入水下行动。
- expanded beats：剩余次数、已验证效果、为何必须夜间秘密使用。
- compressed/omitted beats：不重述每次符咒的购买和使用历史。
- state-changing exchange：消耗品存量接近底线 → 采取一次高风险行动并安排补货。
- opponent/other-character reaction：船员被布置与麻醉，未被赋予冗余对白；环境与目标怪物承担后续反应。
- body/space/detail selection：深夜甲板、船舱门、密封罐和水下服，将资源转成操作步骤。
- ruler/reader model：消耗品价格值得写，是因为其“已验证、剩余少、此刻必须用”三者同时成立。
- stop point：资源部署完成、角色下水后停。
- Interpretation：可消耗资源不必反复报账；只需在耗尽前的一次关键使用中显影。
- transfer observation：消耗品首次或临界使用，写存量、效果证据与使用后的行动窗口。
- anti-inference：若耗材可无限补充或不影响行动，剩余量不应被戏剧化。

## RES-GM-14

- evidence_id：RES-GM-14
- chapter：第四十八章《前奏》
- source lines：84418–84449
- anchor：`前期调查`
- scene posture/type：分段委托与情报采购。
- scene goal：以付款结构换取一个可用的调查网络。
- pre-state：委托人需要危险目标的情报，且线索标准暂不清晰。
- Evidence：起初给出高额跟踪赏金和预付款；当信息商指出条件过宽，委托人改为“基础调查费 + 每条有效信息加价”。信息商用基础款能雇多少人、维系多少依附者来判断任务可接；委托人交钱时又显露个人储蓄下降。
- expanded beats：预付款、有效信息的后付结构、调查网络的实际成本。
- compressed/omitted beats：不列出每位线人的工资或每条无效信息。
- state-changing exchange：模糊委托 → 可执行的分段合同；现金离手 → 情报网络开始运转。
- opponent/other-character reaction：信息商先质疑定义，后因基础款可覆盖网络运行而接受；委托人以信誉取得裁量权。
- body/space/detail selection：拥挤酒吧转入无人桌球室、数钞票、收钱前的停顿。
- ruler/reader model：信息的价格要写成“谁先承担搜寻成本、谁定义有效”，而非单一悬赏数字。
- stop point：预付款交割、双方责任明确后停。
- Interpretation：分段付款能把模糊信息需求变成可追踪的场景发动机。
- transfer observation：情报委托优先明确基础成本、验收权与增量回报三者中的至少两项。
- anti-inference：不适合结果可立即验证的简单跑腿；那种任务只需一次性报酬。

# Cross-Window Findings

1. 数字只在它改写当前选项时值得展开：买不起转为压租、现金不够转为筹资、报价不适配转为拒买。否则数字只会变成设定噪音。
   Evidence：RES-GM-01、RES-GM-05、RES-GM-09、RES-GM-12。

2. “资源稀缺”应优先落为取得权、流动性或风险上限，而不是一味写余额低。高薪仍受材料配额限制；总资产充足仍不能安全获得主材；手中物很多仍未必可出售。
   Evidence：RES-GM-02、RES-GM-07、RES-GM-09、RES-GM-10。

3. 价格的读者刻度来自角色熟悉的生活参照和现场反应，而非作者解释汇率。工资周期、家庭储蓄、身份消费、旁观者停顿，都会把数字转为可感的社会重量。
   Evidence：RES-GM-01、RES-GM-03、RES-GM-06、RES-GM-11、RES-GM-12。

4. 资源配置最有戏的部分常是“为什么不花/不卖/不接”，不是获得本身。被保留的资产、被拒绝的危险物、被拒绝的任务，都会让资源反照人物边界。
   Evidence：RES-GM-07、RES-GM-08、RES-GM-09、RES-GM-12。

5. 仪式与情报的成本应写成可执行条件：前者是材料—环境—风险的组合，后者是预付款—验收权—网络动员的组合。两者都不需要材料目录或人工清单。
   Evidence：RES-GM-04、RES-GM-13、RES-GM-14。

# Counterexamples & Boundaries

- 并非所有仪式都要强调昂贵。RES-GM-04 中，能力与象征匹配可减少辅助品；应写的是不可省的条件，而不是把仪式强行写成烧钱。
- 并非高价必然带来成交。RES-GM-12 中昂贵物品因功能、负面与买方需求不匹配被拒绝；价格只能加压，不能代替适配性。
- 并非资源不足都要制造互害。RES-GM-03 中家庭成员对资金的不同安排增强了温度和隐秘压力，没有转为争吵。
- 并非所有收入场景都要展开预算。若钱只用于交代人物状态、后续没有选择或他人反应，应压缩为一句背景。

# What Existing Skill Misses

现有 `resource_economy` 已覆盖重新估值、机会成本、竞争者反应与“获得后可做什么”。本轮真正新增的判断能力是：

1. 数字的“参照系选择”：先判断此人会拿工资周期、家庭存款、同阶身份、还是组织用途来理解价格；没有参照系的价格不进入正文。见 RES-GM-01、06、11。
2. 资源的双账本：家庭可见资金、秘密储备、身份维持成本不能混成一个余额；其分离本身会改变关系与行动。见 RES-GM-03、05、11。
3. 制度性稀缺：资源戏要区分钱不够、配额不够、渠道不够、可出售资产不够。现有 Skill 偏“估值”，未明确要求先诊断缺口类别。见 RES-GM-02、07、09。
4. 仪式材料的功能性筛选：材料、空间、时机、能力是同一成本包；只展开替代、缺失或误用会改变结果的项。见 RES-GM-04、13。
5. 委托付款结构即场景动作：预付、验收权、增量报酬会决定谁承担不确定性、谁愿意调动网络。见 RES-GM-14。

# Candidate Transfer Rules

1. **价格参照规则**
   - applicability：角色首次面对会改变去留、购买或身份处境的价格。
   - rule：只给一个角色熟悉的参照物，再让他立即做出可见选择。
   - stop rule：选择已落定后，不继续推演全套收支。
   - failure pattern：连续报工资、房租、物价，却没人改变计划或态度。

2. **先判稀缺类型规则**
   - applicability：角色“有资源却办不成事”时。
   - rule：先标定缺的是现金、流动性、配额、渠道、时间或安全边界中的哪一项；随后只写该缺口如何迫使换路。
   - stop rule：新路线已形成即可切场。
   - failure pattern：把制度配额、交易渠道和余额不足全写成泛泛的“缺钱”。

3. **仪式成本包规则**
   - applicability：仪式、制作、配方调制、召唤等准备场景。
   - rule：每个展开的物件必须对应结果、环境、隐蔽、成功率或风险边界中的一项。
   - stop rule：读者已能判断为何这次不能随便替代或省略时停止列物。
   - failure pattern：器材名称越列越多，但撤掉任一项都不影响人物选择或结果。

4. **公开钱与私下钱分离规则**
   - applicability：资源涉及亲属、同伴、组织身份或秘密目标。
   - rule：让一笔钱至少面对两个互斥用途，并让公开配置留下关系反应，私下配置改变后续行动。
   - stop rule：两条用途均已造成具体后果。
   - failure pattern：秘密资金只作为万能后备金，从不影响信任、时间或行动。

5. **高价目标延迟成交规则**
   - applicability：角色有多个资产、想获得高价值目标。
   - rule：只检查会真正改变决定的两三件可动资产；每件给出一个保留/出售后果，再明确筹资期限或放弃。
   - stop rule：资金缺口与下一步动作清楚后停止盘点。
   - failure pattern：把库存完整清单当作紧张感，或让角色无代价地突然筹足钱。

6. **情报付款拆分规则**
   - applicability：目标模糊、搜寻成本高、需要第三方网络的委托。
   - rule：用基础成本启动行动，用结果定义或增量奖励处理不确定性，并让双方争一次“谁判定有效”。
   - stop rule：预付款、责任与验收权足以启动调查后停。
   - failure pattern：高额悬赏直接解决模糊任务，信息商和执行网络没有行动理由。

# Source Fidelity Audit

- 已纳入的 14 个窗口均以 GB18030 解码后的绝对行号复核；未使用网络资料或模型补充情节。
- 章号存在分卷重置，故本报告不将重复章号误当作唯一 locator；所有证据以 `chapter title + source lines` 为准。
- 未纳入的候选：

  - 第六十六章《魔女教派》5957：有收入与消费，但只是一次庆祝性购买，缺少后续资源选择。
  - 第九十一章《解决》8331：工资比较主要用于社会背景说明，窗口内未形成资源决策。
  - 第一百八十章附近 22633：仅有稀有物价格区间，未见完整交易、选择或状态变化。
  - 第一百二十九章附近 53882：涉及 700 镑计划，但本次复核窗口不足以确认其完整资源交换后果，排除。
  - 第九十六章《夜的乐章》71162：筹集 8000 镑只构成角色反应，未形成足够完整的选择链，排除。
  - 第一百四十一章附近 92022：5000 金镑费用为背景信息，缺少可迁移的场景级交换。
- 因此未把“有数字”本身当作证据；所有 Cross-Window Findings 仅由上述 14 个窗口支持。
