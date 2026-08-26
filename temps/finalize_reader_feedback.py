from pathlib import Path
import json,re
exp=Path(r'C:\dev\tgn-story-mvp\books\reader-feedback-prose-v1')
plan=(exp/'CONTINUATION_PLAN.md').read_text(encoding='utf-8')
parts=['# 顾长川 Chapter 4—8｜Reader Feedback 原始阅读版','', '> 以下正文均为当前冻结流水线直接生成结果，未经过后置 Humanizer、Reviewer 或人工润色。阅读时只需要按读者直觉标记“这里怪 / 没看懂 / 很好 / 特别喜欢”。','']
for n in range(4,9):
    m=re.search(rf'^## Chapter {n}:\s*(.+)$',plan,re.M)
    title=m.group(1).strip() if m else f'Chapter {n}'
    body=(exp/'chapters'/f'chapter-{n:04d}.md').read_text(encoding='utf-8').strip()
    parts += [f'## 第{n}章　{title}','',body,'']
(exp/'READER_COPY.md').write_text('\n'.join(parts).rstrip()+'\n',encoding='utf-8')

calls=[]
cp=json.loads((exp/'continuation_plan_acp.json').read_text(encoding='utf-8'))
calls.append({'stage':'continuation_plan','model':cp.get('model'),'effort':cp.get('effort'),'ok':cp.get('ok'),'wall_seconds':cp.get('wall_seconds')})
for n in range(4,9):
    rd=exp/'runs'/f'chapter-{n:04d}'
    for stage in ('director','curator','primary','state'):
        j=json.loads((rd/f'{stage}_acp.json').read_text(encoding='utf-8'))
        calls.append({'chapter':n,'stage':stage,'model':j.get('model'),'effort':j.get('effort'),'ok':j.get('ok'),'wall_seconds':j.get('wall_seconds')})
(exp/'CALL_LOG.json').write_text(json.dumps(calls,ensure_ascii=False,indent=2),encoding='utf-8')

experiment='''# Reader Feedback Prose v1\n\n## Purpose\n\nUse the frozen Selection Prose DNA v2 + Scene Prose Projection runtime to generate five consecutive chapters before any reader-guided learning exists. The user is asked to react as a reader, not rewrite as an author.\n\n## Source\n\n- Canon/fantasy source: `books/real-exp-human-reaction-ch3-v1` through Chapter 3.\n- The old source experiment's “stop after Chapter 3” marker is superseded only inside this new experiment by the user's explicit authorization to continue.\n- Chapter 1—3 Canon, ability limits, relationships and injuries remain authoritative.\n\n## Generated Window\n\n- Chapter 4—8.\n- Continuation planning: GPT-5.6 Luna high.\n- Director: GPT-5.6 Luna high.\n- Curator: GPT-5.6 Luna high.\n- Primary Writer: GPT-5.6 Terra high.\n- State Extraction: GPT-5.6 Luna low.\n- No specialists / integrator / Humanizer / prose reviewer.\n- Curator may output `NONE` or 2—4 sentence Scene Prose Projection.\n\n## Reader Feedback Contract\n\nNo automatic rewrite is performed before human reading. Useful signals are simply: “这里怪”, “这里没看懂”, “这里很好”, “特别喜欢这种感觉”, optionally with the marked span. The next system stage should diagnose those signals and offer local alternatives rather than require the reader to rewrite prose.\n'''
(exp/'EXPERIMENT.md').write_text(experiment,encoding='utf-8')
print('reader copy chars',len((exp/'READER_COPY.md').read_text(encoding='utf-8')))
print('call log',len(calls))
