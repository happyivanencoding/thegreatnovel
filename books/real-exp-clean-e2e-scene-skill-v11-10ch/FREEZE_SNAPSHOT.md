# Freeze Snapshot

记录时间：2026-08-22（Europe/Paris）

## Production baseline

- branch: `principal_dev_new_sys`
- production/evidence HEAD before experiment scaffold: `4dbc289`
- Scene Skill v1.1 implementation commit: `f15190b`
- validated freeze tag: `freeze/principal_dev_new_sys-scene-skill-v1.1-validated-f15190b`
- prose A/B/C evidence commit: `4dbc289`

## Frozen design decision

Scene Skill v1.1 在本实验期间视为冻结：

- 20 个现有 Primary Skill 不增不删；
- `1 Primary + optional 1 Secondary` 不改；
- Curator Selection / runtime loader 不改；
- 不新增 Utility / Modifier / scorer / validator / retry / Scene Agent；
- 如果十章实验暴露真实 bug，先记录，再做最小独立修复，不把实验变成框架扩建。

## Input isolation

唯一人工作者方向见 `INPUT.md`。旧小说与旧实验只可作为代码/运行证据来源，不得作为新书创作内容输入。
