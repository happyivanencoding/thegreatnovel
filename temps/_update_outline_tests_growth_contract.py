from pathlib import Path
p=Path('tests/test_mvp.py'); s=p.read_text(encoding='utf-8')
old='''    outline = DEFAULT_PROMPT_TEMPLATES["outline"]
    for marker in ("### 一级成长主轴", "### 二级收益与反哺", "### 主循环", "### 成本节奏"):
        assert marker in outline
    assert "代价或余波（可选）" in outline
    assert "不强制每块失去或承担什么" in outline
    review = DEFAULT_PROMPT_TEMPLATES["review"]
    for marker in (
        "## 核心幻想是否仍在兑现",
        "## 一级成长是否仍是主轴",
        "## 幻想盈余是否为正",
        "## 冲突是否过度理性化",
        "## 世界是否被程序化",
    ):
        assert marker in review'''
new='''    outline = DEFAULT_PROMPT_TEMPLATES["outline"]
    for marker in (
        "### 已批准长期成长兑现",
        "### 已批准长期后果",
        "Block Delta",
        "Growth is a longitudinal invariant, not a per-block form requirement",
        "Power、奖励、权限、地图都允许整块没有",
    ):
        assert marker in outline
    for retired in ("### 一级成长主轴", "### 二级收益与反哺", "### 主循环", "### 成本节奏"):
        assert retired not in outline
    assert "代价或余波（可选）" in outline
    review = DEFAULT_PROMPT_TEMPLATES["review"]
    for marker in (
        "## 核心幻想是否仍在兑现",
        "## 长期成长承诺是否仍在轨",
        "## 幻想盈余是否为正",
        "## 冲突是否过度理性化",
        "## 世界是否被程序化",
        "Growth is longitudinal, not a ten-chapter tax",
    ):
        assert marker in review'''
assert s.count(old)==1, s.count(old)
p.write_text(s.replace(old,new,1),encoding='utf-8')
