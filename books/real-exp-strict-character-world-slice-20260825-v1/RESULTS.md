# Strict Character Architecture Experiment — Results

## Scope

This experiment reuses the same protagonist-blind `澜生界` and stops at Character Card. No Story Program, Outline, chapter generation, or LLM judge is used after the user requested quota-efficient upstream testing.

The experiment progressively isolates three different authorities:

- `STORY_OPPORTUNITY_LAYER`: named active events, named NPCs, named places, unresolved named mysteries. Hidden from Character generation.
- `POWER_BASELINE`: supernatural laws, normal/rareness distribution, acquisition/承载/use constraints. Authority for Core Fantasy / Legal Exception.
- `LIFE_CONTEXT`: ordinary life, social reality, generic value structures, knowledge boundary. Authority for upbringing, desire, personality, and relationships.

Core architecture hypothesis:

> Character is world-conditioned, story-independent.
>
> Core Fantasy should be conditioned primarily on the world's power normal/rareness distribution; upbringing should shape how the character understands and uses the anomaly, not determine the anomaly by profession.

## A — Previous opportunity-leaking context

The previous context-isolated experiment still exposed active world events, named places, named mysteries and opportunity structures. This produced obvious lock-key coupling, e.g. the world contained a still-running old courier network and a Character candidate was generated with exactly the old identity token needed to access it.

Verdict: **FAIL as the final Character interface**. It proved that independent LLM context is not enough if Story Opportunities remain visible.

## B — Strict World Slice v1

Named hook leakage dropped to zero, but the prompt over-constrained upbringing toward ordinary concrete livelihoods. Four candidates converged toward miner / beast handler / traveling logistics / salt-transport type social professions, and their anomalies became adjacent to job expertise, diagnostic logic or institutional cleverness.

Verdict: **FAIL / useful negative evidence**. Removing Story Opportunities was correct, but `World Reality` was still too undifferentiated: occupation and power anomaly competed inside one context.

## D — Power-System-First v3

The interface was split into:

- `POWER_BASELINE` with no social occupation/identity section;
- `LIFE_CONTEXT` with no power-system section.

Character generation order became Power Normal → Legal Exception → Core Fantasy first, then upbringing → adaptation → behavior.

Four candidates moved decisively back to the supernatural power layer:

- dual stable incompatible carrying structures;
- storing the uncompleted remainder of a spell;
- distributing one power process across connected external carriers;
- preserving the mismatch trace left by a failed/received technique.

Named Story Hook leakage remained zero and the earlier miner/repair/contract/route-optimization collapse largely disappeared.

Verdict: **PASS on authority separation**, but the prompt did not explicitly require compatibility with long-form male progression, so it did not prove that the anomaly could carry a protagonist from low tier to high tier.

## E — Power-System-First + Growth Compatibility v4

The user correctly restored a core product invariant: this is a mature Chinese male-oriented **growth** novel. Short troughs are allowed, but the protagonist must genuinely become stronger over time.

Character Card therefore adds only one lightweight power-growth contract, not a Story Program:

1. `正常修炼轴`: ordinary cultivation must genuinely increase body / spirit / energy / technique capability;
2. `异常掌握轴`: the Legal Exception expands in capacity, precision, recombination, applicable targets, duration, supported level, or action freedom;
3. `永久边界`: at least one high-level limit remains, so world rules stay larger than the cheat.

The four frozen v4 candidates are:

1. `祁砚／借万物一锋` — temporarily connects multiple real external carriers into one improvised power structure. Growth comes from stronger normal cultivation plus wider/more precise recombination; incompatible forces remain dangerous.
2. `陆未／留着未完` — preserves an already-started but unfinished technique and completes it later/in another carrier. Growth expands number, ordering and recombination of incomplete techniques; unfinished techniques continue to consume attention/energy and cannot exceed his carrying ceiling.
3. `温折／受力成路` — after truly receiving a force, preserves its directional relationship and later redirects analogous force. Growth expands the number and kinds of force relationships; first contact with an overwhelmingly strong attack can still kill him.
4. `沈回／两处同身` — maintains a second spatial anchor tied to the same body. Growth expands sensory/action transfer, distance and anchors, while never becoming two complete bodies with two full combat outputs.

All four remain compatible with the world's ordinary cultivation ladder instead of replacing cultivation.

## Automated checks

- Named Story Opportunity leakage in strict Character contexts: **0** for the monitored named hooks.
- v4 generated Character named-hook hits: **0**.
- `POWER_BASELINE` contains the power system and excludes the social-reality section.
- `LIFE_CONTEXT` contains upbringing/social reality and excludes the power-system section.
- Projection unit tests cover the above boundaries.

## Current judgement

**v4 is the first version in this experiment that is worth human audit before spending Sol.**

It does not prove the final architecture yet. Remaining human questions are:

- Are the four Core Fantasies commercially desirable enough, or merely mechanically clever?
- Do the characters remain memorable when the ability description is mentally removed?
- Are Life Context and Core Fantasy chemically related without becoming synonymous?
- Is `Growth Compatibility` enough to support a male progression novel without prematurely turning Character Card into a Story Program?
- Does the eventual Collision model preserve world/character mismatch rather than retroactively rationalizing the world around the protagonist?

Therefore the experiment intentionally stops here. The next expensive step should be **one** Collision Story Program only after human review selects/fixes a Character Card.
