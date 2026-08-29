from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
SOURCE = BOOK / "runs"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "dual-medium-curator"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.hybrid_runtime import (  # noqa: E402
    extract_unresolved_fact_boundary,
    strip_legacy_prose_controls,
)
from story_mvp.scene_skills import (  # noqa: E402
    render_selected_revision_watches,
    strip_scene_skill_selection,
)

AUTHORITY_CURATOR_TEMPLATE = """你是 TGN 的 Authority Boundary Curator，使用 GPT-5.6 Luna medium。你只负责本章事实边界与全章闭合，不负责文风、人物魅力或重新规划。

Frozen Mission 的行动者、对象、事件、直接结果、状态变化与 Ending 不得改写、弱化或提前；Reader Release 逐条保留；Canon/World/Power/Human 中未知、未批准的内容仍未知。不要补造数字、时间、制度、支付方式、到场人物、能力规则或过去事实。

严格只输出：
# Authority Curator
## Curator Audit
最多4条明确冲突/未知；没有写“无”。
## Relevant World Rules
最多8条；Reader Release 优先逐条保留。
## Relevant Open Promises
最多8条，区分本章必须兑现与仍未兑现。
## Already Established — Do Not Re-explain
最多8条。
## Global Closure Watch
最多10条：持有人、时间窗口、数字/档位、Named Entity、能力条件、资源/关系状态与 Ending。

不输出 Relevant Plan，不写正文，不给表达建议，不输出思考。"""

STORY_CURATOR_TEMPLATE = """你是 TGN 的 Male-Fantasy Story Curator，使用 GPT-5.6 Luna medium。你只负责把已经批准的 Mission / Human / Book / Prose / Canon 编译成更接近顶级中文男频长篇的注意力与场面价值；不负责改变事实、补世界或决定事件结果。

优先保护：主角主动性与具体欲望；人物关系与声音；核心幻想/器物/能力最值得馋的体验；具体获得、损失、身份与社会重新定价；Public Proof 需要时群体震动、懂行尺度、关键人物行为变化；真实章末动作。Supporting Logic、登记、报告、路线、协调与重复证明只在真实出现时压缩。

严格只输出：
# Story Curator
## Relevant Book Contract
最多6条。
## Relevant Characters and Relationships
最多8条，写可进入场景的欲望/关系/声音。
## Scene Prose Projection
已经清楚写 NONE；否则2—4句，不新增事件。
## Opening Strategy
2—4句。
## Scene Skill Selection
Primary: <skill_id 或 none>
Secondary: <skill_id 或 none>
## Relevant Inspiration
无相关内容写“无”。
## Reader-Facing Language
2—6条。
## Recent Repetition Risks
最多6条。
## Payoff and Promise Window
明确已拿到/本章必须落地/仍未兑现；最多8条。

不输出 Relevant Plan、World Rules 或事实 Audit，不写正文，不输出思考。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


def call(prompt_path: Path, output_path: Path) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-luna", "medium", str(ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        if process.returncode == 0 and output_path.exists():
            try:
                data = json.loads(output_path.read_text(encoding="utf-8"))
            except Exception as error:
                data = {}
                last = str(error)
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (process.stderr + "\n" + process.stdout)[-3000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(last)


def exact_block(prompt: str, start: str, end: str | None) -> str:
    begin = prompt.index(start) + len(start)
    finish = prompt.index(end, begin) if end else len(prompt)
    return prompt[begin:finish].strip()


def h2_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"(?ms)^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|^#\s+|\Z)")
    match = pattern.search(text)
    if not match:
        raise ValueError(f"missing section: {heading}")
    return match.group(1).strip()


def inputs(chapter: int) -> tuple[str, str, str, str]:
    source = SOURCE / f"chapter-{chapter:04d}"
    prompt = (source / "curator_prompt.md").read_text(encoding="utf-8")
    authority = exact_block(prompt, "## AUTHORITY", "## 当前章事件合同")
    mission = exact_block(prompt, "## 当前章事件合同", "## CONTEXT INDEX——只含可见结构入口，不含被省略正文")
    release = exact_block(prompt, "## READER RELEASE——Outline 排程的本章世界事实", "## WORLD AUTHORITY——本章确定性预取")
    world = exact_block(prompt, "## WORLD AUTHORITY——本章确定性预取", "## FROZEN HUMAN CORE——稳定人格权威，只用于本章相关选择与私人牵引")
    human = exact_block(prompt, "## FROZEN HUMAN CORE——稳定人格权威，只用于本章相关选择与私人牵引", "## 压缩 Growth Genome（本章相关固定小节）")
    book = exact_block(prompt, "## BOOK CONTRACT——本章确定性预取", "## 本章成长收益短投影（规划提示，不是正文措辞）")
    canon = exact_block(prompt, "## CANON INDEX——本章确定性预取", "## 当前大型剧情块与十章计划")
    prose = exact_block(prompt, "## PROSE PROFILE", "## SCENE SKILL CATALOG——只用于选择 1 个 Primary 与可选 1 个 Secondary")
    catalog = exact_block(prompt, "## SCENE SKILL CATALOG——只用于选择 1 个 Primary 与可选 1 个 Secondary", "## OPTIONAL INSPIRATION")
    tail = exact_block(prompt, "## 前文章末局部衔接片段", None)
    authority_input = "\n\n".join((
        "# AUTHORITY\n" + authority,
        "# FROZEN MISSION\n" + mission,
        "# READER RELEASE\n" + (release or "（无）"),
        "# WORLD\n" + world,
        "# CANON\n" + canon,
        "# HUMAN\n" + human,
        "# PREVIOUS TAIL\n" + tail[-1800:],
    ))
    story_input = "\n\n".join((
        "# FROZEN MISSION\n" + mission,
        "# HUMAN\n" + human,
        "# BOOK\n" + book,
        "# CANON\n" + canon,
        "# PROSE\n" + prose,
        "# SCENE SKILL CATALOG\n" + catalog,
        "# READER RELEASE\n" + (release or "（无）"),
        "# PREVIOUS TAIL\n" + tail[-1800:],
    ))
    return authority_input, story_input, mission, prompt


def merge(authority_response: str, story_response: str, mission: str) -> str:
    a = {heading: h2_section(authority_response, heading) for heading in (
        "Curator Audit", "Relevant World Rules", "Relevant Open Promises",
        "Already Established — Do Not Re-explain", "Global Closure Watch",
    )}
    s = {heading: h2_section(story_response, heading) for heading in (
        "Relevant Book Contract", "Relevant Characters and Relationships",
        "Scene Prose Projection", "Opening Strategy", "Scene Skill Selection",
        "Relevant Inspiration", "Reader-Facing Language", "Recent Repetition Risks",
        "Payoff and Promise Window",
    )}
    audit = a["Curator Audit"]
    if a["Global Closure Watch"] and a["Global Closure Watch"] != "无":
        audit = audit + "\n\nGlobal Closure Watch：\n" + a["Global Closure Watch"]
    sections = [
        ("Relevant Book Contract", s["Relevant Book Contract"]),
        ("Relevant Characters and Relationships", s["Relevant Characters and Relationships"]),
        ("Relevant World Rules", a["Relevant World Rules"]),
        ("Relevant Open Promises", a["Relevant Open Promises"]),
        ("Relevant Plan", mission),
        ("Scene Prose Projection", s["Scene Prose Projection"]),
        ("Opening Strategy", s["Opening Strategy"]),
        ("Scene Skill Selection", s["Scene Skill Selection"]),
        ("Relevant Inspiration", s["Relevant Inspiration"]),
        ("Reader-Facing Language", s["Reader-Facing Language"]),
        ("Already Established — Do Not Re-explain", a["Already Established — Do Not Re-explain"]),
        ("Recent Repetition Risks", s["Recent Repetition Risks"]),
        ("Payoff and Promise Window", s["Payoff and Promise Window"]),
    ]
    return "# Curator Audit\n\n" + audit + "\n\n# Curated Chapter Context\n\n" + "\n\n".join(
        f"## {heading}\n\n{value}" for heading, value in sections
    )


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)


def replace_revision_watch(prompt: str, old_curator: str, new_curator: str) -> str:
    old_watch = render_selected_revision_watches(old_curator)
    new_watch = render_selected_revision_watches(new_curator)
    heading = "## ACTIVE SCENE REVISION WATCH｜只在明确失败时局部使用"
    primary_heading = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    if old_watch:
        block = f"{heading}\n\n{old_watch}"
        if block not in prompt:
            raise RuntimeError("old revision watch block missing")
        if new_watch:
            return prompt.replace(block, f"{heading}\n\n{new_watch}", 1)
        return prompt.replace(block + "\n\n", "", 1)
    if new_watch:
        return prompt.replace(primary_heading, f"{heading}\n\n{new_watch}\n\n{primary_heading}", 1)
    return prompt


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    authority_input, story_input, mission, _ = inputs(chapter)
    auth_prompt = AUTHORITY_CURATOR_TEMPLATE + "\n\n" + authority_input
    story_prompt = STORY_CURATOR_TEMPLATE + "\n\n" + story_input
    auth_prompt_path = directory / "authority_curator_prompt.md"
    story_prompt_path = directory / "story_curator_prompt.md"
    auth_prompt_path.write_text(auth_prompt, encoding="utf-8")
    story_prompt_path.write_text(story_prompt, encoding="utf-8")
    with ThreadPoolExecutor(max_workers=2) as executor:
        auth_future = executor.submit(call, auth_prompt_path, directory / "authority_curator_acp.json")
        story_future = executor.submit(call, story_prompt_path, directory / "story_curator_acp.json")
        auth_data = auth_future.result()
        story_data = story_future.result()
    auth_response = clean(auth_data.get("text", ""))
    story_response = clean(story_data.get("text", ""))
    merged = merge(auth_response, story_response, mission)
    (directory / "authority_curator_response.md").write_text(auth_response + "\n", encoding="utf-8")
    (directory / "story_curator_response.md").write_text(story_response + "\n", encoding="utf-8")
    (directory / "merged_curator_response.md").write_text(merged + "\n", encoding="utf-8")

    old_curator = clean((source / "curator_response.md").read_text(encoding="utf-8"))
    old_visible = strip_legacy_prose_controls(strip_scene_skill_selection(old_curator))
    new_visible = strip_legacy_prose_controls(strip_scene_skill_selection(merged))
    old_unresolved = extract_unresolved_fact_boundary(old_curator)
    new_unresolved = extract_unresolved_fact_boundary(merged)
    primary_prompt = (source / "primary_prompt.md").read_text(encoding="utf-8")
    primary_prompt = replace_once(primary_prompt, old_visible, new_visible, f"ch{chapter} curator")
    if old_unresolved != new_unresolved:
        primary_prompt = replace_once(
            primary_prompt,
            old_unresolved or "（Curator 未投影出额外未解事实；仍服从最高事实边界。）",
            new_unresolved or "（Curator 未投影出额外未解事实；仍服从最高事实边界。）",
            f"ch{chapter} unresolved",
        )
    primary_path = directory / "primary_prompt.md"
    primary_path.write_text(primary_prompt, encoding="utf-8")
    primary_data = call(primary_path, directory / "primary_acp.json") if False else None
    # Primary and Reviser use their production models, not the medium curator caller.
    def call_model(prompt_path: Path, output_path: Path, model: str, effort: str) -> dict:
        last = ""
        for attempt in range(3):
            process = subprocess.run(
                ["node", str(RUNNER), str(prompt_path), str(output_path), model, effort, str(ROOT)],
                cwd=ROOT, text=True, capture_output=True, encoding="utf-8", errors="replace",
            )
            if process.returncode == 0 and output_path.exists():
                data = json.loads(output_path.read_text(encoding="utf-8"))
                if data.get("ok"):
                    return data
                last = str(data.get("error", ""))
            else:
                last = (process.stderr + "\n" + process.stdout)[-3000:]
            time.sleep(2 + attempt * 2)
        raise RuntimeError(last)
    primary_data = call_model(primary_path, directory / "primary_acp.json", "gpt-5.6-terra", "high")
    primary_text = clean(primary_data.get("text", "")); primary_body = body(primary_text)
    (directory / "primary_response.md").write_text(primary_text + "\n", encoding="utf-8")
    (directory / "primary_body.md").write_text(primary_body + "\n", encoding="utf-8")

    old_primary = body((source / "primary_response.md").read_text(encoding="utf-8"))
    reviser_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    reviser_prompt = replace_once(reviser_prompt, old_curator, merged, f"ch{chapter} reviser curator")
    reviser_prompt = replace_once(reviser_prompt, old_primary, primary_body, f"ch{chapter} reviser primary")
    reviser_prompt = replace_revision_watch(reviser_prompt, old_curator, merged)
    reviser_path = directory / "reviser_prompt.md"; reviser_path.write_text(reviser_prompt, encoding="utf-8")
    reviser_data = call_model(reviser_path, directory / "reviser_acp.json", "gpt-5.6-luna", "high")
    reviser_text = clean(reviser_data.get("text", "")); final_body = body(reviser_text)
    (directory / "reviser_response.md").write_text(reviser_text + "\n", encoding="utf-8")
    (directory / "final_body.md").write_text(final_body + "\n", encoding="utf-8")

    control = {stage: json.loads((source / f"{stage}_acp.json").read_text(encoding="utf-8")) for stage in ("curator", "primary", "authority_reviser")}
    curator_critical = max(float(auth_data.get("wall_seconds") or 0), float(story_data.get("wall_seconds") or 0))
    treatment = curator_critical + float(primary_data.get("wall_seconds") or 0) + float(reviser_data.get("wall_seconds") or 0)
    control_total = sum(float(control[stage].get("wall_seconds") or 0) for stage in control)
    return {
        "chapter": chapter,
        "authority_curator_seconds": auth_data.get("wall_seconds"),
        "story_curator_seconds": story_data.get("wall_seconds"),
        "curator_parallel_critical_seconds": round(curator_critical, 3),
        "primary_seconds": primary_data.get("wall_seconds"),
        "reviser_seconds": reviser_data.get("wall_seconds"),
        "control_c_p_r_seconds": round(control_total, 3),
        "treatment_c_p_r_seconds": round(treatment, 3),
        "speedup_percent": round((1 - treatment / control_total) * 100, 2),
        "merged_curator_chars": len(merged),
        "final_chars": len(final_body),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    # Each chapter already launches two parallel curator calls; keep chapter workers at 3
    # to avoid turning queue contention into a false latency result.
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result(); rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
