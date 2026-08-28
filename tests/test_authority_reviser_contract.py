from __future__ import annotations

from story_mvp.prompts import DEFAULT_PROMPT_TEMPLATES, generate_prompt


def test_authority_reviser_requires_semantic_conflict_sweep_and_value_relocation() -> None:
    template = DEFAULT_PROMPT_TEMPLATES["authority_reviser"]

    assert "Authority Conflict Sweep｜同一维度冲突必须清零" in template
    assert "Curator / Primary 不能折中或覆盖 Frozen Authority" in template
    assert "必须处理**全部出现位置**" in template
    assert "判断看语义，不看关键词" in template
    assert "远程召回、跨距离沿影子回收或无需重新碰面的合并机制" in template
    assert "Primary 只写了“凝影了 / 通过了 / 被记名”等现象或本地术语" in template
    assert "补一次最短的新档位直称" in template
    assert "修订后再做一次内部 final sweep" in template
    assert "Value-Preserving Relocation｜修事实不顺手磨掉高价值体验" in template
    assert "Sentence-level salvage" in template
    assert "最近的合法时点" in template
    assert "不要把整段一起删" in template
    assert "周围 process carrier 仍按 Attention Reallocation 正常压缩" in template
    assert "不能为了保住好句而继续保留错误机制" in template


def test_authority_reviser_prompt_keeps_frozen_power_and_primary_draft_under_new_contract() -> None:
    character = """# CHARACTER CARD

## POWER CORE｜Frozen Authority

POWER_RULE_MARKER：分开期间经验互不干扰，重新接触后才一次性回流。

## HUMAN CORE｜Frozen Authority

HUMAN_RULE_MARKER

## Composition Boundary
"""
    prompt = generate_prompt(
        mode="authority_reviser",
        template="",
        book_content="",
        character_card=character,
        current_outline="触发事件：A\n推动事件的人：B\n主角行动：C\n对手或世界反应：D\n直接结果：E\n状态变化：F\n叙事功能：G\n结尾推动力：H",
        curator_response="# Curated Chapter Context\n\nCURATOR_MARKER",
        primary_draft="# 正式正文\n\nPRIMARY_MARKER：分开时实时感到另一边疼痛。",
    )

    assert "Authority Conflict Sweep｜同一维度冲突必须清零" in prompt
    assert "POWER_RULE_MARKER" in prompt
    assert "HUMAN_RULE_MARKER" in prompt
    assert "CURATOR_MARKER" in prompt
    assert "PRIMARY_MARKER" in prompt
    assert prompt.index("POWER_RULE_MARKER") < prompt.index("PRIMARY_MARKER")
