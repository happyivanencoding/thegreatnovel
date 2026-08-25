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

## Legendary Power State
如果这项异常长期成长成功，单看力量体验，最终可能达到怎样令人向往的高阶状态？只写能力与行动体验，不写未来身份、组织、统治位置、使命或剧情阶段。

## Power Audit Metadata（非 Canon）
### Future Legend Image
如果他真正成长成功，最值得读者亲眼看到的一幅传奇画面是什么？这是候选审计，不绑定未来剧情。
"""


HUMAN_SEED_SCHEMA = """# HUMAN SEED

## 世界中的初始位置与成长环境
只来自 LIFE_CONTEXT；可以贫穷、普通、富裕、受保护、既得利益、天赋优越或其它世界合法位置，不预设底层受害者。

## Formative Facts → Adaptation → Observable Behavior
具体经历先发生；人物形成可能正确也可能错误的适应；最后落到今天可观察的选择。

## Core Obsession
什么私人牵引不会因当前问题解决就自动结束，并会在更大人生里继续让他做出“别人已经觉得够了、他还是会继续”的选择？它不必积累成资产、事业、社会地位或权威；只要持续改变选择就足够长篇。它不是公共使命，也不必正确或高尚。

## Excess
他在哪一种欲望、厌恶、好奇、恐惧或执念上明显“过量”，以至于普通人觉得已经够了，他仍然不肯停？不要用性格标签或固定菜单回答。

## Behavior Signature
读者逐渐能预测他不会接受什么、会为何承担代价；具体手段仍由当下信息、风险和关系重新生成。

## 重要关系原点
2—4 个即使这个人永远没有特殊能力，彼此之间仍有未完成故事的人；双方都有自己的欲望。

## Initial State Seed
### 当前私人欲望
现在真正牵着他行动的具体东西；它只初始化 Character State，不属于永久 Human Core。

## Audition Metadata（非 Canon）
### 人物钩子
如果完全不知道他以后会得到什么能力，给一个候选审计用的可复述人物场面/印象，证明这个人本身有戏。它不进入永久 Character Core，也不绑定前三章真实事件。
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

    High-Tier Mutation / Legendary Power State / Future Legend Image are part of the
    new schema for future Power generation, but are intentionally not backfilled
    into a frozen baseline candidate because that would contaminate the split-seed A/B.
    """

    first_line = candidate_text.splitlines()[0]
    match = re.match(r"# CHARACTER CANDIDATE (?P<index>\d+)｜(?P<title>.+)", first_line)
    if not match:
        raise ValueError("invalid character candidate heading")
    source_title = match.group("title").strip()
    if "／" in source_title:
        source_name, power_label = (part.strip() for part in source_title.split("／", 1))
    else:
        source_name, power_label = "", source_title
    title = f"# FROZEN POWER SEED {match.group('index')}｜{power_label}"
    parts = [title]
    for heading in _POWER_SECTION_HEADINGS:
        block = _section(candidate_text, heading)
        if not block:
            raise ValueError(f"missing power section: {heading}")
        if source_name:
            block = block.replace(source_name, "持有者")
        parts += ["", block]
    parts += [
        "",
        "## 新版 Power Seed 暂不回填的字段",
        "High-Tier Mutation / Legendary Power State / Future Legend Image 属于新版 schema；本轮为了冻结 v4 Power 变量，不用新模型补写，也不从 Biography 反推。",
    ]
    return "\n".join(parts).strip() + "\n"


def split_human_seed_authorities(human_seed: str) -> dict[str, str]:
    """Separate persistent Human Core, initial mutable state, and non-Canon audition metadata.

    Production Human Seeds use explicit top-level ``Initial State Seed`` and
    ``Audition Metadata`` blocks. Legacy experiment outputs used direct
    ``当前私人欲望`` / ``人物钩子`` headings, so the parser keeps a small fallback.
    """

    initial_block = _section(human_seed, "## Initial State Seed")
    audition_block = _section(human_seed, "## Audition Metadata（非 Canon）")
    current = _section(human_seed, "## 当前私人欲望") if not initial_block else ""
    hook = _section(human_seed, "## 人物钩子") if not audition_block else ""

    core = human_seed
    for block in (initial_block, audition_block, current, hook):
        if block:
            core = core.replace(block, "")
    core = re.sub(r"\n{3,}", "\n\n", core).strip() + "\n"

    if initial_block:
        body = initial_block[len("## Initial State Seed") :].strip()
        body = body.replace("### 当前私人欲望", "## current_desire", 1)
        initial = ("# INITIAL CHARACTER STATE\n\n" + body).strip() + "\n"
    elif current:
        initial = (
            "# INITIAL CHARACTER STATE\n\n"
            + current.replace("## 当前私人欲望", "## current_desire", 1)
        ).strip() + "\n"
    else:
        initial = "# INITIAL CHARACTER STATE\n\n## current_desire\n未初始化\n"

    if audition_block:
        body = audition_block[len("## Audition Metadata（非 Canon）") :].strip()
        body = body.replace("### 人物钩子", "## Character Hook Audition", 1)
        audition = ("# HUMAN AUDITION METADATA｜NON-CANON\n\n" + body).strip() + "\n"
    elif hook:
        audition = (
            "# HUMAN AUDITION METADATA｜NON-CANON\n\n"
            + hook.replace("## 人物钩子", "## Character Hook Audition", 1)
        ).strip() + "\n"
    else:
        audition = "# HUMAN AUDITION METADATA｜NON-CANON\n\n无\n"

    return {
        "human_core": core,
        "initial_state": initial,
        "audition_metadata": audition,
    }


def compose_character_card(*, power_seed: str, human_seed: str, index: int = 1) -> str:
    """Merge stable Power/Human cores without reconciliation.

    Mutable state and audition metadata are intentionally returned by
    :func:`split_human_seed_authorities` and stored separately by production storage.
    """

    human = split_human_seed_authorities(human_seed)
    return (
        f"# CHARACTER CARD {index}｜Split Authority\n\n"
        "## POWER CORE｜Frozen Authority\n\n"
        f"{power_seed.strip()}\n\n"
        "## HUMAN CORE｜Frozen Authority\n\n"
        f"{human['human_core'].strip()}\n\n"
        "## Composition Boundary\n"
        "Power Core 与 Human Core 原样并列。此处不解释为什么某段童年象征某种能力，不重写欲望去适配金手指，也不推演世界将怎样回应。"
        "Mutable Character State 与 non-Canon Audition 分文件保存，不进入本卡。发现、使用、关系化学反应与真正的故事碰撞留给后续 Collision Authority。\n"
    )
