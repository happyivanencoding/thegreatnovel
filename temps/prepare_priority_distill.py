from pathlib import Path
import json, hashlib, re
G=Path(r'C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库')
T=Path(r'C:\dev\tgn-story-mvp')
prose_op=G/'reference-corpus'/'operations'/'gbrain-prose-craft-v2-priority-20260824'
story_op=G/'reference-corpus'/'operations'/'gbrain-story-craft-v3'/'expansion-batch-d-20260824'
for d in [prose_op/'prompts', prose_op/'outputs', story_op/'prompts', story_op/'outputs'/'luna', story_op/'outputs'/'sol']:
    d.mkdir(parents=True, exist_ok=True)
contract=G/'reference-corpus'/'operations'/'gbrain-prose-craft-v2-20260824'/'SELECTION_DNA_V2_CONTRACT.md'
prose=[
 ('gaowu','全球高武','rcv0-20-gaowu-quanqiu-gaowu.md'),
 ('chat','修真聊天群','rcv0-03-dushi-xiuzhen-chatianqun.md'),
 ('firstseq','第一序列','rcv0-27-dushi-diyi-xulie.md'),
 ('jiangye','将夜','rcv0-28-xuanhuan-jiangye.md'),
 ('daogui','道诡异仙','rcv0-18-lingyi-daogui-yixian.md'),
 ('lotm','诡秘之主','rcv0-29-xuanhuan-guimi-zhi-zhu.md'),
]
jobs=[]
for key,title,fn in prose:
    src=G/'reference-corpus'/'prose-dna'/fn
    prompt=f'''你正在执行 GBrain Prose Craft v2 的 Selection DNA 升级。\n\n必须读取：\n- {contract}\n- {src}\n\n书：{title}\n\n目标：把现有 v1 Prose DNA / scene-function evidence 重组为 selection-prose-dna-v2。\n\n硬边界：\n- 只使用上面旧卡中已有 evidence_refs、scene_functions、evidence summaries 与 prose observations；本轮不要重新读取原著，不用模型记忆补证据。\n- 证据不足处写 INSUFFICIENT，不为凑六维制造结论。\n- 输出严格遵守 SELECTION_DNA_V2_CONTRACT 的固定结构：Attention / Knowledge / Causal / Reaction / Rhythm / Lexical + Detail Selection。\n- 重点寻找“作者在什么状态变化时给带宽、何时停止解释、人物状态怎样通过动作/对白泄露、句段怎样随 beat 改变、句子落在什么具体名词/动词上”。\n- 不写禁词表，不写模仿句式，不把 source-specific 人物/专名/事件变成通用规则。\n- Production Implications 只给 Curator 4–6 条正向、scene-conditioned 选择原则；不要变成 Writer hard gates。\n- 明确列出 Evidence Basis，并保留旧卡已有 locator/evidence ID，不新造原文 locator。\n\n只输出最终 Markdown，不修改文件。'''
    pp=prose_op/'prompts'/f'{key}_prose_v2.md'; pp.write_text(prompt,encoding='utf-8')
    jobs.append({'id':f'prose-{key}','kind':'prose','title':title,'prompt':str(pp),'output':str(prose_op/'outputs'/f'{key}.json'),'model':'gpt-5.6-luna','effort':'high'})

story_meta=json.loads((story_op/'SOURCE_MANIFEST.json').read_text(encoding='utf-8')) if (story_op/'SOURCE_MANIFEST.json').exists() else json.loads((story_op/'source_manifest.json').read_text(encoding='utf-8')) if (story_op/'source_manifest.json').exists() else None
# use batch source manifest produced earlier
batch_manifest=json.loads((story_op/'source_manifest.json').read_text(encoding='utf-8')) if (story_op/'source_manifest.json').exists() else []
if not batch_manifest:
    # infer from indexes + known paths
    candidates=[
    ('mushenji','牧神记','01_玄幻'),('dafeng','大奉打更人','02_仙侠'),('gaowu','全球高武','09_高武'),('bukexue','不科学御兽','01_玄幻'),('cangyuantu','沧元图','01_玄幻'),('luanshishu','乱世书','01_玄幻'),('chaoshen','超神机械师','08_游戏'),('mingkejie','明克街13号','03_都市'),('dawang','大王饶命','03_都市'),('manghuangji','莽荒纪','02_仙侠')]
    batch_manifest=[]
    for key,title,cat in candidates:
        raw=G/'小说整理合集'/cat/f'{title}.txt'
        idx=story_op/'indexes'/f'{key}.md'
        batch_manifest.append({'key':key,'title':title,'raw_path':str(raw),'index_path':str(idx)})

focus={
'mushenji':'世界奇观与世界层级持续打开；力量升级后故事问题怎样改变；旧人物与关系怎样跨世界尺度继续有效。',
'dafeng':'复杂世界如何保持可读；调查/修炼/身份/关系/喜剧如何换发动机而不程序化；角色生态和阶段性公开证明。',
'gaowu':'清晰力量尺如何服务危险感与爽点；公开证明、社会反馈、身份跃迁与商业节奏；同一成长主循环怎样持续变异。',
'bukexue':'多成长对象与伙伴自治；宠兽/技能/资源/身份如何互相反哺但不变成库存管理；高价值获得怎样打开新玩法。',
'cangyuantu':'力量层级与战斗差距如何一眼可读；突破如何改变能做什么；大敌压力、家庭/师承与世界扩张怎样连接。',
'luanshishu':'人物关系、欲望和武力成长怎样共同推动剧情；长期竞争/情感人物怎样回流；不同阶段战斗目标怎样变化。',
'chaoshen':'长篇复利、阵营与地图扩张、身份反转、旧能力/旧资产换场景复用；特别区分故事复利与游戏系统/运营表面。',
'mingkejie':'人物声音、家庭/关系发动机、世界入口与身份秘密；氛围如何转成行动；长线人物怎样自主回流而非功能化。',
'dawang':'人物声音、喜剧与社会反馈如何成为故事发动机；力量成长如何和关系/群体评价咬合；旧梗如何产生后续状态变化。',
'manghuangji':'传统力量成长和世界尺度扩张；境界/强者如何成为读者尺子；突破、传承、地图升级怎样持续制造新的欲望而非只增数值。'
}
readme=G/'reference-corpus'/'operations'/'gbrain-story-craft-v3'/'README.md'
needs=G/'reference-corpus'/'operations'/'gbrain-story-craft-v3'/'TGN_NEEDS_MAP.md'
for m in batch_manifest:
    key,title=m['key'],m['title']; raw=Path(m['raw_path']); idx=Path(m['index_path'])
    common=f'''你正在执行 GBrain Story Craft v3 的 SOURCE-FIRST 蒸馏。\n\n必须先阅读：\n- {readme}\n- {needs}\n\n书：{title}\n原文：{raw}\n章节索引：{idx}\n\n本书重点：{focus[key]}\n\n绝对规则：\n- 原文是唯一剧情事实来源，不准用模型记忆补剧情。\n- 先记录“发生了什么 / 人物想要什么 / 做了什么 / 结果改变什么”，再做抽象。\n- 关键 source-specific 结论必须给章节标题或 line locator；索引不足时用 Python 只读原文建立定位。\n- 要跨开篇、前中期、中后期、终局抽样，不能只看开头。\n- 不复制长原文，只做短摘要与 locator。\n- 不默认治理、责任、对称成本、制度成熟是高级答案；原文不是主轴就不要补。\n- 不把超凡玩法自动翻译成工程流程、资产网络、权限树或运营系统。\n- 输出只做 REFERENCE_ONLY/PILOT 研究，不修改文件。\n'''
    luna=common+'''\n任务：LUNA HIGH — Book DNA + World Fantasy。\n\n输出：\n# Evidence Coverage\n# Core Reader Fantasy\n# Protagonist Desire & Agency\n# Reader-Facing World Coordinates（原作实际怎样让读者判断强弱/身份/价值/危险；若无明确等级就写行动阈值）\n# Core Advantage / Power Experience\n# World Fantasy Ladder\n# Major Character & Relationship Engines\n# Payoff Grammar\n# Repeatable Story Engines（1–3个即可）\n# World Expansion Grammar\n# TGN Transfer（Fantasy Seed / World Vision / Story Program / Outline 分开）\n# Evidence Anchors（至少15个，跨不同阶段）\n# Bias Check\n\n尤其注意：世界坐标是“读者怎么读懂差距”，不是强制制作等级表。'''
    sol=common+'''\n任务：SOL HIGH — Longitudinal Threads + Story Program Patterns。\n\n找出6–10条最有长篇价值的纵向故事线。每条输出：Thread name / Length class / Setup / Dormancy / Reminder / Escalation / Collision / Payoff / Second Payoff or Afterlife / Why Reader Cares / Story State Change / Evidence Anchors。\n\n然后输出：\n# Thread Braid Map（至少4个真正同时结算/重写多线的碰撞点）\n# Short / Medium / Long Thread Grammar\n# Core Gameplay Choice Space（核心能力/成长最有趣的选择是什么，为什么表面最强不总是最优；如不适用明确说不适用）\n# Opponent Adaptation Grammar（对手/世界怎样学会针对主角，避免只换更强敌人）\n# Story Program Engine Variation\n# Promotion / Breakthrough Afterlife（晋升、突破或身份跃迁后，世界具体打开了什么，而非只更新称号）\n# TGN Story Program Inspirations（5–10条抽象原则）\n# Anti-Systemization Check\n\n重点分析为什么这本书能写很长且不只是重复同类任务。'''
    lp=story_op/'prompts'/f'{key}_luna.md'; sp=story_op/'prompts'/f'{key}_sol.md'; lp.write_text(luna,encoding='utf-8'); sp.write_text(sol,encoding='utf-8')
    jobs += [
      {'id':f'story-{key}-luna','kind':'story-luna','title':title,'prompt':str(lp),'output':str(story_op/'outputs'/'luna'/f'{key}.json'),'model':'gpt-5.6-luna','effort':'high'},
      {'id':f'story-{key}-sol','kind':'story-sol','title':title,'prompt':str(sp),'output':str(story_op/'outputs'/'sol'/f'{key}.json'),'model':'gpt-5.6-sol','effort':'high'}]
manifest={'gbrain_root':str(G),'jobs':jobs}
(T/'temps'/'priority_distill_jobs.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('jobs',len(jobs),'prose',sum(j['kind']=='prose' for j in jobs),'story',sum(j['kind'].startswith('story') for j in jobs))
print('manifest',T/'temps'/'priority_distill_jobs.json')
