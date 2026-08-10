(function () {
  "use strict";

  const root = document.documentElement;
  const storedTheme = window.localStorage.getItem("novel-theme");
  if (storedTheme) root.dataset.theme = storedTheme;

  document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
    button.addEventListener("click", function () {
      const next = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      window.localStorage.setItem("novel-theme", next);
    });
  });

  document.querySelectorAll("[data-chapter-search]").forEach(function (input) {
    input.addEventListener("input", function () {
      const query = input.value.trim().toLowerCase();
      document.querySelectorAll("[data-chapter-item]").forEach(function (item) {
        item.hidden = query !== "" && !item.textContent.toLowerCase().includes(query);
      });
    });
  });

  function openLatestChapter(bookId, editionId) {
    return fetch("/api/books/" + encodeURIComponent(bookId) + "/editions/" + encodeURIComponent(editionId) + "/chapters")
      .then(function (response) { return response.json(); })
      .then(function (chapters) {
        if (!chapters.length) return;
        window.location.href = "/books/" + encodeURIComponent(bookId) + "/editions/" + encodeURIComponent(editionId) + "/chapters/" + encodeURIComponent(chapters[chapters.length - 1].chapter_id);
      });
  }

  document.querySelectorAll("[data-edition-select]").forEach(function (select) {
    select.addEventListener("change", function () { openLatestChapter(select.dataset.bookId, select.value).catch(function () {}); });
  });
  document.querySelectorAll("[data-book-select]").forEach(function (select) {
    select.addEventListener("change", function () {
      fetch("/api/books/" + encodeURIComponent(select.value) + "/editions")
        .then(function (response) { return response.json(); })
        .then(function (editions) {
          const active = editions.find(function (edition) { return edition.status === "ACTIVE"; }) || editions[0];
          if (active) return openLatestChapter(select.value, active.edition_id);
          return undefined;
        })
        .catch(function () {});
    });
  });

  document.querySelectorAll("[data-view-tab]").forEach(function (tab) {
    tab.addEventListener("click", function () {
      const target = tab.dataset.viewTab;
      document.querySelectorAll("[data-view-tab]").forEach(function (item) { item.classList.toggle("active", item === tab); });
      document.querySelectorAll("[data-view-panel]").forEach(function (panel) { panel.hidden = panel.dataset.viewPanel !== target; });
    });
  });

  document.querySelectorAll("[data-segment-id]").forEach(function (segment) {
    segment.addEventListener("click", function () {
      document.querySelectorAll("[data-segment-id]").forEach(function (item) { item.classList.remove("selected"); });
      segment.classList.add("selected");
    });
  });

  document.querySelectorAll("[data-segment-link]").forEach(function (link) {
    link.addEventListener("click", function () {
      const segmentId = link.dataset.segmentLink;
      if (!segmentId) return;
      const target = document.getElementById("segment-" + segmentId);
      if (!target) return;
      document.querySelectorAll("[data-segment-id]").forEach(function (item) { item.classList.remove("selected"); });
      target.classList.add("selected");
      target.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });

  document.querySelectorAll("[data-component-id]").forEach(function (chip) {
    chip.addEventListener("click", function () {
      document.querySelectorAll("[data-component-id]").forEach(function (item) { item.classList.remove("selected"); });
      chip.classList.add("selected");
      const card = chip.closest("[data-metric-id]");
      const componentKey = chip.dataset.componentId || "";
      const evidence = card && (card.querySelector('[data-evidence-component="' + CSS.escape(componentKey) + '"] [data-segment-link]') || card.querySelector("[data-segment-link]"));
      if (evidence) evidence.click();
      const observationId = chip.dataset.observationId;
      if (!observationId) return;
      const row = document.querySelector('[data-observation-row="' + CSS.escape(observationId) + '"]');
      if (row) row.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });

  document.querySelectorAll("[data-value-mirror]").forEach(function (slider) {
    const target = slider.parentElement && slider.parentElement.parentElement
      ? slider.parentElement.parentElement.querySelector("[data-value-target]")
      : null;
    if (!target) return;
    slider.addEventListener("input", function () { target.value = slider.value; });
    target.addEventListener("input", function () { slider.value = target.value; });
  });

  function csrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.content : "";
  }

  document.querySelectorAll("form[data-api-form]").forEach(function (form) {
    form.querySelectorAll('[data-innovation-auto]').forEach(function (auto) {
      auto.addEventListener("change", function () {
        if (!auto.checked) return;
        form.querySelectorAll('input[name="innovation_focus"]:not([data-innovation-auto])').forEach(function (item) {
          item.checked = false;
        });
      });
    });
    form.querySelectorAll('input[name="innovation_focus"]:not([data-innovation-auto])').forEach(function (item) {
      item.addEventListener("change", function () {
        if (item.checked) {
          const auto = form.querySelector('[data-innovation-auto]');
          if (auto) auto.checked = false;
        }
      });
    });
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const formData = new FormData(form);
      const payload = {};
      formData.forEach(function (value, key) {
        if (key === "evidence_segment_ids") return;
        if (key === "innovation_focus") {
          if (!Array.isArray(payload[key])) payload[key] = [];
          payload[key].push(String(value));
          return;
        }
        payload[key] = value;
      });
      const evidenceSegments = Array.from(form.querySelectorAll('[data-evidence-segment]:checked')).slice(0, 2);
      if (evidenceSegments.length) {
        payload.evidence_links = evidenceSegments.map(function (input) {
          return {
            segment_id: input.value,
            contribution_kind: "AUTHOR_EVIDENCE",
            direction: "SUPPORTS",
            confidence: 1,
            evidence_quote: input.dataset.quote || "",
            rationale: "作者在 Workbench 中选择的段落",
          };
        });
      }
      if (payload.value === "") payload.value = null;
      const valueInput = form.querySelector('[name="value"]');
      if (valueInput && (valueInput.type === "range" || valueInput.type === "number")) payload.value = Number(payload.value);
      fetch(form.action, { method: "POST", headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() }, body: JSON.stringify(payload) })
        .then(function (response) { return response.json().then(function (body) { return { ok: response.ok, body: body }; }); })
        .then(function (result) {
          const notice = document.createElement("p");
          notice.className = result.ok ? "callout" : "callout disputed";
          notice.textContent = result.ok ? "已保存；页面将重新加载当前审核状态。" : ((result.body.error && result.body.error.message) || "保存失败");
          form.appendChild(notice);
          if (result.ok) window.setTimeout(function () { window.location.reload(); }, 500);
        })
        .catch(function () { const notice = document.createElement("p"); notice.className = "callout disputed"; notice.textContent = "请求失败，请刷新后重试。"; form.appendChild(notice); });
    });
  });

  document.querySelectorAll("[data-copy-instruction]").forEach(function (button) {
    button.addEventListener("click", function () {
      fetch(button.dataset.copyInstruction)
        .then(function (response) { return response.json(); })
        .then(function (body) {
          const instruction = body.instruction || "";
          return navigator.clipboard.writeText(instruction).then(function () {
            button.textContent = "已复制";
            window.setTimeout(function () { button.textContent = "复制指令"; }, 1500);
          });
        })
        .catch(function () { button.textContent = "复制失败"; });
    });
  });

  function atlasPathParts() {
    const parts = window.location.pathname.split("/").filter(Boolean);
    return { bookId: parts[1] || "", editionId: parts[3] || "" };
  }

  function atlasCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.content : "";
  }

  function atlasAction(actionType, node, graphData) {
    const parts = atlasPathParts();
    const atlas = graphData.atlas || {};
    return fetch("/api/books/" + encodeURIComponent(parts.bookId) + "/editions/" + encodeURIComponent(parts.editionId) + "/atlas/actions", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRF-Token": atlasCsrfToken() },
      body: JSON.stringify({
        action_type: actionType,
        target_id: node.node_id,
        payload: { target_type: node.node_type },
        expected_atlas_id: atlas.atlas_id || null,
        expected_atlas_version: atlas.atlas_version || null,
        expected_manifest_hash: atlas.artifact_manifest_sha256 || null,
      }),
    }).then(function (response) {
      return response.json().then(function (body) {
        if (!response.ok) throw new Error((body.error && body.error.message) || "作者操作失败");
        return body;
      });
    });
  }

  function showAtlasDetail(detail, node, graphData) {
    while (detail.firstChild) detail.removeChild(detail.firstChild);
    const heading = document.createElement("h2");
    heading.textContent = node.name || node.node_id;
    detail.appendChild(heading);
    const status = document.createElement("p");
    status.textContent = (node.information_status || "UNKNOWN") + " · " + (node.constraint_level || "") + " · " + (node.horizon || "") + " · confidence=" + (node.confidence || "UNKNOWN");
    detail.appendChild(status);
    const description = document.createElement("p");
    description.textContent = node.description || "当前没有额外说明。";
    detail.appendChild(description);
    const evidence = document.createElement("p");
    const evidenceData = node.evidence || {};
    const evidenceIds = [].concat(evidenceData.source_span_ids || [], evidenceData.chapter_ids || [], evidenceData.canon_fact_ids || [], evidenceData.event_ids || []);
    evidence.textContent = "Evidence: " + (evidenceIds.join(", ") || "UNKNOWN");
    detail.appendChild(evidence);
    const actions = document.createElement("div");
    actions.className = "actions";
    [
      ["ACCEPT_SOFT_ANCHOR", "接受 Soft Anchor"],
      ["REJECT_FUTURE_CANDIDATE", "拒绝 Future Candidate"],
      ["ADD_AUTHOR_INTENT", "标记 Author Intent"],
      ["ADD_REVIEW_QUEUE", "加入 Review Queue"],
    ].forEach(function (item) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "button";
      button.textContent = item[1];
      button.addEventListener("click", function () {
        atlasAction(item[0], node, graphData).then(function () {
          button.textContent = "已记录";
          button.disabled = true;
        }).catch(function (error) { button.textContent = error.message; });
      });
      actions.appendChild(button);
    });
    detail.appendChild(actions);
  }

  document.querySelectorAll("[data-atlas-canvas]").forEach(function (svg) {
    let graphData;
    try { graphData = JSON.parse(svg.dataset.graph || "{}"); } catch (error) { return; }
    const nodes = graphData.nodes || [];
    const edges = graphData.edges || [];
    const width = 900;
    const height = Math.max(420, Math.ceil(nodes.length / 4) * 130);
    svg.setAttribute("viewBox", "0 0 " + width + " " + height);
    const positions = {};
    nodes.forEach(function (node, index) {
      positions[node.node_id] = { x: 120 + (index % 4) * 220, y: 70 + Math.floor(index / 4) * 120 };
    });
    edges.forEach(function (edge) {
      const from = positions[edge.from_id];
      const to = positions[edge.to_id];
      if (!from || !to) return;
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", from.x); line.setAttribute("y1", from.y);
      line.setAttribute("x2", to.x); line.setAttribute("y2", to.y);
      line.setAttribute("class", "atlas-edge " + String(edge.information_status || "unknown").toLowerCase());
      svg.appendChild(line);
    });
    const detail = document.querySelector("[data-atlas-detail]");
    nodes.forEach(function (node) {
      const position = positions[node.node_id];
      const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
      group.setAttribute("class", "atlas-svg-node " + String(node.information_status || "unknown").toLowerCase());
      group.setAttribute("tabindex", "0");
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", position.x); circle.setAttribute("cy", position.y); circle.setAttribute("r", "24");
      const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("x", position.x); label.setAttribute("y", position.y + 46); label.setAttribute("text-anchor", "middle");
      label.textContent = node.name || node.node_id;
      group.appendChild(circle); group.appendChild(label); svg.appendChild(group);
      if (detail) {
        group.addEventListener("click", function () { showAtlasDetail(detail, node, graphData); });
        group.addEventListener("keydown", function (event) { if (event.key === "Enter" || event.key === " ") showAtlasDetail(detail, node, graphData); });
      }
    });
    document.querySelectorAll("[data-atlas-node]").forEach(function (card) {
      let node;
      try { node = JSON.parse(card.dataset.atlasNode || "{}"); } catch (error) { return; }
      card.addEventListener("click", function () { if (detail) showAtlasDetail(detail, node, graphData); });
    });
  });
}());

(function () {
  "use strict";

  var layoutKey = "novel-authoring-workbench-layout";

  function csrfToken() {
    var meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.content : "";
  }

  function readLayout(root) {
    var key = root && root.dataset.layoutKey ? root.dataset.layoutKey : layoutKey;
    try { return JSON.parse(window.localStorage.getItem(key) || "{}"); } catch (error) { return {}; }
  }

  function saveLayout(root) {
    var key = root && root.dataset.layoutKey ? root.dataset.layoutKey : layoutKey;
    var value = {
      left: root.style.getPropertyValue("--wb-left"),
      right: root.style.getPropertyValue("--wb-right"),
      leftCollapsed: root.classList.contains("is-left-collapsed"),
      rightCollapsed: root.classList.contains("is-right-collapsed"),
      mainMode: root.dataset.activeMode || "continue",
      rightTab: root.dataset.activeRightTab || "prose",
      stateTab: root.dataset.activeStateTab || "character"
    };
    try { window.localStorage.setItem(key, JSON.stringify(value)); } catch (error) { /* local persistence is optional */ }
  }

  function updatePaneButtons(root, side) {
    var collapsed = root.classList.contains("is-" + side + "-collapsed");
    var label = (collapsed ? "展开" : "隐藏") + (side === "left" ? "左栏" : "右栏");
    var icon = side === "left" ? (collapsed ? "›" : "‹") : (collapsed ? "‹" : "›");
    document.querySelectorAll('[data-toggle-pane="' + side + '"]').forEach(function (button) {
      button.setAttribute("aria-label", label);
      button.setAttribute("title", label);
      var text = button.querySelector("[data-pane-toggle-label]");
      if (text) text.textContent = label;
      var symbol = button.querySelector("[data-pane-toggle-icon]");
      if (symbol) symbol.textContent = icon;
    });
  }

  function stateFromUrl(key) {
    try { return new URL(window.location.href).searchParams.get(key) || ""; } catch (error) { return ""; }
  }

  function setWorkbenchQuery(key, value) {
    try {
      var url = new URL(window.location.href);
      url.searchParams.set(key, value);
      window.history.replaceState({}, "", url.href);
    } catch (error) { /* URL state is a convenience, not a data write. */ }
  }

  function addWorkbenchState(href, root) {
    try {
      var url = new URL(href, window.location.href);
      var saved = readLayout(root);
      var mode = root.dataset.activeMode || saved.mainMode || "continue";
      var rightTab = root.dataset.activeRightTab || saved.rightTab || "prose";
      var stateTab = root.dataset.activeStateTab || saved.stateTab || "character";
      var characterId = root.dataset.selectedCharacterId || stateFromUrl("character_id") || "";
      if (!url.searchParams.get("mode")) url.searchParams.set("mode", mode);
      if (!url.searchParams.get("right_tab")) url.searchParams.set("right_tab", rightTab);
      if (!url.searchParams.get("state_tab")) url.searchParams.set("state_tab", stateTab);
      if (!url.searchParams.get("character_id") && characterId) url.searchParams.set("character_id", characterId);
      return url.href;
    } catch (error) { return href; }
  }

  function initLayout(root) {
    var saved = readLayout(root);
    if (saved.left) root.style.setProperty("--wb-left", saved.left);
    if (saved.right) root.style.setProperty("--wb-right", saved.right);
    if (saved.leftCollapsed) root.classList.add("is-left-collapsed");
    if (saved.rightCollapsed) root.classList.add("is-right-collapsed");
    updatePaneButtons(root, "left");
    updatePaneButtons(root, "right");

    document.querySelectorAll("[data-toggle-pane]").forEach(function (button) {
      if (button.dataset.wbPaneBound === "true") return;
      button.dataset.wbPaneBound = "true";
      button.addEventListener("click", function () {
        var current = document.querySelector("[data-workbench-shell]");
        if (!current) return;
        var side = button.dataset.togglePane;
        current.classList.toggle("is-" + side + "-collapsed");
        updatePaneButtons(current, side);
        saveLayout(current);
      });
    });

    root.querySelectorAll("[data-resizer]").forEach(function (resizer) {
      resizer.addEventListener("pointerdown", function (event) {
        if (window.innerWidth < 900) return;
        event.preventDefault();
        var side = resizer.dataset.resizer;
        var move = function (moveEvent) {
          var maximum = Math.min(window.innerWidth * 0.42, side === "left" ? window.innerWidth - 520 : window.innerWidth * 0.48);
          if (side === "left") {
            root.style.setProperty("--wb-left", Math.max(220, Math.min(maximum, moveEvent.clientX)) + "px");
          } else {
            var width = window.innerWidth - moveEvent.clientX;
            root.style.setProperty("--wb-right", Math.max(300, Math.min(maximum, width)) + "px");
          }
        };
        var stop = function () {
          document.removeEventListener("pointermove", move);
          document.removeEventListener("pointerup", stop);
          saveLayout(root);
        };
        document.addEventListener("pointermove", move);
        document.addEventListener("pointerup", stop, { once: true });
      });
    });
  }

  function initContextTabs(root) {
    root.querySelectorAll("[data-wb-context-tab]").forEach(function (button) {
      button.addEventListener("click", function () {
        var target = button.dataset.wbContextTab;
        root.querySelectorAll("[data-wb-context-tab]").forEach(function (item) { item.classList.toggle("is-active", item === button); });
        root.querySelectorAll("[data-wb-context-panel]").forEach(function (panel) { panel.hidden = panel.dataset.wbContextPanel !== target; });
      });
    });
  }

  function applyMainMode(root, target, persist) {
    var mode = target || "continue";
    var buttons = root.querySelectorAll("[data-wb-mode]");
    var panels = root.querySelectorAll("[data-wb-mode-panel]");
    var matched = false;
    buttons.forEach(function (button) {
      var active = button.dataset.wbMode === mode;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-selected", active ? "true" : "false");
      if (active) matched = true;
    });
    if (!matched) mode = "continue";
    panels.forEach(function (panel) { panel.hidden = panel.dataset.wbModePanel !== mode; });
    root.dataset.activeMode = mode;
    if (persist) {
      setWorkbenchQuery("mode", mode);
      saveLayout(root);
    }
  }

  function applyRightTab(root, target, persist) {
    var tab = target || "prose";
    var buttons = root.querySelectorAll("[data-wb-editor-tab]");
    var matched = false;
    buttons.forEach(function (button) {
      var active = button.dataset.wbEditorTab === tab;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-selected", active ? "true" : "false");
      if (active) matched = true;
    });
    if (!matched) tab = "prose";
    root.querySelectorAll("[data-wb-editor-secondary]").forEach(function (panel) {
      panel.hidden = panel.dataset.wbEditorSecondary !== tab;
    });
    var prosePanel = root.querySelector("[data-wb-editor-prose]");
    if (prosePanel) prosePanel.hidden = tab !== "prose";
    root.dataset.activeRightTab = tab;
    if (persist) {
      setWorkbenchQuery("right_tab", tab);
      saveLayout(root);
    }
  }

  function initEditor(root) {
    root.querySelectorAll("[data-wb-mode]").forEach(function (button) {
      button.addEventListener("click", function () {
        applyMainMode(root, button.dataset.wbMode, true);
      });
    });
    root.querySelectorAll("[data-wb-editor-tab]").forEach(function (button) {
      button.addEventListener("click", function () {
        applyRightTab(root, button.dataset.wbEditorTab, true);
      });
    });
    var saved = readLayout(root);
    applyMainMode(root, stateFromUrl("mode") || saved.mainMode || root.dataset.activeMode || "continue", false);
    applyRightTab(root, stateFromUrl("right_tab") || saved.rightTab || root.dataset.activeRightTab || "prose", false);
    root.querySelectorAll("[data-wb-editor-view]").forEach(function (button) {
      button.addEventListener("click", function () {
        var target = button.dataset.wbEditorView;
        root.querySelectorAll("[data-wb-editor-view]").forEach(function (item) { item.classList.toggle("is-active", item === button); });
        root.querySelectorAll("[data-wb-editor-panel]").forEach(function (panel) { panel.hidden = panel.dataset.wbEditorPanel !== target; });
      });
    });
    root.querySelectorAll("[data-wb-editor]").forEach(function (editor) {
      var counter = root.querySelector("[data-wb-word-count]");
      var update = function () { if (counter) counter.textContent = Array.from(editor.value || "").length + " 字"; };
      editor.addEventListener("input", update);
      update();
    });
    root.querySelectorAll("[data-wb-draft-form]").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var editor = form.querySelector("[name=content]");
        var expected = form.querySelector("[name=expected_content_sha256]");
        fetch(form.action, {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() },
          body: JSON.stringify({ content: editor ? editor.value : "", expected_content_sha256: expected ? expected.value : null })
        }).then(function (response) {
          return response.json().then(function (body) { return { ok: response.ok, body: body }; });
        }).then(function (result) {
          var notice = document.createElement("p");
          notice.className = result.ok ? "callout" : "callout disputed";
          notice.textContent = result.ok ? "草稿已保存，验证状态已清空。" : ((result.body.error && result.body.error.message) || "保存失败");
          form.appendChild(notice);
          if (result.ok) window.setTimeout(function () { window.location.reload(); }, 500);
        }).catch(function () {
          var notice = document.createElement("p");
          notice.className = "callout disputed";
          notice.textContent = "请求失败，请刷新后重试。";
          form.appendChild(notice);
        });
      });
    });
    var search = root.querySelector("[data-wb-chapter-search]");
    if (search) search.addEventListener("input", function () {
      var query = search.value.trim().toLowerCase();
      root.querySelectorAll("[data-wb-chapter-item]").forEach(function (item) {
        item.hidden = query && item.textContent.toLowerCase().indexOf(query) === -1;
      });
    });
  }

  function authorControlPath(root) {
    return "/api/books/" + encodeURIComponent(root.dataset.bookId || "") + "/editions/" + encodeURIComponent(root.dataset.editionId || "") + "/author-commands";
  }

  function commandContext(root) {
    return {
      chapter_id: stateFromUrl("chapter_id") || root.dataset.currentChapterId || null,
      character_id: root.dataset.selectedCharacterId || stateFromUrl("character_id") || null
    };
  }

  function showCommandNotice(form, result) {
    var old = form.querySelector("[data-command-notice]");
    if (old) old.remove();
    var notice = document.createElement("p");
    notice.dataset.commandNotice = "true";
    notice.className = "wb-command-notice" + (result.result === "REJECTED" ? " is-rejected" : "");
    notice.textContent = (result.result === "REJECTED" ? "已拦截：" : "已记录：") + (result.message || "命令已处理");
    if (result.allowed_actions && result.allowed_actions.length) {
      notice.textContent += " 可选：" + result.allowed_actions.join("、");
    }
    form.appendChild(notice);
  }

  function commandPayload(form, commandType) {
    var payload = {};
    form.querySelectorAll("input[name], select[name], textarea[name]").forEach(function (field) {
      if (field.value !== "") payload[field.name] = field.value;
    });
    return { command_type: commandType, payload: payload };
  }

  function postAuthorCommand(root, command) {
    var context = commandContext(root);
    command.chapter_id = context.chapter_id;
    command.character_id = context.character_id;
    return fetch(authorControlPath(root), {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() },
      body: JSON.stringify(command)
    }).then(function (response) {
      return response.json().then(function (body) {
        if (!response.ok) throw new Error((body.error && body.error.message) || "作者命令失败");
        return body;
      });
    });
  }

  function initStateTabs(root) {
    var buttons = root.querySelectorAll("[data-wb-state-tab]");
    if (!buttons.length) return;
    var activate = function (target, persist) {
      var matched = false;
      buttons.forEach(function (button) {
        var active = button.dataset.wbStateTab === target;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-selected", active ? "true" : "false");
        if (active) matched = true;
      });
      if (!matched) target = "character";
      root.querySelectorAll("[data-wb-state-panel]").forEach(function (panel) {
        panel.hidden = panel.dataset.wbStatePanel !== target;
      });
      root.dataset.activeStateTab = target;
      if (persist) {
        setWorkbenchQuery("state_tab", target);
        saveLayout(root);
      }
    };
    buttons.forEach(function (button) {
      button.addEventListener("click", function () { activate(button.dataset.wbStateTab, true); });
    });
    var saved = readLayout(root);
    activate(stateFromUrl("state_tab") || saved.stateTab || "character", false);

    root.querySelectorAll("[data-author-command-form]").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var command = commandPayload(form, form.dataset.commandType || "CREATE_TASK");
        postAuthorCommand(root, command).then(function (result) {
          showCommandNotice(form, result);
          if (result.result === "PLANNED") window.setTimeout(function () { window.location.reload(); }, 650);
        }).catch(function (error) { showCommandNotice(form, { result: "REJECTED", message: error.message }); });
      });
    });

    root.querySelectorAll("[data-task-lifecycle]").forEach(function (select) {
      select.addEventListener("change", function () {
        var taskId = select.dataset.taskId;
        if (!taskId) return;
        postAuthorCommand(root, {
          command_type: "UPDATE_TASK",
          payload: { task_id: taskId, lifecycle_status: select.value }
        }).then(function () { window.location.reload(); }).catch(function () {
          window.alert("任务状态更新失败，请刷新后重试。");
        });
      });
    });

    root.querySelectorAll("[data-task-board-view-button]").forEach(function (button) {
      button.addEventListener("click", function () {
        var target = button.dataset.taskBoardViewButton;
        root.querySelectorAll("[data-task-board-view-button]").forEach(function (item) {
          item.classList.toggle("is-active", item === button);
        });
        root.querySelectorAll("[data-task-board-panel]").forEach(function (panel) {
          panel.hidden = panel.dataset.taskBoardPanel !== target;
        });
      });
    });

    root.querySelectorAll("[data-item-card], .wb-item-card").forEach(function (card) {
      card.addEventListener("click", function () {
        var inspector = root.querySelector("[data-state-inspector]");
        if (!inspector) return;
        var record = {};
        try { record = JSON.parse(card.dataset.stateRecord || "{}"); } catch (error) { record = {}; }
        inspector.innerHTML = "";
        var title = document.createElement("strong");
        title.textContent = record.name || "状态记录";
        var status = document.createElement("span");
        status.textContent = (record.statusLabel || record.status_label || "尚未知")
          + " · 持有者 " + (record.current_holder_id || record.owner_id || "UNKNOWN")
          + " · 数量 " + (record.quantity == null ? "UNKNOWN" : record.quantity)
          + (record.equipped ? " · 已装备" : "")
          + (record.slot ? " · 槽位 " + record.slot : "");
        var statement = document.createElement("p");
        statement.textContent = (record.description || record.statement || "暂无说明")
          + " · 首次确认第" + (record.first_acquired_chapter_ordinal || "UNKNOWN")
          + "章 · 最近确认第" + (record.recent_confirmed_chapter_ordinal || record.chapter_ordinal || "UNKNOWN") + "章";
        inspector.appendChild(title); inspector.appendChild(status); inspector.appendChild(statement);
        [
          ["用途", record.use],
          ["约束", record.constraints],
          ["证据", (record.source_span_ids || []).join("、") || "暂无 source span"],
          ["关联能力/人物/关系", [record.related_ability_id, record.related_person_id, record.related_relationship_id].filter(Boolean).join("、") || "暂无"],
        ].forEach(function (item) {
          if (!item[1]) return;
          var line = document.createElement("small");
          line.textContent = item[0] + "：" + item[1];
          inspector.appendChild(line);
        });
      });
    });

    root.querySelectorAll("[data-knowledge-cell]").forEach(function (cell) {
      cell.addEventListener("click", function () {
        var inspector = root.querySelector("[data-knowledge-inspector]");
        if (!inspector) return;
        var record = {};
        try { record = JSON.parse(cell.dataset.knowledgeCell || "{}"); } catch (error) { record = {}; }
        inspector.innerHTML = "";
        var title = document.createElement("strong");
        title.textContent = (record.knower_name || record.knower_id || "UNKNOWN") + " × " + (record.topic_name || record.topic_id || "主题");
        var status = document.createElement("span");
        status.textContent = (record.state || "UNKNOWN") + " · " + (record.layer || "UNKNOWN")
          + " · 证据章节 " + (record.evidence_chapter_ordinal || "UNKNOWN");
        var evidence = document.createElement("p");
        evidence.textContent = "source spans：" + ((record.source_span_ids || []).join("、") || "无；UNKNOWN 不是推断出的否定");
        inspector.appendChild(title); inspector.appendChild(status); inspector.appendChild(evidence);
      });
    });

    root.querySelectorAll("[data-relationship-record]").forEach(function (card) {
      card.addEventListener("click", function () {
        var inspector = root.querySelector("[data-relationship-inspector]");
        if (!inspector) return;
        var record = {};
        try { record = JSON.parse(card.dataset.relationshipRecord || "{}"); } catch (error) { record = {}; }
        inspector.innerHTML = "";
        var title = document.createElement("strong");
        title.textContent = record.name || ((record.from_entity_id || "A") + " ↔ " + (record.to_entity_id || "B"));
        var summary = document.createElement("span");
        summary.textContent = "当前层 " + (record.current_layer || record.layer || "UNKNOWN")
          + " · 首次第" + (record.first_confirmed_chapter_ordinal || "UNKNOWN")
          + "章 · 最近第" + (record.recent_confirmed_chapter_ordinal || "UNKNOWN") + "章";
        var dimensions = document.createElement("p");
        var values = record.dimensions || {};
        dimensions.textContent = Object.keys(values).map(function (key) { return key + "=" + values[key]; }).join(" · ") || "暂无叙事维度证据";
        inspector.appendChild(title); inspector.appendChild(summary); inspector.appendChild(dimensions);
      });
    });

    var draggingTask = null;
    root.querySelectorAll("[data-author-task-id]").forEach(function (card) {
      card.addEventListener("dragstart", function (event) {
        draggingTask = card.dataset.authorTaskId;
        if (event.dataTransfer) event.dataTransfer.setData("text/plain", draggingTask);
      });
    });
    root.querySelectorAll("[data-author-item-id]").forEach(function (card) {
      card.addEventListener("dragstart", function (event) {
        if (event.dataTransfer) event.dataTransfer.setData("text/plain", card.dataset.authorItemId);
      });
    });
    root.querySelectorAll("[data-task-horizon-drop]").forEach(function (target) {
      target.addEventListener("dragover", function (event) { event.preventDefault(); target.classList.add("is-drag-over"); });
      target.addEventListener("dragleave", function () { target.classList.remove("is-drag-over"); });
      target.addEventListener("drop", function (event) {
        event.preventDefault();
        target.classList.remove("is-drag-over");
        var taskId = draggingTask || (event.dataTransfer && event.dataTransfer.getData("text/plain"));
        if (!taskId) return;
        postAuthorCommand(root, { command_type: "MOVE_TASK_HORIZON", payload: { task_id: taskId, horizon: target.dataset.taskHorizonDrop } })
          .then(function () { window.location.reload(); })
          .catch(function () { window.alert("任务跨度调整失败，请刷新后重试。"); });
      });
    });
    root.querySelectorAll("[data-task-horizon-select]").forEach(function (select) {
      select.addEventListener("change", function () {
        postAuthorCommand(root, {
          command_type: "MOVE_TASK_HORIZON",
          payload: { task_id: select.dataset.taskId, horizon: select.value }
        })
          .then(function () { window.location.reload(); })
          .catch(function () { window.alert("任务跨度调整失败，请刷新后重试。"); });
      });
    });
    root.querySelectorAll("[data-drop-target]").forEach(function (target) {
      target.addEventListener("dragover", function (event) { event.preventDefault(); target.classList.add("is-drag-over"); });
      target.addEventListener("dragleave", function () { target.classList.remove("is-drag-over"); });
      target.addEventListener("drop", function (event) {
        event.preventDefault();
        target.classList.remove("is-drag-over");
        var itemId = event.dataTransfer && event.dataTransfer.getData("text/plain");
        if (!itemId) return;
        postAuthorCommand(root, { command_type: "DROP_ITEM", payload: { item_id: itemId, destination: target.dataset.dropTarget } })
          .then(function (result) { showCommandNotice(target.parentElement || target, result); })
          .catch(function (error) { showCommandNotice(target.parentElement || target, { result: "REJECTED", message: error.message }); });
      });
    });
    initRelationshipGraph(root);
  }

  function initRelationshipGraph(root) {
    root.querySelectorAll("[data-wb-relationship-graph]").forEach(function (container) {
      var graph = [];
      try { graph = JSON.parse(container.dataset.graph || "[]"); } catch (error) { graph = []; }
      if (!graph.length) return;
      while (container.firstChild) container.removeChild(container.firstChild);
      var names = [];
      var edges = graph.map(function (edge) {
        var from = edge.from_name || (edge.raw && edge.raw.from_entity_id) || edge.name || "当前人物";
        var to = edge.to_name || (edge.raw && edge.raw.to_entity_id) || edge.name || "关系目标";
        if (names.indexOf(from) === -1) names.push(from);
        if (names.indexOf(to) === -1) names.push(to);
        return { from: from, to: to, label: edge.label || edge.statement || edge.name || "关系" };
      });
      var width = 720;
      var height = Math.max(150, Math.ceil(names.length / 3) * 100);
      var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("viewBox", "0 0 " + width + " " + height);
      var positions = {};
      names.forEach(function (name, index) {
        positions[name] = { x: 120 + (index % 3) * 240, y: 50 + Math.floor(index / 3) * 90 };
      });
      edges.forEach(function (edge) {
        var from = positions[edge.from]; var to = positions[edge.to];
        if (!from || !to) return;
        var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", from.x); line.setAttribute("y1", from.y); line.setAttribute("x2", to.x); line.setAttribute("y2", to.y); line.setAttribute("class", "wb-relationship-edge");
        svg.appendChild(line);
      });
      names.forEach(function (name) {
        var position = positions[name];
        var group = document.createElementNS("http://www.w3.org/2000/svg", "g");
        group.setAttribute("class", "wb-relationship-node");
        var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", position.x); circle.setAttribute("cy", position.y); circle.setAttribute("r", "25");
        var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", position.x); text.setAttribute("y", position.y + 45); text.textContent = name;
        group.appendChild(circle); group.appendChild(text); svg.appendChild(group);
      });
      container.appendChild(svg);
      var legend = document.createElement("p"); legend.className = "wb-state-note"; legend.textContent = "连线是当前关系或软参考关系；新增关系会进入作者意图。"; container.appendChild(legend);
    });
  }

  function workflowPayload(form) {
    var payload = {};
    new FormData(form).forEach(function (value, key) {
      if (key === "innovation_focus" || key === "author_task_ids") {
        if (!Array.isArray(payload[key])) payload[key] = [];
        payload[key].push(String(value));
        return;
      }
      payload[key] = value;
    });
    if (!payload.innovation_focus || !payload.innovation_focus.length) payload.innovation_focus = ["auto"];
    if (!String(payload.author_goal || "").trim()) payload.author_goal = null;
    return payload;
  }

  function workflowFeedback(form, message, isError) {
    var feedback = form.querySelector("[data-workflow-feedback]");
    if (!feedback) return;
    feedback.hidden = false;
    feedback.classList.toggle("is-error", Boolean(isError));
    feedback.textContent = message;
  }

  function initWorkflowForms(workspace) {
    workspace.querySelectorAll("[data-workflow-form]").forEach(function (form) {
      var auto = form.querySelector("[data-innovation-auto]");
      if (auto) auto.addEventListener("change", function () {
        if (!auto.checked) return;
        form.querySelectorAll('input[name="innovation_focus"]:not([data-innovation-auto])').forEach(function (item) { item.checked = false; });
      });
      form.querySelectorAll('input[name="innovation_focus"]:not([data-innovation-auto])').forEach(function (item) {
        item.addEventListener("change", function () {
          if (!item.checked || !auto) return;
          auto.checked = false;
        });
      });
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var button = form.querySelector("[data-workflow-submit-label]");
        var original = button ? button.dataset.workflowSubmitLabel : "提交任务";
        if (button) { button.disabled = true; button.textContent = "准备中…"; }
        workflowFeedback(form, "正在冻结当前章节上下文，请稍候…", false);
        fetch(form.action, {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() },
          body: JSON.stringify(workflowPayload(form))
        }).then(function (response) {
          return response.json().then(function (body) { return { ok: response.ok, body: body }; });
        }).then(function (result) {
          if (!result.ok) {
            var error = result.body.error && result.body.error.message ? result.body.error.message : "任务暂时无法准备";
            workflowFeedback(form, "无法准备任务：" + error, true);
            if (button) { button.disabled = false; button.textContent = original; }
            return;
          }
          workflowFeedback(form, "✓ 任务已经准备好，正在刷新当前工作列表…", false);
          if (button) button.textContent = "已准备";
          window.setTimeout(function () { window.location.reload(); }, 900);
        }).catch(function () {
          workflowFeedback(form, "无法连接到本地工作流服务，请刷新后重试。", true);
          if (button) { button.disabled = false; button.textContent = original; }
        });
      });
    });
  }

  function initWorkflowWorkspaces() {
    document.querySelectorAll("[data-workflow-workspace]").forEach(function (workspace) {
      var buttons = workspace.querySelectorAll("[data-workflow-mode]");
      var panels = workspace.querySelectorAll("[data-workflow-mode-panel]");
      var activate = function (target) {
        var matched = false;
        buttons.forEach(function (button) {
          var active = button.dataset.workflowMode === target;
          button.setAttribute("aria-selected", active ? "true" : "false");
          if (active) matched = true;
        });
        if (!matched && buttons.length) target = "continue";
        panels.forEach(function (panel) { panel.hidden = panel.dataset.workflowModePanel !== target; });
        workspace.dataset.activeWorkflowMode = target;
      };
      buttons.forEach(function (button) { button.addEventListener("click", function () { activate(button.dataset.workflowMode); }); });
      activate(workspace.dataset.workflowInitialMode || "continue");
      initWorkflowForms(workspace);
      workspace.querySelectorAll("[data-workflow-task-toggle]").forEach(function (button) {
        button.addEventListener("click", function () {
          var row = button.closest("[data-workflow-task-row]");
          var details = row && row.querySelector("[data-workflow-task-details]");
          if (!details) return;
          details.open = !details.open;
          button.textContent = details.open ? "收起任务" : "查看任务";
        });
      });
    });
  }

  function loadWorkbench(link, push) {
    var currentRoot = document.querySelector("[data-workbench-shell]");
    var href = push && currentRoot ? addWorkbenchState(link.href, currentRoot) : link.href;
    var scrollX = window.scrollX;
    var scrollY = window.scrollY;
    var currentTree = currentRoot ? currentRoot.querySelector(".wb-tree") : null;
    var treeScrollLeft = currentTree ? currentTree.scrollLeft : 0;
    var treeScrollTop = currentTree ? currentTree.scrollTop : 0;
    fetch(href, { headers: { Accept: "text/html" } }).then(function (response) {
      if (!response.ok) throw new Error("Workbench 页面加载失败");
      return response.text();
    }).then(function (html) {
      var parsed = new DOMParser().parseFromString(html, "text/html");
      var next = parsed.querySelector("[data-workbench-shell]");
      var current = document.querySelector("[data-workbench-shell]");
      if (!next || !current) { window.location.href = link.href; return; }
      current.replaceWith(next);
      var nextBreadcrumb = parsed.querySelector("[data-wb-breadcrumb]");
      var currentBreadcrumb = document.querySelector("[data-wb-breadcrumb]");
      if (nextBreadcrumb && currentBreadcrumb) currentBreadcrumb.replaceWith(nextBreadcrumb);
      var nextStatus = parsed.querySelector(".wb-top-actions .wb-status-chip");
      var currentStatus = document.querySelector(".wb-top-actions .wb-status-chip");
      if (nextStatus && currentStatus) currentStatus.replaceWith(nextStatus);
      if (parsed.title) document.title = parsed.title;
      if (push) window.history.pushState({}, "", href);
      initWorkbench();
      window.requestAnimationFrame(function () {
        window.scrollTo(scrollX, scrollY);
        var nextTree = next.querySelector(".wb-tree");
        if (nextTree) {
          nextTree.scrollLeft = treeScrollLeft;
          nextTree.scrollTop = treeScrollTop;
        }
      });
    }).catch(function () { window.location.href = link.href; });
  }

  function initWorkbench() {
    var root = document.querySelector("[data-workbench-shell]");
    if (!root) return;
    initLayout(root);
    initContextTabs(root);
    initEditor(root);
    initStateTabs(root);
    initWorkflowWorkspaces();
    root.querySelectorAll("[data-workbench-navigation]").forEach(function (link) {
      link.addEventListener("click", function (event) {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
        event.preventDefault();
        loadWorkbench(link, true);
      });
    });
  }

  window.addEventListener("popstate", function () {
    var link = document.createElement("a");
    link.href = window.location.href;
    loadWorkbench(link, false);
  });

  document.querySelectorAll("[data-hydration-collect]").forEach(function (button) {
    button.addEventListener("click", function () {
      button.disabled = true;
      fetch(button.dataset.hydrationCollect, {
        method: "POST",
        headers: { "X-CSRF-Token": csrfToken() }
      })
        .then(function (response) {
          return response.json().then(function (body) {
            if (!response.ok) throw new Error((body.error && body.error.message) || "收集失败");
            return body;
          });
        })
        .then(function () { window.location.reload(); })
        .catch(function (error) {
          button.disabled = false;
          button.textContent = error.message || "收集失败";
        });
    });
  });
  initWorkbench();
}());
