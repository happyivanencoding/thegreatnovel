from __future__ import annotations

import random
import secrets


_POWER_FANTASIES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("学习 / 复制", "学会别人会的本事", ("只保留自己真正理解的部分", "每次只能留下一个版本", "只保留关键的一步", "用过一次后必须重新学")),
    ("并行 / 多线", "同时做原本不能同时做的事", ("两件事必须都由自己亲自控制", "只能并行两件互相冲突的动作", "其中一件失败时另一件仍可继续", "两条动作可以共享一次发力")),
    ("分身 / 化身", "让另一个自己替自己行动", ("分开时能独立学习，回来后经验回流", "每个分身只能带走一种本事", "分身死后只留下学到的东西", "分身和本体不能同时用同一种能力")),
    ("预知 / 预警", "提前知道接下来会发生什么", ("只提前看见一个危险瞬间", "只能看到自己下一次失败", "预见结果但看不见过程", "只有做出选择后才看到另一条可能")),
    ("移动 / 脱困", "去到别人很难抵达的位置", ("只能去自己亲眼见过的地方", "移动后会留下一个可被利用的旧位置", "只能穿过自己能理解的障碍", "每次移动只能改变一个方向")),
    ("恢复 / 保命", "把本来会失去的东西保下来", ("只能恢复最近一次损失", "身体恢复但伤痛记忆保留", "致命伤可延后一次而不是消失", "只能把一种损失转成另一种代价")),
    ("储存 / 释放", "把一次效果先留下，以后再用", ("一次只能存一种效果", "必须亲自承受后才能储存", "释放时只能复现原效果的一部分", "存得越久越难控制")),
    ("操控 / 驭使", "让兵器或造物像自己的身体一样行动", ("每个目标都需要独立注意力", "只能同时操控彼此性质不同的目标", "目标会记住上一次动作", "离得越远动作越简单")),
    ("借用 / 偷取", "暂时拿来别人最擅长的一件事", ("只能拿走对方此刻正在使用的部分", "借来后原主人仍然能用", "只能借到自己身体承受得住的程度", "每次只能借一种优势")),
    ("变身 / 适配", "临时变成更适合当前处境的状态", ("只能改变一个身体特征", "只能变成自己亲身接触过的状态", "变化结束后保留一点永久痕迹", "同一种变化第二次会更自然但更难撤销")),
    ("积累 / 成长", "把原本会消失的经验永久留下", ("只保留失败里真正学会的一点", "每次只能强化一个已经会的动作", "重复同一失败不会继续收益", "只有跨过原有极限时才会留下变化")),
    ("召唤 / 伴生", "让一个额外帮手长期参与自己的行动", ("帮手会独立学习但不完全听话", "帮手只能继承自己舍弃的一部分能力", "帮手受伤会把一种感觉传回本体", "帮手成长方向由共同经历决定")),
)


def build_power_novelty_bundle(seed: int | None = None) -> str:
    """Return three reproducible, plain-language Power novelty sparks.

    Sparks are non-Canon candidate-divergence inputs. They deliberately use familiar
    reader fantasies plus one simple deviation instead of abstract terminology.
    """

    actual_seed = secrets.randbits(32) if seed is None else int(seed)
    rng = random.Random(actual_seed)
    selected = rng.sample(_POWER_FANTASIES, k=3)
    lines = [
        "# POWER NOVELTY SPARK｜非 Canon",
        f"seed: {actual_seed}",
        "用途：只负责拉开 3 个 Power Candidate 的创意起点；不是能力答案，不得原样抄写。",
        "共同边界：每个候选最多一个主异常；先用大白话说清楚，再考虑世界内短名；专有名词不能替代理解。",
        "",
    ]
    for index, (label, desire, anomalies) in enumerate(selected, start=1):
        lines.extend(
            [
                f"## Candidate {index}",
                f"熟悉幻想：{desire}",
                f"单一异常：{rng.choice(anomalies)}",
                f"内部标签：{label}",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"
