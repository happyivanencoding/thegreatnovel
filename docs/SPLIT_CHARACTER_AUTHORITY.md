# Split Character Authority — Frozen Production Architecture

Status: **FROZEN / production**

This document defines the upstream creative authority used by new TGN books. It is intentionally small. Do not add extra agents, reviewers, scorers, or approval gates merely to enforce these principles.

## 1. Production chain

```text
Author Direction
      |
      v
WORLD VISION
protagonist-blind
      |
      +-----------------------------+
      |                             |
      v                             v
POWER_BASELINE                 LIFE_CONTEXT
      |                             |
      v                             v
POWER SEED                    HUMAN SEED
fresh context                 fresh context
GBrain power craft            GBrain human craft
      |                             |
      +-------------+---------------+
                    v
             CHARACTER.md
        deterministic composition
                    |
                    v
              STORY PROGRAM
          first full collision
                    |
                    v
                 OUTLINE
```

There is no Fantasy Seed production stage.

Power Seed and Human Seed are two independent creative authorities, but they are **not two approval gates**. The author approves Character once; that freezes both selected seeds and deterministically materializes `CHARACTER.md`.

Different model families are optional. The essential decorrelation mechanism is **fresh context + authority isolation**. World and Human may both use Luna high, for example, as long as Human does not inherit hidden Story Opportunity context.

## 2. World Vision

World Vision creates a world that remains worth writing about even if the eventual protagonist is replaced.

It owns:
- ordinary life and routes of social ascent;
- power system and observable normal / rarity baselines;
- social reality and identity consequences;
- concrete things people value;
- independent people and events already moving;
- places, wonders, dangers, and unknowns;
- world knowledge boundaries.

It does **not** own protagonist desire, protagonist biography, protagonist ability, protagonist destiny, first payoff, or final mission.

World Reality and Story Opportunities may coexist in the full World Canon, but downstream visibility is different.

## 3. Power Seed authority

Power Seed sees only the deterministic `POWER_BASELINE`, never the full Story Opportunity layer and never Human biography.

Generation order:

`World Power Normal -> Legal Exception -> Core Fantasy -> Growth Compatibility`

Power Seed owns:
- the relevant world normal / rarity baseline;
- the Legal Exception;
- Core Fantasy and why a reader would want it;
- normal cultivation axis;
- exception mastery axis;
- High-Tier Mutation;
- permanent boundary;
- Legendary Power State.

`Future Legend Image` is audit-only and non-Canon.

The protagonist is a male-oriented progression protagonist: temporary lows are allowed, but normal cultivation must genuinely strengthen the protagonist and the exception must remain compatible with long-form upward progression. The exception must not merely replace cultivation with a clever occupational technique.

Power Seed is anonymous. Name and personal identity never belong to Power authority.

## 4. Human Seed 权威

Human Seed 只读取确定性的 `LIFE_CONTEXT` 与 Human GBrain craft；它对 Power 和已有 Story Opportunity 都保持盲态。

Human 生成遵循：

`生活事实 → 多重动机 → 冲突中的稳定选择偏向 → 具体人物关系`

Human Seed 是一个人的权威快照，不是人格证明论文。过去提供受世界塑形的生活事实，但不需要为后来每一个性格特征逐条作证；不要先决定一个漂亮的人格命题，再反向发明几段恰好证明它的童年。

它负责：
- 初始社会位置与成长环境；
- 具体生活事实；
- 数股可能竞争、重排或被关系改变的长期私人动机；
- 行为签名；
- 重要关系原点；
- 相对稳定的身份事实。

长篇成立**不要求**一个单一核心执念或统一人生哲学。私人动机只要能在更大处境里持续改变选择，就具有长篇生产力；多股动机可以互相冲突，也不需要自动长成事业、资产、标准、决策权、权威位置或组织规模。

行为签名遵循**稳定选择偏向 + 具体实现随现场变化**：读者可以逐渐知道这个人倾向保护什么、拒绝什么、过度看重什么、愿为什么付代价，但具体手段仍由当下信息、风险、力量边界和关系重新生成。具体关系只有在“因为是这个人”而真实改变选择时才成立；同等有用不能替代。

### 可变状态与非正式事实边界

`current private desire` 只初始化 `CHARACTER_INITIAL_STATE.md`，不冻结进 Human Core。

`Character Hook` 属于 `CHARACTER_AUDITION.md`，只证明候选人物在没有特殊力量时也有辨识度；它不绑定开篇章节，也不进入正式故事事实。

`CHARACTER_INITIAL_STATE.md` 只表示 T0。章节开始后，已有 BOOK Canon + State Delta 链仍是唯一运行状态权威，不再创建第二套长期人物状态系统。

## 5. Character 确定性组合

`CHARACTER.md` 只是冻结 Power Core 与 Human Core 的确定性合并，**没有 Character Composer LLM**。

不能为了让两种权威显得“本来就匹配”而补 Biography，例如：
- 两个家，所以得到双位置能力；
- 童年有未完成之事，所以得到未完成术法能力；
- 从事修理，所以得到修理型超能力。

不协调是创作材料，不是错误。

编辑任一已选 Seed 会重新打开 Character 权威并使下游 Story/Outline 失效，但不会重写 World。

## 6. Collision 权威

Story Program 是第一次允许同时看到以下内容的阶段：
- 完整 World；
- 完整 Character；
- Character T0 state；
- Story GBrain / References。

核心合同：**不要把碰撞消解成命中注定的适配。**

World 是事实，Character 是事实。Story Program 的职责是发现二者碰撞以后会发生什么。它可以创造事件、关系、反制、后果、阶段发动机和长期推进，但不能为了主题整齐而重写任一上游权威。

权威与调度必须分开。Power Seed 决定成长语法——正常修炼、异常掌握、高阶质变、永久边界、传奇状态；Story Program 决定**这些已经批准的可能性在什么时候、通过什么故事因果真正成为现实**。成长是全书纵向不变量，但不要求每个大型阶段都出现新升级或新获得。

Collision 允许为了让当前关系、局部性格反应或某次选择更自然，补充少量**非奠基性的过去经历、共同往事或旧事件**。这些过去可以解释局部质感，但不能重写 Human Core，也不能把整个人格收束成创伤因果链；不得为了人格合理化自动制造悲惨童年、背叛、虐待或重大失去。普通、愉快、尴尬、失败、欲望、争执和错过同样可以有重量。

**历史事实与历史揭示必须分开。** 这类新补的过去不得自动成为小说主线或大型阶段发动机，也不得一次性倾倒；Story Program 可以知道它存在，Outline 只在当前故事真正需要时逐步安排读者看见其中一小部分。

当前大型阶段合同保持轻量：为什么现在发生、谁想要什么、主角关键选择/行动、主要阅读满足、`Stage Delta`、下一阶段为何自然发生。`Stage Delta` 只写实际发生变化的维度，例如 Power/Capability、Possession、Relationship、Identity/Access、Knowledge、Enemy State、World State；任何维度都不是阶段必填项。

高价值获得与纵向复利仍是全书级创作原则，不是阶段税。真实发生获得时，应当值得想要、真正被持有/使用，并继续影响后续故事；旧获得不能写完一个阶段就消失。二者都不需要固定的阶段字段。

Outline 在更细分辨率上继承同一权威边界。它是已批准 Story Program 的执行编译层，不是第二个 Story Program。每个故事块只在 `Block Delta` 中写**相对本块开始**真实改变的维度，未变化的维度省略。关系/世界驱动的块可以完全没有 Power/Capability、Possession 或新世界变化；反过来，Story Program 已安排的真实 Power 变化到时必须通过具体故事锚点发生。Outline 不得为了填满块表单制造微升级、填充奖励、新权限或新地图。

反制只能在碰撞后通过学习产生；敌人不能仅仅为了机械克制主角而出生。

## 7. GBrain visibility

GBrain retrieval obeys exactly the same authority boundaries as generation prompts.

- World lane: world craft.
- Power lane: `POWER_BASELINE` only; no named Story Opportunities.
- Human lane: `LIFE_CONTEXT` only; no power and no named Story Opportunities.
- Story lane: Full World + Character for the first time.

Power and Human each remain bounded to a small inspiration bundle. Human GBrain should diversify human appetite, behavior, and relationship gravity rather than classify personalities or prescribe a menu of character types.

## 8. Life texture belongs downstream

`Life Texture / Human Appetite` is **not** an upstream Human Seed field.

Ordinary-life texture is a Writer/Curator-side permission. When the current scene naturally supports it, Curator or a single Writer may project **0–1** small life detail from already approved World Vision facts.

It must not:
- establish a new world rule;
- create a new character motive;
- create a new story obligation;
- become long-running Canon merely because it was used as texture;
- appear mechanically in every chapter.

Texture is decoration carried by story, not the soil that decides who the protagonist must be.

## 9. Approval and stale graph

Production approvals remain compact:

1. approve World Vision;
2. approve Character once (Power + Human together);
3. approve Story Program.

Dependency direction:

`World -> Power/Human -> Character -> Story Program -> BOOK/Outline -> chapters`

A downstream edit never rewrites an upstream authority. A World edit stales Power/Human and everything below. A Power or Human edit stales Character and everything below, but does not stale World.

## 10. What is deliberately not added

Do not add by default:
- Character Composer;
- personality scorer;
- MBTI / trait checklist;
- mandatory weirdness;
- mandatory trauma;
- mandatory anti-world protagonist;
- separate per-character LLM state calls each chapter;
- Life Texture agent;
- new hard gates for Human diversity.

The architecture solves rationalization through **information boundaries**, not through growing negative-prompt walls.
## Human GBrain lane budget

Human Seed GBrain retrieval uses three independent lanes, not one shared Top-N pool:

- `appetite`: what the person privately wants or values even without direct progression payoff;
- `behavior`: stable choice bias / character hook without turning it into a personality taxonomy;
- `relationship`: concrete people whose independent desires can change the person's choices.

Each lane contributes **at most one ACTIVE craft card** and Human Seed still receives at most three cards total. A lane may remain empty; REFERENCE_ONLY / HOLD material never fills a slot merely to reach three. The same card cannot occupy two lanes. New Human Craft should declare `human_lane: appetite|behavior|relationship` in frontmatter; older cards are classified from narrow craft metadata only.

The three lanes are retrieval budgets, **not three required personality dimensions or Hard Gates**.

## Explicit anonymous Human Prototype experiments

Private or author-specific Human prototypes are **explicit-only generation controls**, not default Human craft and not Character Canon.

Current contract:

- default selector is empty; ordinary books cannot silently retrieve an experimental private prototype;
- only `human_seed` may consume a prototype selector; World / Power / Story / Outline ignore it;
- an explicit prototype resolves an allow-listed opaque prototype ID to exact Human craft pages rather than using semantic search;
- the prototype must supply exactly one valid Appetite, Behavior, and Relationship page. Missing, inactive, wrong-prototype, or wrong-lane pages fail closed instead of falling back to generic Human craft;
- explicit prototype pages declare `experimental_activation: EXPLICIT_PROTOTYPE_TEST`; generic Human retrieval rejects them even if a broad query happens to hit them;
- the selector generates **one fictionalized Human Seed**, not multiple personality variants. LIFE_CONTEXT rebuilds family, class, education, work/cultivation exposure and relationships inside the fictional world; real biography is never reconstructed;
- Power remains invisible during Human generation. Character remains a deterministic `Power Core + Human Core` merge; no Composer explains why the prototype “deserves” the Power;
- the opaque prototype ID is generation metadata only. It is not persisted into `CHARACTER.md`, T0 state, Story Program, Outline, or prose Canon.

This mechanism exists to let an author deliberately test a private Human prototype without contaminating ordinary novel generation. Do not generalize a private prototype into a cross-book Human mechanism merely because it produces a compelling protagonist.
