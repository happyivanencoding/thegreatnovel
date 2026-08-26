from story_mvp.gbrain_retrieval import retrieve_gbrain
queries={
'SP01':('idea','同一个核心能力如何在几十章以后换一种剧情发动机，避免重复任务和重复解法'),
'SP02':('idea','多条长期人物线如何在一个高潮事件合流并共同结算，同时产生新的长期承诺'),
'SP03':('idea','角色离队成长后如何回归主线，让回归本身成为延迟兑现'),
'OL01':('outline','长线伏笔如何在几十章沉睡后被重新唤起，又不需要频繁提醒读者'),
'OL02':('outline','牺牲高潮如何同时结算关系线力量线和主线危机，并开启长期复活或新目标'),
'WV01':('world_vision','世界扩大怎样持续产生新的想进入想获得想成为想知道的欲望，而不是只扩大地图'),
'COUNTER':('idea','敌人如何根据主角已经公开的能力学会藏手诱导封锁并改变成功条件，而不是只变强'),
}
for key,(mode,q) in queries.items():
    r=retrieve_gbrain(mode=mode,query_override=q)
    print('\n###',key,mode)
    print('accepted',[(x['slug'],round(x['score'],4)) for x in r['accepted']])
    print('rejected_inactive',[x['slug'] for x in r['rejected'] if '未启用' in x['reason']][:3])
