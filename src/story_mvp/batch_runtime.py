"""Fixed 4–6 chapter production batching for narrative continuity.

This module is intentionally narrow: one planning packet, one Terra prose batch, one
Authority Delta pass, then ordinary per-chapter State Extraction after finalization.
It does not replace Story Program / Outline and does not introduce a generic workflow
engine.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Mapping

from .chapter_context import (
    build_chapter_context,
    project_frozen_human_core,
    project_frozen_power_core,
)
from .prompts import (
    ACCESS_PROVENANCE_RULE,
    READER_FIRST_PROSE_CONTRACT,
)
from .storage import parse_book_sections, validate_chapter_body_for_save


DEFAULT_BATCH_SIZE = 5
MIN_BATCH_SIZE = 4
MAX_BATCH_SIZE = 6
MAX_PATCHES_PER_CHAPTER = 4
MAX_PROSE_PATCHES_PER_BATCH = 15


@dataclass(frozen=True)
class BatchWindow:
    start_chapter: int
    size: int = DEFAULT_BATCH_SIZE

    def __post_init__(self) -> None:
        if self.start_chapter < 1 or self.start_chapter > 9999:
            raise ValueError("Batch 起始章节必须在 1 到 9999 之间")
        if self.size < MIN_BATCH_SIZE or self.size > MAX_BATCH_SIZE:
            raise ValueError("Production Batch 固定支持 4—6 章；默认 5 章")
        if self.end_chapter > 9999:
            raise ValueError("Batch 结束章节不能超过 9999")

    @property
    def end_chapter(self) -> int:
        return self.start_chapter + self.size - 1

    @property
    def chapter_numbers(self) -> tuple[int, ...]:
        return tuple(range(self.start_chapter, self.end_chapter + 1))


@dataclass(frozen=True)
class BatchDelta:
    patches: tuple[dict[str, Any], ...]
    upstream_conflicts: tuple[dict[str, Any], ...]


def _strip_model_preamble(text: str) -> str:
    clean = text.strip()
    if clean.startswith("```"):
        clean = re.sub(r"^```(?:json)?\s*", "", clean)
        clean = re.sub(r"\s*```$", "", clean)
    return clean


def _json_object(text: str) -> dict[str, Any]:
    clean = _strip_model_preamble(text)
    start = clean.find("{")
    end = clean.rfind("}")
    if start < 0 or end < start:
        raise ValueError("Batch Authority Delta 返回缺少 JSON object")
    try:
        value = json.loads(clean[start : end + 1])
    except json.JSONDecodeError as error:
        raise ValueError("Batch Authority Delta JSON 无法解析") from error
    if not isinstance(value, dict):
        raise ValueError("Batch Authority Delta 顶层必须是 JSON object")
    return value


def _extract_numbered_blocks(text: str, heading: str, window: BatchWindow) -> dict[int, str]:
    clean = text.strip()
    first = clean.find(f"# {heading} {window.start_chapter}")
    if first >= 0:
        clean = clean[first:]
    numbers = "|".join(str(number) for number in window.chapter_numbers)
    pattern = re.compile(
        rf"(?ms)^# {re.escape(heading)} ({numbers})\s*$\n(.*?)(?=^# {re.escape(heading)} (?:{numbers})\s*$|\Z)"
    )
    result = {int(match.group(1)): match.group(2).strip() for match in pattern.finditer(clean)}
    if tuple(sorted(result)) != window.chapter_numbers:
        raise ValueError(
            f"{heading} 必须恰好包含第{window.start_chapter}—{window.end_chapter}章"
        )
    return result


def parse_batch_primary_response(text: str, window: BatchWindow) -> dict[int, str]:
    blocks = _extract_numbered_blocks(text, "BATCH CHAPTER", window)
    result: dict[int, str] = {}
    for number, block in blocks.items():
        body = re.sub(r"^## 正式正文\s*\n", "", block).strip()
        validate_chapter_body_for_save(body)
        result[number] = body
    return result


def extract_batch_outline_plans(source: str, window: BatchWindow) -> dict[int, str]:
    """Deterministically extract approved Future-10 entries for one batch.

    ``source`` may be a full BOOK or a raw Outline artifact. The entries are not
    rewritten by another planning LLM before Primary sees them.
    """

    text = source.strip()
    if not text:
        raise ValueError("Batch 缺少已批准的 Future-10 / Outline")
    try:
        sections = parse_book_sections(text)
    except ValueError:
        sections = {}
    plan_text = str(sections.get("small_plan", "")).strip() or text

    heading = re.compile(r"(?m)^#{2,6}\s*第\s*(\d+)\s*章(?:\s*[：:].*)?\s*$")
    matches = list(heading.finditer(plan_text))
    result: dict[int, str] = {}
    wanted = set(window.chapter_numbers)
    for index, match in enumerate(matches):
        number = int(match.group(1))
        if number not in wanted:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(plan_text)
        result[number] = plan_text[match.start():end].strip()

    if tuple(sorted(result)) != window.chapter_numbers:
        missing = sorted(wanted - set(result))
        raise ValueError(f"Future-10 缺少 Batch 所需章节：{missing}")
    return result


def parse_batch_delta_response(text: str, window: BatchWindow) -> BatchDelta:
    value = _json_object(text)
    patches = value.get("patches", [])
    conflicts = value.get("upstream_conflicts", [])
    if not isinstance(patches, list) or not isinstance(conflicts, list):
        raise ValueError("Batch Authority Delta 的 patches / upstream_conflicts 必须是数组")
    if len(patches) > window.size * MAX_PATCHES_PER_CHAPTER:
        raise ValueError("Batch Authority Delta patch 过多；应停止而不是重写整批正文")

    normalized_patches: list[dict[str, Any]] = []
    for patch in patches:
        if not isinstance(patch, dict):
            raise ValueError("Batch Authority Delta patch 必须是 object")
        try:
            chapter = int(patch["chapter"])
            old = str(patch["old"])
            new = str(patch["new"])
            reason = str(patch.get("reason", "")).strip()
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Batch Authority Delta patch 字段无效") from error
        if chapter not in window.chapter_numbers or not old:
            raise ValueError("Batch Authority Delta patch 章节或 OLD 无效")
        normalized_patches.append(
            {"chapter": chapter, "old": old, "new": new, "reason": reason}
        )

    normalized_conflicts: list[dict[str, Any]] = []
    for conflict in conflicts:
        if not isinstance(conflict, dict):
            raise ValueError("upstream_conflicts 必须是 object 数组")
        chapter = int(conflict.get("chapter", 0))
        issue = str(conflict.get("issue", "")).strip()
        required = str(conflict.get("required_upstream", "")).strip()
        if chapter not in window.chapter_numbers or not issue or not required:
            raise ValueError("upstream_conflicts 字段无效")
        normalized_conflicts.append(
            {"chapter": chapter, "issue": issue, "required_upstream": required}
        )
    return BatchDelta(tuple(normalized_patches), tuple(normalized_conflicts))


def apply_batch_delta(
    chapters: Mapping[int, str], delta: BatchDelta, window: BatchWindow
) -> dict[int, str]:
    if tuple(sorted(chapters)) != window.chapter_numbers:
        raise ValueError("Batch Primary chapters 与窗口不一致")
    revised = {number: str(chapters[number]) for number in window.chapter_numbers}
    for patch in delta.patches:
        chapter = int(patch["chapter"])
        old = str(patch["old"])
        new = str(patch["new"])
        count = revised[chapter].count(old)
        if count != 1:
            raise ValueError(
                f"第{chapter}章 Batch Delta OLD 必须逐字且唯一匹配；实际 {count} 次"
            )
        revised[chapter] = revised[chapter].replace(old, new, 1)
    for body in revised.values():
        validate_chapter_body_for_save(body)
    return revised


def parse_batch_prose_delta_response(text: str, window: BatchWindow) -> BatchDelta:
    """Parse the narrow prose-only delta; it may never escalate into upstream facts."""

    delta = parse_batch_delta_response(text, window)
    if delta.upstream_conflicts:
        raise ValueError("Batch Prose Delta 不得报告或修复上游冲突")
    if len(delta.patches) > MAX_PROSE_PATCHES_PER_BATCH:
        raise ValueError("Batch Prose Delta patch 过多；应停止而不是进行全章润色")
    return delta


def compose_batch_deltas(
    chapters: Mapping[int, str],
    authority_delta: BatchDelta,
    prose_delta: BatchDelta,
    window: BatchWindow,
) -> tuple[dict[int, str], tuple[dict[str, Any], ...], tuple[dict[str, Any], ...]]:
    """Authority-first deterministic composition over one immutable Primary.

    Both deltas must have been generated from the same Primary. Authority patches are
    applied first. A prose patch survives only when its exact OLD still occurs once in
    the Authority-closed chapter; otherwise it is skipped, so prose can never override
    an Authority repair.
    """

    if authority_delta.upstream_conflicts:
        raise ValueError("Batch Authority Delta 仍有上游冲突，不能组合正文")
    if prose_delta.upstream_conflicts:
        raise ValueError("Batch Prose Delta 不得包含上游冲突")
    revised = apply_batch_delta(chapters, authority_delta, window)
    applied: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for patch in prose_delta.patches:
        chapter = int(patch["chapter"])
        old = str(patch["old"])
        new = str(patch["new"])
        count = revised[chapter].count(old)
        if count != 1:
            skipped.append({**patch, "match_count_after_authority": count})
            continue
        revised[chapter] = revised[chapter].replace(old, new, 1)
        applied.append(patch)
    for body in revised.values():
        validate_chapter_body_for_save(body)
    return revised, tuple(applied), tuple(skipped)


def build_batch_prose_delta_prompt(
    *,
    window: BatchWindow,
    primary_chapters: Mapping[int, str],
    book_content: str,
) -> str:
    """Build the independent Terra prose patch pass over the immutable Primary."""

    if tuple(sorted(primary_chapters)) != window.chapter_numbers:
        raise ValueError("Batch Primary chapters 与窗口不一致")
    prose_profile = build_chapter_context(
        book_content=book_content,
        chapter_number=window.start_chapter,
    ).prose_profile.strip()
    drafts = "\n\n".join(
        f"# CHAPTER {chapter} PRIMARY\n{primary_chapters[chapter].strip()}"
        for chapter in window.chapter_numbers
    )
    return f"""你是 TGN 的 Batch Prose Delta。你不是第二个 Writer，也不是 Authority Reviser；你只能对同一份 immutable Primary 做 preservation-first exact local patch。

唯一目标：只修当前已验证的三种 reader-facing 问题：
1. **Show-Then-Trust**：动作、对白、物件变化或现实后果已经让同一意义成立后，紧邻着又出现“这是他的选择 / 这意味着 / 他真正想要的是 / 从此关系变成 / 这才算……”等抽象二次判词；只删或改这个后置复述。若句子包含会改变下一动作的新判断，则不动。
2. **Paragraph Continuity**：同一个连续 beat 被机械切成很多一句一段。允许把相邻碎句重组为一个自然段，保留原来的每个动作、感知、对象、顺序和后果；合段是重组，不是压缩场景。
3. **Dialogue Continuity**：没有真实打断时，人物稳定“问一句—答四五个字—再问一句”，每句只报一个剧情字段。允许在同一局部交换内，把**已经存在的语义**重写成更完整的说话回合，让措辞、停顿和对应动作承载当下情绪；但不能减少真实试探、讨价、嘴硬、拒绝或关系摩擦的回合。

## Preservation Boundary
- **不能新增或删除任何 story beat。** 不改变事件身份、参与者、受伤者、被救对象、顺序、胜负、选择、结果、地点、时间、钱、奖励、身份、力量、物件取得/持有/去向、知识边界或关系状态。
- **不能新增任何过去事实。** 不准为了让人物更有感情补父母旧伤、童年旧情、上一趟死人、旧赠物、旧债、过去共同经历或未出现过的生活习惯。
- 不新增专名、数字、世界规则、能力边界、动机或“真正原因”；不把人物暂时判断升级成客观事实。
- 不因“更自然”改写已经自然的段落；不要做全章润色、辞藻升级、删减说明或重排剧情。
- 不以更短为目标；故事密度、对白摩擦、生活细节和社会反应不得少于底稿。
- 如果某处需要新增事实才能变自然，**不要 patch**。
- 典型每章 0—3 个 patch；整批最多 {MAX_PROSE_PATCHES_PER_BATCH} 个。没有真实问题就少改，不凑数量。

# PROSE PROFILE
{prose_profile or "（未提供；只按上述窄合同处理。）"}

# IMMUTABLE BATCH PRIMARY
{drafts}

只输出一个 JSON object；JSON 前后不要解释：
{{
  "patches": [
    {{"chapter": {window.start_chapter}, "old": "逐字且唯一的原文", "new": "局部替换文本", "reason": "只说明上述三类 prose 问题之一"}}
  ],
  "upstream_conflicts": []
}}
`old` 必须是同章逐字唯一片段；允许多段文本。不要输出全文，不要输出 chain-of-thought。
"""


def build_batch_primary_prompt(
    *,
    window: BatchWindow,
    batch_plans: Mapping[int, str],
    book_content: str,
    world_vision: str,
    world_expansions: str,
    character_card: str,
    previous_chapter_text: str = "",
) -> str:
    if tuple(sorted(batch_plans)) != window.chapter_numbers:
        raise ValueError("Approved Batch plans 与窗口不一致")
    authority_packets: list[str] = []
    shared_book_contract = ""
    shared_canon = ""
    shared_prose_profile = ""
    for chapter in window.chapter_numbers:
        packet = build_chapter_context(
            book_content=book_content,
            character_card=character_card,
            world_vision=world_vision,
            world_expansions=world_expansions,
            previous_chapter_text=(previous_chapter_text if chapter == window.start_chapter else ""),
            current_chapter_plan=batch_plans[chapter],
            chapter_number=chapter,
        )
        if not shared_book_contract:
            shared_book_contract = packet.book_contract.strip()
        if not shared_canon:
            shared_canon = packet.canon_context.strip()
        if not shared_prose_profile:
            shared_prose_profile = packet.prose_profile.strip()
        authority_packets.append(
            f"# CHAPTER {chapter} AUTHORITY\n"
            f"## SAFE WORLD\n{packet.world_authority.strip() or 'NONE'}\n"
            f"## READER RELEASE\n{packet.reader_release.strip() or 'NONE'}\n"
            f"## PROTECTED STORY EVENT\n{packet.protected_story_events.strip() or 'NONE'}"
        )

    plans = "\n\n".join(
        f"# BATCH PLAN {chapter}\n{batch_plans[chapter].strip()}"
        for chapter in window.chapter_numbers
    )
    authority_text = "\n\n".join(authority_packets)
    return f"""你是 TGN 的 Terra Primary Writer。一次连续写完第{window.start_chapter}—{window.end_chapter}章；只输出小说正文，不输出 Audit、状态、摘要或写作说明。

这次 Batch 的价值是短中程叙事预见：前章摆出的地形、物件、人物态度、Promise 和局部脑洞，可以在后章自然回收。不要把它写成 {window.size} 个分别启动的任务，也不要为了完成多章压缩成梗概。

{READER_FIRST_PROSE_CONTRACT}

## Batch Continuity
- 你自己刚写完的第N章正文就是第N+1章的直接前文；即时追杀、攻击、谈判、坠落、门正在关闭等不得在章缝里消失。
- 物品、钱、伤势、位置、关系和公开力量位置一旦改变，后章服从新状态。
- 不提前实现后章计划；但可以让上一章 Ending Handoff 的压力真实出现。
- 不为桥接新造禁杀规则、备用传送、强敌心软、免费救援或其它方便机制。
- 已经建立的人格不靠同一句口癖重复证明；让不同真实牵引随现场进入。
- `APPROVED BATCH PLAN` 里的“叙事功能”、策划层动机解释和主题判断只指导你把动作、选择与后果写对，不是正文台词或旁白；当前场面已经用动作与现实后果成立时，直接继续，不把这些策划语义再翻译一遍。**这只删除二次意义说明，不授权你缩掉 Plan 已自然产生的人物互动、关系摩擦、社会反应、生活纹理或动作 beat；段落重组也不能变成场景摘要。**
- 世界独有规则不仅服务解题：若 Batch Plan 已给具体人物命运/关系后果，让它通过人物选择真正进入故事。

# FROZEN POWER CORE
{project_frozen_power_core(character_card) or "（未提供。）"}

# FROZEN HUMAN CORE
{project_frozen_human_core(character_card) or "（未提供。）"}

# SHARED BOOK CONTRACT
{shared_book_contract or "（未提供；不得补造。）"}

# PROSE PROFILE
{shared_prose_profile or "（未提供；使用 Reader-First 基础表达合同。）"}

# STARTING CANON
{shared_canon or "（本窗口没有已发生 Canon 摘要；不要因此补造过去。）"}

# PER-CHAPTER AUTHORITY
{authority_text}

# PREVIOUS FINAL PROSE
{previous_chapter_text.strip() or "（无前章正文。）"}

# APPROVED BATCH PLANS
{plans}

固定输出：
# BATCH CHAPTER {window.start_chapter}
## 正式正文
<完整小说正文>

依次到 # BATCH CHAPTER {window.end_chapter}。
每章必须是完整小说章节；不要为了批量任务缩成摘要。
"""


def build_batch_delta_reviser_prompt(
    *,
    window: BatchWindow,
    batch_plans: Mapping[int, str],
    primary_chapters: Mapping[int, str],
    book_content: str,
    world_vision: str,
    world_expansions: str,
    character_card: str,
    story_program: str,
) -> str:
    if tuple(sorted(batch_plans)) != window.chapter_numbers:
        raise ValueError("Approved Batch plans 与窗口不一致")
    if tuple(sorted(primary_chapters)) != window.chapter_numbers:
        raise ValueError("Batch Primary chapters 与窗口不一致")

    authority_parts: list[str] = []
    for chapter in window.chapter_numbers:
        packet = build_chapter_context(
            book_content=book_content,
            character_card=character_card,
            world_vision=world_vision,
            world_expansions=world_expansions,
            current_chapter_plan=batch_plans[chapter],
            chapter_number=chapter,
        )
        authority_parts.append(
            f"# CHAPTER {chapter} AUTHORITY\n"
            f"## SAFE WORLD\n{packet.world_authority.strip() or 'NONE'}\n"
            f"## READER RELEASE\n{packet.reader_release.strip() or 'NONE'}\n"
            f"## PROTECTED STORY EVENT\n{packet.protected_story_events.strip() or 'NONE'}\n"
            f"## BATCH PLAN\n{batch_plans[chapter].strip()}"
        )
    drafts = "\n\n".join(
        f"# CHAPTER {chapter} PRIMARY\n{primary_chapters[chapter].strip()}"
        for chapter in window.chapter_numbers
    )
    authority_text = "\n\n".join(authority_parts)

    return f"""你是 TGN 的 Batch Authority Delta Reviser。你一次看到第{window.start_chapter}—{window.end_chapter}章完整 Primary，因此能处理跨章 stale；但你**禁止重写整章**。你的唯一正文修改形式是 exact local patch，代码应用后其余字符逐字保留。

目标：保留 Terra Batch 的小说味、人物声音、局部野劲和前后铺垫，同时恢复真正不能错的 Authority。

## 只修真实硬问题
- Frozen Authority / 已发生 Canon 冲突；
- 明确 Reader Release / RSE / Plan Result 完全漏失；
- `PROTECTED STORY EVENT` / RSE 的事件身份、单次性或内部顺序被改写，例如同一场“第一次失败 → 第二次同类动作修正”被拆成多局、另起回合或新增一次胜负；
- 已明确为同一件/唯一凭证的物件，在没有正文转移、归还或复制因果时同时出现在两处，或被第二次发放；
- 跨章物品首次取得、持有人、钱、伤势、位置、时间、力量位置 stale；
- 同一批已经写实发生的具体事件，其参与者身份、受伤者、被救对象、见证者或责任主体在后章被偷偷换人，例如前章明确甲被车辕压伤，后章却回忆成主角从车辕下救出乙；这种 Event Participant stale 也属于同一事实域硬冲突；
- Primary 为了让人物更有感情/更有生活感而新增 Authority 未批准的过去事实，例如父母旧伤、童年旧情、上一趟死人、旧赠物、旧债或早先共同经历；当前关系可以靠当下动作和已批准旧史写活，不能靠 retrospective backfill 偷造 Canon；
- Primary 凭空新增 Approved Plan / Canon 未授权的付款、奖金、报酬、赠予、资源到账或精确时间承诺；这些会进入 State，不是可自由补写的生活细节；
- 第N章关闭/拒绝一个关键边界后，第N+2章人物无因果出现在另一侧；
- 固定空间拓扑、能力边界或知识边界被写反；
- 人物一句话把当前安排升级成未授权客观世界机制。

不要因为“更清楚、更漂亮、更成熟、更商业”而 patch。不要清理口癖、二段论或润色；这些属于 Primary/Planning。不要把可接受的角色要求误判成物理规则。

## Hidden Relationship-History Boundary
`APPROVED STORY PROGRAM` 可能包含作者已批准、但尚未对读者/人物揭露的 Relationship-History Backfill。它是**一致性 Authority，不是自动公开 Authority**：
- 只有当前 `BATCH PLAN` / `PROTECTED STORY EVENT` / `READER RELEASE` / 已发生 Canon 明确安排或已经公开的那一层，才允许 patch 到 reader-facing 正文。
- 不能因为你看见“旧爱、亲缘、师徒、背叛、上一代遗留、隐藏身份”等后台真相，就替 Outline 提前揭露。
- 若 Primary 用全知断言直接写反一个尚未揭露的后台事实，只把断言改成**兼容当前表层认知的中性表达**；不要顺手写出隐藏答案。
- 已排程 reveal 若被 Primary 漏掉，则按既有 Plan / RSE 恢复；未排程的 future reveal 不属于本批硬修复。

{ACCESS_PROVENANCE_RULE}

## Authority Domain Sweep
发现一个硬冲突后，必须在同一批**扫描该事实域的所有出现位置**：例如天海在上不能只修一个“下方”，旧火屑与新奖励不能只修索要句却漏结算句。只修改真正受影响的位置，不扩大到其它文风。

## Upstream Conflict
如果硬问题的根因是 Approved Plan 自己缺少必要因果，而局部修复必须发明新传送、追踪、身份、奖励、胜负或世界机制，**不得 patch**。把它放进 `upstream_conflicts`，指出应该回到 Story / Outline 决定什么。这样做比“聪明地补一个合理机制”更正确。

## Patch Contract
- OLD 必须是当前章 Primary 中逐字存在且只出现一次的连续文本；不用省略号。
- NEW 只做硬修复所需的最小变化；允许在唯一锚点补一两句已批准事实。
- 最多 {window.size * MAX_PATCHES_PER_CHAPTER} 个 patch；达到这个数量仍闭不住时，停止扩写，报告 upstream conflict。
- 不输出完整正文。

# FROZEN POWER CORE
{project_frozen_power_core(character_card) or "NONE"}

# FROZEN HUMAN CORE
{project_frozen_human_core(character_card) or "NONE"}

# APPROVED STORY PROGRAM
{story_program.strip() or "NONE"}

# BOOK / CANON / OUTLINE
{book_content.strip()}

# PER-CHAPTER AUTHORITY
{authority_text}

# BATCH PRIMARY DRAFTS
{drafts}

只输出一个 JSON object；JSON 前后不要解释：
{{
  "patches": [
    {{"chapter": {window.start_chapter}, "old": "逐字原文", "new": "最小修正文", "reason": "具体硬问题"}}
  ],
  "upstream_conflicts": [
    {{"chapter": {window.start_chapter}, "issue": "无法局部合法修复的矛盾", "required_upstream": "Story / Outline 必须决定的最小事实"}}
  ]
}}
没有 patch / conflict 时对应数组为空。
"""
