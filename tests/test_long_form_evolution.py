from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from story_mvp.app import app
from story_mvp.character_context import project_effective_world_reality
from story_mvp.character_prompts import generate_split_prompt
from story_mvp.gbrain_retrieval import build_retrieval_brief
from story_mvp.long_form_evolution import compose_effective_world, extract_world_horizon_handoff
from story_mvp.prompts import DEFAULT_STATE_DELTA_TEMPLATE, OUTLINE_TEMPLATE
from story_mvp.storage import (
    apply_state_delta_to_book,
    approve_character_artifact,
    approve_creative_artifact,
    approve_human_development,
    approve_world_expansion,
    create_book,
    read_book_payload,
    read_creative_payload,
    refresh_current_character,
    write_book,
    write_creative_artifact,
)
from story_mvp.workflow_state import workflow_status


WORLD = """# PROTAGONIST-BLIND WORLD VISION

## 普通人的生活与上升
普通人在山城和商路生活，年轻人可通过武馆或宗门修行。

## 力量体系与正常值
武者以真气淬体；开脉、凝罡、化域是当前公开大档。

### 精确力量主尺｜Frozen Grammar
主尺类型：大境界+数字子级
主尺名称：真气阶
精确位置格式：{大境界}{N}重
数字精度规则：每个大境界1—9重
当前可见范围：开脉1重—化域9重
当前大档位：开脉、凝罡、化域

## 社会现实与身份
青州有宗门、商盟和军府；中域只被确认更强、更大，尚未展开。

## 世界里真正值钱、值得想要的东西
武技、兵器、灵药、异兽材料和跨州入口都真实值钱。

## 世界正在发生的大事
青州之外的跨州商路正在恢复。

## 值得进入的地点、奇观与未知
中域与海上遗迹都只远远存在。

## 世界知识边界
普通人知道青州之外还有更高层世界；具体势力和力量生态未知。
"""

POWER = """# POWER SEED｜借一式
## World Power Normal → Power Asymmetry
普通武者学一门武技需要长期练习；持有者完整看过一式后可无损复现一次。
## Core Fantasy
看懂别人的高明一招，当场变成自己的一次底牌。
## 为什么读者会馋
第一次看见强招就能真的用出来。
## Growth Compatibility
### 正常修炼轴
真气与身体继续正常成长。
### 异常掌握轴
可保存的招式数量逐步增加。
### High-Tier Mutation
可把旧招与新武器形成复合。
### 永久边界
每一式使用后仍会消失。
## Legendary Power State
见过的顶级招式都可能成为一次真实底牌。
"""

HUMAN = """# HUMAN SEED｜顾野／想赢得漂亮
## 世界中的初始位置与成长环境
开局精确力量位置｜主尺：真气阶｜精确位置：开脉3重
山城普通家庭。
## Core Obsession
喜欢赢，也喜欢真正懂行的人看见自己赢得漂亮。
## Excess
会为一件漂亮兵器花掉本来不该花的钱。
## Behavior Signature
面对高收益会冒险，但讨厌长期被组织控制。
## 重要关系原点
沈照是会让他改变一部分风险判断的具体人。
## Initial State Seed
### 当前私人欲望
赢下一场能让自己离开山城的比赛。
## Audition Metadata（非 Canon）
### 人物钩子
看到好刀会先多看一眼。
"""


APPROVED = {
    "world_vision": {"status": "author_approved"},
    "power_seed": {"status": "author_approved"},
    "human_seed": {"status": "author_approved"},
    "character_card": {"status": "author_approved"},
    "proposal": {"status": "author_approved"},
}


def setup_book(tmp_path: Path, book_id: str = "evo") -> Path:
    directory = create_book(book_id, tmp_path)
    write_creative_artifact(book_id, "world_vision", WORLD, tmp_path, origin="author_edited")
    approve_creative_artifact(book_id, "world_vision", tmp_path)
    write_creative_artifact(book_id, "power_seed", POWER, tmp_path, origin="author_edited")
    write_creative_artifact(book_id, "human_seed", HUMAN, tmp_path, origin="author_edited")
    approve_character_artifact(book_id, tmp_path)
    write_creative_artifact(
        book_id,
        "proposal",
        "# STORY PROGRAM\n\n## 当前主线\n先在青州成长。\n",
        tmp_path,
        origin="author_edited",
    )
    approve_creative_artifact(book_id, "proposal", tmp_path)
    return directory


def apply_chapter_one_state(tmp_path: Path, book_id: str = "evo") -> None:
    book = read_book_payload(book_id, tmp_path)["book_content"]
    delta = """# Proposed Active Scene State
当前地点：州府。\n当前主动目标：准备离开青州。

# Proposed Persistent Canon
### Power / Capability
Current Power Position｜主尺：真气阶｜精确位置：开脉6重
顾野仍保有借一式；现已能保存三式。黑曜长刀可临时改变重量。

### Active Relationships
沈照｜准备去中域｜彼此信任且会改变顾野部分路线选择｜顾野答应若路线一致就同行｜尚未决定是否同行到底

### Identity / Access
顾野已是州府大比冠军，可合法加入一次跨州护送。

### Knowledge / Enemy State
青州旧敌已无法继续压住顾野；中域具体势力仍未知。

### World State
青州跨州商路已经恢复，第一批护送队将进入过去未详细展开的中域。

### Tracked Assets
黑曜长刀｜顾野｜随身｜完好｜州府大比后正式归他

# Proposed Chapter Summary
顾野赢下州府大比并拒绝军府长期编制，准备通过跨州护送离开青州。

# Proposed Open Promises
沈照的中域家族旧事仍未解决。
"""
    write_book(book_id, apply_state_delta_to_book(book, 1, delta), tmp_path)


def test_new_book_has_forward_evolution_storage(tmp_path: Path) -> None:
    create_book("evo", tmp_path)
    payload = read_creative_payload("evo", tmp_path)
    assert payload["world_expansions"] == ""
    assert payload["human_development"] == ""
    assert payload["current_character"] == ""
    assert not (tmp_path / "evo" / "world_expansions").exists()
    assert not (tmp_path / "evo" / "human_development").exists()
    assert not (tmp_path / "evo" / "CURRENT_CHARACTER.md").exists()


def test_world_expansion_is_forward_only_and_does_not_stale_origins(tmp_path: Path) -> None:
    directory = setup_book(tmp_path)
    result = approve_world_expansion(
        "evo",
        "# WORLD EXPANSION\n\n## 新增公共现实与普通生活\n中域有沿大河建立的武城群。\n\n## 新力量 / 威胁 / 身份 / 价值尺度\n### 精确力量主尺延展｜Macro\n沿用主尺：真气阶\n主尺语法改动：NONE\n新增可见范围：化域9重—天门9重",
        tmp_path,
        scope="macro",
        effective_from=1,
    )
    assert result["status"] == "approved"
    state = workflow_status(directory)["artifacts"]
    assert state["creative.power_seed"]["status"] == "DONE"
    assert state["creative.human_seed"]["status"] == "DONE"
    assert state["creative.character_card"]["status"] == "DONE"
    assert state["creative.story_program"]["status"] == "STALE"

    apply_chapter_one_state(tmp_path)
    with pytest.raises(ValueError, match="必须向前生效"):
        approve_world_expansion(
            "evo",
            "# WORLD EXPANSION\n\nretroactive",
            tmp_path,
            scope="macro",
            effective_from=1,
        )


def test_effective_world_uses_macro_and_bounded_instance_only_in_window() -> None:
    expansions = """# WORLD EXPANSION 0001
Scope: macro
Effective From Chapter: 101
Effective Until Chapter: 0

## 新增公共现实与普通生活
中域武城群成立。

## 世界人物欲望与正在发生的事
沈家正在秘密追捕一名叛徒。

## 新 World Horizon 能产生的不同故事可能性
可以写追捕、战争或夺宝。

# WORLD EXPANSION 0002
Scope: instance
Effective From Chapter: 121
Effective Until Chapter: 140

## 新增公共现实与普通生活
雾港世界的人靠潮钟决定出海时间。
"""
    before = compose_effective_world(WORLD, expansions, 100)
    inside = compose_effective_world(WORLD, expansions, 130)
    after = compose_effective_world(WORLD, expansions, 150)
    assert "中域武城群成立" not in before
    assert "中域武城群成立" in inside
    assert "雾港世界" in inside
    assert "中域武城群成立" in after
    assert "雾港世界" not in after

    authority = project_effective_world_reality(WORLD, expansions, 130)
    assert "FORWARD WORLD EXPANSION 1" in authority
    assert "雾港世界" in authority
    assert "沈家正在秘密追捕" not in authority
    assert "可以写追捕、战争或夺宝" not in authority


def test_current_character_compiles_two_layer_power_and_three_layer_human(tmp_path: Path) -> None:
    setup_book(tmp_path)
    apply_chapter_one_state(tmp_path)
    approved = approve_human_development(
        "evo",
        """# HUMAN DEVELOPMENT DELTA
顾野仍讨厌长期受组织控制；但经过多次与沈照共同承担真实风险后，沈照已从“会影响一部分判断”变成稳定例外：涉及她不可替代的损失时，他会主动改变原定离开路线。这个变化不推出他对其他人也更负责。
""",
        tmp_path,
    )
    assert approved["effective_from"] == 2
    result = refresh_current_character("evo", tmp_path)
    text = result["content"]
    assert "Power Origin Core｜Frozen" in text
    assert "借一式" in text
    assert "Current Power Portfolio" in text
    assert "保存三式" in text
    assert "Human Origin Core｜Frozen" in text
    assert "Human Development｜Forward-only Stable Deltas" in text
    assert "稳定例外" in text
    assert "Current Human State" in text
    assert "沈照" in text


def test_human_development_none_does_not_manufacture_delta(tmp_path: Path) -> None:
    setup_book(tmp_path)
    result = approve_human_development(
        "evo", "# HUMAN DEVELOPMENT DELTA\n\nNONE", tmp_path
    )
    assert result["status"] == "no_change"
    assert not list((tmp_path / "evo" / "human_development").glob("delta-*.md"))


def test_prompt_boundaries_keep_surprise_until_recollision(tmp_path: Path) -> None:
    setup_book(tmp_path)
    apply_chapter_one_state(tmp_path)
    refresh_current_character("evo", tmp_path)
    creative = read_creative_payload("evo", tmp_path)
    book = read_book_payload("evo", tmp_path)["book_content"]

    world_prompt = generate_split_prompt(
        mode="world_expansion",
        book_content=book,
        creative_direction="传统玄幻",
        world_vision=WORLD,
        world_expansions=creative["world_expansions"],
        proposal_context="## World Horizon Handoff\nSECRET STORY-PREPARED KEYHOLE",
        character_card="SECRET CHARACTER SHOULD NOT LEAK",
        current_character="SECRET CURRENT CHARACTER SHOULD NOT LEAK",
        creative_state=APPROVED,
        evolution_scope="macro",
        effective_from_chapter=2,
    )
    assert "SECRET CHARACTER SHOULD NOT LEAK" not in world_prompt
    assert "SECRET STORY-PREPARED KEYHOLE" not in world_prompt
    assert "CURRENT WORLD STATE" in world_prompt
    assert "青州跨州商路已经恢复" in world_prompt
    assert "保存三式" not in world_prompt
    assert "沈照" not in world_prompt
    assert "World Independence ≠ World Amnesia" in world_prompt
    assert "世界上的凹痕" in world_prompt
    assert "主角私人欲望" not in world_prompt

    human_prompt = generate_split_prompt(
        mode="human_development",
        book_content=book,
        world_expansions="# FUTURE SECRET WORLD",
        character_card=creative["character_card"],
        human_development="",
        creative_state=APPROVED,
    )
    assert "FUTURE SECRET WORLD" not in human_prompt
    assert "Frozen Human Core" in human_prompt or "FROZEN HUMAN CORE" in human_prompt

    refresh = generate_split_prompt(
        mode="story_refresh",
        book_content=book,
        creative_direction="传统玄幻",
        world_vision=WORLD,
        world_expansions="""# WORLD EXPANSION 0001\nScope: macro\nEffective From Chapter: 2\nEffective Until Chapter: 0\n\n## 新增公共现实与普通生活\n中域武城群。""",
        character_card=creative["character_card"],
        current_character=creative["current_character"],
        creative_state=APPROVED,
        proposal_context=creative["proposal"],
        effective_from_chapter=2,
    )
    assert "中域武城群" in refresh
    assert "CURRENT CHARACTER｜Deterministic Forward Snapshot" in refresh
    assert "Independent World × Current Character" in refresh
    assert "Route-Bound Acquisition 继续成立" in refresh
    assert "No Universal World Tour 继续成立" in refresh


def test_world_expansion_keeps_public_world_impact_but_not_private_character_state() -> None:
    book = """# 当前状态、未兑现承诺与作者备注

## PERSISTENT CANON
### Power / Capability
顾野现在是天门2重；SECRET_PRIVATE_POWER：只有他知道移动异常怎样触发。
### Active Relationships
SECRET_PRIVATE_RELATIONSHIP：顾野与沈照关系亲密。
### Identity / Access
顾野已能独立跨州。
### Knowledge / Enemy State
顾野知道中域河城群存在。
### World State
顾野在三万人的青州会武中以天门2重公开击败天门5重镇州使，并斩杀封锁跨州商路十年的黑角王。第一批商队已经把顾野姓名、2重越级胜5重战绩与商路重开的消息带向中域；青州三宗与边境军府都已因此改变行动。
### Tracked Assets
黑曜刀｜顾野｜随身｜完好｜已归属
"""
    prompt = generate_split_prompt(
        mode="world_expansion",
        book_content=book,
        creative_direction="传统玄幻",
        world_vision=WORLD,
        world_expansions="",
        creative_state={"world_vision": {"status": "author_approved"}},
        evolution_scope="macro",
        effective_from_chapter=101,
    )
    assert "顾野在三万人的青州会武" in prompt
    assert "天门2重" in prompt
    assert "天门5重" in prompt
    assert "黑角王" in prompt
    assert "SECRET_PRIVATE_POWER" not in prompt
    assert "SECRET_PRIVATE_RELATIONSHIP" not in prompt
    assert "公开主尺位置" in prompt
    assert "报价、招揽、敌意、警戒、路线或资源行动" in prompt
    assert "谁做了什么 → 世界因此怎样变了" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "只保存世界事实，不保存其隐藏能力原理、私人动机、关系或 Build" in DEFAULT_STATE_DELTA_TEMPLATE


def test_story_program_prepares_handoff_but_does_not_prewrite_next_world() -> None:
    prompt = generate_split_prompt(
        mode="idea",
        creative_direction="传统玄幻长篇",
        world_vision=WORLD,
        character_card="# CHARACTER CARD\n\n## POWER CORE｜Frozen Authority\n借一式\n\n## HUMAN CORE｜Frozen Authority\n想赢。\n\n## Composition Boundary\n",
        character_initial_state="# INITIAL CHARACTER STATE\n\n## current_desire\n先离开山城。",
        creative_state=APPROVED,
    )
    assert "当前 Story Program 只具体规划到当前已批准 World Horizon" in prompt
    assert "## World Horizon Handoff" in prompt
    assert "不得替尚未生成的下一世界设计宝物、能力、势力、人物" in prompt
    assert "protagonist-blind World Expansion" in prompt
    assert "Route-Bound Acquisition" in prompt
    assert "先有人物选择与路线，再有新优势" in prompt
    assert "No Universal World Tour" in prompt
    assert "世界大事不是主角必须逐一打卡的升级路线" in prompt


def test_handoff_is_extracted_for_orchestration_and_outline_stops_at_it(tmp_path: Path) -> None:
    setup_book(tmp_path)
    proposal = """# STORY PROGRAM

## 当前 World Horizon 的长期故事主线
### 阶段1｜青州终局
青州旧线完成。

## World Horizon Handoff
- **触发条件：** 顾野完成跨州护送并真正越过青州边界。
- **Expansion Scope：** `macro`
- **为什么此时必须扩：** 青州的力量、身份与主要争夺已经被活透。
- **Carry Forward：** 跨州商路恢复；沈照旧事未完；黑曜长刀仍在顾野手里。
- **World Expansion Task：** 在触发条件成立后，运行 protagonist-blind World Expansion；World Agent 不读取 Current Character / Power Stack / Human / Future Story。扩展批准后再编译 Current Character，并运行 Story Refresh。

## 远期仍值得追的东西
沈照旧事。
"""
    write_creative_artifact("evo", "proposal", proposal, tmp_path, origin="author_edited")
    approve_creative_artifact("evo", "proposal", tmp_path)
    payload = read_creative_payload("evo", tmp_path)
    handoff = payload["world_horizon_handoff"]
    assert handoff == extract_world_horizon_handoff(proposal)
    assert "跨州护送" in handoff
    assert "## 远期仍值得追的东西" not in handoff
    assert "`World Horizon Handoff` 是 Outline 的前向边界" in OUTLINE_TEMPLATE
    assert "只列到触发章就停止" in OUTLINE_TEMPLATE


def test_refreshed_outline_reads_effective_world_and_current_character(tmp_path: Path) -> None:
    setup_book(tmp_path)
    apply_chapter_one_state(tmp_path)
    approve_world_expansion(
        "evo",
        """# WORLD EXPANSION
## 新增公共现实与普通生活
中域沿大河分布着十二座武城。
## 新力量 / 威胁 / 身份 / 价值尺度
### 精确力量主尺延展｜Macro
沿用主尺：真气阶
主尺语法改动：NONE
新增可见范围：化域9重—天门9重

化域在青州近乎传说，在中域只是能独领一支商队的门槛。
## 新地点、势力与公共识别
百铸台是公开出售高阶兵器的中立重镇。
## 世界人物欲望与正在发生的事
几个宗门正在争一条旧河道。
## 真正值得想要或进入的东西
能承受化域真气的兵器在这里真实流通。
## 新 World Horizon 能产生的不同故事可能性
战争、交易、师承与远行都可能成立。
## 仍未知的边界
更高层强者的来源仍未知。
## 与旧 World Root 的连续性
真气与开脉/凝罡/化域仍是同一套基础 Grammar。
""",
        tmp_path,
        scope="macro",
        effective_from=2,
    )
    refresh_current_character("evo", tmp_path)
    creative = read_creative_payload("evo", tmp_path)
    prompt = generate_split_prompt(
        mode="outline",
        template="",
        book_content=read_book_payload("evo", tmp_path)["book_content"],
        creative_direction="传统玄幻",
        world_vision=WORLD,
        world_expansions=creative["world_expansions"],
        character_card=creative["character_card"],
        character_initial_state=creative["character_initial_state"],
        current_character=creative["current_character"],
        creative_state=APPROVED,
        proposal_context=creative["proposal"],
    )
    assert "EFFECTIVE WORLD｜Root + Approved Forward Expansions" in prompt
    assert "中域沿大河分布着十二座武城" in prompt
    assert "CURRENT CHARACTER｜Forward Authority" in prompt
    assert "保存三式" in prompt
    assert "Character Initial State｜T0 only" not in prompt


def test_api_periodic_refresh_flow_requires_fresh_current_character(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    setup_book(tmp_path)
    client = TestClient(app)

    world_prompt = client.post(
        "/api/prompt",
        json={
            "book_id": "evo",
            "mode": "world_expansion",
            "evolution_scope": "macro",
            "effective_from_chapter": 1,
        },
    )
    assert world_prompt.status_code == 200
    assert "看不到 Current Character" in world_prompt.json()["prompt"]
    assert "想赢得漂亮" not in world_prompt.json()["prompt"]

    approved = client.post(
        "/api/books/evo/world-expansions/approve",
        json={
            "scope": "macro",
            "effective_from": 1,
            "effective_until": 0,
            "content": """# WORLD EXPANSION
## 新增公共现实与普通生活
中域武城群沿大河存在。
## 新力量 / 威胁 / 身份 / 价值尺度
### 精确力量主尺延展｜Macro
沿用主尺：真气阶
主尺语法改动：NONE
新增可见范围：化域9重—天门9重

化域在这里不再是顶点。
## 新地点、势力与公共识别
百铸台是公开兵器重镇。
## 世界人物欲望与正在发生的事
当地宗门正在争河道。
## 真正值得想要或进入的东西
高阶兵器公开交易。
## 新 World Horizon 能产生的不同故事可能性
战争、交易与师承都可能发生。
## 仍未知的边界
更高层仍未知。
## 与旧 World Root 的连续性
真气 Grammar 不变。
""",
        },
    )
    assert approved.status_code == 200

    blocked = client.post(
        "/api/prompt",
        json={"book_id": "evo", "mode": "story_refresh", "effective_from_chapter": 1},
    )
    assert blocked.status_code == 400
    assert "CURRENT_CHARACTER" in blocked.json()["detail"]

    refreshed = client.post("/api/books/evo/current-character/refresh")
    assert refreshed.status_code == 200
    story_refresh = client.post(
        "/api/prompt",
        json={"book_id": "evo", "mode": "story_refresh", "effective_from_chapter": 1},
    )
    assert story_refresh.status_code == 200
    text = story_refresh.json()["prompt"]
    assert "中域武城群沿大河存在" in text
    assert "CURRENT CHARACTER｜Deterministic Forward Snapshot" in text


def test_world_vision_prompt_requires_multiple_route_bearing_possibilities() -> None:
    prompt = generate_split_prompt(
        mode="world_vision",
        creative_direction="成熟中文男频玄幻成长长篇",
    )
    assert "World Possibility Ecology" in prompt
    assert "不同的人真的走不同路线时" in prompt
    assert "不设类别配额" in prompt


def test_world_expansion_gbrain_brief_is_protagonist_blind() -> None:
    brief = build_retrieval_brief(
        mode="world_expansion",
        creative_direction="传统玄幻",
        world_vision=WORLD,
        character_card="SECRET CURRENT CHARACTER KEY SHAPE",
        proposal_context="SECRET STORY HANDOFF TAILORED FOR PROTAGONIST",
        book_content="SECRET BOOK POWER STACK",
        current_long_block="SECRET FUTURE PLAN",
        current_outline="SECRET NEXT REWARD",
        recent_summaries="SECRET RELATIONSHIP STATE",
    )
    assert "SECRET CURRENT CHARACTER KEY SHAPE" not in brief
    assert "SECRET STORY HANDOFF TAILORED FOR PROTAGONIST" not in brief
    assert "SECRET BOOK POWER STACK" not in brief
    assert "SECRET FUTURE PLAN" not in brief
    assert "SECRET NEXT REWARD" not in brief
    assert "SECRET RELATIONSHIP STATE" not in brief
    assert "World Expansion 用途" in brief


def test_outline_cannot_bypass_stale_story_or_current_character(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("STORY_MVP_WORKSPACE", str(tmp_path))
    setup_book(tmp_path)
    apply_chapter_one_state(tmp_path)
    refresh_current_character("evo", tmp_path)
    client = TestClient(app)

    blocked_story = client.post("/api/prompt", json={"book_id": "evo", "mode": "outline"})
    assert blocked_story.status_code == 400
    assert "fresh Story Program" in blocked_story.json()["detail"]

    creative = read_creative_payload("evo", tmp_path)
    write_creative_artifact(
        "evo",
        "proposal",
        creative["proposal"] + "\n## Refresh Marker\n当前人物已进入未来规划。\n",
        tmp_path,
        origin="author_edited",
    )
    approve_creative_artifact("evo", "proposal", tmp_path)
    allowed = client.post("/api/prompt", json={"book_id": "evo", "mode": "outline"})
    assert allowed.status_code == 200

    apply_chapter_one_state_again = read_book_payload("evo", tmp_path)["book_content"]
    delta = """# Proposed Active Scene State
当前地点：跨州商路。\n当前主动目标：继续向中域走。

# Proposed Persistent Canon
### Power / Capability
顾野已把黑曜长刀与借一式的换位打法用熟。

### World State
跨州商路已经正式通行。

# Proposed Chapter Summary
顾野踏上跨州商路。

# Proposed Open Promises
沈照旧事仍未解决。
"""
    write_book("evo", apply_state_delta_to_book(apply_chapter_one_state_again, 2, delta), tmp_path)
    blocked_character = client.post("/api/prompt", json={"book_id": "evo", "mode": "outline"})
    assert blocked_character.status_code == 400
    assert "CURRENT_CHARACTER" in blocked_character.json()["detail"]
