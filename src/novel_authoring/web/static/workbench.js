(function () {
  "use strict";

  var rootSelector = "[data-workbench-shell]";

  function root() { return document.querySelector(rootSelector); }
  function csrfToken() { var meta = document.querySelector('meta[name="csrf-token"]'); return meta ? meta.content : ""; }
  function json(value, fallback) { try { return JSON.parse(value); } catch (error) { return fallback; } }
  function scopedKey(current) { return "novel-workbench-v2.4:" + current.dataset.bookId + ":" + current.dataset.editionId; }
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
      activeMainMode: current.dataset.activeMode || "home",
      activeAction: current.dataset.activeAction || "",
      activeRightTab: current.dataset.activeRightTab || "prose",
      activeStateTab: current.dataset.activeStateTab || "overview",
      activeAnalysisDimension: current.dataset.activeAnalysisDimension || "",
      selectedChapter: current.dataset.currentChapterId || "",
      selectedCharacter: current.dataset.selectedCharacterId || "",
      activityCenterOpen: !current.querySelector("[data-activity-center]").hidden,
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
    setActivityOpen(current, Boolean(state.activityCenterOpen), false);
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
    if (!url.searchParams.has("chapter_id") && !url.searchParams.has("draft_id") && current.dataset.currentChapterId) url.searchParams.set("chapter_id", current.dataset.currentChapterId);
    if (!url.searchParams.has("action") && current.dataset.activeAction && !url.searchParams.has("mode") && url.searchParams.get("node") === "chapter") url.searchParams.set("action", current.dataset.activeAction);
    if (!url.searchParams.has("mode") && !url.searchParams.has("action")) url.searchParams.set("mode", current.dataset.activeMode || "home");
    if (!url.searchParams.has("right_tab")) url.searchParams.set("right_tab", current.dataset.activeRightTab || "prose");
    if (!url.searchParams.has("state_tab") && (current.dataset.activeMode === "state" || url.searchParams.get("mode") === "state")) url.searchParams.set("state_tab", current.dataset.activeStateTab || "overview");
    if (!url.searchParams.has("character_id") && current.dataset.selectedCharacterId) url.searchParams.set("character_id", current.dataset.selectedCharacterId);
    if (!url.searchParams.has("truth_lens") && current.dataset.truthLens) url.searchParams.set("truth_lens", current.dataset.truthLens);
    return url.href;
  }

  function replaceChrome(parsed) {
    [["[data-wb-breadcrumb]", "[data-wb-breadcrumb]"], [".wb-status-chip", ".wb-status-chip"], ["[data-activity-trigger]", "[data-activity-trigger]"]].forEach(function (pair) { var next = parsed.querySelector(pair[0]); var present = document.querySelector(pair[1]); if (next && present) present.replaceWith(next); });
    if (parsed.title) document.title = parsed.title;
  }

  function fullNavigate(href, state) { var current = root(); saveFallback(current, state); location.href = href; }

  function loadWorkbench(href, options) {
    var current = root();
    if (!current) { location.href = href; return; }
    var desired = options && options.restoreState ? options.restoreState : captureNavigationState(current);
    var resolved = options && options.fromPop ? new URL(href, location.href).href : targetUrl(href, current);
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
      if (window.NovelLibraryCatalogInit) window.NovelLibraryCatalogInit();
      restoreNavigationState(next, desired);
      var state = { workbenchState: captureNavigationState(next) };
      if (options && options.push === false) history.replaceState(state, "", resolved); else history.pushState(state, "", resolved);
    }).catch(function () { fullNavigate(resolved, desired); });
  }

  function navigateQuery(current, changes) { var url = new URL(location.href); Object.keys(changes).forEach(function (key) { if (changes[key]) url.searchParams.set(key, changes[key]); else url.searchParams.delete(key); }); loadWorkbench(url.href, { push: true }); }

  function bindNavigation(current) {
    current.querySelectorAll("[data-workbench-navigation]").forEach(function (link) { link.addEventListener("click", function (event) { if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return; event.preventDefault(); loadWorkbench(link.href, { push: true }); }); });
    current.querySelectorAll("[data-wb-mode]").forEach(function (button) { button.addEventListener("click", function () { navigateQuery(current, { mode: button.dataset.wbMode, node: button.dataset.wbMode === "state" ? "state" : button.dataset.wbMode === "truth" ? "truth" : null }); }); });
    current.querySelectorAll("[data-wb-state-tab]").forEach(function (button) { button.addEventListener("click", function () { navigateQuery(current, { mode: "state", node: "state", state_tab: button.dataset.wbStateTab }); }); });
    current.querySelectorAll("[data-wb-editor-tab]").forEach(function (button) { button.addEventListener("click", function () { var previous = captureNavigationState(current); history.replaceState({ workbenchState: previous }, "", location.href); var tab = button.dataset.wbEditorTab; current.querySelectorAll("[data-wb-editor-tab]").forEach(function (item) { var active = item === button; item.setAttribute("aria-selected", active ? "true" : "false"); item.classList.toggle("is-active", active); }); var prose = current.querySelector("[data-wb-editor-prose]"); if (prose) prose.hidden = tab !== "prose"; current.querySelectorAll("[data-wb-editor-secondary]").forEach(function (panel) { panel.hidden = panel.dataset.wbEditorSecondary !== tab; }); current.dataset.activeRightTab = tab; var url = new URL(location.href); url.searchParams.set("right_tab", tab); history.pushState({ workbenchState: captureNavigationState(current) }, "", url.href); }); });
  }

  function bindScrollPersistence(current) {
    var timer = 0;
    [current.querySelector(".wb-left-pane .wb-pane-content"), current.querySelector(".wb-tree"), current.querySelector(".wb-center-scroll"), current.querySelector(".wb-editor-scroll")].forEach(function (node) {
      if (!node) return;
      node.addEventListener("scroll", function () { clearTimeout(timer); timer = setTimeout(function () { var state = captureNavigationState(current); saveFallback(current, state); history.replaceState({ workbenchState: state }, "", location.href); }, 90); }, { passive: true });
    });
  }

  function authorPath(current) { return "/api/books/" + encodeURIComponent(current.dataset.bookId) + "/editions/" + encodeURIComponent(current.dataset.editionId) + "/author-commands"; }
  function sendJson(url, body, method) { return fetch(url, { method: method || "POST", headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() }, body: JSON.stringify(body) }).then(function (response) { return response.json().then(function (value) { if (!response.ok) { var detail = (value.error && value.error.message) || value.detail || "请求失败"; if (typeof detail !== "string") detail = detail.message || JSON.stringify(detail); throw new Error(detail); } return value; }); }); }
  function postJson(url, body) { return sendJson(url, body, "POST"); }
  function patchJson(url, body) { return sendJson(url, body, "PATCH"); }
  function postAuthorCommand(current, command) { command.chapter_id = current.dataset.currentChapterId || null; command.character_id = current.dataset.selectedCharacterId || null; return postJson(authorPath(current), command); }
  function formPayload(form) { var payload = {}; new FormData(form).forEach(function (value, key) { if (String(value).trim()) payload[key] = value; }); return payload; }
  function feedback(target, message, rejected) { var node = target.querySelector(".wb-command-feedback") || target.querySelector("[data-item-modal-feedback]"); if (!node) { node = document.createElement("p"); node.className = "wb-command-feedback"; target.appendChild(node); } node.textContent = message; node.classList.toggle("is-error", Boolean(rejected)); }

  function bindCommands(current) {
    current.querySelectorAll("[data-author-command-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); postAuthorCommand(current, { command_type: form.dataset.commandType, payload: formPayload(form) }).then(function (result) { feedback(form, result.message, result.result === "REJECTED"); if (result.result === "PLANNED") setTimeout(function () { loadWorkbench(location.href, { push: false }); }, 350); }).catch(function (error) { feedback(form, error.message, true); }); }); });
  }

  function inspectorLine(label, value) { var row = document.createElement("div"); var term = document.createElement("span"); var content = document.createElement("strong"); term.textContent = label; content.textContent = value == null || value === "" ? "尚未知" : String(value); row.appendChild(term); row.appendChild(content); return row; }
  function inspectorValue(value) { return Array.isArray(value) ? (value.length ? value.join("、") : "尚未知") : value; }
  function showInspector(current, record, kind) {
    var panel = current.querySelector("[data-wb-inspector]"); if (!panel) return;
    var truth = record.truth || null;
    panel.innerHTML = "";
    var header = document.createElement("header"); var kicker = document.createElement("span"); var title = document.createElement("h3"); kicker.textContent = kind || record.category || "状态记录"; title.textContent = (truth && truth.title) || record.name || record.topic_name || record.label || ((record.from_entity_id || "") + " ↔ " + (record.to_entity_id || "")) || "未命名记录"; header.appendChild(kicker); header.appendChild(title); panel.appendChild(header);
    var grid = document.createElement("div"); grid.className = "wb-inspector-grid";
    var truthWindow = truth ? ("第" + truth.effective_from_chapter + (truth.effective_until_chapter ? "–" + truth.effective_until_chapter : "+") + "章") : null;
    [["信息层", truth ? "作者真相" : (record.layer_label || record.layer || record.current_layer)], ["状态", truth ? truth.status : (record.state_label || record.status_label || record.state || record.status)], ["生效范围", truthWindow], ["兼容性", truth && truth.compatibility_status], ["读者认知", record.reader && record.reader.state], ["当前目标", record.current_goal || record.goal || (record.attributes && (record.attributes.current_goal || record.attributes.goal))], ["公开目标", record.public_goal], ["态度", record.attitude], ["关键人物", inspectorValue(record.key_people)], ["控制地点", inspectorValue(record.controlled_locations)], ["资源", inspectorValue(record.resources)], ["当前行动", record.action], ["已确认", inspectorValue(record.known)], ["仍未知", inspectorValue(record.unknown)], ["关系", inspectorValue(record.relationships)], ["首次获得", record.first_acquired_chapter_ordinal], ["首次确认", record.first_confirmed_chapter_ordinal], ["最近确认", record.recent_confirmed_chapter_ordinal || record.evidence_chapter_ordinal || record.chapter_ordinal], ["持有者", record.current_holder_id || record.owner_id], ["数量", record.quantity], ["槽位", record.slot]].forEach(function (item) { if (item[1] != null && item[1] !== "") grid.appendChild(inspectorLine(item[0], item[1])); }); panel.appendChild(grid);
    var description = document.createElement("p"); description.textContent = (truth && truth.statement) || record.description || record.statement || record.evidence || "当前没有额外说明。"; panel.appendChild(description);
    if (truth && truth.compatibility_summary) { var compatibilitySummary = document.createElement("p"); compatibilitySummary.textContent = truth.compatibility_summary; compatibilitySummary.className = "wb-context-explanation"; panel.appendChild(compatibilitySummary); }
    var spans = record.source_span_ids || []; var evidence = document.createElement("small"); evidence.textContent = "证据：" + (spans.length ? spans.join("、") : "尚无 source span"); panel.appendChild(evidence);
    if (Array.isArray(record.who_knows)) { var heading = document.createElement("h4"); heading.textContent = "Who Knows"; panel.appendChild(heading); var list = document.createElement("ul"); list.className = "wb-who-knows"; record.who_knows.forEach(function (cell) { var item = document.createElement("li"); item.textContent = (cell.knower_name || cell.knower_id) + " · " + (cell.state_label || "尚未知"); list.appendChild(item); }); if (!record.who_knows.length) { var empty = document.createElement("li"); empty.textContent = "所有人物均为尚未知"; list.appendChild(empty); } panel.appendChild(list); }
    if (Array.isArray(record.character_matrix || record.characters)) { var knowledgeHeading = document.createElement("h4"); knowledgeHeading.textContent = "Character Knowledge"; panel.appendChild(knowledgeHeading); var knowledgeList = document.createElement("ul"); knowledgeList.className = "wb-who-knows"; var characterCells = record.character_matrix || record.characters; characterCells.forEach(function (cell) { var item = document.createElement("li"); item.textContent = (cell.name || cell.character_id) + " · " + cell.state + (cell.as_of_chapter_ordinal ? " · 第" + cell.as_of_chapter_ordinal + "章" : ""); knowledgeList.appendChild(item); }); if (!characterCells.length) { var unknown = document.createElement("li"); unknown.textContent = "没有已落地的角色认知；保持 UNKNOWN"; knowledgeList.appendChild(unknown); } panel.appendChild(knowledgeList); }
    if (Array.isArray(record.reveal_plans)) { var planHeading = document.createElement("h4"); planHeading.textContent = "RevealPlan"; panel.appendChild(planHeading); var planList = document.createElement("ul"); planList.className = "wb-who-knows"; record.reveal_plans.forEach(function (plan) { var item = document.createElement("li"); item.textContent = plan.target + " · " + plan.reveal_depth + " · 第" + plan.target_chapter_min + (plan.target_chapter_max ? "–" + plan.target_chapter_max : "+") + "章"; planList.appendChild(item); }); if (!record.reveal_plans.length) { var hidden = document.createElement("li"); hidden.textContent = "尚无计划；默认 KEEP_HIDDEN"; planList.appendChild(hidden); } panel.appendChild(planList); }
    if (Array.isArray(record.compatibility_evidence)) { var compatibilityHeading = document.createElement("h4"); compatibilityHeading.textContent = "已发生章节兼容性"; panel.appendChild(compatibilityHeading); var compatibilityList = document.createElement("ul"); compatibilityList.className = "wb-who-knows"; record.compatibility_evidence.forEach(function (entry) { var item = document.createElement("li"); item.textContent = entry.verdict + (entry.chapter_ordinal ? " · 第" + entry.chapter_ordinal + "章" : "") + " · " + (entry.evidence_quote || entry.explanation || "已审计"); compatibilityList.appendChild(item); }); if (!record.compatibility_evidence.length) { var missing = document.createElement("li"); missing.textContent = "尚无可审计证据；兼容性保持 UNKNOWN"; compatibilityList.appendChild(missing); } panel.appendChild(compatibilityList); }
    if (Array.isArray(record.author_truth_topics) && record.author_truth_topics.length) { var truthHeading = document.createElement("h4"); truthHeading.textContent = "Author Truth（独立层）"; panel.appendChild(truthHeading); record.author_truth_topics.forEach(function (topic) { var card = document.createElement("section"); card.className = "wb-inspector-truth-card"; var topicTitle = document.createElement("b"); topicTitle.textContent = topic.truth.title; var statement = document.createElement("p"); statement.textContent = topic.truth.statement; var reader = document.createElement("small"); reader.textContent = "Reader " + topic.reader.state + " · " + topic.truth.compatibility_status; card.appendChild(topicTitle); card.appendChild(statement); card.appendChild(reader); var matrix = document.createElement("ul"); matrix.className = "wb-who-knows"; (topic.characters || []).forEach(function (cell) { var knowledge = document.createElement("li"); knowledge.textContent = cell.character_id + " · " + cell.state; matrix.appendChild(knowledge); }); card.appendChild(matrix); var plans = document.createElement("ul"); plans.className = "wb-who-knows"; (topic.reveal_plans || []).forEach(function (plan) { var planItem = document.createElement("li"); planItem.textContent = "Reveal " + plan.reveal_depth + " · 第" + plan.target_chapter_min + (plan.target_chapter_max ? "–" + plan.target_chapter_max : "+") + "章"; plans.appendChild(planItem); }); if (!(topic.reveal_plans || []).length) { var noPlan = document.createElement("li"); noPlan.textContent = "Reveal：KEEP_HIDDEN"; plans.appendChild(noPlan); } card.appendChild(plans); panel.appendChild(card); }); }
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
      nodes.forEach(function (node) { var position = positions[node.node_id]; var group = document.createElementNS("http://www.w3.org/2000/svg", "g"); group.setAttribute("class", "wb-relationship-node wb-node-" + String(node.node_type || "unknown").toLowerCase()); group.setAttribute("role", "button"); group.setAttribute("tabindex", "0"); group.setAttribute("aria-label", "查看" + (node.name || "关系对象")); var activate = function () { showInspector(current, node.inspector || node, node.node_type === "FACTION" ? "势力" : "人物"); }; group.addEventListener("click", activate); group.addEventListener("keydown", function (event) { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); activate(); } }); var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle"); circle.setAttribute("cx", position.x); circle.setAttribute("cy", position.y); circle.setAttribute("r", "26"); var label = document.createElementNS("http://www.w3.org/2000/svg", "text"); label.setAttribute("x", position.x); label.setAttribute("y", position.y + 44); label.setAttribute("text-anchor", "middle"); label.textContent = node.name; group.appendChild(circle); group.appendChild(label); svg.appendChild(group); }); container.appendChild(svg);
    });
  }

  function setActivityOpen(current, open, persist) {
    var panel = current && current.querySelector("[data-activity-center]");
    var scrim = current && current.querySelector("[data-activity-close].wb-activity-scrim");
    var trigger = document.querySelector("[data-activity-trigger]");
    if (!panel) return;
    panel.hidden = !open;
    if (scrim) scrim.hidden = !open;
    if (trigger) trigger.setAttribute("aria-expanded", open ? "true" : "false");
    current.classList.toggle("is-activity-open", open);
    if (persist !== false) saveFallback(current, captureNavigationState(current));
  }

  function bindActivityCenter(current) {
    var trigger = document.querySelector("[data-activity-trigger]");
    if (trigger) trigger.addEventListener("click", function () { var panel = current.querySelector("[data-activity-center]"); setActivityOpen(current, Boolean(panel && panel.hidden)); });
    current.querySelectorAll("[data-activity-close]").forEach(function (button) { button.addEventListener("click", function () { setActivityOpen(current, false); }); });
  }

  function closeDialog(dialog) { var form = dialog.querySelector("[data-item-modal-form]"); if (!form) return; form.reset(); form.querySelectorAll(".wb-semantic-actions").forEach(function (node) { node.remove(); }); var message = form.querySelector("[data-item-modal-feedback]"); if (message) { message.textContent = ""; message.classList.remove("is-error"); } }

  function bindItemModal(current) {
    var dialog = current.querySelector("[data-item-modal]"); if (!dialog) return;
    current.querySelectorAll("[data-close-item-modal]").forEach(function (button) { button.addEventListener("click", function () { closeDialog(dialog); }); });
    var form = dialog.querySelector("[data-item-modal-form]"); var submitItem = function (event) { event.preventDefault(); var values = formPayload(form); var scope = values.intent_scope; form.querySelectorAll(".wb-semantic-actions").forEach(function (node) { node.remove(); });
      if (scope === "HIDDEN") {
        var hiddenPath = "/api/books/" + encodeURIComponent(current.dataset.bookId) + "/editions/" + encodeURIComponent(current.dataset.editionId) + "/hidden-items";
        postJson(hiddenPath, { name: values.name, category: values.category || "ITEM", description: values.description || "", effective_from_chapter: number(current.dataset.selectedChapterAnchor) || 1, location_id: values.location || null, owner_id: values.character_id || null, horizon: values.horizon || "MID", priority: values.priority !== undefined && values.priority !== "" ? number(values.priority) : 100, target_chapter_min: values.target_chapter_min ? number(values.target_chapter_min) : null, target_chapter_max: values.target_chapter_max ? number(values.target_chapter_max) : null, reveal_depth: values.reveal_depth || "HINT" }).then(function () { feedback(form, "已创建独立 Author Truth；存在、地点、持有与可见性保持分层。", false); setTimeout(function () { closeDialog(dialog); loadWorkbench(location.href, { push: false }); }, 500); }).catch(function (error) { feedback(form, error.message, true); }); return;
      }
      if (scope === "CURRENT") {
        var inventoryNode = current.querySelector("[data-current-inventory]");
        var inventory = inventoryNode ? json(inventoryNode.textContent || "[]", []) : [];
        var wanted = String(values.name || "").trim().toLocaleLowerCase();
        var existing = inventory.find(function (item) { return [item.record_id, item.name, item.label].some(function (value) { return String(value || "").trim().toLocaleLowerCase() === wanted; }); });
        var actions = document.createElement("div"); actions.className = "wb-modal-actions wb-semantic-actions";
        if (existing) {
          feedback(form, "已存在：" + (existing.name || values.name), false);
          var openButton = document.createElement("button"); openButton.type = "button"; openButton.className = "button primary compact"; openButton.textContent = "打开"; openButton.addEventListener("click", function () { closeDialog(dialog); showInspector(current, existing, "物品"); }); actions.appendChild(openButton);
        } else {
          feedback(form, "没有当前证据。当前状态不会被直接改写。", true);
          [["未来获得", "FUTURE"], ["创建改写", "REVISION"], ["取消", "CANCEL"]].forEach(function (entry) { var button = document.createElement("button"); button.type = "button"; button.className = "button compact"; button.textContent = entry[0]; button.addEventListener("click", function () { if (entry[1] === "FUTURE") { postAuthorCommand(current, { command_type: "CREATE_FUTURE_ITEM", payload: values }).then(function (reply) { feedback(form, reply.message, false); setTimeout(function () { closeDialog(dialog); loadWorkbench(location.href, { push: false }); }, 400); }).catch(function (error) { feedback(form, error.message, true); }); } else if (entry[1] === "REVISION") { postAuthorCommand(current, { command_type: "CREATE_REVISION_REQUEST", payload: { title: "为当前章节加入物品：" + values.name, item_id: values.name, description: values.description || "" } }).then(function (reply) { feedback(form, reply.message, false); }); } else closeDialog(dialog); }); actions.appendChild(button); });
        }
        form.appendChild(actions); return;
      }
      var command = scope === "FUTURE" ? { command_type: "CREATE_FUTURE_ITEM", payload: values } : { command_type: "CREATE_TASK", payload: { title: "候选物品：" + values.name, task_type: "CANDIDATE_ITEM", description: values.description || "", subject_type: "ITEM", subject_id: values.name } };
      postAuthorCommand(current, command).then(function (result) { feedback(form, result.message, result.result === "REJECTED"); if (result.result === "PLANNED") setTimeout(function () { closeDialog(dialog); loadWorkbench(location.href, { push: false }); }, 400); }).catch(function (error) { feedback(form, error.message, true); });
    };
    form.addEventListener("submit", submitItem);
    form.querySelector("[data-item-submit]").addEventListener("click", submitItem);
  }

  function profileBase(current) { return "/api/books/" + encodeURIComponent(current.dataset.bookId) + "/editions/" + encodeURIComponent(current.dataset.editionId) + "/book-profile"; }
  function bindProfile(current) {
    current.querySelectorAll("[data-profile-edit-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); postJson(profileBase(current) + "/edits", formPayload(form)).then(function () { feedback(form, "已保存新 Profile 版本。", false); setTimeout(function () { loadWorkbench(location.href, { push: false }); }, 300); }).catch(function (error) { feedback(form, error.message, true); }); }); });
    current.querySelectorAll("[data-profile-reanalyze]").forEach(function (button) { button.addEventListener("click", function () { button.disabled = true; button.textContent = "正在准备任务…"; postJson(profileBase(current) + "/reanalysis", { context_chapter_id: current.dataset.currentChapterId || null }).then(function (result) { button.textContent = "任务已准备"; button.title = result.handoff_id; var url = new URL(location.href); url.searchParams.set("activity_id", result.handoff_id); setTimeout(function () { loadWorkbench(url.href, { push: false, restoreState: Object.assign(captureNavigationState(current), { activityCenterOpen: true }) }); }, 350); }).catch(function (error) { button.disabled = false; button.textContent = error.message; }); }); });
    current.querySelectorAll("[data-profile-proposal-action]").forEach(function (button) { button.addEventListener("click", function () { postJson(profileBase(current) + "/proposals/" + encodeURIComponent(button.dataset.proposalId) + "/resolve", { action: button.dataset.profileProposalAction }).then(function () { loadWorkbench(location.href, { push: false }); }).catch(function (error) { button.textContent = error.message; }); }); });
  }

  function truthBase(current) { return "/api/books/" + encodeURIComponent(current.dataset.bookId) + "/editions/" + encodeURIComponent(current.dataset.editionId); }
  function bindTruth(current) {
    current.querySelectorAll("[data-author-truth-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); var payload = formPayload(form); var verdict = payload.compatibility_verdict; var evidence = verdict ? { verdict: verdict, chapter_id: payload.compatibility_chapter_id || null, chapter_ordinal: payload.compatibility_chapter_ordinal ? number(payload.compatibility_chapter_ordinal) : null, source_span_id: payload.compatibility_source_span_id || null, evidence_quote: payload.compatibility_evidence_quote || "", explanation: payload.compatibility_explanation || "" } : null; ["compatibility_verdict", "compatibility_chapter_id", "compatibility_chapter_ordinal", "compatibility_source_span_id", "compatibility_evidence_quote", "compatibility_explanation"].forEach(function (key) { delete payload[key]; }); payload.compatibility_evidence = evidence ? [evidence] : []; postJson(truthBase(current) + "/author-truths", payload).then(function (result) { feedback(form, "已保存：" + result.truth.status + " · " + result.truth.compatibility_status, false); setTimeout(function () { loadWorkbench(location.href, { push: false }); }, 500); }).catch(function (error) { feedback(form, error.message, true); }); }); });
    current.querySelectorAll("[data-author-truth-update-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); patchJson(truthBase(current) + "/author-truths/" + encodeURIComponent(form.dataset.truthId), { changes: formPayload(form) }).then(function (result) { feedback(form, "已重新检查：" + result.truth.status + " · " + result.truth.compatibility_status, false); setTimeout(function () { loadWorkbench(location.href, { push: false }); }, 500); }).catch(function (error) { feedback(form, error.message, true); }); }); });
    current.querySelectorAll("[data-reveal-plan-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); postJson(truthBase(current) + "/reveal-plans", formPayload(form)).then(function () { feedback(form, "RevealPlan 已保存；Reader / Character Knowledge 未改变。", false); setTimeout(function () { loadWorkbench(location.href, { push: false }); }, 500); }).catch(function (error) { feedback(form, error.message, true); }); }); });
    current.querySelectorAll("[data-open-question-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); postJson(truthBase(current) + "/open-questions", formPayload(form)).then(function () { feedback(form, "已保存为 Open Creative Question；不会约束 Planner。", false); setTimeout(function () { loadWorkbench(location.href, { push: false }); }, 400); }).catch(function (error) { feedback(form, error.message, true); }); }); });
    current.querySelectorAll("[data-secret-candidate-action]").forEach(function (button) { button.addEventListener("click", function () { postJson(truthBase(current) + "/secret-candidates/" + encodeURIComponent(button.dataset.candidateId) + "/resolve", { action: button.dataset.secretCandidateAction, effective_from_chapter: number(current.dataset.selectedChapterAnchor) || 1 }).then(function () { loadWorkbench(location.href, { push: false }); }).catch(function (error) { button.textContent = error.message; }); }); });
    current.querySelectorAll("[data-truth-search]").forEach(function (search) { search.addEventListener("input", function () { var query = search.value.trim().toLowerCase(); current.querySelectorAll("[data-truth-search-text]").forEach(function (card) { card.hidden = Boolean(query && String(card.dataset.truthSearchText || "").toLowerCase().indexOf(query) === -1); }); var publicIndex = current.querySelector("[data-truth-public-index]"); if (publicIndex && query) publicIndex.open = true; }); });
    current.querySelectorAll("[data-reveal-agenda]").forEach(function (board) { var dragged = ""; board.querySelectorAll("[data-truth-id][draggable]").forEach(function (card) { card.addEventListener("dragstart", function () { dragged = card.dataset.truthId || ""; card.classList.add("is-dragging"); }); card.addEventListener("dragend", function () { card.classList.remove("is-dragging"); }); }); board.querySelectorAll("[data-agenda-bucket]").forEach(function (column) { column.addEventListener("dragover", function (event) { event.preventDefault(); column.classList.add("is-drag-over"); }); column.addEventListener("dragleave", function () { column.classList.remove("is-drag-over"); }); column.addEventListener("drop", function (event) { event.preventDefault(); column.classList.remove("is-drag-over"); if (!dragged) return; var bucket = column.dataset.agendaBucket; var depth = bucket === "SHOULD_HINT" ? "HINT" : bucket === "MUST_REVEAL" ? "PARTIAL_REVEAL" : null; postJson(truthBase(current) + "/reveal-agenda/override", { truth_id: dragged, chapter_ordinal: number(board.dataset.chapterOrdinal), agenda_bucket: bucket, reveal_depth: depth, reason: "作者在 Chapter Reveal Agenda 拖动" }).then(function () { feedback(board, "Agenda 已更新；知识状态没有变化。", false); setTimeout(function () { loadWorkbench(location.href, { push: false }); }, 350); }).catch(function (error) { feedback(board, error.message, true); }); }); }); });
  }

  function bindSecretBoard(current) {
    current.querySelectorAll("[data-secret-board]").forEach(function (board) {
      board.querySelectorAll("[data-secret-horizon-filter]").forEach(function (button) {
        button.addEventListener("click", function () {
          var horizon = button.dataset.secretHorizonFilter || "ALL";
          board.querySelectorAll("[data-secret-horizon-filter]").forEach(function (item) { item.classList.toggle("primary", item === button); });
          board.querySelectorAll("[data-secret-horizons]").forEach(function (card) {
            var horizons = String(card.dataset.secretHorizons || "").split(" ");
            card.hidden = horizon !== "ALL" && horizons.indexOf(horizon) === -1;
          });
        });
      });
      var dragged = "";
      board.querySelectorAll("[data-truth-id][draggable]").forEach(function (card) {
        card.addEventListener("dragstart", function () { dragged = card.dataset.truthId || ""; card.classList.add("is-dragging"); });
        card.addEventListener("dragend", function () { card.classList.remove("is-dragging"); });
      });
      board.querySelectorAll("[data-secret-lifecycle]").forEach(function (column) {
        column.addEventListener("dragover", function (event) { if (column.dataset.secretLifecycle === "RETIRED" || column.dataset.secretLifecycle === "AFTERMATH") return; event.preventDefault(); column.classList.add("is-drag-over"); });
        column.addEventListener("dragleave", function () { column.classList.remove("is-drag-over"); });
        column.addEventListener("drop", function (event) {
          event.preventDefault(); column.classList.remove("is-drag-over"); if (!dragged) return;
          var lifecycle = column.dataset.secretLifecycle;
          var bucket = lifecycle === "HINTING" ? "SHOULD_HINT" : (lifecycle === "PARTIAL_REVEAL" || lifecycle === "PAYOFF_READY" || lifecycle === "REVEALED") ? "MUST_REVEAL" : "KEEP_HIDDEN";
          var depth = lifecycle === "HINTING" ? "HINT" : lifecycle === "REVEALED" ? "FULL_REVEAL" : bucket === "MUST_REVEAL" ? "PARTIAL_REVEAL" : null;
          postJson(truthBase(current) + "/reveal-agenda/override", { truth_id: dragged, chapter_ordinal: number(board.dataset.chapterOrdinal), agenda_bucket: bucket, reveal_depth: depth, reason: "作者在 Secret Board 调整本章揭示阶段" }).then(function () { feedback(board, "已换算为本章 Reveal Agenda；Truth 与 Knowledge 均未改变。", false); setTimeout(function () { loadWorkbench(location.href, { push: false }); }, 350); }).catch(function (error) { feedback(board, error.message, true); });
        });
      });
    });
  }

  function bindDraft(current) { current.querySelectorAll("[data-wb-editor]").forEach(function (editor) { var counter = current.querySelector("[data-wb-word-count]"); var update = function () { if (counter) counter.textContent = Array.from(editor.value || "").length + " 字"; }; editor.addEventListener("input", update); update(); }); current.querySelectorAll("[data-wb-draft-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); var editor = form.querySelector('[name="content"]'); var expected = form.querySelector('[name="expected_content_sha256"]'); postJson(form.action, { content: editor.value, expected_content_sha256: expected ? expected.value : null }).then(function () { loadWorkbench(location.href, { push: false }); }).catch(function (error) { feedback(form, error.message, true); }); }); }); }

  function bindWorkflow(current) {
    current.querySelectorAll("[data-workflow-workspace]").forEach(function (workspace) { var buttons = workspace.querySelectorAll("[data-workflow-mode]"); var panels = workspace.querySelectorAll("[data-workflow-mode-panel]"); function activate(target) { buttons.forEach(function (button) { button.setAttribute("aria-selected", button.dataset.workflowMode === target ? "true" : "false"); }); panels.forEach(function (panel) { panel.hidden = panel.dataset.workflowModePanel !== target; }); } buttons.forEach(function (button) { button.addEventListener("click", function () { activate(button.dataset.workflowMode); }); }); activate(workspace.dataset.workflowInitialMode || "continue"); });
    current.querySelectorAll("[data-workflow-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); var payload = {}; new FormData(form).forEach(function (value, key) { if (key === "innovation_focus" || key === "author_task_ids") { payload[key] = payload[key] || []; payload[key].push(String(value)); } else payload[key] = value; }); postJson(form.action, payload).then(function (result) { var url = new URL(location.href); var kind = form.dataset.workflowKind || "continue"; url.searchParams.set("action", kind); url.searchParams.delete("mode"); if (result.handoff_id) url.searchParams.set("activity_id", result.handoff_id); loadWorkbench(url.href, { push: false, restoreState: Object.assign(captureNavigationState(current), { activityCenterOpen: true }) }); }).catch(function (error) { var node = form.querySelector("[data-workflow-feedback]"); if (node) { node.hidden = false; node.textContent = error.message; } }); }); });
  }

  function bindSearch(current) { var search = current.querySelector("[data-wb-chapter-search]"); if (!search) return; search.addEventListener("input", function () { var query = search.value.trim().toLowerCase(); current.querySelectorAll("[data-wb-chapter-item]").forEach(function (item) { item.hidden = Boolean(query && item.textContent.toLowerCase().indexOf(query) === -1); }); }); }

  function initWorkbench(current) { bindLayout(current); bindNavigation(current); bindScrollPersistence(current); bindActivityCenter(current); bindCommands(current); bindInspector(current); bindRelationshipGraph(current); bindItemModal(current); bindProfile(current); bindTruth(current); bindSecretBoard(current); bindDraft(current); bindWorkflow(current); bindSearch(current); current.querySelectorAll("details[data-explorer-section]").forEach(function (item) { item.addEventListener("toggle", function () { saveFallback(current, captureNavigationState(current)); }); }); }

  window.addEventListener("popstate", function (event) { loadWorkbench(location.href, { push: false, fromPop: true, restoreState: event.state && event.state.workbenchState ? event.state.workbenchState : readFallback(root()) }); });
  var initial = root(); if (initial) { var state = history.state && history.state.workbenchState ? history.state.workbenchState : readFallback(initial); restoreDetails(initial, state); restoreLayout(initial, state); initWorkbench(initial); restoreNavigationState(initial, state); history.replaceState({ workbenchState: captureNavigationState(initial) }, "", location.href); }
}());
