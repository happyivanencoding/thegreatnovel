"""Thin CLI for the filesystem-only Reference Corpus V0 foundation."""

# Typer options intentionally live in function defaults for the project's
# existing Typer compatibility policy.
# ruff: noqa: B008

from __future__ import annotations

from pathlib import Path

import typer

from novel_authoring.cli.legacy import _emit, app
from novel_authoring.reference_corpus.semantic import (
    SemanticCorpusError,
    audit_semantic_corpus,
    compile_semantic_corpus,
    confirm_v0_sources,
    stats_semantic_corpus,
    validate_semantic_corpus,
)
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


@corpus_app.command("semantic-validate")
def corpus_semantic_validate_command(
    corpus_root: Path = typer.Option(..., "--corpus-root", exists=True, file_okay=False),
) -> None:
    """验证 Semantic Distillation V1 的 Markdown、证据与 reference-only 边界。"""

    try:
        result = validate_semantic_corpus(corpus_root)
        _emit(result)
        if not result["valid"]:
            raise typer.Exit(code=1)
    except (SemanticCorpusError, OSError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc


@corpus_app.command("compile")
def corpus_compile_command(
    corpus_root: Path = typer.Option(..., "--corpus-root", exists=True, file_okay=False),
) -> None:
    """把 V1 Markdown 投影编译成 machine package。"""

    try:
        _emit(compile_semantic_corpus(corpus_root))
    except (SemanticCorpusError, OSError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc


@corpus_app.command("audit")
def corpus_audit_command(
    corpus_root: Path = typer.Option(..., "--corpus-root", exists=True, file_okay=False),
) -> None:
    """生成 Corpus Semantic Audit 与 Lens Audit 报告。"""

    try:
        result = audit_semantic_corpus(corpus_root)
        _emit(result)
        if not result["valid"]:
            raise typer.Exit(code=1)
    except (SemanticCorpusError, OSError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc


@corpus_app.command("stats")
def corpus_stats_command(
    corpus_root: Path = typer.Option(..., "--corpus-root", exists=True, file_okay=False),
) -> None:
    """输出确定性覆盖统计，不计算 literary score。"""

    try:
        _emit(stats_semantic_corpus(corpus_root))
    except (SemanticCorpusError, OSError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc


@corpus_app.command("confirm-sources")
def corpus_confirm_sources_command(
    corpus_root: Path = typer.Option(..., "--corpus-root", exists=True, file_okay=False),
) -> None:
    """冻结当前已经实际生成 V0 资产的 26 本来源，不重新运行 selection。"""

    try:
        _emit(confirm_v0_sources(corpus_root))
    except (SemanticCorpusError, OSError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc


__all__ = [
    "corpus_init_command",
    "corpus_inventory_command",
    "corpus_validate_command",
    "corpus_validate_selection_command",
    "corpus_status_command",
    "corpus_audit_command",
    "corpus_compile_command",
    "corpus_confirm_sources_command",
    "corpus_semantic_validate_command",
    "corpus_stats_command",
]
