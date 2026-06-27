"""Autosuggest blueprint.

Phase 4 adds:
    GET /suggest?q=...&field=...   -> JSON list of facet-derived suggestions
"""
from __future__ import annotations

from flask import Blueprint

bp = Blueprint("suggest", __name__)
