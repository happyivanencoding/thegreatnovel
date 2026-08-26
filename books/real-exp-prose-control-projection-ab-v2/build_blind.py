from pathlib import Path
import json,random,re
EXP=Path(r'C:\dev\tgn-story-mvp\books\real-exp-prose-control-projection-ab-v2')
rng=random.Random(202608241134)
key={}
parts=["""你是成熟中文男频正文盲评审稿人。下面有3个不同 Scene 的成对正文。每组 X/Y 使用同一 Chapter Mission、Canon、BOOK Prose Profile 与同一 Terra Primary Writer；你不知道实验条件。\n\n逐组比较，只看成品正文。重点：\n1. 一遍读懂、自然顺畅；\n2. 用词、句式、段落是否像真实小说而非AI方法论执行；\n3. Story-bearing detail 与人物微反应是否有效；\n4. 是否少用“意味着/说明/显然/可以看出/这不是而是”等动作后抽象复述；\n5. 是否忠实于冻结 Mission，不擅自补交易条件、规则、能力或后果；\n6. Scene 专项：Action 看空间因果；Dialogue 看潜台词和筹码变化；Entry 看动作先行和信息负担。\n\n每组输出 X分/Y分（0-10）、Winner、Margin、Confidence，并给3-6条具体理由及 Winner 仍有的问题。最后分别给 Action / Dialogue projection / Entry projection 一个产品判断：PROMOTE / KEEP OPTIONAL / REJECT。不要推测 X/Y 是什么实验条件。"""]
for case,title in [('action_retest','ACTION — public contest / close combat'),('dialogue_projection','DIALOGUE — negotiation'),('entry_projection','ENTRY — opening / escape')]:
    off=(EXP/case/'draft_OFF.md').read_text(encoding='utf-8')
    on=(EXP/case/'draft_ON.md').read_text(encoding='utf-8')
    base=(EXP/case/'prompt_OFF.md').read_text(encoding='utf-8')
    m=re.search(r'## Chapter Mission.*?(?=\n## CANON PROSE|\n# CANON PROSE|\n## CANON INDEX|\n# CANON INDEX)',base,re.S)
    mission=m.group(0).strip() if m else ''
    if rng.random()<0.5:
        X,Y=off,on; key[case]={'X':'OFF','Y':'ON'}
    else:
        X,Y=on,off; key[case]={'X':'ON','Y':'OFF'}
    parts.append(f"\n\n===== CASE {title} =====\n\n### FROZEN MISSION\n{mission}\n\n### VERSION X\n{X}\n\n### VERSION Y\n{Y}")
prompt='\n'.join(parts)
(EXP/'blind_prompt.md').write_text(prompt,encoding='utf-8')
(EXP/'blind_key.json').write_text(json.dumps(key,ensure_ascii=False,indent=2),encoding='utf-8')
print(key); print('chars',len(prompt))
