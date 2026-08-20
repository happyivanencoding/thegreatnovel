# Freeze Snapshot

## 仓库与生产基线

- branch：`principal_dev_new_sys`
- v2 开始 HEAD：`2be3534`（完整 hash 见提交记录）。
- 开始时 Git status：工作树干净，分支与 `origin/principal_dev_new_sys` 同步。
- Frozen Creative Prompt baseline：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`。
- Outline fix commit：`2be3534`，只修改 `src/story_mvp/prompts.py` 的 `OUTLINE_TEMPLATE`。
- Treatment evaluated `OUTLINE_TEMPLATE` SHA-256：`05a679e3d67a3f1429c33020397239bbdfb25c1bc9abce4bcf686d20c388c2e3`；字符数 `3525`。
- Control evaluated `OUTLINE_TEMPLATE` SHA-256：`6462f9c1dfd835dfa19822fd461019434b83bed607e046781a6f492543658baf`。
- Control/Treatment 的模型温度与 sampling：上一轮没有独立记录，本轮不猜测；两轮均使用 `luna_worker` Agent 类型。

## Frozen Creative Chain 复制证据

- INPUT：SHA-256 `c81f58f23d0f5ef457c5ef8294ed6c9a5868e313c7de2ff1635bee2be582ba96`。
- Candidate A Seed：`81923fbf33e8eff3c4f8ed9b4a84f1133eb56d4f412160f61a444722f07f49c1`。
- Candidate A World Vision：`69994c8727c1be9226eaa9651f2b622d80a32c720428eab2197a4afc4dc59560`。
- Candidate A Story Program：`16c10c8d23004213f3d67d6887a84543cd282e8d6fa684a4c13e39f62349cdf8`。
- Candidate B Seed：`2287e791e3e5a3545756f1c38fbc875f5de1e7443db989838bfa9e3df960bcf9`。
- Candidate B World Vision：`1414f5121143c8267e16fe2d1372f12d7d132947913d28310e07c29ce3704e76`。
- Candidate B Story Program：`78f2e3289169adf473aa1f25b6d1eac87cc1a31652844450fedab84e8f8e30ab`。

来源均为 `books/real-exp-outline-eventization-v1/`，来源 commit `20e7974fe00d2045ad059490f15751f7445a11d1`；复制前后逐字节一致。

## Control 复制证据

- Candidate A Control：来源 `books/real-exp-outline-eventization-v1/candidate-a/outline_response.md`，SHA-256 `6010208e2bc0310230dafd468d4a82af718b5a86bdf3df651f0cdfc07dbc91d0`；复制到 `candidate-a/control_outline.md`，逐字节一致。
- Candidate B Control：来源 `books/real-exp-outline-eventization-v1/candidate-b/outline_response.md`，SHA-256 `746a78a70791f2e66a308310452c3fa7a7d28957bae797f46ee99caef7cd81b8`；复制到 `candidate-b/control_outline.md`，逐字节一致。

-## Treatment 生成状态

- Treatment Prompt A：已保存并逐字校验；SHA-256 `c89abf968c0aaec40cbf47301dc2232e92311ee5e4ccf714f0cfa53479021ae0`，25460 字符。
- Treatment Prompt B：已保存并逐字校验；SHA-256 `2cc24d3baadf23a95c8605a78c28564b37d19bcfc5d07ff1253064749088072a`，25802 字符。
- Treatment Outline A：Agent `01a020d3-b3db-7911-9ec0-bec691d43feb`，已生成一次；SHA-256 `7c8b7a5c56f96c9aab4b6dc8b1f8771e2913ed4183722972902822718a84d230`，51082 bytes。
- Treatment Outline B：Agent `01a020d3-b513-7442-bb23-4360bf63e31f`，已生成一次；SHA-256 `b8d5daeaec24252893d2f5684b93ea13c10ea71ad4b1afa78a6b8e4d43dc79d7`，48112 bytes。
- 完整性校验：A/B candidate 目录均只有六个规定文件；Treatment prompt 逐字匹配正式模板；response 均非空并包含四个一级标题。
- Anonymous pair copies：A `outline_x.md` = Treatment、`outline_y.md` = Control；B `outline_x.md` = Control、`outline_y.md` = Treatment；复制 hash 与对应文件一致。
- Candidate A Blind Review：Agent `01a020dc-7463-7e02-8dac-e24441a86b44`；SHA-256 `45175eb207eec20d7f41e346d93cf5bac426d10087dc5c2a6fd95dba7f66872e`。
- Candidate B Blind Review：Agent `01a020dc-758e-71f3-b5d5-82d793e70b4b`；SHA-256 `fe54524cb64d97205bd45a7f7cc21ac1404d3c6cf1762761a0eb81a21d2705b7`。
- Cross/Attribution Review：Agent `01a020e5-a4a4-76f2-9dbe-3fc164b52ed9`；SHA-256 `936c4cbc47f26e39d99ff1b99c2ea380c8a6a8e4700492ad1215cba2364f9bef`。
- Final Verdict：主 Agent 整合完成；SHA-256 `561893e159c7437a95134695a4ae38a0440f5c8a413cc834560bf7c92754586e`。
- 最终结果：`A_EVENTIZATION_IMPROVED`、`B_HEALTH_PRESERVED`、`COMPOUNDING_PRESERVED`、`OUTLINE_FIX_VALIDATED`、`OUTLINE_FROZEN`。
- Blind mapping（Reviewer 完成后揭示）：A X = Treatment / Y = Control；B X = Control / Y = Treatment。
