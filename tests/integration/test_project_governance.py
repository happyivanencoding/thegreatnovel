from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from novel_authoring.db.database import Database
from novel_authoring.library_catalog import CatalogScope, build_library_catalog
from novel_authoring.library_governance import (
    APPLY_CONFIRMATION,
    apply_classification_mapping,
    build_classification_plan,
)
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.library import LibraryAddOptions, add_book
from novel_authoring.storage.registry import BookKind, BookRegistry, CreationMode
from novel_authoring.web.app import create_app


def _source(path: Path, title: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"第1章 {title}\n\n风从门缝里灌进来。\n", encoding="utf-8")
    return path


def _add(
    layout: BookLayout,
    root: Path,
    book_id: str,
    kind: BookKind = BookKind.AUTHOR,
) -> None:
    add_book(
        LibraryAddOptions(
            book_id=book_id,
            title=book_id,
            source=_source(root / f"{book_id}.md", book_id),
            source_origin=root / f"{book_id}.md",
            library_root=layout.library_root,
            book_kind=kind,
        )
    )


def test_author_catalog_hides_technical_and_unclassified_books(tmp_path: Path) -> None:
    layout = BookLayout(tmp_path / "library")
    discovery = tmp_path / "book"
    discovery.mkdir()
    _add(layout, discovery, "author-book")
    _add(layout, tmp_path / "bench", "benchmark-book", BookKind.BENCHMARK)
    BookRegistry(layout).ensure("legacy-book", title="历史未分类")

    author = build_library_catalog(layout, discovery)
    technical = build_library_catalog(layout, discovery, scope=CatalogScope.TECHNICAL)

    assert [item.book_id for item in author.entries] == ["author-book"]
    assert {item.book_id for item in technical.entries} == {
        "benchmark-book",
        "legacy-book",
    }
    assert technical.to_dict()["kind_counts"]["BENCHMARK"] == 1
    assert technical.to_dict()["kind_counts"]["UNCLASSIFIED"] == 1


def test_legacy_import_without_origin_deduplicates_only_exact_source_file(
    tmp_path: Path,
) -> None:
    layout = BookLayout(tmp_path / "library")
    discovery = tmp_path / "book"
    source = _source(discovery / "旧书.md", "旧书")
    add_book(
        LibraryAddOptions(
            book_id="author-book",
            title="旧书",
            source=source,
            source_origin=source,
            library_root=layout.library_root,
        )
    )
    registry = BookRegistry(layout)
    values = registry.read("author-book")
    values.pop("source_origin", None)
    registry.write(layout.for_book("author-book"), values)

    catalog = build_library_catalog(layout, discovery)

    assert source.is_file()
    assert [item.book_id for item in catalog.entries] == ["author-book"]
    assert all(item.candidate_id is None for item in catalog.entries)


def test_formal_import_persists_author_imported_metadata(tmp_path: Path) -> None:
    layout = BookLayout(tmp_path / "library")
    source = _source(tmp_path / "book" / "作者书.md", "作者书")

    add_book(
        LibraryAddOptions(
            book_id="author-book",
            title="作者书",
            source=source,
            library_root=layout.library_root,
        )
    )

    record = BookRegistry(layout).record("author-book")
    assert record.book_kind is BookKind.AUTHOR
    assert record.creation_mode is CreationMode.IMPORTED
    yaml_text = layout.for_book("author-book").book_yaml.read_text(encoding="utf-8")
    assert "book_kind: AUTHOR" in yaml_text
    assert "creation_mode: IMPORTED" in yaml_text


def test_classification_requires_explicit_mapping_and_preserves_other_metadata(
    tmp_path: Path,
) -> None:
    layout = BookLayout(tmp_path / "library")
    registry = BookRegistry(layout)
    registry.ensure("legacy", title="旧项目")
    before = registry.read("legacy")
    mapping = tmp_path / "mapping.json"
    mapping.write_text(
        json.dumps(
            {"mappings": [{"book_id": "legacy", "book_kind": "TEST"}]},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    try:
        apply_classification_mapping(layout, mapping, confirm="wrong")
    except ValueError as exc:
        assert APPLY_CONFIRMATION in str(exc)
    else:  # pragma: no cover - assertion guard
        raise AssertionError("错误确认词不应写入")
    assert registry.record("legacy").book_kind is BookKind.UNCLASSIFIED

    applied = apply_classification_mapping(
        layout, mapping, confirm=APPLY_CONFIRMATION
    )
    after = registry.read("legacy")
    assert applied[0].book_kind is BookKind.TEST
    assert after["title"] == before["title"]
    assert after["active_edition_id"] == before["active_edition_id"]


def test_preview_uses_explicit_evidence_and_does_not_mutate_book_yaml(tmp_path: Path) -> None:
    project = tmp_path / "project"
    layout = BookLayout(project / "library")
    registry = BookRegistry(layout)
    registry.ensure("phase-book", title="任意标题")
    script = project / "scripts" / "phase9_benchmark.py"
    script.parent.mkdir(parents=True)
    script.write_text('BOOK_ID = "phase-book"\n', encoding="utf-8")
    before = layout.for_book("phase-book").book_yaml.read_bytes()

    plan = build_classification_plan(layout, project_root=project)

    item = plan["suggestions"][0]
    assert item["suggested_book_kind"] == "BENCHMARK"
    assert item["confidence"] == "HIGH"
    assert layout.for_book("phase-book").book_yaml.read_bytes() == before


def test_technical_catalog_requires_developer_mode(tmp_path: Path) -> None:
    layout = BookLayout(tmp_path / "library")
    discovery = tmp_path / "book"
    discovery.mkdir()
    _add(layout, discovery, "author-book")
    _add(layout, tmp_path / "bench", "benchmark-book", BookKind.BENCHMARK)

    normal = TestClient(
        create_app(
            Database(tmp_path / "normal.sqlite3"),
            library_root=layout.library_root,
            discovery_root=discovery,
        )
    )
    developer = TestClient(
        create_app(
            Database(tmp_path / "developer.sqlite3"),
            library_root=layout.library_root,
            discovery_root=discovery,
            developer_mode=True,
        )
    )

    assert normal.get("/api/library/catalog?scope=TECHNICAL").status_code == 404
    assert normal.get("/library/technical").status_code == 404
    assert normal.get("/api/library/benchmark-book/paths").status_code == 404
    assert normal.get("/api/books/benchmark-book/editions").status_code == 404
    payload = developer.get("/api/library/catalog?scope=TECHNICAL").json()
    assert [item["book_id"] for item in payload["entries"]] == ["benchmark-book"]
    assert developer.get("/api/library/benchmark-book/paths").status_code == 200
    assert developer.get("/api/books/benchmark-book/editions").status_code == 200
    page = developer.get("/library/technical")
    assert page.status_code == 200
    assert "Benchmark、Test、Demo" in page.text
    assert "benchmark-book" in page.text
    author_payload = developer.get("/api/library/catalog").json()
    assert [item["book_id"] for item in author_payload["entries"]] == ["author-book"]
