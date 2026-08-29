chapter: 16
protagonist: 顾停舟
preflight_eligible: true

## HARD / CONDITIONAL OBLIGATIONS
- [TRG-01] mission_clause / must_hold / hard | 顾停舟 → 旧关外层
  Source: 地潮提前冲入旧关外层，第三座新潮井喷涌、第一辆粮车被石料卡死，西侧迁徙水路同时塌方
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P074
- [TRG-02] mission_clause / must_hold / hard | 顾停舟 → move → 三座新井
  Source: 粮队、三座新井、撤离居民和砺骨部水路即将被同一股潮势一起吞没
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P010, P074, P034
- [ACT-01] actor_action_object / must_hold / hard | 顾停舟 → 成炉
  Source: 顾停舟以成炉本体稳定粮队与主水路
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P026, P045
- [ACT-02] actor_action_object / must_hold / hard | 分身 → move|limit|fix|handle → 回潮楔
  Source: 分身只携带“定住”进入第二个潮压节点，将回潮楔固定在那里
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
- [ACT-03] actor_action_object / must_hold / hard | 顾停舟 → sacrifice|lose|move → 三座新井
  Source: 他不试图用回潮楔压住全部地潮，而是选择把一股本会冲毁三座新井的潮势改向已经决定放弃的旧关外层
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P013, P046
- [REA-01] mission_clause / must_hold / hard | 顾停舟 → sacrifice|move → 残墙
  Source: 地潮沿改向后的节点冲入外层，黑水、泥坡和残墙连片坍塌
  Required state: destroyed
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P013, P073, P055
- [REA-02] mission_clause / must_hold / hard | 顾沉戈 → acquire|protect|move → 砺骨部
  Source: 顾沉戈被迫守住井位，守将带撤离居民改走仍可用的路线，砺骨部前哨获得实际引导迁徙取水的窗口
  Required state: received
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P074, P010, P092
- [REA-03] mission_clause / must_hold / hard | 少东家 → limit|pending|escape → 潮压
  Source: 少东家的粮队暂时脱离最危险的潮压范围，但承运仍未完成
  Required state: pending
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
- [RES-01] direct_result / terminal / hard | 顾停舟 → acquire|protect → 砺骨部
  Source: 粮道保住，三座新潮井没有被毁，砺骨部取得这一轮可实际通过的迁徙取水窗口
  Required state: received
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
- [RES-02] direct_result / terminal / hard | 顾停舟 → sacrifice → 旧关外层
  Source: 旧关外层被改道潮势彻底毁弃
  Required state: destroyed
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P013, P038, P012
- [RES-03] direct_result / terminal / hard | 顾停舟 → possess|repair → 回潮楔
  Source: 回潮楔完成一次完整释放后仍归顾停舟所有，但再次使用前必须散尽残压
  Required state: preserved
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P045, P096, P039
- [STA-01] terminal_state / terminal / hard | 顾停舟 → 回潮楔
  Source: 顾停舟第一次把“借身＋回潮楔”用于改变公共资源和迁徙路线，而非单纯救援
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P045, P096
- [STA-02] terminal_state / terminal / hard | 顾停舟 → protect|sacrifice|lose → 水路
  Source: 他以放弃外层为代价保住井、粮和水路
  Required state: preserved
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P026, P011, P074
- [STA-03] terminal_state / terminal / hard | 顾沉戈 → move|pending → 砺骨部
  Source: 顾沉戈、守将与砺骨部前哨暂时转为执行他的现场分配，旧关的撤离范围和可用水路被重新确定
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P010, P074, P092
- [STA-04] terminal_state / must_remain_unknown / hard | 顾沉戈 → limit|pay|pending
  Source: 地潮提前的原因仍未解决，第一批粮的最终承运也仍未结算
  Required state: pending
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
- [END-01] ending / terminal / hard | 顾停舟 → sacrifice → 照域潮谱
  Source: 外层毁弃后，旧关内侧观测点暴露，照域潮谱仍在其中
  Required state: destroyed
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P088, P085
- [END-02] ending / terminal / hard | 顾停舟 → move → 潮势
  Source: 下一轮潮势将直接冲向撤离队伍
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P091, P063, P052
- [END-03] ending / terminal / hard | 顾停舟 → move → 潮势
  Source: 顾停舟必须进入观测点，弄清潮势下一步的指向并争取撤离时间
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P101, P082, P069
- [A-019] power_boundary / must_not_hold / hard | 顾停舟 → forbid_unapproved_higher_tier → 入潮
  Source: No stable power transition is authorized in the current Mission
  Required state: not_authorized
  Boundary: Current stable Canon plus an explicit Mission transition defines the maximum authorized tier. If current tier is absent, the gate does not guess it; it simply forbids any new explicit transition not approved by Mission. Future promises, battle scale, public proof and Power Seed legend text do not raise this ceiling.
- [A-020] power_boundary / must_not_hold / hard | 顾停舟 → forbid_unapproved_higher_tier → 成炉
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
  Source: 触发事件：地潮提前冲入旧关外层，第三座新潮井喷涌、第一辆粮车被石料卡死，西侧迁徙水路同时塌方；粮队、三座新井、撤离居民和砺骨部水路即将被同一股潮势一起吞没。
主角行动：顾停舟以成炉本体稳定粮队与主水路，分身只携带“定住”进入第二个潮压节点，将回潮楔固定在那里。他不试图用回潮楔压住全部地潮，而是选择把一股本会冲毁三座新井的潮势改向已经决定放弃的旧关外层。
对手或世界反应：地潮沿改向后的节点冲入外层，黑水、泥坡和残墙连片坍塌；顾沉戈被迫守住井位，守将带撤离居民改走仍可用的路线，砺骨部前哨获得实际引导迁徙取水的窗口。少东家的粮队暂时脱离最危险的潮压范围，但承运仍未完成。
直接结果：粮道保住，三座新潮井没有被毁，砺骨部取得这一轮可实际通过的迁徙取水窗口；旧关外层被改道潮势彻底毁弃。回潮楔完成一次完整释放后仍归顾停舟所有，但再次使用前必须散尽残压。
状态变化：顾停舟第一次把“借身＋回潮楔”用于改变公共资源和迁徙路线，而非单纯救援；他以放弃外层为代价保住井、粮和水路。顾沉戈、守将与砺骨部前哨暂时转为执行他的现场分配，旧关的撤离范围和可用水路被重新确定。地潮提前的原因仍未解决，第一批粮的最终承运也仍未结算。
结尾推动力：外层毁弃后，旧关内侧观测点暴露，照域潮谱仍在其中；下一轮潮势将直接冲向撤离队伍。顾停舟必须进入观测点，弄清潮势下一步的指向并争取撤离时间。
  Required state: limited
  Boundary: Require the current limitation without generalizing it into a stronger universal power law.
  Primary evidence: P074
- [A-024] ownership / terminal / hard | 顾停舟 → possess → 回潮楔
  Source: 触发事件：地潮提前冲入旧关外层，第三座新潮井喷涌、第一辆粮车被石料卡死，西侧迁徙水路同时塌方；粮队、三座新井、撤离居民和砺骨部水路即将被同一股潮势一起吞没。
主角行动：顾停舟以成炉本体稳定粮队与主水路，分身只携带“定住”进入第二个潮压节点，将回潮楔固定在那里。他不试图用回潮楔压住全部地潮，而是选择把一股本会冲毁三座新井的潮势改向已经决定放弃的旧关外层。
对手或世界反应：地潮沿改向后的节点冲入外层，黑水、泥坡和残墙连片坍塌；顾沉戈被迫守住井位，守将带撤离居民改走仍可用的路线，砺骨部前哨获得实际引导迁徙取水的窗口。少东家的粮队暂时脱离最危险的潮压范围，但承运仍未完成。
直接结果：粮道保住，三座新潮井没有被毁，砺骨部取得这一轮可实际通过的迁徙取水窗口；旧关外层被改道潮势彻底毁弃。回潮楔完成一次完整释放后仍归顾停舟所有，但再次使用前必须散尽残压。
状态变化：顾停舟第一次把“借身＋回潮楔”用于改变公共资源和迁徙路线，而非单纯救援；他以放弃外层为代价保住井、粮和水路。顾沉戈、守将与砺骨部前哨暂时转为执行他的现场分配，旧关的撤离范围和可用水路被重新确定。地潮提前的原因仍未解决，第一批粮的最终承运也仍未结算。
结尾推动力：外层毁弃后，旧关内侧观测点暴露，照域潮谱仍在其中；下一轮潮势将直接冲向撤离队伍。顾停舟必须进入观测点，弄清潮势下一步的指向并争取撤离时间。
  Required state: preserved
  Boundary: Physical possession, registered ownership, and uncontested legal title are distinct. Require only the explicitly authorized state.
  Primary evidence: P048, P045, P070
- [A-025] actor_action_object / must_hold / hard | 顾停舟 → single_artifact_cycle → 回潮楔
  Source: 触发事件：地潮提前冲入旧关外层，第三座新潮井喷涌、第一辆粮车被石料卡死，西侧迁徙水路同时塌方；粮队、三座新井、撤离居民和砺骨部水路即将被同一股潮势一起吞没。
主角行动：顾停舟以成炉本体稳定粮队与主水路，分身只携带“定住”进入第二个潮压节点，将回潮楔固定在那里。他不试图用回潮楔压住全部地潮，而是选择把一股本会冲毁三座新井的潮势改向已经决定放弃的旧关外层。
对手或世界反应：地潮沿改向后的节点冲入外层，黑水、泥坡和残墙连片坍塌；顾沉戈被迫守住井位，守将带撤离居民改走仍可用的路线，砺骨部前哨获得实际引导迁徙取水的窗口。少东家的粮队暂时脱离最危险的潮压范围，但承运仍未完成。
直接结果：粮道保住，三座新潮井没有被毁，砺骨部取得这一轮可实际通过的迁徙取水窗口；旧关外层被改道潮势彻底毁弃。回潮楔完成一次完整释放后仍归顾停舟所有，但再次使用前必须散尽残压。
状态变化：顾停舟第一次把“借身＋回潮楔”用于改变公共资源和迁徙路线，而非单纯救援；他以放弃外层为代价保住井、粮和水路。顾沉戈、守将与砺骨部前哨暂时转为执行他的现场分配，旧关的撤离范围和可用水路被重新确定。地潮提前的原因仍未解决，第一批粮的最终承运也仍未结算。
结尾推动力：外层毁弃后，旧关内侧观测点暴露，照域潮谱仍在其中；下一轮潮势将直接冲向撤离队伍。顾停舟必须进入观测点，弄清潮势下一步的指向并争取撤离时间。
  Required state: exactly_one_cycle
  Boundary: The explicit count belongs only to this approved use cycle; it is not a universal per-chapter count rule.
- [A-026] power_boundary / must_hold / hard | 回潮楔 → dissipate_before_reuse → 残压
  Source: 顾停舟第一次把“借身＋回潮楔”用于改变公共资源和迁徙路线，而非单纯救援；他以放弃外层为代价保住井、粮和水路。顾沉戈、守将与砺骨部前哨暂时转为执行他的现场分配，旧关的撤离范围和可用水路被重新确定。地潮提前的原因仍未解决，第一批粮的最终承运也仍未结算。
  Required state: cooldown_required
  Boundary: ‘再次使用前必须散尽’是 cooldown，不等于章末已经散尽；只有明确章末终态才要求 residual pressure 已归零。
- [A-027] unresolved_fact / must_remain_unknown / hard | 地潮提前的原因仍未解决，第一批粮的最终承运也仍未结算
  Source: 地潮提前的原因仍未解决，第一批粮的最终承运也仍未结算
  Required state: unknown
  Boundary: Unknown is a no-invention boundary, not a requirement to repeat 'unknown' in prose.
- [A-028] unresolved_fact / must_remain_unknown / hard | 地潮为何提前、下一轮将如何推进，仍属未知。
  Source: 地潮为何提前、下一轮将如何推进，仍属未知。
  Required state: unknown
  Boundary: Unknown is a no-invention boundary, not a requirement to repeat 'unknown' in prose.
- [A-029] commercial_value / preserve_if_present / hard | 顾停舟 → preserve_value → reward
  Source: 只要把那里定住，再把回潮楔放进去，潮势就能偏开。

本体的顾停舟已经抽出回潮楔。

回潮楔脱手而出。

回潮楔从潮泥中弹回，落进他掌心。

顾停舟收紧袖中的回潮楔，转身朝那座暴露出来的石台走去。
  Required state: present_in_primary
  Boundary: Commercial value is category-level, not sentence-level and not a per-chapter quota. Individual carrier paragraphs may change if the authorized desire, relationship, reward or repricing remains visible.
  Primary evidence: P037, P045, P048, P070, P096
