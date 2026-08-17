"""CLI for the isolated Reference Corpus Program-Deep V1 package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from novel_authoring.reference_corpus.program_deep import (
    ProgramDeepError,
    audit_program_deep,
    compile_machine_package,
    initialize_program_deep,
    merge_worker_artifacts,
    reset_book_to_skeleton,
    stats_program_deep,
    validate_program_deep,
)


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--corpus-root", type=Path, required=True)
    parser.add_argument("--operations-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reference Corpus Program-Deep V1 offline adapter")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init")
    _common(init)
    init.add_argument("--raw-root", type=Path)

    merge = subparsers.add_parser("merge-workers")
    _common(merge)
    merge.add_argument("--worker-root", type=Path, required=True)

    reset = subparsers.add_parser("reset-book")
    _common(reset)
    reset.add_argument("--source-book-id", required=True)
    reset.add_argument("--backup-label", required=True)

    for name in ("validate", "compile", "audit"):
        command = subparsers.add_parser(name)
        _common(command)

    stats = subparsers.add_parser("stats")
    stats.add_argument("--output-root", type=Path, required=True)
    return parser


def _run(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "init":
        return initialize_program_deep(
            args.corpus_root,
            args.operations_root,
            args.output_root,
            raw_root=args.raw_root,
        )
    if args.command == "merge-workers":
        return merge_worker_artifacts(
            args.corpus_root,
            args.operations_root,
            args.output_root,
            args.worker_root,
        )
    if args.command == "reset-book":
        return reset_book_to_skeleton(
            args.corpus_root,
            args.operations_root,
            args.output_root,
            args.source_book_id,
            backup_label=args.backup_label,
        )
    if args.command == "validate":
        return validate_program_deep(args.corpus_root, args.operations_root, args.output_root)
    if args.command == "compile":
        return compile_machine_package(args.corpus_root, args.operations_root, args.output_root)
    if args.command == "audit":
        return audit_program_deep(args.corpus_root, args.operations_root, args.output_root)
    if args.command == "stats":
        return stats_program_deep(args.output_root)
    raise ProgramDeepError(f"未知 command：{args.command}")


def main() -> int:
    args = build_parser().parse_args()
    try:
        print(json.dumps(_run(args), ensure_ascii=False, indent=2))
    except (ProgramDeepError, OSError, ValueError) as exc:
        print(str(exc))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
