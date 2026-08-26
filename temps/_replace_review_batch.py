from pathlib import Path
p=Path('src/story_mvp/prompts.py')
s=p.read_text(encoding='utf-8')
rs=s.index('REVIEW_TEMPLATE = f"""')
a=s.index('## 下一批十章总体事件链', rs)
b=s.index('"""', a)
old=s[a:b]
new='''## 下一批十章总体事件链
用 3—6 句话说明这十章承接当前哪个已批准 Story Program / 剧情块因果、主要问题、主角行动、关键转折与批末状态。Growth is longitudinal, not a ten-chapter tax：只有当前计划确实安排 Power / Capability、重要获得或新世界入口时才写；没有时不要为了批次完整补一个。

逐章使用：
## 第N章：具体标题
具体剧情：用 2—4 句写具体人物、事件和主角行动。
结果 / 状态变化：写直接结果和状态变化。
叙事功能：写本章在局部故事中的作用。
结尾推动：写下一章为什么发生。

十章必须连续；第N章的结尾推动必须成为第N+1章具体剧情的直接因果起点；不要求每章都成长或结算，也不要求每十章都新增 Power、奖励、权限、地图或更大世界入口。已经安排在本批发生的真实变化必须通过具体事件兑现；没有安排的维度不要填表式补位。'''
p.write_text(s[:a]+new+s[b:], encoding='utf-8')
print('replaced review chars',len(old),'->',len(new))
