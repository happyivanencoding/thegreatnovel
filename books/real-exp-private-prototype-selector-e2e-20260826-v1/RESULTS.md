# Private Prototype Selector — Production E2E Audit

Date: 2026-08-26
Prototype: `prism-wanderer-alpha` (anonymous, explicit-only)

## Final Verdict

**PASS / PRODUCTION SELECTOR VALIDATED**

Sub-verdicts:

- Explicit selector engineering: **PASS**
- Default privacy / no-silent-retrieval: **PASS**
- Human projection: **PASS**
- Power blindness / Story-hook isolation: **PASS**
- Deterministic Character merge: **PASS**
- Sol Collision: **PASS_WITH_RESIDUAL_CANDIDATE_RISK**

The residual risk is not an authority leak. The selected fictional Human begins in a river-port freight/accounting environment, so the first two phases still reuse bookkeeping / contract facts more than ideal. The story nevertheless escapes that occupational gravity after the early arc and does not turn the Power or the whole novel into professional optimization.

## 1. What Was Engineering-Tested

Production now exposes an explicit Human-only selector. `prism-wanderer-alpha` is not a search keyword. It resolves to an allow-listed opaque prototype spec with exactly three GBrain pages:

- Appetite: `book-dna/private-prototype-pwaalpha-appetite-v1`
- Behavior: `book-dna/private-prototype-pwaalpha-choice-bias-v1`
- Relationship: `book-dna/private-prototype-pwaalpha-relationship-v1`

The selector is default-off and is ignored outside `human_seed`. Explicit mode uses zero semantic/keyword queries and fails closed if any lane is absent, inactive, has the wrong prototype ID, or declares the wrong lane.

The `/api/prompt` path automatically resolves the exact three-lane bundle when the selector is present, so the author does not need to manually query GBrain or remember private aliases. The selector itself is generation metadata only and never enters Character Canon.

## 2. Frozen E2E Inputs

To isolate the selector variable, World and Power were not regenerated.

- World: previously validated protagonist-blind traditional cultivation world `澜照界`.
- Power: previously blind-selected `分流真元`.
- Human: newly generated through the production explicit-prototype selector.
- Character: deterministic composition; no Composer LLM.
- Story Program: current production native Collision compiler, GPT-5.6 Sol high.
- No Outline or prose was run.

## 3. Pre-Run Isolation

```json
{
  "prototype_selected": true,
  "lane_counts": {
    "appetite": 1,
    "behavior": 1,
    "relationship": 1
  },
  "query_texts": [],
  "power_leaks": {},
  "story_hook_leaks": {},
  "prompt_sha256": "5eceda2b4592212434077111f858944ae732012ba6ebff87d510d9efbabab35a",
  "prompt_chars": 6930,
  "default_candidate_contract_hits": 0,
  "single_seed_contract_hits": 2,
  "legacy_fab_hits": 0
}
```

Important points:

- exact three private Human lanes: 3/3;
- search queries: 0;
- Power leaked into Human prompt: 0;
- named Story Opportunities leaked into Human prompt: 0;
- legacy four-candidate contract: 0;
- legacy mandatory Formative→Adaptation→Behavior contract: 0.

## 4. Human Result

Luna high generated exactly one fictionalized Human Seed:

> **谢临川／河港货栈的未定账房**

The output does not contain the prototype ID or private evidence IDs. It keeps multiple competing motives rather than one life thesis:

1. wants high-weight recognition and an undeniable win;
2. directly values color, sound, temperature, food and well-made objects;
3. retains explicit body attraction / intimacy / sexual desire as a real choice variable;
4. wants movement, unfamiliar cities, strange crafts and non-repetitive periods of life.

The motives conflict: travel savings compete with aesthetic consumption / meals / a concrete person; recognition competes with aversion to a fixed institutional role; a safe long contract can lose to vivid companionship.

Relationship Gravity is concrete. Without 温梨, he would have taken an out-of-state long-term bookkeeping job. Because this specific person wanted to see an obscure kiln market, he changed route, spent six days travelling, lost the job and paid the travel cost. The Human text also explicitly preserves physical attraction rather than translating it into spiritual compatibility.

Machine audit:

```json
{
  "human_seed_heading_count": 1,
  "candidate_heading_count": 0,
  "prototype_identifier_leaks": {},
  "power_leaks": {},
  "relationship_choice_delta_markers": {
    "本会": 1,
    "因为是她": 1,
    "改变路线": 1,
    "错过了那份工作": 1,
    "盘缠损失": 1
  },
  "sexuality_markers": {
    "身体吸引": 2,
    "身体靠近": 1,
    "气味": 1,
    "触碰": 1,
    "喜欢她的身体": 1
  },
  "competing_motive_markers": {
    "被看见": 1,
    "胜出": 1,
    "色彩": 1,
    "食物": 1,
    "身体吸引": 2,
    "离开熟悉的河港": 1
  },
  "character_reconciliation_hits": 0,
  "model": "gpt-5.6-luna",
  "effort": "high",
  "wall_seconds": 99.154
}
```

Residual Human risk: the family/occupation is still more thematically aligned with some early behavior than ideal. This is candidate-level drift, not Power↔Biography leakage.

## 5. Deterministic Character

`CHARACTER.md` is simply:

- frozen Power Core: `分流真元`;
- frozen Human Core: 谢临川;
- no reconciliation prose.

The automated reconciliation check found 0 hits. The Human Seed itself had 0 Power leaks.

## 6. Story Program / Collision Result

Sol high completed in 550.344 seconds and produced 7 large stages. Prototype identifiers remained absent.

The opening collision is correct:

> 谢临川没有力量也会想离开河港、看陌生城镇、买自己真心喜欢的东西，并在真正有分量的人面前赢一次。分流真元能帮助他获得通行资格和公开胜利，却不能替他决定该留在宗门、跟温梨改道，还是回家接船。

The Power is not explained as his destiny. Instead, the collision creates a new temptation: because split qi lets him preserve two actions at once, he can start overestimating how many goals / people / outcomes he can keep simultaneously. This is acceptable **post-collision chemistry**, not retrospective biography rationalization.

### Strongest proof: Stage 4

`西州燃雨，错过那艘船` contains **no Power / Capability Delta and no Possession Delta**. It is driven by:

- 温梨 choosing to stay in a disaster workshop;
- 谢临川 explicitly leaving the sect for her, not on mission;
- physical attraction, old conflict and renewed intimacy;
- losing the safest Black-Sun-Island opportunity;
- incomplete knowledge about the burning rain.

The Story Program itself says the relationship/disaster arc is not converted into a prerequisite for the next upgrade. This is strong evidence that the explicit self-prototype did not reintroduce Fantasy-Engine ownership of every stage.

### Longitudinal growth remains intact

The global Power spine contains six observable changes, from first stable two-flow control through ratio swapping, moving-while-casting, heterogeneous flows + recombination, multi-node coordination and final legendary battlefield recombination. Local no-upgrade is legal; whole-book no-growth is not.

### Relationship / sexuality remains real

温梨 has independent work, travel and craft motives. Her body, proximity, response and history alter the protagonist's route. She can make him miss opportunities, stay, leave, return or delay evacuation. She does not become a permanent companion or moral reward.

### World independence remains real

Mine ownership, sect succession, burning rain, Black Sun Island, northern migration and royal/military claims already have actors with independent goals. They are not generated as tests of split qi. Enemies only develop mechanical counterplay after observing the protagonist.

Machine Story audit:

```json
{
  "model": "gpt-5.6-sol",
  "effort": "high",
  "wall_seconds": 550.344,
  "chars": 8987,
  "stage_count": 7,
  "prototype_identifier_leaks": {},
  "reconciliation_suspect_count": 0,
  "reconciliation_samples": [],
  "power_delta_stage_count": 6,
  "relationship_delta_stage_count": 6,
  "sexuality_markers": {
    "身体吸引": 1,
    "身体的靠近": 1,
    "身体": 3,
    "欲望": 1,
    "亲密": 2
  },
  "human_appetite_markers": {
    "被看见": 2,
    "赢": 7,
    "喜欢": 1
  }
}
```

Stage-level summary:

| Stage | Power Delta | Relationship Delta | Key engine |
|---|---:|---:|---|
| 1 万灯河夜渡 | yes | yes | world + recognition + first fantasy proof |
| 2 赤脉山，不做无名账房 | yes | yes | world resource conflict + recognition |
| 3 九檐试剑，赢给谁看 | yes | yes | competition + institutional recognition |
| 4 西州燃雨，错过那艘船 | **no** | yes | relationship + disaster + opportunity loss |
| 5 黑日岛，抢一艘会自己航行的船 | yes | no | exploration + high-value acquisition |
| 6 寒关以北，谁有权征用他的船 | yes | yes | war/world conflict + ownership + misjudgment |
| 7 黑日再临，无人替他定航向 | yes | yes | multi-faction world collision + relationship + legendary payoff |

Six of seven very large stages do contain a Power delta. In isolation that number is worth watching, but it matches the explicit six-step whole-book growth spine and includes a clean no-Power relationship/world stage. It is not currently evidence that the old per-stage upgrade tax returned.

## 7. Default Privacy Regression

Ordinary Human retrieval after this feature remains safe:

```json
{
  "query_strategy": "human_lane_queries",
  "accepted": [
    {
      "lane": "appetite",
      "slug": "mechanisms/private-appetite-continuity-v1",
      "score": 0.3176
    }
  ],
  "prototype_accepted": [],
  "prototype_rejections": [],
  "human_lane_counts": {
    "appetite": 1,
    "behavior": 0,
    "relationship": 0
  },
  "gbrain_default_prototype_safe": true
}
```

No private prototype page is accepted without the explicit selector.

## 8. Production Decision

Freeze the explicit prototype selector as an experimental Human-only production capability.

Keep:

- default-off selector;
- exact allow-listed lane pages, no search;
- all-three-lanes or fail closed;
- one fictionalized Human Seed;
- no real biography reconstruction;
- Power blindness;
- deterministic Character;
- selector metadata never enters Canon;
- current native Collision compiler.

Do not add:

- private-prototype personality scorer;
- Character Composer;
- self-specific Power generator;
- self-specific World generator;
- extra privacy reviewer Agent;
- automatic prototype activation for ordinary books.

## 9. Next Experiment

The next valuable experiment is **not another selector test**. The selector is validated. The next step is to approve or edit this fictionalized Human + independent Power combination, then run the normal Outline and first 3–5 chapters to evaluate whether the prototype's Appetite / Behavior / Relationship variables survive actual scene writing without becoming repeated mannerisms or being purified by the Writer.
