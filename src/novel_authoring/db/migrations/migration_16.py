"""Schema migration 16: frozen PWK planning context."""

SQL = r"""
ALTER TABLE planning_aggregates
ADD COLUMN kernel_context_json TEXT NOT NULL DEFAULT 'null';
"""

__all__ = ["SQL"]
