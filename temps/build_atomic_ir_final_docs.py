from __future__ import annotations
import re, subprocess, shutil, json
from pathlib import Path
repo=Path(r'C:\dev\tgn-story-mvp')
out=repo/'temps'/'atomic-authority-ir-final-staging'
if out.exists(): shutil.rmtree(out)
out.mkdir(parents=True)
base='origin/principal_dev_new_sys'

def read_remote(path:str)->str:
    return subprocess.check_output(['git','show',f'{base}:{path}'],cwd=repo).decode('utf-8')
def write(path:str,text:str)->None:
    p=out/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n',encoding='utf-8')

# PROJECT_RULES: replace the Atomic tail of the latency paragraph only.
path='PROJECT_RULES.md';s=read_remote(path)
old=re.search(r'(低延迟优化优先做确定性上下文裁剪与失败恢复。[^\n]*?本轮明确不修改 ACP runner 与前端。)(?:\s*Atomic[^\n]*)?',s)
if not old: raise SystemExit('PROJECT_RULES latency paragraph missing')
atomic=''' Atomic 最终架构固定分成 `Atomic Authority Contract` 与 `Primary Preservation Map`：Hard Contract 只接受 Entity Registry + Frozen Mission / Canon / World / Power / Human / Reader Release 的可信结构化 artifact，Curator / Primary 只能提供 Runtime签发的 realization location、edit locality 与窄 protection hint，不能创建 Hard Fact、Source Conflict 或 Entity Identity。所有主体、物件、资源、力量与关系使用稳定 Entity ID / slot；不支持的章节直接走当前 Full Reviser，且同一不支持的 Gate 不得反向阻断 Full。禁止继续扩中文关键词 parser、禁止自由文本 Sidecar、禁止新增 LLM safety classifier；只有 native single-source Structured Director、自动 cross-book registry、repeat、Reader+Authority 与完整 fallback-adjusted E2E 同时过线后才可改变 production。'''
s=s[:old.start()]+old.group(1)+atomic+s[old.end():]
write(path,s)

# Runtime: replace old Atomic paragraphs/duplicates with one clean IR v1 section.
path='docs/CHAPTER_RUNTIME_AND_STATE.md';s=read_remote(path)
section='''### Atomic Authority IR v1 实验边界（2026-08-29）

旧 Atomic v0.3 只保留为 Boundary Discovery Experiment。正式架构是两个互不越权的产物：

```text
Atomic Authority Contract
  = Entity Registry + Frozen Mission / Canon / World / Power / Human / Reader Release IR

Primary Preservation Map
  = Runtime签发的 Primary fact evidence + blocker edit window + optional Curator fragment hint
```

Hard Contract 只接收 source-specific trusted artifacts：私有 issuer、normalized-fact SHA-256、稳定 Entity ID / slot、显式 from-state、dependency cycle 与 source conflict 校验。Curator / Primary / Reviser / Judge 不能创建 Hard Fact、Conflict 或 Identity；空 Contract 不 eligible；Registry / Fact / Contract / Preservation 均为不可变快照，序列化重载会重建 artifacts 并复核 digest、fact membership 与 Contract hash。

Preservation 默认依靠 Edit Locality，而不是 Desire / Surprise / Relationship detector。Evidence binding 由 Runtime 签发并绑定 Primary SHA-256；Curator只能给 editable window 内的窄 protection hint，不能伪装成 evidence、扩窗或改变 Contract。Gate 还会拒绝 paragraph-count shift 与 locked-paragraph drift。

两本书四章静态实验：4/4 source-pure、4/4 preflight eligible、4/4窗口外修改被阻止，平均只开放3.11%段落。57项 focused tests、22/22 Schema/runtime checks通过。自由文本 Director Sidecar 三版全部失败：verbose JSON wall +205.83%，compact JSON +147.41%，micro DSL +146.45%；compact blind 中Story 3:1偏原Director，Authority 3:1偏Sidecar。

正确下一步是 native `DirectorStructuredDecision`：模型只返回一份 canonical typed decision，Runtime用 Action/Narrative Registry渲染八字段Mission，并确定性生成Frozen Mission artifact；不存在第二份自由 `human_clause`。当前只有schema/unit evidence，没有真实模型Story/latency/E2E证据。Unsupported chapter绕过Atomic走现有Full；只有supported chapter才允许Delta → Gate → Full fallback → supported Gate。Production五节点不变。完整报告：`books/real-exp-atomic-authority-ir-20260829-v1/RESULTS.md`。

'''
# Replace from first old Atomic section (or old next-direction paragraph) to node duties.
start_candidates=[m.start() for m in re.finditer(r'(?m)^### Atomic (?:Chapter Obligations|Authority IR)',s)]
if start_candidates:
    start=min(start_candidates)
else:
    marker='下一代高潜方向不是再加一个 classifier'
    start=s.find(marker)
    if start<0: raise SystemExit('runtime Atomic start missing')
end=s.find('## 节点职责',start)
if end<0: raise SystemExit('runtime node duties missing')
# Remove stale lead paragraph immediately before Atomic when it says next high-potential obligations.
lead=s.rfind('\n',0,start)+1
prev=s[max(0,s.rfind('\n\n',0,start)):start]
if '下一代高潜方向不是再加一个 classifier' in prev:
    start=s.rfind('\n\n',0,start)+2
s=s[:start]+section+s[end:]
write(path,s)

# Methodology: replace Atomic paragraph.
path='docs/PIPELINE_METHODOLOGY_AND_VALUES.md';s=read_remote(path)
new_para='''Atomic 的稳定方法论进一步收敛为“**Authority Contract 与 Primary Preservation Map 分离**”。Hard Contract 只能由可信结构化 Frozen Authority artifacts 与 Entity Registry 合并产生；Curator / Primary 只做 Runtime签发的 realization location 与 edit locality，不能创建Fact、Conflict或Identity。商业价值默认通过锁住blocker窗口外正文保护，只有editable window本身承载已成功价值时才使用窄fragment hint。Unsupported chapter必须绕过Atomic走当前Full；supported Full才可post-gate。自由文本verbose/compact/micro Sidecar已经否决；下一步只能测试单一语义源的native structured Director。静态fixture、schema valid与Authority更强都不能替代真实模型Story blind、跨书coverage、repeat和完整fallback-adjusted E2E。'''
s,n=re.subn(r'Atomic (?:obligations 的稳定方法论|的稳定方法论进一步收敛为).*?(?=\n\n---)',new_para,s,flags=re.S)
if n==0:
    anchor='确定性删除 stale context 可以冻结；模型、effort、输出协议、并行语义或新 Agent 继续属于实验假设。'
    if anchor not in s: raise SystemExit('methodology anchor missing')
    s=s.replace(anchor,anchor+'\n\n'+new_para,1)
elif n>1:
    raise SystemExit(f'methodology Atomic sections={n}')
write(path,s)

# Handoff: replace all repeated 14.11 content with one authoritative section.
path='DEEP_CONTEXT_HANDOFF_FINAL.md';s=read_remote(path)
handoff='''### 14.11 Atomic Authority IR v1（2026-08-29）

用户对旧Atomic v0.3的关键修正被实验确认：`Atomic Authority Contract` 与 `Primary Preservation Map` 必须彻底拆开。Hard Contract只来自Entity Registry与Frozen Mission / Canon / World / Power / Human / Reader Release的可信typed artifacts；Curator/Primary只能提供realization位置与Edit Locality，不能定义Fact、Conflict或Identity。

稳定decision model：

1. Entity ID替代“Mission名字优先还是Primary名字优先”；正文名字/代词只作evidence mapping。
2. Runtime拥有fact ID、stable slot、source/mode/phase和cross-source dependency；terminal state-bearing transition必须有可验证from-state。
3. Artifact使用source-specific freezer、私有issuer与fact digest；空合同不eligible；Registry/Contract/Map不可变，Contract snapshot重载会复核provenance、membership、digest与hash。
4. Primary evidence由Runtime签发并绑定Primary SHA-256；Curator hint不能扩窗。Preservation校验同一Contract hash、paragraph topology和locked paragraph hashes。
5. Edit Locality是默认商业价值保护：blocker在P42–P43，只开放P42–P43；窗口外欲望、关系、Reward、Surprise不需要语义分类器。
6. 只有money/relationship promise/mystery/current action basis/ownership/active threat等被Authority明确标记的state-bearing history才是Hard，不登记所有旧对白。
7. Unsupported chapter直接走当前Full且不post-gate；supported Delta失败才Full fallback并supported re-gate。
8. Primary不看Atomic Pack；Normal Delta只在失败后看到具体blocker与窄locality。
9. verbose/compact/micro自由文本Sidecar全部失败；目标改为单一canonical `DirectorStructuredDecision`，Runtime双投影human Mission与Frozen Mission artifact，不保留第二份自由human clause。

证据：57项focused tests；两书四章4/4 source-pure/preflight eligible，平均editable 3.11%，窗口外4/4阻止；22/22 Schema/runtime checks；Sidecar wall分别+205.83%/+147.41%/+146.45%，compact blind Story 3:1偏Control、Authority 3:1偏Treatment。Native structured Director仅schema/unit-ready，真实模型Story/latency/最终正文未测；Full Reviser固定税尚未减少。最终分类：Architecture/static implementation PASS；free-text Sidecar FAIL；native model route与Atomic fast route NOT PRODUCTION。完整报告：`books/real-exp-atomic-authority-ir-20260829-v1/RESULTS.md`。
'''
first=re.search(r'(?m)^### 14\.11 Atomic .*$',s)
marker='\n---\n\n## 15. How to Work With the User'
end=s.find(marker,first.start() if first else 0)
if not first or end<0: raise SystemExit('handoff 14.11 boundary missing')
s=s[:first.start()]+handoff+s[end:]
write(path,s)

# Skill based on remote head.
path='.agents/skills/tgn-system-steward/SKILL.md';s=read_remote(path)
version=re.search(r'^version:\s*([^\n]+)',s,re.M)
if not version: raise SystemExit('skill version missing')
parts=version.group(1).strip().split('.')
parts[-1]=str(int(parts[-1])+1)
new_version='.'.join(parts)
s=s[:version.start(1)]+new_version+s[version.end(1):]
atomic_bullet='- Atomic 审计按 `references/atomic-authority-ir-protocol.md`：严格拆开 `Atomic Authority Contract` 与 `Primary Preservation Map`。Hard Contract只接收可信Frozen Authority artifacts与Entity Registry；Curator/Primary不得创建Fact、Conflict或Identity。Evidence binding必须由Runtime签发并绑定Primary hash，默认用Edit Locality锁住窗口外正文；unsupported章节绕过Atomic走当前Full；free-text Sidecar、中文关键词parser与LLM safety classifier均不得productionize；'
s,n=re.subn(r'- Atomic 审计按 `references/atomic-authority-ir-protocol\.md`：[^\n]*',atomic_bullet,s)
if n==0:
    anchor='- 延迟/成本审计先拆开 adopted node wall'
    pos=s.find(anchor)
    if pos<0: raise SystemExit('skill latency anchor missing')
    line_end=s.find('\n',pos)
    s=s[:line_end+1]+atomic_bullet+'\n'+s[line_end+1:]
elif n>1: raise SystemExit(f'skill atomic bullets={n}')
ref='- `references/atomic-authority-ir-protocol.md`'
if ref not in s:
    anchor='- `references/live-system-discovery.md`'
    pos=s.rfind(anchor)
    if pos<0: raise SystemExit('skill reference anchor missing')
    end=pos+len(anchor)
    s=s[:end]+'\n'+ref+s[end:]
write(path,s)

protocol='''# Atomic Authority IR Audit Protocol

> Stable architecture and experiment protocol. It does not authorize production wiring.

## 1. Separate the products

### Atomic Authority Contract

Hard facts may come only from trusted Entity Registry + Frozen Mission / Canon / World / Power / Human / Reader Release artifacts.

### Primary Preservation Map

May contain only Runtime-issued fact→paragraph evidence, blocker edit locality, locked paragraphs and narrow exact-fragment hints. It cannot create Hard Facts, identity or conflicts.

## 2. Trust boundary

- Use source-specific freezer constructors, private issuer and normalized-fact SHA-256.
- Reject direct/self-labelled artifacts, digest tampering, empty contracts and facts lacking artifact membership.
- Registry, Fact payload, Contract and Preservation Map are immutable snapshots.
- Snapshot reload reconstructs source artifacts and verifies fact membership, digest, conflicts/unsupported state and Contract hash.
- Curator diagnostics never enter Contract hash or become conflict.

## 3. Entity and state boundary

- Use stable Entity IDs; Primary names/pronouns never define canonical identity.
- Runtime owns fact IDs and canonical stable slots.
- Validate unknown entities/slots, self-dependency, cycles and same-slot conflicts.
- Terminal state-bearing transitions require explicit `from_state` and a compatible Canon pre-state.

## 4. Preservation boundary

- Primary evidence bindings are Runtime-issued and bound to Primary SHA-256.
- Curator may add ProtectionHint only; it cannot masquerade as Primary evidence or expand the edit window.
- Validation requires the same chapter and Contract hash.
- Reject paragraph-count shifts and any locked-paragraph hash drift.
- Protect desire/relationship/reward/surprise mainly by permission, not semantic detectors.

## 5. Director boundary

Target a native single-source `DirectorStructuredDecision`. Runtime uses Action/Narrative registries to render the human eight-field Mission and deterministic Frozen Mission artifact. Do not keep a second free semantic `human_clause`, free narrative paragraph or machine Sidecar.

Free-text verbose/compact/micro Sidecars are negative evidence and must not be revived.

## 6. Routing

```text
preflight unsupported → current Full Reviser, ungated by unsupported Atomic
preflight supported → Delta → Gate
    PASS → Final
    FAIL → Full Reviser → supported Gate
        PASS → Final
        FAIL → residual failure
```

Atomic is an acceleration layer, not a global hard gate.

## 7. Evidence standard

Report separately:

- source-purity and controlled negative tests;
- static fixture coverage;
- real native structured Director model behavior;
- Story + Authority blind;
- independent repeat;
- cross-book registry coverage;
- fallback-adjusted complete-route wall.

Static fixtures and schema validity do not prove model quality or production speed. A gate that refuses unsupported chapters is safe but not generalized.

## 8. Freeze / do not freeze

Freeze architecture, trust boundary, Entity/slot model, Edit Locality and unsupported bypass. Do not freeze hand-authored fixtures, Runtime surface registries, automatic paragraph locator, native Director quality, Full Reviser removal or any speed claim until real E2E evidence exists.
'''
write('.agents/skills/tgn-system-steward/references/atomic-authority-ir-protocol.md',protocol)

metadata={'skill_version':new_version,'base':base,'paths':[
 'PROJECT_RULES.md','docs/CHAPTER_RUNTIME_AND_STATE.md','docs/PIPELINE_METHODOLOGY_AND_VALUES.md','DEEP_CONTEXT_HANDOFF_FINAL.md','.agents/skills/tgn-system-steward/SKILL.md','.agents/skills/tgn-system-steward/references/atomic-authority-ir-protocol.md']}
write('staging_metadata.json',json.dumps(metadata,ensure_ascii=False,indent=2))
print(out)
print(json.dumps(metadata,ensure_ascii=False,indent=2))
