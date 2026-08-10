(function () {
  "use strict";

  var rootSelector = "[data-workbench-shell]";

  function root() { return document.querySelector(rootSelector); }
  function csrfToken() { var meta = document.querySelector('meta[name="csrf-token"]'); return meta ? meta.content : ""; }
  function json(value, fallback) { try { return JSON.parse(value); } catch (error) { return fallback; } }
  function scopedKey(current) { return "novel-workbench-v2.2:" + current.dataset.bookId + ":" + current.dataset.editionId; }
  function number(value) { return Number.isFinite(Number(value)) ? Number(value) : 0; }

  function captureNavigationState(current) {
    if (!current) return null;
    var leftContent = current.querySelector(".wb-left-pane .wb-pane-content");
    var leftTree = current.querySelector(".wb-tree");
    var center = current.querySelector(".wb-center-scroll");
    var right = current.querySelector(".wb-editor-scroll");
    return {
      leftPaneScrollTop: leftContent ? leftContent.scrollTop : 0,
      leftTreeScrollTop: leftTree ? leftTree.scrollTop : 0,
      leftTreeScrollLeft: leftTree ? leftTree.scrollLeft : 0,
      centerScrollTop: center ? center.scrollTop : 0,
      centerScrollLeft: center ? center.scrollLeft : 0,
      rightScrollTop: right ? right.scrollTop : 0,
      rightScrollLeft: right ? right.scrollLeft : 0,
      openExplorerSections: Array.from(current.querySelectorAll("details[data-explorer-section][open]")).map(function (item) { return item.dataset.explorerSection; }),
      activeMainMode: current.dataset.activeMode || "continue",
      activeRightTab: current.dataset.activeRightTab || "prose",
      activeStateTab: current.dataset.activeStateTab || "overview",
      activeAnalysisDimension: current.dataset.activeAnalysisDimension || "",
      selectedChapter: current.dataset.currentChapterId || "",
      selectedCharacter: current.dataset.selectedCharacterId || "",
      leftCollapsed: current.classList.contains("is-left-collapsed"),
      rightCollapsed: current.classList.contains("is-right-collapsed"),
      paneWidths: {
        left: current.style.getPropertyValue("--wb-left") || getComputedStyle(current).getPropertyValue("--wb-left"),
        right: current.style.getPropertyValue("--wb-right") || getComputedStyle(current).getPropertyValue("--wb-right")
      }
    };
  }

  function saveFallback(current, state) {
    if (!current || !state) return;
    try { sessionStorage.setItem(scopedKey(current), JSON.stringify(state)); } catch (error) { /* optional */ }
  }

  function readFallback(current) {
    if (!current) return null;
    try { return json(sessionStorage.getItem(scopedKey(current)) || "null", null); } catch (error) { return null; }
  }

  function restoreDetails(current, state) {
    if (!state || !Array.isArray(state.openExplorerSections)) return;
    var open = new Set(state.openExplorerSections);
    current.querySelectorAll("details[data-explorer-section]").forEach(function (item) { item.open = open.has(item.dataset.explorerSection); });
  }

  function restoreLayout(current, state) {
    if (!state) return;
    if (state.paneWidths && state.paneWidths.left) current.style.setProperty("--wb-left", state.paneWidths.left);
    if (state.paneWidths && state.paneWidths.right) current.style.setProperty("--wb-right", state.paneWidths.right);
    current.classList.toggle("is-left-collapsed", Boolean(state.leftCollapsed));
    current.classList.toggle("is-right-collapsed", Boolean(state.rightCollapsed));
    updatePaneButtons(current);
  }

  function restoreScroll(current, state) {
    if (!state) return;
    var values = [
      [current.querySelector(".wb-left-pane .wb-pane-content"), "leftPaneScrollTop", null],
      [current.querySelector(".wb-tree"), "leftTreeScrollTop", "leftTreeScrollLeft"],
      [current.querySelector(".wb-center-scroll"), "centerScrollTop", "centerScrollLeft"],
      [current.querySelector(".wb-editor-scroll"), "rightScrollTop", "rightScrollLeft"]
    ];
    values.forEach(function (entry) {
      if (!entry[0]) return;
      entry[0].scrollTop = number(state[entry[1]]);
      if (entry[2]) entry[0].scrollLeft = number(state[entry[2]]);
    });
  }

  function restoreNavigationState(current, state) {
    if (!state) return;
    restoreDetails(current, state);
    restoreLayout(current, state);
    // Restore before the next paint so replacing the workbench shell never
    // exposes a frame at scrollTop=0.  The two animation-frame passes cover
    // layout changes caused by details and dynamically rendered state views.
    restoreScroll(current, state);
    requestAnimationFrame(function () {
      restoreScroll(current, state);
      requestAnimationFrame(function () { restoreScroll(current, state); });
    });
  }

  function updatePaneButtons(current) {
    ["left", "right"].forEach(function (side) {
      var collapsed = current.classList.contains("is-" + side + "-collapsed");
      var label = (collapsed ? "展开" : "隐藏") + (side === "left" ? "左栏" : "右栏");
      var icon = side === "left" ? (collapsed ? "›" : "‹") : (collapsed ? "‹" : "›");
      current.querySelectorAll('[data-toggle-pane="' + side + '"]').forEach(function (button) { button.setAttribute("aria-label", label); button.title = label; var symbol = button.querySelector("[data-pane-toggle-icon]"); if (symbol) symbol.textContent = icon; });
    });
  }

  function bindLayout(current) {
    updatePaneButtons(current);
    current.querySelectorAll("[data-toggle-pane]").forEach(function (button) {
      button.addEventListener("click", function () { current.classList.toggle("is-" + button.dataset.togglePane + "-collapsed"); updatePaneButtons(current); saveFallback(current, captureNavigationState(current)); });
    });
    current.querySelectorAll("[data-resizer]").forEach(function (resizer) {
      resizer.addEventListener("pointerdown", function (event) {
        if (innerWidth < 900) return;
        event.preventDefault();
        var side = resizer.dataset.resizer;
        function move(moveEvent) { var maximum = Math.min(innerWidth * 0.45, side === "left" ? innerWidth - 520 : innerWidth * 0.5); var width = side === "left" ? moveEvent.clientX : innerWidth - moveEvent.clientX; current.style.setProperty(side === "left" ? "--wb-left" : "--wb-right", Math.max(side === "left" ? 230 : 300, Math.min(maximum, width)) + "px"); }
        function stop() { document.removeEventListener("pointermove", move); document.removeEventListener("pointerup", stop); saveFallback(current, captureNavigationState(current)); }
        document.addEventListener("pointermove", move); document.addEventListener("pointerup", stop, { once: true });
      });
    });
  }

  function targetUrl(href, current) {
    var url = new URL(href, location.href);
    if (!url.searchParams.has("mode")) url.searchParams.set("mode", current.dataset.activeMode || "continue");
    if (!url.searchParams.has("right_tab")) url.searchParams.set("right_tab", current.dataset.activeRightTab || "prose");
    if (!url.searchParams.has("state_tab") && (current.dataset.activeMode === "state" || url.searchParams.get("mode") === "state")) url.searchParams.set("state_tab", current.dataset.activeStateTab || "overview");
    if (!url.searchParams.has("character_id") && current.dataset.selectedCharacterId) url.searchParams.set("character_id", current.dataset.selectedCharacterId);
    return url.href;
  }

  function replaceChrome(parsed) {
    [["[data-wb-breadcrumb]", "[data-wb-breadcrumb]"], [".wb-status-chip", ".wb-status-chip"]].forEach(function (pair) { var next = parsed.querySelector(pair[0]); var present = document.querySelector(pair[1]); if (next && present) present.replaceWith(next); });
    if (parsed.title) document.title = parsed.title;
  }

  function fullNavigate(href, state) { var current = root(); saveFallback(current, state); location.href = href; }

  function loadWorkbench(href, options) {
    var current = root();
    if (!current) { location.href = href; return; }
    var desired = options && options.restoreState ? options.restoreState : captureNavigationState(current);
    var resolved = targetUrl(href, current);
    if (!options || !options.fromPop) {
      history.replaceState({ workbenchState: captureNavigationState(current) }, "", location.href);
    }
    saveFallback(current, desired);
    fetch(resolved, { headers: { Accept: "text/html" } }).then(function (response) { if (!response.ok) throw new Error("load"); return response.text(); }).then(function (html) {
      var parsed = new DOMParser().parseFromString(html, "text/html");
      var next = parsed.querySelector(rootSelector);
      var present = root();
      if (!next || !present) { fullNavigate(resolved, desired); return; }
      restoreDetails(next, desired);
      restoreLayout(next, desired);
      present.replaceWith(next);
      replaceChrome(parsed);
      initWorkbench(next);
      restoreNavigationState(next, desired);
      var state = { workbenchState: captureNavigationState(next) };
      if (options && options.push === false) history.replaceState(state, "", resolved); else history.pushState(state, "", resolved);
    }).catch(function () { fullNavigate(resolved, desired); });
  }

  function navigateQuery(current, changes) { var url = new URL(location.href); Object.keys(changes).forEach(function (key) { if (changes[key]) url.searchParams.set(key, changes[key]); else url.searchParams.delete(key); }); loadWorkbench(url.href, { push: true }); }

  function bindNavigation(current) {
    current.querySelectorAll("[data-workbench-navigation]").forEach(function (link) { link.addEventListener("click", function (event) { if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return; event.preventDefault(); loadWorkbench(link.href, { push: true }); }); });
    current.querySelectorAll("[data-wb-mode]").forEach(function (button) { button.addEventListener("click", function () { navigateQuery(current, { mode: button.dataset.wbMode, node: button.dataset.wbMode === "state" ? "state" : null }); }); });
    current.querySelectorAll("[data-wb-state-tab]").forEach(function (button) { button.addEventListener("click", function () { navigateQuery(current, { mode: "state", node: "state", state_tab: button.dataset.wbStateTab }); }); });
    current.querySelectorAll("[data-wb-editor-tab]").forEach(function (button) { button.addEventListener("click", function () { var tab = button.dataset.wbEditorTab; current.querySelectorAll("[data-wb-editor-tab]").forEach(function (item) { var active = item === button; item.setAttribute("aria-selected", active ? "true" : "false"); item.classList.toggle("is-active", active); }); var prose = current.querySelector("[data-wb-editor-prose]"); if (prose) prose.hidden = tab !== "prose"; current.querySelectorAll("[data-wb-editor-secondary]").forEach(function (panel) { panel.hidden = panel.dataset.wbEditorSecondary !== tab; }); current.dataset.activeRightTab = tab; var url = new URL(location.href); url.searchParams.set("right_tab", tab); history.replaceState({ workbenchState: captureNavigationState(current) }, "", url.href); }); });
  }

  function authorPath(current) { return "/api/books/" + encodeURIComponent(current.dataset.bookId) + "/editions/" + encodeURIComponent(current.dataset.editionId) + "/author-commands"; }
  function postJson(url, body) { return fetch(url, { method: "POST", headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() }, body: JSON.stringify(body) }).then(function (response) { return response.json().then(function (value) { if (!response.ok) throw new Error((value.error && value.error.message) || value.detail || "请求失败"); return value; }); }); }
  function postAuthorCommand(current, command) { command.chapter_id = current.dataset.currentChapterId || null; command.character_id = current.dataset.selectedCharacterId || null; return postJson(authorPath(current), command); }
  function formPayload(form) { var payload = {}; new FormData(form).forEach(function (value, key) { if (String(value).trim()) payload[key] = value; }); return payload; }
  function feedback(target, message, rejected) { var node = target.querySelector(".wb-command-feedback") || target.querySelector("[data-item-modal-feedback]"); if (!node) { node = document.createElement("p"); node.className = "wb-command-feedback"; target.appendChild(node); } node.textContent = message; node.classList.toggle("is-error", Boolean(rejected)); }

  function bindCommands(current) {
    current.querySelectorAll("[data-author-command-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); postAuthorCommand(current, { command_type: form.dataset.commandType, payload: formPayload(form) }).then(function (result) { feedback(form, result.message, result.result === "REJECTED"); if (result.result === "PLANNED") setTimeout(function () { loadWorkbench(location.href, { push: false }); }, 350); }).catch(function (error) { feedback(form, error.message, true); }); }); });
  }

  function inspectorLine(label, value) { var row = document.createElement("div"); var term = document.createElement("span"); var content = document.createElement("strong"); term.textContent = label; content.textContent = value == null || value === "" ? "尚未知" : String(value); row.appendChild(term); row.appendChild(content); return row; }
  function showInspector(current, record, kind) {
    var panel = current.querySelector("[data-wb-inspector]"); if (!panel) return;
    panel.innerHTML = "";
    var header = document.createElement("header"); var kicker = document.createElement("span"); var title = document.createElement("h3"); kicker.textContent = kind || record.category || "状态记录"; title.textContent = record.name || record.topic_name || record.label || ((record.from_entity_id || "") + " ↔ " + (record.to_entity_id || "")) || "未命名记录"; header.appendChild(kicker); header.appendChild(title); panel.appendChild(header);
    var grid = document.createElement("div"); grid.className = "wb-inspector-grid";
    [["信息层", record.layer || record.current_layer], ["状态", record.state_label || record.status_label || record.state || record.status], ["首次获得", record.first_acquired_chapter_ordinal], ["首次确认", record.first_confirmed_chapter_ordinal], ["最近确认", record.recent_confirmed_chapter_ordinal || record.evidence_chapter_ordinal || record.chapter_ordinal], ["持有者", record.current_holder_id || record.owner_id], ["数量", record.quantity], ["槽位", record.slot]].forEach(function (item) { if (item[1] != null && item[1] !== "") grid.appendChild(inspectorLine(item[0], item[1])); }); panel.appendChild(grid);
    var description = document.createElement("p"); description.textContent = record.description || record.statement || record.evidence || "当前没有额外说明。"; panel.appendChild(description);
    var spans = record.source_span_ids || []; var evidence = document.createElement("small"); evidence.textContent = "证据：" + (spans.length ? spans.join("、") : "尚无 source span"); panel.appendChild(evidence);
    if (Array.isArray(record.who_knows)) { var heading = document.createElement("h4"); heading.textContent = "Who Knows"; panel.appendChild(heading); var list = document.createElement("ul"); list.className = "wb-who-knows"; record.who_knows.forEach(function (cell) { var item = document.createElement("li"); item.textContent = (cell.knower_name || cell.knower_id) + " · " + (cell.state_label || "尚未知"); list.appendChild(item); }); if (!record.who_knows.length) { var empty = document.createElement("li"); empty.textContent = "所有人物均为尚未知"; list.appendChild(empty); } panel.appendChild(list); }
    panel.dataset.inspectorKind = kind || "record";
  }

  function bindInspector(current) {
    current.querySelectorAll("[data-inspector-record]").forEach(function (control) { var activate = function () { showInspector(current, json(control.dataset.inspectorRecord || "{}", {}), control.dataset.inspectorKind); }; control.addEventListener("click", activate); control.addEventListener("keydown", function (event) { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); activate(); } }); });
  }

  function bindRelationshipGraph(current) {
    current.querySelectorAll("[data-wb-relationship-graph]").forEach(function (container) {
      var graph = json(container.dataset.graph || "{}", {}); var nodes = graph.nodes || []; var edges = graph.edges || []; if (!nodes.length) return;
      container.innerHTML = ""; var width = 760; var height = Math.max(190, Math.ceil(nodes.length / 4) * 140); var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg"); svg.setAttribute("viewBox", "0 0 " + width + " " + height); var positions = {};
      nodes.forEach(function (node, index) { positions[node.node_id] = { x: 100 + (index % 4) * 185, y: 70 + Math.floor(index / 4) * 130 }; });
      edges.forEach(function (edge) { var from = positions[edge.from_id]; var to = positions[edge.to_id]; if (!from || !to) return; var group = document.createElementNS("http://www.w3.org/2000/svg", "g"); group.setAttribute("class", "wb-relationship-edge-control"); group.setAttribute("role", "button"); group.setAttribute("tabindex", "0"); group.setAttribute("aria-label", edge.label || "关系边"); group.dataset.edgeId = edge.edge_id; ["wb-relationship-edge-hit", "wb-relationship-edge"].forEach(function (className) { var line = document.createElementNS("http://www.w3.org/2000/svg", "line"); line.setAttribute("x1", from.x); line.setAttribute("y1", from.y); line.setAttribute("x2", to.x); line.setAttribute("y2", to.y); line.setAttribute("class", className); group.appendChild(line); }); var activate = function () { showInspector(current, edge.inspector || edge, "relationship"); }; group.addEventListener("click", activate); group.addEventListener("keydown", function (event) { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); activate(); } }); svg.appendChild(group); });
      nodes.forEach(function (node) { var position = positions[node.node_id]; var group = document.createElementNS("http://www.w3.org/2000/svg", "g"); group.setAttribute("class", "wb-relationship-node wb-node-" + String(node.node_type || "unknown").toLowerCase()); var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle"); circle.setAttribute("cx", position.x); circle.setAttribute("cy", position.y); circle.setAttribute("r", "26"); var label = document.createElementNS("http://www.w3.org/2000/svg", "text"); label.setAttribute("x", position.x); label.setAttribute("y", position.y + 44); label.setAttribute("text-anchor", "middle"); label.textContent = node.name; group.appendChild(circle); group.appendChild(label); svg.appendChild(group); }); container.appendChild(svg);
    });
  }

  function bindItemModal(current) {
    var dialog = current.querySelector("[data-item-modal]"); if (!dialog) return;
    current.querySelectorAll("[data-open-item-modal]").forEach(function (button) { button.addEventListener("click", function () { dialog.showModal(); }); }); current.querySelectorAll("[data-close-item-modal]").forEach(function (button) { button.addEventListener("click", function () { dialog.close(); }); });
    var form = dialog.querySelector("[data-item-modal-form]"); form.addEventListener("submit", function (event) { event.preventDefault(); var values = formPayload(form); var scope = values.intent_scope; var command = scope === "CURRENT" ? { command_type: "DROP_ITEM", payload: { item_id: values.name, destination: "CURRENT_INVENTORY" } } : scope === "FUTURE" ? { command_type: "CREATE_FUTURE_ITEM", payload: values } : { command_type: "CREATE_TASK", payload: { title: "候选物品：" + values.name, task_type: "CANDIDATE_ITEM", description: values.description || "", subject_type: "ITEM", subject_id: values.name } };
      postAuthorCommand(current, command).then(function (result) { feedback(form, result.message, result.result === "REJECTED"); if (scope === "CURRENT" && result.result === "REJECTED") { var actions = document.createElement("div"); actions.className = "wb-modal-actions wb-semantic-actions"; [["转为未来获得", "FUTURE"], ["创建改写请求", "REVISION"], ["取消", "CANCEL"]].forEach(function (entry) { var button = document.createElement("button"); button.type = "button"; button.className = "button compact"; button.textContent = entry[0]; button.addEventListener("click", function () { if (entry[1] === "FUTURE") { form.querySelector('[name="intent_scope"]').value = "FUTURE"; form.requestSubmit(); } else if (entry[1] === "REVISION") { postAuthorCommand(current, { command_type: "CREATE_REVISION_REQUEST", payload: { title: "为当前章节加入物品：" + values.name, item_id: values.name, description: values.description || "" } }).then(function (reply) { feedback(form, reply.message, false); }); } else dialog.close(); }); actions.appendChild(button); }); form.appendChild(actions); } else if (result.result === "PLANNED") setTimeout(function () { dialog.close(); loadWorkbench(location.href, { push: false }); }, 400); }).catch(function (error) { feedback(form, error.message, true); });
    });
  }

  function profileBase(current) { return "/api/books/" + encodeURIComponent(current.dataset.bookId) + "/editions/" + encodeURIComponent(current.dataset.editionId) + "/book-profile"; }
  function bindProfile(current) {
    current.querySelectorAll("[data-profile-edit-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); postJson(profileBase(current) + "/edits", formPayload(form)).then(function () { feedback(form, "已保存新 Profile 版本。", false); setTimeout(function () { loadWorkbench(location.href, { push: false }); }, 300); }).catch(function (error) { feedback(form, error.message, true); }); }); });
    current.querySelectorAll("[data-profile-reanalyze]").forEach(function (button) { button.addEventListener("click", function () { postJson(profileBase(current) + "/proposals", { source_type: "AUTHOR_REANALYSIS", summary: "作者请求重新分析九维全书画像" }).then(function () { loadWorkbench(location.href, { push: false }); }).catch(function (error) { button.textContent = error.message; }); }); });
    current.querySelectorAll("[data-profile-proposal-action]").forEach(function (button) { button.addEventListener("click", function () { postJson(profileBase(current) + "/proposals/" + encodeURIComponent(button.dataset.proposalId) + "/resolve", { action: button.dataset.profileProposalAction }).then(function () { loadWorkbench(location.href, { push: false }); }).catch(function (error) { button.textContent = error.message; }); }); });
  }

  function bindDraft(current) { current.querySelectorAll("[data-wb-editor]").forEach(function (editor) { var counter = current.querySelector("[data-wb-word-count]"); var update = function () { if (counter) counter.textContent = Array.from(editor.value || "").length + " 字"; }; editor.addEventListener("input", update); update(); }); current.querySelectorAll("[data-wb-draft-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); var editor = form.querySelector('[name="content"]'); var expected = form.querySelector('[name="expected_content_sha256"]'); postJson(form.action, { content: editor.value, expected_content_sha256: expected ? expected.value : null }).then(function () { loadWorkbench(location.href, { push: false }); }).catch(function (error) { feedback(form, error.message, true); }); }); }); }

  function bindWorkflow(current) {
    current.querySelectorAll("[data-workflow-workspace]").forEach(function (workspace) { var buttons = workspace.querySelectorAll("[data-workflow-mode]"); var panels = workspace.querySelectorAll("[data-workflow-mode-panel]"); function activate(target) { buttons.forEach(function (button) { button.setAttribute("aria-selected", button.dataset.workflowMode === target ? "true" : "false"); }); panels.forEach(function (panel) { panel.hidden = panel.dataset.workflowModePanel !== target; }); } buttons.forEach(function (button) { button.addEventListener("click", function () { activate(button.dataset.workflowMode); }); }); activate(workspace.dataset.workflowInitialMode || "continue"); });
    current.querySelectorAll("[data-workflow-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); var payload = {}; new FormData(form).forEach(function (value, key) { if (key === "innovation_focus" || key === "author_task_ids") { payload[key] = payload[key] || []; payload[key].push(String(value)); } else payload[key] = value; }); postJson(form.action, payload).then(function () { loadWorkbench(location.href, { push: false }); }).catch(function (error) { var node = form.querySelector("[data-workflow-feedback]"); if (node) { node.hidden = false; node.textContent = error.message; } }); }); });
  }

  function bindSearch(current) { var search = current.querySelector("[data-wb-chapter-search]"); if (!search) return; search.addEventListener("input", function () { var query = search.value.trim().toLowerCase(); current.querySelectorAll("[data-wb-chapter-item]").forEach(function (item) { item.hidden = Boolean(query && item.textContent.toLowerCase().indexOf(query) === -1); }); }); }

  function initWorkbench(current) { bindLayout(current); bindNavigation(current); bindCommands(current); bindInspector(current); bindRelationshipGraph(current); bindItemModal(current); bindProfile(current); bindDraft(current); bindWorkflow(current); bindSearch(current); current.querySelectorAll("details[data-explorer-section]").forEach(function (item) { item.addEventListener("toggle", function () { saveFallback(current, captureNavigationState(current)); }); }); }

  window.addEventListener("popstate", function (event) { loadWorkbench(location.href, { push: false, fromPop: true, restoreState: event.state && event.state.workbenchState ? event.state.workbenchState : readFallback(root()) }); });
  var initial = root(); if (initial) { var state = history.state && history.state.workbenchState ? history.state.workbenchState : readFallback(initial); restoreDetails(initial, state); restoreLayout(initial, state); initWorkbench(initial); restoreNavigationState(initial, state); history.replaceState({ workbenchState: captureNavigationState(initial) }, "", location.href); }
}());
