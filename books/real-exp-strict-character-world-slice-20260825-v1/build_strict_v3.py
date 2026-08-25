from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path('src').resolve()))
from story_mvp.character_context import (
    project_character_life_context,
    project_character_power_baseline,
)

ROOT = Path('books/real-exp-strict-character-world-slice-20260825-v1')

CHARACTER_PROMPT_V3 = '''你是独立上下文中的 Character / Fantasy 设计者。你会得到同一个已批准世界的两个严格接口：

1. POWER BASELINE：只负责 Core Fantasy / 特殊能力的世界参照；
2. LIFE CONTEXT：只负责人物成长背景、欲望、人格、关系的现实土壤。

两个接口都刻意不包含 named 大事件、named NPC、named 秘境、named 神兵、named 谜团或未来剧情路线。

核心原则：Character is world-conditioned, story-independent。

## 创作顺序
对每个候选，先只依据 POWER BASELINE 完成：
World Power Normal → Legal Exception → Core Fantasy → 为什么读者会馋。
之后才使用 LIFE CONTEXT 选择成长环境，并生成：
经历 → 适应 → 行为 → 私人欲望 → 关系。

成长背景可以解释这个人为什么会发现、隐藏、误用、珍惜或滥用异常，也可以让异常形成独特使用风格；但**不能因为他是矿工、匠人、账房、向导、商人等职业，就反向把异常设计成超级辨矿、维修诊断、路线优化、合同解释等职业强化。**

### Power Exception 原则
- 先说清本世界绝大多数人怎样获得、承载、使用超凡力量，以及哪些能力常见、少见、未被可靠证实。
- 再创造一个仍服从底层力量语法、但真实偏离 Normal / Rarity Distribution 的异常。
- 不要求打破世界硬规则；更好的异常常常是对“通常只能怎样”的合法偏离，而不是凭空新增万能法则。
- 异常可以来自身体、神识、术式、外物兼容、力量获得方式、承载方式、组合方式、成长方式等；也允许组合优势，而非单件外挂。
- 不要简单复用 POWER BASELINE 已列出的“少数人能力”作为金手指；应利用这些正常/稀有边界判断新的异常为什么真特殊。
- Core Fantasy 必须先回答“如果我是他，我具体能做什么”，并产生直接占有欲、力量感、身份快感、探索自由或可复述的场面期待。
- 专业技能可以与异常发生化学反应，但不能替代 Core Fantasy 本身。

### Character 原则
- 人物可来自世界任何合法社会位置：贫寒、普通、中产、富商、军户、宗门家庭、专业家庭、地方权势、既得利益或天赋优越者都可以；不默认底层受压迫者。
- 人格采用 Formative Fact → Adaptation → Observable Behavior；不要从“冷静、护短、记仇”等标签反推童年。
- 不默认主角高尚、可靠、守约、保护弱者、救家人、买房或建立公平小社会；这些只有在具体经历真的导向时才出现。
- 私人欲望可以自利、虚荣、贪婪、好胜、怕死、好奇、享乐、色欲、权欲、安稳、冒险或矛盾，也可以后来变化。
- 人物核心要可预测，具体手段可以随信息、能力边界、对手与关系而变化；不要为了不可预测随机发疯。
- 不写 Story Program，不引用接口中不存在的 named 世界机会。

严格输出 4 个候选，不评分、不排名。候选可不同，也不为了差异牺牲商业潜力；只避免近乎同一个 Power Exception / 人生运动方式换皮。

每个候选严格使用：
# CHARACTER CANDIDATE N｜名字／短标签
## World Power Normal → Exception
先写与本人物异常直接相关的世界正常值，再写他具体偏离哪一条、为何仍合法。
## Core Fantasy / 特殊际遇
先用普通话说“如果我是他，我具体能做什么”，再说明边界。
## 为什么读者会馋
写出具体想拥有、想展示、想试一次、想看别人反应的快感。
## 成长环境切片
从 LIFE CONTEXT 选择一个世界合法但非 named 剧情热点的家庭/阶层/教育环境。它可以与 Core Fantasy 产生化学反应，但不得成为异常的来源说明。
## 形成经历 → 适应 → 行为
写 2—4 条具体因果链。
## 人物钩子
前三章后，读者为什么记得住这个人，而不只是记住能力？用行为、欲望、身份矛盾或可复述印象回答。
## 当前私人欲望
此刻真正牵着他行动的东西，不总结终身主题。
## 行为签名与执念
同样诱惑、羞辱、风险、巨大利益放到别人和他面前，为什么会选得不同？
## 重要关系原点
2—4 个从成长环境自然形成的人；双方各自有欲望，不要求关系健康或长期合作。
## 为什么世界里的人会立刻察觉他特殊
谁会嫉妒、害怕、利用、追逐、崇拜、误解或轻视？为什么？
## 第一次暴露特殊性的场面
一个具体场面，同时让 World Normal、Exception 和这个人的性格被看见；避免写成技术操作说明。
## 世界不容易消化他的地方
不是主题宣言，也不是“他要改革世界”；说明这个人的存在为什么让现有习惯、关系或力量分类变得尴尬。
'''

EXCLUDED = (
    '宋照雪','魏停山','石晚舟','赫连渡','乌芙','青灯盐','白角夔',
    '悬瓮城','沉铃泽','归潮原','黑火井','白鹭天桥','无岸雾海',
    '万兽迁岭','地下驿网','当前没人能完整解释的事实',
)


def clean(path: Path) -> str:
    raw = path.read_text(encoding='utf-8')
    data = json.loads(raw)
    if not data.get('ok', True):
        raise RuntimeError(data.get('error'))
    text = data.get('text', '')
    return re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*', '\n', text).strip() + '\n'


def prepare() -> None:
    world = (ROOT / 'WORLD_VISION.md').read_text(encoding='utf-8')
    power = project_character_power_baseline(world)
    life = project_character_life_context(world)
    gbrain = (ROOT / 'CHARACTER_GBRAIN_V3.md').read_text(encoding='utf-8')
    for label, text in (('D_POWER_BASELINE.md', power), ('D_LIFE_CONTEXT.md', life)):
        (ROOT / label).write_text(text, encoding='utf-8')
        leaks = [x for x in EXCLUDED if x in text]
        if leaks:
            raise RuntimeError(f'{label} leaked named hooks: {leaks}')
    prompt = (
        CHARACTER_PROMPT_V3
        + '\n\n# POWER BASELINE｜Core Fantasy Authority\n' + power
        + '\n\n# LIFE CONTEXT｜Upbringing Authority\n' + life
        + '\n\n# Character GBrain Craft｜Abstract Only\n' + gbrain
    )
    (ROOT / 'D_POWER_FIRST_CHARACTER_PROMPT.md').write_text(prompt, encoding='utf-8')


def materialize() -> None:
    text = clean(ROOT / 'D_POWER_FIRST_CHARACTER_ACP.json')
    (ROOT / 'D_POWER_FIRST_CHARACTER_CANDIDATES.md').write_text(text, encoding='utf-8')
    leaks = [x for x in EXCLUDED if x in text]
    (ROOT / 'D_LEAK_CHECK.json').write_text(json.dumps({'named_hook_hits': leaks}, ensure_ascii=False, indent=2), encoding='utf-8')


def finalize() -> None:
    previous = (ROOT / 'ABC_FULL_ARTIFACTS.md') if (ROOT / 'ABC_FULL_ARTIFACTS.md').exists() else (ROOT / 'AB_FULL_ARTIFACTS.md')
    base = previous.read_text(encoding='utf-8')
    power = (ROOT / 'D_POWER_BASELINE.md').read_text(encoding='utf-8')
    life = (ROOT / 'D_LIFE_CONTEXT.md').read_text(encoding='utf-8')
    gbrain = (ROOT / 'CHARACTER_GBRAIN_V3.md').read_text(encoding='utf-8')
    cards = (ROOT / 'D_POWER_FIRST_CHARACTER_CANDIDATES.md').read_text(encoding='utf-8')
    extra = f'''\n\n---\n\n# D｜Strict v3：Power-System-First Character Exception\n\n> D 修正此前“职业背景→职业外挂”的过修正。Core Fantasy 只以 POWER BASELINE 为异常参照；LIFE CONTEXT 只塑造出身、欲望、性格和关系。Character 仍完全看不到 Story Opportunities。\n\n## D Power Baseline｜完整\n\n{power}\n\n## D Life Context｜完整\n\n{life}\n\n## D Character GBrain Craft｜完整\n\n{gbrain}\n\n## D Character Candidates｜完整 4 张\n\n{cards}\n'''
    (ROOT / 'ABCD_FULL_ARTIFACTS.md').write_text((base + extra).strip() + '\n', encoding='utf-8')


if __name__ == '__main__':
    {'prepare': prepare, 'materialize': materialize, 'finalize': finalize}[sys.argv[1]]()
