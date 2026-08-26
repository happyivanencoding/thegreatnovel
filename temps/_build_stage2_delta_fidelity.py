from pathlib import Path
root=Path(r'C:\dev\tgn-story-mvp'); exp=root/'books'/'real-exp-private-prototype-upstream-20260826-traditional-v1'
world=(exp/'WORLD_VISION.md').read_text(encoding='utf-8'); char=(exp/'CHARACTER_EXPERIMENTAL.md').read_text(encoding='utf-8'); story=(exp/'STORY_PROGRAM_CURRENT_PRODUCTION.md').read_text(encoding='utf-8'); gbrain=(exp/'OUTLINE_CURRENT_GBRAIN.md').read_text(encoding='utf-8')
start=story.index('### 阶段2｜'); end=story.index('### 阶段3｜'); stage=story[start:end].strip()
contract='''每块使用：
## 第X—Y章：具体块名
具体发生：先用一句写清本块真正的故事主问题，再按因果顺序写连续故事锚点。通常 3—5 个；每个锚点写清谁为了什么行动、谁回应或阻止、主角做了什么关键选择或怎样使用已有力量、最后发生什么不可逆变化，以及为何触发下一锚点。
主要阅读兑现：写这一块最主要让读者获得的满足，可以来自力量、胜负、获得、关系、身份、探索、秘密、选择或世界事件；不要为了覆盖所有类型逐项填写。
Block Delta：只写本块结束时真实改变的维度，并使用 Power / Capability、Possession、Relationship、Identity / Access、Knowledge、Enemy State、World State 中适用的项；没变化的维度直接省略。Power Seed 决定成长 grammar，Story Program 决定长期 realization；Outline 只把已经批准的阶段变化落到具体故事事件，不为填表新增微升级、奖励、权限或地图。
代价或余波（可选）：只有真实存在时写。
推向下一块：哪个已发生结果使下一块自然发生？'''
prompt=f'''你是 TGN Outline 的受控保真测试执行者。所有上游冻结，只测试 Block Delta contract 是否在上游明确存在真实 Power progression 时仍能把成长落实到正确的剧情块。不要审查系统，不要解释原则，只生成规划。

- 只展开阶段2「九檐山上，不做顺手的人」。
- 按自然因果切成恰好3个连续剧情块，总计约14—22章。
- 不额外指定哪一块升级；根据 Story Program 自行安排。
- 不新增阶段外能力、奖励、权限、地图；也不要因为没有 mandatory Power 字段而漏掉 Story Program 已批准的真实 Power / Capability 变化。
- 不输出总体画像或未来十章。

# Block Delta contract
{contract}

# 已批准 World Vision
{world}
# 已批准 Character Authority
{char}
# 已批准完整 Story Program
{story}
# 聚焦阶段2
{stage}
# 相同 Outline GBrain Inspiration
{gbrain}
'''
(exp/'OUTLINE_STAGE2_THREE_BLOCK_DELTA_FIDELITY_PROMPT.md').write_text(prompt,encoding='utf-8'); print(len(prompt))
