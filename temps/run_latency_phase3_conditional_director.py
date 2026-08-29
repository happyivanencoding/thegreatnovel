from __future__ import annotations

import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
OUT = (
    ROOT
    / "books"
    / "real-exp-chapter-latency-optimization-20260829-v1"
    / "phase-3-conditional-director"
)
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

CORE = """你是 TGN 当前章 Director。只把已经批准的当前章计划编译成八字段事件合同；不写正文、不重做长期规划、不创造世界/力量/身份/价格/奖励事实。

当前章执行边界是唯一事件预算；大型剧情块只作阶段背景。章末 Handoff 只能制造下一章压力、入口、来人、线索或未完成动作，不能提前完成下一章付款、身份、获得、升级或结算。计划明确的结果/状态变化必须保真；只有已发生 Canon 真使其不可能时，才在“状态变化”写 `[PLAN OUTCOME ADJUSTMENT]` 与最小替代。

优先抓一章最值得读的冲突、选择、力量动作、反转与后果。Supporting Logic 只写到支撑决定和结果；决定后的登记、路线、检查、搬运、协调、责任分配等普通实施压缩。主角可以命令、拒绝、抢夺、交易、保护、结盟和牺牲，但不替多方做协调员。一个事实经动作和一次校准成立后，立即进入 Consequence，不换证据重复证明。

必须只输出：
触发事件：
推动事件的人：
主角行动：
对手或世界反应：
直接结果：
状态变化：
叙事功能：
结尾推动力：

每项具体填写。不得输出 Audit、评分、正文、完整计划或内部推理。"""

MODULES = {
    "opening": """# Conditional｜Opening 1—3
前三章仍服从当前章预算：第一章让核心优势产生真实结果；第二章把优势变成可保留/再调用的东西；第三章让收益进入下一轮行动。不能为完整感提前结算下一章。关键选择要暴露主角自己的欲望，而非通用正确。""",
    "opportunity": """# Conditional｜Named Opportunity
若当前行动因具名试场、招募、契约、名额或邀请发生，保留其具体名字与已批准价值；不新增回报、不预告成功、不把它泛化成“更大机会”。""",
    "reward": """# Conditional｜Reward / Ownership
计划已批准的钱、器物、矿利、身份、入口或其它具体获得必须真正落到结果；不降成资格或以后再给。大胜可有复合结算，但不得凭空增加计划外奖励，也不得把真实牺牲立刻用等价替代抹平。""",
    "ruler": """# Conditional｜Ruler / Public Proof
突破、新层级、新复合或重大公开超标时，先让结果发生，再按现场真实条件保留群体震动、懂行者短校准与关键人物重新定价；三路可并列。已有精确主尺时使用同一坐标，越级胜利不自动升级。""",
    "unknown": """# Conditional｜Unknown / Long History
旧线、秘密、异常或过去原因若未获上游授权，明确仍未知；本章只确立 Mission 已批准的新事实和它造成的当下选择/关系/入口，不让 Writer 自行补旧史。""",
    "counter": """# Conditional｜Repetition / Counter
若最近章节正在重复同一种压力、解法或结算，在不改计划的前提下让当前结果改变身份、关系、敌人策略、获得、目标或舞台；不为形式变化强造新戏。长期对手已学到边界时，反制必须真实改变主角选择或局面。""",
    "handoff": """# Conditional｜World Horizon Handoff
当前世界顶层结算只使用已批准事实；停在 Handoff 的触发、尺度冲击与 carry-forward，不提前设计下一世界的势力、能力、宝物或针对主角 Build 的答案。""",
}

TRIGGERS = {
    "opening": lambda chapter, text: chapter <= 3,
    "opportunity": lambda chapter, text: bool(re.search(r"试场|选拔|招募|契约|名额|邀请|资格|委托", text)),
    "reward": lambda chapter, text: bool(re.search(r"获得|取得|到手|钱|潮铢|预付款|尾款|矿利|回潮楔|潮谱|古器|身份|入口|所有权|持有", text)),
    "ruler": lambda chapter, text: bool(re.search(r"公开|见证|展示|开炉试|突破|成炉|照域|镇海|重新定价|重估|懂行|越级", text)),
    "unknown": lambda chapter, text: bool(re.search(r"未知|未解决|秘密|过去|原因|为何|谜|真相|掩盖", text)),
    "counter": lambda chapter, text: True,
    "handoff": lambda chapter, text: chapter == 20 or "Handoff" in text or "下一世界" in text,
}


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def h2_block(text: str, prefix: str) -> str:
    headings = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(headings):
        if not match.group(1).strip().startswith(prefix):
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        return text[match.end():end].strip()
    return ""


def build_prompt(chapter: int) -> tuple[str, str, list[str]]:
    source = (SOURCE / f"chapter-{chapter:04d}" / "director_prompt.md").read_text(encoding="utf-8")
    context_index = source.index("# Director Context")
    context = source[context_index:].strip()
    opening = ""
    opening_marker = "# Opening Three Chapter Contract"
    if opening_marker in source[:context_index]:
        opening = source[source.index(opening_marker):context_index].strip()
    # Conditional routing must inspect only this chapter's executable plan and the
    # optional deterministic named-opportunity recovery. The broader context carries
    # generic author directions mentioning rewards, Public Proof and the Chapter-20
    # Handoff, which would otherwise turn every conditional module back on.
    signal = "\n\n".join(
        part
        for part in (
            h2_block(context, "当前章执行边界"),
            h2_block(context, "当前章十章计划条目"),
            h2_block(context, f"第{chapter}章"),
            h2_block(context, "当前具名机会权威"),
        )
        if part
    )
    enabled = [name for name, predicate in TRIGGERS.items() if predicate(chapter, signal)]
    module_text = "\n\n".join(MODULES[name] for name in enabled)
    prompt = "\n\n".join(part for part in (CORE, module_text, opening, context) if part)
    return prompt, source, enabled


def run_one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    prompt, control_prompt, modules = build_prompt(chapter)
    prompt_path = directory / "conditional_director_prompt.md"
    output_path = directory / "conditional_director_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    process = subprocess.run(
        ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-luna", "high", str(ROOT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if process.returncode:
        raise RuntimeError(process.stderr[-3000:])
    data = json.loads(output_path.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(str(data.get("error")))
    response = clean(data.get("text", ""))
    (directory / "conditional_director_response.md").write_text(response + "\n", encoding="utf-8")
    control_data = json.loads((SOURCE / f"chapter-{chapter:04d}" / "director_acp.json").read_text(encoding="utf-8"))
    usage = data.get("result", {}).get("usage", {}) or {}
    fields = re.findall(r"(?m)^(触发事件|推动事件的人|主角行动|对手或世界反应|直接结果|状态变化|叙事功能|结尾推动力)：", response)
    return {
        "chapter": chapter,
        "modules": modules,
        "prompt_chars": len(prompt),
        "control_prompt_chars": len(control_prompt),
        "prompt_reduction_percent": round((1 - len(prompt) / len(control_prompt)) * 100, 2),
        "wall_seconds": float(data.get("wall_seconds") or 0),
        "control_wall_seconds": float(control_data.get("wall_seconds") or 0),
        "speedup_percent": round((1 - float(data.get("wall_seconds") or 0) / float(control_data.get("wall_seconds") or 1)) * 100, 2),
        "response_chars": len(response),
        "fields": fields,
        "output_tokens": usage.get("outputTokens", 0),
        "thought_tokens": usage.get("thoughtTokens", 0),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as executor:
        futures = [executor.submit(run_one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
