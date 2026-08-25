# Theme Emergent A/B — Frozen Rules

## Goal
Test whether removing upstream semantic escalation produces more commercial male-progression worlds without weakening novelty.

## A / B
- A = current production Fantasy Seed → World Vision → Story Program prompts.
- B = experiment-only prompt projection. It does not edit production prompts before results are known.

## Frozen model route
- Fantasy Seed: GPT-5.6 Luna, high, GBrain OFF.
- World Vision: GPT-5.6 Luna, high, GBrain ON with current fixed Coordinate Reference + creative inspirations.
- Story Program: GPT-5.6 Sol, high, GBrain ON with current production retrieval.

## Frozen selection
For every arm and every book, continue Candidate 1. No post-hoc selection.

## Three author directions
1. Cultivation / sect / combat / treasure / secret realm. Core advantage is unconstrained by the author; prioritize concrete power possession and acquisition.
2. Eastern fantasy frontier / monsters / ancient ruins / exploration / martial growth. Prioritize dangerous maps, creatures, equipment, materials, companions and personal power.
3. High-martial dynasty / cities / clans / arenas / war / inheritance. Prioritize fighting growth, status ascent, techniques, weapons, masters, rivals and concrete opportunities.

No direction specifies a philosophy, moral thesis, destiny/autonomy theme, or exact ability.

## Predeclared evaluation
1. Philosophy-as-backbone leakage.
2. Independent-world life: would the world still make sense without the protagonist/core advantage?
3. Concrete desire/materiality: named things, places, powers, equipment, opportunities, positions readers want.
4. Core-advantage ↔ world-ontology isomorphism.
5. Plot-engine diversity and opponent autonomy.
6. Male-progression acquisition loop: obtain → possess → use → display → seek higher-value target.
7. Core novelty / fantasy strength retained.
8. Backend-language leakage: action space, irreversible state, expectation ladder, etc. becoming world material.

No cherry-picking. Compare all three pairs and aggregate.

## Clean-pass rule
ACP may append `<oai-mem-citation>` metadata to a final answer. These blocks are not story content. Before one generated stage becomes input to the next stage, the experiment strips the entire block deterministically. The first Program/Judge pass discovered before this sanitation was archived as `*_pass1_with_world_meta.*` and is not used for final scores.
