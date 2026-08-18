const state = {
  bookId: "",
  references: [],
  proposalDraftActive: false,
};

const sectionTitles = {
  core: "# 小说核心与读者承诺",
  values_world: "# 价值观与世界观",
  protagonist: "# 主角、能力与关键关系",
  long_plan: "# 未来100章大型剧情块",
  small_plan: "# 未来十章逐章小纲",
  status: "# 当前状态、未兑现承诺与作者备注",
};

const $ = (id) => document.getElementById(id);

function showStatus(message, isError = false) {
  const target = $("status");
  target.textContent = message;
  target.classList.toggle("error", isError);
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = payload.detail;
    const error = new Error(typeof detail === "string" ? detail : detail?.message || "请求失败");
    error.payload = payload;
    throw error;
  }
  return payload;
}

function composeBookContent() {
  return Object.entries(sectionTitles)
    .map(([key, title]) => `${title}\n\n${$(`section-${key}`).value.trim()}`)
    .join("\n\n") + "\n";
}

function populateBook(book) {
  state.bookId = book.book_id;
  $("book-id").value = book.book_id;
  for (const key of Object.keys(sectionTitles)) {
    $(`section-${key}`).value = book.sections?.[key] || "";
  }
  const templates = book.prompt_templates || {};
  $("template-outline").value = templates.outline || "";
  $("template-chapter").value = templates.chapter || "";
  $("template-review").value = templates.review || "";
  $("proposal-editor").value = book.proposal || "";
  $("codex-response").value = "";
  state.proposalDraftActive = Boolean(book.proposal);
  showStatus(`已加载 ${book.book_id}`);
}

async function refreshBookList() {
  const payload = await requestJson("/api/books");
  const select = $("book-select");
  select.innerHTML = `<option value="">（暂无）</option>`;
  for (const bookId of payload.books) {
    const option = document.createElement("option");
    option.value = bookId;
    option.textContent = bookId;
    select.appendChild(option);
  }
}

async function loadBook(bookId) {
  if (!bookId) {
    showStatus("请先输入或选择小说 ID", true);
    return;
  }
  try {
    populateBook(await requestJson(`/api/books/${encodeURIComponent(bookId)}`));
  } catch (error) {
    showStatus(error.message, true);
  }
}

function referenceValue(value) {
  if (Array.isArray(value)) return value.join("；");
  return value || "（未填写）";
}

function addReferenceField(card, label, value) {
  const line = document.createElement("div");
  line.className = "reference-field";
  const name = document.createElement("strong");
  name.textContent = label;
  const content = document.createElement("span");
  content.textContent = referenceValue(value);
  line.append(name, content);
  card.appendChild(line);
}

function renderReferences(references) {
  const container = $("references");
  container.replaceChildren();
  const labels = [
    "program_id", "story_phase", "input_state", "central_pressure",
    "reusable_program", "applicable_conditions", "failure_modes",
    "anti_repetition_notes", "output_state",
  ];
  for (const [index, reference] of references.entries()) {
    const card = document.createElement("article");
    card.className = "reference-card";
    const header = document.createElement("div");
    header.className = "reference-header";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.id = `reference-${index}`;
    checkbox.addEventListener("change", () => {
      const selected = document.querySelectorAll(".reference-card input:checked").length;
      if (selected > 3) {
        checkbox.checked = false;
        showStatus("最多选择 3 个 Reference Program", true);
        return;
      }
      updateReferenceCount();
    });
    const label = document.createElement("label");
    label.htmlFor = checkbox.id;
    label.textContent = reference.program_id || `Reference ${index + 1}`;
    header.append(checkbox, label);
    card.appendChild(header);
    for (const field of labels) addReferenceField(card, field, reference[field]);
    container.appendChild(card);
  }
  updateReferenceCount();
}

function updateReferenceCount() {
  $("reference-count").textContent = `${document.querySelectorAll(".reference-card input:checked").length} / 3`;
}

function selectedReferences() {
  return [...document.querySelectorAll(".reference-card input:checked")]
    .map((checkbox) => state.references[Number(checkbox.id.split("-").pop())]);
}

function currentTemplate() {
  return {
    outline: $("template-outline").value,
    chapter: $("template-chapter").value,
    review: $("template-review").value,
  }[$("prompt-mode").value];
}

function promptPayload() {
  return {
    mode: $("prompt-mode").value,
    template: currentTemplate(),
    book_content: composeBookContent(),
    current_outline: $("current-outline").value,
    recent_summaries: $("recent-summaries").value,
    selected_references: selectedReferences(),
    actual_summaries: $("actual-summaries").value,
    current_state: $("review-state").value || $("section-status").value,
    unfulfilled_promises: $("unfulfilled-promises").value,
    future_direction: $("future-direction").value,
  };
}

async function generatePrompt() {
  try {
    const payload = await requestJson("/api/prompt", {
      method: "POST",
      body: JSON.stringify(promptPayload()),
    });
    $("prompt-text").value = payload.prompt;
    $("proposal-editor").value = "";
    state.proposalDraftActive = false;
    showStatus("Prompt 已生成，可继续编辑后复制");
  } catch (error) {
    const missing = error.payload?.detail?.missing_fields;
    showStatus(missing?.length ? `当前章节 Prompt 被阻止：${missing.join("、")}` : error.message, true);
  }
}

async function copyPrompt() {
  const text = $("prompt-text").value;
  if (!text) {
    showStatus("Prompt 为空，先生成或编辑 Prompt", true);
    return;
  }
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    $("prompt-text").focus();
    $("prompt-text").select();
    document.execCommand("copy");
  }
  showStatus("Prompt 已复制到剪贴板");
}

function applyResponseToEditor(response, editor) {
  editor.value = response.value;
  editor.dispatchEvent(new Event("input", { bubbles: true }));
}

async function saveBook() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  try {
    await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/book`, {
      method: "PUT",
      body: JSON.stringify({ content: composeBookContent() }),
    });
    showStatus("BOOK.md 已保存");
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function saveTemplates() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  try {
    await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/prompts`, {
      method: "PUT",
      body: JSON.stringify({
        templates: {
          outline: $("template-outline").value,
          chapter: $("template-chapter").value,
          review: $("template-review").value,
        },
      }),
    });
    showStatus("PROMPTS.md 已保存");
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function saveProposal() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  const draft = state.proposalDraftActive ? $("proposal-editor").value : $("codex-response").value;
  try {
    await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/proposal`, {
      method: "PUT",
      body: JSON.stringify({ content: draft }),
    });
    $("proposal-editor").value = draft;
    showStatus("PROPOSAL.md 已保存");
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function approveChapter() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  try {
    const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/chapters`, {
      method: "POST",
      body: JSON.stringify({
        chapter_number: Number($("chapter-number").value),
        content: $("codex-response").value,
      }),
    });
    showStatus(`${payload.file} 已保存`);
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function createBook() {
  const bookId = $("book-id").value.trim();
  try {
    const book = await requestJson("/api/books", {
      method: "POST",
      body: JSON.stringify({ book_id: bookId }),
    });
    populateBook(book);
    await refreshBookList();
    $("book-select").value = bookId;
    showStatus(`已创建并加载 ${bookId}`);
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function initialize() {
  try {
    const payload = await requestJson("/api/references");
    state.references = payload.references;
    $("reference-root").textContent = `来源：${payload.root}`;
    renderReferences(state.references);
    await refreshBookList();
    if ($("book-select").options.length > 1) {
      $("book-select").selectedIndex = 1;
      await loadBook($("book-select").value);
    } else {
      showStatus("请先新建小说");
    }
  } catch (error) {
    showStatus(error.message, true);
  }
}

$("new-book").addEventListener("click", createBook);
$("load-book").addEventListener("click", () => loadBook($("book-select").value));
$("generate-prompt").addEventListener("click", generatePrompt);
$("copy-prompt").addEventListener("click", copyPrompt);
$("apply-response").addEventListener("click", () => {
  applyResponseToEditor($("codex-response"), $("proposal-editor"));
  state.proposalDraftActive = true;
  showStatus("返回文本已应用到浏览器编辑区，尚未写盘");
});
$("codex-response").addEventListener("input", () => {
  state.proposalDraftActive = false;
});
$("proposal-editor").addEventListener("input", () => {
  state.proposalDraftActive = true;
});
$("save-book").addEventListener("click", saveBook);
$("save-templates").addEventListener("click", saveTemplates);
$("save-proposal").addEventListener("click", saveProposal);
$("approve-chapter").addEventListener("click", approveChapter);
initialize();
