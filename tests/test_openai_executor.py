from __future__ import annotations

from types import ModuleType, SimpleNamespace
import sys

from fastapi.testclient import TestClient

import story_mvp.app as app_module
import story_mvp.openai_executor as executor_module
from story_mvp.app import app
from story_mvp.openai_executor import generate_text


class FakeResponses:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(output_text="FAKE OUTPUT")


class FakeClient:
    def __init__(self) -> None:
        self.responses = FakeResponses()


def test_openai_executor_uses_responses_output_text_without_network(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = FakeClient()
    result = generate_text("FULL PROMPT", model="test-model", client=client)

    assert result == {"output_text": "FAKE OUTPUT", "model": "test-model"}
    assert client.responses.calls == [{"model": "test-model", "input": "FULL PROMPT"}]


def test_openai_status_does_not_expose_api_key(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "secret-value")
    monkeypatch.setenv("STORY_MVP_MODEL", "configured-model")
    monkeypatch.setenv("STORY_MVP_STATE_MODEL", "cheap-state-model")
    response = TestClient(app).get("/api/executors")

    assert response.status_code == 200
    assert response.json()["openai_api"] == {
        "available": True,
        "configured": True,
        "model": "configured-model",
        "state_model": "cheap-state-model",
        "authority_reviser_model": "gpt-5.6-luna",
        "authority_reviser_reasoning": "high",
        "batch_primary_model": "gpt-5.6-terra",
        "batch_primary_reasoning": "high",
        "batch_authority_reviser_model": "gpt-5.6-sol",
        "batch_authority_reviser_reasoning": "high",
        "name": "",
    }
    assert "secret-value" not in response.text


def test_openai_endpoint_returns_fake_output_without_saving_artifact(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "configured")
    fake = FakeClient()
    monkeypatch.setattr(
        app_module,
        "generate_text",
        lambda prompt, model="", purpose="default", reasoning_effort="": generate_text(
            prompt, model=model, purpose=purpose, reasoning_effort=reasoning_effort, client=fake
        ),
    )
    response = TestClient(app).post(
        "/api/executors/openai",
        json={"prompt": "FULL PROMPT", "model": "test-model"},
    )

    assert response.status_code == 200
    assert response.json() == {"output_text": "FAKE OUTPUT", "model": "test-model"}


def test_state_extraction_can_use_separate_default_model(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("STORY_MVP_MODEL", "main-model")
    monkeypatch.setenv("STORY_MVP_STATE_MODEL", "cheap-state-model")
    client = FakeClient()

    result = generate_text(
        "STATE PROMPT", purpose="state_extraction", client=client
    )

    assert result["model"] == "cheap-state-model"
    assert client.responses.calls == [
        {"model": "cheap-state-model", "input": "STATE PROMPT"}
    ]


def test_authority_reviser_uses_fixed_luna_high_profile(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("STORY_MVP_AUTHORITY_REVISER_MODEL", raising=False)
    client = FakeClient()

    result = generate_text(
        "REVISER PROMPT",
        model="SHOULD_BE_IGNORED",
        purpose="authority_reviser",
        reasoning_effort="low",
        client=client,
    )

    assert result == {
        "output_text": "FAKE OUTPUT",
        "model": "gpt-5.6-luna",
        "reasoning_effort": "high",
    }
    assert client.responses.calls == [{
        "model": "gpt-5.6-luna",
        "input": "REVISER PROMPT",
        "reasoning": {"effort": "high"},
    }]


def test_batch_authority_reviser_uses_fixed_sol_high_profile(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("STORY_MVP_BATCH_AUTHORITY_REVISER_MODEL", raising=False)
    client = FakeClient()

    result = generate_text(
        "BATCH REVISER PROMPT",
        model="SHOULD_BE_IGNORED",
        purpose="batch_authority_reviser",
        reasoning_effort="low",
        client=client,
    )

    assert result == {
        "output_text": "FAKE OUTPUT",
        "model": "gpt-5.6-sol",
        "reasoning_effort": "high",
    }
    assert client.responses.calls == [{
        "model": "gpt-5.6-sol",
        "input": "BATCH REVISER PROMPT",
        "reasoning": {"effort": "high"},
    }]


def test_openai_endpoint_reports_unconfigured_without_changing_prompt_or_artifact(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = TestClient(app).post(
        "/api/executors/openai",
        json={"prompt": "FULL PROMPT"},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "OPENAI_API_KEY 未配置"


def test_openai_settings_accept_url_and_key_without_echoing_or_persisting_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
    monkeypatch.setattr(executor_module, "_runtime_settings", {"url": "", "api_key": ""})
    persisted: dict[str, str] = {}
    monkeypatch.setattr(
        executor_module,
        "_persist_user_environment",
        lambda name, url, api_key: persisted.update(name=name, url=url, api_key=api_key),
    )
    client = TestClient(app)

    saved = client.put(
        "/api/settings/openai",
        json={"name": "Test Profile", "url": "https://example.test/v1", "api_key": "SECRET_TEST_KEY"},
    )
    assert saved.status_code == 200
    assert saved.json() == {
        "name": "Test Profile",
        "url": "https://example.test/v1",
        "configured": True,
        "source": "memory",
        "persistent": True,
    }
    assert "SECRET_TEST_KEY" not in saved.text
    assert persisted == {
        "name": "Test Profile",
        "url": "https://example.test/v1",
        "api_key": "SECRET_TEST_KEY",
    }
    current = client.get("/api/settings/openai")
    assert current.json() == saved.json()
    assert "SECRET_TEST_KEY" not in current.text


def test_openai_client_receives_runtime_url_and_key(monkeypatch) -> None:
    captured: dict[str, str] = {}

    class FakeOpenAI:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    fake_module = ModuleType("openai")
    fake_module.OpenAI = FakeOpenAI
    monkeypatch.setitem(sys.modules, "openai", fake_module)
    monkeypatch.setattr(
        executor_module,
        "_runtime_settings",
        {"url": "https://example.test/v1", "api_key": "SECRET_TEST_KEY"},
    )

    executor_module._create_client()

    assert captured == {
        "api_key": "SECRET_TEST_KEY",
        "base_url": "https://example.test/v1",
    }
