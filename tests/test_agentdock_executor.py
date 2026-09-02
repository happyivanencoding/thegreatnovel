from __future__ import annotations

import io
import json
import threading
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import story_mvp.app as app_module
from story_mvp.agentdock_executor import AgentDockExecutorError, AgentDockJobManager
from story_mvp.app import app


class FakeProcess:
    def __init__(self, lines: list[dict]) -> None:
        self.stdin = io.StringIO()
        self.stdout = io.StringIO("".join(json.dumps(line) + "\n" for line in lines))
        self.stderr = io.StringIO()
        self.terminated = False

    def poll(self):
        return 0 if self.terminated else None

    def terminate(self) -> None:
        self.terminated = True


def successful_lines() -> list[dict]:
    return [
        {"id": 1, "result": {"protocolVersion": 1}},
        {"id": 2, "result": {"sessionId": "session-1"}},
        {"id": 3, "result": {}},
        {"id": 4, "result": {}},
        {"id": 5, "result": {}},
        {"method": "session/update", "params": {"update": {"sessionUpdate": "agent_message_chunk", "content": {"type": "text", "text": "模型输出"}}}},
        {"id": 6, "result": {"stopReason": "end_turn", "usage": {"inputTokens": 12}}},
    ]


def wait_for(manager: AgentDockJobManager, job_id: str) -> dict:
    for _ in range(100):
        payload = manager.get(job_id)
        if payload["status"] not in {"queued", "running"}:
            return payload
        time.sleep(0.01)
    raise AssertionError("job did not finish")


def manager_with(lines: list[dict], *, max_concurrency: int = 1) -> AgentDockJobManager:
    return AgentDockJobManager(
        Path.cwd(),
        acp_path=Path("fake-acp.ps1"),
        max_concurrency=max_concurrency,
        executable_exists=lambda _path: True,
        process_factory=lambda _command, _cwd: FakeProcess(lines),
    )


def test_agentdock_job_runs_read_only_acp_and_returns_text() -> None:
    manager = manager_with(successful_lines())
    created = manager.create(prompt="完整 Prompt", model="gpt-5.6-terra", reasoning_effort="high")

    result = wait_for(manager, created["job_id"])

    assert result["status"] == "completed"
    assert result["output_text"] == "模型输出"
    assert result["stop_reason"] == "end_turn"
    assert result["usage"] == {"inputTokens": 12}


def test_agentdock_acp_error_is_readable() -> None:
    manager = manager_with([
        {"id": 1, "result": {"protocolVersion": 1}},
        {"id": 2, "error": {"message": "chatgpt login required"}},
    ])
    result = wait_for(manager, manager.create(prompt="Prompt")["job_id"])

    assert result["status"] == "failed"
    assert "chatgpt login required" in result["error"]


def test_agentdock_cancelled_job_does_not_become_completed() -> None:
    factory_started = threading.Event()
    release_factory = threading.Event()
    manager = AgentDockJobManager(
        Path.cwd(),
        acp_path=Path("fake-acp.ps1"),
        executable_exists=lambda _path: True,
        process_factory=lambda _command, _cwd: (factory_started.set(), release_factory.wait(1), FakeProcess(successful_lines()))[2],
    )
    created = manager.create(prompt="Prompt")
    assert factory_started.wait(1)
    cancelled = manager.cancel(created["job_id"])
    release_factory.set()

    assert cancelled["status"] == "cancelled"
    assert wait_for(manager, created["job_id"])["status"] == "cancelled"


def test_agentdock_rejects_unapproved_model_effort_and_long_prompt() -> None:
    manager = manager_with(successful_lines())

    for kwargs, expected in [
        ({"model": "anything"}, "模型"),
        ({"reasoning_effort": "max"}, "reasoning_effort"),
        ({"prompt": "x" * 120_001}, "超过"),
    ]:
        try:
            manager.create(**{"prompt": "Prompt", **kwargs})
        except Exception as error:
            assert expected in str(error)
        else:
            raise AssertionError("expected validation error")


def test_agentdock_status_counts_queued_jobs_under_concurrency_limit() -> None:
    manager = manager_with(successful_lines(), max_concurrency=1)
    first = manager.create(prompt="first")
    second = manager.create(prompt="second")

    assert manager.status()["max_concurrency"] == 1
    assert {manager.get(first["job_id"])["status"], manager.get(second["job_id"])["status"]} <= {"queued", "running", "completed"}
    assert wait_for(manager, first["job_id"])["status"] == "completed"
    assert wait_for(manager, second["job_id"])["status"] == "completed"


class FakeManager:
    def __init__(self) -> None:
        self.created: dict[str, str] = {}

    def status(self):
        return {"available": True, "auth": "chatgpt_login", "models": ["gpt-5.6-terra"], "active_count": 0}

    def create(self, **payload):
        self.created["job-1"] = payload["prompt"]
        return {"job_id": "job-1", "status": "queued", "model": payload["model"] or "gpt-5.6-terra"}

    def get(self, job_id):
        assert job_id == "job-1"
        return {"job_id": job_id, "status": "completed", "output_text": "fake agent response"}

    def cancel(self, job_id):
        return {"job_id": job_id, "status": "cancelled"}

    def list(self, book_id=""):
        return [{"job_id": "job-1", "book_id": book_id, "status": "completed"}]

    def close(self):
        pass


def test_agentdock_api_status_create_poll_cancel_without_artifact_write(monkeypatch) -> None:
    fake = FakeManager()
    monkeypatch.setattr(app_module, "agentdock_job_manager", fake)
    client = TestClient(app)

    assert client.get("/api/executors/agentdock").json()["auth"] == "chatgpt_login"
    created = client.post("/api/executors/agentdock/jobs", json={
        "prompt": "FULL PROMPT", "model": "gpt-5.6-terra", "book_id": "demo-story",
    })
    assert created.status_code == 200
    assert fake.created == {"job-1": "FULL PROMPT"}
    assert client.get("/api/executors/agentdock/jobs/job-1").json()["output_text"] == "fake agent response"
    assert client.delete("/api/executors/agentdock/jobs/job-1").json()["status"] == "cancelled"
    assert client.get("/api/executors/agentdock/jobs?book_id=demo-story").json()["jobs"][0]["book_id"] == "demo-story"


def test_agentdock_summary_is_bounded_and_full_output_requires_get() -> None:
    manager = manager_with(successful_lines())
    created = manager.create(
        prompt="Prompt", book_id="book", workflow_mode="chapter", chapter_number=7, launch_token="launch-1"
    )
    result = wait_for(manager, created["job_id"])
    summary = manager.list(book_id="book")[0]

    assert result["output_text"] == "模型输出"
    assert "output_text" not in summary
    assert summary["has_output"] is True
    assert summary["workflow_mode"] == "chapter"
    assert summary["chapter_number"] == 7
    assert summary["launch_token"] == "launch-1"


def test_agentdock_command_and_rpc_are_fixed_to_project_read_only_and_no_mcp() -> None:
    captured: dict[str, object] = {}

    def factory(command, cwd):
        process = FakeProcess(successful_lines())
        captured.update(command=command, cwd=cwd, process=process)
        return process

    manager = AgentDockJobManager(
        Path.cwd(), acp_path=Path("trusted-acp.ps1"), powershell_host="pwsh.exe",
        executable_exists=lambda _path: True, process_factory=factory,
    )
    result = wait_for(manager, manager.create(prompt="Prompt")["job_id"])

    assert result["status"] == "completed"
    assert captured["cwd"] == Path.cwd().resolve()
    assert captured["command"] == ["pwsh.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "trusted-acp.ps1"]
    sent = str(captured["process"].stdin.getvalue())
    assert '"mcpServers": []' in sent
    assert '"modeId": "read-only"' in sent


def test_agentdock_denies_callbacks_and_does_not_expose_local_path() -> None:
    lines = successful_lines()
    lines.insert(5, {"jsonrpc": "2.0", "id": "permission-1", "method": "session/request_permission", "params": {}})
    process_holder: list[FakeProcess] = []
    manager = AgentDockJobManager(
        Path.cwd(), acp_path=Path(r"C:\Users\private\secret-acp.ps1"), executable_exists=lambda _path: True,
        process_factory=lambda _command, _cwd: process_holder.append(FakeProcess(lines)) or process_holder[-1],
    )
    result = wait_for(manager, manager.create(prompt="Prompt")["job_id"])

    assert result["status"] == "completed"
    assert "permission" not in manager.status()
    assert "acp_path" not in manager.status()
    assert "denies permission" in process_holder[0].stdin.getvalue()


def test_agentdock_timeout_and_pruning_keep_active_jobs_out_of_history_limit() -> None:
    class BlockingStream:
        def __init__(self): self.release = threading.Event()
        def readline(self): self.release.wait(2); return ""

    class BlockingProcess(FakeProcess):
        def __init__(self):
            super().__init__([])
            self.stdout = BlockingStream()
            self.stderr = BlockingStream()
        def terminate(self):
            self.terminated = True
            self.stdout.release.set()
            self.stderr.release.set()
        def wait(self, timeout=None): return 0

    manager = AgentDockJobManager(
        Path.cwd(), acp_path=Path("fake-acp.ps1"), executable_exists=lambda _path: True,
        process_factory=lambda _command, _cwd: BlockingProcess(), job_timeout_seconds=0.1, rpc_timeout_seconds=0.1,
        max_completed_jobs=1,
    )
    failed = wait_for(manager, manager.create(prompt="Prompt") ["job_id"])
    assert failed["status"] == "failed"
    assert "超时" in failed["error"]
    assert manager.status()["active_count"] == 0


def test_agentdock_api_returns_summary_then_full_output_and_validates_metadata(monkeypatch) -> None:
    manager = manager_with(successful_lines())
    monkeypatch.setattr(app_module, "agentdock_job_manager", manager)
    client = TestClient(app)

    created = client.post("/api/executors/agentdock/jobs", json={
        "prompt": "Prompt", "book_id": "demo", "workflow_mode": "chapter", "chapter_number": 2,
        "launch_token": "launch-2",
    })
    assert created.status_code == 200
    job_id = created.json()["job_id"]
    wait_for(manager, job_id)
    summary = client.get("/api/executors/agentdock/jobs?book_id=demo").json()["jobs"][0]
    full = client.get(f"/api/executors/agentdock/jobs/{job_id}").json()

    assert "output_text" not in summary and summary["has_output"] is True
    assert full["output_text"] == "模型输出"
    assert client.post("/api/executors/agentdock/jobs", json={"prompt": "x", "workflow_mode": "x" * 81}).status_code == 422
    assert client.post("/api/executors/agentdock/jobs", json={"prompt": "x", "purpose": "arbitrary"}).status_code == 422
    assert client.post("/api/executors/agentdock/jobs", json={"prompt": "x", "model": "unapproved"}).status_code == 400
    status = client.get("/api/executors/agentdock").json()
    assert status["transport"] == "local-acp"
    assert "acp_path" not in status and "C:\\Users" not in str(status)


def test_agentdock_prompt_uses_job_deadline_not_short_control_rpc_timeout() -> None:
    class DelayedStream:
        def __init__(self, lines: list[dict], *, delayed_index: int, delay_seconds: float) -> None:
            self.lines = [json.dumps(line) + "\n" for line in lines]
            self.index = 0
            self.delayed_index = delayed_index
            self.delay_seconds = delay_seconds

        def readline(self) -> str:
            if self.index >= len(self.lines):
                return ""
            if self.index == self.delayed_index:
                time.sleep(self.delay_seconds)
            line = self.lines[self.index]
            self.index += 1
            return line

    class DelayedProcess(FakeProcess):
        def __init__(self) -> None:
            super().__init__([])
            self.stdout = DelayedStream(successful_lines(), delayed_index=5, delay_seconds=0.15)

    manager = AgentDockJobManager(
        Path.cwd(),
        acp_path=Path("fake-acp.ps1"),
        executable_exists=lambda _path: True,
        process_factory=lambda _command, _cwd: DelayedProcess(),
        rpc_timeout_seconds=0.05,
        job_timeout_seconds=1.0,
    )

    result = wait_for(manager, manager.create(prompt="long-running prompt")["job_id"])

    assert result["status"] == "completed"
    assert result["output_text"] == "模型输出"


def test_agentdock_rejects_unbounded_pending_queue() -> None:
    factory_started = threading.Event()
    release_factory = threading.Event()

    def factory(_command, _cwd):
        factory_started.set()
        release_factory.wait(1)
        return FakeProcess(successful_lines())

    manager = AgentDockJobManager(
        Path.cwd(),
        acp_path=Path("fake-acp.ps1"),
        executable_exists=lambda _path: True,
        process_factory=factory,
        max_concurrency=1,
        max_pending_jobs=2,
    )
    first = manager.create(prompt="first")
    assert factory_started.wait(1)
    second = manager.create(prompt="second")

    with pytest.raises(AgentDockExecutorError) as captured:
        manager.create(prompt="third")
    assert captured.value.code == "queue_full"
    assert captured.value.status_code == 429
    assert manager.status()["max_pending_jobs"] == 2

    release_factory.set()
    assert wait_for(manager, first["job_id"])["status"] == "completed"
    assert wait_for(manager, second["job_id"])["status"] == "completed"
