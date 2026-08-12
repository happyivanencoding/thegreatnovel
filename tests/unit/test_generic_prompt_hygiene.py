from pathlib import Path

FORBIDDEN_FIXTURE_NAMES = (
    "m500",
    "林雨薇",
    "cable-survival",
    "phase4",
    "phase5",
    "phase6",
)


def test_generic_production_prompts_contain_no_fixture_entities() -> None:
    root = Path(__file__).parents[2]
    files = [
        *sorted((root / "src" / "novel_authoring" / "planning").glob("*.py")),
        *sorted((root / "src" / "novel_authoring" / "workflows").glob("*.py")),
        *sorted((root / ".agents" / "skills").glob("*/SKILL.md")),
        *sorted((root / "docs" / "user").rglob("*.md")),
        *sorted((root / "docs" / "operations").rglob("*.md")),
    ]
    findings = {
        str(path.relative_to(root)): [
            name
            for name in FORBIDDEN_FIXTURE_NAMES
            if name in path.read_text(encoding="utf-8").casefold()
        ]
        for path in files
    }
    assert {path: names for path, names in findings.items() if names} == {}
