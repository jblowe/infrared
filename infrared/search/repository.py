"""SolrRepository — the one place that talks to Solr (via pysolr).

Query values are escaped, not f-string-interpolated, so user input can't break
out of the query (the old ``{q[0]}:"{q[1]}"`` was injection-fragile). Facet
selections are applied as filter queries (``fq``); the main query stays ``*:*``.
"""
from __future__ import annotations

import pysolr

from ..config.models import Collection
from .request import SearchRequest
from .response import Facet, SearchResponse

# Lucene/Solr query-syntax characters that must be escaped inside a term value.
_SPECIAL = set('+-&|!(){}[]^"~*?:\\/')


def solr_escape(value: str) -> str:
    return "".join("\\" + ch if ch in _SPECIAL else ch for ch in str(value))


class SolrRepository:
    def __init__(self, collection: Collection, *, timeout: int = 10):
        self.collection = collection
        url = f"{collection.solr.server}/solr/{collection.solr.core}"
        self.client = pysolr.Solr(url, timeout=timeout)

    # --- query construction -------------------------------------------------

    def _result_fields(self, view: str) -> list[str]:
        entries = self.collection.view(view) or self.collection.view("list")
        fields = {e.solr for e in entries}
        fields.add("id")
        if self.collection.display.title_field:
            fields.add(self.collection.display.title_field)
        if self.collection.display.image_field:
            fields.add(self.collection.display.image_field)
        return sorted(fields)

    def _filter_queries(self, terms) -> list[str]:
        fq = []
        for field_name, value in terms:
            if field_name == "*" or value in ("", "*"):
                continue
            fq.append(f'{field_name}:"{solr_escape(value)}"')
        return fq

    def _build_facets(self, raw: dict) -> list[Facet]:
        labels = self.collection.facet_labels
        out: list[Facet] = []
        for field_name, flat in (raw or {}).get("facet_fields", {}).items():
            values = [
                (flat[i], flat[i + 1])
                for i in range(0, len(flat), 2)
                if flat[i + 1]
            ]
            if values:
                out.append(
                    Facet(field=field_name, label=labels.get(field_name, field_name), values=values)
                )
        return out

    # --- public API ---------------------------------------------------------

    def search(self, request: SearchRequest) -> SearchResponse:
        params = {
            "rows": request.per_page,
            "start": request.start,
            "fl": ",".join(self._result_fields(request.view)),
            "facet": "true",
            "facet.field": [e.solr for e in self.collection.facets],
            "facet.limit": self.collection.solr.facet_limit,
            "facet.mincount": self.collection.solr.facet_mincount,
        }
        fq = self._filter_queries(request.terms)
        if fq:
            params["fq"] = fq
        try:
            result = self.client.search("*:*", **params)
        except Exception as exc:  # network/Solr errors surface as response errors
            return SearchResponse(request=request, errors=[str(exc)])
        return SearchResponse(
            request=request,
            documents=list(result.docs),
            total=result.hits,
            facets=self._build_facets(result.facets),
        )

    def get(self, doc_id: str) -> dict | None:
        try:
            result = self.client.search(f'id:"{solr_escape(doc_id)}"', rows=1, fl="*")
        except Exception:
            return None
        docs = list(result.docs)
        return docs[0] if docs else None
