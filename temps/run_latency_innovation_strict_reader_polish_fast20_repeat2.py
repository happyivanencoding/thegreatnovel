from __future__ import annotations

import difflib
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
BOOK = ROOT / "books" / "real-exp-fast-world-20ch-20260828-v1"
SOURCE = BOOK / "runs"
OUT = ROOT / "books" / "real-exp-chapter-latency-innovation-20260829-v1" / "strict-reader-polish-fast20-repeat2"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")
CHAPTERS = tuple(range(1, 21))

PROMPT = """你是 TGN 的 Strict Post-Authority Reader Polish Agent，使用 Terra medium。输入已经完成完整 Authority Revision；事实、人物价值、事件、力量、关系、结果和 Ending 都冻结。

只允许提出最多 2 个**纯删除型**局部 Patch，目标是删除作者替读者重复总结、已经由紧邻动作/对白/物体结果充分证明的抽象载体。NEW 必须仅由 OLD 删除字符、标点或空白得到，不能加入任何新字，也不能把一句改写成更通俗的另一句。

可以考虑：
- “这句话/这件事/那些事/这一刻/三件事……”一类已被上下文完全证明的旁白盖章；
- 紧邻下一句已经用具体位置或动作再次证明的同义结果句；
- 关系或局势已经由对白与动作完成后的一句纯总结。

绝对保护，禁止删除、合并或缩写：
- 人物直接的怕、不怕、想、不想、要、喜欢、舍不得、拒绝、决定、偏心、嫉妒、野心、占有欲及其它私人牵引；
- 人物说话姿态、语气、是否求人、克制、嘴硬、犹豫等关系信号；
- 群体等待、围观、沉默、震惊、压力、社会重新定价；
- 主角独特价值判断、行为签名、幽默、刻薄或世界观措辞；
- 任何事件、动作结果、人物、专名、物件、数字、价格、时间、力量、伤势、持有人、状态、否定/肯定、完成/未完成、Payoff、Public Proof 或 Ending；
- 任何独立停顿句，只要它承担欲望、关系、力量、爽点、情绪或节奏重音。

若不能证明删除后所有人物价值与事实完全等价，输出 `NO_CHANGE`。不要为了有产出而修改。不要同义润色，不追求文学性。

严格只输出：
NO_CHANGE

或：
# PATCH SET
## PATCH 1
OLD:
<正文中唯一连续原文>
NEW:
<仅删除字符后的文本，可以为空>
REASON:
<一句说明为什么是重复总结，且没有删除人物价值>

最多2个 Patch。不要输出完整正文、Audit、评分或思考。"""

PATCH_PATTERN = re.compile(
    r"(?ms)^## PATCH\s+\d+\s*$\nOLD:\s*\n(?P<old>.*?)\nNEW:\s*\n(?P<new>.*?)\nREASON:\s*\n(?P<reason>.*?)(?=^## PATCH\s+\d+\s*$|\Z)"
)
PROTECTED_PATTERNS = tuple(
    re.compile(pattern)
    for pattern in (
        r"(?:他|她|我|自己).{0,12}(?:不怕|害怕|怕|不想|想要|想留下|确实想|想|要|喜欢|舍不得|拒绝|决定|愿意|偏心|嫉妒|恨)",
        r"(?:没有|不是).{0,10}(?:求人|示弱|服软|退让|犹豫|生气|恼火|高兴|失望|嘴硬).{0,4}(?:意思|样子|语气)?",
        r"(?:所有人|众人|全场|周围的人|在场的人|大家).{0,12}(?:等|看|沉默|安静|震惊|盯|目光|反应)",
        r"(?:都在等|等他|等她).{0,8}(?:选择|决定|开口|行动)",
        r"潮灾无情|天灾|不是因为.{0,30}而是因为",
    )
)
FACT_TERMS = (
    "已经", "尚未", "仍未", "没有", "不能", "不得", "必须", "只能", "可以", "不再",
    "归", "持有", "交给", "收下", "到账", "突破", "升级", "死", "伤", "离开", "进入",
    "出发", "完成", "失败", "赢", "输", "第一次", "最后", "立刻", "终于",
)


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def call(prompt_path: Path, output_path: Path) -> dict:
    last = ""
    for attempt in range(3):
        process = subprocess.run(
            ["node", str(RUNNER), str(prompt_path), str(output_path), "gpt-5.6-terra", "medium", str(ROOT)],
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


def is_deletion_only(old: str, new: str) -> bool:
    it = iter(old)
    return all(any(char == candidate for candidate in it) for char in new)


def deleted_fragments(old: str, new: str) -> list[str]:
    matcher = difflib.SequenceMatcher(None, old, new, autojunk=False)
    fragments = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in {"insert", "replace"} and j1 != j2:
            raise ValueError("patch inserts or replaces characters")
        if tag in {"delete", "replace"} and i1 != i2:
            fragments.append(old[i1:i2])
    return fragments


def fact_signature(text: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    numbers = tuple(sorted(re.findall(r"\d+(?:\.\d+)?", text)))
    terms = tuple(term for term in FACT_TERMS if term in text)
    return numbers, terms


def validate_patch(old: str, new: str) -> None:
    if not is_deletion_only(old, new):
        raise ValueError("not deletion-only")
    deleted = "".join(deleted_fragments(old, new))
    if not deleted.strip():
        raise ValueError("no meaningful deletion")
    if fact_signature(old) != fact_signature(new):
        raise ValueError("fact-strength signature changed")
    if any(pattern.search(old) for pattern in PROTECTED_PATTERNS):
        raise ValueError("protected human/relationship/social value")
    if re.search(r"[“”「」『』]", deleted):
        raise ValueError("deleted dialogue content")
    if old.count("\n\n") > 2 or new.count("\n\n") > 2:
        raise ValueError("scope too wide")
    if len(deleted.strip()) > 80:
        raise ValueError("deletion too large")


def apply_patch(response: str, original: str) -> tuple[str, list[dict], str]:
    text = clean(response)
    if text == "NO_CHANGE":
        return original, [], "no_change"
    if not text.startswith("# PATCH SET"):
        raise ValueError("invalid contract")
    result = original
    patches = []
    for match in PATCH_PATTERN.finditer(text):
        old = match.group("old").strip()
        new = match.group("new").strip()
        reason = match.group("reason").strip()
        if not old or result.count(old) != 1:
            raise ValueError(f"OLD occurrence count={result.count(old)}")
        validate_patch(old, new)
        result = result.replace(old, new, 1)
        patches.append({"old": old, "new": new, "reason": reason})
    if not patches or len(patches) > 2:
        raise ValueError(f"patch count={len(patches)}")
    return result.strip(), patches, "patched"


def state_wall(chapter: int) -> float:
    directory = SOURCE / f"chapter-{chapter:04d}"
    for filename in ("state_delta_acp.json", "state_acp.json"):
        path = directory / filename
        if path.exists():
            return float(json.loads(path.read_text(encoding="utf-8")).get("wall_seconds") or 0)
    return 0.0


def one(chapter: int) -> dict:
    directory = OUT / f"chapter-{chapter:04d}"
    directory.mkdir(parents=True, exist_ok=True)
    original = (BOOK / "chapters" / f"chapter-{chapter:04d}.md").read_text(encoding="utf-8").strip()
    prompt = PROMPT + "\n\n# FINAL AUTHORITY-CLEAN BODY\n\n" + original
    prompt_path = directory / "polish_prompt.md"
    output_path = directory / "polish_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(data.get("text", ""))
    (directory / "polish_response.md").write_text(response + "\n", encoding="utf-8")
    fallback = False
    error = ""
    try:
        final, patches, mode = apply_patch(response, original)
    except Exception as exc:
        fallback = True
        error = str(exc)
        final, patches, mode = original, [], "invalid_fallback"
    (directory / "final_body.md").write_text(final + "\n", encoding="utf-8")
    polish_wall = float(data.get("wall_seconds") or 0)
    current_state_wall = state_wall(chapter)
    return {
        "chapter": chapter,
        "state_wall_seconds": current_state_wall,
        "polish_wall_seconds": polish_wall,
        "hidden_by_state": polish_wall <= current_state_wall,
        "added_wall_over_state_seconds": round(max(0.0, polish_wall - current_state_wall), 3),
        "mode": mode,
        "fallback": fallback,
        "error": error,
        "patch_count": len(patches),
        "patches": patches,
        "original_chars": len(original),
        "final_chars": len(final),
        "usage": data.get("result", {}).get("usage", {}),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(one, chapter) for chapter in CHAPTERS]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["chapter"])
    (OUT / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
