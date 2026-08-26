from pathlib import Path
p=Path('tests/test_mvp.py'); s=p.read_text(encoding='utf-8')
repls={
'    assert "不强制每块失去或承担什么" in prompt':'    assert "Power、奖励、权限、地图都允许整块没有" in prompt',
'    assert "通常约 4—10 块" in prompt':'    assert "通常 3—5 个只是密度参考" in prompt',
'    assert "完整输出当前窗口的所有剧情块" in prompt':'    assert "完整输出从第1章到本窗口预计终点的所有自然剧情块" in prompt',
'    assert "覆盖第1章到本窗口预计终点" in prompt':'    assert "不用“后续类似”省略" in prompt',
'    assert "Director 可以直接执行的故事骨架" in prompt':'    assert "Story Program 的执行编译层，不是第二个 Story Program" in prompt',
'    assert "通常约 4—10 块" in outline':'    assert "完整输出从第1章到本窗口预计终点的所有自然剧情块" in outline',
'    assert "只投影到现有字段" in template':'    assert "只通过具体锚点与实际 Delta 自然显现" in template',
'    assert "这里只后验总结" in template':'    assert "只后验总结具体人物和事件已经自然形成的倾向" in template',
'    assert "直接写“暂不预设”" in template':'    assert "没有稳定主题时直接写“暂不预设”" in template',
'    assert "不参与生成世界 ontology、资源体系、敌人设计、能力升格或终局" in template':'    assert "不得反向生成世界 ontology、资源体系、敌人设计、能力升格或终局" in template',
}
for old,new in repls.items():
    c=s.count(old); print(c, old[:45]); assert c==1,(c,old)
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
