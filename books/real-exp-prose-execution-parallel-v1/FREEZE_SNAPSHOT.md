# Freeze Snapshot

## 仓库与生产基线

- repository：`C:\dev\tgn-story-mvp`
- branch：`principal_dev_new_sys`
- HEAD at experiment start：`5992f62d11e8014c3cf783bf993589e1cb881585`
- required Long-Form Pacing baseline：`2c1e3434b6d68043ba0aac556e63d7912ba23368`
- current HEAD contains the documented `CREATIVE_CHAIN_FROZEN_V2` + `OUTLINE_FROZEN_V2` state.
- start Git status：clean apart from this new experiment directory after initialization.

## Frozen source chain

### Candidate A

Source directory is an exact copy of `books/real-exp-dynamic-pacing-v1/candidate-a/`. The execution source is `candidate-a/source/treatment_outline.md`; Seed, World Vision and Story Program are retained beside it for provenance. No A creative artifact is regenerated.

### Candidate C

Source files are exact copies of `books/real-exp-compounding-narrative-downstream-v1/candidate-c/`: `fantasy_seed.md`, `world_vision_prompt.md`, `world_vision_response.md`, `story_program_prompt.md`, and `story_program_response.md`. No C source artifact is modified. A current V2 Outline is absent from this checkout and is therefore the only upstream artifact permitted to be generated in this experiment.

## Runtime isolation

- no GBrain
- no Reference Programs
- no Candidate B files,正文、Reviewer 或结论
- no production code or Prompt edits
- no formal BOOK/Canon writes outside this experiment directory
- maximum generated chapters: six total, A1—A3 and C1—C3

## C Outline supplement

- C Outline prompt：`candidate-c/outline/outline_prompt.md`
- C Outline response：`candidate-c/outline/outline_response.md`
- C window：`N=30`，窗口终点为第 30 章“废弃界门点亮”。
- C source hashes：`fantasy_seed.md`=`368803B914D3D15292A2220D975E7291D5EE101E52A857A892CEAF28D43522E9`；`world_vision_response.md`=`827CB8FEAD5A54A93F83C07185AF914F9DE5BAAD14CCBF9A2B4D5EFA57B8136B`；`story_program_response.md`=`5A897E98BB91A653D9CF81073C936A6C1EB88822FE405C667D84F00AAD38A190`。
- C Outline prompt SHA-256：`8AFA902A32B65EB8F0924533F8FAF4D7A755BAA117B3DD500F32BFACE2536A86`。
- C Outline response SHA-256：`1F5F699062492F31A850C4F70B28FA2F43B28427F9F880F9D576969AA998B6CA`。

## Execution completion

- A/C each have 3 Director, 3 Chapter Prep, 3 Writer and 3 State Delta calls; each call has a saved prompt and response.
- A source Dynamic Outline SHA-256：`101BF079A92D0680C0A5323C4B7BF428E9B340C71087EC3746AB2A06AD4B3001`。
- A/C formal prose body character counts：A=`5367 / 7754 / 9053`；C=`4441 / 6576 / 6069`。
- no Chapter 4 directory exists; production `src/` and `tests/` have no tracked diff.
