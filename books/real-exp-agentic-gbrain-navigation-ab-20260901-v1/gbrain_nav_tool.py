from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
MULTI = ROOT / r"books\real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"
SINGLE = ROOT / r"books\real-exp-private-prototype-asymmetry-pace-ruler-20260827-v1"

sys.path.insert(0, str(ROOT / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from story_mvp.gbrain import get_gbrain, resolve_openai_api_key
from story_mvp.gbrain_retrieval import (
    MODE_ALLOWED_CATEGORIES,
    _has_surface_conflict,
    active_inspiration_allowed,
    extract_abstract_content,
    extract_hard_constraints,
    retrieve_gbrain,
    source_category,
)
from story_mvp.long_form_evolution import compose_effective_world
from heldout_fixture import heldout_a


CASES = ("ning_21_30", "ning_31_40", "wen_singleworld", "heldout_a")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def case_context(case: str) -> dict[str, str]:
    if case == "heldout_a":
        data = heldout_a()
        return {
            "mode": "story_refresh",
            "book_content": str(data["book_content"]),
            "creative_direction": str(data["creative_direction"]),
            "world_vision": compose_effective_world(
                str(data["world_vision"]),
                str(data["world_expansions"]),
                int(data["effective_from_chapter"]),
            ),
            "character_card": str(data["current_character"]),
            "proposal_context": str(data["proposal_context"]),
        }
    if case == "ning_21_30":
        return {
            "mode": "story_refresh",
            "book_content": read(MULTI / "BOOK_AFTER_CH20.md"),
            "creative_direction": (
                "《我身藏诸界》第21—30章 frozen-authority Story Refresh 回归。"
                "不改已批准 World / Character / Canon；只重新规划当前 Horizon，使局部故事成立并让已经发生的历史继续产生真实因果。"
            ),
            "world_vision": read(MULTI / "WORLD_VISION.md"),
            "character_card": read(MULTI / "CHARACTER.md"),
            "proposal_context": read(MULTI / "STORY_PROGRAM_11_20.md"),
        }
    if case == "ning_31_40":
        return {
            "mode": "story_refresh",
            "book_content": read(MULTI / "BOOK_AFTER_CH30.md"),
            "creative_direction": (
                "《我身藏诸界》第31—40章 frozen-authority Story Refresh 回归。"
                "不改已批准 World / Character / Canon；只重新规划当前 Horizon，使局部故事成立并让已经发生的历史继续产生真实因果。"
            ),
            "world_vision": read(MULTI / "WORLD_VISION.md"),
            "character_card": read(MULTI / "CHARACTER.md"),
            "proposal_context": read(MULTI / "STORY_PROGRAM_21_30.md"),
        }
    if case == "wen_singleworld":
        return {
            "mode": "idea",
            "book_content": "",
            "creative_direction": read(SINGLE / "AUTHOR_DIRECTION.md"),
            "world_vision": read(SINGLE / "WORLD_VISION.md"),
            "character_card": read(SINGLE / "CHARACTER.md"),
            "proposal_context": "",
        }
    raise ValueError(f"unknown case: {case}")


def constraints_for(context: dict[str, str]) -> list[str]:
    return extract_hard_constraints(
        context.get("creative_direction", ""),
        context.get("world_vision", ""),
        context.get("character_card", ""),
        context.get("proposal_context", ""),
        context.get("book_content", ""),
    )


def search(case: str, query: str) -> dict:
    context = case_context(case)
    mode = context["mode"]
    result = retrieve_gbrain(
        mode=mode,
        book_content=context.get("book_content", ""),
        creative_direction=context.get("creative_direction", ""),
        world_vision=context.get("world_vision", ""),
        character_card=context.get("character_card", ""),
        proposal_context=context.get("proposal_context", ""),
        query_override=query,
    )
    return {
        "case": case,
        "mode": mode,
        "query": query,
        "semantic_query_available": bool(resolve_openai_api_key()),
        "accepted_count": result["accepted_count"],
        "accepted": [
            {
                "slug": item["slug"],
                "type": item["type"],
                "score": item["score"],
                "abstract": item["abstract"],
                "transfer_boundary": item.get("transfer_boundary", ""),
            }
            for item in result["accepted"]
        ],
        "rejected_count": result["rejected_count"],
    }


def get(case: str, slug: str) -> dict:
    context = case_context(case)
    mode = context["mode"]
    category = source_category(slug)
    if category not in MODE_ALLOWED_CATEGORIES[mode]:
        raise ValueError(f"{mode} does not allow category {category or '<unknown>'}")
    page = get_gbrain(slug)
    if not active_inspiration_allowed(page):
        raise ValueError("card is not active inspiration")
    abstract, transfer_boundary = extract_abstract_content(page)
    if not abstract:
        raise ValueError("card has no source-blind abstract")
    constraints = constraints_for(context)
    if _has_surface_conflict(abstract, constraints):
        raise ValueError("card conflicts with frozen hard constraints")
    return {
        "case": case,
        "mode": mode,
        "slug": slug,
        "type": category,
        "abstract": abstract,
        "transfer_boundary": transfer_boundary,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Bounded source-blind GBrain navigation tool for one experiment.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search")
    p_search.add_argument("--case", required=True, choices=CASES)
    p_search.add_argument("--query", required=True)

    p_get = sub.add_parser("get")
    p_get.add_argument("--case", required=True, choices=CASES)
    p_get.add_argument("--slug", required=True)

    args = parser.parse_args()
    payload = search(args.case, args.query) if args.command == "search" else get(args.case, args.slug)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
