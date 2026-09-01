from pathlib import Path
import shutil,re
root=Path(r'C:\dev\tgn-story-mvp\books')
src=root/'real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1'
dst=root/'real-prod-wo-shen-cang-zhu-jie-20ch-20260901-v1'
if dst.exists(): shutil.rmtree(dst)
(dst/'chapters').mkdir(parents=True)
for n in range(1,21):
    s=src/'chapters'/f'chapter-{n:04d}.md'
    if not s.is_file(): raise SystemExit(f'missing {s}')
    shutil.copy2(s,dst/'chapters'/s.name)
parts=[]
for n in range(1,21):
    parts.append((dst/'chapters'/f'chapter-{n:04d}.md').read_text(encoding='utf-8').strip())
full='\n\n'.join(parts).rstrip()+'\n'
(dst/'FULL_20_CHAPTERS.md').write_text(full,encoding='utf-8')
(dst/'FULL_20_CHAPTERS.txt').write_text(full,encoding='utf-8')
copy_map={
    'BOOK_AFTER_CH20.md':'BOOK_FINAL_CH20.md',
    'WORLD_VISION.md':'WORLD_VISION.md',
    'CHARACTER.md':'CHARACTER.md',
    'WORLD_EXPANSIONS.md':'WORLD_EXPANSION_11_20.md',
    'STORY_PROGRAM_11_20.md':'STORY_PROGRAM_11_20.md',
    'BOOK_PLAN_11_20.md':'BOOK_PLAN_11_20.md',
}
for a,b in copy_map.items():
    s=src/a
    if s.is_file(): shutil.copy2(s,dst/b)
print('dst',dst)
print('chapters',len(list((dst/'chapters').glob('chapter-*.md'))))
print('chars',len(full))
print('headings',sum(1 for x in parts if re.match(r'^第.{0,12}章',x)))
