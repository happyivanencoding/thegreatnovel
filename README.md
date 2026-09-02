# TGN — TheGreatNovel

[简体中文](README.zh-CN.md) | English

**An open-source long-horizon fiction engine for AI-native novels.**

Most AI writing tools optimize the next paragraph. **TGN is built to optimize the book.**

TGN turns an author's intent into persistent story authority, then lets models plan, write, revise, and expand inside that authority. The goal is long-form fiction where characters keep their identity, worlds stay larger than the protagonist, rewards and relationships compound, mysteries can remain genuinely unresolved, and decisions made dozens of chapters earlier still change what can happen next.

> TGN is in active research and development. It is built through end-to-end novel generation, failure analysis, and repeated production experiments — not as a collection of prompts.

## The Problem

LLMs can write impressive scenes while still failing at novels.

Over long horizons, the common failure is not grammar. It is **structural drift**: the model quietly changes the rules, flattens a character into recent behavior, forgets why an old relationship matters, turns worldbuilding into scenery, or optimizes every new arc around the protagonist until the world stops feeling alive.

TGN starts from a different thesis:

> **Long-form AI fiction needs an authority architecture, not a longer prompt.**

## How TGN Thinks About a Novel

```text
Author Intent
    ↓
Optional Premise Search
    ↓
World Authority + Character Authority
    ↓
Story Program
    ↓
Horizon Plan
    ↓
4–6 Chapter Batch Runtime
    ↓
Authority-Preserving Revision
    ↓
Canon + Story State
    ↺
World Expansion / Story Refresh
```

The important boundary is simple: upstream stages are allowed to decide the book; downstream stages are expected to realize those decisions without silently redesigning them.

## What Is Different

### Authority before prose

World rules, character identity, long-term promises, current canon, and approved story decisions are represented separately from prose. A chapter writer receives bounded authority instead of being asked to remember the entire project and improvise safely.

### A world that does not exist only for the protagonist

TGN separates world construction from protagonist optimization before they collide in the Story Program. The world can contain actors, opportunities, conflicts, and futures that continue to exist even when the protagonist chooses another route.

### Longitudinal compounding

A long novel should not reset every time the map changes. TGN carries forward consequences across horizons: power, relationships, identity, enemies, assets, knowledge, social position, and unresolved questions can all be recontextualized by later events.

### Progressive canon instead of premature answers

Not every mystery needs to be solved by the planner. TGN can preserve an explicit unknown, canonize only the smallest layer required for the next story, and reveal it later through reader-facing events.

### Batch prose with authority recovery

Chapters are generated in short batches so the writer can sustain narrative continuity across several chapters. A separate authority pass repairs local factual drift without treating revision as permission to rewrite the story.

### Retrieval as inspiration, not truth

TGN can connect to an external story-craft knowledge base, but retrieved material is kept outside Canon. References can expand the search space; they do not get to become facts merely because retrieval found them.

## What Ships in This Repository

- A local FastAPI author workspace
- Structured premise, world, character, story-program, and outline workflows
- Persistent Canon and story-state handling
- Long-form world expansion and story refresh
- Batch chapter generation and authority-preserving revision
- Optional external story-craft retrieval integration
- Regression tests for runtime and authority behavior

The public `main` branch is intentionally a clean production surface. Internal research notes, private corpora, experiment provenance, and project handoff material are not part of the release.

## Quick Start

Requires Python 3.11+.

```bash
python -m venv .venv
```

Activate the environment, then install TGN:

```bash
pip install -e ".[test]"
```

Run the local author workspace:

```bash
story-mvp
```

Open:

```text
http://127.0.0.1:8000
```

Run the test suite:

```bash
pytest
```

## Repository Layout

```text
src/story_mvp/   Engine, runtime, prompts, storage, and author workspace
books/           Public sample/workspace artifacts already included in releases
tests/           Runtime and regression tests
```

## Direction

TGN is ultimately an attempt to make **book-scale generative systems**: systems that can preserve creative identity and causal memory while still allowing surprise, expansion, and genuine author choice over hundreds of chapters.

The target is not a perfectly controlled text generator. It is a system in which **freedom at the sentence level can coexist with continuity at the scale of a novel**.

## Third-party Material

The TGN license applies only to material that the project has the right to license. Third-party libraries, reference works, datasets, model services, and copyrighted source texts remain subject to their own licenses and terms. No rights to third-party copyrighted novels or private corpora are granted by this repository.

## License

TGN Engine is licensed under the **GNU Affero General Public License v3.0 only** (`AGPL-3.0-only`).

See [`LICENSE`](LICENSE) for the full license text.
