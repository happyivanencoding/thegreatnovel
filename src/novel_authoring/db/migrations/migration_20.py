"""Schema migration 20: pending ORIGINAL Reader Kernel author overrides."""

SQL = r"""
ALTER TABLE original_states ADD COLUMN reader_kernel_author_overrides_json TEXT;
ALTER TABLE original_states ADD COLUMN reader_kernel_author_instruction TEXT NOT NULL DEFAULT '';
"""

__all__ = ["SQL"]
