"""Repository tests: pure unit tests + a Solr-gated integration test."""
import urllib.request

import pytest

from infrared.config.loader import load_collection
from infrared.search.repository import SolrRepository, solr_escape
from infrared.search.request import SearchRequest


# --- pure unit tests (no Solr) ---------------------------------------------

def test_solr_escape_special_chars():
    assert solr_escape('a:b') == 'a\\:b'
    assert solr_escape('he said "hi"') == 'he said \\"hi\\"'
    assert solr_escape('plain') == 'plain'


def test_filter_queries_skip_match_all():
    col = load_collection("ggm")
    repo = SolrRepository(col)
    fq = repo._filter_queries([("*", "*"), ("city_s", "Patan"), ("year_s", "*")])
    assert fq == ['city_s:"Patan"']


def test_build_facets_pairs_and_filters_zero():
    col = load_collection("ggm")
    repo = SolrRepository(col)
    raw = {"facet_fields": {"city_s": ["Patan", 10, "Kathmandu", 0, "Bhaktapur", 3]}}
    facets = repo._build_facets(raw)
    assert len(facets) == 1
    assert facets[0].field == "city_s"
    assert facets[0].label == "City"
    assert facets[0].values == [("Patan", 10), ("Bhaktapur", 3)]


# --- integration (skipped unless Solr is reachable) ------------------------

def _solr_up() -> bool:
    try:
        urllib.request.urlopen("http://localhost:8983/solr/admin/cores?wt=json", timeout=3)
        return True
    except Exception:
        return False


solr = pytest.mark.skipif(not _solr_up(), reason="Solr not reachable on :8983")


@solr
def test_live_search_ggm():
    repo = SolrRepository(load_collection("ggm"))
    resp = repo.search(SearchRequest(per_page=5, view="list"))
    assert resp.ok and not resp.errors
    assert resp.total > 0
    assert len(resp.documents) == 5
    assert all("id" in doc for doc in resp.documents)
    assert resp.facets, "expected at least one facet"


@solr
def test_live_facet_filter_narrows_results():
    repo = SolrRepository(load_collection("ggm"))
    everything = repo.search(SearchRequest(per_page=1))
    filtered = repo.search(SearchRequest(terms=[("city_s", "Patan")], per_page=1))
    assert 0 < filtered.total <= everything.total
