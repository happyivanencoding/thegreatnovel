"""Schema migration 19: confirmed ORIGINAL creative semantics authority."""

SQL = r"""
ALTER TABLE original_states ADD COLUMN confirmed_creative_semantics_json TEXT;
"""

__all__ = ["SQL"]
