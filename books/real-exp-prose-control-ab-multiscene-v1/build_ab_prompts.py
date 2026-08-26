from pathlib import Path
import sys,re
sys.path.insert(0, r'C:\dev\tgn-story-mvp\src')
from story_mvp.gbrain_retrieval import extract_abstract_content

EXP=Path(r'C:\dev\tgn-story-mvp\books\real-exp-prose-control-ab-multiscene-v1')
GB=Path(r'C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\reference-corpus\prose-controls')
CASES={
 'dialogue': {
   'base': Path(r'C:\dev\tgn-story-mvp\books\real-exp-clean-e2e-scene-skill-v11-10ch\chapter-0004\primary_prompt.md'),
   'control':'dialogue-state-pressure-v1.md',
   'scene':'DIALOGUE_NEGOTIATION',
 },
 'action': {
   'base': Path(r'C:\dev\tgn-story-mvp\books\real-exp-clean-e2e-scene-skill-v11-10ch\chapter-0006\primary_prompt.md'),
   'control':'spatially-traceable-causality-v1.md',
   'scene':'ACTION_COMBAT',
 },
 'payoff': {
   'base': Path(r'C:\dev\tgn-story-mvp\books\real-exp-human-reaction-ch3-v1\after-v2\primary_prompt.md'),
   'control':'payoff-consequence-conversion-v1.md',
   'scene':'PAYOFF_POWER_PROOF',
 },
 'entry': {
   'base': Path(r'C:\\dev\\tgn-story-mvp\\books\\real-exp-clean-e2e-scene-skill-v11-10ch\\chapter-0001\\primary_prompt.md'),
   'control':'action-anchored-grounding-v1.md',
   'scene':'ENTRY_EXPLORATION',
 },
}
marker='\n\n# PROSE CONTROL A/B — FROZEN TEST BLOCK\n'
for name,c in CASES.items():
    base=c['base'].read_text(encoding='utf-8')
    # Strip any earlier A/B block if rerun.
    if marker in base:
        base=base.split(marker,1)[0].rstrip()+"\n"
    page=(GB/c['control']).read_text(encoding='utf-8')
    abstract,boundary=extract_abstract_content(page)
    if not abstract:
        raise RuntimeError(f'no abstract for {c["control"]}')
    common=(
      marker+
      f'Scene Family: {c["scene"]}\n'
      '实验规则：本区块只控制 how to say；不得改变 Chapter Mission、Canon、BOOK Prose Profile、事件结果、人物决定或场景顺序。\n'
      'Primary Writer 不得讨论实验本身，不得在正文中提及 Prose Control。\n\n'
      '## Relevant Prose Controls\n'
    )
    off=base.rstrip()+common+'无。\n'
    on=base.rstrip()+common+abstract.strip()+('\n\n使用边界：'+boundary.strip() if boundary else '')+'\n'
    d=EXP/name; d.mkdir(parents=True,exist_ok=True)
    (d/'prompt_OFF.md').write_text(off,encoding='utf-8')
    (d/'prompt_ON.md').write_text(on,encoding='utf-8')
    (d/'control_abstract.md').write_text(abstract+(('\n\n'+boundary) if boundary else '')+'\n',encoding='utf-8')
    print(name, 'scene=',c['scene'],'base_chars=',len(base),'off=',len(off),'on=',len(on),'control_chars=',len(abstract))

