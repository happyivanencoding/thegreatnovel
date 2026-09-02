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
    assert "snapshot.prompt === currentAgentDockPromptForJob(job)" in auto_fill_guard
    assert "snapshot.sourceSnapshot === agentDockSourceSnapshot(job)" in auto_fill_guard
    assert "editor.value === snapshot.initialValue" in auto_fill_guard
    assert "agentDockEditorVersion(editor) === snapshot.editorVersion" in auto_fill_guard
    assert "editorVersion: agentDockEditorVersion(editor)" in APP_JS
    assert "markAgentDockEditorEdited" in APP_JS
    assert "responseEditorForJob(job).value = job.output_text" in completion
    assert "saveRunResponseForMode" not in completion
    assert "adoptRunSource" not in completion


def test_agentdock_long_runs_have_honest_activity_anchor_without_fake_eta() -> None:
    for element_id in (
        "agentdock-progress-anchor", "agentdock-progress-phase", "agentdock-progress-elapsed",
        "agentdock-phase-track", "agentdock-current-activity", "agentdock-heartbeat",
        "agentdock-plan-list", "agentdock-activity-list", "agentdock-active-cancel",
    ):
        assert TEMPLATE.count(f'id="{element_id}"') == 1
    for function_name in (
        "renderAgentDockFocus", "refreshAgentDockFocusClock", "agentHeartbeatText",
        "showAgentDockNotice", "updateDocumentRunState", "maybeShowAgentLongRunReminder",
    ):
        assert f"function {function_name}" in APP_JS
    assert "activity_quiet_seconds" in APP_JS
    assert "plan_completed" in APP_JS and "tool_counts" in APP_JS
    assert "长推理可能暂时没有工具事件" in APP_JS
    assert "预计剩余" not in APP_JS
    assert "progress_percent" not in APP_JS
    assert "AGENT_LONG_RUN_REMINDERS = [60, 180, 300, 600, 900, 1200, 1800, 2700]" in APP_JS
    assert "可以继续写别处，也可随时取消" in APP_JS
    assert "window.setInterval(refreshAgentDockFocusClock, 1000)" in APP_JS
    assert 'auth_state": "checked_when_job_starts"' not in APP_JS
    assert "ChatGPT 登录将在启动时确认" in APP_JS
    assert 'timeoutMs: 20_000' in APP_JS
    assert "AbortController" in APP_JS
    poller = APP_JS.split("async function pollAgentDockJob(jobId)", 1)[1].split("async function cancelAgentDockJob", 1)[0]
    assert "consecutiveStatusErrors" in poller
    assert "continue;" in poller
    assert "trackAgentDockPending(jobId, {}, false)" in poller.split("if (lost)", 1)[1]


def test_agentdock_routes_each_production_stage_to_the_frozen_model_profile() -> None:
    routing = APP_JS.split("function agentDockExecutionProfile(mode)", 1)[1].split("function externalArtifactForMode", 1)[0]
    for mode in (
        "world_vision", "world_expansion", "power_seed", "human_seed", "outline",
        "director", "context_curator", "authority_reviser",
    ):
        assert f'"{mode}"' in routing
    assert 'return { model: "gpt-5.6-luna", reasoningEffort: "high" }' in routing
    assert '["idea", "story_refresh"]' in routing
    assert 'return { model: "gpt-5.6-sol", reasoningEffort: "high" }' in routing
    assert '["premise_compiler", "primary_writer"]' in routing
    assert 'return { model: "gpt-5.6-terra", reasoningEffort: "high" }' in routing


def test_gbrain_is_structured_as_extract_compare_select_and_explicit_assembly() -> None:
    for element_id in (
        "gbrain-readiness", "gbrain-mode-badge", "gbrain-candidate-list", "gbrain-fixed-list",
        "gbrain-selection-count", "gbrain-select-all", "gbrain-clear-selection",
        "gbrain-selection-tray", "gbrain-compare", "gbrain-compare-dialog", "gbrain-compare-list",
        "gbrain-stale-banner", "gbrain-requery", "gbrain-assemble", "gbrain-discard",
        "gbrain-bundle-stage", "gbrain-bundle-state",
    ):
        assert TEMPLATE.count(f'id="{element_id}"') == 1
    for function_name in (
        "refreshGbrainStatus", "renderGbrainCandidates", "assembleGbrainSelection",
        "validateGbrainBundleForPrompt", "gbrainSelectionSignature", "openGbrainCompare",
        "currentGbrainContextSnapshot", "invalidateGbrainResults", "gbrainInspirationForPrompt",
    ):
        assert f"function {function_name}" in APP_JS or f"async function {function_name}" in APP_JS
    assert 'GBRAIN_ACTIVE_MODES = new Set(["world_vision", "world_expansion", "power_seed", "human_seed", "idea", "story_refresh", "outline"])' in APP_JS
    assert '$("gbrain-results").value = payload.result' not in APP_JS
    assert "candidate.formatted_block" in APP_JS
    assert "fixed_references" in APP_JS
    assert "state.gbrainSelected" in APP_JS
    assert "source: ${item.slug}" in APP_JS
    candidates = APP_JS.split("function renderGbrainCandidates(payload)", 1)[1].split("function renderGbrainCompare", 1)[0]
    assert "state.gbrainSelected = new Set();" in candidates
    assert "checkbox.checked = false" in APP_JS
    assert 'card.className = "gbrain-candidate-card"' in APP_JS
    assert "gbrainContextSnapshotMatches" in APP_JS
    assert 'gbrain_inspiration: gbrainInspirationForPrompt($("prompt-mode").value)' in APP_JS
    assert 'payload.mode === "human_seed"' in APP_JS
    assert "上一轮 Bundle 已保留" in APP_JS
    assert "const requestSnapshot = currentGbrainContextSnapshot()" in APP_JS
    assert "检索完成前上下文发生了变化" in APP_JS
    assert "作者现有查询已保留" in APP_JS
    assert 'state.gbrainBundleOrigin = "unbound_manual"' in APP_JS
    assert 'if (!state.gbrainRetrieval) return ""' in APP_JS
    assert "partial failures" in APP_JS
    assert '$("gbrain-query").disabled = pending || !gbrainModeAllowsRetrieval()' in APP_JS
    assert "validateGbrainBundleForPrompt(mode)" in APP_JS.split("async function generatePrompt()", 1)[1][:240]
    assert "/api/gbrain/status" in APP_JS
    assert 'aria-live="polite"' not in TEMPLATE.split('id="agentdock-mini-anchor"', 1)[1].split('</button>', 1)[0]


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
