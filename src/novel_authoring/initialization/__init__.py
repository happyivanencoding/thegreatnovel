"""Existing-novel initialization contracts and deterministic file workflow."""

from novel_authoring.initialization.metrics import (
    ChapterMetricBootstrapRecord,
    InitializationMetricBootstrapManifest,
    MetricBootstrapImportReport,
    import_metric_bootstrap,
    metric_bootstrap_status,
    prepare_metric_bootstrap,
    rebuild_initialization_metric_runs,
)
from novel_authoring.initialization.service import (
    InitializationDepth,
    InitializationError,
    InitializationState,
    calculate_source_coverage,
    create_initialization,
    initialization_root,
    latest_initialization,
    prepare_action_deepening,
    refresh_initialization,
    upgrade_initialization,
)

__all__ = [
    "InitializationError",
    "InitializationDepth",
    "InitializationState",
    "calculate_source_coverage",
    "create_initialization",
    "initialization_root",
    "latest_initialization",
    "prepare_action_deepening",
    "refresh_initialization",
    "upgrade_initialization",
    "ChapterMetricBootstrapRecord",
    "InitializationMetricBootstrapManifest",
    "MetricBootstrapImportReport",
    "import_metric_bootstrap",
    "metric_bootstrap_status",
    "prepare_metric_bootstrap",
    "rebuild_initialization_metric_runs",
]
