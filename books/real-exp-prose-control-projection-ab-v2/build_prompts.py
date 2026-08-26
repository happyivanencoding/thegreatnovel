from pathlib import Path
import hashlib,sys
sys.path.insert(0,r'C:\dev\tgn-story-mvp\src')
from story_mvp.gbrain_retrieval import extract_abstract_content

EXP=Path(r'C:\dev\tgn-story-mvp\books\real-exp-prose-control-projection-ab-v2')
GB=Path(r'C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\reference-corpus\prose-controls')
CASES={
 'action_retest': {
   'base': Path(r'C:\dev\tgn-story-mvp\books\real-exp-human-reaction-ch3-v1\after-v2\primary_prompt.md'),
   'scene':'ACTION_COMBAT',
   'control':'spatially-traceable-causality-v1.md',
   'mode':'full',
 },
 'dialogue_projection': {
   'base': Path(r'C:\dev\tgn-story-mvp\books\real-exp-clean-e2e-scene-skill-v11-10ch\chapter-0004\primary_prompt.md'),
   'scene':'DIALOGUE_NEGOTIATION',
   'mode':'projection',
   'projection':(
      '只前景化真正改变资格、筹码、关系距离或主动权的关键回答、回避、称呼和动作；普通对白不必句句承担转折。\n'
      '潜台词让“说了什么、没回答什么、可见反应和后续选择”共同成立，不用解释性心理补齐；不得为了显得像谈判而新增 Chapter Mission 没有的交易条件、报价或承诺。\n'
      '对白或动作已经让状态变化清楚时立即停止，不再追加“意味着、说明、显然、可以看出、这不是……而是……”式同义解释。'
   ),
 },
 'entry_projection': {
   'base': Path(r'C:\dev\tgn-story-mvp\books\real-exp-clean-e2e-scene-skill-v11-10ch\chapter-0001\primary_prompt.md'),
   'scene':'ENTRY_EXPLORATION',
   'mode':'projection',
   'projection':(
      '先让人物正在做的动作、即时目标和现实限制成立，再写一个会改变下一步路线、位置或安全判断的局部异常；背景只补当前选择需要的部分。\n'
      '优先用具体物件、位置和动作动词承重，不为了“丰富入口”新增 Chapter Mission / Canon 没有的机制、规则或额外解释层。\n'
      '动作、物体变化或现场结果已经说明这个细节为什么重要时立即停止，不再追加“意味着、说明、显然、可以看出、这不是……而是……”式抽象总结。'
   ),
 },
}
MARK='\n\n# PROSE CONTROL MICRO A/B — FROZEN TEST BLOCK\n'
for name,c in CASES.items():
    base=c['base'].read_text(encoding='utf-8')
    if MARK in base: base=base.split(MARK,1)[0].rstrip()+"\n"
    if c['mode']=='full':
        page=(GB/c['control']).read_text(encoding='utf-8')
        abstract,boundary=extract_abstract_content(page)
        control=abstract.strip()+(('\n\n使用边界：'+boundary.strip()) if boundary else '')
    else:
        control=c['projection']
    common=(MARK+f"Scene Family: {c['scene']}\n"+
      '实验规则：本区块只控制 how to say；不得改变 Chapter Mission、Canon、BOOK Prose Profile、事件结果、人物决定、场景顺序或世界事实。\n'+
      'Primary Writer 不得讨论实验本身，不得在正文中提及 Prose Control。\n\n## Relevant Prose Controls\n')
    off=base.rstrip()+common+'无。\n'
    on=base.rstrip()+common+control+'\n'
    d=EXP/name; d.mkdir(parents=True,exist_ok=True)
    (d/'prompt_OFF.md').write_text(off,encoding='utf-8')
    (d/'prompt_ON.md').write_text(on,encoding='utf-8')
    (d/'control_or_projection.md').write_text(control+'\n',encoding='utf-8')
    # mechanical equality outside test block
    b_off=off.split(MARK,1)[0]; b_on=on.split(MARK,1)[0]
    assert b_off==b_on==base.rstrip()
    print(name,c['scene'],c['mode'],'base_sha',hashlib.sha256(base.encode()).hexdigest()[:12],'off',len(off),'on',len(on),'control',len(control))
