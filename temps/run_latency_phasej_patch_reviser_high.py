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
    / "phase-j-patch-reviser-high"
)
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 13, 14, 16, 19)

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.hybrid_runtime import (  # noqa: E402
    _extract_level_one_section,
    _extract_subsection,
    _project_indexed_text,
    _project_relevant_world_authority,
    extract_primary_draft,
)


PATCH_TEMPLATE = """你是 TGN 的 High-Authority Patch Reviser。你不重写整章，不输出完整正文；只对明确失败做最小补丁。

优先级：冻结 Mission / Canon / World / Power / Human > Curator > Primary Draft。没有明确失败时必须输出 `NO_CHANGE`。不要为了更顺、更美或更有文采改写正确句段。

只允许修：
1. 冻结事件、结果、状态变化、Ending 的明确遗漏或冲突；
2. Reader Release / 公开档位的明确漏项；
3. Power / Canon / Named Entity / 未知边界的明确错误；
4. Frozen Human 已自然触发却被完全净化的一个短 cue；
5. 重复证明、程序化实施或后台抽象语言，可用一个局部替换压缩。

禁止：改变事件顺序、人物决定、胜负、资源得失、伤势、关系结果、未知事实；禁止新增世界设定、价格、等级、过去史；禁止把一句局部问题扩成全章润色。

严格只用两种返回之一：

NO_CHANGE

或：

# PATCH SET
## PATCH 1
OLD:
<从 Primary Draft 逐字复制的一段连续原文；必须唯一出现>
NEW:
<完整替换文本；可以为空表示删除>
REASON:
<一句指出具体权威失败>

最多 4 个 Patch。OLD 通常 1—4 句；不得用省略号或改写后的近似锚点。不要输出思考、Audit、完整正文或其它标题。
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


def parse_and_apply(response: str, primary: str) -> tuple[str, list[dict], str]:
    text = clean(response)
    if text == "NO_CHANGE":
        return primary, [], "no_change"
    if not text.startswith("# PATCH SET"):
        raise ValueError("response is neither NO_CHANGE nor # PATCH SET")
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
    if not patches or len(patches) > 4:
        raise ValueError(f"invalid patch count={len(patches)}")
    if len(result) < 1500:
        raise ValueError(f"patched body too short: {len(result)}")
    return result.strip(), patches, "patched"


def run_one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    prompt, primary, full_prompt = build_patch_prompt(chapter)
    prompt_path = directory / "patch_reviser_prompt.md"
    acp_path = directory / "patch_reviser_high_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    process = subprocess.run(
        [
            "node",
            str(RUNNER),
            str(prompt_path),
            str(acp_path),
            "gpt-5.6-luna",
            "high",
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
    return {
        "chapter": chapter,
        "prompt_chars": len(prompt),
        "control_prompt_chars": len(full_prompt),
        "prompt_reduction_percent": round((1 - len(prompt) / len(full_prompt)) * 100, 2),
        "wall_seconds": data.get("wall_seconds"),
        "control_high_wall_seconds": high_data.get("wall_seconds"),
        "measured_speedup_percent": round(
            (1 - float(data.get("wall_seconds") or 0) / float(high_data.get("wall_seconds") or 1))
            * 100,
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
