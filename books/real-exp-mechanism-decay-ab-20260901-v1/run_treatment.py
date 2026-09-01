from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"
OUT = ROOT / "books" / "real-exp-mechanism-decay-ab-20260901-v1"
ACP = ROOT / "temps" / "acp_text_runner.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    baseline = read(BOOK / "chapters" / "chapter-0039.md") + "\n\n" + read(BOOK / "chapters" / "chapter-0040.md")
    (OUT / "BASELINE_CH39_40.md").write_text(baseline, encoding="utf-8")
    prompt = f"""你是 TGN 当前 Primary prose 的 frozen-story A/B Treatment。只重写下面《我身藏诸界》第39—40章的表达，不重新设计故事。

唯一实验变量：Mechanism Explanation Decay / Trust the Reader。

硬要求：
- 所有人物、地点、顺序、选择、胜负、伤势、奖励、回归、天外商会天舟结尾全部保持。
- 四层 Advantage Stack 事实与边界保持：双真；风髓双口只导引风/热/液压等流动力量，不传人或固体、不增加元力；未尽续行只接续宁烬已经真正开始的具体动作；双影为邻只连接宁烬两具真身自己的两道真实影子。
- 第39章仍必须让读者清楚看见：右边真身开始转门后被撞离，左边真身经相邻真影把同一记转门接住；这不是新传送。
- 第40章仍必须让读者清楚看见：赤潮灼风/气压经风髓双口被导向另一端，帮助门框越过最沉段；未尽续行让被打断的转门继续；双影为邻补足两边影路；最终第八接点稳定连接共影棚与赤潮码头。
- 不删阮七娘/许渡重逢，不删贺燃灯斩旗，不删宿无眼退场，不删其它路线真实后果，不删奖励与黑门回玄曜，不删结尾天舟发现黑门。
- 不新增任何新能力、新解释、新人物、新奖励或 Mystery 答案。

Treatment 写法：
1. 第39章机制第一次转入“未尽续行 × 双影为邻”时，保留一次最短必要理解；之后靠动作连续性，不再用“动作没有归零 / 同一记转门落到另一具身体”反复讲同一结论。
2. 第40章开头风髓双口已经是旧能力，直接让风与气压产生结果；除非读者会误以为门框被传送，否则不要重新列完整边界。
3. 最终复合高潮不要在落门前写 `A+B+C=D` 的说明句。先让门真正落稳、关系结果出现；若必须确认复合，只能在结果后用一小句回望，不能列公式。
4. 章名改成画面/争夺/关系结果，不用“被打断的转门”这类后台公式标题。
5. 保持商业男频可读性和速度；不是极简文，不删除必要空间因果、动作方向、危险与人物反应。
6. 禁止为了缩短而把高潮改写成梗概。

输出只包含 Treatment 第39章与第40章完整正文。

=== FROZEN STORY PROGRAM 31—40 ===
{read(BOOK / 'STORY_PROGRAM_31_40.md')}

=== BASELINE CH39—40 ===
{baseline}
"""
    prompt_path = OUT / "prompt.md"
    response_path = OUT / "TREATMENT_CH39_40.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    cmd = [
        sys.executable,
        str(ACP),
        "--model", "gpt-5.6-terra",
        "--effort", "high",
        "--prompt-file", str(prompt_path),
        "--output", str(response_path),
        "--timeout", "9000",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=9300)
    (OUT / "runner_stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (OUT / "runner_stderr.txt").write_text(proc.stderr, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    print(f"MECH_DECAY_READY {response_path.stat().st_size}")


if __name__ == "__main__":
    main()
