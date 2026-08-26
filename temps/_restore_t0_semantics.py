from pathlib import Path
p=Path('src/story_mvp/prompts.py'); s=p.read_text(encoding='utf-8')
old='''写故事开始前的严格 T0 快照、已经建立的远期承诺、当前未解决问题和作者备注。Future 10、当前中期剧情块、未来奖励、未来能力使用、未来获得物品、未来关系变化或未来伤亡，即使本次 Outline 已经规划，也仍属于 Future Plan / Open Promise，绝不能写成 Current State / Canon；“模型已经规划过”不等于“故事已经发生过”。'''
new='''写故事开始前的严格的 T0 快照：只记录第一章第一场事件发生前一刻已经真实成立的事实，并补充已经建立的远期承诺、当前未解决问题和作者备注。Future 10、当前中期剧情块、未来奖励、未来能力使用、未来获得物品、未来关系变化或未来伤亡，即使本次 Outline 已经规划，也仍属于 Future Plan / Open Promise，绝不能写成 Current State / Canon；“模型已经规划过”不等于“故事已经发生过”。Current State 与 Future Plan 在时间上必须互斥。'''
assert s.count(old)==1
p.write_text(s.replace(old,new,1),encoding='utf-8')
