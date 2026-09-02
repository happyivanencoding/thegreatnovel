"""受控的本机 AgentDock ACP 文本执行器。

AgentDock 可以读取项目上下文来回答作者已生成的 Prompt，但客户端被固定为
``read-only``：它不能写入小说、Workflow 或本机文件。返回文本只保存在有界的
内存作业表，采用仍完全由作者在现有工作流中显式完成。
"""

from __future__ import annotations

import json
import os
import queue
import re
import shutil
import subprocess
import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

ALLOWED_MODELS = ("gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol")
ALLOWED_EFFORTS = ("low", "medium", "high")
DEFAULT_MODEL = "gpt-5.6-terra"
DEFAULT_EFFORT = "high"
MAX_PROMPT_CHARS = 120_000
MAX_OUTPUT_CHARS = 100_000
MAX_ERROR_CHARS = 1_000
MAX_STDERR_CHARS = 4_000
MAX_COMPLETED_JOBS = 100
MAX_PENDING_JOBS = 8
MAX_ACTIVITY_EVENTS = 64
MAX_PLAN_ENTRIES = 12
MAX_STDOUT_QUEUE_EVENTS = 256
DEFAULT_JOB_TIMEOUT_SECONDS = 60 * 60
PHASE_ORDER = ("queued", "connecting", "configuring", "planning", "working", "composing", "finalizing", "completed")
PHASE_LABELS = {
    "queued": "等待执行",
    "connecting": "建立会话",
    "configuring": "锁定配置",
    "planning": "理解与计划",
    "working": "读取与执行",
    "composing": "组织输出",
    "finalizing": "完整性收尾",
    "completed": "已完成",
    "failed": "执行失败",
    "cancelled": "已取消",
}
FINAL_MESSAGE_PHASES = {"final", "final_answer"}
DEFAULT_RPC_TIMEOUT_SECONDS = 120


class AgentDockExecutorError(RuntimeError):
    def __init__(self, message: str, *, code: str = "agentdock_error", status_code: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code


def resolve_acp_path() -> Path:
    """Resolve only trusted local ACP locations; browser input is never consulted."""
    configured = os.environ.get("TGN_AGENTDOCK_ACP_PATH", "").strip()
    if configured:
        return Path(configured)
    discovered = shutil.which("codex-acp.ps1")
    if discovered:
        return Path(discovered)
    return Path.home() / "AppData" / "Roaming" / "npm" / "codex-acp.ps1"


def resolve_powershell_host() -> str:
    return shutil.which("pwsh.exe") or shutil.which("powershell.exe") or "powershell.exe"


def _safe_public_text(value: object, *, max_chars: int = 180) -> str:
    """Remove paths/commands and keep only bounded, user-facing activity text."""
    text = str(value or "").replace("\r", " ").replace("\n", " ").strip()
    text = re.sub(r"[A-Za-z]:\\[^\s\"']+", "<项目路径>", text)
    text = re.sub(r"(?i)(api[_ -]?key|authorization|bearer|password|secret|token)\s*[=:]\s*\S+", r"\1=<已隐藏>", text)
    text = re.sub(r"\s+", " ", text)
    return text[:max_chars]


def _public_activity_summary(value: object, *, fallback: str) -> str:
    """Map untrusted model/tool prose to a small, non-sensitive activity vocabulary."""
    signal = str(value or "").casefold()
    if any(token in signal for token in ("pytest", " test", "测试", "lint", "compile", "build", "validation", "验证", "check")):
        return "正在运行验证并核对结果"
    if any(token in signal for token in ("screenshot", "browser", "chrome", "playwright", "截图", "界面")):
        return "正在检查界面表现"
    if any(token in signal for token in ("search", "find", "grep", "select-string", "检索", "搜索", "定位")):
        return "正在定位相关上下文与依赖"
    if any(token in signal for token in ("read", "get-content", "open", "读取", "文档", "规则", "上下文")):
        return "正在读取并整理项目上下文"
    if any(token in signal for token in ("git status", "git diff", "git log", "仓库状态", "变更")):
        return "正在核对项目状态与变更边界"
    if any(token in signal for token in ("plan", "reason", "analy", "audit", "review", "计划", "分析", "审计", "约束")):
        return "正在分析任务、约束与执行顺序"
    if any(token in signal for token in ("final", "summar", "整理结果", "最终", "收尾", "输出")):
        return "正在整理最终输出"
    if any(token in signal for token in ("edit", "patch", "implement", "write", "修改", "实现", "重构")):
        return "正在推演实现方案与影响范围"
    return fallback


def _safe_error(error: Exception | str) -> str:
    """Return an actionable but non-sensitive failure description."""
    text = str(error).replace("\r", " ").replace("\n", " ").strip()
    lowered = text.lower()
    if any(token in lowered for token in ("api_key", "authorization", "bearer ", "openai_api_key", "token=")):
        return "AgentDock 请求失败（敏感运行信息已隐藏）"
    text = re.sub(r"[A-Za-z]:\\[^\s\"']+", "<本机路径>", text)
    text = re.sub(r"(?i)(password|secret|token)\s*[=:]\s*\S+", r"\1=<已隐藏>", text)
    return text[:MAX_ERROR_CHARS] or "AgentDock 请求失败"


@dataclass
class AgentDockJob:
    job_id: str
    prompt: str
    model: str
    reasoning_effort: str
    purpose: str
    context_label: str
    book_id: str
    workflow_mode: str
    chapter_number: int
    launch_token: str
    status: str = "queued"
    created_at: float = 0.0
    started_at: float | None = None
    finished_at: float | None = None
    output_text: str = ""
    error: str = ""
    usage: dict[str, Any] | None = None
    stop_reason: str = ""
    stderr_text: str = ""
    phase: str = "queued"
    current_activity: str = "已进入执行队列"
    last_activity_at: float = 0.0
    activity_version: int = 0
    activities: list[dict[str, Any]] = field(default_factory=list)
    plan_entries: list[dict[str, str]] = field(default_factory=list)
    tool_states: dict[str, str] = field(default_factory=dict, repr=False)
    tool_labels: dict[str, str] = field(default_factory=dict, repr=False)
    process: Any = field(default=None, repr=False)

    def public(self, *, include_output: bool, now: float) -> dict[str, Any]:
        finished = self.finished_at or now
        if self.phase in PHASE_ORDER:
            phase_index = PHASE_ORDER.index(self.phase)
        else:
            phase_index = max(
                (PHASE_ORDER.index(activity["phase"]) for activity in self.activities if activity["phase"] in PHASE_ORDER),
                default=0,
            )
        plan_total = len(self.plan_entries)
        plan_completed = sum(entry.get("status") == "completed" for entry in self.plan_entries)
        tool_counts = {
            "total": len(self.tool_states),
            "running": sum(status == "in_progress" for status in self.tool_states.values()),
            "completed": sum(status == "completed" for status in self.tool_states.values()),
            "failed": sum(status == "failed" for status in self.tool_states.values()),
        }
        payload = {
            "job_id": self.job_id, "status": self.status, "model": self.model,
            "reasoning_effort": self.reasoning_effort, "purpose": self.purpose,
            "context_label": self.context_label, "book_id": self.book_id,
            "workflow_mode": self.workflow_mode, "chapter_number": self.chapter_number,
            "launch_token": self.launch_token, "created_at": self.created_at,
            "started_at": self.started_at, "finished_at": self.finished_at,
            "elapsed_seconds": round(max(0.0, finished - (self.started_at or self.created_at)), 2),
            "has_output": bool(self.output_text), "error": self.error, "usage": self.usage,
            "stop_reason": self.stop_reason,
            "phase": self.phase, "phase_label": PHASE_LABELS.get(self.phase, self.phase),
            "phase_index": phase_index, "phase_total": len(PHASE_ORDER),
            "current_activity": self.current_activity,
            "activity_quiet_seconds": round(max(0.0, now - (self.last_activity_at or self.created_at)), 2),
            "activity_version": self.activity_version,
            "activity_count": len(self.activities),
            "plan_entries": [dict(entry) for entry in self.plan_entries],
            "plan_completed": plan_completed, "plan_total": plan_total,
            "tool_counts": tool_counts,
        }
        if include_output:
            payload["output_text"] = self.output_text
            payload["activities"] = [
                {
                    "sequence": activity["sequence"], "kind": activity["kind"],
                    "phase": activity["phase"], "label": activity["label"],
                    "detail": activity.get("detail", ""),
                    "elapsed_seconds": round(max(0.0, activity["at"] - self.created_at), 2),
                }
                for activity in self.activities
            ]
        return payload


ProcessFactory = Callable[[list[str], Path], Any]
Clock = Callable[[], float]


def _default_process_factory(command: list[str], cwd: Path) -> Any:
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
    return subprocess.Popen(command, cwd=str(cwd), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", bufsize=1, creationflags=flags)


def _stop_process(process: Any, *, wait_seconds: float = 2.0) -> None:
    """Terminate cooperatively first, then kill a stuck ACP process."""
    if process is None or process.poll() is not None:
        return
    try:
        process.terminate()
    except (OSError, AttributeError):
        return
    try:
        process.wait(timeout=wait_seconds)
        return
    except (subprocess.TimeoutExpired, AttributeError, TypeError):
        pass
    try:
        process.kill()
    except (OSError, AttributeError):
        return
    try:
        process.wait(timeout=wait_seconds)
    except (subprocess.TimeoutExpired, AttributeError, TypeError):
        pass


class AgentDockJobManager:
    """有界内存作业表；每条作业只能启动一个受限 ACP 子进程。"""
    def __init__(self, project_root: Path, *, acp_path: Path | None = None, powershell_host: str | None = None,
        max_concurrency: int = 1, max_completed_jobs: int = MAX_COMPLETED_JOBS,
        max_pending_jobs: int = MAX_PENDING_JOBS,
        job_timeout_seconds: float = DEFAULT_JOB_TIMEOUT_SECONDS, rpc_timeout_seconds: float = DEFAULT_RPC_TIMEOUT_SECONDS,
        process_factory: ProcessFactory | None = None, executable_exists: Callable[[Path], bool] | None = None,
        clock: Clock | None = None) -> None:
        self.project_root = Path(project_root).resolve()
        self.acp_path = Path(acp_path) if acp_path is not None else resolve_acp_path()
        self.powershell_host = powershell_host or resolve_powershell_host()
        self.max_concurrency = max(1, min(int(max_concurrency), 2))
        self.max_completed_jobs = max(1, int(max_completed_jobs))
        self.max_pending_jobs = max(self.max_concurrency, int(max_pending_jobs))
        self.job_timeout_seconds, self.rpc_timeout_seconds = max(0.1, float(job_timeout_seconds)), max(0.1, float(rpc_timeout_seconds))
        self._process_factory, self._executable_exists, self._clock = process_factory or _default_process_factory, executable_exists or Path.exists, clock or time.monotonic
        self._jobs: dict[str, AgentDockJob] = {}
        self._lock = threading.RLock()
        self._slots = threading.BoundedSemaphore(self.max_concurrency)

    def _record_activity_locked(
        self,
        job: AgentDockJob,
        *,
        phase: str,
        kind: str,
        label: str,
        detail: str = "",
        append: bool = True,
    ) -> None:
        now = self._clock()
        terminal = phase in {"completed", "failed", "cancelled"}
        current_rank = PHASE_ORDER.index(job.phase) if job.phase in PHASE_ORDER else -1
        next_rank = PHASE_ORDER.index(phase) if phase in PHASE_ORDER else current_rank
        if terminal or next_rank >= current_rank:
            job.phase = phase
        clean_label = _safe_public_text(label, max_chars=140) or PHASE_LABELS.get(job.phase, "Agent 正在工作")
        clean_detail = _safe_public_text(detail, max_chars=180)
        job.current_activity = clean_label
        job.last_activity_at = now
        if not append:
            return
        previous = job.activities[-1] if job.activities else None
        if previous and previous["phase"] == job.phase and previous["kind"] == kind and previous["label"] == clean_label and previous.get("detail", "") == clean_detail:
            return
        job.activity_version += 1
        job.activities.append({
            "sequence": job.activity_version,
            "kind": kind,
            "phase": job.phase,
            "label": clean_label,
            "detail": clean_detail,
            "at": now,
        })
        if len(job.activities) > MAX_ACTIVITY_EVENTS:
            del job.activities[:-MAX_ACTIVITY_EVENTS]

    def _record_activity(self, job_id: str, *, phase: str, kind: str, label: str, detail: str = "", append: bool = True) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is not None:
                self._record_activity_locked(job, phase=phase, kind=kind, label=label, detail=detail, append=append)

    @staticmethod
    def _tool_activity_label(kind: str, title: str, status: str) -> str:
        signal = f"{kind} {title}".casefold()
        if any(token in signal for token in ("pytest", "test", "compile", "node --check", "build", "lint")):
            action = "运行验证"
        elif any(token in signal for token in ("screenshot", "browser", "chrome", "playwright", "界面")):
            action = "检查界面表现"
        elif any(token in signal for token in ("search", "find", "select-string", "grep", "rg ")):
            action = "检索相关上下文"
        elif any(token in signal for token in ("read", "get-content", "cat ", "open")):
            action = "读取项目资料"
        elif any(token in signal for token in ("git status", "git diff", "git log")):
            action = "核对项目状态"
        else:
            action = "执行受控工具步骤"
        if status == "completed":
            return f"{action}已完成"
        if status == "failed":
            return f"{action}失败"
        return f"正在{action}"

    def _handle_transport_update(self, job_id: str, message: dict[str, Any]) -> None:
        update = message.get("params", {}).get("update", {})
        update_type = update.get("sessionUpdate") or update.get("type")
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None or job.status == "cancelled":
                return
            if update_type == "plan":
                entries = []
                for index, entry in enumerate(list(update.get("entries") or [])[:MAX_PLAN_ENTRIES]):
                    status = str(entry.get("status", "pending"))
                    if status not in {"pending", "in_progress", "completed", "failed"}:
                        status = "pending"
                    raw_content = entry.get("content", "")
                    if str(raw_content or "").strip():
                        content = _public_activity_summary(raw_content, fallback=f"推进计划步骤 {index + 1}")
                        entries.append({"status": status, "content": content})
                changed = entries != job.plan_entries
                job.plan_entries = entries
                active = next((entry["content"] for entry in entries if entry["status"] == "in_progress"), "")
                completed = sum(entry["status"] == "completed" for entry in entries)
                detail = f"计划 {completed}/{len(entries)}" if entries else ""
                self._record_activity_locked(
                    job, phase="planning", kind="plan", label=active or "Agent 已形成执行计划",
                    detail=detail, append=changed,
                )
                return
            if update_type in {"tool_call", "tool_call_update"}:
                tool_id = str(update.get("toolCallId", ""))
                status = str(update.get("status", "")) or job.tool_states.get(tool_id, "in_progress")
                if status not in {"in_progress", "completed", "failed"}:
                    status = "in_progress"
                kind = str(update.get("kind", ""))
                title = str(update.get("title", ""))
                previous_status = job.tool_states.get(tool_id)
                if tool_id:
                    job.tool_states[tool_id] = status
                    if title:
                        job.tool_labels[tool_id] = self._tool_activity_label(kind, title, "in_progress")
                if title:
                    label = self._tool_activity_label(kind, title, status)
                else:
                    label = job.tool_labels.get(tool_id, "Agent 工具仍在运行")
                    if status == "completed" and label.startswith("正在"):
                        label = f"{label[2:]}已完成"
                    elif status == "failed" and label.startswith("正在"):
                        label = f"{label[2:]}失败"
                self._record_activity_locked(
                    job, phase="working", kind="tool", label=label,
                    detail=f"工具 {sum(value == 'completed' for value in job.tool_states.values())}/{len(job.tool_states)}",
                    append=bool(title) or status != previous_status,
                )
                return
            if update_type == "agent_thought_chunk":
                self._record_activity_locked(
                    job, phase="working", kind="signal", label="正在分析任务与上下文", append=False,
                )
                return
            if update_type == "agent_message_chunk":
                codex_phase = str(update.get("_meta", {}).get("codex", {}).get("phase", ""))
                content = update.get("content", {})
                visible_text = str(content.get("text", "")) if content.get("type") == "text" else ""
                if codex_phase in FINAL_MESSAGE_PHASES:
                    self._record_activity_locked(job, phase="composing", kind="output", label="正在组织最终输出")
                elif visible_text:
                    self._record_activity_locked(
                        job,
                        phase="working",
                        kind="commentary",
                        label=_public_activity_summary(visible_text, fallback="Agent 正在推进当前任务"),
                    )
                else:
                    self._record_activity_locked(job, phase="working", kind="signal", label="Agent 正在汇报当前动作", append=False)
                return
            if update_type in {"usage_update", "session_info_update"}:
                self._record_activity_locked(
                    job, phase=job.phase, kind="signal", label=job.current_activity or "Agent 保持连接", append=False,
                )

    def status(self) -> dict[str, Any]:
        with self._lock:
            active = sum(job.status in {"queued", "running"} for job in self._jobs.values())
        return {"available": self._available(), "transport": "local-acp", "auth_provider": "chatgpt",
            "auth_state": "checked_when_job_starts", "mode": "read-only",
            "models": list(ALLOWED_MODELS), "reasoning_efforts": list(ALLOWED_EFFORTS), "default_model": DEFAULT_MODEL,
            "default_reasoning_effort": DEFAULT_EFFORT, "max_concurrency": self.max_concurrency,
            "max_pending_jobs": self.max_pending_jobs, "active_count": active}

    def create(self, *, prompt: str, model: str = "", reasoning_effort: str = "", purpose: str = "consultation",
        context_label: str = "", book_id: str = "", workflow_mode: str = "", chapter_number: int = 0,
        launch_token: str = "") -> dict[str, Any]:
        clean_prompt, resolved_model, resolved_effort = prompt.strip(), model.strip() or DEFAULT_MODEL, reasoning_effort.strip() or DEFAULT_EFFORT
        if not clean_prompt:
            raise AgentDockExecutorError("Prompt 不能为空", code="validation_error")
        if len(clean_prompt) > MAX_PROMPT_CHARS:
            raise AgentDockExecutorError(f"Prompt 超过 {MAX_PROMPT_CHARS} 字符限制", code="validation_error")
        if resolved_model not in ALLOWED_MODELS:
            raise AgentDockExecutorError("不允许的 AgentDock 模型", code="validation_error")
        if resolved_effort not in ALLOWED_EFFORTS:
            raise AgentDockExecutorError("不允许的 reasoning_effort", code="validation_error")
        if any(len(value.strip()) > limit for value, limit in ((purpose, 80), (context_label, 160), (book_id, 160), (workflow_mode, 80), (launch_token, 120))):
            raise AgentDockExecutorError("AgentDock 作业元数据过长", code="validation_error")
        if chapter_number < 0 or chapter_number > 9999:
            raise AgentDockExecutorError("章节编号超出范围", code="validation_error")
        if not self._available():
            raise AgentDockExecutorError("AgentDock ACP 本机不可用", code="unavailable", status_code=503)
        now = self._clock()
        job = AgentDockJob(uuid.uuid4().hex, clean_prompt, resolved_model, resolved_effort, purpose.strip() or "consultation",
            context_label.strip(), book_id.strip(), workflow_mode.strip(), chapter_number, launch_token.strip(), created_at=now)
        with self._lock:
            pending = sum(existing.status in {"queued", "running"} for existing in self._jobs.values())
            if pending >= self.max_pending_jobs:
                raise AgentDockExecutorError(
                    "AgentDock 作业队列已满，请等待当前作业结束后重试",
                    code="queue_full",
                    status_code=429,
                )
            self._jobs[job.job_id] = job
            self._record_activity_locked(job, phase="queued", kind="queue", label="已进入执行队列")
            self._prune_completed_locked()
        threading.Thread(target=self._run, args=(job.job_id,), daemon=True, name=f"agentdock-{job.job_id[:8]}").start()
        return job.public(include_output=False, now=self._clock())

    def get(self, job_id: str) -> dict[str, Any]:
        with self._lock:
            return self._require_job(job_id).public(include_output=True, now=self._clock())

    def list(self, book_id: str = "") -> list[dict[str, Any]]:
        with self._lock:
            jobs = [job for job in self._jobs.values() if not book_id or job.book_id == book_id]
            return [job.public(include_output=False, now=self._clock()) for job in sorted(jobs, key=lambda item: item.created_at, reverse=True)]

    def cancel(self, job_id: str) -> dict[str, Any]:
        with self._lock:
            job = self._require_job(job_id)
            if job.status in {"completed", "failed", "cancelled"}:
                return job.public(include_output=False, now=self._clock())
            was_queued = job.status == "queued"
            job.status, job.finished_at, process = "cancelled", self._clock(), job.process
            self._record_activity_locked(job, phase="cancelled", kind="terminal", label="任务已取消；没有写入任何内容")
            if was_queued:
                job.prompt = ""
        _stop_process(process)
        return job.public(include_output=False, now=self._clock())

    def close(self) -> None:
        with self._lock:
            active = [job_id for job_id, job in self._jobs.items() if job.status in {"queued", "running"}]
        for job_id in active:
            self.cancel(job_id)

    def _run(self, job_id: str) -> None:
        with self._lock:
            job = self._jobs[job_id]
            if job.status == "cancelled":
                job.prompt = ""
                return
        with self._slots:
            with self._lock:
                if job.status == "cancelled":
                    job.prompt = ""
                    return
                job.status, job.started_at = "running", self._clock()
                self._record_activity_locked(job, phase="connecting", kind="phase", label="已获得执行位，正在启动 Codex ACP")
            process = None
            try:
                process = self._process_factory(self._command(), self.project_root)
                self._record_activity(job_id, phase="connecting", kind="phase", label="ACP 进程已启动，正在建立安全会话")
                with self._lock:
                    job.process = process
                    cancelled = job.status == "cancelled"
                if cancelled: return
                result = self._execute(process, job)
                with self._lock:
                    if job.status != "cancelled":
                        job.status, job.output_text = "completed", result["output_text"][:MAX_OUTPUT_CHARS]
                        job.usage, job.stop_reason, job.stderr_text = result.get("usage"), result.get("stop_reason", ""), result.get("stderr", "")[:MAX_STDERR_CHARS]
                        self._record_activity_locked(job, phase="completed", kind="terminal", label="任务完成，结果等待作者确认")
            except Exception as error:
                with self._lock:
                    if job.status != "cancelled":
                        job.status, job.error = "failed", _safe_error(error)
                        self._record_activity_locked(job, phase="failed", kind="terminal", label="任务失败；没有写入任何内容", detail=job.error)
            finally:
                _stop_process(process)
                with self._lock:
                    job.process = None
                    job.prompt = ""
                    job.finished_at = job.finished_at or self._clock()
                    self._prune_completed_locked()

    def _command(self) -> list[str]:
        return [self.powershell_host, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(self.acp_path)]

    def _available(self) -> bool:
        try: return bool(self._executable_exists(self.acp_path))
        except OSError: return False

    def _execute(self, process: Any, job: AgentDockJob) -> dict[str, Any]:
        deadline = self._clock() + self.job_timeout_seconds
        transport = _JsonRpcTransport(
            process,
            is_cancelled=lambda: self._cancelled(job.job_id),
            clock=self._clock,
            rpc_timeout_seconds=self.rpc_timeout_seconds,
            deadline=deadline,
            on_update=lambda message: self._handle_transport_update(job.job_id, message),
        )
        self._record_activity(job.job_id, phase="connecting", kind="phase", label="正在协商 ACP 协议")
        transport.request("initialize", {"protocolVersion": 1, "clientCapabilities": {"fs": {"readTextFile": True, "writeTextFile": False}}, "clientInfo": {"name": "tgn-story-mvp", "version": "1.0"}})
        self._record_activity(job.job_id, phase="connecting", kind="phase", label="协议已就绪，正在建立 Codex 会话")
        session = transport.request("session/new", {"cwd": str(self.project_root), "mcpServers": []})
        session_id = str(session.get("sessionId", ""))
        if not session_id: raise AgentDockExecutorError("AgentDock ACP 没有返回 sessionId", code="protocol_error", status_code=502)
        self._record_activity(job.job_id, phase="configuring", kind="phase", label="正在锁定模型、推理强度与只读权限")
        transport.request("session/set_config_option", {"sessionId": session_id, "configId": "model", "value": job.model})
        transport.request("session/set_config_option", {"sessionId": session_id, "configId": "reasoning_effort", "value": job.reasoning_effort})
        transport.request("session/set_mode", {"sessionId": session_id, "modeId": "read-only"})
        self._record_activity(job.job_id, phase="planning", kind="phase", label="Agent 已接收完整任务，正在理解与规划")
        prompt_timeout = max(0.1, deadline - self._clock())
        result = transport.request(
            "session/prompt",
            {"sessionId": session_id, "prompt": [{"type": "text", "text": job.prompt}]},
            timeout_seconds=prompt_timeout,
        )
        self._record_activity(job.job_id, phase="finalizing", kind="phase", label="模型已停止生成，正在核对返回完整性")
        output = transport.text().strip()
        if not output: raise AgentDockExecutorError("AgentDock ACP 没有返回文本", code="empty_output", status_code=502)
        return {"output_text": output, "usage": result.get("usage"), "stop_reason": str(result.get("stopReason", "")), "stderr": transport.stderr_text()}

    def _cancelled(self, job_id: str) -> bool:
        with self._lock: return self._jobs[job_id].status == "cancelled"

    def _require_job(self, job_id: str) -> AgentDockJob:
        job = self._jobs.get(job_id)
        if job is None: raise AgentDockExecutorError("AgentDock 作业不存在或服务已重启", code="not_found", status_code=404)
        return job

    def _prune_completed_locked(self) -> None:
        completed = sorted((job for job in self._jobs.values() if job.status in {"completed", "failed", "cancelled"}), key=lambda job: job.finished_at or job.created_at)
        for job in completed[:-self.max_completed_jobs]: self._jobs.pop(job.job_id, None)


class _JsonRpcTransport:
    """Queue-backed JSON-RPC reader that drains both ACP pipes continuously."""
    _END = object()

    def __init__(
        self,
        process: Any,
        *,
        is_cancelled: Callable[[], bool],
        clock: Clock,
        rpc_timeout_seconds: float,
        deadline: float,
        on_update: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        self.process, self.is_cancelled, self._clock = process, is_cancelled, clock
        self.rpc_timeout_seconds, self.deadline, self._request_id = rpc_timeout_seconds, deadline, 0
        self.on_update = on_update or (lambda _message: None)
        # Apply bounded backpressure instead of letting long ACP notification
        # bursts grow process memory without limit. The request loop drains this
        # FIFO continuously, so RPC responses and callbacks are never dropped.
        self._stdout: queue.Queue[Any] = queue.Queue(maxsize=MAX_STDOUT_QUEUE_EVENTS)
        self._chunks: list[str] = []
        self._output_chars = 0
        self._stderr_chunks: list[str] = []
        self._start_reader(process.stdout, self._stdout, False)
        self._start_reader(process.stderr, None, True)

    def request(
        self,
        method: str,
        params: dict[str, Any],
        *,
        timeout_seconds: float | None = None,
    ) -> dict[str, Any]:
        self._request_id += 1
        request_id, started = self._request_id, self._clock()
        request_timeout = self.rpc_timeout_seconds if timeout_seconds is None else max(0.1, float(timeout_seconds))
        request_deadline = min(self.deadline, started + request_timeout)
        self._send({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params})
        while True:
            if self.is_cancelled(): raise AgentDockExecutorError("AgentDock 作业已取消", code="cancelled", status_code=409)
            now = self._clock()
            if now >= self.deadline: raise AgentDockExecutorError("AgentDock 作业超时", code="job_timeout", status_code=504)
            if now >= request_deadline: raise AgentDockExecutorError(f"AgentDock {method} 请求超时", code="rpc_timeout", status_code=504)
            wait_for = max(0.01, min(0.2, self.deadline - now, request_deadline - now))
            try: line = self._stdout.get(timeout=wait_for)
            except queue.Empty:
                if self.process.poll() is not None: raise self._transport_error("AgentDock ACP 子进程已退出", "process_exit", 502)
                continue
            if line is self._END: raise self._transport_error("AgentDock ACP 子进程已退出", "process_exit", 502)
            try: message = json.loads(line)
            except json.JSONDecodeError: continue
            if "id" in message and "method" in message:
                self._deny_callback(message); continue
            self._record_update(message)
            if message.get("id") == request_id:
                if "error" in message: raise self._transport_error(str(message["error"].get("message", "ACP 请求失败")), "rpc_error", 502)
                return dict(message.get("result") or {})

    def text(self) -> str: return "".join(self._chunks)
    def stderr_text(self) -> str: return "".join(self._stderr_chunks)

    def _transport_error(self, message: str, code: str, status_code: int) -> AgentDockExecutorError:
        stderr = _safe_error(self.stderr_text()) if self.stderr_text().strip() else ""
        suffix = f"（ACP 诊断：{stderr[:320]}）" if stderr else ""
        return AgentDockExecutorError(f"{message}{suffix}", code=code, status_code=status_code)

    def _start_reader(self, stream: Any, target: queue.Queue[Any] | None, is_stderr: bool) -> None:
        def read() -> None:
            try:
                for line in iter(stream.readline, ""):
                    if is_stderr:
                        self._stderr_chunks.append(line)
                        while len("".join(self._stderr_chunks)) > MAX_STDERR_CHARS: self._stderr_chunks.pop(0)
                    elif target is not None: target.put(line)
            finally:
                if target is not None: target.put(self._END)
        threading.Thread(target=read, daemon=True, name="agentdock-pipe-reader").start()

    def _send(self, message: dict[str, Any]) -> None:
        self.process.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
        self.process.stdin.flush()

    def _deny_callback(self, message: dict[str, Any]) -> None:
        self._send({"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32601, "message": "TGN AgentDock read-only client denies permission, file, and terminal callbacks"}})

    def _record_update(self, message: dict[str, Any]) -> None:
        if message.get("method") == "session/update":
            self.on_update(message)
        update = message.get("params", {}).get("update", {})
        if (update.get("sessionUpdate") or update.get("type")) != "agent_message_chunk": return
        codex_phase = str(update.get("_meta", {}).get("codex", {}).get("phase", ""))
        if codex_phase not in FINAL_MESSAGE_PHASES:
            return
        content = update.get("content", {})
        if content.get("type") != "text" or self._output_chars >= MAX_OUTPUT_CHARS:
            return
        remaining = MAX_OUTPUT_CHARS - self._output_chars
        chunk = str(content.get("text", ""))[:remaining]
        if chunk:
            self._chunks.append(chunk)
            self._output_chars += len(chunk)
