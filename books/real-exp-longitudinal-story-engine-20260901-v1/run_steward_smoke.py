from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"
OUT = ROOT / "books" / "real-exp-longitudinal-story-engine-20260901-v1" / "steward-smoke"
ACP = ROOT / "temps" / "acp_text_runner.py"
ACTIVE_SKILL = Path(r"C:\Users\jingx\.agentdock\skill-store\installed\tgn-system-steward\0.3.39")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    prompt = f"""下面是一个 bounded read-only TGN system audit smoke。严格按给出的当前已激活 tgn-system-steward v0.3.39 与 novel-quality-lens 工作；不要改文件，不要提出大重构。

审计对象只有《我身藏诸界》原版 STORY_PROGRAM_21_30.md。请回答：
1. 跨 Horizon 长线在这一段是“真实推进”还是只“被记住/继续存在”？用文件里的具体句子举证。
2. 最早根因层级是什么：State、Story Program / Story Refresh、Outline、Writer，还是别的？只选真实最早层。
3. Chapter 20 回归后的长篇后果是否足够，若不足属于什么失败。
4. 最小 production 修法是什么；明确哪些东西不该新增。
5. 给出 PASS / DIRECTIONAL PASS / PARTIAL PASS / FAIL。

不要因为用户想修长篇就强行找问题；如果这里实际正确就说正确。不要把 State 的记忆职责误判成主线调度，也不要仅凭“人物名字仍在 Canon”就算推进。

=== ACTIVE SKILL ===
{read(ACTIVE_SKILL / 'SKILL.md')}

=== ACTIVE QUALITY LENS ===
{read(ACTIVE_SKILL / 'references' / 'novel-quality-lens.md')}

=== AUDIT TARGET ===
{read(BOOK / 'STORY_PROGRAM_21_30.md')}
"""
    prompt_path = OUT / "prompt.md"
    response_path = OUT / "response.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    cmd = [
        sys.executable,
        str(ACP),
        "--model", "gpt-5.6-luna",
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
    print(f"STEWARD_SMOKE_READY {response_path.stat().st_size}")


if __name__ == "__main__":
    main()
