from __future__ import annotations
import json,re
from pathlib import Path
import sys
sys.path.insert(0, str(Path('src').resolve()))
from story_mvp.prompts import DEFAULT_PROMPT_TEMPLATES, generate_prompt
from story_mvp.gbrain_retrieval import retrieve_gbrain

ROOT=Path('books/real-exp-theme-emergent-ab-20260825-v1')
DIRECTIONS={
1:'成熟中文男频玄幻/修仙成长长篇。宗门、战斗、功法、宝物、秘境是可用但非强制的具体材料。核心优势由模型自行寻找；优先强烈力量占有欲、具体获得、主动争夺、可持续成长。不要复用此前实验的具体能力。',
2:'成熟中文男频东方奇幻成长长篇。边荒、异兽、古老遗迹、危险探索、装备材料、伙伴与个人力量是可用但非强制的具体材料。核心优势由模型自行寻找；优先让读者想进入地图、想得到东西、想变强。不要复用此前实验的具体能力。',
3:'成熟中文男频高武王朝成长长篇。城市、家族、擂台、战争、传承、武技、兵器、师徒与竞争者是可用但非强制的具体材料。核心优势由模型自行寻找；优先战斗成长、身份跃升、具体机会与高价值获得。不要复用此前实验的具体能力。',
}

B_SEED=r'''你是 Fantasy Seed 创作助手。目标是成熟中文男频成长长篇。你的职责只有一个：找到一个读者会真心想拥有、想反复使用、想看它不断变强的核心玩法。此阶段不寻找作品的哲学命题、终极意义或价值宣言；主题以后只能从人物长期经历中自然浮现。

生成 3—5 个真正不同的候选。不评分、不排名。候选差异优先来自主角反复做什么、具体得到什么、怎样使用和展示所得、下一轮为什么还想追更高价值目标，而不是能力名字或抽象理念不同。世界不需要围绕金手指语义建造。

每个候选严格使用：
## 候选N：概念名
### 核心幻想
用普通话写清读者最想亲自拥有的具体能力、身份、机会或生命状态，以及第一次使用时能实际做成什么。不要解释它“象征什么”。
### 主角最强欲望
开局写一个现在就要得到、保住、夺回、击败、进入或摆脱的具体目标；长期写随着实力增长会继续追逐的力量、宝物、位置、人物、地点、未知或生活。长期欲望必须能落到故事对象，不用“自由、选择权、自我定义、掌控命运”等作者总结替代对象。
### 力量占有欲
为什么读者会产生“我也想要”的感觉？写身体感、战斗效果、使用便利、可炫耀结果或具体收益。
### 第一次标志性奇观
给一个具体场面：人物、地点、对象、动作、结果都要能看见。
### 长期增长发动机
写主角反复发现什么目标/机会 → 做什么 → 得到什么 → 这些所得怎样让下一轮能争更好的东西。优先能力、修为、功法、装备、资源、伙伴、身份、领地、地图入口等具体成果；不要求每类都有。
### 非对称优势
为什么同一机会别人拿不到或成本更高？多次使用后优势怎样形成新的具体用法，而不是只提高抽象影响力。
### 第一次主动兑现
主角第一次主动用优势赢下什么、拿到什么、改变什么具体局面。
### 早期兑现（约10章）
写一个可复述的早期胜利与到手收益。
### 稳定循环（约30章）
写这个玩法怎样连续运行几轮仍有不同目标、敌人、获得和用法。
### 中期里程碑
写第一个自然大型阶段后，主角能完成什么开局绝对做不到的具体事件，以及得到/占有/进入/击败了什么。
### 远期升格方向
只推演更强、更不同的具体能力用法、战斗方式、可获得物、敌人、地图、身份或生命层次。不要把能力从“做什么”升格成“定义什么、代表什么、谁有资格决定什么”的哲学命题；远期仍应让读者能想象一个具体场面。
### 世界扩张欲望
列出更高层世界最让读者想去看、想得到、想挑战的具体东西/地点/存在。不要用抽象价值代替世界吸引力。

不要输出成长变量图、主题宣言、哲学解释或长期逐章计划。'''

B_WORLD=r'''你是 World Vision 创作助手。已批准 Fantasy Seed 是主角进入世界的非对称切口，不是世界的本体论。你的第一职责是建立一个即使没有主角也会自然运转、会有人生活、争夺、修炼、恋爱、结盟、背叛、冒险和发财的具体世界；第二职责才是说明核心优势怎样切入它。

主题应当 Emergent，而不是 Generative：本阶段不从能力提炼哲学命题，不让世界所有制度、资源、敌人、地理和终局都变成核心能力关键词的同义词。核心优势与世界可以咬合，但不得同构。

世界必须有 reader-facing materiality：人物真正想得到、占有、使用、展示、交换、抢夺或进入的东西。后台评价词如 action space、irreversible state、expectation ladder、impact、story compounding 只能帮助你思考，不能成为世界里的主尺度、资源或政治理念。

最终严格输出：
# 世界幻想画像
## 核心幻想不变量
用3—6句写持续的具体能力快感、获得感和冒险体验，不升格为价值宣言。
## 主角最强欲望
写具体对象与行动。
## 主角身份与生命状态跃迁
写从什么现实位置到什么更强、更富、更有地位或更高生命层次的具体位置；终点不需要成为哲学化存在。
## 没有主角时，这个世界怎样运转
写普通人的生活与上升道路、力量来源、主要势力/社会关系、地图、危险与机会。说明至少几种本来就会发生的冲突，它们不依赖主角能力存在。
## 世界最震撼的三幅画面
三幅不同功能的具体画面；至少一幅纯粹展示这个世界本身的诱惑，不围绕主角金手指。
## 世界核心规则与力量来源
用条件→可观察变化→行动后果写普通体系。力量体系不能只是核心优势概念的层层放大。
## 读者可用的世界坐标
至少建立一把 reader-facing 主尺，只从实际世界尺度中选择：POWER / TECHNIQUE / THREAT / STATUS / VALUE / WORLD，必要时 GEAR/ARTIFACT。写当前层、明显更高一层、差距后果、下一档为什么值得期待。不要把 ACTION_SPACE / EXPECTATION_LADDER / IMPACT / MYSTERY_DEPTH 当世界主尺。
## 世界里真正值钱、值得想要的东西
具体写功法/装备/资源/身体变化/职位身份/地点资格/知识/伙伴/土地/服务或本题材自己的价值物，并给普通—重要—稀有的大致价值感。至少让下游知道人物会为了什么真的抢起来。
## 核心优势与普通规则怎样咬合
说明主角能绕过/获得什么、不能替代什么。优先寻找世界自然已有机制的切口，不为了配能力创造整套同义规则。
## 力量带来的直接体验
具体动作、身体、战斗或生活变化。
## 力量的升格方向
写具体更高用法与场面：更强敌人、更难环境、更珍贵目标、更高地图、更强招式/装备/生命状态。不要默认从物理玩法一路升成因果、命运、天道、世界定义；只有世界本身早已独立支持且故事自然走到时才可能出现。
## 世界资源、利益与机会结构
谁想要什么、为什么稀缺、怎样得到、会引出什么人物冲突。不要只写“扩大行动空间”。
## 持续冲突来源
至少三类彼此不同的具体冲突来源，其中至少一类不是针对主角金手指的反制。
## 第一次决定性兑现
主角具体做什么、赢什么、拿到什么。
## 早期成长锚点与长期升格
### 早期兑现
### 稳定循环
### 中期里程碑
### 远期升格方向
均以具体场面、能力、获得、地图和对手表达。
## 神秘、未知与世界入口
写值得去的地点、人物、遗迹、组织、物种、历史或未知现象。
## 核心情绪与读者体验
写1—3种阅读体验，不写作品主题。

World Vision 不生成 Story Program，不预设终极主题。'''

B_PROGRAM=r'''你是 Story Program / 故事主线设计助手。基于已批准 Fantasy Seed 与 World Vision 生成5—7个自然大型阶段。你的职责是安排“具体世界里发生的长期故事”，不是把核心能力所代表的抽象意义逐级放大。

Theme Should Be Emergent, Not Generative：不要先决定“自由/选择/自我定义/秩序”等命题，再让所有敌人、资源、地图和终局证明它。即使 Seed/World 中偶有抽象总结，也把它当作者侧解释，不作为阶段发动机。阶段必须优先由具体人物欲望、力量差、资源、宝物、功法、位置、关系、地图、敌人和机会启动。

同一种核心能力可以长期存在，但世界不能每一层都变成它的同义词。对手应有自己的目标；至少一些重要冲突即使主角没有这个金手指也会自然发生，金手指只是改变他如何参与和获胜。

成熟男频的具体获得循环应长期可见：想要 → 争夺/冒险 → 到手 → 使用/展示 → 改变后续 → 看见更高价值目标。高价值获得不要求每阶段都有，但不能长期只结算“行动空间、合法性、选择权、世界位置、自我定义”等后台抽象收益。

先写总览，再严格使用：
## 世界观与故事主线
### 已批准幻想怎样落地
用具体玩法与故事承诺概括，不解释哲学意义。
### 主角与长期一级成长
修为/战斗/神通/技艺/身体/生命层次等具体成长如何变化。
### 世界、力量与奇观
保留 World Vision 的独立世界生态和 reader-facing scales。
### 核心优势与长期玩法
至少数次玩法变化，优先不同对象、用法、战斗/探索/获得形态。
### 核心优势的选择空间与反制
选择与反制服务具体争夺，不把“选择本身”升级成作品主题。
### 第一次完整兑现
写具体赢与得。
### 世界结构与持续冲突
写不依赖金手指同义词的具体势力、地图、资源与矛盾。
### 关键关系（可选）
只写真正长期行动的人。
### 长期故事主线
生成5—7阶段。每阶段使用：
#### 阶段N：阶段名
开局状态：
当前最值得争取的具体机会 / 目标：
主要事件与具体阻力：
主角主动行动：
核心优势怎样产生超额结果：
主角一级成长：
本阶段重要获得/占有/使用（没有则写无新增标志物）：
阶段净新增：写故事事实，不用后台术语作主要结果。
核心幻想兑现：写具体场面与结果。
主要情绪释放：
世界扩张：写新地点/阶层/存在/资源/敌人。
推向下一阶段的具体机会、欲望、竞争或压力：
自然产生的后果或余波（如果有）：

阶段之间不要按“个人概念→城市概念→世界概念→宇宙概念”升级同一哲学命题。升级优先来自更强力量、更值钱的目标、更复杂的人物和更大的具体世界。

### 早期锚点、中期里程碑与远期升格
#### 早期兑现
#### 稳定循环
#### 中期里程碑
#### 远期升格方向
全部写可拍成场面的具体事件。
### 继续探索的世界与未来场面
列最值得期待的具体场面、宝物/力量/地点/对手/关系回收。

不要输出主题宣言、哲学总结、复杂变量图或逐章计划。'''

CLEAN_COORD='''### Fixed Coordinate Reference\nsource: syntheses/reader-facing-world-coordinates-batch-d-v3\nrole: fixed reader-facing coordinate reference; does not consume creative inspiration slots\n\nGuidance: 每本 World Vision 至少建立一把读者能直接感到的主尺。只从 POWER / TECHNIQUE / THREAT / STATUS / VALUE / WORLD 中选择当前真正需要的尺度；必要时可用 GEAR/ARTIFACT。主尺必须说清主角当前能做到什么、明显更高一档能做到什么、差距会造成什么现实结果、下一档为什么值得期待。ACTION_SPACE / EXPECTATION_LADDER / IMPACT / MYSTERY_DEPTH 只属于作者后台分析，不得作为世界主尺、资源或专属概念。不要逐项填满，也不要建战力数据库。\n\n使用边界：只迁移读者坐标原则，不迁移来源作品表层设定。'''

def clean_world_bundle(g:dict)->str:
    s=g['result']
    marker='### Inspiration 1'
    rest=s[s.find(marker):] if marker in s else ''
    return CLEAN_COORD+'\n\n'+rest

def candidate1(text:str)->str:
    m=re.search(r'(?ms)^## 候选1：.*?(?=^## 候选2：|\Z)', text)
    if not m: raise RuntimeError('candidate1 not found')
    return m.group(0).strip()+'\n'

def acp_text(path:Path)->str:
    d=json.loads(path.read_text(encoding='utf-8'))
    if not d.get('ok'): raise RuntimeError(f'ACP failed: {path}: {d.get("error")}')
    text=re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*', '\n', d['text']).strip()
    return text+'\n'

def write_seed_prompts():
    for i,direction in DIRECTIONS.items():
        for arm,template in [('A',DEFAULT_PROMPT_TEMPLATES['fantasy_seed']),('B',B_SEED)]:
            p=ROOT/f'book-{i}'/arm
            p.mkdir(parents=True,exist_ok=True)
            (p/'AUTHOR_DIRECTION.md').write_text(direction+'\n',encoding='utf-8')
            prompt=generate_prompt(mode='fantasy_seed',template=template,book_content='',creative_direction=direction)
            (p/'seed_prompt.md').write_text(prompt,encoding='utf-8')

def materialize_seeds():
    for i in DIRECTIONS:
        for arm in 'AB':
            p=ROOT/f'book-{i}'/arm
            text=acp_text(p/'seed_acp.json')
            (p/'seed_response.md').write_text(text,encoding='utf-8')
            (p/'FANTASY_SEED.md').write_text(candidate1(text),encoding='utf-8')

def write_world_prompts():
    for i,direction in DIRECTIONS.items():
        for arm in 'AB':
            p=ROOT/f'book-{i}'/arm
            seed=(p/'FANTASY_SEED.md').read_text(encoding='utf-8')
            g=retrieve_gbrain(mode='world_vision',creative_direction=direction,fantasy_seed=seed)
            (p/'world_gbrain.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
            bundle=g['result'] if arm=='A' else clean_world_bundle(g)
            (p/'world_gbrain_bundle.md').write_text(bundle+'\n',encoding='utf-8')
            prompt=generate_prompt(mode='world_vision',template=(DEFAULT_PROMPT_TEMPLATES['world_vision'] if arm=='A' else B_WORLD),book_content='',creative_direction=direction,fantasy_seed=seed,creative_state={'fantasy_seed':{'status':'author_approved'}},gbrain_inspiration=bundle)
            (p/'world_prompt.md').write_text(prompt,encoding='utf-8')

def materialize_worlds():
    for i in DIRECTIONS:
        for arm in 'AB':
            p=ROOT/f'book-{i}'/arm
            (p/'WORLD_VISION.md').write_text(acp_text(p/'world_acp.json'),encoding='utf-8')

def write_program_prompts():
    for i,direction in DIRECTIONS.items():
        for arm in 'AB':
            p=ROOT/f'book-{i}'/arm
            seed=(p/'FANTASY_SEED.md').read_text(encoding='utf-8')
            world=(p/'WORLD_VISION.md').read_text(encoding='utf-8')
            g=retrieve_gbrain(mode='idea',creative_direction=direction,fantasy_seed=seed,world_vision=world)
            (p/'program_gbrain.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
            bundle=g['result']
            (p/'program_gbrain_bundle.md').write_text(bundle+'\n',encoding='utf-8')
            prompt=generate_prompt(mode='idea',template=(DEFAULT_PROMPT_TEMPLATES['idea'] if arm=='A' else B_PROGRAM),book_content='',creative_direction=direction,fantasy_seed=seed,world_vision=world,creative_state={'world_vision':{'status':'author_approved'}},gbrain_inspiration=bundle)
            (p/'program_prompt.md').write_text(prompt,encoding='utf-8')

def materialize_programs():
    for i in DIRECTIONS:
        for arm in 'AB':
            p=ROOT/f'book-{i}'/arm
            (p/'STORY_PROGRAM.md').write_text(acp_text(p/'program_acp.json'),encoding='utf-8')

def main():
    cmd=sys.argv[1]
    {'seed-prompts':write_seed_prompts,'seeds':materialize_seeds,'world-prompts':write_world_prompts,'worlds':materialize_worlds,'program-prompts':write_program_prompts,'programs':materialize_programs}[cmd]()
if __name__=='__main__': main()
