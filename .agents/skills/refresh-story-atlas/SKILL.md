---
name: refresh-story-atlas
description: 在 source、edition 或当前边界发生可审计变化后刷新版本化 Story Atlas；保留稳定实体 ID 和旧版本，不写入 Canon。
---

# Refresh Story Atlas

Handoff Mode 只读取 `task.json` 指定的业务输入；START 已负责 source/edition integrity。
读取上一版 Atlas、最新初始化报告和变更证据；如果 Initialization 已提供 verified Arc、
Entity Resolution 或 Synthesis，优先复用并只处理影响范围和新证据，不重复全文 Arc Extraction。
只生成新的不可变 `story_atlas/versions/<atlas_id>/` 派生版本。Atlas Render 是独立显式操作，
refresh 不自动生成七张 SVG。旧 Atlas 不覆盖、不删除；未来路线不能被写成逐章固定大纲。
