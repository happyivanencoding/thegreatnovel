from pathlib import Path
root=Path('books/real-exp-private-prototype-upstream-20260826-v1')
p=root/'HUMAN_PROMPT.md'
text=p.read_text(encoding='utf-8')
text=text.replace('生成 4 个独立候选，不评分、不排名。先保证每个人自身成立，再避免明显心理运动坍缩；不要为了多样性机械分配人格类型。','本次是显式匿名原型实验，只生成 1 个 fictionalized Human Seed，不做多个版本搜索、不评分、不排名。这个人必须重新出生在当前幻想世界中；保留三条原型 lane 的选择结构，但不得复刻现实履历。')
text=text.replace('# HUMAN CANDIDATE N｜姓名／短标签','# HUMAN SEED｜幻想世界姓名／短标签')
text=text.replace('作者选择时会把一个候选编辑成单独的 `# HUMAN SEED`；不要替作者选择。','本次没有 Human 候选选择步骤：直接输出这一份 `# HUMAN SEED`。')
header='''# EXPLICIT ANONYMOUS PROTOTYPE EXPERIMENT\n\n下面三条 prototype selector/card 只是后台匿名 authority。输出中不得出现 `prism-wanderer-alpha`、`pwaalpha`、`Prism Wanderer Alpha`、prototype/evidence ID，也不得猜测现实姓名、地点、职业、机构、教育或现实关系身份。只把 Appetite / Behavior / Relationship 的抽象选择结构重新实现为当前幻想世界中一个全新人物。\n\n'''
text=header+text
p.write_text(text,encoding='utf-8')
print('human prompt chars',len(text))
print('four candidate instruction remains?', '生成 4 个独立候选' in text)
