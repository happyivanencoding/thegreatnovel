from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class HumanPrototypeSpec:
    prototype_id: str
    lane_slugs: Mapping[str, str]


# Explicit-only anonymous prototypes. These opaque IDs contain no real-world identity.
# Keeping exact page slugs here makes activation deterministic: an explicit selector is
# an authority switch, not a semantic-search hint.
HUMAN_PROTOTYPES: dict[str, HumanPrototypeSpec] = {
    "prism-wanderer-alpha": HumanPrototypeSpec(
        prototype_id="prism-wanderer-alpha",
        lane_slugs={
            "appetite": "book-dna/private-prototype-pwaalpha-appetite-v1",
            "behavior": "book-dna/private-prototype-pwaalpha-choice-bias-v1",
            "relationship": "book-dna/private-prototype-pwaalpha-relationship-v1",
        },
    ),
}


def human_prototype_spec(prototype_id: str) -> HumanPrototypeSpec | None:
    value = prototype_id.strip()
    return HUMAN_PROTOTYPES.get(value) if value else None
