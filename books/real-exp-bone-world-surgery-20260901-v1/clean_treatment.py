from __future__ import annotations

from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
EXP = ROOT / "books" / "real-exp-bone-world-surgery-20260901-v1"
BOOK = ROOT / "books" / "real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"

src = EXP / "TREATMENT_CH11_20.md"
dst = EXP / "TREATMENT_CH11_20_CLEAN.md"
text = src.read_text(encoding="utf-8")

text = text.replace(
    "我会依据小说正文实现规范，把冻结事实压进连续的五章叙事，只在最终交付第11—15章正文。",
    "",
    1,
)

old_deed = """傍晚，宁烬回到临时落脚的客栈，桌上放着一张旧宅契。

是有人托商会送来的。

契纸边角已经发黄，上面仍是宁家的旧印。有人开了价，愿意立刻买走；也有人愿意替他押下契纸，换一笔更大的灵玉。

宁烬坐了很久。

这张契，曾经是他身上最后值钱的东西。

如今三十万灵玉、赤曜灯芯、赤鳞云驹，连骨陆那条盐路的三成都挂在他名下。按理说，这张不知道落在哪儿、也不知道还能不能开门的旧契，早该卖了。

可他想起那些人替商妩决定盐该怎么卖，替肋廊的人决定路该不该封，也想起北肋岔里商妩要把自己折进四车盐时说的那句放手。

宁烬将契纸折起，收进储物戒。

“不卖。”

门外没有人答话。"""
new_deed = """傍晚，宁烬回到临时落脚的客栈，取出那张旧宅契。

这张契，曾经是他身上最后值钱的东西。

如今三十万灵玉、赤曜灯芯、赤鳞云驹都已经到了手里，骨陆那条盐路也还留着他的三成。它早已不是他非卖不可才能活下去的东西。

宁烬看了很久，还是把契纸折好，重新收回储物戒。

“不卖。”"""
if text.count(old_deed) != 1:
    raise SystemExit(f"old-deed block count={text.count(old_deed)}")
text = text.replace(old_deed, new_deed, 1)

for old, new in (
    ("骨陆的路已经开始赚钱。", "骨陆那条路还在继续走。"),
    ("他只是按住肋下两处仍在发疼的骨口，望着天都外渐沉的夜色。", "他只是按住两具真身肋下仍在发疼的骨口，望着天都外渐沉的夜色。"),
):
    if text.count(old) != 1:
        raise SystemExit(f"expected exactly one cleanup target: {old!r}, count={text.count(old)}")
    text = text.replace(old, new, 1)

dst.write_text(text, encoding="utf-8")

baseline = "\n\n".join(
    (BOOK / "chapters" / f"chapter-{n:04d}.md").read_text(encoding="utf-8")
    for n in range(11, 21)
)

def metrics(value: str) -> tuple[int, int]:
    return len(value.encode("utf-8")), sum(not c.isspace() for c in value)

for name, value in (("LiveBaseline", baseline), ("TreatmentClean", text)):
    b, non_ws = metrics(value)
    print(f"{name}\tbytes={b}\tnonws={non_ws}")
