from story_mvp.character_prompts import HUMAN_PROMPT
from story_mvp.character_seeds import HUMAN_SEED_SCHEMA
from story_mvp.prompts import (
    DEFAULT_DIRECTOR_TEMPLATE,
    DEFAULT_STATE_DELTA_TEMPLATE,
    HYBRID_PROMPT_TEMPLATES,
    OUTLINE_TEMPLATE,
    REVIEW_TEMPLATE,
    STORY_PROGRAM_TEMPLATE,
)


def test_never_coordinator_is_wired_across_story_chain() -> None:
    marker = "主角永远不是协调员"
    assert marker in HUMAN_PROMPT
    assert marker in HUMAN_SEED_SCHEMA
    assert marker in STORY_PROGRAM_TEMPLATE
    assert marker in OUTLINE_TEMPLATE
    assert marker in REVIEW_TEMPLATE
    assert marker in DEFAULT_DIRECTOR_TEMPLATE
    assert marker in HYBRID_PROMPT_TEMPLATES["context_curator"]
    assert marker in HYBRID_PROMPT_TEMPLATES["authority_reviser"]


def test_major_reward_and_fast_growth_causality_reach_planning() -> None:
    for template in (STORY_PROGRAM_TEMPLATE, OUTLINE_TEMPLATE, REVIEW_TEMPLATE):
        assert "Major Reward Anchor" in template
        assert "Rapid Growth Needs Protagonist-Specific Causality" in template
        assert "Mystery Before Settlement" in template
        assert "Effective Opponent Adaptation" in template


def test_reviser_can_translate_backstage_language_and_compress_coordination() -> None:
    reviser = HYBRID_PROMPT_TEMPLATES["authority_reviser"]
    assert "Backstage Abstraction Translation" in reviser
    assert "Preservation First 保护正确故事，不保护 process carrier" in reviser
    assert "Named Entity Continuity Sweep" in reviser


def test_state_keeps_only_explicit_recurring_identity_facts() -> None:
    assert "固定性别称谓" in DEFAULT_STATE_DELTA_TEMPLATE
    assert "不要从名字猜性别/年龄" in DEFAULT_STATE_DELTA_TEMPLATE
