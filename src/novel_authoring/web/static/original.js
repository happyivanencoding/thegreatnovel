(() => {
  const csrf = document.querySelector('meta[name="csrf-token"]')?.content || "";
  const feedback = document.querySelector("[data-original-feedback]");
  const bookId = document.body.dataset.originalBookId || "";

  const lines = (value) => String(value || "").split(/\r?\n/).map((item) => item.trim()).filter(Boolean);
  const show = (message, failed = false) => {
    if (!feedback) return;
    feedback.textContent = message;
    feedback.classList.toggle("is-error", failed);
  };
  const post = async (url, payload) => {
    const response = await fetch(url, {
      method: "POST",
      headers: {"Content-Type": "application/json", "X-CSRF-Token": csrf},
      body: JSON.stringify(payload),
    });
    const value = await response.json();
    if (!response.ok || value.error) {
      throw new Error(value.error?.message || value.error?.detail || "操作失败");
    }
    return value;
  };

  document.querySelector("[data-original-create]")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    show("正在创建原创项目并准备本地 handoff…");
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

  document.querySelector("[data-original-confirm]")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    show("正在确认基础框架；这一步不会创建章节或 Canon…");
    try {
      await post(`/api/books/${bookId}/original/foundation/confirm`, {
        confirmation: String(form.get("confirmation") || ""),
        selected_title: String(form.get("selected_title") || ""),
        title_override: String(form.get("title_override") || "").trim(),
        selected_foundation_id: String(form.get("selected_foundation_id") || ""),
        selected_route_id: String(form.get("selected_route_id") || ""),
        protagonist_override: String(form.get("protagonist_override") || "").trim(),
        protagonist_goal_override: String(form.get("protagonist_goal_override") || "").trim(),
        main_conflict_override: String(form.get("main_conflict_override") || "").trim(),
        protagonist_cost_override: String(form.get("protagonist_cost_override") || "").trim(),
        protagonist_growth_override: String(form.get("protagonist_growth_override") || "").trim(),
        characters_override: lines(form.get("characters_override")),
        factions_override: lines(form.get("factions_override")),
        world_rules: lines(form.get("world_rules")),
        first_phase_objective: String(form.get("first_phase_objective") || "").trim(),
        rolling_short_override: lines(form.get("rolling_short_override")),
        rolling_mid_override: lines(form.get("rolling_mid_override")),
        rolling_long_override: lines(form.get("rolling_long_override")),
      });
      window.location.reload();
    } catch (error) { show(error.message, true); }
  });

  document.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-original-action]");
    if (!button) return;
    button.disabled = true;
    const action = button.dataset.originalAction;
    try {
      if (action === "bootstrap") {
        show("正在准备新的 Proposal handoff…");
        await post(`/api/books/${bookId}/original/bootstrap`, {});
      } else if (action === "import") {
        show("正在校验并导入 Proposal…");
        await post(`/api/books/${bookId}/original/proposal/import`, {handoff_id: button.dataset.handoffId});
      } else if (action === "select") {
        show("正在建立首章 Chapter Contract 与本地 Draft handoff…");
        await post(`/api/books/${bookId}/original/first-chapter/select`, {candidate_id: button.dataset.candidateId});
      } else if (action === "validate") {
        show("正在运行十项校验…");
        await post(`/api/books/${bookId}/original/first-chapter/validate`, {draft_id: button.dataset.draftId, confirmation: ""});
      } else if (action === "approve") {
        const confirmation = document.querySelector("[data-approval-confirmation]")?.value || "";
        show("正在执行作者显式批准…");
        await post(`/api/books/${bookId}/original/first-chapter/approve`, {draft_id: button.dataset.draftId, confirmation});
      }
      window.location.reload();
    } catch (error) {
      show(error.message, true);
      button.disabled = false;
    }
  });
})();
