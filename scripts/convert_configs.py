#!/usr/bin/env python
"""Convert the legacy ``configs/config-*.py`` profiles to ``configs/*.toml``.

Faithful, verbatim conversion: views keep their order and any duplicate
(solr, label) entries. Nothing is rewritten. Entries that look like artifacts
of the old autosuggest `_s`->`_txt` hack are left as-is but tagged with a
``# FIXME`` comment so they're easy to find and clean by hand.

Run from anywhere:  python scripts/convert_configs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

CONFIGS = Path(__file__).resolve().parents[1] / "configs"
VIEW_ORDER = ["SEARCH", "FACETS", "LIST", "TABLE", "GALLERY", "FULL"]


def load_old(path: Path):
    ns: dict = {}
    exec(compile(path.read_text(), str(path), "exec"), ns)
    return ns["parmz"], ns["FIELD_DEFINITIONS"]


def tstr(value) -> str:
    s = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def suspicious(solr: str) -> list[str]:
    notes = []
    if "?" in solr:
        notes.append("'?' in field name")
    body = solr
    for suf in ("_txt", "_ss", "_s"):
        if body.endswith(suf):
            body = body[: -len(suf)]
            break
    if "_txt" in body:
        notes.append("interior '_txt' (old autosuggest cruft?)")
    return notes


def emit(parmz, field_defs, core: str) -> tuple[str, int]:
    g = lambda name, default=None: getattr(parmz, name, default)
    out: list[str] = []
    out.append(f"# Converted verbatim from config-{core}.py — review any FIXME lines.")
    out.append("")

    out.append("[site]")
    out.append(f"title = {tstr(g('TITLE', ''))}")
    out.append(f"banner = {tstr(g('BANNER', ''))}")
    if g("CITATION"):
        out.append(f"citation = {tstr(g('CITATION'))}")
    if g("LOGO"):
        out.append(f"logo = {tstr(g('LOGO'))}")
    if g("BANNER_COLOR"):
        out.append(f"banner_color = {tstr(g('BANNER_COLOR'))}")
    if g("SECONDARY_COLOR"):
        out.append(f"secondary_color = {tstr(g('SECONDARY_COLOR'))}")
    if g("NAVBAR"):
        out.append(f"navbar = {tstr(g('NAVBAR'))}")
    out.append("")

    out.append("[solr]")
    out.append(f"server = {tstr(g('SOLR_SERVER', 'http://localhost:8983'))}")
    out.append(f"core = {tstr(g('SOLR_CORE', ''))}")
    out.append(f"facet_limit = {int(g('FACET_LIMIT', 100))}")
    out.append(f"facet_mincount = {int(g('FACET_MINCOUNT', 2))}")
    out.append("")

    out.append("[display]")
    per_page = g("ROW_LIMITS", [100, 500, 1000])
    out.append(f"per_page = [{', '.join(str(int(x)) for x in per_page)}]")
    out.append(f"title_field = {tstr(g('TITLE_FIELD', ''))}")
    if g("IMAGE_FIELD"):
        out.append(f"image_field = {tstr(g('IMAGE_FIELD'))}")
    if g("IMAGE_PREFIX"):
        out.append(f"image_prefix = {tstr(g('IMAGE_PREFIX'))}")
    layouts = g("LAYOUTS", [])
    if layouts:
        out.append(f"layouts = [{', '.join(tstr(x.lower()) for x in layouts)}]")
    out.append("")

    out.append("[views]")
    flagged = 0
    for view in VIEW_ORDER:
        if view not in field_defs:
            continue
        out.append(f"{view.lower()} = [")
        for label, solr in field_defs[view]:
            notes = suspicious(solr)
            if notes:
                flagged += 1
                out.append(f"  # FIXME: {'; '.join(notes)}")
            out.append(f"  {{ solr = {tstr(solr)}, label = {tstr(label)} }},")
        out.append("]")
    out.append("")

    return "\n".join(out), flagged


def main() -> int:
    files = sorted(CONFIGS.glob("config-*.py"))
    if not files:
        print(f"no config-*.py found in {CONFIGS}", file=sys.stderr)
        return 1
    for path in files:
        core = path.stem[len("config-"):]
        parmz, field_defs = load_old(path)
        toml, flagged = emit(parmz, field_defs, core)
        out_path = CONFIGS / f"{core}.toml"
        out_path.write_text(toml, encoding="utf-8")
        n = sum(len(field_defs[v]) for v in field_defs)
        flag = f", {flagged} FIXME" if flagged else ""
        print(f"  config-{core}.py -> {out_path.name:24} ({n} entries{flag})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
