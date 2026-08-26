from pathlib import Path
p=Path('tests/test_mvp.py')
s=p.read_text(encoding='utf-8')
items=[
('''    assert "代价或余波（可选）" in template
    assert "本批核心幻想兑现" in template
    assert "不要求每章都成长或结算" in template''','''    assert "代价或余波（可选）" in template
    assert "Block Delta" in template
    assert "相对本块开始" in template
    assert "不要求每章都成长或结算" in template
    assert "本批核心幻想兑现" not in template'''),
('''    assert "核心幻想是否仍在兑现" in prompt
    assert "一级成长是否仍是主轴" in prompt
    assert "幻想盈余是否为正" in prompt''','''    assert "核心幻想是否仍在兑现" in prompt
    assert "长期成长承诺是否仍在轨" in prompt
    assert "不要求最近十章必须升级" in prompt
    assert "幻想盈余是否为正" in prompt'''),
('''    assert "## 0. 本书成长基因图" in prompt
    assert "已批准幻想不变量" in prompt
    assert "主角核心欲望与超越" in prompt
    assert "一级成长主轴" in prompt
    assert "核心优势阶段升格" in prompt
    assert "主循环" in prompt''','''    assert "## 0. 本书成长基因图" in prompt
    assert "已批准幻想不变量" in prompt
    assert "已批准长期成长兑现" in prompt
    assert "已批准长期后果" in prompt
    assert "数量由 Power growth grammar 与 Story Program 决定" in prompt
    assert "至少说明三次" not in prompt''')]
for old,new in items:
    print('count',s.count(old))
    assert s.count(old)==1
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
