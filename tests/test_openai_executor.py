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
    response = TestClient(app).get("/api/executors")

    assert response.status_code == 200
    assert response.json()["openai_api"] == {
        "available": True,
        "configured": True,
        "model": "configured-model",
        "name": "",
    }
    assert "secret-value" not in response.text


def test_openai_endpoint_returns_fake_output_without_saving_artifact(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "configured")
    fake = FakeClient()
    monkeypatch.setattr(app_module, "generate_text", lambda prompt, model="": generate_text(prompt, model=model, client=fake))
    response = TestClient(app).post(
        "/api/executors/openai",
        json={"prompt": "FULL PROMPT", "model": "test-model"},
    )

    assert response.status_code == 200
    assert response.json() == {"output_text": "FAKE OUTPUT", "model": "test-model"}


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
    }
    assert "SECRET_TEST_KEY" not in saved.text
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
