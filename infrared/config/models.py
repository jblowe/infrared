"""Collection configuration model (pydantic v2).

A collection profile is plain data: branding, Solr coordinates, display
defaults, and a set of *views*. A view is an ordered list of ``{solr, label}``
entries — order is UI order, and duplication across views is fine. There is no
field registry; whatever Solr field a view names is what it uses.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator

# Canonical view names. SEARCH = search-box fields, FACETS = sidebar facets,
# LIST/TABLE/GALLERY/FULL = result display modes.
VIEW_NAMES = ("search", "facets", "list", "table", "gallery", "full")


class ViewEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    solr: str
    label: str


class Site(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    banner: str = ""
    citation: str = ""
    logo: str = ""
    banner_color: str = ""
    secondary_color: str = ""
    navbar: str = "navbar-light"


class Solr(BaseModel):
    model_config = ConfigDict(extra="forbid")

    server: str = "http://localhost:8983"
    core: str
    facet_limit: int = 100
    facet_mincount: int = 2


class Display(BaseModel):
    model_config = ConfigDict(extra="forbid")

    row_limits: list[int] = [10, 20, 30]
    title_field: str
    image_field: str | None = None
    image_prefix: str = ""
    layouts: list[str] = []


class Collection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site: Site
    solr: Solr
    display: Display
    views: dict[str, list[ViewEntry]]

    @field_validator("views")
    @classmethod
    def _known_view_names(cls, v: dict) -> dict:
        bad = [k for k in v if k not in VIEW_NAMES]
        if bad:
            raise ValueError(
                f"unknown view name(s) {sorted(bad)}; allowed: {list(VIEW_NAMES)}"
            )
        return v

    # --- convenience accessors used by routes/templates ---

    def view(self, name: str) -> list[ViewEntry]:
        return self.views.get(name, [])

    @property
    def facets(self) -> list[ViewEntry]:
        return self.views.get("facets", [])

    @property
    def facet_labels(self) -> dict[str, str]:
        """solr field -> label, for rendering facet headings."""
        return {e.solr: e.label for e in self.views.get("facets", [])}

    @property
    def labels(self) -> dict[str, str]:
        """solr field -> label across all views (facets/search win), for breadcrumbs."""
        out: dict[str, str] = {}
        for name in VIEW_NAMES:
            for entry in self.views.get(name, []):
                out.setdefault(entry.solr, entry.label)
        return out
