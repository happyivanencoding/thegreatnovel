# TGN — TheGreatNovel

TGN is an experimental long-form AI novel authoring system focused on structured planning, controllable chapter execution, continuity, and reusable story-craft knowledge.

> Status: active development. The architecture and prompts are still evolving through real generation experiments.

## What TGN Does

TGN separates long-form fiction generation into stages with different responsibilities instead of asking one model to plan and write everything at once:

```text
Author Direction
→ Fantasy Seed
→ World Vision
→ Story Program
→ Outline
→ Director
→ Context Curator
→ Primary Writer
→ State Extraction
```

The goal is to keep upstream story decisions explicit while letting downstream chapter generation focus on execution rather than silently redesigning the book.

## Core Design Principles

- **Fantasy First** — preserve the reader-facing fantasy and protagonist agency before optimizing systems or procedures.
- **Few Deep Rules > Many Hard Gates** — prefer clear semantic responsibilities over reviewer and validator proliferation.
- **Supporting Logic Must Not Automatically Become Story Engine** — plausibility, mechanisms, governance, verification, and operations should support the story unless the book explicitly chooses them as its main experience.
- **Story-bearing Texture > Decorative Density** — prose should be concrete and vivid without relying on adjective, metaphor, or sensory-list inflation.
- **Planning and prose are separate responsibilities** — Director decides what happens; Writer realizes it as fiction.
- **Memory stays thin and factual** — State Extraction records what actually happened instead of inventing future implications.

## GBrain

TGN can optionally use a local GBrain knowledge base as curated inspiration for world design, long-form story programs, outlines, and distilled Scene Skills.

GBrain is treated as **optional inspiration**, not Canon or creative authority. Raw reference material is not intended to flow directly into the Primary Writer.

The repository does not require or include private/local source corpora.

## Project Structure

```text
src/story_mvp/   Application, prompts, runtime and storage logic
books/           Book workspaces and generation experiments
docs/            Architecture, methodology and subsystem documentation
tests/           Regression and runtime tests
```

Start with:

- [`docs/PIPELINE_METHODOLOGY_AND_VALUES.md`](docs/PIPELINE_METHODOLOGY_AND_VALUES.md) — system methodology, stage responsibilities and anti-goals
- [`docs/MVP_PRODUCT_DIRECTION.md`](docs/MVP_PRODUCT_DIRECTION.md) — product direction and creative-authority boundaries
- [`docs/GBRAIN_STORY_CRAFT_V3.md`](docs/GBRAIN_STORY_CRAFT_V3.md) — GBrain integration and story-craft knowledge
- [`docs/NOVEL_PROSE_REALIZATION.md`](docs/NOVEL_PROSE_REALIZATION.md) — prose realization and Reader-First principles

## Quick Start

Requires Python 3.11+.

```bash
python -m venv .venv
```

Activate the virtual environment, then install the project:

```bash
pip install -e ".[test]"
```

Run the local application:

```bash
story-mvp
```

Then open:

```text
http://127.0.0.1:8000
```

Run tests with:

```bash
pytest
```

## Third-party Material

The TGN license applies only to material that the project has the right to license. Third-party libraries, reference works, datasets, model services, and copyrighted source texts remain subject to their own licenses and terms. No rights to third-party copyrighted novels or private corpora are granted by this repository.

## License

TGN Engine is licensed under the **GNU Affero General Public License v3.0 only** (`AGPL-3.0-only`).

See [`LICENSE`](LICENSE) for the full license text.
