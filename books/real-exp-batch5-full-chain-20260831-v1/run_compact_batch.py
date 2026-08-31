from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
BASE_SCRIPT = HERE / "run_experiment.py"
spec = importlib.util.spec_from_file_location("batch5_base", BASE_SCRIPT)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)

from story_mvp.hybrid_runtime import extract_primary_draft, extract_primary_fact_summary
from story_mvp.prompts import DEFAULT_PROMPT_TEMPLATES, generate_prompt, parse_canon_memory
from story_mvp.storage import apply_state_delta_to_book, parse_book_sections, validate_book_content_for_save, validate_chapter_body_for_save

OUT = HERE / "treatment_compact_batch5_primary"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def write(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s.rstrip() + "\n", encoding="utf-8")


def dump(p: Path, obj: object) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def book() -> str:
    return read(OUT / "BOOK.md")


def sections() -> dict[str, str]:
    return parse_book_sections(book())


def recent() -> str:
    return parse_canon_memory(sections()["status"]).get("recent_summaries", "").strip()


def previous(n: int) -> str:
    return read(OUT / "chapters" / f"chapter-{n:04d}.md").strip() if n > 1 else ""


def rdir(n: int) -> Path:
    d = OUT / "runs" / f"chapter-{n:04d}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def build_compact_prompt() -> str:
    chapter_packets: list[str] = []
    for n in range(1, 6):
        cd = base.run_dir(base.CONTROL, n)
        director = read(cd / "director_response.md").strip()
        curator = read(cd / "curator_response.md").strip()
        chapter_packets.append(
            f"""# CHAPTER {n} PACKET

+## APPROVED CHAPTER PLAN
+{base.PLANS[n]}
+
+## LUNA DIRECTOR
+{director}
+
+## LUNA CURATOR
+{curator}
+""".replace("\n+", "\n")
        )

    return f"""{DEFAULT_PROMPT_TEMPLATES['primary_writer'].strip()}

# COMPACT BATCH-5 PRIMARY｜FORMAL FULL-CHAIN TREATMENT

你在一次 Terra-high 会话里连续写第1—5章 Primary Draft。下面共享 Authority 只出现一次；每章只重复真正章特异的 Plan + Luna Director + Luna Curator。这是为了测试“五章连续认知窗口”，不是让你把五份任务压缩成提纲。

## 输出展开强度
- 五章都必须是可直接交给 Authority Reviser 的完整中文男频小说正文，不是剧情摘要。
- 以当前 production Terra 单章的正常展开强度为准：动作、空间、对话、欲望、Reward 都要真正发生在场景里。
- 五章合计正文目标约 9,000—13,000 个中文字符；章节可按事件自然长短浮动。不要为了赶完五章缩成 1,000 字符级梗概。
- 不因看见后续 Packet 提前兑现未来章；写完第N章后，你刚写的正文就是第N+1章唯一最新前文。

## Handoff / Canon
- 章边界不是场景边界。上一章结束在追杀、堵路、攻击、坠落、门关闭、当场选择时，下一章必须从该即时局面直接继续或用具体动作桥接。
- 第4→5章：裴照临斩桥堵路、后方追兵逼近是 continuity debt。必须使用已存在的追兵、倒悬城地形、镜离/澜生上下两处动作完成具体脱身；禁止临时新增“城内禁杀”、强敌无因果放行、传送规则。
- 共享 Frozen Authority > 每章 Plan > Director > Curator 的实现建议。Curator 如果带着此前逐章实验中产生的非必要临时事实，而它与 APPROVED CHAPTER PLAN 的首次取得/结果冲突，以 Approved Plan 为准，不把实验性旧实现升级成 Canon。
- 宁烬第1—5章始终灵海3重，不能提前获得永久双真/双在；裴照临始终灵海9重且真实更强。
- NPC 不得知道余门的隐藏永久保留、递归复合或私有触发机制。

# SHARED FROZEN WORLD AUTHORITY
{base.WORLD}

# SHARED FROZEN CHARACTER AUTHORITY
{base.CHARACTER}

# SHARED 5-CHAPTER BLOCK
{base.LONG_PLAN}

# SHARED PROSE / COMMERCIAL DIRECTION
成熟中文男频玄幻。优先抢、逃、打、赌、拿到手、关系换位与具体奇观。不要工程/治理/登记式展开；不要用概念总结替代规则在动作中的实现。宁烬爱钱、敢押、要面子，但不要每段都重复“值多少钱”。镜离冷，澜生冲，裴照临少说且靠实力压迫。

{"\n\n".join(chapter_packets)}

# FIXED OUTPUT FORMAT
恰好输出五个一级标题，不加总审计：
# BATCH CHAPTER 1
## 正式正文
...
## 章节事实摘要
...
依次到 # BATCH CHAPTER 5。
"""


def parse_batch(text: str) -> dict[int, tuple[str, str]]:
    out: dict[int, tuple[str, str]] = {}
    pat = re.compile(r"(?ms)^# BATCH CHAPTER ([1-5])\s*$\n(.*?)(?=^# BATCH CHAPTER [1-5]\s*$|\Z)")
    for m in pat.finditer(text):
        n = int(m.group(1))
        block = m.group(2)
        pm = re.search(r"(?ms)^## 正式正文\s*$\n(.*?)(?=^## 章节事实摘要\s*$|\Z)", block)
        fm = re.search(r"(?ms)^## 章节事实摘要\s*$\n(.*)$", block)
        if not pm or not fm:
            raise RuntimeError(f"chapter {n} missing body/facts")
        body = pm.group(1).strip()
        facts = fm.group(1).strip()
        validate_chapter_body_for_save(body)
        out[n] = (body, facts)
    if set(out) != set(range(1, 6)):
        raise RuntimeError(f"parsed chapters {sorted(out)}")
    return out


def diff_metrics(a: str, b: str) -> dict:
    import difflib
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    changed = [op for op in sm.get_opcodes() if op[0] != "equal"]
    return {
        "similarity": round(sm.ratio(), 4),
        "edit_blocks": len(changed),
        "changed_chars_primary": sum(i2-i1 for tag,i1,i2,j1,j2 in changed),
        "changed_chars_final": sum(j2-j1 for tag,i1,i2,j1,j2 in changed),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "chapters").mkdir(exist_ok=True)
    if not (OUT / "BOOK.md").is_file():
        write(OUT / "BOOK.md", base.base_book())
    calls: list[dict] = []

    prompt = build_compact_prompt()
    write(OUT / "batch_primary_prompt.md", prompt)
    resp = base.run_acp(
        OUT / "batch_primary_prompt.md",
        OUT / "batch_primary_acp.json",
        OUT / "batch_primary_response.md",
        model="gpt-5.6-terra",
        effort="high",
        label="batch5-compact-primary",
        call_log=calls,
    )
    batch = parse_batch(resp)
    dump(OUT / "PRIMARY_LENGTHS.json", {str(n): len(batch[n][0]) for n in range(1,6)})

    for n in range(1, 6):
        d = rdir(n)
        primary_body, primary_fact = batch[n]
        write(d / "batch_primary_body.md", primary_body)
        write(d / "batch_primary_fact.md", primary_fact)
        director = read(base.run_dir(base.CONTROL, n) / "director_response.md").strip()
        curator = read(base.run_dir(base.CONTROL, n) / "curator_response.md").strip()
        common = dict(
            book_content=book(),
            world_vision=base.WORLD,
            world_expansions="",
            character_card=base.CHARACTER,
            current_long_block=base.LONG_PLAN,
            previous_chapter_text=previous(n),
            current_outline=director,
            current_chapter_plan=base.PLANS[n],
            recent_summaries=recent(),
            chapter_number=n,
            creative_direction="Compact Batch-5 Primary formal treatment；逐章 Authority Reviser + State，Treatment rolling Canon 为已发生事实。",
        )
        rp = generate_prompt(
            mode="authority_reviser",
            template="",
            curated_context=curator,
            curator_response=curator,
            primary_draft=primary_body,
            primary_writer_response=f"# 正式正文\n\n{primary_body}\n\n# 章节事实摘要\n\n{primary_fact}",
            **common,
        )
        write(d / "reviser_prompt.md", rp)
        rr = base.run_acp(
            d / "reviser_prompt.md", d / "reviser_acp.json", d / "reviser_response.md",
            model="gpt-5.6-luna", effort="high", label=f"batch5-compact-ch{n:02d}-reviser", call_log=calls,
        )
        final = extract_primary_draft(rr).strip()
        validate_chapter_body_for_save(final)
        write(d / "final_body.md", final)
        write(OUT / "chapters" / f"chapter-{n:04d}.md", final)
        final_fact = extract_primary_fact_summary(rr).strip()
        sp = generate_prompt(mode="state_delta", template="", book_content=book(), recent_summaries=recent(), chapter_number=n, chapter_prose=final, chapter_fact_summary=final_fact)
        write(d / "state_prompt.md", sp)
        sr = base.run_acp(
            d / "state_prompt.md", d / "state_acp.json", d / "state_response.md",
            model="gpt-5.6-luna", effort="low", label=f"batch5-compact-ch{n:02d}-state", call_log=calls,
        )
        updated = apply_state_delta_to_book(book(), n, sr)
        validate_book_content_for_save(updated)
        write(OUT / "BOOK.md", updated)
        print(f"COMPACT CH{n} DONE chars={len(final)}", flush=True)

    compact = "\n\n".join(read(OUT / "chapters" / f"chapter-{n:04d}.md").strip() for n in range(1,6))
    write(OUT / "CHAPTERS_01_05.md", compact)
    control = read(base.CONTROL / "CHAPTERS_01_05.md")

    story_prompt = f"""你是独立中文男频正文盲评员。A/B是同一冻结上游的两个正式 full-chain 最终稿，不知道生成拓扑。不要按长度本身选，但如果某版把应当场景化的动作、对白、奇观、Reward压成摘要，要明确扣分。\n\n比较连续阅读欲、人物具体性、镜海规则可读性、动作因果、对白、爽点/Reward、裴照临压迫、4→5章桥接、AI式总结、100章以上底稿潜力。明确总冠军 A/B/TIE，给3—6条具体证据。\n\n# VERSION A\n{compact}\n\n# VERSION B\n{control}\n"""
    write(OUT / "judge_story_prompt.md", story_prompt)
    base.run_acp(OUT / "judge_story_prompt.md", OUT / "judge_story_acp.json", OUT / "JUDGE_STORY.md", model="gpt-5.6-luna", effort="high", label="batch5-compact-judge-story", call_log=calls)

    authority_prompt = f"""你是独立 TGN Authority / Continuity 盲审。只按冻结 World/Character/Plans 审最终稿A/B，不猜拓扑。\n\n检查真实硬问题：主事件/胜负/Reward改写；灵海3重/9重漂移；提前永久双真；NPC偷知余门；4→5即时堵路无bridge；临时方便规则；持有物/伤势/关系跨章冲突；未来事实提前泄漏。分别给 HARD PROBLEMS 数量与证据，再选 Authority 更可靠的 A/B/TIE。最后单列 Stale 痕迹；没有写NONE。不要制造问题。\n\n# WORLD\n{base.WORLD}\n\n# CHARACTER\n{base.CHARACTER}\n\n# PLANS\n{"\n\n".join(base.PLANS[n] for n in range(1,6))}\n\n# VERSION A\n{control}\n\n# VERSION B\n{compact}\n"""
    write(OUT / "judge_authority_prompt.md", authority_prompt)
    base.run_acp(OUT / "judge_authority_prompt.md", OUT / "judge_authority_acp.json", OUT / "JUDGE_AUTHORITY.md", model="gpt-5.6-terra", effort="high", label="batch5-compact-judge-authority", call_log=calls)

    edit = {}
    for n in range(1,6):
        edit[str(n)] = diff_metrics(read(rdir(n)/"batch_primary_body.md").strip(), read(rdir(n)/"final_body.md").strip())
    primary_wall = sum(float(r.get("wall_seconds") or 0) for r in calls if r["label"] == "batch5-compact-primary")
    reviser_wall = sum(float(r.get("wall_seconds") or 0) for r in calls if r["label"].endswith("-reviser"))
    state_wall = sum(float(r.get("wall_seconds") or 0) for r in calls if r["label"].endswith("-state"))
    control_metrics = json.loads(read(HERE / "METRICS.json"))
    dc = control_metrics["stage_sums_seconds"]["control_director"] + control_metrics["stage_sums_seconds"]["control_curator"]
    metrics = {
        "prompt_bytes": (OUT / "batch_primary_prompt.md").stat().st_size,
        "primary_lengths": {str(n): len(batch[n][0]) for n in range(1,6)},
        "final_lengths": {str(n): len(read(OUT/"chapters"/f"chapter-{n:04d}.md").strip()) for n in range(1,6)},
        "walls": {
            "batch_primary": round(primary_wall,3),
            "reviser": round(reviser_wall,3),
            "state": round(state_wall,3),
            "observed_after_frozen_DC": round(primary_wall+reviser_wall+state_wall,3),
            "stage_cost_equivalent_with_same_control_DC": round(dc+primary_wall+reviser_wall+state_wall,3),
            "control_stage_sum": control_metrics["stage_sums_seconds"]["control_stage_sum"],
        },
        "reviser_edit_metrics": edit,
    }
    dump(OUT / "CALL_LOG.json", calls)
    dump(OUT / "METRICS.json", metrics)
    print(json.dumps(metrics, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
