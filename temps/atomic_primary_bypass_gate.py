from __future__ import annotations
import re,time
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class GateResult:
    supported: bool
    pass_: bool
    blockers: tuple[str,...]
    evidence: tuple[str,...]
    elapsed_ms: float


def _has(text:str, pattern:str)->bool:
    return re.search(pattern,text,re.S) is not None


def _all(text:str, patterns:Iterable[str])->bool:
    return all(_has(text,p) for p in patterns)


def _window(text:str, anchors:Iterable[str], *, radius:int=260)->str:
    positions=[]
    for anchor in anchors:
        m=re.search(anchor,text,re.S)
        if m: positions.append(m.start())
    if not positions:return ''
    lo=max(0,min(positions)-radius); hi=min(len(text),max(positions)+radius)
    return text[lo:hi]


def gate_jiuchui_ch14(text:str)->GateResult:
    t0=time.perf_counter(); blockers=[]; evidence=[]
    checks=(
      ('J14_WEDGE_CYCLE', _all(text,(r'回潮楔',r'锁潮|锁住|扣住|定住',r'改向|改变.{0,8}方向|偏转|转弯|折向',r'释放|放开|泄出|冲出'))),
      ('J14_PUBLIC_RULER', _all(text,(r'成炉',r'百炉会|见证|老者|试官|懂行',r'一段潮势|整段潮势|改变.{0,8}方向|改向'))),
      ('J14_WEDGE_AUTONOMY', _has(text,r'回潮楔.{0,28}(不卖|归我|归顾停舟|自己用|自行处置)|不卖.{0,18}回潮楔')),
      ('J14_MINING_SHARE', _all(text,(r'个人矿利|矿利.{0,12}(份额|另记|名下)',r'确认|另记|份额|名下'))),
      ('J14_WATER_RIGHT', _all(text,(r'砺骨部',r'水路',r'不.{0,8}(并入|属于|算作).{0,12}矿权|不随.{0,12}矿权|另行结算'))),
      ('J14_PAID_INDEPENDENT_COOP', _all(text,(r'少东家',r'固定报酬|报酬.{0,12}(写|定|潮铢)',r'损失|货损|损耗',r'合作|承揽|不是.{0,8}(跑腿|卖命|我的人)|新规矩'))),
      ('J14_COOLDOWN', _all(text,(r'残压',r'不能.{0,12}(连用|连续|第二次|再压|再用)|散尽.{0,12}(才能|再)|不能立刻'))),
      ('J14_DEADLINE', _all(text,(r'十二日地潮',r'旧关',r'第一批货|这批粮|粮队|粮车',r'前'))),
    )
    for fid,ok in checks:
        if ok:evidence.append(fid)
        else:blockers.append(fid)
    # Wrong settlement / ownership states are explicit hard fails if present.
    forbidden=(
      ('J14_FALSE_MINING_PAYMENT',r'矿利.{0,18}(已经|当场|立刻).{0,8}(到账|结清|付清)|个人矿利.{0,12}[一二三四五六七八九十百千0-9]+潮铢.{0,8}(拿到|到账)'),
      ('J14_WEDGE_TRANSFERRED',r'回潮楔.{0,15}(卖给|交给|归阮|归了阮)|阮青蜃.{0,15}(拿走|收走).{0,8}回潮楔'),
    )
    for fid,pat in forbidden:
        if _has(text,pat):blockers.append(fid)
    elapsed=(time.perf_counter()-t0)*1000
    return GateResult(True,not blockers,tuple(blockers),tuple(evidence),elapsed)


def gate_shadow_ch9(text:str)->GateResult:
    t0=time.perf_counter(); blockers=[]; evidence=[]
    checks=[]
    checks.append(('S9_TREATMENT', _all(text,[r'陆绾',r'伤口|伤药|药粉|布带|包扎|缠紧'])))
    checks.append(('S9_MIXED_MOTIVE', _all(text,[r'短兵',r'想要|想拿|要.{0,6}短兵|短兵.{0,10}想',r'不想.{0,12}(你|陆绾).{0,6}死|也想.{0,8}(救|让).{0,8}(你|陆绾).{0,6}(活|出来)|你.{0,8}也想救'])))
    checks.append(('S9_DAMAGE_RETURN_BOUNDARY', _all(text,[r'分影|影身',r'(挨|受|撞|耗).{0,20}(伤|力|骨)|伤.{0,12}(回|落|到).{0,8}(你|本体|自己)',r'最后.{0,16}(你|自己).{0,8}(受|身上)|回到.{0,10}(本体|你身上)'])))
    checks.append(('S9_COOP_BOUNDARY', _all(text,[r'以后|再要|下次|再',r'先.{0,8}(告诉|说)|不能再|别.{0,12}(扔|送死)|该一起|一起挡'])))
    checks.append(('S9_RIVAL_REPRICE', _all(text,[r'顾斜阳',r'普通.{0,12}(护卫|竞争|散修)|判断|重新|再按|不再'])))
    checks.append(('S9_INJURY_PENDING', _has(text,r'走不了|站不住|失力|脱力|一个时辰|半个时辰|伤势.{0,12}(没|未|还)|腿.{0,12}(撑不|伤)')))
    checks.append(('S9_RECORD_ANOMALY', _all(text,[r'领队|铜羽商盟',r'记录|名册|记录板',r'两条路|两条行动|两个位置|两边',r'普通二阶.{0,18}(做不到|不能|解释|写)|不能再按.{0,12}普通二阶',r'沉昼城|上面的人|上层',r'护卫|待遇|价值'])))
    for fid,ok in checks:
        if ok:evidence.append(fid)
        else:blockers.append(fid)
    forbidden=[
      ('S9_REMOTE_KNOWLEDGE',r'(本体|顾临川).{0,20}(隔着|远处|另一边).{0,20}(看见|知道|感知).{0,20}(分影|影身)'),
      ('S9_NEW_PAYMENT_SETTLED',r'(新|更高).{0,8}(护卫)?(待遇|价钱|报酬).{0,12}(到账|已定|已经给|付了)|又.{0,6}(给|塞).{0,6}(钱|钱袋|预付)'),
    ]
    for fid,pat in forbidden:
        if _has(text,pat):blockers.append(fid)
    elapsed=(time.perf_counter()-t0)*1000
    return GateResult(True,not blockers,tuple(blockers),tuple(evidence),elapsed)

def evaluate(sample:str,text:str)->GateResult:
    if sample=='jiuchui_ch14':return gate_jiuchui_ch14(text)
    if sample=='shadow_ch9':return gate_shadow_ch9(text)
    # Fail closed: these two shapes need semantic actor/location/unknown checks that
    # current deterministic evidence adapter cannot prove safely.
    return GateResult(False,False,(f'{sample}:UNSUPPORTED_TYPED_REALIZATION',),(),0.0)
