from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"
OUT = ROOT / "books" / "real-exp-bone-world-surgery-20260901-v1"
ACP = ROOT / "temps" / "acp_text_runner.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def chapters(start: int, end: int) -> str:
    parts: list[str] = []
    for n in range(start, end + 1):
        parts.append(read(BOOK / "chapters" / f"chapter-{n:04d}.md"))
    return "\n\n".join(parts)


def run(prompt: str, output: Path, stdout: Path, stderr: Path) -> None:
    prompt_path = output.with_suffix(".prompt.md")
    prompt_path.write_text(prompt, encoding="utf-8")
    cmd = [
        sys.executable,
        str(ACP),
        "--model", "gpt-5.6-terra",
        "--effort", "high",
        "--prompt-file", str(prompt_path),
        "--output", str(output),
        "--timeout", "9000",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=9300)
    stdout.write_text(proc.stdout, encoding="utf-8")
    stderr.write_text(proc.stderr, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def common_rules() -> str:
    return """这是独立内容手术实验，不覆盖 production 旧书。你是在当前已经冻结的高价值事实内重写故事密度，不是在重新设计世界或能力。

必须保留：葬身骨陆、旧伤返生的身体幻想、返伤相、裂骨风、沉髓海/热髓、新生院、商妩、贺沉骨、宁烬真实失去四车逆月盐、灵海4重正常突破、风髓双口、商妩自己的新盐路与宁烬三成长期利润。风髓双口仍只导引风/热/液压等流动力量，不传人/固体、不增加元力。宁烬不能靠双真抹掉损失。贺沉骨必须真实赢过一次，商妩必须保有自己的欲望。

必须压缩：登记、验货、商籍/担保/骨票程序、盐价核算、连续押运/车辆/路线实施、城主府/商团围绕新路的多轮收费与治理讨论、已经成立后的重复能力说明。它们只有改变人物选择/代价时才留最短一笔。

骨陆首先是“伤口会重新长出东西”的身体幻想世界，不是物流创业篇。世界生活感要通过衣服、护甲、道路、交通、病人身体、返伤相等直接可见结果存在，不靠长制度说明。

正文机制解释遵守衰减：第一次讲清最短必要效果；第二次只补新边界/失败/组合；第三次以后优先动作→外界反应→结果。高潮不先列能力公式。

不得新增未来世界、未来能力、Mystery 真相、悲惨童年。宁烬的人格生活根如需触及，只能使用已经发生的事实：宁家旁支；旧宅契曾是他身上最后值钱的东西；他已经多次对别人替他规定“只能拿一半”出现抵触。不能说明旧宅为什么失去、父母发生什么、宁家是否亏欠他。
"""


def main() -> None:
    plan_path = OUT / "SURGERY_PLAN.md"
    if not plan_path.exists():
        raise SystemExit("SURGERY_PLAN.md missing")
    plan = read(plan_path)
    character = read(BOOK / "CHARACTER.md")
    story = read(BOOK / "STORY_PROGRAM_11_20.md")
    ch10 = read(BOOK / "chapters" / "chapter-0010.md")

    prompt_a = f"""你是 TGN 当前 Terra-high Batch Primary 的内容手术实验。按下方已批准 surgery plan，写完整第11—15章正文；一次保持五章小说连续认知窗口。

{common_rules()}

本批额外目标：
- 原第11—15章约 10363 个非空白字符；Treatment 目标约 7800—8500，不能靠梗概化达标。
- 第11章把三倍押运价/共同验看压成一个真正改变宁烬选择的短现场，尽快进入商妩与骨陆。
- 第12—15章把篇幅给裂骨风生活、贺沉骨封路压力、灵海4重与“商妩还是四车盐”的真实选择；文书、盐价、商团流程只留结果。
- 第15章必须真实失去四车逆月盐，商妩失去继承退路，不能随后立刻补等价奖励。
- 章名用读者画面/冲突/结果，不用后台机制标题。

只输出第11—15章完整正文，不写说明。

=== SURGERY PLAN ===
{plan}

=== FROZEN CHARACTER ===
{character}

=== CHAPTER 10 CONTINUITY ===
{ch10}

=== ORIGINAL 11—20 STORY AUTHORITY ===
{story}

=== BASELINE CHAPTER 11—15 ===
{chapters(11, 15)}
"""
    out_a = OUT / "TREATMENT_CH11_15.md"
    run(prompt_a, out_a, OUT / "prose_a_stdout.txt", OUT / "prose_a_stderr.txt")

    prompt_b = f"""你是 TGN 当前 Terra-high Batch Primary 的内容手术实验。继续同一 Treatment，按下方已批准 surgery plan 与刚写完的第11—15章，写完整第16—20章正文；保持第二个五章小说连续认知窗口。

{common_rules()}

本批额外目标：
- 原第16—20章约 12965 个非空白字符；Treatment 目标约 8300—9000。第16—18章完成骨陆，19—20章把原本会被盐路治理/算账占据的空间交给主世界长期因果。
- 第16—18章重点是新生院/返伤相/宁烬拒绝安全封伤/裂骨风与热髓双端下注/风髓双口高潮；新路产权只用最短结果结账。
- 风髓双口必须通过同一道旧伤在两处真身真实承受不同环境长成，任一端失败都是真风险；不要改成奖励发放或知识传授。
- 第18章结束时商妩留在骨陆自己经营新路，宁烬保留三成长期利润；不写多轮收费治理。
- 第19—20章至少让两条已有跨 Horizon 长线产生新事实。优先使用 surgery plan 已选择的线；回归后的能力/资产/身份必须改变主世界现有价格、战术、关系、入口或 Mystery，而不是“能力还在→下一门”。
- 若使用裴照临，他仍是灵海9重、完整白昼心、raw ruler 明显高于宁烬；外界只能根据公开可观察结果换战术，不得知道风髓双口/余门的隐藏永久机制。
- 骨陆离场恢复 live baseline 已成立的回归连续性：黑门先回到玄曜赤褐山地；若第19—20章要让宁烬重新进入九环天都，必须用正常旅行/时间推进过去，不能把回归点静默改成天都，也不能让人物跨距瞬移。
- 若使用天外商会/商王，必须通过真实接触/目击/可靠消息重新估价，不能全知。可以改变即时报价、交易地位或以后怎样谈，但不要为了证明 Repricing 临时发明一个具名“天洲级宝物会”或新的资格体系。
- 若使用宁家/旧宅契，只能使用上方已成立事实；不要补家史，也不要默认宁烬已能进入、修缮或居住某栋具体旧宅。可以让他重新决定这张契卖不卖、押不押、还留不留，但房屋现状与宅契来源继续未知。它可以是低频人物重量，不要求硬升成家族主线。
- 第20章不能提前具体写无主兵荒原/万门宫的新规则、人物、奖励；下一个 World Horizon 仍未知。
- 章名用读者画面/冲突/结果，不用后台机制标题。

只输出第16—20章完整正文，不写说明。

=== SURGERY PLAN ===
{plan}

=== FROZEN CHARACTER ===
{character}

=== MAIN-WORLD CONTINUITY THROUGH CHAPTER 10 ===
{ch10}

=== ORIGINAL 11—20 STORY AUTHORITY ===
{story}

=== TREATMENT CHAPTER 11—15 (CURRENT CONTINUITY) ===
{read(out_a)}

=== BASELINE CHAPTER 16—20 ===
{chapters(16, 20)}
"""
    out_b = OUT / "TREATMENT_CH16_20.md"
    run(prompt_b, out_b, OUT / "prose_b_stdout.txt", OUT / "prose_b_stderr.txt")

    combined = read(out_a).rstrip() + "\n\n" + read(out_b).lstrip()
    (OUT / "TREATMENT_CH11_20.md").write_text(combined, encoding="utf-8")
    print(f"BONE_PROSE_READY {len(combined)}")


if __name__ == "__main__":
    main()
