from pathlib import Path
import sys
root=Path(r'C:\dev\tgn-story-mvp-creativity-crossrepo-20260830')
sys.path.insert(0,str(root/'src'))
from story_mvp.premise_aperture import build_single_pass_prompt
exp=root/'books'/'real-exp-crossrepo-creativity-20260830-v1'
base=root/'books'/'real-exp-premise-aperture-20260829-v1'
quarry='''你是 TGN 的 Creative Quarry / 创意采石场。你不是 Premise Forge，不写完整小说前提，不决定 World / Power / Human / Story Authority。你的产物全部 Non-Canon、可丢弃，只负责给后续 Premise Forge 提供它自己不容易从模型平均先验里想到的原材料。\n\n方法来自对其他长篇创作系统的抽象：先研究/拆解再架构；只迁移结构与情绪功能；让世界人物像独立玩家一样先有欲望和动作；用少量可反复物件/痕迹承担信息与关系变化。不要提任何来源项目或已知小说，不复制角色、专名、事件组合或具体金手指。\n\n对下方作者方向挖四类原材料。它们必须具体、可感知、低术语，并尽量来自彼此不同的生活/生态/身体/历史/仪式/技术/游戏/社会经验，而不是继续生成“宗门、秘境、灵气、系统”的同义词。可以使用你已有的常识，但不要伪造需要精确考据的数据。\n\n严格禁止：\n- 不写完整 premise；\n- 不给未来主角设计人格、童年或使命；\n- 不生成完整 Power；\n- 不把四类素材互相解释成统一宇宙真相；\n- 不给素材评分或选最佳；\n- 不为了新奇堆抽象名词。\n\n严格输出：\n# CREATIVE QUARRY\n## A. Concrete Substrates｜4条\n每条：一句白话事实/现象 + 它天然允许哪些新动作/画面；不是完整世界。\n## B. Appetite / Emotion Pressures｜4条\n每条：一种具体想要/害怕/嫉妒/占有/炫耀/依恋/报复等压力 + 可见行为；不是主角人设。\n## C. Living Actor Engines｜4条\n每条：一个具体人/生物/小群体现在想要什么、下一步就会做什么、若没有主角仍会造成什么变化；不要写治理协调。\n## D. Recurring Carriers｜4条\n每条：一个物件/地点/身体痕迹/可见规则证据，能跨多次出现改变用途或含义；不要解释幕后真相。\n## E. Collision Invitations｜4条\n只写“哪两类原材料放在一起可能产生什么新动作/反差”，仍不得写成完整 premise。\n\n# 作者方向\n{direction}\n'''
for case in ['generic_fantasy','fast_multiworld','game_instance']:
    d=(base/case/'AUTHOR_DIRECTION.md').read_text(encoding='utf-8')
    cdir=exp/case
    cdir.mkdir(parents=True,exist_ok=True)
    (cdir/'AUTHOR_DIRECTION.md').write_text(d,encoding='utf-8')
    (cdir/'baseline_prompt.md').write_text(build_single_pass_prompt(author_direction=d),encoding='utf-8')
    (cdir/'quarry_prompt.md').write_text(quarry.format(direction=d),encoding='utf-8')
