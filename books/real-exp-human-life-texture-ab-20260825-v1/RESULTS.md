# Human Life Texture / Appetite A-B-C Experiment — Results

## Scope

This experiment runs while the separate Human GBrain diversification distillation is still in progress. That new distillation is intentionally **not used** here.

The frozen architecture remains:

`World → Power Seed ∥ Human Seed → deterministic Character → Collision`

No World/Power/Collision authority is changed. No Sol, Story Program, Outline, or chapter generation is run.

## Variables

### A — existing Split-Seed Human v5

Reused verbatim from `real-exp-split-power-human-seed-20260825-v1`.

- LIFE_CONTEXT: existing resource / identity / profession-heavy projection.
- Human Prompt: frozen.
- Human GBrain: frozen.
- No new model call.

### B — Life Texture only

The only creative change is adding protagonist-blind `Life Texture / Human Appetite` to LIFE_CONTEXT. Human Prompt and Human GBrain remain byte-for-byte the same outside the inserted Life Texture.

Life Texture adds ordinary non-story facts such as food taste arguments, local music, decorative salt lamps, route songs, clothes, companion animals and children's canal races. It contains no Power and no named Story Opportunities.

### C — Life Texture + Long-form Obsession redefinition

Everything from B is frozen. Only two Human Prompt sentences defining `Core Obsession` change.

Old implicit meaning encouraged: long-form desire expands with status/action space and is therefore often converted into business, assets, standards, control or professional authority.

New meaning: long-form only requires the same private pull to continue changing choices after ordinary people would stop. It does **not** need to become an asset, career, standard, authority or organization.

## Results

### A baseline

Candidates:
- 季衡／把名字钉在纸上 — evidence / ownership / traceability.
- 冯渡／先拥有一条船 — assets / shipping / ownership expansion.
- 魏执／我要让别人按我的判断活下来 — decision authority.
- 林问川／不接受“大概” — diagnostic certainty.

Split authority had already solved Power↔Biography thematic mirroring, but Human distribution remained rational/professional.

### B — Life Texture alone

Candidates:
- 周砚秋／把一袋粮卖成一句话.
- 陆潮／把海味做成自己的价码.
- 沈砺／一张不能被涂改的地图.
- 许成器／把一文钱滚成自己的井.

Life Texture successfully entered the surface material, but the Human inference **re-instrumentalized it**:
- food taste → personal pricing standard;
- cooking → market authority across a trade route;
- maps → official authority over judgment;
- salt-craft life → asset compounding and ownership.

Verdict: **Life Texture is useful soil, but insufficient by itself.**

### C — Life Texture + Core Obsession redefinition

Candidates:
- 梁稷／“第一锅饭不能将就” — cannot let a good thing finish as merely “good enough”; this extends into food, dyeing, wine and banquets.
- 顾泊／“不能让一趟船只剩一句损耗” — still rational; cannot accept an unexplained loss being swallowed by “算了”.
- 石砚／“让所有人同时回头” — chases a vanished sound / echo, sacrifices profitable work and money to reproduce it; clear aesthetic/recognition appetite.
- 陆衡／“名字必须落在那一行” — wants public attribution and recognition even when money is already sufficient; clear vanity/status appetite rather than resource optimization alone.

This is a meaningful distribution improvement without personality menus. It does not force all candidates to become impulsive; one remains rational, which is healthy.

## Text heuristic (supporting signal, not a quality judge)

Using a fixed small keyword set:

- A: instrumental/managerial hits **21**, non-instrumental-life hits **2**.
- B: instrumental **35**, non-instrumental **17** — life material increased, but was heavily professionalized.
- C: instrumental **8**, non-instrumental **21**.

The heuristic only corroborates manual reading; it is not a scoring gate.

## Architecture/schema cleanup validated in parallel

1. **Power Seed anonymity**
   - Production-facing Power authority no longer owns a character name.
   - Frozen v4 examples materialize as `POWER SEED 1｜借万物一锋`, etc.
   - Old temporary Character names are deterministically removed from Power text.

2. **Legendary Power State**
   - `Legendary Trajectory` is narrowed to `Legendary Power State`.
   - Power may describe an aspirational high-tier power experience, but not future identity, organization, rule, mission or story outcome.
   - `Future Legend Image` remains non-Canon audit metadata.

3. **Current private desire is mutable State**
   - `当前私人欲望` initializes `INITIAL CHARACTER STATE.current_desire`.
   - It is removed from persistent Human Core so chapter 200 does not keep receiving a stale opening desire.

4. **Character Hook is audition-only**
   - Generated `人物钩子` is stored as `HUMAN AUDITION METADATA｜NON-CANON`.
   - It is absent from persistent Character Card and cannot silently pre-commit the opening chapters.

5. **Life Texture can be native World output without an extra future LLM call**
   - `project_character_life_context()` now preserves an existing `## Life Texture / Human Appetite` section from protagonist-blind World.
   - Optional separately generated texture was used only to isolate this experiment's variable.

## Current verdict

- Split Power/Human authority: **FROZEN / PASS**.
- Schema cleanup: **PASS**.
- Life Texture as Human soil: **KEEP**, but not sufficient alone.
- Core Obsession long-form redefinition: **KEEP as candidate rule**; it materially reduces automatic career/asset/authority conversion.
- Human distribution overall: **IMPROVED, still not final**. Remaining diversity should be addressed primarily by the ongoing Human GBrain diversification, not by adding more negative Prompt rules.

## Next gate

When the Human GBrain diversification finishes, run one cheap Human-only A/B using this C configuration as the baseline. Do not touch World/Power/Split architecture. Only after Human distribution is satisfactory should one selected `Power Seed × Human Seed` receive a Sol Collision Story Program.
