from pathlib import Path
root=Path(r'C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库')
dirs=[root/'reference-corpus'/'prose-controls',root/'reference-corpus'/'operations'/'gbrain-prose-craft-v1-20260824'/'staging'/'prose-controls']

def patch(name, func):
  for d in dirs:
    p=d/name
    t=p.read_text(encoding='utf-8')
    nt=func(t)
    if nt!=t: p.write_text(nt,encoding='utf-8')

def p_action(t):
  text='适用于追逐、多人混战、移动地形、多个入口/层级或站位持续变化，尤其是读者容易丢失方位与因果的 Action。简单一对一、单一场地、位置关系天然清楚时不默认启用。'
  if text not in t:
    t=t.replace('## Applicability Conditions\n','## Applicability Conditions\n\n'+text+'\n',1)
  return t

def p_dialogue(t):
  text='适用于多方、高压、隐含筹码或关系状态不容易仅靠基础对白读清的谈判/试探。基础对白已经自然改变筹码、资格或关系时，不为执行本卡额外增加回合、交易条件、报价或承诺。'
  if text not in t:
    t=t.replace('## Applicability Conditions\n','## Applicability Conditions\n\n'+text+'\n',1)
  return t

def p_entry(t):
  if '## Writer Projection' not in t:
    proj='''## Writer Projection

先让人物正在做的动作、即时目标和现实限制成立，再写一个会改变下一步路线、位置或安全判断的局部异常；背景只补当前选择需要的部分。

优先用具体物件、位置和动作动词承重，不为了“丰富入口”新增 Chapter Mission / Canon 没有的机制、规则或额外解释层。

动作、物体变化或现场结果已经说明这个细节为什么重要时立即停止，不再追加“意味着、说明、显然、可以看出、这不是……而是……”式抽象总结。

'''
    t=t.replace('## Reader Payoff',proj+'## Reader Payoff',1)
  return t

patch('spatially-traceable-causality-v1.md',p_action)
patch('dialogue-state-pressure-v1.md',p_dialogue)
patch('action-anchored-grounding-v1.md',p_entry)
for name,needle in [
 ('spatially-traceable-causality-v1.md','简单一对一'),
 ('dialogue-state-pressure-v1.md','基础对白已经自然改变'),
 ('action-anchored-grounding-v1.md','## Writer Projection')]:
 p=dirs[0]/name; print(name,needle in p.read_text(encoding='utf-8'))
