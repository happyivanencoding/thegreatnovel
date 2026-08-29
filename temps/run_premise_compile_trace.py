from __future__ import annotations

from pathlib import Path
import json
import re
import subprocess
import sys


ROOT = Path(r"C:\dev\tgn-story-mvp")
BASE = ROOT / "books" / "real-exp-premise-aperture-20260829-v1" / "fast_multiworld"
EXP = BASE / "single_pass_compile_trace_v2"
RUNNER = ROOT / "temps" / "acp_readonly_runner.mjs"
sys.path.insert(0, str(ROOT / "src"))

from story_mvp.premise_aperture import (  # noqa: E402
    build_single_pass_lane_bundle,
    build_single_pass_prompt,
    extract_sections,
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def run_acp(
    prompt_path: Path,
    json_path: Path,
    output_path: Path,
    *,
    model: str,
    label: str,
) -> dict[str, object]:
    cp = subprocess.run(
        ["node", str(RUNNER), str(prompt_path), str(json_path), model, "high", label],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if cp.returncode:
        raise RuntimeError(f"{label}: {cp.stderr[-3000:]}")
    data = json.loads(json_path.read_text(encoding="utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"{label}: {data.get('error')}")
    text = clean(str(data.get("text", "")))
    output_path.write_text(text + "\n", encoding="utf-8")
    return {
        "model": model,
        "effort": "high",
        "wall_seconds": data.get("wall_seconds"),
        "chars": len(text),
    }


def main() -> None:
    EXP.mkdir(parents=True, exist_ok=True)
    author = read(BASE / "AUTHOR_DIRECTION.md")
    prompt = build_single_pass_prompt(author_direction=author)
    (EXP / "PROMPT.md").write_text(prompt, encoding="utf-8")
    forge_meta = run_acp(
        EXP / "PROMPT.md",
        EXP / "FORGE_ACP.json",
        EXP / "CANDIDATES.md",
        model="gpt-5.6-luna",
        label="premise-compile-trace-v2-fast-multiworld",
    )

    candidates = extract_sections(read(EXP / "CANDIDATES.md"), prefix="S")
    if tuple(candidates) != ("S1", "S2", "S3"):
        raise RuntimeError(f"expected S1/S2/S3, got {tuple(candidates)}")
    structural: dict[str, object] = {}
    for candidate_id, section in candidates.items():
        bundle = build_single_pass_lane_bundle(section)
        structural[candidate_id] = {
            "parse_passed": True,
            "world_chars": len(bundle.world),
            "world_interface_chars": len(bundle.world_interface),
            "ontology_chars": len(bundle.ontology),
            "origin_chars": len(bundle.origin),
            "power_chars": len(bundle.privilege),
            "story_interface_chars": len(bundle.interface),
        }
    (EXP / "STRUCTURAL_CHECK.json").write_text(
        json.dumps(structural, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    old_s2 = read(BASE / "single_pass" / "SELECTED_S2.md")
    conflict = read(BASE / "downstream_S2_frozen_v2" / "STORY_PROGRAM.md")
    audit_prompt = f"""你是 TGN Premise Authority-Compilability 审计员。只审计，不改稿，不自动选择候选。

这是对 Single-Agent Premise Forge 的近单变量修复：旧版能生成大胆设定，但预注册 S2 在 lane-specific frozen contract 下暴露四类真实冲突：开篇效果早于 Power trigger、Interface 被当作 Power 放大器、T0 声位0不在 World 的1—100尺内、终局假设未定义的全城共同载体。新版仍一次生成 S1/S2/S3，但强制 `Authority-Compilation Trace`，要求每个开篇动作、尺位置和远期复合都从明确字段推出。

对新版 S1/S2/S3 分别判断：
1. 第一章每个超常动作是否能从 World / Interface / Ontology / Origin / Power 直接推出；trigger 是否已满足。
2. Interface 是否只记录/传播/改变社会后果，还是偷偷复制或放大 Power。
3. T0 精确位置是否被 protagonist-blind World grammar 容纳。
4. 20章与百章图景是否只复合已有规则，还是假设共同载体、无限复制或新能力。
5. `Authority-Compilation Trace` 是否引用精确字段并真的闭合，还是只声称合法。
6. 候选是否仍然大胆、Changed Verbs 清楚；不要因为安全审计把“奇怪/激进”本身当缺点。

严格格式：
# PREMISE COMPILE TRACE AUDIT
## Old S2 Failure Baseline
## S1
- Verdict: PASS / CONDITIONAL PASS / FAIL
- Exact conflicts:
- Boldness preserved:
## S2
（同结构）
## S3
（同结构）
## Architecture Verdict
明确区分：搜索器、compile-trace 输出合同、lane-specific frozen contract、当前 production freeze。不得建议新增 Agent/Judge/Hard Gate。

# OLD S2
{old_s2}

# OLD S2 FROZEN-CONTRACT STORY RESULT
{conflict}

# NEW S1/S2/S3
{read(EXP / 'CANDIDATES.md')}
"""
    (EXP / "AUDIT_PROMPT.md").write_text(audit_prompt, encoding="utf-8")
    audit_meta = run_acp(
        EXP / "AUDIT_PROMPT.md",
        EXP / "AUDIT_ACP.json",
        EXP / "AUDIT.md",
        model="gpt-5.6-terra",
        label="premise-compile-trace-v2-fast-multiworld-audit",
    )
    (EXP / "RUN_SUMMARY.json").write_text(
        json.dumps(
            {
                "case": "fast_multiworld",
                "treatment": "single-pass authority-compilation trace v2",
                "production_modified": False,
                "candidate_ids": list(candidates),
                "structural_check": structural,
                "forge": forge_meta,
                "audit": audit_meta,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"forge": forge_meta, "audit": audit_meta}, ensure_ascii=False))


if __name__ == "__main__":
    main()
