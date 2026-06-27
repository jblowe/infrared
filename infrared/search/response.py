"""SearchResponse and friends — the typed result object the templates consume.

This is the replacement for the old untyped ``data`` dict: results, facets,
paging, and errors as attributes rather than dict keys mutated across layers.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class Facet:
    field: str
    label: str
    values: list[tuple[str, int]]  # (value, count), already filtered/ordered


@dataclass
class Pagination:
    page: int
    per_page: int
    total: int

    @property
    def start(self) -> int:
        return (self.page - 1) * self.per_page

    @property
    def pages(self) -> int:
        return max(1, math.ceil(self.total / self.per_page)) if self.per_page else 1

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    @property
    def has_next(self) -> bool:
        return self.page < self.pages


@dataclass
class SearchResponse:
    request: "object"  # SearchRequest; untyped here to avoid a circular import
    documents: list[dict] = field(default_factory=list)
    total: int = 0
    facets: list[Facet] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def pagination(self) -> Pagination:
        return Pagination(
            page=getattr(self.request, "page", 1),
            per_page=getattr(self.request, "per_page", len(self.documents) or 1),
            total=self.total,
        )

    @property
    def ok(self) -> bool:
        return not self.errors
