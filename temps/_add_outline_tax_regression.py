from pathlib import Path
p=Path('tests/test_mvp.py'); s=p.read_text(encoding='utf-8')
anchor='''def test_growth_projection_is_three_lines_and_not_an_outline_gate() -> None:
'''
insert='''def test_outline_growth_is_longitudinal_not_a_block_or_batch_tax() -> None:
    outline = DEFAULT_PROMPT_TEMPLATES["outline"]
    review = DEFAULT_PROMPT_TEMPLATES["review"]

    assert "Outline 是 **Story Program 的执行编译层，不是第二个 Story Program**" in outline
    assert "Block Delta" in outline
    assert "相对本块开始" in outline
    assert "没变化的维度直接省略" in outline
    assert "上一块已经发生的变化不要重复包装成这一块的新 Delta" in outline
    assert "Power、奖励、权限、地图都允许整块没有" in outline
    assert "不要求每十章都新增 Power、奖励、权限、地图" in outline

    for retired in (
        "一级成长变化：主角本人真正多能做了什么？",
        "收益与反哺：写本块结束后主角永久新增",
        "世界扩张：进入什么过去无法进入的地图",
        "本批一级成长目标：",
        "本批实际净收益：",
        "本批打开的新行动空间：",
        "至少说明三次真正改变力量层级",
    ):
        assert retired not in outline

    assert "不要求最近十章必须升级" in review
    assert "不要求每十章都新增 Power、奖励、权限、地图" in review


'''
assert s.count(anchor)==1
p.write_text(s.replace(anchor,insert+anchor,1),encoding='utf-8')
