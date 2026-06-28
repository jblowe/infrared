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


def test_with_term_adds_filter_and_resets_page():
    req = SearchRequest(terms=[("city_s", "Patan")], page=4, per_page=20, view="table")
    qs = parse_qs(req.with_term("year_s", "2010"))
    assert qs["city_s"] == ["Patan"]
    assert qs["year_s"] == ["2010"]
    assert qs["page"] == ["1"]  # adding a facet returns to the first page
    assert qs["view"] == ["table"]  # display mode is preserved


def test_with_term_is_idempotent():
    req = SearchRequest(terms=[("city_s", "Patan")])
    once = parse_qs(req.with_term("city_s", "Patan"))
    assert once["city_s"] == ["Patan"]  # not duplicated


def test_without_term_removes_only_that_filter():
    req = SearchRequest(terms=[("city_s", "Patan"), ("year_s", "2010")], page=2)
    qs = parse_qs(req.without_term("city_s", "Patan"))
    assert "city_s" not in qs
    assert qs["year_s"] == ["2010"]
    assert qs["page"] == ["1"]


def test_is_active():
    req = SearchRequest(terms=[("city_s", "Patan")])
    assert req.is_active("city_s", "Patan")
    assert not req.is_active("city_s", "Kathmandu")


def test_sort_parsed_and_carried_in_links():
    req = SearchRequest.from_params([("city_s", "Patan"), ("sort", "year_s asc")])
    assert req.sort == "year_s asc"
    qs = parse_qs(req.query_string())
    assert qs["sort"] == ["year_s asc"]
    # sort persists when adding a facet
    assert parse_qs(req.with_term("year_s", "2010"))["sort"] == ["year_s asc"]


def test_no_sort_keeps_links_clean():
    req = SearchRequest(terms=[("city_s", "Patan")])
    assert "sort=" not in req.query_string()
    # clearing sort via override drops it from the link
    req2 = SearchRequest(sort="year_s asc")
    assert "sort=" not in req2.query_string(sort="")
