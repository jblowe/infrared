"""Small Jinja helpers for rendering Solr values (which may be multivalued)."""
from __future__ import annotations


def solrval(value) -> str:
    """Render a Solr field value as a string; join multivalued fields."""
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value)
    return str(value)


def as_list(value) -> list:
    """Normalize a scalar-or-list Solr value to a list (for thumbnails, etc.)."""
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]
