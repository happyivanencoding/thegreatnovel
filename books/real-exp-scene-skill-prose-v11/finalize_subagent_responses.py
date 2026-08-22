"""Parse and ledger the eight completed Codex-subagent responses.

No model or network call is made here. Raw response files are never rewritten;
only deterministic derived artifacts and local ledgers are created.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "books" / "real-exp-scene-skill-prose-v11"
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from story_mvp.hybrid_runtime import (  # noqa: E402
    extract_primary_draft,
    extract_primary_fact_summary,
)


CURATOR_AGENTS = {
    2: "01a02b40-30e3-74a1-8559-5f60359b8355",
    3: "01a02b40-b8e5-7500-9536-840e6f9f77de",
}
PRIMARY_AGENTS = {
    (2, "A_no_skill"): "01a02b43-a3c9-71c1-bb80-16ba1fb36e59",
    (2, "B_scene_skill_v1"): "01a02b43-a58f-7e71-9d47-1ba2ab045022",
    (2, "C_scene_skill_v11"): "01a02b43-a83e-7901-87ea-c9ab4fd5adc5",
    (3, "A_no_skill"): "01a02b47-ece9-7c61-ac1c-a4c79fc0b844",
    (3, "B_scene_skill_v1"): "01a02b47-ef53-7be1-9e3a-c1e3cc515ab5",
    (3, "C_scene_skill_v11"): "01a02b47-f201-7d81-9958-aecbb8ca12e8",
}
MODEL_NOTE = "Codex subagent（luna_worker；具体底层模型未由当前实验环境独立暴露）"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    legacy_log = read(OUT / "CALL_LOG.json")
    if legacy_log.strip() and not (OUT / "EXTERNAL_API_ATTEMPTS.json").is_file():
        write(OUT / "EXTERNAL_API_ATTEMPTS.json", legacy_log)

    records: list[dict[str, object]] = []
    parser_records: list[dict[str, object]] = []
    call_index = 0

    for chapter in (2, 3):
        curator_response = read(OUT / f"chapter-{chapter:04d}" / "curator_response.md")
        if not curator_response.strip():
            raise SystemExit(f"Chapter {chapter} Curator Response 缺失")
        call_index += 1
        records.append(
            {
                "call_index": call_index,
                "kind": "context_curator",
                "chapter": chapter,
                "group": None,
                "agent_id": CURATOR_AGENTS[chapter],
                "agent_role": "luna_worker",
                "model": MODEL_NOTE,
                "status": "completed",
                "prompt_file": f"chapter-{chapter:04d}/curator_prompt.md",
                "response_file": f"chapter-{chapter:04d}/curator_response.md",
                "prompt_chars": len(read(OUT / f"chapter-{chapter:04d}" / "curator_prompt.md")),
                "response_chars": len(curator_response),
            }
        )

        for group in ("A_no_skill", "B_scene_skill_v1", "C_scene_skill_v11"):
            response_path = OUT / f"chapter-{chapter:04d}" / group / "primary_response.md"
            response = read(response_path)
            if not response.strip():
                raise SystemExit(f"Primary Response 缺失：{response_path}")
            draft = extract_primary_draft(response)
            facts = extract_primary_fact_summary(response)
            parser_status = "completed" if draft.strip() and facts.strip() else "format_failure"
            write(response_path.parent / "chapter.md", draft if draft.strip() else "[格式遵循失败：缺少 Primary Draft]")
            write(
                response_path.parent / "chapter_fact_summary.md",
                facts if facts.strip() else "[格式遵循失败：缺少 Primary Fact Summary]",
            )
            parser_records.append(
                {
                    "chapter": chapter,
                    "group": group,
                    "status": parser_status,
                    "response_file": str(response_path.relative_to(OUT)),
                    "chapter_file": str((response_path.parent / "chapter.md").relative_to(OUT)),
                    "fact_summary_file": str((response_path.parent / "chapter_fact_summary.md").relative_to(OUT)),
                    "draft_chars": len(draft),
                    "fact_summary_chars": len(facts),
                }
            )
            call_index += 1
            records.append(
                {
                    "call_index": call_index,
                    "kind": "primary_writer",
                    "chapter": chapter,
                    "group": group,
                    "agent_id": PRIMARY_AGENTS[(chapter, group)],
                    "agent_role": "luna_worker",
                    "model": MODEL_NOTE,
                    "status": "completed",
                    "prompt_file": f"chapter-{chapter:04d}/{group}/primary_prompt.md",
                    "response_file": str(response_path.relative_to(OUT)),
                    "prompt_chars": len(read(response_path.parent / "primary_prompt.md")),
                    "response_chars": len(response),
                    "parser_status": parser_status,
                }
            )

    write(OUT / "CALL_LOG.json", json.dumps(records, ensure_ascii=False, indent=2))
    write(OUT / "PARSER_STATUS.json", json.dumps(parser_records, ensure_ascii=False, indent=2))
    write(
        OUT / "EXCLUDED_EXECUTION_FAILURES.json",
        json.dumps(
            [
                {
                    "agent_id": "01a02b40-32be-71b2-b232-afa335a74fba",
                    "status": "excluded_execution_failure",
                    "reason": "Chapter 3 source prompt file was missing before the single allowed retry; no experiment response was produced.",
                }
            ],
            ensure_ascii=False,
            indent=2,
        ),
    )
    write(
        OUT / "EXCLUDED_UNASSIGNED_AGENTS.json",
        json.dumps(
            {
                "status": "excluded_from_A_B_C",
                "reason": "Three agents were spawned before a batch hit the thread limit; their group mapping was not recoverable, so their results are not used for comparison.",
                "agent_ids": [
                    "01a02b43-587a-7e00-9db8-01a5e39ecbd0",
                    "01a02b43-560c-7190-abb0-b979da1afdb0",
                    "01a02b43-5b2f-7903-a966-f53f39908c09",
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
    )
    completed = sum(item["status"] == "completed" for item in parser_records)
    write(
        OUT / "RUN_STATUS.md",
        "\n".join(
            [
                "# Run Status",
                "",
                f"完成时间（UTC）：{datetime.now(timezone.utc).isoformat()}",
                "",
                "目标 Codex subagent 调用：8 / 8",
                f"Primary parser 成功：{completed} / 6",
                "外部 API 调用：不计入实验；失败记录见 EXTERNAL_API_ATTEMPTS.json",
            ]
        ),
    )
    print(json.dumps({"calls": len(records), "primary_parser_success": completed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
