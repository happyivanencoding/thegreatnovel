from __future__ import annotations

import shutil
import subprocess
import os
from pathlib import Path


HERMES_CLI = Path(r"C:\GoogleDrive\hermes\gbrain\src\cli.ts")
NOVEL_GBRAIN_SCOPE = ",".join(
    ("mechanisms", "contrasts", "syntheses", "prose-controls", "book-dna", "prose-dna", "maps", "arcs")
)


class GBrainQueryError(RuntimeError):
    """The public GBrain query command could not return usable text."""


def resolve_openai_api_key() -> str:
    """Resolve the persisted OpenAI key even when the host process is stale.

    AgentDock / desktop clients can stay alive across Windows environment changes,
    so their process environment may not contain a key that is already persisted in
    the user's or machine's Environment registry key. Keep one deterministic lookup
    here instead of requiring every caller to restart the host application.
    """

    inherited = os.environ.get("OPENAI_API_KEY", "").strip()
    if inherited:
        return inherited
    if os.name != "nt":
        return ""
    try:
        import winreg
    except ImportError:
        return ""

    locations = (
        (winreg.HKEY_CURRENT_USER, r"Environment"),
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
        ),
    )
    for hive, subkey in locations:
        try:
            with winreg.OpenKey(hive, subkey) as key:
                value, _ = winreg.QueryValueEx(key, "OPENAI_API_KEY")
        except OSError:
            continue
        resolved = str(value).strip()
        if resolved:
            return resolved
    return ""


def resolve_command_prefix() -> list[str]:
    command = shutil.which("gbrain")
    if command:
        return [command]
    bun = shutil.which("bun")
    if bun and HERMES_CLI.is_file():
        return [bun, "run", str(HERMES_CLI)]
    raise GBrainQueryError("找不到可用的 gbrain 公共 CLI 或 Bun CLI")


def _run_cli(arguments: list[str]) -> str:
    command = resolve_command_prefix()
    child_env = os.environ.copy()
    if not child_env.get("OPENAI_API_KEY", "").strip():
        persisted_key = resolve_openai_api_key()
        if persisted_key:
            child_env["OPENAI_API_KEY"] = persisted_key
    try:
        completed = subprocess.run(
            command + arguments,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=child_env,
            timeout=90,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise GBrainQueryError(f"无法完成 GBrain 操作：{error}") from error

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise GBrainQueryError(detail or f"GBrain 操作失败，退出码 {completed.returncode}")
    result = completed.stdout.strip()
    if not result:
        raise GBrainQueryError("GBrain 操作成功但没有返回文本")
    return result


def query_gbrain(
    text: str,
    *,
    limit: int = 8,
    detail: str = "medium",
    scope: str | None = NOVEL_GBRAIN_SCOPE,
) -> str:
    query = text.strip()
    if not query:
        raise ValueError("GBrain 查询不能为空")
    if limit < 1:
        raise ValueError("GBrain 查询 limit 必须大于 0")
    if detail not in {"low", "medium", "high"}:
        raise ValueError("GBrain 查询 detail 必须是 low、medium 或 high")
    arguments = ["query", query, "--limit", str(limit), "--detail", detail]
    if scope:
        arguments.extend(["--scope", scope])
    return _run_cli(arguments)


def get_gbrain(slug: str) -> str:
    page_slug = slug.strip()
    if not page_slug:
        raise ValueError("GBrain 页面 slug 不能为空")
    return _run_cli(["get", page_slug])
