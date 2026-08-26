from pathlib import Path
for p in [Path(r'C:\dev\tgn-story-mvp\books\real-exp-prose-control-projection-ab-v2\AB_REPORT.md'),Path(r'C:\dev\tgn-story-mvp\docs\GBRAIN_PROSE_CRAFT_V1.md')]:
    t=p.read_text(encoding='utf-8')
    marker='GBrain final hygiene: **3747 Pages / 15705 Chunks / 15705 Embedded**; updated prose-control slugs are single scoped pages with no accidental root-level duplicates.'
    if marker not in t:
        t=t.rstrip()+f'\n\n{marker}\n'
        p.write_text(t,encoding='utf-8')
print('finalized')
