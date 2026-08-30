# Native DirectorStructuredDecision E2E｜冻结实验协议

## 目标

比较当前free-text Director与Native typed Director，在相同下游链中的Story、Authority、wall、跨书coverage、repeat和fallback-adjusted E2E。

## 样本

- 九垂原 Ch14：Public Proof / ownership / money entitlement / relationship / deadline。
- 九垂原 Ch16：protagonist + manifestation / composite ability / sacrifice / unknown / ending。
- 分影原型 Ch4：combat / contract / first payment / reveal / travel relationship。
- 分影原型 Ch9：injury / mixed desire / relationship boundary / rival repricing / ending proof。

## 冻结变量

- 相同pre-Director Authority；
- Director/Curator/Reviser Luna high，Primary Terra high；
- 相同下游Prompt；
- 相同ACP adapter与工作目录；
- Treatment只改Director输出合同与Runtime双投影；
- Fresh Control真实重新运行，不使用历史wall。

## 路由

```text
Native parse / Contract / projection eligible?
  NO → 记录废弃Native wall + free-text Director fallback + 完整下游
  YES → Runtime human Mission + Atomic Contract + 完整下游
```

## 预注册修复

V1因跨书ActionSurface污染无效。V2只允许修：

- 跨书Surface污染；
- 多分句标点；
- 多对象自然渲染；
- outer-pass actor signature；
- foreign display-name/internal-ID leakage fail-closed。

V2 Run4/Run5前记录文件哈希；盲评后不调模板。

## 盲评

每章四路匿名混排：Native4、Native5、Control3、Control4。

分别审：

- Mission Story；
- Mission Authority；
- Final Story；
- Final Authority。

所有候选统一：去citation元数据、去`# 正式正文`标题、只保留同层文本。Judge不知道路线。

## 速度口径

完整Final Draft critical path：

```text
Director + discarded/fallback Director（若有） + Curator + Primary + Authority Reviser
```

不含State，因为用户本轮终点是Final Draft。不能用并行批次elapsed替代单章node wall总和；不能只报最快一轮。

## 采用门槛

必须同时满足：

- Story non-regression；
- Authority non-regression；
- 跨书coverage；
- independent repeat；
- fallback-adjusted E2E同方向加速；
- 自动Registry或明确unsupported bypass；
- 不新增LLM classifier；
- 不把Atomic Pack喂给Primary。
