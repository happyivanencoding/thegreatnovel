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


def test_chapter_primary_action_is_workflow_driven_and_advanced_controls_are_scoped() -> None:
    assert 'id="generate-prompt"' in TEMPLATE
    assert 'id="chapter-generation-target"' in TEMPLATE
    assert 'id="prompt-mode-control"' in TEMPLATE
    assert 'id="chapter-advanced-actions"' in TEMPLATE
    assert 'id="state-delta-block"' in TEMPLATE
    assert 'id="template-editor"' in TEMPLATE
    assert 'id="save-memory"' in TEMPLATE
    assert 'id="edit-future10"' in TEMPLATE
    assert "chapterActionForNode" in APP_JS
    assert "generateCurrentChapterAction" in APP_JS
    assert "next_actionable_node" in APP_JS


def test_workspace_hides_path_and_keeps_prompt_response_in_drawer_mount() -> None:
    assert 'class="workspace-info"' not in TEMPLATE
    assert 'id="workspace-path"' in TEMPLATE
    assert 'id="prompt-response-advanced"' in TEMPLATE
    assert '"prompt-mode-control", "prompt-response-advanced"' in APP_JS
    assert 'navigateToView("tools", "打开 Prompt Templates")' in APP_JS
    assert 'navigateToView("memory", "打开记忆编辑区")' in APP_JS
