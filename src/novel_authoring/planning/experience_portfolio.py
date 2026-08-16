"""Edition-aware structural experience portfolio diagnostics."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from novel_authoring.continuation_quality import structural_overlap
from novel_authoring.planning.models import (
    ChapterExperienceSignature,
    SerialExperiencePortfolio,
)


def _horizon_for(
    signature: ChapterExperienceSignature,
    *,
    current_chapter: int | None,
    policy: Mapping[str, int | None],
) -> str | None:
    if current_chapter is None or signature.chapter_ordinal is None:
        return None
    age = max(0, current_chapter - signature.chapter_ordinal)
    short = policy.get("SHORT")
    mid = policy.get("MID")
    if short is not None and age <= short:
        return "SHORT"
    if mid is not None and age <= mid:
        return "MID"
    if policy.get("LONG") is not None:
        return "LONG"
    return None


def build_serial_experience_portfolio(
    signatures: Sequence[ChapterExperienceSignature | Mapping[str, Any]],
    *,
    current_chapter: int | None = None,
    horizon_policy: Mapping[str, int | None] | None = None,
    reader_promise_targets: Sequence[str] = (),
) -> SerialExperiencePortfolio:
    """Build a diagnostic portfolio without a fixed history window."""

    policy = {
        str(key).upper(): (None if value is None else int(value))
        for key, value in (horizon_policy or {}).items()
    }
    parsed = [
        item
        if isinstance(item, ChapterExperienceSignature)
        else ChapterExperienceSignature.model_validate(item)
        for item in signatures
    ]
    counts: dict[str, int] = {}
    unknown = 0
    for signature in parsed:
        horizon = _horizon_for(
            signature,
            current_chapter=current_chapter,
            policy=policy,
        )
        if horizon is None:
            unknown += 1
        else:
            counts[horizon] = counts.get(horizon, 0) + 1
    repeated: list[dict[str, Any]] = []
    for left_index, left in enumerate(parsed):
        left_payload = left.model_dump(mode="json")
        for right_index in range(left_index + 1, len(parsed)):
            right = parsed[right_index]
            overlap = structural_overlap(left_payload, right.model_dump(mode="json"))
            if overlap["repeated"]:
                repeated.append(
                    {
                        "left_index": left_index,
                        "right_index": right_index,
                        **overlap,
                    }
                )
    targets = list(
        dict.fromkeys(
            str(item).strip() for item in reader_promise_targets if str(item).strip()
        )
    )
    underserved = [
        target
        for target in targets
        if not any(
            target.casefold()
            in " ".join(
                str(value)
                for value in signature.model_dump(mode="json").values()
                if value not in (None, "")
            ).casefold()
            for signature in parsed
        )
    ]
    return SerialExperiencePortfolio(
        current_chapter=current_chapter,
        horizon_policy=policy,
        signatures=parsed,
        horizon_counts=counts,
        unknown_horizon_count=unknown,
        repeated_structure_pairs=repeated,
        reader_promise_targets=targets,
        underserved_reader_promises=underserved,
    )


__all__ = ["build_serial_experience_portfolio"]
