from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP_ROOT = ROOT / "books" / "real-exp-reviser-noop-upstream-heldout-20260830-v1"
BOOK = EXP_ROOT / "heldout-new-novel"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.character_context import project_character_life_context, project_character_power_baseline
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.character_seeds import compose_character_card, split_human_seed_authorities
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.hybrid_runtime import extract_primary_draft
from story_mvp.power_novelty import build_power_novelty_bundle
from story_mvp.prompts import generate_prompt, parse_canon_memory
from story_mvp.storage import apply_state_delta_to_book, parse_book_sections, validate_book_content_for_save, validate_chapter_body_for_save

AUTHOR_DIRECTION = """成熟中文男频玄幻长篇。这个实验必须生成一部与九垂原、分影原型明显不同的新书：禁止把商队契约、粮道、水井/迁徙资源、回潮楔、分身/影身、公开试场契约作为核心故事发动机或核心能力。优先使用传统但有鲜明变体的玄幻/仙侠式强者世界：强敌、修炼、具体宝物/兵器/异兽/遗迹、明确力量主尺、人物欲望和关系可以成为前景，但具体世界、能力、人物与故事由当前系统自己产生。

目标仍是成熟男频成长爽文：主角要主动、想赢、想拿到具体好东西，有可以羡慕的 Power Asymmetry，公共力量尺清楚；私人欲望、钱、面子、审美、野心、报复、吸引、偏心都合法，不净化成正确人格。前四章应自然完成开篇抓力、第一次核心能力兑现、至少一个具体想要/得到/差点失去的高价值对象、一个有个人立场的关系变化，以及下一层世界/敌人/机会的真实入口，但不要为了满足清单硬塞事件。

Supporting Logic 不得成为 Story Engine；不要把新书写成职业流程、治理、测试验证、路线优化或合同执行。"""

NOVELTY_SEED = 202608301901
PROTOCOL_HASH = "56B6ECC21151811F21DDDF2B696B5052DF417AD0419103473D44A25435CE13F3"
WATCH = """## FINAL-DRAFT READINESS WATCH｜只在写完正文前内部检查一次

不要重规划剧情，也不要输出审计。只用本 Prompt 已经给你的 Authority / Mission / Curated Context，对最终正文做一次很窄的提交前检查：

1. **精确事实不自己补全**：金额、价格、旧对白、伤势、身份、持有人、能力边界与历史状态，输入没明确就不补；输入已经给了具体对象/状态时，全章用同一个具体对象/状态，不把“资格/份额/承诺”升级成“已到账/已拥有”。
2. **关键边界只落一次**：若本章结果真实依赖一个已明确的持有/付款/力量/冷却/未知边界，在发生点让读者看懂一次即可；不要漏，也不要后面再解释一遍。
3. **已排程价值说具体一次**：Curated Context / Reader Release 已明确某个具名入口、契约、奖励、地点或身份为什么值，就用现成事实让读者知道一次；不要压成“一个机会 / 更大的入口”，也不要新增待遇。
4. **结果成立就停**：动作、对白、物体变化和人物反应已经把意义写出来后，删掉随后同义的作者解释、人物总结、能力复盘或“不是A也不是B”的裁断；让后果进入下一动作。
5. **私人动机别净化**：Curated Context 已明确钱、胜负、占有、虚荣、审美/身体吸引、嫉妒、报复或某个具体人的牵引，而且现场自然触发时，让它通过一次想法/对白/注意力/选择露出来；不要改写成中性职责或正确分析。

除此之外按原 Primary 合同正常写，不为了通过这五项而新增说明段。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def dump(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def call(prompt_path: Path, out_path: Path, model: str, effort: str, label: str) -> dict:
    last = ""
    for attempt in range(3):
        try:
            proc = subprocess.run(
                ["node", str(RUNNER), str(prompt_path), str(out_path), model, effort, str(ROOT)],
                cwd=ROOT, text=True, capture_output=True, encoding="utf-8", errors="replace", timeout=1200,
            )
        except subprocess.TimeoutExpired:
            last = f"timeout {label}"
            time.sleep(2 + attempt * 2)
            continue
        if proc.returncode == 0 and out_path.exists():
            data = json.loads(out_path.read_text(encoding="utf-8"))
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (proc.stderr + "\n" + proc.stdout)[-4000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(f"ACP failed {label}: {last}")


def run_file(prompt: str, directory: Path, name: str, model: str, effort: str) -> tuple[str, float]:
    directory.mkdir(parents=True, exist_ok=True)
    pp = directory / f"{name}_prompt.md"
    ap = directory / f"{name}_acp.json"
    rp = directory / f"{name}_response.md"
    pp.write_text(prompt, encoding="utf-8")
    data = call(pp, ap, model, effort, name)
    text = clean(data.get("text", ""))
    rp.write_text(text + "\n", encoding="utf-8")
    return text, float(data.get("wall_seconds") or 0)


def numbered_blocks(text: str, marker: str, count: int) -> list[str]:
    starts = [m.start() for m in re.finditer(rf"(?m)^# {re.escape(marker)} \d+", text)]
    if len(starts) != count:
        raise RuntimeError(f"Expected {count} {marker} blocks, got {len(starts)}")
    starts.append(len(text))
    return [text[starts[i]:starts[i+1]].strip() for i in range(count)]


def select_index(text: str, count: int) -> int:
    m = re.search(r"(?mi)^SELECT\s*:\s*(\d+)\s*$", text)
    if not m:
        raise RuntimeError(f"selector missing SELECT: {text[:800]}")
    value = int(m.group(1))
    if not 1 <= value <= count:
        raise RuntimeError(f"selector out of range: {value}")
    return value


def upstream() -> None:
    BOOK.mkdir(parents=True, exist_ok=True)
    (BOOK / "chapters").mkdir(exist_ok=True)
    (BOOK / "runs").mkdir(exist_ok=True)
    (BOOK / "AUTHOR_DIRECTION.md").write_text(AUTHOR_DIRECTION + "\n", encoding="utf-8")

    wr = retrieve_gbrain(mode="world_vision", creative_direction=AUTHOR_DIRECTION)
    wp = generate_split_prompt(mode="world_vision", creative_direction=AUTHOR_DIRECTION, gbrain_inspiration=wr["result"])
    world, ww = run_file(wp, BOOK, "world", "gpt-5.6-luna", "high")
    (BOOK / "WORLD_VISION.md").write_text(world + "\n", encoding="utf-8")

    state = {"world_vision": {"status": "author_approved"}}
    novelty = build_power_novelty_bundle(seed=NOVELTY_SEED)
    pr = retrieve_gbrain(mode="power_seed", creative_direction=AUTHOR_DIRECTION, world_vision=world)
    hr = retrieve_gbrain(mode="human_seed", creative_direction=AUTHOR_DIRECTION, world_vision=world)
    pp = generate_split_prompt(mode="power_seed", world_vision=world, creative_state=state, gbrain_inspiration=pr["result"], power_novelty=novelty)
    hp = generate_split_prompt(mode="human_seed", world_vision=world, creative_state=state, gbrain_inspiration=hr["result"])
    with ThreadPoolExecutor(max_workers=2) as ex:
        fp = ex.submit(run_file, pp, BOOK, "power_candidates", "gpt-5.6-luna", "high")
        fh = ex.submit(run_file, hp, BOOK, "human_candidates", "gpt-5.6-luna", "high")
        (powers, pw), (humans, hw) = fp.result(), fh.result()
    pblocks = numbered_blocks(powers, "POWER CANDIDATE", 3)
    hblocks = numbered_blocks(humans, "HUMAN CANDIDATE", 4)
    psel = f"""你是匿名 Power Selector。只根据当前世界和三个候选盲选最适合成熟中文男频长篇的 Core Asymmetry。优先：想拥有、强而不万能、一句话能懂、可长期复合、不是九垂原/分影旧机制。\n\n严格输出：\nSELECT: 1/2/3\nREASON: 3—6句。\n\n# POWER BASELINE\n{project_character_power_baseline(world)}\n\n# CANDIDATES\n{powers}\n"""
    hsel = f"""你是匿名 Human Selector。只根据当前生活背景和四个候选，盲选最适合成熟男频长篇的具体人物。允许钱、胜负、面子、欲望、审美、自利、报复、野心，不按道德评分。\n\n严格输出：\nSELECT: 1/2/3/4\nREASON: 3—6句。\n\n# LIFE CONTEXT\n{project_character_life_context(world)}\n\n# CANDIDATES\n{humans}\n"""
    with ThreadPoolExecutor(max_workers=2) as ex:
        fp = ex.submit(run_file, psel, BOOK, "power_select", "gpt-5.6-luna", "high")
        fh = ex.submit(run_file, hsel, BOOK, "human_select", "gpt-5.6-luna", "high")
        (ptxt, psw), (htxt, hsw) = fp.result(), fh.result()
    pi, hi = select_index(ptxt, 3), select_index(htxt, 4)
    power = re.sub(r"(?m)^# POWER CANDIDATE \d+｜", "# POWER SEED｜", pblocks[pi-1], count=1)
    human = re.sub(r"(?m)^# HUMAN CANDIDATE \d+｜", "# HUMAN SEED｜", hblocks[hi-1], count=1)
    (BOOK / "POWER_SEED.md").write_text(power + "\n", encoding="utf-8")
    (BOOK / "HUMAN_SEED.md").write_text(human + "\n", encoding="utf-8")
    character = compose_character_card(power_seed=power, human_seed=human)
    ha = split_human_seed_authorities(human)
    (BOOK / "CHARACTER.md").write_text(character, encoding="utf-8")
    (BOOK / "CHARACTER_INITIAL_STATE.md").write_text(ha["initial_state"], encoding="utf-8")

    cs = {"world_vision": {"status": "author_approved"}, "character_card": {"status": "author_approved"}}
    sr = retrieve_gbrain(mode="idea", creative_direction=AUTHOR_DIRECTION, world_vision=world, character_card=character)
    sp = generate_split_prompt(mode="idea", creative_direction=AUTHOR_DIRECTION, world_vision=world, character_card=character, character_initial_state=ha["initial_state"], creative_state=cs, gbrain_inspiration=sr["result"])
    story, sw = run_file(sp, BOOK, "story_program", "gpt-5.6-sol", "high")
    (BOOK / "STORY_PROGRAM.md").write_text(story + "\n", encoding="utf-8")

    os = {"world_vision": {"status": "author_approved"}, "character_card": {"status": "author_approved"}, "proposal": {"status": "author_approved"}}
    orr = retrieve_gbrain(mode="outline", creative_direction=AUTHOR_DIRECTION, world_vision=world, character_card=character, proposal_context=story)
    op = generate_split_prompt(mode="outline", creative_direction=AUTHOR_DIRECTION, world_vision=world, character_card=character, character_initial_state=ha["initial_state"], creative_state=os, proposal_context=story, gbrain_inspiration=orr["result"])
    outline, ow = run_file(op, BOOK, "outline", "gpt-5.6-luna", "high")
    pos = outline.find("# 小说总体设计画像")
    if pos >= 0:
        outline = outline[pos:]
    validate_book_content_for_save(outline)
    (BOOK / "BOOK.md").write_text(outline + "\n", encoding="utf-8")
    dump(BOOK / "UPSTREAM_TIMING.json", {"world":ww,"power_candidates":pw,"human_candidates":hw,"power_select":psw,"human_select":hsw,"story_program":sw,"outline":ow,"selection":{"power":pi,"human":hi}})


def book() -> str:
    return (BOOK / "BOOK.md").read_text(encoding="utf-8")

def sections() -> dict:
    return parse_book_sections(book())

def memory() -> dict:
    return parse_canon_memory(sections()["status"])

def recent() -> str:
    return memory().get("recent_summaries", "").strip()

def previous(n: int) -> str:
    if n <= 1: return ""
    return (BOOK / "chapters" / f"chapter-{n-1:04d}.md").read_text(encoding="utf-8")

def chapter_plan(n: int) -> str:
    src = sections()["small_plan"]
    m = re.search(rf"(?ms)^## 第{n}章：.*?(?=^## 第{n+1}章：|\Z)", src)
    if not m: raise RuntimeError(f"missing chapter plan {n}")
    return m.group(0).strip()

def long_block(n: int) -> str:
    src=sections()["long_plan"]
    for m in re.finditer(r"(?ms)^## 第(\d+)[—-](\d+)章：.*?(?=^## 第\d+[—-]\d+章：|\Z)",src):
        if int(m.group(1)) <= n <= int(m.group(2)): return m.group(0).strip()
    return ""


def chapter(n: int) -> None:
    d=BOOK/'runs'/f'chapter-{n:04d}'; d.mkdir(parents=True,exist_ok=True)
    world=(BOOK/'WORLD_VISION.md').read_text(encoding='utf-8')
    character=(BOOK/'CHARACTER.md').read_text(encoding='utf-8')
    plan=chapter_plan(n); block=long_block(n)
    direction="严格执行当前批准的新书计划。保持主角私人欲望、核心幻想、具体获得、人物冲突在前景；Supporting Logic 不得成为 Story Engine。"
    dp=generate_prompt(mode='director',template='',book_content=book(),world_vision=world,world_expansions='',character_card=character,current_long_block=block,previous_chapter_text=previous(n),current_outline='',current_chapter_plan=plan,recent_summaries=recent(),chapter_number=n,creative_direction=direction)
    dr,dw=run_file(dp,d,'director','gpt-5.6-luna','high')
    cp=generate_prompt(mode='context_curator',template='',book_content=book(),world_vision=world,world_expansions='',character_card=character,current_long_block=block,previous_chapter_text=previous(n),current_outline=dr,current_chapter_plan=plan,recent_summaries=recent(),gbrain_inspiration='',chapter_number=n)
    cu,cw=run_file(cp,d,'curator','gpt-5.6-luna','high')
    base=generate_prompt(mode='primary_writer',template='',book_content=book(),world_vision=world,world_expansions='',character_card=character,current_long_block=block,previous_chapter_text=previous(n),current_outline=dr,current_chapter_plan=plan,recent_summaries=recent(),gbrain_inspiration='',curated_context=cu,curator_response=cu,chapter_number=n)
    (d/'primary_base_prompt.md').write_text(base,encoding='utf-8')
    treatment=base.rstrip()+"\n\n"+WATCH+"\n"
    with ThreadPoolExecutor(max_workers=2) as ex:
        fc=ex.submit(run_file,base,d,'control_primary','gpt-5.6-terra','high')
        ft=ex.submit(run_file,treatment,d,'treatment_primary','gpt-5.6-terra','high')
        (cr,cpw),(tr,tpw)=fc.result(),ft.result()
    cb=extract_primary_draft(cr).strip(); tb=extract_primary_draft(tr).strip()
    validate_chapter_body_for_save(cb);validate_chapter_body_for_save(tb)
    (d/'control_primary_body.md').write_text(cb+'\n',encoding='utf-8');(d/'treatment_primary_body.md').write_text(tb+'\n',encoding='utf-8')
    def rev_prompt(primary_body,primary_raw):
        return generate_prompt(mode='authority_reviser',template='',book_content=book(),world_vision=world,world_expansions='',character_card=character,current_long_block=block,previous_chapter_text=previous(n),current_outline=dr,current_chapter_plan=plan,recent_summaries=recent(),curated_context=cu,curator_response=cu,primary_draft=primary_body,primary_writer_response=primary_raw,chapter_number=n)
    with ThreadPoolExecutor(max_workers=2) as ex:
        fc=ex.submit(run_file,rev_prompt(cb,cr),d,'control_reviser','gpt-5.6-luna','high')
        ft=ex.submit(run_file,rev_prompt(tb,tr),d,'treatment_reviser','gpt-5.6-luna','high')
        (cfr,crw),(tfr,trw)=fc.result(),ft.result()
    cfb=extract_primary_draft(cfr).strip();tfb=extract_primary_draft(tfr).strip()
    validate_chapter_body_for_save(cfb);validate_chapter_body_for_save(tfb)
    (d/'control_final_body.md').write_text(cfb+'\n',encoding='utf-8');(d/'treatment_final_body.md').write_text(tfb+'\n',encoding='utf-8')
    # Canon progression deliberately uses control production final so both arms share future inputs.
    (BOOK/'chapters'/f'chapter-{n:04d}.md').write_text(cfb+'\n',encoding='utf-8')
    sp=generate_prompt(mode='state_delta',template='',book_content=book(),recent_summaries=recent(),chapter_number=n,chapter_prose=cfb)
    st,stw=run_file(sp,d,'state','gpt-5.6-luna','low')
    updated=apply_state_delta_to_book(book(),n,st);validate_book_content_for_save(updated);(BOOK/'BOOK.md').write_text(updated,encoding='utf-8')
    dump(d/'timing.json',{'director':dw,'curator':cw,'control_primary':cpw,'treatment_primary':tpw,'control_reviser':crw,'treatment_reviser':trw,'state':stw,'control_chain_to_final':dw+cw+cpw+crw,'treatment_chain_to_final':dw+cw+tpw+trw})


def main():
    import hashlib
    protocol=(EXP_ROOT/'PROTOCOL.md').read_bytes()
    actual=hashlib.sha256(protocol).hexdigest().upper()
    if actual != PROTOCOL_HASH: raise RuntimeError(f'Protocol changed after freeze: {actual}')
    if not RUNNER.exists(): raise RuntimeError(f'missing runner {RUNNER}')
    upstream()
    for n in range(1,5): chapter(n)
    dump(BOOK/'CONTROL_GENERATION_COMPLETE.json',{'chapters':4,'protocol_sha256':PROTOCOL_HASH,'canon_progression':'control_reviser'})

if __name__=='__main__':main()
