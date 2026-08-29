from __future__ import annotations

import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
OUT = (
    ROOT
    / "books"
    / "real-exp-chapter-latency-optimization-20260829-v1"
    / "phase-1b-safe-patch-reviser"
)
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 5, 12, 15)
ROUTE_REASONS = {
    2: "exploration continuation; no Reader Release, milestone, acquisition or Public Proof",
    5: "choice/conflict chapter; no new power tier, public ruler or completed acquisition",
    12: "chase/transport continuation; existing power boundary only, no milestone or Reader Release",
    15: "strategic choice chapter; no new power, public proof or completed high-value acquisition",
}

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.hybrid_runtime import (  # noqa: E402
    _extract_level_one_section,
    _extract_subsection,
    _project_indexed_text,
    _project_relevant_world_authority,
    extract_primary_draft,
)


PATCH_TEMPLATE = """你是 TGN 的 Routine Patch Reviser。你不重写整章，不输出完整正文；只对明确失败做最小补丁。

优先级：冻结 Mission / Canon / World / Power / Human > Curator > Primary Draft。没有明确失败时必须输出 `NO_CHANGE`。不要为了更顺、更美或更有文采改写正确句段。

Routine Patch 只允许处理：重复证明、无新选择的程序化实施、后台抽象语言，且局部替换前后不得改变事实范围。

下列问题即使明确存在，也不要局部修，必须返回 `ESCALATE_HIGH`：冻结事件、结果、状态变化或 Ending 漏失；Reader Release / 公开档位漏项；Power / Canon / Named Entity / 未知边界错误；Frozen Human cue 漏失；ownership / transfer、时间窗口、数字、角色称谓、力量边界、资源得失或关系结果需要变化。

禁止：改变事件顺序、人物决定、胜负、资源得失、伤势、关系结果、未知事实；禁止新增世界设定、价格、等级、过去史；禁止把一句局部问题扩成全章润色。

严格只用三种返回之一：

NO_CHANGE

或：

ESCALATE_HIGH: <一句说明敏感问题>

或：

# PATCH SET
## PATCH 1
OLD:
<从 Primary Draft 逐字复制的一段连续原文；必须唯一出现>
NEW:
<完整替换文本；可以为空表示删除>
REASON:
<一句指出具体权威失败>

最多 3 个 Patch。OLD 通常 1—4 句；不得用省略号或改写后的近似锚点。不要输出思考、Audit、完整正文或其它标题。
"""


def clean(text: str) -> str:
    return re.sub(
        r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text
    ).strip()


def exact_top_block(prompt: str, start: str, end: str | None) -> str:
    start_index = prompt.index(start) + len(start)
    end_index = prompt.index(end, start_index) if end else len(prompt)
    return prompt[start_index:end_index].strip()


def compact_curator(curator: str) -> str:
    blocks: list[str] = []
    audit = _extract_level_one_section(curator, "# Curator Audit")
    if audit:
        blocks.append("## Curator Audit\n" + audit)
    for heading in (
        "## Relevant Characters and Relationships",
        "## Relevant World Rules",
        "## Relevant Open Promises",
        "## Relevant Plan",
        "## Scene Prose Projection",
        "## Reader-Facing Language",
        "## Already Established — Do Not Re-explain",
        "## Recent Repetition Risks",
        "## Payoff and Promise Window",
    ):
        body = _extract_subsection(curator, heading)
        if body and body != "无":
            blocks.append(f"{heading}\n{body}")
    return "\n\n".join(blocks)


def build_patch_prompt(chapter: int) -> tuple[str, str, str]:
    run = SOURCE / f"chapter-{chapter:04d}"
    full = (run / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    mission = exact_top_block(
        full,
        "## FROZEN CHAPTER MISSION｜不得改剧情",
        "## CURATOR｜本章近端注意力与实现要求",
    )
    curator = exact_top_block(
        full,
        "## CURATOR｜本章近端注意力与实现要求",
        "## WORLD REALITY AUTHORITY｜远端安全世界事实",
    )
    world = exact_top_block(
        full,
        "## WORLD REALITY AUTHORITY｜远端安全世界事实",
        "## READER RELEASE｜本章已批准首次释放事实；逐条核对",
    )
    reader_release = exact_top_block(
        full,
        "## READER RELEASE｜本章已批准首次释放事实；逐条核对",
        "## POWER CORE｜Frozen Authority",
    )
    power = exact_top_block(
        full,
        "## POWER CORE｜Frozen Authority",
        "## HUMAN CORE｜Frozen Authority",
    )
    human = exact_top_block(
        full,
        "## HUMAN CORE｜Frozen Authority",
        "## CANON INDEX｜已发生事实压缩索引",
    )
    canon = exact_top_block(
        full,
        "## CANON INDEX｜已发生事实压缩索引",
        "## CANON TAIL｜上一章必要衔接",
    )
    tail_end = (
        "## ACTIVE SCENE REVISION WATCH｜只在明确失败时局部使用"
        if "## ACTIVE SCENE REVISION WATCH｜只在明确失败时局部使用" in full
        else "## PRIMARY DRAFT｜唯一待修订正文底稿"
    )
    tail = exact_top_block(
        full,
        "## CANON TAIL｜上一章必要衔接",
        tail_end,
    )
    primary = extract_primary_draft(
        clean((run / "primary_response.md").read_text(encoding="utf-8"))
    ).strip()
    compact_attention = compact_curator(curator)
    query = "\n\n".join((mission, compact_attention, reader_release))
    world_projected = _project_relevant_world_authority(world, query, max_chars=2200)
    power_projected = _project_indexed_text(power, query, max_chars=1800)
    human_projected = _project_indexed_text(human, query, max_chars=1800)
    canon_projected = _project_indexed_text(canon, query, max_chars=2600)
    prompt = "\n\n".join(
        (
            PATCH_TEMPLATE,
            "# FROZEN MISSION\n" + mission,
            "# EXPLICIT READER RELEASE CHECKLIST\n"
            + (reader_release or "（本章无 Reader Release。）"),
            "# CURATOR ATTENTION\n" + compact_attention,
            "# RELEVANT WORLD AUTHORITY\n"
            + (world_projected or "（无额外 World fact。）"),
            "# RELEVANT POWER AUTHORITY\n" + power_projected,
            "# RELEVANT HUMAN AUTHORITY\n" + human_projected,
            "# CANON INDEX\n" + canon_projected,
            "# CANON TAIL\n" + tail[-1400:],
            "# PRIMARY DRAFT\n" + primary,
        )
    )
    return prompt, primary, full


_PATCH_PATTERN = re.compile(
    r"(?ms)^## PATCH\s+\d+\s*$\nOLD:\s*\n(?P<old>.*?)\nNEW:\s*\n(?P<new>.*?)\nREASON:\s*\n(?P<reason>.*?)(?=^## PATCH\s+\d+\s*$|\Z)"
)

_SENSITIVE_TERMS = (
    "归", "交给", "交回", "交付", "收下", "推回", "拿走", "持有",
    "所有权", "使用权", "原件", "副本", "登记", "签下", "到账",
    "付款", "尾款", "赔付", "潮铢", "低潮", "地潮", "下一次",
    "之前", "之后", "当场", "已经", "尚未", "仍未", "开始", "即将",
    "入潮", "成炉", "照域", "镇海", "分身", "回潮楔", "锁潮",
    "改向", "释放", "行潮籍", "不能", "不得", "必须", "只能",
    "不再", "仍能",
)


def validate_safe_patch(old: str, new: str) -> None:
    """Reject local edits that can change fact scope or need a whole-chapter sweep."""

    combined = old + "\n" + new
    touched = [term for term in _SENSITIVE_TERMS if term in combined]
    if touched:
        raise ValueError("sensitive patch terms=" + ",".join(touched[:8]))
    if re.search(r"\d", combined):
        raise ValueError("patch touches numeric fact")
    if len(new) > len(old) * 1.5 + 60:
        raise ValueError("patch expands local text too much")
    if old.count("\n\n") > 3 or new.count("\n\n") > 3:
        raise ValueError("patch spans too many paragraphs")


def parse_and_apply(response: str, primary: str) -> tuple[str, list[dict], str]:
    text = clean(response)
    if text == "NO_CHANGE":
        return primary, [], "no_change"
    if text.startswith("ESCALATE_HIGH:"):
        raise ValueError(
            "model requested high escalation: " + text.split(":", 1)[1].strip()
        )
    if not text.startswith("# PATCH SET"):
        raise ValueError(
            "response is neither NO_CHANGE, ESCALATE_HIGH nor # PATCH SET"
        )
    patches = []
    result = primary
    for match in _PATCH_PATTERN.finditer(text):
        old = match.group("old").strip()
        new = match.group("new").strip()
        reason = match.group("reason").strip()
        if not old or "..." in old or "……" in old:
            raise ValueError("patch OLD must be a non-empty exact anchor without ellipsis")
        occurrences = result.count(old)
        if occurrences != 1:
            raise ValueError(f"patch OLD occurrence count={occurrences}")
        if "# 正式正文" in new or "# PATCH" in new:
            raise ValueError("patch NEW contains pipeline heading")
        validate_safe_patch(old, new)
        result = result.replace(old, new, 1)
        patches.append(
            {
                "old": old,
                "new": new,
                "reason": reason,
                "old_chars": len(old),
                "new_chars": len(new),
            }
        )
    if not patches or len(patches) > 3:
        raise ValueError(f"invalid patch count={len(patches)}")
    if sum(max(len(item["old"]), len(item["new"])) for item in patches) > len(primary) * 0.18:
        raise ValueError("patch set touches too much of chapter")
    if len(result) < 1500:
        raise ValueError(f"patched body too short: {len(result)}")
    return result.strip(), patches, "patched"


def run_one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    prompt, primary, full_prompt = build_patch_prompt(chapter)
    prompt_path = directory / "patch_reviser_prompt.md"
    acp_path = directory / "patch_reviser_medium_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    process = subprocess.run(
        [
            "node",
            str(RUNNER),
            str(prompt_path),
            str(acp_path),
            "gpt-5.6-luna",
            "medium",
            str(ROOT),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if process.returncode:
        raise RuntimeError(process.stderr[-3000:])
    data = json.loads(acp_path.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(str(data.get("error")))
    response = clean(data.get("text", ""))
    (directory / "patch_reviser_response.md").write_text(
        response + "\n", encoding="utf-8"
    )
    fallback_reason = ""
    try:
        final, patches, disposition = parse_and_apply(response, primary)
        fallback = False
    except ValueError as error:
        # Production candidate would fail closed to the existing Luna-high full Reviser.
        source = SOURCE / f"chapter-{chapter:04d}" / "authority_reviser_response.md"
        final = extract_primary_draft(clean(source.read_text(encoding="utf-8"))).strip()
        patches = []
        disposition = "fallback_high"
        fallback = True
        fallback_reason = str(error)
    (directory / "final_patch_body.md").write_text(final + "\n", encoding="utf-8")
    high_data = json.loads(
        (
            SOURCE
            / f"chapter-{chapter:04d}"
            / "authority_reviser_acp.json"
        ).read_text(encoding="utf-8")
    )
    high_body = extract_primary_draft(
        clean(
            (
                SOURCE
                / f"chapter-{chapter:04d}"
                / "authority_reviser_response.md"
            ).read_text(encoding="utf-8")
        )
    ).strip()
    usage = data.get("result", {}).get("usage", {}) or {}
    patch_wall = float(data.get("wall_seconds") or 0)
    high_wall = float(high_data.get("wall_seconds") or 0)
    routed_wall = patch_wall + (high_wall if fallback else 0.0)
    return {
        "chapter": chapter,
        "predeclared_route_reason": ROUTE_REASONS[chapter],
        "prompt_chars": len(prompt),
        "control_prompt_chars": len(full_prompt),
        "prompt_reduction_percent": round((1 - len(prompt) / len(full_prompt)) * 100, 2),
        "patch_wall_seconds": patch_wall,
        "control_high_wall_seconds": high_wall,
        "routed_wall_seconds": round(routed_wall, 3),
        "patch_only_speedup_percent": round(
            (1 - patch_wall / float(high_wall or 1)) * 100,
            2,
        ),
        "routed_speedup_percent": round(
            (1 - routed_wall / float(high_wall or 1)) * 100,
            2,
        ),
        "output_tokens": usage.get("outputTokens", 0),
        "thought_tokens": usage.get("thoughtTokens", 0),
        "response_chars": len(response),
        "disposition": disposition,
        "fallback": fallback,
        "fallback_reason": fallback_reason,
        "patch_count": len(patches),
        "patches": patches,
        "primary_chars": len(primary),
        "final_chars": len(final),
        "similarity_to_primary": round(SequenceMatcher(None, primary, final).ratio(), 5),
        "similarity_to_high": round(SequenceMatcher(None, high_body, final).ratio(), 5),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as executor:
        futures = [executor.submit(run_one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
