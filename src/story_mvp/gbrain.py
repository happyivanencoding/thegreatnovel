from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


HERMES_COMMAND = Path(r"C:\GoogleDrive\hermes\gbrain")


class GBrainQueryError(RuntimeError):
    """The public GBrain query command could not return usable text."""


def _resolve_command() -> str:
    command = shutil.which("gbrain")
    if command:
        return command
    if HERMES_COMMAND.is_file():
        return str(HERMES_COMMAND)
    raise GBrainQueryError("找不到可用的 gbrain 公共 CLI")


def query_gbrain(text: str) -> str:
    query = text.strip()
    if not query:
        raise ValueError("GBrain 查询不能为空")

    command = _resolve_command()
    try:
        completed = subprocess.run(
            [command, "query", query, "--limit", "8", "--detail", "medium"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=90,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise GBrainQueryError(f"无法完成 GBrain 查询：{error}") from error

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise GBrainQueryError(detail or f"GBrain 查询失败，退出码 {completed.returncode}")
    result = completed.stdout.strip()
    if not result:
        raise GBrainQueryError("GBrain 查询成功但没有返回文本")
    return result
