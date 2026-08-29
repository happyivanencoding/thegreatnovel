"""Experimental deterministic Atomic Chapter Obligations compiler and gate.

This is experiment code, not production wiring. The gate may prove ADOPT, but it may
never guess ADOPT: ambiguity, unsupported clauses, or conflicting terminal authority
must fall back to the existing Full Luna-high Authority Reviser.
"""
from __future__ import annotations

import difflib
import json
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence


class ObligationKind(str, Enum):
    MISSION_CLAUSE = "mission_clause"
    ACTOR_ACTION_OBJECT = "actor_action_object"
    DIRECT_RESULT = "direct_result"
    TERMINAL_STATE = "terminal_state"
    ENDING = "ending"
    OWNERSHIP = "ownership"
    MONEY = "money"
    TIME_WINDOW = "time_window"
    POWER_POSITION = "power_position"
    POWER_BOUNDARY = "power_boundary"
    PUBLIC_PROOF = "public_proof"
    READER_RELEASE = "reader_release"
    UNRESOLVED_FACT = "unresolved_fact"
    RELATIONSHIP_STATE = "relationship_state"
    HUMAN_CUE = "human_cue"
    COMMERCIAL_VALUE = "commercial_value"
    SOURCE_CONFLICT = "source_conflict"


class ObligationMode(str, Enum):
    MUST_HOLD = "must_hold"
    MUST_NOT_HOLD = "must_not_hold"
    MUST_REMAIN_UNKNOWN = "must_remain_unknown"
    TERMINAL = "terminal"
    PRESERVE_IF_PRESENT = "preserve_if_present"
    CONDITIONAL = "conditional"
    DIAGNOSTIC_FALLBACK = "diagnostic_fallback"


class GateSeverity(str, Enum):
    HARD = "hard"
    CONDITIONAL = "conditional"
    SOFT = "soft"


class CheckStatus(str, Enum):
    PASS = "pass"
    PASS_PRESERVED = "pass_preserved"
    NOT_TRIGGERED = "not_triggered"
    FAIL = "fail"
    UNKNOWN = "unknown"
    CONFLICT = "conflict"


@dataclass(frozen=True)
class AtomicObligation:
    id: str
    kind: ObligationKind
    mode: ObligationMode
    severity: GateSeverity
    source_field: str
    source_text: str
    subject: str = ""
    action: str = ""
    object: str = ""
    status: str = ""
    qualifiers: tuple[str, ...] = ()
    boundary: str = ""
    validator: Mapping[str, Any] = field(default_factory=dict)
    primary_evidence_paragraphs: tuple[int, ...] = ()
    protected_category: str = ""

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["kind"] = self.kind.value
        value["mode"] = self.mode.value
        value["severity"] = self.severity.value
        value["qualifiers"] = list(self.qualifiers)
        value["primary_evidence_paragraphs"] = list(self.primary_evidence_paragraphs)
        value["validator"] = dict(self.validator)
        return value


@dataclass(frozen=True)
class ObligationCheck:
    obligation_id: str
    status: CheckStatus
    reason: str
    evidence: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "obligation_id": self.obligation_id,
            "status": self.status.value,
            "reason": self.reason,
            "evidence": list(self.evidence),
        }


@dataclass
class ObligationPack:
    chapter: int
    protagonist: str
    mission_fields: dict[str, str]
    obligations: list[AtomicObligation]
    source_conflicts: list[str]
    unsupported_clauses: list[str]
    diagnostics: list[str]
    primary_paragraph_count: int

    @property
    def preflight_eligible(self) -> bool:
        return not self.source_conflicts and not self.unsupported_clauses

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": "atomic-obligations-v0.3-boundary-calibrated",
            "chapter": self.chapter,
            "protagonist": self.protagonist,
            "mission_fields": self.mission_fields,
            "obligations": [item.to_dict() for item in self.obligations],
            "source_conflicts": self.source_conflicts,
            "unsupported_clauses": self.unsupported_clauses,
            "diagnostics": self.diagnostics,
            "primary_paragraph_count": self.primary_paragraph_count,
            "preflight_eligible": self.preflight_eligible,
        }


MISSION_FIELDS = (
    "触发事件", "主角行动", "对手或世界反应", "直接结果", "状态变化", "结尾推动力",
)
ACTION_CLASSES: dict[str, tuple[str, ...]] = {
    "acquire": ("取得", "获得", "拿到", "领到", "收到", "落到", "交到", "签下"),
    "register": ("登记", "落籍", "入册", "记入", "留档", "盖印"),
    "possess": ("持有", "持原", "拿着", "保留", "留下", "归", "在手", "带走", "收好"),
    "transfer": ("交给", "送入", "送到", "递给", "交回", "传入", "带回"),
    "refuse": ("拒绝", "不交", "不卖", "不让", "不再", "不同意"),
    "accept": ("接受", "同意", "签", "认下", "承认"),
    "protect": ("保住", "守住", "稳住", "护住", "脱险", "救出"),
    "sacrifice": ("失守", "放弃", "牺牲", "毁弃", "毁掉", "损毁", "坍塌"),
    "lose": ("失去", "落空", "无法兑现", "放弃", "不再交付", "没了"),
    "move": ("进入", "穿过", "送到", "拖到", "拖", "滑去", "带到", "改向", "压回", "撤离", "出发"),
    "depart": ("出发", "上车", "驶去", "离开", "随队", "启程"),
    "confirm": ("确认", "证明", "判定", "公开校准", "公开确认", "记下", "现场见证", "共同看过"),
    "power_transition": ("正式进入", "突破", "晋升", "成为", "成炉已成", "第一次正式"),
    "limit": ("不能", "不得", "尚未", "仍未", "只携带", "承不住", "不可", "未完成"),
    "reprice": ("重新定价", "重新估价", "目光变", "报价", "入册", "不再把"),
    "repair": ("修复", "散压", "散尽", "裂痕", "细裂"),
    "search": ("寻找", "找", "追索", "逼近", "要求查看", "传来消息"),
    "pay": ("支付", "预付", "结算", "到账", "交付", "赔付", "折付"),
    "pending": ("尚未", "仍未", "未完成", "未结算", "未解决", "暂时", "等待"),
    "escape": ("脱离", "摆脱", "离开危险", "退出"),
    "fix": ("固定", "钉住", "钉进", "按住", "定住", "压进"),
    "handle": ("扣住", "拖", "拉住", "捡起", "递给", "固定", "握住"),
}
STATUS_SYNONYMS: dict[str, tuple[str, ...]] = {
    "received": ("取得", "获得", "拿到", "交到", "落到", "到账", "收进", "签下", "登记在", "入册", "结清", "付清", "全部结清"),
    "entitlement_confirmed": ("份额", "矿利", "登记", "确认", "记", "留档", "依据", "资格"),
    "pending": ("尚未", "仍未", "待", "未解决", "未核查", "具体兑现尚待", "以后", "后续"),
    "lost": ("失去", "落空", "无法兑现", "无法交付", "不能交付", "放弃", "不再交付", "没了"),
    "preserved": ("保住", "仍由", "继续由", "归", "持有", "保留", "不被并入", "没有被毁"),
    "destroyed": ("失守", "毁弃", "毁掉", "损毁", "坍塌", "牺牲区域"),
    "disputed": ("争议", "异议", "追索", "主张", "归属未解决", "要争"),
    "transitioned": ("正式进入", "突破", "晋升", "成为", "成炉已成", "第一次正式"),
    "not_transitioned": ("尚未完成", "未成炉", "不是成炉", "仍未进入", "不能写成"),
    "departed": ("随队出发", "上车", "驶去", "启程", "离开"),
}
TERM_LEXICON = tuple(sorted({
    "顾停舟", "本体", "分身", "校路官", "少东家", "阮青蜃", "乌合", "唐绾", "顾沉戈",
    "矿队首领", "旧关守将", "镇潮军府", "百炉会", "校路台", "沉灯商盟", "砺骨部",
    "原路线册", "路线册", "事实副本", "现场记录", "实测契", "侧路实测案", "矿路实测契",
    "行潮籍", "行潮身份", "预付款", "矿路实测预付款", "兼容潮髓", "尾款", "矿利", "个人矿利",
    "护粮结算", "战功", "战绩", "战功牌", "回潮楔", "古器", "矿权标记", "矿样", "深潮矿样",
    "新裂槽", "裂槽", "旧路线", "潮炉", "成炉", "照域", "镇海", "定住", "牵引",
    "撤离车", "粮道", "粮路", "粮队", "粮车", "货队", "三座新井", "新井", "水路", "迁徙水路", "居民", "矿工", "前哨",
    "旧关外层", "残墙", "退潮路线", "潮眼", "潮势", "逆潮", "潮压", "镇海潮兽", "十二日地潮",
    "低潮", "原册", "副本", "契约损失", "个人份额", "自主使用权", "独立合作", "主从关系",
    "公开战绩", "公开确认", "公开校准", "重新定价", "照域潮谱", "反潮记录", "小型潮舟", "母亲",
}, key=lambda value: (-len(value), value)))
STOP_ANCHORS = {"本章", "当前", "已经", "继续", "随后", "因此", "同时", "仍然", "正式", "第一次", "现实", "可以", "必须", "需要", "成为", "完成", "开始", "形成", "发生", "进入", "结果", "状态"}
MONEY_TERMS = ("钱", "潮铢", "预付款", "尾款", "矿利", "结算", "赔付", "报酬", "份额", "票据")
POWER_TARGETS = ("入潮", "成炉", "照域", "镇海")
POWER_RANK = {name: index for index, name in enumerate(POWER_TARGETS, 1)}
NAMED_ACTORS = ("顾停舟", "顾临川", "少东家", "校路官", "阮青蜃", "乌合", "唐绾", "顾沉戈", "矿队首领", "旧关守将")
PUBLIC_PROOF_TOPIC_TERMS = (
    "回潮楔", "古器", "潮炉", "潮压", "潮势", "逆潮", "战绩", "战功",
    "成炉", "照域", "镇海", "分身", "本体",
)
UNKNOWN_MARKERS = ("未知", "未解决", "仍未", "尚未", "不知道", "无法判断", "未核查")
REVELATION_MARKERS = ("真相是", "原来是", "确认是", "证实是", "原因是", "源自", "其实是", "揭开", "查明")
CONTACT_MARKERS = ("抓住", "扶住", "抱住", "压在", "贴近", "靠近", "包扎", "治疗", "触碰", "握住手", "按住伤口")
HUMAN_CUE_MARKERS = ("气味", "体温", "呼吸", "外貌", "姿态", "身体", "肩颈", "皮肤", "发丝", "靠近")
DESIRE_MARKERS = ("我想", "他想", "想要", "舍不得", "不愿", "喜欢", "漂亮", "属于自己", "自己定", "真正属于")
RELATION_MARKERS = ("关系", "旧友", "旧情", "欠情", "合作", "主从", "同行", "信任", "防备", "决裂")
REWARD_MARKERS = ("钱", "潮铢", "矿利", "份额", "行潮籍", "身份", "回潮楔", "潮髓", "战功", "票据")
REPRICE_MARKERS = ("目光变", "重新定价", "重新估价", "报价", "入册", "看法", "不再把", "追索失去")
SURPRISE_MARKERS = ("没想到", "谁也没想到", "竟然", "竟是", "原来", "多出来", "忽然发现", "反而")
PARTIAL_RESOURCE_MARKERS = ("首笔", "第一笔", "部分", "一部分", "一半", "先行", "暂付", "折付")
PRIOR_QUOTE_PATTERN = re.compile(
    r"(?:那句|刚才(?:说的)?|先前(?:说的)?|曾经(?:说过)?|说过的|原话|当时(?:说的)?)"
    r"[^“”‘’\n]{0,16}[“‘]([^”’]{2,48})[”’]"
)
MONEY_AMOUNT_PATTERN = re.compile(
    r"(?:\d+(?:\.\d+)?|[零一二三四五六七八九十百千万两]+)(?:枚|笔|份)?(?:潮铢|铜钱|银钱|金币|灵石|份额)"
)


def clean(text: str) -> str:
    return re.sub(r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$", "", text).strip()


def body(text: str) -> str:
    return clean(text).rsplit("# 正式正文", 1)[-1].strip()


def paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]


def normalized(text: str) -> str:
    return re.sub(r"[\s，。；：、！？“”‘’（）()《》\-—]", "", text)


def extract_h2_block(text: str, heading_prefix: str) -> str:
    headings = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    for index, match in enumerate(headings):
        if match.group(1).strip().startswith(heading_prefix):
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            return text[match.end():end].strip()
    return ""


def extract_h2_range(text: str, start_prefix: str, end_prefix: str) -> str:
    headings = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    start_match = next(
        (match for match in headings if match.group(1).strip().startswith(start_prefix)),
        None,
    )
    if start_match is None:
        return ""
    end_match = next(
        (
            match for match in headings
            if match.start() > start_match.start()
            and match.group(1).strip().startswith(end_prefix)
        ),
        None,
    )
    end = end_match.start() if end_match is not None else len(text)
    return text[start_match.end():end].strip()


def parse_mission_fields(authority_prompt: str) -> dict[str, str]:
    mission = extract_h2_block(authority_prompt, "FROZEN CHAPTER MISSION")
    if not mission:
        raise ValueError("missing FROZEN CHAPTER MISSION")
    labels = "|".join(re.escape(item) for item in MISSION_FIELDS)
    result: dict[str, str] = {}
    for match in re.finditer(rf"(?ms)^(?P<label>{labels})[：:]\s*(?P<body>.*?)(?=^(?:{labels})[：:]|^规划备注|\Z)", mission):
        result[match.group("label")] = match.group("body").strip()
    missing = [item for item in MISSION_FIELDS if not result.get(item)]
    if missing:
        raise ValueError("missing mission fields=" + ",".join(missing))
    return result


def parse_curator_sections(curator: str) -> dict[str, str]:
    result: dict[str, str] = {}
    audit = re.search(r"(?ms)^# Curator Audit\s*(.*?)(?=^#\s|\Z)", curator)
    if audit:
        result["Curator Audit"] = audit.group(1).strip()
    headings = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", curator))
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(curator)
        result[match.group(1).strip()] = curator[match.end():end].strip()
    return result


def split_clauses(text: str) -> list[str]:
    result = []
    for item in re.split(r"[；。]\s*", text):
        item = re.sub(r"^(?:并且|并|同时|随后|因此|但|而|且|又|仍然|则)", "", item.strip()).strip()
        if len(item) >= 4:
            result.append(item)
    return result


def split_field_clauses(field_name: str, text: str) -> list[str]:
    clauses: list[str] = []
    for clause in split_clauses(text):
        if field_name == "主角行动":
            pieces = [
                item.strip()
                for item in re.split(
                    r"，(?=(?:本体|分身|顾停舟|顾临川|主角|校路官|少东家|阮青蜃|乌合|唐绾|顾沉戈))",
                    clause,
                )
                if item.strip()
            ]
            clauses.extend(pieces or [clause])
        else:
            clauses.append(clause)
    return clauses


def detect_action_classes(text: str) -> list[str]:
    return [name for name, markers in ACTION_CLASSES.items() if any(marker in text for marker in markers)]


def known_terms(text: str, protagonist: str = "") -> list[str]:
    values = [term for term in TERM_LEXICON if term in text]
    if protagonist and protagonist in text and protagonist not in values:
        values.insert(0, protagonist)
    for quoted in re.findall(r"[“\"]([^”\"]{2,16})[”\"]", text):
        if quoted not in values and not any(mark in quoted for mark in ("什么", "怎么", "为什么")):
            values.append(quoted)
    for expression in re.findall(r"(?:下一次|本次|首次|第一次|一整段|两处|三座|十二日|四十丈|三十丈)[^，；。]{0,10}", text):
        if expression not in values:
            values.append(expression)
    return values[:14]


def expand_topic_terms(terms: Sequence[str]) -> list[str]:
    aliases = {
        "行潮身份": ("行潮身份", "行潮籍", "合法行潮身份", "独立身份"),
        "行潮籍": ("行潮籍", "行潮身份", "合法行潮身份", "独立身份"),
        "个人矿利": ("个人矿利", "矿利", "个人份额"),
        "矿利": ("矿利", "个人矿利", "个人份额"),
        "首批粮运": ("首批粮运", "第一批承运", "粮运短契", "第一批粮"),
        "第一批粮": ("第一批粮", "首批粮运", "第一批承运", "粮车", "粮队", "货队", "粮路", "粮道", "旧关"),
        "粮路": ("粮路", "粮道", "粮队", "粮车", "货队", "第一批粮", "旧关"),
        "粮道": ("粮道", "粮路", "粮队", "粮车", "货队", "第一批粮", "旧关"),
        "粮队": ("粮队", "粮车", "货队", "粮路", "粮道", "第一批粮", "旧关"),
    }
    result: list[str] = []
    for term in terms:
        for value in aliases.get(term, (term,)):
            if value not in result:
                result.append(value)
    return result


def ngram_set(text: str, size: int = 2) -> set[str]:
    value = normalized(text)
    return {value[index:index + size] for index in range(max(0, len(value) - size + 1))}


def clause_similarity(source: str, candidate: str, terms: Sequence[str], actions: Sequence[str]) -> float:
    source_norm, candidate_norm = normalized(source), normalized(candidate)
    if not source_norm or not candidate_norm:
        return 0.0
    sequence = difflib.SequenceMatcher(None, source_norm, candidate_norm, autojunk=False).ratio()
    source_bigrams, candidate_bigrams = ngram_set(source), ngram_set(candidate)
    overlap = len(source_bigrams & candidate_bigrams) / max(1, len(source_bigrams))
    term_score = sum(term in candidate for term in terms) / max(1, min(4, len(terms)))
    action_score = 0.0
    if actions:
        action_score = len(set(actions) & set(detect_action_classes(candidate))) / len(set(actions))
    return 0.28 * sequence + 0.32 * overlap + 0.25 * min(1.0, term_score) + 0.15 * action_score


def find_primary_evidence(source: str, primary_parts: Sequence[str], protagonist: str) -> tuple[list[int], list[str], float]:
    terms, actions = known_terms(source, protagonist), detect_action_classes(source)
    ranked = sorted(
        [
            (clause_similarity(source, paragraph, terms, actions), index, paragraph)
            for index, paragraph in enumerate(primary_parts, 1)
        ],
        reverse=True,
    )
    selected = [(score, index, paragraph) for score, index, paragraph in ranked[:3] if score >= 0.19]
    anchors: list[str] = []
    for _, _, paragraph in selected:
        matcher = difflib.SequenceMatcher(None, normalized(source), normalized(paragraph), autojunk=False)
        for block in sorted(matcher.get_matching_blocks(), key=lambda item: item.size, reverse=True):
            if block.size < 2:
                continue
            anchor = normalized(source)[block.a:block.a + block.size]
            if anchor in STOP_ANCHORS or any(anchor in old or old in anchor for old in anchors):
                continue
            anchors.append(anchor)
            if len(anchors) >= 6:
                break
    return [index for _, index, _ in selected], anchors, selected[0][0] if selected else 0.0


def _remote_human_protagonist(authority_prompt: str) -> str:
    human = extract_h2_range(authority_prompt, "HUMAN CORE", "CANON INDEX")
    match = re.search(r"HUMAN SEED[｜|]\s*([^／\n]+)", human)
    return match.group(1).strip() if match else "主角"


def _mission_protagonist(mission_fields: Mapping[str, str]) -> str:
    """Return an explicit current Mission actor without guessing from remote cards."""

    action = mission_fields.get("主角行动", "")
    for candidate in NAMED_ACTORS:
        if candidate and candidate in action:
            return candidate
    # Generic current books may use a name not yet present in the bounded lexicon.
    # Accept only a short clause-leading Chinese name immediately followed by an
    # action marker; role nouns and pronouns remain unsupported rather than guessed.
    match = re.match(
        r"^\s*([\u4e00-\u9fff]{2,4})(?=(?:把|将|用|让|拒绝|接受|抓住|稳住|保住|带|进入|穿过|确认|公开|取得|获得|拿|签|守|压|拖|问|查看|对照))",
        action,
    )
    if match and match.group(1) not in {"主角", "本体", "分身", "他", "我", "校路官", "少东家"}:
        return match.group(1)
    return ""


def _primary_protagonist(primary_body: str, remote_name: str) -> str:
    """Use Primary only when the Mission is generic and the name is explicit."""

    if remote_name and remote_name != "主角" and remote_name in primary_body:
        return remote_name
    counts: dict[str, int] = {}
    pattern = re.compile(
        r"([\u4e00-\u9fff]{2,4})(?=(?:把|将|用|让|拒绝|接受|抓住|稳住|保住|带|进入|穿过|确认|公开|取得|获得|拿|签|守|压|拖|问|看))"
    )
    excluded = {
        "校路官", "少东家", "矿队首领", "旧关守将", "镇潮军府", "百炉会",
        "居民", "矿工", "本体", "分身", "主角",
    }
    for paragraph in paragraphs(primary_body)[:12]:
        for match in pattern.finditer(paragraph):
            name = match.group(1)
            if name in excluded or name in TERM_LEXICON:
                continue
            counts[name] = counts.get(name, 0) + 1
    return max(counts, key=lambda name: (counts[name], -primary_body.find(name))) if counts else ""


def protagonist_from_sources(
    authority_prompt: str,
    mission_fields: Mapping[str, str],
    primary_body: str,
) -> str:
    """Current Mission actor > explicit current Primary fallback > remote Human seed."""

    mission_name = _mission_protagonist(mission_fields)
    if mission_name:
        return mission_name
    remote_name = _remote_human_protagonist(authority_prompt)
    primary_name = _primary_protagonist(primary_body, remote_name)
    return primary_name or remote_name or "主角"


def status_of(text: str) -> str:
    if re.search(r"尚未完成|未成炉|不是成炉|仍未进入", text): return "not_transitioned"
    if re.search(r"尚未|仍未|未解决|未核查|具体兑现尚待|还需要|待后续|以后再", text): return "pending"
    if re.search(r"无法兑现|尾款落空|失去|公开放弃|明确放弃|不再交付", text): return "lost"
    if re.search(r"正式进入|第一次正式|成炉已成|突破|晋升|成为", text): return "transitioned"
    if re.search(r"随队出发|已经出发|驶去|启程", text): return "departed"
    if re.search(r"公开确认.*份额|取得.*份额|矿利份额|现实依据|后续.*结算.*依据", text): return "entitlement_confirmed"
    if re.search(r"取得|获得|拿到|落到.*手|交到|登记在.*名下|签下|入册", text): return "received"
    if re.search(r"仍由|继续由|归.*所有|个人持有|保住|不被并入|没有被毁", text): return "preserved"
    if re.search(r"失守|毁弃|彻底毁|损毁|坍塌|牺牲区域", text): return "destroyed"
    if re.search(r"争议|异议|追索|归属.*未解决|继续主张", text): return "disputed"
    return "asserted"


def financial_status_of(text: str) -> str:
    """Classify only the local money/resource clause; unrelated power words do not leak in."""

    if re.search(r"无法兑现|尾款落空|明确放弃|公开放弃|不再交付|失去", text):
        return "lost"
    if re.search(r"尚未.*(?:到账|结算|支付|兑现)|仍未.*(?:到账|结算|支付|兑现)|具体兑现尚待|待.*结算|未结算", text):
        return "pending"
    if re.search(r"现实依据|结算依据|确认.*份额|取得.*份额|登记.*份额|矿利份额", text):
        return "entitlement_confirmed"
    if re.search(r"到账|终于落到.*手|交到.*手|当场付清|已经结清|取得.*(?:钱|潮铢|预付款|矿利)|获得.*(?:钱|潮铢|预付款|矿利)", text):
        return "received"
    return "asserted"


def is_unresolved_clause(text: str) -> bool:
    if re.search(r"未知|不知道|无法判断|未查明|真相未|来源未|原因(?:仍未|尚未|未知)|为何(?:仍未|尚未)", text):
        return True
    if re.search(r"(?:原因|来源|真相|是谁|谁做的|为何).*(?:仍未|尚未|未解决)", text):
        return True
    return False


def authorized_power_transition(mission_fields: Mapping[str, str]) -> str:
    combined = "\n".join(mission_fields.values())
    authorized = ""
    for target in POWER_TARGETS:
        if re.search(
            rf"(?:正式进入|第一次正式进入|突破(?:到|至)?|晋升(?:到|至)?|成为){target}|{target}已成",
            combined,
        ):
            authorized = target
    return authorized


def current_stable_power_tier(authority_prompt: str) -> tuple[str, str]:
    """Read only occurred Canon; Future Promises and Power Seed legends are excluded."""

    canon = extract_h2_range(authority_prompt, "CANON INDEX", "CANON TAIL")
    persistent = extract_h2_range(canon, "PERSISTENT CANON", "OPEN PROMISES") or canon
    patterns = {
        "镇海": (
            r"已(?:经)?(?:正式)?进入镇海",
            r"当前稳定(?:处于|为)镇海",
            r"镇海(?:境|层级)已成",
        ),
        "照域": (
            r"照域潮谱已被[^。；\n]{0,20}正式掌握",
            r"首次正式施展照域",
            r"已(?:经)?(?:正式)?进入照域",
            r"当前照域",
            r"照域已(?:经)?稳定",
        ),
        "成炉": (
            r"成炉潮息",
            r"潮炉(?:已经|已)?成形",
            r"潮炉已成",
            r"成炉已成",
            r"已(?:经)?(?:正式)?进入成炉",
        ),
        "入潮": (
            r"已(?:经)?(?:正式)?进入入潮",
            r"当前稳定(?:处于|为)入潮",
            r"入潮(?:境|层级)已成",
        ),
    }
    for target in reversed(POWER_TARGETS):
        for pattern in patterns[target]:
            match = re.search(pattern, persistent)
            if match:
                return target, match.group(0)
    return "", ""


def compile_source_conflicts(curator_sections: Mapping[str, str], mission_fields: Mapping[str, str]) -> tuple[list[str], list[str]]:
    conflicts, diagnostics = [], []
    audit = curator_sections.get("Curator Audit", "")
    for line in [item.strip("- ") for item in audit.splitlines() if item.strip().startswith("-")]:
        resolved = bool(re.search(
            r"本章按|本章保留|仅保留|不补|不得补|不应补|不据此补|不得推断|保持未知|不能把|以.*为准",
            line,
        ))
        explicit_no_conflict = bool(re.search(r"无明确权威冲突|无需要报告的冲突|无明确冲突", line))
        missing_repetition_context = bool(re.search(r"未提供最近.*(?:摘要|正文|片段).*重复", line))
        hard = bool(re.search(r"时间归属冲突|明确冲突|无法判断|无法确定|无法可靠判断", line))
        if explicit_no_conflict or missing_repetition_context:
            hard = False
        (conflicts if hard and not resolved else diagnostics).append(line)
    state, ending = mission_fields.get("状态变化", ""), mission_fields.get("结尾推动力", "")
    for term in MONEY_TERMS:
        state_statuses = {
            financial_status_of(clause) for clause in split_clauses(state) if term in clause
        }
        ending_statuses = {
            financial_status_of(clause) for clause in split_clauses(ending) if term in clause
        }
        if "pending" in state_statuses and "received" in ending_statuses:
            conflicts.append(
                "Mission terminal conflict: 状态变化仍标为 pending，但结尾推动力写成已到账："
                + term
            )
    return conflicts, diagnostics


def _field_prefix(field_name: str) -> str:
    return {
        "触发事件": "TRG", "主角行动": "ACT", "对手或世界反应": "REA",
        "直接结果": "RES", "状态变化": "STA", "结尾推动力": "END",
    }[field_name]


def _subject_for_clause(clause: str, protagonist: str, carry: str = "") -> str:
    candidates = (
        "本体", "分身", protagonist, "校路官", "少东家", "阮青蜃", "乌合", "唐绾", "顾沉戈",
        "矿队首领", "旧关守将", "镇潮军府", "百炉会", "校路台", "砺骨部", "居民", "矿工",
    )
    for candidate in candidates:
        if candidate and clause.startswith(candidate):
            return candidate
    if clause.startswith(("他", "其")):
        return protagonist
    return carry or protagonist


def _object_for_clause(clause: str, subject: str) -> str:
    terms = [term for term in known_terms(clause, subject) if term != subject]
    return terms[0] if terms else ""


def _clause_validator(source: str, protagonist: str, evidence_ids: Sequence[int], anchors: Sequence[str]) -> dict[str, Any]:
    return {
        "type": "mission_clause", "source": source, "terms": known_terms(source, protagonist),
        "actions": detect_action_classes(source), "anchors": list(anchors), "minimum_score": 0.23,
        "primary_evidence_paragraphs": list(evidence_ids),
    }


def _actor_action_object_validator(
    source: str,
    protagonist: str,
    subject: str,
    object_: str,
    evidence_ids: Sequence[int],
) -> dict[str, Any]:
    subject_terms = {
        protagonist: [protagonist, "他", "我"],
        "本体": ["本体", protagonist, "他", "我"],
        "分身": ["分身", "它"],
    }.get(subject, [subject])
    object_terms = {
        "回潮楔": ["回潮楔", "楔子", "古器", "楔尾", "楔体", "楔尖"],
        "古器": ["古器", "回潮楔", "楔子", "楔尾", "楔体", "楔尖"],
        "原路线册": ["原路线册", "路线册", "原册"],
        "事实副本": ["事实副本", "副本", "校路纸"],
    }.get(object_, [object_])
    return {
        "type": "actor_action_object",
        "source": source,
        "subject_terms": subject_terms,
        "object_terms": object_terms,
        "actions": detect_action_classes(source),
        "primary_evidence_paragraphs": list(evidence_ids),
    }


def find_actor_action_object_evidence(
    primary_parts: Sequence[str],
    validator: Mapping[str, Any],
) -> list[int]:
    actions = set(validator.get("actions", []))
    result: list[int] = []
    for index, paragraph in enumerate(primary_parts, 1):
        if not any(term in paragraph for term in validator.get("subject_terms", [])):
            continue
        if not any(term in paragraph for term in validator.get("object_terms", [])):
            continue
        if actions and not actions.intersection(detect_action_classes(paragraph)):
            continue
        result.append(index)
    return result


def compile_reader_release(authority_prompt: str, primary_parts: Sequence[str], protagonist: str, start_index: int) -> list[AtomicObligation]:
    block = extract_h2_block(authority_prompt, "READER RELEASE")
    if not block or "没有排程" in block or "没有单独排程" in block:
        return []
    result = []
    for offset, bullet in enumerate(re.findall(r"(?m)^-\s+(.+)$", block), 1):
        evidence_ids, anchors, _ = find_primary_evidence(bullet, primary_parts, protagonist)
        result.append(AtomicObligation(
            id=f"RR-{start_index + offset:03d}", kind=ObligationKind.READER_RELEASE,
            mode=ObligationMode.MUST_HOLD, severity=GateSeverity.HARD,
            source_field="READER RELEASE", source_text=bullet,
            boundary="Reader Release is a timing obligation: the reader must learn the approved fact once; atmosphere or terminology alone is insufficient, but no extra encyclopedia is required.",
            validator={"type": "reader_release", "source": bullet, "terms": known_terms(bullet, protagonist), "actions": [], "anchors": anchors, "minimum_score": 0.19},
            primary_evidence_paragraphs=tuple(evidence_ids),
        ))
    return result


def compile_specialized_obligations(
    chapter: int,
    protagonist: str,
    mission_fields: Mapping[str, str],
    curator_sections: Mapping[str, str],
    authority_prompt: str,
    primary_parts: Sequence[str],
    start_index: int,
) -> list[AtomicObligation]:
    obligations: list[AtomicObligation] = []
    combined = "\n".join(f"{field}：{value}" for field, value in mission_fields.items())
    counter = start_index

    def add(
        kind: ObligationKind, mode: ObligationMode, source_field: str, source_text: str,
        *, subject: str = "", action: str = "", object_: str = "", status: str = "",
        qualifiers: Sequence[str] = (), boundary: str, validator: Mapping[str, Any],
        evidence_ids: Sequence[int] = (), severity: GateSeverity = GateSeverity.HARD,
        protected_category: str = "",
    ) -> None:
        nonlocal counter
        counter += 1
        obligations.append(AtomicObligation(
            id=f"A-{counter:03d}", kind=kind, mode=mode, severity=severity,
            source_field=source_field, source_text=source_text, subject=subject, action=action,
            object=object_, status=status, qualifiers=tuple(qualifiers), boundary=boundary,
            validator=dict(validator), primary_evidence_paragraphs=tuple(evidence_ids),
            protected_category=protected_category,
        ))

    # Whole-draft no-invention boundary. A line presented as something that was
    # said earlier must already exist in Frozen Authority outside the current
    # Primary Draft. This catches Authority defects already present in Primary,
    # not only text newly introduced by Delta.
    authority_before_primary = authority_prompt.split("## PRIMARY DRAFT", 1)[0]
    authorized_prior_quotes = [
        normalized(quote)
        for quote in re.findall(r"[“‘]([^”’]{2,48})[”’]", authority_before_primary)
        if normalized(quote)
    ]
    add(
        ObligationKind.SOURCE_CONFLICT,
        ObligationMode.MUST_NOT_HOLD,
        "Frozen Authority",
        "Do not invent prior dialogue/history backreferences.",
        subject=protagonist,
        action="no_invented_prior_quote",
        object_="previous dialogue",
        status="not_invented",
        boundary="A line framed as previously spoken must already exist in Frozen Authority; current dialogue is unaffected.",
        validator={"type": "prior_quote", "authorized_quotes": authorized_prior_quotes},
    )

    # Stable tier versus battle-pressure boundary.
    for field_name, text in mission_fields.items():
        for target in POWER_TARGETS:
            if target not in text:
                continue
            if re.search(rf"(?:正式进入|第一次正式进入|突破(?:到|至)?|晋升(?:到|至)?|成为){target}|{target}已成", text):
                evidence_ids, _, _ = find_primary_evidence(text, primary_parts, protagonist)
                add(
                    ObligationKind.POWER_POSITION, ObligationMode.TERMINAL, field_name, text,
                    subject=protagonist, action="stable_transition", object_=target, status="transitioned",
                    boundary=f"Only an explicit stable transition authorizes {target}; battle pressure or performance at that scale is not enough.",
                    validator={"type": "power_transition", "target": target, "subject": protagonist},
                    evidence_ids=evidence_ids,
                )
            if re.search(rf"尚未(?:完成)?{target}|未{target}|不是{target}", text):
                add(
                    ObligationKind.POWER_BOUNDARY, ObligationMode.MUST_NOT_HOLD, field_name, text,
                    subject=protagonist, action="not_yet", object_=target, status="not_transitioned",
                    boundary=f"Pressure/growth may occur, but the draft cannot promote it into stable {target}.",
                    validator={"type": "forbid_power_transition", "target": target, "subject": protagonist},
                )

    current_tier, current_tier_evidence = current_stable_power_tier(authority_prompt)
    authorized_tier = authorized_power_transition(mission_fields)
    ceiling_rank = max(
        POWER_RANK.get(current_tier, 0),
        POWER_RANK.get(authorized_tier, 0),
    )
    for target in POWER_TARGETS:
        if POWER_RANK[target] <= ceiling_rank:
            continue
        if any(
            item.validator.get("type") == "forbid_power_transition"
            and item.validator.get("target") == target
            for item in obligations
        ):
            continue
        add(
            ObligationKind.POWER_BOUNDARY,
            ObligationMode.MUST_NOT_HOLD,
            "CANON INDEX / current stable power",
            current_tier_evidence
            or (
                f"Mission only authorizes stable transition through {authorized_tier}"
                if authorized_tier
                else "No stable power transition is authorized in the current Mission"
            ),
            subject=protagonist,
            action="forbid_unapproved_higher_tier",
            object_=target,
            status="not_authorized",
            boundary="Current stable Canon plus an explicit Mission transition defines the maximum authorized tier. If current tier is absent, the gate does not guess it; it simply forbids any new explicit transition not approved by Mission. Future promises, battle scale, public proof and Power Seed legend text do not raise this ceiling.",
            validator={
                "type": "forbid_power_transition",
                "target": target,
                "subject": protagonist,
                "current_tier": current_tier,
                "authorized_tier": authorized_tier,
            },
        )
    if ("镇海战局" in combined or "镇海正面" in combined or "镇海冲击" in combined) and not re.search(r"正式进入镇海|突破(?:到|至)?镇海|成为镇海", combined):
        add(
            ObligationKind.POWER_BOUNDARY, ObligationMode.MUST_NOT_HOLD, "Mission composite", combined,
            subject=protagonist, action="battle_scale_not_stable_tier", object_="镇海", status="battle_position_only",
            boundary="镇海战局/冲击/承压 is a battle category, not permission to write a stable 镇海 breakthrough.",
            validator={"type": "forbid_power_transition", "target": "镇海", "subject": protagonist},
        )
    if "分身" in combined and re.search(r"不能.*完整|不能无条件|只携带|尚不能.*传给分身|不携带完整", combined):
        evidence_ids, _, _ = find_primary_evidence(combined, primary_parts, protagonist)
        ability_terms = [term for term in ("牵引", "定住", "压住", "推出冲击") if term in combined]
        add(
            ObligationKind.POWER_BOUNDARY, ObligationMode.MUST_HOLD, "Mission composite", combined,
            subject="分身", action="limited_carry", object_="完整力量", status="limited",
            boundary="Require the current limitation without generalizing it into a stronger universal power law.",
            validator={
                "type": "clone_boundary",
                "subject_terms": ["分身", "它"],
                "limit_terms": ["只能", "不能", "承不住", "不携带", "无法", "只带", "只携"],
                "full_terms": ["完整", "潮炉", "成炉", "照域", "力量"],
                "ability_terms": ability_terms,
            },
            evidence_ids=evidence_ids,
        )

    # Ownership: original/copy, possession/title/dispute are separate states.
    ownership_specs: list[tuple[str, str]] = []
    if ("原路线册" in combined or "原册" in combined) and re.search(
        r"原路线册.*(?:仍归|继续由|保留|持有)|原册.*(?:仍归|继续由|保留|持有)|"
        r"(?:保留|持有|拿着|留着).*原(?:路线)?册|原(?:路线)?册.*(?:还是|仍是).*你的",
        combined,
    ):
        ownership_specs.append(("原路线册", protagonist))
    if "回潮楔" in combined and re.search(r"回潮楔.*(?:由.*带走|仍由.*持有|个人持有|归.*所有|保住)", combined):
        ownership_specs.append(("回潮楔", protagonist))
    for object_, owner in ownership_specs:
        evidence_ids, _, _ = find_primary_evidence(object_, primary_parts, protagonist)
        add(
            ObligationKind.OWNERSHIP, ObligationMode.TERMINAL, "Mission composite", combined,
            subject=owner, action="possess", object_=object_, status="preserved",
            boundary="Physical possession, registered ownership, and uncontested legal title are distinct. Require only the explicitly authorized state.",
            validator={
                "type": "ownership",
                "object_terms": [object_, object_.replace("原路线", "路线")] + (["楔子", "古器"] if object_ == "回潮楔" else ["原册"]),
                "owner_terms": [owner, "他", "自己", "个人"],
                "possession_terms": ["持有", "保留", "带走", "收好", "在手", "手里", "掌心", "收回袖中", "收进袖中", "归", "仍由", "留在", "不卖", "不交", "塞回"],
                "forbidden_transfer_terms": ["送入", "送到", "送回", "传入", "交给", "交出", "收走", "拿走", "带走", "带着"],
                "forbidden_destination_terms": ["校路台", "校路官", "沉灯商盟"] if object_ == "原路线册" else [],
            },
            evidence_ids=evidence_ids,
        )
    if "事实副本" in combined and re.search(r"事实副本.*(?:送入|送到|传入|带回)", combined):
        add(
            ObligationKind.OWNERSHIP, ObligationMode.MUST_HOLD, "Mission composite", combined,
            subject="校路官", action="transfer_copy", object_="事实副本", status="transferred",
            boundary="Original and copy are separate objects. Sending the fact copy must not imply transferring the original route book.",
            validator={"type": "transfer", "object_terms": ["事实副本", "副本"], "destination_terms": ["校路台", "校路官", "沉灯商盟"], "transfer_terms": ["送入", "送到", "传入", "带回", "卷好", "防潮筒"]},
        )
    if "回潮楔" in combined and re.search(r"归属争议|继续主张回潮楔|归属.*未解决|提出归属异议", combined):
        add(
            ObligationKind.OWNERSHIP, ObligationMode.MUST_HOLD, "Mission composite", combined,
            subject="矿队/阮青蜃", action="dispute", object_="回潮楔", status="disputed",
            boundary="The protagonist may possess the object while title remains disputed. Do not collapse possession into uncontested ownership.",
            validator={"type": "dispute", "object_terms": ["回潮楔", "楔子", "古器"], "dispute_terms": ["争", "争议", "异议", "追索", "主张", "要重算"]},
        )

    # Money/resources: received, entitlement, pending and lost are different.
    for term in ("预付款", "尾款", "个人矿利", "矿利", "护粮结算"):
        relevant_clauses = [
            (field, clause)
            for field, text in mission_fields.items()
            for clause in split_clauses(text)
            if term in clause
        ]
        if not relevant_clauses:
            continue
        statuses = [(field, clause, financial_status_of(clause)) for field, clause in relevant_clauses]
        terminal_statuses = {status for _, _, status in statuses if status != "asserted"}
        if not terminal_statuses:
            continue
        if len(terminal_statuses) > 1:
            # The source conflict gate handles pending->received across State/Ending.
            # Other mixed statuses are too ambiguous for a deterministic fast path.
            continue
        status = next(iter(terminal_statuses))
        source_text = "\n".join(f"{field}：{clause}" for field, clause, clause_status in statuses if clause_status == status)
        authorized_amounts: list[str] = []
        for sentence in re.split(r"[。；\n]", authority_prompt):
            if term not in sentence:
                continue
            for amount in MONEY_AMOUNT_PATTERN.findall(sentence):
                if amount not in authorized_amounts:
                    authorized_amounts.append(amount)
        partial_authorized = any(marker in source_text for marker in PARTIAL_RESOURCE_MARKERS)
        evidence_ids, _, _ = find_primary_evidence(source_text, primary_parts, protagonist)
        add(
            ObligationKind.MONEY,
            ObligationMode.TERMINAL if status in {"received", "lost", "preserved", "departed"} else ObligationMode.MUST_HOLD,
            "Mission composite", source_text, subject=protagonist, action=status, object_=term, status=status,
            boundary="Received cash/resource, confirmed entitlement, settlement basis, pending payment and forfeiture are distinct. Never invent an amount or payment mechanism.",
            validator={
                "type": "status",
                "object_terms": [term],
                "status": status,
                "status_terms": list(STATUS_SYNONYMS.get(status, ())),
                "partial_authorized": partial_authorized,
                "authorized_amounts": authorized_amounts,
            },
            evidence_ids=evidence_ids,
        )

    # Deadlines do not imply completion; the lexical word “提前” is not a deadline.
    deadline_pattern = re.compile(
        r"(?:下一次|下一轮|十二日)?(?:低潮|地潮)(?:到来|过去|结束)?(?:之)?前|"
        r"在[^，；。]{0,16}(?:低潮|地潮)[^，；。]{0,8}前"
    )
    for field_name, text in mission_fields.items():
        for clause in split_clauses(text):
            match = deadline_pattern.search(clause)
            if not match:
                continue
            expression = match.group(0)
            add(
                ObligationKind.TIME_WINDOW, ObligationMode.MUST_HOLD, field_name, clause,
                object_=expression, status="deadline",
                boundary="A deadline constrains a later action; it does not mean the action is already completed in this chapter.",
                validator={
                    "type": "deadline",
                    "terms": [term for term in ("下一次", "下一轮", "十二日", "低潮", "地潮", "前") if term in expression],
                    "future_only": field_name == "结尾推动力",
                    "topic_terms": [term for term in known_terms(clause, protagonist) if term != protagonist][:4],
                },
            )
    ending = mission_fields.get("结尾推动力", "")
    if re.search(r"随队出发|已经出发|驶去|启程", ending):
        evidence_ids, _, _ = find_primary_evidence(ending, primary_parts, protagonist)
        add(
            ObligationKind.ENDING, ObligationMode.TERMINAL, "结尾推动力", ending,
            subject=protagonist, action="depart", object_="队伍/目的地", status="departed",
            boundary="Vehicles waiting or a plan to depart is not enough; actual departure must occur.",
            validator={
                "type": "departure",
                "protagonist": protagonist,
                "subject_terms": [protagonist, "他", "我"],
                "terms": ["随队出发", "上车", "踩上车辕", "坐进", "驶去", "启程", "离开"],
                "context_terms": expand_topic_terms([
                    term for term in known_terms(ending, protagonist)
                    if term != protagonist and not re.match(r"(?:下一次|本次|首次|第一次|十二日)", term)
                ]),
            },
            evidence_ids=evidence_ids,
        )

    # Explicit one-cycle artifact use and terminal cooldown.
    if re.search(r"只完成一次|完成一次完整|一次真实", combined) and "回潮楔" in combined:
        explicit_sequence = all(term in combined for term in ("锁", "改向", "释放"))
        required_steps = ["锁", "改向", "释放"] if explicit_sequence else ["释放"]
        add(
            ObligationKind.ACTOR_ACTION_OBJECT, ObligationMode.MUST_HOLD, "Mission composite", combined,
            subject=protagonist, action="single_artifact_cycle", object_="回潮楔", status="exactly_one_cycle",
            qualifiers=tuple(required_steps + ["一次"]),
            boundary="The explicit count belongs only to this approved use cycle; it is not a universal per-chapter count rule.",
            validator={
                "type": "single_cycle",
                "object_terms": ["回潮楔", "楔子"],
                "step_terms": required_steps,
                "repeat_forbidden": ["第二次", "再压一次", "连续硬压", "又压一次"],
            },
        )
    if "残压" in combined and (
        "散尽残压" in combined
        or "残压已经散尽" in combined
        or "残压彻底散尽" in combined
        or "不能连续" in combined
        or "再次使用前" in combined
    ):
        state_text = mission_fields.get("状态变化", "")
        terminal = bool(
            re.search(
                r"(?:章末|本章结束(?:前|时)?|结束时|最终)[^。；]{0,12}残压(?:已经|彻底)?散尽|"
                r"残压(?:已经|彻底)散尽",
                state_text,
            )
        )
        add(
            ObligationKind.POWER_BOUNDARY, ObligationMode.TERMINAL if terminal else ObligationMode.MUST_HOLD,
            "状态变化", state_text or combined, subject="回潮楔",
            action="dissipate_before_reuse", object_="残压", status="dissipated" if terminal else "cooldown_required",
            boundary="‘再次使用前必须散尽’是 cooldown，不等于章末已经散尽；只有明确章末终态才要求 residual pressure 已归零。",
            validator={
                "type": "residual_pressure",
                "terminal": terminal,
                "object_terms": ["回潮楔", "楔子", "残压"],
                "cooldown_terms": ["散", "散尽", "不能再压", "不能连续", "暂时不能", "散尽之前", "没散完"],
            },
        )

    # Public Proof: visible performance + qualified ruler + behavior change; no tier upgrade.
    public_source = "\n".join(text for text in mission_fields.values() if re.search(r"公开校准|懂行者|重新定价|公开战绩|力量尺|公开确认", text))
    if public_source:
        evidence_ids, _, _ = find_primary_evidence(public_source, primary_parts, protagonist)
        public_topics = [term for term in PUBLIC_PROOF_TOPIC_TERMS if term in public_source]
        if not public_topics:
            public_topics = [
                term for term in known_terms(public_source, protagonist)
                if term not in NAMED_ACTORS
                and term not in MONEY_TERMS
                and term not in {
                    protagonist, "主从关系", "独立合作",
                    "公开战绩", "公开确认", "公开校准", "重新定价",
                }
            ][:6]
        add(
            ObligationKind.PUBLIC_PROOF, ObligationMode.MUST_HOLD, "Mission composite", public_source,
            subject=protagonist, action="public_proof", object_="力量/器物/战绩", status="publicly_calibrated",
            boundary="Require performance, qualified ruler and behavioral consequence. Public Proof never authorizes an unapproved stable tier.",
            validator={
                "type": "public_proof",
                "subject_terms": [protagonist, "他", "我", "你"],
                "topic_terms": public_topics,
                "performance_terms": [
                    "稳住", "改向", "锁住", "锁在", "拧进", "拧到",
                    "改到", "引到", "送回", "压回", "护住", "战绩", "入册",
                ],
                "ruler_terms": ["成炉者", "照域者", "镇海", "懂行", "白须老人", "验器人", "军府", "守将", "铜尺"],
                "repricing_terms": ["报价", "价钱", "目光", "入册", "重新", "不再把", "公开", "追索", "买断"],
            },
            evidence_ids=evidence_ids,
        )

    relationship_source = "\n".join(text for text in (mission_fields.get("直接结果", ""), mission_fields.get("状态变化", "")) if re.search(r"主从关系|合作关系|相互欠情|公开决裂|关系.*转|转为.*同行|有价合作", text))
    if relationship_source:
        evidence_ids, _, _ = find_primary_evidence(relationship_source, primary_parts, protagonist)
        counterpart_terms = [
            actor for actor in NAMED_ACTORS
            if actor != protagonist and actor in relationship_source
        ]
        transition_terms = [
            term for term in ("不再", "转为", "主从", "同行", "合作", "欠情", "决裂", "各走自己的")
            if term in relationship_source
        ]
        add(
            ObligationKind.RELATIONSHIP_STATE, ObligationMode.TERMINAL, "状态变化", relationship_source,
            subject=protagonist, action="relationship_transition", object_="current named counterpart", status="changed",
            boundary="Only the explicit relationship state is required; do not infer romance, loyalty, forgiveness or a stronger bond.",
            validator={
                "type": "relationship",
                "subject_terms": [protagonist, "他", "我", "你"],
                "counterpart_terms": counterpart_terms,
                "terms": ["合作", "主从", "欠情", "决裂", "同行", "信任", "关系", "不再替", "一起走", "各走自己的"],
                "transition_terms": transition_terms,
            },
            evidence_ids=evidence_ids,
            severity=GateSeverity.CONDITIONAL,
        )

    # Unknown is a no-invention boundary, not a mention quota.
    unresolved_sources: list[tuple[str, str]] = []
    for field_name in ("状态变化", "结尾推动力"):
        for clause in split_clauses(mission_fields.get(field_name, "")):
            if is_unresolved_clause(clause):
                unresolved_sources.append((field_name, clause))
    for line in [item.strip("- ") for item in curator_sections.get("Relevant Open Promises", "").splitlines() if item.strip().startswith("-")]:
        if is_unresolved_clause(line) or re.search(r"原因|来源|真相|为何", line):
            unresolved_sources.append(("Relevant Open Promises", line))
    seen_unknown: set[str] = set()
    for field_name, source_text in unresolved_sources:
        topic_terms = [term for term in known_terms(source_text, protagonist) if term not in {protagonist, "状态"}][:4]
        key = "|".join(topic_terms) or source_text[:30]
        if key in seen_unknown:
            continue
        seen_unknown.add(key)
        add(
            ObligationKind.UNRESOLVED_FACT, ObligationMode.MUST_REMAIN_UNKNOWN, field_name, source_text,
            object_=key, status="unknown",
            boundary="Unknown is a no-invention boundary, not a requirement to repeat 'unknown' in prose.",
            validator={"type": "unresolved", "topic_terms": topic_terms, "revelation_terms": list(REVELATION_MARKERS)},
        )

    # Human cue only when the Frozen Human text names the same current person and
    # Primary already has direct contact / near treatment with that person.
    human_core = extract_h2_range(authority_prompt, "HUMAN CORE", "CANON INDEX")
    relationship_context = curator_sections.get("Relevant Characters and Relationships", "")
    current_people = []
    for match in re.finditer(r"(?m)^-\s*([^：:\n]{1,12})[：:]", relationship_context):
        name = match.group(1).strip()
        if name and name != protagonist and name not in current_people:
            current_people.append(name)
    cue_people: list[str] = []
    cue_terms: list[str] = []
    for sentence in re.split(r"[。\n]", human_core):
        named = [name for name in current_people if name in sentence]
        markers = [marker for marker in HUMAN_CUE_MARKERS if marker in sentence]
        if named and markers:
            for name in named:
                if name not in cue_people:
                    cue_people.append(name)
            for marker in markers:
                if marker not in cue_terms:
                    cue_terms.append(marker)
    contact_ids = [
        index for index, paragraph in enumerate(primary_parts, 1)
        if any(person in paragraph for person in cue_people)
        and any(marker in paragraph for marker in CONTACT_MARKERS)
    ]
    if cue_people and cue_terms and contact_ids:
        add(
            ObligationKind.HUMAN_CUE, ObligationMode.CONDITIONAL, "HUMAN CORE + Primary contact", human_core,
            subject=protagonist, action="notice_specific_cue", object_="specific current person", status="triggered",
            boundary="Trigger requires a Human-Core-specific cue plus direct body contact or near treatment. Co-presence, battle beside each other, moving a third person, or passing an object does not count.",
            validator={
                "type": "human_cue",
                "person_terms": cue_people,
                "contact_paragraphs": contact_ids,
                "cue_terms": cue_terms,
                "contact_terms": list(CONTACT_MARKERS),
            },
            evidence_ids=contact_ids,
            severity=GateSeverity.HARD,
        )

    # Commercial value: one category-level obligation, not one frozen obligation per
    # sentence. A Delta may rewrite/delete individual carriers if the authorized value
    # remains visible somewhere in the final chapter.
    curated_support = "\n".join(
        curator_sections.get(name, "")
        for name in (
            "Relevant Book Contract",
            "Relevant Characters and Relationships",
            "Payoff and Promise Window",
        )
    )
    categories = (
        ("desire", DESIRE_MARKERS),
        ("reward", REWARD_MARKERS),
        ("relationship", RELATION_MARKERS),
        ("social_repricing", REPRICE_MARKERS),
        ("surprise", SURPRISE_MARKERS),
    )
    for category, markers in categories:
        if not any(marker in curated_support or marker in combined for marker in markers):
            continue
        ids = [
            index
            for index, paragraph in enumerate(primary_parts, 1)
            if any(marker in paragraph for marker in markers)
        ][:6]
        if not ids:
            continue
        source_text = "\n\n".join(primary_parts[index - 1] for index in ids)
        key_terms = [
            term for term in known_terms(source_text + "\n" + curated_support, protagonist)
            if term != protagonist
        ][:8]
        add(
            ObligationKind.COMMERCIAL_VALUE,
            ObligationMode.PRESERVE_IF_PRESENT,
            "Primary + approved Curator support",
            source_text,
            subject=protagonist,
            action="preserve_value",
            object_=category,
            status="present_in_primary",
            boundary="Commercial value is category-level, not sentence-level and not a per-chapter quota. Individual carrier paragraphs may change if the authorized desire, relationship, reward or repricing remains visible.",
            validator={
                "type": "commercial_preserve",
                "category": category,
                "markers": list(markers),
                "source_paragraphs": ids,
                "key_terms": key_terms,
                "source_text": source_text,
            },
            evidence_ids=ids,
            protected_category=category,
        )
    return obligations


def compile_obligations(*, chapter: int, authority_prompt: str, curator_response: str, primary_body: str) -> ObligationPack:
    mission_fields = parse_mission_fields(authority_prompt)
    curator_sections = parse_curator_sections(curator_response)
    protagonist = protagonist_from_sources(authority_prompt, mission_fields, primary_body)
    primary_parts = paragraphs(primary_body)
    conflicts, diagnostics = compile_source_conflicts(curator_sections, mission_fields)
    obligations: list[AtomicObligation] = []
    unsupported: list[str] = []
    for field_name in MISSION_FIELDS:
        carry_subject = protagonist
        for clause_index, clause in enumerate(split_field_clauses(field_name, mission_fields[field_name]), 1):
            subject = _subject_for_clause(clause, protagonist, carry_subject)
            carry_subject = subject
            object_ = _object_for_clause(clause, subject)
            evidence_ids, anchors, best_score = find_primary_evidence(clause, primary_parts, protagonist)
            actions, terms = detect_action_classes(clause), known_terms(clause, protagonist)
            supported = (
                bool(evidence_ids and best_score >= 0.19)
                or bool(actions and (terms or anchors))
                or any(marker in clause for marker in UNKNOWN_MARKERS)
            )
            if not supported:
                unsupported.append(f"{field_name}[{clause_index}] {clause}")
            kind = {"直接结果": ObligationKind.DIRECT_RESULT, "状态变化": ObligationKind.TERMINAL_STATE, "结尾推动力": ObligationKind.ENDING}.get(field_name, ObligationKind.ACTOR_ACTION_OBJECT if field_name == "主角行动" else ObligationKind.MISSION_CLAUSE)
            validator = _clause_validator(clause, protagonist, evidence_ids, anchors)
            mode = ObligationMode.TERMINAL if field_name in {"直接结果", "状态变化", "结尾推动力"} else ObligationMode.MUST_HOLD
            if is_unresolved_clause(clause):
                mode = ObligationMode.MUST_REMAIN_UNKNOWN
                validator = {
                    "type": "unresolved",
                    "topic_terms": [term for term in known_terms(clause, protagonist) if term != protagonist][:4],
                    "revelation_terms": list(REVELATION_MARKERS),
                }
            elif re.search(r"尚未|仍未|未完成|未结算|待后续|等待", clause):
                mode = ObligationMode.MUST_HOLD
                validator = {
                    "type": "pending_boundary",
                    "topic_terms": expand_topic_terms(
                        [term for term in known_terms(clause, protagonist) if term != protagonist][:4]
                    ),
                    "completion_terms": ["已经完成", "已经送到", "已经结算", "已经到账", "全部完成", "正式完成", "交付完毕", "已经取得", "正式取得", "已经落籍", "正式落籍", "已经入册", "正式入册", "已经登记", "身份当场完成"],
                    "pending_terms": ["尚未", "仍未", "没到", "未完成", "未结算", "待", "别当契完了"],
                }
            if field_name == "主角行动" and subject and object_ and actions and subject != protagonist:
                validator = _actor_action_object_validator(
                    clause, protagonist, subject, object_, evidence_ids
                )
                evidence_ids = find_actor_action_object_evidence(primary_parts, validator)
                validator["primary_evidence_paragraphs"] = list(evidence_ids)
            obligations.append(AtomicObligation(
                id=f"{_field_prefix(field_name)}-{clause_index:02d}", kind=kind,
                mode=mode,
                severity=GateSeverity.HARD, source_field=field_name, source_text=clause,
                subject=subject, action="|".join(actions), object=object_, status=status_of(clause),
                boundary="Clause semantics are mandatory, but exact wording and unapproved implementation detail are not. Untouched Primary evidence is preserved without re-interpretation.",
                validator=validator,
                primary_evidence_paragraphs=tuple(evidence_ids),
            ))
    obligations.extend(compile_reader_release(authority_prompt, primary_parts, protagonist, len(obligations)))
    obligations.extend(compile_specialized_obligations(chapter, protagonist, mission_fields, curator_sections, authority_prompt, primary_parts, len(obligations)))
    for index, conflict in enumerate(conflicts, 1):
        obligations.append(AtomicObligation(
            id=f"CONFLICT-{index:02d}", kind=ObligationKind.SOURCE_CONFLICT,
            mode=ObligationMode.DIAGNOSTIC_FALLBACK, severity=GateSeverity.HARD,
            source_field="Authority conflict", source_text=conflict,
            boundary="The gate must not silently pick a winner between incompatible terminal authorities.",
            validator={"type": "source_conflict"},
        ))
    return ObligationPack(
        chapter=chapter, protagonist=protagonist, mission_fields=mission_fields,
        obligations=obligations, source_conflicts=conflicts, unsupported_clauses=unsupported,
        diagnostics=diagnostics, primary_paragraph_count=len(primary_parts),
    )


def touched_source_paragraphs(operations: Sequence[Mapping[str, Any]]) -> set[int]:
    result: set[int] = set()
    for operation in operations:
        if str(operation.get("kind", "")) not in {"REPLACE", "DELETE"}:
            continue
        start = int(operation.get("start", 0))
        end = int(operation.get("end", start))
        result.update(range(start, end + 1))
    return result


def infer_diff_operations(primary_body: str, final_body: str) -> list[dict[str, Any]]:
    """Project a full-text revision back to conservative Primary paragraph ranges."""

    primary_parts = paragraphs(primary_body)
    final_parts = paragraphs(final_body)
    matcher = difflib.SequenceMatcher(None, primary_parts, final_parts, autojunk=False)
    operations: list[dict[str, Any]] = []
    for tag, first_start, first_end, second_start, second_end in matcher.get_opcodes():
        if tag == "equal":
            continue
        if tag == "insert":
            target = min(len(primary_parts), first_start + 1)
            operations.append({"kind": "INSERT_BEFORE", "start": target, "end": target})
            continue
        operations.append({
            "kind": "DELETE" if tag == "delete" else "REPLACE",
            "start": first_start + 1,
            "end": max(first_start + 1, first_end),
        })
    return operations


def _any_paragraph_with_groups(parts: Sequence[str], groups: Sequence[Sequence[str]]) -> tuple[bool, str]:
    for paragraph in parts:
        if all(any(term and term in paragraph for term in group) for group in groups):
            return True, paragraph
    return False, ""


def _any_local_window_with_groups(
    parts: Sequence[str],
    groups: Sequence[Sequence[str]],
    *,
    window_size: int = 2,
) -> tuple[bool, str]:
    for start in range(len(parts)):
        window = "\n\n".join(parts[start:start + window_size])
        if all(any(term and term in window for term in group) for group in groups):
            return True, window
    return False, ""


NEGATED_ACTION_PREFIX = re.compile(
    r"(?:没有|还没有|尚未|仍未|并未|未曾|未能|不曾|并没有|没有把|未把|没有将|未将|"
    r"不能|无法|不可|不得|别|不许|准备|正要|打算|等着)[^，。；！？\n]{0,10}$"
)


def contains_unnegated_term(text: str, terms: Sequence[str]) -> bool:
    """True only when a lexical action denotes occurrence, not negation or preparation."""

    for term in terms:
        if not term:
            continue
        for match in re.finditer(re.escape(term), text):
            prefix = text[max(0, match.start() - 18):match.start()]
            if NEGATED_ACTION_PREFIX.search(prefix):
                continue
            return True
    return False


def _local_windows(parts: Sequence[str], window_size: int = 2) -> list[str]:
    return [
        "\n\n".join(parts[start:start + window_size])
        for start in range(len(parts))
    ]


def _check_obligation(
    obligation: AtomicObligation,
    final_body: str,
    final_parts: Sequence[str],
    touched: set[int],
) -> ObligationCheck:
    rule = obligation.validator
    rule_type = rule.get("type")
    oid = obligation.id

    if rule_type == "prior_quote":
        authorized = [value for value in rule.get("authorized_quotes", []) if value]
        invented: list[str] = []
        for match in PRIOR_QUOTE_PATTERN.finditer(final_body):
            quote = normalized(match.group(1))
            if not quote:
                continue
            if any(quote == value or quote in value or value in quote for value in authorized):
                continue
            invented.append(match.group(0))
        return ObligationCheck(
            oid,
            CheckStatus.FAIL if invented else CheckStatus.PASS,
            "invented prior dialogue/history backreference" if invented else "no unauthorized prior-dialogue backreference",
            tuple(invented[:4]),
        )

    if rule_type == "source_conflict":
        return ObligationCheck(oid, CheckStatus.CONFLICT, obligation.source_text)

    if rule_type in {"mission_clause", "reader_release"}:
        evidence_ids = set(obligation.primary_evidence_paragraphs)
        if evidence_ids and not (evidence_ids & touched):
            return ObligationCheck(
                oid, CheckStatus.PASS_PRESERVED,
                "Primary evidence paragraphs were not touched.",
                tuple(f"P{index:03d}" for index in sorted(evidence_ids)),
            )
        best_score, best = 0.0, ""
        source = obligation.source_text
        terms = list(rule.get("terms", []))
        actions = list(rule.get("actions", detect_action_classes(source)))
        threshold = float(rule.get("minimum_score", 0.23))
        for paragraph in final_parts:
            score = clause_similarity(source, paragraph, terms, actions)
            if score > best_score:
                best_score, best = score, paragraph
            candidate_actions = set(detect_action_classes(paragraph))
            matched_terms = [term for term in terms if term in paragraph]
            if matched_terms and actions and candidate_actions.intersection(actions):
                return ObligationCheck(
                    oid,
                    CheckStatus.PASS,
                    "strong term + action bundle found",
                    (paragraph[:220],),
                )
        matched_terms = [term for term in terms if term in final_body]
        required_terms = min(3, max(1, (len(terms) + 1) // 2)) if terms else 0
        action_overlap = set(actions).intersection(detect_action_classes(final_body))
        if required_terms and len(matched_terms) >= required_terms and (not actions or action_overlap):
            return ObligationCheck(
                oid,
                CheckStatus.PASS,
                f"chapter-wide clause coverage terms={len(matched_terms)}/{len(terms)} actions={sorted(action_overlap)}",
                tuple(matched_terms[:6]),
            )
        if best_score >= threshold:
            return ObligationCheck(oid, CheckStatus.PASS, f"semantic anchor score={best_score:.3f}", (best[:220],))
        return ObligationCheck(
            oid, CheckStatus.FAIL,
            f"No final paragraph met threshold {threshold:.2f}; best={best_score:.3f}.",
            (best[:220],) if best else (),
        )

    if rule_type == "actor_action_object":
        evidence_ids = set(obligation.primary_evidence_paragraphs)
        if evidence_ids and not (evidence_ids & touched):
            return ObligationCheck(
                oid,
                CheckStatus.PASS_PRESERVED,
                "Primary actor-action-object evidence was untouched.",
                tuple(f"P{index:03d}" for index in sorted(evidence_ids)),
            )
        source_actions = set(rule.get("actions", []))
        for paragraph in final_parts:
            if not any(term in paragraph for term in rule.get("subject_terms", [])):
                continue
            if not any(term in paragraph for term in rule.get("object_terms", [])):
                continue
            if source_actions and not source_actions.intersection(detect_action_classes(paragraph)):
                continue
            return ObligationCheck(
                oid,
                CheckStatus.PASS,
                "actor, action class and object co-occur in one paragraph",
                (paragraph[:220],),
            )
        return ObligationCheck(
            oid,
            CheckStatus.FAIL,
            "actor-action-object did not close in one local paragraph",
        )

    if rule_type == "power_transition":
        target = re.escape(str(rule["target"]))
        pattern = rf"(?:正式进入|第一次正式进入|突破(?:到|至)?|晋升(?:到|至)?|成为)\s*{target}|{target}(?:已成|成立)"
        match = re.search(pattern, final_body)
        return ObligationCheck(
            oid, CheckStatus.PASS if match else CheckStatus.FAIL,
            "explicit stable transition found" if match else "battle/result implication is not an explicit stable transition",
            (match.group(0),) if match else (),
        )

    if rule_type == "forbid_power_transition":
        target = re.escape(str(rule["target"]))
        pattern = rf"(?:正式进入|第一次正式进入|突破(?:到|至)?|晋升(?:到|至)?|成为)\s*{target}|{target}(?:已成|成立)"
        match = re.search(pattern, final_body)
        return ObligationCheck(
            oid, CheckStatus.FAIL if match else CheckStatus.PASS,
            "unauthorized stable transition" if match else "no unauthorized stable transition",
            (match.group(0),) if match else (),
        )

    if rule_type == "clone_boundary":
        evidence_ids = set(obligation.primary_evidence_paragraphs)
        ability_terms = rule.get("ability_terms", [])
        unauthorized_patterns = (
            r"分身[^。]{0,30}(?:携带|拥有|获得|带着)(?:本体)?全部力量",
            r"分身[^。]{0,30}完整(?:潮炉|成炉|照域|力量)",
            r"分身[^。]{0,30}与本体同等力量",
        )
        for pattern in unauthorized_patterns:
            match = re.search(pattern, final_body)
            if match:
                prefix = final_body[max(0, match.start() - 12):match.start()]
                if re.search(r"没有|并无|不携带|不能携带|未携带|不具备", prefix):
                    continue
                return ObligationCheck(
                    oid,
                    CheckStatus.FAIL,
                    "clone limitation was upgraded into full-power transfer",
                    (match.group(0),),
                )
        groups = [rule["subject_terms"], rule["limit_terms"], rule["full_terms"] + ability_terms]
        ok, evidence = _any_local_window_with_groups(final_parts, groups)
        if ok:
            return ObligationCheck(
                oid,
                CheckStatus.PASS,
                "explicit current clone limitation realized",
                (evidence[:220],),
            )
        if evidence_ids and not (evidence_ids & touched):
            return ObligationCheck(
                oid,
                CheckStatus.PASS_PRESERVED,
                "Primary clone-boundary evidence was untouched.",
                tuple(f"P{index:03d}" for index in sorted(evidence_ids)),
            )
        return ObligationCheck(
            oid,
            CheckStatus.PASS,
            "no unauthorized full-power transfer; explicit re-explanation is not a quota",
        )

    if rule_type == "ownership":
        if rule.get("forbidden_destination_terms"):
            # Original/copy transfer must bind inside one sentence-level action domain.
            # Do not merge “顾停舟收好原册” with the next paragraph where another
            # actor carries a fact copy.
            sentences = [
                sentence.strip()
                for sentence in re.split(r"[。！？\n]+", final_body)
                if sentence.strip()
            ]
            for sentence in sentences:
                if not any(term in sentence for term in rule["object_terms"]):
                    continue
                if not any(term in sentence for term in rule.get("forbidden_destination_terms", [])):
                    continue
                if not contains_unnegated_term(sentence, rule.get("forbidden_transfer_terms", [])):
                    continue
                return ObligationCheck(
                    oid,
                    CheckStatus.FAIL,
                    "original object was transferred to a destination that should receive only a copy",
                    (sentence[:220],),
                )
        ok, evidence = _any_local_window_with_groups(
            final_parts, [rule["object_terms"], rule["owner_terms"], rule["possession_terms"]]
        )
        return ObligationCheck(
            oid, CheckStatus.PASS if ok else CheckStatus.FAIL,
            "authorized possession state found" if ok else "missing or weakened possession state",
            (evidence[:220],) if evidence else (),
        )

    if rule_type == "transfer":
        evidence = ""
        for window in _local_windows(final_parts):
            if not any(term in window for term in rule["object_terms"]):
                continue
            if not any(term in window for term in rule["destination_terms"]):
                continue
            if contains_unnegated_term(window, rule["transfer_terms"]):
                evidence = window
                break
        return ObligationCheck(
            oid, CheckStatus.PASS if evidence else CheckStatus.FAIL,
            "copy transfer found" if evidence else "missing or negated copy transfer / original-copy distinction",
            (evidence[:220],) if evidence else (),
        )

    if rule_type == "dispute":
        ok, evidence = _any_local_window_with_groups(
            final_parts, [rule["object_terms"], rule["dispute_terms"]]
        )
        return ObligationCheck(
            oid, CheckStatus.PASS if ok else CheckStatus.FAIL,
            "ongoing dispute preserved" if ok else "possession collapsed into uncontested title",
            (evidence[:220],) if evidence else (),
        )

    if rule_type == "status":
        object_terms = rule["object_terms"]
        status = str(rule["status"])
        expected = list(dict.fromkeys([
            *rule.get("status_terms", []),
            *STATUS_SYNONYMS.get(status, ()),
        ]))
        ok, evidence = _any_local_window_with_groups(final_parts, [object_terms, expected]) if expected else (False, "")
        if not ok and status == "entitlement_confirmed":
            ok, evidence = _any_local_window_with_groups(
                final_parts, [object_terms, ["份额", "依据", "登记", "确认", "记"]]
            )
        if not ok:
            return ObligationCheck(oid, CheckStatus.FAIL, f"missing terminal status={status} for {object_terms}")
        object_paragraphs = [
            paragraph for paragraph in final_parts
            if any(term in paragraph for term in object_terms)
        ]
        if status == "received":
            partial_markers = [
                marker for marker in PARTIAL_RESOURCE_MARKERS
                if any(marker in paragraph for paragraph in object_paragraphs)
            ]
            if partial_markers and not bool(rule.get("partial_authorized")):
                return ObligationCheck(
                    oid,
                    CheckStatus.FAIL,
                    "partial receipt cannot satisfy a full terminal settlement",
                    tuple(partial_markers),
                )
            authorized_amounts = set(rule.get("authorized_amounts", []))
            seen_amounts = {
                amount
                for paragraph in object_paragraphs
                for amount in MONEY_AMOUNT_PATTERN.findall(paragraph)
            }
            unauthorized_amounts = seen_amounts - authorized_amounts
            if unauthorized_amounts:
                return ObligationCheck(
                    oid,
                    CheckStatus.FAIL,
                    "unauthorized amount or unit in received resource",
                    tuple(sorted(unauthorized_amounts)),
                )
        incompatible_patterns = {
            "entitlement_confirmed": r"到账|终于落进.*手|交到.*手|交进.*手|已经结清|当场付清|已经拿到|已经领到",
            "pending": r"到账|终于落进.*手|交到.*手|交进.*手|已经结清|当场付清|已经拿到|已经领到|交付完毕",
            "lost": r"到账|终于落进.*手|交到.*手|交进.*手|已经结清|当场付清|已经拿到|已经领到|重新兑现",
            "received": r"无法兑现|明确放弃|已经放弃|仍未到账|尚未到账|待.*结算",
        }
        incompatible = incompatible_patterns.get(status)
        if incompatible:
            for paragraph in final_parts:
                if any(term in paragraph for term in object_terms) and re.search(incompatible, paragraph):
                    return ObligationCheck(
                        oid,
                        CheckStatus.FAIL,
                        f"terminal status={status} conflicts with another state",
                        (paragraph[:220],),
                    )
        return ObligationCheck(oid, CheckStatus.PASS, f"status={status} found", (evidence[:220],))

    if rule_type == "deadline":
        terms = rule["terms"]
        matches = [paragraph for paragraph in final_parts if sum(term in paragraph for term in terms) >= max(2, len(terms) - 1)]
        return ObligationCheck(
            oid, CheckStatus.PASS if matches else CheckStatus.FAIL,
            "deadline retained" if matches else "deadline window missing",
            (matches[0][:220],) if matches else (),
        )

    if rule_type == "departure":
        protagonist = str(rule.get("protagonist", ""))
        context_terms = list(rule.get("context_terms", []))
        for index, paragraph in enumerate(final_parts):
            action_terms = [term for term in rule["terms"] if term in paragraph]
            if not action_terms or not contains_unnegated_term(paragraph, action_terms):
                continue
            action_start = min(paragraph.find(term) for term in action_terms if paragraph.find(term) >= 0)
            prefix = paragraph[:action_start]
            named_positions = [
                (prefix.rfind(name), name)
                for name in NAMED_ACTORS
                if prefix.rfind(name) >= 0
            ]
            resolved = max(named_positions)[1] if named_positions else ""
            if not resolved and re.search(r"(?:^|[。！？”])\s*(?:他|我)[^。！？]{0,24}$", prefix):
                for previous in reversed(final_parts[max(0, index - 5):index]):
                    names = [name for name in NAMED_ACTORS if name in previous]
                    if names:
                        resolved = names[-1]
                        break
            if resolved != protagonist:
                continue
            local = "\n\n".join(final_parts[max(0, index - 1):index + 2])
            explicit_departure = "随队出发" in paragraph
            if context_terms and not explicit_departure and not any(term in local for term in context_terms):
                continue
            return ObligationCheck(
                oid,
                CheckStatus.PASS,
                "actual protagonist departure shown with bound journey context",
                (paragraph[:220],),
            )
        return ObligationCheck(
            oid,
            CheckStatus.FAIL,
            "ending stopped at preparation, negated departure, or another person's departure",
        )

    if rule_type == "single_cycle":
        has_object = any(term in final_body for term in rule["object_terms"])
        equivalents = {
            "锁": ("锁", "钉定"),
            "改向": ("改向", "转向", "拧进", "送回主槽", "改变"),
            "释放": ("释放", "放出", "泻出", "该放", "送回主槽", "弹回"),
        }
        has_steps = all(any(term in final_body for term in equivalents.get(step, (step,))) for step in rule["step_terms"])
        repeated = False
        for term in rule["repeat_forbidden"]:
            for match in re.finditer(re.escape(term), final_body):
                prefix = final_body[max(0, match.start() - 8):match.start()]
                if re.search(r"不能|不可|不得|没有|未曾|不许|别", prefix):
                    continue
                repeated = True
                break
            if repeated:
                break
        ok = has_object and has_steps and not repeated
        return ObligationCheck(
            oid, CheckStatus.PASS if ok else CheckStatus.FAIL,
            f"single cycle object={has_object} steps={has_steps} repeated={repeated}",
        )

    if rule_type == "residual_pressure":
        if bool(rule.get("terminal")):
            counter = re.search(r"残压(?:还|仍|正在).*散|残压没散|残压未散", final_body)
            if counter:
                return ObligationCheck(
                    oid, CheckStatus.FAIL,
                    "terminal state still says residual pressure is dissipating",
                    (counter.group(0),),
                )
            ok = any(pattern in final_body for pattern in ("残压散尽", "残压已经散", "残压彻底散", "不再有残压"))
            return ObligationCheck(
                oid, CheckStatus.PASS if ok else CheckStatus.FAIL,
                "residual pressure terminal state complete" if ok else "missing explicit terminal dissipation",
            )
        ok = "残压" in final_body and any(term in final_body for term in rule["cooldown_terms"])
        return ObligationCheck(
            oid, CheckStatus.PASS if ok else CheckStatus.FAIL,
            "cooldown boundary retained" if ok else "missing cooldown before reuse",
        )

    if rule_type == "public_proof":
        subject_terms = list(rule.get("subject_terms", []))
        topic_terms = list(rule.get("topic_terms", []))
        components: dict[str, str] = {}
        component_link_terms = [
            *topic_terms,
            *subject_terms,
            *rule.get("performance_terms", []),
            "战绩", "这一下", "这次", "刚才", "看完", "当场",
        ]
        for index, paragraph in enumerate(final_parts):
            if not any(term in paragraph for term in rule.get("performance_terms", [])):
                continue
            local = "\n\n".join(final_parts[max(0, index - 1):index + 2])
            if subject_terms and not any(term in local for term in subject_terms):
                continue
            if topic_terms and not any(term in local for term in topic_terms):
                continue
            ruler_index = next(
                (
                    candidate_index
                    for candidate_index in range(index, min(len(final_parts), index + 24))
                    if any(term in final_parts[candidate_index] for term in rule.get("ruler_terms", []))
                    and any(term in final_parts[candidate_index] for term in component_link_terms)
                ),
                -1,
            )
            if ruler_index < 0:
                continue
            repricing_index = next(
                (
                    candidate_index
                    for candidate_index in range(ruler_index, min(len(final_parts), ruler_index + 32))
                    if any(term in final_parts[candidate_index] for term in rule.get("repricing_terms", []))
                    and any(term in final_parts[candidate_index] for term in component_link_terms)
                ),
                -1,
            )
            if repricing_index < 0:
                continue
            components = {
                "performance": paragraph,
                "ruler": final_parts[ruler_index],
                "repricing": final_parts[repricing_index],
            }
            break
        passed = all(components.get(name) for name in ("performance", "ruler", "repricing"))
        return ObligationCheck(
            oid, CheckStatus.PASS if passed else CheckStatus.FAIL,
            "public proof components=" + ",".join(name for name, value in components.items() if value),
            tuple(value[:180] for value in components.values() if value),
        )

    if rule_type == "relationship":
        evidence = ""
        for window in _local_windows(final_parts, window_size=2):
            if not any(term in window for term in rule.get("terms", [])):
                continue
            counterpart_terms = list(rule.get("counterpart_terms", []))
            if counterpart_terms and not any(term in window for term in counterpart_terms):
                continue
            subject_terms = list(rule.get("subject_terms", []))
            if subject_terms and not any(term in window for term in subject_terms):
                continue
            transition_terms = list(rule.get("transition_terms", []))
            if transition_terms and not any(term in window for term in transition_terms):
                continue
            evidence = window
            break
        return ObligationCheck(
            oid, CheckStatus.PASS if evidence else CheckStatus.FAIL,
            "relationship transition visible for the named counterpart" if evidence else "relationship state missing, unbound, or attached to another counterpart",
            (evidence[:220],) if evidence else (),
        )

    if rule_type == "unresolved":
        topic_terms = rule.get("topic_terms", [])
        for paragraph in final_parts:
            if topic_terms and not any(term in paragraph for term in topic_terms):
                continue
            if any(marker in paragraph for marker in rule.get("revelation_terms", [])):
                if re.search(r"不知道|未知|未查明|仍未", paragraph):
                    continue
                return ObligationCheck(
                    oid, CheckStatus.FAIL,
                    "unresolved fact converted into revelation",
                    (paragraph[:220],),
                )
        return ObligationCheck(
            oid, CheckStatus.PASS,
            "no unauthorized revelation; explicit mention was not required",
        )

    if rule_type == "pending_boundary":
        topic_terms = rule.get("topic_terms", [])
        for paragraph in final_parts:
            if topic_terms and not any(term in paragraph for term in topic_terms):
                continue
            if any(term in paragraph for term in rule.get("completion_terms", [])):
                return ObligationCheck(
                    oid,
                    CheckStatus.FAIL,
                    "pending state was upgraded into completed",
                    (paragraph[:220],),
                )
        evidence = next(
            (
                paragraph for paragraph in final_parts
                if (not topic_terms or any(term in paragraph for term in topic_terms))
                and any(term in paragraph for term in rule.get("pending_terms", []))
            ),
            "",
        )
        return ObligationCheck(
            oid,
            CheckStatus.PASS,
            "pending boundary preserved" if evidence else "no contradictory completion; explicit repetition not required",
            (evidence[:220],) if evidence else (),
        )

    if rule_type == "human_cue":
        for paragraph in final_parts:
            if (
                any(person in paragraph for person in rule.get("person_terms", []))
                and any(contact in paragraph for contact in rule.get("contact_terms", []))
                and any(cue in paragraph for cue in rule.get("cue_terms", []))
            ):
                return ObligationCheck(
                    oid, CheckStatus.PASS,
                    "specific cue appears at direct-contact trigger",
                    (paragraph[:220],),
                )
        return ObligationCheck(
            oid, CheckStatus.FAIL,
            "Human-specific cue trigger was active but no approved cue appeared",
        )

    if rule_type == "commercial_preserve":
        source_ids = set(rule.get("source_paragraphs", []))
        if not source_ids and rule.get("source_paragraph"):
            source_ids = {int(rule["source_paragraph"])}
        if source_ids and not (source_ids & touched):
            return ObligationCheck(
                oid,
                CheckStatus.PASS_PRESERVED,
                "protected commercial category evidence was untouched",
                tuple(f"P{source_id:03d}" for source_id in sorted(source_ids)),
            )
        category = str(rule.get("category", ""))
        markers = list(rule.get("markers", []))
        key_terms = list(rule.get("key_terms", []))
        category_markers = {
            "desire": ["想要", "舍不得", "不愿", "喜欢", "自己", "属于", "带母亲", "离开"],
            "reward": ["钱", "潮铢", "矿利", "份额", "行潮籍", "回潮楔", "潮髓", "战功", "票据", "使用权"],
            "relationship": ["合作", "主从", "旧情", "欠情", "同行", "不再替", "一起走", "各走", "朋友", "站在", "不是让你回去听令", "找你承运", "另谈", "短契", "按了印"],
            "social_repricing": ["目光", "报价", "价钱", "买断", "入册", "公开", "重新", "不再把", "承认", "追索"],
            "surprise": ["没想到", "谁也没想到", "竟然", "竟是", "原来", "多出来", "忽然发现", "反而"],
        }.get(category, [])
        evidence = next(
            (
                paragraph for paragraph in final_parts
                if any(marker in paragraph for marker in [*markers, *category_markers])
                and (not key_terms or any(term in paragraph for term in key_terms) or category in {"desire", "social_repricing"})
            ),
            "",
        )
        if not evidence and category != "surprise" and rule.get("source_text"):
            source_text = str(rule["source_text"])
            best_score, best = 0.0, ""
            for paragraph in final_parts:
                score = clause_similarity(source_text, paragraph, key_terms, detect_action_classes(source_text))
                if score > best_score:
                    best_score, best = score, paragraph
            if best_score >= 0.20:
                evidence = best
        return ObligationCheck(
            oid,
            CheckStatus.PASS if evidence else CheckStatus.FAIL,
            f"protected {category} retained" if evidence else f"touched category lost protected {category}",
            (evidence[:220],) if evidence else (),
        )

    return ObligationCheck(oid, CheckStatus.UNKNOWN, f"unsupported validator type={rule_type}")


def validate_candidate(
    pack: ObligationPack,
    *,
    primary_body: str,
    final_body: str,
    operations: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    final_parts = paragraphs(final_body)
    touched = touched_source_paragraphs(operations)
    checks = [_check_obligation(item, final_body, final_parts, touched) for item in pack.obligations]
    severity_by_id = {item.id: item.severity for item in pack.obligations}
    blocking = [
        item for item in checks
        if item.status in {CheckStatus.FAIL, CheckStatus.UNKNOWN, CheckStatus.CONFLICT}
        and severity_by_id[item.obligation_id] == GateSeverity.HARD
    ]
    decision = "ADOPT_DELTA" if pack.preflight_eligible and not blocking else "FALLBACK_FULL_REVISER"
    return {
        "version": "atomic-obligations-v0.3-boundary-calibrated",
        "chapter": pack.chapter,
        "preflight_eligible": pack.preflight_eligible,
        "decision": decision,
        "touched_source_paragraphs": sorted(touched),
        "blocking_checks": [item.to_dict() for item in blocking],
        "checks": [item.to_dict() for item in checks],
        "status_counts": {
            status.value: sum(item.status == status for item in checks)
            for status in CheckStatus
        },
    }


def save_pack(pack: ObligationPack, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(pack.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_operations(summary_path: Path, chapter: int) -> list[dict[str, Any]]:
    rows = json.loads(summary_path.read_text(encoding="utf-8"))
    return list(next(item for item in rows if int(item["chapter"]) == int(chapter)).get("operations", []))
