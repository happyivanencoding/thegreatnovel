from pathlib import Path
import json
exp=Path(r'C:\dev\tgn-story-mvp\books\real-exp-prose-control-projection-ab-v2')
o=json.loads((exp/'blind_judge.json').read_text(encoding='utf-8'))
print('ok',o.get('ok'),'sec',o.get('wall_seconds'),'chars',len(o.get('text','')))
print('--- JUDGE ---')
print(o.get('text',''))
print('--- KEY ---')
print((exp/'blind_key.json').read_text(encoding='utf-8'))
print('--- METRICS ---')
print((exp/'metrics.json').read_text(encoding='utf-8'))
