const state = {
  bookId: "",
  references: [],
  currentRun: null,
  creativeState: {},
  creativeArtifacts: {},
  creativeSources: {},
  workflow: null,
  view: "overview",
  designTab: "overall",
  chapterTab: "outline",
  designEditing: false,
  dirtyEditors: new Set(),
  gbrainDefaultBrief: "",
};

const creativeUi = {
  world_vision: {
    editor: "creative-world-vision",
    meta: "creative-meta-world-vision",
    save: "save-world-vision",
    approve: "approve-world-vision",
    generate: "generate-world-vision-prompt",
    apply: "apply-world-vision-response",
  },
  power_seed: {
    editor: "creative-power-seed",
    meta: "creative-meta-power-seed",
    save: "save-power-seed",
    generate: "generate-power-seed-prompt",
    apply: "apply-power-seed-response",
  },
  human_seed: {
    editor: "creative-human-seed",
    meta: "creative-meta-human-seed",
    save: "save-human-seed",
    generate: "generate-human-seed-prompt",
    apply: "apply-human-seed-response",
  },
  proposal: {
    editor: "proposal-editor",
    meta: "creative-meta-proposal",
    save: "save-proposal",
    approve: "approve-proposal",
    generate: "generate-story-program-prompt",
    apply: "apply-story-program-response",
  },
};

const sectionTitles = {
  design: "# 小说总体设计画像",
  long_plan: "# 当前中期规划窗口",
  small_plan: "# 未来十章逐章小纲",
  status: "# 当前状态、未兑现承诺与作者备注",
};
const legacySectionTitleAliases = {
  "# 未来100章大型剧情块": "long_plan",
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

const viewNames = new Set(["overview", "creative", "design", "chapter", "memory", "tools"]);

function currentViewFromHash() {
  const value = window.location.hash.replace(/^#/, "");
  return viewNames.has(value) ? value : "overview";
}

function dirtyEditorIds() {
  return [...document.querySelectorAll("textarea:not([readonly])"), $("creative-direction")]
    .map((element) => element.id)
    .filter(Boolean);
}

function markEditorDirty(id) {
  if (!id || !state.bookId) return;
  state.dirtyEditors.add(id);
  renderDirtyState();
}

function clearEditorDirty(ids = dirtyEditorIds()) {
  for (const id of ids) state.dirtyEditors.delete(id);
  renderDirtyState();
}

function hasDirtyEditors() {
  return state.dirtyEditors.size > 0;
}

function confirmDiscardIfNeeded(action = "离开当前工作区") {
  if (!hasDirtyEditors()) return true;
  return window.confirm(`当前有未保存的编辑，${action}不会自动保存。继续吗？`);
}

function renderDirtyState() {
  const count = state.dirtyEditors.size;
  const overview = $("overview-dirty");
  if (overview) overview.textContent = count ? `未保存编辑 ${count} 项` : "";
  document.body.classList.toggle("has-unsaved-edits", count > 0);
}

function setView(view, updateHash = true) {
  if (!viewNames.has(view)) view = "overview";
  state.view = view;
  document.querySelectorAll(".workspace-view").forEach((element) => {
    element.hidden = element.dataset.view !== view;
  });
  document.querySelectorAll(".nav-link").forEach((link) => {
    link.classList.toggle("active", link.dataset.viewTarget === view);
  });
  document.body.dataset.view = view;
  if (view !== "memory") document.body.classList.remove("memory-editor-open");
  if (updateHash && window.location.hash !== `#${view}`) window.location.hash = view;
  if (view === "chapter") {
    if (["world_vision", "power_seed", "human_seed", "idea", "outline", "review"].includes($("prompt-mode")?.value)) {
      $("prompt-mode").value = "chapter";
    }
    setChapterTab(state.chapterTab);
    updateChapterWorkspace();
  }
  if (view === "design") setDesignTab(state.designTab);
  if (view === "memory") renderMemoryWorkspace();
  renderDirtyState();
}

function navigateToView(view, action = "离开当前工作区") {
  if (view === state.view) return true;
  if (!confirmDiscardIfNeeded(action)) return false;
  setView(view, true);
  return true;
}

function setDesignTab(tab) {
  if (!["overall", "midterm", "future10"].includes(tab)) tab = "overall";
  state.designTab = tab;
  document.querySelectorAll("[data-design-view]").forEach((element) => {
    element.hidden = element.dataset.designView !== tab;
  });
  document.querySelectorAll("[data-design-tab]").forEach((button) => {
    button.classList.toggle("active", button.dataset.designTab === tab);
  });
  if (tab === "midterm") renderLongPlanPanorama();
  if (tab === "future10") renderFuture10Cards();
}

function setChapterTab(tab) {
  if (!["outline", "body", "execution"].includes(tab)) tab = "outline";
  state.chapterTab = tab;
  document.querySelectorAll("[data-chapter-tab]").forEach((button) => {
    button.classList.toggle("active", button.dataset.chapterTab === tab);
  });
  const showOutline = tab === "outline" || tab === "execution";
  const showBody = tab === "body" || tab === "execution";
  const showExecution = tab === "execution";
  const toggle = (id, visible) => {
    const element = $(id);
    if (!element) return;
    const wrapper = element.closest("label") || element.closest(".state-delta-block") || element;
    wrapper.hidden = !visible;
  };
  toggle("chapter-outline-actions", showOutline);
  toggle("current-chapter-plan", showOutline);
  toggle("current-outline", showOutline);
  const bodyEditor = $("chapter-body-editor");
  if (bodyEditor) bodyEditor.hidden = !showBody;
  const advanced = $("chapter-advanced-actions");
  if (advanced) advanced.hidden = !showExecution;
  const execution = $("chapter-execution-details");
  if (execution) execution.hidden = !showExecution;
  const contextButton = $("toggle-chapter-context");
  if (contextButton) contextButton.textContent = document.body.classList.contains("chapter-context-open") ? "隐藏上下文" : "显示上下文";
  document.body.dataset.chapterTab = tab;
}

function updateChapterWorkspace() {
  const chapter = currentChapterNumber();
  const action = chapterActionForNode(state.workflow?.next_actionable_node);
  const title = $("chapter-workspace-title");
  if (title) title.textContent = `第 ${chapter} 章`;
  const next = $("chapter-workspace-next");
  if (next) next.textContent = state.workflow ? `下一步：${action.title}` : "等待 Workflow";
  const target = $("chapter-generation-target");
  if (target) target.textContent = state.workflow ? `Workflow 下一步：${action.title}` : "加载小说后由 Workflow State 决定下一步";
  const button = $("generate-prompt");
  if (button) button.textContent = action.button;
  const sidebarChapter = $("sidebar-book-chapter");
  if (sidebarChapter) sidebarChapter.textContent = `当前第 ${chapter} 章`;
}

function renderDesignPreviews() {
  for (const key of Object.keys(designTitles)) {
    const target = $("design-preview-" + key);
    const source = $("design-" + key);
    if (!target || !source) continue;
    const value = source.value.trim().replace(/\s+/g, " ");
    target.textContent = value ? (value.length > 220 ? `${value.slice(0, 220)}…` : value) : "尚未填写。";
  }
}

function parseFuture10Entries(text) {
  const headingPattern = /^\s*##\s*第\s*(\d+)\s*章\s*[：:]\s*(.+?)\s*$/;
  const entries = [];
  let current = null;
  for (const line of text.split(/\r?\n/)) {
    const match = line.match(headingPattern);
    if (match) {
      if (current) entries.push(current);
      current = { number: Number(match[1]), title: match[2], lines: [] };
    } else if (current) {
      current.lines.push(line);
    }
  }
  if (current) entries.push(current);
  return entries;
}

function renderFuture10Cards() {
  const container = $("future10-cards");
  if (!container) return;
  const entries = parseFuture10Entries($("section-small_plan")?.value || "");
  $("future10-count").textContent = `${entries.length} 章`;
  container.replaceChildren();
  if (!entries.length) {
    const empty = document.createElement("p");
    empty.className = "panorama-empty";
    empty.textContent = "尚未识别到 ## 第N章：标题 格式；原文仍可编辑。";
    container.appendChild(empty);
    return;
  }
  for (const entry of entries) {
    const card = document.createElement("article");
    card.className = "future10-card";
    const heading = document.createElement("strong");
    heading.textContent = `第${entry.number}章 · ${entry.title}`;
    const summary = document.createElement("p");
    summary.textContent = entry.lines.filter((line) => line.trim()).slice(0, 4).join(" ") || "尚未填写章节小纲。";
    card.append(heading, summary);
    container.appendChild(card);
  }
}

function memorySection(text, heading) {
  const lines = text.split(/\r?\n/);
  const index = lines.findIndex((line) => line.trim().toUpperCase() === `## ${heading}`);
  if (index < 0) return "";
  const result = [];
  for (const line of lines.slice(index + 1)) {
    if (/^##\s+/.test(line.trim())) break;
    result.push(line);
  }
  return result.join("\n").trim();
}

function renderMemoryWorkspace() {
  const container = $("memory-cards");
  if (!container) return;
  const status = $("section-status")?.value || "";
  container.replaceChildren();
  const sections = [
    ["ACTIVE SCENE STATE", "当前场景状态"],
    ["PERSISTENT CANON", "持久正史"],
    ["RECENT SUMMARIES", "最近摘要"],
    ["OPEN PROMISES", "未兑现承诺"],
    ["AUTHOR NOTES", "作者备注"],
  ];
  for (const [heading, label] of sections) {
    const card = document.createElement("article");
    card.className = "memory-card";
    const title = document.createElement("h3");
    title.textContent = label;
    const body = document.createElement("p");
    const value = memorySection(status, heading);
    body.textContent = value ? (value.length > 420 ? `${value.slice(0, 420)}…` : value) : "尚未记录。";
    card.append(title, body);
    container.appendChild(card);
  }
  const entry = state.workflow?.artifacts?.["book.canon_state"];
  $("memory-revision").textContent = entry ? `rev ${entry.revision || 0} · ${entry.status || "EMPTY"}` : "未加载";
}

function renderOverview(snapshot) {
  const book = state.bookId || "未加载";
  const chapter = snapshot?.current_chapter || currentChapterNumber();
  const artifacts = snapshot?.artifacts || {};
  const stale = Object.values(artifacts).filter((entry) => entry.status === "STALE").length;
  const next = snapshot?.next_actionable_node || "等待 Workflow";
  const nextAction = chapterActionForNode(snapshot?.next_actionable_node);
  $("overview-book").textContent = book;
  $("overview-book-path").textContent = book === "未加载" ? "请从上方加载小说" : "本地工作区已连接";
  $("overview-chapter").textContent = snapshot ? `第 ${chapter} 章` : "—";
  $("overview-chapter-state").textContent = snapshot ? (artifacts[`chapter.${chapter}.body`]?.status || "正文未载入") : "—";
  $("overview-next").textContent = snapshot ? nextAction.title : next;
  $("overview-next-detail").textContent = snapshot ? `主操作：${nextAction.button}` : "加载小说后显示";
  $("overview-stale").textContent = snapshot ? `${stale} 项 stale` : "—";
  $("overview-stale-detail").textContent = stale ? "打开执行透明度查看依赖影响" : "暂无需要处理的 stale";
  $("continue-chapter").textContent = snapshot ? `继续写第 ${chapter} 章` : "继续写作";
  const flow = $("overview-flow");
  if (!flow) return;
  flow.replaceChildren();
  for (const stage of workflowStages) {
    const item = document.createElement("span");
    item.className = "flow-step";
    item.textContent = stage.title;
    flow.appendChild(item);
  }
}

function mountRightDrawer() {
  const body = $("right-drawer-body");
  if (!body) return;
  for (const id of ["workflow-panel", "prompt-mode-control", "prompt-response-advanced"]) {
    const element = $(id);
    if (element && element.parentElement !== body) body.appendChild(element);
  }
}

function openRightDrawer() {
  mountRightDrawer();
  const drawer = $("right-drawer");
  if (!drawer) return;
  drawer.classList.add("open");
  drawer.setAttribute("aria-hidden", "false");
}

function closeRightDrawer() {
  const drawer = $("right-drawer");
  if (!drawer) return;
  drawer.classList.remove("open");
  drawer.setAttribute("aria-hidden", "true");
}

function initializeReadingState() {
  document.querySelectorAll(".creative-stage").forEach((stage) => {
    stage.open = true;
    const summary = stage.querySelector("summary");
    if (!summary || summary.dataset.readingBound) return;
    summary.dataset.readingBound = "true";
    summary.addEventListener("click", (event) => {
      event.preventDefault();
      stage.classList.toggle("stage-editing");
      stage.open = true;
    });
  });
  document.querySelectorAll(".design-card").forEach((card) => { card.open = true; });
}

const workflowStages = [
  { title: "创意", keys: ["creative.world_vision", "creative.power_seed", "creative.human_seed", "creative.character_card", "creative.story_program"] },
  { title: "设计", keys: ["book.design"] },
  { title: "规划", keys: ["book.long_plan", "book.future_10"] },
  { title: "当前章节", keys: [] },
  { title: "记忆", keys: ["book.canon_state"] },
];

const workflowLabels = {
  "creative.world_vision": "世界幻想",
  "creative.power_seed": "力量种子",
  "creative.human_seed": "人物种子",
  "creative.character_card": "人物权威",
  "creative.story_program": "故事方案",
  "book.design": "总体设计",
  "book.long_plan": "中期规划",
  "book.future_10": "未来十章",
  "book.canon_state": "记忆状态",
};

const chapterActionDefaults = {
  director: { mode: "director", title: "当前章 Director", button: "生成当前章 Director", tab: "outline" },
  chapter_prep: { mode: "chapter_prep", title: "当前章执行小纲", button: "生成执行小纲", tab: "outline" },
  curator: { mode: "context_curator", title: "上下文整理", button: "生成上下文整理", tab: "execution" },
  primary: { mode: "primary_writer", title: "主稿正文", button: "生成正文草稿", tab: "body" },
  opening: { mode: "specialist_opening", title: "开场建议", button: "生成开场建议", tab: "execution" },
  dialogue: { mode: "specialist_dialogue", title: "对话建议", button: "生成对话建议", tab: "execution" },
  action: { mode: "specialist_action", title: "动作建议", button: "生成动作建议", tab: "execution" },
  emotion: { mode: "specialist_emotion", title: "情绪建议", button: "生成情绪建议", tab: "execution" },
  integrator: { mode: "chapter_integrator", title: "整合正文", button: "生成整合正文", tab: "execution" },
  state_delta: { mode: "state_delta", title: "状态更新", button: "生成状态更新 Prompt", tab: "execution" },
};

function chapterActionForNode(node) {
  if (node === "primary" && $("writer-mode")?.value === "single") {
    return { mode: "chapter", title: "正式正文", button: "生成正文 Prompt", tab: "body" };
  }
  return chapterActionDefaults[node] || {
    mode: "chapter",
    title: "正式正文",
    button: "生成正文 Prompt",
    tab: "body",
  };
}

function currentChapterActionNode() {
  return state.workflow?.next_actionable_node || "director";
}

let selectedWorkflowArtifact = "";

function workflowArtifactLabel(artifact) {
  if (workflowLabels[artifact]) return workflowLabels[artifact];
  const match = artifact.match(/^chapter\.(\d+)\.(run|body|state_delta)$/);
  if (!match) return artifact;
  const labels = { run: "Run", body: "正式正文", state_delta: "State Delta" };
  return `第${match[1]}章 ${labels[match[2]]}`;
}

function workflowLocation(artifact) {
  const staticPaths = {
    "creative.world_vision": "WORLD_VISION.md",
    "creative.power_seed": "POWER_SEED.md",
    "creative.human_seed": "HUMAN_SEED.md",
    "creative.character_card": "CHARACTER.md",
    "creative.story_program": "PROPOSAL.md",
    "book.design": "BOOK.md · design",
    "book.long_plan": "BOOK.md · long_plan",
    "book.future_10": "BOOK.md · small_plan",
    "book.canon_state": "BOOK.md · status",
  };
  if (staticPaths[artifact]) return staticPaths[artifact];
  const match = artifact.match(/^chapter\.(\d+)\.(run|body|state_delta)$/);
  if (!match) return artifact;
  const files = { run: "runs/chapter-NNNN/manifest.json", body: "chapters/chapter-NNNN.md", state_delta: "runs/chapter-NNNN/manifest.json" };
  return files[match[2]].replace("NNNN", String(match[1]).padStart(4, "0"));
}

function workflowStatusLabel(status) {
  return status || "EMPTY";
}

function renderWorkflow(snapshot) {
  const stages = $("workflow-stages");
  if (!stages) return;
  stages.replaceChildren();
  state.workflow = snapshot;
  renderOverview(snapshot);
  renderMemoryWorkspace();
  renderDesignPreviews();
  renderFuture10Cards();
  updateChapterWorkspace();
  if (!snapshot) {
    $("workflow-current").textContent = "Workflow：未加载";
    $("workflow-impact").textContent = "点击节点后显示实际存在的受影响下游。";
    $("workflow-detail").textContent = "点击节点查看状态和实际影响。";
    $("locate-workflow-artifact").disabled = true;
    return;
  }
  const artifacts = snapshot.artifacts || {};
  const staleCount = Object.values(artifacts).filter((entry) => entry.status === "STALE").length;
  $("workflow-current").textContent = `当前：Chapter ${snapshot.current_chapter} · Next：${snapshot.next_actionable_node || "—"} · STALE ${staleCount}`;
  $("chapter-workspace-next").textContent = snapshot.next_actionable_node
    ? `下一节点：${snapshot.next_actionable_node}`
    : "没有下一节点";
  for (const stage of workflowStages) {
    const card = document.createElement("div");
    card.className = "workflow-stage";
    const title = document.createElement("div");
    title.className = "workflow-stage-title";
    title.textContent = stage.title;
    card.appendChild(title);
    const list = document.createElement("div");
    list.className = "workflow-node-list";
    let keys = [...stage.keys];
    if (stage.title === "当前章节") {
      const chapter = snapshot.current_chapter;
      keys = ["run", "body", "state_delta"].map((kind) => `chapter.${chapter}.${kind}`)
        .filter((key) => artifacts[key]);
      if (!keys.length) {
        const empty = document.createElement("span");
        empty.className = "workflow-detail";
        empty.textContent = `第${chapter}章 · Run 尚未创建`;
        list.appendChild(empty);
      }
    }
    for (const key of keys) {
      const entry = artifacts[key];
      if (!entry) continue;
      const button = document.createElement("button");
      button.type = "button";
      button.className = "workflow-node";
      button.dataset.artifact = key;
      const name = document.createElement("span");
      name.textContent = workflowArtifactLabel(key);
      const status = document.createElement("span");
      status.className = `workflow-node-status ${String(entry.status || "").toLowerCase()}`;
      status.textContent = `${workflowStatusLabel(entry.status)} · rev ${entry.revision || 0}`;
      button.append(name, status);
      button.addEventListener("click", () => showWorkflowArtifact(key));
      list.appendChild(button);
    }
    card.appendChild(list);
    stages.appendChild(card);
  }
}

async function showWorkflowArtifact(artifact) {
  selectedWorkflowArtifact = artifact;
  const entry = state.workflow?.artifacts?.[artifact] || {};
  $("workflow-detail").textContent = [
    `节点：${workflowArtifactLabel(artifact)}`,
    `状态：${entry.status || "EMPTY"}`,
    `revision：${entry.revision || 0}`,
    `最后来源：${entry.last_source || "—"}`,
    `真实位置：${workflowLocation(artifact)}`,
    `stale 原因：${(entry.stale_from || []).join("、") || "—"}`,
  ].join("\n");
  $("locate-workflow-artifact").disabled = false;
  try {
    const impact = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/workflow/impact?artifact=${encodeURIComponent(artifact)}`);
    const actual = impact.existing_nodes_affected || [];
    const protectedChapters = impact.protected_completed_chapters || [];
    $("workflow-impact").textContent = [
      `直接下游：${(impact.direct_dependents || []).map(workflowArtifactLabel).join("、") || "无"}`,
      `实际受影响：${actual.map(workflowArtifactLabel).join("、") || "无"}`,
      `保护历史章节：${protectedChapters.join("、") || "无"}`,
    ].join("\n");
  } catch (error) {
    $("workflow-impact").textContent = `Impact 读取失败：${error.message}`;
  }
}

function locateWorkflowArtifact() {
  if (!selectedWorkflowArtifact) return;
  const match = selectedWorkflowArtifact.match(/^chapter\.(\d+)\.(run|body|state_delta)$/);
  if (match) {
    $("chapter-number").value = match[1];
    navigateToView("chapter", "定位章节节点");
    if (match[2] === "body") loadCurrentChapterBody();
    else loadRun();
    setChapterTab(match[2] === "body" ? "body" : "execution");
    closeRightDrawer();
  }
  const targets = {
    "creative.world_vision": "creative-world-vision",
    "creative.power_seed": "creative-power-seed",
    "creative.human_seed": "creative-human-seed",
    "creative.character_card": "creative-character-card",
    "creative.story_program": "proposal-editor",
    "book.design": "design-sections",
    "book.long_plan": "section-long_plan",
    "book.future_10": "section-small_plan",
    "book.canon_state": "section-status",
  };
  const target = $(targets[selectedWorkflowArtifact] || "prompt-panel");
  if (selectedWorkflowArtifact.startsWith("creative.")) navigateToView("creative", "定位创意节点");
  if (selectedWorkflowArtifact === "book.design") navigateToView("design", "定位设计节点");
  if (selectedWorkflowArtifact === "book.long_plan") { navigateToView("design", "定位中期规划"); setDesignTab("midterm"); }
  if (selectedWorkflowArtifact === "book.future_10") { navigateToView("design", "定位未来十章"); setDesignTab("future10"); }
  if (selectedWorkflowArtifact === "book.canon_state") { navigateToView("memory", "定位记忆节点"); }
  target?.scrollIntoView({ behavior: "smooth", block: "center" });
}

async function refreshWorkflow() {
  if (!state.bookId) {
    renderWorkflow(null);
    return;
  }
  try {
    const [workflow, executors] = await Promise.all([
      requestJson(`/api/books/${encodeURIComponent(state.bookId)}/workflow`),
      requestJson("/api/executors"),
    ]);
    renderWorkflow(workflow);
    const openai = executors.openai_api || {};
    $("openai-executor-status").textContent = openai.configured
      ? `OpenAI API：已配置 · main=${openai.model} · state=${openai.state_model || openai.model}`
      : "OpenAI API：未配置";
  } catch (error) {
    renderWorkflow(null);
    showStatus(`Workflow 刷新失败：${error.message}`, true);
  }
}

async function refreshExecutorStatus() {
  try {
    const executors = await requestJson("/api/executors");
    const openai = executors.openai_api || {};
    $("openai-executor-status").textContent = openai.configured
      ? `OpenAI API：已配置 · ${openai.name || openai.model} · state=${openai.state_model || openai.model}`
      : "OpenAI API：未配置";
  } catch (error) {
    $("openai-executor-status").textContent = "OpenAI API：读取失败";
  }
}

async function loadOpenAISettings() {
  try {
    const settings = await requestJson("/api/settings/openai");
    $("settings-api-name").value = settings.name || "";
    $("settings-api-url").value = settings.url || "";
    $("settings-api-key").value = "";
    $("settings-status").textContent = settings.configured
      ? "已配置：" + (settings.name || "未命名") + (settings.persistent ? "（用户环境变量；Key 不回显）" : "（Key 不回显）")
      : "未配置";
  } catch (error) {
    $("settings-status").textContent = `读取失败：${error.message}`;
  }
}

async function saveOpenAISettings() {
  try {
    const settings = await requestJson("/api/settings/openai", {
      method: "PUT",
      body: JSON.stringify({
        name: $("settings-api-name").value,
        url: $("settings-api-url").value,
        api_key: $("settings-api-key").value,
      }),
    });
    $("settings-api-key").value = "";
    $("settings-status").textContent = settings.configured
      ? "已保存：" + (settings.name || "未命名") + (settings.persistent ? "（用户环境变量；Key 不回显）" : "（Key 不回显）")
      : "未配置";
    await refreshExecutorStatus();
    showStatus("OpenAI API 设置已保存到当前后端进程");
  } catch (error) {
    $("settings-status").textContent = `保存失败：${error.message}`;
    showStatus(error.message, true);
  }
}

function showStatus(message, isError = false) {
  const target = $("status");
  target.textContent = message;
  target.classList.toggle("error", isError);
}

function renderCreativeMeta(artifact) {
  const ui = creativeUi[artifact];
  const value = state.creativeArtifacts[artifact] || state.creativeState[artifact] || {};
  const target = $(ui.meta);
  if (!target) return;
  target.textContent = `${value.origin || "empty"} · ${value.status || "empty"}`;
}

function renderCreativePreview(artifact) {
  const ui = creativeUi[artifact];
  const target = $("creative-preview-" + (artifact === "proposal" ? "proposal" : artifact.replaceAll("_", "-")));
  const source = $(ui.editor);
  if (!target || !source) return;
  const value = source.value.trim().replace(/\s+/g, " ");
  target.textContent = value ? (value.length > 260 ? `${value.slice(0, 260)}…` : value) : "尚未填写。";
}

function setCreativePayload(payload) {
  state.creativeState = payload?.creative_state || {};
  state.creativeArtifacts = payload?.creative_artifacts || {};
  state.creativeSources = {};
  for (const artifact of Object.keys(creativeUi)) {
    const ui = creativeUi[artifact];
    const value = state.creativeArtifacts[artifact] || {
      content: payload?.[artifact] || "",
      origin: state.creativeState[artifact]?.origin || "empty",
      status: state.creativeState[artifact]?.status || "empty",
    };
    state.creativeArtifacts[artifact] = value;
    $(ui.editor).value = value.content || "";
    renderCreativeMeta(artifact);
    renderCreativePreview(artifact);
  }
  const character = state.creativeArtifacts.character_card || {
    content: payload?.character_card || "",
    origin: state.creativeState.character_card?.origin || "empty",
    status: state.creativeState.character_card?.status || "empty",
  };
  state.creativeArtifacts.character_card = character;
  $("creative-character-card").value = character.content || "";
  $("creative-character-initial-state").value = payload?.character_initial_state || "";
  $("creative-character-audition").value = payload?.character_audition || "";
  $("creative-meta-character-card").textContent = `${character.origin || "empty"} · ${character.status || "empty"}`;
}

function markCreativeEdited(artifact) {
  const current = state.creativeArtifacts[artifact] || {};
  state.creativeSources[artifact] = "author_edited";
  state.creativeArtifacts[artifact] = {
    content: $(creativeUi[artifact].editor).value,
    origin: "author_edited",
    status: "draft",
  };
  state.creativeState[artifact] = {
    origin: state.creativeArtifacts[artifact].origin,
    status: state.creativeArtifacts[artifact].status,
  };
  if (!current.content && !$(creativeUi[artifact].editor).value.trim()) {
    state.creativeArtifacts[artifact] = { content: "", origin: "empty", status: "empty" };
    state.creativeState[artifact] = { origin: "empty", status: "empty" };
  }
  renderCreativeMeta(artifact);
  renderCreativePreview(artifact);
}

function applyCreativeResponse(artifact) {
  const ui = creativeUi[artifact];
  if (artifact === "proposal") {
    applyResponseToEditor($("codex-response"), $("proposal-editor"));
  } else {
    applyResponseToEditor($("codex-response"), $(ui.editor));
  }
  state.creativeSources[artifact] = "model_generated";
  state.creativeArtifacts[artifact] = {
    content: $(ui.editor).value,
    origin: "model_generated",
    status: "draft",
  };
  state.creativeState[artifact] = {
    origin: "model_generated",
    status: "draft",
  };
  renderCreativeMeta(artifact);
  renderCreativePreview(artifact);
  showStatus(`模型返回已放入 ${artifact} 编辑器，仍为 draft，尚未保存或批准`);
}

async function saveCreativeArtifact(artifact) {
  if (!state.bookId) return showStatus("请先加载小说", true);
  const ui = creativeUi[artifact];
  const paths = {
    world_vision: "world-vision",
    power_seed: "power-seed",
    human_seed: "human-seed",
    proposal: "proposal",
  };
  const path = paths[artifact];
  if (!path) return showStatus(`未知创意产物：${artifact}`, true);
  try {
    const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/${path}`, {
      method: "PUT",
      body: JSON.stringify({
        content: $(ui.editor).value,
        origin: state.creativeSources[artifact] || null,
      }),
    });
    setCreativePayload(payload);
    clearEditorDirty([ui.editor]);
    await refreshWorkflow();
    showStatus(`${artifact} 已保存，仍需作者明确批准`);
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function approveCreativeArtifact(artifact) {
  if (!state.bookId) return showStatus("请先加载小说", true);
  const paths = { world_vision: "world-vision", proposal: "proposal" };
  const path = paths[artifact];
  if (!path) return showStatus("Power/Human 只通过一次 Character 批准冻结", true);
  try {
    const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/${path}/approve`, {
      method: "POST",
    });
    setCreativePayload(payload);
    clearEditorDirty([creativeUi[artifact].editor]);
    await refreshWorkflow();
    showStatus(`${artifact} 已由作者明确批准`);
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function approveCharacter() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  const power = $("creative-power-seed").value;
  const human = $("creative-human-seed").value;
  try {
    const base = `/api/books/${encodeURIComponent(state.bookId)}`;
    await requestJson(`${base}/power-seed`, {
      method: "PUT",
      body: JSON.stringify({ content: power, origin: state.creativeSources.power_seed || "author_edited" }),
    });
    await requestJson(`${base}/human-seed`, {
      method: "PUT",
      body: JSON.stringify({ content: human, origin: state.creativeSources.human_seed || "author_edited" }),
    });
    const payload = await requestJson(`${base}/character/approve`, { method: "POST" });
    setCreativePayload(payload);
    clearEditorDirty(["creative-power-seed", "creative-human-seed"]);
    await refreshWorkflow();
    showStatus("Character 已批准：Power + Human 同时冻结，CHARACTER.md 已确定性合成");
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function generateCreativePrompt(mode) {
  await activatePromptMode(mode);
  await generatePrompt();
}

const runNodeByMode = {
  chapter: "primary",
  director: "director",
  context_curator: "curator",
  primary_writer: "primary",
  specialist_opening: "opening",
  specialist_dialogue: "dialogue",
  specialist_action: "action",
  specialist_emotion: "emotion",
  chapter_integrator: "integrator",
  state_delta: "state_delta",
};

function currentChapterNumber() {
  return Number($("chapter-number").value);
}

function checkedSpecialistNames() {
  return ["opening", "dialogue", "action", "emotion"]
    .filter((name) => $(`specialist-${name}-enabled`).checked);
}

function selectedSpecialistNames() {
  const selected = checkedSpecialistNames();
  if (["single", "curator_primary"].includes($("writer-mode").value)) return [];
  if ($("writer-mode").value === "hybrid_selective") return selected.slice(0, 2);
  return selected;
}

function runBaseUrl() {
  return `/api/books/${encodeURIComponent(state.bookId)}/runs/${currentChapterNumber()}`;
}

function renderRunLedger(manifest) {
  state.currentRun = manifest;
  const summary = $("run-ledger-summary");
  const container = $("run-ledger-status");
  if (!summary || !container) return;
  if (!manifest) {
    summary.textContent = "Run Ledger：未载入";
    container.replaceChildren();
    return;
  }
  summary.textContent = `Run Ledger：${manifest.run_status} · final=${manifest.final_source || "未采用"}`;
  container.replaceChildren();
  const table = document.createElement("table");
  table.className = "run-ledger-table";
  const head = document.createElement("tr");
  ["节点", "状态", "attempts", "Prompt", "Response", "操作"].forEach((label) => {
    const cell = document.createElement("th");
    cell.textContent = label;
    head.appendChild(cell);
  });
  table.appendChild(head);
  for (const [node, info] of Object.entries(manifest.nodes || {})) {
    const row = document.createElement("tr");
    [node, info.status, String(info.attempts || 0), info.prompt_file || "—", info.response_file || "—"]
      .forEach((value) => {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.appendChild(cell);
      });
    const actions = document.createElement("td");
    if (["failed", "stale"].includes(info.status)) {
      const retry = document.createElement("button");
      retry.textContent = "重试节点";
      retry.addEventListener("click", () => retryRunNode(node));
      actions.appendChild(retry);
    }
    if (["completed", "adopted"].includes(info.status) && ["primary", "integrator"].includes(node)) {
      const adopt = document.createElement("button");
      adopt.textContent = `采用${node === "primary" ? "Primary" : "Integrator"}`;
      adopt.addEventListener("click", () => adoptRunSource(node));
      actions.appendChild(adopt);
    }
    row.appendChild(actions);
    table.appendChild(row);
  }
  container.appendChild(table);
}

async function loadRun() {
  if (!state.bookId || !Number.isInteger(currentChapterNumber()) || currentChapterNumber() < 1) return;
  try {
    renderRunLedger(await requestJson(runBaseUrl()));
  } catch (error) {
    if (error.payload?.detail && String(error.payload.detail).includes("尚未创建 Run")) {
      renderRunLedger(null);
      return;
    }
    showStatus(`读取 Run 失败：${error.message}`, true);
  }
}

async function createRun() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  try {
    const payload = await requestJson(runBaseUrl(), {
      method: "POST",
      body: JSON.stringify({
        writer_mode: $("writer-mode").value,
        selected_specialists: selectedSpecialistNames(),
      }),
    });
    renderRunLedger(payload);
    await refreshWorkflow();
    showStatus("当前章 Run 已创建或载入");
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function activateSelectedRepair() {
  if (!state.bookId || !state.currentRun) return showStatus("请先创建当前章 Run", true);
  const selected = checkedSpecialistNames();
  if (!selected.length) return showStatus("请至少勾选一个 Specialist", true);
  try {
    const payload = await requestJson(`${runBaseUrl()}/repair-specialists`, {
      method: "PUT",
      body: JSON.stringify({ selected_specialists: selected }),
    });
    renderRunLedger(payload);
    await refreshWorkflow();
    showStatus(`已显式启用 repair：${selected.join("、")}；默认主链仍保持 curator_primary。`);
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function saveRunPromptForMode(mode, prompt) {
  const node = runNodeByMode[mode];
  if (!node || !state.currentRun || !prompt.trim()) return;
  try {
    renderRunLedger(await requestJson(`${runBaseUrl()}/nodes/${node}/prompt`, {
      method: "PUT",
      body: JSON.stringify({ content: prompt }),
    }));
    await refreshWorkflow();
  } catch (error) {
    showStatus(`保存 ${node} Prompt 到 Run 失败：${error.message}`, true);
  }
}

async function saveRunResponseForMode(mode, response) {
  const node = runNodeByMode[mode];
  if (!node || !state.currentRun || !response.trim()) return;
  try {
    renderRunLedger(await requestJson(`${runBaseUrl()}/nodes/${node}/response`, {
      method: "PUT",
      body: JSON.stringify({ content: response }),
    }));
    await refreshWorkflow();
  } catch (error) {
    showStatus(`保存 ${node} Response 到 Run 失败：${error.message}`, true);
  }
}

async function retryRunNode(node) {
  try {
    renderRunLedger(await requestJson(`${runBaseUrl()}/nodes/${node}/retry`, { method: "POST" }));
    await refreshWorkflow();
    showStatus(`${node} 已按原 Prompt 准备重试`);
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function adoptRunSource(source) {
  try {
    renderRunLedger(await requestJson(`${runBaseUrl()}/adopt`, {
      method: "POST",
      body: JSON.stringify({ source }),
    }));
    await refreshWorkflow();
    showStatus(`已在 Run Ledger 中采用 ${source}；章节仍需作者显式保存`);
  } catch (error) {
    showStatus(error.message, true);
  }
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
  const stopPattern = /^\s*(具体发生|阶段结果|叙事功能|推向下一块|核心幻想推进|一级成长变化|主要情绪兑现|二级收益结算|世界扩张|代价或余波(?:（可选）)?)\s*[：:]/;
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
    const stage = panoramaField(block.lines, "阶段结果") || panoramaField(block.lines, "一级成长变化");
    const functionText = panoramaField(block.lines, "叙事功能") || panoramaField(block.lines, "核心幻想推进");
    const emotion = panoramaField(block.lines, "主要情绪兑现");
    const next = panoramaField(block.lines, "推向下一块");
    const fields = [
      ["核心变化", stage],
      ["关键兑现 / 功能", functionText],
      ["主要情绪", emotion],
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

function setDesignEditing(open) {
  state.designEditing = open;
  document.body.classList.toggle("design-editor-open", open);
  document.querySelectorAll(".design-card").forEach((card) => card.classList.toggle("is-editing", open));
  for (const id of ["long-plan-editor", "small-plan-editor"]) {
    const element = $(id);
    if (element) element.classList.toggle("is-editing", open);
  }
  const button = $("toggle-design-editor");
  if (button) button.textContent = open ? "收起原文编辑" : "编辑原文";
}

function populateBook(book) {
  invalidateGbrainResults("切换小说");
  clearReferenceSelection();
  clearEditorDirty();
  setDesignEditing(false);
  document.querySelectorAll(".creative-stage").forEach((stage) => stage.classList.remove("stage-editing"));
  state.bookId = book.book_id;
  state.workflow = null;
  selectedWorkflowArtifact = "";
  $("book-id").value = book.book_id;
  $("sidebar-book-name").textContent = book.book_id;
  setCreativePayload(book);
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
  $("director-response").value = "";
  $("codex-response").value = "";
  $("chapter-body-for-save").value = "";
  $("chapter-fact-summary").value = "";
  $("state-delta-response").value = "";
  for (const id of [
    "director-response",
    "curator-response", "primary-writer-response", "opening-specialist-response",
    "dialogue-specialist-response", "action-specialist-response",
    "emotion-specialist-response", "integrator-response",
  ]) $(id).value = "";
  renderRunLedger(null);
  renderLongPlanPanorama();
  renderFuture10Cards();
  renderDesignPreviews();
  renderMemoryWorkspace();
  updateChapterWorkspace();
  refreshPreviousChapterText();
  loadRun();
  refreshWorkflow();
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
  if (bookId !== state.bookId && !confirmDiscardIfNeeded("加载另一本小说")) return;
  try {
    populateBook(await requestJson(`/api/books/${encodeURIComponent(bookId)}`));
    await setDefaultGbrainQuery();
  } catch (error) {
    showStatus(error.message, true);
  }
}

function openMemoryEditor() {
  if (!navigateToView("memory", "打开记忆编辑区")) return;
  document.body.classList.add("memory-editor-open");
  $("memory-status-editor")?.scrollIntoView({ behavior: "smooth", block: "center" });
}

function openPromptTemplates() {
  if (!navigateToView("tools", "打开 Prompt Templates")) return;
  const editor = $("template-editor");
  if (editor) {
    editor.open = true;
    editor.scrollIntoView({ behavior: "smooth", block: "center" });
  }
}

function editFuture10() {
  if (!navigateToView("design", "编辑 Future 10")) return;
  setDesignTab("future10");
  setDesignEditing(true);
  $("small-plan-editor")?.scrollIntoView({ behavior: "smooth", block: "center" });
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
    world_vision: "",
    power_seed: "",
    human_seed: "",
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
    world_vision: $("creative-world-vision").value,
    prototype_id: $("human-prototype-selector")?.value || "",
    character_card: $("creative-character-card").value,
    proposal_context: $("proposal-editor").value,
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
    state.gbrainDefaultBrief = payload.retrieval_brief || "";
    $("gbrain-query").value = state.gbrainDefaultBrief;
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
    book_id: state.bookId,
    template: currentTemplate(),
    writer_mode: $("writer-mode").value,
    chapter_number: Number($("chapter-number").value),
    book_content: composeBookContent(),
    creative_direction: $("creative-direction").value,
    world_vision: $("creative-world-vision").value,
    power_seed: $("creative-power-seed").value,
    human_seed: $("creative-human-seed").value,
    prototype_id: $("human-prototype-selector")?.value || "",
    character_card: $("creative-character-card").value,
    character_initial_state: $("creative-character-initial-state").value,
    creative_state: state.creativeState,
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
    const manualOverride = query === state.gbrainDefaultBrief ? "" : query;
    const payload = await requestJson("/api/gbrain/query", {
      method: "POST",
      body: JSON.stringify(gbrainContextPayload(manualOverride)),
    });
    $("gbrain-results").value = payload.result;
    $("gbrain-raw-results").value = payload.raw_stdout || "（没有可解析的原始检索结果）";
    $("gbrain-rejections").value = (payload.rejected || [])
      .map((item) => `${item.slug}：${item.reason}`)
      .join("\n") || "（没有排除项）";
    const coordinateCount = payload.coordinate_reference_count || 0;
    $("gbrain-count").textContent = `raw ${payload.raw_count} / coordinate ${coordinateCount} + creative ${payload.accepted_count} / rejected ${payload.rejected_count} / limit ${payload.requested_limit} / final ${payload.final_limit}`;
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
  const mode = $("prompt-mode").value;
  try {
    const payload = await requestJson("/api/prompt", {
      method: "POST",
      body: JSON.stringify(promptPayload()),
    });
    $("prompt-text").value = payload.prompt;
    await saveRunPromptForMode(mode, payload.prompt);
    renderCodexTaskWrapper(mode);
    if (currentExecutorMode() === "openai_api") await executeOpenAI(payload.prompt, mode);
    showStatus("Prompt 已生成，可继续编辑后复制");
  } catch (error) {
    const missing = error.payload?.detail?.missing_fields;
    const missingArtifacts = error.payload?.detail?.missing_artifacts;
    showStatus(
      missingArtifacts?.length
        ? `${error.payload.detail.message}（缺少：${missingArtifacts.join("、")}）`
        : missing?.length ? `当前章节 Prompt 被阻止：${missing.join("、")}` : error.message,
      true,
    );
  }
}

async function generateIdeaPrompt() {
  await activatePromptMode("idea");
  await generatePrompt();
}

function currentExecutorMode() {
  return $("executor-mode").value;
}

function externalArtifactForMode(mode) {
  const creative = {
    world_vision: "creative.world_vision",
    power_seed: "creative.power_seed",
    human_seed: "creative.human_seed",
    idea: "creative.story_program",
  };
  if (creative[mode]) return creative[mode];
  const node = runNodeByMode[mode];
  if (node) return `chapter.${currentChapterNumber()}.run`;
  return mode === "outline" || mode === "review" ? "book.future_10" : "book.future_10";
}

function renderCodexTaskWrapper(mode) {
  const panel = $("codex-task-wrapper-panel");
  const output = $("codex-task-wrapper");
  if (currentExecutorMode() !== "codex_external" || !state.bookId) {
    panel.hidden = true;
    output.value = "";
    return;
  }
  const artifact = externalArtifactForMode(mode);
  const node = runNodeByMode[mode] || "";
  const chapter = currentChapterNumber();
  const workspace = $("workspace-path")?.textContent.trim() || "<workspace>";
  const promptPath = node && state.currentRun
    ? `${workspace}\\${state.bookId}\\runs\\chapter-${String(chapter).padStart(4, "0")}\\${node}_prompt.md`
    : "当前页面的完整 Prompt 文本框（请先保存/复制）";
  const tempPath = `${workspace}\\${state.bookId}\\.workflow_tmp\\${artifact.replaceAll(".", "-")}-response.md`;
  const nodeArgs = node ? ` --chapter ${chapter} --node ${node}` : "";
  output.value = [
    "在当前 thegreatnovel 工作区执行 Story MVP 节点。",
    "",
    `Book: ${state.bookId}`,
    `Artifact: ${artifact}`,
    `读取已经保存的 Prompt：${promptPath}`,
    "严格按该 Prompt 生成最终输出。",
    "不要修改其它上游文件。",
    `把最终输出暂存到：${tempPath}`,
    "然后运行：",
    `story-mvp-workflow apply --book ${state.bookId} --artifact ${artifact} --input "${tempPath}" --source codex_external${nodeArgs}`,
    "完成后报告：node、output path、workflow status、stale dependents。",
    "不要继续运行下一节点。",
  ].join("\n");
  panel.hidden = false;
}

async function executeOpenAI(prompt, mode = "") {
  const isStateExtraction = mode === "state_delta";
  const explicitModel = isStateExtraction
    ? $("state-model").value.trim()
    : $("openai-model").value.trim();
  const payload = await requestJson("/api/executors/openai", {
    method: "POST",
    body: JSON.stringify({
      prompt,
      model: explicitModel,
      purpose: isStateExtraction ? "state_extraction" : "default",
    }),
  });
  $("codex-response").value = payload.output_text;
  showStatus(`OpenAI API 已返回 ${payload.model}；结果仍需作者 Apply / Save`);
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

function setPromptModeSilently(mode) {
  const select = $("prompt-mode");
  if (!select || ![...select.options].some((option) => option.value === mode)) return;
  select.value = mode;
}

function chapterNeedsPlan(node) {
  return [
    "director", "chapter_prep", "curator", "primary", "opening", "dialogue", "action", "emotion", "integrator",
  ].includes(node);
}

async function ensureChapterRun() {
  if (state.currentRun) return true;
  await createRun();
  return Boolean(state.currentRun);
}

async function prepareChapterAction() {
  const node = currentChapterActionNode();
  const action = chapterActionForNode(node);
  setPromptModeSilently(action.mode);
  setChapterTab(action.tab);
  if (chapterNeedsPlan(node) && !$("current-chapter-plan").value.trim()) loadCurrentChapterPlan();
  updateChapterWorkspace();
  return { node, action };
}

async function generateCurrentChapterAction() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  const { node, action } = await prepareChapterAction();
  if (["director", "curator", "primary", "opening", "dialogue", "action", "emotion", "integrator", "state_delta"].includes(node)) {
    if (!await ensureChapterRun()) return;
  }
  if (node === "chapter_prep") {
    await generateChapterPrepPrompt();
  } else if (node === "state_delta") {
    await generateStateDeltaPrompt();
  } else if (node === "director") {
    await generateHybridNodePrompt("director");
  } else if (node === "primary" && action.mode === "chapter") {
    await activatePromptMode("chapter");
    await generatePrompt();
  } else if (node === "primary") {
    await generateHybridNodePrompt("primary_writer");
  } else if (node === "curator") {
    await generateHybridNodePrompt("context_curator");
  } else if (node === "opening") {
    await generateHybridNodePrompt("specialist_opening");
  } else if (node === "dialogue") {
    await generateHybridNodePrompt("specialist_dialogue");
  } else if (node === "action") {
    await generateHybridNodePrompt("specialist_action");
  } else if (node === "emotion") {
    await generateHybridNodePrompt("specialist_emotion");
  } else if (node === "integrator") {
    await generateHybridNodePrompt("chapter_integrator");
  } else {
    await activatePromptMode(action.mode);
    await generatePrompt();
  }
  openRightDrawer();
}

function stateDeltaPayload() {
  return {
    mode: "state_delta",
    book_content: composeBookContent(),
    chapter_number: Number($("chapter-number").value),
    recent_summaries: $("recent-summaries").value,
    chapter_prose: $("chapter-body-for-save").value,
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
    await saveRunPromptForMode("state_delta", payload.prompt);
    if (currentExecutorMode() === "openai_api") await executeOpenAI(payload.prompt, "state_delta");
    showStatus("轻量 State Extraction Prompt 已生成；OpenAI 模式可使用独立 State 模型。它不会写盘，也不是章节门禁。");
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
  let source = text;
  if (titles === sectionTitles) {
    const firstHeading = sectionTitles.design;
    const firstHeadingIndex = source.indexOf(firstHeading);
    if (firstHeadingIndex >= 0) source = source.slice(firstHeadingIndex);
  }
  const headingToKey = Object.fromEntries(
    Object.entries(titles).map(([key, heading]) => [heading, key]),
  );
  if (titles === sectionTitles) Object.assign(headingToKey, legacySectionTitleAliases);
  const result = {};
  let currentKey = "";
  let lines = [];
  const save = () => {
    if (currentKey) result[currentKey] = lines.join("\n").trim();
  };
  for (const line of source.split(/\r?\n/)) {
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

async function skipIntegratorWithoutPatches(responses) {
  try {
    renderRunLedger(await requestJson(`${runBaseUrl()}/integrator/skip-if-no-patches`, {
      method: "POST",
      body: JSON.stringify({ specialist_responses: responses }),
    }));
    showStatus("所有已运行专项都没有有效 Patch，Integrator 已 skipped；可直接采用 Primary");
  } catch (error) {
    showStatus(error.message, true);
  }
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
        markEditorDirty(`design-${designKey}`);
        applied += 1;
      }
    } else {
      $(`section-${key}`).value = content;
      markEditorDirty(`section-${key}`);
      applied += 1;
    }
  }
  renderLongPlanPanorama();
  renderFuture10Cards();
  renderDesignPreviews();

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
  const formalHeading = "# 正式正文";
  const formalStart = response.indexOf(formalHeading);
  if (formalStart >= 0) {
    return response.slice(formalStart + formalHeading.length).trim();
  }
  const legacyHeading = "# Primary Draft";
  const legacyStart = response.indexOf(legacyHeading);
  if (legacyStart >= 0) {
    const contentStart = legacyStart + legacyHeading.length;
    const end = response.indexOf("# Primary Fact Summary", contentStart);
    return response.slice(contentStart, end >= 0 ? end : response.length).trim();
  }
  const clean = response.trim();
  if (/^#\s+(Primary Writer Audit|Primary Fact Summary|Writer Audit|章节事实摘要)\s*$/m.test(clean)) return "";
  return clean;
}

function extractPrimaryFactSummary(response) {
  const heading = "# Primary Fact Summary";
  const start = response.indexOf(heading);
  if (start < 0) return "";
  return response.slice(start + heading.length).trim();
}

async function applyDirectorResponse() {
  const response = $("codex-response").value;
  if (!response.trim()) {
    showStatus("Director 返回为空，未改变当前章小纲", true);
    return;
  }
  $("director-response").value = response;
  const lines = [];
  const fieldLabels = new Set();
  let afterField = false;
  for (const line of response.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (/^#{1,6}\s/.test(trimmed)) {
      if (afterField) break;
      continue;
    }
    const fieldMatch = /^(触发事件|推动事件的人|主角行动|对手或世界反应|直接结果|状态变化|叙事功能|结尾推动力)\s*[：:]/.exec(trimmed);
    if (fieldMatch) {
      fieldLabels.add(fieldMatch[1]);
      afterField = true;
      lines.push(trimmed);
    } else if (afterField && trimmed) {
      lines.push(trimmed);
    }
  }
  if (fieldLabels.size !== 8) {
    showStatus("Director 返回没有完整八字段，未改变当前章小纲", true);
    return;
  }
  $("current-outline").value = lines.join("\n");
  markEditorDirty("current-outline");
  await saveRunResponseForMode("director", response);
  showStatus("Director 八字段已采用到当前章小纲；尚未写盘");
}

async function applyHybridResponse(response, editorId) {
  applyResponseToEditor($("codex-response"), $(editorId));
  const modeByEditor = {
    "curator-response": "context_curator",
    "primary-writer-response": "primary_writer",
    "opening-specialist-response": "specialist_opening",
    "dialogue-specialist-response": "specialist_dialogue",
    "action-specialist-response": "specialist_action",
    "emotion-specialist-response": "specialist_emotion",
  };
  await saveRunResponseForMode(modeByEditor[editorId] || "", response);
  showStatus(`已将当前 Codex 返回放入 ${editorId}，尚未自动采用或写盘`);
}

async function generateHybridNodePrompt(mode) {
  await activatePromptMode(mode);
  if (mode === "chapter_integrator" && state.currentRun) {
    const responses = {
      opening: $("opening-specialist-response").value,
      dialogue: $("dialogue-specialist-response").value,
      action: $("action-specialist-response").value,
      emotion: $("emotion-specialist-response").value,
    };
    const hasPatch = Object.values(responses).some((value) => /^##\s+Patch\s+\d+/m.test(value));
    if (!hasPatch) {
      await skipIntegratorWithoutPatches(responses);
      return;
    }
  }
  await generatePrompt();
}

async function extractIntegratorBody() {
  const artifact = extractChapterArtifact($("integrator-response").value);
  if (!artifact) {
    showStatus("Integrator 返回缺少非空 `# 正式正文`，未改变保存内容", true);
    return false;
  }
  $("chapter-body-for-save").value = artifact.body;
  $("chapter-fact-summary").value = artifact.summary;
  markEditorDirty("chapter-body-for-save");
  markEditorDirty("chapter-fact-summary");
  await saveRunResponseForMode("chapter_integrator", $("integrator-response").value);
  showStatus("已从 Integrator 提取正式正文；尚未保存章节");
  return true;
}

async function adoptPrimaryDraft() {
  const body = extractPrimaryDraft($("primary-writer-response").value);
  if (!body) {
    showStatus("Primary Writer 返回缺少非空正式正文，未改变保存内容", true);
    return false;
  }
  $("chapter-body-for-save").value = body;
  $("chapter-fact-summary").value = "";
  markEditorDirty("chapter-body-for-save");
  await saveRunResponseForMode("primary_writer", $("primary-writer-response").value);
  await adoptRunSource("primary");
  showStatus("已采用 Primary 正式正文；下一步直接进入轻量 State Extraction。尚未保存章节");
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
  markEditorDirty("chapter-body-for-save");
  markEditorDirty("chapter-fact-summary");
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

function extractStateDeltaV2(response) {
  const stripped = response.replace(/^```[^\n]*\n[\s\S]*?^```[ \t]*$/gm, "");
  if (/^#{1,2}\s+AUTHOR NOTES\s*$/m.test(stripped)) {
    return { error: "State Delta 返回不得包含 AUTHOR NOTES；旧 AUTHOR NOTES 必须由代码逐字保留" };
  }
  const headings = {
    "# Proposed Active Scene State": "active_scene_state",
    "# Proposed Persistent Canon": "persistent_canon",
    "# Proposed Chapter Summary": "chapter_summary",
    "# Proposed Open Promises": "open_promises",
  };
  const lines = stripped.split(/\r?\n/);
  const result = {};
  for (const [heading, key] of Object.entries(headings)) {
    const start = lines.findIndex((line) => line.trim() === heading);
    if (start < 0) continue;
    const collected = [];
    for (const line of lines.slice(start + 1)) {
      if (/^#(?!#)/.test(line)) break;
      collected.push(line);
    }
    const content = collected.join("\n").trim();
    if (content) result[key] = content;
  }
  const missing = Object.values(headings).filter((key) => !result[key]);
  if (missing.length) return null;
  return result;
}

function existingCanonSection(status, v2Heading, legacyLabel) {
  const lines = status.split(/\r?\n/);
  const start = lines.findIndex((line) => line.trim() === v2Heading || line.trim().startsWith(`${legacyLabel}：`) || line.trim().startsWith(`${legacyLabel}:`));
  if (start < 0) return "";
  const first = lines[start].trim() === v2Heading ? "" : lines[start].replace(/^.*?[：:]/, "").trim();
  const collected = first ? [first] : [];
  for (const line of lines.slice(start + 1)) {
    if (line.trim().startsWith("## ") || line.trim().startsWith("# ") || /^(最近章节摘要|当前状态|未兑现承诺|作者备注)[：:]/.test(line.trim())) break;
    collected.push(line);
  }
  return collected.join("\n").trim();
}

function existingAuthorNotes(status) {
  return existingCanonSection(status, "## AUTHOR NOTES", "作者备注");
}

function compactPromiseWindow(text, maxEntries = 12) {
  const entries = [];
  const seen = new Set();
  for (const rawLine of text.split(/\r?\n/)) {
    let clean = rawLine.replace(/^\s*(?:[-*+]\s+|\d+[.)、]\s*)/, "").trim();
    if (!clean) continue;
    clean = clean.replace(/\s+/g, " ");
    const key = clean.replace(/[\s，。；;：:！？!?、]/g, "").toLowerCase();
    if (!key || seen.has(key)) continue;
    seen.add(key);
    if (clean.length > 240) clean = `${clean.slice(0, 239).trim()}…`;
    entries.push(clean);
    if (entries.length >= maxEntries) break;
  }
  return entries.length ? entries.map((entry) => `- ${entry}`).join("\n") : "无。";
}

function compactRecentSummaryWindow(text, keep = 3) {
  const clean = text.trim();
  if (!clean) return "";
  const lines = clean.split(/\r?\n/);
  const blocks = [];
  let current = [];
  const chapterHeading = /^(?:[-*]\s*)?第\s*\d+\s*章\s*[：:].*$/;
  for (const line of lines) {
    if (chapterHeading.test(line.trim())) {
      if (current.length) blocks.push(current.join("\n").trim());
      current = [line];
    } else if (current.length) {
      current.push(line);
    }
  }
  if (current.length) blocks.push(current.join("\n").trim());
  if (blocks.length) return blocks.slice(-keep).join("\n");
  return clean.split(/\n\s*\n/).filter(Boolean).slice(-keep).join("\n\n");
}

function buildCanonMemoryStatus(proposed) {
  const chapterNumber = currentChapterNumber();
  const oldStatus = $("section-status").value;
  const previousSummaries = existingCanonSection(oldStatus, "## RECENT SUMMARIES", "最近章节摘要");
  const summaries = compactRecentSummaryWindow([
    previousSummaries,
    `第${chapterNumber}章：${proposed.chapter_summary}`,
  ].filter(Boolean).join("\n"));
  const authorNotes = existingAuthorNotes(oldStatus);
  return [
    `当前已完成第${chapterNumber}章。`,
    "## ACTIVE SCENE STATE",
    proposed.active_scene_state,
    "## PERSISTENT CANON",
    proposed.persistent_canon,
    "## RECENT SUMMARIES",
    summaries,
    "## OPEN PROMISES",
    compactPromiseWindow(proposed.open_promises),
    "## AUTHOR NOTES",
    authorNotes,
  ].join("\n\n").trim();
}

function applyCanonIndexProposal() {
  const v2 = extractStateDeltaV2($("state-delta-response").value);
  if (v2?.error) {
    showStatus(v2.error, true);
    return;
  }
  if (v2) {
    $("section-status").value = buildCanonMemoryStatus(v2);
    markEditorDirty("section-status");
    renderMemoryWorkspace();
    saveRunResponseForMode("state_delta", $("state-delta-response").value);
    showStatus("Canon Memory v2 已应用到浏览器 BOOK 状态编辑区，尚未写盘；确认后请点“保存 BOOK.md”");
    return;
  }
  const proposed = extractProposedCanonIndex($("state-delta-response").value);
  if (!proposed) {
    showStatus("模型返回缺少 `# Proposed Canon Index` 一级标题或内容为空，未修改 BOOK 状态编辑区", true);
    return;
  }
  // 旧版路径曾使用 $("section-status").value = proposed; v2 缺标题时现在明确拒绝。
  showStatus("旧版 Proposed Canon Index 不能应用；State Delta 必须同时提供 v2 的四个 Proposed 标题，未修改 BOOK 状态编辑区，尚未写盘", true);
}

async function saveBook() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  try {
    await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/book`, {
      method: "PUT",
      body: JSON.stringify({ content: composeBookContent() }),
    });
    await refreshWorkflow();
    clearEditorDirty([
      ...Object.keys(designTitles).map((key) => `design-${key}`),
      "section-long_plan", "section-small_plan", "section-status",
    ]);
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
                world_vision: "",
    power_seed: "",
    human_seed: "",
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
    clearEditorDirty([...document.querySelectorAll(".template-editor textarea")].map((element) => element.id));
    showStatus("PROMPTS.md 已保存");
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function saveProposal() {
  await saveCreativeArtifact("proposal");
}

async function approveChapter() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  const chapterBody = $("chapter-body-for-save").value.trim();
  if (!chapterBody) {
    return showStatus("请先从 Codex 返回文本提取正式正文，再保存章节", true);
  }
  try {
    const chapterNumber = Number($("chapter-number").value);
    const existing = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/chapters/${chapterNumber}`);
    const payload = await requestJson(
      `/api/books/${encodeURIComponent(state.bookId)}/chapters${existing.content ? `/${chapterNumber}` : ""}`,
      {
        method: existing.content ? "PUT" : "POST",
        body: existing.content
          ? JSON.stringify({ content: chapterBody })
          : JSON.stringify({ chapter_number: chapterNumber, content: chapterBody }),
      },
    );
    await refreshPreviousChapterText();
    await refreshWorkflow();
    clearEditorDirty(["chapter-body-for-save", "chapter-fact-summary"]);
    showStatus(`${payload.file} 已保存`);
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function loadCurrentChapterBody() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  const chapterNumber = currentChapterNumber();
  try {
    const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/chapters/${chapterNumber}`);
    $("chapter-body-for-save").value = payload.content || "";
    showStatus(payload.content ? `已加载第${chapterNumber}章正式正文，可编辑后保存` : `第${chapterNumber}章尚未保存`);
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
    await refreshExecutorStatus();
    await loadOpenAISettings();
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
$("settings-button").addEventListener("click", async () => {
  await loadOpenAISettings();
  $("settings-dialog").showModal();
});
$("close-settings").addEventListener("click", () => $("settings-dialog").close());
$("save-settings").addEventListener("click", saveOpenAISettings);
$("default-gbrain-query").addEventListener("click", setDefaultGbrainQuery);
$("query-gbrain").addEventListener("click", queryGbrain);
$("generate-idea-prompt").addEventListener("click", generateIdeaPrompt);
$("generate-world-vision-prompt").addEventListener("click", () => generateCreativePrompt("world_vision"));
$("generate-power-seed-prompt").addEventListener("click", () => generateCreativePrompt("power_seed"));
$("generate-human-seed-prompt").addEventListener("click", () => generateCreativePrompt("human_seed"));
$("human-prototype-selector").addEventListener("change", async () => {
  invalidateGbrainResults("切换 Human Prototype");
  if ($("prompt-mode").value === "human_seed") await setDefaultGbrainQuery();
});
$("generate-story-program-prompt").addEventListener("click", () => generateCreativePrompt("idea"));
$("apply-world-vision-response").addEventListener("click", () => applyCreativeResponse("world_vision"));
$("apply-power-seed-response").addEventListener("click", () => applyCreativeResponse("power_seed"));
$("apply-human-seed-response").addEventListener("click", () => applyCreativeResponse("human_seed"));
$("apply-story-program-response").addEventListener("click", () => applyCreativeResponse("proposal"));
$("save-world-vision").addEventListener("click", () => saveCreativeArtifact("world_vision"));
$("save-power-seed").addEventListener("click", () => saveCreativeArtifact("power_seed"));
$("save-human-seed").addEventListener("click", () => saveCreativeArtifact("human_seed"));
$("approve-world-vision").addEventListener("click", () => approveCreativeArtifact("world_vision"));
$("approve-character").addEventListener("click", approveCharacter);
$("approve-proposal").addEventListener("click", () => approveCreativeArtifact("proposal"));
$("generate-prompt").addEventListener("click", generateCurrentChapterAction);
$("generate-director-prompt").addEventListener("click", () => generateHybridNodePrompt("director"));
$("generate-curator-prompt").addEventListener("click", () => generateHybridNodePrompt("context_curator"));
$("generate-primary-writer-prompt").addEventListener("click", () => generateHybridNodePrompt("primary_writer"));
$("generate-opening-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_opening"));
$("generate-dialogue-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_dialogue"));
$("generate-action-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_action"));
$("generate-emotion-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_emotion"));
$("generate-integrator-prompt").addEventListener("click", () => generateHybridNodePrompt("chapter_integrator"));
$("apply-curator-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "curator-response"));
$("apply-director-response").addEventListener("click", applyDirectorResponse);
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
$("refresh-workflow").addEventListener("click", refreshWorkflow);
$("locate-workflow-artifact").addEventListener("click", locateWorkflowArtifact);
$("copy-codex-task").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText($("codex-task-wrapper").value);
    showStatus("Codex External 任务已复制");
  } catch (error) {
    showStatus("复制 Codex 任务失败，请手动复制", true);
  }
});
$("executor-mode").addEventListener("change", () => {
  renderCodexTaskWrapper($("prompt-mode").value);
  showStatus("Executor Mode：" + $("executor-mode").selectedOptions[0].textContent);
});
$("load-current-chapter-body").addEventListener("click", loadCurrentChapterBody);
$("apply-chapter-prep").addEventListener("click", () => {
  applyResponseToEditor($("codex-response"), $("current-outline"));
  showStatus("Codex 返回已放入当前章小纲，尚未写盘");
});
$("chapter-number").addEventListener("change", () => {
  $("chapter-body-for-save").value = "";
  $("chapter-fact-summary").value = "";
  $("current-chapter-plan").value = "";
  for (const id of [
    "director-response",
    "curator-response", "primary-writer-response", "opening-specialist-response",
    "dialogue-specialist-response", "action-specialist-response",
    "emotion-specialist-response", "integrator-response",
  ]) $(id).value = "";
  invalidateGbrainResults("切换章节");
  refreshPreviousChapterText();
  loadRun();
  updateChapterWorkspace();
});
$("create-run").addEventListener("click", createRun);
$("refresh-run").addEventListener("click", loadRun);
$("activate-repair-specialists").addEventListener("click", activateSelectedRepair);
$("prompt-mode").addEventListener("change", handlePromptModeChange);
$("expand-design").addEventListener("click", () => setDesignDetails(true));
$("collapse-design").addEventListener("click", () => setDesignDetails(false));
$("section-long_plan").addEventListener("input", renderLongPlanPanorama);
  $("section-long_plan").addEventListener("input", () => {
  invalidateGbrainResults("当前中期规划窗口已变化");
});
$("section-small_plan").addEventListener("input", () => {
  $("current-chapter-plan").value = "";
  renderFuture10Cards();
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
  applyCreativeResponse("proposal");
});
$("apply-outline-to-book").addEventListener("click", applyOutlineToBook);
$("extract-chapter-body").addEventListener("click", extractChapterBody);
$("generate-state-delta-prompt").addEventListener("click", generateStateDeltaPrompt);
$("apply-canon-index-proposal").addEventListener("click", applyCanonIndexProposal);
$("save-book").addEventListener("click", saveBook);
$("save-memory").addEventListener("click", saveBook);
$("save-templates").addEventListener("click", saveTemplates);
$("save-proposal").addEventListener("click", saveProposal);
$("approve-chapter").addEventListener("click", approveChapter);
for (const artifact of Object.keys(creativeUi)) {
  $(creativeUi[artifact].editor).addEventListener("input", () => markCreativeEdited(artifact));
}
document.querySelectorAll("[data-creative-edit]").forEach((button) => {
  button.addEventListener("click", () => {
    const stage = button.closest(".creative-stage");
    if (!stage) return;
    stage.open = true;
    stage.classList.add("stage-editing");
  });
});

document.querySelectorAll(".nav-link").forEach((link) => {
  link.addEventListener("click", (event) => {
    const target = link.dataset.viewTarget;
    if (target !== state.view && !confirmDiscardIfNeeded("切换工作区")) event.preventDefault();
  });
});
window.addEventListener("hashchange", () => {
  const next = currentViewFromHash();
  if (next !== state.view && !confirmDiscardIfNeeded("切换工作区")) {
    window.history.replaceState(null, "", `#${state.view}`);
    return;
  }
  setView(next, false);
});

document.addEventListener("input", (event) => {
  const target = event.target;
  if (!(target instanceof HTMLTextAreaElement || target instanceof HTMLInputElement)) return;
  if (dirtyEditorIds().includes(target.id)) markEditorDirty(target.id);
});

document.querySelectorAll("[data-design-tab]").forEach((button) => {
  button.addEventListener("click", () => setDesignTab(button.dataset.designTab));
});
$("toggle-design-editor").addEventListener("click", () => setDesignEditing(!state.designEditing));
$("edit-future10").addEventListener("click", editFuture10);
document.querySelectorAll("[data-chapter-tab]").forEach((button) => {
  button.addEventListener("click", () => setChapterTab(button.dataset.chapterTab));
});
$("toggle-chapter-context").addEventListener("click", () => {
  document.body.classList.toggle("chapter-context-open");
  setChapterTab(state.chapterTab);
});
$("chapter-previous").addEventListener("click", () => {
  if (!confirmDiscardIfNeeded("切换章节")) return;
  const next = Math.max(1, currentChapterNumber() - 1);
  $("chapter-number").value = next;
  $("chapter-number").dispatchEvent(new Event("change"));
  updateChapterWorkspace();
});
$("chapter-next").addEventListener("click", () => {
  if (!confirmDiscardIfNeeded("切换章节")) return;
  $("chapter-number").value = currentChapterNumber() + 1;
  $("chapter-number").dispatchEvent(new Event("change"));
  updateChapterWorkspace();
});
$("continue-chapter").addEventListener("click", () => {
  if (state.workflow?.current_chapter) $("chapter-number").value = state.workflow.current_chapter;
  if (!navigateToView("chapter", "继续写作")) return;
  prepareChapterAction();
  updateChapterWorkspace();
});
$("overview-open-workflow").addEventListener("click", openRightDrawer);
$("memory-open-workflow").addEventListener("click", openRightDrawer);
$("open-workflow-drawer").addEventListener("click", openRightDrawer);
$("open-workflow-from-tools").addEventListener("click", openRightDrawer);
$("open-executor-drawer").addEventListener("click", () => {
  setChapterTab("execution");
  openRightDrawer();
});
$("open-prompt-drawer").addEventListener("click", openRightDrawer);
$("close-right-drawer").addEventListener("click", closeRightDrawer);
$("close-workflow-drawer").addEventListener("click", closeRightDrawer);
document.querySelectorAll("[data-close-drawer]").forEach((element) => element.addEventListener("click", closeRightDrawer));
$("open-memory-editor").addEventListener("click", openMemoryEditor);
$("open-prompt-templates").addEventListener("click", openPromptTemplates);
$("open-settings-from-tools").addEventListener("click", () => $("settings-button").click());
$("open-references").addEventListener("click", () => {
  navigateToView("creative", "打开 References");
  const section = document.querySelector(".references-section");
  if (section) {
    section.open = true;
    section.scrollIntoView({ behavior: "smooth", block: "center" });
  }
});

mountRightDrawer();
initializeReadingState();
setView(currentViewFromHash(), false);
setDesignEditing(false);
renderDirtyState();
initialize();
