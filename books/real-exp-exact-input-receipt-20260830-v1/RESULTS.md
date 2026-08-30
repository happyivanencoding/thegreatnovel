# Exact-Input Phase Receipt｜Final Report

> Date: 2026-08-30
> Status: **PASS / PRODUCTION INCREMENTAL-RECOVERY OPTIMIZATION**

## Final Verdict

受 novel-studio 的 sealed input/body identity 与 ainovel-cli 的 deterministic checkpoint/recovery 启发，本轮没有再改变 TGN 的 Story/Authority 模型链，而是寻找“已经做过的昂贵推理是否被 Workflow 无效重跑”。

结论：**存在真实可达 false-stale，并已用 exact-input receipt 安全消除。**

这不是首次章节生成加速器。默认首跑仍是：

`Luna Director → Luna Curator → Terra Primary → Luna high Authority Reviser → Luna State`。

它优化的是：作者修改 World / Character / Canon / Plan 等上游后，future run 因依赖关系被标 stale，但某个节点最终 bounded Prompt 实际逐字没有变化的增量恢复。

## 1. Existing TGN behavior that was already good

TGN 原本已经具备 ainovel-cli 式 step-level retry：failed/stale 节点可以复用保存 Prompt 单点 retry，completed 上游不会因下游失败而重跑。因此没有新增 checkpoint framework。

TGN 也已经真实否决过跨章 Speculative Director / Pre-Curator 作为默认快路，因此没有重新测试“提前猜下一章”。

真正缺口在于：Workflow stale 依据上游 artifact revision；而章节节点实际只消费 bounded projection。Artifact revision changed 并不总等于 final model input changed。

## 2. Reachable false-stale proof

在第一部 held-out 新小说的 future Ch5 上，使用 production prompt builder：

- 修改 `WORLD_VISION.md` 的实质世界事实行；
- Workflow 正常将 future Director 标 `stale`；
- 重新构建 Ch5 Director Prompt：**exact identical**。

同样的现象也在 `CHARACTER.md` 上出现。

逐行 substantive mutation audit：

| Artifact | substantive candidates | Director exact unchanged | Curator exact unchanged | Primary exact unchanged* | Reviser exact unchanged* |
|---|---:|---:|---:|---:|---:|
| World Vision | 42 | **42/42** | **38/42** | **42/42** | 17/42 |
| Character | 26 | **26/26** | 12/26 | **26/26** | 1/26 |

`*` Primary/Reviser 统计固定其上游 LLM response，用来测该 artifact 是否进入该节点最终 Prompt；真实恢复会逐节点 promotion，前一节点 Prompt/Response exact 才继续尝试下一节点 receipt。

这说明 broad dependency stale 是正确的保守第一步，但不能直接推导“每个 stale node 都必须重新调用模型”。

## 3. Production receipt contract

每个新节点 manifest 额外保存：

- `prompt_sha256`：当前 Prompt exact UTF-8 identity；
- `response_prompt_sha256`：产生当前 Response 时消费的 Prompt identity；
- `response_sha256`：Response 文件 exact body identity；
- `response_receipt_status`；
- `receipt_reuses` / one-shot `receipt_reused`。

恢复逻辑：

```text
upstream artifact changed
        ↓
existing dependency logic marks future node STALE
        ↓
Runtime rebuilds node Prompt normally
        ↓
new prompt SHA == response receipt prompt SHA ?
        │
      NO ───────────────→ normal LLM rerun
        │
       YES
        ↓
response file SHA still exact ?
        │
      NO ───────────────→ normal LLM rerun
        │
       YES
        ↓
restore COMPLETED / ADOPTED
0 LLM calls
```

Explicit `retry_node()` never uses receipt. Legacy manifests without receipt fail closed and rerun normally. No fuzzy/semantic hash exists.

## 4. Real integration result

同一 held-out Ch5，冻结一条 World substantive edit，它改变 Reviser Prompt，但不改变 D/C/P Prompt。

Workflow change 后：

```text
Director = STALE
Curator  = STALE
Primary  = STALE
```

重新构建并保存 Prompt 后：

| Node | receipt revalidation | model calls | Response |
|---|---:|---:|---|
| Director | 2.96ms | 0 | exact preserved |
| Curator | 2.889ms | 0 | exact preserved |
| Primary | 2.265ms | 0 | exact preserved |
| Total | **8.794ms** | **0** | **3/3 exact** |

同一本新书已实际生成的历史平均 wall：

- Director: 26.848s
- Curator: 112.512s
- Primary: 35.436s
- D+C+P: **174.796s**

因此这个真实增量恢复 case：

> **174.796s → 0.008794s，净省约 174.787s，即约 2分55秒 / 受影响章节。**

如果某次 edit 连 Authority Reviser Prompt 也 exact unchanged，则该节点也可以同样复用；本轮示例故意选择 Reviser Prompt 会变化的 World edit，因此 Reviser 仍正常重跑。

## 5. UI / executor integration

仅后端恢复 status 不足以省时间。旧 Web OpenAI 路径在 PUT Prompt 后会无条件调用 executor。

现在：

- Prompt PUT 返回 node `receipt_reused=true`；
- Web 不调用 OpenAI，也不生成 Codex task；
- 通过只读 Run Response endpoint 回填已保存 Response；
- Workflow 刷新后直接进入下一个 actionable node。

因此这是实际 0-call reuse，不是 manifest bookkeeping。

## 6. Safety boundaries

以下全部正常重跑：

- Prompt 任一字符变化；
- Response 文件被人工修改；
- receipt digest 缺失；
- historical manifest 未建立 receipt；
- explicit retry / intentional resampling；
- previous failed response / Outcome Repair failed response。

Receipt 不判断 Story 语义，也不决定两个 Prompt “意思差不多”。它只回答 exact identity。

## 7. What this improves / does not improve

### Improves

- 作者修改上游后的 future-run 恢复；
- broad stale 后的逐节点重验证；
- 不影响 bounded projection 的 World/Character 编辑；
- 后续相同模式的 safe recovery。

### Does not improve

- 第一次生成一章的 5分钟级 wall；
- Full Luna-high Reviser 133s 的首次 reasoning；
- Story/Authority 模型质量；
- 模型本身 latency。

因此不能把 `174.787s` 写成“每章常态提速”。它是**一个真实 author-edit stale recovery case 的节省**。

## Production Decision

**PASS，进入 production Run Ledger。**

原因不是“缓存通常有用”，而是：项目自身存在 `stale + exact identical final Prompt` 的可达 case；digest 直接替代昂贵 LLM rerun；复用 Response 字节完全相同，质量风险为零；explicit retry 与不完整旧 receipt 均 fail closed。
