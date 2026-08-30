# Exact-Input Phase Receipt｜Validation Protocol

> Date: 2026-08-30
> Scope: deterministic incremental stale recovery; no Story/Authority model change.

## Hypothesis

TGN may conservatively stale a future node after an upstream Authority artifact revision even when the node's final bounded Prompt is byte-for-byte unchanged. If a completed/adopted Response is provably bound to that exact Prompt and its saved body is unchanged, re-running the model is redundant.

## Acceptance conditions

1. Find a project-reachable substantive upstream edit that stales a future node while rebuilt Prompt remains exact-identical.
2. Receipt must bind exact UTF-8 Prompt SHA-256 and exact saved Response SHA-256.
3. Exact hit restores only `completed/adopted`; no model call occurs and Response bytes remain identical.
4. Prompt mismatch, Response body drift, missing legacy receipt, failed response, or explicit retry must rerun normally.
5. Existing dependency stale graph runs before receipt revalidation; receipt cannot declare semantic equivalence.
6. Web OpenAI/Codex dispatch must actually stop before executor invocation when a receipt is reused.
7. Existing Run Ledger retry, Outcome Repair, final_source and Workflow tests must remain green.
8. Report benefit only as incremental stale-recovery savings, never as first-pass chapter latency.

## No quality blind required

A receipt hit returns the exact previously saved Response bytes for the exact previously consumed Prompt bytes. There is no Treatment prose to compare against Control prose; Reader/Authority A/B would compare a document with itself. Quality risk is therefore tested through identity/fail-closed invariants, not another LLM judge.
