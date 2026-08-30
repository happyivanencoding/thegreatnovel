from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .character_seeds import compose_character_card, split_human_seed_authorities
from .long_form_evolution import (
    CURRENT_CHARACTER_FILENAME,
    HUMAN_DEVELOPMENT_DIR,
    WORLD_EXPANSION_DIR,
    compile_current_character,
    extract_world_horizon_handoff,
)
from .prompts import (
    DEFAULT_PROMPT_TEMPLATES,
    compact_open_promises,
    compact_recent_summaries,
    parse_canon_memory,
    parse_state_delta_v2,
)
from .power_ruler import (
    parse_root_precise_power_ruler,
    preserve_or_require_current_power_position,
    validate_human_seed_start,
    validate_world_expansion_ruler,
)
from .progressive_canon import (
    MysteryRevealContract,
    MysteryThread,
    adopt_hidden_fixed_point,
    advance_after_reveal,
    compile_runtime_mystery_projection,
    extract_reveal_contracts,
    render_planning_projection,
    strip_reveal_contracts,
)


SECTION_TITLES = {
    "design": "# 小说总体设计画像",
    "long_plan": "# 当前中期规划窗口",
    "small_plan": "# 未来十章逐章小纲",
    "status": "# 当前状态、未兑现承诺与作者备注",
}
LEGACY_SECTION_TITLES = {"# 未来100章大型剧情块": "long_plan"}

DESIGN_SECTION_TITLES = {
    "growth_genome": "## 0. 本书成长基因图",
    "type_promise": "## 1. 核心类型与读者承诺",
    "world_structure": "## 2. 世界观结构",
    "world_pressure": "## 3. 世界如何持续制造剧情压力",
    "protagonist_model": "## 4. 主角模型、人物弧与核心矛盾",
    "relationships": "## 5. 配角与关系系统",
    "plot_engine": "## 6. 核心情节发动机",
    "narrative_structure": "## 7. 叙事结构",
    "prose": "## 8. 文风与可操作参数",
    "dialogue": "## 9. 对话特点",
    "rhythm": "## 10. 节奏结构",
    "theme": "## 11. 主题、价值观与长期问题",
    "strengths_risks": "## 12. 当前设计最强点与最弱点",
}

PROMPT_TEMPLATE_LABELS = {
    "idea": "Story Program / 商业化结构方案",
    "outline": "新书/总纲规划",
    "chapter_prep": "当前章执行小纲",
    "chapter": "当前章节写作",
    "review": "十章复盘与下一批十章",
    "context_curator": "Hybrid Context Curator",
    "primary_writer": "Hybrid Primary Writer",
    "specialist_opening": "Opening & Scene Entry Specialist",
    "specialist_dialogue": "Dialogue & Character Voice Specialist",
    "specialist_action": "Action & Spatial Logic Specialist",
    "specialist_emotion": "Emotion & Aftermath Specialist",
    "chapter_integrator": "Hybrid Revision Integrator",
}
LEGACY_PROMPT_TEMPLATE_HEADINGS = {"# 男频爽文创意生成": "idea"}

CREATIVE_ARTIFACT_FILES = {
    "world_vision": "WORLD_VISION.md",
    "power_seed": "POWER_SEED.md",
    "human_seed": "HUMAN_SEED.md",
    "character_card": "CHARACTER.md",
    "proposal": "PROPOSAL.md",
}
CHARACTER_AUX_FILES = {
    "character_initial_state": "CHARACTER_INITIAL_STATE.md",
    "character_audition": "CHARACTER_AUDITION.md",
}
CREATIVE_ORIGINS = frozenset(
    {"empty", "model_generated", "model_selected", "author_edited", "legacy_unknown", "deterministic"}
)
CREATIVE_STATUSES = frozenset({"empty", "draft", "author_approved"})
MYSTERY_CONTROL_FILENAME = "MYSTERY_CONTROL.json"

BOOK_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")

CHAPTER_BODY_FORBIDDEN_MARKERS = (
    "# Writer Audit",
    "# Primary Writer Audit",
    "# Primary Draft",
    "# Primary Fact Summary",
    "# 章节事实摘要",
    "---FACT_SUMMARY---",
    "\\n---FACT_SUMMARY---",
    "# State Delta Audit",
    "# Proposed Active Scene State",
    "# Proposed Persistent Canon",
    "# Proposed Chapter Summary",
    "# Proposed Open Promises",
    "# Proposed Canon Index",
)


def validate_chapter_body_for_save(content: str) -> None:
    """只允许正式小说正文进入 chapter-NNNN.md。"""

    if not content.strip():
        raise ValueError("章节正文不能为空")
    for line in content.splitlines():
        for marker in CHAPTER_BODY_FORBIDDEN_MARKERS:
            if line.startswith(marker):
                raise ValueError(f"正式章节正文不能包含内部区块标记：{marker}")


def default_book_content() -> str:
    design_bodies = {
        key: "（请填写这项总体设计。）" for key in DESIGN_SECTION_TITLES
    }
    bodies = {
        "design": compose_design_content(design_bodies),
        "long_plan": "（先写具体事件链，再写叙事功能。）",
        "small_plan": "（每章请写具体剧情、结果 / 状态变化、叙事功能和结尾推动。）",
        "status": "当前状态：\n\n未兑现承诺：\n\n作者备注：",
    }
    return compose_book_content(bodies)


def compose_book_content(sections: dict[str, str]) -> str:
    chunks: list[str] = []
    for key, title in SECTION_TITLES.items():
        chunks.append(f"{title}\n\n{sections.get(key, '').strip()}")
    return "\n\n".join(chunks).rstrip() + "\n"


def compose_design_content(design_sections: dict[str, str]) -> str:
    chunks: list[str] = []
    for key, title in DESIGN_SECTION_TITLES.items():
        chunks.append(f"{title}\n\n{design_sections.get(key, '').strip()}")
    return "\n\n".join(chunks).rstrip() + "\n"


def validate_book_content_for_save(content: str) -> None:
    """BOOK.md 是持久结构文件；保存前只校验四个一级区块没有被格式破坏。"""

    lines = [line.strip() for line in content.splitlines()]
    positions: list[int] = []
    for key, title in SECTION_TITLES.items():
        candidates = [title]
        if key == "long_plan":
            candidates.extend(
                legacy_title
                for legacy_title, legacy_key in LEGACY_SECTION_TITLES.items()
                if legacy_key == key
            )
        matches = [index for index, line in enumerate(lines) if line in candidates]
        if len(matches) != 1:
            raise ValueError(f"BOOK.md 必须且只能包含一个独立一级标题：{title}")
        positions.append(matches[0])
    if positions != sorted(positions):
        raise ValueError("BOOK.md 一级区块顺序无效")


def parse_book_sections(content: str) -> dict[str, str]:
    headings = {title: key for key, title in SECTION_TITLES.items()}
    headings.update(LEGACY_SECTION_TITLES)
    sections = {key: "" for key in SECTION_TITLES}
    current_key: str | None = None
    lines: list[str] = []
    for line in content.splitlines():
        title = line.strip()
        if title in headings:
            if current_key is not None:
                sections[current_key] = "\n".join(lines).strip()
            current_key = headings[title]
            lines = []
            continue
        if current_key is not None:
            lines.append(line)
    if current_key is not None:
        sections[current_key] = "\n".join(lines).strip()
    return sections


def parse_design_sections(content: str) -> dict[str, str]:
    headings = {title: key for key, title in DESIGN_SECTION_TITLES.items()}
    sections = {key: "" for key in DESIGN_SECTION_TITLES}
    current_key: str | None = None
    lines: list[str] = []
    for line in content.splitlines():
        title = line.strip()
        if title in headings:
            if current_key is not None:
                sections[current_key] = "\n".join(lines).strip()
            current_key = headings[title]
            lines = []
            continue
        if current_key is not None:
            lines.append(line)
    if current_key is not None:
        sections[current_key] = "\n".join(lines).strip()
    return sections


def prompt_templates_to_text(templates: dict[str, str]) -> str:
    chunks: list[str] = []
    for key, label in PROMPT_TEMPLATE_LABELS.items():
        chunks.append(f"# {label}\n\n{templates.get(key, '').strip()}")
    return "\n\n".join(chunks).rstrip() + "\n"


def text_to_prompt_templates(content: str) -> dict[str, str]:
    headings = {f"# {label}": key for key, label in PROMPT_TEMPLATE_LABELS.items()}
    headings.update(LEGACY_PROMPT_TEMPLATE_HEADINGS)
    templates = {key: "" for key in PROMPT_TEMPLATE_LABELS}
    current_key: str | None = None
    lines: list[str] = []
    for line in content.splitlines():
        title = line.strip()
        if title in headings:
            if current_key is not None:
                templates[current_key] = "\n".join(lines).strip()
            current_key = headings[title]
            lines = []
            continue
        if title.startswith("# "):
            if current_key is not None:
                templates[current_key] = "\n".join(lines).strip()
            current_key = None
            lines = []
            continue
        if current_key is not None:
            lines.append(line)
    if current_key is not None:
        templates[current_key] = "\n".join(lines).strip()
    return templates


def default_prompt_templates() -> dict[str, str]:
    # Creative split prompts (World/Power/Human) are architecture-owned and not
    # editable per-book templates. Only downstream/runtime templates live in PROMPTS.md.
    from .character_prompts import adapt_split_planning_template

    templates = {
        key: DEFAULT_PROMPT_TEMPLATES.get(key, "")
        for key in PROMPT_TEMPLATE_LABELS
    }
    for mode in ("idea", "outline"):
        templates[mode] = adapt_split_planning_template(templates[mode], mode=mode)
    return templates


def validate_book_id(book_id: str) -> str:
    value = book_id.strip()
    if not BOOK_ID_PATTERN.fullmatch(value):
        raise ValueError("book_id 只能包含字母、数字、下划线和短横线，且必须以字母或数字开头")
    return value


def book_directory(book_id: str, workspace: Path) -> Path:
    return workspace / validate_book_id(book_id)


def create_book(book_id: str, workspace: Path) -> Path:
    workspace.mkdir(parents=True, exist_ok=True)
    directory = book_directory(book_id, workspace)
    if directory.exists():
        raise FileExistsError(f"小说已存在：{book_id}")
    directory.mkdir()
    (directory / "chapters").mkdir()
    (directory / "BOOK.md").write_text(default_book_content(), encoding="utf-8")
    (directory / "PROMPTS.md").write_text(
        prompt_templates_to_text(default_prompt_templates()), encoding="utf-8"
    )
    for artifact, filename in CREATIVE_ARTIFACT_FILES.items():
        if artifact != "proposal":
            (directory / filename).write_text("", encoding="utf-8")
    (directory / "PROPOSAL.md").write_text("", encoding="utf-8")
    for filename in CHARACTER_AUX_FILES.values():
        (directory / filename).write_text("", encoding="utf-8")
    _write_creative_state(directory, _empty_creative_state())
    _write_mystery_control(directory, {"threads": {}, "reveals": {}, "compiler_inputs": {}})
    return directory


def list_books(workspace: Path) -> list[str]:
    if not workspace.exists():
        return []
    return sorted(
        directory.name
        for directory in workspace.iterdir()
        if directory.is_dir() and (directory / "BOOK.md").is_file()
    )


def require_book(book_id: str, workspace: Path) -> Path:
    directory = book_directory(book_id, workspace)
    if not (directory / "BOOK.md").is_file():
        raise FileNotFoundError(f"找不到小说：{book_id}")
    return directory


def _mystery_thread_from_dict(value: dict[str, Any]) -> MysteryThread:
    return MysteryThread(
        mystery_id=str(value.get("mystery_id", "")).strip(),
        question=str(value.get("question", "")).strip(),
        state=str(value.get("state", "OPEN")).strip().upper(),  # type: ignore[arg-type]
        known_anchors=str(value.get("known_anchors", "")).strip(),
        decision_trigger=str(value.get("decision_trigger", "")).strip(),
        fixed_point=str(value.get("fixed_point", "")).strip(),
        remains_unknown=str(value.get("remains_unknown", "")).strip(),
        reveal_boundary=str(value.get("reveal_boundary", "")).strip(),
        route=str(value.get("route", "story")).strip().casefold(),  # type: ignore[arg-type]
    )


def _reveal_contract_from_dict(value: dict[str, Any]) -> MysteryRevealContract:
    anchors = value.get("reader_anchors", [])
    if not isinstance(anchors, list):
        raise ValueError("Mystery Reveal reader_anchors 必须是数组")
    return MysteryRevealContract(
        mystery_id=str(value.get("mystery_id", "")).strip(),
        reveal_chapter=int(value.get("reveal_chapter", 0)),
        event_atom=str(value.get("event_atom", "")).strip(),
        state_residue=str(value.get("state_residue", "")).strip(),
        reader_anchors=tuple(str(item).strip() for item in anchors if str(item).strip()),
        still_open_after_reveal=str(value.get("still_open_after_reveal", "")).strip(),
    )


def _mystery_thread_to_dict(thread: MysteryThread) -> dict[str, Any]:
    return {
        "mystery_id": thread.mystery_id,
        "question": thread.question,
        "state": thread.state,
        "known_anchors": thread.known_anchors,
        "decision_trigger": thread.decision_trigger,
        "fixed_point": thread.fixed_point,
        "remains_unknown": thread.remains_unknown,
        "reveal_boundary": thread.reveal_boundary,
        "route": thread.route,
    }


def _reveal_contract_to_dict(contract: MysteryRevealContract) -> dict[str, Any]:
    return {
        "mystery_id": contract.mystery_id,
        "reveal_chapter": contract.reveal_chapter,
        "event_atom": contract.event_atom,
        "state_residue": contract.state_residue,
        "reader_anchors": list(contract.reader_anchors),
        "still_open_after_reveal": contract.still_open_after_reveal,
    }


def _read_mystery_control(directory: Path) -> dict[str, Any]:
    path = directory / MYSTERY_CONTROL_FILENAME
    if not path.is_file():
        return {"threads": {}, "reveals": {}, "compiler_inputs": {}}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("MYSTERY_CONTROL.json 不是有效 JSON") from error
    if (
        not isinstance(raw, dict)
        or not isinstance(raw.get("threads", {}), dict)
        or not isinstance(raw.get("reveals", {}), dict)
        or not isinstance(raw.get("compiler_inputs", {}), dict)
    ):
        raise ValueError("MYSTERY_CONTROL.json 结构无效")
    threads: dict[str, Any] = {}
    for mystery_id, value in raw.get("threads", {}).items():
        if not isinstance(value, dict):
            raise ValueError(f"Mystery {mystery_id} 状态必须是对象")
        thread = _mystery_thread_from_dict(value)
        if not thread.mystery_id or thread.mystery_id != mystery_id:
            raise ValueError(f"Mystery {mystery_id} ID 不一致")
        render_planning_projection(thread)
        threads[mystery_id] = _mystery_thread_to_dict(thread)
    reveals: dict[str, Any] = {}
    for mystery_id, value in raw.get("reveals", {}).items():
        if not isinstance(value, dict):
            raise ValueError(f"Mystery Reveal {mystery_id} 必须是对象")
        contract = _reveal_contract_from_dict(value)
        if (
            contract.mystery_id != mystery_id
            or contract.reveal_chapter < 1
            or not contract.event_atom
            or not contract.state_residue
            or not contract.reader_anchors
        ):
            raise ValueError(f"Mystery Reveal {mystery_id} 无效")
        reveals[mystery_id] = _reveal_contract_to_dict(contract)
    compiler_inputs: dict[str, Any] = {}
    for mystery_id, value in raw.get("compiler_inputs", {}).items():
        if not isinstance(value, dict):
            raise ValueError(f"Mystery Compiler Input {mystery_id} 必须是对象")
        required = ("thread", "selected_candidate", "decision_surface", "planning_need", "current_context")
        if any(key not in value for key in required) or not isinstance(value.get("thread"), dict):
            raise ValueError(f"Mystery Compiler Input {mystery_id} 结构无效")
        compiler_inputs[mystery_id] = {
            "thread": value["thread"],
            "selected_candidate": str(value["selected_candidate"]),
            "decision_surface": str(value["decision_surface"]),
            "planning_need": str(value["planning_need"]),
            "current_context": str(value["current_context"]),
        }
    return {"threads": threads, "reveals": reveals, "compiler_inputs": compiler_inputs}


def _write_mystery_control(directory: Path, value: dict[str, Any]) -> None:
    (directory / MYSTERY_CONTROL_FILENAME).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_mystery_control(book_id: str, workspace: Path) -> dict[str, Any]:
    return _read_mystery_control(require_book(book_id, workspace))


def get_mystery_thread(book_id: str, mystery_id: str, workspace: Path) -> MysteryThread:
    control = read_mystery_control(book_id, workspace)
    value = control["threads"].get(mystery_id)
    if not isinstance(value, dict):
        raise ValueError(f"找不到 Mystery：{mystery_id}")
    return _mystery_thread_from_dict(value)


def save_mystery_thread(book_id: str, thread: MysteryThread, workspace: Path) -> dict[str, Any]:
    directory = require_book(book_id, workspace)
    if not thread.mystery_id.strip() or not thread.question.strip():
        raise ValueError("Mystery 需要 mystery_id 与 question")
    render_planning_projection(thread)
    control = _read_mystery_control(directory)
    control["threads"][thread.mystery_id] = _mystery_thread_to_dict(thread)
    _write_mystery_control(directory, control)
    return control


def save_mystery_compiler_input(
    book_id: str,
    mystery_id: str,
    *,
    selected_candidate: str,
    decision_surface: str,
    planning_need: str,
    current_context: str,
    workspace: Path,
) -> dict[str, Any]:
    directory = require_book(book_id, workspace)
    control = _read_mystery_control(directory)
    thread_value = control["threads"].get(mystery_id)
    if not isinstance(thread_value, dict):
        raise ValueError(f"找不到 Mystery：{mystery_id}")
    control["compiler_inputs"][mystery_id] = {
        "thread": thread_value,
        "selected_candidate": selected_candidate,
        "decision_surface": decision_surface,
        "planning_need": planning_need,
        "current_context": current_context,
    }
    _write_mystery_control(directory, control)
    return control


def adopt_mystery_candidate(
    book_id: str,
    mystery_id: str,
    *,
    selected_candidate: str,
    compiler_report: str,
    current_context: str,
    workspace: Path,
) -> dict[str, Any]:
    directory = require_book(book_id, workspace)
    control = _read_mystery_control(directory)
    thread_value = control["threads"].get(mystery_id)
    compiler_input = control["compiler_inputs"].get(mystery_id)
    if not isinstance(thread_value, dict):
        raise ValueError(f"找不到 Mystery：{mystery_id}")
    if not isinstance(compiler_input, dict):
        raise ValueError("Mystery 尚无当前 Compiler Input；请先重新生成 Compiler Prompt")
    if compiler_input.get("thread") != thread_value:
        raise ValueError("Mystery 状态已变化；旧 Compiler Report 已 stale，请重新编译")
    if compiler_input.get("selected_candidate") != selected_candidate:
        raise ValueError("Selected Mystery Candidate 与 Compiler Input 不一致；请重新编译")
    if compiler_input.get("current_context") != current_context:
        raise ValueError("BOOK / Canon 已变化；旧 Compiler Report 已 stale，请重新编译")
    adopted = adopt_hidden_fixed_point(
        thread=_mystery_thread_from_dict(thread_value),
        selected_candidate=selected_candidate,
        compiler_report=compiler_report,
    )
    control["threads"][mystery_id] = _mystery_thread_to_dict(adopted)
    del control["compiler_inputs"][mystery_id]
    _write_mystery_control(directory, control)
    return control


def save_mystery_reveal(
    book_id: str,
    contract: MysteryRevealContract,
    workspace: Path,
) -> dict[str, Any]:
    return save_mystery_reveals(book_id, (contract,), workspace)


def save_mystery_reveals(
    book_id: str,
    contracts: tuple[MysteryRevealContract, ...],
    workspace: Path,
) -> dict[str, Any]:
    directory = require_book(book_id, workspace)
    control = _read_mystery_control(directory)
    pending: dict[str, dict[str, Any]] = {}
    for contract in contracts:
        thread_value = control["threads"].get(contract.mystery_id)
        if not isinstance(thread_value, dict):
            raise ValueError(f"找不到 Mystery：{contract.mystery_id}")
        thread = _mystery_thread_from_dict(thread_value)
        if thread.state != "FIXED_HIDDEN":
            raise ValueError("只有 FIXED_HIDDEN Mystery 才能保存 Reveal Contract")
        compile_runtime_mystery_projection(
            thread, contract, chapter_number=contract.reveal_chapter
        )
        pending[contract.mystery_id] = _reveal_contract_to_dict(contract)
    control["reveals"].update(pending)
    _write_mystery_control(directory, control)
    return control


def render_mystery_planning_context(book_id: str, workspace: Path, *, route: str) -> str:
    control = read_mystery_control(book_id, workspace)
    projections: list[str] = []
    for value in control["threads"].values():
        thread = _mystery_thread_from_dict(value)
        if thread.route == route:
            projections.append(render_planning_projection(thread))
    return "\n\n".join(projections).strip()


def render_mystery_outline_schedule(book_id: str, workspace: Path) -> str:
    control = read_mystery_control(book_id, workspace)
    lines: list[str] = []
    for value in control["reveals"].values():
        contract = _reveal_contract_from_dict(value)
        lines.append(
            f"- 第{contract.reveal_chapter}章｜[MYSTERY-REVEAL:{contract.mystery_id}]｜只排 Reveal 时机；答案与 Event Atom 不进入 Outline。"
        )
    return "\n".join(lines)


def _append_chapter_plan_field(plan: str, label: str, addition: str) -> str:
    field_labels = ("具体剧情", "结果 / 状态变化", "叙事功能", "结尾推动")
    alternation = "|".join(re.escape(item) for item in field_labels)
    pattern = re.compile(
        rf"(?ms)^({re.escape(label)}\s*[：:]\s*)(.*?)(?=^(?:{alternation})\s*[：:]|^##\s|\Z)"
    )
    match = pattern.search(plan)
    if not match:
        raise ValueError(f"Reveal 章计划缺少字段：{label}")
    original = match.group(2).rstrip()
    replacement = match.group(1) + original + ("\n" if original else "") + addition.strip() + "\n"
    return plan[: match.start()] + replacement + plan[match.end():]


def inject_mystery_reveals_into_chapter_plan(
    book_id: str,
    chapter_number: int,
    current_chapter_plan: str,
    workspace: Path,
) -> str:
    """Inject only reader-facing reveal events into the scheduled chapter."""

    control = read_mystery_control(book_id, workspace)
    result = current_chapter_plan
    for value in control["reveals"].values():
        contract = _reveal_contract_from_dict(value)
        if contract.reveal_chapter != chapter_number:
            continue
        result = _append_chapter_plan_field(result, "具体剧情", contract.event_atom)
        result = _append_chapter_plan_field(
            result,
            "结果 / 状态变化",
            contract.state_residue + " 更深未知继续保留：" + contract.still_open_after_reveal,
        )
        result = _append_chapter_plan_field(
            result,
            "叙事功能",
            f"[MYSTERY-REVEAL:{contract.mystery_id}] 只兑现本次 Reveal Boundary，不解释更深来源。",
        )
    return result


def advance_mystery_after_reveal(
    book_id: str,
    mystery_id: str,
    *,
    next_decision_trigger: str,
    workspace: Path,
) -> dict[str, Any]:
    directory = require_book(book_id, workspace)
    control = _read_mystery_control(directory)
    thread_value = control["threads"].get(mystery_id)
    reveal_value = control["reveals"].get(mystery_id)
    if not isinstance(thread_value, dict) or not isinstance(reveal_value, dict):
        raise ValueError("Mystery Reveal 尚未准备完成")
    contract = _reveal_contract_from_dict(reveal_value)
    book_text = (directory / "BOOK.md").read_text(encoding="utf-8")
    sections = parse_book_sections(book_text)
    completed_match = re.search(r"当前已完成第\s*(\d+)\s*章", sections["status"])
    completed = int(completed_match.group(1)) if completed_match else 0
    if completed < contract.reveal_chapter:
        raise ValueError(
            f"Mystery Reveal 第{contract.reveal_chapter}章尚未完成并进入 State；当前只完成到第{completed}章"
        )
    next_thread = advance_after_reveal(
        _mystery_thread_from_dict(thread_value),
        contract,
        next_decision_trigger=next_decision_trigger,
    )
    control["threads"][mystery_id] = _mystery_thread_to_dict(next_thread)
    del control["reveals"][mystery_id]
    _write_mystery_control(directory, control)
    return control


def _empty_creative_state() -> dict[str, dict[str, str]]:
    return {
        artifact: {"origin": "empty", "status": "empty"}
        for artifact in CREATIVE_ARTIFACT_FILES
    }


def _read_creative_state(directory: Path) -> dict[str, dict[str, str]]:
    state_path = directory / "CREATIVE_STATE.json"
    if not state_path.is_file():
        return _empty_creative_state()
    try:
        raw = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("CREATIVE_STATE.json 不是有效 JSON") from error
    if not isinstance(raw, dict):
        raise ValueError("CREATIVE_STATE.json 必须是对象")
    state = _empty_creative_state()
    for artifact in state:
        value = raw.get(artifact, {})
        if not isinstance(value, dict):
            raise ValueError(f"CREATIVE_STATE.json 的 {artifact} 状态必须是对象")
        origin = value.get("origin", "empty")
        status = value.get("status", "empty")
        if origin not in CREATIVE_ORIGINS or status not in CREATIVE_STATUSES:
            raise ValueError(f"CREATIVE_STATE.json 的 {artifact} 状态值无效")
        state[artifact] = {"origin": origin, "status": status}
    return state


def _write_creative_state(directory: Path, state: dict[str, dict[str, str]]) -> None:
    normalized = _empty_creative_state()
    for artifact in normalized:
        value = state.get(artifact, {})
        origin = value.get("origin", "empty")
        status = value.get("status", "empty")
        if origin not in CREATIVE_ORIGINS or status not in CREATIVE_STATUSES:
            raise ValueError(f"{artifact} 创意状态值无效")
        normalized[artifact] = {"origin": origin, "status": status}
    (directory / "CREATIVE_STATE.json").write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _read_creative_text(directory: Path, artifact: str) -> str:
    filename = CREATIVE_ARTIFACT_FILES[artifact]
    path = directory / filename
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def read_creative_payload(book_id: str, workspace: Path) -> dict[str, Any]:
    directory = require_book(book_id, workspace)
    state = _read_creative_state(directory)
    contents = {
        artifact: _read_creative_text(directory, artifact)
        for artifact in CREATIVE_ARTIFACT_FILES
    }
    for artifact, content in contents.items():
        if content.strip() and state[artifact]["origin"] == "empty":
            state[artifact] = {"origin": "legacy_unknown", "status": "draft"}
    auxiliary = {
        key: (directory / filename).read_text(encoding="utf-8")
        if (directory / filename).is_file()
        else ""
        for key, filename in CHARACTER_AUX_FILES.items()
    }
    payload: dict[str, Any] = {
        "creative_state": state,
        "mystery_control": _read_mystery_control(directory),
        "creative_artifacts": {
            artifact: {
                "content": contents[artifact],
                **state[artifact],
            }
            for artifact in CREATIVE_ARTIFACT_FILES
        },
        **contents,
        **auxiliary,
        **read_long_form_evolution_payload(directory),
        "world_horizon_handoff": extract_world_horizon_handoff(contents["proposal"]),
    }
    from .premise_workflow import read_premise_payload

    payload["premise"] = read_premise_payload(directory)
    return payload


def invalidate_creative_authorities_for_premise_change(directory: Path) -> None:
    """Reopen only materialized creative authorities when the frozen premise changes."""

    state = _read_creative_state(directory)
    changed = False
    for artifact in CREATIVE_ARTIFACT_FILES:
        content = _read_creative_text(directory, artifact)
        if not content.strip():
            continue
        entry = state[artifact]
        if entry["origin"] == "empty":
            entry["origin"] = "legacy_unknown"
            changed = True
        if entry["status"] != "draft":
            entry["status"] = "draft"
            changed = True
    if changed:
        _write_creative_state(directory, state)


def require_premise_ready_for_authority(directory: Path) -> None:
    """Allow the legacy path only before Premise starts or after explicit skip/approval."""

    from .premise_workflow import read_premise_payload

    premise = read_premise_payload(directory)
    if premise["started_unapproved"]:
        raise ValueError(
            "Premise Aperture 已开始但尚未批准：请让所选候选获得 strict PASS 并批准，或由作者显式跳过"
        )


def _evolution_files(directory: Path, folder: str, prefix: str) -> list[Path]:
    root = directory / folder
    if not root.is_dir():
        return []
    return sorted(path for path in root.glob(f"{prefix}-*.md") if path.is_file())


def _read_evolution_collection(directory: Path, folder: str, prefix: str) -> str:
    return "\n\n".join(
        path.read_text(encoding="utf-8").strip()
        for path in _evolution_files(directory, folder, prefix)
        if path.read_text(encoding="utf-8").strip()
    ).strip()


def read_long_form_evolution_payload(directory: Path) -> dict[str, str]:
    current_path = directory / CURRENT_CHARACTER_FILENAME
    return {
        "world_expansions": _read_evolution_collection(
            directory, WORLD_EXPANSION_DIR, "expansion"
        ),
        "human_development": _read_evolution_collection(
            directory, HUMAN_DEVELOPMENT_DIR, "delta"
        ),
        "current_character": (
            current_path.read_text(encoding="utf-8") if current_path.is_file() else ""
        ),
    }


def _completed_chapter_from_book(directory: Path) -> int:
    book = (directory / "BOOK.md").read_text(encoding="utf-8")
    status = parse_book_sections(book)["status"]
    match = re.search(r"当前已完成第\s*(\d+)\s*章", status)
    return int(match.group(1)) if match else 0


def _strip_model_heading(content: str, heading: str) -> str:
    lines = content.strip().splitlines()
    if lines and lines[0].strip().startswith(heading):
        lines = lines[1:]
    return "\n".join(lines).strip()


def approve_world_expansion(
    book_id: str,
    content: str,
    workspace: Path,
    *,
    scope: str,
    effective_from: int,
    effective_until: int = 0,
    source: str = "author_approved",
) -> dict[str, Any]:
    """Adopt one immutable forward World expansion without rewriting the root World."""

    if scope not in {"macro", "instance"}:
        raise ValueError("World Expansion scope 必须是 macro 或 instance")
    directory = require_book(book_id, workspace)
    completed = _completed_chapter_from_book(directory)
    if effective_from <= completed:
        raise ValueError(
            f"World Expansion 必须向前生效：当前已完成第{completed}章，effective_from 必须更大"
        )
    if effective_until and effective_until < effective_from:
        raise ValueError("World Expansion 的 effective_until 不能早于 effective_from")
    body = _strip_model_heading(content, "# WORLD EXPANSION")
    if not body:
        raise ValueError("World Expansion 内容不能为空")
    world_root = _read_creative_text(directory, "world_vision")
    validate_world_expansion_ruler(body, world_root, scope=scope)
    folder = directory / WORLD_EXPANSION_DIR
    folder.mkdir(exist_ok=True)
    existing = _evolution_files(directory, WORLD_EXPANSION_DIR, "expansion")
    index = len(existing) + 1
    old_collection = _read_evolution_collection(directory, WORLD_EXPANSION_DIR, "expansion")
    text = "\n".join(
        (
            f"# WORLD EXPANSION {index:04d}",
            f"Scope: {scope}",
            f"Effective From Chapter: {effective_from}",
            f"Effective Until Chapter: {effective_until}",
            "",
            body,
        )
    ).strip() + "\n"
    target = folder / f"expansion-{index:04d}.md"
    target.write_text(text, encoding="utf-8")
    new_collection = _read_evolution_collection(directory, WORLD_EXPANSION_DIR, "expansion")
    from .workflow_state import record_content_change

    record_content_change(
        directory,
        "evolution.world",
        old_collection,
        new_collection,
        source=source,
    )
    return {
        "status": "approved",
        "file": str(target.relative_to(directory)),
        "effective_from": effective_from,
        "effective_until": effective_until,
        "scope": scope,
    }


def approve_human_development(
    book_id: str,
    content: str,
    workspace: Path,
    *,
    source: str = "author_approved",
) -> dict[str, Any]:
    """Adopt a source-backed stable Human delta; NONE creates no fake development."""

    directory = require_book(book_id, workspace)
    body = _strip_model_heading(content, "# HUMAN DEVELOPMENT DELTA")
    if not body or body.strip().upper() == "NONE":
        return {"status": "no_change", "file": ""}
    completed = _completed_chapter_from_book(directory)
    folder = directory / HUMAN_DEVELOPMENT_DIR
    folder.mkdir(exist_ok=True)
    existing = _evolution_files(directory, HUMAN_DEVELOPMENT_DIR, "delta")
    index = len(existing) + 1
    old_collection = _read_evolution_collection(directory, HUMAN_DEVELOPMENT_DIR, "delta")
    text = "\n".join(
        (
            f"# HUMAN DEVELOPMENT DELTA {index:04d}",
            f"Evidence Through Chapter: {completed}",
            f"Effective From Chapter: {completed + 1}",
            "",
            body,
        )
    ).strip() + "\n"
    target = folder / f"delta-{index:04d}.md"
    target.write_text(text, encoding="utf-8")
    new_collection = _read_evolution_collection(directory, HUMAN_DEVELOPMENT_DIR, "delta")
    from .workflow_state import record_content_change

    record_content_change(
        directory,
        "evolution.human_development",
        old_collection,
        new_collection,
        source=source,
    )
    return {
        "status": "approved",
        "file": str(target.relative_to(directory)),
        "evidence_through": completed,
        "effective_from": completed + 1,
    }


def refresh_current_character(book_id: str, workspace: Path) -> dict[str, Any]:
    """Compile the current Character deterministically; no future World is visible here."""

    directory = require_book(book_id, workspace)
    book = (directory / "BOOK.md").read_text(encoding="utf-8")
    status = parse_book_sections(book)["status"]
    completed = _completed_chapter_from_book(directory)
    character = _read_creative_text(directory, "character_card")
    if not character.strip():
        raise ValueError("刷新 Current Character 前必须先有已批准 CHARACTER.md")
    evolution = read_long_form_evolution_payload(directory)
    new_content = compile_current_character(
        character_card=character,
        status_text=status,
        human_development=evolution["human_development"],
        chapter_number=completed + 1,
    )
    target = directory / CURRENT_CHARACTER_FILENAME
    old_content = target.read_text(encoding="utf-8") if target.is_file() else ""
    target.write_text(new_content, encoding="utf-8")
    from .workflow_state import record_content_change

    record_content_change(
        directory,
        "evolution.current_character",
        old_content,
        new_content,
        source="deterministic_refresh",
    )
    return {
        "status": "refreshed",
        "file": CURRENT_CHARACTER_FILENAME,
        "compiled_through": completed,
        "content": new_content,
    }


def write_creative_artifact(
    book_id: str,
    artifact: str,
    content: str,
    workspace: Path,
    *,
    origin: str | None = None,
    workflow_source: str = "author_edit",
) -> dict[str, Any]:
    if artifact not in CREATIVE_ARTIFACT_FILES:
        raise ValueError(f"未知创意产物：{artifact}")
    if artifact == "character_card":
        raise ValueError("CHARACTER.md 只能由 Power Seed + Human Seed 确定性合成，不能直接保存")
    directory = require_book(book_id, workspace)
    require_premise_ready_for_authority(directory)
    new_content = str(content)
    reveal_contracts: tuple[MysteryRevealContract, ...] = ()
    if artifact == "proposal":
        reveal_contracts = extract_reveal_contracts(new_content)
        new_content = strip_reveal_contracts(new_content)
        if reveal_contracts:
            save_mystery_reveals(book_id, reveal_contracts, workspace)
    old_content = _read_creative_text(directory, artifact)
    from .workflow_state import ensure_workflow_state

    ensure_workflow_state(directory)
    state = _read_creative_state(directory)
    if old_content != new_content:
        source = origin if origin in {"model_generated", "model_selected"} else "author_edited"
        state[artifact] = {"origin": source, "status": "draft"}
    elif origin in {"model_generated", "model_selected"} and new_content.strip():
        state[artifact] = {"origin": origin, "status": "draft"}
    elif state[artifact]["origin"] == "empty" and new_content.strip():
        state[artifact] = {"origin": "author_edited", "status": "draft"}
    if artifact in {"power_seed", "human_seed"} and old_content != new_content:
        # One Character approval gate freezes both seeds together. Any seed edit reopens
        # the whole Character authority without deleting long-running Character State.
        for seed in ("power_seed", "human_seed"):
            if _read_creative_text(directory, seed).strip() or seed == artifact:
                state[seed]["status"] = "draft"
        old_character = _read_creative_text(directory, "character_card")
        (directory / CREATIVE_ARTIFACT_FILES["character_card"]).write_text("", encoding="utf-8")
        (directory / CHARACTER_AUX_FILES["character_audition"]).write_text("", encoding="utf-8")
        state["character_card"] = {"origin": "empty", "status": "empty"}
        if old_character:
            from .workflow_state import record_content_change

            record_content_change(
                directory,
                "creative.character_card",
                old_character,
                "",
                source="seed_edit",
            )
    (directory / CREATIVE_ARTIFACT_FILES[artifact]).write_text(
        new_content, encoding="utf-8"
    )
    _write_creative_state(directory, state)
    from .workflow_state import record_content_change

    workflow_artifact = (
        "creative.story_program" if artifact == "proposal" else f"creative.{artifact}"
    )
    record_content_change(
        directory,
        workflow_artifact,
        old_content,
        new_content,
        source=workflow_source,
    )
    return read_creative_payload(book_id, workspace)


def approve_creative_artifact(
    book_id: str, artifact: str, workspace: Path
) -> dict[str, Any]:
    if artifact not in CREATIVE_ARTIFACT_FILES:
        raise ValueError(f"未知创意产物：{artifact}")
    if artifact in {"power_seed", "human_seed", "character_card"}:
        raise ValueError("Power/Human 不单独批准；请使用一次 Character 批准同时冻结两份 Seed")
    directory = require_book(book_id, workspace)
    require_premise_ready_for_authority(directory)
    content = _read_creative_text(directory, artifact)
    if not content.strip():
        raise ValueError(f"{CREATIVE_ARTIFACT_FILES[artifact]} 不能为空，无法批准")
    if artifact == "world_vision":
        parse_root_precise_power_ruler(content)
    if artifact == "proposal":
        from .story_event_obligations import parse_story_program_protected_events

        parse_story_program_protected_events(content)
    state = _read_creative_state(directory)
    if state[artifact]["origin"] == "empty":
        state[artifact] = {"origin": "author_edited", "status": "draft"}
    state[artifact]["status"] = "author_approved"
    _write_creative_state(directory, state)
    return read_creative_payload(book_id, workspace)


def _validate_selected_seed(content: str, heading: str, *, label: str) -> None:
    stripped = content.lstrip()
    if not stripped.startswith(heading):
        raise ValueError(f"{label} 必须先由作者从候选中选择/编辑成单独的 `{heading}`")
    candidate_markers = ("# POWER CANDIDATE ", "# HUMAN CANDIDATE ", "# CHARACTER CANDIDATE ")
    if any(marker in content for marker in candidate_markers):
        raise ValueError(f"{label} 仍包含候选批次；批准 Character 前只能保留一个已选择 Seed")


def approve_character_artifact(book_id: str, workspace: Path) -> dict[str, Any]:
    """Freeze Power + Human with one author approval and deterministically compose Character."""

    directory = require_book(book_id, workspace)
    require_premise_ready_for_authority(directory)
    power = _read_creative_text(directory, "power_seed")
    human = _read_creative_text(directory, "human_seed")
    world = _read_creative_text(directory, "world_vision")
    _validate_selected_seed(power, "# POWER SEED", label="POWER_SEED.md")
    _validate_selected_seed(human, "# HUMAN SEED", label="HUMAN_SEED.md")
    validate_human_seed_start(human, world)

    human_parts = split_human_seed_authorities(human)
    character = compose_character_card(power_seed=power, human_seed=human)
    character_path = directory / CREATIVE_ARTIFACT_FILES["character_card"]
    old_character = character_path.read_text(encoding="utf-8") if character_path.is_file() else ""
    character_path.write_text(character, encoding="utf-8")

    state_path = directory / CHARACTER_AUX_FILES["character_initial_state"]
    if not state_path.is_file() or not state_path.read_text(encoding="utf-8").strip():
        state_path.write_text(human_parts["initial_state"], encoding="utf-8")
    (directory / CHARACTER_AUX_FILES["character_audition"]).write_text(
        human_parts["audition_metadata"], encoding="utf-8"
    )

    state = _read_creative_state(directory)
    for seed in ("power_seed", "human_seed"):
        if state[seed]["origin"] == "empty":
            state[seed]["origin"] = "author_edited"
        state[seed]["status"] = "author_approved"
    state["character_card"] = {"origin": "deterministic", "status": "author_approved"}
    _write_creative_state(directory, state)

    from .workflow_state import record_content_change

    record_content_change(
        directory,
        "creative.character_card",
        old_character,
        character,
        source="character_approval",
    )
    return read_creative_payload(book_id, workspace)


def read_book_payload(book_id: str, workspace: Path) -> dict[str, Any]:
    directory = require_book(book_id, workspace)
    book_content = (directory / "BOOK.md").read_text(encoding="utf-8")
    prompt_path = directory / "PROMPTS.md"
    prompt_content = prompt_path.read_text(encoding="utf-8") if prompt_path.is_file() else ""
    sections = parse_book_sections(book_content)
    stored_templates = text_to_prompt_templates(prompt_content)
    prompt_templates = default_prompt_templates()
    prompt_templates.update({
        key: value
        for key, value in stored_templates.items()
        if value.strip()
    })
    from .character_prompts import adapt_split_planning_template

    for mode in ("idea", "outline"):
        prompt_templates[mode] = adapt_split_planning_template(prompt_templates[mode], mode=mode)
    creative = read_creative_payload(book_id, workspace)
    return {
        "book_id": book_id,
        "book_content": book_content,
        "sections": sections,
        "design_sections": parse_design_sections(sections["design"]),
        "prompt_templates": prompt_templates,
        **creative,
        "chapters": sorted(path.name for path in (directory / "chapters").glob("chapter-*.md")),
    }


def write_book(
    book_id: str,
    content: str,
    workspace: Path,
    *,
    source: str = "author_edit",
) -> None:
    directory = require_book(book_id, workspace)
    path = directory / "BOOK.md"
    old_content = path.read_text(encoding="utf-8")
    validate_book_content_for_save(content)
    creative_state = _read_creative_state(directory)
    if creative_state.get("proposal", {}).get("status") == "author_approved":
        from .story_event_obligations import validate_book_registry_against_story_program

        validate_book_registry_against_story_program(
            _read_creative_text(directory, "proposal"), content
        )
    from .workflow_state import ensure_workflow_state

    ensure_workflow_state(directory)
    path.write_text(content, encoding="utf-8")
    from .workflow_state import record_book_change

    record_book_change(directory, old_content, content, source=source)


def write_prompt_templates(book_id: str, templates: dict[str, str], workspace: Path) -> None:
    directory = require_book(book_id, workspace)
    normalized = {
        key: str(templates.get(key, "")) for key in PROMPT_TEMPLATE_LABELS
    }
    (directory / "PROMPTS.md").write_text(
        prompt_templates_to_text(normalized), encoding="utf-8"
    )


def write_proposal(book_id: str, content: str, workspace: Path) -> None:
    write_creative_artifact(book_id, "proposal", content, workspace)


def apply_state_delta_to_book(
    book_content: str, chapter_number: int, state_delta_response: str
) -> str:
    """确定性构造 State Delta v2 的 BOOK 状态区；调用方仍需显式写盘。"""

    if chapter_number < 1:
        raise ValueError("State Delta 应用需要正整数章节编号")
    proposal = parse_state_delta_v2(state_delta_response)
    sections = parse_book_sections(book_content)
    current = parse_canon_memory(sections["status"])
    proposal["persistent_canon"] = preserve_or_require_current_power_position(
        proposal["persistent_canon"],
        current.get("persistent_canon", ""),
    )
    previous = current.get("recent_summaries", "").strip()
    if previous == "当前尚无已完成正文或已批准章节摘要。":
        previous = ""
    summary_text = proposal["chapter_summary"].strip()
    if re.match(rf"^第\s*{chapter_number}\s*章\s*[：:]", summary_text):
        summary = summary_text
    else:
        summary = f"第{chapter_number}章：{summary_text}"
    recent = compact_recent_summaries(
        "\n".join(part for part in (previous, summary) if part).strip()
    )
    open_promises = compact_open_promises(proposal["open_promises"])
    status_content = "\n\n".join(
        (
            f"当前已完成第{chapter_number}章。",
            "## ACTIVE SCENE STATE\n\n" + proposal["active_scene_state"],
            "## PERSISTENT CANON\n\n" + proposal["persistent_canon"],
            "## RECENT SUMMARIES\n\n" + recent,
            "## OPEN PROMISES\n\n" + open_promises,
            "## AUTHOR NOTES\n\n" + current.get("author_notes", ""),
        )
    ).strip()
    status_title = SECTION_TITLES["status"]
    matches = list(re.finditer(rf"(?m)^{re.escape(status_title)}\s*$", book_content))
    if len(matches) != 1:
        raise ValueError(f"BOOK.md 必须且只能包含一个独立一级标题：{status_title}")
    prefix = book_content[: matches[0].start()].rstrip()
    return f"{prefix}\n\n{status_title}\n\n{status_content}\n"


def save_chapter(
    book_id: str,
    chapter_number: int,
    content: str,
    workspace: Path,
    *,
    source: str = "author_edit",
) -> Path:
    directory = require_book(book_id, workspace)
    if chapter_number < 1 or chapter_number > 9999:
        raise ValueError("章节编号必须在 1 到 9999 之间")
    validate_chapter_body_for_save(content)
    target = directory / "chapters" / f"chapter-{chapter_number:04d}.md"
    if target.exists():
        raise ValueError(f"第{chapter_number}章已经存在，请先明确处理已有章节")
    from .workflow_state import ensure_workflow_state

    ensure_workflow_state(directory)
    target.write_text(content, encoding="utf-8")
    from .workflow_state import record_chapter_body_change

    record_chapter_body_change(directory, chapter_number, "", content, source=source)
    return target


def replace_chapter(
    book_id: str,
    chapter_number: int,
    content: str,
    workspace: Path,
    *,
    source: str = "author_edit",
) -> Path:
    directory = require_book(book_id, workspace)
    if chapter_number < 1 or chapter_number > 9999:
        raise ValueError("章节编号必须在 1 到 9999 之间")
    validate_chapter_body_for_save(content)
    target = directory / "chapters" / f"chapter-{chapter_number:04d}.md"
    if not target.is_file():
        raise FileNotFoundError(f"第{chapter_number}章尚未保存，不能编辑")
    from .workflow_state import ensure_workflow_state

    ensure_workflow_state(directory)
    old_content = target.read_text(encoding="utf-8")
    if old_content != content:
        target.write_text(content, encoding="utf-8")
    from .workflow_state import record_chapter_body_change

    record_chapter_body_change(
        directory, chapter_number, old_content, content, source=source
    )
    return target


def read_chapter(book_id: str, chapter_number: int, workspace: Path) -> str:
    directory = require_book(book_id, workspace)
    if chapter_number < 1 or chapter_number > 9999:
        raise ValueError("章节编号必须在 1 到 9999 之间")
    target = directory / "chapters" / f"chapter-{chapter_number:04d}.md"
    if not target.is_file():
        return ""
    return target.read_text(encoding="utf-8")
