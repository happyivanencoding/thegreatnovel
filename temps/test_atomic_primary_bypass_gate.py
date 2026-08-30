from pathlib import Path
import json,re,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from atomic_primary_bypass_gate import evaluate

OLD=Path(r"C:\dev\tgn-story-mvp-native-e2e\books\real-exp-native-structured-e2e-20260830-v1")
EXP=Path(__file__).resolve().parents[1]/"books"/"real-exp-free-text-atomic-gate-skip-reviser-20260830-v1"

def gate_decision(sample,text):
    g=evaluate(sample,text)
    return "PASS_DIRECT_FINAL" if g.supported and g.pass_ else "FALLBACK_FULL"

def test_calibration_matches_safe_subset_without_false_safe():
    oracle=json.loads((EXP/"feasibility-oracle"/"summary.json").read_text(encoding="utf-8"))
    expected={(r["run"],r["sample"]):r["decision"] for r in oracle["rows"]}
    false_safe=0; passes=0
    for run in ("fresh-control-3","fresh-control-4"):
        for sample in ("jiuchui_ch14","jiuchui_ch16","shadow_ch4","shadow_ch9"):
            text=(OLD/run/sample/"primary_response.md").read_text(encoding="utf-8")
            got=gate_decision(sample,text)
            false_safe += got=="PASS_DIRECT_FINAL" and expected[(run,sample)]=="FALLBACK_FULL"
            passes += got=="PASS_DIRECT_FINAL"
    assert false_safe==0
    assert passes==4

def test_targeted_hard_fact_mutations_block():
    j14=(OLD/"fresh-control-3"/"jiuchui_ch14"/"primary_response.md").read_text(encoding="utf-8")
    s9=(OLD/"fresh-control-3"/"shadow_ch9"/"primary_response.md").read_text(encoding="utf-8")
    mutations=[]
    mutations.append(("jiuchui_ch14",re.sub(r"[^\n]*砺骨部依靠潮井和迁徙水路生存[^\n]*\n?","",j14)))
    x=re.sub(r"[^\n]*(固定报酬|报酬、货单、损失边界|损耗按货单|超过约定的损失)[^\n]*\n?","",j14);mutations.append(("jiuchui_ch14",x))
    mutations.append(("jiuchui_ch14",j14.replace("回潮楔不卖","回潮楔卖给阮青蜃")))
    mutations.append(("jiuchui_ch14",re.sub(r"[^\n]*残压未散[^\n]*\n?","",re.sub(r"[^\n]*残压还没彻底散尽[^\n]*\n?","",j14))))
    mutations.append(("jiuchui_ch14",j14.replace("赶在下一次十二日地潮前送到旧关","送到旧关").replace("地潮不会等人","路上别耽搁")))
    x=re.sub(r"[^\n]*(短兵我想拿|我想要那对短兵|我也不想|你我也想救|两个我都没想放)[^\n]*\n?","",s9);mutations.append(("shadow_ch9",x))
    mutations.append(("shadow_ch9",re.sub(r"[^\n]*影身不是替你去送死[^\n]*\n?","",re.sub(r"[^\n]*它挨的刀[^\n]*\n?","",s9))))
    mutations.append(("shadow_ch9",s9.replace("普通二阶护卫，做不到这种事。","这次记录照常写。").replace("你原先那份护卫待遇，得重新算。","你原先那份护卫待遇照旧。")))
    mutations.append(("shadow_ch9",s9+"\n\n顾临川隔着很远也能看见分影那边发生的一切。"))
    mutations.append(("shadow_ch9",s9+"\n\n更高护卫待遇已经给了他，新的报酬当场到账。"))
    assert all(gate_decision(sample,text)=="FALLBACK_FULL" for sample,text in mutations)
