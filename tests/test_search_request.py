"""Unit tests for SearchRequest parsing (no Solr needed)."""
from urllib.parse import parse_qs

from infrared.search.request import SearchRequest


def test_terms_and_controls_split():
    req = SearchRequest.from_params(
        [("city_s", "Patan"), ("year_s", "2010"), ("page", "3"), ("view", "table")]
    )
    assert req.terms == [("city_s", "Patan"), ("year_s", "2010")]
    assert req.page == 3
    assert req.view == "table"


def test_defaults_and_start():
    req = SearchRequest.from_params([], default_view="list", default_per_page=20)
    assert req.terms == []
    assert req.page == 1 and req.per_page == 20 and req.view == "list"
    assert req.start == 0
    assert SearchRequest(page=3, per_page=20).start == 40


def test_bad_page_falls_back():
    assert SearchRequest.from_params([("page", "nonsense")]).page == 1


def test_search_field_value_injection():
    req = SearchRequest.from_params(
        [("search_field", "title_txt"), ("search_value", "kirtipur")]
    )
    assert req.terms == [("title_txt", "kirtipur")]


def test_query_string_roundtrips_terms_and_overrides():
    req = SearchRequest(terms=[("city_s", "Patan")], page=1, per_page=20, view="list")
    qs = parse_qs(req.query_string(page=2))
    assert qs["city_s"] == ["Patan"]
    assert qs["page"] == ["2"]
    assert qs["view"] == ["list"]
