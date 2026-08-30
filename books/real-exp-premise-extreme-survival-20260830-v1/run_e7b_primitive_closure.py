from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from story_mvp.premise_aperture import build_selected_premise_compiler_prompt, build_single_pass_prompt, extract_sections

RUNNER = ROOT / "temps" / "acp_readonly_runner.mjs"

TREATMENT = r"""# EXPERIMENT TREATMENT｜EXTREME RIGHT-TAIL + PRIMITIVE CLOSURE

这是一个新的 fresh Forge Treatment，不是对上一张候选的 Repair。仍一次生成 S1/S2/S3，仍不自动选择；本实验在生成前预注册 S3。

创意电压要求：
- S3 进入极端右尾：只押一个主异常，优先打碎一个深层男频默认假设；主角默认不是标准人类少年，且必须拥有 4—7 个只有这本书才自然存在的 Changed Verbs。
- 第一章必须立刻有 unfair payoff；现场有真实观众/敌人/生态位时必须产生一次直接 repricing。
- 允许主角明显占便宜，只留一条真正防万能的根边界，不做对称平衡。
- 一句话必须听懂；不用抽象术语、概念哲学、更多系统数量冒充大胆。

新增的 Primitive Closure 只约束**因果可编译性**，不要求保守：
1. 在 `Power-only Direction` 中必须明写 `Legal Primitive Set`：3—5 个最小动作原语；再明写 `Legal Carrier / Target Classes`：一到少数类在当前 World 已真实定义的载体/目标。它们必须已经足以产生第一章高电压。
2. `主角反复会做的新动作` 中每个 Changed Verb 都必须是这些原语的直接动作或顺序/位置/组合结果，不能新增 target class、远程路由、共同网络、中央控制、无限复制或未定义出口。
3. `20章玩法扩张` 每个关键玩法后用括号写 `primitive composition:`，明确由哪几个已写原语 + 哪个已写载体组合。20章可以变得非常夸张，但只能“旧动作以新顺序/新位置/新对象实例复合”，不能把一条单点通道静默升级成全城网络。
4. `100章以上仍能长出的不同故事` 同样只能说明现有原语在未来 approved World 提供的新**实例**上怎样产生不同玩法；不能预先把“什么算合格载体”扩成新类别，也不能凭空新增跨世界出口。未来 World 若要增加新类别，那是未来 Authority 的新事实，不得在当前卡里当作已经可用。
5. `Authority-Compilation Trace` 必须覆盖第一章、每个 Changed Verb、20章终局最强动作。若某个想要的酷动作不能用 Legal Primitive Set 严格拼出来，删除/替换那个动作，而不是补一句新机制圆它。
6. Initial Scale Position 必须被 protagonist-blind World 自己定义的公共 grammar 容纳；不使用主角专属 `0级/尺外` 补洞。
7. Interface 仍只记录/观看/传播/改变社会后果，不参与 Power 路由。

**不要因为 Primitive Closure 把 S3 降成“分析更准/效率更高/正常修士多一个技巧”。目标是：极端 premise + 少量闭合原语 → 大量新动作。**
"""


def dump(p: Path, obj: object) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def run(prompt: Path, outj: Path, outm: Path, model: str, label: str) -> dict:
    started=time.time()
    proc=subprocess.run(["node",str(RUNNER),str(prompt),str(outj),model,"high",label],cwd=ROOT,text=True,capture_output=True,encoding="utf-8",errors="replace")
    if proc.returncode: raise RuntimeError(proc.stderr[-4000:]+"\n"+proc.stdout[-4000:])
    d=json.loads(outj.read_text(encoding="utf-8"))
    if not d.get("ok"): raise RuntimeError(str(d.get("error")))
    t=str(d.get("text","")).strip()
    outm.write_text(t+"\n",encoding="utf-8")
    print(json.dumps({"label":label,"wall":round(time.time()-started,2),"agent_wall":d.get("wall_seconds"),"chars":len(t)},ensure_ascii=False),flush=True)
    return d


def verdict(text: str) -> str:
    m=re.search(r"(?mi)^-?\s*Verdict\s*:\s*(PASS|CONDITIONAL PASS|FAIL)\s*$",text)
    if not m: raise RuntimeError("missing Verdict")
    return m.group(1).upper()


def main() -> None:
    author=(EXP/"AUTHOR_DIRECTION.md").read_text(encoding="utf-8")
    dump(EXP/"E7B_PRE_REGISTERED_SELECTION.json",{"selected_candidate":"S3","registered_before_generation":True,"continue_only_on":"PASS","fresh_generation_not_repair":True})
    p=build_single_pass_prompt(author_direction=author+"\n\n"+TREATMENT)
    (EXP/"E7B_FORGE_PROMPT.md").write_text(p,encoding="utf-8")
    run(EXP/"E7B_FORGE_PROMPT.md",EXP/"E7B_FORGE_ACP.json",EXP/"E7B_FORGE_RESPONSE.md","gpt-5.6-luna","premise-e7b-primitive-closure-forge")
    secs=extract_sections((EXP/"E7B_FORGE_RESPONSE.md").read_text(encoding="utf-8"),prefix="S")
    if tuple(secs)!=("S1","S2","S3"): raise RuntimeError(f"bad sections {tuple(secs)}")
    s3=secs["S3"]
    (EXP/"E7B_SELECTED_S3.md").write_text(s3+"\n",encoding="utf-8")
    cp=build_selected_premise_compiler_prompt(candidate=s3)
    (EXP/"E7B_COMPILER_PROMPT.md").write_text(cp,encoding="utf-8")
    run(EXP/"E7B_COMPILER_PROMPT.md",EXP/"E7B_COMPILER_ACP.json",EXP/"E7B_COMPILER_REPORT.md","gpt-5.6-terra","premise-e7b-primitive-closure-compiler")
    v=verdict((EXP/"E7B_COMPILER_REPORT.md").read_text(encoding="utf-8"))
    dump(EXP/"E7B_SUMMARY.json",{"selected":"S3","compiler_verdict":v,"downstream_authorized":v=="PASS","fresh_generation_not_repair":True,"production_modified":False})
    print(f"E7B_COMPILER_VERDICT={v}",flush=True)

if __name__=="__main__": main()
