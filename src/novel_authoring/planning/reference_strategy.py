"""Small deterministic selector for ordinary continuation planning references."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from novel_authoring.planning.models import PlanningReferenceStrategy
from novel_authoring.utils import stable_id

_TYPE_ORDER = {"contrast-card": 0, "mechanism-card": 1, "corpus-synthesis": 2}
_QUERY_DIMENSIONS = (
    "creative_problem_tags",
    "reader_experiences",
    "narrative_drives",
    "payoff_channels",
    "scene_functions",
)


def _card_sort_key(card: Mapping[str, Any]) -> tuple[int, int, str]:
    card_type = str(card.get("card_type") or "")
    fields = card.get("metadata_match_fields")
    match_count = len(fields) if isinstance(fields, Sequence) and not isinstance(fields, str) else 0
    return (_TYPE_ORDER.get(card_type, 9), -match_count, str(card.get("card_id") or ""))


def _tokens(value: object) -> set[str]:
    import re

    tokens: set[str] = set()
    for run in re.findall(r"[\u4e00-\u9fff]+|[A-Za-z0-9_]+", str(value or "")):
        if re.fullmatch(r"[\u4e00-\u9fff]+", run):
            tokens.update(run[index : index + 2] for index in range(len(run) - 1))
        else:
            tokens.add(run.casefold())
    return {item for item in tokens if len(item) >= 2}


def _card_text(card: Mapping[str, Any]) -> set[str]:
    values: list[object] = []
    for key, value in card.items():
        if key in {"source_refs", "source_book_ids", "metadata_match_fields"}:
            continue
        if isinstance(value, Mapping):
            values.extend(value.values())
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            values.extend(value)
        else:
            values.append(value)
    return _tokens(" ".join(str(item) for item in values))


def _query_context(
    snapshot: Mapping[str, Any],
    *,
    creative_problem: str | None,
    reader_experiences: Sequence[str] | None,
    narrative_drives: Sequence[str] | None,
    payoff_channels: Sequence[str] | None,
    scene_functions: Sequence[str] | None,
) -> tuple[str, dict[str, list[str]]]:
    original = snapshot.get("original_query")
    source = original if isinstance(original, Mapping) else snapshot
    problem = (
        str(creative_problem)
        if creative_problem is not None
        else str(snapshot.get("creative_problem") or source.get("creative_problem") or "")
    )
    context: dict[str, list[str]] = {}
    for field, override in (
        ("reader_experiences", reader_experiences),
        ("narrative_drives", narrative_drives),
        ("payoff_channels", payoff_channels),
        ("scene_functions", scene_functions),
        ("creative_problem_tags", None),
    ):
        values = override if override is not None else source.get(field, [])
        context[field] = (
            [str(item) for item in values]
            if isinstance(values, Sequence) and not isinstance(values, (str, bytes))
            else []
        )
    return problem, context


def _card_relevance(
    card: Mapping[str, Any],
    *,
    problem: str,
    dimensions: Mapping[str, Sequence[str]],
    recent_signature_tokens: set[str],
) -> int:
    query_tokens = _tokens(problem)
    for values in dimensions.values():
        query_tokens.update(_tokens(" ".join(values)))
    card_tokens = _card_text(card)
    score = len(query_tokens & card_tokens)
    matched_fields = card.get("metadata_match_fields", [])
    if isinstance(matched_fields, Sequence) and not isinstance(matched_fields, (str, bytes)):
        score += 4 * sum(
            bool(dimensions.get(str(field))) for field in matched_fields
        )
    for field, values in dimensions.items():
        if not values:
            continue
        card_values = card.get(field, [])
        if isinstance(card_values, Sequence) and not isinstance(card_values, (str, bytes)):
            score += 3 * len(
                {_item.casefold() for _item in map(str, values)}
                & {_item.casefold() for _item in map(str, card_values)}
            )
    if recent_signature_tokens:
        score -= min(3, len(recent_signature_tokens & card_tokens))
    return score


def _solution_score(solution: Mapping[str, Any], query_tokens: set[str]) -> int:
    values = [
        solution.get("label"),
        solution.get("description"),
        solution.get("conditions"),
        solution.get("reader_experience_differences"),
        solution.get("tradeoffs"),
        solution.get("failure_risks"),
    ]
    return len(query_tokens & _tokens(" ".join(str(item) for item in values)))


def select_planning_reference_strategy(
    snapshot: Mapping[str, Any],
    *,
    recent_card_ids: Sequence[str] = (),
    recent_solution_ids: Sequence[str] = (),
    creative_problem: str | None = None,
    reader_experiences: Sequence[str] | None = None,
    narrative_drives: Sequence[str] | None = None,
    payoff_channels: Sequence[str] | None = None,
    scene_functions: Sequence[str] | None = None,
    recent_signatures: Sequence[Mapping[str, Any]] = (),
) -> PlanningReferenceStrategy:
    """Select at most three compact cards and record a no-card fallback.

    This selector only sees the already-frozen compact snapshot.  It never
    reads source prose, creates embeddings, or changes Candidate/Canon state.
    """

    snapshot_id = str(snapshot.get("snapshot_id") or "") or None
    snapshot_hash = str(snapshot.get("snapshot_hash") or "") or None
    raw_cards = snapshot.get("compact_cards", [])
    cards = (
        [dict(item) for item in raw_cards if isinstance(item, Mapping)]
        if isinstance(raw_cards, Sequence)
        else []
    )
    problem, dimensions = _query_context(
        snapshot,
        creative_problem=creative_problem,
        reader_experiences=reader_experiences,
        narrative_drives=narrative_drives,
        payoff_channels=payoff_channels,
        scene_functions=scene_functions,
    )
    recent_signature_tokens = _tokens(
        " ".join(
            str(value)
            for signature in recent_signatures
            for value in signature.values()
            if not isinstance(value, (dict, list))
        )
    )
    cards.sort(
        key=lambda card: (
            -_card_relevance(
                card,
                problem=problem,
                dimensions=dimensions,
                recent_signature_tokens=recent_signature_tokens,
            ),
            *_card_sort_key(card),
        )
    )
    recent = {str(item) for item in recent_card_ids}
    recent_solutions = {str(item) for item in recent_solution_ids}
    selected: list[dict[str, Any]] = []
    reused = False
    fresh_cards: list[dict[str, Any]] = []
    repeated_cards: list[dict[str, Any]] = []
    for card in cards:
        card_id = str(card.get("card_id") or "")
        if not card_id:
            continue
        solution_ids = {
            str(solution.get("solution_id") or solution.get("label") or "")
            for solution in card.get("solutions", [])
            if isinstance(solution, Mapping)
        }
        if card_id in recent or recent_solutions.intersection(solution_ids):
            repeated_cards.append(card)
        else:
            fresh_cards.append(card)
    for card in [*fresh_cards, *repeated_cards]:
        if card in repeated_cards:
            reused = True
        selected.append(card)
        if len(selected) == 3:
            break
    if not selected and cards:
        selected = cards[:3]
        reused = True
    selected_ids = [str(card["card_id"]) for card in selected]
    contrast_solutions: list[str] = []
    query_tokens = _tokens(problem)
    for values in dimensions.values():
        query_tokens.update(_tokens(" ".join(values)))
    failure_modes: list[str] = []
    for card in selected:
        if str(card.get("card_type")) == "contrast-card":
            solutions = [
                solution
                for solution in card.get("solutions", [])
                if isinstance(solution, Mapping)
            ]
            if solutions:
                selected_solution = sorted(
                    solutions,
                    key=lambda solution: (
                        -_solution_score(solution, query_tokens),
                        str(solution.get("solution_id") or solution.get("label") or ""),
                    ),
                )[0]
                value = str(
                    selected_solution.get("solution_id")
                    or selected_solution.get("label")
                    or ""
                )
                if value:
                    contrast_solutions.append(value)
        for key in ("failure_risks", "when_not_to_use"):
            values = card.get(key, [])
            if isinstance(values, Sequence) and not isinstance(values, str):
                failure_modes.extend(str(item) for item in values if str(item).strip())
    strategy_id = stable_id(
        "planning-reference-strategy",
        snapshot_id or "NO_SNAPSHOT",
        snapshot_hash or "NO_HASH",
        ",".join(selected_ids),
    )
    status = str(snapshot.get("status") or "")
    match_tier = str(
        snapshot.get("match_tier")
        or (
            "ZERO_RESULTS"
            if not selected or (status and status != "ENABLED")
            else "EXACT"
        )
    )
    if selected:
        used_dimensions = [
            field
            for field, values in dimensions.items()
            if values and any(
                field in (card.get("metadata_match_fields") or [])
                for card in selected
            )
        ]
        dimension_text = "、".join(used_dimensions) or "creative_problem"
        card_text = "、".join(selected_ids)
        solution_text = (
            f"；仅选对照方案 {contrast_solutions[0]}"
            if contrast_solutions
            else ""
        )
        summary = (
            f"按 {dimension_text} 从冻结卡片中选择 {card_text}{solution_text}；"
            "仅迁移可复用机制，当前书事实、状态与最终选择仍由本次合同决定。"
        )
        reason = "复用近期卡片并未找到更合适的 bounded card" if reused else None
    else:
        summary = "当前没有可用 Reference Corpus card；候选生成沿用当前书的冻结 Boundary/Kernel。"
        reason = "ZERO_RESULTS_OR_REFERENCE_UNAVAILABLE"
    return PlanningReferenceStrategy(
        strategy_id=strategy_id,
        snapshot_id=snapshot_id,
        snapshot_hash=snapshot_hash,
        selected_card_ids=selected_ids,
        selected_cards=selected,
        selected_contrast_solutions=contrast_solutions,
        application_summary=summary,
        failure_modes=list(dict.fromkeys(failure_modes)),
        match_tier=match_tier,
        reuse_reason=reason,
    )


__all__ = ["select_planning_reference_strategy"]
