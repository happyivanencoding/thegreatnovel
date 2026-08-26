# Split Character Authority — Frozen Production Architecture

Status: **FROZEN / production**

This document defines the upstream creative authority used by new TGN books. It is intentionally small. Do not add extra agents, reviewers, scorers, or approval gates merely to enforce these principles.

## 1. Production chain

```text
Author Direction
      |
      v
WORLD VISION
protagonist-blind
      |
      +-----------------------------+
      |                             |
      v                             v
POWER_BASELINE                 LIFE_CONTEXT
      |                             |
      v                             v
POWER SEED                    HUMAN SEED
fresh context                 fresh context
GBrain power craft            GBrain human craft
      |                             |
      +-------------+---------------+
                    v
             CHARACTER.md
        deterministic composition
                    |
                    v
              STORY PROGRAM
          first full collision
                    |
                    v
                 OUTLINE
```

There is no Fantasy Seed production stage.

Power Seed and Human Seed are two independent creative authorities, but they are **not two approval gates**. The author approves Character once; that freezes both selected seeds and deterministically materializes `CHARACTER.md`.

Different model families are optional. The essential decorrelation mechanism is **fresh context + authority isolation**. World and Human may both use Luna high, for example, as long as Human does not inherit hidden Story Opportunity context.

## 2. World Vision

World Vision creates a world that remains worth writing about even if the eventual protagonist is replaced.

It owns:
- ordinary life and routes of social ascent;
- power system and observable normal / rarity baselines;
- social reality and identity consequences;
- concrete things people value;
- independent people and events already moving;
- places, wonders, dangers, and unknowns;
- world knowledge boundaries.

It does **not** own protagonist desire, protagonist biography, protagonist ability, protagonist destiny, first payoff, or final mission.

World Reality and Story Opportunities may coexist in the full World Canon, but downstream visibility is different.

## 3. Power Seed authority

Power Seed sees only the deterministic `POWER_BASELINE`, never the full Story Opportunity layer and never Human biography.

Generation order:

`World Power Normal -> Legal Exception -> Core Fantasy -> Growth Compatibility`

Power Seed owns:
- the relevant world normal / rarity baseline;
- the Legal Exception;
- Core Fantasy and why a reader would want it;
- normal cultivation axis;
- exception mastery axis;
- High-Tier Mutation;
- permanent boundary;
- Legendary Power State.

`Future Legend Image` is audit-only and non-Canon.

The protagonist is a male-oriented progression protagonist: temporary lows are allowed, but normal cultivation must genuinely strengthen the protagonist and the exception must remain compatible with long-form upward progression. The exception must not merely replace cultivation with a clever occupational technique.

Power Seed is anonymous. Name and personal identity never belong to Power authority.

## 4. Human Seed authority

Human Seed sees only deterministic `LIFE_CONTEXT` plus Human GBrain craft. It is power-blind and Story-Opportunity-blind.

Human generation follows:

`Lived Facts -> Competing Motives -> Stable Choice Bias under conflict`

The Human Seed is a person snapshot, not a psychological proof. Biography provides world-conditioned life facts; it does not need to justify every later trait. Do not decide one elegant personality thesis and reverse-engineer childhood events that each prove it.

It owns:
- initial social position and upbringing;
- concrete lived facts;
- several persistent private drives that may compete, reorder, or be changed by relationships;
- Behavior Signature;
- relationship origins;
- relatively stable identity facts.

Long-form viability does **not** require one Core Obsession or a single life philosophy. A private drive is long-form compatible when it can continue to alter choices in larger circumstances; several such drives may conflict. They do not need to turn into an accumulating business, asset, standard, decision right, authority position, or organization.

Behavior Signature means **Stable Choice Bias + Variable Realization**: readers can learn what this person tends to protect, reject, overvalue, or pay for, while the actual tactic remains generated from current information, risk, power limits, and relationships. A specific relationship matters only when that specific person can change a real choice; equivalent usefulness is not enough.

### Mutable and non-Canon boundaries

`current private desire` initializes `CHARACTER_INITIAL_STATE.md`; it is not frozen in Human Core.

`Character Hook` belongs to `CHARACTER_AUDITION.md`; it proves the candidate can be memorable without a power, but it does not bind the opening chapters and is not Canon.

`CHARACTER_INITIAL_STATE.md` is T0 only. Once chapters begin, the existing BOOK Canon + State Delta pipeline remains the sole running-state authority. Do not create a second long-running character-state system.

## 5. Character composition

`CHARACTER.md` is a deterministic merge of frozen Power Core and Human Core.

There is **no Character Composer LLM**.

Do not reconcile the two authorities by inventing biography such as:
- two homes therefore two-position power;
- unfinished childhood therefore unfinished-spell power;
- repair profession therefore repair superpower.

Mismatch is creative material, not an error.

Editing either selected seed reopens Character authority and stales downstream Story/Outline, but does not rewrite World.

## 6. Collision authority

Story Program is the first stage allowed to see:
- Full World;
- Full Character;
- Character T0 state;
- Story GBrain / References.

Core contract: **Do Not Reconcile Away the Collision.**

World is fact. Character is fact. Story Program discovers what happens when they meet. It may create incidents, relationships, counterplay, consequences, phase engines, and long-form progression, but cannot rewrite either upstream authority to make them thematically neat.

Authority and scheduling are different. Power Seed owns the growth grammar—normal progression, exception mastery, high-tier mutation, permanent boundary, legendary state. Story Program owns **when and through what story causality those approved possibilities become real**. It must preserve a longitudinal male-progression invariant and periodic Core Fantasy payoff without forcing every large stage to contain a new upgrade or acquisition.

Current large-stage compilation is intentionally light: why now, who wants what, protagonist choice/action, primary reading satisfaction, `Stage Delta`, and why the next stage follows. `Stage Delta` writes only dimensions that actually changed (for example Power/Capability, Possession, Relationship, Identity/Access, Knowledge, Enemy State, World State). No dimension is mandatory per stage.

High-Value Acquisition and Compounding remain longitudinal craft principles, not stage taxes. When an acquisition really occurs it should be desirable, actually possessed/used, and continue to affect later story; prior gains should not vanish after one arc. Neither principle requires a fixed per-stage field.

Counterplay is learned after collision; enemies are not born merely as a mechanical counter to the protagonist.

## 7. GBrain visibility

GBrain retrieval obeys exactly the same authority boundaries as generation prompts.

- World lane: world craft.
- Power lane: `POWER_BASELINE` only; no named Story Opportunities.
- Human lane: `LIFE_CONTEXT` only; no power and no named Story Opportunities.
- Story lane: Full World + Character for the first time.

Power and Human each remain bounded to a small inspiration bundle. Human GBrain should diversify human appetite, behavior, and relationship gravity rather than classify personalities or prescribe a menu of character types.

## 8. Life texture belongs downstream

`Life Texture / Human Appetite` is **not** an upstream Human Seed field.

Ordinary-life texture is a Writer/Curator-side permission. When the current scene naturally supports it, Curator or a single Writer may project **0–1** small life detail from already approved World Vision facts.

It must not:
- establish a new world rule;
- create a new character motive;
- create a new story obligation;
- become long-running Canon merely because it was used as texture;
- appear mechanically in every chapter.

Texture is decoration carried by story, not the soil that decides who the protagonist must be.

## 9. Approval and stale graph

Production approvals remain compact:

1. approve World Vision;
2. approve Character once (Power + Human together);
3. approve Story Program.

Dependency direction:

`World -> Power/Human -> Character -> Story Program -> BOOK/Outline -> chapters`

A downstream edit never rewrites an upstream authority. A World edit stales Power/Human and everything below. A Power or Human edit stales Character and everything below, but does not stale World.

## 10. What is deliberately not added

Do not add by default:
- Character Composer;
- personality scorer;
- MBTI / trait checklist;
- mandatory weirdness;
- mandatory trauma;
- mandatory anti-world protagonist;
- separate per-character LLM state calls each chapter;
- Life Texture agent;
- new hard gates for Human diversity.

The architecture solves rationalization through **information boundaries**, not through growing negative-prompt walls.
## Human GBrain lane budget

Human Seed GBrain retrieval uses three independent lanes, not one shared Top-N pool:

- `appetite`: what the person privately wants or values even without direct progression payoff;
- `behavior`: stable choice bias / character hook without turning it into a personality taxonomy;
- `relationship`: concrete people whose independent desires can change the person's choices.

Each lane contributes **at most one ACTIVE craft card** and Human Seed still receives at most three cards total. A lane may remain empty; REFERENCE_ONLY / HOLD material never fills a slot merely to reach three. The same card cannot occupy two lanes. New Human Craft should declare `human_lane: appetite|behavior|relationship` in frontmatter; older cards are classified from narrow craft metadata only.

The three lanes are retrieval budgets, **not three required personality dimensions or Hard Gates**.
