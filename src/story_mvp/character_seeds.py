from __future__ import annotations

import re


_CANDIDATE_RE = re.compile(
    r"(?ms)^# CHARACTER CANDIDATE (?P<index>\d+)｜(?P<title>.+?)\n(?P<body>.*?)(?=^# CHARACTER CANDIDATE \d+｜|\Z)"
)
_SECTION_RE = re.compile(r"(?m)^## .+$")

_POWER_SECTION_HEADINGS = (
    "## World Power Normal → Exception",
    "## Core Fantasy / 特殊际遇",
    "## Growth Compatibility｜怎样真正越来越强",
    "## 为什么读者会馋",
)


POWER_SEED_SCHEMA = """# POWER SEED

## World Power Normal → Legal Exception
先说明与本异常直接相关的世界力量正常值、稀缺度或获得/承载规则，再说明人物合法偏离哪一条正常分布。

## Core Fantasy
用普通话说明：如果我是他，我具体能做什么，为什么这件事本身值得想拥有。

## Growth Compatibility
- 正常修炼轴：世界正常修炼怎样真实增强基础力量。
- 异常掌握轴：Exception 怎样扩大容量、精度、组合、适用对象、持续时间、层级或行动自由。
- High-Tier Mutation：进入高层力量竞争后发生什么质变，而不只是数量/距离/持续时间变大。
- 永久边界：至少一条高阶也不会自动消失的限制。

## Legendary Trajectory
如果这个成长方向长期成立，他最终有机会成为怎样令人向往的强者/存在？只写上限方向，不写剧情阶段。

## Power Audit Metadata（非 Canon）
### Future Legend Image
如果他真正成长成功，最值得读者亲眼看到的一幅传奇画面是什么？这是候选审计，不绑定未来剧情。
"""


HUMAN_SEED_SCHEMA = """# HUMAN SEED

## 世界中的初始位置与成长环境
只来自 LIFE_CONTEXT；可以贫穷、普通、富裕、受保护、既得利益、天赋优越或其它世界合法位置，不预设底层受害者。

## Formative Facts → Adaptation → Observable Behavior
具体经历先发生；人物形成可能正确也可能错误的适应；最后落到今天可观察的选择。

## 当前私人欲望
现在真正牵着他行动的具体东西，不总结终身主题。

## Core Obsession
什么东西不会因为一个任务完成就消失，反而可能随着能力、见识和行动空间扩大而越来越想要？它不是公共使命，也不必正确或高尚。

## Excess
他在哪一种欲望、厌恶、好奇、恐惧或执念上明显“过量”，以至于普通人觉得已经够了，他仍然不肯停？不要用性格标签或固定菜单回答。

## Behavior Signature
读者逐渐能预测他不会接受什么、会为何承担代价；具体手段仍由当下信息、风险和关系重新生成。

## 重要关系原点
2—4 个即使这个人永远没有特殊能力，彼此之间仍有未完成故事的人；双方都有自己的欲望。

## 人物钩子
如果完全不知道他以后会得到什么能力，前三章后读者为什么仍会记得并想继续看这个人？
"""


def _section(block: str, heading: str) -> str:
    start = block.find(heading)
    if start < 0:
        return ""
    tail = block[start + len(heading):]
    match = _SECTION_RE.search(tail)
    end = start + len(heading) + (match.start() if match else len(tail))
    return block[start:end].strip()


def split_character_candidates(text: str) -> list[dict[str, str | int]]:
    return [
        {
            "index": int(match.group("index")),
            "title": match.group("title").strip(),
            "text": match.group(0).strip() + "\n",
        }
        for match in _CANDIDATE_RE.finditer(text)
    ]


def extract_frozen_power_seed(candidate_text: str) -> str:
    """Extract the already-generated v4 power authority without inventing new facts.

    High-Tier Mutation / Legendary Trajectory / Future Legend Image are part of the
    new schema for future Power generation, but are intentionally not backfilled
    into a frozen baseline candidate because that would contaminate the split-seed A/B.
    """

    title = candidate_text.splitlines()[0].replace("# CHARACTER CANDIDATE", "# FROZEN POWER SEED", 1)
    parts = [title]
    for heading in _POWER_SECTION_HEADINGS:
        block = _section(candidate_text, heading)
        if not block:
            raise ValueError(f"missing power section: {heading}")
        parts += ["", block]
    parts += [
        "",
        "## 新版 Power Seed 暂不回填的字段",
        "High-Tier Mutation / Legendary Trajectory / Future Legend Image 属于新版 schema；本轮为了冻结 v4 Power 变量，不用新模型补写，也不从 Biography 反推。",
    ]
    return "\n".join(parts).strip() + "\n"


def compose_character_card(*, power_seed: str, human_seed: str, index: int) -> str:
    """Merge two frozen authorities without reconciling or explaining them."""

    return (
        f"# CHARACTER CARD {index}｜Split Authority\n\n"
        "## POWER CORE｜Frozen Authority\n\n"
        f"{power_seed.strip()}\n\n"
        "## HUMAN CORE｜Frozen Authority\n\n"
        f"{human_seed.strip()}\n\n"
        "## Composition Boundary\n"
        "两份 Seed 原样并列。此处不解释为什么某段童年象征某种能力，不重写欲望去适配金手指，也不推演世界将怎样回应。发现、使用、关系化学反应与真正的故事碰撞留给后续 Collision Authority。\n"
    )
