from pathlib import Path

v3 = Path(r"books/real-exp-private-prototype-upstream-20260826-v3")
trad = Path(r"books/real-exp-private-prototype-upstream-20260826-traditional-v1")

required = [
    v3 / "WORLD_VISION.md",
    v3 / "HUMAN_SEED.md",
    v3 / "STORY_PROGRAM_BLIND_FIRST_PRINCIPLES.md",
    v3 / "STORY_PROGRAM_ORDINAL1.md",
    trad / "WORLD_VISION.md",
    trad / "HUMAN_SEED.md",
    trad / "STORY_PROGRAM_BLIND_SELECTED.md",
    trad / "STORY_PROGRAM_FIRST_PRINCIPLES.md",
]
for path in required:
    if not path.exists():
        raise SystemExit(f"missing {path}")

old_trad = (trad / "STORY_PROGRAM_BLIND_SELECTED.md").read_text(encoding="utf-8")
# The legacy output duplicated its entire Story Program. Keep only the first version for literary comparison;
# duplication is recorded separately as a contract-stability fact.
second = old_trad.find("\n## 总览", 1)
old_trad_first = old_trad[:second] if second > 0 else old_trad

prompt = """你是 TGN 上游架构实验的独立审计者。这不是 production Reviewer，只用于判断一次根因修复是否成立。不要重写故事，不发明新设定，不做评分表。

这次不是在比较两个 Power 谁更好，而是在判断一个系统根缺陷：Split Character Authority 已经把 World / Power / Human 解耦，但 Story Program 是否仍被旧 Fantasy-Seed-era 阶段表单强迫成“每阶段都要能力参与、升级、获得、净新增”的 Fantasy Engine 税。

实验事实：
- B0（传统修仙，分流真元）：旧 Story Program 合同，Sol high，809s，最终输出 1143 行，并把整套 Story Program 生成了两遍。
- B1（同 World / 同 Character / 同 Story GBrain / 同 Sol high）：只把合同换成 native Collision compiler，778s，188 行，唯一版本。
- A0（百铸身，活相）：旧合同，Sol high，正常完成但每个阶段都有固定“一级成长/关键获得/核心优势参与”等字段。
- A-old-blind（百铸身，blind selector 选离印）：旧合同，Sol high，运行超过15分钟超时，无产物。
- A1（同 blind-selected 离印 / 同 World / 同 Human / 同 Story GBrain / 同 Sol high）：只换 native Collision compiler，485s，171 行，唯一版本。

请有文本证据地判断：
1. `Story Program legacy contract` 是否是一个可复现的最早语义坍缩点，而不是某本书/某个 Power 的偶发问题。
2. B0→B1 是否真正让 Life / World Engine 获得阶段发动权：指出 B1 中没有新能力/掉宝仍然完整成立的阶段，并比较 B0 为什么更容易把关系/世界冲突重新接回升级收益。
3. A0/A-old-blind→A1 是否同样改善：重点看白盐海、无面案、青铜王庭等是否不再必须把世界事件解释成下一件相材/能力成长。
4. native contract 是否仍保留男频成长：全书 progression spine 是否足够明确，Core Fantasy 是否持续兑现，而不是从一个极端走到“人物文、成长消失”。
5. World 是否需要继续加所谓“正交删除测试”等新规则，还是现有 protagonist-blind World 已经基本足够，真正问题出在 Collision 编译。
6. 当前旧 Human schema 曾把 Biography 写成对单一 Core Obsession 的逐条证明；新版 `生活事实 + competing motives + Stable Choice Bias + person-specific relationship` 已在另一组同模型 A/B 中改善。结合这里的 Story 输出，判断 Human 的这个结构替换是否与 native Collision 同方向，还是会制造新的缺口。
7. 最后只给最多两处 production 根改：如果应当替换 Human schema / Story compiler，就明确说；如果 World、Power、Outline 不该因此再加东西，也明确说不要动。不得建议新 Agent、Reviewer、scorer、Hard Gate 或额外长期状态系统。

# B0｜传统修仙旧 Story Program（仅第一套，重复输出事实已单列）
""" + old_trad_first + "\n\n# B1｜传统修仙 native Collision\n" + (trad / "STORY_PROGRAM_FIRST_PRINCIPLES.md").read_text(encoding="utf-8") + "\n\n# A0｜百铸身旧合同 sensitivity（活相）\n" + (v3 / "STORY_PROGRAM_ORDINAL1.md").read_text(encoding="utf-8") + "\n\n# A1｜百铸身 blind-selected 离印 + native Collision\n" + (v3 / "STORY_PROGRAM_BLIND_FIRST_PRINCIPLES.md").read_text(encoding="utf-8") + "\n\n# Human old-vs-new excerpt｜同一百铸身世界 / 同一匿名 prototype\n\n## OLD HUMAN\n" + (v3 / "HUMAN_SEED.md").read_text(encoding="utf-8") + "\n\n## FIRST-PRINCIPLES HUMAN\n" + (v3 / "HUMAN_FIRST_PRINCIPLES.md").read_text(encoding="utf-8")

out = Path(r"books/real-exp-private-prototype-upstream-20260826-collision-audit")
out.mkdir(parents=True, exist_ok=True)
(out / "COLLISION_AUDIT_PROMPT.md").write_text(prompt, encoding="utf-8")
(out / "PROTOCOL.md").write_text(
    "# Protocol\n\nPrimary comparison: blind-selected A vs B. A0 is sensitivity only. Same Story GBrain bundle in A/B. Audit is experimental only, not production runtime.\n",
    encoding="utf-8",
)
print(f"prompt_chars={len(prompt)}")
