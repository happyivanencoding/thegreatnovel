"""可选的 OpenAI Responses API Executor。

这里只负责把完整 Prompt 交给官方 SDK 并返回 output_text；不会保存 Story Artifact、
修改 Run Ledger 或自动采用任何结果。
"""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import urlparse


DEFAULT_OPENAI_MODEL = "gpt-5.6"
DEFAULT_AUTHORITY_REVISER_MODEL = "gpt-5.6-luna"
_runtime_settings = {"name": "", "url": "", "api_key": ""}


class OpenAIExecutorError(RuntimeError):
    def __init__(self, message: str, *, configured: bool) -> None:
        super().__init__(message)
        self.configured = configured


def _runtime_or_environment(name: str) -> str:
    runtime_value = _runtime_settings.get(name, "").strip()
    if runtime_value:
        return runtime_value
    environment_name = "OPENAI_API_KEY" if name == "api_key" else "OPENAI_BASE_URL"
    return os.environ.get(environment_name, "").strip()


def configured() -> bool:
    return bool(_runtime_or_environment("api_key"))


def settings_status() -> dict[str, str | bool]:
    name = _runtime_settings.get("name", "").strip()
    url = _runtime_or_environment("url")
    key = _runtime_or_environment("api_key")
    return {
        "name": name,
        "url": url,
        "configured": bool(key),
        "source": "memory" if _runtime_settings.get("api_key", "").strip() else "environment" if key else "none",
        "persistent": bool(_runtime_settings.get("persistent", False)),
    }


def _persist_user_environment(name: str, url: str, api_key: str) -> None:
    if os.name != "nt":
        raise ValueError("系统环境变量设置目前只支持 Windows")
    import ctypes
    import winreg

    values = {
        "STORY_MVP_API_PROFILE": name,
        "OPENAI_API_KEY": api_key,
    }
    if url:
        values["OPENAI_BASE_URL"] = url
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Environment",
        0,
        winreg.KEY_SET_VALUE,
    ) as environment_key:
        for variable, value in values.items():
            winreg.SetValueEx(environment_key, variable, 0, winreg.REG_SZ, value)
        if not url:
            try:
                winreg.DeleteValue(environment_key, "OPENAI_BASE_URL")
            except FileNotFoundError:
                pass
    try:
        ctypes.windll.user32.SendMessageTimeoutW(
            0xFFFF, 0x001A, 0, "Environment", 0x0002, 1000, None
        )
    except (AttributeError, OSError):
        pass


def configure_settings(name: str, url: str, api_key: str) -> dict[str, str | bool]:
    clean_name = name.strip()
    clean_url = url.strip()
    if not clean_name:
        raise ValueError("配置名称不能为空")
    if clean_url:
        parsed = urlparse(clean_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("API URL 必须是完整的 http(s) URL")
    resolved_key = api_key.strip() or _runtime_or_environment("api_key")
    if not resolved_key:
        raise ValueError("API Key 不能为空")
    _persist_user_environment(clean_name, clean_url, resolved_key)
    _runtime_settings["api_key"] = resolved_key
    _runtime_settings["name"] = clean_name
    _runtime_settings["url"] = clean_url
    _runtime_settings["persistent"] = True
    os.environ["OPENAI_API_KEY"] = resolved_key
    if clean_url:
        os.environ["OPENAI_BASE_URL"] = clean_url
    else:
        os.environ.pop("OPENAI_BASE_URL", None)
    return settings_status()


def default_model() -> str:
    return os.environ.get("STORY_MVP_MODEL", "").strip() or DEFAULT_OPENAI_MODEL


def state_extraction_model() -> str:
    """State Extraction 可单独使用更便宜/更快模型；未配置时安全回退主模型。"""

    return os.environ.get("STORY_MVP_STATE_MODEL", "").strip() or default_model()


def authority_reviser_model() -> str:
    """Authority Reviser 的架构级默认模型；允许环境级运维覆盖，不接受每书模板覆盖。"""

    return os.environ.get("STORY_MVP_AUTHORITY_REVISER_MODEL", "").strip() or DEFAULT_AUTHORITY_REVISER_MODEL


def _create_client() -> Any:
    try:
        from openai import OpenAI
    except ImportError as error:
        raise OpenAIExecutorError(
            "OpenAI Python SDK 未安装，请安装项目依赖", configured=configured()
        ) from error
    kwargs: dict[str, str] = {"api_key": _runtime_or_environment("api_key")}
    base_url = _runtime_or_environment("url")
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def generate_text(
    prompt: str,
    *,
    model: str = "",
    purpose: str = "default",
    reasoning_effort: str = "",
    client: Any = None,
) -> dict[str, str]:
    if not prompt.strip():
        raise OpenAIExecutorError("Prompt 不能为空", configured=configured())
    if not configured() and client is None:
        raise OpenAIExecutorError("OPENAI_API_KEY 未配置", configured=False)
    executor = client or _create_client()
    if purpose == "authority_reviser":
        resolved_model = authority_reviser_model()
        resolved_effort = "high"
    else:
        resolved_model = model.strip() or (
            state_extraction_model() if purpose == "state_extraction" else default_model()
        )
        resolved_effort = reasoning_effort.strip()
    request: dict[str, Any] = {"model": resolved_model, "input": prompt}
    if resolved_effort:
        request["reasoning"] = {"effort": resolved_effort}
    try:
        response = executor.responses.create(**request)
    except Exception as error:  # SDK errors vary by installed SDK version.
        raise OpenAIExecutorError("OpenAI Responses API 请求失败", configured=True) from error
    output = str(getattr(response, "output_text", "") or "").strip()
    if not output:
        raise OpenAIExecutorError("OpenAI Responses API 没有返回文本", configured=True)
    result = {"output_text": output, "model": resolved_model}
    if resolved_effort:
        result["reasoning_effort"] = resolved_effort
    return result
