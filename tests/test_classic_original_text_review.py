from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "novel-original-text-review"
    / "scripts"
    / "classic_text.py"
)
SPEC = importlib.util.spec_from_file_location("classic_text", SCRIPT)
assert SPEC and SPEC.loader
classic_text = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = classic_text
SPEC.loader.exec_module(classic_text)


def _write_book(root: Path, name: str, text: str, encoding: str = "utf-8") -> Path:
    path = root / "01、玄幻" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode(encoding))
    return path


def test_resolve_prefers_exact_original_over_sequel(tmp_path: Path) -> None:
    original = _write_book(tmp_path, "《斗罗大陆》（校对版全本）.txt", "第一章 开始\n正文")
    _write_book(tmp_path, "《斗罗大陆II绝世唐门》（校对版全本）.txt", "第一章 续作\n正文")

    book, alternatives = classic_text.resolve_book("斗罗大陆", (tmp_path,))

    assert book.path == original
    assert alternatives and "II绝世唐门" in alternatives[0].title


def test_alias_resolves_doupo_cangqiong_to_local_doupo(tmp_path: Path) -> None:
    expected = _write_book(tmp_path, "《斗破》（校对版全本）.txt", "第1章 陨落的天才\n正文")

    book, _ = classic_text.resolve_book("斗破苍穹", (tmp_path,))

    assert book.path == expected


def test_gb18030_and_chinese_number_chapters_are_parsed(tmp_path: Path) -> None:
    path = _write_book(
        tmp_path,
        "《经典样本》（精校版全本）.txt",
        "书名\n第一章 起点\n甲乙\n第二章 转折\n丙丁\n第十一章 后段\n戊己",
        "gb18030",
    )

    text, encoding = classic_text.read_book(path)
    chapters = classic_text.parse_chapters(text)

    assert encoding == "gb18030"
    assert [chapter.number for chapter in chapters] == [1, 2, 11]
    assert chapters[1].heading == "第二章 转折"
    assert chapters[1].start_line == 4


def test_search_returns_locator_without_copying_raw_text(tmp_path: Path) -> None:
    _write_book(
        tmp_path,
        "《场景样本》.txt",
        "第一章 开始\n普通生活。\n第二章 多人战斗\n东门战斗。西台战斗。人物换位。\n第三章 余波\n安静下来。",
    )
    book, _ = classic_text.resolve_book("场景样本", (tmp_path,))
    text, _ = classic_text.read_book(book.path)
    rows = classic_text.search_chapters(classic_text.parse_chapters(text), "战斗 换位", 3)

    assert rows[0]["chapter"] == 2
    assert rows[0]["heading"] == "第二章 多人战斗"
    assert "text" not in rows[0]
    assert rows[0]["source_lines"] == [3, 4]


def test_window_writes_continuous_receipt_and_text(tmp_path: Path) -> None:
    _write_book(
        tmp_path,
        "《窗口样本》.txt",
        "第一章 一\nA\n第二章 二\nB\n第三章 三\nC",
    )
    book, _ = classic_text.resolve_book("窗口样本", (tmp_path,))
    text, encoding = classic_text.read_book(book.path)
    chapters = classic_text.parse_chapters(text)
    selected = chapters[0:3]
    rendered = classic_text.window_text(book, encoding, selected)

    assert "continuous_window: YES" in rendered
    assert "gbrain_used_as_original_evidence: NO" in rendered
    assert "第一章 一" in rendered
    assert "第二章 二" in rendered
    assert "第三章 三" in rendered
    assert f"source_path: {book.path}" in rendered


def test_duplicate_chapter_numbers_require_unique_ordinal(tmp_path: Path) -> None:
    _write_book(
        tmp_path,
        "《分卷样本》.txt",
        "第一章 卷一起点\nA\n第二章 卷一后续\nB\n第一章 卷二起点\nC",
    )
    book, _ = classic_text.resolve_book("分卷样本", (tmp_path,))
    text, _ = classic_text.read_book(book.path)
    chapters = classic_text.parse_chapters(text)

    try:
        classic_text.choose_chapter(chapters, number=1)
    except LookupError as error:
        assert "--ordinal" in str(error)
    else:
        raise AssertionError("重复章号必须要求唯一 ordinal")

    assert classic_text.choose_chapter(chapters, ordinal=3).heading == "第一章 卷二起点"
