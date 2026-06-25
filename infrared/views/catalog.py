"""Catalog blueprint: search and record browsing.

Phase 1 provides a boot/health check only. Phase 4 adds:
    GET /            home / empty search
    GET /search      faceted search
    GET /record/<id> single record
"""
from __future__ import annotations

from flask import Blueprint, current_app, render_template

bp = Blueprint("catalog", __name__)


@bp.get("/")
def index():
    return render_template(
        "index.html",
        core=current_app.config.get("INFRARED_CORE") or "(none)",
    )


@bp.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "core": current_app.config.get("INFRARED_CORE") or None,
    }
