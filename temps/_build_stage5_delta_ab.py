from pathlib import Path
root=Path(r'C:\dev\tgn-story-mvp')
exp=root/'books'/'real-exp-private-prototype-upstream-20260826-traditional-v1'
world=(exp/'WORLD_VISION.md').read_text(encoding='utf-8')
char=(exp/'CHARACTER_EXPERIMENTAL.md').read_text(encoding='utf-8')
story=(exp/'STORY_PROGRAM_CURRENT_PRODUCTION.md').read_text(encoding='utf-8')
gbrain=(exp/'OUTLINE_CURRENT_GBRAIN.md').read_text(encoding='utf-8')
start=story.index('### 阶段5｜'); end=story.index('### 阶段6｜'); stage5=story[start:end].strip()
contract='''每块使用：

## 第X—Y章：具体块名
具体发生：先用一句写清本块真正的故事主问题，再按因果顺序写连续故事锚点。通常 3—5 个；每个锚点写清谁为了什么行动、谁回应或阻止、主角做了什么关键选择或怎样使用已有力量、最后发生什么不可逆变化，以及为何触发下一锚点。
主要阅读兑现：写这一块最主要让读者获得的满足，可以来自力量、胜负、获得、关系、身份、探索、秘密、选择或世界事件；不要为了覆盖所有类型逐项填写。
Block Delta：只写本块结束时真实改变的维度，并使用 Power / Capability、Possession、Relationship、Identity / Access、Knowledge、Enemy State、World State 中适用的项；没变化的维度直接省略。Power Seed 决定成长 grammar，Story Program 决定长期 realization；Outline 只把已经批准的阶段变化落到具体故事事件，不为填表新增微升级、奖励、权限或地图。
代价或余波（可选）：只有真实存在时写。
推向下一块：哪个已发生结果使下一块自然发生？'''
prompt=f'''你是 TGN Outline 的受控 A/B 实验执行者。冻结所有输入，只改变剧情块输出 contract，用来测试当前 mandatory growth/reward/world-expansion fields 是否制造语义填表压力。不要审查系统，不要解释原则，只生成规划。

冻结条件：
- World / Character / Story Program 与上一组完全相同，均已批准，不得改写。
- 只展开阶段5「开山之后，没有他的位置」。
- 与 control 相同，按自然因果切成恰好3个连续剧情块，总计约10—14章。
- 不额外告诉你每块是否应该升级、获得奖励或扩张世界；从冻结上游自行判断。
- 不输出总体画像或未来十章。
- GBrain 相同，仅为可选灵感。

# A/B 唯一变量：剧情块输出格式
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
(exp/'OUTLINE_STAGE5_THREE_BLOCK_DELTA_AB_PROMPT.md').write_text(prompt,encoding='utf-8')
print(len(prompt))
