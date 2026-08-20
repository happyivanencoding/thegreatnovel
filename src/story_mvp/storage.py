from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .prompts import (
    DEFAULT_PROMPT_TEMPLATES,
    parse_canon_memory,
    parse_state_delta_v2,
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
    "fantasy_seed": "Fantasy Seed / 核心幻想种子",
    "world_vision": "World Vision / 世界幻想画像",
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
    "fantasy_seed": "FANTASY_SEED.md",
    "world_vision": "WORLD_VISION.md",
    "proposal": "PROPOSAL.md",
}
CREATIVE_ORIGINS = frozenset(
    {"empty", "model_generated", "model_selected", "author_edited", "legacy_unknown"}
)
CREATIVE_STATUSES = frozenset({"empty", "draft", "author_approved"})

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
        if current_key is not None:
            lines.append(line)
    if current_key is not None:
        templates[current_key] = "\n".join(lines).strip()
    return templates


def default_prompt_templates() -> dict[str, str]:
    return dict(DEFAULT_PROMPT_TEMPLATES)


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
    _write_creative_state(directory, _empty_creative_state())
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


def _empty_creative_state() -> dict[str, dict[str, str]]:
    return {
        artifact: {"origin": "empty", "status": "empty"}
        for artifact in ("fantasy_seed", "world_vision", "proposal")
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
    if contents["proposal"].strip() and state["proposal"]["origin"] == "empty":
        state["proposal"] = {"origin": "legacy_unknown", "status": "draft"}
    for artifact in ("fantasy_seed", "world_vision"):
        if contents[artifact].strip() and state[artifact]["origin"] == "empty":
            state[artifact] = {"origin": "legacy_unknown", "status": "draft"}
    return {
        "creative_state": state,
        "creative_artifacts": {
            artifact: {
                "content": contents[artifact],
                **state[artifact],
            }
            for artifact in CREATIVE_ARTIFACT_FILES
        },
        "fantasy_seed": contents["fantasy_seed"],
        "world_vision": contents["world_vision"],
        "proposal": contents["proposal"],
    }


def write_creative_artifact(
    book_id: str,
    artifact: str,
    content: str,
    workspace: Path,
    *,
    origin: str | None = None,
) -> dict[str, Any]:
    if artifact not in CREATIVE_ARTIFACT_FILES:
        raise ValueError(f"未知创意产物：{artifact}")
    directory = require_book(book_id, workspace)
    new_content = str(content)
    old_content = _read_creative_text(directory, artifact)
    state = _read_creative_state(directory)
    if old_content != new_content:
        source = origin if origin in {"model_generated", "model_selected"} else "author_edited"
        state[artifact] = {"origin": source, "status": "draft"}
    elif origin in {"model_generated", "model_selected"} and new_content.strip():
        state[artifact] = {"origin": origin, "status": "draft"}
    elif state[artifact]["origin"] == "empty" and new_content.strip():
        state[artifact] = {"origin": "author_edited", "status": "draft"}
    (directory / CREATIVE_ARTIFACT_FILES[artifact]).write_text(
        new_content, encoding="utf-8"
    )
    _write_creative_state(directory, state)
    return read_creative_payload(book_id, workspace)


def approve_creative_artifact(
    book_id: str, artifact: str, workspace: Path
) -> dict[str, Any]:
    if artifact not in CREATIVE_ARTIFACT_FILES:
        raise ValueError(f"未知创意产物：{artifact}")
    directory = require_book(book_id, workspace)
    content = _read_creative_text(directory, artifact)
    if not content.strip():
        raise ValueError(f"{CREATIVE_ARTIFACT_FILES[artifact]} 不能为空，无法批准")
    state = _read_creative_state(directory)
    if state[artifact]["origin"] == "empty":
        state[artifact] = {"origin": "author_edited", "status": "draft"}
    state[artifact]["status"] = "author_approved"
    _write_creative_state(directory, state)
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


def write_book(book_id: str, content: str, workspace: Path) -> None:
    directory = require_book(book_id, workspace)
    (directory / "BOOK.md").write_text(content, encoding="utf-8")


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
    previous = current.get("recent_summaries", "").strip()
    if previous == "当前尚无已完成正文或已批准章节摘要。":
        previous = ""
    summary_text = proposal["chapter_summary"].strip()
    if re.match(rf"^第\s*{chapter_number}\s*章\s*[：:]", summary_text):
        summary = summary_text
    else:
        summary = f"第{chapter_number}章：{summary_text}"
    recent = "\n".join(part for part in (previous, summary) if part).strip()
    sections["status"] = "\n\n".join(
        (
            f"当前已完成第{chapter_number}章。",
            "## ACTIVE SCENE STATE\n\n" + proposal["active_scene_state"],
            "## PERSISTENT CANON\n\n" + proposal["persistent_canon"],
            "## RECENT SUMMARIES\n\n" + recent,
            "## OPEN PROMISES\n\n" + proposal["open_promises"],
            "## AUTHOR NOTES\n\n" + current.get("author_notes", ""),
        )
    ).strip()
    return compose_book_content(sections)


def save_chapter(book_id: str, chapter_number: int, content: str, workspace: Path) -> Path:
    directory = require_book(book_id, workspace)
    if chapter_number < 1 or chapter_number > 9999:
        raise ValueError("章节编号必须在 1 到 9999 之间")
    validate_chapter_body_for_save(content)
    target = directory / "chapters" / f"chapter-{chapter_number:04d}.md"
    if target.exists():
        raise ValueError(f"第{chapter_number}章已经存在，请先明确处理已有章节")
    target.write_text(content, encoding="utf-8")
    return target


def read_chapter(book_id: str, chapter_number: int, workspace: Path) -> str:
    directory = require_book(book_id, workspace)
    if chapter_number < 1 or chapter_number > 9999:
        raise ValueError("章节编号必须在 1 到 9999 之间")
    target = directory / "chapters" / f"chapter-{chapter_number:04d}.md"
    if not target.is_file():
        return ""
    return target.read_text(encoding="utf-8")
