from pathlib import Path
from story_mvp.character_prompts import generate_split_prompt
root=Path(r'C:\dev\tgn-story-mvp')
exp=root/'books'/'real-exp-private-prototype-upstream-20260826-traditional-v1'
read=lambda n:(exp/n).read_text(encoding='utf-8')
prompt=generate_split_prompt(
    mode='outline',
    template='',
    creative_direction=read('AUTHOR_DIRECTION.md'),
    world_vision=read('WORLD_VISION.md'),
    character_card=read('CHARACTER_EXPERIMENTAL.md'),
    character_initial_state=read('CHARACTER_INITIAL_STATE_EXPERIMENTAL.md'),
    proposal_context=read('STORY_PROGRAM_CURRENT_PRODUCTION.md'),
    book_content='',
    creative_state={'world_vision':{'status':'author_approved'},'character_card':{'status':'author_approved'},'proposal':{'status':'author_approved'}},
    selected_references=[],
    gbrain_inspiration=read('OUTLINE_CURRENT_GBRAIN.md'),
)
(exp/'OUTLINE_AFTER_FIX_PROMPT.md').write_text(prompt,encoding='utf-8')
print('prompt_chars',len(prompt))
