(function () {
  "use strict";

  function csrfToken() {
    var meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.content : "";
  }

  function feedback(message, error) {
    var nodes = document.querySelectorAll("[data-library-feedback], [data-onboarding-feedback]");
    nodes.forEach(function (node) {
      node.textContent = message || "";
      node.classList.toggle("is-error", Boolean(error));
    });
  }

  function copyText(value) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(value);
    var area = document.createElement("textarea");
    area.value = value;
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    document.execCommand("copy");
    area.remove();
    return Promise.resolve();
  }

  function bindCopyPaths() {
    document.querySelectorAll("[data-copy-path]").forEach(function (button) {
      button.addEventListener("click", function () {
        copyText(button.dataset.copyPath || "").then(function () {
          feedback("书籍目录已复制。", false);
        }).catch(function () { feedback("无法复制，请在技术详情中手动复制路径。", true); });
      });
    });
  }

  function bindBookSelectors() {
    document.querySelectorAll("[data-book-selector]").forEach(function (selector) {
      var input = selector.querySelector("[data-book-search]");
      if (!input || input.dataset.catalogBound) return;
      input.dataset.catalogBound = "true";
      input.addEventListener("input", function () {
        var query = input.value.trim().toLocaleLowerCase();
        selector.querySelectorAll("[data-book-option]").forEach(function (option) {
          option.hidden = Boolean(query) && !option.textContent.toLocaleLowerCase().includes(query);
        });
        selector.querySelectorAll("[data-book-group]").forEach(function (group) {
          group.hidden = !group.querySelector("[data-book-option]:not([hidden])");
        });
      });
    });

    var shell = document.querySelector("[data-workbench-shell]");
    if (shell && shell.dataset.bookId && location.pathname.includes("/workbench")) {
      try { localStorage.setItem("novel-studio-recent:" + shell.dataset.bookId, location.href); } catch (error) { /* optional */ }
    }
    document.querySelectorAll("[data-book-switch]").forEach(function (link) {
      if (link.dataset.catalogBound) return;
      link.dataset.catalogBound = "true";
      link.addEventListener("click", function (event) {
        var targetBook = link.dataset.bookId;
        if (!targetBook) return;
        try {
          var recent = localStorage.getItem("novel-studio-recent:" + targetBook);
          if (!recent) return;
          var url = new URL(recent, location.origin);
          if (url.origin !== location.origin || !url.pathname.includes("/books/" + targetBook + "/")) return;
          event.preventDefault();
          location.href = url.href;
        } catch (error) { /* use normal href */ }
      });
    });
  }

  function bindPaneToggles() {
    if (!document.querySelector("[data-onboarding-card]")) return;
    var shell = document.querySelector("[data-workbench-shell]");
    if (!shell) return;
    document.querySelectorAll("[data-toggle-pane]").forEach(function (button) {
      button.addEventListener("click", function () {
        var side = button.dataset.togglePane;
        shell.classList.toggle("is-" + side + "-collapsed");
      });
    });
  }

  function setOnboardingActivityOpen(open) {
    var panel = document.querySelector("[data-onboarding-activity-center]");
    var scrim = document.querySelector("[data-onboarding-activity-close].wb-activity-scrim");
    var trigger = document.querySelector("[data-onboarding-activity-trigger]");
    if (!panel) return;
    panel.hidden = !open;
    if (scrim) scrim.hidden = !open;
    if (trigger) trigger.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function bindOnboardingActivityCenter() {
    var trigger = document.querySelector("[data-onboarding-activity-trigger]");
    if (trigger) trigger.addEventListener("click", function () {
      var panel = document.querySelector("[data-onboarding-activity-center]");
      setOnboardingActivityOpen(Boolean(panel && panel.hidden));
    });
    document.querySelectorAll("[data-onboarding-activity-close]").forEach(function (button) {
      button.addEventListener("click", function () { setOnboardingActivityOpen(false); });
    });
  }

  function postJson(url, payload) {
    return fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() },
      body: JSON.stringify(payload || {})
    }).then(function (response) {
      return response.json().then(function (body) {
        if (!response.ok) throw new Error((body.error && body.error.message) || "请求失败");
        return body;
      });
    });
  }

  function instructionErrorMessage(response) {
    return response.json().then(function (body) {
      var detail = body && body.error && body.error.message ? String(body.error.message) : "";
      return detail
        ? detail + "（HTTP " + response.status + "）"
        : "无法读取交接指令（HTTP " + response.status + "）";
    }).catch(function () {
      return "无法读取交接指令（HTTP " + response.status + "）";
    });
  }

  function bindInitializationActions() {
    function selectedDepth() {
      var selected = document.querySelector('input[name="initialization-depth"]:checked');
      return selected ? selected.value : "BALANCED";
    }
    function selectedGoal() {
      var selected = document.querySelector('input[name="author-goal"]:checked');
      return selected ? selected.value : "CONTINUE";
    }
    document.querySelectorAll("[data-initialize-candidate]").forEach(function (button) {
      button.addEventListener("click", function () {
        button.disabled = true;
        feedback("正在读取正文并建立章节…", false);
        postJson("/api/library/candidates/" + encodeURIComponent(button.dataset.candidateId) + "/initialize", { depth: selectedDepth(), author_goal: selectedGoal() })
          .then(function (body) {
            feedback("正文与章节已建立，初始化任务已准备好。", false);
            location.href = body.workbench_url;
          })
          .catch(function (error) { button.disabled = false; feedback(error.message, true); });
      });
    });
    document.querySelectorAll("[data-prepare-initialization]").forEach(function (button) {
      button.addEventListener("click", function () {
        button.disabled = true;
        feedback("正在准备初始化任务…", false);
        var url = "/api/books/" + encodeURIComponent(button.dataset.bookId) + "/editions/" + encodeURIComponent(button.dataset.editionId) + "/initialization";
        postJson(url, { depth: selectedDepth(), author_goal: selectedGoal() }).then(function () {
          feedback("初始化任务已准备好。", false);
          button.disabled = false;
          refreshCatalog(false);
        }).catch(function (error) { button.disabled = false; feedback(error.message, true); });
      });
    });
    document.querySelectorAll("[data-copy-handoff]").forEach(function (button) {
      button.addEventListener("click", function () {
        fetch(button.dataset.instructionUrl, { headers: { Accept: "application/json" } })
          .then(function (response) {
            if (!response.ok) {
              return instructionErrorMessage(response).then(function (message) {
                throw new Error(message);
              });
            }
            return response.json();
          })
          .then(function (body) { return copyText(body.instruction || ""); })
          .then(function () { feedback("给 Codex 的真实初始化指令已复制。", false); })
          .catch(function (error) { feedback(error.message, true); });
      });
    });
  }

  function bindAuthorGoalSelector() {
    var selector = document.querySelector("[data-author-goal-selector]");
    var plan = document.querySelector("[data-initialization-plan]");
    if (!selector || !plan) return;
    var configurations = {
      CONTINUE: { depth: "BALANCED", title: "为你推荐：均衡准备", items: ["全书结构索引", "全书连续性轻分析", "最近章节与当前活跃人物、物品、规则和伏笔优先深读", "每个故事阶段选择代表章节做文学分析"], effort: "预计任务量：较长；完成第一批分析后提供时间范围。" },
      UNDERSTAND: { depth: "QUICK", title: "为你推荐：快速了解", items: ["全书结构索引", "开篇基础与最近章节深读", "少量文学代表章节", "需要正式续写时再按相关性补齐历史"], effort: "预计任务量：较短。" },
      REWRITE: { depth: "BALANCED", title: "为你推荐：均衡准备 + 指定范围补齐", items: ["全书结构索引", "全书连续性轻分析", "进入工作台后选择改写章节", "只补齐目标章节、相邻章节与被后文引用的事实"], effort: "预计任务量：取决于改写范围。" },
      AUDIT: { depth: "FULL", title: "为你推荐：完整全书审查", items: ["全书结构与连续性索引", "每一章文学深分析", "全局综合、指标与图谱", "完整历史状态与严格验收"], effort: "预计任务量：很长；完成第一批分析后提供时间范围。" }
    };
    function render() {
      var goal = selector.querySelector('input[name="author-goal"]:checked')?.value || "CONTINUE";
      var config = configurations[goal];
      var depth = document.querySelector('input[name="initialization-depth"][value="' + config.depth + '"]');
      if (depth) depth.checked = true;
      plan.querySelector("[data-plan-title]").textContent = config.title;
      plan.querySelector("[data-plan-items]").innerHTML = config.items.map(function (item) { return "<li>" + item + "</li>"; }).join("");
      plan.querySelector("[data-plan-effort]").textContent = config.effort;
    }
    selector.addEventListener("change", render);
    render();
  }

  function bindImportDialog() {
    var dialog = document.querySelector("[data-import-dialog]");
    if (!dialog) return;
    document.querySelectorAll("[data-open-import]").forEach(function (button) {
      button.addEventListener("click", function () { dialog.showModal(); });
    });
    dialog.querySelectorAll("[data-close-import]").forEach(function (button) {
      button.addEventListener("click", function () { dialog.close(); });
    });
    var form = dialog.querySelector("[data-import-form]");
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var status = form.querySelector("[data-import-feedback]");
      status.textContent = "正在安全复制正文…";
      fetch("/api/library/upload", {
        method: "POST",
        headers: { "X-CSRF-Token": csrfToken() },
        body: new FormData(form)
      }).then(function (response) {
        return response.json().then(function (body) {
          if (!response.ok) throw new Error((body.error && body.error.message) || body.detail || "导入失败");
          return body;
        });
      }).then(function (body) {
        status.textContent = body.message;
        form.reset();
        window.setTimeout(function () { dialog.close(); refreshCatalog(true); }, 500);
      }).catch(function (error) { status.textContent = error.message; status.classList.add("is-error"); });
    });
  }

  function bindClassification() {
    document.querySelectorAll("[data-save-classification]").forEach(function (button) {
      button.addEventListener("click", function () {
        var card = button.closest("[data-unclassified-book]");
        var kind = card.querySelector("[data-book-kind]").value;
        postJson("/api/library/" + encodeURIComponent(card.dataset.unclassifiedBook) + "/classify", { book_kind: kind })
          .then(function () { card.remove(); })
          .catch(function (error) { button.textContent = error.message; });
      });
    });
  }

  function showReady(entry) {
    var card = document.querySelector("[data-onboarding-card]");
    if (!card) return;
    card.dataset.state = "READY";
    var mark = card.querySelector("[data-onboarding-mark]");
    var headline = card.querySelector("[data-onboarding-headline]");
    var summary = card.querySelector("[data-onboarding-summary]");
    var actions = card.querySelector("[data-onboarding-actions]");
    if (mark) mark.textContent = "✓";
    if (headline) headline.textContent = entry.readiness_label || "当前创作能力已经开放";
    if (summary) summary.textContent = entry.author_summary || "这本书已经可以进入小说工作台。";
    document.querySelectorAll("[data-onboarding-status-label], [data-onboarding-left-status]").forEach(function (node) { node.textContent = "可创作"; });
    document.querySelectorAll("[data-current-book-state-label], [data-current-book-option-state-label]").forEach(function (node) { node.textContent = "可创作"; });
    var selectorDot = document.querySelector("[data-current-book-state-dot]");
    if (selectorDot) selectorDot.className = "wb-book-state-dot wb-book-state-ready";
    var activityCount = document.querySelector("[data-onboarding-activity-count]");
    var activityStatus = document.querySelector("[data-onboarding-activity-status]");
    var activityGroup = document.querySelector("[data-onboarding-activity-group]");
    var activitySummary = document.querySelector("[data-onboarding-activity-summary]");
    if (activityCount) activityCount.textContent = "0";
    if (activityStatus) activityStatus.textContent = "已完成";
    if (activityGroup) activityGroup.textContent = "已完成";
    if (activitySummary) activitySummary.textContent = entry.author_summary || "当前可用能力已经开放，其余分析可继续在后台完成。";
    if (actions) actions.innerHTML = '<a class="button primary" href="' + entry.href + '">进入小说工作台</a><a class="button" href="/library">返回书库</a>';
    var missing = document.querySelector("[data-onboarding-missing]");
    if (missing) missing.remove();
  }

  function currentEntry(payload, root) {
    var id = root.dataset.currentCatalogId;
    return (payload.entries || []).find(function (entry) { return entry.catalog_id === id || (root.dataset.bookId && entry.book_id === root.dataset.bookId); });
  }

  function refreshCatalog(manual) {
    var root = document.querySelector("[data-library-catalog]");
    if (!root) return Promise.resolve();
    var request = manual ? postJson("/api/library/discovery/refresh") : fetch("/api/library/catalog", { headers: { Accept: "application/json" } }).then(function (response) { if (!response.ok) throw new Error("刷新书籍失败"); return response.json(); });
    return request.then(function (payload) {
      if (manual) feedback("书籍列表已刷新。", false);
      if (payload.revision === root.dataset.catalogRevision) return;
      var entry = currentEntry(payload, root);
      if (entry && entry.studio_accessible && document.querySelector("[data-onboarding-card]")) {
        root.dataset.catalogRevision = payload.revision;
        if (entry.studio_ready) showReady(entry);
        else window.location.assign(entry.href);
        return;
      }
      root.dataset.catalogRevision = payload.revision;
      if (entry && document.querySelector("[data-onboarding-card]")) {
        document.querySelectorAll("[data-onboarding-status-label], [data-onboarding-left-status]").forEach(function (node) { node.textContent = entry.state_label; });
        var summary = document.querySelector("[data-onboarding-summary]");
        if (summary) summary.textContent = entry.author_summary;
        return;
      }
      if (location.pathname.includes("/workbench") || window.__novelDraftDirty || document.hidden) {
        document.dispatchEvent(new CustomEvent("novel:catalog-updated", { detail: payload }));
        return;
      }
      if (location.pathname === "/library" || location.pathname === "/library/technical") {
        fetch(location.href, { headers: { Accept: "text/html" } }).then(function (response) { return response.text(); }).then(function (html) {
          var next = new DOMParser().parseFromString(html, "text/html").querySelector("[data-library-groups]");
          var current = document.querySelector("[data-library-groups]");
          if (next && current) current.replaceWith(next);
        });
      }
    }).catch(function (error) { if (manual) feedback(error.message, true); });
  }

  function bindRefresh() {
    document.querySelectorAll("[data-refresh-library]").forEach(function (button) {
      button.addEventListener("click", function () { refreshCatalog(true); });
    });
    document.querySelectorAll('[data-wb-editor][data-editor-mode="draft"]').forEach(function (editor) {
      editor.addEventListener("input", function () { window.__novelDraftDirty = true; });
    });
    if (document.querySelector("[data-library-catalog]")) {
      window.setInterval(function () { if (!document.hidden) refreshCatalog(false); }, 10000);
    }
  }

  bindCopyPaths();
  bindBookSelectors();
  bindPaneToggles();
  bindOnboardingActivityCenter();
  bindAuthorGoalSelector();
  bindInitializationActions();
  bindImportDialog();
  bindClassification();
  bindRefresh();
  window.NovelLibraryCatalogInit = bindBookSelectors;
})();
