from pathlib import Path
from story_mvp.gbrain_retrieval import retrieve_gbrain
book=Path(r'C:\dev\tgn-story-mvp\books\real-exp-human-reaction-ch3-v1\BOOK.md').read_text(encoding='utf-8')
r=retrieve_gbrain(mode='outline', book_content=book, current_outline='为顾长川在公开升院考核通过后规划第4—8章连续故事：正式进入内门后的新行动空间、武学观察机会、竞争者与关系延续、第一次真正主动选择力量路径。避免连续五章都是考核/流程/训练；避免技能面板、工程流程、职业化蓝领叙事。')
print(r['result'])
print('\n---META---')
print('accepted',r['accepted_count'],'strategy',r['query_strategy'])
for x in r['accepted']: print(x['slug'])
