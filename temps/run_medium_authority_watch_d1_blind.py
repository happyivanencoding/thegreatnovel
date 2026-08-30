from __future__ import annotations

import json
import random
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "books" / "real-exp-medium-authority-watch-20260830-v1"
SOURCE = Path(r"C:\dev\tgn-story-mvp-reviser-noop-20260830\books\real-exp-reviser-noop-upstream-heldout-20260830-v1\heldout-new-novel-2")
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def call(prompt_path: Path, out_path: Path, model: str, label: str) -> dict:
    last = ""
    for attempt in range(3):
        try:
            p = subprocess.run(
                ["node", str(RUNNER), str(prompt_path), str(out_path), model, "high", str(ROOT)],
                cwd=ROOT, text=True, capture_output=True, encoding="utf-8", errors="replace", timeout=1200,
            )
        except subprocess.TimeoutExpired:
            last = f"timeout {label}"; time.sleep(2 + attempt * 2); continue
        if p.returncode == 0 and out_path.exists():
            data = json.loads(out_path.read_text(encoding="utf-8"))
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (p.stderr + "\n" + p.stdout)[-4000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(f"{label}: {last}")


def parse(raw: str) -> dict:
    m = re.search(r"\{.*\}", clean(raw), re.S)
    if not m:
        raise ValueError(raw[:1000])
    return json.loads(m.group(0))


def source_dir(run: str, chapter: int) -> Path:
    return SOURCE / ("runs" if run == "repeat1" else "repeat2") / f"chapter-{chapter:04d}"


def authority(chapter: int) -> str:
    prompt = (SOURCE / "runs" / f"chapter-{chapter:04d}" / "treatment_reviser_prompt.md").read_text(encoding="utf-8")
    marker = "## PRIMARY DRAFT｜唯一待修订正文底稿"
    return prompt.split(marker, 1)[0].strip()


def candidates(run: str, chapter: int) -> dict[str, str]:
    src = source_dir(run, chapter)
    medium = SOURCE / "medium-reviser-screen" / run / f"chapter-{chapter:04d}" / "medium_final_body.md"
    watch = EXP / "derivation-heldout2" / run / f"chapter-{chapter:04d}" / "medium_watch_final_body.md"
    return {
        "medium_base": medium.read_text(encoding="utf-8").strip(),
        "medium_watch": watch.read_text(encoding="utf-8").strip(),
        "high": (src / "treatment_final_body.md").read_text(encoding="utf-8").strip(),
    }


def one(run: str, chapter: int, judge: str) -> dict:
    texts = candidates(run, chapter)
    names = list(texts)
    random.Random(f"d1:{run}:{chapter}:{judge}").shuffle(names)
    letters = "ABC"
    key = {letters[i]: names[i] for i in range(3)}
    cand = "\n\n".join(f"# {letter}\n\n{texts[key[letter]]}" for letter in letters)
    if judge == "story":
        prompt = f"""你是 fresh-context 匿名成熟中文男频商业编辑。A/B/C来自同一冻结Primary：一个是Luna-medium基础Reviser，一个是Luna-medium加极短Authority Watch，一个是Luna-high Reviser，但你不知道对应关系。只评最终读者体验：续读欲、主角主动性与私人欲望、动作/冲突、Power Fantasy、Reward/Public Proof、关系、节奏、AI总结/报告味。不要因更长或更像修订稿偏爱。

严格只输出JSON：{{"ranking":["A","B","C"],"scores":{{"A":0,"B":0,"C":0}},"reason":"中文5-8句具体比较"}}

{cand}"""
        model = "gpt-5.6-terra"
    else:
        prompt = f"""你是 fresh-context 匿名TGN Frozen Authority审计员。A/B/C来自同一冻结Primary：一个是Luna-medium基础Reviser，一个是Luna-medium+Authority Watch，一个是Luna-high Reviser，但你不知道对应关系。只比较actor/action/object、Direct Result、State Change、Ending、Reader Release、精确力量位置、Power permanent boundary、money/ownership/provenance、relationship、unknown与跨章timing，不评文笔。只有具体Hard conflict、required missing、未授权旧史/数字/伤势/来源/结果才扣分。

严格只输出JSON：{{"ranking":["A","B","C"],"scores":{{"A":0,"B":0,"C":0}},"hard_problems":{{"A":[],"B":[],"C":[]}},"reason":"中文5-8句具体比较"}}

# FROZEN AUTHORITY
{authority(chapter)}

{cand}"""
        model = "gpt-5.6-luna"
    out = EXP / "derivation-blind-d1" / run / f"chapter-{chapter:04d}"
    out.mkdir(parents=True, exist_ok=True)
    pp=out/f"{judge}_prompt.md"; ap=out/f"{judge}_acp.json"; rp=out/f"{judge}_response.md"
    pp.write_text(prompt,encoding="utf-8")
    data=call(pp,ap,model,f"{run}-{chapter}-{judge}")
    raw=str(data.get("text", "")); rp.write_text(raw.strip()+"\n",encoding="utf-8")
    val=parse(raw)
    ranking=[key[x] for x in val["ranking"]]
    scores={key[x]:float(v) for x,v in val["scores"].items()}
    problems={key[x]:v for x,v in val.get("hard_problems",{}).items()} if judge=="authority" else {}
    return {"run":run,"chapter":chapter,"judge":judge,"ranking":ranking,"scores":scores,"hard_problems":problems,"reason":val.get("reason","")}


def main():
    rows=[]
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures=[ex.submit(one,run,ch,judge) for run in ("repeat1","repeat2") for ch in range(1,5) for judge in ("story","authority")]
        for f in as_completed(futures):
            row=f.result(); rows.append(row); print(row["run"],row["chapter"],row["judge"],row["ranking"][0],flush=True)
    rows.sort(key=lambda x:(x["run"],x["chapter"],x["judge"]))
    agg={}
    for judge in ("story","authority"):
        group=[r for r in rows if r["judge"]==judge]; agg[judge]={}
        for name in ("medium_base","medium_watch","high"):
            agg[judge][name]={
                "mean_score":round(sum(r["scores"][name] for r in group)/len(group),3),
                "first_place":sum(r["ranking"][0]==name for r in group),
                "mean_rank":round(sum(r["ranking"].index(name)+1 for r in group)/len(group),3),
                "hard_problems":sum(len(r["hard_problems"].get(name,[])) for r in group),
            }
    result={"schema_version":"medium-authority-watch-d1-blind-v1","aggregates":agg,"rows":rows}
    (EXP/"DERIVATION_D1_BLIND.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(agg,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
