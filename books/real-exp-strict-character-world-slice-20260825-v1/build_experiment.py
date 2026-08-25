from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path('src').resolve()))
from story_mvp.character_context import (
    project_character_world_slice,
    project_story_opportunity_layer,
)

ROOT = Path('books/real-exp-strict-character-world-slice-20260825-v1')
SOURCE = Path('books/real-exp-independent-world-character-collision-ab-20260825-v1')

EXCLUDED_HOOK_TERMS = (
    '宋照雪', '魏停山', '石晚舟', '赫连渡', '乌芙', '青灯盐', '白角夔',
    '悬瓮城', '沉铃泽', '归潮原', '黑火井', '白鹭天桥', '无岸雾海',
    '万兽迁岭', '地下驿网', '当前没人能完整解释的事实',
)

CHARACTER_PROMPT = '''你是独立上下文中的 Character / Fantasy 设计者。你只得到一个已批准世界的 Character World Slice：它包含世界规则、正常值/稀缺度、社会文化、普通生活与知识边界，但刻意不包含 named 大事件、named NPC、named 秘境、named 神兵、named 谜团或未来剧情路线。

你的职责不是替世界已有故事机会配钥匙，而是在这个世界真实土壤里生成 4 个有商业潜力、彼此不近似的成熟中文男频主角候选。

核心原则：Character is world-conditioned, story-independent。
- 人物的出身、阶层、身体、教育、能力、欲望、偏见和恐惧必须被这个世界塑造。
- 人物不能为了某个未展示给你的剧情钩子而出生，也不要虚构一个“世界早已等着他来开启”的专属谜团。
- 性格采用 Formative Fact → Adaptation → Observable Behavior：先有世界内经历，再形成适应方式，再落到可观察选择，不从性格标签反推童年。
- 特殊性采用 World Normal → Legal Exception：先明确本世界普通人/普通修士通常怎样，再设计一个仍服从世界底层规则、但真实偏离正常分布的异常。特殊性必须是相对的；若去掉世界正常值就看不出它为什么稀有，则说明还没设计好。
- Core Fantasy/特殊际遇可以天生、获得、身份、关系、知识、经历型，也允许严格意义上没有传统外挂；但必须产生具体的男频占有欲、行动空间或场面快感。
- 不默认主角高尚、可靠、护短、守约或想建立一个更公平的小社会；人物可以自私、虚荣、好胜、怕死、贪婪、爱面子、偏执、好奇、冷漠或难相处，只要这些来自具体经历并能持续制造剧情。不要为了“不同”随机极端。
- 不写 Story Program，不引用不存在于 Slice 中的 named 世界机会。GBrain 只借鉴人物 craft，不复制来源人物。

严格输出 4 个候选，不评分、不排名。每个候选使用：
# CHARACTER CANDIDATE N｜名字／短标签
## 人物钩子
前三章后，读者最容易因什么记住他？用行为、身份、矛盾或可复述印象回答，不只写形容词。
## 普通出生切片
从 Slice 允许的普通生活环境中具体化一个出生地/家庭生态；不得把出生地设计成世界级秘境或剧情中心。
## 形成经历 → 适应 → 行为
写 2—4 条链：具体经历 → 他学会/误学会了什么 → 今天会怎样做。
## 当前私人欲望
现在真正牵着他行动的东西；可以阶段性、自利、幼稚、虚荣、矛盾，不替他总结终身主题。
## World Normal → Exception
先写一个明确世界正常值，再写这个人偏离了哪一条正常分布；说明异常为何仍符合世界底层规则。
## Core Fantasy / 特殊际遇
把异常落实成读者能代入和想拥有的具体能力、身份、身体、关系、知识或机会；说明能做什么，不能只写抽象概念。
## 为什么世界里的人会立刻察觉它特殊
谁会嫉妒、害怕、利用、嘲笑或误判？为什么？
## 行为签名与执念
同样诱惑、羞辱、风险或巨大利益放到别人和他面前，为什么会选得不同？
## 重要关系原点
2—4 个从普通成长环境自然形成的人。双方各自想要什么；不要让所有人都围着主角提供功能。
## 第一次暴露特殊性的场面
只写一个具体场面，优先展示人物性格与世界正常值被同时撞开，不写完整大纲。
## 世界不容易消化他的地方
不是主题宣言；说明现有生活习惯、关系或规则为什么无法轻易把他变成一个普通成员。
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


def prepare() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    world = (SOURCE / 'WORLD_VISION.md').read_text(encoding='utf-8')
    strict = project_character_world_slice(world)
    opportunities = project_story_opportunity_layer(world)
    (ROOT / 'WORLD_VISION.md').write_text(world, encoding='utf-8')
    (ROOT / 'CHARACTER_WORLD_SLICE.md').write_text(strict, encoding='utf-8')
    (ROOT / 'STORY_OPPORTUNITY_LAYER.md').write_text(opportunities, encoding='utf-8')
    shutil.copy2(SOURCE / 'CHARACTER_GBRAIN.md', ROOT / 'CHARACTER_GBRAIN.md')
    shutil.copy2(SOURCE / 'B' / 'CHARACTER_CANDIDATES.md', ROOT / 'A_PREVIOUS_CONTEXT_CHARACTER_CANDIDATES.md')
    shutil.copy2(SOURCE / 'WORLD_CHARACTER_CONTEXT.md', ROOT / 'A_PREVIOUS_WORLD_CHARACTER_CONTEXT.md')
    leaked = [term for term in EXCLUDED_HOOK_TERMS if term in strict]
    if leaked:
        raise RuntimeError(f'named hook leakage in strict slice: {leaked}')
    required = ('纳息者', '通脉修士', '照域修士', '宗门', '商盟', '军府', '普通人的生活与上升', '世界知识边界')
    missing = [term for term in required if term not in strict]
    if missing:
        raise RuntimeError(f'missing world reality terms: {missing}')
    prompt = CHARACTER_PROMPT + '\n\n# Character World Slice\n' + strict + '\n\n# Character GBrain Craft\n' + (ROOT / 'CHARACTER_GBRAIN.md').read_text(encoding='utf-8')
    (ROOT / 'B_STRICT_CHARACTER_PROMPT.md').write_text(prompt, encoding='utf-8')
    rules = '''# Test Rules\n\n- Purpose: test a stricter Character World Slice boundary before spending Sol.\n- Reuse the exact same protagonist-blind 澜生界 from the previous architecture experiment; no new World LLM call.\n- A baseline: reuse the previous context-isolated Character candidates whose context still leaked active events / named locations / named mysteries.\n- B strict: deterministic Character World Slice keeps laws, World Normal/Rarity, culture/social reality, generic value structures, ordinary life, and non-hook knowledge boundaries; it excludes active named events, named NPCs, named locations, named mysteries, Reader Coordinates, and future story routes.\n- A and B use the same Character GBrain craft.\n- Only B makes one new GPT-5.6 Luna high Character call. Generate 4 candidates.\n- NO Story Program, Outline, chapters, or LLM judge.\n- Audit questions: relative specialness, formative causality, hook leakage, character diversity, commercial fantasy appetite, and engineering/social-hero collapse.\n'''
    (ROOT / 'TEST_RULES.md').write_text(rules, encoding='utf-8')


def materialize() -> None:
    text = clean_acp(ROOT / 'B_STRICT_CHARACTER_ACP.json')
    (ROOT / 'B_STRICT_CHARACTER_CANDIDATES.md').write_text(text, encoding='utf-8')
    leaks = [term for term in EXCLUDED_HOOK_TERMS if term in text]
    (ROOT / 'LEAK_CHECK.json').write_text(json.dumps({'named_hook_hits': leaks}, ensure_ascii=False, indent=2), encoding='utf-8')


def finalize() -> None:
    world = (ROOT / 'WORLD_VISION.md').read_text(encoding='utf-8')
    old_context = (ROOT / 'A_PREVIOUS_WORLD_CHARACTER_CONTEXT.md').read_text(encoding='utf-8')
    strict = (ROOT / 'CHARACTER_WORLD_SLICE.md').read_text(encoding='utf-8')
    opportunities = (ROOT / 'STORY_OPPORTUNITY_LAYER.md').read_text(encoding='utf-8')
    gbrain = (ROOT / 'CHARACTER_GBRAIN.md').read_text(encoding='utf-8')
    a = (ROOT / 'A_PREVIOUS_CONTEXT_CHARACTER_CANDIDATES.md').read_text(encoding='utf-8')
    b = (ROOT / 'B_STRICT_CHARACTER_CANDIDATES.md').read_text(encoding='utf-8')
    rules = (ROOT / 'TEST_RULES.md').read_text(encoding='utf-8')
    combined = f'''# Strict Character World Slice A/B｜完整审计合集\n\n{rules}\n\n---\n\n# Shared Protagonist-Blind World\n\n{world}\n\n---\n\n# Hidden Story Opportunity Layer（Character 不可见）\n\n{opportunities}\n\n---\n\n# Character GBrain Craft（A/B 同一份）\n\n{gbrain}\n\n---\n\n# A｜上一轮 Context-Isolated，但仍泄漏 Story Opportunities\n\n## A Character Context｜完整\n\n{old_context}\n\n## A Character Candidates｜完整 3 张\n\n{a}\n\n---\n\n# B｜Strict Character World Slice\n\n## B Character World Slice｜完整\n\n{strict}\n\n## B Character Candidates｜完整 4 张\n\n{b}\n'''
    combined = re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*', '\n', combined)
    (ROOT / 'AB_FULL_ARTIFACTS.md').write_text(combined.strip() + '\n', encoding='utf-8')


if __name__ == '__main__':
    cmd = sys.argv[1]
    {'prepare': prepare, 'materialize': materialize, 'finalize': finalize}[cmd]()
