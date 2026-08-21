"""章节运行记录 Ledger。

这是一个固定节点的文件记录器，不负责调用 Agent、不负责写 BOOK 或章节正文，
也不抽象成通用 Workflow Engine。Prompt 文件就是节点输入快照；Response 文件
和 manifest 只记录作者已经显式保存的中间产物。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .hybrid_runtime import count_specialist_patches


RUN_NODES = (
    "director",
    "curator",
    "primary",
    "opening",
    "dialogue",
    "action",
    "emotion",
    "integrator",
    "state_delta",
)
SPECIALIST_NODES = ("opening", "dialogue", "action", "emotion")
NODE_STATUSES = frozenset({"pending", "completed", "failed", "skipped", "stale", "adopted"})

_DEPENDENTS = {
    "director": ("curator", "primary", "opening", "dialogue", "action", "emotion", "integrator", "state_delta"),
    "curator": ("primary", "opening", "dialogue", "action", "emotion", "integrator", "state_delta"),
    "primary": ("opening", "dialogue", "action", "emotion", "integrator", "state_delta"),
    "opening": ("integrator", "state_delta"),
    "dialogue": ("integrator", "state_delta"),
    "action": ("integrator", "state_delta"),
    "emotion": ("integrator", "state_delta"),
    "integrator": ("state_delta",),
    "state_delta": (),
}


def _chapter_name(chapter_number: int) -> str:
    if chapter_number < 1 or chapter_number > 9999:
        raise ValueError("章节编号必须在 1 到 9999 之间")
    return f"chapter-{chapter_number:04d}"


def run_directory(book_directory: Path, chapter_number: int) -> Path:
    return book_directory / "runs" / _chapter_name(chapter_number)


def _manifest_path(book_directory: Path, chapter_number: int) -> Path:
    return run_directory(book_directory, chapter_number) / "manifest.json"


def _node_manifest(node: str, status: str = "pending") -> dict[str, Any]:
    return {
        "status": status,
        "attempts": 0,
        "prompt_file": None,
        "response_file": None,
        "prompt_chars": 0,
        "response_chars": 0,
    }


def _write_manifest(path: Path, manifest: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _read_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"无法读取章节 Run manifest：{path}") from error
    if not isinstance(value, dict) or not isinstance(value.get("nodes"), dict):
        raise ValueError(f"章节 Run manifest 结构无效：{path}")
    return value


def create_or_load_run(
    book_directory: Path,
    chapter_number: int,
    *,
    writer_mode: str = "curator_primary",
    selected_specialists: list[str] | None = None,
) -> dict[str, Any]:
    """创建或载入固定节点 Run；已有 manifest 不被覆盖。"""

    if writer_mode not in {
        "single",
        "curator_primary",
        "hybrid_selective",
        "hybrid_full",
    }:
        raise ValueError(f"未知 writer_mode：{writer_mode}")
    requested = selected_specialists
    if requested is None:
        requested = list(SPECIALIST_NODES) if writer_mode == "hybrid_full" else []
    unknown = sorted(set(requested) - set(SPECIALIST_NODES))
    if unknown:
        raise ValueError("未知专项 Agent：" + "、".join(unknown))
    if writer_mode == "curator_primary" and requested:
        raise ValueError(
            "curator_primary 的 Specialist 必须在 Primary 完成后通过 repair endpoint 显式启用"
        )

    manifest_path = _manifest_path(book_directory, chapter_number)
    if manifest_path.is_file():
        return _read_manifest(manifest_path)

    directory = manifest_path.parent
    directory.mkdir(parents=True, exist_ok=True)
    nodes = {node: _node_manifest(node) for node in RUN_NODES}
    for node in SPECIALIST_NODES:
        if node not in requested:
            nodes[node]["status"] = "skipped"
    if writer_mode == "curator_primary":
        nodes["integrator"]["status"] = "skipped"
    manifest = {
        "chapter_number": chapter_number,
        "writer_mode": writer_mode,
        "run_status": "in_progress",
        "selected_specialists": list(requested),
        "final_source": None,
        "nodes": nodes,
    }
    _write_manifest(manifest_path, manifest)
    return manifest


def set_selected_specialists(
    book_directory: Path, chapter_number: int, selected_specialists: list[str]
) -> dict[str, Any]:
    """作者或 Director 建议确定后，更新本章实际运行的专项集合。"""

    unknown = sorted(set(selected_specialists) - set(SPECIALIST_NODES))
    if unknown:
        raise ValueError("未知专项 Agent：" + "、".join(unknown))
    manifest = load_run(book_directory, chapter_number)
    manifest["selected_specialists"] = list(selected_specialists)
    for node in SPECIALIST_NODES:
        node_manifest = _require_node(manifest, node)
        if node in selected_specialists:
            if node_manifest["status"] == "skipped":
                node_manifest["status"] = "pending"
        elif node_manifest["status"] in {"pending", "stale"}:
            node_manifest["status"] = "skipped"
    return _save(manifest, book_directory)


def load_run(book_directory: Path, chapter_number: int) -> dict[str, Any]:
    path = _manifest_path(book_directory, chapter_number)
    if not path.is_file():
        raise FileNotFoundError(f"第{chapter_number}章尚未创建 Run")
    return _read_manifest(path)


def _require_node(manifest: dict[str, Any], node: str) -> dict[str, Any]:
    if node not in RUN_NODES:
        raise ValueError(f"未知固定节点：{node}")
    value = manifest.get("nodes", {}).get(node)
    if not isinstance(value, dict):
        raise ValueError(f"Run 缺少固定节点：{node}")
    return value


def _save(manifest: dict[str, Any], book_directory: Path) -> dict[str, Any]:
    statuses = [info.get("status") for info in manifest.get("nodes", {}).values()]
    if "failed" in statuses:
        manifest["run_status"] = "failed"
    elif (
        manifest.get("final_source")
        and manifest["nodes"]["state_delta"].get("status") == "completed"
        and all(status in {"skipped", "completed", "adopted"} for status in statuses)
    ):
        manifest["run_status"] = "completed"
    else:
        manifest["run_status"] = "in_progress"
    _write_manifest(_manifest_path(book_directory, int(manifest["chapter_number"])), manifest)
    from .workflow_state import sync_run_manifest

    sync_run_manifest(book_directory, manifest)
    return manifest


def _mark_dependents_stale(manifest: dict[str, Any], node: str) -> None:
    visited: set[str] = set()
    queue = list(_DEPENDENTS.get(node, ()))
    while queue:
        child = queue.pop(0)
        if child in visited:
            continue
        visited.add(child)
        child_manifest = _require_node(manifest, child)
        if child_manifest["status"] != "skipped":
            child_manifest["status"] = "stale"
        queue.extend(_DEPENDENTS.get(child, ()))


def save_node_prompt(
    book_directory: Path, chapter_number: int, node: str, prompt: str
) -> dict[str, Any]:
    manifest = load_run(book_directory, chapter_number)
    node_manifest = _require_node(manifest, node)
    if not prompt.strip():
        raise ValueError("节点 Prompt 不能为空")
    path = run_directory(book_directory, chapter_number) / f"{node}_prompt.md"
    path.write_text(prompt, encoding="utf-8")
    if node_manifest["attempts"] == 0:
        node_manifest["attempts"] = 1
    if node_manifest["status"] == "stale" and not node_manifest.get("response_file"):
        node_manifest["status"] = "pending"
    node_manifest["prompt_file"] = path.name
    node_manifest["prompt_chars"] = len(prompt)
    return _save(manifest, book_directory)


def save_node_response(
    book_directory: Path,
    chapter_number: int,
    node: str,
    response: str,
    *,
    status: str = "completed",
) -> dict[str, Any]:
    manifest = load_run(book_directory, chapter_number)
    node_manifest = _require_node(manifest, node)
    if status not in NODE_STATUSES - {"pending", "stale"}:
        raise ValueError(f"不允许的节点响应状态：{status}")
    if not response.strip():
        raise ValueError("节点 Response 不能为空")
    previous_status = node_manifest["status"]
    previous_response = ""
    if node_manifest.get("response_file"):
        old_path = run_directory(book_directory, chapter_number) / node_manifest["response_file"]
        if old_path.is_file():
            previous_response = old_path.read_text(encoding="utf-8")
    attempts = max(1, int(node_manifest.get("attempts", 0)))
    filename = f"{node}_response.md" if attempts == 1 else f"{node}_response_attempt-{attempts}.md"
    path = run_directory(book_directory, chapter_number) / filename
    path.write_text(response, encoding="utf-8")
    node_manifest.update(
        {
            "status": status,
            "attempts": attempts,
            "response_file": path.name,
            "response_chars": len(response),
        }
    )
    if (
        previous_response != response
        and (previous_status in {"completed", "adopted", "failed", "stale"} or attempts > 1)
    ):
        _mark_dependents_stale(manifest, node)
    return _save(manifest, book_directory)


def mark_node_failed(book_directory: Path, chapter_number: int, node: str) -> dict[str, Any]:
    manifest = load_run(book_directory, chapter_number)
    _require_node(manifest, node)["status"] = "failed"
    return _save(manifest, book_directory)


def mark_run_stale(book_directory: Path, chapter_number: int) -> dict[str, Any]:
    """将已有未来 Run 的真实节点整体标记 stale；不触发任何生成。"""

    manifest = load_run(book_directory, chapter_number)
    for info in manifest["nodes"].values():
        if info.get("status") != "skipped":
            info["status"] = "stale"
    return _save(manifest, book_directory)


def mark_node_stale(
    book_directory: Path, chapter_number: int, node: str
) -> dict[str, Any]:
    manifest = load_run(book_directory, chapter_number)
    node_manifest = _require_node(manifest, node)
    if node_manifest.get("status") != "skipped":
        node_manifest["status"] = "stale"
    return _save(manifest, book_directory)


def mark_node_skipped(book_directory: Path, chapter_number: int, node: str) -> dict[str, Any]:
    if node not in SPECIALIST_NODES:
        raise ValueError("只有专项节点可以标记 skipped")
    manifest = load_run(book_directory, chapter_number)
    _require_node(manifest, node)["status"] = "skipped"
    _mark_dependents_stale(manifest, node)
    return _save(manifest, book_directory)


def retry_node(book_directory: Path, chapter_number: int, node: str) -> dict[str, Any]:
    manifest = load_run(book_directory, chapter_number)
    node_manifest = _require_node(manifest, node)
    if node_manifest["status"] not in {"failed", "stale"}:
        raise ValueError("只有 failed 或 stale 节点可以重试")
    if not node_manifest.get("prompt_file"):
        raise ValueError("节点没有已保存 Prompt，不能复用重试")
    node_manifest["attempts"] = max(1, int(node_manifest.get("attempts", 0))) + 1
    node_manifest["status"] = "pending"
    _mark_dependents_stale(manifest, node)
    return _save(manifest, book_directory)


def adopt_final_source(
    book_directory: Path, chapter_number: int, source: str
) -> dict[str, Any]:
    if source not in {"primary", "integrator"}:
        raise ValueError("final_source 只能是 primary 或 integrator")
    manifest = load_run(book_directory, chapter_number)
    source_manifest = _require_node(manifest, source)
    if source_manifest["status"] not in {"completed", "adopted"}:
        raise ValueError(f"节点 {source} 尚未完成，不能采用")
    previous = manifest.get("final_source")
    manifest["final_source"] = source
    source_manifest["status"] = "adopted"
    if previous != source:
        _mark_dependents_stale(manifest, "integrator" if source == "integrator" else "primary")
    return _save(manifest, book_directory)


def should_run_integrator(specialist_responses: Mapping[str, str]) -> bool:
    return any(count_specialist_patches(value) > 0 for value in specialist_responses.values())


def activate_optional_repair(
    book_directory: Path, chapter_number: int, selected_specialists: list[str]
) -> dict[str, Any]:
    """作者在 Primary 完成后显式启用 curator_primary 的局部修复层。"""

    manifest = load_run(book_directory, chapter_number)
    if manifest.get("writer_mode") != "curator_primary":
        raise ValueError("只有 curator_primary Run 可以通过 repair endpoint 启用 Specialist")
    if not selected_specialists:
        raise ValueError("至少需要选择一个 Specialist")
    unknown = sorted(set(selected_specialists) - set(SPECIALIST_NODES))
    if unknown:
        raise ValueError("未知专项 Agent：" + "、".join(unknown))
    primary_status = _require_node(manifest, "primary").get("status")
    if primary_status not in {"completed", "adopted"}:
        raise ValueError("Primary 尚未完成，不能启用 repair Specialist")

    selected = set(selected_specialists)
    manifest["selected_specialists"] = list(selected_specialists)
    for node in SPECIALIST_NODES:
        _require_node(manifest, node)["status"] = (
            "pending" if node in selected else "skipped"
        )
    _require_node(manifest, "integrator")["status"] = "pending"
    return _save(manifest, book_directory)


def skip_integrator_if_no_patches(
    book_directory: Path,
    chapter_number: int,
    specialist_responses: Mapping[str, str],
) -> dict[str, Any]:
    if should_run_integrator(specialist_responses):
        return load_run(book_directory, chapter_number)
    manifest = load_run(book_directory, chapter_number)
    _require_node(manifest, "integrator")["status"] = "skipped"
    return _save(manifest, book_directory)


def next_actionable_node(book_directory: Path, chapter_number: int) -> str | None:
    manifest = load_run(book_directory, chapter_number)
    for node in RUN_NODES:
        if _require_node(manifest, node)["status"] in {"pending", "failed", "stale"}:
            return node
    return None
