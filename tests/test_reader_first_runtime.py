from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from story_mvp.app import app
from story_mvp.chapter_context import build_chapter_context
from story_mvp.hybrid_runtime import (
    build_specialist_context,
    extract_specialist_patches,
)
from story_mvp.prompts import (
    DEFAULT_STATE_DELTA_TEMPLATE,
    REQUIRED_OUTLINE_FIELDS,
    READER_FIRST_PROSE_CONTRACT,
    generate_prompt,
    parse_canon_memory,
    parse_state_delta_v2,
    render_canon_memory,
)
from story_mvp.gbrain_retrieval import genre_prior_matches_query, is_genre_prior_page, retrieve_gbrain
from story_mvp.run_ledger import (
    create_or_load_run,
    load_run,
    mark_node_failed,
    next_actionable_node,
    retry_node,
    save_node_prompt,
    save_node_response,
    skip_integrator_if_no_patches,
)
from story_mvp.storage import apply_state_delta_to_book, save_chapter, validate_chapter_body_for_save


OUTLINE = "\n".join(
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


def test_reader_first_contract_and_curator_sections_are_scoped() -> None:
    curator = generate_prompt(
        mode="context_curator",
        template="",
        book_content="# 小说总体设计画像\n\n## 7. 叙事结构\n贴近主角",
        current_outline=OUTLINE,
    )
    for heading in (
        "## Reader-Facing Language",
        "## Already Established — Do Not Re-explain",
        "## Recent Repetition Risks",
        "## Payoff and Promise Window",
    ):
        assert heading in curator
    assert "Reader-First Prose Contract" not in curator
    for marker in (
        "当前最在意的事",
        "自尊/恐惧/欲望",
        "行为习惯或说话声音",
        "不要生成 Character Card",
    ):
        assert marker in curator
    assert "## Character Card" not in curator
    for marker in (
        "关系阶段、状态变化、社会评价、收益结算等抽象内容属于 Writer 的内部理解",
        "不能直接复制总结",
        "Curator 不必自行把这些内容改写成正文句子",
    ):
        assert marker in curator

    primary = generate_prompt(
        mode="primary_writer",
        template="",
        book_content="",
        current_outline=OUTLINE,
        curated_context="# Curated Chapter Context\n\n## Reader-Facing Language\n动作优先",
    )
    assert primary.count(READER_FIRST_PROSE_CONTRACT) == 1
    for marker in (
        "清楚 > 顺畅 > 有画面 > 文学感",
        "普通中文男频网文读者",
        "明确写人物、对象、动作、原因和结果",
        "重要能力、物品和规则第一次出现时",
        "少连续使用“不是……”",
        "对话像人在现场传递信息",
        "世界观和空间信息只解释当前行动需要的最小部分",
        "简单不等于空泛",
        "当前读者主问题",
        "具名的重要物品一旦明确换了持有人或位置",
        "关键因果节点",
        "第一息 / 第二息 / 第三息",
        "新章不要原样或近似复述上一章最后一句",
        "朴素、直接不等于情绪中性",
        "人物不是状态更新器",
        "有反应后选择压住",
        "重大胜利、失败、羞辱、翻盘",
        "不必每句高效",
        "核心欲望、自尊、恐惧或期待",
        "不要只用疼痛、战术判断、看一眼或状态确认代替它",
        "策划层可以使用抽象关系和状态语言",
        "不要再追加同义的抽象旁白",
        "不要再用抽象旁白总结同一意义",
        "策划层的关系阶段、状态变化、社会评价和收益结算属于内部理解",
    ):
        assert marker in primary
    assert primary.count("人物不是状态更新器") == 2
    specialist = generate_prompt(
        mode="specialist_action",
        template="",
        book_content="",
        current_outline=OUTLINE,
        primary_draft="正文底稿",
    )
    assert specialist.count(READER_FIRST_PROSE_CONTRACT) == 1


def test_specialist_patch_projection_excludes_audit_and_context_is_cropped() -> None:
    response = "# Specialist Audit\nSECRET_AUDIT\n# Proposed Patches\n## Patch 1\n目标锚点：开头\n操作：replace\n建议文本：保留动作。"
    assert "SECRET_AUDIT" not in extract_specialist_patches(response)
    assert "## Patch 1" in extract_specialist_patches(response)

    packet = build_chapter_context(
        book_content="# 小说总体设计画像\n## 0. 本书成长基因图\n### 核心不变量\n持续行动\n## 1. 核心类型与读者承诺\n成长",
        current_outline=OUTLINE,
        current_chapter_plan="## 第2章：当前条目\nCURRENT_CHAPTER_PLAN",
        current_long_block="CURRENT_BLOCK",
    )
    primary = "\n\n".join([f"前部{i}" + ("x" * 400) for i in range(8)]) + "\n\nTAIL_MARKER"
    opening = build_specialist_context(packet, "# Curated Chapter Context", primary, "opening")
    assert len(opening.primary_draft) <= 1800
    assert "CURRENT_CHAPTER_PLAN" in packet.chapter_plan_context
    assert packet.current_long_block == "CURRENT_BLOCK"


def test_director_prompt_uses_only_light_projection_and_selective_default() -> None:
    prompt = generate_prompt(
        mode="director",
        template="",
        book_content="# 小说总体设计画像\n## 0. 本书成长基因图\n### 核心不变量\nGENOME",
        current_long_block="CURRENT_BLOCK",
        current_chapter_plan="CURRENT_CHAPTER_PLAN",
        previous_chapter_text="PREVIOUS_TAIL",
        recent_summaries="RECENT_SUMMARY",
        creative_direction="AUTHOR_INTENT",
    )
    for marker in ("CURRENT_BLOCK", "CURRENT_CHAPTER_PLAN", "GENOME", "PREVIOUS_TAIL", "RECENT_SUMMARY", "AUTHOR_INTENT"):
        assert marker in prompt
    assert "writer_mode" not in prompt
    assert "专项建议" in prompt
    director_contract = prompt.split("# Director Context", 1)[0]
    for field in REQUIRED_OUTLINE_FIELDS:
        assert f"{field}：" in director_contract
    assert "八个字段仍是唯一事件合同字段" in director_contract
    assert "情绪字段：" not in director_contract

    hybrid = generate_prompt(
        mode="context_curator",
        template="",
        book_content="",
        current_outline=OUTLINE,
    )
    assert "writer_mode: hybrid_selective" in hybrid


def test_canon_memory_v2_and_state_delta_parser() -> None:
    status = """当前已完成第3章。

## ACTIVE SCENE STATE
废井；沈砚在场；左臂受伤。

## PERSISTENT CANON
砾角能在湿壁上短暂借力；关系阶段：容忍同行。
### Active Relationships
沈禾｜寻找失踪弟弟｜与主角暂时合作｜主角救过她一次｜答应提供旧矿图
### Tracked Assets
黑炉钥匙｜沈砚｜废井腰包｜可开旧炉门｜刚从主角转交

## RECENT SUMMARIES
第3章：主角打开闸门。

## OPEN PROMISES
沈禾的去向。

## AUTHOR NOTES
逐字保留这句。"""
    fields = parse_canon_memory(status)
    assert fields["active_scene_state"].startswith("废井")
    assert "短暂借力" in fields["persistent_canon"]
    assert "Active Relationships" in fields["persistent_canon"]
    assert "Tracked Assets" in fields["persistent_canon"]
    assert fields["author_notes"] == "逐字保留这句。"
    rendered = render_canon_memory(fields)
    assert "## ACTIVE SCENE STATE" in rendered
    assert "## PERSISTENT CANON" in rendered
    assert "沈禾｜寻找失踪弟弟" in rendered
    assert "黑炉钥匙｜沈砚" in rendered
    assert "当前主动目标" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "### Active Relationships" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "### Tracked Assets" in DEFAULT_STATE_DELTA_TEMPLATE

    proposal = parse_state_delta_v2(
        """# State Delta Audit
无。

# Proposed Active Scene State
新地点；无追兵。

# Proposed Persistent Canon
能力限制仍为短暂借力。

# Proposed Chapter Summary
主角拿到一枚钥匙。

# Proposed Open Promises
钥匙来自谁。"""
    )
    assert proposal["chapter_summary"] == "主角拿到一枚钥匙。"
    assert "# Proposed Canon Index" not in DEFAULT_STATE_DELTA_TEMPLATE

    updated = apply_state_delta_to_book(
        """# 小说总体设计画像
内容

# 当前状态、未兑现承诺与作者备注
当前已完成第0章。

## ACTIVE SCENE STATE
旧场景

## PERSISTENT CANON
旧长期事实

## RECENT SUMMARIES
当前尚无已完成正文或已批准章节摘要。

## OPEN PROMISES
旧承诺

## AUTHOR NOTES
作者原话。""",
        1,
        """# State Delta Audit
无。
# Proposed Active Scene State
新场景
# Proposed Persistent Canon
新能力限制
### Active Relationships
沈禾｜寻找弟弟｜暂时合作｜主角救援｜提供旧矿图
### Tracked Assets
黑炉钥匙｜沈禾｜回收册｜已转交｜刚从主角转出
# Proposed Chapter Summary
第一章事实
# Proposed Open Promises
新承诺""",
    )
    assert "当前已完成第1章。" in updated
    assert "第1章：第一章事实" in updated
    assert "作者原话。" in updated
    assert "沈禾｜寻找弟弟" in updated
    assert "黑炉钥匙｜沈禾" in updated
    assert "旧场景" not in updated

    prefixed = apply_state_delta_to_book(
        """# 小说总体设计画像
内容
# 当前状态、未兑现承诺与作者备注
## ACTIVE SCENE STATE
旧
## PERSISTENT CANON
旧
## RECENT SUMMARIES
旧
## OPEN PROMISES
旧
## AUTHOR NOTES
原话""",
        3,
        """# State Delta Audit
无。
# Proposed Active Scene State
新
# Proposed Persistent Canon
新
# Proposed Chapter Summary
第3章：已经发生。
# Proposed Open Promises
新""",
    )
    assert "第3章：第3章：" not in prefixed


def test_chapter_save_rejects_internal_sections_without_mutating_input(tmp_path: Path) -> None:
    body = "第一段正文。\n\n# Writer Audit\n不应保存。"
    try:
        validate_chapter_body_for_save(body)
    except ValueError as error:
        assert "Writer Audit" in str(error)
    else:
        raise AssertionError("internal chapter sections must be rejected")
    assert body.endswith("不应保存。")

    book_dir = tmp_path / "books" / "demo"
    (book_dir / "chapters").mkdir(parents=True)
    (book_dir / "BOOK.md").write_text("# book", encoding="utf-8")
    try:
        save_chapter("demo", 1, "---FACT_SUMMARY---\n摘要", tmp_path / "books")
    except ValueError as error:
        assert "FACT_SUMMARY" in str(error)
    else:
        raise AssertionError("fact summary must not be saved")
    assert not (book_dir / "chapters" / "chapter-0001.md").exists()


def test_run_ledger_retries_one_failed_node_and_keeps_upstream(tmp_path: Path) -> None:
    book_dir = tmp_path / "demo"
    (book_dir / "BOOK.md").parent.mkdir(parents=True)
    (book_dir / "BOOK.md").write_text("# book", encoding="utf-8")
    manifest = create_or_load_run(
        book_dir,
        1,
        writer_mode="hybrid_selective",
        selected_specialists=["opening"],
    )
    assert manifest["nodes"]["dialogue"]["status"] == "skipped"
    save_node_prompt(book_dir, 1, "director", "DIRECTOR_PROMPT")
    save_node_response(book_dir, 1, "director", "DIRECTOR_RESPONSE")
    save_node_prompt(book_dir, 1, "primary", "PRIMARY_PROMPT")
    save_node_response(book_dir, 1, "primary", "PRIMARY_RESPONSE")
    save_node_prompt(book_dir, 1, "opening", "OPENING_PROMPT")
    mark_node_failed(book_dir, 1, "opening")
    before = load_run(book_dir, 1)
    retried = retry_node(book_dir, 1, "opening")
    assert retried["nodes"]["opening"]["attempts"] == 2
    assert retried["nodes"]["director"]["status"] == "completed"
    assert retried["nodes"]["primary"]["status"] == "completed"
    save_node_response(book_dir, 1, "opening", "OPENING_RESPONSE")
    completed = load_run(book_dir, 1)
    assert completed["nodes"]["opening"]["response_file"].endswith("attempt-2.md")
    assert completed["nodes"]["integrator"]["status"] == "stale"
    assert next_actionable_node(book_dir, 1) == "curator"
    assert before["nodes"]["director"]["response_file"] == "director_response.md"
    skipped = skip_integrator_if_no_patches(book_dir, 1, {"opening": "# Proposed Patches\n无"})
    assert skipped["nodes"]["integrator"]["status"] == "skipped"


def test_genre_prior_is_capped_for_planning_and_excluded_from_chapter() -> None:
    genre = """---
creative_problem_tags:
- genre-prior
- idea
title: 题材先验｜玄幻修仙
---
## Reader Promise
题材先验内容。
## Failure Risks
风险。
"""
    mechanism = """---
creative_problem_tags:
- mechanism
---
## Mechanism
具体机制内容。
"""
    assert is_genre_prior_page(genre)
    pages = {
        "syntheses/genre-priors/a": genre,
        "syntheses/genre-priors/b": genre,
        "syntheses/genre-priors/c": genre,
        "mechanisms/concrete": mechanism,
    }
    raw = "\n".join(
        [
            "[0.99] syntheses/genre-priors/a -- prior",
            "[0.98] syntheses/genre-priors/b -- prior",
            "[0.97] syntheses/genre-priors/c -- prior",
            "[0.96] mechanisms/concrete -- mechanism",
        ]
    )
    idea = retrieve_gbrain(
        mode="idea", book_content="玄幻成长", query_override="玄幻修仙", query_func=lambda *_args, **_kwargs: raw, page_func=pages.__getitem__
    )
    assert idea["genre_prior_count"] == 2
    assert any(item["reason"] == "超过 Genre Prior 接受上限" for item in idea["rejected"])
    chapter = retrieve_gbrain(
        mode="chapter", book_content="玄幻成长", query_override="玄幻修仙", query_func=lambda *_args, **_kwargs: raw, page_func=pages.__getitem__
    )
    assert all(not item.get("is_genre_prior") for item in chapter["accepted"])
    assert any(item["reason"] == "章节节点不自动使用 Genre Prior" for item in chapter["rejected"])
    prompt = generate_prompt(
        mode="chapter",
        template="CHAPTER",
        book_content="",
        current_outline=OUTLINE,
        gbrain_inspiration="### Inspiration 1\nsource: syntheses/genre-priors/a\n可用抽象：题材先验",
    )
    assert "genre-priors/a" not in prompt
    assert not genre_prior_matches_query("---\ntitle: 题材先验｜宫斗宅斗\ncreative_problem_tags:\n- genre-prior\n---", "高武个人战斗", "syntheses/genre-priors/宫斗宅斗")


def test_run_ledger_api_persists_prompt_response_and_retry(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    client = TestClient(app)
    assert client.post("/api/books", json={"book_id": "ledger-api"}).status_code == 201
    created = client.post(
        "/api/books/ledger-api/runs/1",
        json={"writer_mode": "hybrid_selective", "selected_specialists": ["opening"]},
    )
    assert created.status_code == 200
    assert created.json()["nodes"]["dialogue"]["status"] == "skipped"
    prompt = client.put(
        "/api/books/ledger-api/runs/1/nodes/director/prompt",
        json={"content": "director prompt"},
    )
    assert prompt.status_code == 200
    response = client.put(
        "/api/books/ledger-api/runs/1/nodes/director/response",
        json={"content": "director response"},
    )
    assert response.status_code == 200
    failed = client.post("/api/books/ledger-api/runs/1/nodes/director/failed")
    assert failed.status_code == 200
    retried = client.post("/api/books/ledger-api/runs/1/nodes/director/retry")
    assert retried.status_code == 200
    assert retried.json()["nodes"]["director"]["attempts"] == 2
    assert (tmp_path / "ledger-api" / "runs" / "chapter-0001" / "director_prompt.md").is_file()
