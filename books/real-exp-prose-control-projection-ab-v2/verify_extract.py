from pathlib import Path
import sys
sys.path.insert(0,r'C:\dev\tgn-story-mvp\src')
from story_mvp.gbrain_retrieval import extract_abstract_content
root=Path(r'C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\reference-corpus\prose-controls')
for n in ['spatially-traceable-causality-v1.md','dialogue-state-pressure-v1.md','action-anchored-grounding-v1.md']:
    t=(root/n).read_text(encoding='utf-8'); a,b=extract_abstract_content(t)
    print(n,'suppression=', '动作、对白、物体变化或人物反应已经让意义成立时' in a,'writer_projection=', '## Writer Projection' in t,'abstract_chars=',len(a))
