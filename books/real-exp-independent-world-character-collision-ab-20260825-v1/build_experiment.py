from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path('src').resolve()))
from story_mvp.gbrain_retrieval import retrieve_gbrain

ROOT = Path('books/real-exp-independent-world-character-collision-ab-20260825-v1')
DIRECTION = ('成熟中文男频玄幻/修仙成长长篇。除此之外，不指定核心能力、主角性格、世界结构、资源类型、'
             '势力结构、冲突类型、题材子类型或长期主题，由当前实验架构自主生成。')

WORLD_TEMPLATE = '''你是独立世界设计者。根据作者粗方向，先创造一个**没有主角、没有金手指、没有预设主题使命**也值得写很多故事的成熟中文男频玄幻/修仙世界。

这是 Protagonist-blind World：你不知道未来主角是谁，也不知道他会拥有什么特殊能力。不要替未来主角预留专属敌人、专属资源、专属社会问题或主题回声；不要猜“这本书最后应该讲什么”。

世界首先要像一个已经存在很久的地方：不同的人追不同东西，有些欲望彼此无关；有强者、普通人、野心家、怪人、家族、宗门、商人、战争、奇观、职业、资源、爱情、仇恨、发财梦、长生欲、地位竞争或其它真实生活。不是每件事都要围绕同一个中心命题。

优先具体、可感、让人想进入；Supporting reality 只写到足够可信，不要把世界写成治理/工程模拟器。GBrain 只借抽象 craft，不复制来源作品表层设定。

严格按以下结构输出：
# PROTAGONIST-BLIND WORLD VISION
## 普通人的生活与上升
## 力量体系与正常值
说明普通、优秀、罕见分别大约是什么；什么能力在世界中本来就常见/罕见/不存在。
## 社会现实与身份
只写会真实塑造人生选择的事实，不做价值判断。
## 世界里真正值钱、值得想要的东西
## 世界正在发生的大事
至少写 6 条彼此不需要共享主题的具体人物/势力欲望与事件，其中至少一半以具体人物为中心，而不是组织名词。
## 值得进入的地点、奇观与未知
## 世界知识边界
普通人、专业人士、顶层势力分别大概知道什么；列出 3—5 个当前没人能完整解释的事实。
## 读者可用的世界坐标
用世界内事实说明力量、威胁、地位、价值、世界尺度、可见的下一层期待；不要出现后台术语。
'''

CHARACTER_SCHEMA = '''严格输出 3 个候选，不评分、不排名。每个候选使用：
# CHARACTER CANDIDATE N｜名字/短标签
## 人物钩子
前三章后，读者最容易因什么记住他？不要只写性格形容词。
## 世界相对位置
按世界正常值，他现在究竟普通、优秀、边缘、特权还是异常在哪里？
## 成长背景
只写 2—4 个真正塑造他的具体经历；人格必须能看见这些经历留下的痕迹。
## 当前私人欲望
现在真正牵着他行动的东西；可以自私、幼稚、虚荣、矛盾、阶段性，不替他总结终身主题。
## 行为签名与执念
同样的诱惑、羞辱、风险或巨大利益摆在别人面前与摆在他面前，为什么会出现不同选择？
## 重要关系原点
2—4 个具体人。写双方各自要什么、为什么即使没有金手指也仍有未完成故事。
## Core Fantasy / 特殊际遇
可以天生、获得、关系、身份、知识、经历型，也允许严格意义上没有外挂；必须能在本世界规则下成立。
## 为什么在这个世界里特殊
明确对比世界正常值，说明别人为什么会嫉妒、害怕、想利用或根本理解不了。
## 为什么读者会想要/想看
用具体占有欲、场面或身份快感回答，不用抽象价值词。
## 第一次暴露特殊性的场面
只写一个具体场面，不写完整大纲。
## 世界不容易消化他的地方
不是“他代表什么主题”，而是世界现有的人、规则或习惯为什么很难把这个人收编成正常成员。
'''

CHARACTER_A_TEMPLATE = '''你是 Character / Fantasy 设计者。这里有一个已经独立生成并批准的完整世界。基于这个世界，生成最有商业潜力的成熟中文男频主角候选与 Core Fantasy/特殊际遇。人物必须遵守世界事实，特殊性要相对于世界正常值真实可见。

不要修改世界事实。不要写 Story Program。GBrain 只借鉴人物塑造 craft，不复制来源人物。

{schema}
'''

CHARACTER_B_TEMPLATE = '''你是独立上下文中的 Character / Fantasy 设计者。你只得到从一个已批准世界**确定性投影出的事实接口**，没有看到世界设计者对故事焦点的完整组织方式。

基于这些事实生成最有商业潜力的成熟中文男频主角候选与 Core Fantasy/特殊际遇。人物必须是 World-conditioned：能力、际遇、成长背景和性格都要相对于这个世界的正常值成立；但不要把人物设计成“这个世界问题的答案”，不要从世界的社会矛盾提纯公共使命，也不要为了匹配世界已有事件而制造专属救世主。

优先寻找一个**世界无法轻易消化的具体人**：他可能在乎世界多数人不在乎的东西，也可能以异常强度追逐一个普通欲望，或拥有让现有关系/规则尴尬的特殊位置。Mismatch 必须来自人物与世界事实的真实摩擦，不是为了反套路而随机怪异。

不要修改世界事实。不要写 Story Program。GBrain 只借鉴人物塑造 craft，不复制来源人物。

{schema}
'''

COLLISION_TEMPLATE = '''你是长期 Story Program / Collision Designer。你收到两个已经独立批准的创意权威：
1. 一个在主角出现前就成立的完整 World Vision；
2. 一个在独立上下文里形成的 Character / Fantasy Card。

你的职责不是让二者“更一致”，而是设计**为什么偏偏这个人进入这个世界后特别好看**。Do Not Reconcile Away the Collision：不得修改 World 去暗示它早就在等待主角；不得把 Character 校正成更成熟、更合理、更符合世界主题的人。

世界中已有的人继续追自己的欲望；他们首先是人，不是能力 Counter。Counterplay 只能在真实碰撞和学习以后自然长出。Core Fantasy 是长期 Reader Promise，但不要让世界后续全部变成它的语义同义词。

重点制造：具体欲望、具体人、不可替代关系、令人眼馋的获得、世界本来就在运动的大事、主角自己的异常选择，以及两条原本独立的线突然相撞。允许某些好玩的角色/奇观/关系不立即转成成长收益；重要长期投资需要复利，但不是每个 memorable object 都必须证明“有用”。

生成 5—7 个自然大型阶段，不绑定固定章数。每个阶段写：
### 阶段N｜名称
- 阶段为什么现在发生
- 主角此时真正想要什么
- 世界里谁/什么本来就在行动
- 两者怎样撞上
- 关键人物与关系变化
- Core Fantasy 在这里怎样参与（可以不是主发动机）
- 关键获得/失去/占有/首次使用
- 本阶段最让读者上头的具体场面或期待
- 故事局面怎样不可逆地改变
- 下一段故事从哪里撞进来（可以是后果，也可以是世界另一条早就在运动的线）

在阶段前先写：
# COLLISION STORY PROGRAM
## 为什么偏偏是这个人与这个世界
## 三个最值得长期惦记的人/关系
## 三个当前已经可见但尚未得到/进入/知道的对象

不要写主题总结，不要替世界给出正确答案，不要写 Outline 或正文。
'''


def clean_acp(path: Path) -> str:
    raw = path.read_text(encoding='utf-8')
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = None
    if isinstance(data, dict):
        if not data.get('ok', True):
            raise RuntimeError(data.get('error'))
        text = data.get('text', '')
    else:
        text = raw
    text = re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*', '\n', text)
    return text.strip() + '\n'


def section(text: str, heading: str) -> str:
    m = re.search(rf'(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)', text)
    return m.group(1).strip() if m else ''


def candidate(text: str, n: int) -> str:
    m = re.search(rf'(?s)# CHARACTER CANDIDATE {n}.*?(?=# CHARACTER CANDIDATE {n+1}|\Z)', text)
    if not m:
        raise RuntimeError(f'character candidate {n} missing')
    return m.group(0).strip() + '\n'


def write_world_prompt() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT/'AUTHOR_DIRECTION.md').write_text(DIRECTION+'\n', encoding='utf-8')
    g = retrieve_gbrain(mode='world_vision', creative_direction=DIRECTION)
    (ROOT/'world_gbrain.json').write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding='utf-8')
    prompt = WORLD_TEMPLATE + '\n\n# 作者粗方向\n' + DIRECTION + '\n\n# GBrain World Craft（可选）\n' + g['result']
    (ROOT/'world_prompt.md').write_text(prompt, encoding='utf-8')
    print('world coordinate', g.get('coordinate_reference_count'), 'creative', g.get('accepted_count'), [x.get('slug') for x in g.get('accepted',[])])


def materialize_world() -> None:
    world = clean_acp(ROOT/'world_acp.json')
    (ROOT/'WORLD_VISION.md').write_text(world, encoding='utf-8')
    headings = ['普通人的生活与上升','力量体系与正常值','社会现实与身份','世界里真正值钱、值得想要的东西','世界正在发生的大事','值得进入的地点、奇观与未知','世界知识边界']
    blocks = [f'## {h}\n{section(world,h)}' for h in headings if section(world,h)]
    ctx = '# WORLD CHARACTER CONTEXT｜Facts Only\n\n' + '\n\n'.join(blocks) + '\n'
    (ROOT/'WORLD_CHARACTER_CONTEXT.md').write_text(ctx, encoding='utf-8')


def character_gbrain() -> str:
    ctx = (ROOT/'WORLD_CHARACTER_CONTEXT.md').read_text(encoding='utf-8')
    q = '"character autonomy" OR "character hook" OR "protagonist behavior" OR "protagonist identity" OR "relationship chemistry"'
    g = retrieve_gbrain(mode='idea', creative_direction=DIRECTION, world_vision=ctx, query_override=q)
    (ROOT/'character_gbrain.json').write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding='utf-8')
    (ROOT/'CHARACTER_GBRAIN.md').write_text(g['result']+'\n', encoding='utf-8')
    print('character gbrain', g.get('accepted_count'), [x.get('slug') for x in g.get('accepted',[])])
    return g['result']


def write_character_prompts() -> None:
    world = (ROOT/'WORLD_VISION.md').read_text(encoding='utf-8')
    ctx = (ROOT/'WORLD_CHARACTER_CONTEXT.md').read_text(encoding='utf-8')
    gb = character_gbrain()
    for side, source, template in [('A',world,CHARACTER_A_TEMPLATE),('B',ctx,CHARACTER_B_TEMPLATE)]:
        p = ROOT/side
        p.mkdir(exist_ok=True)
        prompt = template.format(schema=CHARACTER_SCHEMA) + '\n\n# World Input\n' + source + '\n\n# Character GBrain Craft（同一份，可选）\n' + gb
        (p/'character_prompt.md').write_text(prompt, encoding='utf-8')


def materialize_characters() -> None:
    for side in ('A','B'):
        p=ROOT/side
        text=clean_acp(p/'character_acp.json')
        (p/'CHARACTER_CANDIDATES.md').write_text(text,encoding='utf-8')
        (p/'CHARACTER_SELECTED.md').write_text(candidate(text,1),encoding='utf-8')


def write_program_prompts() -> None:
    world=(ROOT/'WORLD_VISION.md').read_text(encoding='utf-8')
    g=retrieve_gbrain(mode='idea',creative_direction=DIRECTION,world_vision=world)
    (ROOT/'program_gbrain.json').write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'PROGRAM_GBRAIN.md').write_text(g['result']+'\n',encoding='utf-8')
    for side in ('A','B'):
        p=ROOT/side
        char=(p/'CHARACTER_SELECTED.md').read_text(encoding='utf-8')
        prompt=COLLISION_TEMPLATE+'\n\n# Approved World Vision\n'+world+'\n\n# Approved Character / Fantasy Card\n'+char+'\n\n# Shared Story GBrain Craft（可选）\n'+g['result']
        (p/'program_prompt.md').write_text(prompt,encoding='utf-8')
    print('program gbrain',g.get('accepted_count'),[x.get('slug') for x in g.get('accepted',[])])


def materialize_programs() -> None:
    for side in ('A','B'):
        p=ROOT/side
        (p/'STORY_PROGRAM.md').write_text(clean_acp(p/'program_acp.json'),encoding='utf-8')


def hshift(text: str, d: int=2) -> str:
    out=[]
    for line in text.splitlines():
        m=re.match(r'^(#{1,6})(\s+.*)$',line)
        if m: line='#'*min(6,len(m.group(1))+d)+m.group(2)
        out.append(line)
    return '\n'.join(out).strip()+'\n'


def finalize() -> None:
    rules='''# Test Rules\n\n- Shared protagonist-blind World Vision for A/B.\n- World: GPT-5.6 Luna high, GBrain World ON.\n- A Character: GPT-5.6 Luna high in a fresh ACP session, sees FULL World Vision + shared Character GBrain.\n- B Character: GPT-5.6 Luna high in a separate fresh ACP session, sees only deterministic WORLD_CHARACTER_CONTEXT + the SAME Character GBrain; explicit preserve-mismatch contract.\n- A/B each produce 3 Character/Fantasy candidates; candidate 1 is frozen before Story Program, no cherry-picking.\n- A/B Story Program: GPT-5.6 Sol high, same Collision prompt, same full World, same Story GBrain; only selected Character differs.\n- Stop at Story Program. No Outline / chapters / LLM judge.\n'''
    (ROOT/'TEST_RULES.md').write_text(rules,encoding='utf-8')
    world=(ROOT/'WORLD_VISION.md').read_text(encoding='utf-8')
    ctx=(ROOT/'WORLD_CHARACTER_CONTEXT.md').read_text(encoding='utf-8')
    parts=['# Independent World × Character Context Isolation A/B｜全部产物','',rules.strip(),'','# Author Direction','',DIRECTION,'','# Shared Protagonist-Blind World Vision','',hshift(world,1),'# Deterministic World Character Context','',hshift(ctx,1)]
    meta={'direction':DIRECTION,'sides':{}}
    for side,label in [('A','A｜Full-World Coupled Character'),('B','B｜Context-Isolated Character')]:
        p=ROOT/side
        chars=(p/'CHARACTER_CANDIDATES.md').read_text(encoding='utf-8')
        selected=(p/'CHARACTER_SELECTED.md').read_text(encoding='utf-8')
        prog=(p/'STORY_PROGRAM.md').read_text(encoding='utf-8')
        parts += ['---','',f'# {label}','','## Complete Character/Fantasy Candidates','',hshift(chars,1),'## Frozen Candidate 1','',hshift(selected,1),'## Collision Story Program','',hshift(prog,1)]
        title=re.search(r'^# CHARACTER CANDIDATE 1｜(.+)$',selected,re.M)
        meta['sides'][side]={'selected':title.group(1).strip() if title else 'candidate1','stages':len(re.findall(r'(?m)^### 阶段\d+',prog))}
    merged='\n'.join(parts).strip()+'\n'
    merged=re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*','\n',merged)
    (ROOT/'AB_FULL_ARTIFACTS.md').write_text(merged,encoding='utf-8')
    (ROOT/'RUN_METADATA.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(meta,ensure_ascii=False,indent=2))


if __name__=='__main__':
    cmd=sys.argv[1]
    {'world-prompt':write_world_prompt,'world':materialize_world,'character-prompts':write_character_prompts,'characters':materialize_characters,'program-prompts':write_program_prompts,'programs':materialize_programs,'finalize':finalize}[cmd]()
