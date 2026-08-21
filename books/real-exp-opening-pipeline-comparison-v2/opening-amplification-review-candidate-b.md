# Opening Contract amplification 后验审阅

审阅对象：candidate-b《炉藏万象》；范围限于 `runs/chapter-0001`、`chapter-0002`、`chapter-0003` 下获准的 Prompt、Response、manifest、`final_formal_prose`、`execution.json`，以及同一 candidate 的 `BOOK_after_state_delta`。未读取其它实验目录，未修改生产或实验文件。本报告不打分、不改文本。

## 执行前提

三章的 manifest 都记录 `selected_specialists=[]`、`final_source=primary`（例如 `runs/chapter-0001/manifest.json:5`、`:6`）；三章的 execution 都记录 `integrator_executed=false`（例如 `runs/chapter-0001/execution.json:5`、`:6`），并将 integrator 标为 skipped（`runs/chapter-0001/manifest.json:64`、`:65`）。因此，B 的 Primary→Specialist/Integrator 链路实际没有发生；E 也没有一个 Integrator 版本可与 Primary 正文比较。

## A. payoff 是否重复强化

结论：是。这里观察到的是同一核心 payoff 的跨章、且部分同章内的重复强化；不是完全相同的句子或同一扇门的机械复述。

实际观察：

- 第 1 章把“废物仍能完成最后动作”兑现为一次救人开路。正文在黑铁锋片安静后明确写“他没有再试第二次”（`runs/chapter-0001/final_formal_prose.md:237`、`:239`），矿工随后自行处理伤者并按他的手势撤离（`:241`、`:247`）。同章 state delta 也把断镐锋力记为完成一次动作且已经耗尽（`runs/chapter-0001/state_delta_response.md:20`、`:21`）。
- 第 2 章 Primary 明确把第 1 章已耗尽的锋力改写成“黑铁锋片和右臂裂痕中尚未完成的方向性余响”，并引入粗铁铸成新器（`runs/chapter-0002/primary_response.md:3`）。同章两次实际驱动裂路器：先劈开石壁，再切断封钉救出被卡住的伤者（`runs/chapter-0002/primary_response.md:379`、`:380`、`:381`）；正文还明确两次震动分别指向石壁和封钉（`runs/chapter-0002/final_formal_prose.md:321`）。
- 第 3 章继续强化同一主循环：裂路器连续打开旧通风门和倒悬废炉闸，随后焦黑炉鳞短时分开火流，沈燧再带出未完成传火的火鳞胚（`runs/chapter-0003/curator_response.md:41`、`:42`）。五名炉工实际脱险（`runs/chapter-0003/final_formal_prose.md:343`），火鳞胚被明确命名为“还没传完火”（`:367`），不是已经完成的器物。

所以前三章的 payoff 形态是“断镐一击救人 → 残响铸成可保留的裂路器 → 裂路器进入更危险场景并带出新的承火材料”。第 3 章 director response 也直接把它称为前三章的“第一次小复利闭环”（`runs/chapter-0003/director_response.md:20`）。不同对象和不同现实结果使它不是单纯重复说明，但“最后动作转化为持续行动能力”确实被连续强化。

## B. 同一能力是否 Primary→Specialist/Integrator 重复解释

结论：`UNKNOWN`（实际链路未发生，不能把“没有观察到”当成“确认没有重复”）。

三章均没有选中 Specialist，且 Integrator 均跳过；最终来源均为 Primary。现有 Response 中关于能力的重复，主要出现在跨章的 Primary 衔接、Curator 上下文或 state delta 元数据中，例如第 2 章 Primary 的必要桥接（`runs/chapter-0002/primary_response.md:3`）和第 2 章 state delta 对两次驱动的记录（`runs/chapter-0002/state_delta_response.md:3`）。这些不是 Primary 输出后再交给 Specialist/Integrator 的实际解释，因此不能据此判定 B 为“有”或“无”。

## C. 是否为前三章合同过度前置未来升级

结论：否——按“正式未来升级”理解，前三章没有把火鳞器、个人炉心、私人炉场或完整传火提前结算。精确的后续完成章节和条件仍是 `UNKNOWN`。

实际观察：

- 第 1 章只留下黑铁锋片，断镐锋力耗尽且不能立即再次驱动；state delta 没有把它记成完整道器（`runs/chapter-0001/BOOK_after_state_delta.md:482`、`:491`、`:492`）。
- 第 2 章确实铸成粗糙、可再次使用的裂路器，但当前状态只确认它能切石壁和薄型封钉、不能切火流，剩余次数和条件未定（`runs/chapter-0002/BOOK_after_state_delta.md:483`、`:491`、`:492`）。这是第二章合同要求的“把第一次震撼变成可保留优势”，不是把后续正式火鳞升级提前完成。
- 第 3 章只取出尚未完成传火的火鳞胚；其能否完成、如何发挥作用及代价均未确认（`runs/chapter-0003/BOOK_after_state_delta.md:491`、`:493`），开放承诺也明确“是否能形成可用器物”尚未揭示（`:512`）。Curator 同样明确本章不铸成火鳞器（`runs/chapter-0003/curator_response.md:44`）。
- 同一 candidate 的状态文本把第一件真正属于自己的下品道器、独立修炼和私人炉场放在“第十章左右”的早期兑现窗口（`runs/chapter-0001/BOOK_after_state_delta.md:68`、`:70`）。这与前三章实际只得到粗糙裂路器和未完成火鳞胚相符。

因此，前三章有能力资产的递进，但没有观察到未来正式升级被过度前置。正式火鳞器的最终完成时点、条件和代价在本次范围内仍为 `UNKNOWN`。

## D. 是否把主角/NPC 工具化

结论：主角未观察到被工具化；阮青禾、裴照川等关键 NPC 仍有行动性；但伤者、普通矿工和五名炉工存在“作为 payoff 证明和运输对象”的局部功能化倾向，尚不足以判定为全面工具化。

实际观察：

- 沈燧不是只被能力推着走：第 1 章他拒绝独自逃生，开路后还把照明符推回去，要求对方照顾伤者（`runs/chapter-0001/final_formal_prose.md:247`、`:251`）；第 3 章在可以寻找个人窄缝时选择先开门救五名炉工（`runs/chapter-0003/final_formal_prose.md:49`、`:53`、`:55`）。他承受掌伤、肩伤和高温，选择与代价均由动作呈现。
- 阮青禾实际判断路线、分配伤者位置并指挥通风门和闸门通过（`runs/chapter-0003/final_formal_prose.md:45`、`:57`、`:159`），不是只等待主角施法。裴照川看到裂路器后改变部署、封死前后出口（`runs/chapter-0002/final_formal_prose.md:281`、`:285`），也不是静态的追兵背景。
- 普通矿工在第 2 章回火逼近时“不再等沈燧下令”而主动搬运伤者（`runs/chapter-0002/final_formal_prose.md:237`、`:239`）；第 3 章五名炉工和矿工在脱险后自行分组保护伤者和炉工（`runs/chapter-0003/final_formal_prose.md:343`、`:389`），并有人主动提出替沈燧分担裂路器（`:411`）。这些是实际的有限主体性。
- 局部功能化也确实存在：正文多以“腿伤者、胸口伤者、额头伤者、五名炉工”标记人物，救出人数和是否有人被留下成为能力结果的量尺；第 3 章 state delta 也确认原有队伍精确总人数未知、合作仍只是临时协作（`runs/chapter-0003/BOOK_after_state_delta.md:481`、`:494`）。他们在前三章之外是否有独立目标、冲突和长期选择，本范围不能确认，属于 `UNKNOWN`。

## E. Primary 的 result-stop 是否被后续节点破坏

结论：否。没有观察到后续节点改写或破坏 Primary 的 result-stop；有一处 Primary 内部的边界性 NPC 确认，但它紧接着改变敌方部署，不是后续节点追加的重复解释。

Primary 的 result-stop 规则要求直接结果通过动作、物体变化、人物反应和现实后果成立后，只保留必要余波、收益/损失、重要人物行动和章末推动，停止再次证明（`runs/chapter-0001/primary_prompt.md:33`；第 2、3 章同文位置相同）。本次只读比较 Primary response 中 `# Primary Draft` 与 `final_formal_prose.md`：三章去除空行后均为 `nonblank_diff=0`，没有发现落盘阶段的正文改写。

正文层面：

- 第 1 章在一次开路结果成立后没有再次试用，转入矿工处理伤者、异常被定位和进入废窟等必要余波（`runs/chapter-0001/final_formal_prose.md:239`、`:241`、`:277`）。
- 第 2 章的两次驱动是本章合同规定的两个不同直接结果，不是同一结果的再证明；“它能再次驱动”的一句确实复述了机制，但随后立即导致裴照川封死前后出口并改变追捕方式（`runs/chapter-0002/final_formal_prose.md:281`、`:285`、`:287`），属于带有现实后果的敌方反应。
- 第 3 章在救出五名炉工后核对人数、展示火鳞胚未完成状态、承接侧门封锁和队伍继续向窟心移动（`runs/chapter-0003/final_formal_prose.md:343`、`:367`、`:381`、`:409`），是收益、余波和下一步压力，不是再次解释裂路器或火鳞机制。

state delta 会在元数据中复述已发生事实，例如第 3 章把两次开路、救人和火鳞胚写入当前状态（`runs/chapter-0003/state_delta_response.md:3`、`:30`），但它没有改变 `final_formal_prose`，不构成对 Primary result-stop 的正文破坏。

## 未能由本范围确认的事项

- Specialist/Integrator 若实际执行时是否会重复解释能力：`UNKNOWN`，本 candidate 的前三章没有该链路。
- 正式火鳞器何时完成、完成条件和代价：`UNKNOWN`。
- 救援群体在离开废窟后的长期目标、分歧和是否形成长期盟约：`UNKNOWN`。
