"""Phase 1 smoke tests: the app boots, wires blueprints, and honors the core."""
from infrared import create_app


def _client(core="mmap"):
    app = create_app(core=core)
    app.testing = True
    return app.test_client()


def test_index_renders_with_core():
    resp = _client("mmap").get("/")
    assert resp.status_code == 200
    assert b"Infrared (Flask)" in resp.data
    assert b"mmap" in resp.data


def test_healthz_reports_core():
    resp = _client("ggm").get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok", "core": "ggm"}


def test_core_defaults_to_none_when_unset():
    resp = _client(core="").get("/healthz")
    assert resp.get_json()["core"] is None
