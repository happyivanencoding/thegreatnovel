from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
INNOVATION = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1"
OUT = ROOT / "books" / "real-exp-atomic-chapter-obligations-20260829-v1" / "phase-b-calibration"
CHAPTERS = (2, 3, 9, 10, 14, 16, 19)

sys.path.insert(0, str(ROOT / "temps"))
from atomic_chapter_obligations import (  # noqa: E402
    body,
    compile_obligations,
    infer_diff_operations,
    load_operations,
    save_pack,
    validate_candidate,
)


def read_body(path: Path) -> str:
    return body(path.read_text(encoding="utf-8"))


def mutation_copy_becomes_original(text: str) -> str:
    changed = text.replace("事实副本", "原路线册").replace("记录副本", "原路线册")
    return changed


def mutation_append(text: str, paragraph: str) -> str:
    return text.rstrip() + "\n\n" + paragraph.strip()


def mutation_remove_departure(text: str) -> str:
    marker = "他踩上车辕"
    if marker in text:
        prefix = text.split(marker, 1)[0].rstrip()
        return prefix + "\n\n第一批粮车仍停在巷口等着，顾停舟还没有上车。"
    return re.sub(r"(?ms)\n[^\n]*上车[^\n]*\n.*?车轮.*?驶去.*$", "\n\n第一批粮车仍停在巷口等着。", text)


def mutation_remove_relationship_value(text: str) -> str:
    parts = [
        paragraph for paragraph in re.split(r"\n\s*\n", text)
        if not any(term in paragraph for term in ("少东家", "短契", "合作", "承运", "旧情"))
    ]
    return "\n\n".join(parts)


def make_mutations(chapter: int, full_body: str) -> list[tuple[str, str, str]]:
    result: list[tuple[str, str, str]] = []
    if chapter == 2:
        result.extend(
            [
                ("MUT-copy-original-collapse", mutation_copy_becomes_original(full_body), "KNOWN_BAD"),
                ("MUT-license-completed-early", mutation_append(full_body, "顾停舟的行潮籍已经正式落籍，独立身份当场完成。"), "KNOWN_BAD"),
            ]
        )
    if chapter == 9:
        result.extend(
            [
                ("MUT-unapproved-chenglu", mutation_append(full_body, "这一刻，顾停舟正式进入成炉。"), "KNOWN_BAD"),
                ("MUT-lost-tail-received", mutation_append(full_body, "矿路实测尾款随后又交到顾停舟手里。"), "KNOWN_BAD"),
                ("MUT-clone-full-power", mutation_append(full_body, "分身已经携带本体全部力量，与本体没有差别。"), "KNOWN_BAD"),
            ]
        )
    if chapter == 14:
        result.extend(
            [
                ("MUT-not-departed", mutation_remove_departure(full_body), "KNOWN_BAD"),
                ("MUT-unapproved-zhaoyu", mutation_append(full_body, "顾停舟借这次开炉试正式进入照域。"), "KNOWN_BAD"),
                ("MUT-entitlement-to-cash", mutation_append(full_body, "个人矿利八百潮铢已经当场到账。"), "KNOWN_BAD"),
                ("MUT-delete-relationship-value", mutation_remove_relationship_value(full_body), "KNOWN_BAD"),
            ]
        )
    if chapter == 16:
        result.extend(
            [
                ("MUT-reveal-unknown-cause", mutation_append(full_body, "地潮提前的原因是照域潮谱提前泄出了力量。"), "KNOWN_BAD"),
                ("MUT-complete-pending-carriage", mutation_append(full_body, "第一批承运已经全部完成，粮运短契当场结清。"), "KNOWN_BAD"),
                ("MUT-unapproved-zhaoyu", mutation_append(full_body, "顾停舟在旧关外层正式进入照域。"), "KNOWN_BAD"),
            ]
        )
    return result


def candidate_rows(chapter: int, primary: str, full: str) -> list[tuple[str, str, list[dict[str, Any]], str]]:
    rows: list[tuple[str, str, list[dict[str, Any]], str]] = [
        ("PRIMARY", primary, [], "DIAGNOSTIC"),
        ("FULL_REVISER", full, infer_diff_operations(primary, full), ""),
    ]
    for name, rel in (
        ("DELTA_RUN1", "paragraph-delta-reviser"),
        ("DELTA_REPEAT2", "paragraph-delta-reviser-repeat2"),
    ):
        directory = INNOVATION / rel
        candidate = directory / f"chapter-{chapter:04d}" / "final_body.md"
        summary = directory / "summary.json"
        if candidate.exists() and summary.exists():
            rows.append(
                (
                    name,
                    candidate.read_text(encoding="utf-8").strip(),
                    load_operations(summary, chapter),
                    "",
                )
            )
    rows.extend(
        (name, text, infer_diff_operations(primary, text), label)
        for name, text, label in make_mutations(chapter, full)
    )
    return rows


def expected_label(chapter: int, candidate: str, preflight: bool, explicit: str) -> str:
    if explicit:
        return explicit
    if not preflight:
        return "KNOWN_BAD"
    if candidate == "FULL_REVISER":
        return "KNOWN_BAD" if chapter == 16 else "KNOWN_SAFE"
    if candidate == "DELTA_RUN1":
        return "KNOWN_SAFE" if chapter in {2, 14} else "KNOWN_BAD"
    # Repeat2 and Primary are diagnostic because prior Reader/Authority evidence split.
    return "DIAGNOSTIC"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for chapter in CHAPTERS:
        source = SOURCE / f"chapter-{chapter:04d}"
        chapter_dir = OUT / f"chapter-{chapter:04d}"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        primary = read_body(source / "primary_response.md")
        full = read_body(source / "authority_reviser_response.md")
        pack = compile_obligations(
            chapter=chapter,
            authority_prompt=(source / "authority_reviser_prompt.md").read_text(encoding="utf-8"),
            curator_response=(source / "curator_response.md").read_text(encoding="utf-8"),
            primary_body=primary,
        )
        save_pack(pack, chapter_dir / "obligation_pack.json")
        for candidate_name, candidate_body, operations, explicit_label in candidate_rows(chapter, primary, full):
            result = validate_candidate(
                pack,
                primary_body=primary,
                final_body=candidate_body,
                operations=operations,
            )
            label = expected_label(chapter, candidate_name, pack.preflight_eligible, explicit_label)
            row = {
                "chapter": chapter,
                "candidate": candidate_name,
                "expected": label,
                "preflight_eligible": pack.preflight_eligible,
                "decision": result["decision"],
                "obligation_count": len(pack.obligations),
                "unsupported_count": len(pack.unsupported_clauses),
                "source_conflict_count": len(pack.source_conflicts),
                "operation_count": len(operations),
                "touched_source_paragraphs": result["touched_source_paragraphs"],
                "status_counts": result["status_counts"],
                "blocking_ids": [item["obligation_id"] for item in result["blocking_checks"]],
                "blocking_reasons": [item["reason"] for item in result["blocking_checks"]],
            }
            rows.append(row)
            safe_name = re.sub(r"[^A-Za-z0-9_-]+", "-", candidate_name).strip("-").lower()
            (chapter_dir / f"gate-{safe_name}.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            if candidate_name.startswith("MUT-"):
                (chapter_dir / f"{safe_name}.md").write_text(candidate_body + "\n", encoding="utf-8")
            print(json.dumps(row, ensure_ascii=False), flush=True)

    known_safe = [row for row in rows if row["expected"] == "KNOWN_SAFE"]
    known_bad = [row for row in rows if row["expected"] == "KNOWN_BAD"]
    safe_adopted = sum(row["decision"] == "ADOPT_DELTA" for row in known_safe)
    bad_blocked = sum(row["decision"] == "FALLBACK_FULL_REVISER" for row in known_bad)
    summary = {
        "version": "atomic-obligations-v0.1",
        "chapters": list(CHAPTERS),
        "candidate_rows": len(rows),
        "known_safe": len(known_safe),
        "known_safe_adopted": safe_adopted,
        "known_safe_acceptance_rate": round(safe_adopted / max(1, len(known_safe)), 4),
        "known_bad": len(known_bad),
        "known_bad_blocked": bad_blocked,
        "known_bad_recall": round(bad_blocked / max(1, len(known_bad)), 4),
        "preflight_fallback_chapters": [
            chapter for chapter in CHAPTERS
            if not next(row for row in rows if row["chapter"] == chapter)["preflight_eligible"]
        ],
        "rows": rows,
    }
    (OUT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: value for key, value in summary.items() if key != "rows"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
