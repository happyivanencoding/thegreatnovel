我会先读取当前激活的 `tgn-system-steward` Skill；随后只在该 Skill 明确需要时读取列出的项目文件，保持只读、限定范围。**Verdict：FAIL（bounded smoke）**  
问题是高价值 Story Authority 在 `Story Program → Outline/Future-10 → Primary` 运输中发生了语义压缩：唐鹭44级“共载”、韩狩68级“择风”及其鸣骨峡展示没有作为可复用的 actor+ruler+demo 锚点继续传递；空间与配角因此退化为名词和功能对白。

**Earliest Root Cause：Outline transport。**  
不是先怪 Story Program：它已经定义了具体人物、等级、地点和展示。也不是先怪 Primary：除非确认 Primary 已收到这些锚点却仍删掉，否则下游不能承担上游丢失的责任。

**Smallest Fix：**  
在 Outline/Future-10 到 Batch Packet 的窄运输层，原样保留已批准的 `人物 + 精确等级 + 当前地点/阶段 + 公共展示 + 现场意义`。同时给鸣骨峡固定少量可复用空间锚点，并要求每次动作换位、路线开闭或局势变化后做一次最小 Situation Re-anchor。不要重写完整 Story Program，不新增全局数据库或 Agent。

**Reader-Facing Actor Ruler Anchors：不创造新等级或新展示。**  
它们只运输 Story Program 已决定的事实，防止 actor、number、demo 和意义在摘要时丢失；不能补设定、升级人物或替作者安排新 payoff。

四个概念分别解决：

- **Stable Scene Geography**：让读者持续知道鸣骨峡的固定空间关系、入口、险点、可见位置和路线，不让地图变成不断新增的名词。
- **Situation Re-anchor**：局势、位置、目标或通路变化后，短暂重新告诉读者“谁在哪、要什么、现在卡在哪里”。
- **Active Interior**：把重要人物当前真正起作用的私人压力、旧关系或偏好，落实为对白、停顿、误判、拒绝、让步或选择；不是补传记。
- **Earned Convergence**：多方在共享因果铰链上相撞；每条线都必须有自己的目标和即时行动，移除它会改变结果或后续可行性，不是把人物同时装载进场。

**What Not to Add：**

- 不新增 Scene Graph；现阶段是 Outline 锚点运输和场景重定位不足。
- 不新增 Reader State DB；现有 State 不能替代事件与读者可见展示。
- 不新增 Power Ecology Agent；精确力量生态应由已有 Authority 和局部场景实现。
- 不让 Primary 直接读取完整 Story Program；这会扩大 Authority 泄漏和运行时负担，绕过必要的 reader-safe projection。

Memory used: relevant prior TGN audit principles.