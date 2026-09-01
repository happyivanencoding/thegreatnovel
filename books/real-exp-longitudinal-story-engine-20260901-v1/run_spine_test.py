from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"
OUT = ROOT / "books" / "real-exp-longitudinal-story-engine-20260901-v1" / "spine-100ch"
ACP = ROOT / "temps" / "acp_text_runner.py"
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.prompts import (
    LONGITUDINAL_THREAD_ADVANCE_DIRECTION,
    MAIN_WORLD_RETURN_CONSEQUENCE_DIRECTION,
    PERSISTENT_GLOBAL_PROGRESS_RULER_DIRECTION,
    PROTAGONIST_LIFE_ENGINE_DIRECTION,
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    prompt = f"""你是 TGN 的 Book-Level Longitudinal Spine 受控实验。这里只测试《我身藏诸界》从第40章已发生 Canon 出发，能否形成约60—120章尺度的整本牵引；你不是 World Expansion，也不是下一卷 Story Refresh。

这是 frozen-authority 实验，必须保护当前已验证的四层 Advantage Stack：双真、风髓双口、未尽续行、双影为邻。不得把任何一项替换成新能力，不得重新设计万门宫结局。

必须遵守以下 production 原则：

{LONGITUDINAL_THREAD_ADVANCE_DIRECTION}

{MAIN_WORLD_RETURN_CONSEQUENCE_DIRECTION}

{PERSISTENT_GLOBAL_PROGRESS_RULER_DIRECTION}

{PROTAGONIST_LIFE_ENGINE_DIRECTION}

本实验额外硬边界：
1. 只从下方已经发生的正文/Character/Story Program 提取 2—4 条真正够强的 Book-Level Spine；不要为了凑数发明线。
2. 每条 Spine 只写：`当前仍在问什么 → 下一次读者可见升级/变化的类型 → 当前仍必须未知什么 → 为什么它能跨多个 World Horizon 继续牵引`。
3. 不得设计第41章后的新世界、世界规则、人物、宝物、能力、具体未来章号或 Mystery 真相；未来 World Expansion 继续 protagonist-blind。
4. 可以让现有主世界人物/势力/物件在未来发生“哪一类变化”，但不能宣布尚未发生的具体事实已经成立。
5. 宁烬主力量尺当前是玄曜灵海4重；本地尺不能冒充全书进度。Meta Ruler 只允许输出 `Current Meta Capability + Next Observable Question`，不得列“第一阶/第二阶/第三阶”技能树，不得预授权带人、两界融合、定点传送等未来能力。
6. 人物生活根只能使用正文已存在的事实。特别可审查：宁家旁支、旧宅契、它曾是宁烬身上最后值钱的东西，以及他面对“只能拿一半”时明确出现过“凭什么？”；如果这些不足以形成可靠人物线，就明确说不足，不补父母惨死、家产被夺、背叛或其它旧历史。
7. 输出必须让未来每个 World Horizon 仍只具体规划自己的世界；Book-Level Spine 负责的是跨 Horizon 的问题压力，不是提前给未来副本派任务。

请输出：
# BOOK-LEVEL LONGITUDINAL SPINE TEST
## 总牵引判断
## Spine 1...（2—4条）
## Main-World Return Compounding
## Persistent Progress Coordinate
## Character Life Root
## Unknown Boundary / World Expansion Boundary
## Verdict（PASS / DIRECTIONAL PASS / PARTIAL PASS / FAIL，并明确理由）

=== FROZEN CHARACTER ===
{read(BOOK / 'CHARACTER.md')}

=== CHAPTER 1 EVIDENCE ===
{read(BOOK / 'chapters' / 'chapter-0001.md')}

=== CHAPTER 7 EVIDENCE ===
{read(BOOK / 'chapters' / 'chapter-0007.md')}

=== CURRENT BOOK STATE THROUGH CHAPTER 40 ===
{read(BOOK / 'BOOK_FINAL.md')}

=== CURRENT STORY PROGRAM THROUGH CHAPTER 40 ===
{read(BOOK / 'STORY_PROGRAM_FINAL.md')}
"""
    prompt_path = OUT / "prompt.md"
    response_path = OUT / "response.md"
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
    (OUT / "runner_stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (OUT / "runner_stderr.txt").write_text(proc.stderr, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    print(f"SPINE_READY {response_path.stat().st_size}")


if __name__ == "__main__":
    main()
