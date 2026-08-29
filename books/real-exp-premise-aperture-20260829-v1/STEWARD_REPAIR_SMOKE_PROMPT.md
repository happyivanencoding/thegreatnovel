Use the current installed `tgn-system-steward` skill as your operating method.

READ-ONLY audit. Do not edit files.

Read exactly:

1. `docs/PREMISE_APERTURE_EXPERIMENTAL_CANDIDATE.md`.
2. `books/real-exp-premise-aperture-20260829-v1/RESULTS.md` sections 8.6—13.
3. `books/real-exp-premise-aperture-20260829-v1/fast_multiworld/compilable_single_v5_repair/PROTOCOL.md`.
4. `books/real-exp-premise-aperture-20260829-v1/fast_multiworld/compilable_single_v5_repair/ORIGINAL_SELECTED_S2.md`.
5. `books/real-exp-premise-aperture-20260829-v1/fast_multiworld/compilable_single_v5_repair/REPAIRED_S2.md`.
6. `books/real-exp-premise-aperture-20260829-v1/fast_multiworld/compilable_single_v5_repair/PROTECTED_CORE_VALIDATION.json`.
7. `books/real-exp-premise-aperture-20260829-v1/fast_multiworld/compilable_single_v5_repair/RUN_SUMMARY.json`.

Question:

> A bold selected premise failed the independent Compiler. Should TGN automatically repair it, silently copy missing protected fields back, choose another candidate, or stop and return the exact conflicts to the author? What is stable, what is merely experimental, and what should production do now?

Requirements:
- distinguish Stable Principle / Current Default / Experimental Candidate;
- verify the actual V5 failure instead of trusting the Prompt;
- identify the missing protected field;
- say whether Compiler/downstream should have run;
- explain why this failure does not invalidate Premise Forge or the independent Compiler;
- no automatic selector, no repair loop, no new per-chapter agent;
- give a concise freeze recommendation and residual risk.
