# Strict Character Architecture Experiment

This experiment reuses the previously generated protagonist-blind `澜生界` and iteratively tests the boundary between world-conditioned Character generation and story-opportunity leakage.

Final candidate architecture separates three authorities without adding an LLM stage:

- `STORY_OPPORTUNITY_LAYER`: named events/NPCs/places/mysteries, hidden from Character generation.
- `POWER_BASELINE`: world power laws + Normal/Rarity, used to generate Core Fantasy / Legal Exception and long-form growth compatibility.
- `LIFE_CONTEXT`: ordinary life + social reality + generic values + knowledge boundary, used to generate upbringing, desire, behavior and relationships.

The final v4 Character contract is `Power-System-First + Life-Conditioned + Male Progression Growth Compatibility`.

No Story Program, Outline, chapter generation, or LLM judge is run in this experiment. Sol is intentionally deferred until human audit approves a Character Card.
