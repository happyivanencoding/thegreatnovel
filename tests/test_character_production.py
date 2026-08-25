from __future__ import annotations

from pathlib import Path

import pytest

from story_mvp.character_prompts import generate_split_prompt
from story_mvp.gbrain_retrieval import build_retrieval_brief, default_effective_query
from story_mvp.storage import (
    approve_character_artifact,
    approve_creative_artifact,
    create_book,
    read_creative_payload,
    write_creative_artifact,
)
from story_mvp.workflow_state import workflow_status


WORLD = """# PROTAGONIST-BLIND WORLD VISION

## 普通人的生活与上升
普通人住在河谷和港口，年轻人可进宗门、军府或学手艺。

## 力量体系与正常值
普通人不会正式修行；纳息、通脉、立相、照域逐层稀少。一人通常只能维持一种稳定主承载。

## 社会现实与身份
宗门、世家、商盟、军府并存，身份影响师承与资源。

## 世界里真正值钱、值得想要的东西
功法、兵器、灵田、师承和进入高层区域的资格都真实值钱。

## 世界正在发生的大事
剑修宋甲正在追一名叛徒；商队准备穿过归潮区。

## 值得进入的地点、奇观与未知
北境有一座倒悬石城，没人知道它为何不坠落。

## 世界知识边界
普通人知道境界差距；顶层修士知道旧时代曾出现过空间异常。
当前没人能完整解释的事实：倒悬石城为何不坠落。
"""

POWER = """# POWER SEED｜两处同身
## World Power Normal → Legal Exception
普通人只有一个当前位置；持有者可保留第二空间锚点。
## Core Fantasy
我能在第二个真实位置保留行动支点。
## 为什么读者会馋
探索、逃脱与战斗自由显著增加。
## Growth Compatibility
### 正常修炼轴
修为提升身体、神识与灵力。
### 异常掌握轴
锚点距离、持续和局部动作逐步扩张。
### High-Tier Mutation
高阶可让两个位置共同参与同一力量动作，但不是两具完整身体。
### 永久边界
始终只有一份完整战力。
## Legendary Power State
很难被单一战场困住。
## Power Audit Metadata（非 Canon）
### Future Legend Image
两地大战同时出现他的动作痕迹。
"""

HUMAN = """# HUMAN SEED｜石砚／让所有人同时回头
## 世界中的初始位置与成长环境
山城石匠家庭，从小做石笛。
## Formative Facts → Adaptation → Observable Behavior
曾偶然吹出一次极好听的回声 → 不能接受“差不多” → 会为找回那个声音浪费钱和时间。
## Core Obsession
别人觉得已经够好，他仍会继续追那个真正让自己满意的声音。
## Excess
有稳定订单后仍把积蓄换成废石，只为验证一段回声。
## Behavior Signature
面对足够好的结果，他会先找自己仍不满意的那一点。
## 重要关系原点
父亲想让他接普通石活；旧友觉得他为了声音不顾生活。
## Initial State Seed
### 当前私人欲望
在长风廊吹出一声让所有人同时回头的声音。
## Audition Metadata（非 Canon）
### 人物钩子
他吹出全场喝彩的一声，却当众折断石笛：不是这个。
"""


def _approved_state() -> dict[str, dict[str, str]]:
    return {
        "world_vision": {"status": "author_approved"},
        "power_seed": {"status": "author_approved"},
        "human_seed": {"status": "author_approved"},
        "character_card": {"status": "author_approved"},
        "proposal": {"status": "draft"},
    }


def test_new_book_contains_split_character_artifacts(tmp_path: Path) -> None:
    create_book("split-book", tmp_path)
    payload = read_creative_payload("split-book", tmp_path)
    assert payload["power_seed"] == ""
    assert payload["human_seed"] == ""
    assert payload["character_card"] == ""
    assert payload["character_initial_state"] == ""
    assert payload["character_audition"] == ""


def test_one_character_approval_freezes_both_seeds_and_separates_state(tmp_path: Path) -> None:
    create_book("split-book", tmp_path)
    write_creative_artifact("split-book", "world_vision", WORLD, tmp_path, origin="model_generated")
    approve_creative_artifact("split-book", "world_vision", tmp_path)
    write_creative_artifact("split-book", "power_seed", POWER, tmp_path, origin="author_edited")
    write_creative_artifact("split-book", "human_seed", HUMAN, tmp_path, origin="author_edited")

    payload = approve_character_artifact("split-book", tmp_path)
    assert payload["creative_state"]["power_seed"]["status"] == "author_approved"
    assert payload["creative_state"]["human_seed"]["status"] == "author_approved"
    assert payload["creative_state"]["character_card"] == {
        "origin": "deterministic",
        "status": "author_approved",
    }
    assert "两处同身" in payload["character_card"]
    assert "让所有人同时回头" in payload["character_card"]
    assert "当前私人欲望" not in payload["character_card"]
    assert "当众折断石笛" not in payload["character_card"]
    assert "让所有人同时回头的声音" in payload["character_initial_state"]
    assert "当众折断石笛" in payload["character_audition"]


def test_seed_edit_reopens_character_but_preserves_long_running_state(tmp_path: Path) -> None:
    create_book("split-book", tmp_path)
    write_creative_artifact("split-book", "world_vision", WORLD, tmp_path, origin="author_edited")
    approve_creative_artifact("split-book", "world_vision", tmp_path)
    write_creative_artifact("split-book", "power_seed", POWER, tmp_path, origin="author_edited")
    write_creative_artifact("split-book", "human_seed", HUMAN, tmp_path, origin="author_edited")
    approve_character_artifact("split-book", tmp_path)
    state_path = tmp_path / "split-book" / "CHARACTER_INITIAL_STATE.md"
    state_path.write_text("# CHARACTER STATE\n\n## current_desire\n现在想赢下一场比试。\n", encoding="utf-8")

    write_creative_artifact("split-book", "human_seed", HUMAN + "\n", tmp_path, origin="author_edited")
    payload = read_creative_payload("split-book", tmp_path)
    assert payload["character_card"] == ""
    assert payload["creative_state"]["character_card"]["status"] == "empty"
    assert "现在想赢下一场比试" in payload["character_initial_state"]


def test_human_prompt_is_power_blind_and_has_no_life_texture_input() -> None:
    prompt = generate_split_prompt(
        mode="human_seed",
        creative_direction="男频修仙",
        world_vision=WORLD,
        power_seed=POWER,
        creative_state={"world_vision": {"status": "author_approved"}},
        gbrain_inspiration="character hook craft",
    )
    assert "两处同身" not in prompt
    assert "第二空间锚点" not in prompt
    assert "Life Texture / Human Appetite" not in prompt
    assert "长篇性**不等于可复利事业" in prompt
    assert "character hook craft" in prompt


def test_power_prompt_uses_world_normal_but_not_story_opportunities() -> None:
    prompt = generate_split_prompt(
        mode="power_seed",
        world_vision=WORLD,
        creative_state={"world_vision": {"status": "author_approved"}},
        gbrain_inspiration="power progression craft",
    )
    assert "一人通常只能维持一种稳定主承载" in prompt
    assert "宋甲" not in prompt
    assert "倒悬石城" not in prompt
    assert "Legendary Power State" in prompt
    assert "未来身份、组织、统治地位、使命" in prompt


def test_collision_prompt_first_combines_full_world_and_character() -> None:
    prompt = generate_split_prompt(
        mode="idea",
        creative_direction="男频修仙",
        world_vision=WORLD,
        character_card="# CHARACTER CARD\n\n## POWER CORE\n两处同身\n\n## HUMAN CORE\n石砚想让所有人回头。",
        character_initial_state="# INITIAL CHARACTER STATE\n\n## current_desire\n现在想找到一块会回响的石头。",
        creative_state=_approved_state(),
        gbrain_inspiration="thread collision",
    )
    assert "Do Not Reconcile Away the Collision" in prompt
    assert "宋甲正在追一名叛徒" in prompt
    assert "石砚想让所有人回头" in prompt
    assert "现在想找到一块会回响的石头" in prompt
    assert "Approved Fantasy Seed" not in prompt


def test_character_modes_have_stable_keyword_gbrain_queries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("story_mvp.gbrain_retrieval._semantic_query_available", lambda: False)
    q1, strategy1 = default_effective_query("power_seed", "semantic brief")
    q2, strategy2 = default_effective_query("human_seed", "semantic brief")
    assert strategy1 == strategy2 == "planning_keyword_aliases"
    assert "core fantasy" in q1
    assert "character hook" in q2


def test_gbrain_briefs_preserve_split_authority_visibility() -> None:
    power = build_retrieval_brief(mode="power_seed", world_vision=WORLD)
    human = build_retrieval_brief(mode="human_seed", world_vision=WORLD)
    story = build_retrieval_brief(
        mode="idea",
        world_vision=WORLD,
        character_card="# CHARACTER CARD\n石砚与两处同身。",
    )

    assert "一人通常只能维持一种稳定主承载" in power
    assert "宋甲" not in power
    assert "倒悬石城" not in power
    assert "普通人住在河谷和港口" not in power

    assert "普通人住在河谷和港口" in human
    assert "宗门、世家、商盟、军府并存" in human
    assert "一人通常只能维持一种稳定主承载" not in human
    assert "宋甲" not in human
    assert "倒悬石城" not in human

    assert "宋甲正在追一名叛徒" in story
    assert "倒悬石城" in story
    assert "石砚与两处同身" in story


def test_split_creative_prompts_do_not_surface_retired_fantasy_seed_concept() -> None:
    state = _approved_state()
    state["proposal"] = {"status": "author_approved"}
    common = {
        "creative_direction": "男频修仙",
        "world_vision": WORLD,
        "character_card": "# CHARACTER CARD\n\n## POWER CORE\n两处同身\n\n## HUMAN CORE\n石砚。",
        "character_initial_state": "# INITIAL CHARACTER STATE\n\n## current_desire\n找回那个声音。",
        "creative_state": state,
        "proposal_context": "PROGRAM",
    }
    prompts = [
        generate_split_prompt(mode="world_vision", creative_direction="男频修仙"),
        generate_split_prompt(mode="power_seed", **common),
        generate_split_prompt(mode="human_seed", **common),
        generate_split_prompt(mode="idea", **common),
        generate_split_prompt(mode="outline", **common),
    ]
    assert all("Fantasy Seed" not in prompt for prompt in prompts)
    assert all("FANTASY_SEED" not in prompt for prompt in prompts)
