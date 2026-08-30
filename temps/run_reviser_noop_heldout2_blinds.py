from __future__ import annotations

import json
import random
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = (
    ROOT
    / "books"
    / "real-exp-reviser-noop-upstream-heldout-20260830-v1"
    / "heldout-new-novel-2"
)
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")


def clean(text: str) -> str:
    return re.sub(
        r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$",
        "",
        text,
    ).strip()


def call(prompt_path: Path, out_path: Path, model: str, label: str) -> dict:
    last = ""
    for attempt in range(3):
        try:
            proc = subprocess.run(
                [
                    "node",
                    str(RUNNER),
                    str(prompt_path),
                    str(out_path),
                    model,
                    "high",
                    str(ROOT),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=1200,
            )
        except subprocess.TimeoutExpired:
            last = f"timeout {label}"
            time.sleep(2 + attempt * 2)
            continue
        if proc.returncode == 0 and out_path.exists():
            data = json.loads(out_path.read_text(encoding="utf-8"))
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (proc.stderr + "\n" + proc.stdout)[-4000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(f"{label}: {last}")


def parse(raw: str) -> dict:
    text = clean(raw)
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError(text[:1200])
    return json.loads(match.group(0))


def authority_context(chapter: int) -> str:
    prompt = (
        BASE
        / "runs"
        / f"chapter-{chapter:04d}"
        / "control_reviser_prompt.md"
    ).read_text(encoding="utf-8")
    marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    if marker not in prompt:
        raise RuntimeError(f"missing Primary marker in chapter {chapter}")
    return prompt.split(marker, 1)[0].strip()


def candidates(run: str, chapter: int) -> dict[str, str]:
    directory = (
        BASE / "runs" / f"chapter-{chapter:04d}"
        if run == "repeat1"
        else BASE / "repeat2" / f"chapter-{chapter:04d}"
    )
    return {
        "control_primary": (directory / "control_primary_body.md")
        .read_text(encoding="utf-8")
        .strip(),
        "treatment_primary": (directory / "treatment_primary_body.md")
        .read_text(encoding="utf-8")
        .strip(),
        "control_reviser": (directory / "control_final_body.md")
        .read_text(encoding="utf-8")
        .strip(),
        "treatment_reviser": (directory / "treatment_final_body.md")
        .read_text(encoding="utf-8")
        .strip(),
    }


def one(blind_repeat: int, run: str, chapter: int, judge: str) -> dict:
    texts = candidates(run, chapter)
    names = list(texts)
    random.Random(
        f"heldout2:{blind_repeat}:{run}:{chapter}:{judge}"
    ).shuffle(names)
    letters = "ABCD"
    key = {letters[index]: names[index] for index in range(4)}
    candidate_text = "\n\n".join(
        f"# {letter}\n\n{texts[key[letter]]}" for letter in letters
    )

    if judge == "story":
        prompt = f"""你是 fresh-context 匿名成熟中文男频商业编辑。下面四个候选来自同一章、同一冻结上游；两个是 Primary，两个是 Full Authority Reviser Final，但你不知道对应关系。

只评普通男频读者最终阅读体验：续读欲、主角私人欲望与主动选择、冲突和动作清晰度、Power Fantasy、Reward / Public Proof / Surprise、关系、节奏、AI总结味、重复证明、程序/报告味、漂亮二段论。不要因更长、更短、更像修订稿而偏爱。

严格只输出 JSON：
{{"ranking":["A","B","C","D"],"scores":{{"A":0,"B":0,"C":0,"D":0}},"reason":"中文6-10句，必须指出真正决定排序的具体文本差异"}}

{candidate_text}
"""
        model = "gpt-5.6-terra"
    else:
        authority = authority_context(chapter)
        prompt = f"""你是 fresh-context 匿名 TGN Frozen Authority 审计员。下面四个候选来自同一章同一冻结 Authority。

只比较 actor/action/object、Direct Result、State Change、Ending、money/ownership、Power Permanent Boundary、relationship、Reader Release、unknown 与跨章 timing，不评文笔。只有具体 Hard conflict、required missing、未授权旧史/数字/结果才扣分；激进、爽、群众反应强本身不是错。

严格只输出 JSON：
{{"ranking":["A","B","C","D"],"scores":{{"A":0,"B":0,"C":0,"D":0}},"hard_problems":{{"A":[],"B":[],"C":[],"D":[]}},"reason":"中文6-10句，必须指出具体事实边界"}}

# FROZEN AUTHORITY
{authority}

{candidate_text}
"""
        model = "gpt-5.6-luna"

    out = BASE / f"blind-final-facts-{blind_repeat}" / run / f"chapter-{chapter:04d}"
    out.mkdir(parents=True, exist_ok=True)
    prompt_path = out / f"{judge}_prompt.md"
    acp_path = out / f"{judge}_acp.json"
    response_path = out / f"{judge}_response.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(
        prompt_path,
        acp_path,
        model,
        f"{blind_repeat}-{run}-{chapter}-{judge}",
    )
    raw = str(data.get("text", ""))
    response_path.write_text(raw.strip() + "\n", encoding="utf-8")
    value = parse(raw)
    ranking = [key[item] for item in value["ranking"]]
    scores = {key[item]: float(score) for item, score in value["scores"].items()}
    hard_problems = (
        {key[item]: problems for item, problems in value.get("hard_problems", {}).items()}
        if judge == "authority"
        else {}
    )
    return {
        "blind_repeat": blind_repeat,
        "run": run,
        "chapter": chapter,
        "judge": judge,
        "ranking": ranking,
        "scores": scores,
        "hard_problems": hard_problems,
        "reason": value.get("reason", ""),
        "blind_key": key,
        "wall_seconds": float(data.get("wall_seconds") or 0),
    }


def main() -> None:
    if not (BASE / "repeat2" / "summary.json").exists():
        raise RuntimeError("repeat2 not complete")
    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [
            executor.submit(one, blind_repeat, run, chapter, judge)
            for blind_repeat in (1, 2)
            for run in ("repeat1", "repeat2")
            for chapter in range(1, 5)
            for judge in ("story", "authority")
        ]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(
                row["blind_repeat"],
                row["run"],
                row["chapter"],
                row["judge"],
                row["ranking"][0],
                flush=True,
            )
    rows.sort(
        key=lambda item: (
            item["blind_repeat"],
            item["run"],
            item["chapter"],
            item["judge"],
        )
    )
    aggregates: dict[str, dict] = {}
    names = (
        "control_primary",
        "treatment_primary",
        "control_reviser",
        "treatment_reviser",
    )
    for judge in ("story", "authority"):
        group = [row for row in rows if row["judge"] == judge]
        aggregates[judge] = {}
        for name in names:
            aggregates[judge][name] = {
                "mean_score": round(
                    sum(row["scores"][name] for row in group) / len(group),
                    3,
                ),
                "first_place": sum(row["ranking"][0] == name for row in group),
                "mean_rank": round(
                    sum(row["ranking"].index(name) + 1 for row in group)
                    / len(group),
                    3,
                ),
                "hard_problems": sum(
                    len(row["hard_problems"].get(name, [])) for row in group
                ),
            }
    result = {
        "schema_version": "heldout2-final-facts-fourway-blind-v1",
        "judge_rows": len(rows),
        "aggregates": aggregates,
        "rows": rows,
    }
    (BASE / "BLIND_SUMMARY.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(aggregates, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
