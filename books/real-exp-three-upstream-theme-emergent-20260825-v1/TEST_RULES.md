# 三本新书上游生成规则

- 目的：验证 2026-08-25 Theme Emergent production 上游链，并交付三本截至 Story Program 的完整上游产物。
- 作者方向在 Seed 前冻结；Seed 仅跑一次 production Prompt，生成后固定继续候选 1 / 2 / 3，不事后挑选。
- Fantasy Seed：GPT-5.6 Luna high，GBrain OFF。
- World Vision：GPT-5.6 Luna high，固定 1 条 Coordinate Reference + 最多 3 条 creative GBrain。
- Story Program：GPT-5.6 Sol high，最多 3 条 creative GBrain。固定 World Coordinate Reference 不重复占 downstream creative 名额。
- 每个阶段进入下游前统一剥离 ACP `<oai-mem-citation>` 辅助 metadata；raw ACP JSON 保留作审计。
- 本轮按作者要求停止在 Story Program；不保留、不交付 Outline。
- 不生成章节。
