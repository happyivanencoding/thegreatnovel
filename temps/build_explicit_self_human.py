from pathlib import Path
from story_mvp.character_prompts import HUMAN_PROMPT
from story_mvp.character_context import project_character_life_context
root=Path(r'books/real-exp-private-prototype-upstream-20260826-v3')
world=(root/'WORLD_VISION.md').read_text(encoding='utf-8')
bundle=(root/'EXPLICIT_ANON_HUMAN_BUNDLE.md').read_text(encoding='utf-8')
p=HUMAN_PROMPT
old='生成 4 个独立候选，不评分、不排名。先保证每个人自身成立，再避免明显心理运动坍缩；不要为了多样性机械分配人格类型。\n\n每个候选使用：\n\n# HUMAN CANDIDATE N｜姓名／短标签'
new='这是显式匿名原型实验，不再搜索人物分布。只生成 **1 个** fictionalized Human Seed：三条匿名 prototype lane 是人物内核权威，但表层身份、家庭、职业、关系对象与具体欲望对象必须在当前幻想世界重新出生。不要生成多个版本，不评分，不替未来 Power 做适配。\n\n严格使用：\n\n# HUMAN SEED｜幻想姓名／短标签'
p=p.replace(old,new)
p=p.replace('作者选择时会把一个候选编辑成单独的 `# HUMAN SEED`；不要替作者选择。','这是已显式选择的匿名 prototype；直接输出一份 `# HUMAN SEED`，不要再让作者从多个 Human 候选中选择。')
full='\n\n'.join([p.strip(),project_character_life_context(world).strip(),'# Explicit Anonymous Human Prototype Selector\n\n'+bundle.strip()])+'\n'
(root/'HUMAN_PROMPT.md').write_text(full,encoding='utf-8')
print('chars',len(full),'prototype mentions',full.count('prism-wanderer-alpha'))
