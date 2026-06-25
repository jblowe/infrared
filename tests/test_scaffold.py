"""Phase 1 smoke tests: the app boots, wires blueprints, and honors the core."""
from infrared import create_app


def _client(core="mmap"):
    app = create_app(core=core)
    app.testing = True
    return app.test_client()


def test_index_renders_search_page_with_core():
    # "/" now renders the search page; the collection banner proves the
    # profile loaded and themed the page (renders 200 even if Solr is down).
    resp = _client("mmap").get("/")
    assert resp.status_code == 200
    assert b"Middle Mekong Archaeology Project" in resp.data


def test_healthz_reports_core():
    resp = _client("ggm").get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok", "core": "ggm"}


def test_core_defaults_to_none_when_unset():
    resp = _client(core="").get("/healthz")
    assert resp.get_json()["core"] is None
