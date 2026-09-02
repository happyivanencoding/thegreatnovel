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
DEFAULT_JOB_TIMEOUT_SECONDS = 60 * 60
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
    process: Any = field(default=None, repr=False)

    def public(self, *, include_output: bool, now: float) -> dict[str, Any]:
        finished = self.finished_at or now
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
        }
        if include_output:
            payload["output_text"] = self.output_text
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

    def status(self) -> dict[str, Any]:
        with self._lock:
            active = sum(job.status in {"queued", "running"} for job in self._jobs.values())
        return {"available": self._available(), "transport": "local-acp", "auth": "chatgpt", "mode": "read-only",
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
            process = None
            try:
                process = self._process_factory(self._command(), self.project_root)
                with self._lock:
                    job.process = process
                    cancelled = job.status == "cancelled"
                if cancelled: return
                result = self._execute(process, job)
                with self._lock:
                    if job.status != "cancelled":
                        job.status, job.output_text = "completed", result["output_text"][:MAX_OUTPUT_CHARS]
                        job.usage, job.stop_reason, job.stderr_text = result.get("usage"), result.get("stop_reason", ""), result.get("stderr", "")[:MAX_STDERR_CHARS]
            except Exception as error:
                with self._lock:
                    if job.status != "cancelled": job.status, job.error = "failed", _safe_error(error)
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
        transport = _JsonRpcTransport(process, is_cancelled=lambda: self._cancelled(job.job_id), clock=self._clock,
            rpc_timeout_seconds=self.rpc_timeout_seconds, deadline=deadline)
        transport.request("initialize", {"protocolVersion": 1, "clientCapabilities": {"fs": {"readTextFile": True, "writeTextFile": False}}, "clientInfo": {"name": "tgn-story-mvp", "version": "1.0"}})
        session = transport.request("session/new", {"cwd": str(self.project_root), "mcpServers": []})
        session_id = str(session.get("sessionId", ""))
        if not session_id: raise AgentDockExecutorError("AgentDock ACP 没有返回 sessionId", code="protocol_error", status_code=502)
        transport.request("session/set_config_option", {"sessionId": session_id, "configId": "model", "value": job.model})
        transport.request("session/set_config_option", {"sessionId": session_id, "configId": "reasoning_effort", "value": job.reasoning_effort})
        transport.request("session/set_mode", {"sessionId": session_id, "modeId": "read-only"})
        prompt_timeout = max(0.1, deadline - self._clock())
        result = transport.request(
            "session/prompt",
            {"sessionId": session_id, "prompt": [{"type": "text", "text": job.prompt}]},
            timeout_seconds=prompt_timeout,
        )
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

    def __init__(self, process: Any, *, is_cancelled: Callable[[], bool], clock: Clock, rpc_timeout_seconds: float, deadline: float) -> None:
        self.process, self.is_cancelled, self._clock = process, is_cancelled, clock
        self.rpc_timeout_seconds, self.deadline, self._request_id = rpc_timeout_seconds, deadline, 0
        self._stdout: queue.Queue[Any] = queue.Queue()
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
        update = message.get("params", {}).get("update", {})
        if (update.get("sessionUpdate") or update.get("type")) != "agent_message_chunk": return
        content = update.get("content", {})
        if content.get("type") != "text" or self._output_chars >= MAX_OUTPUT_CHARS:
            return
        remaining = MAX_OUTPUT_CHARS - self._output_chars
        chunk = str(content.get("text", ""))[:remaining]
        if chunk:
            self._chunks.append(chunk)
            self._output_chars += len(chunk)
