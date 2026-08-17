# Deterministic audit

## Scope

- Actual close: 6 Canon chapters, stopped by explicit user instruction after Chapter 6.
- Not claimed: Chapters 7–10, formal Batch Continuation, or a mature long-form quality conclusion.
- Approval source: browser Draft Review only.

## State checks

- Chapter ordinals: exactly 1, 2, 3, 4, 5, 6.
- Canon commits: 6.
- Event ranges: 1–5, 6–11, 12–17, 18–23, 24–29, 30–35.
- Snapshot through-event sequence: 5, 11, 17, 23, 29, 35.
- Content hashes are distinct across all six chapters.
- Validator reports: 60 total, 60 PASS, 0 FAIL.
- Semantic publication review: 6/6 REVIEWED; findings 0.
- Browser UI after close: 正文 6 and 6 见证者名单上的新名字 正史; no dialog/modal observed.
- No CLI approve and no direct SQLite Canon mutation were used.

## Retained non-success paths

The audit deliberately retains failed/retried artifacts rather than deleting them:

- Chapter 1 initial failed draft: draft_f8dad90c3947326a539a1b02
- Chapter 2 stale direct handoff: handoff_02d0c91f21869a54e69e6589
- Chapter 3 pre-normalization/retry drafts: draft_ecb3af8872104bb1502c62e6, draft_438ae7c91101b1f8f6b9c64e
- Browser clicks sometimes needed a second force click to expose a newly created READY handoff; this is recorded in browser_workflow_audit.md and does not alter Canon.

## Quality interpretation

The deterministic layer is green for the six committed chapters. That only proves state/evidence/approval integrity. It does not prove the prose is mature, non-repetitive, or ready for a ten-chapter claim.

## Repository verification

- Full pytest under the correct project runtime: 573 passed, 1 failed.
- The only failure reads the pre-existing deleted root AGENTS.md; it was not restored.
- Full-source strict mypy: 203 files passed; compileall passed; touched-file Ruff rules passed.
- Final targeted quality and Original initialization tests: 32 passed.
