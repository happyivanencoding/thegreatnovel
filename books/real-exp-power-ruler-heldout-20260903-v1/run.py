from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.character_seeds import compose_character_card, split_human_seed_authorities
from story_mvp.gbrain_retrieval import retrieve_gbrain
from story_mvp.power_novelty import build_power_novelty_bundle

CASES = {
    "A_body_martial": """成熟中文男频玄幻成长长篇。建立一个完全全新的血肉近战武道世界：主流力量必须主要来自身体、呼吸、血骨、近战兵器与直接肉身战斗，不以法术、召唤、空间术、规则权限或职业流程为核心。公共精确力量主尺必须真实改变输出/爆发、身体承受、反应速度、持续作战与能否进入更危险环境；不要把主尺写成只有称号的装饰数字。世界、地点、异兽、势力和高价值对象自行原创。

Power Asymmetry 由当前系统自行生成，不预指定能力。开局前段必须自然出现一次：主角刚获得/第一次稳定使用 Core Asymmetry 后，与公开主尺上明显更高一档或大档的人物发生真实冲突。不要规定主角必须赢，也不要为了测试刻意让他输；让 Story Program 根据当前 World + Power 自己决定是完整胜利、局部翻盘、夺物、逼退、逃生或其它结果。后续要有可长期成长和复合的男频爽感。""",
    "B_beast_bond": """成熟中文男频玄幻成长长篇。建立一个完全全新的浮空群岛驭兽/伴生兽世界：主流力量来自人与真实存在的伴生兽、契兽或异兽伙伴之间的共鸣与共同作战；个人可以修炼，但伙伴必须有自己的身体、习性与行动，不能降成技能按钮。公共精确力量主尺必须真实改变共享力量强度、骑乘/承载、双方反应与同步、作用距离/持续，以及能否进入更危险风层；不要把主尺写成只有称号的装饰数字。不要使用亚特兰蒂斯、海相、静默水等旧设定。

Power Asymmetry 由当前系统自行生成，不预指定能力。开局前段必须自然出现一次：主角刚获得/第一次稳定使用 Core Asymmetry 后，与公开主尺上明显更高一档或大档的人物发生真实冲突。不要规定主角必须赢，也不要为了测试刻意让他输；让 Story Program 根据当前 World + Power 自己决定是完整胜利、局部翻盘、夺物、逼退、逃生或其它结果。后续要保持人物自身 Power Identity 与真实伙伴/外部资产的区别。""",
    "C_spatial_fold": """成熟中文男频玄幻成长长篇。建立一个完全全新的巨城折叠空间术世界：主流力量是读者一眼能看懂的直接空间动作，例如移动、置换、折叠距离、改变落点、切开空间或穿过空间层；不要把核心写成理解/定义/权限/验证等抽象 ontology，也不要以驭兽、纯肉身体修或工程流程为主。公共精确力量主尺必须真实改变可作用的质量/对象规模、距离、连续使用次数或持续、身体承受，以及能否进入更危险折叠层；不要把主尺写成只有称号的装饰数字。

Power Asymmetry 由当前系统自行生成，不预指定能力。开局前段必须自然出现一次：主角刚获得/第一次稳定使用 Core Asymmetry 后，与公开主尺上明显更高一档或大档的人物发生真实冲突。不要规定主角必须赢，也不要为了测试刻意让他输；让 Story Program 根据当前 World + Power 自己决定是完整胜利、局部翻盘、夺物、逼退、逃生或其它结果。后续允许非常大胆的空间玩法，但必须让公共主尺的基础盘继续有现实意义。""",
}

SEEDS = {
    "A_body_martial": 2026090301,
    "B_beast_bond": 2026090302,
    "C_spatial_fold": 2026090303,
}


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
                cwd=ROOT,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=1800,
            )
        except subprocess.TimeoutExpired:
            last = f"timeout {label}"
            time.sleep(3 + attempt * 2)
            continue
        if proc.returncode == 0 and out_path.exists():
            data = json.loads(out_path.read_text(encoding="utf-8"))
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (proc.stderr + "\n" + proc.stdout)[-6000:]
        time.sleep(3 + attempt * 2)
    raise RuntimeError(f"ACP failed {label}: {last}")


def run_llm(prompt: str, directory: Path, name: str, model: str, effort: str) -> tuple[str, float]:
    pp = directory / f"{name}_prompt.md"
    ap = directory / f"{name}_acp.json"
    rp = directory / f"{name}_response.md"
    pp.write_text(prompt, encoding="utf-8")
    data = call(pp, ap, model, effort, f"{directory.name}:{name}")
    text = clean(data.get("text", ""))
    rp.write_text(text + "\n", encoding="utf-8")
    return text, float(data.get("wall_seconds") or 0)


def blocks(text: str, marker: str, expected: int) -> list[str]:
    starts = [m.start() for m in re.finditer(rf"(?m)^# {re.escape(marker)} \d+｜", text)]
    if len(starts) != expected:
        raise RuntimeError(f"expected {expected} {marker}, got {len(starts)}")
    starts.append(len(text))
    return [text[starts[i]:starts[i + 1]].strip() for i in range(expected)]


def adopt_first(text: str, marker: str, seed_marker: str, expected: int) -> str:
    first = blocks(text, marker, expected)[0]
    return re.sub(rf"(?m)^# {re.escape(marker)} 1｜", f"# {seed_marker}｜", first, count=1)


def run_case(case_id: str, direction: str) -> dict:
    d = EXP / case_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "AUTHOR_DIRECTION.md").write_text(direction + "\n", encoding="utf-8")
    timing: dict[str, float] = {}

    # World — production GBrain route + production prompt.
    wr = retrieve_gbrain(mode="world_vision", creative_direction=direction)
    dump(d / "gbrain_world.json", wr)
    world_prompt = generate_split_prompt(
        mode="world_vision",
        creative_direction=direction,
        gbrain_inspiration=wr["result"],
    )
    world, timing["world"] = run_llm(world_prompt, d, "world", "gpt-5.6-luna", "high")
    (d / "WORLD_VISION.md").write_text(world + "\n", encoding="utf-8")

    state_world = {"world_vision": {"status": "author_approved"}}
    novelty = build_power_novelty_bundle(seed=SEEDS[case_id])
    (d / "POWER_NOVELTY.md").write_text(novelty + "\n", encoding="utf-8")

    # Power + Human are isolated production lanes. Fixed candidate-1 adoption is preregistered.
    pr = retrieve_gbrain(mode="power_seed", creative_direction=direction, world_vision=world)
    hr = retrieve_gbrain(mode="human_seed", creative_direction=direction, world_vision=world)
    dump(d / "gbrain_power.json", pr)
    dump(d / "gbrain_human.json", hr)
    power_prompt = generate_split_prompt(
        mode="power_seed",
        world_vision=world,
        creative_state=state_world,
        gbrain_inspiration=pr["result"],
        power_novelty=novelty,
    )
    human_prompt = generate_split_prompt(
        mode="human_seed",
        world_vision=world,
        creative_state=state_world,
        gbrain_inspiration=hr["result"],
    )
    with ThreadPoolExecutor(max_workers=2) as ex:
        fp = ex.submit(run_llm, power_prompt, d, "power_candidates", "gpt-5.6-luna", "high")
        fh = ex.submit(run_llm, human_prompt, d, "human_candidates", "gpt-5.6-luna", "high")
        powers, timing["power_candidates"] = fp.result()
        humans, timing["human_candidates"] = fh.result()

    power = adopt_first(powers, "POWER CANDIDATE", "POWER SEED", 3)
    human = adopt_first(humans, "HUMAN CANDIDATE", "HUMAN SEED", 4)
    (d / "POWER_SEED.md").write_text(power + "\n", encoding="utf-8")
    (d / "HUMAN_SEED.md").write_text(human + "\n", encoding="utf-8")
    character = compose_character_card(power_seed=power, human_seed=human)
    human_parts = split_human_seed_authorities(human)
    (d / "CHARACTER.md").write_text(character, encoding="utf-8")
    (d / "CHARACTER_INITIAL_STATE.md").write_text(human_parts["initial_state"], encoding="utf-8")

    # Story Program — first full collision, current Sol-high production route.
    state_character = {
        "world_vision": {"status": "author_approved"},
        "character_card": {"status": "author_approved"},
    }
    sr = retrieve_gbrain(
        mode="idea",
        creative_direction=direction,
        world_vision=world,
        character_card=character,
    )
    dump(d / "gbrain_story.json", sr)
    story_prompt = generate_split_prompt(
        mode="idea",
        creative_direction=direction,
        world_vision=world,
        character_card=character,
        character_initial_state=human_parts["initial_state"],
        creative_state=state_character,
        gbrain_inspiration=sr["result"],
    )
    story, timing["story_program"] = run_llm(story_prompt, d, "story_program", "gpt-5.6-sol", "high")
    (d / "STORY_PROGRAM.md").write_text(story + "\n", encoding="utf-8")

    # Outline — to see how the early confrontation is concretely scheduled.
    state_story = {
        "world_vision": {"status": "author_approved"},
        "character_card": {"status": "author_approved"},
        "proposal": {"status": "author_approved"},
    }
    orr = retrieve_gbrain(
        mode="outline",
        creative_direction=direction,
        world_vision=world,
        character_card=character,
        proposal_context=story,
    )
    dump(d / "gbrain_outline.json", orr)
    outline_prompt = generate_split_prompt(
        mode="outline",
        creative_direction=direction,
        world_vision=world,
        character_card=character,
        character_initial_state=human_parts["initial_state"],
        creative_state=state_story,
        proposal_context=story,
        book_content="",
        gbrain_inspiration=orr["result"],
    )
    outline, timing["outline"] = run_llm(outline_prompt, d, "outline", "gpt-5.6-luna", "high")
    (d / "OUTLINE.md").write_text(outline + "\n", encoding="utf-8")

    dump(d / "TIMING.json", timing)
    return {"case": case_id, "timing": timing}


def main() -> None:
    if not RUNNER.exists():
        raise SystemExit(f"ACP runner missing: {RUNNER}")
    started = time.perf_counter()
    results = []
    errors = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(run_case, case_id, direction): case_id for case_id, direction in CASES.items()}
        for future in as_completed(futures):
            case_id = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(f"DONE {case_id}", flush=True)
            except Exception as exc:
                errors.append({"case": case_id, "error": repr(exc)})
                print(f"FAIL {case_id}: {exc!r}", flush=True)
    summary = {
        "selection_rule": "fixed candidate 1 for Power and Human; preregistered",
        "cases": results,
        "errors": errors,
        "total_wall_seconds": round(time.perf_counter() - started, 3),
    }
    dump(EXP / "RUN_SUMMARY.json", summary)
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
