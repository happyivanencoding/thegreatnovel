"""Compilation of author-confirmed custom progression grammars."""

from novel_authoring.progression.models import (
    DerivedAdapterSpec,
    GenreAdapter,
    GenreAdapterKind,
)


def compile_derived_adapter(spec: DerivedAdapterSpec) -> GenreAdapter:
    """Translate a derived specification without classifying it as a known trope."""

    return GenreAdapter(
        adapter_id=GenreAdapterKind.CUSTOM,
        label=f"自定义成长：{spec.growth_object}",
        capabilities=spec.capabilities,
        expected_payoff_channels=spec.payoff_channels,
        genre_native_scene_types=spec.verification_modes,
        genre_native_resource_types=spec.growth_resources,
        genre_native_conflicts=spec.growth_costs,
        drift_risks=[
            "不得把作者确认的原创成长语法替换为已有 Adapter 的表层套路",
        ],
    )


__all__ = ["compile_derived_adapter"]
