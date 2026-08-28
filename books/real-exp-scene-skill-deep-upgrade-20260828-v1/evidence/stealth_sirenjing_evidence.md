我会按 Source-First 的方式直接从本地《死人经》取证，并对照当前 Scene Skill 找出真正缺失的判断能力；不会联网，也不会把模型记忆补进事实。为确保产物能追溯，我先读取小说分析与现有 scene-skill 的约束，再分段检索全书的高信号场景。已确认原著为 84,583 行、1,212 个章节标题，且通过 GB18030 解码建立行号；我把早中后段交叉检索，避免把同一段连续剧情误当成多份证据。当前的 v1 `stealth_infiltration` 已含“风险状态更新/暴露后转场”，但尚未明确“守卫的注意力如何被事件重分配、何时保留退出权、发现后怎样将控制权移交给下一场戏”这类可执行判据。我会把“第305章的两名少年混入后失踪”保留为反例，而非成功模板：它证明身份伪装能短暂过关，但路线失真、没有可验证的接应与退出状态时，潜入应立即转为救援/谈判问题，不能继续把它写成“仍在潜行”。取证口径已固定：只有能看到“一个具体痕迹/权限/守卫动作变化 → 人物下一拍改策 → 场景主问题转移或停止”的窗口才入选。单纯的夜行成功、旁观者概述或只有结果没有过程的刺杀，我会在最终审计中明确排除。我已要求各段检索先回传已核验的窗口，正在把重复功能的候选去重。例如“身份进门成功”与“撤离时暗哨注意、随后失联”不会被拆成两条独立证据；后一条才足以支持退出权与 handoff 的结论。已完成逐窗核验并保留 12 条：早、中、后段均有覆盖；其中第21、203、305、430、572、598、635、657、919、1164章构成主证据，第290、1155章补足“声音判别”和“城市掩护消失”的边界。下面按要求给出仅含可复核定位的 Markdown。# Source

- SOURCE BOOK：`死人经`
- SOURCE PATH：`C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\小说整理合集\07_武侠\死人经.txt`
- 编码与定位：以 `read_bytes()` 后按 `gb18030` 解码，并对解码文本 `splitlines()` 计行。
- SOURCE ID：`sirjing-01`
- RESEARCH LANE：`stealth_sirenjing`

# Research Question

潜入或刺杀前，身份、位置、声音、视线、守卫行为、退出权如何被少量现场证据更新；一旦被发现或任务性质改变，如何立即 handoff，而非重复潜行流程。

# Evidence Windows

## SC-01｜床下等待被目标的临时要求改写

- evidence_id：`SC-01`
- chapter：第0021章《床下》
- source lines：1571–1669
- scene posture/type：室内伏藏刺杀。
- scene goal：在不暴露藏身处的前提下，等待目标进入可刺杀位置。
- pre-state：人物藏在床下；同伴在外制造掩护；目标位置和到访时间不稳定。
- expanded beats：喷嚏险些发声；外部同伴以放大说话声覆盖；目标临时要求叫来本应在房内的潜伏者，直接威胁身份；人物一度准备在无法确认位置时冒险下手，随后因同伴把目标重新诱回床位而复位。
- compressed/omitted beats：重复等待、床下姿势调整、无新状态的忍耐被略过。
- state-changing exchange：目标要求把“欢奴”叫来，使“不在场”成为可核验的暴露点；同伴改变互动，将目标的位置重新锁回床上。
- opponent/other-character reaction：目标并未察觉床下人，却因自身警觉和临时欲望不断改变现场条件。
- body/space/detail selection：喷嚏、呼吸、床板缝隙、脚步落点与床上位置。
- Evidence：隐藏不是静止状态；一个本不该出现的点名就足以击穿身份掩护。anchor：“鬼鬼祟祟的”
- Interpretation：场景把“能否出刀”建立在“目标是否会验证人物不在场”上，而非单纯忍耐。
- ruler/reader model：读者持续追问的是：藏身者还能否维持“本该在别处”的身份，且是否还有可执行的攻击窗口。
- stop point：刺杀动作落地、目标死亡后，潜伏目标结束。
- transfer observation：把身份伪装写成可能被现场人物随手验证的缺口；验证一旦发生，下一拍应是改位、撤离或把目标引回可控位置。
- anti-inference：此窗不能证明每次潜伏都需要“险些打喷嚏”；关键是可被现场验证的异常。

## SC-02｜村落踩点、声音信号与迟滞撤离

- evidence_id：`SC-02`
- chapter：第0203章《村子》
- source lines：14191–14234
- scene posture/type：旁观式监视一支入村刺杀队。
- scene goal：判断敌方潜入方案并等待其行动后再介入。
- pre-state：敌方白日伪装过路客完成摸底；夜间分为入村、堵截、望风三类岗位。
- expanded beats：先遣者二次确认；入村者与望风者分工；监视者把呼吸融入虫鸣；屋内的轻微杀戮声使望风者误判任务完成；惨叫改变整个村庄的声场和人群行为；望风者迟到的撤退决定被封死。
- compressed/omitted beats：无新信息的夜间埋伏不展开。
- state-changing exchange：闷响先令望风者放松；惨叫令村民、伏兵和望风者同时更新局势。
- opponent/other-character reaction：守望者不是自动报警器；其反应迟滞直接造成退出权消失。
- body/space/detail selection：村墙距离、虫鸣、闷响、惨叫、土屋与两侧房屋。
- Evidence：白日身份可换来初始准入，但夜间声音会重置所有人对安全的判断。anchor：“抓活的”
- Interpretation：暴露不是“看到刺客”才开始；异常声音先改变守卫与旁人是否仍按日常逻辑行动。
- ruler/reader model：读者看的是：敌方能否在信息尚未统一前拿回出口。
- stop point：村民与伏兵完成合围，潜入流程结束，转为围捕。
- transfer observation：声音 detail 只在它改变守卫判断、出口或行动节奏时展开；守卫的迟疑也应带来后果。
- anti-inference：不能据此推出所有刺杀都应制造惨叫；本窗的声音升级来自陷阱反转。

## SC-03｜腰牌通过，不等于路线与接应成立

- evidence_id：`SC-03`
- chapter：第0305章《失踪》
- source lines：21125–21155
- scene posture/type：未经授权的身份混入，失败反例。
- scene goal：伪装成学徒进入石堡内宅并救出目标。
- pre-state：两名少年有衣着、腰牌和预设路线，但缺少对内部空间、接应和回撤的真实掌握。
- expanded beats：守卫检查腰牌后放行；守卫因当日确有学徒下山而降低警惕；两人经多个路口迷失；被暗处守卫拦下时，以强硬口吻索路；进入内宅后失联。
- compressed/omitted beats：计划文本本身不逐项复述。
- state-changing exchange：第一轮盘查通过；迷路暴露了“身份可过、位置不可控”；守卫给路并不等于安全。
- opponent/other-character reaction：守卫误把过度大胆视为“不像伪装者”，但后续机构没有因此承担即时可见的失败成本。
- body/space/detail selection：腰牌、学徒衣着、七八个路口、暗处守卫。
- Evidence：身份道具只解决第一道验证，无法替代空间认知与退出状态。anchor：“石沉大海”
- Interpretation：这是“准入成功、任务失败”的反例，而非潜入成功范本。
- ruler/reader model：读者随后追问的已是失联者在哪、谁控制了他们，主问题应转救援或谈判。
- stop point：二人进入内宅失联时，潜入场景必须停止。
- transfer observation：把“已通过门禁”与“仍拥有路线、接应、退出权”分开记录。
- anti-inference：不能仅因两人被放行，就断言守卫系统失效；文本保留了后续陷阱的可能。

## SC-04｜安全路线被看见后，监视者不抢戏

- evidence_id：`SC-04`
- chapter：第0430章《有事》
- source lines：29798–29805
- scene posture/type：反潜入监视。
- scene goal：通过敌方刺客的行动路径反查其巢穴与首脑。
- pre-state：军营持续遇刺；主角已布置暗哨，但尚未掌握敌方路线。
- expanded beats：主角模拟杀手如何选目标；发现三人沿“安全路线”进入；两人望风、一人入帐；刺客迅速撤离；主角不当场干涉，改由暗哨尾随。
- compressed/omitted beats：刺客具体如何穿过每一道营防未展开。
- state-changing exchange：刺客的路径与岗位分工成为新情报；主角把“立即救人”换成“保留跟踪链”。
- opponent/other-character reaction：刺客认为无事发生，照常撤离，正因此暴露其后续路线。
- body/space/detail selection：帐篷、望风人数、三更、延迟出现的惊呼。
- Evidence：守卫空隙对刺客是路线，对反制者则是可追踪的行为模式。anchor：“安全路线”
- Interpretation：本窗的有效动作不是拦截，而是延迟反应以换取更高价值的定位。
- ruler/reader model：读者知道眼前损失真实存在，却追问尾随能否触及更大目标。
- stop point：尾随启动后，场景转为追踪/反制。
- transfer observation：当场干预会毁掉更高价值情报时，明确写出人物放弃什么、换取什么。
- anti-inference：不适用于必须即时保护的目标；本窗以战争与更大目标为条件。

## SC-05｜唯一空档既是通道，也是邀请函

- evidence_id：`SC-05`
- chapter：第0572章《忠心》
- source lines：39582–39589
- scene posture/type：疑似陷阱中的主动潜入。
- scene goal：确认失踪者线索，并接触布置漏洞的一方。
- pre-state：目标营地已强化巡逻；人物知道夜闯本身可能成为对方处置自己的借口。
- expanded beats：发现高戒备中唯一可穿越的巡逻错身空档；识别其重复周期；判断这不是自然漏洞，而是专门留给自己的“晋见之路”；进入亮灯小帐。
- compressed/omitted beats：跨越通道的具体步数未铺陈。
- state-changing exchange：守卫轮换的短空档本身就是对人物的无声邀请。
- opponent/other-character reaction：布置者按人物过往风格设计路径；守卫行为在此承担传话功能。
- body/space/detail selection：一刻钟、两队互错、唯一通道、主帐附近亮灯。
- Evidence：当漏洞过于精准时，它不能再按普通潜入收益计算。anchor：“晋见之路”
- Interpretation：场景主问题从“能否潜入”立即改成“谁希望他进来、代价是什么”。
- ruler/reader model：读者应从空档的异常性先于进入动作感到风险。
- stop point：确认路径是人为设置并进入会面空间时，转接触/谈判/陷阱场景。
- transfer observation：把“异常顺利”设为状态更新，而不是奖励；它应触发意图判断。
- anti-inference：并非所有守卫漏洞都是陷阱；本窗有过度严密与唯一周期性缺口两项支撑。

## SC-06｜撤离时被暗哨注意，后果不再重演潜入

- evidence_id：`SC-06`
- chapter：第0598章《折磨》
- source lines：41475–41479
- scene posture/type：成功取物后的撤离失败边界。
- scene goal：进入王府取回物品并退出。
- pre-state：两人夜入王府，目标明确，原计划是迅速取物离开。
- expanded beats：取物过程顺利；撤退时暗哨注意到异常；巡夜卫兵尚未反应前，两人已离营；之后二人遭迷药、失散与拘押。
- compressed/omitted beats：取物细节、撤离路径和后续被制过程均未充分展示。
- state-changing exchange：暗哨注意是“成功取物”与“后续失联”之间唯一明确的暴露标记。
- opponent/other-character reaction：暗哨尚未来得及调动巡夜人，短期退出成功；更晚的风险并未因离营而消失。
- body/space/detail selection：三更、首饰匣、暗哨、巡夜卫兵。
- Evidence：退出营地不是风险清零。anchor：“引起一名暗哨”
- Interpretation：文本拒绝把一次离开写成完整安全；但未给足后续过程，不能补造伏击机制。
- ruler/reader model：读者知道两人越过了当前门槛，却仍需等候新的因果说明。
- stop point：暗哨注意后人物离营，潜入段结束；后续应转失联/救援调查。
- transfer observation：撤离阶段只要出现可追溯的注意变化，即应保留它为未结风险，而不继续重复潜行 beat。
- anti-inference：不可断言迷药必由该暗哨触发；原文未精确连接二者。

## SC-07｜借用卫兵身份后，立即拆分为不同任务

- evidence_id：`SC-07`
- chapter：第0635章《王宫》
- source lines：44182–44210
- scene posture/type：借用合法队伍进入、再分头潜入。
- scene goal：进入王宫，分别完成不同目标。
- pre-state：三名杀手以女主人的卫兵身份进入；王宫警戒加强，核心地点不公开。
- expanded beats：随女主人反复进入帐篷；在频繁进出中消失；三人预先约定分头行动；主角先藏身等待营地复静，再进入无人看守的帐；火把骤亮，现场转为正面试探。
- compressed/omitted beats：三人各自的全部路线不展开。
- state-changing exchange：外部身份使进入成立；进入后不再共享路径；火把亮起则把隐藏状态转为对峙状态。
- opponent/other-character reaction：守卫放过的是“女主人卫兵”这一社会身份，而非确认每个个体真实目的。
- body/space/detail selection：卫兵服饰、频繁帐篷进出、空帐、火把、十步距离。
- Evidence：合法队伍能给准入，但不能替三个不同目标提供共同退出方案。anchor：“各行其是”
- Interpretation：身份借用完成后，潜入应拆为个体行动场景，不能继续作为集体行军。
- ruler/reader model：读者追问的是每个人的目标是否会先改变另外两人的风险。
- stop point：火把亮起、对方提出要求时，转入对峙/抉择。
- transfer observation：群体潜入只在共享准入阶段合写；目标、暴露面或信任边界分裂时立即分场。
- anti-inference：分头不是专业人士的默认最优解；此处由互不信任及不同任务造成。

## SC-08｜第一道盘查通过，第二道改验“群体是否合理”

- evidence_id：`SC-08`
- chapter：第0656章《入夜》、第0657章《逃亡》
- source lines：45761–45825
- scene posture/type：越狱后伪装撤离。
- scene goal：带领多人离开禁区并取得庇护。
- pre-state：营地因外部混乱而抽调大量兵力；队伍拥有头目腰牌、部分僧衣与一名可用武力者。
- expanded beats：先让一人以随从身份离营报信；潜入头目帐取得腰牌；趁守卫松动带队离开；第一队巡逻兵因腰牌和“尼姑去百花营”的说法放行；第二队由知情更高的军官逐人检查；领队以眼神示意，队员击倒巡逻队，场景转为公开逃亡。
- compressed/omitted beats：无差异的骑行和换装过程被压缩。
- state-changing exchange：腰牌通过低信息验证；第二队的传闻与逐人察看使身份伪装失效；眼神成为行动授权。
- opponent/other-character reaction：第一队“不敢多问”，第二队开始核对人数、性别与囚犯传闻。
- body/space/detail selection：腰牌、僧衣、夜色、七人巡逻、十余人队列、眼神。
- Evidence：盘查强度取决于守卫知道什么，而非守卫人数。anchor：“左瞧右望”
- Interpretation：一套伪装可通过常规流程，却会在拥有局部情报的检查者面前崩塌。
- ruler/reader model：读者看到“已离开监狱”并不等于“已脱险”，第二次检查才是真正的状态门槛。
- stop point：巡逻者被击倒后，隐藏身份不再是主问题，转逃亡/追捕。
- transfer observation：将每次检查写成不同验证维度：凭证、路线、人数、衣着、目的或人物常识。
- anti-inference：不能把暴力制服设为常规补丁；它在此是伪装已无法维持后的 handoff。

## SC-09｜被发现时，预先限定优先级与退出方向

- evidence_id：`SC-09`
- chapter：第0919章《厚刀》
- source lines：65018–65069
- scene posture/type：深处侦察、室内高位藏身。
- scene goal：查明敌方隐秘石室中的情报后脱离。
- pre-state：一人在外望风；人物确认室内无声后进入，摸清空间与壁刻。
- expanded beats：两圈贴墙摸索；外部开门声早于预警；人物攀至高墙缝隙；两名敌人进屋练习；借兵器碰撞声换气；其中一人翻滚时看到高处异物；人物预先决定先击杀未察觉者、再处理发现者，并准备沿原路撤退；敌人间的误杀突然制造空档；人物利用空档下落、补看关键信息后离开。
- compressed/omitted beats：后续其他石室探索不计作本窗潜入证据。
- state-changing exchange：视线掠到高处使“未发现”转为“局部发现”；敌人误杀又把局面转成即时退出机会。
- opponent/other-character reaction：发现者立即改变击杀对象；未发现者仍按原有对练逻辑行动。
- body/space/detail selection：半圆石屋、高墙缝隙、屏息、油灯、翻滚视线、刀风。
- Evidence：被发现并不自动等于交战；先明确谁知道、谁不知道、出口是否仍在。anchor：“脱身的机会”
- Interpretation：退出权不是地理路线而已，也取决于现场知情分布。
- ruler/reader model：读者会持续计算：发现者能否先开口、第三人是否仍不知情、人物是否值得多停一拍。
- stop point：人物离开石屋、危险区域暂时脱离。
- transfer observation：一旦暴露，先写“知情者集合”和优先级，再决定战、骗、藏或撤。
- anti-inference：不能把敌方互杀当作通用巧合；此窗的机会来自既有对练关系与错误目标切换。

## SC-10｜刺杀报告使守卫行为转入追捕

- evidence_id：`SC-10`
- chapter：第1164章《夺兵》
- source lines：81169–81208
- scene posture/type：守方视角下的刺杀暴露与指挥层反应。
- scene goal：在夺取军权的同时控制突发刺杀的政治影响。
- pre-state：伪装者已进入中军帐并取得将领服从；外部守卫维持封锁。
- expanded beats：帐外先报“有刺客”；卫兵立即分为追击与封锁两组；稍后确认刺客已被发现、逃窜且有同伙接应；主事者继续维持帐内秩序，外部视线转向被怀疑的来客。
- compressed/omitted beats：刺客完整入侵路线、交手过程和城市追逐未展示。
- state-changing exchange：一声示警使守卫从礼仪护卫转为追击与隔离；后续报告确定事件不是单人事故。
- opponent/other-character reaction：守卫反应快，但主事者不许警报接管全部议程。
- body/space/detail selection：帐帘、十余卫兵、外围封锁、远处报讯、被盯住的目光。
- Evidence：发现后的有效场景不是再写刺客如何躲，而是写谁被调走、谁被隔离、谁因此获得或失去行动空间。anchor：“有刺客”
- Interpretation：暴露本身是一次守卫资源再分配。
- ruler/reader model：读者从“刺客是否逃掉”转而追问“追捕重排会让谁暴露、谁获得机会”。
- stop point：追击队离开且封锁建立后，转追逐/权力博弈。
- transfer observation：发现后至少更新：追击力量、留守力量、封锁对象与仍可利用的空档。
- anti-inference：不能由本窗推出所有守卫都会高效分工；这里有预备卫兵和权力控制的条件。

## SC-11｜用声音差异确认“目标并未如常沉睡”

- evidence_id：`SC-11`
- chapter：第0290章《刚柔》
- source lines：20613–20648
- scene posture/type：低声进入后的证词逼取。
- scene goal：不惊动外部人手，确认住持是否掌握谋杀信息。
- pre-state：人物夜入寺庙，听到东厢有轻微呼吸；目标表面上熟睡。
- expanded beats：翻墙、撬门进入；先以较轻动作试探；从鼾声的异常规律与此前事件的声音规模判断目标在伪装无知；场景立即转审问。
- compressed/omitted beats：翻墙与开门不作为技巧教学展开。
- state-changing exchange：目标的呼吸与鼾声不匹配，改变人物对“睡眠者”的判断。
- opponent/other-character reaction：目标因观察被点破而失去原有说辞。
- body/space/detail selection：轻微呼吸、无规律鼾声、夜间寺庙、门闩。
- Evidence：声音不只是氛围，而是判断现场人物是否处于可控状态的证据。anchor：“没什么规律”
- Interpretation：当声音改变人物对目标知识状态的判断时，潜入应转讯问或对峙。
- ruler/reader model：读者追问的由“能否进屋”改为“他到底知道什么”。
- stop point：确认目标知情并开始审问，潜入段结束。
- transfer observation：只保留能推出下一步行动的声音差异；不要把“安静”泛化为紧张描写。
- anti-inference：不应把任何鼾声都写成破绽；此处依赖人物已有观察与上下文矛盾。

## SC-12｜城市掩护消失后，立即改变位置策略

- evidence_id：`SC-12`
- chapter：第1155章《寻人》
- source lines：80581–80604
- scene posture/type：城市骚乱中的低可见行动。
- scene goal：在混乱中寻找同伴与目标动向。
- pre-state：人物借拥挤街道缓慢观察；本可混在人流中移动。
- expanded beats：市面因政变谣言迅速清空；人员减少使人物失去人群掩护；他不再继续街面尾随，转而上墙窥探；见目标队伍离开后回到街面，藏到屋檐下；当地人把他拉入店中，他由此获得服饰识别情报。
- compressed/omitted beats：街道谣言的全部版本不逐条保留。
- state-changing exchange：人流散去改变可见性；陌生人的收留同时改变人物藏身处与信息来源。
- opponent/other-character reaction：群众按自保逻辑撤离，并非为主角提供便利。
- body/space/detail selection：空街、院墙、临街屋檐、门缝、腰带颜色。
- Evidence：环境掩护会自行消失，原来的“低调走路”不能机械延续。anchor：“无处藏身”
- Interpretation：位置暴露风险由人群密度与旁人行为共同决定。
- ruler/reader model：读者会问：人物还能否不显眼地观察，又从谁那里获得新的识别信息。
- stop point：获得服饰差异等可用情报后，转追踪/寻找人物。
- transfer observation：把人流、噪声、营业状态视为会变化的掩护资源；资源消失时必须换位或换方法。
- anti-inference：不是所有混乱城市都更适合潜入；本窗恰恰显示混乱也会清空掩护。

# Cross-Window Findings

1. 暴露管理应追踪具体“可验证状态”，而不是笼统风险值：人物是否应在场、守卫是否听到异常、路径是否仍可用、谁已知情。支持：`SC-01`、`SC-02`、`SC-09`、`SC-11`。

2. 凭证只能通过某一类验证，不能自动覆盖路线、人数、目的与人物常识。低信息守卫可能放行，高信息守卫会把同一伪装转成暴露。支持：`SC-03`、`SC-07`、`SC-08`。

3. 守卫不是背景墙；其注意力被声音、轮换、报讯和政治命令重新分配，分配结果应改变角色下一拍。支持：`SC-02`、`SC-05`、`SC-08`、`SC-10`。

4. “退出权”应作为独立状态：离开当前空间不等于安全；一旦有人注意、发现或追击重排，潜入主问题必须交给逃亡、追踪、救援、讯问或谈判。支持：`SC-06`、`SC-08`、`SC-09`、`SC-10`；反证边界：`SC-04`中观察者故意不立即拦截，以保留跟踪链。

5. 异常顺利不是奖励，而是信息。唯一可穿越的空档、过分方便的进入路径，应先改变人物对对方意图的判断。支持：`SC-05`、`SC-07`、`SC-08`。

# Counterexamples & Boundaries

- `SC-03`：身份混入成功但路线与接应失效；不能把“过门禁”当完成潜入。
- `SC-04`：反潜入者可故意不当场阻断，以换取更高价值目标；这不是失职，而是目标从保护单点转为追踪组织。
- `SC-05`：守卫漏洞可能是会面或陷阱入口；此时不宜套用普通绕卫流程。
- `SC-06`：暗哨注意后虽已离营，后续风险如何兑现文本未充分展示；不能伪造“暗哨立刻通报并设伏”的因果。
- `SC-12`：街头混乱并非天然隐蔽优势；人群退散会反而提高位置暴露。

# What Existing Skill Misses

当前 `stealth_infiltration` 已正确要求更新暴露风险、让守卫按规则行动、并在完全暴露后转 `chase_escape`。新增且非近义重复的能力是：

1. 将暴露拆成可写的状态载体：身份可验点、位置可见性、守卫注意力、路线有效性、退出权、知情者集合。
2. 区分不同盘查的“验证维度”，避免把腰牌、制服或一句谎言写成万能通行证。
3. 将“守卫资源重排”作为发现后的首要结果：谁追、谁守、谁被隔离、何处变空。
4. 将异常顺利识别为对方意图信息，而非继续追加顺畅潜行。
5. 给出明确 handoff：当发现改变知情分布、出口或任务性质时，立即换场景问题，不回头重复躲藏与绕路。

# Candidate Transfer Rules

1. **身份只解决它被验证的那一层**

   - applicability：角色依赖制服、腰牌、熟人身份或编造任务进入受控区。
   - rule：每一次盘查只验证一个具体维度；后续盘查应换成路线、人数、目的、时段或人物常识。
   - stop rule：身份与目标/人数/路线发生不可圆的矛盾时，停止继续“装得像”，转谈判、强行脱离或逃亡。
   - failure pattern：让同一张凭证连续解决所有问题，守卫因此成为无反应布景。

2. **把退出权作为独立状态维护**

   - applicability：角色已进入目标区，或已取得物品/情报。
   - rule：每个关键推进同时更新“出口仍在吗、谁能封出口、是否有人已注意到异常”。
   - stop rule：出口被封、知情者扩散或警报调动开始时，潜入段结束。
   - failure pattern：角色已被看见、已有追击，却继续描写同一种躲藏和绕路。

3. **声音、视线与人流只在改变判断时展开**

   - applicability：近距离伏藏、夜间进入、城市混行、绕过守卫。
   - rule：选择一个能改变人物或守卫下一拍的感官证据，如鼾声异常、巡逻错身、惨叫、人流消失、视线扫到多余物。
   - stop rule：感官证据已完成状态更新后，不重复堆叠同类氛围。
   - failure pattern：以“静、黑、脚步轻”持续制造紧张，但没有任何人改变判断或行动。

4. **发现后先重算知情者，再选择交接场景**

   - applicability：有人看见、听见、怀疑，或守卫开始调动。
   - rule：先确定谁知道、谁还不知道、谁被调去追击、谁继续留守；再转入逃亡、战斗、审问、谈判或反追踪。
   - stop rule：主问题不再是隐藏身份/位置/目的时，退出 `stealth_infiltration`。
   - failure pattern：把“被发现”机械写成立刻全员开战，或反过来假装发现从未发生。

# Source Fidelity Audit

- 已纳入的 12 个窗口均有本地 GB18030 解码后核对的章节与行号；正文仅保留短 anchor，其余均为意译。
- 不将 `SC-06` 的后续失联机制确认为暗哨直接造成；原文不足以精确连接。
- 以下检索命中未纳入结论：第0217章《偷听》、第0223章《救人》、第0235章《卧房》、第0411章《搜城》、第0417章《无路》、第0493章《离军》、第0528章《相遇》。原因是本轮未取得足以同时覆盖潜入前状态、状态交换与 handoff 的完整可核验窗口，避免以摘要性命中或单句结果充数。
- 本报告只支持《死人经》上述窗口内的有限观察；不将其推广为该书全篇或潜入场景的一般定律。
