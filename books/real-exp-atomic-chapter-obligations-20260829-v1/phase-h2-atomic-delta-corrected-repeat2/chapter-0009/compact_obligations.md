chapter: 9
protagonist: 顾停舟
preflight_eligible: true

## HARD / CONDITIONAL OBLIGATIONS
- [TRG-01] mission_clause / must_hold / hard | 顾停舟 → 回潮楔
  Source: 回潮楔已经蓄满，继续钉在原位会让峡壁塌毁
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P069, P084, P076
- [TRG-02] mission_clause / must_hold / hard | 顾停舟 → sacrifice → 矿队首领
  Source: 左侧受伤矿工与两名矿工、右侧砺骨部前哨仍被困在两处，且矿队首领已故意毁掉两边撤路
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P056, P006
- [ACT-01] actor_action_object / must_hold / hard | 本体 → 回潮楔
  Source: 本体继续留在正面承受逆潮，让回潮楔吃下最后一记冲击
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P020
- [ACT-02] actor_action_object / must_hold / hard | 分身 → move|limit|handle → 古器
  Source: 分身只携带牵引穿过侧壁裂隙，把蓄满的古器拖到另一处潮口
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P013, P016, P060
- [ACT-03] actor_action_object / must_hold / hard | 顾停舟 → 潮压
  Source: 顾停舟重新钉定楔面方向，将锁住的潮压释放出去
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P067, P012, P039
- [REA-01] mission_clause / must_hold / hard | 顾停舟 → 逆潮
  Source: 逆潮沿新方向爆发，击穿矿队退路并撕开塌壁窄道
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P042, P020, P003
- [REA-02] mission_clause / must_hold / hard | 矿队首领 → lose|move → 砺骨部
  Source: 矿队首领失去对古器和撤路的控制，矿工与砺骨部前哨被迫同时撤离
  Required state: lost
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P006, P082
- [REA-03] mission_clause / must_hold / hard | 阮青蜃 → search → 顾停舟
  Source: 阮青蜃随后公开主张契约追索，把救援造成的矿权与尾款损失转成对顾停舟的追责
  Required state: disputed
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P083, P087, P079
- [RES-01] direct_result / terminal / hard | 顾停舟 → protect → 砺骨部
  Source: 左侧受伤矿工、两名被困矿工和右侧砺骨部前哨全部脱险
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P069, P006, P053
- [RES-02] direct_result / terminal / hard | 顾停舟 → possess|sacrifice|lose|escape → 矿权标记
  Source: 独家矿权标记损毁，矿路实测尾款无法兑现，回潮楔脱离现场争夺并由顾停舟带走
  Required state: lost
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P080, P060, P079
- [RES-03] direct_result / terminal / hard | 顾停舟 → 第一次让同一股力量在两个相
  Source: 顾停舟第一次让同一股力量在两个相隔位置先后产生结果
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P064, P019, P017
- [STA-01] terminal_state / terminal / hard | 顾停舟 → 乌合
  Source: 顾停舟与乌合形成一次建立在具体救援结果上的相互欠情
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P064, P028, P019
- [STA-02] terminal_state / terminal / hard | 阮青蜃
  Source: 阮青蜃与他公开决裂
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P082, P087, P083
- [STA-03] terminal_state / terminal / hard | 顾停舟 → 分身
  Source: 顾停舟的分身完成“只携一种能力、让两具身体改变同一局势”的复合用法
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P061, P013, P060
- [STA-04] terminal_state / must_hold / hard | 顾停舟 → limit|pending → 兼容潮髓
  Source: 两具身体重新合一时，回潮楔残留潮压与兼容潮髓同时冲入体内，原有潮炉开始扩张，但尚未完成成炉
  Required state: not_transitioned
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P063
- [END-01] ending / terminal / hard | 顾停舟 → move → 兼容潮髓
  Source: 回潮楔残压和兼容潮髓已经进入顾停舟体内，潮炉扩张的后果无法回避
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P063, P033, P074
- [END-02] ending / terminal / hard | 顾停舟 → repair|search → 阮青蜃
  Source: 古器还需要修复与反潮实测，阮青蜃的正式追索也将逼近，因此下一章必须处理顾停舟身体与古器的新状态
  Required state: pending
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P079, P082, P061
- [RR-018] reader_release / must_hold / hard
  Source: 第9章｜触发：倒悬峡低潮时会出现向天空流动的河水，水中悬着倒置石林和残破建筑；已知潮兽不会进入峡谷最深处。
  Boundary: Reader Release is a timing obligation: the reader must learn the approved fact once; atmosphere or terminology alone is insufficient, but no extra encyclopedia is required.
- [A-019] power_boundary / must_not_hold / hard | 顾停舟 → not_yet → 成炉
  Source: 顾停舟与乌合形成一次建立在具体救援结果上的相互欠情；阮青蜃与他公开决裂。顾停舟的分身完成“只携一种能力、让两具身体改变同一局势”的复合用法。两具身体重新合一时，回潮楔残留潮压与兼容潮髓同时冲入体内，原有潮炉开始扩张，但尚未完成成炉。
  Required state: not_transitioned
  Boundary: Pressure/growth may occur, but the draft cannot promote it into stable 成炉.
- [A-020] power_boundary / must_not_hold / hard | 顾停舟 → forbid_unapproved_higher_tier → 入潮
  Source: No stable power transition is authorized in the current Mission
  Required state: not_authorized
  Boundary: Current stable Canon plus an explicit Mission transition defines the maximum authorized tier. If current tier is absent, the gate does not guess it; it simply forbids any new explicit transition not approved by Mission. Future promises, battle scale, public proof and Power Seed legend text do not raise this ceiling.
- [A-021] power_boundary / must_not_hold / hard | 顾停舟 → forbid_unapproved_higher_tier → 照域
  Source: No stable power transition is authorized in the current Mission
  Required state: not_authorized
  Boundary: Current stable Canon plus an explicit Mission transition defines the maximum authorized tier. If current tier is absent, the gate does not guess it; it simply forbids any new explicit transition not approved by Mission. Future promises, battle scale, public proof and Power Seed legend text do not raise this ceiling.
- [A-022] power_boundary / must_not_hold / hard | 顾停舟 → forbid_unapproved_higher_tier → 镇海
  Source: No stable power transition is authorized in the current Mission
  Required state: not_authorized
  Boundary: Current stable Canon plus an explicit Mission transition defines the maximum authorized tier. If current tier is absent, the gate does not guess it; it simply forbids any new explicit transition not approved by Mission. Future promises, battle scale, public proof and Power Seed legend text do not raise this ceiling.
- [A-023] power_boundary / must_hold / hard | 分身 → limited_carry → 完整力量
  Source: 触发事件：回潮楔已经蓄满，继续钉在原位会让峡壁塌毁；左侧受伤矿工与两名矿工、右侧砺骨部前哨仍被困在两处，且矿队首领已故意毁掉两边撤路。
主角行动：本体继续留在正面承受逆潮，让回潮楔吃下最后一记冲击；分身只携带牵引穿过侧壁裂隙，把蓄满的古器拖到另一处潮口。顾停舟重新钉定楔面方向，将锁住的潮压释放出去。
对手或世界反应：逆潮沿新方向爆发，击穿矿队退路并撕开塌壁窄道；矿队首领失去对古器和撤路的控制，矿工与砺骨部前哨被迫同时撤离。阮青蜃随后公开主张契约追索，把救援造成的矿权与尾款损失转成对顾停舟的追责。
直接结果：左侧受伤矿工、两名被困矿工和右侧砺骨部前哨全部脱险；独家矿权标记损毁，矿路实测尾款无法兑现，回潮楔脱离现场争夺并由顾停舟带走。顾停舟第一次让同一股力量在两个相隔位置先后产生结果。
状态变化：顾停舟与乌合形成一次建立在具体救援结果上的相互欠情；阮青蜃与他公开决裂。顾停舟的分身完成“只携一种能力、让两具身体改变同一局势”的复合用法。两具身体重新合一时，回潮楔残留潮压与兼容潮髓同时冲入体内，原有潮炉开始扩张，但尚未完成成炉。
结尾推动力：回潮楔残压和兼容潮髓已经进入顾停舟体内，潮炉扩张的后果无法回避；古器还需要修复与反潮实测，阮青蜃的正式追索也将逼近，因此下一章必须处理顾停舟身体与古器的新状态。
  Required state: limited
  Boundary: Require the current limitation without generalizing it into a stronger universal power law.
  Primary evidence: P080, P079, P006
- [A-024] ownership / terminal / hard | 顾停舟 → possess → 回潮楔
  Source: 触发事件：回潮楔已经蓄满，继续钉在原位会让峡壁塌毁；左侧受伤矿工与两名矿工、右侧砺骨部前哨仍被困在两处，且矿队首领已故意毁掉两边撤路。
主角行动：本体继续留在正面承受逆潮，让回潮楔吃下最后一记冲击；分身只携带牵引穿过侧壁裂隙，把蓄满的古器拖到另一处潮口。顾停舟重新钉定楔面方向，将锁住的潮压释放出去。
对手或世界反应：逆潮沿新方向爆发，击穿矿队退路并撕开塌壁窄道；矿队首领失去对古器和撤路的控制，矿工与砺骨部前哨被迫同时撤离。阮青蜃随后公开主张契约追索，把救援造成的矿权与尾款损失转成对顾停舟的追责。
直接结果：左侧受伤矿工、两名被困矿工和右侧砺骨部前哨全部脱险；独家矿权标记损毁，矿路实测尾款无法兑现，回潮楔脱离现场争夺并由顾停舟带走。顾停舟第一次让同一股力量在两个相隔位置先后产生结果。
状态变化：顾停舟与乌合形成一次建立在具体救援结果上的相互欠情；阮青蜃与他公开决裂。顾停舟的分身完成“只携一种能力、让两具身体改变同一局势”的复合用法。两具身体重新合一时，回潮楔残留潮压与兼容潮髓同时冲入体内，原有潮炉开始扩张，但尚未完成成炉。
结尾推动力：回潮楔残压和兼容潮髓已经进入顾停舟体内，潮炉扩张的后果无法回避；古器还需要修复与反潮实测，阮青蜃的正式追索也将逼近，因此下一章必须处理顾停舟身体与古器的新状态。
  Required state: preserved
  Boundary: Physical possession, registered ownership, and uncontested legal title are distinct. Require only the explicitly authorized state.
  Primary evidence: P084, P076, P011
- [A-025] money / terminal / hard | 顾停舟 → lost → 尾款
  Source: 直接结果：独家矿权标记损毁，矿路实测尾款无法兑现，回潮楔脱离现场争夺并由顾停舟带走
  Required state: lost
  Boundary: Received cash/resource, confirmed entitlement, settlement basis, pending payment and forfeiture are distinct. Never invent an amount or payment mechanism.
  Primary evidence: P080, P060, P079
- [A-026] relationship_state / terminal / conditional | 顾停舟 → relationship_transition → current named counterpart
  Source: 顾停舟与乌合形成一次建立在具体救援结果上的相互欠情；阮青蜃与他公开决裂。顾停舟的分身完成“只携一种能力、让两具身体改变同一局势”的复合用法。两具身体重新合一时，回潮楔残留潮压与兼容潮髓同时冲入体内，原有潮炉开始扩张，但尚未完成成炉。
  Required state: changed
  Boundary: Only the explicit relationship state is required; do not infer romance, loyalty, forgiveness or a stronger bond.
  Primary evidence: P079, P063, P060
- [A-027] unresolved_fact / must_remain_unknown / hard | 塌毁侧室牵扯的真实来源仍未知。
  Source: 塌毁侧室牵扯的真实来源仍未知。
  Required state: unknown
  Boundary: Unknown is a no-invention boundary, not a requirement to repeat 'unknown' in prose.
- [A-028] commercial_value / preserve_if_present / hard | 顾停舟 → preserve_value → reward
  Source: 回潮楔发出一声沉闷的嗡鸣。

裂缝里的石面湿滑，分身侧着身挤进去，肩膀被凸起的石棱刮开一道口子。他伸出手，牵引越过石缝，扣住回潮楔中段。

他把回潮楔横在身前，楔面仍对着正面逆潮，硬吃下最后一记冲击。

回潮楔没有脱手，而是被那股力量拖着擦过石面，朝侧壁裂缝一点点滑去。楔身划过湿石，带出一串刺耳的摩擦声。

松石滚进黑水，正撞在首领腿前。首领脚下一滑，半边身子撞上石脊，只能眼睁睁看着回潮楔被拖进裂缝。

回潮楔穿过裂缝，落入另一处潮口。
  Required state: present_in_primary
  Boundary: Commercial value is category-level, not sentence-level and not a per-chapter quota. Individual carrier paragraphs may change if the authorized desire, relationship, reward or repricing remains visible.
  Primary evidence: P011, P016, P020, P026, P029, P033

## NON-BLOCKING SOURCE DIAGNOSTICS
- 第7章摘要称左侧两名矿工已经获救，但当前场景正文、当前章事件合同与现场状态都明确显示两名矿工仍被困。本章按当前场景正文与事件合同处理。
- 当前章事件合同规定潮炉“开始扩张，但尚未完成成炉”；大型剧情块的“Block Delta”却写成“顾停舟进入成炉”。本章保留“扩张、未成炉”的边界。
