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
OUT = ROOT / "books" / "real-exp-atomic-authority-ir-20260829-v1" / "phase-c-compact-director-sidecar"
RUNNER = Path(r"C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs")

sys.path.insert(0, str(ROOT / "temps"))

from atomic_authority_ir_v1 import (  # noqa: E402
    AtomicAuthorityContractBuilder,
    EntityRegistry,
    IRValidationError,
    expand_compact_mission_sidecar,
    save_json,
)
from run_atomic_authority_ir_v1_static import sample_specs  # noqa: E402


COMPACT_INSTRUCTION = r"""

# AAIR1｜同次 Director 决策的短机器 Sidecar

先照常输出八字段事件合同与必要的 `## 专项建议`。最后追加：

```text
## AAIR1
```json
{...}
```

Sidecar 不是事后解析，也不允许包含 Primary / Curator / prose 保护。只把八字段里已经决定的 Hard facts 写成短槽位；Runtime 会确定性补 fact_id、source、source_ref、mode 和 phase。

严格 JSON：

```json
{
  "v": "AAIR1",
  "chapter": "Registry chapter_id",
  "protagonist": "Registry protagonist_id",
  "actions": [
    {"slot":"event:<chapter>:<short>","actor":"ID","verb":"snake_case","objects":["ID"],"counterparties":["ID"]}
  ],
  "results": [
    {"slot":"resource:<ID> 或 ownership:<ID> 或 result:<chapter>:<short>","kind":"direct_result|resource_transition|ownership_transition|public_proof","actor":"ID","verb":"snake_case","objects":["ID"],"counterparties":["ID"],"from":"","to":"","value":null,"terminal":true,"depends":["stable slot"],"meta":{}}
  ],
  "states": [
    {"slot":"power:<ID> 或 relationship:<ID>:<ID> 或 state:<ID>","kind":"state_transition|power_transition|relationship_transition|ability_boundary","actor":"ID","verb":"snake_case","objects":["ID"],"counterparties":["ID"],"from":"","to":"","value":null,"terminal":true,"depends":["stable slot"],"meta":{}}
  ],
  "ending": [
    {"slot":"ending:<chapter>:<short>","kind":"ending|deadline","actor":"ID","verb":"snake_case","objects":["ID"],"counterparties":["ID"],"from":"","to":"","value":null,"terminal":true,"depends":["stable slot"],"meta":{}}
  ],
  "boundaries": [
    {"slot":"mystery:<ID> 或 ability:<ID>:<short>","kind":"unknown_boundary|ability_boundary|historical_claim_boundary","mode":"must_hold|must_not_hold|must_remain_unknown|conditional","actor":"ID或空","verb":"snake_case","objects":["ID"],"counterparties":["ID"],"from":"","to":"","value":null,"depends":["stable slot"],"meta":{}}
  ]
}
```

严格限制：

- actions最多3，results最多5，states最多5，ending最多2，boundaries最多4；空类别写 `[]`。
- 不输出 event trigger、叙事功能、情绪、欲望写法、Surprise、段落建议或同义重复 fact。
- 所有实体只用 Registry ID；当前 protagonist 只用 Registry protagonist_id。
- `slot` 是跨 Authority 稳定接口，不能自由写 fact_id。跨源依赖只引用 slot。
- ownership必须使用 `ownership:<object_id>`；resource使用 `resource:<object_id>`；relationship使用 `relationship:<actor_id>:<counterparty_id>`；power使用 `power:<actor_id>`。
- “第一笔”保持 explicit partial；deadline不写成当前已经完成；战斗表现不写成 stable power transition。
- 若八字段没有批准稳定升级，不输出 power_transition。
- Hard Sidecar 只覆盖关键主角行动、直接结果、章末状态、Ending、明确 boundary。宁可少而准确，不要把整份八字段逐句转写。

# ENTITY REGISTRY

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
    marker = "## AAIR1"
    if marker not in text:
        raise IRValidationError("missing AAIR1 marker")
    mission, tail = text.split(marker, 1)
    match = re.search(r"```json\s*(\{.*?\})\s*```", tail, re.S)
    if not match:
        raise IRValidationError("missing compact JSON fenced block")
    return mission.strip(), json.loads(match.group(1))


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
    expected_terminal = bool(expected.get("terminal", False))
    generated_terminal = bool(generated.get("terminal", False))
    if expected_terminal and not generated_terminal:
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
    prompt = original_prompt.rstrip() + "\n\n" + COMPACT_INSTRUCTION.replace(
        "{ENTITY_REGISTRY_JSON}",
        json.dumps(registry.to_dict(), ensure_ascii=False, separators=(",", ":")),
    )
    prompt_path = directory / "compact_director_prompt.md"
    output_path = directory / "compact_director_acp.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    data = call(prompt_path, output_path)
    response = clean(str(data.get("text", "")))
    (directory / "compact_director_response.md").write_text(
        response + "\n", encoding="utf-8"
    )

    parse_error = ""
    mission = ""
    sidecar: dict[str, Any] = {}
    contract = None
    generated_facts = []
    try:
        mission, sidecar = parse_response(response)
        save_json(directory / "compact_sidecar.json", sidecar)
        generated_facts = expand_compact_mission_sidecar(sidecar, registry)
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
    sidecar_chars = len(
        json.dumps(sidecar, ensure_ascii=False, separators=(",", ":"))
    ) if sidecar else 0

    (directory / "director_mission_only.md").write_text(
        mission + "\n", encoding="utf-8"
    )
    return {
        "sample": name,
        "chapter_id": registry.chapter_id,
        "parse_ok": not parse_error,
        "parse_error": parse_error,
        "mission_fields_present": sum(field in mission for field in REQUIRED_FIELDS),
        "sidecar_version": sidecar.get("v", "") if sidecar else "",
        "chapter_id_matches": sidecar.get("chapter") == registry.chapter_id
        if sidecar
        else False,
        "protagonist_id_matches": sidecar.get("protagonist")
        == registry.protagonist_id
        if sidecar
        else False,
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
        "compact_sidecar_chars": sidecar_chars,
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
        "schema_version": "atomic-authority-ir-v1-compact-sidecar-experiment",
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
        "average_compact_sidecar_chars": round(
            sum(row["compact_sidecar_chars"] for row in rows) / len(rows),
            1,
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
