from pathlib import Path
base=Path(r'books/real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1')
files=[
 base/'planning/story-11-20/response.md',
 base/'planning/story-11-20/FINAL_STORY_PROGRAM.md',
 base/'STORY_PROGRAM_11_20.md',
]
old='宁烬本可带剩余盐货退回断脊渡，却拒绝用逆月盐封住自己在镜海界留下的旧伤。'
new='宁烬本可留在新生院，用现有逆月盐把镜海界留下的旧伤压到返伤相过去，安全退出这次争夺；他却拒绝封住这道旧伤。'
old2='永久可能性只能在宁烬放弃安全退出、亲自承受两地旧伤生长并完成骨芽廊道因果后取得'
new2='永久可能性只能在宁烬放弃留在新生院以逆月盐安全躲过返伤相、亲自承受两地旧伤生长并完成骨芽廊道因果后取得'
for p in files:
    if not p.exists(): continue
    t=p.read_text(encoding='utf-8')
    if old not in t: print('MISS1',p)
    else: t=t.replace(old,new)
    if old2 not in t: print('MISS2',p)
    else: t=t.replace(old2,new2)
    p.write_text(t,encoding='utf-8')

files2=[base/'planning/outline-11-20/response.md', base/'planning/outline-11-20/BOOK_PLANNED.md', base/'BOOK_PLAN_11_20.md']
old3='宁烬本可带剩余盐货退回断脊渡，却拒绝用逆月盐封住自己在镜海界留下的旧伤；'
new3='鹿闻灯明确可以让宁烬留在新生院，用现有逆月盐把镜海界留下的旧伤压到返伤相过去，安全退出这次争夺；宁烬却拒绝封住旧伤，'
old4='宁烬放弃安全返回与保全旧伤原样的路线；'
new4='宁烬放弃留在新生院用逆月盐安全躲过返伤相、保全旧伤原样的路线；'
for p in files2:
    if not p.exists(): continue
    t=p.read_text(encoding='utf-8')
    if old3 not in t: print('MISS3',p)
    else: t=t.replace(old3,new3)
    if old4 not in t: print('MISS4',p)
    else: t=t.replace(old4,new4)
    p.write_text(t,encoding='utf-8')
print('done')
