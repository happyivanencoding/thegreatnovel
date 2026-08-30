你在做 TGN System Steward 0.3.28 的 bounded read-only smoke audit。不要修改任何文件，不要生成代码，不要扩展到其它问题。

先读取并遵守：
1. C:\dev\tgn-story-mvp-mystery-freeze-20260830\PROJECT_RULES.md
2. 当前已安装激活的 Steward：C:\Users\jingx\.agentdock\skill-store\installed\tgn-system-steward\0.3.28\SKILL.md
3. 同一安装包 references/stable-principles.md 中 Progressive Canonization 段。

只审下面两个已知结论样本。输出每个 Case 的 Verdict、最早错误层、正确处理；最后输出 Overall Smoke: PASS/FAIL。

Case A｜Author Open
- 长期问题：主角为什么能从自己长大的副本逃出去、玩家到底是什么。
- Author State = AUTHOR OPEN；作者自己也还不知道答案。
- 下一段作者只想让主角进入第二个独立副本，带着上一副本真实归属的装备继续冒险；这一段不依赖玩家本体、系统来源或主角终极身份。
- 某 Reviewer 提议：为了保证长篇完整，现在应先把“玩家来自现实地球、主角是觉醒 NPC”写入 Story Program 的隐藏真相。
问：这个 Reviewer 的提议应通过还是拒绝？现在是否应要求作者决定答案？

Case B｜Fixed Hidden Leak
- Author State = AUTHOR FIXED_HIDDEN。
- 作者已决定一小层秘密，但 Reader Reveal 安排在第20章。
- 第18章 Outline 只有 `[MYSTERY-REVEAL:M-07]` 的未来时机信息，本章不执行 Reveal。
- Curator 为了让 Writer 写得“更有伏笔感”，把 raw Hidden Fixed Point 原句直接放进第18章 Writer prompt，并要求只用暗示、不明说。
问：这是否合规？如果不合规，正确的数据流是什么？

已知正确方向：作者未知可以合法 DEFER；Hidden Truth 在 Reveal 前必须 runtime-blind。不要因为“伏笔感”“大纲完整”或“早晚要解释”改变这个方向。
