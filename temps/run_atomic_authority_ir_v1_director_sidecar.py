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
OUT = ROOT / "books" / "real-exp-atomic-authority-ir-20260829-v1" / "phase-b-director-sidecar"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")

sys.path.insert(0, str(ROOT / "temps"))

from atomic_authority_ir_v1 import (  # noqa: E402
    AtomicAuthorityContractBuilder,
    EntityRegistry,
    FactKind,
    IRValidationError,
    save_json,
)
from run_atomic_authority_ir_v1_static import sample_specs  # noqa: E402


SIDECAR_INSTRUCTION = r"""

# ATOMIC AUTHORITY IR v1｜本实验附加输出

你仍然先完成上方八字段 Director 事件合同。随后必须追加一个机器 Sidecar；Sidecar 与八字段在同一次 Director 决策中产生，不是事后重新理解中文。

Hard IR 只允许记录你已经在八字段中决定的当前章事实。它不能读取或投影未来 Primary / Curator，不包含 prose 保护、写法建议、欲望检测、Surprise 检测或评分。

严格输出顺序：

1. 原本的八字段事件合同；
2. 可选 `## 专项建议`；
3. `## ATOMIC AUTHORITY IR`；
4. 一个且仅一个 `json` fenced block。

JSON 格式：

```json
{
  "schema_version": "atomic-mission-ir-v1",
  "chapter_id": "<必须等于下方 Registry chapter_id>",
  "protagonist_id": "<必须等于下方 Registry protagonist_id>",
  "facts": [
    {
      "fact_id": "全大写稳定ID",
      "slot_id": "本章稳定状态槽",
      "source_ref": "director.<field>.<index>",
      "kind": "event | action | direct_result | state_transition | ending | power_transition | resource_transition | ownership_transition | relationship_transition | deadline | public_proof | reader_release | unknown_boundary | ability_boundary | historical_claim_boundary",
      "mode": "must_hold | terminal | must_not_hold | must_remain_unknown | conditional",
      "phase": "during_chapter | chapter_end | post_chapter | reader_knowledge",
      "actor_id": "Registry entity ID 或空字符串",
      "action_id": "简短英文snake_case动作，不写中文句子",
      "object_ids": ["Registry entity ID"],
      "counterparty_ids": ["Registry entity ID"],
      "from_state": "已知前态或空字符串",
      "to_state": "明确后态或空字符串",
      "value": null,
      "terminal": false,
      "condition_fact_ids": [],
      "depends_on_fact_ids": [],
      "metadata": {}
    }
  ]
}
```

边界：

- `source` 不由你输出；Runtime 会固定为 `frozen_mission`。
- 所有 actor/object/counterparty 必须使用 Registry ID，不能发明新 ID，也不能用名字代替 ID。
- 当前 protagonist 永远引用 Registry 的 `protagonist_id`；Primary 不参与身份判定。
- 只记录 Hard facts：谁做什么、对谁/什么、直接结果、章末状态、Ending、明确 deadline、明确 Power/Resource/Ownership/Relationship transition、已排程 Reader Release、必须保持未知的具体对象。
- “叙事功能”、情绪氛围、漂亮反应、欲望写法、Surprise、正文段落、Curator 判断都不进入 Hard IR。
- 不把首笔付款写成全额结清，不把资格写成到账，不把战斗表现写成稳定升阶，不把 deadline 写成已经完成。
- 若当前八字段没有决定稳定升级，就不要输出 `power_transition`。
- 同一事实不要拆成许多同义 fact；每个事实使用一个稳定 slot。
- Sidecar 必须完整覆盖八字段中的关键 action、Direct Result、State Change 与 Ending，但不得新增八字段没有的事实。

# ENTITY REGISTRY｜只允许引用下列 ID

{ENTITY_REGISTRY_JSON}
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


def parse_response(text: str) -> tuple[str, dict[str, Any]]:
    marker = "## ATOMIC AUTHORITY IR"
    if marker not in text:
        raise IRValidationError("missing ATOMIC AUTHORITY IR marker")
    mission, tail = text.split(marker, 1)
    match = re.search(r"```json\s*(\{.*?\})\s*```", tail, re.S)
    if not match:
        raise IRValidationError("missing JSON fenced block")
    payload = json.loads(match.group(1))
    return mission.strip(), payload


def expected_mission_facts(spec: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [
        fact
        for fragment in spec["fragments"]
        if fragment["source"] == "frozen_mission"
        for fact in fragment["facts"]
    ]


def match_expected(
    expected: Mapping[str, Any],
    generated: Mapping[str, Any],
) -> bool:
    if expected["kind"] != generated.get("kind"):
        return False
    if expected["phase"] != generated.get("phase"):
        return False
    expected_actor = expected.get("actor_id", "")
    if expected_actor and expected_actor != generated.get("actor_id", ""):
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
    return True


def one(spec: Mapping[str, Any]) -> dict[str, Any]:
    name = str(spec["name"])
    directory = OUT / name
    directory.mkdir(parents=True, exist_ok=True)
    registry = EntityRegistry.from_dict(spec["registry"])
    original_prompt = (spec["source_dir"] / "director_prompt.md").read_text(
        encoding="utf-8"
    )
    prompt = original_prompt.rstrip() + "\n\n" + SIDECAR_INSTRUCTION.replace(
        "{ENTITY_REGISTRY_JSON}",
        json.dumps(registry.to_dict(), ensure_ascii=False, indent=2),
    )
    prompt_path = directory / "director_sidecar_prompt.md"
    output_path = directory / "director_sidecar_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(str(data.get("text", "")))
    (directory / "director_sidecar_response.md").write_text(
        response + "\n", encoding="utf-8"
    )

    parse_error = ""
    mission = ""
    sidecar: dict[str, Any] = {}
    contract = None
    try:
        mission, sidecar = parse_response(response)
        save_json(directory / "mission_sidecar.json", sidecar)
        builder = AtomicAuthorityContractBuilder(registry)
        for fragment in spec["fragments"]:
            if fragment["source"] != "frozen_mission":
                builder.add_fragment(fragment)
        builder.add_fragment(
            {
                "source": "frozen_mission",
                "facts": sidecar.get("facts", []),
            }
        )
        contract = builder.build()
        save_json(directory / "merged_atomic_authority_contract.json", contract.to_dict())
    except Exception as error:
        parse_error = f"{type(error).__name__}: {error}"

    control_data = json.loads(
        (spec["source_dir"] / "director_acp.json").read_text(encoding="utf-8")
    )
    expected = expected_mission_facts(spec)
    generated = sidecar.get("facts", []) if isinstance(sidecar, dict) else []
    matched_expected = sum(
        any(match_expected(expected_fact, generated_fact) for generated_fact in generated)
        for expected_fact in expected
    )
    fact_kinds = sorted(
        {
            str(item.get("kind", ""))
            for item in generated
            if isinstance(item, Mapping)
        }
    )
    expected_kinds = sorted({str(item["kind"]) for item in expected})
    mission_fields_present = sum(field in mission for field in REQUIRED_FIELDS)
    registry_ids = set(registry.entities)
    referenced_ids = {
        entity_id
        for item in generated
        if isinstance(item, Mapping)
        for entity_id in (
            [str(item.get("actor_id", ""))]
            + [str(value) for value in item.get("object_ids", [])]
            + [str(value) for value in item.get("counterparty_ids", [])]
        )
        if entity_id
    }
    unknown_ids = sorted(referenced_ids - registry_ids)
    hard_sources = contract.to_dict()["hard_sources"] if contract else []

    (directory / "director_mission_only.md").write_text(
        mission + "\n", encoding="utf-8"
    )
    return {
        "sample": name,
        "chapter_id": registry.chapter_id,
        "parse_ok": not parse_error,
        "parse_error": parse_error,
        "mission_fields_present": mission_fields_present,
        "mission_fields_required": len(REQUIRED_FIELDS),
        "sidecar_schema_version": sidecar.get("schema_version", "")
        if isinstance(sidecar, dict)
        else "",
        "sidecar_chapter_id_matches": sidecar.get("chapter_id")
        == registry.chapter_id
        if isinstance(sidecar, dict)
        else False,
        "sidecar_protagonist_id_matches": sidecar.get("protagonist_id")
        == registry.protagonist_id
        if isinstance(sidecar, dict)
        else False,
        "generated_fact_count": len(generated),
        "generated_fact_kinds": fact_kinds,
        "expected_fact_count": len(expected),
        "expected_fact_kinds": expected_kinds,
        "expected_structural_matches": matched_expected,
        "expected_structural_coverage": round(
            matched_expected / max(1, len(expected)), 4
        ),
        "unknown_entity_ids": unknown_ids,
        "merged_contract_preflight_eligible": contract.preflight_eligible
        if contract
        else False,
        "merged_contract_conflicts": contract.conflicts if contract else [],
        "merged_contract_unsupported": contract.unsupported if contract else [],
        "hard_sources": hard_sources,
        "curator_or_primary_hard_source": any(
            source in {"curator", "primary", "primary_draft"}
            for source in hard_sources
        ),
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
        "sidecar_chars": len(
            json.dumps(sidecar, ensure_ascii=False, sort_keys=True)
        )
        if sidecar
        else 0,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    specs = sample_specs()
    with ThreadPoolExecutor(max_workers=len(specs)) as executor:
        futures = [executor.submit(one, spec) for spec in specs]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    rows.sort(key=lambda item: item["sample"])
    control_total = sum(row["control_director_wall_seconds"] for row in rows)
    treatment_total = sum(row["treatment_director_wall_seconds"] for row in rows)
    summary = {
        "schema_version": "atomic-authority-ir-v1-director-sidecar-experiment",
        "samples": len(rows),
        "parse_ok": sum(row["parse_ok"] for row in rows),
        "all_eight_fields_present": sum(
            row["mission_fields_present"] == row["mission_fields_required"]
            for row in rows
        ),
        "entity_ids_valid": sum(not row["unknown_entity_ids"] for row in rows),
        "merged_contracts_preflight_eligible": sum(
            row["merged_contract_preflight_eligible"] for row in rows
        ),
        "source_pure_contracts": sum(
            not row["curator_or_primary_hard_source"] for row in rows
        ),
        "average_expected_structural_coverage": round(
            sum(row["expected_structural_coverage"] for row in rows)
            / len(rows),
            4,
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
