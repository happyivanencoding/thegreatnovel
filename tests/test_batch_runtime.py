from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from story_mvp.app import app
from story_mvp.batch_runtime import (
    BatchWindow,
    apply_batch_delta,
    build_batch_delta_reviser_prompt,
    build_batch_primary_prompt,
    build_batch_prose_delta_prompt,
    compose_batch_deltas,
    extract_batch_outline_plans,
    parse_batch_delta_response,
    parse_batch_primary_response,
    parse_batch_prose_delta_response,
)


def _primary_response(window: BatchWindow) -> str:
    return "note\n" + "\n\n".join(
        f"# BATCH CHAPTER {number}\n## 正式正文\n第{number}章正文。关键物{number}仍在。"
        for number in window.chapter_numbers
    )


def test_batch_window_defaults_to_five_and_bounds_four_to_six() -> None:
    assert BatchWindow(11).chapter_numbers == (11, 12, 13, 14, 15)
    assert BatchWindow(11, 4).end_chapter == 14
    assert BatchWindow(11, 6).end_chapter == 16
    with pytest.raises(ValueError):
        BatchWindow(1, 3)
    with pytest.raises(ValueError):
        BatchWindow(1, 7)


def test_batch_primary_parser_accepts_small_model_preamble_and_requires_every_chapter() -> None:
    window = BatchWindow(1, 5)
    chapters = parse_batch_primary_response(_primary_response(window), window)
    assert chapters[3] == "第3章正文。关键物3仍在。"

    with pytest.raises(ValueError):
        parse_batch_primary_response("# BATCH CHAPTER 1\n## 正式正文\nonly one", window)


def test_batch_default_can_use_future10_directly_without_replanning_llm() -> None:
    window = BatchWindow(2, 4)
    outline = """# 未来十章逐章小纲

## 第1章：一
具体剧情：A
结果 / 状态变化：A1

## 第2章：二
具体剧情：B
结果 / 状态变化：B1

## 第3章：三
具体剧情：C
结果 / 状态变化：C1

## 第4章：四
具体剧情：D
结果 / 状态变化：D1

## 第5章：五
具体剧情：E
结果 / 状态变化：E1
"""
    plans = extract_batch_outline_plans(outline, window)
    assert tuple(plans) == (2, 3, 4, 5)
    assert "具体剧情：B" in plans[2]
    assert "## 第5章：五" in plans[5]


def test_batch_primary_packet_compiles_protected_event_and_shared_canon_before_writing() -> None:
    window = BatchWindow(1, 4)
    book = """# 小说总体设计画像

## 1. 核心类型与读者承诺

### 不可降格 Reader-Facing Story Event Registry
#### RSE-01
事件原子：界签首次显现 → 故乡被标成第一副本 → 十二日与归门规则进入认知
状态残留：界阶1成立；不能替代现场事件
排程边界：第1章
读者证明锚点：界签；第一副本；十二日

## 5. 配角与关系系统
父亲裴桐烧昼炭。

## 8. 文风与可操作参数
贴近裴骁现场认知；重要动作先发生，再补最少解释。

## 9. 对话特点
说话直接，条件先落到具体物和钱。

# 当前中期规划窗口
阶段仍在北燧城。

# 未来十章逐章小纲
## 第1章：A
具体剧情：A1
结果 / 状态变化：A2
不可降格 Story Event：RSE-01
结尾推动：A3
## 第2章：B
具体剧情：B1
结果 / 状态变化：B2
结尾推动：B3
## 第3章：C
具体剧情：C1
结果 / 状态变化：C2
结尾推动：C3
## 第4章：D
具体剧情：D1
结果 / 状态变化：D2
结尾推动：D3

# 当前状态、未兑现承诺与作者备注
当前地点：炭窑街。
父亲：裴桐。
"""
    plans = extract_batch_outline_plans(book, window)
    prompt = build_batch_primary_prompt(
        window=window,
        batch_plans=plans,
        book_content=book,
        world_vision="WORLD",
        world_expansions="",
        character_card="## POWER CORE｜Frozen Authority\nP\n## HUMAN CORE｜Frozen Authority\nH",
    )
    assert "界签首次显现" in prompt
    assert "读者证明锚点：界签；第一副本；十二日" in prompt
    assert "父亲裴桐烧昼炭" in prompt
    assert "父亲：裴桐" in prompt
    assert "# PROSE PROFILE" in prompt
    assert "贴近裴骁现场认知；重要动作先发生，再补最少解释。" in prompt
    assert "说话直接，条件先落到具体物和钱。" in prompt


def test_batch_delta_changes_only_exact_unique_text_and_preserves_other_chapters() -> None:
    window = BatchWindow(1, 4)
    primary = parse_batch_primary_response(_primary_response(window), window)
    delta = parse_batch_delta_response(
        "说明句\n"
        + json.dumps(
            {
                "patches": [
                    {
                        "chapter": 2,
                        "old": "关键物2仍在",
                        "new": "关键物2已经交给镜离",
                        "reason": "持有人 stale",
                    }
                ],
                "upstream_conflicts": [],
            },
            ensure_ascii=False,
        ),
        window,
    )
    revised = apply_batch_delta(primary, delta, window)
    assert revised[1] == primary[1]
    assert revised[3] == primary[3]
    assert "关键物2已经交给镜离" in revised[2]

    duplicate = dict(primary)
    duplicate[2] = "重复。重复。"
    duplicate_delta = parse_batch_delta_response(
        json.dumps(
            {
                "patches": [
                    {"chapter": 2, "old": "重复", "new": "修", "reason": "x"}
                ],
                "upstream_conflicts": [],
            },
            ensure_ascii=False,
        ),
        window,
    )
    with pytest.raises(ValueError, match="唯一匹配"):
        apply_batch_delta(duplicate, duplicate_delta, window)


def test_batch_prose_delta_is_narrow_and_composes_authority_first() -> None:
    window = BatchWindow(1, 4)
    primary = parse_batch_primary_response(_primary_response(window), window)
    prose_prompt = build_batch_prose_delta_prompt(
        window=window,
        primary_chapters=primary,
        book_content="""# 小说总体设计画像

## 8. 文风与可操作参数
动作成立后不要重复下判词。

## 9. 对话特点
人物把一个完整意思说完。
""",
    )
    assert "Batch Prose Delta" in prose_prompt
    assert "immutable Primary" in prose_prompt
    assert "Show-Then-Trust" in prose_prompt
    assert "Paragraph Continuity" in prose_prompt
    assert "Dialogue Continuity" in prose_prompt
    assert "不能新增或删除任何 story beat" in prose_prompt
    assert "动作成立后不要重复下判词" in prose_prompt

    authority = parse_batch_delta_response(
        json.dumps(
            {
                "patches": [
                    {"chapter": 2, "old": "关键物2仍在", "new": "关键物2已经交出", "reason": "Authority"}
                ],
                "upstream_conflicts": [],
            },
            ensure_ascii=False,
        ),
        window,
    )
    prose = parse_batch_prose_delta_response(
        json.dumps(
            {
                "patches": [
                    {"chapter": 1, "old": "第1章正文。", "new": "第1章正文——", "reason": "合并同一 beat"},
                    {"chapter": 2, "old": "关键物2仍在", "new": "关键物2还在", "reason": "与 Authority 重叠"},
                ],
                "upstream_conflicts": [],
            },
            ensure_ascii=False,
        ),
        window,
    )
    final, applied, skipped = compose_batch_deltas(primary, authority, prose, window)
    assert "第1章正文——关键物1仍在" in final[1]
    assert "关键物2已经交出" in final[2]
    assert len(applied) == 1
    assert len(skipped) == 1
    assert skipped[0]["chapter"] == 2
    assert skipped[0]["match_count_after_authority"] == 0


def test_batch_prose_delta_rejects_upstream_conflicts() -> None:
    window = BatchWindow(1, 4)
    with pytest.raises(ValueError, match="Prose Delta 不得报告"):
        parse_batch_prose_delta_response(
            json.dumps(
                {
                    "patches": [],
                    "upstream_conflicts": [
                        {"chapter": 2, "issue": "计划缺因果", "required_upstream": "先修 Outline"}
                    ],
                },
                ensure_ascii=False,
            ),
            window,
        )


def test_batch_delta_keeps_upstream_plan_conflict_out_of_prose_patch() -> None:
    window = BatchWindow(1, 5)
    delta = parse_batch_delta_response(
        json.dumps(
            {
                "patches": [],
                "upstream_conflicts": [
                    {
                        "chapter": 4,
                        "issue": "第2章明确关门，第4章裴照临已在异界",
                        "required_upstream": "Outline 必须先决定合法跨界路径或调整第4章出现",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        window,
    )
    assert not delta.patches
    assert delta.upstream_conflicts[0]["chapter"] == 4


def test_batch_prompts_preserve_narrative_window_and_reviser_does_not_invent_access() -> None:
    window = BatchWindow(1, 5)
    outline = "\n".join(
        f"## 第{n}章：第{n}章\n具体剧情：E{n}\n结果 / 状态变化：R{n}\n结尾推动：H{n}"
        for n in window.chapter_numbers
    )
    plans = extract_batch_outline_plans(outline, window)
    chapters = parse_batch_primary_response(_primary_response(window), window)
    primary = build_batch_primary_prompt(
        window=window,
        batch_plans=plans,
        book_content=outline,
        world_vision="海在天上，陆在下。",
        world_expansions="",
        character_card="## POWER CORE｜Frozen Authority\nP\n## HUMAN CORE｜Frozen Authority\nH",
    )
    assert "# APPROVED BATCH PLANS" in primary
    assert "一次连续写完" in primary
    assert "Stable Scene Geography" in primary
    assert "Action Advance ≠ Situation Memory" in primary
    assert "Active Interior Continuity" in primary
    assert "Living Power Ecology 要在正文里真正约束行为" in primary
    assert "短独段只留给真正的冲击" in primary
    assert "功能型乒乓" in primary
    assert "叙事功能" in primary and "不把这些策划语义再翻译一遍" in primary
    reviser = build_batch_delta_reviser_prompt(
        window=window,
        batch_plans=plans,
        primary_chapters=chapters,
        book_content="BOOK",
        world_vision="海在天上，陆在下。",
        world_expansions="",
        character_card="## POWER CORE｜Frozen Authority\nP\n## HUMAN CORE｜Frozen Authority\nH",
        story_program="STORY",
    )
    assert "禁止重写整章" in reviser
    assert "upstream_conflicts" in reviser
    assert "不得 patch" in reviser
    assert "扫描该事实域的所有出现位置" in reviser
    assert "同一场“第一次失败 → 第二次同类动作修正”" in reviser
    assert "唯一凭证" in reviser
    assert "Event Participant stale" in reviser
    assert "retrospective backfill 偷造 Canon" in reviser


def test_batch_api_builds_prompts_and_marks_upstream_conflict_non_adoptable() -> None:
    client = TestClient(app)
    window = BatchWindow(1, 4)
    primary_response = _primary_response(window)
    outline = "\n".join(
        f"## 第{n}章：第{n}章\n具体剧情：E{n}\n结果 / 状态变化：R{n}\n结尾推动：H{n}"
        for n in window.chapter_numbers
    )
    common = {
        "start_chapter": 1,
        "batch_size": 4,
        "book_content": outline,
        "world_vision": "WORLD",
        "character_card": "## POWER CORE｜Frozen Authority\nP\n## HUMAN CORE｜Frozen Authority\nH",
        "story_program": "STORY",
        "batch_primary_response": primary_response,
    }
    response = client.post("/api/batch/primary-prompt", json=common)
    assert response.status_code == 200
    assert "## 第4章：第4章" in response.json()["content"]

    prose_prompt = client.post("/api/batch/prose-delta-prompt", json=common)
    assert prose_prompt.status_code == 200
    assert "Batch Prose Delta" in prose_prompt.json()["content"]

    delta = json.dumps(
        {
            "patches": [],
            "upstream_conflicts": [
                {
                    "chapter": 2,
                    "issue": "门已关闭但人物越界",
                    "required_upstream": "先修计划",
                }
            ],
        },
        ensure_ascii=False,
    )
    applied = client.post(
        "/api/batch/apply-authority-delta",
        json={
            "start_chapter": 1,
            "batch_size": 4,
            "batch_primary_response": primary_response,
            "batch_delta_response": delta,
        },
    )
    assert applied.status_code == 200
    assert applied.json()["adoptable"] is False
    assert applied.json()["patch_count"] == 0


def test_batch_api_composes_authority_then_surviving_prose_patch() -> None:
    client = TestClient(app)
    window = BatchWindow(1, 4)
    primary = _primary_response(window)
    authority = json.dumps(
        {
            "patches": [
                {"chapter": 2, "old": "关键物2仍在", "new": "关键物2已经交出", "reason": "Authority"}
            ],
            "upstream_conflicts": [],
        },
        ensure_ascii=False,
    )
    prose = json.dumps(
        {
            "patches": [
                {"chapter": 1, "old": "第1章正文。", "new": "第1章正文——", "reason": "prose"},
                {"chapter": 2, "old": "关键物2仍在", "new": "关键物2还在", "reason": "overlap"},
            ],
            "upstream_conflicts": [],
        },
        ensure_ascii=False,
    )
    applied = client.post(
        "/api/batch/apply-authority-delta",
        json={
            "start_chapter": 1,
            "batch_size": 4,
            "batch_primary_response": primary,
            "batch_delta_response": authority,
            "batch_prose_delta_response": prose,
        },
    )
    assert applied.status_code == 200
    body = applied.json()
    assert body["adoptable"] is True
    assert body["patch_count"] == 1
    assert body["prose_patch_count"] == 2
    assert body["prose_applied_count"] == 1
    assert len(body["prose_skipped"]) == 1
    assert "第1章正文——关键物1仍在" in body["chapters"]["1"]
    assert "关键物2已经交出" in body["chapters"]["2"]


def test_batch_api_defaults_to_approved_future10_without_replanning_llm() -> None:
    client = TestClient(app)
    outline = """# 未来十章逐章小纲
## 第1章：A
具体剧情：A1
结果 / 状态变化：A2
结尾推动：A3
## 第2章：B
具体剧情：B1
结果 / 状态变化：B2
结尾推动：B3
## 第3章：C
具体剧情：C1
结果 / 状态变化：C2
结尾推动：C3
## 第4章：D
具体剧情：D1
结果 / 状态变化：D2
结尾推动：D3
"""
    payload = {
        "start_chapter": 1,
        "batch_size": 4,
        "book_content": outline,
        "world_vision": "WORLD",
        "character_card": "## POWER CORE｜Frozen Authority\nP\n## HUMAN CORE｜Frozen Authority\nH",
        "story_program": "STORY",
    }
    response = client.post("/api/batch/primary-prompt", json=payload)
    assert response.status_code == 200
    prompt = response.json()["content"]
    assert "# APPROVED BATCH PLANS" in prompt
    assert "## 第1章：A" in prompt
    assert "## 第4章：D" in prompt


def test_batch_adopt_preflights_conflicts_then_saves_whole_batch(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "batch-adopt"}).status_code == 201
    window = BatchWindow(1, 4)
    primary = _primary_response(window)

    conflict = json.dumps(
        {
            "patches": [],
            "upstream_conflicts": [
                {
                    "chapter": 3,
                    "issue": "缺少合法到达因果",
                    "required_upstream": "先修 Outline",
                }
            ],
        },
        ensure_ascii=False,
    )
    blocked = client.post(
        "/api/books/batch-adopt/batch/adopt-authority-delta",
        json={
            "start_chapter": 1,
            "batch_size": 4,
            "batch_primary_response": primary,
            "batch_delta_response": conflict,
        },
    )
    assert blocked.status_code == 400
    assert not (tmp_path / "batch-adopt" / "chapters" / "chapter-0001.md").exists()

    delta = json.dumps(
        {
            "patches": [
                {
                    "chapter": 2,
                    "old": "关键物2仍在",
                    "new": "关键物2已经交出",
                    "reason": "持有人修复",
                }
            ],
            "upstream_conflicts": [],
        },
        ensure_ascii=False,
    )
    saved = client.post(
        "/api/books/batch-adopt/batch/adopt-authority-delta",
        json={
            "start_chapter": 1,
            "batch_size": 4,
            "batch_primary_response": primary,
            "batch_delta_response": delta,
        },
    )
    assert saved.status_code == 200
    assert saved.json()["state_next"] == 1
    assert saved.json()["patch_count"] == 1
    assert all(
        (tmp_path / "batch-adopt" / "chapters" / f"chapter-{n:04d}.md").is_file()
        for n in range(1, 5)
    )
    assert "关键物2已经交出" in (
        tmp_path / "batch-adopt" / "chapters" / "chapter-0002.md"
    ).read_text(encoding="utf-8")
