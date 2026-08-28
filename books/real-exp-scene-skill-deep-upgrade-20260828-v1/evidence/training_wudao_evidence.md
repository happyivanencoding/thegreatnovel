我会按“原著定位—窗口取证—现有 Scene Skill 对照”来做；将使用 `distill-novels` 约束来源可追溯性，并读取当前 `novel-scene-skills` 的既有能力，以避免把泛化建议误报成新增结论。已确认原著为 GBK 编码、共 67,825 行且有多卷章节重置；当前已锁定跨早中晚期的 13 个候选窗口。核心不是收集“苦练成功”，而是核对每次展开是否真的改变了下一拍、是否由身体/他人/实战给出可比较回馈。# Source

- source_id：`WDZS-LOCAL-GBK`
- 原著：《武道宗师》
- 本地路径：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\小说整理合集\01_玄幻\武道宗师.txt`
- 编码：GBK；共 67,825 行。
- 注：全书存在分卷后章节号重置；以下以“章节标题 + 源文件行号”作为唯一 locator。

# Research Question

研究 Training / Learning / Comprehension 如何通过即时错误、身体变化、比较 ruler、他人反应与下一目标，写成有状态变化的场景；识别应压缩的重复训练，并区分“领悟出现”“局部能用”“压力下可调用”“可稳定迁移”。

# Evidence Windows

## `TW-01`

**Evidence**

- chapter：第009章《雷部绝学》；source lines `690–739`。
- scene posture/type：首次训练／差异诊断。
- scene goal：从静桩中获得可用的身体感知，而非直接获得力量。
- pre-state：主角杂念多、站桩不稳；同场成员身体和基础不同。
- expanded beats：第一次失败后改用与自身特殊条件相关的观想；重心移动时发现发力不是孤立动作，而有连续传导；教练巡视时对不同成员分别判断卡点。
- compressed/omitted beats：首次训练只进行有限时长，没有把长期站桩逐次展开。
- state-changing exchange：训练后的险跌中，他凭刚得到的重心感知调整站稳；随后力量房测试否定了“特殊条件直接提升蛮力”的猜测。
- opponent/other-character reaction：教练的作用是诊断不同人的当前可练内容，不是统一授课。
- body/space/detail selection：重心、脚下传导、失衡边缘；训练场与力量房构成两个不同 ruler。
- ruler/reader model：能站住不等于力量变强；新感知还须接受边界测试。
- stop point：第一次可辨认的身体变化和一次反证均已出现。
- transfer observation：首练应让读者看见“得到什么”与“没有得到什么”。
- anti-inference：不能据此推出所有新手都需要特殊观想或设备测试。

**Interpretation**

本窗支持“群体训练可以以差异诊断建立起点”，但“偏差—调整—比较结果”本身已被现有 `training_learning` 覆盖，不应把它重复算作新增能力。

## `TW-02`

**Evidence**

- chapter：第013章《这日子没法过了》；source lines `934–954`。
- scene posture/type：初次对抗纠错。
- scene goal：把空练动作变成能应对他人攻击的反应。
- pre-state：主角只盯着对方拳头，仍按普通人的闪避习惯行动。
- expanded beats：第一次被下绊；第二次因同时预演多个选项而反应迟滞；同伴把错误归因到“可被对手利用的空档”与临战犹豫。
- compressed/omitted beats：没有展开大量回合，只保留两种不同错误。
- state-changing exchange：失败的原因从“我反应慢”变成可修正的注意分配与应对习惯问题。
- opponent/other-character reaction：对练者实际完成的下绊，是比讲解更强的反馈；同伴随后命名错误类型。
- body/space/detail selection：视线、重心、被攻击的空档和来不及动作的时间窗。
- ruler/reader model：ruler 不是空练时动作正确，而是对手能否抓住其间隙。
- stop point：错误模型已明确，下一目标转为把常见局面练成反应。
- transfer observation：对抗训练的反馈最好落在对手真正利用了什么。
- anti-inference：这不是“新手都该立刻自由对练”的论据；`TW-08` 与 `TW-09`给出相反边界。

**Interpretation**

本窗的新增价值在于把“可调用性”单列：能做出动作，不等于在对手、时间窗和压力下用得出来。

## `TW-03`

**Evidence**

- chapter：第040章《有缘千里来相会》；source lines `3130–3137`。
- scene posture/type：由套路复现转为情境重组。
- scene goal：把已学的固定分组，转为针对假想敌的自由调用。
- pre-state：动作原先被分组和固定顺序组织，适合初学快速掌握。
- expanded beats：观看比赛后带着具体对手想象演练；先拆散组内顺序重组，再完全按假想敌招式取用；过程从杂乱到重新形成整体。
- compressed/omitted beats：未逐式讲教学原理，也不逐一复盘每个组合。
- state-changing exchange：练习结构本身改变——从“照组完成”变为“按外部威胁调用”。
- opponent/other-character reaction：无现场对手；假想敌承担了外部约束。
- body/space/detail selection：不同拳脚连续衔接、风声与疲劳恢复。
- ruler/reader model：读者可比较“依顺序完成”与“能按敌方选择”的能力层级。
- stop point：动作已形成可辨认整体，停止继续演示组合。
- transfer observation：当问题改为应对变化，入门顺序应从脚手架退场。
- anti-inference：基础动作尚不稳时，不该直接拆掉脚手架。

**Interpretation**

这支持一个现有 Skill 未明说的切换判断：训练目标从“复现”变成“回应外部条件”时，scene 应换用情境重组，而不是继续加量重复原套路。

## `TW-04`

**Evidence**

- chapter：第160章《我来》；source lines `13285–13326`。
- scene posture/type：伤后复训／局部试错。
- scene goal：在右臂刚恢复、仍脆弱的前提下，让新技法首次入门。
- pre-state：主角有一次被动经验，但尚不能主动稳定复现；伤臂不能贸然承压。
- expanded beats：先以既有桩功、套路和热身恢复身体控制；初次新技法失败，错误落实为肌肉紧度、压缩程度与节奏；重复尝试排除错误；最后出现空气波纹与反向震荡。
- compressed/omitted beats：数日练量与大量相同失败被概述，不逐次叙述。
- state-changing exchange：失败不是“没学会”，而是逐步排除错误、确认门槛已跨过。
- opponent/other-character reaction：导师旁观、偶尔点出关窍；最终认可入门，同时警告伤臂风险。
- body/space/detail selection：手部至肩背的肌肉链、腰背中转、汗、右臂不适与湖边训练地。
- ruler/reader model：首次成功的 ruler 是可见效果加身体反应，不是抽象等级。
- stop point：确认“入门”，并把下一个目标明确为熟练后再实战。
- transfer observation：高风险技法前先恢复可控身体状态；错误要落到一项可调参数。
- anti-inference：不应把超常恢复能力当常规训练强度的依据。

**Interpretation**

“具体偏差—调整—下一次比较”已有覆盖；本窗真正可补的是身体可用性 gate：当前身体尚未承载时，先训练恢复控制，不用新招硬顶。

## `TW-05`

**Evidence**

- chapter：第161章《五连击》；source lines `13378–13445`。
- scene posture/type：低风险实战验证。
- scene goal：验证刚入门的技法能否在动态对抗中连贯调用。
- pre-state：新技法刚入门，右臂仍须保守使用；对手力量占优。
- expanded beats：对手冲锋制造真实压力；主角以首次冲撞检验新技法，再根据对方震荡迟滞追击；连续攻击推动对手从能硬抗变为脚步虚浮。
- compressed/omitted beats：不展开完整竞技赛程，只保留验证连击上限的关键交换。
- state-changing exchange：技法从静态入门，变成能在对手主动反抗中造成连续效果。
- opponent/other-character reaction：对手从惊讶到主动化解，再到难以出声；其反应持续校准技法效果。
- body/space/detail selection：青砖裂痕、双臂承载差异、气血翻涌、每一击后的迟滞。
- ruler/reader model：真正的 ruler 是对手能否抵消、技法能否在压力和体力消耗下衔接。
- stop point：对手已失去稳定反击能力，主角也主动收手。
- transfer observation：入门后的第一场验证不必赢得正式比赛，但应让对手把“哪里有效、哪里仍有限”打出来。
- anti-inference：一次切磋不能证明该技法已适用于所有敌人或正式高压场景。

**Interpretation**

本窗与 `TW-04` 共同支持 proof ladder：入门 → 可重复 → 低风险对抗调用，而非把第一次成功直接写成完全战力。

## `TW-06`

**Evidence**

- chapter：第212章《施老头的教诲》；source lines `18226–18239`。
- scene posture/type：赛前焦躁训练／导师否决。
- scene goal：在临战前获得新杀招。
- pre-state：两种训练模型互相排斥，主角急于在比赛前补足短板。
- expanded beats：尝试连接两种模型、反复感到排斥和焦躁；导师不继续给步骤，而是问：对手是否会等待其准备完成。
- compressed/omitted beats：之后的长期适应被省略，场景不强行制造赛前成功。
- state-changing exchange：目标从“赶紧学会”转为“不要把刚入门能力当比赛依赖”。
- opponent/other-character reaction：导师用对手会如何打断的预判，替代空泛的风险警告。
- body/space/detail selection：排斥感、心浮气躁、短暂准备时间与对手的攻击时间窗。
- ruler/reader model：刚能做出，不等于对抗中有机会调用；不熟练招式还可能反伤使用者。
- stop point：不让训练在虚假成功中结束，而是在能力边界明确后收束。
- transfer observation：对抗型能力要以敌方干扰和准备时间判定可用性。
- anti-inference：不能将其泛化为“赛前绝不尝试新方法”；这里只是否定把未稳定招式当胜负依赖。

**Interpretation**

这是“练得出”和“战场可用”必须分开的强证据。

## `TW-07`

**Evidence**

- chapter：第004章《利益当头》；source lines `19773–19782`。
- scene posture/type：导师交棒／自主探索启动。
- scene goal：为下一阶段领悟建立必要前提和探索边界。
- pre-state：主角刚完成前一身体阶段，急于获得下一阶段的具体练法。
- expanded beats：导师指出必须先达到整体身体条件；给出少量辨认锚点；明确人物路线含自身特殊条件，不能照搬别人路径。
- compressed/omitted beats：不解释完整方法，不代劳后续体悟。
- state-changing exchange：学习责任从导师讲授转交给人物的长期摸索；导师保留“遇到问题可再问”的边界。
- opponent/other-character reaction：导师拒绝继续细化，不是信息缺失，而是对阶段性质的判断。
- body/space/detail selection：整体劲力的统一性作为前置，而非抽象悟性。
- ruler/reader model：读者知道此刻还不具备直接攻克目标的条件。
- stop point：前提、辨认锚点和求助边界已交付。
- transfer observation：当答案必须与人物身体结构、长期路线结合时，导师应退场，而不是继续派发标准步骤。
- anti-inference：不能将“少教”合理化为无依据的故弄玄虚；本窗先给了明确前提与回访边界。

**Interpretation**

现有 Skill 已要求导师不要开场讲全套理论；新增判断是“何时应该有边界地退场”。

## `TW-08`

**Evidence**

- chapter：第010章《学员们》；source lines `20249–20291`。
- scene posture/type：初学者群训／课程门槛控制。
- scene goal：让不同身体条件的孩子获得基础姿势和负荷控制，而不是追求刺激。
- pre-state：成员年龄、体型、目标不同，部分只求强身或减重。
- expanded beats：教练先说明为什么不能直接学高阶内容；逐个纠正站姿；对出现颤抖者提前休息；在群体烦躁时切换到下一种基础内容；拒绝马上让零基础成员互练。
- compressed/omitted beats：不逐个展示十人的全部动作。
- state-changing exchange：课程从统一热情转为每个人有不同姿势、不同负荷和不同下一步。
- opponent/other-character reaction：孩子期待对练；教练明确指出早期对练会固化错误。
- body/space/detail selection：发抖、汗、姿势、脚踝至膝关节的发力；场地中逐个校正。
- ruler/reader model：是否进入对练不取决于无聊或兴奋，而取决于动作、负荷与错误成本。
- stop point：基础内容开始产生烦躁且新信息下降，转入下一项；对练延后。
- transfer observation：训练形式的升级，应由可维持的动作质量而非读者期待决定。
- anti-inference：不代表所有基础训练都必须冗长；该边界来自目标群体与错误会被互练放大的条件。

**Interpretation**

这是“课程准入”证据：错误会被新形式放大时，不能用更刺激的训练来解决无聊。

## `TW-09`

**Evidence**

- chapter：第015章《狐假虎威》；source lines `20780–20787`。
- scene posture/type：间隔后的复训／反证窗口。
- scene goal：检查上一课的基础姿势是否已成为稳定能力。
- pre-state：首次训练刚结束，孩子们表面上完成过基础桩功。
- expanded beats：隔天回训，十人中多数动作重新变形；教练必须再次讲解、再次纠正。
- compressed/omitted beats：不复述前一课全部教学内容。
- state-changing exchange：上一课的“做过”被降级为“尚未稳定”，下一步不是进阶而是重建基础。
- opponent/other-character reaction：无对手；复训结果本身构成反应。
- body/space/detail selection：动作标准度和隔日记忆，而非抽象努力程度。
- ruler/reader model：稳定能力至少要经间隔后保持验证。
- stop point：错误类型已重现，场景转入纠正与适当预期。
- transfer observation：首次成功不等于可升级；间隔后的再现可以是场景中更有价值的 ruler。
- anti-inference：不要求每次训练都跳时验证；只有决定开放下一层能力时，才需要这种证据。

**Interpretation**

本窗是 `TW-08` 的反证边界，支持“复现、间隔保持、错误成本”三项准入判断。

## `TW-10`

**Evidence**

- chapter：第026章《不靠谱的加油团》；source lines `21925–21945`。
- scene posture/type：部分领悟后的首次功能证明。
- scene goal：证明新领悟是否已经改变身体调用方式，同时保留未完成限制。
- pre-state：距离完整状态仍差长期水磨；能力尚不能脱离特殊支点完整运行。
- expanded beats：身体整体贯通；收缩、维持、爆开；一次出拳让湖面出现可见波动；随后立即说明仍欠缺完整条件。
- compressed/omitted beats：长期水磨只以未来时间估计带过。
- state-changing exchange：能力从纯内部体悟变成一次可见输出，但不能被宣告为完整突破。
- opponent/other-character reaction：无直接对手；湖面波动与身体疲竭是外部、内部双 ruler。
- body/space/detail selection：肌肉、筋膜、骨骼贯通；湖面、风和气流承担效果显示。
- ruler/reader model：局部功能出现 + 明确未稳定缺口。
- stop point：第一次功能已成立，下一目标转为不依赖特殊支点继续打磨。
- transfer observation：一次领悟可先兑现为“部分成立”的 payoff，不必立刻命名、升级或全能。
- anti-inference：局部可用不是完整境界证明。

**Interpretation**

现有 `payoff_realization` 仅是 Utility 名称，缺少“首次功能证明—限制保留—下次验证目标”的可执行结构。

## `TW-11`

**Evidence**

- chapter：第049章《触类旁通》；source lines `42861–42883`。
- scene posture/type：领悟受阻后的换模试验。
- scene goal：从目标图谱中抓住难以稳定的核心感受。
- pre-state：主角已有积累，但被两种互相干扰的感受打断，越练越急。
- expanded beats：先停止直盯目标，平复状态；调用已经掌握的身体调整和观想作为引子；试验产生可见爆发；后续仍多次失败，却确认了正确方向。
- compressed/omitted beats：后续水磨不再逐次描写。
- state-changing exchange：失败从“没有收获”转为“已得到可追踪的路径”。
- opponent/other-character reaction：旁观者对意外爆发与外部影响作出反应，迫使人物转移到更合适地点继续。
- body/space/detail selection：急躁、平复、肌肉和脏腑状态、短暂失控的火焰。
- ruler/reader model：是否成功不只看成招；能否留下可重复追踪的局部结果同样重要。
- stop point：人物已确认方法方向，剩下无新信息的失败压缩为水磨。
- transfer observation：若失败改变了下一次可操作的路径，它不是空失败。
- anti-inference：一次有反应的试验不等于能力已稳定；本窗明确保留反复失败。

**Interpretation**

这是“部分成立”与“可常规调用”要分层的强证据。

## `TW-12`

**Evidence**

- chapter：第105章《说话算话》；source lines `29635–29673`。
- scene posture/type：跨媒介领悟／即时他证。
- scene goal：让难以形成神韵的字符观想，转化为稳定的内练与外用。
- pre-state：单纯观想反复失败，无法形成目标神韵。
- expanded beats：先确认发音；纯观想无效；提出“声音能否反向制造神韵”的假设；声、意、身体反应联动后重新观想成功；再以外用影响同室者的疲劳感。
- compressed/omitted beats：连续记忆和重复内练只保留结果。
- state-changing exchange：理解从视觉符号，转成可由声、意、身共同调用的模型。
- opponent/other-character reaction：同伴先困倦，后精神骤振；其身体变化给出非主角自证。
- body/space/detail selection：腹部、声带、精神状态、寝室栏杆与同伴的疲倦。
- ruler/reader model：领悟不仅是“看懂”，而是能让自身与他人的即时状态出现变化。
- stop point：最低限度现实反馈已发生，后续进入记录和熟练。
- transfer observation：抽象领悟可借不同感官通道交叉试验，并用他人体验完成最小证明。
- anti-inference：旁人一次反应不足以证明方法对所有人安全、有效或可教学。

**Interpretation**

本窗补强“领悟之后能做什么”的证明方式：不是解释更多，而是让新模型产生一个之前不能造成的现实结果。

## `TW-13`

**Evidence**

- chapter：第110章《总不让人省心》；source lines `48320–48350`。
- scene posture/type：多路径失败后的局部功能输出。
- scene goal：从高阶图谱中寻找可推进的理解。
- pre-state：直接参悟无效；两种基于物理设想的尝试均失败。
- expanded beats：补读文字、图谱和前人笔记；尝试两种模型失败；转而用人物自身已掌握的平衡状态模拟目标；借外力完成一次明显更强的效果。
- compressed/omitted beats：重复取暖、反复失败等用概述处理。
- state-changing exchange：一次输出能形成特殊现象，但立刻消失且造成明显脱力。
- opponent/other-character reaction：进入者看到其状态不佳，劝其停止；外部反应没有把局部成功误读为稳定掌握。
- body/space/detail selection：严寒、颤抖、身体透支、短暂冰晶现象。
- ruler/reader model：可见输出 + 持续时间极短 + 代价明确。
- stop point：人物提出“不借外力能否推进”的下一问题，不继续虚报掌握。
- transfer observation：局部功能证明可成立，但应同时留下稳定性、代价和依赖条件。
- anti-inference：不能把“曾经做到一次”直接兑现为常规战力。

**Interpretation**

与 `TW-10`、`TW-12` 共同支持：部分成功应被承认，但不能被升级为稳定掌握。

## `TW-14`

**Evidence**

- chapter：第031章《极地实验室》；source lines `56514–56534`。
- scene posture/type：环境变量训练。
- scene goal：在可观察、可退出的严寒环境中测试人与环境的连接。
- pre-state：第一次进入该设施，对环境阈值和自身反应均未知。
- expanded beats：进入预设低温；身体立即产生不同感受；由静态体悟转为风雪中的招式演练；外部观察者、监测数据和时间共同确认状态。
- compressed/omitted beats：数小时中的大量重复演练未逐招展示。
- state-changing exchange：训练后不是泛泛“变强”，而是主角依据现场状态提出下一次更低温的具体参数。
- opponent/other-character reaction：观察者从担心到震动；监测人员以数据确认其没有异常。
- body/space/detail selection：刺骨低温、呼吸受限、风雪、湿衣、密闭空间、观察窗和控制面板。
- ruler/reader model：环境是可调训练变量；升级由此次身体和现场反馈决定。
- stop point：下一轮参数已具体化，结束当前环境体验。
- transfer observation：环境训练可让空间与监测承担 ruler，而不是依赖旁白报进度。
- anti-inference：不是通用“加大环境刺激”的公式；须满足错误后果可承受、可观察、可停止。

**Interpretation**

现有 Skill 只笼统允许不同环境；本窗支持把环境作为可被结果调节的训练变量。

## `TW-15`

**Evidence**

- chapter：第037章《正式签约》；source lines `57101–57103`。
- scene posture/type：高风险环境的准入否决。
- scene goal：判断人物能否进入更高温、更高错误成本的训练设施。
- pre-state：人物想进入火部高温环境，但相关能力还未基本入门。
- expanded beats：教练直接禁止；说明高温错误发生极快、当前无法及时纠正；给出先练稳基础、后逐步适应的路径。
- compressed/omitted beats：不展开设施训练本身，因为进入条件尚未满足。
- state-changing exchange：目标从“马上尝试高温”改为“先完成基础能力”。
- opponent/other-character reaction：导师以即时致命的错误成本作判断。
- body/space/detail selection：高温、瞬时失控、无法救援的后果。
- ruler/reader model：不是人物胆量，而是错误是否还来得及被发现和纠正。
- stop point：准入被否决、先决条件明确。
- transfer observation：若反馈不能在场内被承受或修正，应停留在低风险练法。
- anti-inference：不能把此门槛泛化到所有环境；严寒窗口在可监测、可退出条件下允许渐进试验。

**Interpretation**

`TW-14` 与本窗构成边界：环境递进不是刺激升级，而是由可观察性、可纠正性和错误成本决定。

## `TW-16`

**Evidence**

- chapter：第143章《寒假最后》；source lines `33439–33472`。
- scene posture/type：领悟后的迁移证明。
- scene goal：把刚获得的个人理解，迁移成另一人也可开始学习的媒介。
- pre-state：人物能短暂调用新能力，但尚不能把核心感受稳定外化。
- expanded beats：多种错误推演被排除；获得一次速度效果；随后以书写反复尝试保留核心感受；大量废纸后，找到能让外化媒介保留部分真意的方法。
- compressed/omitted beats：多次失败以材料消耗与时间跳跃概述。
- state-changing exchange：能力不再只是个人瞬时体验，而能被外化为有限、可转交的学习入口。
- opponent/other-character reaction：同伴先对即时速度效果震惊，后接受该媒介作为入门帮助。
- body/space/detail selection：高速移动、风声、手势、毛笔、废纸与最终成字。
- ruler/reader model：ruler 从“自己能发动”提高到“能否留下他人可用的部分”。
- stop point：外化媒介已足以让对方入门，但仍承认与完整原能力存在差距。
- transfer observation：领悟的更高一级证明可以是迁移，而非单纯更大威力。
- anti-inference：能教人入门不等于已完整复制原理，也不等于应把所有私人领悟都转授。

**Interpretation**

这为 Scene Skill v2 增加了可选的第四层 proof：稳定调用之后，才可能检验其是否能外化、迁移或被他人使用。

# Cross-Window Findings

1. **训练 scene 只展开会改变下一拍的尝试；已知关系成立后的同类重复应压缩。**
   `TW-03` 展开“固定组法→按假想敌重组”；`TW-04` 展开每次新错误；`TW-11` 展开换模后的首次局部结果；`TW-14` 用时间和空间状态压缩数小时演练。
   **判断**：压缩的条件不是“练了很多次”，而是“错误—修法—结果的因果已不再变化”。[TW-03, TW-04, TW-11, TW-14]

2. **训练反馈最有叙事价值的形式，是当前身体或对手实际暴露出的偏差。**
   重心与注意分配的错误可导致被绊倒或险跌；伤臂、颤抖、脱力、对手迟滞、环境数据都能给出不同粒度的反馈。
   **判断**：避免以“悟性不足”“练得不够”代替偏差；应指出失控发生在何处，人物据此改变何项动作或条件。[TW-01, TW-02, TW-04, TW-05, TW-14]

3. **“做得出”与“可调用”之间存在至少四层 ruler。**
   入门的身体反应、可重复的局部效果、压力下调用、可迁移给他人，分别由不同场景证明。
   **判断**：不需要每项能力走完全部四层；当前情节需要哪一层，就只写到该层。把一次成功跨写成全部能力，是失真。[TW-04, TW-05, TW-10, TW-12, TW-13, TW-16]

4. **部分成立也应有 payoff，但必须同时保留限制和下一验证目标。**
   湖面波动、短暂特殊现象、让他人疲劳消退，都能证明新理解开始工作；但依赖外力、持续时间短、体力代价和未稳定性必须在同一窗口留下。
   **判断**：不能因为未突破就把成果写成零，也不能把一次效果写成稳定能力。[TW-10, TW-11, TW-12, TW-13]

5. **导师的职责会随阶段变化：早期诊断与纠正，中段交付边界，后段以 ruler 否决错误目标。**
   **判断**：当答案仍可被观察修正，导师应具体指出；当答案依赖人物路线，导师应留下前提、锚点和求助边界；当人物把“刚入门”误认作战力时，导师应以真实对手或错误成本否决。[TW-01, TW-06, TW-07, TW-15]

6. **训练形式的升级必须先经过准入判断。**
   基础是否能隔日保持、错误会否被自由对练放大、环境错误是否可观察且可停止，决定能否升级。
   **判断**：读者期待更刺激的训练，不是升级理由；场内错误成本才是。[TW-08, TW-09, TW-14, TW-15]

# Counterexamples & Boundaries

- **不应把“对练”当作消除枯燥的默认升级。** 基础动作会被对抗放大且固化时，应先纠正；`TW-08` 禁止早期互练，`TW-09` 更显示首课完成不代表隔日稳定。

- **不应把“突然明白”直接写成可战斗能力。** `TW-06` 明确否决赛前刚入门招式作为胜负依赖；`TW-13` 的局部效果仍伴随外力依赖与脱力。

- **不应把环境强度机械上调。** `TW-14` 能升级，是因为状态可监测且可退出；`TW-15` 则因错误瞬时、难以纠正而禁止准入。

- **不应为了保留神秘而让导师完全不说。** `TW-07` 的导师虽退场，仍交付前提、辨认锚点和求助边界。

- **不应把首次成功写成长期稳定。** `TW-09` 的隔日变形与 `TW-11` 的反复失败均表明：间隔后保持、压力下调用是另一项证据。

# What Existing Skill Misses

现有 `training_learning.md:3–11` 已充分覆盖“具体偏差→调整→比较结果”“无新信息的重复压缩”“不把练熟自动当突破”。以下不把这些近义能力重复算作贡献。

1. **可用性 ruler。**
   现有规则要求实际执行证明进步，但没有明确审查：该执行是否需要对手配合、较长准备时间、外部支点，是否能在敌方干扰下调用。`TW-02`、`TW-05`、`TW-06`、`TW-13` 支持补入这一判断。

2. **从脚手架到情境重组的切换。**
   现有规则有“比较”和“复杂情境”，但没有规定何时废除入门顺序、改用外部威胁组织训练。`TW-03` 给出明确阶段转折，`TW-08`、`TW-09` 给出不能过早切换的边界。

3. **导师的有边界退场。**
   当前只说导师说明应绑定刚出现的问题；尚缺“方法必须依赖人物自身路线时，导师只给前提、辨认锚点与求助阈值”的退出判断。[TW-07]

4. **训练层级准入。**
   当前提及稳定复现，却未将“隔次保持”“错误是否会被新形式固化”“错误成本是否能在场内纠正”写成进入对练或高压环境前的 scene 判断。[TW-08, TW-09, TW-14, TW-15]

5. **部分成立的 payoff 结构。**
   根 Skill 将 `payoff_realization` 列为 Utility（`.agents/skills/novel-scene-skills/SKILL.md:53,69`），但 `scenes/` 中没有对应可执行文件。缺失的是：首次功能证明、限制/代价、下一验证目标、何时停止的完整结构。[TW-10, TW-11, TW-12, TW-13]

6. **领悟的迁移层证明。**
   当前 Skill 覆盖“新模型可解释或控制”；尚未区分“自己能发动”与“能否外化为他人可进入的学习媒介”。这应是可选的高阶 ruler，而非强制要求。[TW-16]

# Candidate Transfer Rules

1. **可用性分层 rule**

   - applicability：新技法、领悟或临时能力刚首次成功，且后续剧情需要决定能否上场。
   - rule：先标记当前成立层级：入门、可重复、压力调用、可迁移；只安排当前情节需要的下一层证明。
   - stop rule：一旦当前层级的 ruler 已给出，转入下一行动，不追加同层炫技。
   - failure pattern：一次静态成功后，直接按完整战力处理；或连续安排同类测试却不改变读者判断。

2. **训练准入 rule**

   - applicability：人物要求进入对练、自由重组、高压环境或更大负荷。
   - rule：检查动作是否能在间隔后保持、是否仍需即时纠正、错误会否被新形式放大、现场是否能观察和止损。
   - stop rule：任一关键条件不足，就明确下一基础目标，不让场景假装升级。
   - failure pattern：因人物无聊、旁人起哄或作者想加快节奏，就放开高风险训练。

3. **身体可用性 gate**

   - applicability：伤后恢复、疲劳、身体结构变化，或高风险招式依赖特定部位。
   - rule：先让人物通过既有低风险动作确认身体控制，再碰目标技法；反馈落在具体链条、节奏或承载部位。
   - stop rule：获得足以决定“继续、降级、换目标”的身体反馈即止。
   - failure pattern：用“已经痊愈”替代实际控制恢复，导致新技法只作为设定兑现。

4. **部分成立 payoff rule**

   - applicability：人物找到正确模型或打出一次新效果，但尚不能稳定复现。
   - rule：同时给出一次可见功能、一个明确限制或代价、一个下一验证目标。
   - stop rule：读者已能回答“它现在能做什么、还不能做什么、接下来验证什么”。
   - failure pattern：要么把未稳定成果写成完全失败，要么把偶发效果直接命名为稳定能力。

5. **导师交棒 rule**

   - applicability：学习瓶颈已不再是缺动作知识，而是人物路线、身体条件或长期意志的重组。
   - rule：导师提供前提、辨认锚点、不可跨越的边界与何时可回问；把探索权交回人物。
   - stop rule：人物明确知道当前不能照抄什么、该观察什么、遇到何种失败再求助。
   - failure pattern：导师继续讲成教程；或反过来只说“自己悟”，没有任何可执行锚点。

6. **环境变量 rule**

   - applicability：空间、气候、器械或特殊场地会改变训练对象本身。
   - rule：把环境作为可调变量，以现场身体反应、观察者或数据决定下一次参数；高错误成本环境先建立低风险基础。
   - stop rule：当前环境已经产生一项足以决定升、降或维持的反馈。
   - failure pattern：把环境强度单纯当“更难、更酷”的升级条，不交代可观察性和错误成本。

# Source Fidelity Audit

- 已纳入窗口均有本地 source line locator；未依赖联网信息、模型记忆或外部剧情摘要。
- 全书章节号会重置，因此没有只使用章号作为定位依据；复核应以本报告中的 source lines 为准。
- 明确排除：

  - 第100章《炙手可热》`47543–47559`：只有前辈电话指点，缺少同窗内练习、失败或结果证明，不能作为完整 Training/Learning window。
  - 第131章《各有奋进》`32311–32314`：虽能证明长期情绪磨炼的重要性，但主要是回顾性概述，不是可展开的现场 scene。
  - 第117章《再上征程》`30969–30985`：以赛后重振为主，训练动作与可比较结果不足，未纳入主证据。
  - 第013章《意志》`20613–20628`：提供“个人道路不能照抄”的方向性讨论，但没有在同一窗中完成可验证的能力变化，故未单独作为领悟成功证据。

- 因此，所有 Cross-Window Findings 只建立在至少三窗支持，或“两项直接强证据 + 一项反证边界”支持的结论上；未将计划、导师说法或单次偶发效果提升为普遍规律。
