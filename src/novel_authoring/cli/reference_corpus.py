"""Thin CLI for the filesystem-only Reference Corpus V0 foundation."""

# Typer options intentionally live in function defaults for the project's
# existing Typer compatibility policy.
# ruff: noqa: B008

from __future__ import annotations

from pathlib import Path

import typer

from novel_authoring.cli.legacy import _emit, app
from novel_authoring.reference_corpus.service import (
    ReferenceCorpusError,
    build_inventory,
    corpus_status,
    create_scaffold,
    load_inventory,
    load_selection,
    propose_selection,
    validate_corpus,
    validate_selection,
    write_inventory,
    write_selection_proposal,
)

corpus_app = typer.Typer(help="Reference Corpus V0 确定性基础与作者选择提案")
app.add_typer(corpus_app, name="corpus")


@corpus_app.command("init")
def corpus_init_command(
    raw_root: Path = typer.Option(..., "--raw-root", help="只读来源小说目录"),
    corpus_root: Path = typer.Option(..., "--corpus-root", help="派生 Reference Corpus 目录"),
) -> None:
    """建立不含原文的 Reference Corpus V0 脚手架。"""

    try:
        _emit(create_scaffold(corpus_root, raw_root))
    except (ReferenceCorpusError, OSError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc


@corpus_app.command("inventory")
def corpus_inventory_command(
    raw_root: Path = typer.Option(..., "--raw-root", exists=True, file_okay=False),
    corpus_root: Path = typer.Option(..., "--corpus-root"),
) -> None:
    """扫描 raw root，写入 inventory 与 PROPOSED selection，不读取派生原文。"""

    try:
        manifest = build_inventory(raw_root, corpus_root)
        paths = write_inventory(manifest, corpus_root)
        proposal_paths = write_selection_proposal(propose_selection(manifest))
        _emit(
            {
                "schema_version": manifest.schema_version,
                "raw_root": manifest.raw_root,
                "corpus_root": manifest.corpus_root,
                "actual_category_count": len(manifest.actual_categories),
                "file_count": len(manifest.files),
                "category_counts": {
                    item.category_id: item.file_count for item in manifest.categories
                },
                "warnings": manifest.warnings,
                "paths": {**paths, **proposal_paths},
            }
        )
    except (ReferenceCorpusError, OSError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc


@corpus_app.command("validate-selection")
def corpus_validate_selection_command(
    corpus_root: Path = typer.Option(..., "--corpus-root", exists=True, file_okay=False),
    selection: Path | None = typer.Option(None, "--selection", help="默认 proposed YAML"),
) -> None:
    """验证 selection 与 inventory 对齐，并报告类别数量 blocker。"""

    try:
        root = corpus_root.expanduser().resolve()
        inventory = load_inventory(root / "selection/inventory.json")
        selection_path = (
            selection.expanduser().resolve()
            if selection
            else root / "selection/pilot-selection.proposed.yaml"
        )
        result = validate_selection(inventory, load_selection(selection_path))
        _emit(result)
        if not result["valid"]:
            raise typer.Exit(code=1)
    except (ReferenceCorpusError, OSError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc


@corpus_app.command("validate")
def corpus_validate_command(
    corpus_root: Path = typer.Option(..., "--corpus-root", exists=True, file_okay=False),
) -> None:
    """验证脚手架、schema pack、selection 对齐与来源正文泄漏边界。"""

    try:
        result = validate_corpus(corpus_root)
        _emit(result)
        if not result["valid"]:
            raise typer.Exit(code=1)
    except (ReferenceCorpusError, OSError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc


@corpus_app.command("status")
def corpus_status_command(
    corpus_root: Path = typer.Option(..., "--corpus-root", exists=True, file_okay=False),
) -> None:
    """显示本地脚手架、inventory、selection 与 GBrain pending 状态。"""

    try:
        _emit(corpus_status(corpus_root))
    except (ReferenceCorpusError, OSError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc


__all__ = [
    "corpus_init_command",
    "corpus_inventory_command",
    "corpus_validate_command",
    "corpus_validate_selection_command",
    "corpus_status_command",
]
