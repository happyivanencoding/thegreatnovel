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

PROMPT = '''你是独立上下文中的 Character / Fantasy 设计者。你会得到同一个已批准世界的两个严格接口：

1. POWER BASELINE：只负责 Core Fantasy / 特殊能力及其成长的世界参照；
2. LIFE CONTEXT：只负责人物成长背景、欲望、人格、关系的现实土壤。

两个接口都刻意不包含 named 大事件、named NPC、named 秘境、named 神兵、named 谜团或未来剧情路线。

这是成熟中文男频**成长**长篇。主角可以经历短暂低谷、失败和限制，但长期必须通过正常修炼 + 自身异常的深入掌握真正越来越强，最终能进入这个世界更高层力量竞争。Core Fantasy 不能只是一次性解题技巧、职业技能、身份缝隙或永远停留在低阶的聪明玩法。

核心原则：Character is world-conditioned, story-independent。

## 严格创作顺序
对每个候选，先只依据 POWER BASELINE 完成：
1. World Power Normal
2. Legal Exception
3. Core Fantasy
4. Growth Compatibility
5. 为什么读者会馋

之后才使用 LIFE CONTEXT 选择成长环境，并生成：
经历 → 适应 → 行为 → 私人欲望 → 关系。

成长背景可以解释人物为什么发现、隐藏、误用、珍惜、炫耀或滥用异常，也可以形成独特使用风格；但不能因为他是矿工、匠人、账房、向导、商人等职业，就反向把异常设计成超级辨矿、维修诊断、路线优化、合同解释等职业强化。

### Power Exception
- 先明确本世界绝大多数人怎样获得、承载、使用超凡力量，以及哪些能力常见、少见、未被可靠证实。
- 再创造一个仍服从底层力量语法、但真实偏离 Normal / Rarity Distribution 的异常。
- 异常可以来自身体、神识、术式、外物兼容、力量获得方式、承载方式、组合方式、成长方式等，也允许组合优势。
- 不简单复用 POWER BASELINE 已列出的“少数人能力”作为金手指。
- Core Fantasy 必须先回答“如果我是他，我具体能做什么”，并产生直接占有欲、力量感、身份快感、探索自由或可复述的场面期待。

### Growth Compatibility
必须同时说明三条：
- **正常修炼轴**：从纳息、通脉、立相、照域等正常成长中，身体/神识/灵力/术式如何真实变强；不能让外挂替代修炼。
- **异常掌握轴**：随着人物成长，Exception 的容量、精度、组合、适用对象、持续时间、可承担层级或行动自由具体怎样扩张；不是只把同一技巧数字放大。
- **永久边界**：至少一条即使高阶也不能自动消失的限制，让世界规则始终大于外挂。

不要在 Character Card 里写六卷大纲，也不要指定未来 Boss、秘境和 named 奖励。这里只证明：这个人和这个异常有成为长期强者的成长空间。

### Character
- 人物可来自世界任何合法社会位置，不默认底层受压迫者。
- 人格采用 Formative Fact → Adaptation → Observable Behavior；不从标签反推童年。
- 不默认主角高尚、可靠、守约、保护弱者、救家人、买房或建立公平小社会。
- 私人欲望可以自利、虚荣、贪婪、好胜、怕死、好奇、享乐、色欲、权欲、安稳、冒险或矛盾，也可以后来变化。
- 人物核心可预测，具体手段随信息、能力边界、对手与关系变化。
- 不写 Story Program，不引用接口中不存在的 named 世界机会。

严格输出 4 个候选，不评分、不排名。每个候选严格使用：
# CHARACTER CANDIDATE N｜名字／短标签
## World Power Normal → Exception
## Core Fantasy / 特殊际遇
先用普通话说“如果我是他，我具体能做什么”，再说明边界。
## Growth Compatibility｜怎样真正越来越强
分别写：正常修炼轴 / 异常掌握轴 / 永久边界。只写成长语法，不写未来剧情阶段。
## 为什么读者会馋
## 成长环境切片
## 形成经历 → 适应 → 行为
## 人物钩子
## 当前私人欲望
## 行为签名与执念
## 重要关系原点
## 为什么世界里的人会立刻察觉他特殊
## 第一次暴露特殊性的场面
## 世界不容易消化他的地方
'''

EXCLUDED = (
    '宋照雪','魏停山','石晚舟','赫连渡','乌芙','青灯盐','白角夔',
    '悬瓮城','沉铃泽','归潮原','黑火井','白鹭天桥','无岸雾海',
    '万兽迁岭','地下驿网','当前没人能完整解释的事实',
)


def clean(path: Path) -> str:
    data = json.loads(path.read_text(encoding='utf-8'))
    if not data.get('ok', True):
        raise RuntimeError(data.get('error'))
    return re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*', '\n', data.get('text', '')).strip() + '\n'


def prepare() -> None:
    world = (ROOT / 'WORLD_VISION.md').read_text(encoding='utf-8')
    power = project_character_power_baseline(world)
    life = project_character_life_context(world)
    gbrain = (ROOT / 'CHARACTER_GBRAIN_V3.md').read_text(encoding='utf-8')
    (ROOT / 'E_POWER_BASELINE.md').write_text(power, encoding='utf-8')
    (ROOT / 'E_LIFE_CONTEXT.md').write_text(life, encoding='utf-8')
    for label, text in (('power', power), ('life', life)):
        leaks = [x for x in EXCLUDED if x in text]
        if leaks:
            raise RuntimeError(f'{label} leaked named hooks: {leaks}')
    full = PROMPT + '\n\n# POWER BASELINE\n' + power + '\n\n# LIFE CONTEXT\n' + life + '\n\n# CHARACTER GBRAIN CRAFT\n' + gbrain
    (ROOT / 'E_GROWTH_COMPAT_CHARACTER_PROMPT.md').write_text(full, encoding='utf-8')


def materialize() -> None:
    text = clean(ROOT / 'E_GROWTH_COMPAT_CHARACTER_ACP.json')
    (ROOT / 'E_GROWTH_COMPAT_CHARACTER_CANDIDATES.md').write_text(text, encoding='utf-8')
    leaks = [x for x in EXCLUDED if x in text]
    (ROOT / 'E_LEAK_CHECK.json').write_text(json.dumps({'named_hook_hits': leaks}, ensure_ascii=False, indent=2), encoding='utf-8')


def finalize() -> None:
    base_file = ROOT / 'ABCD_FULL_ARTIFACTS.md'
    if not base_file.exists():
        base_file = ROOT / 'AB_FULL_ARTIFACTS.md'
    base = base_file.read_text(encoding='utf-8')
    power = (ROOT / 'E_POWER_BASELINE.md').read_text(encoding='utf-8')
    life = (ROOT / 'E_LIFE_CONTEXT.md').read_text(encoding='utf-8')
    cards = (ROOT / 'E_GROWTH_COMPAT_CHARACTER_CANDIDATES.md').read_text(encoding='utf-8')
    extra = f'''\n\n---\n\n# E｜Strict v4：Power-System-First + Male Progression Growth Compatibility\n\n> E 在 D 的基础上补回男频成长硬前提：主角可以短暂低谷，但长期必须通过正常修炼与 Exception 掌握真正越来越强。Character Card 只定义成长语法，不提前写 Story Program。\n\n## E Power Baseline｜完整\n\n{power}\n\n## E Life Context｜完整\n\n{life}\n\n## E Character Candidates｜完整 4 张\n\n{cards}\n'''
    (ROOT / 'FINAL_CHARACTER_ARCHITECTURE_ARTIFACTS.md').write_text((base + extra).strip() + '\n', encoding='utf-8')


if __name__ == '__main__':
    {'prepare': prepare, 'materialize': materialize, 'finalize': finalize}[sys.argv[1]]()
