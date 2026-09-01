from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / r"books\real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"
OUT = ROOT / r"books\real-exp-book-engine-mutation-ab-20260901-v1\steward-smoke"
ACP = ROOT / r"temps\acp_text_runner.py"
ACTIVE = Path(r"C:\Users\jingx\.agentdock\skill-store\installed\tgn-system-steward\0.3.40")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    prompt = f"""这是 bounded read-only TGN System Steward smoke。只审《我身藏诸界》原版 STORY_PROGRAM_21_30.md，不改文件，不重设计世界。

严格使用下方 active tgn-system-steward 0.3.40 与 quality lens。回答：
1. 这里的 World Engine 与 Book Engine 各自是否成立？不要因为新世界好看就把整本牵引判 PASS。
2. 用 Local Closure / Book State Mutation 区分：本段哪些只是 local story / Canon retained，哪些真正改变整本书后续行动条件？
3. 旧人物/旧资产/长期 Mystery 没在本 Horizon 进前景时，是否应该强制召回？若不该，什么才算真实推进？
4. 宁烬的 Behavior Signature 是否已经自动等于人物张力？怎样判断 Decision Vector 是否真的被 incompatible values 激活？禁止倒推创伤。
5. Chapter 20 回归主世界若只确认能力再开下一门，应如何判；Main-World Return Consequence 与一般 Book Mutation 谁更具体？
6. 最早根因层级与最小修法；明确不新增 Thread DB、Relationship Portfolio、Reviewer、Scorer、回访税。
7. 给 PASS / DIRECTIONAL PASS / PARTIAL PASS / FAIL。

已知审计目标里存在不少“某人仍在做某事 / 某收益仍存在”的保留信息。不要把 retained name 自动当 Plot advancing；也不要反向要求每 Horizon 固定推进 1—3 条旧线。对的地方就说对。

=== ACTIVE SKILL ===
{read(ACTIVE / 'SKILL.md')}

=== QUALITY LENS ===
{read(ACTIVE / 'references' / 'novel-quality-lens.md')}

=== AUDIT TARGET ===
{read(BOOK / 'STORY_PROGRAM_21_30.md')}
"""
    prompt_path = OUT / "prompt.md"
    response_path = OUT / "response.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(ACP), "--model", "gpt-5.6-luna", "--effort", "high", "--prompt-file", str(prompt_path), "--output", str(response_path), "--timeout", "9000"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=9300,
    )
    (OUT / "runner_stdout.txt").write_text(proc.stdout, encoding="utf-8")
    (OUT / "runner_stderr.txt").write_text(proc.stderr, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    print(f"STEWARD_SMOKE_READY {response_path.stat().st_size}")


if __name__ == "__main__":
    main()
