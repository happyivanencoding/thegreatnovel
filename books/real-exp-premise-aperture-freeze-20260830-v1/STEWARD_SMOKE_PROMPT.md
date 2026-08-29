Use the currently installed `tgn-system-steward` skill as your operating method.

READ-ONLY bounded audit. Do not edit files.

Read exactly:

1. `PROJECT_RULES.md` sections 2.1, 2.2 and 5.
2. `docs/PREMISE_APERTURE.md`.
3. `src/story_mvp/premise_workflow.py`.
4. `src/story_mvp/app.py` only the PromptRequest, Premise routes, `_prompt_kwargs`, and `/api/prompt` branches.
5. `src/story_mvp/character_prompts.py` only the Premise contract injections.
6. `src/story_mvp/workflow_state.py` only `premise.contract` registration and invalidation.
7. `tests/test_premise_production.py`.
8. `tests/test_author_workspace_ui.py` only the Premise test.

Question:

> Has the previously experimental F1–F5 Premise Aperture actually become a correct optional production opening stage, or is it only documented as frozen? Audit the real state machine, author gate, compiler snapshot binding, lane isolation, runtime cutoff, workflow authority, UI choices, and legacy-path compatibility.

Required output:

# PREMISE APERTURE FREEZE SMOKE
## Verdict
PASS / CONDITIONAL PASS / FAIL.

## Current Default Verified
State exactly what is now production and what remains research-only.

## State Machine Trace
Verify `not_started`, `skipped`, started-unapproved, strict PASS, edited-after-compiler, approved, and World-approved behavior.

## Authority Visibility Trace
Verify what World / Power / Human / Story see, and confirm Outline / chapter do not receive raw Premise.

## Workflow / UI Trace
Verify only `premise.contract` is formal authority and that UI has author selection, approve and skip but no auto selector / repair loop.

## Findings
Report only real defects that would change the freeze decision. Do not manufacture findings. If correct, say it is correct.

## Residual Risks
Name only risks not already solved by current tests and contract.

Do not recommend a new Reviewer, Scorer, repair loop, feature flag, migration framework, compatibility wrapper, checksum, hash, or per-chapter Premise Agent.
