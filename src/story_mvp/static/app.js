const state = {
  bookId: "",
  references: [],
  proposalDraftActive: false,
};

const sectionTitles = {
  design: "# 小说总体设计画像",
  long_plan: "# 未来100章大型剧情块",
  small_plan: "# 未来十章逐章小纲",
  status: "# 当前状态、未兑现承诺与作者备注",
};

const designTitles = {
  type_promise: "## 1. 核心类型与读者承诺",
  world_structure: "## 2. 世界观结构",
  world_pressure: "## 3. 世界如何持续制造剧情压力",
  protagonist_model: "## 4. 主角模型、人物弧与核心矛盾",
  relationships: "## 5. 配角与关系系统",
  plot_engine: "## 6. 核心情节发动机",
  narrative_structure: "## 7. 叙事结构",
  prose: "## 8. 文风与可操作参数",
  dialogue: "## 9. 对话特点",
  rhythm: "## 10. 节奏结构",
  theme: "## 11. 主题、价值观与长期问题",
  strengths_risks: "## 12. 当前设计最强点与最弱点",
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
  const design = Object.entries(designTitles)
    .map(([key, title]) => `${title}\n\n${$(`design-${key}`).value.trim()}`)
    .join("\n\n");
  return Object.entries(sectionTitles)
    .map(([key, title]) => `${title}\n\n${key === "design" ? design : $(`section-${key}`).value.trim()}`)
    .join("\n\n") + "\n";
}

function parseLongPlanBlocks(text) {
  const headingPattern = /^\s*##\s*第\s*(\d+)\s*[—–-]\s*(\d+)\s*章\s*[：:]\s*(.+?)\s*$/;
  const lines = text.split(/\r?\n/);
  const blocks = [];
  let current = null;
  for (const line of lines) {
    const match = line.match(headingPattern);
    if (match) {
      if (current) blocks.push(current);
      current = { start: Number(match[1]), end: Number(match[2]), title: match[3], lines: [] };
    } else if (current) {
      current.lines.push(line);
    }
  }
  if (current) blocks.push(current);
  return blocks;
}

function panoramaField(lines, label) {
  const labelPattern = new RegExp(`^\\s*${label}\\s*[：:]\\s*(.*)$`);
  const stopPattern = /^\s*(具体发生|阶段结果|叙事功能|推向下一块)\s*[：:]/;
  const start = lines.findIndex((line) => labelPattern.test(line));
  if (start < 0) return "";
  const first = lines[start].match(labelPattern)?.[1] || "";
  const rest = [];
  for (const line of lines.slice(start + 1)) {
    if (stopPattern.test(line)) break;
    rest.push(line);
  }
  return [first, ...rest].join("\n").trim();
}

function renderLongPlanPanorama() {
  const container = $("long-plan-panorama");
  if (!container) return;
  const blocks = parseLongPlanBlocks($("section-long_plan").value);
  $("panorama-count").textContent = `${blocks.length} 个剧情块`;
  container.replaceChildren();
  if (!blocks.length) {
    const empty = document.createElement("p");
    empty.className = "panorama-empty";
    empty.textContent = "尚未识别到 ## 第X—Y章：标题 格式；原文仍可正常编辑和保存。";
    container.appendChild(empty);
    return;
  }
  for (const block of blocks) {
    const card = document.createElement("article");
    card.className = "panorama-card";
    const range = document.createElement("div");
    range.className = "panorama-range";
    range.textContent = `${block.start}—${block.end}章`;
    const title = document.createElement("h4");
    title.textContent = block.title;
    card.append(range, title);
    const stage = panoramaField(block.lines, "阶段结果");
    const functionText = panoramaField(block.lines, "叙事功能");
    const next = panoramaField(block.lines, "推向下一块");
    const fields = [
      ["核心变化", stage],
      ["关键兑现 / 功能", functionText],
      ["进入下一块", next],
    ];
    for (const [label, value] of fields) {
      if (!value) continue;
      const line = document.createElement("p");
      const name = document.createElement("strong");
      name.textContent = `${label}：`;
      line.append(name, document.createTextNode(value));
      card.appendChild(line);
    }
    if (!stage && !functionText && !next) {
      const fallback = document.createElement("p");
      fallback.textContent = block.lines.filter((line) => line.trim()).slice(0, 3).join(" ");
      card.appendChild(fallback);
    }
    container.appendChild(card);
  }
}

function setDesignDetails(open) {
  document.querySelectorAll(".design-card").forEach((card) => { card.open = open; });
}

function populateBook(book) {
  state.bookId = book.book_id;
  $("book-id").value = book.book_id;
  for (const key of Object.keys(designTitles)) {
    $(`design-${key}`).value = book.design_sections?.[key] || "";
  }
  for (const key of ["long_plan", "small_plan", "status"]) {
    $(`section-${key}`).value = book.sections?.[key] || "";
  }
  const templates = book.prompt_templates || {};
  $("template-idea").value = templates.idea || $("template-idea").value;
  $("template-outline").value = templates.outline || $("template-outline").value;
  $("template-chapter").value = templates.chapter || $("template-chapter").value;
  $("template-review").value = templates.review || $("template-review").value;
  $("proposal-editor").value = book.proposal || "";
  $("codex-response").value = "";
  state.proposalDraftActive = Boolean(book.proposal);
  renderLongPlanPanorama();
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
    idea: $("template-idea").value,
    outline: $("template-outline").value,
    chapter: $("template-chapter").value,
    review: $("template-review").value,
  }[$("prompt-mode").value];
}

function defaultGbrainQuery() {
  const direction = $("creative-direction").value.trim() || "当前创作方向";
  const mode = $("prompt-mode").value;
  const novelKnowledge = "reference-corpus-program-deep-v1 修仙小说素材库 book-dna syntheses observations Reference Program";
  const powerFantasySearch = "Payoff Grammar Core Progression Grammar Advantage / Special Capability Action-Space Expansion World Expansion Grammar Repeatable Reader Loop POWER_BREAKTHROUGH NEW_TECHNIQUE COMBAT_DOMINANCE UNDERDOG_VICTORY RESOURCE_GAIN STATUS_RISE WORLD_EXPANSION STRATEGIC_ADVANTAGE";
  if (mode === "outline") {
    return `针对以下中文男频成长爽文设定：\n${novelKnowledge}\n${powerFantasySearch}\n仙侠 玄幻 高武 修炼 突破 战斗验证 秘境 身份跃迁\n创作方向：${direction}\n一句话创意与读者承诺：${$("design-type_promise").value.trim() || "（未填写）"}\n主角模型与人物弧：${$("design-protagonist_model").value.trim() || "（未填写）"}\n当前状态：${$("section-status").value.trim() || "（未填写）"}\n\n寻找能够让资源转化为修为、功法、技法、战斗优势、新身份和新地图的小说蒸馏知识；同时寻找男频成长循环、公开证明、中期换挡、避免重复、Book DNA、Mechanism、Contrast 和 Reference Program。`;
  }
  if (mode === "review") {
    return `当前小说是中文男频成长爽文，方向为“${direction}”。\n${novelKnowledge}\n${powerFantasySearch}\n当前真实状态：${$("review-state").value.trim() || $("section-status").value.trim() || "（未填写）"}\n实际十章摘要：${$("actual-summaries").value.trim() || "（未填写）"}\n未兑现承诺：${$("unfulfilled-promises").value.trim() || "（未填写）"}\n\n寻找小说蒸馏知识中的 loop break、力量兑现、身份变化、关系压力、新行动空间、资源复利、中期换挡、不同类型 payoff、Book DNA、Mechanism、Contrast 和避免重复案例。`;
  }
  return `${novelKnowledge}；${powerFantasySearch}；仙侠 玄幻 高武 修炼 突破 战斗验证 秘境 身份跃迁；中文男频成长爽文；\n只寻找与“${direction}”相关的男频成长循环、核心爽点、金手指玩法、资源转修为、信息差、公开证明、payoff、早期兑现、长篇世界扩张、容易重复的失败模式和可借鉴的结构机制。`;
}

function setDefaultGbrainQuery() {
  $("gbrain-query").value = defaultGbrainQuery();
}

function populatePromptTemplates(templates) {
  for (const key of ["idea", "outline", "chapter", "review"]) {
    $(`template-${key}`).value = templates[key] || "";
  }
}

function promptPayload() {
  return {
    mode: $("prompt-mode").value,
    template: currentTemplate(),
    book_content: composeBookContent(),
    creative_direction: $("creative-direction").value,
    current_long_block: $("current-long-block").value,
    current_outline: $("current-outline").value,
    recent_summaries: $("recent-summaries").value,
    selected_references: selectedReferences(),
    gbrain_inspiration: $("gbrain-results").value,
    actual_summaries: $("actual-summaries").value,
    current_state: $("review-state").value || $("section-status").value,
    unfulfilled_promises: $("unfulfilled-promises").value,
    future_direction: $("future-direction").value,
  };
}

async function queryGbrain() {
  const query = $("gbrain-query").value.trim();
  if (!query) {
    $("gbrain-status").textContent = "GBrain：查询失败 — 查询不能为空";
    $("gbrain-status").classList.add("error");
    return showStatus("GBrain 查询不能为空", true);
  }
  try {
    const payload = await requestJson("/api/gbrain/query", {
      method: "POST",
      body: JSON.stringify({ query }),
    });
    $("gbrain-results").value = payload.result;
    $("gbrain-scope").textContent = `GBrain 范围：${payload.scope || "全 Brain"}`;
    $("gbrain-status").textContent = "GBrain：可用";
    $("gbrain-status").classList.remove("error");
    showStatus("GBrain 灵感已返回，可删改后进入 Prompt");
  } catch (error) {
    $("gbrain-results").value = "";
    $("gbrain-status").textContent = `GBrain：查询失败 — ${error.message}`;
    $("gbrain-status").classList.add("error");
    showStatus(error.message, true);
  }
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

async function generateIdeaPrompt() {
  $("prompt-mode").value = "idea";
  await generatePrompt();
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

function splitHeadingBlocks(text, titles) {
  const headingToKey = Object.fromEntries(
    Object.entries(titles).map(([key, heading]) => [heading, key]),
  );
  const result = {};
  let currentKey = "";
  let lines = [];
  const save = () => {
    if (currentKey) result[currentKey] = lines.join("\n").trim();
  };
  for (const line of text.split(/\r?\n/)) {
    const key = headingToKey[line.trim()];
    if (key) {
      save();
      currentKey = key;
      lines = [];
    } else if (currentKey) {
      lines.push(line);
    }
  }
  save();
  return result;
}

function applyOutlineToBook() {
  const source = state.proposalDraftActive ? $("proposal-editor").value : $("codex-response").value;
  const sections = splitHeadingBlocks(source, sectionTitles);
  let applied = 0;
  for (const [key, content] of Object.entries(sections)) {
    if (key === "design") {
      const designSections = splitHeadingBlocks(content, designTitles);
      for (const [designKey, designContent] of Object.entries(designSections)) {
        $(`design-${designKey}`).value = designContent;
        applied += 1;
      }
    } else {
      $(`section-${key}`).value = content;
      applied += 1;
    }
  }
  renderLongPlanPanorama();

  if (!applied) {
    showStatus("返回文本没有找到 BOOK 的四个固定标题或总体画像标题，未改变 BOOK 编辑区", true);
    return;
  }
  showStatus(`已将 ${applied} 个 BOOK 区域应用到浏览器编辑区，尚未写盘`);
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
          idea: $("template-idea").value,
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
    renderLongPlanPanorama();
    const defaultTemplates = await requestJson("/api/prompt-templates");
    populatePromptTemplates(defaultTemplates.templates);
    setDefaultGbrainQuery();
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
$("default-gbrain-query").addEventListener("click", setDefaultGbrainQuery);
$("query-gbrain").addEventListener("click", queryGbrain);
$("generate-idea-prompt").addEventListener("click", generateIdeaPrompt);
$("generate-prompt").addEventListener("click", generatePrompt);
$("copy-prompt").addEventListener("click", copyPrompt);
$("expand-design").addEventListener("click", () => setDesignDetails(true));
$("collapse-design").addEventListener("click", () => setDesignDetails(false));
$("section-long_plan").addEventListener("input", renderLongPlanPanorama);
$("apply-response").addEventListener("click", () => {
  applyResponseToEditor($("codex-response"), $("proposal-editor"));
  state.proposalDraftActive = true;
  showStatus("返回文本已应用到浏览器编辑区，尚未写盘");
});
$("apply-outline-to-book").addEventListener("click", applyOutlineToBook);
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
