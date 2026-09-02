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
        "creative-world-vision", "creative-power-seed", "creative-human-seed",
        "creative-character-card", "proposal-editor", "section-status",
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


def test_agentdock_uses_identity_guarded_responses_and_never_auto_applies_authority() -> None:
    for element_id in (
        "agentdock-panel", "agentdock-run-current", "agentdock-job-list",
        "agentdock-consult-prompt", "agentdock-consult-response",
    ):
        assert TEMPLATE.count(f'id="{element_id}"') == 1
    assert '<option value="agentdock_acp">' in TEMPLATE
    assert "function startAgentDockJob" in APP_JS
    assert "function pollAgentDockJob" in APP_JS
    completion = APP_JS.split('if (job.status === "completed")', 1)[1].split('} else if (job.status === "failed")', 1)[0]
    auto_fill_guard = APP_JS.split("function canAutoFillAgentDockJob(job)", 1)[1].split("async function startAgentDockJob", 1)[0]
    assert "canAutoFillAgentDockJob(job)" in completion
    assert "state.agentdockLatestLaunch" in auto_fill_guard
    assert "jobMatchesCurrentIdentity(job)" in auto_fill_guard
    assert "state.agentdockLaunchSnapshots" in auto_fill_guard
    assert "editor.value === snapshot.initialValue" in auto_fill_guard
    assert "agentDockEditorVersion(editor) === snapshot.editorVersion" in auto_fill_guard
    assert "editorVersion: agentDockEditorVersion(editor)" in APP_JS
    assert "markAgentDockEditorEdited" in APP_JS
    assert "responseEditorForJob(job).value = job.output_text" in completion
    assert "saveRunResponseForMode" not in completion
    assert "adoptRunSource" not in completion


def test_navigation_is_unique_and_batch_controls_use_existing_endpoints() -> None:
    targets = re.findall(r'data-view-target="([^"]+)"', TEMPLATE)
    assert len(targets) == len(set(targets)) == 6
    assert 'data-drawer-section="workflow-audit-section"' in TEMPLATE
    assert 'data-drawer-section="agentdock-run-log"' in TEMPLATE
    for element_id in (
        "story-structure-tree", "batch-compile-primary", "batch-run-primary", "batch-compile-delta",
        "batch-run-delta", "batch-preflight", "batch-adopt", "batch-load-state", "batch-primary-response",
        "batch-delta-response", "agentdock-result-preview", "agentdock-load-current",
    ):
        assert TEMPLATE.count(f'id="{element_id}"') == 1
    for endpoint in (
        "/api/batch/primary-prompt", "/api/batch/authority-reviser-prompt", "/api/batch/apply-authority-delta",
        "/batch/adopt-authority-delta",
    ):
        assert endpoint in APP_JS
    assert "gpt-5.6-terra" in APP_JS and "gpt-5.6-sol" in APP_JS
    assert "pollAgentDockJob(job.job_id)" in APP_JS
    assert "window.setTimeout(resolve, 1400)" in APP_JS
    assert 'if (job.workflow_mode === "state_delta") return "state_delta"' in APP_JS
    assert 'if (target === "state_delta") return $("state-delta-response")' in APP_JS
    assert "trackAgentDockPending(job.job_id, job, true)" in APP_JS
    assert "loadContinuityContextBefore(window.startChapter)" in APP_JS
    assert "batchPreflightMatchesCurrent" in APP_JS
    assert "handleBatchWindowChange" in APP_JS
    assert '$("batch-primary-response").addEventListener("input", invalidateBatchPrimaryDependents)' in APP_JS
    assert '$("batch-delta-response").addEventListener("input", invalidateBatchPreflight)' in APP_JS
    assert '"codex-response", "state-delta-response", "agentdock-consult-response"' in APP_JS
    assert 'markAgentDockEditorEdited(event.currentTarget)' in APP_JS
    assert "await loadCurrentChapterBody()" in APP_JS


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

def test_explicit_anonymous_human_prototype_selector_is_visible_but_default_off() -> None:
    assert 'id="human-prototype-selector"' in TEMPLATE
    assert '<option value="">普通 Human Seed（默认）</option>' in TEMPLATE
    assert '<option value="prism-wanderer-alpha">匿名私人原型实验</option>' in TEMPLATE
    assert 'prototype_id: $("human-prototype-selector")?.value || ""' in APP_JS
    assert 'invalidateGbrainResults("切换 Human Prototype")' in APP_JS


def test_premise_workspace_is_author_gated_without_selector_or_repair_loop() -> None:
    for element_id in (
        "premise-stage",
        "premise-candidates",
        "selected-premise",
        "premise-compiler-report",
        "generate-premise-forge-prompt",
        "generate-premise-batch-compiler",
        "generate-selected-premise-compiler",
        "approve-premise",
        "skip-premise",
        "premise-world-contract",
        "premise-power-contract",
        "premise-human-contract",
        "premise-story-contract",
    ):
        assert TEMPLATE.count(f'id="{element_id}"') == 1
    assert all(f'data-premise-select="S{number}"' in TEMPLATE for number in (1, 2, 3))
    assert "choosePremiseCandidate" in APP_JS
    assert "approvePremiseContract" in APP_JS
    assert "skipPremiseAperture" in APP_JS
    assert 'id="repair-premise"' not in TEMPLATE
    assert "autoSelectPremise" not in APP_JS

def test_exact_input_receipt_reuse_skips_executor_and_hydrates_saved_response() -> None:
    assert "runResponseEditorByMode" in APP_JS
    assert "hydrateReceiptReusedResponse" in APP_JS
    assert "manifest?.nodes?.[node]?.receipt_reused" in APP_JS
    block = APP_JS.split("if (node && manifest?.nodes?.[node]?.receipt_reused)", 1)[1].split("renderCodexTaskWrapper(mode);", 1)[0]
    assert "hydrateReceiptReusedResponse(mode, node)" in block
    assert "return;" in block
    assert "executeOpenAI" not in block
    assert "/response`" in APP_JS
