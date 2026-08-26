from pathlib import Path
import json,re
root=Path(r'books/real-exp-private-prototype-upstream-20260826-v3')
for stem,out in [('POWER','POWER_SEEDS.md'),('HUMAN','HUMAN_SEED.md')]:
    j=json.loads((root/f'{stem}_ACP.json').read_text(encoding='utf-8'))
    (root/out).write_text(j.get('text',''),encoding='utf-8')
    print(stem,'ok',j.get('ok'),'model',j.get('model'),'chars',len(j.get('text','')),'wall',j.get('wall_seconds'))
print('--- POWER HEADINGS ---')
for line in (root/'POWER_SEEDS.md').read_text(encoding='utf-8').splitlines():
    if line.startswith('# POWER'): print(line)
print('--- HUMAN HEADINGS ---')
for line in (root/'HUMAN_SEED.md').read_text(encoding='utf-8').splitlines():
    if line.startswith('# HUMAN'): print(line)
# hard isolation text checks
human=(root/'HUMAN_SEED.md').read_text(encoding='utf-8')
power=(root/'POWER_SEEDS.md').read_text(encoding='utf-8')
prototype_terms=['prism-wanderer-alpha','pwaalpha','Appetite lane','Behavior lane','Relationship lane','情欲与肉体吸引']
print('power prototype hits',{t:power.count(t) for t in prototype_terms if t in power})
# collect candidate short names from headings and see if leaked into human
names=[]
for m in re.finditer(r'^# POWER CANDIDATE \d+｜(.+)$',power,re.M): names.append(m.group(1).strip())
print('power names',names)
print('human power-name hits',{n:human.count(n) for n in names if n in human})
