# Freeze Snapshot

## 仓库与生产 Prompt

- branch：`principal_dev_new_sys`
- HEAD：`170da2221ca38948dce66fa0a48041cfeeede75b`
- 开始时 Git status：`## principal_dev_new_sys...origin/principal_dev_new_sys`
- Creative Prompt baseline：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`
- Prompt source：`src/story_mvp/prompts.py`
- Prompt source last commit：`e2e3bac29039afa075a60d48b31abe1d0d9ff3f2`
- Prompt source blob SHA-1：`43026d3fd7922eb8f1d4b52b1a570a690557c8c5`
- `OUTLINE_TEMPLATE` source lines：`637—735`
- evaluated `OUTLINE_TEMPLATE` UTF-8 SHA-256：`6462f9c1dfd835dfa19822fd461019434b83bed607e046781a6f492543658baf`
- evaluated `OUTLINE_TEMPLATE` 字符数：`3060`

## 作者方向来源

- source：`books/real-exp-compounding-narrative-downstream-v1/INPUT.md`
- source commit：`170da2221ca38948dce66fa0a48041cfeeede75b`
- source blob SHA-1：`92bf6edf62ae5c378a6a3c6fb01c9ee24a84060d`
- copied `INPUT.md` SHA-256：`c81f58f23d0f5ef457c5ef8294ed6c9a5868e313c7de2ff1635bee2be582ba96`
- 复制校验：新旧文件字节逐字一致。

## Candidate A 冻结输入

来源目录：`books/real-exp-compounding-narrative-downstream-v1/candidate-a/`；来源 commit：`170da2221ca38948dce66fa0a48041cfeeede75b`。

- `fantasy_seed.md`：source SHA-256 `81923fbf33e8eff3c4f8ed9b4a84f1133eb56d4f412160f61a444722f07f49c1`；copied SHA-256 相同。
- `world_vision.md`（来源 `world_vision_response.md`）：source SHA-256 `69994c8727c1be9226eaa9651f2b622d80a32c720428eab2197a4afc4dc59560`；copied SHA-256 相同。
- `story_program.md`（来源 `story_program_response.md`）：source SHA-256 `16c10c8d23004213f3d67d6887a84543cd282e8d6fa684a4c13e39f62349cdf8`；copied SHA-256 相同。

## Candidate B 冻结输入

来源目录：`books/real-exp-compounding-narrative-downstream-v1/candidate-b/`；来源 commit：`170da2221ca38948dce66fa0a48041cfeeede75b`。

- `fantasy_seed.md`：source SHA-256 `2287e791e3e5a3545756f1c38fbc875f5de1e7443db989838bfa9e3df960bcf9`；copied SHA-256 相同。
- `world_vision.md`（来源 `world_vision_response.md`）：source SHA-256 `1414f5121143c8267e16fe2d1372f12d7d132947913d28310e07c29ce3704e76`；copied SHA-256 相同。
- `story_program.md`（来源 `story_program_response.md`）：source SHA-256 `78f2e3289169adf473aa1f25b6d1eac87cc1a31652844450fedab84e8f8e30ab`；copied SHA-256 相同。

## 生成与审查状态

- Frozen Creative Chain：已记录，禁止修改。
- Outline Agent A：`01a02082-a40d-7e70-b0b0-7f0e6a3ef849`，已生成一次；response SHA-256 `6010208e2bc0310230dafd468d4a82af718b5a86bdf3df651f0cdfc07dbc91d0`，prompt SHA-256 `e4de2a9371c52db3404ff4f8d35a4f3e80e9f1d24cb0c9c3683c340a34e87859`。
- Outline Agent B：`01a02082-a53f-72e2-928c-68199c73425d`，已生成一次；response SHA-256 `746a78a70791f2e66a308310452c3fa7a7d28957bae797f46ee99caef7cd81b8`，prompt SHA-256 `b9433c81aeba5cff77c31635ac386685829a3929310264bbe033710598cd1122`。
- Prompt artifact 复核：初次保存的 A/B prompt 均出现输入拼接不完整；未重生成 Outline response。A/B 仅重建 `outline_prompt.md`，最终两个 prompt 均与正式 `generate_prompt` 逐字一致；response 文件未被修复操作修改。
- Outline Review A：Agent `01a02095-57f3-79b1-a1ee-46987b0b6f71`，已完成；review SHA-256 `afd418de4295c8a5e12d02dd778c48211c9dfaf4bfd1a9772aefb7a8dc7e15bf`。
- Outline Review B：Agent `01a02095-591f-7983-be3a-f1fef93acffa`，已完成；review SHA-256 `5cae6865fda6289d5608739665badc53dba9391bad8a65e41dd759381d47d8e9`。
- Cross-Candidate Review：Agent `01a0209e-09ac-76e2-8646-b7dbc35fbf56`，已完成；review SHA-256 `27689f333ea52dc599db9602bba85dabcfcb70ae905abc6ec313a2488bcd8c62`。
- Final Verdict：主 Agent 整合完成；SHA-256 `701f766be6134198a894bf0a18309329edae4facf2baa82f94cf15aec1f80f68`。
