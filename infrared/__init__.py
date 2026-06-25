"""Infrared — a configurable Solr discovery UI (Flask).

The active Solr core is chosen at deploy time via the ``INFRARED_CORE``
environment variable (e.g. ``INFRARED_CORE=mmap`` selects ``configs/mmap.toml``).
One app serves any core; switching cores requires no code change.
"""
from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, send_from_directory

from .templating import as_list, solrval

__all__ = ["create_app"]


def create_app(core: str | None = None) -> Flask:
    """Application factory.

    :param core: name of the collection profile to load. Falls back to the
        ``INFRARED_CORE`` environment variable. Tests pass it explicitly.
    """
    core = core or os.environ.get("INFRARED_CORE", "")

    app = Flask(__name__)
    app.config["INFRARED_CORE"] = core
    app.jinja_env.filters["solrval"] = solrval
    app.jinja_env.filters["as_list"] = as_list

    from .config.loader import load_collection

    collection = load_collection(core) if core else None
    app.config["COLLECTION"] = collection

    repository = None
    if collection is not None:
        from .search.repository import SolrRepository

        repository = SolrRepository(collection)
    app.config["REPOSITORY"] = repository

    @app.context_processor
    def _inject_collection():
        return {
            "collection": collection,
            "site": collection.site if collection else None,
        }

    # Serve per-core images locally in development (Apache handles this in prod).
    if collection is not None and collection.display.image_prefix:
        prefix = "/" + collection.display.image_prefix.strip("/")
        image_dir = Path(__file__).resolve().parents[1] / prefix.strip("/")

        @app.route(f"{prefix}/<path:filename>")
        def collection_images(filename):
            return send_from_directory(image_dir, filename)

    from .views.catalog import bp as catalog_bp
    from .views.suggest import bp as suggest_bp

    app.register_blueprint(catalog_bp)
    app.register_blueprint(suggest_bp)

    return app
