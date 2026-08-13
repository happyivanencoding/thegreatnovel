"""S2：migrate-legacy 对真实 handoff 行的迁移回归。

覆盖：
- legacy flat 布局 handoff 行迁移后 prompt_path/result_path 指向真实存在的
  ``input/`` / ``output/`` 文件，且 ``copy_instruction`` 可用；
- W3：``task_directory`` 不在本次迁移 operations 目标前缀下的行不被
  ``_align_workflow_handoff_paths`` 误改；
- 幂等：对已迁移数据库重复执行路径改写不再产生变化。
"""

from __future__ import annotations

from pathlib import Path

from novel_authoring.config import load_settings
from novel_authoring.db.database import Database
from novel_authoring.ingest.service import ingest_book
from novel_authoring.storage.layout import BookLayout
from novel_authoring.storage.migration import (
    MigrationOptions,
    _path_mapping,
    _rewrite_database_paths,
    migrate_legacy,
)
from novel_authoring.workflows.handoffs import (
    copy_instruction,
    create_initialization_handoff,
)

_PATH_COLUMNS = (
    "task_directory",
    "prompt_path",
    "task_manifest_path",
    "output_schema_path",
    "result_path",
    "event_log_path",
)


def _legacy_book(tmp_path: Path) -> tuple[Path, Path]:
    source = tmp_path / "source"
    source.mkdir()
    (source / "story.md").write_text(
        "第1章 测试\n\n潮声盖过了警报。\n\n第2章 余波\n\n灯塔重新亮起。\n",
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    ingest_book(
        book_id="canonical-book",
        title="Canonical Book",
        source_root=source,
        workspace_root=workspace,
        settings=load_settings(),
    )
    return source, workspace / "canonical-book"


def _relocate_handoff_row(
    database: Database, handoff_id: str, old_root: Path, new_root: Path
) -> None:
    """Move a legacy handoff directory outside editions/*/handoffs and update the row."""

    new_root.parent.mkdir(parents=True, exist_ok=True)
    old_root.rename(new_root)
    with database.connect() as connection:
        for column in _PATH_COLUMNS:
            connection.execute(
                f'UPDATE workflow_handoffs SET "{column}"=REPLACE("{column}", ?, ?) '
                "WHERE handoff_id=?",
                (str(old_root), str(new_root), handoff_id),
            )


def _handoff_row(database: Database, handoff_id: str) -> dict[str, str]:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT * FROM workflow_handoffs WHERE handoff_id=?", (handoff_id,)
        ).fetchone()
    assert row is not None
    payload = dict(row)
    return {key: str(value) for key, value in payload.items()}


def test_migrate_legacy_real_handoff_rows(tmp_path: Path) -> None:
    source, workspace = _legacy_book(tmp_path)
    database = Database(workspace / "state.sqlite3")

    real = create_initialization_handoff(
        database, "canonical-book", requested_stage="NOVEL_INITIALIZATION"
    )
    real_id = str(real["handoff_id"])
    real_dir = Path(str(real["task_directory"]))
    # Legacy 布局：prompt.md/result.json 平铺在 task_directory 下。
    assert (real_dir / "prompt.md").is_file()
    assert (real_dir / "result.json").is_file()
    assert real_dir.parent.name == "handoffs"

    # W3 场景：把第二个 handoff 行搬到不会被 _import_handoff 重定位的目录
    # （迁移时只会被 _copy_tree_no_symlink 原样复制到 writing/）。
    stray = create_initialization_handoff(
        database, "canonical-book", requested_stage="NOVEL_INITIALIZATION"
    )
    stray_id = str(stray["handoff_id"])
    stray_old = Path(str(stray["task_directory"]))
    stray_new = workspace / "misc" / stray_id
    _relocate_handoff_row(database, stray_id, stray_old, stray_new)
    assert (stray_new / "prompt.md").is_file()

    library = tmp_path / "library"
    result = migrate_legacy(
        MigrationOptions(
            book_id="canonical-book",
            source_root=source,
            workspace_root=workspace,
            library_root=library,
            apply=True,
        )
    )
    assert result.plan.status == "APPLIED"

    paths = BookLayout(library).for_book("canonical-book")
    migrated = Database(paths.database)

    # 真实 handoff：被 _import_handoff 重定位，路径对齐到 input//output/。
    real_row = _handoff_row(migrated, real_id)
    operation = paths.edition("base").operations / real_id
    assert Path(real_row["task_directory"]) == operation
    assert Path(real_row["prompt_path"]) == operation / "input" / "prompt.md"
    assert Path(real_row["prompt_path"]).is_file()
    assert Path(real_row["result_path"]) == operation / "output" / "result.json"
    assert Path(real_row["result_path"]).is_file()
    expected_prompt = (operation / "input" / "prompt.md").read_text(encoding="utf-8")
    instruction = copy_instruction(migrated, real_id, library_root=library)
    assert instruction.startswith(expected_prompt.rstrip())
    assert f'--library-root "{library.resolve()}"' in instruction

    # W3：非重定位行只经过前缀改写，保持平铺文件名，不被误改成 input//output/。
    stray_row = _handoff_row(migrated, stray_id)
    stray_target = paths.edition("base").writing / "misc" / stray_id
    assert Path(stray_row["task_directory"]) == stray_target
    assert Path(stray_row["prompt_path"]) == stray_target / "prompt.md"
    assert Path(stray_row["prompt_path"]).is_file()
    assert Path(stray_row["result_path"]) == stray_target / "result.json"
    assert Path(stray_row["result_path"]).is_file()

    # 幂等：重复执行同一套路径改写不再产生任何变化。
    assert _rewrite_database_paths(paths.database, _path_mapping(source, workspace, paths)) == 0
