from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "src/story_mvp/templates/index.html").read_text(encoding="utf-8")
APP_JS = (ROOT / "src/story_mvp/static/app.js").read_text(encoding="utf-8")


def test_author_workspace_has_the_six_hash_views() -> None:
    assert all(f'href="#{view}"' in TEMPLATE for view in (
        "overview", "creative", "design", "chapter", "memory", "tools"
    ))
    assert 'id="overview-workspace"' in TEMPLATE
    assert 'id="memory-workspace"' in TEMPLATE
    assert 'id="tools-workspace"' in TEMPLATE


def test_existing_editors_are_single_sources_and_drawer_reuses_them() -> None:
    ids = re.findall(r'id="([^"]+)"', TEMPLATE)
    assert len(ids) == len(set(ids))
    for editor_id in (
        "creative-fantasy-seed", "proposal-editor", "section-status",
        "current-outline", "prompt-text", "codex-response", "chapter-body-for-save",
    ):
        assert TEMPLATE.count(f'id="{editor_id}"') == 1
    assert TEMPLATE.count('id="right-drawer"') == 1
    assert TEMPLATE.count('id="prompt-response-advanced"') == 1
    assert "mountRightDrawer();" in APP_JS


def test_reading_first_controls_keep_advanced_sources_explicit() -> None:
    assert 'class="source-details"' in TEMPLATE
    assert 'class="references-section"' in TEMPLATE
    assert 'id="toggle-design-editor"' in TEMPLATE
    assert 'id="toggle-chapter-context"' in TEMPLATE
    assert 'id="open-executor-drawer"' in TEMPLATE
    assert "initializeReadingState" in APP_JS
    assert "state.dirtyEditors" in APP_JS


def test_author_workspace_keeps_existing_prompt_and_save_paths() -> None:
    for function_name in (
        "promptPayload", "generatePrompt", "copyPrompt", "applyResponseToEditor",
        "applyOutlineToBook", "applyCanonIndexProposal", "saveBook", "approveChapter",
        "saveRunPromptForMode", "saveRunResponseForMode",
    ):
        assert f"function {function_name}" in APP_JS or f"async function {function_name}" in APP_JS
