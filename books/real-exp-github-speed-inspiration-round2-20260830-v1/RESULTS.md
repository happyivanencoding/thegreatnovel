# GitHub Speed Inspiration Round 2｜2026-08-30

## Goal

Search contemporary long-form fiction / novel-agent projects for execution ideas that could reduce TGN latency without lowering Story or Authority quality. Do not re-run already rejected TGN ideas under new names.

Production baseline remains the five-node chapter chain. No production code was changed in this round.

## External inspiration inspected

- novel-studio: sealed/projected arc, promotion/receipt, async/post-generation extraction patterns.
- ainovel-cli: deterministic engine, step checkpoint, append-only state changes, small agent surface.
- openovel: foreground prose separated from background memory/state maintenance.
- EMBER: typed BookStateDiff after accepted draft.
- LangGraph-based-Novel-by-Agents / InStoryBook-style systems: batch parallel chapter generation after frozen planning.
- NovelForge-like systems: rules/skills on demand.

## Experiments

### 1. Cache-aware Curator block reorder — FAIL

Same Curator content, only moved book-stable blocks earlier to lengthen provider prefix.

Screen showed apparent wall improvement (~21.4%), but `cachedReadTokens` decreased by ~7,509/chapter. The causal chain `longer stable prefix -> more cached tokens -> lower wall` did not hold, so the wall difference was treated as provider noise. No repeat or downstream blind was justified.

### 2. Projected-outcome overlap Director — FAIL at Mission Gate

Inspired by seal/promote. After previous Final prose, construct a provisional deterministic outcome from Frozen Mission while State Extraction runs, then start next Director early.

The mission blind exposed state-closure loss (for example, missing the returned old crossbow state in one transition). TGN does not currently have a pre-prose projected-state substrate equivalent to novel-studio. No downstream run.

### 3. Hedged Curator — FAIL speed gate

Two identical Luna-high Curator calls raced; retain both, use the faster response only if speed screen passes.

- single-call counterfactual mean: 85.05s
- hedged mean: 74.06s
- saved: 10.98s/chapter
- relative: 12.9%
- request factor: 2x

Pre-registered gate was >=20%. Rejected before quality blind.

### 4. Hedged Authority Reviser — FAIL speed gate

Four frozen Reviser prompts, two identical Luna-high calls each.

- single-call counterfactual mean: 149.59s
- hedged mean: 135.15s
- saved: 14.44s/chapter
- relative: 9.65%
- request factor: 2x

Two samples saved ~26s, two saved only ~2–3s. Pre-registered gate required >=20% and >=20s/chapter. Rejected before quality blind.

### 5. Parallel State ledgers — FAIL speed gate

Split Luna-low State into two concurrent lanes:

- Lane A: Active Scene State + Chapter Summary
- Lane B: Persistent Canon + Open Promises

Fresh V2 cross-book screen:

- control mean: 26.260s
- parallel mean: 20.494s
- saved: 5.766s/chapter
- relative: 21.96%
- request factor: 2x

Gate required >=25% and >=5s/chapter. Absolute threshold passed, percent threshold failed. No State quality blind.

### 6. Append-only State change log — FAIL

Inspired by `state_changes.jsonl`: keep Active Scene + Summary full, but make Persistent Canon and Open Promises emit KEEP/REPLACE/REMOVE/ADD deltas.

Historical static analysis showed meaningful repetition mainly in Open Promises (~55.8% line retention) and Persistent Canon (~29.8%). Real Luna-low screen nevertheless got slower:

- full-State mean: 26.683s
- change-log mean: 31.620s
- delta: -4.937s/chapter
- relative: -18.50%
- output tokens also increased in all four samples.

Conclusion: for a ~1k-character State, diff protocol reasoning costs more than rewriting the compact state.

### 7. Exact duplicate removal in Reviser — NO CANDIDATE

Measured exact repeated lines/paragraphs across Frozen Mission, Curator, Watch, Power/Human and other Reviser blocks on four held-out prompts.

- exact duplicate line ratio: 0%
- exact duplicate paragraph ratio: 0%

TGN's earlier context bounding has already removed this easy waste.

### 8. Scene Skill on-demand shortlist — FAIL static gate

Curator Scene Skill Catalog occupies about 1.3k–3.2k chars (up to ~14% of tested Curator prompts). Tested deterministic character-ngram retrieval of Top-4 skills from Frozen Mission + Active Scene State, using official skill descriptions only.

Against the actual Curator Primary/Secondary choices, 0/4 chapters had full expected skill coverage. Increasing K would erase most input savings; adding an LLM router would add a new call. No LLM A/B.

### 9. Arc Seal -> parallel render — FAIL Seal Gate

This was the highest-upside novel-studio-inspired experiment.

A Luna-high Arc Projector saw only pre-generation authority (World, Character, Story Program, Outline, Ch1 T0 Canon), not any sequential chapter prose/Director/State. It projected Ch1–Ch4 missions and post-state before prose.

- Projector wall: 166.003s
- four chapters structurally present
- power position remained exact at 星力3级
- no illegal early Ch4 reward acquisition found

However, projected state missed prose-realization facts that materially carry into later chapters:

- projected Ch1 injuries: none; actual Ch1: palm/arm heat and numbness
- projected Ch2 injuries: none; actual Ch2: palm swelling/pain
- projected Ch3 injuries: none; actual Ch3 carries the palm pain into final calibration
- projected Ch4 injuries: none; actual Ch4 has shoulder/chest/palm damage

These are not cosmetic details: fatigue/injury changes the next chapter's action conditions. Therefore the projected `post_state(n)` is not safe as `pre_state(n+1)`. Parallel Curator/Primary/Reviser was not launched.

Conclusion: TGN cannot copy parallel chapter rendering without first adding a trustworthy pre-prose world/realization simulation layer; adding that layer purely for speed is out of scope.

### 10. Combined Director + Curator Planning Pass — FAIL speed gate

Single Luna-high call first freezes an eight-field Mission and then emits the Curator packet. Writer/Reviser remain separate.

Held-out four-chapter screen:

| Chapter | Sequential historical D+C | Combined | Change |
|---|---:|---:|---:|
| 1 | 134.363s | 107.947s | +19.66% |
| 2 | 83.779s | 100.269s | -19.68% |
| 3 | 199.470s | 116.320s | +41.69% |
| 4 | 139.827s | 128.608s | +8.02% |

Mean:

- sequential planning: 139.360s
- combined planning: 113.286s
- saved: 26.074s/chapter
- relative: 18.71%

Pre-registered gate required >=25% and >=20s/chapter. Absolute threshold passed, percentage threshold failed; variance was high and Ch2 regressed. No Primary/Reviser or blind evaluation was justified.

### 11. Foreground final prose + background State — DIRECTIONAL PASS for perceived latency only

Inspired by openovel's foreground narrator / background maintenance separation.

No semantic change is needed: State already consumes the accepted/final Authority Revision and does not alter that prose. Historical 20-chapter baseline:

- full chain including State: 370.299s/chapter
- time to final readable prose (through Reviser): 342.860s/chapter
- State tail that could be hidden behind author reading: 27.439s/chapter
- median hidden tail: 27.267s
- visible wait reduction: 7.59%
- State range: 23.240–32.466s

This does **not** reduce headless continuous generation total wall, because next-chapter Director still needs committed State. It can reduce interactive `Generate -> I can start reading` latency by ~27s/chapter.

Current PROJECT_RULES explicitly excludes frontend changes in this latency round, so this was not productionized here.

## Overall verdict

No new first-generation semantic/runtime route passed the production gate in this round.

What did survive:

1. Previously productionized Exact-Input Receipt remains the strongest zero-quality-risk optimization for incremental regeneration/stale recovery.
2. Foreground prose + background State is a clean product-latency direction for a future frontend/runtime round: ~27.44s earlier readable prose on the real 20-chapter baseline, with no claim of headless throughput improvement.
3. Provider-native `prompt_cache_key` / cache breakpoint remains worth testing if TGN's direct OpenAI API execution is later configured; ACP currently does not expose those controls, so no valid real A/B was possible in this round.

What this round strongly rejects as current defaults:

- block reorder as cache optimization;
- projected next-Director without a true sealed world-state substrate;
- Curator/Reviser hedging at 2x requests;
- two-lane State extraction;
- LLM state diff grammar;
- deterministic lexical Scene Skill shortlist;
- arc-level parallel render using plan-only projected state;
- merged Director+Curator planning pass.

Production code changed: **NO**.
Docs / PROJECT_RULES / Steward / handoff changed: **NO**, because no production/default rule changed.
