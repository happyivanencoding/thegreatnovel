"""可选的 OpenAI Responses API Executor。

这里只负责把完整 Prompt 交给官方 SDK 并返回 output_text；不会保存 Story Artifact、
修改 Run Ledger 或自动采用任何结果。
"""

from __future__ import annotations

import os
from typing import Any


DEFAULT_OPENAI_MODEL = "gpt-5.6"


class OpenAIExecutorError(RuntimeError):
    def __init__(self, message: str, *, configured: bool) -> None:
        super().__init__(message)
        self.configured = configured


def configured() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY", "").strip())


def default_model() -> str:
    return os.environ.get("STORY_MVP_MODEL", "").strip() or DEFAULT_OPENAI_MODEL


def _create_client() -> Any:
    try:
        from openai import OpenAI
    except ImportError as error:
        raise OpenAIExecutorError(
            "OpenAI Python SDK 未安装，请安装项目依赖", configured=configured()
        ) from error
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def generate_text(prompt: str, *, model: str = "", client: Any = None) -> dict[str, str]:
    if not prompt.strip():
        raise OpenAIExecutorError("Prompt 不能为空", configured=configured())
    if not configured() and client is None:
        raise OpenAIExecutorError("OPENAI_API_KEY 未配置", configured=False)
    executor = client or _create_client()
    try:
        response = executor.responses.create(
            model=model.strip() or default_model(),
            input=prompt,
        )
    except Exception as error:  # SDK errors vary by installed SDK version.
        raise OpenAIExecutorError("OpenAI Responses API 请求失败", configured=True) from error
    output = str(getattr(response, "output_text", "") or "").strip()
    if not output:
        raise OpenAIExecutorError("OpenAI Responses API 没有返回文本", configured=True)
    return {"output_text": output, "model": model.strip() or default_model()}
