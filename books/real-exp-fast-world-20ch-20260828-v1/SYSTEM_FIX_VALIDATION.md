# Chapter Authority System Fix Validation

Date: 2026-08-29

## Scope

This validation freezes two production failures exposed by the 20-chapter fast-world E2E. It does not judge the novel as a whole.

## Failure 1 — Cross-chapter spill

Real failure: Chapter 1 was planned to finish the tide-road accident, rescue people and preserve one ore cart. The Director also prematurely completed outcomes that belonged to Chapter 2: payment, post-accident accounting/social repricing, and the route-inspector conclusion. Chapter 2 then repeated them.

Root cause: Future-10 stored current events/outcomes and `结尾推动` in one raw chapter entry, while Long Block was also visible. A soft “do not cross chapters” instruction did not reliably distinguish executable event budget from next-chapter handoff.

Production fix:

- deterministically parse the current Future-10 chapter entry;
- expose `具体剧情 + 结果 / 状态变化` as `本章唯一可执行事件预算`;
- expose `结尾推动` separately as `章末 Handoff Reservation`;
- mark Long Block as stage context only, never extra chapter event authority.

Real-model regression: fresh-context Luna high rerun on the original Chapter 1 inputs stopped after rescue/cart preservation and left payment/formal settlement as next-chapter pressure. PASS.

## Failure 2 — Explicit milestone silently lost

Real failure: Chapter 19 plan explicitly approved `顾停舟本人进入镇海`. The final Director / Primary / Authority Reviser / State only established that he survived and won a 镇海-level battle. The reader was never told that his own tier had changed.

### Prompt-only attempts

The following controlled attempts all failed on the same real Chapter 19 shape:

1. make the approved outcome more visible to Director;
2. append the approved outcome beside Frozen Mission;
3. deterministically merge it into Frozen Mission and rerun Terra Primary;
4. expose a short first-class Outcome Authority to Primary/Reviser.

Models repeatedly rationalized `进入镇海` into `镇海级战绩 / 站住镇海战局`. Therefore prompt-only repair is rejected.

### Frozen production solution

1. Future-10 `结果 / 状态变化` is deterministically merged into Frozen Mission `状态变化`; Director silence cannot cancel it. Canon still wins on a real conflict.
2. A real Canon conflict may cancel/replace that outcome only through an explicit `[PLAN OUTCOME ADJUSTMENT]` in Director State Change; silence or stylistic preference cannot cancel it.
3. Run Ledger detects only narrow explicit milestone transitions inside the composed Frozen Mission, approved with verbs such as `进入 / 踏入 / 晋升 / 突破 / 成为`.
4. If the first Authority Revision still only implies that milestone through battle/atmosphere/qualification, it cannot become final source and State cannot run.
5. The same Authority Reviser gets one bounded Preservation-First `Outcome Repair` retry. It may only add the minimum causal bridge and one direct milestone statement; it cannot alter events, victory, resources, injuries, relationships, ending, or unknown facts.
6. A second miss stays failed. There is no infinite self-retry loop.
7. Web UI and Codex External apply use the same Run Ledger gate.

Real-model automatic repair: Luna high, 85.4s. It restored an explicit equivalent of `顾停舟本人已经进入镇海`; similarity to the failed Authority Revision was about 96.75%. PASS.

## Static / workflow coverage

New tests cover:

- deterministic Future-10 field parsing;
- execute-now vs handoff separation;
- Long Block context-only behavior;
- plan outcome composition into Frozen Mission;
- Primary/Reviser Outcome Authority visibility;
- explicit milestone detection vs mere battle-level implication;
- bounded one-time Reviser repair lifecycle;
- no infinite retry;
- API retrieval of prepared repair prompt;
- Codex External apply cannot bypass the repair gate.

## What This Did Not Solve

- This does not semantically judge every arbitrary sentence in `结果 / 状态变化`. The conditional repair is intentionally limited to explicit milestone transitions that must be directly legible to the reader.
- It does not create a general chapter-result scorer, reviewer, or hard gate.
- It does not guarantee that every Director will choose the best chapter ending; it prevents a demonstrated authority failure: executing reserved next-chapter settlement as current budget.
- Ordinary chapters add zero model calls. The extra Luna call happens only after an explicit milestone is approved and the first Authority Revision still fails to realize it.
