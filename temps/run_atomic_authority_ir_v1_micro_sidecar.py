from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(r"C:\dev\tgn-story-mvp")
OUT = ROOT / "books" / "real-exp-atomic-authority-ir-20260829-v1" / "phase-d-micro-director-sidecar"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")

sys.path.insert(0, str(ROOT / "temps"))

from atomic_authority_ir_v1 import (  # noqa: E402
    AtomicAuthorityContractBuilder,
    EntityKind,
    EntityRegistry,
    IRValidationError,
    expand_micro_mission_sidecar,
    save_json,
)
from run_atomic_authority_ir_v1_static import sample_specs  # noqa: E402


MICRO_INSTRUCTION = r"""

# AAIR1 MICRO｜同次 Director 决策的极短 Sidecar

先照常输出八字段事件合同与必要的 `## 专项建议`。最后追加：

```text
## AAIR1 MICRO
```text
A|P|verb|OBJ1,OBJ2|CP1
R|kind|P|verb|OBJ1|CP1|from|to|json_or_-
S|kind|P|verb|OBJ1|CP1|from|to|json_or_-
E|kind|P|verb|OBJ1|CP1|from|to|json_or_-
B|kind|P_or_-|verb|OBJ1|CP1|mode|to|json_or_-
```
```

只允许这些行；不要输出 JSON、fact_id、slot、source、source_ref、phase、paragraph、欲望/Surprise/写法建议。Runtime 会确定性生成 persistent IDs 和 slots。

类别：
- `A` = current-chapter protagonist/clone action；最多3行。
- `R` kind = `direct|resource|ownership|proof`；最多5行。
- `S` kind = `state|power|relationship|ability`；最多5行。
- `E` kind = `ending|deadline`；最多2行。
- `B` kind = `unknown|ability|history`；最多4行。

字段规则：
- `-` 表示空。
- 实体只用下方短句柄；`P` 是 canonical protagonist，不得用人物名字或另造句柄。
- `verb/from/to` 使用很短的英文 snake_case，无空格。
- R/S/E 的最后一列只有需要机器值时才写单行 JSON，否则 `-`。
- B 的第7列是 mode：`must_hold|must_not_hold|must_remain_unknown|conditional`。
- 不输出 trigger、叙事功能、普通气氛或同义重复；只保留关键 action、Direct Result、State Change、Ending、明确 deadline/boundary。
- “第一笔”必须保留 partial 状态；deadline不能写成已完成；战斗表现不能写成稳定升阶。
- Stable power transition 只有八字段明确批准时才写 `S|power`。
- 普通旧对白/生活记忆不写 history；只有改变 money/relationship/promise/mystery/current action basis/ownership/threat 的 critical history 才写。

# HANDLE TABLE

{HANDLE_TABLE}
"""


REQUIRED_FIELDS = (
    "触发事件：",
    "推动事件的人：",
    "主角行动：",
    "对手或世界反应：",
    "直接结果：",
    "状态变化：",
    "叙事功能：",
    "结尾推动力：",
)


KIND_PREFIX = {
    EntityKind.CHARACTER: "C",
    EntityKind.MANIFESTATION: "X",
    EntityKind.FACTION: "F",
    EntityKind.ORGANIZATION: "O",
    EntityKind.LOCATION: "L",
    EntityKind.ITEM: "I",
    EntityKind.RESOURCE: "M",
    EntityKind.CONTRACT: "K",
    EntityKind.ROUTE: "R",
    EntityKind.POWER_TIER: "T",
    EntityKind.ABILITY: "A",
    EntityKind.GROUP: "G",
    EntityKind.MYSTERY: "Y",
    EntityKind.EVENT: "E",
}


def handles_for(registry: EntityRegistry) -> dict[str, str]:
    result = {"P": registry.protagonist_id}
    counters: dict[str, int] = {}
    for entity_id in sorted(registry.entities):
        if entity_id == registry.protagonist_id:
            continue
        entity = registry.entities[entity_id]
        prefix = KIND_PREFIX[entity.kind]
        counters[prefix] = counters.get(prefix, 0) + 1
        result[f"{prefix}{counters[prefix]}"] = entity_id
    return result


def handle_table(registry: EntityRegistry, handles: Mapping[str, str]) -> str:
    return "\n".join(
        f"{handle} = {entity_id} = {registry.entities[entity_id].display_name}"
        for handle, entity_id in handles.items()
    )


def clean(text: str) -> str:
    return re.sub(
        r"(?ms)\n*<oai-mem-citation>.*?</oai-mem-citation>\s*$",
        "",
        text,
    ).strip()


def call(prompt: Path, output: Path) -> dict[str, Any]:
    last = ""
    for attempt in range(3):
        try:
            process = subprocess.run(
                [
                    "node",
                    str(RUNNER),
                    str(prompt),
                    str(output),
                    "gpt-5.6-luna",
                    "high",
                    str(ROOT),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=1200,
            )
        except subprocess.TimeoutExpired:
            last = f"timeout after 1200s: {prompt}"
            time.sleep(2 + attempt * 2)
            continue
        if process.returncode == 0 and output.exists():
            try:
                data = json.loads(output.read_text(encoding="utf-8"))
            except Exception as error:
                data = {}
                last = str(error)
            if data.get("ok"):
                return data
            last = str(data.get("error", ""))
        else:
            last = (process.stderr + "\n" + process.stdout)[-4000:]
        time.sleep(2 + attempt * 2)
    raise RuntimeError(last)


def parse_response(text: str) -> tuple[str, str]:
    marker = "## AAIR1 MICRO"
    if marker not in text:
        raise IRValidationError("missing AAIR1 MICRO marker")
    mission, tail = text.split(marker, 1)
    match = re.search(r"```(?:text)?\s*(.*?)\s*```", tail, re.S)
    if not match:
        raise IRValidationError("missing micro fenced block")
    return mission.strip(), match.group(1).strip()


def expected_mission_facts(spec: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [
        fact
        for fragment in spec["fragments"]
        if fragment["source"] == "frozen_mission"
        for fact in fragment["facts"]
    ]


def match_expected(expected: Mapping[str, Any], generated: Mapping[str, Any]) -> bool:
    if expected["kind"] != generated.get("kind"):
        return False
    if expected.get("actor_id") and expected.get("actor_id") != generated.get(
        "actor_id"
    ):
        return False
    expected_objects = set(expected.get("object_ids", []))
    generated_objects = set(generated.get("object_ids", []))
    if expected_objects and not expected_objects.intersection(generated_objects):
        return False
    expected_counterparties = set(expected.get("counterparty_ids", []))
    generated_counterparties = set(generated.get("counterparty_ids", []))
    if expected_counterparties and not expected_counterparties.intersection(
        generated_counterparties
    ):
        return False
    if bool(expected.get("terminal", False)) and not bool(
        generated.get("terminal", False)
    ):
        return False
    return True


def one(spec: Mapping[str, Any]) -> dict[str, Any]:
    name = str(spec["name"])
    directory = OUT / name
    directory.mkdir(parents=True, exist_ok=True)
    registry = EntityRegistry.from_dict(spec["registry"])
    handles = handles_for(registry)
    original_prompt = (spec["source_dir"] / "director_prompt.md").read_text(
        encoding="utf-8"
    )
    prompt = original_prompt.rstrip() + "\n\n" + MICRO_INSTRUCTION.replace(
        "{HANDLE_TABLE}", handle_table(registry, handles)
    )
    prompt_path = directory / "micro_director_prompt.md"
    output_path = directory / "micro_director_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(str(data.get("text", "")))
    (directory / "micro_director_response.md").write_text(
        response + "\n", encoding="utf-8"
    )

    parse_error = ""
    mission = ""
    micro = ""
    generated_facts = []
    contract = None
    try:
        mission, micro = parse_response(response)
        (directory / "micro_sidecar.txt").write_text(
            micro + "\n", encoding="utf-8"
        )
        generated_facts = expand_micro_mission_sidecar(
            micro, registry, handles
        )
        save_json(
            directory / "expanded_mission_fragment.json",
            {
                "source": "frozen_mission",
                "facts": [fact.to_dict() for fact in generated_facts],
            },
        )
        builder = AtomicAuthorityContractBuilder(registry)
        for fragment in spec["fragments"]:
            if fragment["source"] != "frozen_mission":
                builder.add_fragment(fragment)
        for fact in generated_facts:
            builder.add_fact(fact)
        contract = builder.build()
        save_json(
            directory / "merged_atomic_authority_contract.json",
            contract.to_dict(),
        )
    except Exception as error:
        parse_error = f"{type(error).__name__}: {error}"

    control_data = json.loads(
        (spec["source_dir"] / "director_acp.json").read_text(encoding="utf-8")
    )
    expected = expected_mission_facts(spec)
    generated_dicts = [fact.to_dict() for fact in generated_facts]
    matches = sum(
        any(match_expected(item, candidate) for candidate in generated_dicts)
        for item in expected
    )
    (directory / "director_mission_only.md").write_text(
        mission + "\n", encoding="utf-8"
    )
    return {
        "sample": name,
        "chapter_id": registry.chapter_id,
        "parse_ok": not parse_error,
        "parse_error": parse_error,
        "mission_fields_present": sum(field in mission for field in REQUIRED_FIELDS),
        "generated_fact_count": len(generated_facts),
        "expected_fact_count": len(expected),
        "expected_structural_matches": matches,
        "expected_structural_coverage": round(
            matches / max(1, len(expected)), 4
        ),
        "merged_contract_preflight_eligible": contract.preflight_eligible
        if contract
        else False,
        "merged_contract_conflicts": contract.conflicts if contract else [],
        "merged_contract_unsupported": contract.unsupported if contract else [],
        "hard_sources": contract.to_dict()["hard_sources"] if contract else [],
        "control_director_wall_seconds": float(
            control_data.get("wall_seconds") or 0
        ),
        "treatment_director_wall_seconds": float(data.get("wall_seconds") or 0),
        "control_response_chars": len(
            (spec["source_dir"] / "director_response.md").read_text(
                encoding="utf-8"
            )
        ),
        "treatment_mission_chars": len(mission),
        "micro_sidecar_chars": len(micro),
        "micro_line_count": len(
            [line for line in micro.splitlines() if line.strip()]
        ),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    specs = sample_specs()
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=len(specs)) as executor:
        futures = [executor.submit(one, spec) for spec in specs]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["sample"])
    control_total = sum(row["control_director_wall_seconds"] for row in rows)
    treatment_total = sum(
        row["treatment_director_wall_seconds"] for row in rows
    )
    summary = {
        "schema_version": "atomic-authority-ir-v1-micro-sidecar-experiment",
        "samples": len(rows),
        "parse_ok": sum(row["parse_ok"] for row in rows),
        "all_eight_fields_present": sum(
            row["mission_fields_present"] == len(REQUIRED_FIELDS)
            for row in rows
        ),
        "merged_contracts_preflight_eligible": sum(
            row["merged_contract_preflight_eligible"] for row in rows
        ),
        "average_expected_structural_coverage": round(
            sum(row["expected_structural_coverage"] for row in rows)
            / len(rows),
            4,
        ),
        "average_micro_sidecar_chars": round(
            sum(row["micro_sidecar_chars"] for row in rows) / len(rows), 1
        ),
        "average_micro_line_count": round(
            sum(row["micro_line_count"] for row in rows) / len(rows), 2
        ),
        "control_total_seconds": round(control_total, 3),
        "treatment_total_seconds": round(treatment_total, 3),
        "sidecar_wall_change_percent": round(
            (treatment_total / control_total - 1) * 100, 2
        )
        if control_total
        else None,
        "rows": rows,
    }
    save_json(OUT / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
