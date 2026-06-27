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


# A few CSS color names the configs actually use; everything else falls back to
# white text (safe on the strong banner colors). Keeps the theme per-core.
_NAMED_COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
}


def _rgb(color: str):
    color = (color or "").strip().lower()
    if color in _NAMED_COLORS:
        return _NAMED_COLORS[color]
    if color.startswith("#"):
        hex_part = color[1:]
        if len(hex_part) == 3:
            hex_part = "".join(ch * 2 for ch in hex_part)
        if len(hex_part) == 6:
            try:
                return tuple(int(hex_part[i : i + 2], 16) for i in (0, 2, 4))
            except ValueError:
                return None
    return None


def contrast_color(color: str) -> str:
    """Return black or white — whichever is readable on ``color``.

    Used to pick legible text for per-core themed buttons (e.g. dark text on
    mmap's pale banner, white text on tap's red).
    """
    rgb = _rgb(color)
    if rgb is None:
        return "#ffffff"
    r, g, b = rgb
    # Perceived luminance (ITU-R BT.601).
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#000000" if luminance > 0.6 else "#ffffff"
