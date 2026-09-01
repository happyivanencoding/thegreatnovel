from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(r"C:\dev\tgn-story-mvp")
OUT = ROOT / "books" / "real-prod-wo-shen-cang-zhu-jie-40ch-20260901-v1"

spec = importlib.util.spec_from_file_location("run40", OUT / "run_to_40.py")
run40 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(run40)

start, end = 31, 40
book = run40.read(OUT / "BOOK_AFTER_CH30.md")
world = run40.read(OUT / "WORLD_VISION.md")
character = run40.read(OUT / "CHARACTER.md")
story = run40.read(OUT / "STORY_PROGRAM_31_40.md")
world_expansions = run40.read(OUT / "WORLD_EXPANSIONS.md")
status = run40.parse_book_sections(book)["status"]
current_character = run40.compile_current_character(
    character_card=character,
    status_text=status,
    human_development="",
    chapter_number=start,
)
run40.write(OUT / "planning" / "current-character-through-30.md", current_character)

outline_direction = """当前已完成第30章，作者已授权后续自行选择并持续写到第40章，不再等待人工审批。第31—40章使用已批准 Story Program：宁烬进入无墙万门宫殿，选择阮七娘—共影棚—第八接点路线，永久取得“双影为邻”，并在无影换席高潮完成双真+双影为邻+风髓双口+未尽续行四层复合。
第40章只是当前大型 Horizon 的阶段收束，不是小说终局；禁止 `FINAL NOVEL END`，禁止结清裴照临、黑门骨来源、诸界数量、镜海旧线等全书长期承诺。必须保留普通 World Horizon Handoff 与长篇继续动力。
RSE-07/08/09 的 Event Atom、State Residue、Timing Boundary 和 Reader Anchors 必须完整保护：RSE-07完成三个高价值方向同时可选且真实错失；RSE-08在无影换席前一夜取得双影为邻并完成灵海4重/接影境7级双尺 Public Proof；RSE-09完成无影换席与四层复合，并按已批准的具体人物后果结账。
正确当前 Canon：灵海4重；双真两个同等真实位置且共享元力/伤势/死亡；风髓双口只能在双真同时存在且两端未堵死时导引风、热、液压等流动力量，不能传人或固体、不增加元力；未尽续行只接续已经真正开始的具体动作；双影为邻取得前不存在，取得后只连接宁烬两具真身自己的两道真影，使宁烬亲手开始的动作及直接驱动物体把两处影边视作相邻下一寸，不增加第三端点、不提供力量、不自动成功。
第31章必须先兑现宫殿公共常识：门是一轮太阳划出的边界；影子落门内会被太阳逐步认领；两扇门是否相近看影子能否连续接上，影接则天涯为邻。用生活与现场讲清，不写百科。
宁烬不是协调员。陆移烛、宿无眼、贺燃灯、叶回纱、苏照庭等继续按自己的欲望行动；宁烬真实错过的悬胎院身体谱、黑根田、背日兽、祖门太阳等不得后续补拿。避免兵籍/门权/资源分配流程、漂亮二段论、固定爱钱口癖、Competence Filler。
AGGRESSIVE 兑现：只要 Story Program 已批准，大场面、群体震动、懂行者精确尺校准、关键人物改价/改战术、战利品与关系收益都可以吃满，不因“克制”自动削弱。"""

folder = OUT / "planning" / "outline-31-40"
gbrain = run40.safe_gbrain(
    "outline",
    folder,
    book_content=book,
    creative_direction=outline_direction,
    world_vision=world,
    character_card=character,
    proposal_context=story,
    recent_summaries=status,
)
prompt = run40.generate_split_prompt(
    mode="outline",
    book_content=book,
    creative_direction=outline_direction,
    world_vision=world,
    world_expansions=world_expansions,
    character_card=character,
    current_character=current_character,
    creative_state=run40.CREATIVE_STATE,
    proposal_context=story,
    selected_references=[],
    gbrain_inspiration=gbrain,
)
response = run40.run_acp(
    label="outline-31-40",
    model="gpt-5.6-luna",
    effort="high",
    prompt=prompt,
    folder=folder,
    timeout=7200,
)
planned_book = run40.build_outline_book(
    response=response,
    current_book=book,
    story_program=story,
    start=start,
    end=end,
    folder=folder,
)
run40.write(OUT / "BOOK_PLAN_31_40.md", planned_book)
print("OUTLINE_31_40_READY", flush=True)

chapters = {
    n: run40.read(OUT / "chapters" / f"chapter-{n:04d}.md").strip()
    for n in range(1, 31)
}

book_after_35, chapters = run40.run_batch(
    batch_start=31,
    book=planned_book,
    world=world,
    character=character,
    story_program=story,
    world_expansions=world_expansions,
    chapters=chapters,
)
print("BATCH_31_35_READY", flush=True)

book_after_40, chapters = run40.run_batch(
    batch_start=36,
    book=book_after_35,
    world=world,
    character=character,
    story_program=story,
    world_expansions=world_expansions,
    chapters=chapters,
)
run40.validate_book_content_for_save(book_after_40)
run40.write(OUT / "BOOK_AFTER_CH40.md", book_after_40)
run40.write(OUT / "CHAPTERS_0031_0040.md", "\n\n".join(chapters[n].strip() for n in range(31, 41)))
full = "\n\n".join(chapters[n].strip() for n in range(1, 41)).strip() + "\n"
run40.write(OUT / "FULL_40_CHAPTERS.md", full)
run40.write(OUT / "FULL_40_CHAPTERS.txt", full)
print("BATCH_36_40_READY", flush=True)
print("CH31_40_COMPLETE", flush=True)
print("FULL40_READY", len(full), flush=True)
