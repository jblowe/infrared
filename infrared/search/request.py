"""SearchRequest: the parsed search inputs (filters + paging + display mode).

Replaces the old ``parameters``/``controls`` dicts and the manual ``parse_qsl``
juggling. It parses query parameters into ``terms`` (field/value constraints)
plus the display ``controls``, and can rebuild its own query string for links.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlencode

# query-param names that are controls rather than field constraints
CONTROL_KEYS = ("page", "per_page", "view")


def _int(value, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@dataclass
class SearchRequest:
    terms: list[tuple[str, str]] = field(default_factory=list)
    page: int = 1
    per_page: int = 20
    view: str = "list"

    @classmethod
    def from_params(cls, pairs, *, default_view: str = "list", default_per_page: int = 20):
        """Build from an iterable of (key, value) pairs (order preserved)."""
        terms: list[tuple[str, str]] = []
        page, per_page, view = 1, default_per_page, default_view
        search_field = search_value = None

        for key, value in pairs:
            if key == "page":
                page = _int(value, 1)
            elif key == "per_page":
                per_page = _int(value, default_per_page)
            elif key == "view":
                view = value or default_view
            elif key == "search_field":
                search_field = value
            elif key == "search_value":
                search_value = value
            elif key == "query_string":
                continue  # legacy no-op
            else:
                terms.append((key, value))

        if search_field:
            terms.append((search_field, search_value or "*"))

        return cls(terms=terms, page=max(page, 1), per_page=per_page, view=view)

    @classmethod
    def from_request(cls, req, **kwargs):
        """Build from a Flask/Werkzeug request (uses ``request.args``)."""
        return cls.from_params(req.args.items(multi=True), **kwargs)

    @property
    def start(self) -> int:
        return (self.page - 1) * self.per_page

    def _qs(self, terms, **controls) -> str:
        merged = {"view": self.view, "per_page": self.per_page, "page": self.page}
        merged.update(controls)
        return urlencode(list(terms) + list(merged.items()))

    def query_string(self, **overrides) -> str:
        """Same terms, optionally changed controls (paging, view toggle)."""
        return self._qs(self.terms, **overrides)

    def with_term(self, field: str, value: str) -> str:
        """Query string with (field, value) added as a filter; resets to page 1."""
        terms = self.terms if (field, value) in self.terms else self.terms + [(field, value)]
        return self._qs(terms, page=1)

    def without_term(self, field: str, value: str) -> str:
        """Query string with (field, value) removed; resets to page 1."""
        return self._qs([t for t in self.terms if t != (field, value)], page=1)

    def is_active(self, field: str, value: str) -> bool:
        return (field, value) in self.terms
