# Local Authority Repair L2 High-Local｜Frozen Derivation Protocol

> Derivation source: held-out novel 2 from the prior Reviser-noop experiment. This protocol is frozen before any L1 model output is generated.

## Goal

Test a materially different route from the rejected whole-chapter Patch-only Reviser:

```text
Frozen Authority clauses
    ↓ deterministic lexical locality selection
small read-only windows + <=5 editable paragraph IDs
    ↓ Luna high local repair
single-paragraph replacements only
    ↓ code apply; every unselected paragraph remains byte-identical
```

## Active lanes

1. `state`: exact Frozen Mission `直接结果 + 状态变化`.
2. `reader`: exact scheduled `READER RELEASE`; absent/none => lane disabled.
3. `audit`: exact `Curator Audit` boundary. Curator remains diagnostic/locality guidance; it does not create Hard Authority.

No global Permanent-Boundary Watch and no generic full Authority checklist are appended.

## Locality selector

- Split Primary into existing blank-line paragraphs.
- Extract protagonist display name from Frozen Human header and remove only that exact surface from lexical scoring to prevent name-frequency dominance.
- Normalize punctuation/whitespace only; no Chinese semantic parser, synonym lexicon, classifier or embedding.
- Use binary Chinese character bigram cosine overlap between each lane clause and each paragraph.
- Ignore paragraphs with <8 normalized characters after protagonist removal.
- Per-lane centers: `reader=3`, `state=2`, `audit=2`; minimum score `0.04`.
- Merge duplicate centers, order by lane priority `reader > audit > state`, then score; cap editable centers at 5.
- Provide ±1 paragraph context as read-only; only center paragraph IDs may be replaced.
- If no center survives, L2 is unsupported and the real route would fallback high.

## Medium output contract

- Input contains only active Authority lane text plus selected local windows; it never sees the full chapter.
- Output JSON only: `{"patches":[{"paragraph_id":N,"new_text":"one paragraph","reason":"..."}]}`.
- Max 5 patches; each patch replaces exactly one existing editable paragraph with exactly one paragraph.
- No insertion/deletion/reordering; no edits outside selected IDs.
- Already-correct text stays unchanged; do not use the call for general polishing.
- Never invent injuries, numbers, ownership/source, old history, private cognition or new powers.

## Derivation acceptance gate

Across 2 repeats × 4 chapters, anonymous fresh Story + Authority three-way blind compares:

`Primary` vs `L2 High-Local Repair` vs `Luna-high Full Reviser`.

L1 may advance to a third entirely new held-out novel only if all are true:

1. L2 Story mean is within 2 points of both Primary and high, with no catastrophic truncation.
2. L2 Authority hard-problem count <= high + 2 across the 8 samples, and Authority mean is within 3 points of high.
3. All unselected paragraphs remain exact; paragraph count unchanged; patch parse/apply 8/8.
4. Mean L2 repair wall is at least 40s/chapter lower than high Reviser wall on the same stored sample set.

If any condition fails, stop this candidate family; do not generate held-out3.


## Single changed variable
L1 → L2 changes only the local repair model effort: `gpt-5.6-luna medium` → `gpt-5.6-luna high`. Locality selector, quotas, threshold, editable paragraph IDs, patch grammar and acceptance gate remain unchanged.
