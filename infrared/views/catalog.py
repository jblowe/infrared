"""Catalog blueprint: search, record display, health check."""
from __future__ import annotations

from flask import Blueprint, abort, current_app, render_template, request

from ..search.request import SearchRequest

bp = Blueprint("catalog", __name__)

DISPLAY_MODES = ("list", "table", "gallery", "full")


def _collection():
    return current_app.config.get("COLLECTION")


def _repository():
    repo = current_app.config.get("REPOSITORY")
    if repo is None:
        abort(503, "no collection configured (set INFRARED_CORE)")
    return repo


def _display_modes(collection) -> list[str]:
    modes = [m for m in collection.display.layouts if m in DISPLAY_MODES]
    return modes or ["list"]


def _defaults(collection):
    modes = _display_modes(collection)
    view = "list" if "list" in modes else modes[0]
    per_page = collection.display.row_limits[0] if collection.display.row_limits else 20
    return view, per_page


@bp.get("/")
@bp.get("/search")
def search():
    collection = _collection()
    if collection is None:
        return render_template(
            "index.html", core=current_app.config.get("INFRARED_CORE") or "(none)"
        )
    default_view, default_per_page = _defaults(collection)
    sreq = SearchRequest.from_request(
        request, default_view=default_view, default_per_page=default_per_page
    )
    response = _repository().search(sreq)
    return render_template(
        "search.html",
        response=response,
        sreq=sreq,
        display_modes=_display_modes(collection),
    )


@bp.get("/record/<path:doc_id>")
def record(doc_id):
    if _collection() is None:
        abort(503)
    document = _repository().get(doc_id)
    if document is None:
        abort(404)
    return render_template("record.html", document=document)


@bp.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "core": current_app.config.get("INFRARED_CORE") or None,
    }
