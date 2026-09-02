from __future__ import annotations

import pytest

from story_mvp.gbrain_retrieval import (
    CREATIVE_PLANNING_FINAL_RESULT_LIMIT,
    POWER_NAMING_REFERENCE_SLUG,
    retrieve_gbrain,
)


def _page(heading: str, body: str, *, active: bool = True) -> str:
    active_text = "true" if active else "false"
    return (
        "---\n"
        f"active_inspiration: {active_text}\n"
        "---\n\n"
        f"## {heading}\n\n{body}\n\n"
        "## Transfer Boundary\n\n只迁移抽象 craft，不迁移来源作品表层设定。\n"
    )


def test_power_seed_fixed_naming_reference_does_not_consume_creative_slots() -> None:
    raw = "\n".join(
        [
            f"[0.99] {POWER_NAMING_REFERENCE_SLUG} -- naming craft",
            "[0.98] mechanisms/power-a -- power a",
            "[0.97] mechanisms/power-b -- power b",
            "[0.96] mechanisms/power-c -- power c",
        ]
    )
    pages = {
        POWER_NAMING_REFERENCE_SLUG: _page(
            "Guidance",
            "先把能力写成白话，再命名；世界已有词根优先，名字不得反向授权新机制。",
        ),
        "mechanisms/power-a": _page("Mechanism", "力量优势 A。"),
        "mechanisms/power-b": _page("Mechanism", "力量优势 B。"),
        "mechanisms/power-c": _page("Mechanism", "力量优势 C。"),
    }

    result = retrieve_gbrain(
        mode="power_seed",
        creative_direction="男频玄幻",
        world_vision="# PROTAGONIST-BLIND WORLD VISION\n\n## 力量体系与正常值\n普通修士以血劲战斗。",
        query_override="manual power query",
        query_func=lambda _query, **_kwargs: raw,
        page_func=pages.__getitem__,
    )

    assert result["naming_reference_count"] == 1
    assert result["naming_reference"]["slug"] == POWER_NAMING_REFERENCE_SLUG
    assert result["accepted_count"] == CREATIVE_PLANNING_FINAL_RESULT_LIMIT
    assert [item["slug"] for item in result["accepted"]] == [
        "mechanisms/power-a",
        "mechanisms/power-b",
        "mechanisms/power-c",
    ][:CREATIVE_PLANNING_FINAL_RESULT_LIMIT]
    assert "### Fixed Naming Craft Reference" in result["result"]
    assert "先把能力写成白话，再命名" in result["result"]
    assert result["fixed_references"] == [
        {
            "id": "naming_reference",
            "label": "固定命名工艺参考",
            "required": True,
            "slug": POWER_NAMING_REFERENCE_SLUG,
            "formatted_block": result["fixed_references"][0]["formatted_block"],
        }
    ]
    assert "### Fixed Naming Craft Reference" in result["fixed_references"][0]["formatted_block"]
    assert all("formatted_block" in item for item in result["accepted"])
    assert "source: mechanisms/power-a" in result["accepted"][0]["formatted_block"]


@pytest.mark.parametrize("mode", ["world_vision", "idea", "outline"])
def test_power_naming_reference_does_not_reenter_other_creative_stages(mode: str) -> None:
    raw = "\n".join(
        [
            f"[0.99] {POWER_NAMING_REFERENCE_SLUG} -- naming craft",
            "[0.98] mechanisms/plot-engine-variation-v3 -- plot",
            "[0.97] mechanisms/thread-collision-v3 -- thread",
            "[0.96] mechanisms/earned-high-value-acquisition-v3 -- reward",
        ]
    )
    pages = {
        POWER_NAMING_REFERENCE_SLUG: _page("Guidance", "命名参考。"),
        "mechanisms/plot-engine-variation-v3": _page("Mechanism", "换 Plot Engine。"),
        "mechanisms/thread-collision-v3": _page("Mechanism", "线程碰撞。"),
        "mechanisms/earned-high-value-acquisition-v3": _page("Mechanism", "高价值获得。"),
    }

    kwargs = {
        "mode": mode,
        "creative_direction": "男频玄幻",
        "query_override": "manual query",
        "query_func": lambda _query, **_kwargs: raw,
        "page_func": pages.__getitem__,
    }
    if mode in {"idea", "outline"}:
        kwargs["world_vision"] = "# PROTAGONIST-BLIND WORLD VISION\n\n## 力量体系与正常值\n普通修士用内劲。"
        kwargs["character_card"] = "# CHARACTER\n\n## POWER CORE\n能穿墙。\n\n## HUMAN CORE\n想赢。"

    result = retrieve_gbrain(**kwargs)
    accepted_slugs = [item["slug"] for item in result["accepted"]]
    assert POWER_NAMING_REFERENCE_SLUG not in accepted_slugs
    assert any(
        item["slug"] == POWER_NAMING_REFERENCE_SLUG and "只在 Power Seed 读取" in item["reason"]
        for item in result["rejected"]
    )
