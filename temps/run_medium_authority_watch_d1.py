from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "books" / "real-exp-medium-authority-watch-20260830-v1"
SOURCE = Path(r"C:\dev\tgn-story-mvp-reviser-noop-20260830\books\real-exp-reviser-noop-upstream-heldout-20260830-v1\heldout-new-novel-2")
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
PROTOCOL_HASH = "B468C950DBD9B667F011DFBD18D8A6B4BE9350F029776A57DEDE7F16A982A69E"


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def exact_line(text: str, label: str) -> str:
    m = re.search(rf"(?m)^{re.escape(label)}：\s*(.+)$", text)
    if not m:
        raise RuntimeError(f"missing line {label}")
    return f"{label}：{m.group(1).strip()}"


def section(text: str, heading_pattern: str, next_level: str) -> str:
    m = re.search(
        rf"(?ms)^{heading_pattern}\s*$\n(.*?)(?=^{next_level} |\Z)",
        text,
    )
    return m.group(1).strip() if m else ""


def compile_watch(prompt: str) -> str:
    mission = [
        exact_line(prompt, "主角行动"),
        exact_line(prompt, "直接结果"),
        exact_line(prompt, "状态变化"),
        exact_line(prompt, "结尾推动力"),
    ]
    reader = section(
        prompt,
        r"## READER RELEASE｜本章已批准首次释放事实；逐条核对",
        r"##",
    )
    if "没有排程 Reader Release" in reader or "（本章没有排程 Reader Release。）" in reader:
        reader = "NONE"
    curator = section(prompt, r"# Curator Audit", r"#")
    if not curator:
        curator = "NONE"
    permanent = section(prompt, r"### 永久边界", r"###")
    if not permanent:
        permanent = "NONE"
    return "\n".join([
        "## MEDIUM AUTHORITY WATCH D1｜Runtime deterministic; no new story facts",
        "只做最后一次局部 Authority 扫尾；正确正文保持不动。",
        *mission,
        f"Reader Release：{reader}",
        f"Curator Audit Boundary：{curator}",
        f"Permanent Power Boundary：{permanent}",
        "No-Invention Boundary：Authority 未明确给出的伤势、数字、物品来源/持有关系、旧史、他人内心/认知或新能力，一律保持未知；不要为了连贯补事实。",
    ])


def call(prompt_path: Path, out_path: Path, label: str) -> dict:
    last = ""
    for attempt in range(3):
        try:
            p = subprocess.run(
                ["node", str(RUNNER), str(prompt_path), str(out_path), "gpt-5.6-luna", "medium", str(ROOT)],
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
        if p.returncode == 0 and out_path.exists():
            data = json.loads(out_path.read_text(encoding="utf-8"))
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (p.stderr + "\n" + p.stdout)[-4000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(f"{label}: {last}")


def body(raw: str) -> str:
    raw = clean(raw)
    return raw.rsplit("# 正式正文", 1)[-1].strip() if "# 正式正文" in raw else raw


def source_dir(run: str, chapter: int) -> Path:
    return SOURCE / ("runs" if run == "repeat1" else "repeat2") / f"chapter-{chapter:04d}"


def one(run: str, chapter: int) -> dict:
    src = source_dir(run, chapter)
    prompt = (src / "treatment_reviser_prompt.md").read_text(encoding="utf-8")
    watch = compile_watch(prompt)
    out = EXP / "derivation-heldout2" / run / f"chapter-{chapter:04d}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "watch.md").write_text(watch + "\n", encoding="utf-8")
    treatment = prompt.rstrip() + "\n\n" + watch + "\n"
    pp = out / "medium_watch_prompt.md"
    ap = out / "medium_watch_acp.json"
    rp = out / "medium_watch_response.md"
    fp = out / "medium_watch_final_body.md"
    pp.write_text(treatment, encoding="utf-8")
    data = call(pp, ap, f"{run}-{chapter}")
    raw = str(data.get("text", ""))
    rp.write_text(raw.strip() + "\n", encoding="utf-8")
    final = body(raw)
    fp.write_text(final + "\n", encoding="utf-8")
    high = json.loads((src / "treatment_reviser_acp.json").read_text(encoding="utf-8"))
    base_medium = json.loads((SOURCE / "medium-reviser-screen" / run / f"chapter-{chapter:04d}" / "medium_reviser_acp.json").read_text(encoding="utf-8"))
    return {
        "run": run,
        "chapter": chapter,
        "watch_chars": len(watch),
        "medium_watch_wall": float(data.get("wall_seconds") or 0),
        "medium_base_wall": float(base_medium.get("wall_seconds") or 0),
        "high_wall": float(high.get("wall_seconds") or 0),
    }


def main() -> None:
    actual = hashlib.sha256((EXP / "PROTOCOL_DERIVATION_D1.md").read_bytes()).hexdigest().upper()
    if actual != PROTOCOL_HASH:
        raise RuntimeError(f"D1 protocol changed after freeze: {actual}")
    rows = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(one, run, ch) for run in ("repeat1", "repeat2") for ch in range(1, 5)]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(row, flush=True)
    rows.sort(key=lambda x: (x["run"], x["chapter"]))
    n = len(rows)
    summary = {
        "schema_version": "medium-authority-watch-d1-derivation-v1",
        "protocol_sha256": PROTOCOL_HASH,
        "rows": rows,
        "mean_watch_chars": round(sum(x["watch_chars"] for x in rows) / n, 3),
        "mean_medium_watch_wall": round(sum(x["medium_watch_wall"] for x in rows) / n, 3),
        "mean_medium_base_wall": round(sum(x["medium_base_wall"] for x in rows) / n, 3),
        "mean_high_wall": round(sum(x["high_wall"] for x in rows) / n, 3),
    }
    (EXP / "DERIVATION_D1_TIMING.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
