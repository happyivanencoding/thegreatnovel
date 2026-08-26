from pathlib import Path
p=Path('docs/SPLIT_CHARACTER_AUTHORITY.md')
s=p.read_text(encoding='utf-8')
old='''High-Value Acquisition and Compounding remain longitudinal craft principles, not stage taxes. When an acquisition really occurs it should be desirable, actually possessed/used, and continue to affect later story; prior gains should not vanish after one arc. Neither principle requires a fixed per-stage field.

Counterplay is learned after collision; enemies are not born merely as a mechanical counter to the protagonist.'''
new='''High-Value Acquisition and Compounding remain longitudinal craft principles, not stage taxes. When an acquisition really occurs it should be desirable, actually possessed/used, and continue to affect later story; prior gains should not vanish after one arc. Neither principle requires a fixed per-stage field.

Outline inherits the same authority boundary at finer resolution. It is an execution compiler for the approved Story Program, not a second Story Program. Each story block uses `Block Delta`: only dimensions that changed **relative to the start of that block** are written, and unchanged dimensions are omitted. A relationship/world-driven block may have no Power/Capability, Possession, or new-world delta at all; conversely, a Power change already scheduled by Story Program must be realized through concrete story anchors when its time arrives. Outline must not create micro-upgrades, filler rewards, permissions, or maps merely to complete a block form.

Counterplay is learned after collision; enemies are not born merely as a mechanical counter to the protagonist.'''
assert s.count(old)==1
p.write_text(s.replace(old,new),encoding='utf-8')
