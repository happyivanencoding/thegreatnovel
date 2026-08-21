# Freeze Snapshot

记录时间：2026-08-21（Europe/Paris）

## Git

- branch: `principal_dev_new_sys`
- HEAD: `5992f62d11e8014c3cf783bf993589e1cb881585`
- status: clean（`git status --short` 无输出）
- HEAD subject: `docs: record dynamic pacing freeze verdict`

## 有效生产 Prompt

- source: `src/story_mvp/prompts.py`
- `DEFAULT_DIRECTOR_TEMPLATE`: line 108
- `FANTASY_SEED_TEMPLATE`: line 484
- `WORLD_VISION_TEMPLATE`: line 535
- `STORY_PROGRAM_TEMPLATE`: line 599；通过 `DEFAULT_PROMPT_TEMPLATES["idea"]` 注册
- `OUTLINE_TEMPLATE`: line 669
- `DEFAULT_STATE_DELTA_TEMPLATE`: line 835
- Writer 的当前正式模板：`DEFAULT_PROMPT_TEMPLATES["chapter"]`，并由 `generate_prompt(mode="chapter", ...)` 追加 `PROSE_REALIZATION_CONTRACT`
- Chapter Prep 的当前正式模板：`DEFAULT_PROMPT_TEMPLATES["chapter_prep"]`

## Prompt 相关提交证据

当前 `src/story_mvp/prompts.py` 的最近相关提交为：

- `2c1e3434b6d68043ba0aac556e63d7912ba23368` — Long-Form Pacing
- `2be35340b36aa05588c85324ffd5e2e1bfa6d951` — Outline Eventization
- `e2e3bac29039afa075a60d48b31abe1d0d9ff3f2` — compounding growth engine
- `b6828961e9e4939577e66264cc0b9a62de1ade95` — first-payoff moral default neutralization
- `a6e551460f1f13a8d42c44d43e8961b4f552958e` — Fantasy-First production prompt neutralization
- `bb5361519929c996aa386672897bc98756e02a51` — Fantasy-First Story System v1

## 输入隔离

本轮生成阶段不读取 GBrain、Reference Programs、旧 BOOK、Growth Genome 旧实例、历史候选、旧 Reviewer、旧评价或其它小说正文。唯一作者输入是 `INPUT.md`。
