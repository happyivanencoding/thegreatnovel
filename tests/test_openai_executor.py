from __future__ import annotations

from types import SimpleNamespace

from fastapi.testclient import TestClient

import story_mvp.app as app_module
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
