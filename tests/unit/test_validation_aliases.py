from novel_authoring.validation.aliases import resolve_projection_alias


def test_projection_alias_resolves_unique_alias_and_exact_id() -> None:
    collection = {
        "resource-1": {"name": "边界钥匙", "aliases": ["旧钥匙"]},
        "resource-2": {"name": "维修材料", "aliases": []},
    }

    assert resolve_projection_alias(collection, "resource-1").status == "EXACT"
    resolved = resolve_projection_alias(collection, "旧钥匙")
    assert resolved.status == "UNIQUE_ALIAS"
    assert resolved.canonical_id == "resource-1"


def test_projection_alias_distinguishes_missing_ambiguous_and_conflict() -> None:
    collection = {
        "resource-1": {"name": "钥匙甲", "aliases": ["钥匙"]},
        "resource-2": {"name": "钥匙乙", "aliases": ["钥匙"]},
        "钥匙": {"name": "另一条正史记录", "aliases": []},
    }

    assert resolve_projection_alias(collection, "不存在").status == "NOT_FOUND"
    assert resolve_projection_alias(collection, "钥匙").status == "CONFLICT"
    ambiguous = resolve_projection_alias(
        {
            "resource-1": {"name": "钥匙甲", "aliases": ["通称"]},
            "resource-2": {"name": "钥匙乙", "aliases": ["通称"]},
        },
        "通称",
    )
    assert ambiguous.status == "AMBIGUOUS"
