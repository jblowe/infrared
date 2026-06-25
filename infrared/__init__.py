"""Infrared — a configurable Solr discovery UI (Flask).

The active Solr core is chosen at deploy time via the ``INFRARED_CORE``
environment variable (e.g. ``INFRARED_CORE=mmap`` selects ``configs/mmap.toml``).
One app serves any core; switching cores requires no code change.
"""
from __future__ import annotations

import os

from flask import Flask

__all__ = ["create_app"]


def create_app(core: str | None = None) -> Flask:
    """Application factory.

    :param core: name of the collection profile to load. Falls back to the
        ``INFRARED_CORE`` environment variable. Tests pass it explicitly.
    """
    core = core or os.environ.get("INFRARED_CORE", "")

    app = Flask(__name__)
    app.config["INFRARED_CORE"] = core

    from .config.loader import load_collection

    collection = load_collection(core) if core else None
    app.config["COLLECTION"] = collection

    @app.context_processor
    def _inject_collection():
        return {
            "collection": collection,
            "site": collection.site if collection else None,
        }

    from .views.catalog import bp as catalog_bp
    from .views.suggest import bp as suggest_bp

    app.register_blueprint(catalog_bp)
    app.register_blueprint(suggest_bp)

    return app
