# Novel Prose Realization Layer

## 定位

Novel Prose Realization 是 TheGreatNovel 的独立 prose 执行层，服务于 Draft 阶段。它与
`reference-corpus-distillation` 并列但不合并：前者理解故事设计，后者把已决定的事件写成自然中文。

它不是新的 Canon、不是 Planner、不是 Chapter Contract 生成器，也不是后期把整章盲目重写一遍的润色器。

## 权威边界

故事事实遵循：

`Chapter Contract > Canon > Current Scene Context > Prose Controls`

表达风格遵循：

`Current Book Prose DNA > Author Explicit Style Intent > Reference Corpus Prose Controls > Humanizer Generic Guidance > Generic LLM Prior`

Prose 层只改变 how to say，不改变 what happens。任何表达修复都必须保留事件顺序、线索、setup、payoff、
角色意图、不可逆改变和章节结尾状态。

## 数据分层

Reference Corpus 新增 `prose-dna/`，刻意不复用 `book-dna/`：

- `book-dna/`：读者承诺、推进语法、机制、回报与长篇结构；
- `prose-dna/`：句子、段落、叙述距离、对话、动作、感官、过渡、标点与回报呈现的写法观察；
- `prose-controls/`：只有在至少 4 本书、至少 3 个类别出现的跨书抽象控制；
- `novel-prose-realization`：Draft 阶段执行指令、审阅触发器和有界修复规则。

Prose DNA 每本书按照场景功能而非随机全文平均抽样，使用 opening、ordinary、dialogue、action、payoff、
aftermath、exposition、emotion、late、ending 等有界窗口。短 segment、解析警告和缺失功能保持
`UNKNOWN` 或 `NOT_APPLICABLE`，不伪造覆盖。

## Machine Contract

`prose-dna` 是 `reference-corpus-card-v1` 的独立 `card_type`，每张卡：

- 只有一个 `source_book_id`，`knowledge_level=BOOK_OBSERVATION`，`status=REFERENCE_ONLY`；
- 每个 sample window 带 `segment_id` 与 line range；
- 包含 15 个 prose observations 和 12 个 soft controls；
- `source_style_leakage_check=PASS` 只表示没有把来源正文、句式、口癖或签名隐喻写入卡片；
- `depends_on` 只指向同书的 `reference-book` 索引卡，表示来源关系，不代表故事规划依赖；
- 进入统一 `machine/cards.jsonl`，由 `prose_dna` 计数标识；不复制原文，不进入 Canon。

## Humanizer-zh 的采用边界

本层采纳的只是可迁移原则：删除填充和过度 signposting、避免机械二元/三段式、让句子与段落节奏随场景变化、
用具体动作和细节替换空泛总结、信任读者、保留角色个性与合理的不规则性。

不直接采用的规则包括：文章/营销文本中的宣传性词汇清单、Wikipedia 式文章结构、通用 1–10 分质量评分、
把某个连接词或标点视为全局禁用，以及任何“骗 AI 检测器”的目标。网文对话、战斗、修炼、专业现场和古风场景
必须由当前书与当前场景决定。

Influenced by: [`op7418/Humanizer-zh`](https://github.com/op7418/Humanizer-zh)。该项目 README 声明其核心文件
译自 `blader/humanizer`，实用工具部分参考 `hardikpandya/stop-slop`，上游依据 Wikipedia 的
“Signs of AI writing”观察；其 `LICENSE` 为 MIT。本文档只重写抽象原则到中文小说场景，不复制其技能文本、
文章示例或作者声音。

## ORIGINAL 小说

没有当前书正文时，不随机挑选参考书模仿。用 Reader Kernel、Genre/Tone、Narrative Drive 与选择出的
Prose Controls 形成 `Original Prose Profile`，并在后续章节根据作者显式意图逐步更新。Reference Corpus
只能提供变量和可选的写法控制。
