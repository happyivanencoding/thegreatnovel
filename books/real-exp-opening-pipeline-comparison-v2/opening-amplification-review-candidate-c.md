# Opening Contract amplification 后验审阅：candidate-c《掌中天工》

审阅日期：2026-08-21

## 范围与证据口径

本审阅只使用 candidate-c 的 `runs/chapter-0001`、`chapter-0002`、`chapter-0003` 下的 prompt、response、manifest、final_formal_prose、execution，以及同一 candidate 的 `BOOK_after_state_delta.md`。没有把其它目录的内容作为证据。

三章的实际执行链均为 Primary → 已选 Specialist → Integrator → State Delta，三章最终正文来源均为 Integrator：Chapter 1 选 `opening/action`（`runs/chapter-0001/manifest.json:4-9`），Chapter 2 选 `dialogue/action`（`runs/chapter-0002/manifest.json:4-9`），Chapter 3 选 `action`（`runs/chapter-0003/manifest.json:4-8`）。三次 `execution.json` 都记录 Integrator 已执行且最终来源为 Integrator（各文件的 `integrator_executed`、`final_source` 字段）。

下文把正式正文和节点 response 中已经发生的内容记为“实际观察”；prompt、BOOK 和 State Delta 中尚未发生的内容只作为合同、设计或状态记录，不当作正文事实。无法由这些工件确认的部分明确写为 `UNKNOWN`。

## A. payoff 是否重复强化

判定：存在同一核心快感的跨章重复调用，但没有观察到同一结果的无变化复播或过度重复强化；整体是递进兑现。

实际观察：

- Chapter 1 的 payoff 是新造护腕在沈砚自身灵力耗尽后，重新牵回地火和散灵，沿刚施过的引砂诀切断锁链，救出唐鹭和三名矿奴（`runs/chapter-0001/final_formal_prose.md:193-223`）。结果之后只写四人脱险、霍沉改变处置并留下地底脉动，不再用旁白重复证明护腕机制（同文件 `:225-273`）。
- Chapter 2 继续调用同一护腕，但对象和结果都改变：沈砚在第二次断灵环境中先修承重骨、再接通断轨，让载着一批矿奴的运输车越过塌陷段（`runs/chapter-0002/final_formal_prose.md:187-217`、`:219-289`）。这不是重新救同一个塌口，而是把“空竭后还能行动”落实成可保留、可再次调用的现场优势；Chapter 2 的 Curator/Prep 也把“第二次使用、两次修补、矿车通过”列为本章结果（`runs/chapter-0002/curator_response.md:39-45`）。
- Chapter 3 的连续调用进一步改变行动尺度：护腕先修复两只滑轮（`runs/chapter-0003/final_formal_prose.md:159-191`），再修门栓和支撑，使通道从只够两人通过扩大为可供数人依次通过（同文件 `:419-485`）。结果重点从“再救一次人”转为“保留更多人能够通过的出口”，随后才得到阵眼局部结构和下一步取火入口（同文件 `:295-389`、`:503-581`）。

因此，重复的是“废料灵路 → 护腕借外部能量 → 改变现场”的核心机制；每章新增了不同的结构对象、风险代价和行动空间。没有看到 payoff 成立后再用同义句连续加码的段落。

`UNKNOWN`：无法仅凭这三章工件判断读者主观上是否会觉得“连续三章都在用护腕”偏重复；Chapter 3 之后的 payoff 节奏也不在本审阅窗口内。

## B. 同一能力是否 Primary→Specialist/Integrator 重复解释

判定：没有观察到 response/正式正文层面的重复解释。Prompt 输入层有重复携带合同和已知能力，但没有转化为 Primary、Specialist、Integrator 依次复述同一机制的正文段落。

实际观察：

- Chapter 1 的 Opening Specialist 明确无修改；Action Specialist 只补了唐鹭从车架下脱身到塌口外的路径（`runs/chapter-0001/action_response.md:1-6`）。Integrator 审计也明确只采用这一处局部插入，没有改写护腕机制（`runs/chapter-0001/integrator_response.md:1-5`）。
- Chapter 2 的 Action Specialist无修改；Dialogue Specialist 的 Patch 2 只补足唐鹭对“下面有人”和协作边界的对白（`runs/chapter-0002/dialogue_response.md:29-48`）。Integrator 采用 Patch 2，拒绝会删掉推车和断灵动作、并把尚未发生的意图提前说出的 Patch 1（`runs/chapter-0002/integrator_response.md:1-5`）。这不是重复解释护腕，而是修正人物协作对白。
- Chapter 3 的 Action Specialist 只补空白记录片来源、短锤来源和阵线方位（`runs/chapter-0003/action_response.md:3-5`、`:9-17`、`:19-37`）；Integrator 审计确认采用的正是这三个局部事实修补（`runs/chapter-0003/integrator_response.md:1-5`）。没有新增一段“护腕如何工作”的说明。

正式正文保留 Primary 的连续动作，只在新对象发生变化时重新落地能力：Chapter 2 解释车底热量如何进入承重骨和断轨（`runs/chapter-0002/final_formal_prose.md:199-217`、`:259-275`），Chapter 3 解释同一余力如何进入滑轮、门栓和支撑（`runs/chapter-0003/final_formal_prose.md:171-189`、`:461-485`）；这些都发生在新的修补动作中，不是 Specialist/Integrator 对同一结果的旁白复述。

`UNKNOWN`：隐藏的模型内部推理不可由这些 response 工件确认；本判断只针对可见 prompt、response 和正式正文。

## C. 是否为前三章合同过度前置未来升级

判定：未观察到正式正文把未来升级提前结算。

实际观察：

- Chapter 1 只完成护腕的铸成与第一次运行；正文没有逆灵炉、黑色晶核、境界跃迁或脱离矿场（`runs/chapter-0001/final_formal_prose.md:105-121`、`:193-225`）。对应 Curator 明确把逆灵炉、黑色晶核和正式升格留在本章之外（`runs/chapter-0001/curator_response.md:11-15`、`:24-30`）。
- Chapter 2 的新收益是护腕第二次调用、修车和黑铜回收片；霍沉的处置、废器堆工作位置及支巷线索仍是当前结果，未写成逆灵炉或黑色晶核已经存在（`runs/chapter-0002/final_formal_prose.md:303-343`、`:351-447`）。Chapter 2 的 Curator 也明确不提前兑现逆灵炉、黑色晶核、雨埋城或更远阶段（`runs/chapter-0002/curator_response.md:9-14`、`:43-45`）。
- Chapter 3 只取得阵眼局部结构、被压矿车的骨架位置和地火路线。大型废矿车在正文中是“能拆”的未来材料，伪造记录和“回来拆车、取火”仍是章末计划（`runs/chapter-0003/final_formal_prose.md:541-581`），不是已经完成的新法器。Chapter 3 的 Curator 明确写出“不铸成新法器”，把这些内容限定为下一步入口（`runs/chapter-0003/curator_response.md:3-5`、`:45-48`）。
- `BOOK_after_state_delta.md` 顶部确实保留逆灵炉、黑色晶核、行炉、洞天等长期升级设计（`:21-40`），但这是总体设计画像，不是本三章正文事实；同一状态文件又明确“当前已完成第3章”（`:418-430`），并把取火、记录生效和下一轮救援列为仍未兑现的 open promises（`:450-457`）。

`UNKNOWN`：实验只到 Chapter 3，无法判断后续章节是否会把当前入口过快兑现为升级；在本审阅范围内没有这类正文现象。

## D. 是否把主角/NPC 工具化

判定：主角没有被写成纯粹的能力展示工具；但 Chapter 2 存在一个真实、局部的 NPC 工具化风险，不能写成“完全没有问题”。

实际观察：

- Chapter 2 中沈砚确实“故意”让载着一批矿奴的车在断轨处卡死，等待断灵后试用护腕（`runs/chapter-0002/final_formal_prose.md:141-171`）。他随后明确意识到“不喜欢拿人试东西”，但仍在车上人员会被切锁或埋掉的压力下启动护腕（同文件 `:187-203`）。这使车上矿奴承担了验证第二次能力的风险；他们大多没有个体声音，主要以被锁住的乘客、危险后果和“都在”来呈现（同文件 `:167-179`、`:285-307`）。这是本项唯一明确的局部风险。
- 风险没有扩展成全程工具化：第一章唐鹭会指挥三名矿奴让出车轮、参与脱困（`runs/chapter-0001/final_formal_prose.md:155-167`、`:217-231`）；第二章她质疑把一车人拿来试路，并实际扶人、救人、藏下黑铜片，章末还给沈砚设下“再拿一车人试路，先告诉我”的协作边界（`runs/chapter-0002/final_formal_prose.md:169-181`、`:295-369`、`:425-447`）。Dialogue Specialist 的 Patch 2 也正是把这条边界写实，且被 Integrator 采用（`runs/chapter-0002/dialogue_response.md:29-48`、`integrator_response.md:1-5`）。
- 第三章唐鹭进一步参与取舍：她先要求回去救至少一批人，随后接受把窄门保留为后来者的出口，并亲手用松石改善承重（`runs/chapter-0003/final_formal_prose.md:391-417`、`:503-519`）。沈砚的选择也持续受材料、余灵、伤势和炉印代价约束，而不是只为证明能力而无成本成功（同文件 `:459-501`）。
- 霍沉在三章中有自己的调度、盘查和处置行动，不只是替作者复述设定；但三名矿奴和第二章车上多数矿奴仍是匿名群体，这一层人物主体性明显弱于唐鹭。

`UNKNOWN`：第三章阵壁后的呼吸者的确切身份、数量、位置和敌我关系均未确认（`runs/chapter-0003/BOOK_after_state_delta.md:428-441`）；因此不能判断他们后续是否会拥有选择和行动，只能确认当前文本把他们作为未知受害群体/危机线索使用。

## E. Primary 的 result-stop 是否被后续节点破坏

判定：未观察到被破坏。后续节点保留了 Primary 的 result-stop；结果之后增加的是必要余波、状态变化、新线索和章末推动，不是再次证明同一结果。

合同本身在 Primary/Integrator prompt 中要求“结果发生后停止再证明一次”，只继续必要的余波、收益、人物反应和章末推动（`runs/chapter-0001/primary_prompt.md:28-33`、`runs/chapter-0001/integrator_prompt.md:19-21`）。实际正文符合这一边界：

- Chapter 1 在锁链断开、四人脱险后（`runs/chapter-0001/final_formal_prose.md:209-223`），只写霍沉改变封存和盘问、护腕受到更深脉动牵引（同文件 `:245-273`）；没有再解释一次“护腕如何聚能”。
- Chapter 2 在断轨接通、矿车实际前进后（`runs/chapter-0002/final_formal_prose.md:259-289`），继续的是安全抵达、霍沉改变处置、唐鹭交付黑铜片和支巷呼吸线索（同文件 `:291-447`）。这些是新的现实后果和行动入口，不是同义重述。
- Chapter 3 第一次把门缝扩大到两肩宽后，先进入阵眼取得新信息，再因“更多人能否通过”的新取舍把结构扩大到三四人通行（`runs/chapter-0003/final_formal_prose.md:255-265`、`:295-389`、`:419-485`）。这是两个不同的现场结果，不是对第一次结果的重复确认；最终结果后只保留唐鹭的实际接受、霍沉的新命令和取火计划（同文件 `:487-581`）。
- 后续 Specialist/Integrator 也没有破坏 stop：Chapter 1 只插入脱身路径，Chapter 2 采用协作对白而非机制复述，Chapter 3 只修补物品来源和方位（各对应 response 与 Integrator 审计见 B）。State Delta 中对能力和结果的再次概括是审计/状态记账，不是正式正文中的再证明。

`UNKNOWN`：无法从可见工件判断读者是否把 Chapter 3 的“两次扩门”感受为重复；从事件因果上看，后一次有新的多人通行目标和结构取舍，不属于 result-stop 违规。

## 总结（非评分）

- A：同一核心快感有跨章递进调用，但未见同质 payoff 的过度重复。
- B：未见 Primary→Specialist/Integrator 在正文层重复解释同一能力。
- C：未见前三章正文提前结算未来升级；未来内容仍作为入口和 open promise 保留。
- D：Chapter 2 有局部 NPC 工具化风险；唐鹭的持续行动和边界使其未扩展为全程工具化，主角仍是有代价的决策者。
- E：未见 Primary 的 result-stop 被后续节点破坏。

本次仅写入本报告，未修改生产文件或实验工件。
