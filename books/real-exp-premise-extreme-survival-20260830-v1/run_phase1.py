from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.premise_aperture import (
    build_selected_premise_compiler_prompt,
    build_single_pass_prompt,
    extract_sections,
)

RUNNER = ROOT / "temps" / "acp_readonly_runner.mjs"

EXTREME_TREATMENT = r"""# EXPERIMENT TREATMENT｜EXTREME RIGHT-TAIL

原 S1/S2/S3 梯度保持，但本实验特别要求 S3 进入更右侧的创意尾部，而不是只比 S2 多一个机制。

S3 必须同时满足：
- 只押一个主异常；不要把四个怪点拼成四套系统。
- 优先打碎一个中文男频成长文很深的默认假设，例如“主角必须是连续的人形生命”“地图是主角进入的外部空间”“死亡只能终止行动”“武器只是被使用的外物”“别人确认你存在通常只会让你更危险”等；具体砸哪一个由你重新发明，不要照抄这些例子。
- Protagonist Ontology 默认不得是普通人类少年身体；若坚持普通人形，必须有一个更强、更直接的单一偏离足以改变整本书的基本动作语法。
- `主角反复会做的新动作` 必须是 4—7 个具体动词/动作短语，至少 3 个普通人类修士在没有这项 premise 时根本不会自然拥有。禁止用“分析、判断、规划、登记、维护、优化、获得资格”凑数。
- 第一章就发生一次清楚的 unfair payoff；如果现场存在真实观众/敌人/生态位，必须立刻产生一次可见 repricing、恐惧、争抢、失态、模仿、围猎或其它第二层后果。
- S3 可以让主角非常占便宜，不为平衡主动加对称代价；只保留真正防止故事直接失去冲突的一条根边界。
- 极端仍必须一句话听懂，优先身体、空间、战斗、移动、吞噬、占有、变形、生存、召唤、死亡等直接动作，不用抽象哲学词冒充大胆。
- 仍必须严格 Authority-compilable；不允许先写一个酷画面再靠 Trace 替它补不存在的门、载体、见证者、等级或 trigger。

不要在输出外解释本 Treatment。"""

MUTATION_PROMPT = r"""你是 Matched Premise Mutation Lab。下面给你一张已经生成的完整 Premise Card。你的任务不是再想五个新题材，而是把**同一个 premise DNA**沿创意电压做五档连续突变，让作者能直接判断 aggressive sweet spot。

硬约束：
- M0—M4 必须保持同一个核心世界异常、同一个 Protagonist Ontology 家族、同一个核心 Privilege 因果和同一个商业类型锚点；不能每档换主角、换世界或新增另一套独立系统。
- 变化只能来自：特权幅度、身体/空间/社会后果、Changed Verbs 丰富度、第一章兑现强度、长期复合深度与“一个默认假设被砸碎到什么程度”。
- M0 是明显更保守但仍值得卖的版本；M1 是商业强版；M2 明显 aggressive；M3 extreme；M4 overdrive，允许作者最后判断它确实过头。
- 不许因为 M3/M4 更强就自动加等价反噬、寿命、冷却、道德惩罚来平账；只有母 premise 的根边界必须继续成立。
- 任何一档都必须一句话可懂；更极端不等于新名词更多。
- 每档必须给 4—7 个具体 Changed Verbs，并写一幅第一章画面与一次第一章不公平兑现。
- 明确写“相对上一档究竟升级了哪一件事”，禁止用“更大胆、更极端”空话。

严格输出：
# MATCHED MUTATION LADDER
## M0｜保守可卖
### 一句话货架简介
### 核心 Ontology / Privilege（保持同 DNA）
### Changed Verbs
### 第一章标志性画面
### 第一次不公平兑现
### 20章玩法
### 100章以上变异
### 相对上一档的唯一升级
## M1｜商业强版
（同结构）
## M2｜AGGRESSIVE
（同结构）
## M3｜EXTREME
（同结构）
## M4｜OVERDRIVE
（同结构；允许真实过头）

# 母 Premise Card
{CARD}
"""


def dump(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def run_acp(prompt_path: Path, out_json: Path, out_md: Path, *, model: str, effort: str, label: str) -> dict:
    started = time.time()
    cmd = ["node", str(RUNNER), str(prompt_path), str(out_json), model, effort, label]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f"ACP {label} failed: {proc.stderr[-4000:]}\n{proc.stdout[-4000:]}")
    data = json.loads(out_json.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"ACP {label} failed: {data.get('error')}")
    text = str(data.get("text", "")).strip()
    if not text:
        raise RuntimeError(f"ACP {label}: empty response")
    out_md.write_text(text + "\n", encoding="utf-8")
    print(json.dumps({"label": label, "wall": round(time.time()-started, 2), "agent_wall": data.get("wall_seconds"), "chars": len(text)}, ensure_ascii=False), flush=True)
    return data


def selected_verdict(report: str) -> str:
    m = re.search(r"(?mi)^-?\s*Verdict\s*:\s*(PASS|CONDITIONAL PASS|FAIL)\s*$", report)
    if not m:
        m = re.search(r"(?mi)^Verdict\s*:\s*(PASS|CONDITIONAL PASS|FAIL)\s*$", report)
    if not m:
        raise RuntimeError("selected compiler report missing Verdict")
    return m.group(1).upper()


def main() -> None:
    author = (EXP / "AUTHOR_DIRECTION.md").read_text(encoding="utf-8")
    prereg = {
        "e7_selected_candidate": "S3",
        "selection_registered_before_forge": True,
        "e7_continue_only_on": "PASS",
        "power_candidate_if_downstream": 2,
        "human_candidate_if_downstream": 2,
        "mutation_source": "same generated S3",
        "no_candidate_substitution": True,
    }
    dump(EXP / "PRE_REGISTERED_SELECTION.json", prereg)

    forge_prompt = build_single_pass_prompt(author_direction=author + "\n\n" + EXTREME_TREATMENT)
    (EXP / "EXTREME_FORGE_PROMPT.md").write_text(forge_prompt, encoding="utf-8")
    run_acp(EXP / "EXTREME_FORGE_PROMPT.md", EXP / "EXTREME_FORGE_ACP.json", EXP / "EXTREME_FORGE_RESPONSE.md", model="gpt-5.6-luna", effort="high", label="premise-extreme-e7-forge")
    forge = (EXP / "EXTREME_FORGE_RESPONSE.md").read_text(encoding="utf-8")
    sections = extract_sections(forge, prefix="S")
    if tuple(sections) != ("S1", "S2", "S3"):
        raise RuntimeError(f"expected S1/S2/S3, got {tuple(sections)}")
    selected = sections["S3"]
    (EXP / "SELECTED_S3.md").write_text(selected + "\n", encoding="utf-8")

    compiler_prompt = build_selected_premise_compiler_prompt(candidate=selected)
    (EXP / "SELECTED_S3_COMPILER_PROMPT.md").write_text(compiler_prompt, encoding="utf-8")
    run_acp(EXP / "SELECTED_S3_COMPILER_PROMPT.md", EXP / "SELECTED_S3_COMPILER_ACP.json", EXP / "SELECTED_S3_COMPILER_REPORT.md", model="gpt-5.6-terra", effort="high", label="premise-extreme-e7-compiler")
    report = (EXP / "SELECTED_S3_COMPILER_REPORT.md").read_text(encoding="utf-8")
    verdict = selected_verdict(report)

    mutation = MUTATION_PROMPT.replace("{CARD}", selected.strip())
    (EXP / "MUTATION_LADDER_PROMPT.md").write_text(mutation, encoding="utf-8")
    run_acp(EXP / "MUTATION_LADDER_PROMPT.md", EXP / "MUTATION_LADDER_ACP.json", EXP / "MUTATION_LADDER.md", model="gpt-5.6-luna", effort="high", label="premise-e1-mutation-ladder")

    dump(EXP / "PHASE1_SUMMARY.json", {
        "selected": "S3",
        "compiler_verdict": verdict,
        "downstream_authorized": verdict == "PASS",
        "mutation_ladder_generated": True,
        "production_modified": False,
    })
    print(f"COMPILER_VERDICT={verdict}", flush=True)


if __name__ == "__main__":
    main()

