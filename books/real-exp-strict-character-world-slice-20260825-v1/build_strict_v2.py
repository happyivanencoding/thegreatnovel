from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path('src').resolve()))
from story_mvp.character_context import project_character_world_slice

ROOT = Path('books/real-exp-strict-character-world-slice-20260825-v1')

CHARACTER_PROMPT_V2 = '''你是独立上下文中的 Character / Fantasy 设计者。你只得到一个已批准世界的 Character World Slice：它包含世界规则、正常值/稀缺度、社会文化、普通生活与知识边界，但刻意不包含 named 大事件、named NPC、named 秘境、named 神兵、named 谜团或未来剧情路线。

你的职责不是替世界已有故事机会配钥匙，而是在这个世界真实土壤里生成 4 个有商业潜力的成熟中文男频主角候选。

核心原则：Character is world-conditioned, story-independent。
- 人物的出身、阶层、身体、教育、能力、欲望、偏见和恐惧必须被这个世界塑造。
- 成长切片可以处于这个世界任何合法社会位置，不默认从底层、被压迫者、无籍者或手艺人开始。切片只需要不是 named 剧情热点，也不能藏一个专门等主角开启的世界级秘密。
- 人格采用 Formative Fact → Adaptation → Observable Behavior：先有世界内经历，再形成适应方式，再落到可观察选择，不从性格标签反推童年。
- 特殊性采用 World Normal → Legal Exception：先明确本世界普通人/普通修士/某类身份通常怎样，再创造一个仍服从世界底层规则、但真实偏离正常分布的异常。
- 异常不能只是一项更高效的职业技能、诊断流程、维护技巧、路线优化或行政缝隙。若人物拥有专业能力，它只能是人物生活的一部分；Core Fantasy 仍应形成一个读者可以直接理解、想拥有、想看它在场面中兑现的个人优势、身份、关系、身体状态或行动自由。
- 不默认主角高尚、可靠、护短、守约、想保护弱者或建立公平小社会；也不把“买房/救家人/摆脱控制”自动视为更成熟的人生欲望。让私人欲望来自这个具体人的经历和偏爱。
- 不要求四个候选为了多样性刻意反套路，但避免近乎同一社会位置、同一人生运动方式和同一异常家族换皮。
- 不写 Story Program，不引用 Slice 中不存在的 named 世界机会。GBrain 只借鉴人物 craft，不复制来源人物。

严格输出 4 个候选，不评分、不排名。每个候选使用：
# CHARACTER CANDIDATE N｜名字／短标签
## 人物钩子
前三章后，读者最容易因什么记住他？优先写一个可以复述的行为、身份矛盾、欲望或形象。
## 成长环境切片
写这个世界里真实存在的一种家庭/阶层/教育/职业环境；可以贫穷，也可以富裕、受保护、既得利益或天赋优越，但不能是未提供的 named 剧情热点。
## 形成经历 → 适应 → 行为
写 2—4 条因果链，每条必须从具体经历走到今天的可观察行为。
## 当前私人欲望
现在真正牵着他行动的东西；可以自利、幼稚、虚荣、贪婪、好胜、怕死、好奇、享乐、矛盾或后来变化，不替他总结终身主题。
## World Normal → Exception
明确写：世界正常值是什么；他偏离哪一条；为什么这种偏离仍符合底层规则，而不是凭空追加世界法则。
## Core Fantasy / 特殊际遇
把异常落实成具体能力、身份、身体、关系、知识或机会。先回答“如果我是他，我具体能做什么”，再写边界。
## 为什么读者会馋
不要只说有趣/聪明；写出读者会想亲自拥有、展示、冒险、占有、赢或进入的具体快感。
## 为什么世界里的人会立刻察觉它特殊
谁会嫉妒、害怕、利用、追逐、崇拜、误解或轻视？为什么？
## 行为签名与执念
同样的诱惑、羞辱、风险或巨大利益放到别人和他面前，为什么会选得不同？
## 重要关系原点
2—4 个从成长环境自然形成的人；双方各自有欲望，不要求关系健康、平等或长期合作。
## 第一次暴露特殊性的场面
一个具体场面，同时证明人物性格、World Normal 与 Exception；避免写成操作说明。
## 世界不容易消化他的地方
不是主题宣言，也不是“他会改革世界”；说明这个人的存在为什么让现有习惯、关系或分类变得尴尬。
'''


def clean(path: Path) -> str:
    data = json.loads(path.read_text(encoding='utf-8'))
    if not data.get('ok', True):
        raise RuntimeError(data.get('error'))
    text = data.get('text', '')
    text = re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*', '\n', text)
    return text.strip() + '\n'


def prepare() -> None:
    world = (ROOT / 'WORLD_VISION.md').read_text(encoding='utf-8')
    strict_v2 = project_character_world_slice(world)
    (ROOT / 'C_STRICT_V2_CHARACTER_WORLD_SLICE.md').write_text(strict_v2, encoding='utf-8')
    gbrain = (ROOT / 'CHARACTER_GBRAIN.md').read_text(encoding='utf-8')
    prompt = CHARACTER_PROMPT_V2 + '\n\n# Character World Slice\n' + strict_v2 + '\n\n# Character GBrain Craft\n' + gbrain
    (ROOT / 'C_STRICT_V2_CHARACTER_PROMPT.md').write_text(prompt, encoding='utf-8')


def materialize() -> None:
    text = clean(ROOT / 'C_STRICT_V2_CHARACTER_ACP.json')
    (ROOT / 'C_STRICT_V2_CHARACTER_CANDIDATES.md').write_text(text, encoding='utf-8')
    excluded = ('宋照雪','魏停山','石晚舟','赫连渡','乌芙','青灯盐','白角夔','悬瓮城','沉铃泽','归潮原','黑火井','白鹭天桥','无岸雾海','万兽迁岭','地下驿网','当前没人能完整解释的事实')
    leaks = [x for x in excluded if x in text]
    (ROOT / 'C_LEAK_CHECK.json').write_text(json.dumps({'named_hook_hits': leaks}, ensure_ascii=False, indent=2), encoding='utf-8')


def finalize() -> None:
    base = (ROOT / 'AB_FULL_ARTIFACTS.md').read_text(encoding='utf-8')
    slice_v2 = (ROOT / 'C_STRICT_V2_CHARACTER_WORLD_SLICE.md').read_text(encoding='utf-8')
    cards_v2 = (ROOT / 'C_STRICT_V2_CHARACTER_CANDIDATES.md').read_text(encoding='utf-8')
    extra = f'''\n\n---\n\n# C｜Strict v2：Non-Hook Upbringing + World Normal Exception\n\n> C 修正 B 的过修正：仍然完全看不到 Story Opportunities，但不再要求普通底层出生；允许世界合法的任何社会位置。特殊性也不能只停在高效职业技能/诊断/行政缝隙。\n\n## C Character World Slice｜完整\n\n{slice_v2}\n\n## C Character Candidates｜完整 4 张\n\n{cards_v2}\n'''
    (ROOT / 'ABC_FULL_ARTIFACTS.md').write_text((base + extra).strip() + '\n', encoding='utf-8')


if __name__ == '__main__':
    {'prepare': prepare, 'materialize': materialize, 'finalize': finalize}[sys.argv[1]]()
