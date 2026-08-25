from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path('src').resolve()))

from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.prompts import DEFAULT_PROMPT_TEMPLATES, generate_prompt

ROOT = Path('books/real-exp-neutral-three-program-20260825-v1')
DIRECTION = (
    '成熟中文男频玄幻/修仙成长长篇。除此之外，不指定核心能力、主角性格、世界结构、'
    '资源类型、势力结构、冲突类型、题材子类型或长期主题，由当前 production creative chain 自主生成。'
)


def clean_acp(path: Path) -> str:
    data = json.loads(path.read_text(encoding='utf-8'))
    if not data.get('ok'):
        raise RuntimeError(f'ACP failed: {path}: {data.get("error")}')
    text = data['text']
    text = re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*', '\n', text)
    return text.strip() + '\n'


def candidate(text: str, n: int) -> str:
    m = re.search(rf'(?ms)^## 候选{n}：.*?(?=^## 候选{n+1}：|\Z)', text)
    if not m:
        raise RuntimeError(f'candidate {n} not found')
    return m.group(0).strip() + '\n'


def write_seed_prompt() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / 'AUTHOR_DIRECTION.md').write_text(DIRECTION + '\n', encoding='utf-8')
    rules = '''# Test Rules\n\n- Production baseline: current HEAD after upstream bias repair.\n- Author direction: one neutral request only.\n- Fantasy Seed: GPT-5.6 Luna high, GBrain OFF.\n- Freeze candidates 1/2/3 before downstream generation; no cherry-picking.\n- World Vision: GPT-5.6 Luna high, fixed Coordinate Reference 1 + creative GBrain <=3.\n- Story Program: GPT-5.6 Sol high, creative GBrain <=3.\n- Stop at Story Program. No Outline, no chapters.\n- Generated auxiliary ACP memory-citation blocks are stripped before downstream use and final artifacts.\n'''
    (ROOT / 'TEST_RULES.md').write_text(rules, encoding='utf-8')
    prompt = generate_prompt(
        mode='fantasy_seed',
        template=DEFAULT_PROMPT_TEMPLATES['fantasy_seed'],
        book_content='',
        creative_direction=DIRECTION,
    )
    (ROOT / 'seed_prompt.md').write_text(prompt, encoding='utf-8')


def materialize_seed() -> None:
    text = clean_acp(ROOT / 'seed_acp.json')
    (ROOT / 'FANTASY_SEED_ALL.md').write_text(text, encoding='utf-8')
    for i in (1, 2, 3):
        p = ROOT / f'book-{i}'
        p.mkdir(parents=True, exist_ok=True)
        seed = candidate(text, i)
        (p / 'FANTASY_SEED.md').write_text(seed, encoding='utf-8')


def write_world_prompts() -> None:
    for i in (1, 2, 3):
        p = ROOT / f'book-{i}'
        seed = (p / 'FANTASY_SEED.md').read_text(encoding='utf-8')
        g = retrieve_gbrain(mode='world_vision', creative_direction=DIRECTION, fantasy_seed=seed)
        (p / 'world_gbrain.json').write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding='utf-8')
        bundle = g['result']
        (p / 'world_gbrain_bundle.md').write_text(bundle + '\n', encoding='utf-8')
        prompt = generate_prompt(
            mode='world_vision',
            template=DEFAULT_PROMPT_TEMPLATES['world_vision'],
            book_content='',
            creative_direction=DIRECTION,
            fantasy_seed=seed,
            creative_state={'fantasy_seed': {'status': 'author_approved'}},
            gbrain_inspiration=bundle,
        )
        (p / 'world_prompt.md').write_text(prompt, encoding='utf-8')
        print(i, 'coordinate', g.get('coordinate_reference_count'), 'creative', g.get('accepted_count'), [x.get('slug') for x in g.get('accepted', [])])


def materialize_worlds() -> None:
    for i in (1, 2, 3):
        p = ROOT / f'book-{i}'
        (p / 'WORLD_VISION.md').write_text(clean_acp(p / 'world_acp.json'), encoding='utf-8')


def write_program_prompts() -> None:
    for i in (1, 2, 3):
        p = ROOT / f'book-{i}'
        seed = (p / 'FANTASY_SEED.md').read_text(encoding='utf-8')
        world = (p / 'WORLD_VISION.md').read_text(encoding='utf-8')
        g = retrieve_gbrain(mode='idea', creative_direction=DIRECTION, fantasy_seed=seed, world_vision=world)
        (p / 'program_gbrain.json').write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding='utf-8')
        bundle = g['result']
        (p / 'program_gbrain_bundle.md').write_text(bundle + '\n', encoding='utf-8')
        prompt = generate_prompt(
            mode='idea',
            template=DEFAULT_PROMPT_TEMPLATES['idea'],
            book_content='',
            creative_direction=DIRECTION,
            fantasy_seed=seed,
            world_vision=world,
            creative_state={'fantasy_seed': {'status': 'author_approved'}, 'world_vision': {'status': 'author_approved'}},
            gbrain_inspiration=bundle,
        )
        (p / 'program_prompt.md').write_text(prompt, encoding='utf-8')
        print(i, 'creative', g.get('accepted_count'), [x.get('slug') for x in g.get('accepted', [])])


def materialize_programs() -> None:
    for i in (1, 2, 3):
        p = ROOT / f'book-{i}'
        (p / 'STORY_PROGRAM.md').write_text(clean_acp(p / 'program_acp.json'), encoding='utf-8')


def hshift(text: str, delta: int = 2) -> str:
    out = []
    for line in text.splitlines():
        m = re.match(r'^(#{1,6})(\s+.*)$', line)
        if m:
            line = '#' * min(6, len(m.group(1)) + delta) + m.group(2)
        out.append(line)
    return '\n'.join(out).strip() + '\n'


def finalize() -> None:
    titles = []
    combined = [
        '# 三本中立新书｜上游合集（截至 Story Program）',
        '',
        '> 生成链：GPT-5.6 Luna high Fantasy Seed → GPT-5.6 Luna high World Vision → GPT-5.6 Sol high Story Program。',
        '> 作者输入只规定“成熟中文男频玄幻/修仙成长长篇”，不指定能力、主角性格、世界结构、资源、势力、冲突、题材子类型或主题。',
        '> Fantasy Seed 候选 1/2/3 在下游生成前冻结，无人工挑选；不包含 Outline。',
        '',
    ]
    meta = {'author_direction': DIRECTION, 'books': []}
    for i in (1, 2, 3):
        p = ROOT / f'book-{i}'
        seed = (p / 'FANTASY_SEED.md').read_text(encoding='utf-8')
        world = (p / 'WORLD_VISION.md').read_text(encoding='utf-8')
        program = (p / 'STORY_PROGRAM.md').read_text(encoding='utf-8')
        title_match = re.search(r'^## 候选\d+：(.+)$', seed, re.M)
        title = title_match.group(1).strip() if title_match else f'Book {i}'
        titles.append(title)
        book_text = f'# {title}\n\n## Fantasy Seed\n\n{hshift(seed, 2)}\n## World Vision\n\n{hshift(world, 2)}\n## Story Program\n\n{hshift(program, 2)}'
        (p / 'BOOK.md').write_text(book_text, encoding='utf-8')
        combined += ['---', '', f'# 第{i}本｜{title}', '', '## Fantasy Seed', '', hshift(seed, 2), '## World Vision', '', hshift(world, 2), '## Story Program', '', hshift(program, 2), '']
        wg = json.loads((p / 'world_gbrain.json').read_text(encoding='utf-8'))
        pg = json.loads((p / 'program_gbrain.json').read_text(encoding='utf-8'))
        stages = len(re.findall(r'(?m)^#### 阶段\d+：', program))
        meta['books'].append({
            'index': i,
            'title': title,
            'world_coordinate_reference_count': wg.get('coordinate_reference_count'),
            'world_creative_count': wg.get('accepted_count'),
            'program_creative_count': pg.get('accepted_count'),
            'story_program_stage_count': stages,
        })
    merged = '\n'.join(combined).strip() + '\n'
    merged = re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*', '\n', merged)
    (ROOT / 'BOOKS_UPSTREAM.md').write_text(merged, encoding='utf-8')
    meta['titles'] = titles
    (ROOT / 'RUN_METADATA.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(meta, ensure_ascii=False, indent=2))


COMMANDS = {
    'seed-prompt': write_seed_prompt,
    'seed': materialize_seed,
    'world-prompts': write_world_prompts,
    'worlds': materialize_worlds,
    'program-prompts': write_program_prompts,
    'programs': materialize_programs,
    'finalize': finalize,
}

if __name__ == '__main__':
    COMMANDS[sys.argv[1]]()
