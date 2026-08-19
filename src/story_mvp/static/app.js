const state = {
  bookId: "",
  references: [],
};

const sectionTitles = {
  design: "# 小说总体设计画像",
  long_plan: "# 未来100章大型剧情块",
  small_plan: "# 未来十章逐章小纲",
  status: "# 当前状态、未兑现承诺与作者备注",
};

const designTitles = {
  growth_genome: "## 0. 本书成长基因图",
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

function invalidateGbrainResults(reason = "") {
  $("gbrain-results").value = "";
  $("gbrain-raw-results").value = "";
  $("gbrain-rejections").value = "";
  $("gbrain-count").textContent = "raw 0 / accepted 0 / rejected 0";
  $("gbrain-status").textContent = "GBrain：上下文已变化，请重新查询";
  $("gbrain-status").classList.remove("error");
  if (reason) showStatus(`GBrain 结果已失效：${reason}`);
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
  invalidateGbrainResults("切换小说");
  clearReferenceSelection();
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
  $("template-chapter_prep").value = templates.chapter_prep || $("template-chapter_prep").value;
  $("template-chapter").value = templates.chapter || $("template-chapter").value;
  $("template-review").value = templates.review || $("template-review").value;
  for (const key of [
    "context_curator", "primary_writer", "specialist_opening", "specialist_dialogue",
    "specialist_action", "specialist_emotion", "chapter_integrator",
  ]) {
    $(`template-${key}`).value = templates[key] || $(`template-${key}`).value;
  }
  $("proposal-editor").value = book.proposal || "";
  $("current-chapter-plan").value = "";
  $("codex-response").value = "";
  $("chapter-body-for-save").value = "";
  $("chapter-fact-summary").value = "";
  $("state-delta-response").value = "";
  for (const id of [
    "curator-response", "primary-writer-response", "opening-specialist-response",
    "dialogue-specialist-response", "action-specialist-response",
    "emotion-specialist-response", "integrator-response",
  ]) $(id).value = "";
  renderLongPlanPanorama();
  refreshPreviousChapterText();
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

async function refreshPreviousChapterText() {
  const target = $("previous-chapter-text");
  if (!target || !state.bookId) return;
  const chapterNumber = Number($("chapter-number").value);
  if (!Number.isInteger(chapterNumber) || chapterNumber <= 1) {
    target.value = "";
    return;
  }
  const first = Math.max(1, chapterNumber - 2);
  const chapters = [];
  for (let number = first; number < chapterNumber; number += 1) {
    try {
      const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/chapters/${number}`);
      if (payload.content) chapters.push(`# ${number}章正文\n\n${payload.content}`);
    } catch (error) {
      showStatus(`读取第${number}章连续性上下文失败：${error.message}`, true);
      return;
    }
  }
  target.value = chapters.join("\n\n");
}

async function loadBook(bookId) {
  if (!bookId) {
    showStatus("请先输入或选择小说 ID", true);
    return;
  }
  try {
    populateBook(await requestJson(`/api/books/${encodeURIComponent(bookId)}`));
    await setDefaultGbrainQuery();
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

function clearReferenceSelection() {
  document.querySelectorAll(".reference-card input:checked").forEach((checkbox) => {
    checkbox.checked = false;
  });
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
    chapter_prep: $("template-chapter_prep").value,
    chapter: $("template-chapter").value,
    review: $("template-review").value,
    context_curator: $("template-context_curator").value,
    primary_writer: $("template-primary_writer").value,
    specialist_opening: $("template-specialist_opening").value,
    specialist_dialogue: $("template-specialist_dialogue").value,
    specialist_action: $("template-specialist_action").value,
    specialist_emotion: $("template-specialist_emotion").value,
    chapter_integrator: $("template-chapter_integrator").value,
  }[$("prompt-mode").value];
}

function gbrainContextPayload(queryOverride = "") {
  return {
    mode: $("prompt-mode").value,
    book_content: composeBookContent(),
    creative_direction: $("creative-direction").value,
    current_long_block: $("current-long-block").value,
    current_outline: $("current-outline").value,
    recent_summaries: $("recent-summaries").value,
    query_override: queryOverride,
  };
}

async function setDefaultGbrainQuery() {
  try {
    const payload = await requestJson("/api/gbrain/brief", {
      method: "POST",
      body: JSON.stringify(gbrainContextPayload()),
    });
    $("gbrain-query").value = payload.effective_query || payload.retrieval_brief || "";
    $("gbrain-scope").textContent = "GBrain 范围：修仙小说素材库小说蒸馏域 → 小说来源过滤 → BOOK 兼容性筛选";
  } catch (error) {
    showStatus(`生成 BOOK-aware Retrieval Brief 失败：${error.message}`, true);
  }
}

async function handlePromptModeChange() {
  clearReferenceSelection();
  invalidateGbrainResults("切换 Prompt 模式");
  await setDefaultGbrainQuery();
}

async function activatePromptMode(mode) {
  const changed = $("prompt-mode").value !== mode;
  $("prompt-mode").value = mode;
  if (changed) await handlePromptModeChange();
}

function populatePromptTemplates(templates) {
  for (const key of [
    "idea", "outline", "chapter_prep", "chapter", "review",
    "context_curator", "primary_writer", "specialist_opening", "specialist_dialogue",
    "specialist_action", "specialist_emotion", "chapter_integrator",
  ]) {
    $(`template-${key}`).value = templates[key] || "";
  }
}

function promptPayload() {
  return {
    mode: $("prompt-mode").value,
    template: currentTemplate(),
    writer_mode: $("writer-mode").value,
    book_content: composeBookContent(),
    creative_direction: $("creative-direction").value,
    current_long_block: $("current-long-block").value,
    previous_chapter_text: $("previous-chapter-text").value,
    current_outline: $("current-outline").value,
    current_chapter_plan: $("current-chapter-plan").value,
    recent_summaries: $("recent-summaries").value,
    selected_references: selectedReferences(),
    gbrain_inspiration: $("gbrain-results").value,
    proposal_context: $("proposal-editor").value,
    actual_summaries: $("actual-summaries").value,
    current_state: $("review-state").value || $("section-status").value,
    unfulfilled_promises: $("unfulfilled-promises").value,
    future_direction: $("future-direction").value,
    curator_response: $("curator-response").value,
    curated_context: $("curator-response").value,
    primary_writer_response: $("primary-writer-response").value,
    primary_draft: extractPrimaryDraft($("primary-writer-response").value),
    primary_fact_summary: extractPrimaryFactSummary($("primary-writer-response").value),
    specialist_opening_response: $("opening-specialist-response").value,
    specialist_dialogue_response: $("dialogue-specialist-response").value,
    specialist_action_response: $("action-specialist-response").value,
    specialist_emotion_response: $("emotion-specialist-response").value,
    enabled_specialists: {
      opening: $("specialist-opening-enabled").checked,
      dialogue: $("specialist-dialogue-enabled").checked,
      action: $("specialist-action-enabled").checked,
      emotion: $("specialist-emotion-enabled").checked,
    },
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
      body: JSON.stringify(gbrainContextPayload(query)),
    });
    $("gbrain-results").value = payload.result;
    $("gbrain-raw-results").value = payload.raw_stdout || "（没有可解析的原始检索结果）";
    $("gbrain-rejections").value = (payload.rejected || [])
      .map((item) => `${item.slug}：${item.reason}`)
      .join("\n") || "（没有排除项）";
    $("gbrain-count").textContent = `raw ${payload.raw_count} / accepted ${payload.accepted_count} / rejected ${payload.rejected_count} / limit ${payload.requested_limit} / final ${payload.final_limit}`;
    $("gbrain-scope").textContent = payload.scope || "GBrain 范围：修仙小说素材库小说蒸馏域 → 小说来源过滤 → BOOK 兼容性筛选";
    $("gbrain-status").textContent = "GBrain：可用，已完成 BOOK 筛选";
    $("gbrain-status").classList.remove("error");
    showStatus("已生成可编辑 Inspiration Bundle；原始结果和排除原因留在折叠面板");
  } catch (error) {
    $("gbrain-results").value = "";
    $("gbrain-raw-results").value = "";
    $("gbrain-rejections").value = "";
    $("gbrain-count").textContent = "raw 0 / accepted 0 / rejected 0";
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
    showStatus("Prompt 已生成，可继续编辑后复制");
  } catch (error) {
    const missing = error.payload?.detail?.missing_fields;
    showStatus(missing?.length ? `当前章节 Prompt 被阻止：${missing.join("、")}` : error.message, true);
  }
}

async function generateIdeaPrompt() {
  await activatePromptMode("idea");
  await generatePrompt();
}

function parseChapterPlanEntry(text, chapterNumber) {
  const headingPattern = /^\s*##\s*第\s*(\d+)\s*章\s*[：:]\s*(.+?)\s*$/;
  let current = null;
  for (const line of text.split(/\r?\n/)) {
    const match = line.match(headingPattern);
    if (match) {
      if (current && current.number === chapterNumber) return current.lines.join("\n").trim();
      current = { number: Number(match[1]), lines: [line.trim()] };
      continue;
    }
    if (current) current.lines.push(line);
  }
  if (current && current.number === chapterNumber) return current.lines.join("\n").trim();
  return "";
}

function loadCurrentChapterPlan() {
  const chapterNumber = Number($("chapter-number").value);
  if (!Number.isInteger(chapterNumber) || chapterNumber < 1) {
    $("current-chapter-plan").value = "";
    showStatus("章节编号必须是正整数", true);
    return false;
  }
  const plan = parseChapterPlanEntry($("section-small_plan").value, chapterNumber);
  if (!plan) {
    $("current-chapter-plan").value = "";
    showStatus(`未来十章中没有找到第 ${chapterNumber} 章`, true);
    return false;
  }
  $("current-chapter-plan").value = plan;
  invalidateGbrainResults("当前章计划已加载");
  showStatus(`已加载第 ${chapterNumber} 章十章计划，可生成当前章执行小纲 Prompt`);
  return true;
}

async function generateChapterPrepPrompt() {
  await activatePromptMode("chapter_prep");
  if (!loadCurrentChapterPlan()) return;
  await generatePrompt();
}

function stateDeltaPayload() {
  return {
    mode: "state_delta",
    book_content: composeBookContent(),
    chapter_number: Number($("chapter-number").value),
    recent_summaries: $("recent-summaries").value,
    chapter_prose: $("chapter-body-for-save").value,
    chapter_fact_summary: $("chapter-fact-summary").value,
  };
}

async function generateStateDeltaPrompt() {
  // 只拦截「生成 State Delta Prompt」动作本身，不是章节门禁：
  // 不影响正式正文提取、章节批准或保存路径。
  const chapterNumber = Number($("chapter-number").value);
  if (!Number.isInteger(chapterNumber) || chapterNumber < 1) {
    showStatus("生成 State Delta Prompt 需要正整数的当前章节编号", true);
    return;
  }
  if (!$("chapter-body-for-save").value.trim()) {
    showStatus("正式正文为空，无法生成 State Delta Prompt；请先提取或粘贴本章正式正文", true);
    return;
  }
  try {
    const payload = await requestJson("/api/prompt/state-delta", {
      method: "POST",
      body: JSON.stringify(stateDeltaPayload()),
    });
    $("prompt-text").value = payload.prompt;
    showStatus("State Delta Prompt 已生成，可复制给模型；它不会写盘，也不是章节门禁。已替换原 Prompt 输出区内容");
  } catch (error) {
    showStatus(error.message, true);
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
  const source = $("proposal-editor").value;
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
    showStatus("Proposal 编辑区没有找到 BOOK 的四个固定标题或总体画像标题，未改变 BOOK 编辑区", true);
    return;
  }
  showStatus(`已将 Proposal 编辑区中的 ${applied} 个 BOOK 区域应用到浏览器编辑区，尚未写盘`);
}

function extractChapterArtifact(response) {
  const bodyHeading = "# 正式正文";
  const summaryHeading = "# 章节事实摘要";
  const bodyStart = response.indexOf(bodyHeading);
  if (bodyStart < 0) return null;
  const bodyContentStart = bodyStart + bodyHeading.length;
  const summaryStart = response.indexOf(summaryHeading, bodyContentStart);
  const bodyEnd = summaryStart >= 0 ? summaryStart : response.length;
  const body = response.slice(bodyContentStart, bodyEnd).trim();
  if (!body) return null;
  const summary = summaryStart >= 0
    ? response.slice(summaryStart + summaryHeading.length).trim()
    : "";
  return { body, summary };
}

function extractPrimaryDraft(response) {
  const heading = "# Primary Draft";
  const start = response.indexOf(heading);
  if (start < 0) return "";
  const contentStart = start + heading.length;
  const end = response.indexOf("# Primary Fact Summary", contentStart);
  return response.slice(contentStart, end >= 0 ? end : response.length).trim();
}

function extractPrimaryFactSummary(response) {
  const heading = "# Primary Fact Summary";
  const start = response.indexOf(heading);
  if (start < 0) return "";
  return response.slice(start + heading.length).trim();
}

function applyHybridResponse(response, editorId) {
  applyResponseToEditor($("codex-response"), $(editorId));
  showStatus(`已将当前 Codex 返回放入 ${editorId}，尚未自动采用或写盘`);
}

async function generateHybridNodePrompt(mode) {
  await activatePromptMode(mode);
  await generatePrompt();
}

function extractIntegratorBody() {
  const artifact = extractChapterArtifact($("integrator-response").value);
  if (!artifact) {
    showStatus("Integrator 返回缺少非空 `# 正式正文`，未改变保存内容", true);
    return false;
  }
  $("chapter-body-for-save").value = artifact.body;
  $("chapter-fact-summary").value = artifact.summary;
  showStatus("已从 Integrator 提取正式正文；尚未保存章节");
  return true;
}

function adoptPrimaryDraft() {
  const body = extractPrimaryDraft($("primary-writer-response").value);
  if (!body) {
    showStatus("Primary Writer 返回缺少非空 `# Primary Draft`，未改变保存内容", true);
    return false;
  }
  $("chapter-body-for-save").value = body;
  $("chapter-fact-summary").value = extractPrimaryFactSummary($("primary-writer-response").value);
  showStatus("已显式采用 Primary Draft 作为最终正文；尚未保存章节");
  return true;
}

function extractChapterBody() {
  const artifact = extractChapterArtifact($("codex-response").value);
  if (!artifact) {
    showStatus("返回文本没有找到“# 正式正文”区块，未改变保存内容", true);
    return false;
  }
  $("chapter-body-for-save").value = artifact.body;
  $("chapter-fact-summary").value = artifact.summary;
  showStatus("已提取正式正文；审计信息和事实摘要不会写入章节文件");
  return true;
}

function extractProposedCanonIndex(response) {
  // 先剥离围栏代码块，避免命中代码块内或 Audit 中的引用；
  // 只匹配行首一级标题，终止条件限定下一个一级标题（提案内 ## 子标题不截断）。
  const heading = /^# Proposed Canon Index[ \t]*$/;
  const stripped = response.replace(/^```[^\n]*\n[\s\S]*?^```[ \t]*$/gm, "");
  const lines = stripped.split(/\r?\n/);
  const start = lines.findIndex((line) => heading.test(line));
  if (start < 0) return null;
  const collected = [];
  for (const line of lines.slice(start + 1)) {
    if (/^#(?!\#)/.test(line)) break;
    collected.push(line);
  }
  const content = collected.join("\n").trim();
  return content ? content : null;
}

function applyCanonIndexProposal() {
  const proposed = extractProposedCanonIndex($("state-delta-response").value);
  if (!proposed) {
    showStatus("模型返回缺少 `# Proposed Canon Index` 一级标题或内容为空，未修改 BOOK 状态编辑区", true);
    return;
  }
  $("section-status").value = proposed;
  showStatus("Proposed Canon Index 已应用到浏览器 BOOK 状态编辑区，尚未写盘；确认后请点“保存 BOOK.md”");
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
          chapter_prep: $("template-chapter_prep").value,
          chapter: $("template-chapter").value,
          review: $("template-review").value,
          context_curator: $("template-context_curator").value,
          primary_writer: $("template-primary_writer").value,
          specialist_opening: $("template-specialist_opening").value,
          specialist_dialogue: $("template-specialist_dialogue").value,
          specialist_action: $("template-specialist_action").value,
          specialist_emotion: $("template-specialist_emotion").value,
          chapter_integrator: $("template-chapter_integrator").value,
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
  const draft = $("proposal-editor").value;
  try {
    await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/proposal`, {
      method: "PUT",
      body: JSON.stringify({ content: draft }),
    });
    showStatus("Proposal 编辑区已保存到 PROPOSAL.md");
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function approveChapter() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  const chapterBody = $("chapter-body-for-save").value.trim();
  if (!chapterBody) {
    return showStatus("请先从 Codex 返回文本提取正式正文，再保存章节", true);
  }
  try {
    const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/chapters`, {
      method: "POST",
      body: JSON.stringify({
        chapter_number: Number($("chapter-number").value),
        content: chapterBody,
      }),
    });
    await refreshPreviousChapterText();
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
    await setDefaultGbrainQuery();
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
      await setDefaultGbrainQuery();
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
$("generate-curator-prompt").addEventListener("click", () => generateHybridNodePrompt("context_curator"));
$("generate-primary-writer-prompt").addEventListener("click", () => generateHybridNodePrompt("primary_writer"));
$("generate-opening-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_opening"));
$("generate-dialogue-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_dialogue"));
$("generate-action-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_action"));
$("generate-emotion-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_emotion"));
$("generate-integrator-prompt").addEventListener("click", () => generateHybridNodePrompt("chapter_integrator"));
$("apply-curator-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "curator-response"));
$("apply-primary-writer-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "primary-writer-response"));
$("apply-opening-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "opening-specialist-response"));
$("apply-dialogue-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "dialogue-specialist-response"));
$("apply-action-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "action-specialist-response"));
$("apply-emotion-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "emotion-specialist-response"));
$("extract-integrator-body").addEventListener("click", extractIntegratorBody);
$("adopt-primary-draft").addEventListener("click", adoptPrimaryDraft);
$("load-current-chapter-plan").addEventListener("click", loadCurrentChapterPlan);
$("generate-chapter-prep").addEventListener("click", generateChapterPrepPrompt);
$("copy-prompt").addEventListener("click", copyPrompt);
$("apply-chapter-prep").addEventListener("click", () => {
  applyResponseToEditor($("codex-response"), $("current-outline"));
  showStatus("Codex 返回已放入当前章小纲，尚未写盘");
});
$("chapter-number").addEventListener("change", () => {
  $("chapter-body-for-save").value = "";
  $("chapter-fact-summary").value = "";
  $("current-chapter-plan").value = "";
  for (const id of [
    "curator-response", "primary-writer-response", "opening-specialist-response",
    "dialogue-specialist-response", "action-specialist-response",
    "emotion-specialist-response", "integrator-response",
  ]) $(id).value = "";
  invalidateGbrainResults("切换章节");
  refreshPreviousChapterText();
});
$("prompt-mode").addEventListener("change", handlePromptModeChange);
$("expand-design").addEventListener("click", () => setDesignDetails(true));
$("collapse-design").addEventListener("click", () => setDesignDetails(false));
$("section-long_plan").addEventListener("input", renderLongPlanPanorama);
$("section-long_plan").addEventListener("input", () => {
  invalidateGbrainResults("未来100章剧情块已变化");
});
$("section-small_plan").addEventListener("input", () => {
  $("current-chapter-plan").value = "";
  invalidateGbrainResults("未来十章计划已变化");
});
for (const id of [
  "creative-direction", "current-long-block", "current-outline", "recent-summaries",
]) {
  $(id).addEventListener("input", () => invalidateGbrainResults(`${id} 已变化`));
}
for (const key of Object.keys(designTitles)) {
  $(`design-${key}`).addEventListener("input", () => invalidateGbrainResults("BOOK 核心设计已变化"));
}
$("apply-response").addEventListener("click", () => {
  applyResponseToEditor($("codex-response"), $("proposal-editor"));
  showStatus("Codex 返回已放入 Proposal 编辑区，尚未写盘");
});
$("apply-outline-to-book").addEventListener("click", applyOutlineToBook);
$("extract-chapter-body").addEventListener("click", extractChapterBody);
$("generate-state-delta-prompt").addEventListener("click", generateStateDeltaPrompt);
$("apply-canon-index-proposal").addEventListener("click", applyCanonIndexProposal);
$("save-book").addEventListener("click", saveBook);
$("save-templates").addEventListener("click", saveTemplates);
$("save-proposal").addEventListener("click", saveProposal);
$("approve-chapter").addEventListener("click", approveChapter);
initialize();
