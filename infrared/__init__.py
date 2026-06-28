"""Infrared — a configurable Solr discovery UI (Flask).

Two serving modes, chosen at startup:

* **Single-tenant** — one core for the whole process, via ``INFRARED_CORE``
  (e.g. ``INFRARED_CORE=mmap``) or ``create_app(core="mmap")``. This is the
  mod_wsgi / one-app-per-vhost model.
* **Multi-tenant** — one process serves many cores, picked per request from the
  ``Host`` header. Enable it with ``INFRARED_SITES`` pointing at a sites TOML
  (host→core map, see ``configs/sites.toml``) or ``create_app(sites={...})``.
  This is the containerized model: one app behind a reverse proxy.

Either way, switching/adding cores requires no code change.
"""
from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, g, request, send_from_directory

from .templating import as_list, contrast_color, solrval

__all__ = ["create_app"]


def _footer_info(repo_root: Path) -> str:
    """Version + start time for the footer (replaces utils.add_time_and_version)."""
    from datetime import datetime

    version_file = repo_root / "VERSION"
    version = version_file.read_text().strip() if version_file.exists() else ""
    started = datetime.now().strftime("%Y-%m-%d %H:%M")
    parts = [p for p in (f"v{version}" if version else "", f"started {started}") if p]
    return " · ".join(parts)


def create_app(
    core: str | None = None,
    *,
    sites: dict[str, str] | None = None,
    default_core: str | None = None,
) -> Flask:
    """Application factory.

    :param core: single-tenant core name. Falls back to ``INFRARED_CORE``.
    :param sites: multi-tenant host→core map. Falls back to the ``INFRARED_SITES``
        file when *core* is unset.
    :param default_core: core used when a request Host matches no site.
    """
    core = core or os.environ.get("INFRARED_CORE", "")
    repo_root = Path(__file__).resolve().parents[1]

    # Serve the bundled assets (Bootstrap, jQuery, FontAwesome, etc.) locally so
    # the app works with no internet connection. FontAwesome's all.min.css
    # references ../webfonts, which resolves under /static/webfonts/.
    app = Flask(
        __name__,
        static_folder=str(repo_root / "static"),
        static_url_path="/static",
    )
    app.config["REPO_ROOT"] = str(repo_root)
    app.jinja_env.filters["solrval"] = solrval
    app.jinja_env.filters["as_list"] = as_list
    app.jinja_env.filters["contrast_color"] = contrast_color

    footer_info = _footer_info(repo_root)

    from .config.loader import load_collection, load_sites

    # --- resolve tenancy: a single core, or a host->core map ----------------
    sites_map: dict[str, str] = {}
    if core:
        default_core = core
    else:
        if sites is not None:
            sites_map = {str(h).lower(): str(c) for h, c in sites.items()}
        elif os.environ.get("INFRARED_SITES"):
            sites_map, file_default = load_sites(os.environ["INFRARED_SITES"])
            default_core = default_core or file_default
        default_core = default_core or os.environ.get("INFRARED_DEFAULT_CORE") or None

    needed = {core} if core else set(sites_map.values())
    if default_core:
        needed.add(default_core)

    from .search.repository import SolrRepository

    collections = {c: load_collection(c) for c in sorted(needed)}
    repositories = {c: SolrRepository(col) for c, col in collections.items()}

    app.config["COLLECTIONS"] = collections
    app.config["REPOSITORIES"] = repositories
    app.config["SITES"] = sites_map
    app.config["DEFAULT_CORE"] = default_core
    app.config["INFRARED_CORE"] = core or default_core or ""

    @app.before_request
    def _resolve_tenant():
        host = (request.host or "").split(":")[0].lower()
        resolved = sites_map.get(host) or default_core
        g.core = resolved
        g.collection = collections.get(resolved) if resolved else None
        g.repository = repositories.get(resolved) if resolved else None

    @app.context_processor
    def _inject_collection():
        col = g.get("collection")
        return {
            "collection": col,
            "site": col.site if col else None,
            "footer_info": footer_info,
            "show_sidebar_toggle": False,  # search page overrides this to True
        }

    # Dev convenience: serve per-core images locally (Caddy/Apache do this in
    # production). One route per distinct image_prefix; the on-disk directory is
    # named by the prefix, so it is host-independent.
    prefixes = {
        "/" + c.display.image_prefix.strip("/")
        for c in collections.values()
        if c.display.image_prefix
    }
    for prefix in prefixes:
        image_dir = repo_root / prefix.strip("/")
        endpoint = "images_" + prefix.strip("/").replace("/", "_").replace("-", "_")
        app.add_url_rule(
            f"{prefix}/<path:filename>",
            endpoint=endpoint,
            view_func=lambda filename, _dir=image_dir: send_from_directory(_dir, filename),
        )

    from .views.catalog import bp as catalog_bp
    from .views.suggest import bp as suggest_bp

    app.register_blueprint(catalog_bp)
    app.register_blueprint(suggest_bp)

    return app
