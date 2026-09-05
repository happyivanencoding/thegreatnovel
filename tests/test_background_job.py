from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

import pytest

from story_mvp.background_job import get_job, stop_job


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def job_root() -> Path:
    # Windows Task Scheduler launches outside AgentDock's private temp ACLs. The
    # supported runtime root is project-local .local, so exercise that real path.
    root = PROJECT_ROOT / ".local" / "pytest-background" / uuid.uuid4().hex
    root.mkdir(parents=True)
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _launcher_env(job_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    src = str(PROJECT_ROOT / "src")
    current = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join([src, *[part for part in current.split(os.pathsep) if part]])
    env["PYTHONIOENCODING"] = "utf-8"
    env["TGN_BACKGROUND_JOBS_ROOT"] = str(job_root)
    return env


def _wait_for_terminal(job_id: str, root: Path, timeout: float = 10.0) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        job = get_job(job_id, root=root, tail_lines=20)
        if job["status"] in {"completed", "failed", "cancelled"}:
            return job
        time.sleep(0.1)
    raise AssertionError(f"background job did not finish: {get_job(job_id, root=root)}")


def test_detached_job_survives_launcher_process_exit(job_root: Path) -> None:
    command = [
        sys.executable,
        "-c",
        "import time; print('BEGIN', flush=True); time.sleep(1.2); print('DONE', flush=True)",
    ]
    launcher = subprocess.run(
        [
            sys.executable,
            "-m",
            "story_mvp.background_job",
            "start",
            "--label",
            "detach-smoke",
            "--",
            *command,
        ],
        cwd=PROJECT_ROOT,
        env=_launcher_env(job_root),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=5,
    )
    assert launcher.returncode == 0, launcher.stderr
    started = json.loads(launcher.stdout)
    assert started["status"] == "queued"

    # The launcher process above is already gone. The independent worker must still
    # finish the child command and persist its result without any polling owner.
    finished = _wait_for_terminal(started["job_id"], job_root)
    assert finished["status"] == "completed"
    assert finished["exit_code"] == 0
    assert finished["stdout_tail"] == ["BEGIN", "DONE"]


def test_background_job_persists_runner_failure(job_root: Path) -> None:
    launcher = subprocess.run(
        [
            sys.executable,
            "-m",
            "story_mvp.background_job",
            "start",
            "--label",
            "failure-smoke",
            "--",
            sys.executable,
            "-c",
            "import sys; print('BROKEN', flush=True); sys.exit(7)",
        ],
        cwd=PROJECT_ROOT,
        env=_launcher_env(job_root),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=5,
    )
    assert launcher.returncode == 0, launcher.stderr
    started = json.loads(launcher.stdout)
    finished = _wait_for_terminal(started["job_id"], job_root)
    assert finished["status"] == "failed"
    assert finished["exit_code"] == 7
    assert finished["error"] == "runner 退出码 7"
    assert finished["stdout_tail"] == ["BROKEN"]


def test_stop_marks_long_job_cancelled(job_root: Path) -> None:
    launcher = subprocess.run(
        [
            sys.executable,
            "-m",
            "story_mvp.background_job",
            "start",
            "--label",
            "cancel-smoke",
            "--",
            sys.executable,
            "-c",
            "import time; print('WAITING', flush=True); time.sleep(30)",
        ],
        cwd=PROJECT_ROOT,
        env=_launcher_env(job_root),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=5,
    )
    assert launcher.returncode == 0, launcher.stderr
    started = json.loads(launcher.stdout)

    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        current = get_job(started["job_id"], root=job_root)
        if current["status"] == "running":
            break
        time.sleep(0.05)
    else:
        raise AssertionError("background worker never reached running state")

    cancelled = stop_job(started["job_id"], root=job_root)
    assert cancelled["status"] == "cancelled"
    assert cancelled["finished_at"]
