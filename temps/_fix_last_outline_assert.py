from pathlib import Path
p=Path('tests/test_mvp.py')
s=p.read_text(encoding='utf-8')
old='    assert "通常 3—5 个只是密度参考" in prompt'
new='    assert "通常 3—5 个锚点只是密度参考" in prompt'
assert s.count(old)==1, s.count(old)
p.write_text(s.replace(old,new,1),encoding='utf-8')
