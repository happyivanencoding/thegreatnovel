from pathlib import Path

from fastapi.testclient import TestClient

from story_mvp.app import app
from story_mvp.outcome_fidelity import (
    build_explicit_milestone_repair_prompt,
    detect_explicit_milestone_outcome,
    explicit_milestone_realized,
)
from story_mvp.run_ledger import (
    create_or_load_run,
    load_node_prompt,
    retry_node,
    save_node_prompt,
    save_node_response,
)


AUTHORITY_PROMPT = """# Authority

WORLD REALITY AUTHORITY
- 照域者能压住一段街巷。
- 镇海者能改变一场战斗或一座潮关的结果；九垂原不超过数十名。

FROZEN CHAPTER MISSION
状态变化：顾停舟重伤。
上游计划已批准结果（本章必须同时成立；若与已发生 Canon 冲突则 Canon 优先）：顾停舟本人进入镇海，镇海潮兽被压回远潮；回潮楔新增裂痕。
结尾推动力：战后结算。
"""


MISSING_RESPONSE = """# 正式正文
顾停舟以照域正面承住镇海潮兽的冲击，最终将它压回远潮。众人都看见了这一战的分量。"""

REALIZED_RESPONSE = """# 正式正文
持续承压逼过照域极限后，顾停舟的潮炉跨过关口。他本人正式进入镇海。镇海潮兽随后被压回远潮。"""


def test_detects_explicit_milestone_but_does_not_count_battle_level_implication() -> None:
    requirement = detect_explicit_milestone_outcome(AUTHORITY_PROMPT)
    assert requirement is not None
    assert requirement.target == "镇海"
    assert "顾停舟本人进入镇海" in requirement.outcome
    assert not explicit_milestone_realized(MISSING_RESPONSE, requirement)
    assert explicit_milestone_realized(REALIZED_RESPONSE, requirement)


def test_repair_prompt_is_narrow_and_preservation_first() -> None:
    requirement = detect_explicit_milestone_outcome(AUTHORITY_PROMPT)
    assert requirement is not None
    prompt = build_explicit_milestone_repair_prompt(
        AUTHORITY_PROMPT, MISSING_RESPONSE, requirement
    )
    assert "条件性 Outcome Repair" in prompt
    assert "Preservation First" in prompt
    assert "顾停舟本人进入镇海" in prompt
    assert "不新增战斗、考核、资源、功法、仪式" in prompt
    assert MISSING_RESPONSE in prompt


def test_authority_reviser_prepares_one_bounded_retry_and_only_completes_after_realization(
    tmp_path: Path,
) -> None:
    book_dir = tmp_path / "book"
    create_or_load_run(book_dir, 19, writer_mode="curator_primary")
    save_node_prompt(book_dir, 19, "authority_reviser", AUTHORITY_PROMPT)

    first = save_node_response(book_dir, 19, "authority_reviser", MISSING_RESPONSE)
    node = first["nodes"]["authority_reviser"]
    assert node["status"] == "failed"
    assert node["attempts"] == 1
    assert node["repair_reason"] == "missing_explicit_milestone_outcome"
    assert node["required_target"] == "镇海"
    assert "条件性 Outcome Repair" in load_node_prompt(book_dir, 19, "authority_reviser")
    assert (book_dir / "runs" / "chapter-0019" / "authority_reviser_prompt_attempt-1.md").is_file()

    retried = retry_node(book_dir, 19, "authority_reviser")
    assert retried["nodes"]["authority_reviser"]["status"] == "pending"
    assert retried["nodes"]["authority_reviser"]["attempts"] == 2

    second = save_node_response(book_dir, 19, "authority_reviser", REALIZED_RESPONSE)
    node = second["nodes"]["authority_reviser"]
    assert node["status"] == "completed"
    assert node["attempts"] == 2
    assert "repair_reason" not in node
    assert "required_target" not in node


def test_second_failed_repair_does_not_create_an_infinite_retry_loop(tmp_path: Path) -> None:
    book_dir = tmp_path / "book"
    create_or_load_run(book_dir, 19, writer_mode="curator_primary")
    save_node_prompt(book_dir, 19, "authority_reviser", AUTHORITY_PROMPT)
    save_node_response(book_dir, 19, "authority_reviser", MISSING_RESPONSE)
    retry_node(book_dir, 19, "authority_reviser")

    second = save_node_response(book_dir, 19, "authority_reviser", MISSING_RESPONSE)
    node = second["nodes"]["authority_reviser"]
    assert node["status"] == "failed"
    assert node["attempts"] == 2
    assert node["repair_reason"] == "explicit_milestone_repair_failed"
    assert "条件性 Outcome Repair" in load_node_prompt(book_dir, 19, "authority_reviser")


def test_run_api_exposes_prepared_outcome_repair_prompt(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "outcome-api"}).status_code == 201
    assert client.post(
        "/api/books/outcome-api/runs/19",
        json={"writer_mode": "curator_primary", "selected_specialists": []},
    ).status_code == 200
    assert client.put(
        "/api/books/outcome-api/runs/19/nodes/authority_reviser/prompt",
        json={"content": AUTHORITY_PROMPT},
    ).status_code == 200
    response = client.put(
        "/api/books/outcome-api/runs/19/nodes/authority_reviser/response",
        json={"content": MISSING_RESPONSE},
    )
    assert response.status_code == 200
    assert response.json()["nodes"]["authority_reviser"]["repair_reason"] == "missing_explicit_milestone_outcome"

    prompt = client.get(
        "/api/books/outcome-api/runs/19/nodes/authority_reviser/prompt"
    )
    assert prompt.status_code == 200
    assert "条件性 Outcome Repair" in prompt.json()["content"]
    assert "顾停舟本人进入镇海" in prompt.json()["content"]
