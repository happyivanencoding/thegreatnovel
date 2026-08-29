# Chapter Latency Optimization｜Experiment Protocol

## Goal

Reduce normal per-chapter wall-clock without lowering final novel quality. This experiment treats the current five-stage chain as the control and changes one stage variable at a time.

## Frozen source

`books/real-exp-fast-world-20ch-20260828-v1`

## Phase A｜Curator effort isolation

Frozen chapters: 3, 10, 14, 19. Their Director prompt/response, BOOK/Canon/World/Character authority, chapter plan, previous prose, retrieval result, Primary model and Authority Reviser contract remain frozen.

Control: existing `Luna high Curator → Terra high Primary → Luna high Authority Reviser`.
Treatment A1: same exact Curator prompt, Luna medium. No prompt compression yet.

Pass conditions:
- Curator keeps required authority/plan/relationship/world/repetition/payoff information and does not invent facts;
- downstream final draft preserves Chapter Mission, Canon, power/human/world authority, reader release and ending;
- blind reader finds no stable quality regression versus production control;
- wall-clock/tokens improve materially.

## Phase B｜Routine Reviser effort isolation

Use frozen Primary drafts and identical Reviser prompts. Test Luna medium only on chapters classified routine before seeing outputs. High-risk chapters remain Luna high.

Potential high-risk signals are evaluated separately and cannot be inferred from how much the control happened to edit.

## Invalid shortcuts

- deleting Curator or Reviser based only on similarity;
- using output length as a quality score;
- allowing a stronger downstream stage to hide a changed Chapter Mission;
- claiming direct-API latency from ACP measurements.
