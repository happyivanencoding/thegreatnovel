"""ChatGPT 发起的 TGN 长任务后台执行器。

启动命令只负责把一个已经定义好的本地 runner 交给独立 worker；真正任务随后在
本机继续运行，并把状态与日志写入 ``.local/background_jobs``。因此发起它的
ChatGPT turn / AgentDock command session 结束后，不会成为任务继续执行的前提。

它不改变任何小说 Authority / Approval 边界，也不替模型调用选择认证方式；runner
内部若继续使用 ``AgentDockJobManager``，仍走 codex-acp + ChatGPT 登录。
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JOB_ROOT = PROJECT_ROOT / ".local" / "background_jobs"
JOB_FILE = "job.json"
STDOUT_FILE = "stdout.log"
STDERR_FILE = "stderr.log"
WORKER_CMD_FILE = "worker.cmd"
WORKER_BOOTSTRAP_LOG = "worker-bootstrap.log"
TERMINAL_STATUSES = {"completed", "failed", "cancelled"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _job_root() -> Path:
    configured = os.environ.get("TGN_BACKGROUND_JOBS_ROOT", "").strip()
    return Path(configured).resolve() if configured else DEFAULT_JOB_ROOT


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"后台任务状态无效：{path}")
    return value


def _job_directory(job_id: str, *, root: Path | None = None) -> Path:
    base = (root or _job_root()).resolve()
    return base / job_id


def _new_job_id() -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{uuid.uuid4().hex[:8]}"


def _child_env() -> dict[str, str]:
    env = os.environ.copy()
    src = str(PROJECT_ROOT / "src")
    current = env.get("PYTHONPATH", "")
    parts = [item for item in current.split(os.pathsep) if item]
    if src not in parts:
        env["PYTHONPATH"] = os.pathsep.join([src, *parts])
    return env


def _detached_popen(command: Sequence[str], *, cwd: Path) -> subprocess.Popen[Any]:
    kwargs: dict[str, Any] = {
        "cwd": str(cwd),
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "close_fds": True,
        "env": _child_env(),
    }
    if os.name == "nt":
        kwargs["creationflags"] = (
            getattr(subprocess, "DETACHED_PROCESS", 0)
            | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            | getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
    else:
        kwargs["start_new_session"] = True
    return subprocess.Popen(list(command), **kwargs)


def _launch_worker(worker_command: Sequence[str], directory: Path) -> int | None:
    if os.name != "nt":
        worker = _detached_popen(worker_command, cwd=PROJECT_ROOT)
        return worker.pid

    # AgentDock command sessions run inside a Windows Job Object. That Job Object
    # rejects CREATE_BREAKAWAY_FROM_JOB and kills descendants when the tool call
    # ends, so a normal detached Popen is still not persistent. Win32_Process.Create
    # is invoked through WMI/CIM so the worker is created by the OS service rather
    # than by the short-lived AgentDock process tree.
    launcher = directory / WORKER_CMD_FILE
    bootstrap_log = directory / WORKER_BOOTSTRAP_LOG
    src = str(PROJECT_ROOT / "src")
    launcher.write_text(
        "@echo off\n"
        f'set "PYTHONPATH={src};%PYTHONPATH%"\n'
        f'{subprocess.list2cmdline(list(worker_command))} >> "{bootstrap_log}" 2>&1\n',
        encoding="utf-8",
    )
    command_line = subprocess.list2cmdline(["cmd.exe", "/d", "/s", "/c", str(launcher)])
    env = os.environ.copy()
    env["TGN_BACKGROUND_BOOTSTRAP_COMMAND"] = command_line
    script = (
        "$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create "
        "-Arguments @{CommandLine=$env:TGN_BACKGROUND_BOOTSTRAP_COMMAND}; "
        "Write-Output ($r.ReturnValue.ToString() + '|' + $r.ProcessId.ToString())"
    )
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"无法启动 TGN 后台 worker：{result.stderr.strip()[:500]}")
    line = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ""
    try:
        return_value_text, pid_text = line.split("|", 1)
        return_value = int(return_value_text)
        bootstrap_pid = int(pid_text)
    except (ValueError, IndexError) as error:
        raise RuntimeError("Windows 后台 worker 启动结果无法解析") from error
    if return_value != 0:
        raise RuntimeError(f"Windows 后台 worker 启动失败，Win32_Process 返回 {return_value}")
    return bootstrap_pid


def start_job(
    command: Sequence[str],
    *,
    label: str = "",
    cwd: Path | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    clean_command = [str(part) for part in command if str(part)]
    if not clean_command:
        raise ValueError("后台任务 command 不能为空")
    run_cwd = (cwd or PROJECT_ROOT).resolve()
    if not run_cwd.is_dir():
        raise FileNotFoundError(f"后台任务工作目录不存在：{run_cwd}")

    job_id = _new_job_id()
    directory = _job_directory(job_id, root=root)
    directory.mkdir(parents=True, exist_ok=False)
    manifest: dict[str, Any] = {
        "job_id": job_id,
        "label": label.strip() or clean_command[0],
        "status": "queued",
        "created_at": _utc_now(),
        "started_at": None,
        "finished_at": None,
        "worker_pid": None,
        "child_pid": None,
        "exit_code": None,
        "cwd": str(run_cwd),
        "command": clean_command,
        "cancel_requested": False,
        "error": "",
        "stdout_file": STDOUT_FILE,
        "stderr_file": STDERR_FILE,
        "bootstrap_pid": None,
    }
    _write_json(directory / JOB_FILE, manifest)

    worker_command = [
        sys.executable,
        "-m",
        "story_mvp.background_job",
        "_worker",
        "--job-dir",
        str(directory),
    ]
    try:
        bootstrap_pid = _launch_worker(worker_command, directory)
    except Exception as error:
        manifest.update({"status": "failed", "finished_at": _utc_now(), "error": str(error)[:1000]})
        _write_json(directory / JOB_FILE, manifest)
        raise
    manifest["bootstrap_pid"] = bootstrap_pid
    # The worker may already have changed status/pids while the WMI call returned.
    current = _read_json(directory / JOB_FILE)
    current["bootstrap_pid"] = bootstrap_pid
    _write_json(directory / JOB_FILE, current)
    manifest = current
    return manifest


def run_worker(job_directory: Path) -> int:
    directory = job_directory.resolve()
    manifest_path = directory / JOB_FILE
    manifest = _read_json(manifest_path)
    if manifest.get("cancel_requested"):
        manifest.update({"status": "cancelled", "finished_at": _utc_now()})
        _write_json(manifest_path, manifest)
        return 0
    manifest.update({"status": "running", "started_at": _utc_now(), "worker_pid": os.getpid()})
    _write_json(manifest_path, manifest)

    child: subprocess.Popen[Any] | None = None
    try:
        with (directory / STDOUT_FILE).open("ab", buffering=0) as stdout, (directory / STDERR_FILE).open("ab", buffering=0) as stderr:
            child = subprocess.Popen(
                list(manifest["command"]),
                cwd=str(manifest["cwd"]),
                stdin=subprocess.DEVNULL,
                stdout=stdout,
                stderr=stderr,
                env=os.environ.copy(),
            )
            manifest = _read_json(manifest_path)
            manifest["child_pid"] = child.pid
            _write_json(manifest_path, manifest)
            exit_code = child.wait()

        manifest = _read_json(manifest_path)
        manifest["exit_code"] = exit_code
        if manifest.get("cancel_requested"):
            manifest["status"] = "cancelled"
        elif exit_code == 0:
            manifest["status"] = "completed"
        else:
            manifest["status"] = "failed"
            manifest["error"] = f"runner 退出码 {exit_code}"
        manifest["finished_at"] = _utc_now()
        _write_json(manifest_path, manifest)
        return int(exit_code)
    except Exception as error:
        manifest = _read_json(manifest_path)
        manifest.update(
            {
                "status": "cancelled" if manifest.get("cancel_requested") else "failed",
                "finished_at": _utc_now(),
                "error": str(error)[:1000],
            }
        )
        _write_json(manifest_path, manifest)
        return 1


def get_job(job_id: str, *, root: Path | None = None, tail_lines: int = 0) -> dict[str, Any]:
    directory = _job_directory(job_id, root=root)
    manifest = _read_json(directory / JOB_FILE)
    if tail_lines > 0:
        for key, filename in (("stdout_tail", STDOUT_FILE), ("stderr_tail", STDERR_FILE)):
            path = directory / filename
            if path.is_file():
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
                manifest[key] = lines[-tail_lines:]
            else:
                manifest[key] = []
    return manifest


def list_jobs(*, root: Path | None = None) -> list[dict[str, Any]]:
    base = (root or _job_root()).resolve()
    if not base.is_dir():
        return []
    jobs: list[dict[str, Any]] = []
    for directory in base.iterdir():
        path = directory / JOB_FILE
        if not path.is_file():
            continue
        try:
            jobs.append(_read_json(path))
        except (OSError, json.JSONDecodeError, ValueError):
            continue
    return sorted(jobs, key=lambda item: str(item.get("created_at", "")), reverse=True)


def stop_job(job_id: str, *, root: Path | None = None) -> dict[str, Any]:
    directory = _job_directory(job_id, root=root)
    manifest_path = directory / JOB_FILE
    manifest = _read_json(manifest_path)
    if manifest.get("status") in TERMINAL_STATUSES:
        return manifest
    manifest["cancel_requested"] = True
    _write_json(manifest_path, manifest)

    worker_pid = int(manifest.get("worker_pid") or 0)
    if worker_pid > 0:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/PID", str(worker_pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        else:
            try:
                os.killpg(worker_pid, 15)
            except (ProcessLookupError, PermissionError):
                pass
    manifest = _read_json(manifest_path)
    manifest.update({"status": "cancelled", "finished_at": manifest.get("finished_at") or _utc_now()})
    _write_json(manifest_path, manifest)
    return manifest


def _strip_remainder(command: Sequence[str]) -> list[str]:
    values = list(command)
    return values[1:] if values and values[0] == "--" else values


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="story-mvp-background")
    sub = parser.add_subparsers(dest="action", required=True)

    start = sub.add_parser("start", help="启动独立于当前 ChatGPT turn 的本机长任务")
    start.add_argument("--label", default="")
    start.add_argument("--cwd", type=Path, default=PROJECT_ROOT)
    start.add_argument("command", nargs=argparse.REMAINDER)

    status = sub.add_parser("status", help="读取单个后台任务状态")
    status.add_argument("job_id")
    status.add_argument("--tail", type=int, default=12)

    sub.add_parser("list", help="列出本机后台任务")

    stop = sub.add_parser("stop", help="停止后台任务")
    stop.add_argument("job_id")

    worker = sub.add_parser("_worker")
    worker.add_argument("--job-dir", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = _parser().parse_args(list(argv) if argv is not None else None)
    if args.action == "start":
        output = start_job(_strip_remainder(args.command), label=args.label, cwd=args.cwd)
    elif args.action == "status":
        output = get_job(args.job_id, tail_lines=max(0, args.tail))
    elif args.action == "list":
        output = list_jobs()
    elif args.action == "stop":
        output = stop_job(args.job_id)
    else:
        raise SystemExit(run_worker(args.job_dir))
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
