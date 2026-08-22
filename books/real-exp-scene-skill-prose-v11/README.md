# Scene Skill v1.1 真实章节 A/B/C 实验

本实验比较同一冻结 Chapter 2 / Chapter 3 上的三组 Primary Writer：

- A：不注入 Scene Skill；
- B：注入 `c5be62c` 的旧 Scene Skill v1；
- C：注入当前 HEAD 的 Scene Skill v1.1。

每章先调用一次当前生产 Context Curator，再用同一份 Curator Response 生成 A/B/C。除 Scene Skill 注入内容外，三组共用冻结 Primary Prompt 骨架、同一模型和同一章节上下文。不运行 Director、Specialist、Integrator 或 State Delta，不写入 BOOK / 正式 Canon，不人工润色，不自动重试。
