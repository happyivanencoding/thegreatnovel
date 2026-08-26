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
contract='''每块严格使用：

## 第X—Y章：具体块名
具体发生：先用一句写清本块真正的故事主问题，再在这个字段内按因果顺序写连续故事锚点。通常 3—5 个锚点；只有很短的剧情块可以 2 个，这只是内容密度参考，不是 Hard Gate。每个锚点用 1—3 句写清具体人物为了什么采取行动、谁阻止或回应、主角做了什么关键选择或怎样使用核心优势、最后发生什么不可逆变化，以及这个结果怎样引出下一个锚点。
核心幻想推进：读者在本块获得什么力量、自由、反转、探索或升格体验？
一级成长变化：主角本人真正多能做了什么？
主要情绪兑现：本块压抑了什么，最后怎样释放？
收益与反哺：写本块结束后主角永久新增、掌握、控制或能够稳定调用什么，以及这些新增接下来具体能让主角做什么过去做不到的事。重要新增不要只停留在资产名词上，应通过后续实际行动、人物反应或社会后果进入剧情；没有时说明本块不结算。
世界扩张：进入什么过去无法进入的地图、层级、秘密或敌人范围？
代价或余波（可选）：只有本块真实需要时才写，不得为了显得成熟强制制造等量损失。
推向下一块：哪个具体事件、新敌人或新入口导致下一块发生？'''
prompt=f'''你是 TGN 当前 Outline contract 的受控实验执行者。本实验只测试现行剧情块表单在细粒度规划时会如何展开一个已批准 Story Program 阶段。不要审查系统，不要解释原则，只生成规划。

冻结条件：
- World / Character / Story Program 均已批准，不得改写。
- 只展开阶段5「开山之后，没有他的位置」。
- 为模拟当前 Outline 常见 3—5 章剧情块粒度，请把这一阶段按自然因果切成 **恰好3个连续剧情块**，总计约10—14章；章节边界由事件自然决定。
- 每个块严格使用当前生产格式，不新增字段，不省略字段。
- 不额外告诉你每块是否应该升级、获得奖励或扩张世界；请从冻结上游自行判断。
- 不输出总体画像、Growth Genome 或未来十章，只隔离测试这3个剧情块。
- GBrain 仅为可选灵感，不得覆盖批准产物。

# 当前生产剧情块格式
{contract}

# 已批准 World Vision
{world}

# 已批准 Character Authority
{char}

# 已批准完整 Story Program
{story}

# 聚焦阶段5
{stage5}

# 当前 Outline GBrain Inspiration
{gbrain}
'''
(exp/'OUTLINE_STAGE5_THREE_BLOCK_TAX_PROBE_PROMPT.md').write_text(prompt,encoding='utf-8')
print(len(prompt))
