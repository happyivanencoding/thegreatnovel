from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
SOURCE = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1" / "runs"
OUT = (
    ROOT
    / "books"
    / "real-exp-chapter-latency-optimization-20260829-v1"
    / "phase-2-slim-curator-medium"
)
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

sys.path.insert(0, str(ROOT / "src"))
from story_mvp.hybrid_runtime import _project_indexed_text  # noqa: E402


SLIM_TEMPLATE = """你是 TGN 的 Slim Context Curator。你只做本章注意力编译，不重新规划，不修改冻结 Mission，不创造事实，也不替 Writer 写正文。

本章输入已经由 runtime 确定性缩成 Authority Envelope。你不需要恢复完整 BOOK、完整长纲或完整 Scene Skill。Mission 中明确的行动者、对象、事件顺序、直接结果、状态变化与 Ending 必须原样保真；Audit 发现冲突只负责指出，不能借此静默换事件、换行动者、弱化结果或补一套更合理的实现。

严格输出：
# Curator Audit
只写会影响本章的明确冲突/未知；没有写“无”。最多3条。

# Curated Chapter Context
## Relevant Characters and Relationships
最多5条，只保留会改变本章注意、选择或说话方式的人物欲望/关系。
## Relevant World Rules
逐条保留已排程 Reader Release；其它只保留理解当前动作所必需的已批准事实。最多6条。
## Relevant Open Promises
最多6条，只保留本章仍未知/未兑现、会约束正文的项目。
## Relevant Plan
用3—6条复制 Mission 的关键行动、反应、结果与停点；不得替换行动者、关键物件、胜负、获得、损失或里程碑。
## Scene Prose Projection
已经清楚写 `NONE`；否则只写2—4句，控制注意、展开/压缩、POV知识边界与结果停点，不新增动作步骤或世界事实。
## Scene Skill Selection
Primary: <仅从 shortlist 选1个或 none>
Secondary: <仅从 shortlist 选0—1个或 none>
## Already Established — Do Not Re-explain
最多6条，只列本章仍有效、但不得重复证明的已成立事实。

不要输出 Reader-Facing Language、Opening Strategy、Payoff清单、完整 Book Contract、完整 Prose Profile、评分或思考。不要因为“更完整”增加钱数、时间、制度、人物到场、能力机制、路线步骤或契约条款。"""

SKILL_KEYWORDS = {
    "social_bargain_decision": ("契约", "价格", "赔付", "追索", "拒绝", "条件", "归属", "买断", "合作", "身份"),
    "relationship": ("关系", "旧友", "母亲", "乌合", "唐绾", "少东家", "舍不得", "离开", "同行"),
    "identity_reveal": ("身份", "公开", "揭露", "名字", "落籍", "见证"),
    "sacrifice_convergence": ("放弃", "牺牲", "保住", "取舍", "失去", "代价", "撤离"),
    "investigation": ("对照", "记录", "事实", "核查", "判断", "追查", "证据"),
    "exploration": ("裂槽", "进入", "通道", "遗迹", "峡", "矿样", "路线", "未知"),
    "survival_endurance": ("逃", "撤离", "活", "压住", "危险", "余震", "伤员"),
    "chase_escape": ("追", "拦截", "逃", "赶", "撤路", "逼近"),
    "combat": ("攻击", "冲击", "潮兽", "战", "挡住", "击败", "承压", "正面"),
    "hunt_acquisition": ("获得", "夺取", "古器", "回潮楔", "矿样", "潮谱", "持有"),
    "breakthrough_advancement": ("突破", "成炉", "照域", "镇海", "提升", "潮炉", "进入"),
    "showcase_evaluation": ("公开", "懂行", "评价", "重新定价", "见证", "展示", "开炉试"),
    "resource_economy": ("钱", "预付款", "矿利", "尾款", "报酬", "粮", "井", "资源"),
    "crafting_creation": ("修复", "制作", "铸", "裂痕", "作品"),
    "recovery_restoration": ("修复", "恢复", "裂痕", "伤势", "残压"),
}


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def exact_block(prompt: str, start: str, end: str | None) -> str:
    begin = prompt.index(start) + len(start)
    finish = prompt.index(end, begin) if end else len(prompt)
    return prompt[begin:finish].strip()


def catalog_shortlist(catalog: str, mission: str, limit: int = 5) -> str:
    lines = [line.strip() for line in catalog.splitlines() if line.strip().startswith("- ")]
    parsed = []
    for index, line in enumerate(lines):
        skill_id = line[2:].split(":", 1)[0].strip()
        score = sum(1 for keyword in SKILL_KEYWORDS.get(skill_id, ()) if keyword in mission)
        parsed.append((score, index, skill_id, line))
    selected = sorted(parsed, key=lambda item: (-item[0], item[1]))[:limit]
    # A zero-score tail is allowed only to keep the fixed shortlist size; it remains optional.
    return "\n".join(item[3] for item in selected)


def build_prompt(chapter: int) -> tuple[str, str]:
    source = SOURCE / f"chapter-{chapter:04d}" / "curator_prompt.md"
    full = source.read_text(encoding="utf-8")
    authority = exact_block(full, "## AUTHORITY", "## 当前章事件合同")
    mission = exact_block(full, "## 当前章事件合同", "## CONTEXT INDEX——只含可见结构入口，不含被省略正文")
    reader_release = exact_block(full, "## READER RELEASE——Outline 排程的本章世界事实", "## WORLD AUTHORITY——本章确定性预取")
    world = exact_block(full, "## WORLD AUTHORITY——本章确定性预取", "## FROZEN HUMAN CORE——稳定人格权威，只用于本章相关选择与私人牵引")
    human = exact_block(full, "## FROZEN HUMAN CORE——稳定人格权威，只用于本章相关选择与私人牵引", "## 压缩 Growth Genome（本章相关固定小节）")
    book = exact_block(full, "## BOOK CONTRACT——本章确定性预取", "## 本章成长收益短投影（规划提示，不是正文措辞）")
    canon = exact_block(full, "## CANON INDEX——本章确定性预取", "## 当前大型剧情块与十章计划")
    prose = exact_block(full, "## PROSE PROFILE", "## SCENE SKILL CATALOG——只用于选择 1 个 Primary 与可选 1 个 Secondary")
    catalog = exact_block(full, "## SCENE SKILL CATALOG——只用于选择 1 个 Primary 与可选 1 个 Secondary", "## OPTIONAL INSPIRATION")
    tail = exact_block(full, "## 前文章末局部衔接片段", None)
    query = mission + "\n\n" + reader_release
    book_focus = _project_indexed_text(book, query, max_chars=1300)
    canon_focus = _project_indexed_text(canon, query, max_chars=2600)
    prose_focus = _project_indexed_text(prose, query, max_chars=900)
    shortlist = catalog_shortlist(catalog, mission)
    envelope = "\n\n".join(
        (
            "# AUTHORITY\n" + authority,
            "# FROZEN MISSION\n" + mission,
            "# READER RELEASE CHECKLIST\n" + (reader_release or "（本章无 Reader Release。）"),
            "# RELEVANT WORLD FACTS\n" + (world or "（无额外 World fact。）"),
            "# FROZEN HUMAN CORE\n" + human,
            "# BOOK FOCUS\n" + book_focus,
            "# CANON FOCUS\n" + canon_focus,
            "# PROSE FOCUS\n" + prose_focus,
            "# SCENE SKILL SHORTLIST\n" + shortlist,
            "# PREVIOUS TAIL\n" + tail[-1200:],
        )
    )
    return SLIM_TEMPLATE + "\n\n" + envelope, full


def run_one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    prompt, control_prompt = build_prompt(chapter)
    prompt_path = directory / "slim_curator_prompt.md"
    output_path = directory / "slim_curator_medium_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    process = subprocess.run(
        ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-luna", "medium", str(ROOT)],
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
    (directory / "slim_curator_response.md").write_text(response + "\n", encoding="utf-8")
    headings = re.findall(r"(?m)^##\s+(.+?)\s*$", response)
    control_data = json.loads((SOURCE / f"chapter-{chapter:04d}" / "curator_acp.json").read_text(encoding="utf-8"))
    usage = data.get("result", {}).get("usage", {}) or {}
    return {
        "chapter": chapter,
        "prompt_chars": len(prompt),
        "control_prompt_chars": len(control_prompt),
        "prompt_reduction_percent": round((1 - len(prompt) / len(control_prompt)) * 100, 2),
        "wall_seconds": float(data.get("wall_seconds") or 0),
        "control_high_wall_seconds": float(control_data.get("wall_seconds") or 0),
        "speedup_percent": round((1 - float(data.get("wall_seconds") or 0) / float(control_data.get("wall_seconds") or 1)) * 100, 2),
        "response_chars": len(response),
        "output_tokens": usage.get("outputTokens", 0),
        "thought_tokens": usage.get("thoughtTokens", 0),
        "headings": headings,
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
    (OUT / "curator_summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
