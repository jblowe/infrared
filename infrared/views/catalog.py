"""Catalog blueprint: search, record display, health check."""
from __future__ import annotations

from pathlib import Path

from flask import Blueprint, abort, current_app, g, render_template, request
from markupsafe import Markup

from ..search.request import SearchRequest

bp = Blueprint("catalog", __name__)

DISPLAY_MODES = ("list", "table", "gallery", "full")


def _collection():
    """Collection for the current request (resolved by Host in before_request)."""
    return g.get("collection")


def _about_html() -> Markup:
    """Per-core About content: about/<core>.html, else about/default.html.

    Plain static HTML fragments (no templating) — easy to hand-edit per core,
    living next to configs/<core>.toml. Returns empty if neither file exists.
    """
    core = g.get("core") or ""
    about_dir = Path(current_app.config["REPO_ROOT"]) / "about"
    for name in (f"{core}.html", "default.html"):
        path = about_dir / name
        if path.is_file():
            return Markup(path.read_text(encoding="utf-8"))
    return Markup("")


def _repository():
    repo = g.get("repository")
    if repo is None:
        abort(503, "no collection configured for this host (set INFRARED_CORE or INFRARED_SITES)")
    return repo


def _display_modes(collection) -> list[str]:
    modes = [m for m in collection.display.layouts if m in DISPLAY_MODES]
    return modes or ["list"]


def _defaults(collection):
    modes = _display_modes(collection)
    view = "list" if "list" in modes else modes[0]
    per_page = collection.display.per_page[0] if collection.display.per_page else 100
    return view, per_page


def _render_search(collection, *, show_about: bool):
    """Render the search shell. The content pane shows the About panel on the
    landing page / About link, and results once a search is under way. The Solr
    query still runs so the facets are populated in either case."""
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
        show_sidebar_toggle=True,
        show_about=show_about,
        about_html=_about_html() if show_about else None,
    )


@bp.get("/")
@bp.get("/search")
def search():
    collection = _collection()
    if collection is None:
        return render_template("index.html", core=g.get("core") or "(none)")
    # The start page (no query yet) shows About in the content pane.
    return _render_search(collection, show_about=not request.args)


@bp.get("/about")
def about():
    collection = _collection()
    if collection is None:
        return render_template("about.html", about_html=_about_html())
    return _render_search(collection, show_about=True)


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
    return {"status": "ok", "core": g.get("core") or None}
