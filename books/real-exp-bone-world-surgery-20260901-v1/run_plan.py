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


def main() -> None:
    prompt = f"""你是 TGN 的《我身藏诸界》11—20章内容手术规划器。这里只做一个独立实验分支，不覆盖 production 旧书。

目标不是改变葬身骨陆，而是解决该段“Supporting Logic 抢成 Story Engine”的篇幅失衡。当前最终正文约 7.5 万 UTF-8 bytes；Treatment 正文目标约缩短 25—30%，允许把骨陆本体压到约 7—8 章的密度，并把省出的篇幅给主世界长期故事。

必须保护的高价值事实/幻想：
- 葬身骨陆与巨尸生活感；旧伤会在返伤相重新生长新身体结构；衣服/护甲/交通/医疗因此改变。
- 痕生、返伤相、裂骨风、巨尸旧创、新生院；Local ruler 与玄曜主尺分离。
- 商妩、贺沉骨都保留自己的欲望与行动，不成为主角附庸。
- 宁烬在北肋岔真实选择商妩而放掉四车逆月盐，损失大半预期利润；错失必须保留。
- 宁烬真实突破玄曜灵海4重；不能把本地事件等同为额外玄曜升级。
- 风髓双口的核心取得与边界不变：两具真身分别承受裂骨风与热髓，旧伤痕生为两个活口，只导引风/热/液压等流动力量，不传人/固体，不增加元力；这条永久可能性必须保留。
- 商妩最终保有一条继续自行经营的新盐路，宁烬保有三成长期利润；盐路只需作为关系/资产后果，不再承担连续物流正文。
- 宁烬仍通过黑门骨回玄曜；下一具体世界仍未知，不提前写无主兵荒原或万门宫细节。

必须大幅压缩或改成结果级因果的内容：
- 外来者登记、反复验货、商籍/担保/骨票程序；
- 盐价核算、连续押运/车辆/路线实施；
- 城主府/商团围绕新路的多轮秩序与收费争论；
- 已经成立后继续解释“逆月盐只能...”“风髓双口不能...”等规则。
这些信息只有在改变人物选择/代价时才留一笔。

Treatment 结构要求：
1. 优先让第11—18章完成骨陆本体（允许你判断 7 或 8 章更自然），第19—20章用于“回玄曜后的真实后果”；不要为了凑10章拉长骨陆。
2. 回归后的两章至少让两条已有长线产生新事实，优先从：裴照临/白昼心、天外商会/商王、宁家/旧宅契、黑门骨 Mystery、主世界社会估价中选择。不得只“再次提到”。
3. 宁家/旧宅契如果进入，只能使用已经发生的事实：宁烬是宁家旁支；旧宅契曾是他身上最后值钱的东西；他现在已经拥有三十万灵玉等现实财富。不得补父母惨死、家产被夺、背叛或旧宅来源真相。可以让“曾经最后值钱的东西现在经济上已经微不足道，但宁烬如何处置它”形成一个新的可见选择。
4. 裴照临仍远强于宁烬；如果他/其势力因风髓双口改变策略，只能基于公开可观察结果，不得知道余门、永久性或内部触发。
5. 天外商会/商王若重新估价，必须由真实接触/见证/可靠消息成立；不要凭空全知。
6. 回归不要求打脸；重点是上一世界获得改变主世界价格、战术、关系、入口或 Mystery。
7. 章节标题不要用后台机制公式。
8. Treatment 要能接回长篇，而不是把主世界后果写成两章结算报告。

请先只输出 `SURGERY_PLAN.md`，不要写正文。每章写：核心场面 / 保留的世界幻想 / 人物选择 / 直接结果 / 删掉或压缩的旧内容 / 向下一章的因果。最后给出预计篇幅分配，并明确哪两条以上跨 Horizon 长线产生了什么新事实。

=== FROZEN CHARACTER ===
{read(BOOK / 'CHARACTER.md')}

=== CHAPTER 10 PREVIOUS CONTINUITY ===
{read(BOOK / 'chapters' / 'chapter-0010.md')}

=== BASELINE STORY PROGRAM 11—20 ===
{read(BOOK / 'STORY_PROGRAM_11_20.md')}

=== BASELINE FINAL PROSE 11—20 ===
{read(OUT / 'BASELINE_CH11_20.md')}
"""
    prompt_path = OUT / "plan_prompt.md"
    response_path = OUT / "SURGERY_PLAN.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    cmd = [
        sys.executable,
        str(ACP),
        "--model", "gpt-5.6-sol",
        "--effort", "high",
        "--prompt-file", str(prompt_path),
        "--output", str(response_path),
        "--timeout", "9000",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=9300)
    (OUT / "plan_runner_stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (OUT / "plan_runner_stderr.txt").write_text(proc.stderr, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    print(f"BONE_PLAN_READY {response_path.stat().st_size}")


if __name__ == "__main__":
    main()
