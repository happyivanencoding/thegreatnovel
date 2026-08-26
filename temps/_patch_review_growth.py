from pathlib import Path
p=Path('src/story_mvp/prompts.py')
s=p.read_text(encoding='utf-8')
old='''## 一级成长是否仍是主轴
主角本人是否真正多能做了什么，还是只增加职位、资格、权限、责任、组织规模或外界评价。'''
new='''## 长期成长承诺是否仍在轨
不要求最近十章必须升级。检查 Story Program 已批准的纵向 Power / Capability progression 是否仍被忠实保留：如果真实质变原本就安排在本批，应由具体事件兑现；如果本批主要由关系、选择或世界事件成立，可以没有新的 Power Delta。真正需要警惕的是长期只增加职位、资格、权限、责任、组织规模或外界评价，却把已批准的主角成长永久挤掉。'''
assert s.count(old)==1, s.count(old)
p.write_text(s.replace(old,new,1),encoding='utf-8')
