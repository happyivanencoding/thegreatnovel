# Freeze Snapshot

## 仓库与生产 Prompt

- 用户指定开始 HEAD：`90b05697e94e2d70e5a57dd5ce7a0ea6434049ab`。
- 生成开始 HEAD：`2c1e3434b6d68043ba0aac556e63d7912ba23368`。
- branch：`principal_dev_new_sys`。
- 当前生产修改：`2c1e3434b6d68043ba0aac556e63d7912ba23368`。
- Creative Chain baseline：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`。
- 当前 prompts.py blob SHA-1：`06ce9e78d9c4753b56bc7550129f54828763e7df`。
- 当前 `LONG_FORM_PACING_DIRECTION` evaluated SHA-256：`6e10ee6328107157b14c6de90a8cc2c9b6325e1d8c7dda4af33da24164c35103`。

## Legacy 输入来源

- INPUT 来源：`books/real-exp-outline-eventization-v1/INPUT.md`。
- Candidate A legacy Seed 来源：`books/real-exp-outline-eventization-v1/candidate-a/fantasy_seed.md`。
- Candidate A control 来源：`books/real-exp-outline-eventization-v1/candidate-a/outline_response.md`。
- Candidate B legacy Seed 来源：`books/real-exp-outline-eventization-v1/candidate-b/fantasy_seed.md`。
- Candidate B control 来源：`books/real-exp-outline-eventization-v1/candidate-b/outline_response.md`。
- 来源 commit：`20e7974fe00d2045ad059490f15751f7445a11d1`。
- INPUT SHA-256：`c81f58f23d0f5ef457c5ef8294ed6c9a5868e313c7de2ff1635bee2be582ba96`。
- Candidate A legacy Seed SHA-256：`81923fbf33e8eff3c4f8ed9b4a84f1133eb56d4f412160f61a444722f07f49c1`。
- Candidate A Control SHA-256：`6010208e2bc0310230dafd468d4a82af718b5a86bdf3df651f0cdfc07dbc91d0`。
- Candidate B legacy Seed SHA-256：`2287e791e3e5a3545756f1c38fbc875f5de1e7443db989838bfa9e3df960bcf9`。
- Candidate B Control SHA-256：`746a78a70791f2e66a308310452c3fa7a7d28957bae797f46ee99caef7cd81b8`。
- 新目录复制前后逐字节校验：全部通过。

## Treatment 生成状态

- Candidate A World Vision prompt/response：已生成并冻结。
- Candidate A Story Program prompt/response：已生成并冻结。
- Candidate A Dynamic Outline prompt/response：已生成并冻结。
- Candidate B World Vision prompt/response：已生成并冻结。
- Candidate B Story Program prompt/response：已生成并冻结。
- Candidate B Dynamic Outline prompt/response：已生成并冻结。
- Candidate A World Vision response SHA-256：`b7f59e8143d678e0ccd56005a1ac859970eae08043ecea372eb2929bff5ee33f`；Story Program response SHA-256：`945553a4d52e3597f70bf4e1ee97de5f02b24d37d4b73cf5643ded8971374134`。
- Candidate B World Vision response SHA-256：`683b88bd63d268df2dd103e96eeda8d87b4477ed321cd9b35358bb03dd9671a5`；Story Program response SHA-256：`9388bf974af29048c754380a82df918c1cd97adbd152400ab514cde7c42e1c93`。
- Candidate A Dynamic Outline：规划范围 `N=60`；response SHA-256 `101bf079a92d0680c0a5323c4b7bf428e9b340c71087ec3746ab2a06ad4b3001`；prompt SHA-256 `c8127ee2ed5069023323258e521ff3d7a2c5cffc8759e85fe5cb8d2aa187951a`。
- Candidate B Dynamic Outline：规划范围 `N=96`；response SHA-256 `f0b1c75d29898c02af5a1cf8e6436bbcc95ed07699e7548b9de2f301b96297ae`；prompt SHA-256 `7034dcf64828ac6af4c3548138a9dd6ee453282374b918d805c40fefb642276c`。
- Treatment prompt 先保存后校验：A/B World Vision、Story Program、Outline 全部逐字匹配正式 `generate_prompt`，随后才调用模型。
- Blind mapping（Reviewer 完成后揭示）：Candidate A X = Treatment / Y = Control；Candidate B X = Control / Y = Treatment。
- Candidate A Blind Review：SHA-256 `4a11de95a0f8c1d9b29766c6488e74184880ec3957e0225c2b48b39839bfdd71`。
- Candidate B Blind Review：SHA-256 `7c67bb5c37841935da2a19e91c744935ec2da3621eb3f4c88ae897bbf9a66fdb`。
- Cross-Candidate Attribution：SHA-256 `fc05b5a33f65cb8a12dbb18996d02d486063f25a713239d374d579f07f67d349`。
- Final Verdict：SHA-256 `2ddb65849da03ab12a30f99c58a37b241abfd247d9ee4180eeccdab6ab730c2c`。
- 最终结果：`A_PACING_IMPROVED`、`B_HEALTHY_PACE_PRESERVED`、`COMPOUNDING_PRESERVED`、`NARRATIVE_PRESERVED`、`EVENTIZATION_PRESERVED`、`LONG_TERM_RUNWAY_PRESERVED`、`PACING_FIX_VALIDATED`。
- 正式冻结状态：`CREATIVE_CHAIN_FROZEN_V2` + `OUTLINE_FROZEN_V2`。
