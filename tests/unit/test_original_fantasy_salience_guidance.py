from pathlib import Path


def test_original_skills_preserve_exceptional_advantage_and_scope_realism() -> None:
    root = Path(__file__).parents[2]
    reader_skill = (
        root
        / ".agents"
        / "skills"
        / "interpret-original-reader-kernel"
        / "SKILL.md"
    ).read_text(encoding="utf-8")
    bootstrap_skill = (
        root / ".agents" / "skills" / "bootstrap-original-novel" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert "realism_anchors` 描述作者要求保持可信的局部摩擦与后果" in reader_skill
    assert "普通人无法复制" in reader_skill
    assert "反事实替代检查" in reader_skill
    assert "主角因此能做到什么普通人做不到的事情" in bootstrap_skill
    assert "删除特殊机制后" in bootstrap_skill
    assert "现实锚点只约束作者明确要求可信" in bootstrap_skill
    assert "selected Core semantic identity" in bootstrap_skill
    assert "READER-PROMISE PAYOFF ENVIRONMENT" in bootstrap_skill
    assert "Core Identity Self-Check" in bootstrap_skill
    assert "Core Replacement Test" in bootstrap_skill
    assert "Core-internal open questions" in bootstrap_skill
    assert "限制、燃料、维护、暴露和社会反应是后果" in bootstrap_skill


def test_foundation_development_preserves_fantasy_amplitude() -> None:
    root = Path(__file__).parents[2]
    bootstrap_skill = (
        root / ".agents" / "skills" / "bootstrap-original-novel" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert "FANTASY AMPLITUDE MUST NOT SILENTLY DECREASE DOWNSTREAM" in bootstrap_skill
    assert "FUNCTIONAL CONTINUITY != PHYSICAL REALISM CEILING" in bootstrap_skill
    assert "AMPLIFYING THE CONFIRMED CORE" in bootstrap_skill
    assert "ADDING A COMPETING SECOND CORE" in bootstrap_skill
    assert "ability_unlock_model" in bootstrap_skill
    assert "artifact_or_equipment_model" in bootstrap_skill
    assert "next_ceiling_model" in bootstrap_skill
    assert "verification_modes" in bootstrap_skill
    assert "PayoffChannel" in bootstrap_skill
    assert "FANTASY AMPLITUDE CHECK" in bootstrap_skill
    assert "PROFESSIONAL ENGINEER REPLACEMENT TEST" in bootstrap_skill


def test_original_studio_surfaces_fantasy_salience_at_review_points() -> None:
    root = Path(__file__).parents[2]
    template = (
        root / "src" / "novel_authoring" / "web" / "templates" / "original_studio.html"
    ).read_text(encoding="utf-8")

    assert "现实锚点只约束这里明确列出的部分" in template
    assert "主角为什么特殊" in template
    assert "主要怎么兑现" in template
    assert "特殊机制如何成为主要兑现" in template
    assert "下一能力上限" in template
    assert "能力 / 资产成长" in template
    assert "能力验证" in template
    assert "成长承诺" in template
    assert "成长代价（如适用）" in template
    assert "代价 / 约束（如适用）" in template
    assert "首个资源瓶颈（如适用）" in template
    assert "人物行动、核心兑现、不可逆变化与后续空间选择" in template
    assert "主要冲突 / 阻力" in template
    assert "必须付出的代价" not in template
    assert "{% if item.required_cost and item.required_cost.strip() %}" in template
    assert "{% if phase.first_resource_bottleneck.strip() %}" in template
    assert "<small>代价：{{ item.required_cost }}</small>" not in template
