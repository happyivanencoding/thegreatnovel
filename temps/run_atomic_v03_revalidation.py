from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r'C:\dev\tgn-story-mvp')
SOURCE = ROOT / 'books' / 'real-exp-fast-world-20ch-20260828-v1' / 'runs'
BASE = ROOT / 'books' / 'real-exp-atomic-chapter-obligations-20260829-v1'
RUNS = {
    'run1': BASE / 'phase-h-atomic-delta-corrected',
    'run2': BASE / 'phase-h2-atomic-delta-corrected-repeat2',
}
OUT = BASE / 'phase-k-v03-revalidation'
CHAPTERS = (2, 9, 14, 16)

sys.path.insert(0, str(ROOT / 'temps'))
from atomic_chapter_obligations import (  # noqa: E402
    body,
    compile_obligations,
    infer_diff_operations,
    save_pack,
    validate_candidate,
)


def load_summary(directory: Path) -> dict[int, dict]:
    raw = json.loads((directory / 'summary.json').read_text(encoding='utf-8'))
    return {int(row['chapter']): row for row in raw['rows']}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    old_summaries = {name: load_summary(path) for name, path in RUNS.items()}
    rows = []
    route_bodies: dict[str, dict[int, str]] = {name: {} for name in RUNS}

    for chapter in CHAPTERS:
        source = SOURCE / f'chapter-{chapter:04d}'
        primary = body((source / 'primary_response.md').read_text(encoding='utf-8'))
        full = body((source / 'authority_reviser_response.md').read_text(encoding='utf-8'))
        pack = compile_obligations(
            chapter=chapter,
            authority_prompt=(source / 'authority_reviser_prompt.md').read_text(encoding='utf-8'),
            curator_response=(source / 'curator_response.md').read_text(encoding='utf-8'),
            primary_body=primary,
        )
        target = OUT / f'chapter-{chapter:04d}'
        save_pack(pack, target / 'obligation_pack.json')
        full_gate = validate_candidate(
            pack,
            primary_body=primary,
            final_body=full,
            operations=infer_diff_operations(primary, full),
        )
        (target / 'historical_full_gate.json').write_text(
            json.dumps(full_gate, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
        )

        for run_name, run_dir in RUNS.items():
            candidate = (run_dir / f'chapter-{chapter:04d}' / 'delta_body.md').read_text(encoding='utf-8').strip()
            delta_gate = validate_candidate(
                pack,
                primary_body=primary,
                final_body=candidate,
                operations=infer_diff_operations(primary, candidate),
            )
            (target / f'{run_name}_delta_gate.json').write_text(
                json.dumps(delta_gate, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
            )
            old_row = old_summaries[run_name][chapter]
            delta_seconds = float(old_row['delta_wall_seconds'])
            full_seconds = float(old_row['control_full_reviser_seconds'])

            if not pack.preflight_eligible:
                route_status = 'PREFLIGHT_FULL_REVISER'
                route_body = full
                effective_seconds = full_seconds
            elif delta_gate['decision'] == 'ADOPT_DELTA':
                route_status = 'ADOPT_DELTA'
                route_body = candidate
                effective_seconds = delta_seconds
            elif full_gate['decision'] == 'ADOPT_DELTA':
                route_status = 'FALLBACK_FULL_REVISER'
                route_body = full
                effective_seconds = delta_seconds + full_seconds
            else:
                route_status = 'FULL_REVISER_RESIDUAL_FAILURE'
                route_body = full
                effective_seconds = delta_seconds + full_seconds

            route_bodies[run_name][chapter] = route_body
            (target / f'{run_name}_route_final_body.md').write_text(route_body + '\n', encoding='utf-8')
            rows.append({
                'chapter': chapter,
                'run': run_name,
                'protagonist': pack.protagonist,
                'preflight_eligible': pack.preflight_eligible,
                'obligation_count': len(pack.obligations),
                'delta_gate_decision': delta_gate['decision'],
                'delta_blocking_ids': [item['obligation_id'] for item in delta_gate.get('blocking_checks', [])],
                'delta_blocking_reasons': [item['reason'] for item in delta_gate.get('blocking_checks', [])],
                'historical_full_gate_decision': full_gate['decision'],
                'historical_full_blocking_ids': [item['obligation_id'] for item in full_gate.get('blocking_checks', [])],
                'historical_full_blocking_reasons': [item['reason'] for item in full_gate.get('blocking_checks', [])],
                'route_status': route_status,
                'delta_seconds': delta_seconds,
                'control_full_seconds': full_seconds,
                'effective_seconds': round(effective_seconds, 3),
                'fallback_adjusted_speedup_percent': round((1 - effective_seconds / full_seconds) * 100, 2),
                'operation_count': int(old_row['operation_count']),
            })

    repeatability = []
    for chapter in CHAPTERS:
        run1_delta = (RUNS['run1'] / f'chapter-{chapter:04d}' / 'delta_body.md').read_text(encoding='utf-8').strip()
        run2_delta = (RUNS['run2'] / f'chapter-{chapter:04d}' / 'delta_body.md').read_text(encoding='utf-8').strip()
        repeatability.append({
            'chapter': chapter,
            'delta_exact': run1_delta == run2_delta,
            'route_exact': route_bodies['run1'][chapter] == route_bodies['run2'][chapter],
            'run1_route_status': next(row['route_status'] for row in rows if row['chapter'] == chapter and row['run'] == 'run1'),
            'run2_route_status': next(row['route_status'] for row in rows if row['chapter'] == chapter and row['run'] == 'run2'),
        })

    by_run = {}
    for run_name in RUNS:
        selected = [row for row in rows if row['run'] == run_name]
        control = sum(row['control_full_seconds'] for row in selected)
        effective = sum(row['effective_seconds'] for row in selected)
        by_run[run_name] = {
            'samples': len(selected),
            'adopted': sum(row['route_status'] == 'ADOPT_DELTA' for row in selected),
            'fallback_full': sum(row['route_status'] == 'FALLBACK_FULL_REVISER' for row in selected),
            'preflight_full': sum(row['route_status'] == 'PREFLIGHT_FULL_REVISER' for row in selected),
            'residual_failure': sum(row['route_status'] == 'FULL_REVISER_RESIDUAL_FAILURE' for row in selected),
            'control_total_seconds': round(control, 3),
            'effective_total_seconds': round(effective, 3),
            'fallback_adjusted_speedup_percent': round((1 - effective / control) * 100, 2),
        }

    summary = {
        'version': 'atomic-obligations-v0.3-boundary-calibrated',
        'chapters': list(CHAPTERS),
        'by_run': by_run,
        'repeatability': {
            'delta_exact_count': sum(row['delta_exact'] for row in repeatability),
            'route_exact_count': sum(row['route_exact'] for row in repeatability),
            'samples': len(repeatability),
            'rows': repeatability,
        },
        'rows': rows,
    }
    (OUT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in summary.items() if key != 'rows'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
