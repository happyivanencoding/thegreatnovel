from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path('src').resolve()))
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.prompts import DEFAULT_PROMPT_TEMPLATES, generate_prompt

ROOT = Path('books/real-exp-life-engine-softening-ab-20260825-v1')
DIRECTION = ('成熟中文男频玄幻/修仙成长长篇。除此之外，不指定核心能力、主角性格、世界结构、资源类型、'
             '势力结构、冲突类型、题材子类型或长期主题，由当前 production creative chain 自主生成。')


def clean(path: Path) -> str:
    raw = path.read_text(encoding='utf-8')
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = None
    text = data.get('text', '') if isinstance(data, dict) else raw
    if isinstance(data, dict) and not data.get('ok', True):
        raise RuntimeError(data.get('error'))
    text = re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*', '\n', text)
    return text.strip() + '\n'


def candidate(text: str, n: int) -> str:
    m = re.search(rf'(?ms)^## 候选{n}：.*?(?=^## 候选{n+1}：|\Z)', text)
    if not m:
        raise RuntimeError(f'candidate {n} not found')
    return m.group(0).strip() + '\n'


def write_seed_prompt(side: str) -> None:
    p = ROOT / side
    p.mkdir(parents=True, exist_ok=True)
    (ROOT / 'AUTHOR_DIRECTION.md').write_text(DIRECTION + '\n', encoding='utf-8')
    prompt = generate_prompt(mode='fantasy_seed', template=DEFAULT_PROMPT_TEMPLATES['fantasy_seed'],
                             book_content='', creative_direction=DIRECTION)
    (p / 'seed_prompt.md').write_text(prompt, encoding='utf-8')


def materialize_seed(side: str) -> None:
    p = ROOT / side
    text = clean(p / 'seed_acp.json')
    (p / 'FANTASY_SEED_ALL.md').write_text(text, encoding='utf-8')
    for i in (1, 2, 3):
        b = p / f'book-{i}'
        b.mkdir(parents=True, exist_ok=True)
        (b / 'FANTASY_SEED.md').write_text(candidate(text, i), encoding='utf-8')


def write_world_prompts(side: str) -> None:
    p = ROOT / side
    for i in (1, 2, 3):
        b = p / f'book-{i}'
        seed = (b / 'FANTASY_SEED.md').read_text(encoding='utf-8')
        g = retrieve_gbrain(mode='world_vision', creative_direction=DIRECTION, fantasy_seed=seed)
        (b / 'world_gbrain.json').write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding='utf-8')
        prompt = generate_prompt(mode='world_vision', template=DEFAULT_PROMPT_TEMPLATES['world_vision'],
                                 book_content='', creative_direction=DIRECTION, fantasy_seed=seed,
                                 creative_state={'fantasy_seed': {'status': 'author_approved'}},
                                 gbrain_inspiration=g['result'])
        (b / 'world_prompt.md').write_text(prompt, encoding='utf-8')
        print(side, i, 'coordinate', g.get('coordinate_reference_count'), 'creative', g.get('accepted_count'))


def materialize_worlds(side: str) -> None:
    p = ROOT / side
    for i in (1, 2, 3):
        b = p / f'book-{i}'
        (b / 'WORLD_VISION.md').write_text(clean(b / 'world_acp.json'), encoding='utf-8')


def hshift(text: str, delta: int = 2) -> str:
    out=[]
    for line in text.splitlines():
        m=re.match(r'^(#{1,6})(\s+.*)$', line)
        if m: line='#'*min(6,len(m.group(1))+delta)+m.group(2)
        out.append(line)
    return '\n'.join(out).strip()+'\n'


def finalize() -> None:
    rules = '''# A/B Test Rules\n\n- Test target: ONLY Life Engine softening.\n- A: production baseline before Life Engine softening.\n- B: same production chain with only Life Engine changed from a durable/life-mission framing to a personal, provisional, changeable pull; it must not auto-derive public/social missions from the Core Fantasy.\n- Same neutral author direction for A and B.\n- Fantasy Seed: GPT-5.6 Luna high, GBrain OFF.\n- Freeze candidates 1/2/3 on each side before World generation; no cherry-picking.\n- World Vision: GPT-5.6 Luna high, fixed Coordinate Reference 1 + creative GBrain <=3.\n- Stop at World Vision. NO Story Program / Outline / chapters.\n- No LLM judge; user audits the full artifacts.\n'''
    (ROOT/'TEST_RULES.md').write_text(rules,encoding='utf-8')
    combined=['# Life Engine Softening A/B｜完整产物合集','',rules.strip(),'','# Author Direction','',DIRECTION,'']
    meta={'direction':DIRECTION,'sides':{}}
    for side,label in [('A','A｜当前 production baseline'),('B','B｜Life Engine softening')]:
        p=ROOT/side
        allseed=(p/'FANTASY_SEED_ALL.md').read_text(encoding='utf-8')
        combined += ['---','',f'# {label}','','## Fantasy Seed｜完整候选批次','',hshift(allseed,1)]
        sm=[]
        for i in (1,2,3):
            b=p/f'book-{i}'
            seed=(b/'FANTASY_SEED.md').read_text(encoding='utf-8')
            world=(b/'WORLD_VISION.md').read_text(encoding='utf-8')
            title=re.search(r'^## 候选\d+：(.+)$',seed,re.M)
            title=title.group(1).strip() if title else f'Book {i}'
            wg=json.loads((b/'world_gbrain.json').read_text(encoding='utf-8'))
            combined += ['',f'## {side}{i}｜{title}','','### Frozen Fantasy Seed','',hshift(seed,2),'### World Vision','',hshift(world,2)]
            sm.append({'index':i,'title':title,'coordinate_reference_count':wg.get('coordinate_reference_count'),'creative_count':wg.get('accepted_count')})
        meta['sides'][side]=sm
    merged='\n'.join(combined).strip()+'\n'
    merged=re.sub(r'(?s)\s*<oai-mem-citation>.*?</oai-mem-citation>\s*','\n',merged)
    (ROOT/'AB_FULL_ARTIFACTS.md').write_text(merged,encoding='utf-8')
    (ROOT/'RUN_METADATA.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')


if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='seed-prompt': write_seed_prompt(sys.argv[2])
    elif cmd=='seed': materialize_seed(sys.argv[2])
    elif cmd=='world-prompts': write_world_prompts(sys.argv[2])
    elif cmd=='worlds': materialize_worlds(sys.argv[2])
    elif cmd=='finalize': finalize()
    else: raise SystemExit(cmd)
