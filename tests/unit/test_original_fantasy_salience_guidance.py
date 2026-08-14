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


def test_original_studio_surfaces_fantasy_salience_at_review_points() -> None:
    root = Path(__file__).parents[2]
    template = (
        root / "src" / "novel_authoring" / "web" / "templates" / "original_studio.html"
    ).read_text(encoding="utf-8")

    assert "现实锚点只约束这里明确列出的部分" in template
    assert "主角为什么特殊" in template
    assert "主要怎么兑现" in template
    assert "特殊机制如何成为主要兑现" in template
