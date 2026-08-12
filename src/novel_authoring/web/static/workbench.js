(function () {
  "use strict";

  var rootSelector = "[data-workbench-shell]";

  function root() { return document.querySelector(rootSelector); }
  function csrfToken() { var meta = document.querySelector('meta[name="csrf-token"]'); return meta ? meta.content : ""; }
  function json(value, fallback) { try { return JSON.parse(value); } catch (error) { return fallback; } }
  function scopedKey(current) { return "novel-workbench-v2.4:" + current.dataset.bookId + ":" + current.dataset.editionId; }
  function number(value) { return Number.isFinite(Number(value)) ? Number(value) : 0; }

  function copyText(value) {
    if (!value) return Promise.reject(new Error("AI 任务中没有可复制的指令"));
    var area = document.createElement("textarea");
    area.value = value;
    area.style.position = "fixed";
    area.style.left = "-9999px";
    area.style.top = "0";
    area.setAttribute("readonly", "");
    document.body.appendChild(area);
    area.focus();
    area.select();
    area.setSelectionRange(0, area.value.length);
    var copied = document.execCommand("copy");
    area.remove();
    if (copied) return Promise.resolve();
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(value);
    return Promise.reject(new Error("浏览器未允许复制，请重试"));
  }

  function bindInstructionCopy(button) {
    if (!button || button.dataset.copyInstructionBound === "true") return;
    button.dataset.copyInstructionBound = "true";
    button.addEventListener("click", function () {
      var label = button.textContent;
      button.disabled = true;
      fetch(button.dataset.copyInstruction, { headers: { Accept: "application/json" } }).then(function (response) {
        return response.json().then(function (value) {
          if (!response.ok || value.error) throw new Error((value.error && value.error.message) || "指令不可用");
          return value;
        });
      }).then(function (value) { return copyText(value.instruction || ""); }).then(function () {
        button.textContent = "已复制";
      }).catch(function (error) {
        button.textContent = error.message;
      }).finally(function () {
        window.setTimeout(function () { button.textContent = label; button.disabled = false; }, 1500);
      });
    });
  }

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
      activeStateScope: current.dataset.activeStateScope || "character",
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
    if (!url.searchParams.has("state_scope") && (current.dataset.activeMode === "state" || url.searchParams.get("mode") === "state")) url.searchParams.set("state_scope", current.dataset.activeStateScope || "character");
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
    if ((!options || !options.fromPop) && desired) {
      var nextLocation = new URL(resolved, location.href);
      var changesCenterView = (nextLocation.searchParams.get("mode") || current.dataset.activeMode) !== current.dataset.activeMode || (nextLocation.searchParams.get("state_tab") || current.dataset.activeStateTab) !== current.dataset.activeStateTab || (nextLocation.searchParams.get("chapter_id") || current.dataset.currentChapterId) !== current.dataset.currentChapterId;
      if (changesCenterView) { desired.centerScrollTop = 0; desired.centerScrollLeft = 0; desired.rightScrollTop = 0; desired.rightScrollLeft = 0; }
    }
    if (!options || !options.fromPop) {
      history.replaceState({ workbenchState: captureNavigationState(current) }, "", location.href);
    }
    saveFallback(current, desired);
    fetch(resolved, { headers: { Accept: "text/html" } }).then(function (response) { if (!response.ok) throw new Error("load"); return response.text(); }).then(function (html) {
      var parsed = new DOMParser().parseFromString(html, "text/html");
      var next = parsed.querySelector(rootSelector);
      var present = root();
      if (!next || !present) { fullNavigate(resolved, desired); return; }
      if (present._pendingActionTimer) clearInterval(present._pendingActionTimer);
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

  function inspectorLine(label, value) { var row = document.createElement("div"); var term = document.createElement("span"); var content = document.createElement("strong"); term.textContent = label; content.textContent = value == null || value === "" || value === "UNKNOWN" ? "尚未知 / 无证据" : String(value); row.appendChild(term); row.appendChild(content); return row; }
  function inspectorValue(value) { if (Array.isArray(value)) return value.length ? value.map(function (item) { return typeof item === "object" ? (item.name || item.label || item.author_name || "关联对象") : item; }).join("、") : "尚未知 / 无证据"; if (value && typeof value === "object") return value.label || value.name || "已有结构化记录"; return value; }
  function inspectorHeading(panel, title) { var heading = document.createElement("h4"); heading.textContent = title; panel.appendChild(heading); return heading; }
  function inspectorList(panel, className) { var list = document.createElement("ul"); list.className = className || "wb-who-knows"; panel.appendChild(list); return list; }
  function showInspector(current, record, kind) {
    var panel = current.querySelector("[data-wb-inspector]"); if (!panel) return;
    var truth = record.truth || null;
    panel.innerHTML = "";
    var header = document.createElement("header"); var kicker = document.createElement("span"); var title = document.createElement("h3"); kicker.textContent = record.source_label || kind || record.author_category_label || "状态记录"; title.textContent = (truth && (truth.author_name || truth.title)) || record.author_name || record.topic_name || record.label || "未命名记录"; header.appendChild(kicker); header.appendChild(title); panel.appendChild(header);
    inspectorHeading(panel, "当前状态");
    var grid = document.createElement("div"); grid.className = "wb-inspector-grid";
    var truthWindow = truth ? ("第" + truth.effective_from_chapter + (truth.effective_until_chapter ? "–" + truth.effective_until_chapter : "+") + "章") : null;
    var recordCategory = String(record.category || "").toLowerCase(); var itemLike = ["item", "resource", "equipment"].indexOf(recordCategory) >= 0 || ["背包", "装备", "物品"].indexOf(kind) >= 0;
    [["证据层", truth ? "独立作者真相" : (record.source_label || record.layer_label)], ["状态", truth ? (truth.status_label || "作者已记录") : (record.state_label || record.status_label || record.state || record.status)], ["本章操作", record.operation_label], ["生效范围", truthWindow], ["关系双方", record.from_name && record.to_name ? record.from_name + " ↔ " + record.to_name : null], ["当前关系", record.relationship_label], ["公开状态", record.public_status], ["公开目标", record.public_goal], ["作者全知目标", record.goal], ["态度", record.attitude], ["当前行动", record.action], ["在场人物", inspectorValue(record.present_characters)], ["关键人物", inspectorValue(record.key_people)], ["控制地点", inspectorValue(record.controlled_locations)], ["资源", inspectorValue(record.resources)], ["关联势力", inspectorValue(record.related_factions)], ["势力关系", inspectorValue(record.relationships)], ["近期事件", inspectorValue(record.recent_events)], ["首次出现", record.first_confirmed_chapter_ordinal || record.chapter_ordinal], ["首次获得", itemLike ? record.first_acquired_chapter_ordinal : null], ["最近确认", record.recent_chapter_ordinal || record.recent_confirmed_chapter_ordinal || record.evidence_chapter_ordinal || record.chapter_ordinal], ["持有者", record.owner_name], ["数量", record.quantity], ["是否装备", itemLike ? (record.equipped === true ? "已装备" : record.equipped === false ? "未装备" : null) : null], ["明确槽位", record.slot], ["所在地点", record.location_name || record.location_id], ["用途", record.use], ["限制", inspectorValue(record.constraints)]].forEach(function (item) { if (item[1] != null && item[1] !== "" && item[1] !== "UNKNOWN") grid.appendChild(inspectorLine(item[0], item[1])); }); panel.appendChild(grid);
    var description = document.createElement("p"); description.textContent = inspectorValue((truth && truth.statement) || record.description || record.statement || record.evidence || "当前没有额外说明。"); panel.appendChild(description);
    if (truth && truth.compatibility_summary) { var compatibilitySummary = document.createElement("p"); compatibilitySummary.textContent = truth.compatibility_summary; compatibilitySummary.className = "wb-context-explanation"; panel.appendChild(compatibilitySummary); }
    if (record.dimensions && typeof record.dimensions === "object") { inspectorHeading(panel, "关系维度"); var dimensions = document.createElement("div"); dimensions.className = "wb-inspector-grid"; var dimensionLabels = {trust: "信任", dependence: "依赖", conflict: "冲突", intimacy: "亲密", power: "权力", fear: "恐惧", obligation: "义务"}; Object.keys(dimensionLabels).forEach(function (key) { dimensions.appendChild(inspectorLine(dimensionLabels[key], record.dimensions[key])); }); panel.appendChild(dimensions); }
    inspectorHeading(panel, "变化历史");
    var historyList = inspectorList(panel, "wb-inspector-history"); var history = record.history || [];
    history.forEach(function (entry) { var item = document.createElement("li"); var heading = document.createElement("b"); var copy = document.createElement("span"); heading.textContent = "第" + (entry.chapter_ordinal || "—") + "章 · " + (entry.operation_label || "状态记录"); copy.textContent = entry.statement || "有确认变化"; item.appendChild(heading); item.appendChild(copy); historyList.appendChild(item); });
    if (!history.length) { var noHistory = document.createElement("li"); noHistory.textContent = "暂无可回指的变化历史。"; historyList.appendChild(noHistory); }
    if (Array.isArray(record.who_knows)) { inspectorHeading(panel, "谁知道"); var list = inspectorList(panel); record.who_knows.forEach(function (cell) { var item = document.createElement("li"); item.textContent = (cell.knower_name || "未命名人物") + " · " + (cell.state_label || "尚未知 / 无证据"); list.appendChild(item); }); if (!record.who_knows.length) { var empty = document.createElement("li"); empty.textContent = "尚无人物认知证据。"; list.appendChild(empty); } }
    if (record.reader) { inspectorHeading(panel, "读者边界"); var reader = document.createElement("p"); reader.textContent = "截至本章：" + (record.reader.state_label || "尚未知 / 无证据"); panel.appendChild(reader); }
    if (Array.isArray(record.character_matrix || record.characters)) { inspectorHeading(panel, "人物认知"); var knowledgeList = inspectorList(panel); var characterCells = record.character_matrix || record.characters; characterCells.forEach(function (cell) { var item = document.createElement("li"); item.textContent = (cell.name || "未命名人物") + " · " + (cell.state_label || "尚未知 / 无证据") + (cell.as_of_chapter_ordinal ? " · 第" + cell.as_of_chapter_ordinal + "章" : ""); knowledgeList.appendChild(item); }); if (!characterCells.length) { var unknown = document.createElement("li"); unknown.textContent = "尚无人物认知证据。"; knowledgeList.appendChild(unknown); } }
    if (Array.isArray(record.reveal_plans)) { inspectorHeading(panel, "揭示计划（不属于当前事实）"); var planList = inspectorList(panel); var revealTargets = {READER: "读者", CHARACTER: "人物", FACTION: "势力"}; var revealDepths = {HINT: "暗示", PARTIAL_REVEAL: "部分揭示", FULL_REVEAL: "完整揭示"}; record.reveal_plans.forEach(function (plan) { var item = document.createElement("li"); item.textContent = "第" + plan.target_chapter_min + (plan.target_chapter_max ? "–" + plan.target_chapter_max : "+") + "章 · " + (revealTargets[plan.target] || "目标待定") + " · " + (revealDepths[plan.reveal_depth] || "揭示深度待定"); planList.appendChild(item); }); if (!record.reveal_plans.length) { var hidden = document.createElement("li"); hidden.textContent = "尚无揭示计划。"; planList.appendChild(hidden); } }
    if (Array.isArray(record.compatibility_evidence)) { var compatibilityHeading = document.createElement("h4"); compatibilityHeading.textContent = "已发生章节兼容性"; panel.appendChild(compatibilityHeading); var compatibilityList = document.createElement("ul"); compatibilityList.className = "wb-who-knows"; var compatibilityLabels = {CONTRADICTION: "存在明确冲突", NO_CONTRADICTION: "未发现明确冲突", SUPPORTING: "正文提供支持"}; record.compatibility_evidence.forEach(function (entry) { var item = document.createElement("li"); item.textContent = (compatibilityLabels[entry.verdict] || "已审计") + (entry.chapter_ordinal ? " · 第" + entry.chapter_ordinal + "章" : "") + " · " + (entry.evidence_quote || entry.explanation || "已审计"); compatibilityList.appendChild(item); }); if (!record.compatibility_evidence.length) { var missing = document.createElement("li"); missing.textContent = "尚无可审计证据；兼容性仍待确认"; compatibilityList.appendChild(missing); } panel.appendChild(compatibilityList); }
    if (Array.isArray(record.author_truth_topics) && record.author_truth_topics.length) { inspectorHeading(panel, "当前镜头可见的幕后信息"); record.author_truth_topics.forEach(function (topic) { var card = document.createElement("section"); card.className = "wb-inspector-truth-card"; var topicTitle = document.createElement("b"); topicTitle.textContent = topic.truth.author_name || topic.truth.title; var statement = document.createElement("p"); statement.textContent = topic.truth.statement; var readerLine = document.createElement("small"); readerLine.textContent = "读者：" + ((topic.reader && topic.reader.state_label) || "当前镜头未提供"); card.appendChild(topicTitle); card.appendChild(statement); card.appendChild(readerLine); panel.appendChild(card); }); }
    if ((Array.isArray(record.known) && record.known.length) || (Array.isArray(record.unknown) && record.unknown.length)) { inspectorHeading(panel, "公开与未知边界"); var boundaryList = inspectorList(panel); (record.known || []).forEach(function (entry) { var item = document.createElement("li"); item.textContent = "已确认 · " + inspectorValue(entry); boundaryList.appendChild(item); }); (record.unknown || []).forEach(function (entry) { var item = document.createElement("li"); item.textContent = "尚未确认 · " + inspectorValue(entry); boundaryList.appendChild(item); }); }
    var related = [["能力", record.related_ability_id], ["任务", record.related_task_id], ["剧情线", record.related_plot_thread_id], ["关系", record.related_relationship_id], ["人物", record.related_person_id]].filter(function (entry) { return entry[1]; }); if (related.length) { inspectorHeading(panel, "相关对象"); var relatedList = inspectorList(panel); related.forEach(function (entry) { var item = document.createElement("li"); item.textContent = entry[0] + " · 已有关联记录"; relatedList.appendChild(item); }); }
    inspectorHeading(panel, "原文证据"); var evidenceList = inspectorList(panel, "wb-inspector-evidence"); var rawLocators = record.evidence_locator || record.evidence || []; var locators = Array.isArray(rawLocators) ? rawLocators : [];
    locators.forEach(function (entry) { var item = document.createElement("li"); item.textContent = typeof entry === "object" ? ((entry.chapter_ordinal ? "第" + entry.chapter_ordinal + "章 · " : "") + (entry.note || entry.evidence_quote || "已有原文定位")) : String(entry); evidenceList.appendChild(item); });
    if (record.evidence_excerpt && !locators.length) { var excerpt = document.createElement("li"); excerpt.textContent = record.evidence_excerpt; evidenceList.appendChild(excerpt); }
    if (!locators.length && !record.evidence_excerpt) { var noEvidence = document.createElement("li"); noEvidence.textContent = (record.source_span_ids || []).length ? "已有原文定位；技术详情中可查看引用标识。" : "尚无可回指的原文证据。"; evidenceList.appendChild(noEvidence); }
    var technical = document.createElement("details"); technical.className = "wb-technical-details wb-inspector-technical"; var summary = document.createElement("summary"); summary.textContent = "技术详情"; technical.appendChild(summary); var technicalGrid = document.createElement("div"); technicalGrid.className = "wb-inspector-grid"; [["记录 ID", record.record_id || record.state_key || (truth && truth.truth_id)], ["原始类别", record.category], ["原始操作", record.operation], ["原始状态", record.status || record.layer], ["Source spans", (record.source_span_ids || []).join("、")]].forEach(function (item) { if (item[1]) technicalGrid.appendChild(inspectorLine(item[0], item[1])); }); technical.appendChild(technicalGrid); if (record.raw && typeof record.raw === "object") { var raw = document.createElement("pre"); raw.className = "wb-inspector-raw"; raw.textContent = JSON.stringify(record.raw, null, 2); technical.appendChild(raw); } panel.appendChild(technical);
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

  function applyStateFilters(current, key) {
    var search = current.querySelector('[data-state-search="' + key + '"]');
    var category = current.querySelector('[data-state-category-filter="' + key + '"]');
    var recency = current.querySelector('[data-state-recency-filter="' + key + '"]');
    var query = search ? search.value.trim().toLocaleLowerCase() : "";
    var selectedCategory = category ? category.value : "all";
    var selectedRecency = recency ? recency.value : "all";
    current.querySelectorAll('[data-state-search-record="' + key + '"]').forEach(function (record) {
      var matchesText = !query || String(record.dataset.searchText || record.textContent || "").toLocaleLowerCase().indexOf(query) !== -1;
      var matchesCategory = selectedCategory === "all" || record.dataset.category === selectedCategory;
      var matchesRecency = selectedRecency === "all" || record.dataset.recency === selectedRecency || (selectedRecency === "recent" && record.dataset.recency === "current");
      record.hidden = !(matchesText && matchesCategory && matchesRecency);
    });
  }

  function buildKnowledgeMatrix(workspace) {
    var container = workspace.querySelector("[data-knowledge-matrix-container]");
    if (!container || container.dataset.built === "true") return;
    var cells = json((workspace.querySelector("[data-knowledge-matrix-payload]") || {}).textContent || "[]", []);
    var characters = json((workspace.querySelector("[data-knowledge-characters]") || {}).textContent || "[]", []);
    var topics = json((workspace.querySelector("[data-knowledge-topics]") || {}).textContent || "[]", []);
    var byKey = {}; cells.forEach(function (cell) { byKey[String(cell.knower_id) + "::" + String(cell.topic_id)] = cell; });
    var table = document.createElement("table"); table.className = "wb-knowledge-table"; table.setAttribute("aria-label", "完整人物认知矩阵");
    var head = document.createElement("thead"); var headRow = document.createElement("tr"); var corner = document.createElement("th"); corner.textContent = "人物"; headRow.appendChild(corner);
    topics.forEach(function (topic) { var cell = document.createElement("th"); cell.textContent = topic.author_name || topic.name || "认知主题"; headRow.appendChild(cell); }); head.appendChild(headRow); table.appendChild(head);
    var body = document.createElement("tbody"); characters.forEach(function (character) { var row = document.createElement("tr"); var name = document.createElement("th"); name.textContent = character.author_name || character.name || "未命名人物"; row.appendChild(name); topics.forEach(function (topic) { var wrapper = document.createElement("td"); var value = byKey[String(character.character_id) + "::" + String(topic.topic_id)] || { state: "UNKNOWN", state_label: "尚未知 / 无证据", knower_name: character.author_name || character.name, topic_name: topic.author_name || topic.name }; var button = document.createElement("button"); button.type = "button"; button.className = "wb-knowledge-cell wb-knowledge-cell-" + String(value.state || "UNKNOWN").toLocaleLowerCase(); button.textContent = value.state_label || "尚未知 / 无证据"; button.addEventListener("click", function () { showInspector(root(), Object.assign({ category: "knowledge", author_name: topic.author_name || topic.name }, value), "认知边界"); }); wrapper.appendChild(button); row.appendChild(wrapper); }); body.appendChild(row); }); table.appendChild(body);
    container.innerHTML = ""; var wrap = document.createElement("div"); wrap.className = "wb-knowledge-table-wrap"; wrap.appendChild(table); container.appendChild(wrap); container.dataset.built = "true";
  }

  function bindStateWorkspace(current) {
    current.querySelectorAll("[data-state-view-toggle]").forEach(function (button) { button.addEventListener("click", function () { var value = button.dataset.stateViewToggle; current.querySelectorAll("[data-state-view-toggle]").forEach(function (item) { var active = item === button; item.classList.toggle("is-active", active); item.setAttribute("aria-pressed", active ? "true" : "false"); }); current.querySelectorAll("[data-state-view-panel]").forEach(function (panel) { panel.hidden = panel.dataset.stateViewPanel !== value; }); }); });
    current.querySelectorAll("[data-state-character-select]").forEach(function (select) { select.addEventListener("change", function () { if (!select.value) return; navigateQuery(current, { character_id: select.value, state_scope: "character" }); }); });
    current.querySelectorAll("[data-state-search]").forEach(function (search) { search.addEventListener("input", function () { applyStateFilters(current, search.dataset.stateSearch); }); });
    current.querySelectorAll("[data-state-category-filter]").forEach(function (select) { select.addEventListener("change", function () { applyStateFilters(current, select.dataset.stateCategoryFilter); }); });
    current.querySelectorAll("[data-state-recency-filter]").forEach(function (select) { select.addEventListener("change", function () { applyStateFilters(current, select.dataset.stateRecencyFilter); }); });
    current.querySelectorAll("[data-state-sort]").forEach(function (select) { select.addEventListener("change", function () { var key = select.dataset.stateSort; var container = current.querySelector('[data-state-sort-container="' + key + '"]'); if (!container) return; var records = Array.from(container.querySelectorAll("[data-sort-name]")); records.sort(function (left, right) { if (select.value === "name") return String(left.dataset.sortName).localeCompare(String(right.dataset.sortName), "zh-CN"); var field = select.value === "first" ? "first" : "recent"; var difference = number(left.dataset[field]) - number(right.dataset[field]); return select.value === "first" ? difference : -difference; }); records.forEach(function (record) { container.appendChild(record); }); }); select.dispatchEvent(new Event("change")); });
    current.querySelectorAll("[data-knowledge-workspace]").forEach(function (workspace) { workspace.querySelectorAll("[data-knowledge-view]").forEach(function (button) { button.addEventListener("click", function () { var view = button.dataset.knowledgeView; workspace.querySelectorAll("[data-knowledge-view]").forEach(function (item) { var active = item === button; item.classList.toggle("is-active", active); item.setAttribute("aria-pressed", active ? "true" : "false"); }); workspace.querySelectorAll("[data-knowledge-panel]").forEach(function (panel) { panel.hidden = panel.dataset.knowledgePanel !== view; }); }); }); var build = workspace.querySelector("[data-build-knowledge-matrix]"); if (build) build.addEventListener("click", function () { buildKnowledgeMatrix(workspace); }); });
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
    current.querySelectorAll("[data-open-activity-center]").forEach(function (button) { button.addEventListener("click", function () { setActivityOpen(current, true); }); });
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

  function bindProgressionContracts(current) {
    var base = "/api/books/" + encodeURIComponent(current.dataset.bookId) + "/editions/" + encodeURIComponent(current.dataset.editionId) + "/progression-contracts";
    current.querySelectorAll("[data-infer-progression-contracts]").forEach(function (button) {
      button.addEventListener("click", function () {
        button.disabled = true;
        button.textContent = "正在冻结语义发现任务…";
        postJson(base + "/discovery", { context_chapter_id: current.dataset.currentChapterId || null }).then(function (result) {
          button.textContent = "任务已准备";
          button.title = result.handoff_id;
          var url = new URL(location.href);
          url.searchParams.set("activity_id", result.handoff_id);
          setTimeout(function () { loadWorkbench(url.href, { push: false, restoreState: Object.assign(captureNavigationState(current), { activityCenterOpen: true }) }); }, 350);
        }).catch(function (error) { button.disabled = false; button.textContent = error.message; });
      });
    });
    current.querySelectorAll("[data-confirm-progression-contract]").forEach(function (button) {
      button.addEventListener("click", function () {
        button.disabled = true;
        postJson(base + "/" + encodeURIComponent(button.dataset.confirmProgressionContract) + "/confirm", { effective_from_boundary: number(current.dataset.selectedChapterAnchor) || 0, author_notes: "作者在成长工作台逐项确认" }).then(function () { loadWorkbench(location.href, { push: false }); }).catch(function (error) { button.disabled = false; button.textContent = error.message; });
      });
    });
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
    current.querySelectorAll("[data-activate-edition]").forEach(function (button) {
      button.addEventListener("click", function () {
        var name = button.dataset.editionName || "这个版本";
        if (!window.confirm("将“" + name + "”设为当前正式版本。原正式版本会保留并归档，正式正文不会被删除。是否继续？")) return;
        button.disabled = true;
        postJson("/api/books/" + encodeURIComponent(current.dataset.bookId) + "/editions/" + encodeURIComponent(current.dataset.editionId) + "/activate", { confirmed: true }).then(function (result) {
          location.assign(result.redirect_url);
        }).catch(function (error) { button.disabled = false; button.textContent = error.message; });
      });
    });
    current.querySelectorAll("[data-workflow-workspace]").forEach(function (workspace) { var buttons = workspace.querySelectorAll("[data-workflow-mode]"); var panels = workspace.querySelectorAll("[data-workflow-mode-panel]"); function activate(target) { buttons.forEach(function (button) { button.setAttribute("aria-selected", button.dataset.workflowMode === target ? "true" : "false"); }); panels.forEach(function (panel) { panel.hidden = panel.dataset.workflowModePanel !== target; }); } buttons.forEach(function (button) { button.addEventListener("click", function () { activate(button.dataset.workflowMode); }); }); activate(workspace.dataset.workflowInitialMode || "continue"); });
    current.querySelectorAll("[data-workflow-form]").forEach(function (form) { form.addEventListener("submit", function (event) { event.preventDefault(); var payload = {}; new FormData(form).forEach(function (value, key) { if (key === "innovation_focus" || key === "author_task_ids") { payload[key] = payload[key] || []; payload[key].push(String(value)); } else payload[key] = value; }); postJson(form.action, payload).then(function (result) { var url = new URL(location.href); var kind = form.dataset.workflowKind || "continue"; url.searchParams.set("action", kind); url.searchParams.delete("mode"); if (result.handoff_id) url.searchParams.set("activity_id", result.handoff_id); loadWorkbench(url.href, { push: false, restoreState: Object.assign(captureNavigationState(current), { activityCenterOpen: true }) }); }).catch(function (error) { var node = form.querySelector("[data-workflow-feedback]"); if (node) { node.hidden = false; node.textContent = error.message; } }); }); });
  }

  function bindPendingActions(current) {
    if (!current.querySelector("[data-pending-action-id]")) return;
    var url = "/api/books/" + encodeURIComponent(current.dataset.bookId) + "/pending-actions?edition_id=" + encodeURIComponent(current.dataset.editionId);
    current._pendingActionTimer = setInterval(function () {
      fetch(url, { headers: { Accept: "application/json" } }).then(function (response) {
        if (!response.ok) throw new Error("pending-actions");
        return response.json();
      }).then(function (items) {
        items.forEach(function (item) {
          var card = current.querySelector('[data-pending-action-id="' + item.pending_action_id + '"]');
          if (!card) return;
          var status = card.querySelector(".workflow-status-chip");
          if (status) status.textContent = item.author_status;
          card.querySelectorAll(".wb-activity-timeline li").forEach(function (node, index) {
            var step = item.timeline[index];
            if (!step) return;
            node.className = "is-" + step.state;
          });
          if (item.resumed_handoff_id && !card.querySelector(".wb-activity-actions")) {
            var actions = document.createElement("div");
            actions.className = "wb-activity-actions";
            var button = document.createElement("button");
            button.type = "button";
            button.className = "button compact primary";
            button.dataset.copyInstruction = "/api/books/" + encodeURIComponent(current.dataset.bookId) + "/editions/" + encodeURIComponent(current.dataset.editionId) + "/handoffs/" + encodeURIComponent(item.resumed_handoff_id) + "/instruction";
            button.textContent = "复制给 Codex 的指令";
            bindInstructionCopy(button);
            actions.appendChild(button);
            card.insertBefore(actions, card.querySelector("details"));
          }
        });
      }).catch(function () { /* 下一轮继续，不打断作者输入。 */ });
    }, 5000);
  }

  function bindSearch(current) { var search = current.querySelector("[data-wb-chapter-search]"); if (!search) return; search.addEventListener("input", function () { var query = search.value.trim().toLowerCase(); current.querySelectorAll("[data-wb-chapter-item]").forEach(function (item) { item.hidden = Boolean(query && item.textContent.toLowerCase().indexOf(query) === -1); }); }); }

  function initWorkbench(current) { bindLayout(current); bindNavigation(current); bindScrollPersistence(current); bindActivityCenter(current); bindCommands(current); bindInspector(current); bindRelationshipGraph(current); bindStateWorkspace(current); bindItemModal(current); bindProfile(current); bindProgressionContracts(current); bindTruth(current); bindSecretBoard(current); bindDraft(current); bindWorkflow(current); bindPendingActions(current); bindSearch(current); current.querySelectorAll("[data-copy-instruction]").forEach(bindInstructionCopy); current.querySelectorAll("details[data-explorer-section]").forEach(function (item) { item.addEventListener("toggle", function () { saveFallback(current, captureNavigationState(current)); }); }); }

  window.addEventListener("popstate", function (event) { loadWorkbench(location.href, { push: false, fromPop: true, restoreState: event.state && event.state.workbenchState ? event.state.workbenchState : readFallback(root()) }); });
  var initial = root(); if (initial) { var state = history.state && history.state.workbenchState ? history.state.workbenchState : readFallback(initial); restoreDetails(initial, state); restoreLayout(initial, state); initWorkbench(initial); restoreNavigationState(initial, state); history.replaceState({ workbenchState: captureNavigationState(initial) }, "", location.href); }
}());
