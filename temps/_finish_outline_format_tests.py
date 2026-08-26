from pathlib import Path
p=Path('src/story_mvp/prompts.py'); s=p.read_text(encoding='utf-8')
s=s.replace('通常 3—5 个只是密度参考。每个锚点写清', '通常 3—5 个锚点只是密度参考。每个锚点写清', 1)
s=s.replace(
'具体剧情：用 2—4 句写具体人物、事件和主角行动；本章明确推进、转折或结算当前剧情块中的某个故事锚点，或完成必要且有故事价值的桥接。',
'具体剧情：用 2—4 句写具体人物、事件和主角行动；本章明确推进、转折或结算当前剧情块中的某个故事锚点，或完成必要且有故事价值的桥接。不要为了填章数，把一个锚点拆成连续几章同类操作步骤。',1)
p.write_text(s,encoding='utf-8')

p=Path('tests/test_mvp.py'); s=p.read_text(encoding='utf-8')
old='''    assert "通常 3—5 个锚点" in prompt
    assert "只有很短的剧情块可以 2 个" in prompt
    assert "这只是内容密度参考，不是 Hard Gate" in prompt
    assert "锚点是故事转折，不是场景分镜或操作步骤" in prompt
    assert "提高故事确定性，不是提高施工步骤确定性" in prompt
    assert "推进、转折或结算当前剧情块中的某个故事锚点" in prompt
    assert "不要为了填章数，把一个锚点拆成连续几章" in prompt
    assert "结果 / 状态变化" in prompt
    assert "结尾推动" in prompt
    assert "第一章开篇策略" in prompt
    assert "本批核心幻想兑现" in prompt
    assert "不要求每章都成长或结算" in prompt'''
new='''    assert "通常 3—5 个锚点只是密度参考" in prompt
    assert "每个剧情块是若干会改变局势的故事转折，不是实施步骤" in prompt
    assert "提高故事确定性，不是提高施工步骤确定性" in prompt
    assert "推进、转折或结算当前剧情块中的某个故事锚点" in prompt
    assert "不要为了填章数，把一个锚点拆成连续几章" in prompt
    assert "结果 / 状态变化" in prompt
    assert "结尾推动" in prompt
    assert "第一章开篇策略" in prompt
    assert "本批核心幻想兑现" not in prompt
    assert "不要求每章都成长或结算" in prompt'''
assert s.count(old)==1,s.count(old)
p.write_text(s.replace(old,new,1),encoding='utf-8')
