from pathlib import Path
root=Path(r'C:\dev\tgn-story-mvp')
exp=root/'books'/'real-exp-private-prototype-upstream-20260826-traditional-v1'
world=(exp/'WORLD_VISION.md').read_text(encoding='utf-8')
char=(exp/'CHARACTER_EXPERIMENTAL.md').read_text(encoding='utf-8')
story=(exp/'STORY_PROGRAM_CURRENT_PRODUCTION.md').read_text(encoding='utf-8')
gbrain=(exp/'OUTLINE_CURRENT_GBRAIN.md').read_text(encoding='utf-8')
start=story.index('### 阶段5｜')
end=story.index('### 阶段6｜')
stage5=story[start:end].strip()
block_contract='''每块严格使用：

## 第X—Y章：具体块名
具体发生：先用一句写清本块真正的故事主问题，再在这个字段内按因果顺序写连续故事锚点。通常 3—5 个锚点；只有很短的剧情块可以 2 个，这只是内容密度参考，不是 Hard Gate。每个锚点用 1—3 句写清具体人物为了什么采取行动、谁阻止或回应、主角做了什么关键选择或怎样使用核心优势、最后发生什么不可逆变化，以及这个结果怎样引出下一个锚点。能力、资产、身份、法则、关系和世界升级必须通过这些事件发生，不用“掌握更深、进入更高层、理解更多规则、获得更强能力”代替剧情。
核心幻想推进：读者在本块获得什么力量、自由、反转、探索或升格体验？
一级成长变化：主角本人真正多能做了什么？
主要情绪兑现：本块压抑了什么，最后怎样释放？
收益与反哺：写本块结束后主角永久新增、掌握、控制或能够稳定调用什么，以及这些新增接下来具体能让主角做什么过去做不到的事。重要新增不要只停留在资产名词上，应通过后续实际行动、人物反应或社会后果进入剧情；没有时说明本块不结算。
世界扩张：进入什么过去无法进入的地图、层级、秘密或敌人范围？
代价或余波（可选）：只有本块真实需要时才写，不得为了显得成熟强制制造等量损失。
推向下一块：哪个具体事件、新敌人或新入口导致下一块发生？'''
prompt=f'''你是 TGN 当前 Outline contract 的受控实验执行者。本实验只测试“当前剧情块表单是否会对一个上游明确没有 Power / Capability Delta 的完整阶段重新征收成长/奖励/世界扩张税”。不要审查系统，不要解释原则，只按当前生产剧情块格式生成结果。

实验冻结条件：
- World / Character / Story Program 均已批准，不得改写。
- 使用 GPT-5.6 Luna high。
- 只展开 Story Program 的阶段5「开山之后，没有他的位置」。
- 不要求覆盖其他阶段，也不输出 0—12 总体画像或未来十章；这是为了隔离“剧情块字段结构”本身。
- 不额外告诉你 Stage5 应不应该升级；请忠实从已批准 Story Program 判断。
- GBrain 仅为可选灵感，不得覆盖批准产物。

# 当前生产剧情块格式
{block_contract}

# 已批准 World Vision
{world}

# 已批准 Character Authority
{char}

# 已批准完整 Story Program
{story}

# 本次聚焦阶段5（与完整 Story Program 内容相同，仅方便定位）
{stage5}

# 当前 Outline GBrain Inspiration
{gbrain}
'''
(exp/'OUTLINE_STAGE5_BLOCK_TAX_PROBE_PROMPT.md').write_text(prompt,encoding='utf-8')
print(len(prompt), len(stage5))
