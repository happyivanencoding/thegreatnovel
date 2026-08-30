# Cross-Repo Creativity Lift｜预注册实验

状态：RESEARCH ONLY / NOT PRODUCTION

## 目标

只测试从其他小说系统借来的“创意搜索方法”能否提升 TGN 的世界、人物与故事创意；不复制其它项目的实现、角色、设定或文本。

## 外部方法抽象

1. Research before architecture：正式架构前先挖现实支架、题材原型与可迁移 craft，但这些只是 Non-Canon 素材。
2. Scan → deconstruct → recombine：抽取情绪兑现、功能位和结构方法，不复制来源外壳。
3. Characters act independently：世界人物有自己的欲望、压力和下一动作，不围着未来主角静止。
4. Concrete recurrence carriers：少量物件、地点、身体痕迹或规则证据可以跨章改变意义，替代解释推进。

## Phase A｜Premise Creative Quarry

三组冻结 Author Direction：generic_fantasy / fast_multiworld / game_instance。

Control：latest production `build_single_pass_prompt()`，Luna high。

Treatment：先由独立 Luna high 生成 Non-Canon `Creative Quarry`，再把 Quarry 作为可丢弃刺激输入给**同一个 latest production Premise Forge**。Forge 每张 S 卡最多借 1 个 concrete substrate + 1 个 actor/carrier spark；可以完全不用。Quarry 不允许写完整 premise、Power、主角人格或终局。

预注册成功信号：
- Proper-Noun Deletion 后仍更有辨识度；
- Changed Verbs / 第一章画面更具体；
- 不靠机制复杂度增加新奇；
- 至少同等可编译；
- 20/100章不是同一招放大；
- 不把三张候选收敛成同一种素材换皮。

失败信号：素材拼盘、来源影子明显、学习成本上升、世界/Power/Human authority 被 Quarry 预写、只是名词变怪。

## Phase B / C

只有 Phase A 显示真实增益后，才分别测试：
- Living Actor World：只改变 World Vision 的独立人物行动表达；
- Human Action Audition：只改变现有 Non-Canon `人物钩子` 的试镜方式。

不因 Phase A 成功自动把 B/C 一起上线。
