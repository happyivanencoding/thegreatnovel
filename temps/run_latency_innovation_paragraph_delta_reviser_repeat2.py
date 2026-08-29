from __future__ import annotations

import difflib
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
SOURCE = BOOK / "runs"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "paragraph-delta-reviser-repeat2"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

DELTA_TEMPLATE = """你是 TGN 的 Paragraph-Delta Authority Reviser，使用与 production 相同的 GPT-5.6 Luna high。你读取与完整 Authority Reviser 相同的 Frozen Mission、Curator、World/Power/Human Authority、Reader Release、Canon Tail/Index 和 Primary Draft；区别只在输出协议。

Primary Draft 已按自然段编号。Preservation First：没有明确失败的段落保持原样，不输出、不改写。你必须在内部完成 production Reviser 同样的全章语义 sweep：
- Frozen Mission 的行动者、对象、Direct Result、State Change 与 Ending 必须真实完成；不能降成准备、资格、依据、以后结算或“即将”。
- Canon / World / Power / Human / Reader Release 决定事实边界；未知仍未知；Named Entity、时间、数字/档位、持有人、资源、关系和能力条件全文一致。
- 同一个错误事实若影响多个非相邻段落，必须把所有相关段落列入操作，不能只修第一处。
- 修事实时保护可分离的主角主动性、人物欲望、关系、核心幻想、奖励占有、Public Proof、社会重估、惊喜与真实章末动作。
- 只有 Draft 真实出现无新选择的登记、报告、路线、协调、重复证明或后台抽象时才压缩；不要把正常场景、谈判、人物反应或 payoff 删成摘要。

严格只允许两种输出：

KEEP_ALL

或：

# PARAGRAPH OPS
## REPLACE P005-P007
<替换这段连续范围的完整新正文；可含多个自然段>
## DELETE P012-P013
## INSERT_BEFORE P020
<插入正文>
## INSERT_AFTER P025
<插入正文>

规则：
- P 编号必须来自下方 Draft；范围闭合、不可重叠。
- REPLACE 可替换单段或连续多段；DELETE 不带正文；INSERT 只针对单个 P。
- 输出所有需要修改的非相邻位置；不输出未修改段落。
- 新正文不得包含 P 编号、Audit、解释、评分或操作理由。
- 不限制操作数量，但不得为了润色整章重写；若只有一句有问题，只替换所在最小段落。
"""

OP_PATTERN = re.compile(
    r"(?ms)^##\s+(REPLACE|DELETE|INSERT_BEFORE|INSERT_AFTER)\s+P(\d+)(?:-P(\d+))?\s*$\n?(.*?)(?=^##\s+(?:REPLACE|DELETE|INSERT_BEFORE|INSERT_AFTER)\s+P\d+|\Z)"
)


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


def paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]


def numbered(text: str) -> str:
    return "\n\n".join(f"[[P{index:03d}]]\n{paragraph}" for index, paragraph in enumerate(paragraphs(text), 1))


def call(prompt_path: Path, output_path: Path) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-luna", "high", str(ROOT)],
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
                data = {}; last = str(error)
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (process.stderr + "\n" + process.stdout)[-3000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(last)


def apply_ops(response: str, primary: str) -> tuple[str, list[dict]]:
    text = clean(response)
    if text == "KEEP_ALL":
        return primary.strip(), []
    if not text.startswith("# PARAGRAPH OPS"):
        raise ValueError("missing KEEP_ALL or # PARAGRAPH OPS")
    original = paragraphs(primary)
    replacements: dict[int, tuple[int, list[str], str]] = {}
    inserts_before: dict[int, list[str]] = {}
    inserts_after: dict[int, list[str]] = {}
    operations = []
    occupied: set[int] = set()
    for match in OP_PATTERN.finditer(text):
        kind = match.group(1)
        start = int(match.group(2))
        end = int(match.group(3) or start)
        payload = match.group(4).strip()
        if start < 1 or end < start or end > len(original):
            raise ValueError(f"invalid range {start}-{end}/{len(original)}")
        if kind in {"REPLACE", "DELETE"}:
            ids = set(range(start, end + 1))
            if occupied & ids:
                raise ValueError("overlapping replace/delete ranges")
            occupied |= ids
            new_parts = paragraphs(payload) if kind == "REPLACE" else []
            if kind == "REPLACE" and not new_parts:
                raise ValueError("empty replacement")
            replacements[start] = (end, new_parts, kind)
        else:
            if end != start:
                raise ValueError("insert cannot use a range")
            new_parts = paragraphs(payload)
            if not new_parts:
                raise ValueError("empty insert")
            target = inserts_before if kind == "INSERT_BEFORE" else inserts_after
            target.setdefault(start, []).extend(new_parts)
        operations.append({"kind": kind, "start": start, "end": end, "payload_chars": len(payload)})
    if not operations:
        raise ValueError("no operations parsed")
    for target in list(inserts_before) + list(inserts_after):
        if target in occupied:
            raise ValueError("insert target lies inside replaced/deleted range")
    output: list[str] = []
    index = 1
    while index <= len(original):
        output.extend(inserts_before.get(index, []))
        if index in replacements:
            end, new_parts, _ = replacements[index]
            output.extend(new_parts)
            output.extend(inserts_after.get(end, []))
            index = end + 1
            continue
        output.append(original[index - 1])
        output.extend(inserts_after.get(index, []))
        index += 1
    final = "\n\n".join(output).strip()
    if not final or "[[P" in final or "# PARAGRAPH OPS" in final:
        raise ValueError("invalid assembled final")
    return final, operations


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    full_prompt = (source / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    primary = body((source / "primary_response.md").read_text(encoding="utf-8"))
    runtime_start = full_prompt.index("# Hybrid Runtime")
    draft_marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    draft_start = full_prompt.index(draft_marker, runtime_start)
    authority_context = full_prompt[runtime_start:draft_start].strip()
    prompt = DELTA_TEMPLATE + "\n\n" + authority_context + "\n\n# NUMBERED PRIMARY DRAFT\n\n" + numbered(primary)
    prompt_path = directory / "paragraph_delta_prompt.md"
    output_path = directory / "paragraph_delta_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    (directory / "paragraph_delta_response.md").write_text(response + "\n", encoding="utf-8")
    final, operations = apply_ops(response, primary)
    (directory / "final_body.md").write_text(final + "\n", encoding="utf-8")

    control_data = json.loads((source / "authority_reviser_acp.json").read_text(encoding="utf-8"))
    control_body = body((source / "authority_reviser_response.md").read_text(encoding="utf-8"))
    similarity = difflib.SequenceMatcher(None, primary, final).ratio()
    changed_source_paragraphs = sum(op["end"] - op["start"] + 1 for op in operations if op["kind"] in {"REPLACE", "DELETE"})
    return {
        "chapter": chapter,
        "wall_seconds": float(data.get("wall_seconds") or 0),
        "control_wall_seconds": float(control_data.get("wall_seconds") or 0),
        "speedup_percent": round((1 - float(data.get("wall_seconds") or 0) / float(control_data.get("wall_seconds") or 1)) * 100, 2),
        "full_prompt_chars": len(full_prompt),
        "delta_prompt_chars": len(prompt),
        "response_chars": len(response),
        "operation_count": len(operations),
        "changed_source_paragraphs": changed_source_paragraphs,
        "primary_paragraphs": len(paragraphs(primary)),
        "primary_similarity": round(similarity, 6),
        "final_chars": len(final),
        "control_final_chars": len(control_body),
        "operations": operations,
        "usage": data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result(); rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
