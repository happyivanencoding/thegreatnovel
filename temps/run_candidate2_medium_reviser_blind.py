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
SCREEN = BASE / "medium-reviser-screen"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def call(prompt_path: Path, out_path: Path, model: str, label: str) -> dict:
    last = ""
    for attempt in range(3):
        try:
            proc = subprocess.run(
                ["node", str(RUNNER), str(prompt_path), str(out_path), model, "high", str(ROOT)],
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
    match = re.search(r"\{.*\}", clean(raw), re.S)
    if not match:
        raise ValueError(raw[:1000])
    return json.loads(match.group(0))


def source_dir(run: str, chapter: int) -> Path:
    return (
        BASE / "runs" / f"chapter-{chapter:04d}"
        if run == "repeat1"
        else BASE / "repeat2" / f"chapter-{chapter:04d}"
    )


def authority(chapter: int) -> str:
    prompt = (BASE / "runs" / f"chapter-{chapter:04d}" / "control_reviser_prompt.md").read_text(encoding="utf-8")
    marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    return prompt.split(marker, 1)[0].strip()


def one(run: str, chapter: int, judge: str) -> dict:
    src = source_dir(run, chapter)
    medium = SCREEN / run / f"chapter-{chapter:04d}" / "medium_final_body.md"
    texts = {
        "primary": (src / "treatment_primary_body.md").read_text(encoding="utf-8").strip(),
        "medium": medium.read_text(encoding="utf-8").strip(),
        "high": (src / "treatment_final_body.md").read_text(encoding="utf-8").strip(),
    }
    names = list(texts)
    random.Random(f"candidate2-medium:{run}:{chapter}:{judge}").shuffle(names)
    letters = "ABC"
    key = {letters[index]: names[index] for index in range(3)}
    candidates = "\n\n".join(f"# {letter}\n\n{texts[key[letter]]}" for letter in letters)
    if judge == "story":
        prompt = f"""你是 fresh-context 匿名成熟中文男频商业编辑。A/B/C来自同一冻结上游：一个是Treatment Primary，一个经Luna medium Reviser，一个经Luna high Reviser，但你不知道对应关系。只评最终读者体验：续读欲、主动选择、动作、Power Fantasy、Reward、关系、节奏、AI总结味。不要因更长或更像修订稿偏爱。

严格只输出JSON：{{"ranking":["A","B","C"],"scores":{{"A":0,"B":0,"C":0}},"reason":"中文5-8句具体比较"}}

{candidates}
"""
        model = "gpt-5.6-terra"
    else:
        prompt = f"""你是 fresh-context 匿名TGN Frozen Authority审计员。A/B/C来自同一冻结Authority：一个是Treatment Primary，一个经Luna medium Reviser，一个经Luna high Reviser，但你不知道对应关系。只比较actor/action/object、Direct Result、State Change、Ending、money/ownership、Power boundary、relationship、Reader Release、unknown、timing；不评文笔。只有具体Hard conflict、required missing、未授权旧史/数字/结果才扣分。

严格只输出JSON：{{"ranking":["A","B","C"],"scores":{{"A":0,"B":0,"C":0}},"hard_problems":{{"A":[],"B":[],"C":[]}},"reason":"中文5-8句具体比较"}}

# AUTHORITY
{authority(chapter)}

{candidates}
"""
        model = "gpt-5.6-luna"
    out = SCREEN / "blind" / run / f"chapter-{chapter:04d}"
    out.mkdir(parents=True, exist_ok=True)
    pp = out / f"{judge}_prompt.md"
    ap = out / f"{judge}_acp.json"
    pp.write_text(prompt, encoding="utf-8")
    data = call(pp, ap, model, f"{run}-{chapter}-{judge}")
    value = parse(str(data.get("text", "")))
    ranking = [key[item] for item in value["ranking"]]
    scores = {key[item]: float(score) for item, score in value["scores"].items()}
    problems = {key[item]: ps for item, ps in value.get("hard_problems", {}).items()} if judge == "authority" else {}
    return {"run": run, "chapter": chapter, "judge": judge, "ranking": ranking, "scores": scores, "hard_problems": problems, "reason": value.get("reason", "")}


def main() -> None:
    if not (SCREEN / "summary.json").exists():
        raise RuntimeError("medium screen generation not complete")
    rows = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(one, run, chapter, judge) for run in ("repeat1", "repeat2") for chapter in range(1, 5) for judge in ("story", "authority")]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(row["run"], row["chapter"], row["judge"], row["ranking"][0], flush=True)
    rows.sort(key=lambda item: (item["run"], item["chapter"], item["judge"]))
    aggregates = {}
    for judge in ("story", "authority"):
        group = [row for row in rows if row["judge"] == judge]
        aggregates[judge] = {}
        for name in ("primary", "medium", "high"):
            aggregates[judge][name] = {
                "mean_score": round(sum(row["scores"][name] for row in group) / len(group), 3),
                "first_place": sum(row["ranking"][0] == name for row in group),
                "hard_problems": sum(len(row["hard_problems"].get(name, [])) for row in group),
            }
    result = {"schema_version": "candidate2-medium-reviser-blind-v1", "aggregates": aggregates, "rows": rows}
    (SCREEN / "BLIND_SUMMARY.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(aggregates, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
