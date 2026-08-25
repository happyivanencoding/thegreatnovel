from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path('src').resolve()))
from story_mvp.character_seeds import compose_character_card, extract_frozen_power_seed, split_character_candidates

ROOT = Path('books/real-exp-split-power-human-seed-20260825-v1')
SOURCE = Path('books/real-exp-strict-character-world-slice-20260825-v1')

HUMAN_PROMPT = '''你是成熟中文男频成长长篇的 Human Seed 设计者。你只负责创造“这个人原本是谁”。

你会看到同一个已批准世界的 LIFE CONTEXT：普通生活、社会现实、阶层、身份、价值结构和普通知识边界。你**完全不知道**这个人未来会有什么 Core Fantasy、金手指、特殊体质、特殊身份或力量异常；也看不到世界的 named 大事件、named NPC、named 秘境、named 神兵、named 谜团和未来剧情路线。

这是刻意的 authority 隔离。不要猜未来 Power，不要写“也许他以后会获得某种能力”，不要为了一个不存在于输入里的外挂预留主题化童年。

目标：生成 4 个彼此都具有商业男频人物潜力的 Human Seeds。先保证每个人独立值得看，再检查候选集是否出现明显心理运动坍缩；如果四个人虽然阶层/职业不同，却都在说“不要控制我 / 不被定义 / 想有自己的空间 / 摆脱体系”，请重新拉开人物欲望与生命运动，但**不要**用预设人格菜单机械分配类型。

核心原则：
- 人物必须 world-conditioned：出身、教育、阶层、欲望、偏见、恐惧和关系应来自 LIFE CONTEXT 的真实社会土壤。
- 人物必须 power-blind：Human Seed 不知道任何未来能力，所以 Biography 不得解释能力，也不得围绕能力隐喻组织。
- 人格采用 Formative Fact → Adaptation → Observable Behavior。经历先发生；他学会或误学会某个生存经验；今天因此会做出可观察的选择。
- 当前私人欲望可以很具体、很俗、很自利，也可以高远；不自动提纯成公共改革或制度理想。
- Core Obsession 不是三百万字使命，而是一种不会因单次任务完成就消失、反而可能随着见识与行动空间扩大而继续膨胀的私人追逐。
- Excess 问“哪里过量”：普通人觉得够了，他为什么仍不肯停？不要用贪、好胜、好奇等标签菜单直接作答，而要写具体行为证据。
- Behavior Signature 固定人物核心，不固定解决手段。读者应逐渐知道他不愿接受什么、会为什么承担代价，却不能因此按模板猜中每一步。
- 关系必须在没有任何特殊能力的前提下仍值得继续看。双方都有自己的欲望，允许不健康、不平等、崇拜、嫉妒、竞争、依赖、疏远或分离，只要来自具体人物。
- 不默认主角善良、可靠、护短、守约、反权威、反控制、保护弱者、救家人、买房、建家、建立公平小社会。
- 这是男频成长小说的人物，但此阶段只定义“人会怎样追逐人生”；修为成长与金手指成长由独立 Power Seed 负责，不要代替它。

严格生成 4 个候选，不评分、不排名，不引用其它候选作为对照。每个候选严格使用：

# HUMAN SEED CANDIDATE N｜姓名／短标签
## 世界中的初始位置与成长环境
世界里的具体家庭/阶层/教育/生活位置。可以贫寒、普通、富裕、既得利益、受保护、有前途或边缘；不默认底层。

## Formative Facts → Adaptation → Observable Behavior
写 2—4 条“具体经历 → 他学会/误学会什么 → 今天怎样做”的链。不要写任何未来特殊能力。

## 当前私人欲望
他现在真正想得到、成为、体验、保住、赢过、追上、摆脱或完成什么？要能用人物自己的日常语言说出来。

## Core Obsession
什么追逐不会因当前问题解决就自动结束，反而可能随着见识、地位和行动空间扩大而越来越强？不要写公共使命。

## Excess｜哪里过量
用一个具体选择或习惯证明：普通人觉得已经够了，他还会继续到什么程度？不要用性格标签替代。

## Behavior Signature
面对高价值机会、羞辱、恐惧、关系压力和重大损失时，哪些选择倾向能让读者认出“这就是他”？具体手段仍可变化。

## 重要关系原点
2—4 个具体人。写双方各自在追什么，为什么即使这个人永远没有任何金手指，两个人之间仍然有未完成故事。

## 人物钩子
完全不知道未来能力的情况下，前三章后读者为什么仍会记住并想继续看这个人？用可复述行为、矛盾、欲望或关系回答。
'''

EXCLUDED_POWER_TERMS = (
    '借万物一锋','复合借相','留着未完','未完承载','受力成路','受力留向','两处同身','双锚驻身',
    'World Power Normal','Legal Exception','Growth Compatibility','POWER BASELINE',
)
EXCLUDED_STORY_TERMS = (
    '宋照雪','魏停山','石晚舟','赫连渡','乌芙','青灯盐','白角夔','悬瓮城','沉铃泽','归潮原','黑火井','白鹭天桥','无岸雾海','万兽迁岭','地下驿网',
)


def parse_human_candidates(text: str) -> list[str]:
    matches = list(re.finditer(r'(?ms)^# HUMAN SEED CANDIDATE \d+｜.*?(?=^# HUMAN SEED CANDIDATE \d+｜|\Z)', text))
    return [m.group(0).strip() + '\n' for m in matches]


def clean_acp(path: Path) -> str:
    data = json.loads(path.read_text(encoding='utf-8'))
    if not data.get('ok', True):
        raise RuntimeError(data.get('error'))
    text = data.get('text', '')
    return re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*', '\n', text).strip() + '\n'


def prepare() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    life = (SOURCE / 'E_LIFE_CONTEXT.md').read_text(encoding='utf-8')
    gbrain = (ROOT / 'HUMAN_GBRAIN.md').read_text(encoding='utf-8')
    v4 = (SOURCE / 'E_GROWTH_COMPAT_CHARACTER_CANDIDATES.md').read_text(encoding='utf-8')
    cards = split_character_candidates(v4)
    if len(cards) != 4:
        raise RuntimeError(f'expected 4 v4 candidates, got {len(cards)}')
    power_dir = ROOT / 'POWER_SEEDS_FROZEN'
    power_dir.mkdir(exist_ok=True)
    for card in cards:
        power = extract_frozen_power_seed(str(card['text']))
        (power_dir / f"POWER_SEED_{card['index']}.md").write_text(power, encoding='utf-8')
    prompt = HUMAN_PROMPT + '\n\n# LIFE CONTEXT｜Human Authority\n' + life + '\n\n# HUMAN GBRAIN CRAFT｜Abstract Only\n' + gbrain
    leaks = [x for x in EXCLUDED_POWER_TERMS if x in prompt]
    if leaks:
        raise RuntimeError(f'Human prompt leaked Power authority: {leaks}')
    story_leaks = [x for x in EXCLUDED_STORY_TERMS if x in prompt]
    if story_leaks:
        raise RuntimeError(f'Human prompt leaked Story Opportunities: {story_leaks}')
    (ROOT / 'HUMAN_SEED_PROMPT.md').write_text(prompt, encoding='utf-8')
    (ROOT / 'LIFE_CONTEXT.md').write_text(life, encoding='utf-8')
    (ROOT / 'V4_INTEGRATED_CHARACTER_BASELINE.md').write_text(v4, encoding='utf-8')


def materialize() -> None:
    text = clean_acp(ROOT / 'HUMAN_SEED_ACP.json')
    humans = parse_human_candidates(text)
    if len(humans) != 4:
        raise RuntimeError(f'expected 4 Human Seeds, got {len(humans)}')
    (ROOT / 'HUMAN_SEEDS.md').write_text(text, encoding='utf-8')
    power_hits = [x for x in EXCLUDED_POWER_TERMS if x in text]
    story_hits = [x for x in EXCLUDED_STORY_TERMS if x in text]
    (ROOT / 'LEAK_CHECK.json').write_text(json.dumps({'power_hits':power_hits,'story_opportunity_hits':story_hits},ensure_ascii=False,indent=2),encoding='utf-8')
    pair_dir = ROOT / 'PAIRED_CHARACTER_CARDS'
    pair_dir.mkdir(exist_ok=True)
    for i, human in enumerate(humans, start=1):
        power = (ROOT / 'POWER_SEEDS_FROZEN' / f'POWER_SEED_{i}.md').read_text(encoding='utf-8')
        combined = compose_character_card(power_seed=power, human_seed=human, index=i)
        (pair_dir / f'CHARACTER_CARD_{i}.md').write_text(combined, encoding='utf-8')


def finalize() -> None:
    rules = '''# Split Power Seed × Human Seed Experiment\n\n- Shared world: exact same protagonist-blind 澜生界; no new World call.\n- Power: exact v4 power-related sections, deterministic extraction, frozen before Human generation.\n- Human: one fresh GPT-5.6 Luna high call; sees LIFE_CONTEXT + Human-only GBrain craft; sees no Power Seed, Power Baseline, named Story Opportunity, future route, or Collision result.\n- Pairing: index 1↔1, 2↔2, 3↔3, 4↔4; no model chooses the best fit.\n- Composition: deterministic concatenation only; no Character Composer and no post-hoc explanation.\n- No Sol, Story Program, Outline, chapters, or LLM judge.\n'''
    (ROOT / 'TEST_RULES.md').write_text(rules,encoding='utf-8')
    parts=[
        '# Power Seed × Human Seed｜完整审计包', rules,
        '# LIFE CONTEXT｜Human 可见\n\n'+(ROOT/'LIFE_CONTEXT.md').read_text(encoding='utf-8'),
        '# HUMAN GBRAIN｜Human 可见\n\n'+(ROOT/'HUMAN_GBRAIN.md').read_text(encoding='utf-8'),
        '# A｜v4 Integrated Character Baseline\n\n'+(ROOT/'V4_INTEGRATED_CHARACTER_BASELINE.md').read_text(encoding='utf-8'),
        '# B｜Frozen Power Seeds',
    ]
    for i in range(1,5):
        parts.append((ROOT/'POWER_SEEDS_FROZEN'/f'POWER_SEED_{i}.md').read_text(encoding='utf-8'))
    parts += ['# B｜Independent Human Seeds\n\n'+(ROOT/'HUMAN_SEEDS.md').read_text(encoding='utf-8'), '# B｜Deterministically Paired Character Cards']
    for i in range(1,5):
        parts.append((ROOT/'PAIRED_CHARACTER_CARDS'/f'CHARACTER_CARD_{i}.md').read_text(encoding='utf-8'))
    parts += ['# Leak Check\n\n```json\n'+(ROOT/'LEAK_CHECK.json').read_text(encoding='utf-8')+'\n```']
    (ROOT/'SPLIT_SEED_AUDIT_PACKAGE.md').write_text('\n\n---\n\n'.join(x.strip() for x in parts)+'\n',encoding='utf-8')

if __name__=='__main__':
    {'prepare':prepare,'materialize':materialize,'finalize':finalize}[sys.argv[1]]()
