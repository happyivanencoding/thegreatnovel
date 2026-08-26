from pathlib import Path
p=Path('tests/test_mvp.py')
s=p.read_text(encoding='utf-8')
repls={
'''    assert "代价或余波（可选）" in template
    assert "本批核心幻想兑现" in template
    assert "不要求每章都成长或结算" in template
''':'''    assert "代价或余波（可选）" in template
    assert "Block Delta" in template
    assert "相对本块开始" in template
    assert "不要求每章都成长或结算" in template
    assert "本批核心幻想兑现" not in template
''',
'''    assert "核心幻想是否仍在兑现" in prompt
    assert "一级成长是否仍是主轴" in prompt
    assert "幻想盈余是否为正" in prompt
''':'''    assert "核心幻想是否仍在兑现" in prompt
    assert "长期成长承诺是否仍在轨" in prompt
    assert "不要求最近十章必须升级" in prompt
    assert "幻想盈余是否为正" in prompt
''',
'''    assert "## 0. 本书成长基因图" in prompt
    assert "已批准幻想不变量" in prompt
    assert "主角核心欲望与超越" in prompt
    assert "一级成长主轴" in prompt
    assert "核心优势阶段升格" in prompt
    assert "主循环" in prompt
''':'''    assert "## 0. 本书成长基因图" in prompt
    assert "已批准幻想不变量" in prompt
    assert "已批准长期成长兑现" in prompt
    assert "已批准长期后果" in prompt
    assert "数量由 Power growth grammar 与 Story Program 决定" in prompt
    assert "至少说明三次" not in prompt
''',
'''    outline = DEFAULT_PROMPT_TEMPLATES["outline"]
    for marker in ("### 一级成长主轴", "### 二级收益与反哺", "### 主循环", "### 成本节奏"):
        assert marker in outline
    review = DEFAULT_PROMPT_TEMPLATES["review"]
    assert "一级成长是否仍是主轴" in review
''':'''    outline = DEFAULT_PROMPT_TEMPLATES["outline"]
    for marker in ("### 已批准长期成长兑现", "### 已批准长期后果", "Block Delta", "Growth is a longitudinal invariant, not a per-block form requirement"):
        assert marker in outline
    for retired in ("### 一级成长主轴", "### 二级收益与反哺", "### 主循环", "### 成本节奏"):
        assert retired not in outline
    review = DEFAULT_PROMPT_TEMPLATES["review"]
    assert "长期成长承诺是否仍在轨" in review
    assert "Growth is longitudinal, not a ten-chapter tax" in review
'''
}
for old,new in repls.items():
    count=s.count(old)
    assert count==1,(count,old[:80])
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
