# Three Random Books to Story Program — Test Rules

- Date: 2026-08-25
- Baseline: `21ba884` on `principal_dev_new_sys`
- Goal: generate three entirely new books through Story Program using the current production prompts and GBrain routing.
- Fantasy Seed: one GPT-5.6 Luna high call; freeze candidates 1, 2, 3 as Book A/B/C before seeing downstream outputs. No cherry-picking. GBrain OFF.
- World Vision: one independent GPT-5.6 Luna high call per book; GBrain ON with fixed 1 Coordinate Reference + up to 3 creative inspirations.
- Story Program: one independent GPT-5.6 Sol high call per book; GBrain ON up to 3 creative inspirations.
- Approval fixture: the user explicitly requested automatic generation through Story Program; frozen candidate selection is treated as experimental author approval solely to traverse the production approval gates.
- No Outline or chapter generation.
- No production prompt/code modification during this generation experiment.
