"""Schema migration 21: pending Reader Kernel overrides need regeneration."""

SQL = r"""
ALTER TABLE original_states
ADD COLUMN reader_kernel_overrides_need_regeneration INTEGER NOT NULL DEFAULT 0;
"""

__all__ = ["SQL"]
