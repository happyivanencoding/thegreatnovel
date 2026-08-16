"""Small deterministic selector for ordinary continuation planning references."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from novel_authoring.planning.models import PlanningReferenceStrategy
from novel_authoring.utils import stable_id

_TYPE_ORDER = {"contrast-card": 0, "mechanism-card": 1, "corpus-synthesis": 2}


def _card_sort_key(card: Mapping[str, Any]) -> tuple[int, int, str]:
    card_type = str(card.get("card_type") or "")
    fields = card.get("metadata_match_fields")
    match_count = len(fields) if isinstance(fields, Sequence) and not isinstance(fields, str) else 0
    return (_TYPE_ORDER.get(card_type, 9), -match_count, str(card.get("card_id") or ""))


def select_planning_reference_strategy(
    snapshot: Mapping[str, Any],
    *,
    recent_card_ids: Sequence[str] = (),
    recent_solution_ids: Sequence[str] = (),
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
    cards.sort(key=_card_sort_key)
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
    failure_modes: list[str] = []
    for card in selected:
        if str(card.get("card_type")) == "contrast-card":
            for solution in card.get("solutions", []):
                if isinstance(solution, Mapping):
                    value = str(solution.get("solution_id") or solution.get("label") or "")
                    if value and value not in contrast_solutions:
                        contrast_solutions.append(value)
                if len(contrast_solutions) >= 3:
                    break
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
        summary = (
            "只把冻结 Reference Corpus 的机制/对照作为参考；候选的事实、状态与选择"
            "仍由当前书上下文决定。"
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
