"""Codex External 的文件/CLI 合同。

CLI 只把外部 response 接入现有保存服务；它不直接编辑 manifest 或 Workflow State。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .run_ledger import (
    adopt_final_source,
    load_run,
    retry_node,
    save_node_response,
)
from .storage import (
    compose_book_content,
    parse_book_sections,
    replace_chapter,
    require_book,
    save_chapter,
    write_book,
    write_creative_artifact,
)
from .workflow_state import (
    BOOK_SECTIONS,
    CREATIVE_FILES,
    workflow_impact,
    workflow_status,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def workspace_path() -> Path:
    configured = os.environ.get("STORY_MVP_WORKSPACE", "")
    return Path(configured) if configured else PROJECT_ROOT / "books"


def _read_input(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"找不到 External response：{path}")
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError("External response 不能为空")
    return content


def _apply_book_section(book_id: str, artifact: str, content: str, source: str) -> None:
    directory = require_book(book_id, workspace_path())
    old = (directory / "BOOK.md").read_text(encoding="utf-8")
    sections = parse_book_sections(old)
    sections[BOOK_SECTIONS[artifact]] = content
    write_book(book_id, compose_book_content(sections), workspace_path(), source=source)


def apply_response(
    *,
    book_id: str,
    artifact: str,
    input_path: Path,
    source: str,
    chapter: int | None = None,
    node: str | None = None,
) -> dict[str, object]:
    content = _read_input(input_path)
    directory = require_book(book_id, workspace_path())
    if artifact in CREATIVE_FILES:
        storage_artifact = artifact.removeprefix("creative.")
        if storage_artifact == "story_program":
            storage_artifact = "proposal"
        write_creative_artifact(
            book_id,
            storage_artifact,
            content,
            workspace_path(),
            origin="author_edited",
            workflow_source=source,
        )
    elif artifact in BOOK_SECTIONS:
        _apply_book_section(book_id, artifact, content, source)
    else:
        parsed = artifact.split(".")
        if len(parsed) != 3 or parsed[0] != "chapter" or not parsed[1].isdigit():
            raise ValueError(f"不支持的 External Artifact：{artifact}")
        chapter_number = int(parsed[1])
        kind = parsed[2]
        if chapter is not None and chapter != chapter_number:
            raise ValueError("--chapter 与 artifact 章节编号不一致")
        if kind == "body":
            target = directory / "chapters" / f"chapter-{chapter_number:04d}.md"
            if target.is_file():
                replace_chapter(book_id, chapter_number, content, workspace_path(), source=source)
            else:
                save_chapter(book_id, chapter_number, content, workspace_path(), source=source)
        elif kind in {"run", "state_delta"}:
            if not node:
                raise ValueError("Run / State Delta External apply 需要 --node")
            if kind == "state_delta" and node != "state_delta":
                raise ValueError("chapter.N.state_delta 只能使用 --node state_delta")
            load_run(directory, chapter_number)
            run_manifest = save_node_response(directory, chapter_number, node, content)
            if node == "authority_reviser":
                reviser = run_manifest["nodes"]["authority_reviser"]
                if reviser.get("status") in {"completed", "adopted"}:
                    # Production fixed reviser is the default final prose source; optional repair may later replace it with Integrator.
                    adopt_final_source(directory, chapter_number, "authority_reviser")
                elif reviser.get("repair_reason") == "missing_explicit_milestone_outcome":
                    # External Codex has no UI button to prepare the bounded retry, so advance the same
                    # node to attempt 2 and expose the already-saved narrow repair prompt in the result.
                    retry_node(directory, chapter_number, "authority_reviser")
        else:
            raise ValueError(f"不支持的章节 Artifact：{artifact}")

    result = workflow_status(directory)
    impact = workflow_impact(directory, artifact)
    if (
        input_path.parent.name == ".workflow_tmp"
        and directory.resolve() in input_path.resolve().parents
    ):
        input_path.unlink()
    output: dict[str, object] = {
        "status": "applied",
        "artifact": artifact,
        "source": source,
        "workflow": result,
        "stale_dependents": impact["existing_nodes_affected"],
    }
    if artifact.startswith("chapter.") and node == "authority_reviser":
        manifest = load_run(directory, chapter_number)
        reviser = manifest["nodes"]["authority_reviser"]
        if reviser.get("repair_reason") == "missing_explicit_milestone_outcome":
            output["status"] = "repair_required"
            output["repair_prompt_file"] = reviser.get("prompt_file")
            output["repair_reason"] = reviser.get("repair_reason")
        elif reviser.get("repair_reason") == "explicit_milestone_repair_failed":
            output["status"] = "repair_failed"
            output["repair_reason"] = reviser.get("repair_reason")
    return output


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="story-mvp-workflow")
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="读取 Workflow State")
    status.add_argument("--book", required=True)

    impact = sub.add_parser("impact", help="读取实际 Dependency Impact")
    impact.add_argument("--book", required=True)
    impact.add_argument("--artifact", required=True)

    apply = sub.add_parser("apply", help="通过统一保存服务 ingest External response")
    apply.add_argument("--book", required=True)
    apply.add_argument("--artifact", required=True)
    apply.add_argument("--input", required=True, type=Path)
    apply.add_argument("--source", default="codex_external")
    apply.add_argument("--chapter", type=int)
    apply.add_argument("--node")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = _parser().parse_args(argv)
    directory = require_book(args.book, workspace_path())
    if args.command == "status":
        output = workflow_status(directory)
    elif args.command == "impact":
        output = workflow_impact(directory, args.artifact)
    else:
        output = apply_response(
            book_id=args.book,
            artifact=args.artifact,
            input_path=args.input,
            source=args.source,
            chapter=args.chapter,
            node=args.node,
        )
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
