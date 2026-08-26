from pathlib import Path
import json,random
root=Path(r'C:\dev\tgn-story-mvp\books\real-exp-prose-control-ab-multiscene-v1')
missions={
 'dialogue': Path(r'C:\dev\tgn-story-mvp\books\real-exp-clean-e2e-scene-skill-v11-10ch\chapter-0004\director_response.md'),
 'action': Path(r'C:\dev\tgn-story-mvp\books\real-exp-clean-e2e-scene-skill-v11-10ch\chapter-0006\director_response.md'),
 'payoff': Path(r'C:\dev\tgn-story-mvp\books\real-exp-human-reaction-ch3-v1\after-v2\director_response.md'),
 'entry': Path(r'C:\dev\tgn-story-mvp\books\real-exp-clean-e2e-scene-skill-v11-10ch\chapter-0001\director_response.md'),
}
scene_labels={
 'dialogue':'Dialogue / Negotiation',
 'action':'Action / Pursuit',
 'payoff':'Payoff / Public Proof',
 'entry':'Entry / Opening / Exploration',
}
r=random.Random(20260824)
key={}
chunks=[]
for case in ['dialogue','action','payoff','entry']:
    arms=['OFF','ON']; r.shuffle(arms)
    key[case]={'X':arms[0],'Y':arms[1]}
    mission=missions[case].read_text(encoding='utf-8').strip()
    x=(root/case/f'{arms[0]}_body.md').read_text(encoding='utf-8').strip()
    y=(root/case/f'{arms[1]}_body.md').read_text(encoding='utf-8').strip()
    chunks.append(f'''# CASE {case.upper()} — {scene_labels[case]}

## Frozen Chapter Mission
{mission}

## Version X
{x}

## Version Y
{y}
''')
prompt='''你是中文男频网文正文盲评审稿人。下面有4组 A/B，每组两篇都由同一模型、同一 Chapter Mission、同一 Canon、同一 BOOK Prose Profile 生成；你不知道哪一篇使用了额外的 prose control，也不要猜实验标签。

你的任务不是评价剧情设计，而是比较“同一件事怎样写出来”。重点判断：
1. Chapter Mission / Canon fidelity：有没有偷偷改事实、漏掉直接结果、提前结算未发生内容。
2. Reader-first clarity：普通读者一遍能否知道谁做了什么、为什么、结果是什么。
3. Diction specificity：具体名词/动词是否承担意义，是否少依赖抽象词、泛化判断、同义解释。
4. Sentence & paragraph function：长短句、断段是否跟随真实状态变化，而不是机械碎段或均匀节奏。
5. Story-bearing detail：细节是否改变力量、关系、身份、风险、位置或下一步，而非只做环境装饰。
6. Human / embodied reaction：人物反应是否具体、个体化且有后果；避免“众人震惊/心情复杂”模板。
7. Scene-specific execution：
   - Dialogue：对白是否真正改变筹码/关系/主动权，而不是轮流解释。
   - Action：位置、方向、接触、受力、结果是否可追踪，又不逐招流水账。
   - Payoff：结果是否先成立，再通过相关人物/环境/身份变化留下余波，不用作者总结冲淡爽点。
   - Entry：是否从人物正在做的事、局部异常和即时限制进入，不先做世界导览。
8. AI味与 procedural expansion：是否出现“信息都对但像系统报告”、解释机制过头、规划语言泄漏、连续排除式句型、环境很细但人物没生命。

对每组：
- 分别给 X/Y 0-10 总分（可一位小数）。
- 明确选择 Winner: X / Y / TIE。
- 给 3-6 条最关键理由，必须落到具体文字行为，不要只说“更自然”。
- 指出 Winner 仍然存在的1-3个问题。
- 评估置信度 high / medium / low。

最后输出总表：CASE | X | Y | Winner | Margin | Confidence。
再回答：如果这是一个“是否默认开启新的 Prose Control”的产品决策，证据支持 `FREEZE ON`、`KEEP OPTIONAL` 还是 `REJECT`？必须基于跨场景一致性，不允许因为单个场景胜出就宣布冻结。

不要提模型名称，不要推测哪一边是实验组。

'''+"\n\n".join(chunks)
(root/'blind_judge_prompt.md').write_text(prompt,encoding='utf-8')
(root/'blind_key.json').write_text(json.dumps(key,ensure_ascii=False,indent=2),encoding='utf-8')
print(key)
print('prompt chars',len(prompt))
