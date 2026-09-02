from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from story_mvp.app import app
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.premise_workflow import (
    approve_premise,
    read_premise_payload,
    record_premise_compiler_input,
    save_premise_candidates,
    save_premise_compiler_report,
    save_selected_premise,
    skip_premise,
)
from story_mvp.storage import (
    approve_creative_artifact,
    create_book,
    read_creative_payload,
    write_creative_artifact,
)
from story_mvp.workflow_state import workflow_status


WORLD = """# PROTAGONIST-BLIND WORLD VISION

## 世界核心幻想
WORLD_AUTHORITY

## 力量体系与正常值
公开行动者按灯阶比较，未点灯者是普通公开类别。

### 精确力量主尺｜Frozen Grammar
主尺类型：连续数字
主尺名称：灯阶
精确位置格式：灯阶{N}级
数字精度规则：1—72，每1级可记录
当前可见范围：灯阶1级—灯阶36级
当前大档位：NONE

## T0 通用位置
未点灯者为灯阶1级之前的公开普通类别，不是主角专属例外。
"""


def candidate(number: int) -> str:
    sid = f"S{number}"
    return f"""## {sid}｜候选{number}
### 一句话货架简介
SHELF_{sid}：主角以非标准存在方式改变战斗。
### World-only Direction
WORLD_{sid}：所有城市每天都会公开重排一条街。
### World Interface-only Direction
WORLD_INTERFACE_{sid}：每次重排都会被全城钟楼公开记录。
### Protagonist Ontology-only Direction
ONTOLOGY_{sid}：主角是一扇不能恢复人形的活门。
### Initial Origin-only Direction
ORIGIN_{sid}：他在废屋门槛上醒来，第一场事件前没有训练经历。
### Initial Scale Position-only Direction
SCALE_{sid}：公共主尺灯阶 1—72；T0 为未点灯公开类别。
### Power-only Direction
POWER_{sid}：只有完整穿过门槛的封闭空间才能被吞入；唯一真实门是载体。
### Story Interface / Opening Promise
STORY_{sid}：第一章全城钟楼把他吞下房间的动作公开重映。
### Authority-Compilation Trace
TRACE_{sid}：封闭空间完整过门，钟楼只记录，不替 Power 搬运。
### 第一章标志性画面
IMAGE_{sid}：一间棚屋完整穿门后消失。
### 主角反复会做的新动作
VERBS_{sid}：吞下房间；把门槛变成战场边界。
### 第一次不公平兑现
PAYOFF_{sid}：从同一扇门吐回完整棚屋。
### 20章玩法扩张
TWENTY_{sid}：逐级吞入更大的完整壳体。
### 100章以上仍能长出的不同故事
HUNDRED_{sid}：不同世界争夺谁能进入、居住或控制出口。
### 最小可信桥梁
BRIDGE_{sid}：目标其余出口必须先封死。
### 不可磨平的三点
IMMUTABLE_{sid}：非人活门；过门即战斗；身体成长改变关系。
"""


CANDIDATES = "# SINGLE-PASS PREMISE CANDIDATES\n\n" + "\n\n".join(
    candidate(number) for number in (1, 2, 3)
)


def batch_report(*, s1: str = "PASS", s2: str = "PASS", s3: str = "FAIL") -> str:
    return f"""# PREMISE AUTHORITY COMPILER
## S1
- Verdict: {s1}
- Opening legality: closed
- Scale legality: closed
- Long-form legality: closed
## S2
- Verdict: {s2}
- Opening legality: closed
- Scale legality: closed
- Long-form legality: closed
## S3
- Verdict: {s3}
- Opening legality: conflict
- Scale legality: conflict
- Long-form legality: conflict
## Author-facing result
只返回状态，不选择。
"""


def selected_report(candidate_id: str, verdict: str = "PASS") -> str:
    return f"""# SELECTED PREMISE AUTHORITY COMPILER
## {candidate_id}
- Verdict: {verdict}
- Opening legality: closed
- Scale legality: closed
- Long-form legality: closed
- Remaining hidden bridges: none
- Protected creative core: preserved
"""


def save_batch_compiler(directory: Path, report: str | None = None) -> dict[str, object]:
    record_premise_compiler_input(directory, scope="candidates")
    return save_premise_compiler_report(directory, report or batch_report())


def save_selected_compiler(
    directory: Path, report: str | None = None
) -> dict[str, object]:
    record_premise_compiler_input(directory, scope="selected")
    return save_premise_compiler_report(directory, report or selected_report("S2"))


def test_optional_path_remains_available_until_premise_starts(tmp_path: Path) -> None:
    create_book("legacy-open", tmp_path)

    write_creative_artifact("legacy-open", "world_vision", WORLD, tmp_path)
    payload = read_creative_payload("legacy-open", tmp_path)

    assert payload["premise"]["status"] == "not_started"
    assert payload["creative_state"]["world_vision"]["status"] == "draft"


def test_started_premise_blocks_authority_until_approved_or_skipped(tmp_path: Path) -> None:
    create_book("blocked", tmp_path)
    directory = tmp_path / "blocked"
    save_premise_candidates(directory, CANDIDATES)

    with pytest.raises(ValueError, match="已开始但尚未批准"):
        write_creative_artifact("blocked", "world_vision", WORLD, tmp_path)

    skipped = skip_premise(directory)
    assert skipped["status"] == "skipped"
    write_creative_artifact("blocked", "world_vision", WORLD, tmp_path)


def test_batch_compiler_plus_author_selection_builds_four_lane_contracts(tmp_path: Path) -> None:
    create_book("freeze", tmp_path)
    directory = tmp_path / "freeze"
    save_premise_candidates(directory, CANDIDATES)
    save_batch_compiler(directory)
    selected = candidate(2)
    saved = save_selected_premise(directory, selected)

    assert saved["can_approve"] is True
    approved = approve_premise(directory)

    assert approved["status"] == "approved"
    assert approved["selected_id"] == "S2"
    assert "WORLD_S2" in approved["contracts"]["world"]
    assert "ONTOLOGY_S2" not in approved["contracts"]["world"]
    assert "ONTOLOGY_S2" in approved["contracts"]["power"]
    assert "POWER_S2" in approved["contracts"]["power"]
    assert "WORLD_S2" not in approved["contracts"]["power"]
    assert "ONTOLOGY_S2" in approved["contracts"]["human"]
    assert "POWER_S2" not in approved["contracts"]["human"]
    assert "STORY_S2" in approved["contracts"]["story"]
    assert (directory / "PREMISE_CONTRACT.md").is_file()
    assert all((directory / filename).is_file() for filename in (
        "PREMISE_WORLD_CONTRACT.md",
        "PREMISE_POWER_CONTRACT.md",
        "PREMISE_HUMAN_CONTRACT.md",
        "PREMISE_STORY_CONTRACT.md",
    ))


def test_selected_edit_requires_selected_recompile(tmp_path: Path) -> None:
    create_book("recompile", tmp_path)
    directory = tmp_path / "recompile"
    save_premise_candidates(directory, CANDIDATES)
    save_batch_compiler(directory)
    edited = candidate(2).replace("BRIDGE_S2", "AUTHOR_EDITED_BRIDGE_S2")
    payload = save_selected_premise(directory, edited)

    assert payload["selected_verdict"] == "PASS"
    assert payload["compiled_input_matches"] is False
    assert payload["can_approve"] is False
    with pytest.raises(ValueError, match="重新独立编译"):
        approve_premise(directory)

    save_selected_compiler(directory)
    assert approve_premise(directory)["approved"] is True


def test_compiler_report_requires_prompt_time_snapshot(tmp_path: Path) -> None:
    create_book("missing-snapshot", tmp_path)
    directory = tmp_path / "missing-snapshot"
    save_premise_candidates(directory, CANDIDATES)

    with pytest.raises(ValueError, match="Input snapshot"):
        save_premise_compiler_report(directory, batch_report())


def test_edit_after_selected_prompt_keeps_old_snapshot_and_blocks_approval(
    tmp_path: Path,
) -> None:
    create_book("prompt-race", tmp_path)
    directory = tmp_path / "prompt-race"
    save_premise_candidates(directory, CANDIDATES)
    save_selected_premise(directory, candidate(2))
    record_premise_compiler_input(directory, scope="selected")

    edited = candidate(2).replace("BRIDGE_S2", "CHANGED_AFTER_PROMPT_S2")
    save_selected_premise(directory, edited)
    payload = save_premise_compiler_report(directory, selected_report("S2"))

    assert payload["selected_verdict"] == "PASS"
    assert payload["compiled_input_matches"] is False
    assert payload["can_approve"] is False
    with pytest.raises(ValueError, match="重新独立编译"):
        approve_premise(directory)


def test_conditional_pass_and_fail_never_authorize_approval(tmp_path: Path) -> None:
    create_book("fail", tmp_path)
    directory = tmp_path / "fail"
    save_premise_candidates(directory, CANDIDATES)
    save_selected_premise(directory, candidate(2))
    payload = save_selected_compiler(
        directory, selected_report("S2", verdict="CONDITIONAL PASS")
    )

    assert payload["can_approve"] is False
    with pytest.raises(ValueError, match="strict PASS"):
        approve_premise(directory)


def test_world_approval_freezes_premise_decision(tmp_path: Path) -> None:
    create_book("immutable", tmp_path)
    directory = tmp_path / "immutable"
    skip_premise(directory)
    write_creative_artifact("immutable", "world_vision", WORLD, tmp_path)
    approve_creative_artifact("immutable", "world_vision", tmp_path)

    with pytest.raises(ValueError, match="Premise 决定已冻结"):
        save_premise_candidates(directory, CANDIDATES)


def test_approving_premise_marks_existing_world_draft_stale(tmp_path: Path) -> None:
    create_book("stale-world", tmp_path)
    directory = tmp_path / "stale-world"
    write_creative_artifact("stale-world", "world_vision", WORLD, tmp_path)
    assert workflow_status(directory)["artifacts"]["creative.world_vision"]["status"] == "DRAFT"

    save_premise_candidates(directory, CANDIDATES)
    save_batch_compiler(directory)
    save_selected_premise(directory, candidate(2))
    approve_premise(directory)

    state = workflow_status(directory)
    assert state["artifacts"]["creative.world_vision"]["status"] == "STALE"
    assert "premise.contract" in state["artifacts"]["creative.world_vision"]["stale_from"]


def test_prompt_api_exposes_forge_compiler_and_started_gate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "api-premise"}).status_code == 201

    forge = client.post(
        "/api/prompt",
        json={
            "book_id": "api-premise",
            "mode": "premise_forge",
            "creative_direction": "大胆快节奏玄幻",
        },
    )
    assert forge.status_code == 200
    assert "SINGLE-PASS PREMISE CANDIDATES" in forge.json()["prompt"]

    assert client.put(
        "/api/books/api-premise/premise/candidates",
        json={"content": CANDIDATES},
    ).status_code == 200
    blocked = client.post(
        "/api/prompt",
        json={"book_id": "api-premise", "mode": "world_vision"},
    )
    assert blocked.status_code == 400
    assert "strict PASS" in blocked.json()["detail"]

    compiler = client.post(
        "/api/prompt",
        json={"book_id": "api-premise", "mode": "premise_compiler"},
    )
    assert compiler.status_code == 200
    assert "PREMISE AUTHORITY COMPILER" in compiler.json()["prompt"]

    assert client.put(
        "/api/books/api-premise/premise/selected",
        json={"content": candidate(2)},
    ).status_code == 200
    selected_compiler = client.post(
        "/api/prompt",
        json={
            "book_id": "api-premise",
            "mode": "premise_compiler",
            "premise_compiler_scope": "selected",
        },
    )
    assert selected_compiler.status_code == 200
    selected_prompt = selected_compiler.json()["prompt"]
    assert "SELECTED PREMISE AUTHORITY COMPILER" in selected_prompt
    assert "## S2｜候选2" in selected_prompt
    assert "## S1｜候选1" not in selected_prompt


def test_prompt_api_refuses_new_premise_after_world_approval(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "world-frozen"}).status_code == 201
    assert client.post("/api/books/world-frozen/premise/skip").status_code == 200
    assert client.put(
        "/api/books/world-frozen/world-vision",
        json={"content": WORLD},
    ).status_code == 200
    assert client.post("/api/books/world-frozen/world-vision/approve").status_code == 200

    response = client.post(
        "/api/prompt",
        json={"book_id": "world-frozen", "mode": "premise_forge"},
    )
    assert response.status_code == 400
    assert "Premise 决定已冻结" in response.json()["detail"]


def test_approved_contracts_enter_only_their_authority_lanes(tmp_path: Path) -> None:
    create_book("prompts", tmp_path)
    directory = tmp_path / "prompts"
    save_premise_candidates(directory, CANDIDATES)
    save_batch_compiler(directory)
    save_selected_premise(directory, candidate(2))
    premise = approve_premise(directory)
    contracts = premise["contracts"]

    world_prompt = generate_split_prompt(
        mode="world_vision",
        creative_direction="方向",
        premise_world_contract=contracts["world"],
    )
    assert "WORLD_S2" in world_prompt
    assert "ONTOLOGY_S2" not in world_prompt
    assert "POWER_S2" not in world_prompt

    state = {"world_vision": {"status": "author_approved"}}
    power_prompt = generate_split_prompt(
        mode="power_seed",
        world_vision=WORLD,
        creative_state=state,
        premise_power_contract=contracts["power"],
        power_novelty="",
        power_lexique="",
    )
    human_prompt = generate_split_prompt(
        mode="human_seed",
        world_vision=WORLD,
        creative_state=state,
        premise_human_contract=contracts["human"],
    )
    assert "ONTOLOGY_S2" in power_prompt and "POWER_S2" in power_prompt
    assert "STORY_S2" not in power_prompt
    assert "ONTOLOGY_S2" in human_prompt
    assert "POWER_S2" not in human_prompt
    assert "STORY_S2" not in human_prompt


def test_raw_premise_enters_story_once_but_not_outline_or_chapter(tmp_path: Path) -> None:
    create_book("runtime", tmp_path)
    directory = tmp_path / "runtime"
    save_premise_candidates(directory, CANDIDATES)
    save_batch_compiler(directory)
    save_selected_premise(directory, candidate(2))
    contracts = approve_premise(directory)["contracts"]

    approved_state = {
        "world_vision": {"status": "author_approved"},
        "character_card": {"status": "author_approved"},
        "proposal": {"status": "author_approved"},
    }
    character = "# CHARACTER CARD\n\n## POWER CORE\n能力\n\n## HUMAN CORE\n欲望"
    initial = "# INITIAL CHARACTER STATE\n\n## current_desire\n赢"
    story = generate_split_prompt(
        mode="idea",
        creative_direction="方向",
        world_vision=WORLD,
        character_card=character,
        character_initial_state=initial,
        creative_state=approved_state,
        premise_story_contract=contracts["story"],
    )
    outline = generate_split_prompt(
        mode="outline",
        creative_direction="方向",
        world_vision=WORLD,
        character_card=character,
        character_initial_state=initial,
        proposal_context="# STORY PROGRAM\nPROGRAM",
        creative_state=approved_state,
        premise_story_contract=contracts["story"],
    )

    assert "STORY_S2" in story
    assert "IMMUTABLE_S2" in story
    assert "STORY_S2" not in outline
    assert "IMMUTABLE_S2" not in outline


def test_real_chapter_prompt_does_not_receive_raw_premise_card(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    create_book("chapter-cutoff", tmp_path)
    directory = tmp_path / "chapter-cutoff"
    save_premise_candidates(directory, CANDIDATES)
    save_batch_compiler(directory)
    save_selected_premise(directory, candidate(2))
    approve_premise(directory)

    chapter_plan = "\n".join(
        f"{field}：内容"
        for field in (
            "触发事件",
            "推动事件的人",
            "主角行动",
            "对手或世界反应",
            "直接结果",
            "状态变化",
            "叙事功能",
            "结尾推动力",
        )
    )
    response = TestClient(app).post(
        "/api/prompt",
        json={
            "book_id": "chapter-cutoff",
            "mode": "chapter",
            "template": "CHAPTER TEMPLATE",
            "book_content": "BOOK AUTHORITY ONLY",
            "current_long_block": "CURRENT LONG BLOCK",
            "current_outline": chapter_plan,
            "chapter_number": 4,
        },
    )

    assert response.status_code == 200
    prompt = response.json()["prompt"]
    for raw_marker in (
        "SHELF_S2",
        "WORLD_S2",
        "ONTOLOGY_S2",
        "POWER_S2",
        "STORY_S2",
        "TRACE_S2",
        "VERBS_S2",
        "IMMUTABLE_S2",
    ):
        assert raw_marker not in prompt


def test_workflow_exposes_only_frozen_contract_not_raw_search_artifacts(tmp_path: Path) -> None:
    create_book("workflow", tmp_path)
    directory = tmp_path / "workflow"
    before = workflow_status(directory)
    assert before["artifacts"]["premise.contract"]["status"] == "EMPTY"

    save_premise_candidates(directory, CANDIDATES)
    assert workflow_status(directory)["artifacts"]["premise.contract"]["status"] == "EMPTY"
    save_batch_compiler(directory)
    save_selected_premise(directory, candidate(2))
    approve_premise(directory)

    after = workflow_status(directory)
    assert after["artifacts"]["premise.contract"]["status"] == "DONE"
    assert "premise.candidates" not in after["artifacts"]
    assert "premise.compiler" not in after["artifacts"]
