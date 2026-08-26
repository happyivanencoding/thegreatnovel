from pathlib import Path
import yaml, json, re
G=Path(r'C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库')
T=Path(r'C:\dev\tgn-story-mvp')
# ---------- helpers ----------
def split_card(path):
    text=path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        raise ValueError(path)
    end=text.find('\n---',3)
    fm=yaml.safe_load(text[3:end]) or {}
    body=text[end+4:].lstrip()
    return fm,body

def dump_card(fm,body,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    raw=yaml.safe_dump(fm,allow_unicode=True,sort_keys=False,width=1000).rstrip()
    path.write_text('---\n'+raw+'\n---\n\n'+body.strip()+'\n',encoding='utf-8')

def strip_to_heading(text, patterns):
    positions=[]
    for pat in patterns:
        m=re.search(pat,text,re.M)
        if m: positions.append(m.start())
    if not positions: return text.strip()
    return text[min(positions):].strip()

# ---------- Prose v2 canonical cards ----------
prose_op=G/'reference-corpus'/'operations'/'gbrain-prose-craft-v2-priority-20260824'
prose_map={
 'gaowu':('rcv0-20-gaowu-quanqiu-gaowu.md','rcv0-20-gaowu-quanqiu-gaowu-prose-dna-v2.md'),
 'chat':('rcv0-03-dushi-xiuzhen-chatianqun.md','rcv0-03-dushi-xiuzhen-chatianqun-prose-dna-v2.md'),
 'firstseq':('rcv0-27-dushi-diyi-xulie.md','rcv0-27-dushi-diyi-xulie-prose-dna-v2.md'),
 'jiangye':('rcv0-28-xuanhuan-jiangye.md','rcv0-28-xuanhuan-jiangye-prose-dna-v2.md'),
 'daogui':('rcv0-18-lingyi-daogui-yixian.md','rcv0-18-lingyi-daogui-yixian-prose-dna-v2.md'),
 'lotm':('rcv0-29-xuanhuan-guimi-zhi-zhu.md','rcv0-29-xuanhuan-guimi-zhi-zhu-prose-dna-v2.md'),
}
keep_keys=['schema_version','card_type','knowledge_level','status','source_book_ids','evidence_refs','creative_problem_tags','reader_experiences','narrative_drives','payoff_channels','evidence_scope','maturity','category_ids','depends_on','source_book_id','title','category','sampling_strategy','coverage_mode','sample_window_count','scene_functions']
for key,(oldfn,newfn) in prose_map.items():
    old=G/'reference-corpus'/'prose-dna'/oldfn
    oldfm,_=split_card(old)
    fm={k:oldfm[k] for k in keep_keys if k in oldfm}
    oldid=oldfm['card_id']
    fm['card_id']=oldid[:-2]+'v2' if oldid.endswith('v1') else oldid+'-v2'
    fm['status']='REFERENCE_ONLY'
    fm['active_inspiration']=False
    fm['prose_dna_schema']='selection-prose-dna-v2'
    fm['derived_from_card_id']=oldid
    fm['source_style_leakage_check']='PASS'
    fm['transfer_boundary']='只迁移词汇选择、句法功能、段落节奏、细节选择、叙述距离、对白功能、动作可视化、信息时序和回报落点；不迁移人物、事件、专名、原句、口癖或签名比喻。'
    body=(prose_op/'materialized'/f'{key}.md').read_text(encoding='utf-8')
    dump_card(fm,body,G/'reference-corpus'/'prose-dna'/newfn)

# Clean prose cross synthesis from final coherent occurrence
cross=json.loads((prose_op/'outputs'/'cross_selection_priority.json').read_text(encoding='utf-8'))['text']
pos=cross.rfind('# Evidence Matrix')
clean=cross[pos:].strip() if pos>=0 else cross.strip()
(prose_op/'CROSS_BOOK_SELECTION_SYNTHESIS_PRIORITY_20260824.md').write_text(clean+'\n',encoding='utf-8')
# HOLD candidate control, not canonical runtime control
hold_dir=prose_op/'staging'/'prose-controls'; hold_dir.mkdir(parents=True,exist_ok=True)
hold_fm={
 'schema_version':'reference-corpus-card-v1','card_id':'prose-character-voice-pressure-routing-v1','card_type':'prose-control',
 'knowledge_level':'CROSS_BOOK_CONTRAST','status':'HOLD','source_book_ids':[ 'rcv0-20-gaowu-quanqiu-gaowu','rcv0-03-dushi-xiuzhen-chatianqun','rcv0-27-dushi-diyi-xulie','rcv0-28-xuanhuan-jiangye','rcv0-18-lingyi-daogui-yixian','rcv0-29-xuanhuan-guimi-zhi-zhu'],
 'evidence_refs':[],'evidence_scope':'MULTI_BOOK','maturity':'PILOT','active_inspiration':False,
 'title':'人物声音压力路由：用不同压力处理方式区分声音（HOLD）'
}
hold_body='''# Character Voice Pressure Routing v1 — HOLD\n\n## Shared Creative Problem\n同一压力进入多个角色后，模型容易把所有人写成冷静、聪明、边界清楚、短句谈条件的同一种声音。\n\n## Mechanism\n只从当前 Canon、关系位置、知识差和已存在的人物行为中选择不同的压力处理通道，例如计算、纠正、嘴硬、玩笑、礼貌、回避、命令、交易或继续行动。声音差异来自“人物注意什么、误判什么、拒答什么、保护什么、把什么当筹码”，而不是额外发明口癖或性格标签。\n\n## Applicability\n只有当前场景存在明显 voice merge 风险，且输入已经支持角色之间不同的知识、利益或反应方式时，才有候选价值。\n\n## Guidance\nCurator 若使用，只应把当前场景的差异编译成 1–2 条局部压力，不要求每个角色都展示独特动作，也不要求对白逐句改变筹码。\n\n## Failure Modes\n- 为区分声音凭空新增性格、过去或口癖。\n- 把“更活泼/更冷”当作人物区分。\n- 为制造人味强行加入停顿、手部动作或玩笑。\n- 把所有场景都变成多人声音展示。\n\n## Evidence Basis\n全球高武、修真聊天群、第一序列、将夜、道诡异仙、诡秘之主的 bounded Selection DNA v2。\n\n## Status\nHOLD。暂不加入生产路由；需要独立 A/B 验证后才能考虑激活。'''
dump_card(hold_fm,hold_body,hold_dir/'character-voice-pressure-routing-v1.md')

# ---------- Story Craft v3 Batch D ----------
story_root=G/'reference-corpus'/'operations'/'gbrain-story-craft-v3'
batch=story_root/'expansion-batch-d-20260824'
staging=batch/'staging'
meta={
 'mushenji':('牧神记','rcv0-41-xuanhuan-mushenji'),
 'dafeng':('大奉打更人','rcv0-42-xianxia-dafeng-dagengren'),
 'gaowu':('全球高武','rcv0-20-gaowu-quanqiu-gaowu'),
 'bukexue':('不科学御兽','rcv0-43-xuanhuan-bukexue-yushou'),
 'cangyuantu':('沧元图','rcv0-44-xuanhuan-cangyuantu'),
 'luanshishu':('乱世书','rcv0-45-xuanhuan-luanshishu'),
 'chaoshen':('超神机械师','rcv0-46-youxi-chaoshen-jixieshi'),
 'mingkejie':('明克街13号','rcv0-47-dushi-mingkejie-13hao'),
 'dawang':('大王饶命','rcv0-48-dushi-dawang-raoming'),
 'manghuangji':('莽荒纪','rcv0-49-xianxia-manghuangji'),
}
book_tags=['读者幻想','世界坐标','能力边界','世界扩张','高价值获得','story-craft-v3']
arc_tags=['longitudinal-thread','thread-braid','玩法选择','敌人反制','阶段变异','promotion-afterlife']
for key,(title,sid) in meta.items():
    luna=(batch/'materialized'/'luna'/f'{key}.md').read_text(encoding='utf-8')
    sol=(batch/'materialized'/'sol'/f'{key}.md').read_text(encoding='utf-8')
    luna=strip_to_heading(luna,[r'^# Evidence Coverage\s*$',r'^# Core Reader Fantasy\s*$'])
    # Preserve title if Sol has it; remove any preamble before first source heading
    sol=strip_to_heading(sol,[r'^# 《[^\n]+》.*$',r'^# Longitudinal Threads\s*$'])
    common={
      'schema_version':'reference-corpus-card-v1','knowledge_level':'BOOK_OBSERVATION','status':'PILOT','source_book_ids':[sid],
      'evidence_refs':[],'reader_experiences':['PROGRESSION','POWER_VERIFICATION','WORLD_EXPANSION','RELATIONSHIP'],
      'narrative_drives':['POWER_PROGRESSION','RELATIONSHIP_EMOTIONAL','WORLD_EXPLORATION'],
      'payoff_channels':['POWER_BREAKTHROUGH','RELATIONSHIP_ADVANCE','WORLD_EXPANSION'],'maturity':'PILOT','source_book_id':sid,
    }
    fm=dict(common); fm.update({'card_id':sid+'-story-craft-v3','card_type':'book-dna','creative_problem_tags':book_tags,'evidence_scope':'SINGLE_BOOK','title':title+'｜Story Craft v3'})
    dump_card(fm,luna,staging/'book-dna'/(sid+'-story-craft-v3.md'))
    fm=dict(common); fm.update({'card_id':sid+'-longitudinal-story-craft-v3','card_type':'arc-observation','creative_problem_tags':arc_tags,'evidence_scope':'LONGITUDINAL_TRAJECTORY','title':title+'｜长期结构 v3','span_kind':'LONGITUDINAL_TRAJECTORY'})
    dump_card(fm,sol,staging/'arcs'/(sid+'-longitudinal-story-craft-v3.md'))

# clean cross syntheses into reports
for src,outname,start in [
 ('cross_world_batch_d.json','CROSS_WORLD_SYNTHESIS_BATCH_D_20260824.md','# Cross-Book Evidence Matrix'),
 ('cross_program_batch_d.json','CROSS_PROGRAM_SYNTHESIS_BATCH_D_20260824.md','# Cross-Book Evidence Matrix')]:
    text=json.loads((batch/'outputs'/src).read_text(encoding='utf-8'))['text']
    pos=text.rfind(start)
    (batch/outname).write_text((text[pos:] if pos>=0 else text).strip()+'\n',encoding='utf-8')

# new mechanism 1: opponent learning
source_ids=[sid for _,sid in meta.values()]
mech_common={'schema_version':'reference-corpus-card-v1','card_type':'mechanism-card','knowledge_level':'CROSS_BOOK_CONTRAST','status':'PILOT','source_book_ids':source_ids,'evidence_refs':[],'reader_experiences':['PROGRESSION','POWER_VERIFICATION','RELATIONSHIP'],'narrative_drives':['POWER_PROGRESSION','IDENTITY_PRESSURE','RELATIONSHIP_EMOTIONAL'],'payoff_channels':['POWER_BREAKTHROUGH','RELATIONSHIP_ADVANCE'],'evidence_scope':'MULTI_BOOK','maturity':'PILOT'}
fm=dict(mech_common); fm.update({'card_id':'mech-opponent-learning-success-condition-rewrite-v3','creative_problem_tags':['敌人反制','敌方学习','成功条件','玩法变异','opponent-adaptation'],'title':'敌方学习：根据已暴露事实改写主角的成功条件'})
body='''Retrieval aliases: opponent learning adaptation counterplay success condition rewrite hide bait block force early use\n\n## Creative Problem\n核心优势第一次公开成功后，如果敌人只提高等级，后续冲突仍会重复同一种能力和同一种解法。\n\n## Mechanism\n对手只能根据已经观察到的动作、战绩、情报或损失学习。它识别主角优势依赖的某个条件，再通过藏手、诱导、封锁、改变目标、逼提前消耗、代理行动或反向利用输入条件，改变胜负结构。反制的价值不是删除核心幻想，而是迫使主角换对象、换时机、换组合、换战场或隐藏新的信息。\n\n## Variants\n- 隐藏关键动作或真实目标。\n- 用假目标/假信息诱导主角浪费优势。\n- 攻击使用窗口、距离、补给、关系或主角不在场的位置。\n- 逼主角提前消耗一次性优势。\n- 学会利用主角必须满足的观察/接触/材料/身份条件。\n\n## Guidance\n先写清敌人看见了什么，再决定它合理能推断什么。第一次反制不必完美；敌人可以试错、误判，再逐步形成真正有效的新策略。\n\n## Failure Modes\n- 敌人凭空知道秘密或读取系统说明书。\n- 反制只是加血、免疫或更高等级。\n- 每次都用同一种封锁。\n- 能力被完全封死，主角没有新的选择。\n- 退化成程序化“反制—反反制”循环。\n\n## Evidence Basis\nBatch D 十本均观察到跨阶段 opponent adaptation：不科学御兽、沧元图、大奉打更人、大王饶命、全球高武、乱世书、莽荒纪、明克街13号、牧神记、超神机械师。详见 `CROSS_PROGRAM_SYNTHESIS_BATCH_D_20260824.md`。\n\n## Transfer Boundary\n迁移“敌人基于已暴露事实学习并改变成功条件”的结构；不要求每个敌人都理解完整机制，不规定固定反制形式。'''
dump_card(fm,body,staging/'mechanisms'/'opponent-learning-success-condition-rewrite-v3.md')
# new mechanism 2: thread dormancy-collision-afterlife
fm=dict(mech_common); fm.update({'card_id':'mech-longitudinal-thread-dormancy-collision-afterlife-v3','creative_problem_tags':['长线伏笔','沉睡','提醒','thread-collision','second-payoff','afterlife'],'title':'长线余生：沉睡、行动性提醒、碰撞与二次兑现'})
body='''Retrieval aliases: longitudinal thread dormancy reminder collision second payoff afterlife thread braid\n\n## Creative Problem\n长线容易退化成角色名单或伏笔台账：为了不忘而频繁提醒，高潮只结算输赢，第一次兑现后人物或关系立即冻结。\n\n## Mechanism\n以具体欲望、关系、身份、物件或世界问题建立线程；允许它自然休眠或离屏推进。只有当新处境会改变这条线的含义、可行性或人物选择时，用行为、选择、新证据或新位置召回。成熟时让它与当前力量、关系、身份或世界线发生真实因果碰撞，产生不可回滚状态。第一次 payoff 后，继续保留人物新的生活、关系、权限、敌人或自主目标，形成 second payoff / afterlife。\n\n## Variants\n- 关系线长期离屏后以新生活状态回归。\n- 旧身份在新地图被重新定价。\n- 旧物/旧能力从工具变成关系或世界入口。\n- 私人欲望在世界级事件中改变最终选择。\n- 大战同时结束旧仇并开启新的生活或权力位置。\n\n## Guidance\nReminder 必须改变当前行动或解释，不以“提到一次”保活。碰撞不追求固定线数；只要异质线程真正互相改写即可。兑现后优先问“人物现在能做什么、还想做什么、谁会因此改变策略”。\n\n## Failure Modes\n- 只回忆，不改变行动。\n- 为了多线汇合强行巧合。\n- 所有配角都等待主角召回。\n- 大战只结算输赢。\n- Afterlife 只是同类考核重开。\n- 把开放或未知结局补成完整战后秩序。\n\n## Evidence Basis\nBatch D 十本均支持长线沉睡、行动性提醒、碰撞与兑现余生；详见 `CROSS_PROGRAM_SYNTHESIS_BATCH_D_20260824.md`。\n\n## Relationship to Existing Cards\n与 `thread-ecology-v3`、`thread-collision-v3`、`reward-afterlife-v3` 相邻，但补足“第一次兑现之后人物/线程继续拥有行动位置”的完整跨阶段结构。\n\n## Transfer Boundary\n迁移线程生命周期与 afterlife，不要求每条长线都有二次兑现，不要求所有线程在终局汇合。'''
dump_card(fm,body,staging/'mechanisms'/'longitudinal-thread-dormancy-collision-afterlife-v3.md')

# synthesis cards imported as reference only
synth_dir=staging/'syntheses'; synth_dir.mkdir(parents=True,exist_ok=True)
for name,title,report,stage in [
 ('reader-facing-world-coordinates-batch-d-v3','Batch D｜世界可读坐标、能力兼容与晋升后世界打开','CROSS_WORLD_SYNTHESIS_BATCH_D_20260824.md','World Vision / Outline'),
 ('gameplay-counterplay-thread-afterlife-batch-d-v3','Batch D｜玩法选择、敌方学习、长线碰撞与兑现余生','CROSS_PROGRAM_SYNTHESIS_BATCH_D_20260824.md','Story Program / Outline')]:
    fm={'schema_version':'reference-corpus-card-v1','card_id':'synth-'+name,'card_type':'synthesis','knowledge_level':'CROSS_BOOK_CONTRAST','status':'REFERENCE_ONLY','source_book_ids':source_ids,'evidence_refs':[],'creative_problem_tags':['cross-book-synthesis','story-craft-v3'],'evidence_scope':'MULTI_BOOK','maturity':'PILOT','active_inspiration':False,'title':title,'stage':stage}
    dump_card(fm,(batch/report).read_text(encoding='utf-8'),synth_dir/(name+'.md'))

# prose synthesis reference card
fm={'schema_version':'reference-corpus-card-v1','card_id':'synth-prose-selection-priority-20260824','card_type':'synthesis','knowledge_level':'CROSS_BOOK_CONTRAST','status':'REFERENCE_ONLY','source_book_ids':hold_fm['source_book_ids'],'evidence_refs':[],'creative_problem_tags':['selection-policy','character-voice','causal-stop','reaction','rhythm'],'evidence_scope':'MULTI_BOOK','maturity':'PILOT','active_inspiration':False,'title':'Priority Prose v2｜人物声音、状态可读性与解释停点跨书综合'}
dump_card(fm,clean,prose_op/'staging'/'syntheses'/'priority-selection-synthesis-20260824.md')

# source registry append
registry=story_root/'SOURCE_REGISTRY.md'
text=registry.read_text(encoding='utf-8').rstrip()
append='''\n\n## Batch D 2026-08-24\n\n| key | source_book_id | source file | encoding | current corpus status |\n|---|---|---|---|---|\n'''
manifest={x['key']:x for x in json.loads((batch/'source_manifest.json').read_text(encoding='utf-8'))}
for key,(title,sid) in meta.items():
    m=manifest[key]; raw=Path(m['raw_path']); rel=raw.relative_to(G/'小说整理合集')
    status='existing source; Batch D Story Craft v3 refresh' if key=='gaowu' else 'NEW PILOT; Batch D Story Craft v3'
    append+=f'| {key} | `{sid}` | `小说整理合集/{rel.as_posix()}` | {m["encoding"].upper()} | {status} |\n'
if '## Batch D 2026-08-24' not in text:
    registry.write_text(text+append,encoding='utf-8')

print('prose v2 cards',sum(1 for _,(_,f) in prose_map.items() if (G/'reference-corpus'/'prose-dna'/f).exists()))
print('story book cards',len(list((staging/'book-dna').glob('rcv0-4*-story-craft-v3.md')))+int((staging/'book-dna'/'rcv0-20-gaowu-quanqiu-gaowu-story-craft-v3.md').exists()))
print('batch D arcs',len([p for p in (staging/'arcs').glob('*longitudinal-story-craft-v3.md') if any(sid in p.name for _,sid in meta.values())]))
print('new mechanisms',[p.name for p in (staging/'mechanisms').glob('*v3.md') if p.name in {'opponent-learning-success-condition-rewrite-v3.md','longitudinal-thread-dormancy-collision-afterlife-v3.md'}])
