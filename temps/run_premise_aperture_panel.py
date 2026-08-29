from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
import json
import random
import re
import subprocess


ROOT = Path(r"C:\dev\tgn-story-mvp")
EXP = ROOT / "books" / "real-exp-premise-aperture-20260829-v1"
RUNNER = ROOT / "temps" / "acp_readonly_runner.mjs"


@dataclass(frozen=True)
class Case:
    case_id: str
    display: str


CASES = (
    Case("generic_fantasy", "通用玄幻成长"),
    Case("fast_multiworld", "20章一世界快节奏长篇"),
    Case("game_instance", "游戏副本／无限流"),
)

IDS = ("B0", "S1", "S2", "S3", "C1", "C2", "C3")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def run_one(
    prompt_path: Path,
    out_json: Path,
    response_path: Path,
    *,
    label: str,
    model: str,
    effort: str = "high",
) -> dict[str, object]:
    cp = subprocess.run(
        ["node", str(RUNNER), str(prompt_path), str(out_json), model, effort, label],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if cp.returncode:
        raise RuntimeError(f"{label}: {cp.stderr[-2500:]}")
    data = json.loads(out_json.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"{label}: {data.get('error')}")
    text = clean(str(data.get("text", "")))
    response_path.write_text(text + "\n", encoding="utf-8")
    return {
        "label": label,
        "model": model,
        "effort": effort,
        "wall_seconds": data.get("wall_seconds"),
        "chars": len(text),
    }


def extraction_prompt(case: Case) -> str:
    case_dir = EXP / case.case_id
    baseline = read(case_dir / "CURRENT_BASELINE_PACKAGE.md")
    single = read(case_dir / "single_pass" / "response.md")
    collision = read(case_dir / "orthogonal" / "collision" / "response.md")
    return f"""你是事实压缩员，不是创意作者、评审或改稿者。把下列三种来源压成七张完全同构的“小说前提卡”，供之后盲评。

绝对规则：
- 不评价、不排名、不修补、不替任何方案增加更好的桥梁。
- 只能使用来源中明确存在的事实；缺失就写“未明确”。
- 不因来源篇幅长而写得更多。每张卡 430—650 个中文字符，字段完全相同。
- B0 是现有 production 已选中的完整 World / Power / Human / Story 方案，只压成一张卡。
- S1/S2/S3 与 C1/C2/C3 各自保持原候选边界。
- 卡内不要再次提到 B0/S1/C1 等来源代号，也不要说“基线”“单代理”“正交”。
- “大胆”不等于猎奇；你只做事实提取。

严格格式，不要前言：
# STANDARDIZED PREMISE CARDS｜{case.display}
## B0
### 一句话货架简介
### 主角开局存在形态
### 世界眼前高压事实
### 直接不公平特权
### 第一章标志性画面
### 反复改变玩法的新动作
### 首次兑现与他人反应
### 20章换挡与百章长线
### 最小边界与主要风险
## S1
（同字段）
## S2
（同字段）
## S3
（同字段）
## C1
（同字段）
## C2
（同字段）
## C3
（同字段）

# SOURCE A｜CURRENT PRODUCTION PACKAGE
{baseline}

# SOURCE B｜THREE SINGLE-PASS CANDIDATES
{single}

# SOURCE C｜THREE FIXED-COLLISION CANDIDATES
{collision}
"""


def parse_cards(text: str) -> dict[str, str]:
    pattern = re.compile(r"(?m)^## (B0|S1|S2|S3|C1|C2|C3)\s*$")
    matches = list(pattern.finditer(text))
    cards: dict[str, str] = {}
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        cards[match.group(1)] = text[match.end() : end].strip()
    missing = [source_id for source_id in IDS if source_id not in cards]
    if missing:
        raise RuntimeError(f"standardizer missing cards: {missing}")
    return cards


def anonymize(case: Case, cards: dict[str, str]) -> tuple[str, dict[str, str]]:
    labels = list("ABCDEFG")
    rng = random.Random(20260829 + sum(ord(ch) for ch in case.case_id))
    source_ids = list(IDS)
    rng.shuffle(source_ids)
    label_to_source = dict(zip(labels, source_ids, strict=True))
    blocks = [f"# CASE｜{case.display}"]
    for label in labels:
        blocks.extend(("", f"## 方案 {label}", cards[label_to_source[label]]))
    return "\n".join(blocks).strip() + "\n", label_to_source


COMMON_JUDGE = """你将看到三组匿名、同格式的中文男频长篇“前提卡”。来源未知，可能来自现有 production，也可能来自实验候选。

评价原则：
- 不奖励篇幅、术语数量、血腥、生理猎奇或“设定很多”。
- 真正的 Boldness 是：一个高风险押注，能一句话让人看见，并永久改变主角动作、欲望或社会位置。
- 高分方案应让读者很快知道“我为什么想点开、主角会反复做什么、第一次怎么不公平地赢、别人为什么会重新估价他”。
- 同时惩罚：四个同等响亮的 gimmick 抢主轴、世界与外挂像钥匙锁孔般过度预配、只靠换名词、需要长解释才成立、百章后只剩同一招放大。
- 非人主角可以高分，也可以低分；关键是可读、可欲、能持续，而不是仅仅奇怪。
- 每组独立评价，不跨题材强行比较。

每个方案都给出以下 0—10 分：
1. Click Desire：一句话/第一画面是否真想点开。
2. Boldness：是否跳出安全平均值而非换皮。
3. Clarity：读者是否迅速明白核心，而非认知负担。
4. Changed Verbs：是否让主角反复做出普通升级文没有的新动作。
5. Immediate Payoff：第一次不公平兑现是否具体、够爽。
6. Social Repricing：观众、敌人、关系是否因显露而真实改变。
7. Long-form Runway：20章换挡、100章后是否还有不同故事。
8. Coherence Without Overfit：能成立但没有把所有层统一成同一个意义。
9. Gimmick / Body-horror / Overload Risk：0最好，10最危险。
10. Overall：综合 0—100；不要机械平均，要符合你的角色判断。

严格输出：
# BLIND PANEL
## CASE｜题材名
### Score Table
| 方案 | Click | Bold | Clear | Verbs | Payoff | Social | Long | Indep | Risk | Overall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
（七行都必须有）
### Top 3
1. 方案X：一句最强理由；一句最大风险。
2. ...
3. ...
### Commercial Decision
- 最愿意直接试写前三章：方案X，因为……
- 最有野心但目前过载：方案Y，因为……
- 最安全却最可能被忘记：方案Z，因为……
（对三组 CASE 重复）
"""


ROLE_PROMPTS = {
    "commercial": """你是极其熟悉起点式男频商业阅读的主编。你的第一责任是判断读者在书城、简介和第一章是否会继续点，以及高概念能否快速兑现。你允许夸张、粗粝、荒诞和强爽感，不因“不够文学”降分；但绝不把认知负担、抽象机制或单纯恶心当创新。""",
    "cold_reader": """你是苛刻的冷启动男频读者兼反 AI 味编辑。你没有义务替作者解释设定。第一句话不清、动作不具体、四套机制同时争夺注意力，都会明显降分。你同样会惩罚安全、熟悉、像系统设计文档而不想读正文的方案。""",
    "longform": """你是顶级男频长篇架构师。你重视第一章电压，也重视五百章内是否能不断换故事姿态、关系与世界位置。你会识别“看起来很完整但世界、身体、能力、终局全是同一隐喻”的过度自洽，也会识别随机拼接而没有主轴；两者都扣分。""",
}


def judge_prompt(role: str, blind_package: str) -> str:
    return "\n\n".join((ROLE_PROMPTS[role].strip(), COMMON_JUDGE.strip(), blind_package.strip())) + "\n"


def main() -> None:
    panel_dir = EXP / "blind_panel"
    panel_dir.mkdir(exist_ok=True)
    run_meta: list[dict[str, object]] = []

    extraction_jobs: list[tuple[Path, Path, Path, str]] = []
    for case in CASES:
        d = panel_dir / case.case_id
        d.mkdir(exist_ok=True)
        prompt_path = d / "STANDARDIZE_PROMPT.md"
        prompt_path.write_text(extraction_prompt(case), encoding="utf-8")
        extraction_jobs.append(
            (
                prompt_path,
                d / "STANDARDIZE_ACP.json",
                d / "STANDARDIZED_CARDS.md",
                f"premise-panel-standardize-{case.case_id}",
            )
        )

    print("STANDARDIZE", len(extraction_jobs), flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(
                run_one,
                p,
                o,
                r,
                label=label,
                model="gpt-5.6-terra",
            ): label
            for p, o, r, label in extraction_jobs
        }
        for future in as_completed(futures):
            result = future.result()
            run_meta.append(result)
            print("DONE", result, flush=True)

    mappings: dict[str, dict[str, str]] = {}
    blind_blocks: list[str] = []
    for case in CASES:
        d = panel_dir / case.case_id
        cards = parse_cards(read(d / "STANDARDIZED_CARDS.md"))
        blind, mapping = anonymize(case, cards)
        (d / "BLIND_CARDS.md").write_text(blind, encoding="utf-8")
        mappings[case.case_id] = mapping
        blind_blocks.append(blind)
    blind_package = "\n\n".join(blind_blocks).strip() + "\n"
    (panel_dir / "BLIND_PACKAGE.md").write_text(blind_package, encoding="utf-8")
    (panel_dir / "ANON_MAPPING.json").write_text(
        json.dumps(mappings, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    judge_jobs: list[tuple[Path, Path, Path, str, str]] = []
    models = {
        "commercial": "gpt-5.6-luna",
        "cold_reader": "gpt-5.6-terra",
        "longform": "gpt-5.6-sol",
    }
    for role, model in models.items():
        d = panel_dir / role
        d.mkdir(exist_ok=True)
        prompt_path = d / "PROMPT.md"
        prompt_path.write_text(judge_prompt(role, blind_package), encoding="utf-8")
        judge_jobs.append(
            (
                prompt_path,
                d / "ACP.json",
                d / "REPORT.md",
                f"premise-panel-{role}",
                model,
            )
        )

    print("JUDGES", len(judge_jobs), flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(run_one, p, o, r, label=label, model=model): label
            for p, o, r, label, model in judge_jobs
        }
        for future in as_completed(futures):
            result = future.result()
            run_meta.append(result)
            print("DONE", result, flush=True)

    synthesis_prompt = f"""你是实验统计与架构审计员。下方给出匿名映射和三份独立盲评。请解盲并做事实综合，不重写创意、不替作者冻结 production。

三种来源：
- B0 = 当前 production 已选方案（每题材1个）
- S1/S2/S3 = 单代理 Premise Forge 候选池
- C1/C2/C3 = fresh-context 四轴 + 代码固定碰撞候选池

必须分别回答：
1. 每个题材里 B0 的分数区间与排名。
2. Single pool 与 Orthogonal pool 的 ceiling（各自最高候选）、floor（最低候选）、平均稳定性。
3. 预注册 S2 vs C2，不能用事后最好候选替代。
4. 哪种机制提升了 Click/Bold/Verbs/Payoff；哪种机制恶化了 Clear/Risk/Independence。
5. 三位评审意见不一致之处，不能强行平均掉。
6. 只给三档候选结论：值得冻结、值得保留为实验开关、应拒绝；每项都需证据。不得宣称已经进入 production。
7. 给出最少下一步验证：只做真正会改变冻结判断的测试，不建议无限加代理。

严格格式：
# PANEL SYNTHESIS
## Executive Verdict
## Per-Case De-blinded Results
### 通用玄幻成长
### 20章一世界快节奏长篇
### 游戏副本／无限流
## Generator-Level Findings
## Pre-registered S2 vs C2
## Reviewer Disagreement
## Freeze Candidates
### 值得冻结
### 只保留实验开关
### 应拒绝
## Minimal Next Validation

# ANON MAPPING
{json.dumps(mappings, ensure_ascii=False, indent=2)}

# COMMERCIAL REPORT
{read(panel_dir / 'commercial' / 'REPORT.md')}

# COLD READER REPORT
{read(panel_dir / 'cold_reader' / 'REPORT.md')}

# LONGFORM REPORT
{read(panel_dir / 'longform' / 'REPORT.md')}
"""
    synth_dir = panel_dir / "synthesis"
    synth_dir.mkdir(exist_ok=True)
    synth_prompt_path = synth_dir / "PROMPT.md"
    synth_prompt_path.write_text(synthesis_prompt, encoding="utf-8")
    result = run_one(
        synth_prompt_path,
        synth_dir / "ACP.json",
        synth_dir / "REPORT.md",
        label="premise-panel-synthesis",
        model="gpt-5.6-luna",
    )
    run_meta.append(result)
    print("DONE", result, flush=True)

    (panel_dir / "RUN_SUMMARY.json").write_text(
        json.dumps(run_meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
