# Independent Cross-Layer Review

## 证据链

```mermaid
flowchart LR
S["Fantasy Seed<br/>最后用途 → 亲自完成 → 道器与持续资产"]
W["World Vision<br/>毁灭保留最后行动；不能无条件占有"]
P["Story Program<br/>借响 → 铸器 → 合炉 → 载城"]
O["Outline<br/>第1—3章借响凿路；第4—6章铸器"]
C1["Chapter 1<br/>封炉危机；触到断镐"]
C2["Chapter 2<br/>首次借响；打开临时裂口"]
C3["Chapter 3<br/>凿穿封壁；矿工转移；锋意留在碎铁"]
S --> W --> P --> O --> C1 --> C2 --> C3
```

- Seed 明确承诺“最后用途”被主角亲自完成并铸成可持续道器：[selected_candidate.md:5](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/seed/selected_candidate.md:5)、[selected_candidate.md:37](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/seed/selected_candidate.md:37)。
- World Vision 保持同一不变量，并规定只有亲自完成行动后残响才可被铸入器胚：[world_vision_response.md:59](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/world/world_vision_response.md:59)、[world_vision_response.md:65](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/world/world_vision_response.md:65)。
- Story Program 将其具体化为“进入毁灭现场→辨认最后用途→亲自完成→留下资产→进入下一处现场”的循环：[story_program_response.md:7](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/story/story_program_response.md:7)。
- Outline 有意把“借响凿路”与“铸成第一件可复用道器”拆成相邻阶段：[outline_response.md:186](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/outline/outline_response.md:186)、[outline_response.md:204](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/outline/outline_response.md:204)。

## 到第三章的判断

### `CORE_PROMISE_PRESERVED`

理由：

- 第一章不是等待奇遇：沈燧拒绝回屋等死，主动进入下层矿道寻找生路；结尾触到断镐并感知其最后用途：[chapter-01/chapter.md:159](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/chapter-01/chapter.md:159)、[chapter-01/chapter.md:447](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/chapter-01/chapter.md:447)。
- 第二章把能力变成具体身体行动：断镐残响提供方向与力量，沈燧凿开仅容一人通过的临时裂口，并组织矿工转移：[chapter-02/chapter.md:1](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/chapter-02/chapter.md:1)、[chapter-02/chapter.md:249](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/chapter-02/chapter.md:249)。
- 第三章完成第一次不可逆的核心行动：沈燧在巡炉队和塌方压力下凿穿封壁，冷风与微光进入，矿工开始逃出：[chapter-03/chapter.md:221](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/chapter-03/chapter.md:221)、[chapter-03/chapter.md:253](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/chapter-03/chapter.md:275)。
- 核心承诺尚未完整结算为道器，但没有被替换成普通逃生或泛化力量；碎铁仍保留锋意，铸器明确作为下一步开放承诺：[chapter-03/canon_after.md:16](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/chapter-03/canon_after.md:16)、[chapter-03/canon_after.md:35](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/chapter-03/canon_after.md:35)。

### Long-Form Pacing Early Signal：`EARLY_PACING_HEALTHY`

前三章虽然持续在同一处矿道内，但不是重复延迟：

- 第一章建立倒计时、主动求生和残响发现。
- 第二章完成首次借响并产生可见的临时通路。
- 第三章引入巡炉队反制，完成更高难度的贯通行动，并留下碎铁、残火、断链等后续资产。

Outline 本身将第一件可复用道器安排在后续第4—6章，约第10章完成废窟开炉；这符合“软锚点而非固定期限”的长篇节奏设计。因此当前没有 `PACING_FIX_OVERDELAY` 证据。

需要继续观察的是：第三章结束时沈燧本人尚未脱身，粗铁和完整断链的回收也未确认。如果后续继续重复“窄缝收缩—再凿一下”而不完成脱身或铸器，才会形成延迟风险。

## 历史 attractor

未见整体沿用，因此不报告 `HISTORICAL_ATTRACTOR_RECURRED`。

“废弃炼器窟”“炉心”“铸器”属于本轮已批准核心设定；“身份权柄”只作为泛化力量来源出现，没有发展成“名字权柄”式主发动机。其余“偷未来、吞世界、唯一现实、败世”等目标模式在选定链条及前三章中没有形成整体复现。

## Frozen 上游是否应重开

**没有理由重开 Fantasy Seed、World Vision、Story Program 或 Outline。**

上游承诺、世界规则、故事循环和前三章的实际推进相互一致。当前需要保留的是第三章的局部未决状态，而不是重新生成上游设计：

- 粗铁是否拔出；
- 断链是否完整带走；
- 残火是否保全；
- 矿工和沈燧是否安全脱身；
- 碎铁锋意能否进入下一步铸造。

另有一处摘要层不确定性：`chapter-03/director_response.md:11`(/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/chapter-03/director_response.md:11) 将粗铁、断链、残火概括为“被保住”，但正文与正式状态仍显示粗铁卡在窄缝中、断链只部分进入风槽、最终出口未确认：[chapter-03/state_delta.md:3](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/chapter-03/state_delta.md:3)、[chapter-03/canon_after.md:8](/C:/dev/tgn-story-mvp/books/real-exp-clean-e2e-novel-v1/chapter-03/canon_after.md:8)。本审查以正文及正式状态为准；这属于下游连续性问题，不构成 Frozen 上游重开理由。
