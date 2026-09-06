# GPT-6 Astra replacing GPT-5.6 Sol — controlled screen

Date: 2026-09-06

## Scope
Only production stages currently routed to GPT-5.6 Sol were tested at matched `high` reasoning:
- Story Program
- Story Refresh
- Batch Authority Delta

All other model routes stayed fixed. Each A/B used the exact same prompt. GPT-6 was `gpt-6-astra[high]`; control was `gpt-5.6-sol[high]`.

## Bottom line
**Do not globally replace GPT-5.6 Sol with GPT-6 Astra.**

### Story Program / Story Refresh
Blind planning judges preferred **Sol 4/4**.

Observed Astra regression pattern:
- more likely to turn a rich collision into a programmatic growth / training / business / responsibility chain;
- more likely to let Tier Pace consume Plot Engine;
- in some samples, more likely to make the protagonist responsible / steady in a way that flattens Frozen Human differences.

Astra was faster, especially in Story Refresh, but the quality regression is decisive.

### Batch Authority Delta
Authority blind auditors preferred **Astra 3/3**.
- fast: Astra PARTIAL, Sol FAIL
- shadow: Astra PASS, Sol FAIL
- pace: Astra PARTIAL, Sol PARTIAL, Astra cleaner

Astra produced 44 patches vs Sol 19 and found multiple real hard issues missed by Sol. All Astra deltas parsed and applied under the current exact-OLD production contract; no false positive was identified by the blind Authority auditors.

However, final-prose Reader blind results were **Astra 1/3, Sol 2/3**. Astra's extra Authority repairs sometimes created visible patch / explanation texture, especially when removing unauthorized history or restoring omitted facts. Therefore Astra Authority Delta is **directionally promising but not production-freeze ready under the current prompt**.

## Performance
| Stage | Sol wall (s) | Astra wall (s) | Result |
|---|---:|---:|---|
| Story Program (2) | 784.3 | 670.6 | Astra ~14.5% faster, but loses quality 2/2 |
| Story Refresh (2) | 810.7 | 416.3 | Astra ~48.6% faster, but loses quality 2/2 |
| Authority Delta (3) | 524.9 | 599.9 | Astra ~14.3% slower aggregate; quality 3/3 better |

Astra also used substantially fewer total/reasoning tokens in the planning samples. Speed/tokens did not compensate for planning-quality loss.

## Production decision
- **Story Program: keep GPT-5.6 Sol high.**
- **Story Refresh: keep GPT-5.6 Sol high.**
- **Batch Authority Delta: keep GPT-5.6 Sol high for now.** GPT-6 Astra high is the next targeted candidate, but requires a narrower realization A/B that preserves its higher Authority recall without the 2/3 Reader regression.
- No production model route was changed by this experiment.

## ACP prerequisite
Initial GPT-6 probe failed because local `@agentclientprotocol/codex-acp` 1.6.2 did not expose `gpt-6-astra`. Updating it to **1.10.0** made `gpt-6-astra` available and the real probe succeeded.

## Generation ACP sessions
### Story Program
- cultivation Astra: `01a0781a-0aa2-7b73-83ae-49fb18b0b9b3`
- cultivation Sol: `01a0781a-0a35-72b3-af32-035c440bbef2`
- ocean Astra: `01a07821-143e-7a82-8c82-31a5a9ee481f`
- ocean Sol: `01a0781f-0edb-7273-9f64-b6ca2705e481`

### Story Refresh
- open Astra: `01a07826-4b5e-7903-a7f5-2c0feab42c14`
- open Sol: `01a07823-fda4-7aa3-a550-2d1a55b36fd5`
- cycle2 Astra: `01a07829-3b2e-7b12-8e9a-d4d21910ae68`
- cycle2 Sol: `01a07828-7821-7d23-a209-d60e666bdfea`

### Batch Authority Delta
- fast Astra: `01a0782f-4782-7282-b8d8-695c097df422`
- fast Sol: `01a0782d-6983-7cd3-8e08-129353047f22`
- shadow Astra: `01a07831-936e-7a12-a339-cd5d53755de9`
- shadow Sol: `01a0782f-998e-7140-88af-fafa00c3c9d4`
- pace Astra: `01a07835-bf5d-74e0-9d65-ac01b9486812`
- pace Sol: `01a07831-f3bd-7903-a618-ad6071e8fe32`

## Blind judge ACP sessions
- story_ocean: `01a0783a-7e38-7380-a402-c2c8ce871fab`
- story_cultivation: `01a0783a-7e3e-7de2-8c1a-7feb7cf3aaf7`
- refresh_open: `01a0783c-f442-7480-86e4-a6876248f4f9`
- refresh_cycle2: `01a0783e-9ea2-7660-a8a2-8d78d4c3043b`
- authority_fast: `01a0783f-2002-7e20-8fa9-c9bc94cc6591`
- authority_shadow: `01a07840-8400-7ac2-9256-ab7efc8990ba`
- authority_pace: `01a07842-f1d4-7f30-a107-26b5f891acc2`

Final Reader judges used Terra-high; the direct runner did not expose their session IDs in its metadata, but all three completed successfully and the raw ACP outputs are stored under `blind_reader_authority/*/judge_acp.json`.

## What this did not solve
This experiment does not establish that Astra can never be better for planning, only that **direct substitution under current production prompts is worse on the tested held-out samples**. It also does not freeze Astra Authority Delta: its higher closure recall is real, but prose-preservation must be improved and re-tested before adoption.
