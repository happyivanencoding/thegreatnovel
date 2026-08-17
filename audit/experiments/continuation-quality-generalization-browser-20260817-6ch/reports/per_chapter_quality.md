# 逐章质量证据（截至第 6 章）

这里记录可复核的机器事实，不把 validator 通过等同于文学质量全通过。

| 章 | 标题 | 字符数 | 事件范围 | Canon commit | Validator | Semantic review | 正文 hash |
|---:|---|---:|---:|---|---|---|---|
| 1 | 名籍之外的第一场挑战 | 2028 | 1–5 | canon-commit_9ccb975a8a997ba4d3fc56c4 | 10/10 PASS | REVIEWED | 806b68f6…60aaa6 |
| 2 | 记录上的下一道门 | 1930 | 6–11 | canon-commit_af65d712e850921c56e6e480 | 10/10 PASS | REVIEWED | f136b404…5bfa39 |
| 3 | 被看见之后的邀请 | 2249 | 12–17 | canon-commit_f31950f27f0db74be2e10c29 | 10/10 PASS | REVIEWED | d1bb9f34…c14c6 |
| 4 | 渡口规则的第一道门 | 1781 | 18–23 | canon-commit_efa72a3c7830d57190394781 | 10/10 PASS | REVIEWED | b38bfd47…7392d |
| 5 | 黑石前的第二次判定 | 895 | 24–29 | canon-commit_a339bc7c6fb17abf09028eec | 10/10 PASS | REVIEWED | d54119b8…344c3 |
| 6 | 见证者名单上的新名字 | 1352 | 30–35 | canon-commit_205e3257fad8d9edffbaea79 | 10/10 PASS | REVIEWED | bc9ff09e…4d4fc |

## 机器边界

- 六个 Canon commit 的 event ranges 连续覆盖 1–35，无缺口或重叠。
- 每章都有独立 publication review，状态为 REVIEWED；本报告没有把 review claims 复制到创作输出。
- 第 3 章发现并修复了 review 正文哈希规范化和 world/social state changes 合同标签映射问题；修复后第 3–6 章均以零 hard error 通过。
- 第 5 章字符数明显较短；这是需要盲读关注的质量风险，不是 validator failure。

