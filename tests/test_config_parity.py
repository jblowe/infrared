"""Parity: every generated TOML reproduces its source config-*.py exactly."""
from pathlib import Path

import pytest

from infrared.config.loader import load_collection

CONFIGS = Path(__file__).resolve().parents[1] / "configs"
VIEW_MAP = {
    "SEARCH": "search",
    "FACETS": "facets",
    "LIST": "list",
    "TABLE": "table",
    "GALLERY": "gallery",
    "FULL": "full",
}
CORES = sorted(p.stem[len("config-"):] for p in CONFIGS.glob("config-*.py"))


def _old(core):
    ns = {}
    src = (CONFIGS / f"config-{core}.py").read_text()
    exec(compile(src, f"config-{core}.py", "exec"), ns)
    return ns["parmz"], ns["FIELD_DEFINITIONS"]


@pytest.mark.parametrize("core", CORES)
def test_views_match_old_config(core):
    parmz, field_defs = _old(core)
    col = load_collection(core)
    for old_name, new_name in VIEW_MAP.items():
        expected = [(label, solr) for label, solr in field_defs.get(old_name, [])]
        got = [(e.label, e.solr) for e in col.views.get(new_name, [])]
        assert got == expected, f"{core}.{new_name} differs from {old_name}"


@pytest.mark.parametrize("core", CORES)
def test_scalars_match_old_config(core):
    parmz, _ = _old(core)
    col = load_collection(core)
    assert col.site.title == parmz.TITLE
    assert col.site.banner == parmz.BANNER
    assert col.solr.core == parmz.SOLR_CORE
    assert col.solr.facet_limit == parmz.FACET_LIMIT
    assert col.display.title_field == parmz.TITLE_FIELD
    assert col.display.image_field == getattr(parmz, "IMAGE_FIELD", None)
