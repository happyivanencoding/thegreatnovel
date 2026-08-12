(() => {
  "use strict";

  const csrf = document.querySelector('meta[name="csrf-token"]')?.content || "";
  const feedback = document.querySelector("[data-original-feedback]");
  const bookId = document.body.dataset.originalBookId || "";
  const lines = (value) => String(value || "").split(/\r?\n/).map((item) => item.trim()).filter(Boolean);

  const show = (message, failed = false) => {
    if (!feedback) return;
    feedback.textContent = message;
    feedback.classList.toggle("is-error", failed);
  };

  const responseError = (value) => value?.error?.message || value?.detail?.message || value?.detail || "操作失败";
  const pollGeneration = () => {
    if (!document.body.dataset.originalGenerating) return;
    let checking = false;
    const check = async () => {
      if (checking) return;
      checking = true;
      try {
        const response = await fetch(window.location.href, {
          headers: {Accept: "text/html", "X-Requested-With": "original-status-poll"},
          cache: "no-store",
        });
        if (!response.ok) return;
        const html = await response.text();
        if (!html.includes("data-original-generating=\"true\"")) {
          window.location.reload();
        }
      } catch (_) {
        // A transient network failure should not turn a status poll into an
        // error banner; the next poll will retry.
      } finally {
        checking = false;
      }
    };
    const timer = window.setInterval(check, 4000);
    window.addEventListener("beforeunload", () => window.clearInterval(timer), {once: true});
  };
  const copyText = async (value) => {
    if (!value) throw new Error("AI 任务中没有可复制的指令");
    const area = document.createElement("textarea");
    area.value = value;
    area.style.position = "fixed";
    area.style.left = "-9999px";
    area.style.top = "0";
    area.setAttribute("readonly", "");
    document.body.appendChild(area);
    area.focus();
    area.select();
    area.setSelectionRange(0, area.value.length);
    const copied = document.execCommand("copy");
    area.remove();
    if (copied) return;
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(value);
    throw new Error("浏览器未允许复制，请重试");
  };
  const post = async (url, payload) => {
    const response = await fetch(url, {
      method: "POST",
      headers: {"Content-Type": "application/json", "X-CSRF-Token": csrf},
      body: JSON.stringify(payload),
    });
    const value = await response.json();
    if (!response.ok || value.error) throw new Error(responseError(value));
    return value;
  };

  document.querySelectorAll("[data-copy-instruction]").forEach((button) => {
    button.addEventListener("click", async () => {
      const label = button.textContent;
      button.disabled = true;
      try {
        const response = await fetch(button.dataset.copyInstruction, {headers: {Accept: "application/json"}});
        const value = await response.json();
        if (!response.ok || value.error) throw new Error(responseError(value));
        await copyText(value.instruction || "");
        button.textContent = "已复制";
        show("给 Codex 的指令已复制。请回到 Codex 桌面端粘贴处理。", false);
      } catch (error) {
        button.textContent = "复制失败";
        show(error.message, true);
      } finally {
        window.setTimeout(() => { button.textContent = label; button.disabled = false; }, 1500);
      }
    });
  });

  document.querySelector("[data-original-create]")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    show("正在创建原创项目并理解核心阅读体验…");
    try {
      const value = await post("/api/library/original", {
        premise: String(form.get("premise") || "").trim(),
        genre: String(form.get("genre") || "").trim(),
        tone_style: String(form.get("tone_style") || "").trim(),
        pov: String(form.get("pov") || "").trim(),
        expected_length: String(form.get("expected_length") || "").trim(),
        must_include: lines(form.get("must_include")),
        forbidden: lines(form.get("forbidden")),
        reference_traits: lines(form.get("reference_traits")),
      });
      window.location.assign(value.original_url);
    } catch (error) { show(error.message, true); }
  });

  const wizard = document.querySelector("[data-original-confirm]");
  const readerControls = (() => {
    const root = document.querySelector("[data-reader-experience-controls]");
    if (!root) return null;
    const presets = {
      PAYOFF_STRONGER: {POWER_VERIFICATION: "CORE", COMBAT: "CORE", BREAKTHROUGH: "STRONG"},
      MYSTERY_STRONGER: {MYSTERY: "CORE", REVEAL: "CORE", WORLD_EXPANSION: "STRONG"},
      TEAM_STRONGER: {TEAM_GROWTH: "CORE", RELATIONSHIP: "STRONG", FACTION_CONFLICT: "STRONG"},
      RELATIONSHIP_STRONGER: {RELATIONSHIP: "CORE", ROMANCE: "CORE", TEAM_GROWTH: "STRONG"},
      CAREER_STRONGER: {STATUS_RISE: "CORE", PROGRESSION: "STRONG", RESOURCE_OPPORTUNITY: "STRONG"},
    };
    const select = (row, value) => {
      const option = row.querySelector(`[data-reader-strength="${value}"]`);
      if (!option) return;
      row.querySelectorAll("[data-reader-strength]").forEach((item) => {
        const selected = item === option;
        item.classList.toggle("is-selected", selected);
        item.setAttribute("aria-pressed", selected ? "true" : "false");
      });
      const label = row.querySelector("[data-reader-strength-label]");
      if (label) label.textContent = option.textContent;
    };
    root.querySelectorAll("[data-reader-experience-item]").forEach((row) => {
      row.querySelectorAll("[data-reader-strength]").forEach((option) => {
        option.addEventListener("click", () => select(row, option.dataset.readerStrength));
      });
    });
    return {
      applyPreset(name) {
        Object.entries(presets[name] || {}).forEach(([key, value]) => {
          const row = root.querySelector(`[data-reader-experience-key="${key}"]`);
          if (row) select(row, value);
        });
      },
      collect() {
        return Object.fromEntries(
          [...root.querySelectorAll("[data-reader-experience-item]")].map((row) => [
            row.dataset.readerExperienceKey,
            row.querySelector("[data-reader-strength].is-selected")?.dataset.readerStrength || "NORMAL",
          ]),
        );
      },
    };
  })();
  pollGeneration();
  document.querySelector("[data-core-innovation-select]")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const selected = String(form.get("selected_primary_innovation_id") || "").trim();
    if (!selected) { show("请选择一个 Primary Innovation。", true); return; }
    show("正在冻结 Core Innovation Intent，并准备 Story Foundation Proposal…");
    try {
      await post(`/api/books/${bookId}/original/core-innovation/select`, {
        selected_primary_innovation_id: selected,
        optional_mix_notes: String(form.get("optional_mix_notes") || "").trim(),
      });
      window.location.replace(window.location.href);
    } catch (error) { show(error.message, true); }
  });
  if (wizard) {
    let step = 2;
    const renderStep = () => {
      wizard.querySelectorAll("[data-wizard-step]").forEach((panel) => { panel.hidden = Number(panel.dataset.wizardStep) !== step; });
      wizard.querySelectorAll("[data-wizard-indicator]").forEach((item) => { item.classList.toggle("is-active", Number(item.dataset.wizardIndicator) === step); item.classList.toggle("is-done", Number(item.dataset.wizardIndicator) < step); });
      wizard.querySelector("[data-wizard-back]").hidden = step === 2;
      wizard.querySelector("[data-wizard-next]").hidden = step === 5;
      wizard.querySelector("[data-wizard-submit]").hidden = step !== 5;
      if (step === 5) {
        const form = new FormData(wizard);
        const choice = wizard.querySelector('[name="selected_foundation_id"]:checked')?.closest("label");
        wizard.querySelector("[data-preview-foundation]").textContent = choice?.querySelector("span")?.textContent || "";
        wizard.querySelector("[data-preview-protagonist]").textContent = `${form.get("protagonist_override")}：${form.get("protagonist_goal_override")}`;
        wizard.querySelector("[data-preview-world]").textContent = lines(form.get("world_rules")).slice(0, 3).join("；");
        wizard.querySelector("[data-preview-phase]").textContent = String(form.get("first_phase_objective") || "");
      }
    };
      wizard.querySelector("[data-wizard-next]").addEventListener("click", () => { step = Math.min(5, step + 1); renderStep(); wizard.scrollIntoView({behavior: "smooth", block: "start"}); });
      wizard.querySelector("[data-wizard-back]").addEventListener("click", () => { step = Math.max(2, step - 1); renderStep(); wizard.scrollIntoView({behavior: "smooth", block: "start"}); });
    renderStep();

    wizard.addEventListener("submit", async (event) => {
      event.preventDefault();
      const form = new FormData(wizard);
      const selectedFoundation = String(form.get("selected_foundation_id") || "");
      const title = String(form.get("title_override") || form.get("selected_title") || "").trim();
      if (!window.confirm(`确认《${title}》的故事基础并开始准备第一章？\n\n这会写入作者幕后设定、全书画像和剧情方向，但不会创建或批准正式正文。`)) return;
      const settingStrengths = {};
      const openQuestionActions = {};
      const hiddenTruthActions = {};
      const firstPhaseOverrides = {};
      for (const [key, value] of form.entries()) {
        if (key.startsWith("setting_strength__")) settingStrengths[key.slice(18)] = String(value);
        if (key.startsWith("open_question_action__")) {
          const index = key.slice(22);
          openQuestionActions[`question-${wizard.dataset.proposalVersionId}-${selectedFoundation}-${index}`] = String(value);
        }
        if (key.startsWith("hidden_truth_action__")) hiddenTruthActions[key.slice(21)] = String(value);
        if (key.startsWith("first_phase__")) firstPhaseOverrides[key.slice(13)] = String(value).trim();
      }
      show("正在以单一事务确认故事基础…");
      try {
        await post(`/api/books/${bookId}/original/foundation/confirm`, {
          confirmed: true,
          selected_title: String(form.get("selected_title") || ""),
          title_override: String(form.get("title_override") || "").trim(),
          selected_foundation_id: selectedFoundation,
          selected_route_id: String(form.get("selected_route_id") || ""),
          protagonist_override: String(form.get("protagonist_override") || "").trim(),
          protagonist_goal_override: String(form.get("protagonist_goal_override") || "").trim(),
          main_conflict_override: String(form.get("main_conflict_override") || "").trim(),
          protagonist_cost_override: String(form.get("protagonist_cost_override") || "").trim(),
          protagonist_growth_override: String(form.get("protagonist_growth_override") || "").trim(),
          first_phase_overrides: firstPhaseOverrides,
          characters_override: lines(form.get("characters_override")),
          factions_override: lines(form.get("factions_override")),
          world_rules: lines(form.get("world_rules")),
          first_phase_objective: String(form.get("first_phase_objective") || "").trim(),
          rolling_short_override: lines(form.get("rolling_short_override")),
          rolling_mid_override: lines(form.get("rolling_mid_override")),
          rolling_long_override: lines(form.get("rolling_long_override")),
          setting_strength_overrides: settingStrengths,
          open_question_actions: openQuestionActions,
          hidden_truth_actions: hiddenTruthActions,
          confirm_kernel_contracts: String(form.get("confirm_kernel_contracts") || "") === "true",
        });
        window.location.replace(window.location.href);
      } catch (error) { show(error.message, true); }
    });
  }

  const renderComparison = (value) => {
    const target = document.querySelector("[data-original-compare]");
    if (!target) return;
    const column = (label, proposal) => `<article><h3>${label}</h3><p><strong>${proposal.expanded_premise}</strong></p>${proposal.foundation_candidates.map((item) => `<div><b>${item.title}</b><span>${item.core_reading_promise}</span><small>${item.main_conflict}</small></div>`).join("")}</article>`;
    target.innerHTML = column("当前方案", value.current) + column("新方案", value.target);
    target.hidden = false;
    target.scrollIntoView({behavior: "smooth", block: "center"});
  };

  document.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-original-action]");
    if (!button) return;
    const action = button.dataset.originalAction;
    button.disabled = true;
    try {
      if (action === "confirm-reader") {
        show("正在确认阅读体验并准备共享 Contract 的三个故事方向…");
        await post(`/api/books/${bookId}/original/reader-experience/confirm`, {
          adjustment: "CONFIRM",
          priority_overrides: readerControls?.collect() || {},
        });
        window.location.replace(window.location.href);
      } else if (action === "reader-preset") {
        readerControls?.applyPreset(button.dataset.readerPreset || "");
        show("快捷组合已应用；你仍可以逐项调整后再确认。", false);
        button.disabled = false;
      } else if (action === "prepare-core") {
        show("正在检查 Core Innovation Proposal…");
        await post(`/api/books/${bookId}/original/core-innovation/prepare`, {});
        window.location.replace(window.location.href);
      } else if (action === "bootstrap") {
        show("正在准备新的故事方案；当前方案会保留…");
        const value = await post(`/api/books/${bookId}/original/bootstrap`, {});
        const message = value.proposal_imported
          ? "方案已完成并读取，正在刷新页面…"
          : value.deduplicated
            ? "新方案已经在生成，已恢复原 AI 任务。"
            : "新方案任务已准备好，只需复制一次指令给 Codex。";
        show(message);
        setTimeout(() => window.location.replace(window.location.href), 500);
      } else if (action === "import") {
        show("正在读取完成的故事方案…");
        await post(`/api/books/${bookId}/original/proposal/import`, {handoff_id: button.dataset.handoffId});
        window.location.replace(window.location.href);
      } else if (action === "compare-proposal") {
        const response = await fetch(`/api/books/${bookId}/original/proposals/${button.dataset.proposalVersionId}/compare`);
        const value = await response.json();
        if (!response.ok || value.error) throw new Error(responseError(value));
        renderComparison(value);
        button.disabled = false;
      } else if (action === "replace-proposal") {
        if (!window.confirm("用新方案替换当前待确认方案？已经确认的作者设定和正式正文不会改变。")) { button.disabled = false; return; }
        await post(`/api/books/${bookId}/original/proposals/${button.dataset.proposalVersionId}/resolve`, {action: "REPLACE_CURRENT"});
        window.location.replace(window.location.href);
      } else if (action === "keep-proposal") {
        await post(`/api/books/${bookId}/original/proposals/${button.dataset.proposalVersionId}/resolve`, {action: "KEEP_CURRENT"});
        window.location.replace(window.location.href);
      } else if (action === "select") {
        show("正在冻结第一章要求并准备 AI 任务…");
        await post(`/api/books/${bookId}/original/first-chapter/select`, {candidate_id: button.dataset.candidateId});
        window.location.replace(window.location.href);
      } else if (action === "validate") {
        show("正在运行十项校验…");
        await post(`/api/books/${bookId}/original/first-chapter/validate`, {draft_id: button.dataset.draftId, confirmation: ""});
        window.location.replace(window.location.href);
      } else if (action === "approve") {
        if (!window.confirm("批准后，第一章草稿将写入正式正文，并成为后续创作的权威边界。是否继续？")) { button.disabled = false; return; }
        show("正在写入正式正文…");
        await post(`/api/books/${bookId}/original/first-chapter/approve`, {draft_id: button.dataset.draftId, confirmation: "批准写入正史"});
        window.location.replace(window.location.href);
      }
    } catch (error) {
      show(error.message, true);
      button.disabled = false;
    }
  });
})();
