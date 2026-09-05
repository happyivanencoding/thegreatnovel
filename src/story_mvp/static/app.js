const state = {
  bookId: "",
  references: [],
  currentRun: null,
  creativeState: {},
  creativeArtifacts: {},
  creativeSources: {},
  premise: {},
  premiseCompilerScope: "candidates",
  workflow: null,
  view: "overview",
  designTab: "overall",
  chapterTab: "outline",
  designEditing: false,
  dirtyEditors: new Set(),
  gbrainDefaultBrief: "",
  gbrainStatus: null,
  gbrainRetrieval: null,
  gbrainSelected: new Set(),
  gbrainBundleSignature: "",
  gbrainBundleOrigin: "empty",
  gbrainBundleProgrammatic: false,
  gbrainContextSnapshot: null,
  gbrainStale: false,
  gbrainStaleReason: "",
  gbrainQuerying: false,
  agentdockJobs: [],
  agentdockAvailable: false,
  agentdockFocusedJob: null,
  agentdockNotifiedJobs: new Set(),
  agentdockPhaseSeen: new Map(),
  agentdockReminderSeen: new Map(),
  agentdockPollers: new Set(),
  agentdockLatestLaunch: new Map(),
  agentdockPendingJobs: new Map(),
  agentdockLaunchSnapshots: new Map(),
  agentdockEditorVersions: new Map(),
  agentdockPreviewJob: null,
  productionRuns: [],
  batch: {
    preflight: null,
    adopted: null,
    continuityText: "",
    primaryPromptWindow: "",
    deltaPromptWindow: "",
    deltaPromptPrimary: "",
    window: { startChapter: 1, batchSize: 5 },
  },
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
const GBRAIN_ACTIVE_MODES = new Set(["world_vision", "world_expansion", "power_seed", "human_seed", "idea", "story_refresh", "outline"]);
const GBRAIN_MODE_LABELS = {
  world_vision: "World Vision",
  world_expansion: "World Expansion",
  power_seed: "Power Seed",
  human_seed: "Human Seed",
  idea: "Story Program",
  story_refresh: "Story Refresh",
  outline: "Outline",
};

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
  const saveState = $("topbar-save-status");
  if (saveState) saveState.textContent = count ? `未保存编辑 ${count} 项` : "所有写入均需作者确认";
}

function setView(view, updateHash = true) {
  if (!viewNames.has(view)) view = "overview";
  state.view = view;
  document.querySelectorAll(".workspace-view").forEach((element) => {
    element.hidden = element.dataset.view !== view;
  });
  document.querySelectorAll(".nav-link").forEach((link) => {
    const active = link.dataset.viewTarget === view;
    link.classList.toggle("active", active);
    if (active) link.setAttribute("aria-current", "page"); else link.removeAttribute("aria-current");
  });
  document.querySelectorAll("[data-top-view]").forEach((button) => {
    const active = button.dataset.topView === view;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  document.body.dataset.view = view;
  if (view !== "memory") document.body.classList.remove("memory-editor-open");
  if (updateHash && window.location.hash !== `#${view}`) window.location.hash = view;
  if (view === "chapter") {
    if (["premise_forge", "premise_compiler", "world_vision", "power_seed", "human_seed", "idea", "outline", "review"].includes($("prompt-mode")?.value)) {
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
  if ($("batch-start-chapter") && !batchProductionHasContent()) {
    $("batch-start-chapter").value = chapter;
    state.batch.window = {
      startChapter: chapter,
      batchSize: Number($("batch-size")?.value || 5),
    };
  }
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
  const activeProductionRun = state.productionRuns.find((run) => ["queued", "running"].includes(run.status));
  const latestProductionRun = state.productionRuns[0];
  $("overview-book").textContent = book;
  $("overview-book-path").textContent = book === "未加载" ? "请从上方加载小说" : "本地工作区已连接";
  $("overview-chapter").textContent = snapshot ? `第 ${chapter} 章` : "—";
  $("overview-chapter-state").textContent = snapshot ? (artifacts[`chapter.${chapter}.body`]?.status || "正文未载入") : "—";
  $("overview-next").textContent = activeProductionRun
    ? productionRunStatusLabel(activeProductionRun.status)
    : (latestProductionRun?.status === "completed" ? "最近自动任务已完成" : "等待 Automatic Production Run");
  $("overview-next-detail").textContent = activeProductionRun?.label
    || latestProductionRun?.label
    || "从 ChatGPT 给出方向与目标章数；中间 checkpoint 自动处理";
  $("overview-stale").textContent = snapshot ? `${stale} 项 stale` : "—";
  $("overview-stale-detail").textContent = stale ? "高级区可查看依赖影响；自动任务会按原 runner 逻辑处理" : "暂无需要处理的 stale";
  $("continue-chapter").textContent = snapshot ? `查看第 ${chapter} 章` : "查看当前章节";
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
    stage.open = false;
    const summary = stage.querySelector("summary");
    if (!summary || summary.dataset.readingBound) return;
    summary.dataset.readingBound = "true";
    summary.addEventListener("click", () => {
      window.setTimeout(() => stage.classList.toggle("stage-editing", stage.open), 0);
    });
  });
  document.querySelectorAll(".design-card").forEach((card) => { card.open = true; });
}

const workflowStages = [
  { title: "大胆前提（可选）", keys: ["premise.contract"] },
  { title: "创意", keys: ["creative.world_vision", "creative.power_seed", "creative.human_seed", "creative.character_card", "creative.story_program"] },
  { title: "长篇演化", keys: ["evolution.world", "evolution.human_development", "evolution.current_character"] },
  { title: "设计", keys: ["book.design"] },
  { title: "规划", keys: ["book.long_plan", "book.future_10"] },
  { title: "当前章节", keys: [] },
  { title: "记忆", keys: ["book.canon_state"] },
];

const workflowLabels = {
  "premise.contract": "大胆前提合同",
  "creative.world_vision": "世界幻想",
  "creative.power_seed": "力量种子",
  "creative.human_seed": "人物种子",
  "creative.character_card": "人物权威",
  "creative.story_program": "故事方案",
  "evolution.world": "向前世界拓展",
  "evolution.human_development": "人物长期发展",
  "evolution.current_character": "当前人物权威",
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
  authority_reviser: { mode: "authority_reviser", title: "Authority 二次修订", button: "生成二次修订", tab: "body" },
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
    "premise.contract": "PREMISE_CONTRACT.md",
    "creative.world_vision": "WORLD_VISION.md",
    "creative.power_seed": "POWER_SEED.md",
    "creative.human_seed": "HUMAN_SEED.md",
    "creative.character_card": "CHARACTER.md",
    "creative.story_program": "PROPOSAL.md",
    "evolution.world": "world_expansions/expansion-NNNN.md",
    "evolution.human_development": "human_development/delta-NNNN.md",
    "evolution.current_character": "CURRENT_CHARACTER.md",
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
  renderStoryStructure(snapshot);
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
    "evolution.world": "evolution-world-history",
    "evolution.human_development": "evolution-human-history",
    "evolution.current_character": "evolution-current-character",
    "book.design": "design-sections",
    "book.long_plan": "section-long_plan",
    "book.future_10": "section-small_plan",
    "book.canon_state": "section-status",
  };
  const target = $(targets[selectedWorkflowArtifact] || "prompt-panel");
  if (selectedWorkflowArtifact.startsWith("creative.") || selectedWorkflowArtifact.startsWith("evolution.")) navigateToView("creative", "定位创意节点");
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
    renderAgentDockStatus(executors.agentdock_acp || {});
    await refreshAgentDockJobs();
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
    renderAgentDockStatus(executors.agentdock_acp || {});
  } catch (error) {
    $("openai-executor-status").textContent = "OpenAI API：读取失败";
  }
}

function renderStoryStructure(snapshot) {
  const tree = $("story-structure-tree");
  if (!tree) return;
  tree.replaceChildren();
  const artifacts = snapshot?.artifacts || {};
  const appendArtifact = (label, artifact, view, tab = "") => {
    const button = document.createElement("button");
    button.type = "button";
    const entry = artifacts[artifact] || {};
    button.className = "story-tree-item";
    button.textContent = `${label} · ${entry.status || "EMPTY"}`;
    button.addEventListener("click", () => {
      if (artifact in artifacts) showWorkflowArtifact(artifact);
      navigateToView(view, `定位${label}`);
      if (tab === "future10") setDesignTab("future10");
      if (tab === "midterm") setDesignTab("midterm");
      openRightDrawer();
    });
    tree.appendChild(button);
  };
  appendArtifact("World Vision", "creative.world_vision", "creative");
  appendArtifact("Power / Human / Character", "creative.character_card", "creative");
  appendArtifact("Story Program", "creative.story_program", "creative");
  const gbrainButton = document.createElement("button");
  gbrainButton.type = "button";
  gbrainButton.className = "story-tree-item story-tree-utility";
  gbrainButton.textContent = `GBrain 灵感实验室 · ${state.gbrainStatus?.available ? "READY" : "CHECK"}`;
  gbrainButton.addEventListener("click", () => {
    if (!navigateToView("creative", "打开 GBrain 灵感实验室")) return;
    const studio = $("gbrain-details");
    if (studio) {
      studio.open = true;
      studio.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
  tree.appendChild(gbrainButton);
  appendArtifact("当前 Long Plan", "book.long_plan", "design", "midterm");
  const future = parseFuture10Entries($("section-small_plan")?.value || "");
  const futureGroup = document.createElement("div");
  futureGroup.className = "story-tree-group";
  futureGroup.textContent = `Future-10 · ${future.length} 章`;
  tree.appendChild(futureGroup);
  for (const entry of future.slice(0, 10)) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "story-tree-item story-tree-child";
    button.textContent = `第${entry.number}章 · ${entry.title}`;
    button.addEventListener("click", () => {
      $("chapter-number").value = entry.number;
      navigateToView("chapter", "进入 Future-10 章节");
      setChapterTab("outline");
      loadCurrentChapterPlan();
    });
    tree.appendChild(button);
  }
  appendArtifact(`当前章 · ${snapshot?.current_chapter || currentChapterNumber()}`, `chapter.${snapshot?.current_chapter || currentChapterNumber()}.body`, "chapter");
  appendArtifact("Canon Memory", "book.canon_state", "memory");
  appendArtifact("Run / Archive", `chapter.${snapshot?.current_chapter || currentChapterNumber()}.run`, "chapter");
}

function renderAgentDockStatus(executor) {
  const status = $("agentdock-executor-status");
  if (!status) return;
  const available = Boolean(executor.available);
  state.agentdockAvailable = available;
  status.textContent = available
    ? `AgentDock ACP：入口可用 · ChatGPT 登录将在启动时确认 · ${executor.mode || "read-only"} · 活跃 ${executor.active_count || 0}`
    : "AgentDock ACP：本机不可用";
  const models = $("agentdock-model");
  const efforts = $("agentdock-effort");
  if (models && executor.models?.length && !models.options.length) {
    for (const model of executor.models) {
      const option = document.createElement("option");
      option.value = model;
      option.textContent = model;
      option.selected = model === executor.default_model;
      models.appendChild(option);
    }
  }
  if (efforts && executor.reasoning_efforts?.length && !efforts.options.length) {
    for (const effort of executor.reasoning_efforts) {
      const option = document.createElement("option");
      option.value = effort;
      option.textContent = effort;
      option.selected = effort === executor.default_reasoning_effort;
      efforts.appendChild(option);
    }
  }
  syncAgentDockPendingButtons();
}

const AGENT_PHASES = [
  ["queued", "排队"],
  ["connecting", "连接"],
  ["configuring", "配置"],
  ["planning", "理解"],
  ["working", "工作"],
  ["composing", "输出"],
  ["finalizing", "收尾"],
  ["completed", "完成"],
];
const BASE_DOCUMENT_TITLE = document.title;
let agentDockTitleResetTimer = null;
let agentDockMiniResetTimer = null;

function formatAgentDuration(seconds) {
  const value = Math.max(0, Math.floor(Number(seconds) || 0));
  const hours = Math.floor(value / 3600);
  const minutes = Math.floor((value % 3600) / 60);
  const remainder = value % 60;
  return hours
    ? `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(remainder).padStart(2, "0")}`
    : `${String(minutes).padStart(2, "0")}:${String(remainder).padStart(2, "0")}`;
}

function agentHeartbeatText(job) {
  const quiet = Math.max(0, Math.round(Number(job.activity_quiet_seconds) || 0));
  if (!["queued", "running"].includes(job.status)) {
    return job.status === "completed" ? "输出已安全返回，等待作者确认" : "本任务已经停止";
  }
  if (job.status === "queued") return "正在等待可用的 Agent 执行位";
  if (quiet < 6) return "刚刚收到新的运行信号";
  if (quiet < 30) return `最近活动 ${quiet} 秒前 · Agent 仍在运行`;
  if (quiet < 90) return `正在处理较长步骤 · 最近可见活动 ${quiet} 秒前`;
  return `仍保持运行连接 · 长推理可能暂时没有工具事件 · 最近信号 ${quiet} 秒前`;
}

const AGENT_LONG_RUN_REMINDERS = [60, 180, 300, 600, 900, 1200, 1800, 2700];

function maybeShowAgentLongRunReminder(job) {
  if (!job || !["queued", "running"].includes(job.status)) return;
  const elapsed = Math.max(0, Math.floor(Number(job.elapsed_seconds) || 0));
  const reached = AGENT_LONG_RUN_REMINDERS.filter((threshold) => elapsed >= threshold).at(-1) || 0;
  const previous = Number(state.agentdockReminderSeen.get(job.job_id) || 0);
  if (!reached || reached <= previous) return;
  state.agentdockReminderSeen.set(job.job_id, reached);
  showAgentDockNotice(
    `仍在运行 · 已用时 ${formatAgentDuration(elapsed)}。${agentHeartbeatText(job)}；可以继续写别处，也可随时取消。`,
    "progress",
  );
}

function showAgentDockNotice(message, tone = "info") {
  const notice = $("agentdock-notice");
  if (!notice) return;
  notice.hidden = !message;
  notice.className = `agentdock-notice agentdock-notice-${tone}`;
  notice.textContent = message;
}

function updateDocumentRunState(job) {
  window.clearTimeout(agentDockTitleResetTimer);
  if (job && ["queued", "running"].includes(job.status)) {
    document.title = `● ${job.phase_label || "Agent 运行中"} · ${BASE_DOCUMENT_TITLE}`;
    return;
  }
  if (job?.status === "completed") {
    document.title = `✓ ${job.context_label || "Agent 完成"} · ${BASE_DOCUMENT_TITLE}`;
    agentDockTitleResetTimer = window.setTimeout(() => { document.title = BASE_DOCUMENT_TITLE; }, 8000);
    return;
  }
  document.title = BASE_DOCUMENT_TITLE;
}

function renderAgentDockFocus(job) {
  const panel = $("agentdock-progress-anchor");
  if (!panel) return;
  if (!job) {
    panel.hidden = true;
    if ($("agentdock-mini-anchor")) $("agentdock-mini-anchor").hidden = true;
    updateDocumentRunState(null);
    return;
  }
  const previousPhase = state.agentdockPhaseSeen.get(job.job_id);
  state.agentdockFocusedJob = { ...job, _receivedAt: Date.now() };
  state.agentdockPhaseSeen.set(job.job_id, job.phase);
  if (previousPhase && previousPhase !== job.phase && ["queued", "running"].includes(job.status)) {
    showAgentDockNotice(`进度更新 · ${job.phase_label || job.phase}：${job.current_activity || "Agent 正在工作"}`, "progress");
  }
  panel.hidden = false;
  panel.dataset.status = job.status;
  $("agentdock-progress-context").textContent = job.context_label || job.purpose || "Agent 任务";
  $("agentdock-progress-phase").textContent = job.phase_label || job.phase || job.status;
  $("agentdock-progress-elapsed").textContent = formatAgentDuration(job.elapsed_seconds);
  $("agentdock-current-activity").textContent = job.current_activity || "Agent 正在工作";
  $("agentdock-heartbeat").textContent = agentHeartbeatText(job);
  $("agentdock-signal-metric").textContent = `${Math.max(0, Math.round(Number(job.activity_quiet_seconds) || 0))}s`;
  $("agentdock-plan-metric").textContent = job.plan_total ? `${job.plan_completed || 0}/${job.plan_total}` : "—";
  const tools = job.tool_counts || {};
  $("agentdock-tool-metric").textContent = tools.total || 0;
  $("agentdock-activity-count").textContent = job.activity_count || job.activities?.length || 0;

  const track = $("agentdock-phase-track");
  track.replaceChildren();
  const phaseIndex = Number.isInteger(job.phase_index) ? job.phase_index : 0;
  AGENT_PHASES.forEach(([key, label], index) => {
    const step = document.createElement("span");
    step.className = index < phaseIndex ? "is-complete" : index === phaseIndex ? "is-current" : "";
    if (["failed", "cancelled"].includes(job.status) && index === phaseIndex) step.classList.add("is-stopped");
    step.dataset.phase = key;
    step.textContent = label;
    track.appendChild(step);
  });

  const plan = $("agentdock-plan-list");
  plan.replaceChildren();
  for (const entry of job.plan_entries || []) {
    const item = document.createElement("li");
    item.dataset.status = entry.status || "pending";
    const mark = document.createElement("span");
    mark.setAttribute("aria-hidden", "true");
    mark.textContent = entry.status === "completed" ? "✓" : entry.status === "in_progress" ? "●" : entry.status === "failed" ? "!" : "○";
    const content = document.createElement("span");
    content.textContent = entry.content;
    item.append(mark, content);
    plan.appendChild(item);
  }
  plan.hidden = !(job.plan_entries || []).length;

  const activities = $("agentdock-activity-list");
  activities.replaceChildren();
  for (const activity of (job.activities || []).slice(-10).reverse()) {
    const item = document.createElement("li");
    const time = document.createElement("time");
    time.textContent = `+${formatAgentDuration(activity.elapsed_seconds)}`;
    const content = document.createElement("div");
    const title = document.createElement("strong");
    title.textContent = activity.label;
    content.appendChild(title);
    if (activity.detail) {
      const detail = document.createElement("span");
      detail.textContent = activity.detail;
      content.appendChild(detail);
    }
    item.append(time, content);
    activities.appendChild(item);
  }
  if (!activities.children.length) {
    const empty = document.createElement("li");
    empty.className = "is-empty";
    empty.textContent = "等待第一条可见活动";
    activities.appendChild(empty);
  }
  $("agentdock-active-cancel").disabled = !["queued", "running"].includes(job.status);
  const mini = $("agentdock-mini-anchor");
  if (mini) {
    window.clearTimeout(agentDockMiniResetTimer);
    mini.hidden = false;
    mini.dataset.status = job.status;
    $("agentdock-mini-phase").textContent = job.status === "completed" ? "Agent 已完成" : job.phase_label || "Agent 运行中";
    $("agentdock-mini-activity").textContent = job.current_activity || "查看实时活动";
    $("agentdock-mini-elapsed").textContent = formatAgentDuration(job.elapsed_seconds);
    if (!["queued", "running"].includes(job.status)) {
      agentDockMiniResetTimer = window.setTimeout(() => { mini.hidden = true; }, 12000);
    }
  }
  updateDocumentRunState(job);
}

function refreshAgentDockFocusClock() {
  const job = state.agentdockFocusedJob;
  if (!job || !["queued", "running"].includes(job.status)) return;
  const delta = Math.max(0, (Date.now() - Number(job._receivedAt || Date.now())) / 1000);
  const liveJob = {
    ...job,
    elapsed_seconds: Number(job.elapsed_seconds || 0) + delta,
    activity_quiet_seconds: Number(job.activity_quiet_seconds || 0) + delta,
  };
  if ($("agentdock-progress-elapsed")) $("agentdock-progress-elapsed").textContent = formatAgentDuration(liveJob.elapsed_seconds);
  if ($("agentdock-heartbeat")) $("agentdock-heartbeat").textContent = agentHeartbeatText(liveJob);
  if ($("agentdock-signal-metric")) $("agentdock-signal-metric").textContent = `${Math.max(0, Math.round(liveJob.activity_quiet_seconds))}s`;
  if ($("agentdock-mini-elapsed")) $("agentdock-mini-elapsed").textContent = formatAgentDuration(liveJob.elapsed_seconds);
  if ($("agentdock-mini-activity")) {
    $("agentdock-mini-activity").textContent = liveJob.activity_quiet_seconds >= 20
      ? agentHeartbeatText(liveJob)
      : liveJob.current_activity || agentHeartbeatText(liveJob);
  }
  maybeShowAgentLongRunReminder(liveJob);
}

function selectAgentDockFocus(jobs) {
  const focusedId = state.agentdockFocusedJob?.job_id;
  const focused = jobs.find((job) => job.job_id === focusedId && ["queued", "running"].includes(job.status));
  const active = focused || jobs.find((job) => job.status === "running") || jobs.find((job) => job.status === "queued");
  if (active) {
    const existing = state.agentdockFocusedJob?.job_id === active.job_id ? state.agentdockFocusedJob : null;
    renderAgentDockFocus(existing?.activities?.length && !active.activities
      ? { ...existing, ...active, activities: existing.activities }
      : active);
    return;
  }
  if (!state.agentdockFocusedJob) renderAgentDockFocus(null);
}

function renderAgentDockJobs(jobs) {
  state.agentdockJobs = jobs;
  const container = $("agentdock-job-list");
  const active = $("agentdock-active-status");
  if (!container) return;
  container.replaceChildren();
  const activeCount = jobs.filter((job) => ["queued", "running"].includes(job.status)).length;
  if (active) active.textContent = activeCount ? `${activeCount} 个作业运行中` : "无运行作业";
  selectAgentDockFocus(jobs);
  if (!jobs.length) {
    const empty = document.createElement("p");
    empty.className = "hint agentdock-empty-state";
    empty.textContent = "还没有运行记录。启动后，这里会保留本次服务会话中的真实作业。";
    container.appendChild(empty);
    return;
  }
  for (const job of jobs.slice(0, 12)) {
    const card = document.createElement("article");
    card.className = `agentdock-job agentdock-job-${job.status}`;
    card.tabIndex = 0;
    card.setAttribute("role", "button");
    card.setAttribute("aria-label", `查看 ${job.context_label || job.purpose} 的运行详情`);
    const heading = document.createElement("div");
    heading.className = "agentdock-job-heading";
    const title = document.createElement("strong");
    title.textContent = job.context_label || job.purpose;
    const badge = document.createElement("span");
    badge.className = "agentdock-job-badge";
    badge.textContent = job.phase_label || job.status;
    heading.append(title, badge);
    const detail = document.createElement("span");
    detail.className = "agentdock-job-detail";
    detail.textContent = job.current_activity || `${job.model || "—"} · ${job.reasoning_effort || "—"}`;
    const meta = document.createElement("small");
    meta.textContent = `${job.model || "—"} · ${job.reasoning_effort || "—"} · ${formatAgentDuration(job.elapsed_seconds)}`;
    const actions = document.createElement("div");
    actions.className = "agentdock-job-actions";
    if (["queued", "running"].includes(job.status)) {
      const cancel = document.createElement("button");
      cancel.type = "button";
      cancel.textContent = "取消";
      cancel.addEventListener("click", (event) => { event.stopPropagation(); cancelAgentDockJob(job.job_id); });
      actions.appendChild(cancel);
    }
    if (job.has_output) {
      const view = document.createElement("button");
      view.type = "button";
      view.textContent = "查看结果";
      view.addEventListener("click", (event) => { event.stopPropagation(); viewAgentDockJob(job.job_id); });
      actions.appendChild(view);
    }
    const openProgress = () => {
      if (["queued", "running"].includes(job.status)) {
        requestJson(`/api/executors/agentdock/jobs/${encodeURIComponent(job.job_id)}`, { timeoutMs: 20_000 })
          .then((full) => renderAgentDockFocus(full))
          .catch((error) => showStatus(`读取 Agent 活动失败：${error.message}`, true));
      } else if (job.has_output) {
        viewAgentDockJob(job.job_id);
      }
    };
    card.addEventListener("click", openProgress);
    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") { event.preventDefault(); openProgress(); }
    });
    if (job.error) detail.textContent = `失败：${job.error}`;
    card.append(heading, detail, meta, actions);
    container.appendChild(card);
  }
}

function agentDockButtonsForTarget(target) {
  return {
    workflow_response: ["agentdock-run-current"],
    state_delta: ["agentdock-run-current", "generate-state-delta-prompt"],
    consultation: ["agentdock-run-consult"],
    batch_primary: ["batch-run-primary"],
    batch_delta: ["batch-run-delta"],
  }[target] || [];
}

function syncAgentDockPendingButtons() {
  const activeTargets = new Set(
    [...state.agentdockPendingJobs.values()]
      .filter((entry) => entry.bookId === state.bookId)
      .map((entry) => entry.target),
  );
  for (const target of ["workflow_response", "state_delta", "consultation", "batch_primary", "batch_delta"]) {
    const pending = activeTargets.has(target);
    for (const id of agentDockButtonsForTarget(target)) {
      if ($(id)) $(id).disabled = !state.agentdockAvailable || pending;
    }
  }
}

function trackAgentDockPending(jobKey, job, pending) {
  const previous = state.agentdockPendingJobs.get(jobKey) || null;
  if (pending) {
    state.agentdockPendingJobs.set(jobKey, {
      target: responseTargetForJob(job),
      bookId: job.book_id || state.bookId,
      launchToken: job.launch_token || "",
    });
  } else {
    state.agentdockPendingJobs.delete(jobKey);
  }
  syncAgentDockPendingButtons();
  return previous;
}

async function refreshAgentDockJobs() {
  if (!state.bookId) {
    syncAgentDockPendingButtons();
    return renderAgentDockJobs([]);
  }
  try {
    const payload = await requestJson(`/api/executors/agentdock/jobs?book_id=${encodeURIComponent(state.bookId)}`, { timeoutMs: 20_000 });
    const jobs = payload.jobs || [];
    const activeJobs = jobs.filter((job) => ["queued", "running"].includes(job.status));
    const activeIds = new Set(activeJobs.map((job) => job.job_id));
    for (const [jobKey, entry] of state.agentdockPendingJobs.entries()) {
      if (entry.bookId === state.bookId && !jobKey.startsWith("launch:") && !activeIds.has(jobKey)) {
        state.agentdockPendingJobs.delete(jobKey);
      }
    }
    for (const job of activeJobs) {
      const target = responseTargetForJob(job);
      if (!state.agentdockLatestLaunch.has(target)) state.agentdockLatestLaunch.set(target, job.launch_token);
      trackAgentDockPending(job.job_id, job, true);
      pollAgentDockJob(job.job_id);
    }
    syncAgentDockPendingButtons();
    renderAgentDockJobs(jobs);
  } catch (error) {
    syncAgentDockPendingButtons();
    renderAgentDockJobs(state.agentdockJobs || []);
    showAgentDockNotice("暂时无法刷新作业列表；已有运行任务仍保持锁定，系统会继续等待状态恢复。", "progress");
  }
}

function responseTargetForJob(job) {
  if (job.purpose === "consultation") return "consultation";
  if (job.purpose === "batch_primary") return "batch_primary";
  if (job.purpose === "batch_authority_reviser") return "batch_delta";
  if (job.workflow_mode === "state_delta") return "state_delta";
  return "workflow_response";
}

function currentIdentity() {
  return { book_id: state.bookId, chapter_number: currentChapterNumber(), workflow_mode: $("prompt-mode")?.value || "" };
}

function currentBatchWorkflowMode(purpose) {
  return `${purpose}:${Number($("batch-size")?.value || 5)}`;
}

function currentAgentDockPromptForJob(job) {
  const target = responseTargetForJob(job);
  if (target === "consultation") return $("agentdock-consult-prompt")?.value || "";
  if (target === "batch_primary") return $("batch-primary-prompt")?.value || "";
  if (target === "batch_delta") return $("batch-delta-prompt")?.value || "";
  return $("prompt-text")?.value || "";
}

function agentDockSourceSnapshot(job, prompt = currentAgentDockPromptForJob(job)) {
  const target = responseTargetForJob(job);
  if (target === "consultation") return JSON.stringify({ prompt });
  if (["batch_primary", "batch_delta"].includes(target)) {
    return JSON.stringify({ prompt, window: batchWindowKey(), inputs: batchPayload() });
  }
  return JSON.stringify({ prompt, inputs: promptPayload() });
}

function jobMatchesCurrentIdentity(job) {
  if (job.purpose === "consultation") return job.book_id === state.bookId;
  if (job.purpose === "batch_primary" || job.purpose === "batch_authority_reviser") {
    return job.book_id === state.bookId
      && job.chapter_number === Number($("batch-start-chapter")?.value || 0)
      && job.workflow_mode === currentBatchWorkflowMode(job.purpose);
  }
  if (job.workflow_mode === "state_delta") {
    return job.book_id === state.bookId && job.chapter_number === currentChapterNumber();
  }
  const current = currentIdentity();
  return job.book_id === current.book_id && job.chapter_number === current.chapter_number && job.workflow_mode === current.workflow_mode;
}

function responseEditorForJob(job) {
  const target = responseTargetForJob(job);
  if (target === "consultation") return $("agentdock-consult-response");
  if (target === "batch_primary") return $("batch-primary-response");
  if (target === "batch_delta") return $("batch-delta-response");
  if (target === "state_delta") return $("state-delta-response");
  return $("codex-response");
}

function agentDockEditorVersion(editor) {
  return Number(state.agentdockEditorVersions.get(editor?.id || "") || 0);
}

function markAgentDockEditorEdited(editor) {
  if (!editor?.id) return;
  state.agentdockEditorVersions.set(editor.id, agentDockEditorVersion(editor) + 1);
}

function canAutoFillAgentDockJob(job) {
  const target = responseTargetForJob(job);
  const snapshot = state.agentdockLaunchSnapshots.get(job.launch_token);
  const editor = responseEditorForJob(job);
  return Boolean(
    snapshot
    && editor
    && state.agentdockLatestLaunch.get(target) === job.launch_token
    && jobMatchesCurrentIdentity(job)
    && snapshot.target === target
    && snapshot.bookId === job.book_id
    && snapshot.chapterNumber === job.chapter_number
    && snapshot.workflowMode === job.workflow_mode
    && snapshot.prompt === currentAgentDockPromptForJob(job)
    && snapshot.sourceSnapshot === agentDockSourceSnapshot(job)
    && editor.value === snapshot.initialValue
    && agentDockEditorVersion(editor) === snapshot.editorVersion
  );
}

async function startAgentDockJob(prompt, { mode = "", purpose = "consultation", contextLabel = "", model = "", reasoningEffort = "" } = {}) {
  const identity = { book_id: state.bookId, chapter_number: purpose === "consultation" ? 0 : currentChapterNumber(), workflow_mode: mode };
  if (purpose === "batch_primary" || purpose === "batch_authority_reviser") {
    identity.chapter_number = Number($("batch-start-chapter").value);
    identity.workflow_mode = currentBatchWorkflowMode(purpose);
  }
  const jobIdentity = { purpose, ...identity };
  const target = responseTargetForJob(jobIdentity);
  const launchToken = `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
  const temporaryKey = `launch:${launchToken}`;
  const editor = responseEditorForJob(jobIdentity);
  const sourceSnapshot = agentDockSourceSnapshot(jobIdentity, prompt);
  state.agentdockLatestLaunch.set(target, launchToken);
  state.agentdockLaunchSnapshots.set(launchToken, {
    target,
    bookId: identity.book_id,
    chapterNumber: identity.chapter_number,
    workflowMode: identity.workflow_mode,
    prompt,
    sourceSnapshot,
    initialValue: editor?.value || "",
    editorVersion: agentDockEditorVersion(editor),
  });
  trackAgentDockPending(temporaryKey, { ...jobIdentity, launch_token: launchToken }, true);
  try {
    const payload = await requestJson("/api/executors/agentdock/jobs", {
      method: "POST",
      timeoutMs: 30_000,
      body: JSON.stringify({
        prompt,
        model: model || $("agentdock-model")?.value || "",
        reasoning_effort: reasoningEffort || $("agentdock-effort")?.value || "",
        purpose,
        context_label: contextLabel || mode || "临时咨询",
        ...identity,
        launch_token: launchToken,
      }),
    });
    trackAgentDockPending(temporaryKey, jobIdentity, false);
    trackAgentDockPending(payload.job_id, { ...jobIdentity, launch_token: launchToken }, true);
    renderAgentDockFocus(payload);
    showAgentDockNotice(`已启动 · ${contextLabel || mode || "Agent 任务"}。右侧会持续显示真实活动。`, "progress");
    openRightDrawer();
    $("agentdock-progress-anchor")?.scrollIntoView({ behavior: "smooth", block: "start" });
    await refreshAgentDockJobs();
    pollAgentDockJob(payload.job_id);
    return payload;
  } catch (error) {
    trackAgentDockPending(temporaryKey, jobIdentity, false);
    state.agentdockLaunchSnapshots.delete(launchToken);
    if (state.agentdockLatestLaunch.get(target) === launchToken) state.agentdockLatestLaunch.delete(target);
    throw error;
  }
}

async function pollAgentDockJob(jobId) {
  if (state.agentdockPollers.has(jobId)) return;
  state.agentdockPollers.add(jobId);
  let consecutiveStatusErrors = 0;
  try {
    while (true) {
      let job;
      try {
        job = await requestJson(`/api/executors/agentdock/jobs/${encodeURIComponent(jobId)}`, { timeoutMs: 20_000 });
        consecutiveStatusErrors = 0;
      } catch (error) {
        const lost = error.status === 404 || error.payload?.detail?.code === "not_found";
        if (lost) {
          const pending = trackAgentDockPending(jobId, {}, false);
          if (pending?.launchToken) state.agentdockLaunchSnapshots.delete(pending.launchToken);
          showStatus("AgentDock 作业状态已丢失（服务可能已重启）；未写入任何 Response。", true);
          break;
        }
        consecutiveStatusErrors += 1;
        showAgentDockNotice(
          `暂时无法读取 Agent 状态（第 ${consecutiveStatusErrors} 次）；任务仍保持锁定，将自动重试。`,
          "progress",
        );
        await new Promise((resolve) => window.setTimeout(resolve, Math.min(10_000, 1500 * consecutiveStatusErrors)));
        continue;
      }
      renderAgentDockFocus(job);
      if (["queued", "running"].includes(job.status)) {
        await new Promise((resolve) => window.setTimeout(resolve, 1400));
        continue;
      }
      const target = responseTargetForJob(job);
      trackAgentDockPending(jobId, job, false);
      if (job.status === "completed") {
        if (canAutoFillAgentDockJob(job)) {
          responseEditorForJob(job).value = job.output_text || "";
          if (target === "batch_primary") invalidateBatchPrimaryDependents();
          if (target === "batch_delta") invalidateBatchPreflight();
          showStatus(job.purpose === "consultation" ? "AgentDock 临时咨询已完成；结果没有写入小说或工作流。" : "AgentDock 已返回匹配的 Response；仍需作者明确 Apply / Save / Approve。 ");
        } else {
          showStatus("AgentDock 结果待查看：页面已刷新、作者已编辑目标区域，或当前小说/章节/节点不匹配，因此未覆盖编辑区。 ");
        }
        if (!state.agentdockNotifiedJobs.has(job.job_id)) {
          state.agentdockNotifiedJobs.add(job.job_id);
          showAgentDockNotice(`任务完成 · ${job.context_label || job.purpose}。结果仍需作者确认。`, "success");
        }
      } else if (job.status === "failed") {
        showStatus(`AgentDock 失败：${job.error || "未返回详情"}`, true);
        showAgentDockNotice(`任务失败 · ${job.error || "未返回详情"}。没有写入任何内容。`, "error");
      } else if (job.status === "cancelled") {
        showStatus("AgentDock 作业已取消；没有写入 Response。 ");
        showAgentDockNotice("任务已取消，没有写入任何内容。", "quiet");
      }
      state.agentdockLaunchSnapshots.delete(job.launch_token);
      await refreshAgentDockJobs();
      break;
    }
  } finally {
    state.agentdockPollers.delete(jobId);
  }
}

async function cancelAgentDockJob(jobId) {
  try {
    await requestJson(`/api/executors/agentdock/jobs/${encodeURIComponent(jobId)}`, { method: "DELETE", timeoutMs: 20_000 });
    await refreshAgentDockJobs();
    showStatus("已请求取消 AgentDock 作业");
  } catch (error) {
    showStatus(`取消 AgentDock 作业失败：${error.message}`, true);
  }
}

async function viewAgentDockJob(jobId) {
  try {
    const job = await requestJson(`/api/executors/agentdock/jobs/${encodeURIComponent(jobId)}`, { timeoutMs: 20_000 });
    state.agentdockPreviewJob = job;
    $("agentdock-result-preview").value = job.output_text || "";
    const matches = jobMatchesCurrentIdentity(job);
    $("agentdock-preview-status").textContent = matches
      ? "身份匹配：作者可显式载入当前 Response；旧版本也不会自动覆盖。" : "身份不匹配：只读预览，不能覆盖当前 Response。";
    $("agentdock-load-current").disabled = !matches;
  } catch (error) {
    return showStatus(`读取 AgentDock 结果失败：${error.message}`, true);
  }
  openRightDrawer();
}

function loadAgentDockPreview() {
  const job = state.agentdockPreviewJob;
  if (!job || !jobMatchesCurrentIdentity(job)) {
    return showStatus("该结果不匹配当前小说、章节、节点或 Batch 窗口，不能载入。", true);
  }
  if (!window.confirm("确认将这份 AgentDock 结果载入当前 Response？这不会保存、采用或批准。")) return;
  const target = responseTargetForJob(job);
  const editor = responseEditorForJob(job);
  markAgentDockEditorEdited(editor);
  editor.value = job.output_text || "";
  if (target === "batch_primary") invalidateBatchPrimaryDependents();
  if (target === "batch_delta") invalidateBatchPreflight();
  showStatus("结果已载入当前 Response；尚未保存、采用或批准。 ");
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

function productionRunStatusLabel(status) {
  return ({ queued: "等待开始", running: "后台运行中", completed: "已完成", failed: "失败", cancelled: "已取消" })[status] || status || "未知";
}

function renderProductionRuns() {
  const target = $("production-run-list");
  if (!target) return;
  target.replaceChildren();
  if (!state.productionRuns.length) {
    const empty = document.createElement("p");
    empty.className = "hint";
    empty.textContent = "暂无后台 Production Run。你从 ChatGPT 发起的持久长任务会显示在这里。";
    target.appendChild(empty);
    return;
  }
  for (const run of state.productionRuns.slice(0, 8)) {
    const card = document.createElement("article");
    card.className = "overview-card";
    const label = document.createElement("span");
    label.textContent = run.label || "Production Run";
    const status = document.createElement("strong");
    status.textContent = productionRunStatusLabel(run.status);
    const detail = document.createElement("small");
    detail.textContent = run.status === "failed" && run.error
      ? run.error
      : (run.finished_at || run.started_at || run.created_at || "");
    card.append(label, status, detail);
    if (["queued", "running"].includes(run.status)) {
      const cancel = document.createElement("button");
      cancel.type = "button";
      cancel.textContent = "取消";
      cancel.addEventListener("click", async () => {
        try {
          await requestJson(`/api/production-runs/${encodeURIComponent(run.job_id)}`, { method: "DELETE" });
          await refreshProductionRuns();
        } catch (error) {
          showStatus(`取消后台任务失败：${error.message}`, true);
        }
      });
      card.appendChild(cancel);
    }
    target.appendChild(card);
  }
}

async function refreshProductionRuns() {
  try {
    const payload = await requestJson("/api/production-runs", { timeoutMs: 10_000 });
    state.productionRuns = Array.isArray(payload.runs) ? payload.runs : [];
    renderProductionRuns();
    renderOverview(state.workflow);
  } catch (error) {
    const target = $("production-run-list");
    if (target) target.textContent = `后台任务状态暂时不可读：${error.message}`;
  }
}

function renderCreativeMeta(artifact) {
  const ui = creativeUi[artifact];
  const value = state.creativeArtifacts[artifact] || state.creativeState[artifact] || {};
  const target = $(ui.meta);
  if (!target) return;
  const displayStatus = value.status === "author_approved" ? "frozen" : (value.status || "empty");
  target.textContent = `${value.origin || "empty"} · ${displayStatus}`;
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
  setPremisePayload(payload?.premise || {});
  setEvolutionPayload(payload || {});
}

function setPremisePayload(premise) {
  state.premise = premise || {};
  const frozenByWorld = state.creativeState?.world_vision?.status === "author_approved";
  $("premise-candidates").value = premise?.candidates || "";
  $("selected-premise").value = premise?.selected || "";
  $("premise-compiler-report").value = premise?.compiler_report || "";
  $("premise-candidates").readOnly = frozenByWorld;
  $("selected-premise").readOnly = frozenByWorld;
  $("premise-compiler-report").readOnly = frozenByWorld;
  const contracts = premise?.contracts || {};
  $("premise-world-contract").value = contracts.world || "";
  $("premise-power-contract").value = contracts.power || "";
  $("premise-human-contract").value = contracts.human || "";
  $("premise-story-contract").value = contracts.story || "";
  const status = premise?.status || "not_started";
  const selected = premise?.selected_id ? ` · ${premise.selected_id}` : "";
  const verdict = premise?.selected_verdict ? ` · ${premise.selected_verdict}` : "";
  $("premise-status").textContent = `${status}${selected}${verdict}`;
  const previewSource = premise?.selected || premise?.candidates || "";
  const compact = previewSource.trim().replace(/\s+/g, " ");
  $("premise-preview").textContent = compact
    ? (compact.length > 280 ? `${compact.slice(0, 280)}…` : compact)
    : status === "skipped"
      ? "作者已显式跳过；当前书使用原 Split Authority 开书路径。"
      : "尚未开始；可直接跳过，或先生成三张完整大胆候选。";
  for (const id of (
    [
      "generate-premise-forge-prompt",
      "apply-premise-forge-response",
      "save-premise-candidates",
      "generate-premise-batch-compiler",
      "save-selected-premise",
      "generate-selected-premise-compiler",
      "apply-premise-compiler-response",
      "save-premise-compiler",
    ]
  )) {
    $(id).disabled = frozenByWorld;
  }
  document.querySelectorAll("[data-premise-select]").forEach((button) => {
    button.disabled = frozenByWorld;
  });
  $("approve-premise").disabled = frozenByWorld || !premise?.can_approve || Boolean(premise?.approved);
  $("skip-premise").disabled = frozenByWorld || Boolean(premise?.approved);
}

function extractPremiseCandidate(candidateId) {
  const text = $("premise-candidates").value;
  const headings = [...text.matchAll(/^## (S[1-9])(?:｜[^\n]*)?\s*$/gm)];
  const index = headings.findIndex((match) => match[1] === candidateId);
  if (index < 0) return "";
  const start = headings[index].index;
  const end = index + 1 < headings.length ? headings[index + 1].index : text.length;
  return text.slice(start, end).trim();
}

async function savePremiseCandidates() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  try {
    const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/premise/candidates`, {
      method: "PUT",
      body: JSON.stringify({ content: $("premise-candidates").value }),
    });
    setPremisePayload(payload);
    clearEditorDirty(["premise-candidates", "selected-premise", "premise-compiler-report"]);
    await refreshWorkflow();
    showStatus("三张 Premise 候选已保存；仍为 Non-Canon");
    return true;
  } catch (error) {
    showStatus(error.message, true);
    return false;
  }
}

function choosePremiseCandidate(candidateId) {
  const candidate = extractPremiseCandidate(candidateId);
  if (!candidate) return showStatus(`候选中没有找到 ${candidateId}`, true);
  $("selected-premise").value = candidate;
  markEditorDirty("selected-premise");
  showStatus(`${candidateId} 已放入作者选择区；可编辑，但编辑后必须单卡复编`);
}

async function saveSelectedPremise() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  try {
    const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/premise/selected`, {
      method: "PUT",
      body: JSON.stringify({ content: $("selected-premise").value }),
    });
    setPremisePayload(payload);
    clearEditorDirty(["selected-premise"]);
    await refreshWorkflow();
    showStatus("Selected Premise 已保存；模型没有替作者选择");
    return true;
  } catch (error) {
    showStatus(error.message, true);
    return false;
  }
}

async function savePremiseCompilerReport() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  try {
    const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/premise/compiler`, {
      method: "PUT",
      body: JSON.stringify({ content: $("premise-compiler-report").value }),
    });
    setPremisePayload(payload);
    clearEditorDirty(["premise-compiler-report"]);
    await refreshWorkflow();
    showStatus(payload.can_approve
      ? "Compiler Report 已保存：所选卡 strict PASS，可由作者批准"
      : "Compiler Report 已保存；CONDITIONAL PASS / FAIL 不会自动选择或修复");
    return true;
  } catch (error) {
    showStatus(error.message, true);
    return false;
  }
}

async function generatePremiseForgePrompt() {
  state.premiseCompilerScope = "candidates";
  await generateCreativePrompt("premise_forge");
}

async function generatePremiseCompilerPrompt(scope) {
  const saved = scope === "selected" ? await saveSelectedPremise() : await savePremiseCandidates();
  if (!saved) return;
  state.premiseCompilerScope = scope;
  await generateCreativePrompt("premise_compiler");
}

function applyPremiseResponse(targetId, label) {
  applyResponseToEditor($("codex-response"), $(targetId));
  markEditorDirty(targetId);
  showStatus(`${label} 已放入编辑区；模型返回尚未保存或批准`);
}

async function approvePremiseContract() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  try {
    const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/premise/approve`, {
      method: "POST",
    });
    setPremisePayload(payload);
    await refreshWorkflow();
    showStatus("Premise 已批准并确定性拆为 World / Power / Human / Story 四条冻结合同");
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function skipPremiseAperture() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  if (!window.confirm("显式跳过会清除未批准 Premise 候选与 Compiler 结果，并继续原 Split Authority 路径。继续吗？")) return;
  try {
    const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/premise/skip`, {
      method: "POST",
    });
    setPremisePayload(payload);
    clearEditorDirty(["premise-candidates", "selected-premise", "premise-compiler-report"]);
    await refreshWorkflow();
    showStatus("作者已显式跳过 Premise Aperture");
  } catch (error) {
    showStatus(error.message, true);
  }
}

function setEvolutionPayload(payload) {
  if ($("evolution-world-handoff")) $("evolution-world-handoff").value = payload?.world_horizon_handoff || "";
  if ($("evolution-world-history")) $("evolution-world-history").value = payload?.world_expansions || "";
  if ($("evolution-human-history")) $("evolution-human-history").value = payload?.human_development || "";
  if ($("evolution-current-character")) $("evolution-current-character").value = payload?.current_character || "";
}

async function refreshEvolutionPayload() {
  if (!state.bookId) return;
  const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/evolution`);
  setEvolutionPayload(payload);
  if (payload.workflow) renderWorkflow(payload.workflow);
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

function applyEvolutionResponse(kind) {
  const target = kind === "world" ? $("evolution-world-candidate") : $("evolution-human-candidate");
  applyResponseToEditor($("codex-response"), target);
  showStatus(`${kind === "world" ? "World Expansion" : "Human Development"} 模型返回已放入候选区；尚未成为 Authority`);
}

async function approveWorldExpansion() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  const content = $("evolution-world-candidate").value.trim();
  if (!content) return showStatus("World Expansion 候选为空", true);
  try {
    await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/world-expansions/approve`, {
      method: "POST",
      body: JSON.stringify({
        content,
        scope: $("evolution-world-scope").value,
        effective_from: Number($("evolution-world-from").value),
        effective_until: Number($("evolution-world-until").value || 0),
      }),
    });
    $("evolution-world-candidate").value = "";
    await refreshEvolutionPayload();
    showStatus("World Expansion 已批准为 forward-only Authority；Origin Power/Human 未被重写，未来 Story/Outline 已 stale");
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function approveHumanDevelopment() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  const content = $("evolution-human-candidate").value.trim();
  if (!content) return showStatus("Human Development 候选为空；没有稳定变化时模型应明确返回 NONE", true);
  try {
    const result = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/human-development/approve`, {
      method: "POST",
      body: JSON.stringify({ content }),
    });
    $("evolution-human-candidate").value = "";
    await refreshEvolutionPayload();
    showStatus(result.status === "no_change"
      ? "Human Development = NONE：没有制造人格变化"
      : "Human Development 已批准；请刷新 Current Character 后再做 Story Refresh");
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function refreshCurrentCharacter() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  try {
    const result = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/current-character/refresh`, {
      method: "POST",
    });
    $("evolution-current-character").value = result.content || "";
    await refreshWorkflow();
    showStatus(`Current Character 已确定性刷新到第${result.compiled_through}章；未调用 LLM`);
  } catch (error) {
    showStatus(error.message, true);
  }
}

function applyStoryRefreshResponse() {
  applyCreativeResponse("proposal");
  $("proposal-editor")?.scrollIntoView({ behavior: "smooth", block: "center" });
  showStatus("Story Refresh 已放入 Story Program 编辑器；请阅读/编辑后走现有保存与批准流程");
}

const runNodeByMode = {
  chapter: "primary",
  director: "director",
  context_curator: "curator",
  primary_writer: "primary",
  authority_reviser: "authority_reviser",
  specialist_opening: "opening",
  specialist_dialogue: "dialogue",
  specialist_action: "action",
  specialist_emotion: "emotion",
  chapter_integrator: "integrator",
  state_delta: "state_delta",
};

const runResponseEditorByMode = {
  chapter: "primary-writer-response",
  context_curator: "curator-response",
  primary_writer: "primary-writer-response",
  authority_reviser: "authority-reviser-response",
  specialist_opening: "opening-specialist-response",
  specialist_dialogue: "dialogue-specialist-response",
  specialist_action: "action-specialist-response",
  specialist_emotion: "emotion-specialist-response",
  chapter_integrator: "integrator-response",
  state_delta: "state-delta-response",
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
    const adoptable = manifest.writer_mode === "curator_primary"
      ? ["authority_reviser", "integrator"]
      : ["primary", "integrator"];
    if (["completed", "adopted"].includes(info.status) && adoptable.includes(node)) {
      const adopt = document.createElement("button");
      const label = node === "authority_reviser" ? "Authority Revision" : node === "primary" ? "Primary" : "Integrator";
      adopt.textContent = `采用${label}`;
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
  if (!node || !state.currentRun || !prompt.trim()) return null;
  try {
    const manifest = await requestJson(`${runBaseUrl()}/nodes/${node}/prompt`, {
      method: "PUT",
      body: JSON.stringify({ content: prompt }),
    });
    renderRunLedger(manifest);
    await refreshWorkflow();
    return manifest;
  } catch (error) {
    showStatus(`保存 ${node} Prompt 到 Run 失败：${error.message}`, true);
    return null;
  }
}

function hydrateDirectorResponseEditors(response) {
  if (!response.trim()) return false;
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
  if (fieldLabels.size !== 8) return false;
  $("current-outline").value = lines.join("\n");
  return true;
}

async function hydrateReceiptReusedResponse(mode, node) {
  const payload = await requestJson(`${runBaseUrl()}/nodes/${node}/response`);
  const response = payload.content || "";
  if (!response.trim()) throw new Error(`${node} receipt 指向的 Response 为空`);
  $("codex-response").value = response;
  if (mode === "director") {
    if (!hydrateDirectorResponseEditors(response)) {
      throw new Error("复用的 Director Response 不含完整八字段");
    }
  } else {
    const editorId = runResponseEditorByMode[mode];
    if (editorId && $(editorId)) $(editorId).value = response;
  }
  $("codex-task-wrapper-panel").hidden = true;
  $("codex-task-wrapper").value = "";
}

async function saveRunResponseForMode(mode, response) {
  const node = runNodeByMode[mode];
  if (!node || !state.currentRun || !response.trim()) return null;
  try {
    const manifest = await requestJson(`${runBaseUrl()}/nodes/${node}/response`, {
      method: "PUT",
      body: JSON.stringify({ content: response }),
    });
    renderRunLedger(manifest);
    await refreshWorkflow();
    return manifest;
  } catch (error) {
    showStatus(`保存 ${node} Response 到 Run 失败：${error.message}`, true);
    return null;
  }
}

async function retryRunNode(node) {
  try {
    const manifest = await requestJson(`${runBaseUrl()}/nodes/${node}/retry`, { method: "POST" });
    renderRunLedger(manifest);
    await refreshWorkflow();
    const info = manifest.nodes?.[node] || {};
    if (node === "authority_reviser" && info.repair_reason) {
      const saved = await requestJson(`${runBaseUrl()}/nodes/${node}/prompt`);
      $("prompt-text").value = saved.content || "";
      renderCodexTaskWrapper("authority_reviser");
      if (currentExecutorMode() === "openai_api" && saved.content?.trim()) {
        await executeOpenAI(saved.content, "authority_reviser");
        showStatus("显式里程碑 Outcome Repair 已执行；请检查并 Apply 返回。最多只允许这一次条件性重试。");
      } else if (currentExecutorMode() === "agentdock_acp" && saved.content?.trim()) {
        const profile = agentDockExecutionProfile("authority_reviser");
        await startAgentDockJob(saved.content, {
          mode: "authority_reviser",
          purpose: "workflow_response",
          contextLabel: "Authority Delta 重试",
          model: profile.model,
          reasoningEffort: profile.reasoningEffort,
        });
        showStatus("Authority Delta 重试已交给 AgentDock；完成后仍需作者检查与 Apply。 ");
      } else {
        showStatus("已加载显式里程碑 Outcome Repair Prompt；这是一次性窄修复，不会重跑普通 Reviser。 ");
      }
      return;
    }
    showStatus(`${node} 已按当前保存 Prompt 准备重试`);
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

function gbrainModeAllowsRetrieval(mode = $("prompt-mode")?.value || "") {
  return GBRAIN_ACTIVE_MODES.has(mode);
}

function currentGbrainContextSnapshot() {
  const payload = gbrainContextPayload();
  return {
    book_id: state.bookId,
    chapter_number: currentChapterNumber(),
    mode: payload.mode,
    query: $("gbrain-query")?.value || "",
    book_content: payload.book_content,
    creative_direction: payload.creative_direction,
    world_vision: payload.world_vision,
    prototype_id: payload.prototype_id,
    character_card: payload.character_card,
    proposal_context: payload.proposal_context,
    current_long_block: payload.current_long_block,
    current_outline: payload.current_outline,
    recent_summaries: payload.recent_summaries,
  };
}

function gbrainContextSnapshotMatches() {
  if (!state.gbrainContextSnapshot) return true;
  return JSON.stringify(state.gbrainContextSnapshot) === JSON.stringify(currentGbrainContextSnapshot());
}

function gbrainHasMaterial() {
  return Boolean(state.gbrainRetrieval || $("gbrain-results")?.value.trim());
}

function resetGbrainCandidateView({ clearBundle = false } = {}) {
  if ($("gbrain-compare-dialog")?.open) $("gbrain-compare-dialog").close();
  state.gbrainRetrieval = null;
  state.gbrainSelected = new Set();
  state.gbrainBundleSignature = "";
  state.gbrainContextSnapshot = null;
  state.gbrainStale = false;
  state.gbrainStaleReason = "";
  if (clearBundle) {
    state.gbrainBundleProgrammatic = true;
    $("gbrain-results").value = "";
    state.gbrainBundleProgrammatic = false;
    state.gbrainBundleOrigin = "empty";
    $("gbrain-raw-results").value = "";
    $("gbrain-rejections").value = "";
    $("gbrain-count").textContent = "raw 0 / accepted 0 / rejected 0";
  } else if (!$("gbrain-results")?.value.trim()) {
    state.gbrainBundleOrigin = "empty";
  }
  const fixed = $("gbrain-fixed-list");
  const candidates = $("gbrain-candidate-list");
  const tray = $("gbrain-selection-tray");
  if (fixed) fixed.replaceChildren();
  if (tray) tray.replaceChildren();
  if (candidates) {
    candidates.replaceChildren();
    const empty = document.createElement("p");
    empty.className = "gbrain-empty";
    empty.textContent = "检索后，这里会显示经过 BOOK 兼容性筛选的可迁移抽象。";
    candidates.appendChild(empty);
  }
  if ($("gbrain-selection-count")) $("gbrain-selection-count").textContent = "尚未检索";
  renderGbrainBundleState();
  renderGbrainStaleState();
}

function clearGbrainWorkspace(reason = "", { quiet = false } = {}) {
  resetGbrainCandidateView({ clearBundle: true });
  $("gbrain-status").textContent = reason ? `GBrain：${reason}` : "GBrain：本轮不注入";
  $("gbrain-status").classList.remove("error");
  renderGbrainModeState();
  if (reason && !quiet) showStatus(`GBrain 已清空：${reason}`);
}

function renderGbrainStaleState() {
  const studio = $("gbrain-details");
  const banner = $("gbrain-stale-banner");
  const active = gbrainModeAllowsRetrieval();
  const stale = Boolean(state.gbrainStale && gbrainHasMaterial());
  if (studio) {
    studio.classList.toggle("is-stale", stale);
    studio.classList.toggle("is-off", !active);
    studio.classList.toggle("is-querying", state.gbrainQuerying);
  }
  if (banner) banner.hidden = !stale;
  if ($("gbrain-stale-reason")) {
    $("gbrain-stale-reason").textContent = state.gbrainStaleReason || "当前 BOOK、章节或规划输入已经变化。";
  }
  if ($("gbrain-requery")) $("gbrain-requery").disabled = !active || state.gbrainQuerying;
  document.querySelectorAll(".gbrain-candidate-card input[type='checkbox']").forEach((checkbox) => {
    checkbox.disabled = !active || stale || state.gbrainQuerying;
  });
}

function invalidateGbrainResults(reason = "上下文已变化") {
  if (!gbrainHasMaterial()) return;
  if ($("gbrain-compare-dialog")?.open) $("gbrain-compare-dialog").close();
  const firstTransition = !state.gbrainStale;
  state.gbrainStale = true;
  state.gbrainStaleReason = reason;
  $("gbrain-status").textContent = "GBrain：旧材料已保留，但不会进入 Prompt";
  $("gbrain-status").classList.remove("error");
  renderGbrainBundleState();
  renderGbrainModeState();
  if (firstTransition) showStatus(`GBrain 材料已标记为旧上下文：${reason}。请重新检索后再使用。`);
}

function setGbrainQueryPending(pending) {
  state.gbrainQuerying = pending;
  for (const id of ["default-gbrain-query", "query-gbrain"]) {
    if ($(id)) $(id).disabled = pending || !gbrainModeAllowsRetrieval();
  }
  if ($("gbrain-query")) $("gbrain-query").disabled = pending || !gbrainModeAllowsRetrieval();
  if ($("query-gbrain")) $("query-gbrain").textContent = pending ? "正在检索与抽取…" : "检索并抽取";
  if (state.gbrainRetrieval) updateGbrainSelectionState(false);
  renderGbrainStaleState();
}

function renderGbrainModeState() {
  const mode = $("prompt-mode")?.value || "";
  const active = gbrainModeAllowsRetrieval(mode);
  const badge = $("gbrain-mode-badge");
  const readiness = $("gbrain-readiness");
  if (badge) {
    badge.textContent = active ? `${GBRAIN_MODE_LABELS[mode] || mode} · ON` : `${mode || "当前阶段"} · OFF`;
    badge.classList.toggle("is-off", !active);
  }
  if (readiness) {
    if (!active) {
      readiness.textContent = gbrainHasMaterial()
        ? "本阶段 GBrain 固定 OFF · 旧材料只读保留，不会注入"
        : "本阶段按 production 规则不接收 raw GBrain";
      readiness.dataset.state = "off";
    } else if (!state.gbrainStatus) {
      readiness.textContent = "正在检查 GBrain CLI 与 embedding…";
      readiness.dataset.state = "checking";
    } else if (state.gbrainStatus.available) {
      readiness.textContent = "检索环境就绪 · embedding ON · Optional Inspiration";
      readiness.dataset.state = "ready";
    } else {
      const missing = [
        !state.gbrainStatus.cli_available ? "GBrain CLI" : "",
        !state.gbrainStatus.embedding_ready ? "embedding 凭据" : "",
      ].filter(Boolean).join(" + ");
      readiness.textContent = `${missing || "检索环境"}未就绪；GBrain ON 阶段将 fail loud`;
      readiness.dataset.state = "error";
    }
  }
  if ($("generate-idea-prompt")) {
    $("generate-idea-prompt").disabled = !active;
    $("generate-idea-prompt").textContent = active
      ? `使用当前 Bundle 生成 ${GBRAIN_MODE_LABELS[mode] || mode} Prompt`
      : "当前阶段不注入 GBrain";
  }
  setGbrainQueryPending(state.gbrainQuerying);
  updateGbrainSelectionState(false);
  renderGbrainStaleState();
}

async function refreshGbrainStatus() {
  try {
    state.gbrainStatus = await requestJson("/api/gbrain/status");
  } catch (error) {
    state.gbrainStatus = { available: false, cli_available: false, embedding_ready: false };
  }
  renderGbrainModeState();
}

function gbrainSelectionSignature() {
  const payload = state.gbrainRetrieval || {};
  return JSON.stringify({
    mode: payload.mode || $("prompt-mode")?.value || "",
    effective_query: payload.effective_query || "",
    fixed: (payload.fixed_references || []).map((item) => item.id || item.slug),
    selected: [...state.gbrainSelected].sort(),
  });
}

function selectedGbrainCandidates() {
  return (state.gbrainRetrieval?.accepted || []).filter((item) => state.gbrainSelected.has(item.slug));
}

function renderGbrainSelectionTray(selected) {
  const tray = $("gbrain-selection-tray");
  if (!tray) return;
  tray.replaceChildren();
  if (!state.gbrainRetrieval) return;
  if (!selected.length) {
    const empty = document.createElement("span");
    empty.className = "gbrain-selection-empty";
    empty.textContent = "尚未选择候选；可以只使用固定参考，也可以完全不注入。";
    tray.appendChild(empty);
    return;
  }
  for (const candidate of selected) {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "gbrain-selection-chip";
    chip.dataset.slug = candidate.slug;
    chip.title = `移除 ${candidate.slug}`;
    chip.textContent = `${candidate.human_lane ? `${candidate.human_lane} · ` : ""}${candidate.abstract.split(/[。；\n]/)[0].slice(0, 26)}`;
    chip.addEventListener("click", () => {
      state.gbrainSelected.delete(candidate.slug);
      const checkbox = document.querySelector(`.gbrain-candidate-card[data-slug="${CSS.escape(candidate.slug)}"] input[type="checkbox"]`);
      if (checkbox) checkbox.checked = false;
      updateGbrainSelectionState(true);
    });
    tray.appendChild(chip);
  }
}

function renderGbrainBundleState() {
  const target = $("gbrain-bundle-state");
  if (!target) return;
  target.className = "";
  if (state.gbrainStale && gbrainHasMaterial()) {
    target.textContent = "旧上下文 · 当前 Bundle 不会进入 Prompt";
    target.className = "is-stale";
    return;
  }
  const selectedCount = selectedGbrainCandidates().length;
  const fixedCount = state.gbrainRetrieval?.fixed_references?.length || 0;
  if (state.gbrainBundleOrigin === "assembled") {
    target.textContent = `已组装 · ${selectedCount} 条候选 + ${fixedCount} 条固定参考`;
    target.className = "is-ready";
  } else if (state.gbrainBundleOrigin === "manual") {
    target.textContent = "作者已编辑当前组装 Bundle";
    target.className = "is-manual";
  } else if (state.gbrainBundleOrigin === "unbound_manual") {
    target.textContent = "未绑定当前检索 · 不会进入 Prompt";
    target.className = "is-stale";
  } else if (state.gbrainBundleOrigin === "selection_stale") {
    target.textContent = "选择已变化 · 旧 Bundle 已保留，请重新组装";
    target.className = "is-stale";
  } else if (state.gbrainBundleOrigin === "previous") {
    target.textContent = "上一轮 Bundle 已保留 · 当前候选尚未组装";
    target.className = "is-stale";
  } else {
    target.textContent = state.gbrainRetrieval ? "候选已抽取 · 请显式选择后组装" : "尚未组装";
  }
}

function updateGbrainSelectionState(markBundleStale = true) {
  const retrieval = state.gbrainRetrieval;
  const selected = selectedGbrainCandidates();
  const fixedCount = retrieval?.fixed_references?.length || 0;
  if ($("gbrain-selection-count")) {
    $("gbrain-selection-count").textContent = retrieval
      ? `已选 ${selected.length}/${retrieval.accepted?.length || 0} · 固定参考 ${fixedCount}`
      : "尚未检索";
  }
  document.querySelectorAll(".gbrain-candidate-card").forEach((card) => {
    const checked = state.gbrainSelected.has(card.dataset.slug);
    card.classList.toggle("is-selected", checked);
    const checkbox = card.querySelector('input[type="checkbox"]');
    if (checkbox) checkbox.checked = checked;
  });
  renderGbrainSelectionTray(selected);
  const active = gbrainModeAllowsRetrieval();
  const usable = active && retrieval && !state.gbrainStale && !state.gbrainQuerying;
  const hasBundleParts = selected.length > 0 || fixedCount > 0;
  if ($("gbrain-assemble")) $("gbrain-assemble").disabled = !usable || !hasBundleParts;
  if ($("gbrain-select-all")) $("gbrain-select-all").disabled = !usable || !(retrieval.accepted || []).length;
  if ($("gbrain-clear-selection")) $("gbrain-clear-selection").disabled = !usable || !selected.length;
  if ($("gbrain-compare")) $("gbrain-compare").disabled = !usable || selected.length < 2;
  if ($("gbrain-discard")) $("gbrain-discard").disabled = !gbrainHasMaterial();
  if (markBundleStale) {
    if (["assembled", "manual"].includes(state.gbrainBundleOrigin)
        && state.gbrainBundleSignature !== gbrainSelectionSignature()) {
      state.gbrainBundleOrigin = "selection_stale";
    }
  }
  renderGbrainBundleState();
  renderGbrainStaleState();
}

function renderGbrainFixedReferences(references) {
  const container = $("gbrain-fixed-list");
  if (!container) return;
  container.replaceChildren();
  for (const reference of references || []) {
    const card = document.createElement("article");
    card.className = "gbrain-fixed-card";
    const mark = document.createElement("span");
    mark.textContent = "◆";
    mark.setAttribute("aria-hidden", "true");
    const body = document.createElement("div");
    const title = document.createElement("strong");
    title.textContent = reference.label || "固定 Reference";
    const meta = document.createElement("small");
    meta.textContent = `${reference.slug} · 不占候选名额 · 使用 Bundle 时必须保留`;
    body.append(title, meta);
    card.append(mark, body);
    container.appendChild(card);
  }
}

function createGbrainCandidateCard(candidate, index) {
  const card = document.createElement("article");
  card.className = "gbrain-candidate-card";
  card.dataset.slug = candidate.slug;
  const selector = document.createElement("label");
  selector.className = "gbrain-candidate-selector";
  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = false;
  checkbox.setAttribute("aria-label", `选择 ${candidate.slug}`);
  checkbox.addEventListener("change", () => {
    if (checkbox.checked) state.gbrainSelected.add(candidate.slug); else state.gbrainSelected.delete(candidate.slug);
    updateGbrainSelectionState(true);
  });
  const indexMark = document.createElement("span");
  indexMark.className = "gbrain-candidate-index";
  indexMark.textContent = String(index + 1).padStart(2, "0");
  selector.append(checkbox, indexMark);
  const body = document.createElement("div");
  body.className = "gbrain-candidate-body";
  const header = document.createElement("div");
  header.className = "gbrain-candidate-header";
  const title = document.createElement("strong");
  title.textContent = candidate.abstract.split(/[。；\n]/)[0].slice(0, 44) || candidate.slug;
  const chips = document.createElement("div");
  for (const label of [candidate.type, candidate.human_lane, candidate.is_genre_prior ? "genre prior" : ""].filter(Boolean)) {
    const chip = document.createElement("span");
    chip.textContent = label;
    chips.appendChild(chip);
  }
  header.append(title, chips);
  const abstract = document.createElement("p");
  abstract.textContent = candidate.abstract;
  const details = document.createElement("details");
  details.className = "gbrain-candidate-details";
  const summary = document.createElement("summary");
  summary.textContent = `来源与迁移边界 · 相关性 ${Number(candidate.score || 0).toFixed(2)}`;
  const source = document.createElement("code");
  source.textContent = candidate.slug;
  const boundary = document.createElement("p");
  boundary.textContent = candidate.transfer_boundary || "只迁移抽象机制，不迁移来源表层。";
  details.append(summary, source, boundary);
  body.append(header, abstract, details);
  card.append(selector, body);
  return card;
}

function renderGbrainCandidates(payload) {
  const existingBundle = $("gbrain-results").value.trim();
  state.gbrainRetrieval = payload;
  state.gbrainSelected = new Set();
  state.gbrainBundleSignature = "";
  state.gbrainBundleOrigin = existingBundle ? "previous" : "empty";
  renderGbrainFixedReferences(payload.fixed_references || []);
  const container = $("gbrain-candidate-list");
  container.replaceChildren();
  const candidates = payload.accepted || [];
  if (!candidates.length) {
    const empty = document.createElement("p");
    empty.className = "gbrain-empty";
    empty.textContent = "没有通过 BOOK 兼容性筛选的 creative candidate；可以修改 Retrieval Brief 后重试。";
    container.appendChild(empty);
  } else if (payload.mode === "human_seed" && (payload.human_lane_order || []).length) {
    const labels = { appetite: "欲望 Appetite", behavior: "行为 Behavior", relationship: "关系 Relationship" };
    for (const lane of payload.human_lane_order) {
      const section = document.createElement("section");
      section.className = "gbrain-lane-section";
      section.dataset.lane = lane;
      const heading = document.createElement("div");
      heading.className = "gbrain-lane-heading";
      const title = document.createElement("strong");
      title.textContent = labels[lane] || lane;
      const laneCandidates = candidates.filter((candidate) => candidate.human_lane === lane);
      const count = document.createElement("span");
      count.textContent = `${laneCandidates.length} 条`;
      heading.append(title, count);
      section.appendChild(heading);
      if (!laneCandidates.length) {
        const empty = document.createElement("p");
        empty.className = "gbrain-lane-empty";
        empty.textContent = "本轮没有足够可靠的候选；不会为了凑齐而补弱卡。";
        section.appendChild(empty);
      } else {
        laneCandidates.forEach((candidate) => section.appendChild(createGbrainCandidateCard(candidate, candidates.indexOf(candidate))));
      }
      container.appendChild(section);
    }
  } else {
    candidates.forEach((candidate, index) => container.appendChild(createGbrainCandidateCard(candidate, index)));
  }
  updateGbrainSelectionState(false);
}

function renderGbrainCompare() {
  const container = $("gbrain-compare-list");
  if (!container) return;
  container.replaceChildren();
  for (const candidate of selectedGbrainCandidates()) {
    const card = document.createElement("article");
    card.className = "gbrain-compare-card";
    const heading = document.createElement("div");
    const title = document.createElement("strong");
    title.textContent = candidate.abstract.split(/[。；\n]/)[0].slice(0, 52) || candidate.slug;
    const score = document.createElement("span");
    score.textContent = `相关性 ${Number(candidate.score || 0).toFixed(2)}`;
    heading.append(title, score);
    const metadata = document.createElement("dl");
    const rows = [
      ["来源类型", candidate.type || "—"],
      ["Human lane", candidate.human_lane || "—"],
      ["来源", candidate.slug || "—"],
      ["可迁移抽象", candidate.abstract || "—"],
      ["使用边界", candidate.transfer_boundary || "只迁移抽象机制，不迁移来源表层。"],
    ];
    for (const [label, value] of rows) {
      const dt = document.createElement("dt");
      dt.textContent = label;
      const dd = document.createElement("dd");
      dd.textContent = value;
      metadata.append(dt, dd);
    }
    card.append(heading, metadata);
    container.appendChild(card);
  }
}

function openGbrainCompare() {
  if (state.gbrainStale) return showStatus("当前候选基于旧上下文，请先重新检索。", true);
  if (selectedGbrainCandidates().length < 2) return showStatus("至少选择两条候选才能比较。", true);
  renderGbrainCompare();
  $("gbrain-compare-dialog").showModal();
}

function assembleGbrainSelection() {
  const payload = state.gbrainRetrieval;
  if (!payload) return showStatus("请先检索 GBrain", true);
  if (state.gbrainStale || !gbrainContextSnapshotMatches()) {
    invalidateGbrainResults(state.gbrainStaleReason || "当前上下文与检索快照不一致");
    return showStatus("当前候选基于旧上下文，请重新检索。", true);
  }
  const blocks = (payload.fixed_references || []).map((item) => item.formatted_block).filter(Boolean);
  selectedGbrainCandidates().forEach((candidate, index) => {
    const block = String(candidate.formatted_block || "").replace(/^### Inspiration(?:\s+\d+)?/m, `### Inspiration ${index + 1}`);
    if (block) blocks.push(block);
  });
  if (!blocks.length) return showStatus("没有选择任何可组装的 Inspiration", true);
  if ($("gbrain-results").value.trim() && state.gbrainBundleOrigin !== "assembled"
      && !window.confirm("当前 Bundle 已有作者内容。按当前选择重建会覆盖它，继续吗？")) return;
  state.gbrainBundleProgrammatic = true;
  $("gbrain-results").value = blocks.join("\n\n");
  state.gbrainBundleProgrammatic = false;
  state.gbrainBundleOrigin = "assembled";
  state.gbrainBundleSignature = gbrainSelectionSignature();
  renderGbrainBundleState();
  showStatus("所选 GBrain 抽象已组装到可编辑 Bundle；仍不会自动保存或批准。 ");
}

function discardGbrainForCurrentRun() {
  if (gbrainHasMaterial() && !window.confirm("确认本轮不注入 GBrain？候选、诊断和 Bundle 会从当前页面清空。")) return;
  clearGbrainWorkspace("本轮不注入", { quiet: true });
  showStatus("本轮已明确不注入 GBrain；其它规划流程仍可继续。 ");
}

function handleGbrainBundleInput() {
  if (state.gbrainBundleProgrammatic) return;
  const hasText = $("gbrain-results").value.trim();
  if (!hasText) {
    state.gbrainBundleOrigin = "empty";
    state.gbrainBundleSignature = "";
  } else if (!state.gbrainRetrieval) {
    state.gbrainBundleOrigin = "unbound_manual";
    state.gbrainBundleSignature = "";
  } else if (["assembled", "manual"].includes(state.gbrainBundleOrigin)
      && state.gbrainBundleSignature === gbrainSelectionSignature()) {
    state.gbrainBundleOrigin = "manual";
  } else {
    state.gbrainBundleOrigin = "selection_stale";
  }
  renderGbrainBundleState();
}

function validateGbrainBundleForPrompt(mode) {
  if (!GBRAIN_ACTIVE_MODES.has(mode)) return true;
  const bundle = $("gbrain-results").value.trim();
  if (!bundle) return true;
  if (state.gbrainStale || !gbrainContextSnapshotMatches()) {
    invalidateGbrainResults(state.gbrainStaleReason || "当前上下文与检索快照不一致");
    $("gbrain-stale-banner")?.scrollIntoView({ behavior: "smooth", block: "center" });
    return false;
  }
  if (!state.gbrainRetrieval) {
    showStatus("手工文本尚未绑定本轮 GBrain 检索。请先检索并组装，再编辑 Bundle；或明确选择“本轮不注入”。", true);
    $("gbrain-bundle-stage")?.scrollIntoView({ behavior: "smooth", block: "center" });
    return false;
  }
  const requiredReferences = (state.gbrainRetrieval.fixed_references || []).filter((item) => item.required);
  const missingFixed = requiredReferences.filter((item) => !bundle.includes(`source: ${item.slug}`));
  if (missingFixed.length) {
    showStatus(`当前 Bundle 使用了 GBrain，但缺少固定 Reference：${missingFixed.map((item) => item.label || item.slug).join("、")}。请重新组装或明确不注入。`, true);
    $("gbrain-bundle-stage")?.scrollIntoView({ behavior: "smooth", block: "center" });
    return false;
  }
  if (!["assembled", "manual"].includes(state.gbrainBundleOrigin)
      || state.gbrainBundleSignature !== gbrainSelectionSignature()) {
    showStatus("当前 Bundle 与卡片选择不一致。请按当前选择重新组装，或明确选择“本轮不注入”。", true);
    $("gbrain-bundle-stage")?.scrollIntoView({ behavior: "smooth", block: "center" });
    return false;
  }
  return true;
}

function gbrainInspirationForPrompt(mode) {
  if (!GBRAIN_ACTIVE_MODES.has(mode)) return "";
  if (state.gbrainStale || !gbrainContextSnapshotMatches()) return "";
  if (!state.gbrainRetrieval) return "";
  if (!["assembled", "manual"].includes(state.gbrainBundleOrigin)) return "";
  if (state.gbrainBundleSignature !== gbrainSelectionSignature()) return "";
  return $("gbrain-results").value;
}

async function requestJson(url, options = {}) {
  const { timeoutMs = 60_000, ...fetchOptions } = options;
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), Math.max(1, Number(timeoutMs) || 60_000));
  try {
    const response = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...fetchOptions,
      signal: controller.signal,
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      const detail = payload.detail;
      const error = new Error(typeof detail === "string" ? detail : detail?.message || "请求失败");
      error.payload = payload;
      error.status = response.status;
      throw error;
    }
    return payload;
  } catch (error) {
    if (error.name === "AbortError") {
      const timeoutError = new Error(`请求超时（${Math.round((Number(timeoutMs) || 60_000) / 1000)} 秒）`);
      timeoutError.code = "request_timeout";
      timeoutError.status = 0;
      throw timeoutError;
    }
    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
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
  clearGbrainWorkspace("已切换小说", { quiet: true });
  clearReferenceSelection();
  clearEditorDirty();
  setDesignEditing(false);
  document.querySelectorAll(".creative-stage").forEach((stage) => stage.classList.remove("stage-editing"));
  state.bookId = book.book_id;
  state.workflow = null;
  state.agentdockLaunchSnapshots.clear();
  state.agentdockLatestLaunch.clear();
  state.agentdockPreviewJob = null;
  if ($("agentdock-result-preview")) $("agentdock-result-preview").value = "";
  if ($("agentdock-consult-response")) $("agentdock-consult-response").value = "";
  clearBatchProductionBuffers();
  selectedWorkflowArtifact = "";
  $("book-id").value = book.book_id;
  $("sidebar-book-name").textContent = book.book_id;
  $("topbar-book").textContent = book.book_id;
  setCreativePayload(book);
  for (const key of Object.keys(designTitles)) {
    $(`design-${key}`).value = book.design_sections?.[key] || "";
  }
  for (const key of ["long_plan", "small_plan", "status"]) {
    $(`section-${key}`).value = book.sections?.[key] || "";
  }
  const completed = (book.sections?.status || "").match(/当前已完成第\s*(\d+)\s*章/);
  if ($("evolution-world-from")) $("evolution-world-from").value = String((completed ? Number(completed[1]) : 0) + 1);
  if ($("evolution-world-until")) $("evolution-world-until").value = "0";
  if ($("evolution-world-candidate")) $("evolution-world-candidate").value = "";
  if ($("evolution-human-candidate")) $("evolution-human-candidate").value = "";
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
    "curator-response", "primary-writer-response", "authority-reviser-response", "opening-specialist-response",
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
  try {
    target.value = await loadContinuityContextBefore(chapterNumber);
  } catch (error) {
    showStatus(`读取第${chapterNumber}章连续性上下文失败：${error.message}`, true);
  }
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
    premise_forge: "",
    premise_compiler: "",
    world_vision: "",
    world_expansion: "",
    power_seed: "",
    human_seed: "",
    human_development: "",
    idea: $("template-idea").value,
    story_refresh: "",
    outline: $("template-outline").value,
    chapter_prep: $("template-chapter_prep").value,
    chapter: $("template-chapter").value,
    review: $("template-review").value,
    context_curator: $("template-context_curator").value,
    primary_writer: $("template-primary_writer").value,
    authority_reviser: "",
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

function gbrainOffScopeText(mode) {
  return {
    premise_forge: "GBrain：Premise Forge 固定 OFF；先测模型自身完整前提搜索，不复制来源作品。",
    premise_compiler: "GBrain：Premise Compiler 固定 OFF；只做所见候选的因果可满足性检查。",
    human_development: "GBrain：Human Development 固定 OFF；只根据 Frozen Human + 已发生 Canon 判断稳定变化。",
    authority_reviser: "GBrain：Authority Reviser 固定 OFF；只读取 safe Authority Refresh Pack。",
    state_delta: "GBrain：State Extraction 固定 OFF；只提取最终正文已经发生的事实。",
    batch_primary: "GBrain：Batch Primary 固定 OFF；只消费已批准的上游 Authority。",
    batch_authority_reviser: "GBrain：Batch Authority Delta 固定 OFF；只修复 Frozen Authority 闭合。",
  }[mode] || "GBrain：当前 production 阶段固定 OFF；raw inspiration 不进入正文与 Authority recovery。";
}

async function setDefaultGbrainQuery() {
  const mode = $("prompt-mode").value;
  renderGbrainModeState();
  if (!gbrainModeAllowsRetrieval(mode)) {
    $("gbrain-scope").textContent = gbrainOffScopeText(mode);
    return;
  }
  const requestSnapshot = currentGbrainContextSnapshot();
  const button = $("default-gbrain-query");
  if (button) {
    button.disabled = true;
    button.textContent = "正在生成…";
  }
  try {
    const payload = await requestJson("/api/gbrain/brief", {
      method: "POST",
      timeoutMs: 90_000,
      body: JSON.stringify(gbrainContextPayload()),
    });
    if (JSON.stringify(requestSnapshot) !== JSON.stringify(currentGbrainContextSnapshot())) {
      return showStatus("默认 Retrieval Brief 已返回，但当前上下文或作者查询已变化，因此没有覆盖现有内容。", true);
    }
    const nextBrief = payload.retrieval_brief || "";
    if ($("gbrain-query").value !== nextBrief) {
      invalidateGbrainResults("Retrieval Brief 已按当前上下文重新生成");
    }
    state.gbrainDefaultBrief = nextBrief;
    $("gbrain-query").value = state.gbrainDefaultBrief;
    $("gbrain-scope").textContent = payload.scope || "GBrain 范围：修仙小说素材库小说蒸馏域 → 小说来源过滤 → BOOK 兼容性筛选";
    showStatus(`已根据 ${GBRAIN_MODE_LABELS[mode] || mode} 与当前 BOOK 生成 Retrieval Brief。`);
  } catch (error) {
    showStatus(`生成 BOOK-aware Retrieval Brief 失败：${error.message}；作者现有查询已保留。`, true);
  } finally {
    if (button) button.textContent = "生成默认查询";
    renderGbrainModeState();
  }
}

async function handlePromptModeChange() {
  clearReferenceSelection();
  invalidateGbrainResults("切换 Prompt 模式");
  const mode = $("prompt-mode").value;
  renderGbrainModeState();
  if (!gbrainModeAllowsRetrieval(mode)) {
    $("gbrain-scope").textContent = gbrainOffScopeText(mode);
    return;
  }
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

function revisionBaseDraftForMode() {
  const primary = extractPrimaryDraft($("primary-writer-response").value);
  const mode = $("prompt-mode").value;
  if (["specialist_opening", "specialist_dialogue", "specialist_action", "specialist_emotion", "chapter_integrator"].includes(mode)) {
    return extractPrimaryDraft($("authority-reviser-response").value) || primary;
  }
  return primary;
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
    premise_candidates: $("premise-candidates").value,
    selected_premise: state.premiseCompilerScope === "selected" ? $("selected-premise").value : "",
    premise_compiler_scope: state.premiseCompilerScope,
    world_vision: $("creative-world-vision").value,
    world_expansions: $("evolution-world-history")?.value || "",
    power_seed: $("creative-power-seed").value,
    human_seed: $("creative-human-seed").value,
    prototype_id: $("human-prototype-selector")?.value || "",
    character_card: $("creative-character-card").value,
    character_initial_state: $("creative-character-initial-state").value,
    human_development: $("evolution-human-history")?.value || "",
    current_character: $("evolution-current-character")?.value || "",
    evolution_scope: $("evolution-world-scope")?.value || "macro",
    effective_from_chapter: Number($("evolution-world-from")?.value || 0),
    effective_until_chapter: Number($("evolution-world-until")?.value || 0),
    creative_state: state.creativeState,
    current_long_block: $("current-long-block").value,
    previous_chapter_text: $("previous-chapter-text").value,
    current_outline: $("current-outline").value,
    current_chapter_plan: $("current-chapter-plan").value,
    recent_summaries: $("recent-summaries").value,
    selected_references: selectedReferences(),
    gbrain_inspiration: gbrainInspirationForPrompt($("prompt-mode").value),
    proposal_context: $("proposal-editor").value,
    actual_summaries: $("actual-summaries").value,
    current_state: $("review-state").value || $("section-status").value,
    unfulfilled_promises: $("unfulfilled-promises").value,
    future_direction: $("future-direction").value,
    curator_response: $("curator-response").value,
    curated_context: $("curator-response").value,
    primary_writer_response: $("primary-writer-response").value,
    primary_draft: revisionBaseDraftForMode(),
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
  const mode = $("prompt-mode").value;
  if (!gbrainModeAllowsRetrieval(mode)) {
    $("gbrain-status").textContent = "GBrain：当前阶段固定 OFF";
    $("gbrain-status").classList.add("error");
    return showStatus(gbrainOffScopeText(mode), true);
  }
  if (!state.gbrainStatus?.available) {
    await refreshGbrainStatus();
    if (!state.gbrainStatus?.available) {
      $("gbrain-status").textContent = "GBrain：检索环境未就绪";
      $("gbrain-status").classList.add("error");
      return showStatus("GBrain ON 阶段需要可用 CLI 与 embedding 凭据；当前不会降级为 keyword-only。", true);
    }
  }
  const query = $("gbrain-query").value.trim();
  if (!query) {
    $("gbrain-status").textContent = "GBrain：查询失败 — 查询不能为空";
    $("gbrain-status").classList.add("error");
    return showStatus("GBrain 查询不能为空", true);
  }
  const requestSnapshot = currentGbrainContextSnapshot();
  setGbrainQueryPending(true);
  $("gbrain-status").textContent = "GBrain：正在检索、读取完整页面并抽取抽象机制…";
  $("gbrain-status").classList.remove("error");
  try {
    const manualOverride = query === state.gbrainDefaultBrief ? "" : query;
    const payload = await requestJson("/api/gbrain/query", {
      method: "POST",
      timeoutMs: 240_000,
      body: JSON.stringify(gbrainContextPayload(manualOverride)),
    });
    if (JSON.stringify(requestSnapshot) !== JSON.stringify(currentGbrainContextSnapshot())) {
      if (gbrainHasMaterial()) invalidateGbrainResults("检索期间当前上下文已变化");
      $("gbrain-status").textContent = "GBrain：检索已返回，但结果属于旧上下文，未载入";
      return showStatus("GBrain 检索完成前上下文发生了变化；旧材料已保留，本次返回未覆盖当前工作区。", true);
    }
    $("gbrain-raw-results").value = payload.raw_stdout || "（没有可解析的原始检索结果）";
    const diagnostics = [
      ...(payload.rejected || []).map((item) => `${item.slug}：${item.reason}`),
      ...(payload.query_failures || []).map((item) => `检索分支失败：${item.query} → ${item.error}`),
    ];
    $("gbrain-rejections").value = diagnostics.join("\n") || "（没有排除项或检索失败）";
    const fixedCount = payload.fixed_references?.length || 0;
    const failureCount = payload.query_failures?.length || 0;
    $("gbrain-count").textContent = `raw ${payload.raw_count} / unique ${payload.unique_raw_count ?? payload.raw_count} / accepted ${payload.accepted_count} + fixed ${fixedCount} / rejected ${payload.rejected_count}${failureCount ? ` / partial failures ${failureCount}` : ""}`;
    $("gbrain-scope").textContent = payload.scope || "GBrain 范围：修仙小说素材库小说蒸馏域 → 小说来源过滤 → BOOK 兼容性筛选";
    state.gbrainContextSnapshot = requestSnapshot;
    state.gbrainStale = false;
    state.gbrainStaleReason = "";
    renderGbrainCandidates(payload);
    renderGbrainModeState();
    $("gbrain-status").textContent = failureCount
      ? `GBrain：已抽取 ${payload.accepted_count || 0} 条候选；${failureCount} 路检索失败，请查看诊断后再选择`
      : `GBrain：已抽取 ${payload.accepted_count || 0} 条候选，等待作者比较与组装`;
    $("gbrain-status").classList.toggle("error", failureCount > 0);
    showStatus(failureCount
      ? `GBrain 返回了可用候选，但有 ${failureCount} 路检索失败；默认仍未选择任何候选。`
      : "GBrain 已完成 BOOK 兼容性筛选与抽象抽取；默认未选择任何候选，请比较后显式组装。 ",
      failureCount > 0);
  } catch (error) {
    $("gbrain-status").textContent = `GBrain：查询失败 — ${error.message}`;
    $("gbrain-status").classList.add("error");
    showStatus(`${error.message}；已有候选和作者 Bundle 均未被覆盖。`, true);
  } finally {
    setGbrainQueryPending(false);
  }
}

async function generatePrompt() {
  const mode = $("prompt-mode").value;
  if (!validateGbrainBundleForPrompt(mode)) return;
  try {
    const payload = await requestJson("/api/prompt", {
      method: "POST",
      body: JSON.stringify(promptPayload()),
    });
    $("prompt-text").value = payload.prompt;
    const manifest = await saveRunPromptForMode(mode, payload.prompt);
    const node = runNodeByMode[mode];
    if (node && manifest?.nodes?.[node]?.receipt_reused) {
      await hydrateReceiptReusedResponse(mode, node);
      await refreshWorkflow();
      showStatus(`${node} 的最终 Prompt 未变化；已复用 Run Receipt，跳过模型调用。`);
      return;
    }
    renderCodexTaskWrapper(mode);
    if (currentExecutorMode() === "openai_api") {
      await executeOpenAI(payload.prompt, mode);
      return;
    }
    if (currentExecutorMode() === "agentdock_acp") {
      const profile = agentDockExecutionProfile(mode);
      await startAgentDockJob(payload.prompt, {
        mode,
        purpose: "workflow_response",
        contextLabel: chapterActionForNode(state.workflow?.next_actionable_node).title,
        model: profile.model,
        reasoningEffort: profile.reasoningEffort,
      });
      showStatus("AgentDock 作业已启动；完成后只会回填 Response，仍需作者明确 Apply / Save。 ");
      return;
    }
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

async function generateCurrentGbrainPrompt() {
  const mode = $("prompt-mode").value;
  if (!gbrainModeAllowsRetrieval(mode)) return showStatus(gbrainOffScopeText(mode), true);
  await generatePrompt();
}

function currentExecutorMode() {
  return $("executor-mode").value;
}

function agentDockExecutionProfile(mode) {
  if ([
    "premise_forge", "world_vision", "world_expansion", "power_seed", "human_seed",
    "human_development", "outline", "director", "context_curator", "authority_reviser",
    "specialist_opening", "specialist_dialogue", "specialist_action", "specialist_emotion", "chapter_integrator",
  ].includes(mode)) {
    return { model: "gpt-5.6-luna", reasoningEffort: "high" };
  }
  if (["premise_compiler", "primary_writer"].includes(mode)) {
    return { model: "gpt-5.6-terra", reasoningEffort: "high" };
  }
  if (["idea", "story_refresh"].includes(mode)) {
    return { model: "gpt-5.6-sol", reasoningEffort: "high" };
  }
  return { model: "", reasoningEffort: "" };
}

function externalArtifactForMode(mode) {
  const creative = {
    premise_forge: "premise.candidates",
    premise_compiler: "premise.compiler",
    world_vision: "creative.world_vision",
    power_seed: "creative.power_seed",
    human_seed: "creative.human_seed",
    idea: "creative.story_program",
    story_refresh: "creative.story_program",
    world_expansion: "evolution.world-candidate",
    human_development: "evolution.human-development-candidate",
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
  const runPromptFile = node && state.currentRun?.nodes?.[node]?.prompt_file
    ? state.currentRun.nodes[node].prompt_file
    : node ? `${node}_prompt.md` : "";
  const promptPath = node && state.currentRun
    ? `${workspace}\\${state.bookId}\\runs\\chapter-${String(chapter).padStart(4, "0")}\\${runPromptFile}`
    : "当前页面的完整 Prompt 文本框（请先保存/复制）";
  const tempPath = `${workspace}\\${state.bookId}\\.workflow_tmp\\${artifact.replaceAll(".", "-")}-response.md`;
  const nodeArgs = node ? ` --chapter ${chapter} --node ${node}` : "";
  const executionProfile = mode === "authority_reviser"
    ? "执行配置：GPT-5.6 Luna，reasoning=high。"
    : mode === "premise_compiler"
      ? "执行配置：GPT-5.6 Terra，reasoning=high；fresh context，不评分、不选择、不修稿。"
      : mode === "premise_forge"
        ? "执行配置：GPT-5.6 Luna，reasoning=high；GBrain OFF。"
    : mode === "story_refresh"
      ? "执行配置：GPT-5.6 Sol，reasoning=high。"
      : ["world_expansion", "human_development"].includes(mode)
        ? "执行配置：GPT-5.6 Luna，reasoning=high。"
        : "";
  if (["premise_forge", "premise_compiler", "world_expansion", "human_development"].includes(mode)) {
    output.value = [
      ["premise_forge", "premise_compiler"].includes(mode)
        ? "在当前 thegreatnovel 工作区执行开书期 Non-Canon Premise 节点。"
        : "在当前 thegreatnovel 工作区执行周期性 Long-form Evolution 候选。",
      "",
      `Book: ${state.bookId}`,
      `Mode: ${mode}`,
      `读取已经保存的 Prompt：${promptPath}`,
      executionProfile,
      "严格按该 Prompt 生成最终输出。",
      `把模型返回暂存到：${tempPath}`,
      "不要运行 story-mvp-workflow apply，也不要修改任何 Authority：模型返回 ≠ 作者批准。",
      "完成后只报告 output path；作者会在 UI 中审阅后显式批准。",
    ].join("\n");
    panel.hidden = false;
    return;
  }
  output.value = [
    "在当前 thegreatnovel 工作区执行 Story MVP 节点。",
    "",
    `Book: ${state.bookId}`,
    `Artifact: ${artifact}`,
    `读取已经保存的 Prompt：${promptPath}`,
    "严格按该 Prompt 生成最终输出。",
    executionProfile,
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
  const isAuthorityReviser = mode === "authority_reviser";
  const premiseModel = mode === "premise_forge"
    ? "gpt-5.6-luna"
    : mode === "premise_compiler" ? "gpt-5.6-terra" : "";
  const periodicModel = mode === "story_refresh"
    ? "gpt-5.6-sol"
    : ["world_expansion", "human_development"].includes(mode) ? "gpt-5.6-luna" : "";
  const explicitModel = premiseModel || periodicModel || (isStateExtraction
    ? $("state-model").value.trim()
    : isAuthorityReviser ? "" : $("openai-model").value.trim());
  const payload = await requestJson("/api/executors/openai", {
    method: "POST",
    timeoutMs: 3_600_000,
    body: JSON.stringify({
      prompt,
      model: explicitModel,
      purpose: isStateExtraction ? "state_extraction" : isAuthorityReviser ? "authority_reviser" : "default",
      reasoning_effort: isAuthorityReviser || premiseModel || periodicModel ? "high" : "",
    }),
  });
  const target = isStateExtraction ? $("state-delta-response") : $("codex-response");
  target.value = payload.output_text;
  showStatus(`OpenAI API 已返回 ${payload.model}；结果仍需作者 Apply / Save`);
}

async function runCurrentAgentDockPrompt() {
  const prompt = $("prompt-text").value.trim();
  if (!prompt) return showStatus("当前 Prompt 为空，请先生成或编辑 Prompt", true);
  try {
    await startAgentDockJob(prompt, {
      mode: $("prompt-mode").value,
      purpose: "workflow_response",
      contextLabel: $("prompt-mode").selectedOptions[0]?.textContent || "当前节点",
    });
    showStatus("AgentDock 作业已启动；不会自动保存、采用或批准。 ");
  } catch (error) {
    showStatus(`启动 AgentDock 失败：${error.message}`, true);
  }
}

async function runAgentDockConsult() {
  const prompt = $("agentdock-consult-prompt").value.trim();
  if (!prompt) return showStatus("请输入临时咨询内容", true);
  try {
    $("agentdock-consult-response").value = "";
    await startAgentDockJob(prompt, { purpose: "consultation", contextLabel: "临时只读咨询" });
    showStatus("临时只读咨询已启动；Agent 可读取项目上下文，但不会写入小说或工作流。 ");
  } catch (error) {
    showStatus(`启动临时咨询失败：${error.message}`, true);
  }
}

function currentBatchWindow() {
  return {
    startChapter: Number($("batch-start-chapter")?.value || 1),
    batchSize: Number($("batch-size")?.value || 5),
  };
}

function batchWindowKey() {
  const window = currentBatchWindow();
  return `${state.bookId}:${window.startChapter}:${window.batchSize}`;
}

function batchProductionHasContent() {
  const ids = ["batch-primary-prompt", "batch-primary-response", "batch-delta-prompt", "batch-delta-response"];
  return Boolean(
    state.batch.preflight
    || state.batch.adopted
    || ids.some((id) => $(id)?.value.trim()),
  );
}

function invalidateBatchPreflight() {
  state.batch.preflight = null;
  state.batch.adopted = null;
  renderBatchStatus();
}

function invalidateBatchPrimaryDependents() {
  state.batch.deltaPromptWindow = "";
  state.batch.deltaPromptPrimary = "";
  invalidateBatchPreflight();
}

function clearBatchProductionBuffers() {
  for (const id of ["batch-primary-prompt", "batch-primary-response", "batch-delta-prompt", "batch-delta-response"]) {
    if ($(id)) $(id).value = "";
  }
  state.batch.preflight = null;
  state.batch.adopted = null;
  state.batch.continuityText = "";
  state.batch.primaryPromptWindow = "";
  state.batch.deltaPromptWindow = "";
  state.batch.deltaPromptPrimary = "";
  renderBatchStatus();
}

function handleBatchWindowChange() {
  const next = currentBatchWindow();
  const previous = state.batch.window || next;
  if (next.startChapter === previous.startChapter && next.batchSize === previous.batchSize) return;
  if (batchProductionHasContent() && !window.confirm("切换 Batch 窗口会清空当前 Batch Prompt、Response 与预检结果。继续吗？")) {
    $("batch-start-chapter").value = previous.startChapter;
    $("batch-size").value = previous.batchSize;
    return;
  }
  state.batch.window = next;
  clearBatchProductionBuffers();
  $("batch-window").textContent = `第${next.startChapter}—${next.startChapter + next.batchSize - 1}章 · 生产默认`;
}

async function loadContinuityContextBefore(chapterNumber) {
  if (!state.bookId || chapterNumber <= 1) return "";
  const first = Math.max(1, chapterNumber - 2);
  const chapters = [];
  for (let number = first; number < chapterNumber; number += 1) {
    const payload = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/chapters/${number}`);
    if (payload.content) chapters.push(`# ${number}章正文\n\n${payload.content}`);
  }
  return chapters.join("\n\n");
}

function batchPayload() {
  return {
    start_chapter: Number($("batch-start-chapter").value),
    batch_size: Number($("batch-size").value),
    book_content: composeBookContent(),
    world_vision: $("creative-world-vision").value,
    world_expansions: $("evolution-world-history")?.value || "",
    character_card: $("creative-character-card").value,
    story_program: $("proposal-editor").value,
    previous_chapter_text: state.batch.continuityText,
    batch_primary_response: $("batch-primary-response").value,
  };
}

function batchPreflightMatchesCurrent() {
  const preflight = state.batch.preflight;
  return Boolean(
    preflight
    && preflight.windowKey === batchWindowKey()
    && preflight.primaryResponse === $("batch-primary-response").value
    && preflight.deltaResponse === $("batch-delta-response").value,
  );
}

function renderBatchStatus() {
  const preflight = state.batch.preflight;
  const currentPreflight = batchPreflightMatchesCurrent();
  const primaryResponse = $("batch-primary-response").value;
  const deltaResponse = $("batch-delta-response").value;
  const deltaCurrent = state.batch.deltaPromptWindow === batchWindowKey()
    && state.batch.deltaPromptPrimary === primaryResponse;
  $("batch-primary-status").textContent = primaryResponse.trim() ? "Primary Response 已就绪" : "等待 Batch Primary";
  $("batch-delta-status").textContent = deltaResponse.trim()
    ? (deltaCurrent ? "Authority Delta 已就绪" : "Authority Delta 已失效；请重新编译")
    : "等待 Authority Delta";
  $("batch-state-status").textContent = state.batch.adopted ? `已采用；下一步 State：第${state.batch.adopted.state_next}章` : "未采用；不会自动更新 State";
  $("batch-preflight-result").textContent = !preflight ? "尚未预检。" : [
    `Patch：${preflight.patch_count}`,
    `章节：${(preflight.revised_chapters || []).join("、") || "—"}`,
    `上游冲突：${(preflight.upstream_conflicts || []).join("；") || "无"}`,
    currentPreflight ? (preflight.adoptable ? "可由作者显式采用" : "不可采用") : "预检已失效：Batch 窗口或 Response 已变化",
  ].join("\n");
  $("batch-adopt").disabled = !(preflight?.adoptable && currentPreflight);
}

async function compileBatchPrimaryPrompt() {
  if (!state.bookId) return showStatus("请先加载小说", true);
  if (("batch-primary-response batch-delta-prompt batch-delta-response").split(" ").some((id) => $(id).value.trim())
      && !window.confirm("重新编译 Batch Primary 会清空当前 Primary/Delta Response 与预检结果。继续吗？")) return;
  try {
    const window = currentBatchWindow();
    const continuityText = await loadContinuityContextBefore(window.startChapter);
    const payload = { ...batchPayload(), previous_chapter_text: continuityText };
    const result = await requestJson("/api/batch/primary-prompt", { method: "POST", body: JSON.stringify(payload) });
    clearBatchProductionBuffers();
    state.batch.window = window;
    state.batch.continuityText = continuityText;
    state.batch.primaryPromptWindow = batchWindowKey();
    $("batch-primary-prompt").value = result.content || "";
    $("prompt-text").value = result.content || "";
    $("batch-window").textContent = `第${result.start_chapter}—${result.end_chapter}章 · Terra high`;
    renderBatchStatus();
    showStatus("Batch Packet / Primary Prompt 已编译；尚未运行或写入任何小说文件。 ");
  } catch (error) { showStatus(`编译 Batch Primary 失败：${error.message}`, true); }
}

async function runBatchPrimary() {
  const prompt = $("batch-primary-prompt").value.trim();
  if (!prompt) return showStatus("请先编译 Batch Primary Prompt", true);
  if (state.batch.primaryPromptWindow !== batchWindowKey()) return showStatus("Batch 窗口已变化，请重新编译 Primary Prompt。", true);
  try {
    await startAgentDockJob(prompt, { purpose: "batch_primary", mode: "batch_primary", contextLabel: "Batch Primary", model: "gpt-5.6-terra", reasoningEffort: "high" });
    showStatus("Batch Primary 已启动（Terra high）；结果只进入 Batch Primary Response。 ");
  } catch (error) { showStatus(`启动 Batch Primary 失败：${error.message}`, true); }
}

async function compileBatchDeltaPrompt() {
  const primaryResponse = $("batch-primary-response").value;
  if (!primaryResponse.trim()) return showStatus("请先获得完整 Batch Primary Response", true);
  try {
    const result = await requestJson("/api/batch/authority-reviser-prompt", { method: "POST", body: JSON.stringify(batchPayload()) });
    $("batch-delta-response").value = "";
    state.batch.preflight = null;
    state.batch.adopted = null;
    state.batch.deltaPromptWindow = batchWindowKey();
    state.batch.deltaPromptPrimary = primaryResponse;
    $("batch-delta-prompt").value = result.content || "";
    $("prompt-text").value = result.content || "";
    $("batch-window").textContent = `第${result.start_chapter}—${result.end_chapter}章 · Sol high`;
    renderBatchStatus();
    showStatus("Authority Delta Prompt 已编译；尚未运行或采用。 ");
  } catch (error) { showStatus(`编译 Authority Delta 失败：${error.message}`, true); }
}

async function runBatchDelta() {
  const prompt = $("batch-delta-prompt").value.trim();
  if (!prompt) return showStatus("请先编译 Authority Delta Prompt", true);
  if (state.batch.deltaPromptWindow !== batchWindowKey() || state.batch.deltaPromptPrimary !== $("batch-primary-response").value) {
    return showStatus("Batch 窗口或 Primary Response 已变化，请重新编译 Authority Delta Prompt。", true);
  }
  try {
    await startAgentDockJob(prompt, { purpose: "batch_authority_reviser", mode: "batch_authority_reviser", contextLabel: "Batch Authority Delta", model: "gpt-5.6-sol", reasoningEffort: "high" });
    showStatus("Batch Authority Delta 已启动（Sol high）；结果只进入 Delta Response。 ");
  } catch (error) { showStatus(`启动 Authority Delta 失败：${error.message}`, true); }
}

async function preflightBatchDelta() {
  const primaryResponse = $("batch-primary-response").value;
  const deltaResponse = $("batch-delta-response").value;
  if (!primaryResponse.trim() || !deltaResponse.trim()) return showStatus("需要完整 Primary Response 与 Authority Delta Response", true);
  if (state.batch.deltaPromptWindow !== batchWindowKey() || state.batch.deltaPromptPrimary !== primaryResponse) {
    return showStatus("Primary Response 或 Batch 窗口已变化，请重新编译并运行 Authority Delta。", true);
  }
  try {
    const payload = { ...batchPayload(), batch_delta_response: deltaResponse };
    const result = await requestJson("/api/batch/apply-authority-delta", { method: "POST", body: JSON.stringify(payload) });
    state.batch.preflight = {
      patch_count: result.patch_count,
      upstream_conflicts: result.upstream_conflicts || [],
      adoptable: Boolean(result.adoptable),
      revised_chapters: Object.keys(result.chapters || {}),
      windowKey: batchWindowKey(),
      primaryResponse,
      deltaResponse,
    };
    state.batch.adopted = null;
    renderBatchStatus();
    showStatus(result.adoptable ? "Batch Delta 预检通过；仍需作者显式采用。" : "Batch Delta 有上游冲突，不能采用。", !result.adoptable);
  } catch (error) { state.batch.preflight = null; renderBatchStatus(); showStatus(`Batch Delta 预检失败：${error.message}`, true); }
}

async function adoptBatchDelta() {
  if (!state.batch.preflight?.adoptable || !batchPreflightMatchesCurrent()) return showStatus("预检已失败或失效，不能采用 Batch。", true);
  if (!window.confirm("确认整批采用？此操作会保存这批正式正文；不会自动写 Canon 或 State。")) return;
  try {
    const result = await requestJson(`/api/books/${encodeURIComponent(state.bookId)}/batch/adopt-authority-delta`, { method: "POST", body: JSON.stringify({ ...batchPayload(), batch_delta_response: $("batch-delta-response").value }) });
    state.batch.adopted = result;
    renderBatchStatus();
    await refreshWorkflow();
    showStatus(`整批已保存。下一步请逐章进入 State Extraction（从第${result.state_next}章开始）；不会自动写 Canon。`);
  } catch (error) { showStatus(`整批采用失败：${error.message}`, true); }
}

async function loadBatchStateChapter() {
  const next = state.batch.adopted?.state_next;
  if (!next) return showStatus("请先成功采用 Batch，才能载入 State 工作区。", true);
  $("chapter-number").value = next;
  $("chapter-number").dispatchEvent(new Event("change"));
  if (!navigateToView("chapter", "进入 State 工作区")) return;
  setChapterTab("execution");
  await loadCurrentChapterBody();
  showStatus(`已载入第${next}章正文与 State 工作区；State 仍须逐章由作者触发。`);
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
    "director", "chapter_prep", "curator", "primary", "authority_reviser", "opening", "dialogue", "action", "emotion", "integrator",
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
  if (["director", "curator", "primary", "authority_reviser", "opening", "dialogue", "action", "emotion", "integrator", "state_delta"].includes(node)) {
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
  } else if (node === "authority_reviser") {
    await generateHybridNodePrompt("authority_reviser");
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
    book_id: state.bookId,
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
    if (currentExecutorMode() === "openai_api") {
      await executeOpenAI(payload.prompt, "state_delta");
      return;
    }
    if (currentExecutorMode() === "agentdock_acp") {
      await startAgentDockJob(payload.prompt, { mode: "state_delta", purpose: "workflow_response", contextLabel: "State 提取" });
      showStatus("State Extraction 已交给 AgentDock；结果只进入 State Delta Response，不会写盘。 ");
      return;
    }
    showStatus("轻量 State Extraction Prompt 已生成；OpenAI 模式使用独立 State 模型。它不会写盘，也不是章节门禁。");
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
    showStatus("所有已运行专项都没有有效 Patch，Integrator 已 skipped；继续保留 Authority Revision 作为 final_source");
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
  if (!hydrateDirectorResponseEditors(response)) {
    showStatus("Director 返回没有完整八字段，未改变当前章小纲", true);
    return;
  }
  markEditorDirty("current-outline");
  await saveRunResponseForMode("director", response);
  showStatus("Director 八字段已采用到当前章小纲；尚未写盘");
}

async function applyHybridResponse(response, editorId) {
  applyResponseToEditor($("codex-response"), $(editorId));
  const modeByEditor = {
    "curator-response": "context_curator",
    "primary-writer-response": "primary_writer",
    "authority-reviser-response": "authority_reviser",
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

async function adoptAuthorityRevision() {
  const body = extractPrimaryDraft($("authority-reviser-response").value);
  if (!body) {
    showStatus("Authority Reviser 返回缺少非空正式正文，未改变保存内容", true);
    return false;
  }
  $("chapter-body-for-save").value = body;
  $("chapter-fact-summary").value = "";
  markEditorDirty("chapter-body-for-save");
  const manifest = await saveRunResponseForMode("authority_reviser", $("authority-reviser-response").value);
  const reviser = manifest?.nodes?.authority_reviser || {};
  if (reviser.status === "failed" && reviser.repair_reason === "missing_explicit_milestone_outcome") {
    $("chapter-body-for-save").value = "";
    showStatus("Authority Revision 漏掉已批准的显式里程碑结果；系统已准备一次窄 Outcome Repair。请在 Run Ledger 点击“重试节点”。", true);
    return false;
  }
  if (reviser.status === "failed") {
    $("chapter-body-for-save").value = "";
    showStatus("Authority Reviser 仍未满足显式里程碑 Outcome Authority；不会采用，也不会进入 State。", true);
    return false;
  }
  await adoptRunSource("authority_reviser");
  showStatus("已采用 Authority Revision 作为正式正文；State Extraction 将只读取修订稿。尚未保存章节");
  return true;
}

async function applyAuthorityReviserResponse() {
  await applyHybridResponse($("codex-response").value, "authority-reviser-response");
  return adoptAuthorityRevision();
}

async function adoptPrimaryDraft() {
  if (state.currentRun?.writer_mode === "curator_primary") {
    showStatus("curator_primary production 必须先经过 Authority Reviser；Primary 只能作为草稿，不能直接成为 final_source。", true);
    return false;
  }
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

function exactPowerPositionLine(text, prefix) {
  return text.split(/\r?\n/)
    .map((line) => line.trim().replace(/^[-*]\s*/, ""))
    .find((line) => line.startsWith(prefix) && /精确位置[：:].*\d/.test(line)) || "";
}

function preserveExactPowerPosition(proposedPersistent, oldStatus) {
  if (exactPowerPositionLine(proposedPersistent, "Current Power Position｜")) return proposedPersistent;

  const oldPersistent = existingCanonSection(oldStatus, "## PERSISTENT CANON", "长期事实");
  let position = exactPowerPositionLine(oldPersistent, "Current Power Position｜");
  if (!position) {
    const characterCard = $("creative-character-card")?.value || "";
    const initial = exactPowerPositionLine(characterCard, "开局精确力量位置｜");
    if (initial) position = initial.replace(/^开局精确力量位置｜/, "Current Power Position｜");
  }
  if (!position) return proposedPersistent;

  const heading = "### Power / Capability";
  if (proposedPersistent.includes(heading)) {
    return proposedPersistent.replace(heading, `${heading}\n${position}`);
  }
  return `${heading}\n${position}\n${proposedPersistent}`.trim();
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
  const persistentCanon = preserveExactPowerPosition(proposed.persistent_canon, oldStatus);
  return [
    `当前已完成第${chapterNumber}章。`,
    "## ACTIVE SCENE STATE",
    proposed.active_scene_state,
    "## PERSISTENT CANON",
    persistentCanon,
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
    const savedTheme = window.localStorage.getItem("tgn-theme");
    if (savedTheme === "dark") {
      document.body.classList.add("theme-dark");
      $("theme-toggle").textContent = "浅色";
      $("theme-toggle").setAttribute("aria-pressed", "true");
      $("theme-color-meta").setAttribute("content", "#0e1720");
    }
    renderLongPlanPanorama();
    renderBatchStatus();
    renderGbrainModeState();
    await Promise.all([refreshExecutorStatus(), refreshGbrainStatus(), refreshProductionRuns()]);
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
$("topbar-settings").addEventListener("click", () => $("settings-button").click());
$("theme-toggle").addEventListener("click", () => {
  const dark = document.body.classList.toggle("theme-dark");
  $("theme-toggle").textContent = dark ? "浅色" : "深色";
  $("theme-toggle").setAttribute("aria-pressed", String(dark));
  $("theme-color-meta").setAttribute("content", dark ? "#0e1720" : "#f2f0eb");
  window.localStorage.setItem("tgn-theme", dark ? "dark" : "light");
});
document.querySelectorAll("[data-top-view]").forEach((button) => {
  button.addEventListener("click", () => navigateToView(button.dataset.topView, "切换创作模式"));
});
document.querySelectorAll("[data-drawer-section]").forEach((button) => {
  button.addEventListener("click", () => {
    openRightDrawer();
    $(button.dataset.drawerSection)?.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});
$("workspace-search").addEventListener("change", () => {
  const query = $("workspace-search").value.trim();
  if (!query) return;
  const match = [...document.querySelectorAll(".workspace-view")].find((element) => element.textContent.includes(query));
  if (!match) return showStatus(`当前工作台未找到“${query}”`, true);
  navigateToView(match.dataset.view, "定位搜索结果");
  match.scrollIntoView({ behavior: "smooth", block: "start" });
  showStatus(`已定位包含“${query}”的工作区`);
});
$("close-settings").addEventListener("click", () => $("settings-dialog").close());
$("save-settings").addEventListener("click", saveOpenAISettings);
$("default-gbrain-query").addEventListener("click", setDefaultGbrainQuery);
$("query-gbrain").addEventListener("click", queryGbrain);
$("gbrain-requery").addEventListener("click", queryGbrain);
$("gbrain-compare").addEventListener("click", openGbrainCompare);
$("gbrain-compare-close").addEventListener("click", () => $("gbrain-compare-dialog").close());
$("gbrain-discard").addEventListener("click", discardGbrainForCurrentRun);
$("gbrain-query").addEventListener("input", () => invalidateGbrainResults("Retrieval Brief 已变化"));
$("gbrain-select-all").addEventListener("click", () => {
  state.gbrainSelected = new Set((state.gbrainRetrieval?.accepted || []).map((item) => item.slug));
  document.querySelectorAll(".gbrain-candidate-card input[type='checkbox']").forEach((checkbox) => { checkbox.checked = true; });
  updateGbrainSelectionState(true);
});
$("gbrain-clear-selection").addEventListener("click", () => {
  state.gbrainSelected.clear();
  document.querySelectorAll(".gbrain-candidate-card input[type='checkbox']").forEach((checkbox) => { checkbox.checked = false; });
  updateGbrainSelectionState(true);
});
$("gbrain-assemble").addEventListener("click", assembleGbrainSelection);
$("gbrain-results").addEventListener("input", handleGbrainBundleInput);
$("generate-premise-forge-prompt").addEventListener("click", generatePremiseForgePrompt);
$("apply-premise-forge-response").addEventListener("click", () => applyPremiseResponse("premise-candidates", "Premise Forge 返回"));
$("save-premise-candidates").addEventListener("click", savePremiseCandidates);
$("generate-premise-batch-compiler").addEventListener("click", () => generatePremiseCompilerPrompt("candidates"));
document.querySelectorAll("[data-premise-select]").forEach((button) => {
  button.addEventListener("click", () => choosePremiseCandidate(button.dataset.premiseSelect));
});
$("save-selected-premise").addEventListener("click", saveSelectedPremise);
$("generate-selected-premise-compiler").addEventListener("click", () => generatePremiseCompilerPrompt("selected"));
$("apply-premise-compiler-response").addEventListener("click", () => applyPremiseResponse("premise-compiler-report", "Premise Compiler 返回"));
$("save-premise-compiler").addEventListener("click", savePremiseCompilerReport);
$("approve-premise").addEventListener("click", approvePremiseContract);
$("skip-premise").addEventListener("click", skipPremiseAperture);
$("generate-idea-prompt").addEventListener("click", generateCurrentGbrainPrompt);
$("generate-world-vision-prompt").addEventListener("click", () => generateCreativePrompt("world_vision"));
$("generate-power-seed-prompt").addEventListener("click", () => generateCreativePrompt("power_seed"));
$("generate-human-seed-prompt").addEventListener("click", () => generateCreativePrompt("human_seed"));
$("human-prototype-selector").addEventListener("change", async () => {
  invalidateGbrainResults("切换 Human Prototype");
  if ($("prompt-mode").value === "human_seed") await setDefaultGbrainQuery();
});
$("generate-story-program-prompt").addEventListener("click", () => generateCreativePrompt("idea"));
$("generate-world-expansion-prompt").addEventListener("click", () => generateCreativePrompt("world_expansion"));
$("generate-human-development-prompt").addEventListener("click", () => generateCreativePrompt("human_development"));
$("generate-story-refresh-prompt").addEventListener("click", () => generateCreativePrompt("story_refresh"));
$("apply-world-vision-response").addEventListener("click", () => applyCreativeResponse("world_vision"));
$("apply-power-seed-response").addEventListener("click", () => applyCreativeResponse("power_seed"));
$("apply-human-seed-response").addEventListener("click", () => applyCreativeResponse("human_seed"));
$("apply-story-program-response").addEventListener("click", () => applyCreativeResponse("proposal"));
$("apply-world-expansion-response").addEventListener("click", () => applyEvolutionResponse("world"));
$("apply-human-development-response").addEventListener("click", () => applyEvolutionResponse("human"));
$("apply-story-refresh-response").addEventListener("click", applyStoryRefreshResponse);
$("save-world-vision").addEventListener("click", () => saveCreativeArtifact("world_vision"));
$("save-power-seed").addEventListener("click", () => saveCreativeArtifact("power_seed"));
$("save-human-seed").addEventListener("click", () => saveCreativeArtifact("human_seed"));
$("approve-world-vision").addEventListener("click", () => approveCreativeArtifact("world_vision"));
$("approve-character").addEventListener("click", approveCharacter);
$("approve-proposal").addEventListener("click", () => approveCreativeArtifact("proposal"));
$("approve-world-expansion").addEventListener("click", approveWorldExpansion);
$("approve-human-development").addEventListener("click", approveHumanDevelopment);
$("refresh-current-character").addEventListener("click", refreshCurrentCharacter);
$("generate-prompt").addEventListener("click", generateCurrentChapterAction);
$("generate-director-prompt").addEventListener("click", () => generateHybridNodePrompt("director"));
$("generate-curator-prompt").addEventListener("click", () => generateHybridNodePrompt("context_curator"));
$("generate-primary-writer-prompt").addEventListener("click", () => generateHybridNodePrompt("primary_writer"));
$("generate-authority-reviser-prompt").addEventListener("click", () => generateHybridNodePrompt("authority_reviser"));
$("generate-opening-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_opening"));
$("generate-dialogue-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_dialogue"));
$("generate-action-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_action"));
$("generate-emotion-prompt").addEventListener("click", () => generateHybridNodePrompt("specialist_emotion"));
$("generate-integrator-prompt").addEventListener("click", () => generateHybridNodePrompt("chapter_integrator"));
$("apply-curator-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "curator-response"));
$("apply-director-response").addEventListener("click", applyDirectorResponse);
$("apply-primary-writer-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "primary-writer-response"));
$("apply-authority-reviser-response").addEventListener("click", applyAuthorityReviserResponse);
$("apply-opening-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "opening-specialist-response"));
$("apply-dialogue-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "dialogue-specialist-response"));
$("apply-action-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "action-specialist-response"));
$("apply-emotion-response").addEventListener("click", () => applyHybridResponse($("codex-response").value, "emotion-specialist-response"));
$("extract-integrator-body").addEventListener("click", extractIntegratorBody);
$("adopt-authority-revision").addEventListener("click", adoptAuthorityRevision);
$("adopt-primary-draft").addEventListener("click", adoptPrimaryDraft);
$("load-current-chapter-plan").addEventListener("click", loadCurrentChapterPlan);
$("generate-chapter-prep").addEventListener("click", generateChapterPrepPrompt);
$("copy-prompt").addEventListener("click", copyPrompt);
$("refresh-workflow").addEventListener("click", refreshWorkflow);
$("agentdock-run-current").addEventListener("click", runCurrentAgentDockPrompt);
$("agentdock-refresh-jobs").addEventListener("click", refreshAgentDockJobs);
$("agentdock-mini-anchor").addEventListener("click", () => {
  openRightDrawer();
  $("agentdock-progress-anchor")?.scrollIntoView({ behavior: "smooth", block: "start" });
});
$("agentdock-active-cancel").addEventListener("click", () => {
  const job = state.agentdockFocusedJob;
  if (job && ["queued", "running"].includes(job.status)) cancelAgentDockJob(job.job_id);
});
$("agentdock-collapse-activity").addEventListener("click", () => {
  const details = document.querySelector(".agent-activity-details");
  if (!details) return;
  details.open = !details.open;
  $("agentdock-collapse-activity").textContent = details.open ? "收起活动" : "展开活动";
});
$("agentdock-run-consult").addEventListener("click", runAgentDockConsult);
$("agentdock-load-current").addEventListener("click", loadAgentDockPreview);
$("batch-compile-primary").addEventListener("click", compileBatchPrimaryPrompt);
$("batch-run-primary").addEventListener("click", runBatchPrimary);
$("batch-compile-delta").addEventListener("click", compileBatchDeltaPrompt);
$("batch-run-delta").addEventListener("click", runBatchDelta);
$("batch-preflight").addEventListener("click", preflightBatchDelta);
$("batch-adopt").addEventListener("click", adoptBatchDelta);
$("batch-load-state").addEventListener("click", loadBatchStateChapter);
$("batch-start-chapter").addEventListener("change", handleBatchWindowChange);
$("batch-size").addEventListener("change", handleBatchWindowChange);
for (const id of ["codex-response", "state-delta-response", "agentdock-consult-response", "batch-primary-response", "batch-delta-response"]) {
  if ($(id)) $(id).addEventListener("input", (event) => markAgentDockEditorEdited(event.currentTarget));
}
$("batch-primary-response").addEventListener("input", invalidateBatchPrimaryDependents);
$("batch-delta-response").addEventListener("input", invalidateBatchPreflight);
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
    "curator-response", "primary-writer-response", "authority-reviser-response", "opening-specialist-response",
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
  "creative-direction", "creative-world-vision", "creative-character-card", "proposal-editor",
  "current-long-block", "current-outline", "recent-summaries", "section-status",
]) {
  $(id).addEventListener("input", () => invalidateGbrainResults(`${id} 已变化`));
}
$("human-prototype-selector").addEventListener("change", () => invalidateGbrainResults("Human Prototype 已变化"));
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
$("refresh-production-runs").addEventListener("click", refreshProductionRuns);
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

window.setInterval(refreshAgentDockFocusClock, 1000);
window.setInterval(refreshProductionRuns, 15_000);

mountRightDrawer();
initializeReadingState();
setView(currentViewFromHash(), false);
setDesignEditing(false);
renderDirtyState();
initialize();
