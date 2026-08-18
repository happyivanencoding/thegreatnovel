from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


HERMES_CLI = Path(r"C:\GoogleDrive\hermes\gbrain\src\cli.ts")


class GBrainQueryError(RuntimeError):
    """The public GBrain query command could not return usable text."""


def resolve_command_prefix() -> list[str]:
    command = shutil.which("gbrain")
    if command:
        return [command]
    bun = shutil.which("bun")
    if bun and HERMES_CLI.is_file():
        return [bun, "run", str(HERMES_CLI)]
    raise GBrainQueryError("找不到可用的 gbrain 公共 CLI 或 Bun CLI")


def query_gbrain(text: str, source: str | None = None) -> str:
    query = text.strip()
    if not query:
        raise ValueError("GBrain 查询不能为空")
    if source:
        raise ValueError("当前已验证的 gbrain query CLI 没有 source 参数")

    command = resolve_command_prefix()
    try:
        completed = subprocess.run(
            command + ["query", query, "--limit", "8", "--detail", "medium"],
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
