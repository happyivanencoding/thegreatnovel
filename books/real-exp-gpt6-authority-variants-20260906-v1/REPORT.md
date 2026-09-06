# GPT-6 Authority follow-up: medium reasoning and split Finder→Realizer

Date: 2026-09-06

## Question
After the first Sol-vs-Astra screen showed `Astra-high` had higher Authority recall but worse final prose, test two targeted variants on the exact same three immutable Primary + Frozen Authority cases (`fast / shadow / pace`):

1. **Astra-medium direct Authority Delta** — one reasoning level below the previous Astra-high.
2. **Astra-high Finder → Terra-high Patch Realizer** — Astra may only identify semantic hard issues; Terra may only turn those findings into exact-local patches.

Baselines are the already-generated matched `Sol-high direct` and `Astra-high direct` finals from `real-exp-gpt6-sol-replacement-screen-20260906-v1`. No Primary, Story, Outline, retrieval bundle, or production code was regenerated.

## Bottom line

**Both new variants FAIL as production replacements. Keep `Batch Authority Delta = GPT-5.6 Sol high` for now.**

### 1. Astra-medium direct — FAIL

Performance is excellent, but quality is not equivalent.

- wall: **305.8s aggregate** vs Astra-high 599.9s (**~49% faster**) and Sol-high 524.9s (**~41.7% faster**).
- patches: **40 total** (10 / 19 / 11), close to Astra-high 44 and far above Sol-high 19.
- Authority: medium never beats Astra-high. `fast: high > medium > Sol`; `shadow: high > medium > Finder→Terra > Sol`; `pace: high = medium > Sol` under the new stricter audit.
- Reader: **medium loses to both Sol and Astra-high on all 3 samples**. Rankings are:
  - fast: `Sol > Astra-high > Astra-medium`
  - shadow: `Sol > Astra-high > Astra-medium > Finder→Terra`
  - pace: `Sol > Astra-high > Astra-medium`
- concrete failure: fast medium leaked the Authority prompt's trailing JSON output instructions into a `NEW` patch, so the final chapter literally ended with `只输出一个 JSON object...`. This is a real realization/output-contract failure, not a judge preference.

Decision: **do not downgrade Astra Authority reasoning to medium.** The speed win is real, but medium is not quality-equivalent.

### 2. Astra-high Finder → Terra-high Realizer — FAIL

The decomposition did not produce the hoped-for `strong semantic auditor + natural prose hand` synergy.

Generation:

| case | Finder findings | Finder upstream | Terra patches | Terra upstream | Finder wall | Terra wall | sequential wall |
|---|---:|---:|---:|---:|---:|---:|---:|
| fast | 8 | 1 | 9 | 1 | 255.6s | 53.6s | 309.3s |
| shadow | 10 | 0 | 13 | 0 | 164.2s | 68.8s | 233.0s |
| pace | 6 | 2 | 8 | 2 | 166.6s | 47.8s | 214.4s |

Aggregate sequential wall is **756.6s**, slower than both Astra-high direct (599.9s) and Sol-high direct (524.9s). The two calls also repeat the full Authority/Primary context and consume roughly twice the aggregate ACP tokens of one-pass Astra-high.

The architecture also became too eager to escalate to upstream:

- fast Finder conflict (remote merge/reunion) → independent conflict auditor: **FALSE_POSITIVE**. Existing Authority already allows both real bodies to move and locally reunite; a local patch can make the physical reunion explicit without inventing a new mechanism.
- pace Finder emitted two conflicts:
  - midterm `9–18` block vs per-chapter `4–5` White-Horn scheduling → **LEGITIMATE_UPSTREAM**.
  - chapter-5 package / injury / identity chain → **FALSE_POSITIVE**; Persistent Canon already supplies the necessary event chain and chapter 6 owns the identity reveal.

So conflict precision in this screen is only **1 legitimate out of 3 reported conflicts**. The Finder did discover a real upstream schedule conflict missed by direct passes, which is valuable, but it blocked too aggressively.

On the only case with a legal two-stage FINAL (`shadow`):

- Authority ranking: `Astra-high > Astra-medium > Finder→Terra > Sol`.
- Reader ranking: `Sol > Astra-high > Astra-medium > Finder→Terra`.

Terra realization therefore **did not repair Astra's prose-preservation problem; it made Reader quality worse on this matched sample**. The patch output had more visible seams / deletions and did not preserve the high model's best Authority closure.

Decision: **do not add a permanent Finder→Realizer stage.** This would increase topology, wall, token use, false upstream stops, and still fail Reader preservation.

## What the experiment actually teaches

The first screen's diagnosis holds: Astra-high's useful advantage is **semantic Authority recall**, but the unsolved problem is not simply `reasoning too high` or `same model should not write patches`.

- Lowering reasoning mostly buys speed and loses realization stability / recall quality.
- Splitting semantic detection from patch wording does not automatically make patches more natural; the realizer still needs to understand when a fact should be deleted, neutralized, minimally restored, or left as upstream.
- A generic second LLM stage is not justified by these samples.
- Astra Finder's ability to notice the `pace` midterm-vs-Future-10 schedule conflict is real and potentially useful as **experimental diagnosis**, but its current false-upstream rate makes it unsuitable as a production gate.

## Production decision

No production route changes.

- Story Program: GPT-5.6 Sol high
- Story Refresh: GPT-5.6 Sol high
- Batch Authority Delta: **GPT-5.6 Sol high**
- Astra-high Authority remains an experimental high-recall candidate only.

## ACP sessions

### Astra-medium direct
- fast: `01a07887-00b4-7641-9233-7c7131540351`
- shadow: `01a07888-5f17-7112-81b6-daa39b54f244`
- pace: `01a0788a-e71e-7d91-9f5c-29656378c90c`

### Astra-high Finder
- fast: `01a07887-00b4-70a2-bf62-74bcbe8f3a6f`
- shadow: `01a0788a-1523-7bf0-a52c-5b18c0ea06c5`
- pace: `01a0788c-7f20-71c3-abd9-294f575ecebc`

### Terra-high Realizer
- fast: `01a0788f-09f6-7361-9b40-5bfaa952317d`
- shadow: `01a0788f-09f2-7652-a671-a74551a2f0da`
- pace: `01a0788f-db78-7ba1-a9b6-4a573c9ce75f`

### Independent judge sessions
- fast Reader: `01a07891-fa60-7b33-90c2-4da828972a2a`
- fast Authority: `01a07891-facd-7851-8d8e-9f311c5c07f8`
- fast Conflict: `01a07895-5e1e-7851-b6c9-15f9344d4e0d`
- shadow Authority: `01a07895-933c-7b70-a5b8-f510bd0d86a6`
- shadow Reader: `01a07898-4fbf-73d0-8c3c-4bef757a3564`
- pace Reader: `01a0789b-ad5e-71c1-a31a-be895f4989e7`
- pace Authority: `01a0789b-7ec3-74a2-8b02-e329cd5227ce`
- pace Conflict: `01a0789d-88f1-7463-8b4e-6ece82a3926d`

## What this did not solve

This is a matched follow-up screen on the same three Authority cases used in the prior GPT-6 screen. It is sufficient to reject these two concrete variants, but it does **not** prove every possible detector/realizer decomposition will fail. In particular it did not test a newly designed deterministic patch compiler or every possible second-model choice; those would be separate hypotheses and should not be added without a concrete reason.
