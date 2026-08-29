from __future__ import annotations

import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
SOURCE = BOOK / "runs"
AUTH = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "parallel-authority-watch"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "twin-blueprint-primary"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = (2, 3, 10, 14, 19)

STORY_PLANNER_TEMPLATE = """你是 TGN 的 Pre-Draft Male-Fantasy Story Value Planner，使用 GPT-5.6 Luna high。你在正式 Writer 写正文前独立工作，不写正文、不修改 Frozen Mission、不创造世界/力量/价格/人物事实。

你的职责是把同一 Authority 中**最接近顶级中文男频长篇的阅读价值**编译成少量可执行场景要求，防止后续 Writer 为了守事实而把小说写成摘要、流程或无欲望的安全版本。

优先保护：
- 主角主动做了什么、为什么是他自己的欲望/偏爱，而不是被流程推动；
- 本章读者最想看到、得到、确认或继续追的对象；
- 核心幻想/能力/器物最独特、最值得馋的体验；
- 具体奖励、持有、身份、关系、世界入口与实际后果真正落地；
- Public Proof 需要时允许群体震动、懂行者尺度校准、关键人物行为重估三路并列；
- 人物关系、钱、胜负、面子、审美、身体感、享受、偏心、舍不得等已批准私人牵引；
- 章末必须是真实动作/选择/新局面，不是后台总结或“以后会发生”。

只使用下方 Mission / Curator / Canon / Frozen Human-Power-World 已有事实；激进只体现在场面、欲望、收益和社会重量，不体现在补造新事实。

严格输出，总长 1000—1800 中文字符：
# CORE READER QUESTION
一句。
# PROTAGONIST AGENCY CHAIN
用 A1/A2… 写主角主动动作与选择链。
# HUMAN / RELATIONSHIP BEATS
用 H1/H2… 写本章人物欲望、关系或私人牵引；没有写 NONE。
# FANTASY / PAYOFF BEATS
用 F1/F2… 写必须充分戏剧化的能力、器物、获得、损失、社会反馈；没有写 NONE。
# FULL SCENES
列 2—5 个值得展开成完整场景的 beat，说明每个 beat 的冲突与落点；不得新增事件。
# ENDING ACTION
写本章最后必须真实发生的动作/选择/局面。
# DO NOT FLATTEN
列出不能被压成摘要、资格、流程、记录或一句说明的价值。

不要输出审计、事实边界、评分、正文或思考过程。"""

FINAL_WRITER_CONTRACT = """# Twin-Blueprint Final Writer Contract

本次 Terra Writer 直接产出候选最终正文。你同时收到两个独立 Luna-high 蓝图：
- `AUTHORITY BLUEPRINT` 负责事实、Mission、未知边界与全章闭合；
- `STORY VALUE BLUEPRINT` 负责主角主动性、人物欲望、核心幻想、Payoff、Public Proof、关系和完整场面。

两者同样重要：不能为了更有戏越过 Authority，也不能为了更安全把 Story Value 写薄。

- Authority 的 MUST LAND / GLOBAL CLOSURE 必须通过正文真实完成；不得降成准备、资格、依据、以后结算或“即将”。
- Story Value 的 FULL SCENES / AGENCY / PAYOFF / ENDING 是商业表达下限，应通过动作、对白、空间、身体反馈、差异化反应与具体结果展开，不是逐条复述蓝图。
- 保留当前 BOOK prose profile 与 Curator attention；人物可以贪钱、嘴硬、舍不得、好胜、想要，不统一翻译成成熟协作。
- 大胜、获得或公开超标已有因果时，可以明显、具体、偏强地落地，不主动少给或削弱社会反应。
- 只压缩真实出现的程序、报告、登记、路线和重复证明；不能以“简洁”为由删掉人物、关系、幻想、收益或真实章末动作。

严格只输出 `# 正式正文` 和完整小说正文，不输出说明、Audit 或摘要。"""


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


def call(prompt_path: Path, output_path: Path, model: str) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), model, "high", str(ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        if process.returncode == 0 and output_path.exists():
            try:
                data = json.loads(output_path.read_text(encoding="utf-8"))
            except Exception as error:
                data = {}
                last = str(error)
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (process.stderr + "\n" + process.stdout)[-3000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(last)


def planner_input(chapter: int) -> str:
    primary_prompt = (SOURCE / f"chapter-{chapter:04d}" / "primary_prompt.md").read_text(encoding="utf-8")
    authority_prompt = (SOURCE / f"chapter-{chapter:04d}" / "authority_reviser_prompt.md").read_text(encoding="utf-8")
    # Primary already contains Mission, Canon prose and Curator attention; add only the
    # frozen Human/Power/World authority prefix, excluding the draft itself.
    authority_prefix = authority_prompt.split("## PRIMARY DRAFT｜唯一待修订正文底稿", 1)[0]
    return primary_prompt + "\n\n# FROZEN VALUE AUTHORITY\n\n" + authority_prefix


def one(chapter: int) -> dict:
    source = SOURCE / f"chapter-{chapter:04d}"
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    story_prompt = STORY_PLANNER_TEMPLATE + "\n\n# CHAPTER INPUT\n\n" + planner_input(chapter)
    story_prompt_path = directory / "story_value_planner_prompt.md"
    story_output_path = directory / "story_value_planner_acp.json"
    story_prompt_path.write_text(story_prompt, encoding="utf-8")
    story_data = call(story_prompt_path, story_output_path, "gpt-5.6-luna")
    story_blueprint = clean(story_data.get("text", ""))
    (directory / "story_value_blueprint.md").write_text(story_blueprint + "\n", encoding="utf-8")

    authority_blueprint = (AUTH / f"chapter-{chapter:04d}" / "watchlist.md").read_text(encoding="utf-8").strip()
    primary_prompt = (source / "primary_prompt.md").read_text(encoding="utf-8")
    marker = "## CANON PROSE——上一章全文与上上章必要章末"
    if marker not in primary_prompt:
        raise RuntimeError(f"ch{chapter}: marker missing")
    injection = (
        FINAL_WRITER_CONTRACT
        + "\n\n# AUTHORITY BLUEPRINT\n\n"
        + authority_blueprint
        + "\n\n# STORY VALUE BLUEPRINT\n\n"
        + story_blueprint
        + "\n\n"
        + marker
    )
    final_prompt = primary_prompt.replace(marker, injection, 1)
    final_prompt_path = directory / "twin_blueprint_primary_prompt.md"
    final_output_path = directory / "twin_blueprint_primary_acp.json"
    final_prompt_path.write_text(final_prompt, encoding="utf-8")
    writer_data = call(final_prompt_path, final_output_path, "gpt-5.6-terra")
    response = clean(writer_data.get("text", ""))
    final_body = body(response)
    (directory / "twin_blueprint_primary_response.md").write_text(response + "\n", encoding="utf-8")
    (directory / "final_body.md").write_text(final_body + "\n", encoding="utf-8")

    auth_data = json.loads((AUTH / f"chapter-{chapter:04d}" / "watch_planner_acp.json").read_text(encoding="utf-8"))
    primary_data = json.loads((source / "primary_acp.json").read_text(encoding="utf-8"))
    reviser_data = json.loads((source / "authority_reviser_acp.json").read_text(encoding="utf-8"))
    auth_wall = float(auth_data.get("wall_seconds") or 0)
    story_wall = float(story_data.get("wall_seconds") or 0)
    writer_wall = float(writer_data.get("wall_seconds") or 0)
    control_wall = float(primary_data.get("wall_seconds") or 0) + float(reviser_data.get("wall_seconds") or 0)
    treatment_critical = max(auth_wall, story_wall) + writer_wall
    return {
        "chapter": chapter,
        "authority_planner_wall_seconds": auth_wall,
        "story_planner_wall_seconds": story_wall,
        "writer_wall_seconds": writer_wall,
        "control_primary_plus_reviser_seconds": round(control_wall, 3),
        "treatment_parallel_blueprints_plus_writer_seconds": round(treatment_critical, 3),
        "critical_path_speedup_percent": round((1 - treatment_critical / control_wall) * 100, 2),
        "story_blueprint_chars": len(story_blueprint),
        "final_prompt_chars": len(final_prompt),
        "final_chars": len(final_body),
        "story_usage": story_data.get("result", {}).get("usage", {}),
        "writer_usage": writer_data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=len(CHAPTERS)) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
