chapter: 14
protagonist: 顾停舟
preflight_eligible: true

## HARD / CONDITIONAL OBLIGATIONS
- [TRG-01] mission_clause / must_hold / hard | 百炉会
  Source: 百炉会炉钟响起，入口即将封闭
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P001, P098, P160
- [TRG-02] mission_clause / must_hold / hard | 顾停舟 → move|search → 契约损失
  Source: 顾停舟携回潮楔进入开炉试，阮青蜃带人当众追索古器与契约损失
  Required state: disputed
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P030, P064, P024
- [ACT-01] actor_action_object / must_hold / hard | 顾停舟 → move|confirm → 回潮楔
  Source: 顾停舟让回潮楔只完成一次真实的锁潮、改向、释放，证明它能改变一整段潮势方向
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P024, P030, P088
- [ACT-02] actor_action_object / must_hold / hard | 顾停舟 → possess|refuse|accept → 自主使用权
  Source: 面对两份条件，他拒绝出售回潮楔，接受少东家的独立合作，并坚持保留自主使用权与个人矿利
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P146
- [REA-01] mission_clause / must_hold / hard | 顾停舟 → confirm → 回潮楔
  Source: 现场懂行者以一次比较确认，普通成炉者只能在自身附近稳定重压，而回潮楔能改动整段潮势
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P069, P019
- [REA-02] mission_clause / must_hold / hard | 顾停舟 → reprice → 重新定价
  Source: 顾停舟因此被重新定价
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P073, P110, P140
- [REA-03] mission_clause / must_hold / hard | 阮青蜃 → refuse|lose|reprice|search → 百炉会
  Source: 阮青蜃的买断与追索失去原本的压制力，百炉会及相关见证者不再把首批矿脉的独家标记视为阮青蜃的完整矿权
  Required state: lost
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P095, P106, P109
- [RES-01] direct_result / terminal / hard | 顾停舟 → acquire|confirm → 公开确认
  Source: 回潮楔的实际价值与使用代价获得公开确认
  Required state: received
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P148, P060, P079
- [RES-02] direct_result / terminal / hard | 顾停舟 → acquire|protect|confirm → 个人矿利
  Source: 顾停舟保住回潮楔，取得公开确认的个人矿利份额，砺骨部水路不被并入阮青蜃的矿权
  Required state: entitlement_confirmed
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P109, P100, P030
- [RES-03] direct_result / terminal / hard | 少东家 → 主从关系
  Source: 少东家的粮路承运合作正式取代旧主从关系
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P128
- [STA-01] terminal_state / must_hold / hard | 顾停舟 → possess|search|pending → 个人矿利
  Source: 顾停舟从“持有古器、等待追索处理”转为拥有古器自主权、个人矿利和独立合作入口的承揽者
  Required state: disputed
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P109, P146
- [STA-02] terminal_state / terminal / hard | 顾停舟 → possess|search → 少东家
  Source: 他与少东家变为有价合作关系，与阮青蜃的争执从私下追索升级为公开的利益与归属对立
  Required state: disputed
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P095
- [STA-03] terminal_state / terminal / hard | 顾停舟 → move|limit|repair → 回潮楔
  Source: 回潮楔完成本章一次改向后必须散尽残压，不能连续硬压
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P101, P037, P060
- [END-01] ending / terminal / hard | 顾停舟 → transfer|move → 十二日地潮
  Source: 粮路合作的第一批货必须赶在下一次十二日地潮前送到旧关
  Required state: asserted
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P173, P135, P021
- [END-02] ending / terminal / hard | 顾停舟 → move|depart
  Source: 顾停舟随队出发，新的合作关系立即进入必须兑现的现实期限
  Required state: departed
  Boundary: Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.
  Primary evidence: P002, P168, P114
- [A-016] power_boundary / must_not_hold / hard | 顾停舟 → forbid_unapproved_higher_tier → 照域
  Source: 成炉潮息
  Required state: not_authorized
  Boundary: Current stable Canon plus an explicit Mission transition defines the maximum authorized tier. If current tier is absent, the gate does not guess it; it simply forbids any new explicit transition not approved by Mission. Future promises, battle scale, public proof and Power Seed legend text do not raise this ceiling.
- [A-017] power_boundary / must_not_hold / hard | 顾停舟 → forbid_unapproved_higher_tier → 镇海
  Source: 成炉潮息
  Required state: not_authorized
  Boundary: Current stable Canon plus an explicit Mission transition defines the maximum authorized tier. If current tier is absent, the gate does not guess it; it simply forbids any new explicit transition not approved by Mission. Future promises, battle scale, public proof and Power Seed legend text do not raise this ceiling.
- [A-018] ownership / terminal / hard | 顾停舟 → possess → 回潮楔
  Source: 触发事件：百炉会炉钟响起，入口即将封闭；顾停舟携回潮楔进入开炉试，阮青蜃带人当众追索古器与契约损失。
主角行动：顾停舟让回潮楔只完成一次真实的锁潮、改向、释放，证明它能改变一整段潮势方向；面对两份条件，他拒绝出售回潮楔，接受少东家的独立合作，并坚持保留自主使用权与个人矿利。
对手或世界反应：现场懂行者以一次比较确认，普通成炉者只能在自身附近稳定重压，而回潮楔能改动整段潮势；顾停舟因此被重新定价。阮青蜃的买断与追索失去原本的压制力，百炉会及相关见证者不再把首批矿脉的独家标记视为阮青蜃的完整矿权。
直接结果：回潮楔的实际价值与使用代价获得公开确认；顾停舟保住回潮楔，取得公开确认的个人矿利份额，砺骨部水路不被并入阮青蜃的矿权。少东家的粮路承运合作正式取代旧主从关系。
状态变化：顾停舟从“持有古器、等待追索处理”转为拥有古器自主权、个人矿利和独立合作入口的承揽者；他与少东家变为有价合作关系，与阮青蜃的争执从私下追索升级为公开的利益与归属对立。回潮楔完成本章一次改向后必须散尽残压，不能连续硬压。
结尾推动力：粮路合作的第一批货必须赶在下一次十二日地潮前送到旧关。顾停舟随队出发，新的合作关系立即进入必须兑现的现实期限。
  Required state: preserved
  Boundary: Physical possession, registered ownership, and uncontested legal title are distinct. Require only the explicitly authorized state.
  Primary evidence: P148, P030, P064
- [A-019] money / must_hold / hard | 顾停舟 → entitlement_confirmed → 个人矿利
  Source: 直接结果：顾停舟保住回潮楔，取得公开确认的个人矿利份额，砺骨部水路不被并入阮青蜃的矿权
  Required state: entitlement_confirmed
  Boundary: Received cash/resource, confirmed entitlement, settlement basis, pending payment and forfeiture are distinct. Never invent an amount or payment mechanism.
  Primary evidence: P109, P100, P030
- [A-020] money / must_hold / hard | 顾停舟 → entitlement_confirmed → 矿利
  Source: 直接结果：顾停舟保住回潮楔，取得公开确认的个人矿利份额，砺骨部水路不被并入阮青蜃的矿权
  Required state: entitlement_confirmed
  Boundary: Received cash/resource, confirmed entitlement, settlement basis, pending payment and forfeiture are distinct. Never invent an amount or payment mechanism.
  Primary evidence: P109, P100, P030
- [A-021] time_window / must_hold / hard | 在下一次十二日地潮前
  Source: 粮路合作的第一批货必须赶在下一次十二日地潮前送到旧关
  Required state: deadline
  Boundary: A deadline constrains a later action; it does not mean the action is already completed in this chapter.
- [A-022] ending / terminal / hard | 顾停舟 → depart → 队伍/目的地
  Source: 粮路合作的第一批货必须赶在下一次十二日地潮前送到旧关。顾停舟随队出发，新的合作关系立即进入必须兑现的现实期限。
  Required state: departed
  Boundary: Vehicles waiting or a plan to depart is not enough; actual departure must occur.
  Primary evidence: P173, P135
- [A-023] actor_action_object / must_hold / hard | 顾停舟 → single_artifact_cycle → 回潮楔
  Source: 触发事件：百炉会炉钟响起，入口即将封闭；顾停舟携回潮楔进入开炉试，阮青蜃带人当众追索古器与契约损失。
主角行动：顾停舟让回潮楔只完成一次真实的锁潮、改向、释放，证明它能改变一整段潮势方向；面对两份条件，他拒绝出售回潮楔，接受少东家的独立合作，并坚持保留自主使用权与个人矿利。
对手或世界反应：现场懂行者以一次比较确认，普通成炉者只能在自身附近稳定重压，而回潮楔能改动整段潮势；顾停舟因此被重新定价。阮青蜃的买断与追索失去原本的压制力，百炉会及相关见证者不再把首批矿脉的独家标记视为阮青蜃的完整矿权。
直接结果：回潮楔的实际价值与使用代价获得公开确认；顾停舟保住回潮楔，取得公开确认的个人矿利份额，砺骨部水路不被并入阮青蜃的矿权。少东家的粮路承运合作正式取代旧主从关系。
状态变化：顾停舟从“持有古器、等待追索处理”转为拥有古器自主权、个人矿利和独立合作入口的承揽者；他与少东家变为有价合作关系，与阮青蜃的争执从私下追索升级为公开的利益与归属对立。回潮楔完成本章一次改向后必须散尽残压，不能连续硬压。
结尾推动力：粮路合作的第一批货必须赶在下一次十二日地潮前送到旧关。顾停舟随队出发，新的合作关系立即进入必须兑现的现实期限。
  Required state: exactly_one_cycle
  Boundary: The explicit count belongs only to this approved use cycle; it is not a universal per-chapter count rule.
- [A-024] power_boundary / must_hold / hard | 回潮楔 → dissipate_before_reuse → 残压
  Source: 顾停舟从“持有古器、等待追索处理”转为拥有古器自主权、个人矿利和独立合作入口的承揽者；他与少东家变为有价合作关系，与阮青蜃的争执从私下追索升级为公开的利益与归属对立。回潮楔完成本章一次改向后必须散尽残压，不能连续硬压。
  Required state: cooldown_required
  Boundary: ‘再次使用前必须散尽’是 cooldown，不等于章末已经散尽；只有明确章末终态才要求 residual pressure 已归零。
- [A-025] public_proof / must_hold / hard | 顾停舟 → public_proof → 力量/器物/战绩
  Source: 现场懂行者以一次比较确认，普通成炉者只能在自身附近稳定重压，而回潮楔能改动整段潮势；顾停舟因此被重新定价。阮青蜃的买断与追索失去原本的压制力，百炉会及相关见证者不再把首批矿脉的独家标记视为阮青蜃的完整矿权。
回潮楔的实际价值与使用代价获得公开确认；顾停舟保住回潮楔，取得公开确认的个人矿利份额，砺骨部水路不被并入阮青蜃的矿权。少东家的粮路承运合作正式取代旧主从关系。
  Required state: publicly_calibrated
  Boundary: Require performance, qualified ruler and behavioral consequence. Public Proof never authorizes an unapproved stable tier.
  Primary evidence: P109, P100, P069
- [A-026] relationship_state / terminal / conditional | 顾停舟 → relationship_transition → current named counterpart
  Source: 回潮楔的实际价值与使用代价获得公开确认；顾停舟保住回潮楔，取得公开确认的个人矿利份额，砺骨部水路不被并入阮青蜃的矿权。少东家的粮路承运合作正式取代旧主从关系。
顾停舟从“持有古器、等待追索处理”转为拥有古器自主权、个人矿利和独立合作入口的承揽者；他与少东家变为有价合作关系，与阮青蜃的争执从私下追索升级为公开的利益与归属对立。回潮楔完成本章一次改向后必须散尽残压，不能连续硬压。
  Required state: changed
  Boundary: Only the explicit relationship state is required; do not infer romance, loyalty, forgiveness or a stronger bond.
  Primary evidence: P109, P100
- [A-027] commercial_value / preserve_if_present / hard | 顾停舟 → preserve_value → desire
  Source: “我铸潮时只能替它把步骤走顺。刚才那一下，是顾停舟自己定的方向。”

“我想买的是麻烦。”

“这是我花钱修回来的。”他说，“怎么用，卖不卖，归我自己定。”

他想起以前替对方跑事时，很多话根本不用说。因为说了也没用。上头一句交代，底下的人就得把命和路一起填进去。
  Required state: present_in_primary
  Boundary: Commercial value is category-level, not sentence-level and not a per-chapter quota. Individual carrier paragraphs may change if the authorized desire, relationship, reward or repricing remains visible.
  Primary evidence: P072, P085, P090, P153
- [A-028] commercial_value / preserve_if_present / hard | 顾停舟 → preserve_value → reward
  Source: 顾停舟把回潮楔放到她掌心。

顾停舟抬起回潮楔。

再往前，就是百炉会立着验石的地方。若让它直撞过去，最多砸碎几块石头，谁也看不出回潮楔到底值不值钱。

回潮楔先亮起一道细潮纹。

是从地下闸口冲出来的那一段潮，被回潮楔锁住后，硬生生拧进了另一条路。

回潮楔在他掌中震得越来越厉害，楔身上的浅裂亮得发白。他知道该放了。
  Required state: present_in_primary
  Boundary: Commercial value is category-level, not sentence-level and not a per-chapter quota. Individual carrier paragraphs may change if the authorized desire, relationship, reward or repricing remains visible.
  Primary evidence: P024, P030, P035, P037, P050, P055
- [A-029] commercial_value / preserve_if_present / hard | 顾停舟 → preserve_value → relationship
  Source: 也不是一句旧情，要他再替人把麻烦扛过去。

是一张写着报酬、责任和退路的合作短契。
  Required state: present_in_primary
  Boundary: Commercial value is category-level, not sentence-level and not a per-chapter quota. Individual carrier paragraphs may change if the authorized desire, relationship, reward or repricing remains visible.
  Primary evidence: P143, P144
- [A-030] commercial_value / preserve_if_present / hard | 顾停舟 → preserve_value → social_repricing
  Source: 这句话落下，场里看顾停舟的目光变了。
  Required state: present_in_primary
  Boundary: Commercial value is category-level, not sentence-level and not a per-chapter quota. Individual carrier paragraphs may change if the authorized desire, relationship, reward or repricing remains visible.
  Primary evidence: P073
