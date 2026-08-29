chapter: 2
protagonist: 顾停舟
preflight_eligible: true

## HARD / CONDITIONAL OBLIGATIONS
- [TRG-01] mission_clause / must_hold / hard | 顾停舟 → refuse → 新裂槽
  Source: 天色将暗，校路官决定不再回头核对旧路线册上的兽迹，直接带顾停舟沿断路外缘查看地潮顶出的新裂槽
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P040, P078, P035
- [ACT-01] actor_action_object / must_hold / hard | 顾停舟 → move|confirm → 裂槽
  Source: 顾停舟用原路线记录与现场裂槽、石桩和新鲜矿层对照，确认这不是旧路的局部偏移，而是已经改向的新通道
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P047, P073, P035
- [ACT-02] actor_action_object / must_hold / hard | 顾停舟 → possess|accept → 原册
  Source: 他保留原册，接受作为本次现场事实的实际见证人
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P065
- [REA-01] mission_clause / must_hold / hard | 顾停舟 → 低潮
  Source: 地潮改变了通行结构，裂槽通向深潮矿脉外缘，并只在下一次低潮前短暂可行
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P074, P036, P025
- [REA-02] mission_clause / must_hold / hard | 校路官 → confirm|limit → 旧路线
  Source: 校路官据此判定旧路线不能继续使用
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P025, P054, P035
- [RES-01] direct_result / terminal / hard | 顾停舟 → lose → 旧路线
  Source: 旧路线彻底失去可用性
  Required state: lost
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P040, P025, P054
- [RES-02] direct_result / terminal / hard | 顾停舟 → confirm → 深潮矿样
  Source: 新裂槽与露出的深潮矿样被确认为独立事件
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P014, P035, P040
- [RES-03] direct_result / terminal / hard | 校路官 → transfer|refuse|reprice → 事实副本
  Source: 校路官将事实副本送入校路台，双方不再把它当作商号旧线的延续
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P072, P033, P065
- [STA-01] terminal_state / must_hold / hard | 顾停舟 → acquire|limit|pending → 行潮籍
  Source: 顾停舟仍未取得合法行潮籍，也未正式获得独立实测工作
  Required state: pending
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P074, P007, P060
- [STA-02] terminal_state / terminal / hard | 顾停舟 → possess|confirm|power_transition|escape → 原路线册
  Source: 他持有的原路线册与现场见证身份，已经成为脱离商号账目、争取个人接活的现实依据
  Required state: transitioned
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P005, P042, P035
- [STA-03] terminal_state / terminal / hard | 校路官 → confirm
  Source: 校路官与他的关系从查阅记录转为共同确认现场事实
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P035, P017, P072
- [END-01] ending / terminal / hard | 校路台 → transfer|search → 沉灯商盟
  Source: 校路台的事实记录传入沉灯商盟，阮青蜃开始寻找能够以个人名义完成实测的人
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P085, P076
- [END-02] ending / terminal / hard | 校路台 → 顾停舟
  Source: 裂槽的短暂通行窗口也使顾停舟下一步必须面对这次独立工作的入口
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P073, P010, P034
- [A-014] power_boundary / must_not_hold / hard | 顾停舟 → forbid_unapproved_higher_tier → 入潮
  Source: No stable power transition is authorized in the current Mission
  Required state: not_authorized
  Boundary: Current stable Canon plus an explicit Mission transition defines the maximum authorized tier. If current tier is absent, the gate does not guess it; it simply forbids any new explicit transition not approved by Mission. Future promises, battle scale, public proof and Power Seed legend text do not raise this ceiling.
- [A-015] power_boundary / must_not_hold / hard | 顾停舟 → forbid_unapproved_higher_tier → 成炉
  Source: No stable power transition is authorized in the current Mission
  Required state: not_authorized
  Boundary: Current stable Canon plus an explicit Mission transition defines the maximum authorized tier. If current tier is absent, the gate does not guess it; it simply forbids any new explicit transition not approved by Mission. Future promises, battle scale, public proof and Power Seed legend text do not raise this ceiling.
- [A-016] power_boundary / must_not_hold / hard | 顾停舟 → forbid_unapproved_higher_tier → 照域
  Source: No stable power transition is authorized in the current Mission
  Required state: not_authorized
  Boundary: Current stable Canon plus an explicit Mission transition defines the maximum authorized tier. If current tier is absent, the gate does not guess it; it simply forbids any new explicit transition not approved by Mission. Future promises, battle scale, public proof and Power Seed legend text do not raise this ceiling.
- [A-017] power_boundary / must_not_hold / hard | 顾停舟 → forbid_unapproved_higher_tier → 镇海
  Source: No stable power transition is authorized in the current Mission
  Required state: not_authorized
  Boundary: Current stable Canon plus an explicit Mission transition defines the maximum authorized tier. If current tier is absent, the gate does not guess it; it simply forbids any new explicit transition not approved by Mission. Future promises, battle scale, public proof and Power Seed legend text do not raise this ceiling.
- [A-018] ownership / terminal / hard | 顾停舟 → possess → 原路线册
  Source: 触发事件：天色将暗，校路官决定不再回头核对旧路线册上的兽迹，直接带顾停舟沿断路外缘查看地潮顶出的新裂槽。
主角行动：顾停舟用原路线记录与现场裂槽、石桩和新鲜矿层对照，确认这不是旧路的局部偏移，而是已经改向的新通道；他保留原册，接受作为本次现场事实的实际见证人。
对手或世界反应：地潮改变了通行结构，裂槽通向深潮矿脉外缘，并只在下一次低潮前短暂可行；校路官据此判定旧路线不能继续使用。
直接结果：旧路线彻底失去可用性；新裂槽与露出的深潮矿样被确认为独立事件。校路官将事实副本送入校路台，双方不再把它当作商号旧线的延续。
状态变化：顾停舟仍未取得合法行潮籍，也未正式获得独立实测工作；但他持有的原路线册与现场见证身份，已经成为脱离商号账目、争取个人接活的现实依据。校路官与他的关系从查阅记录转为共同确认现场事实。
结尾推动力：校路台的事实记录传入沉灯商盟，阮青蜃开始寻找能够以个人名义完成实测的人；而裂槽的短暂通行窗口也使顾停舟下一步必须面对这次独立工作的入口。
  Required state: preserved
  Boundary: Physical possession, registered ownership, and uncontested legal title are distinct. Require only the explicitly authorized state.
  Primary evidence: P005, P026, P059
- [A-019] ownership / must_hold / hard | 校路官 → transfer_copy → 事实副本
  Source: 触发事件：天色将暗，校路官决定不再回头核对旧路线册上的兽迹，直接带顾停舟沿断路外缘查看地潮顶出的新裂槽。
主角行动：顾停舟用原路线记录与现场裂槽、石桩和新鲜矿层对照，确认这不是旧路的局部偏移，而是已经改向的新通道；他保留原册，接受作为本次现场事实的实际见证人。
对手或世界反应：地潮改变了通行结构，裂槽通向深潮矿脉外缘，并只在下一次低潮前短暂可行；校路官据此判定旧路线不能继续使用。
直接结果：旧路线彻底失去可用性；新裂槽与露出的深潮矿样被确认为独立事件。校路官将事实副本送入校路台，双方不再把它当作商号旧线的延续。
状态变化：顾停舟仍未取得合法行潮籍，也未正式获得独立实测工作；但他持有的原路线册与现场见证身份，已经成为脱离商号账目、争取个人接活的现实依据。校路官与他的关系从查阅记录转为共同确认现场事实。
结尾推动力：校路台的事实记录传入沉灯商盟，阮青蜃开始寻找能够以个人名义完成实测的人；而裂槽的短暂通行窗口也使顾停舟下一步必须面对这次独立工作的入口。
  Required state: transferred
  Boundary: Original and copy are separate objects. Sending the fact copy must not imply transferring the original route book.
- [A-020] time_window / must_hold / hard | 在下一次低潮前
  Source: 地潮改变了通行结构，裂槽通向深潮矿脉外缘，并只在下一次低潮前短暂可行
  Required state: deadline
  Boundary: A deadline constrains a later action; it does not mean the action is already completed in this chapter.
- [A-021] relationship_state / terminal / conditional | 顾停舟 → relationship_transition → current named counterpart
  Source: 顾停舟仍未取得合法行潮籍，也未正式获得独立实测工作；但他持有的原路线册与现场见证身份，已经成为脱离商号账目、争取个人接活的现实依据。校路官与他的关系从查阅记录转为共同确认现场事实。
  Required state: changed
  Boundary: Only the explicit relationship state is required; do not infer romance, loyalty, forgiveness or a stronger bond.
  Primary evidence: P035, P047
- [A-022] commercial_value / preserve_if_present / hard | 顾停舟 → preserve_value → reward
  Source: 那册子并没有忽然变成通行凭证，也没替他拿到行潮籍。可它不再只是商号账房手里一摞会被改写的旧纸。

“先有资格接，再谈价钱。”

“价钱也得先谈。”

他知道自己现在还不能进。没有行潮籍，没有正式委托，也没有人替他承担下一次低潮后的风险。可裂槽就在眼前，深潮矿层也在眼前。旧路已经断了，新的入口却刚刚露出来。
  Required state: present_in_primary
  Boundary: Commercial value is category-level, not sentence-level and not a per-chapter quota. Individual carrier paragraphs may change if the authorized desire, relationship, reward or repricing remains visible.
  Primary evidence: P060, P068, P069, P074
