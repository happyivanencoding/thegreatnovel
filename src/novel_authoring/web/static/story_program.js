(function () {
  "use strict";

  const body = document.body;
  const csrf = document.querySelector('meta[name="csrf-token"]')?.content || "";
  const bookId = body.dataset.storyProgramBookId || "";

  function feedback(message, isError) {
    document.querySelectorAll("[data-story-program-feedback]").forEach((node) => {
      node.textContent = message || "";
      node.classList.toggle("is-error", Boolean(isError));
    });
  }

  async function api(path, payload) {
    const response = await fetch(path, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": csrf,
      },
      body: JSON.stringify(payload || {}),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data?.error?.message || data?.detail || `请求失败（${response.status}）`);
    }
    return data;
  }

  const createForm = document.querySelector("[data-story-program-create]");
  if (createForm) {
    createForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const form = new FormData(createForm);
      const payload = Object.fromEntries(form.entries());
      try {
        const result = await api("/api/story-program/books", payload);
        window.location.href = result.redirect_url;
      } catch (error) {
        feedback(error.message, true);
      }
    });
    return;
  }

  const app = document.querySelector("[data-story-program]");
  if (!app || !bookId) return;

  const output = document.querySelector("[data-prompt-output]");
  const mode = document.querySelector("[data-prompt-mode]");
  const board = document.querySelector("[data-board-markdown]");
  const proposalRaw = document.querySelector("[data-proposal-raw]");
  const proposalSections = document.querySelector("[data-proposal-sections]");
  const provisionalEnabled = body.dataset.storyProgramProvisional === "true";

  const visibleByMode = {
    new_book: ["title", "premise", "genre", "reader_experience", "forbidden_style", "reference_profile", "include_reference_profile", "reference_reason"],
    next_batch: ["completed_summaries", "current_block", "current_module", "current_state", "debts", "reference_reason"],
    current_chapter: ["core_promise", "world_rules", "decision_mode", "chapter_plan", "recent_summaries", "current_state", "debts", "hard_facts", "reference_reason"],
    review: ["original_ten_plan", "ten_chapter_plan", "actual_summaries", "current_state", "debts", "reference_reason"],
  };

  function syncInputs() {
    const visible = new Set(visibleByMode[mode.value] || visibleByMode.new_book);
    document.querySelectorAll("[data-prompt-input]").forEach((label) => {
      label.hidden = !visible.has(label.dataset.promptInput);
    });
  }

  function collectPromptPayload() {
    const payload = {
      mode: mode.value,
      board_markdown: board.value,
      program_ids: Array.from(document.querySelectorAll("[data-program-checkbox]:checked"))
        .map((node) => node.value),
      allow_provisional: provisionalEnabled,
    };
    document.querySelectorAll("[data-prompt-field]").forEach((field) => {
      if (field.type === "checkbox") payload[field.dataset.promptField] = field.checked;
      else payload[field.dataset.promptField] = field.value;
    });
    return payload;
  }

  function showGate(result) {
    const gate = document.querySelector("[data-concrete-gate]");
    if (!gate) return;
    if (!result.gate) {
      gate.textContent = "当前模式不需要 Concrete Plan Gate。";
      gate.className = "story-program-gate is-soft";
      return;
    }
    if (result.gate.passed) {
      gate.textContent = "Concrete Plan Gate：通过，可以生成当前章节 Prompt。";
      gate.className = "story-program-gate is-passed";
    } else {
      gate.textContent = `Concrete Plan Gate：未通过。缺少：${result.gate.missing.join("、")}。`;
      gate.className = "story-program-gate is-blocked";
    }
  }

  function showWarnings(result) {
    const node = document.querySelector("[data-soft-warnings]");
    if (!node) return;
    node.textContent = (result.soft_warnings || []).join("\n");
  }

  async function generatePrompt(forceMode) {
    if (forceMode) {
      mode.value = forceMode;
      syncInputs();
    }
    try {
      const result = await api(`/api/books/${encodeURIComponent(bookId)}/story-program/prompt`, collectPromptPayload());
      showGate(result);
      showWarnings(result);
      if (result.prompt) {
        output.value = result.prompt;
        feedback("完整 Prompt 已生成。页面显示的文本就是复制内容。", false);
      } else {
        output.value = "";
        feedback("Concrete Plan Gate 未通过，未生成 Writer Prompt。请补齐页面列出的字段。", true);
      }
      output.dispatchEvent(new Event("input"));
      return result;
    } catch (error) {
      feedback(error.message, true);
      return null;
    }
  }

  mode.addEventListener("change", syncInputs);
  syncInputs();
  document.querySelector("[data-generate-prompt]")?.addEventListener("click", () => generatePrompt());
  document.querySelector("[data-generate-chapter-prompt]")?.addEventListener("click", () => generatePrompt("current_chapter"));

  document.querySelector("[data-copy-prompt]")?.addEventListener("click", async () => {
    if (!output.value) {
      feedback("当前没有可复制的 Prompt。", true);
      return;
    }
    try {
      await navigator.clipboard.writeText(output.value);
      feedback("已复制。剪贴板内容与页面 Prompt 文本完全一致。", false);
    } catch (error) {
      output.focus();
      output.select();
      feedback("浏览器未授权自动复制，已选中页面中的完整 Prompt，请手动复制。", true);
    }
  });

  document.querySelector("[data-save-board]")?.addEventListener("click", async () => {
    try {
      await api(`/api/books/${encodeURIComponent(bookId)}/story-program/board`, { markdown: board.value });
      feedback("Book Board 已按作者明确操作保存。", false);
    } catch (error) {
      feedback(error.message, true);
    }
  });

  function renderProposal(data) {
    const proposal = data.proposal || {};
    const errorNode = document.querySelector("[data-proposal-error]");
    if (errorNode) errorNode.textContent = proposal.parse_error || "已解析可采用区块。";
    const preview = document.querySelector("[data-proposal-raw-preview]");
    if (preview) preview.textContent = proposal.raw || "";
    proposalSections.textContent = "";
    (proposal.sections || []).filter((item) => item.adoptable).forEach((item) => {
      const label = document.createElement("label");
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = true;
      checkbox.dataset.proposalSection = "";
      checkbox.value = item.key;
      const title = document.createElement("strong");
      title.textContent = item.title;
      const body = document.createElement("pre");
      body.textContent = item.body;
      label.append(checkbox, title, body);
      proposalSections.append(label);
    });
  }

  document.querySelector("[data-import-proposal]")?.addEventListener("click", async () => {
    try {
      const data = await api(`/api/books/${encodeURIComponent(bookId)}/story-program/proposal`, { raw: proposalRaw.value });
      renderProposal(data);
      feedback(data.board_unchanged ? "Proposal 已导入；Book Board 未改变。" : "Proposal 已导入。", false);
    } catch (error) {
      feedback(error.message, true);
    }
  });

  async function adoptSelected(all) {
    const sections = all
      ? Array.from(document.querySelectorAll("[data-proposal-section]"), (node) => node.value)
      : Array.from(document.querySelectorAll("[data-proposal-section]:checked"), (node) => node.value);
    try {
      const data = await api(`/api/books/${encodeURIComponent(bookId)}/story-program/proposal/adopt`, {
        sections,
        board_markdown: board.value,
      });
      board.value = data.board_markdown;
      feedback(`已明确采用 ${sections.length} 个 Proposal 区块；其他区块未进入 Book Board。`, false);
    } catch (error) {
      feedback(error.message, true);
    }
  }

  document.querySelector("[data-adopt-selected]")?.addEventListener("click", () => adoptSelected(false));
  document.querySelector("[data-adopt-all]")?.addEventListener("click", () => adoptSelected(true));
  document.querySelector("[data-reject-proposal]")?.addEventListener("click", () => {
    proposalRaw.value = "";
    proposalSections.textContent = "Proposal 已拒绝；正式 Book Board 没有改变。"
    feedback("Proposal 已从当前审核界面移除；正式 Book Board 没有改变。", false);
  });

  document.querySelector("[data-reference-query]")?.addEventListener("input", (event) => {
    const needle = event.target.value.trim().toLowerCase();
    document.querySelectorAll("[data-reference-card]").forEach((card) => {
      card.hidden = needle && !card.textContent.toLowerCase().includes(needle);
    });
  });

  document.querySelector("[data-save-chapter]")?.addEventListener("click", async () => {
    const number = Number(document.querySelector("[data-chapter-number]").value);
    const title = document.querySelector("[data-chapter-title]").value;
    const markdown = document.querySelector("[data-chapter-markdown]").value;
    const commit = document.querySelector("[data-chapter-commit]").value;
    try {
      const data = await api(`/api/books/${encodeURIComponent(bookId)}/story-program/chapter`, {
        chapter_number: number,
        title,
        chapter_markdown: markdown,
        chapter_commit: commit,
      });
      document.querySelector("[data-chapter-result]").textContent = `已批准并保存 ${data.path}。Canon/旧 Edition 未被自动修改。`;
      window.setTimeout(() => window.location.reload(), 350);
    } catch (error) {
      document.querySelector("[data-chapter-result]").textContent = error.message;
    }
  });
})();
