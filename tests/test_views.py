"""Template/route tests for the restored UI features.

These render real templates through a Flask test client. The chrome tests
(nav, search bar, breadcrumbs, local assets, per-core theme) do not need a live
Solr: the search route catches connection errors and still renders the page, so
the surrounding layout is always present. The feature tests that need result
rows are gated on Solr being reachable on :8983.
"""
import urllib.request

import pytest

from infrared import create_app
from infrared.templating import contrast_color


def _client(core="tap"):
    app = create_app(core=core)
    app.testing = True
    return app.test_client()


def _html(path, core="tap"):
    return _client(core).get(path).get_data(as_text=True)


# --- contrast_color (pure unit) --------------------------------------------

def test_contrast_color_dark_bg_gets_white_text():
    assert contrast_color("#A51931") == "#ffffff"  # tap red
    assert contrast_color("black") == "#ffffff"
    assert contrast_color("#002868") == "#ffffff"


def test_contrast_color_light_bg_gets_black_text():
    assert contrast_color("#f9d88d") == "#000000"  # mmap pale yellow
    assert contrast_color("#fff") == "#000000"
    assert contrast_color("white") == "#000000"


def test_contrast_color_unknown_defaults_to_white():
    assert contrast_color("") == "#ffffff"
    assert contrast_color("rebeccapurple") == "#ffffff"  # not a hex/known name


# --- self-contained assets (no CDN) ----------------------------------------

def test_no_external_asset_references():
    # Asset tags (scripts/stylesheets) must be local; content hyperlinks may be
    # external, so target the asset tags specifically.
    html = _html("/")
    assert "jsdelivr" not in html
    assert '<script src="http' not in html
    assert 'stylesheet" href="http' not in html


def test_local_bundles_referenced():
    html = _html("/")
    for ref in (
        "/static/js/jquery.min.js",
        "/static/js/bootstrap.min.js",
        "/static/js/bootstrap-sortable.js",
        "/static/css/bootstrap.min.css",
        "/static/css/all.min.css",
        "/static/css/infrared.css",
    ):
        assert ref in html, ref


def test_static_assets_are_served():
    c = _client()
    for path in (
        "/static/css/bootstrap.min.css",
        "/static/css/all.min.css",
        "/static/js/bootstrap-sortable.js",
        "/static/js/infrared.js",
        "/static/webfonts/fa-solid-900.woff2",
        "/static/images/favicon.ico",
    ):
        assert c.get(path).status_code == 200, path


# --- nav / chrome ----------------------------------------------------------

def test_nav_has_home_about_and_toggle_sidebar():
    html = _html("/")
    assert "fa-home" in html
    assert "fa-info-circle" in html
    assert 'id="toggle_sidebar"' in html


def test_about_page_renders():
    resp = _client().get("/about")
    assert resp.status_code == 200
    assert b"About" in resp.data


def test_landing_shows_about_in_content_pane():
    # The start page shows the About panel inside the result pane, within the
    # normal search shell (searchbar + facets still present).
    html = _html("/")
    assert 'id="about"' in html
    assert 'id="content"' in html
    assert 'name="search_value"' in html


def test_about_link_shows_about_in_content_pane():
    html = _html("/about")
    assert 'id="about"' in html
    assert 'id="content"' in html


def test_about_content_is_per_core():
    tap = _html("/about", core="tap")
    assert "The TAP Finder" in tap

    ggm = _html("/about", core="ggm")
    assert "Maskarinec" in ggm
    assert "The TAP Finder" not in ggm  # no cross-core leakage


def test_about_falls_back_to_default_when_no_core_file():
    # 'marc' has no about/marc.html, so about/default.html is used.
    html = _html("/about", core="marc")
    assert "About this collection" in html


def test_search_with_query_does_not_show_about():
    # Once a search is under way, the content pane shows results, not About.
    html = _html("/search?search_value=foo")
    assert 'id="about"' not in html


def test_start_over_lands_on_results_not_about():
    # Start over carries a view param so it shows the full (*:*) result list,
    # not the About landing — unlike the home/brand links which go to About.
    html = _html("/")
    assert 'id="startover"' in html
    assert "/search?view=" in html  # the Start over href
    assert 'id="about"' not in _html("/search?view=list")


def test_start_over_present_and_clear_all_gone():
    html = _html("/")
    assert 'id="startover"' in html
    assert "Start over" in html
    assert "clear all" not in html


def test_layout_has_leftpane_and_content_ids():
    html = _html("/")
    assert 'id="leftpane"' in html
    assert 'id="content"' in html


def test_searchbar_lists_search_view_fields():
    html = _html("/")
    assert 'name="search_field"' in html
    assert 'name="search_value"' in html
    assert "Record types" in html  # a tap search-view label


# --- per-core theming ------------------------------------------------------

def test_theme_colors_are_per_core():
    tap = _html("/about", core="tap")
    assert "#A51931" in tap  # tap banner color injected into the theme block

    ggm = _html("/about", core="ggm")
    assert "#EC5800" in ggm
    assert "#A51931" not in ggm  # tap's color must not leak into another core


def test_shipped_sites_file_is_valid():
    # The shipped configs/sites.toml must parse and map only to real cores.
    from infrared.config.loader import available_cores, config_dir, load_sites

    sites, default = load_sites(config_dir() / "sites.toml")
    cores = set(available_cores())
    assert default in cores
    assert sites  # non-empty
    for host, core in sites.items():
        assert core in cores, f"{host} → {core} has no configs/{core}.toml"


def test_multitenant_routes_by_host():
    app = create_app(sites={"ggm.test": "ggm", "tap.test": "tap"}, default_core="ggm")
    app.testing = True
    c = app.test_client()

    ggm = c.get("/", headers={"Host": "ggm.test"}).get_data(as_text=True)
    assert "Maskarinec" in ggm  # ggm banner

    tap = c.get("/", headers={"Host": "tap.test"}).get_data(as_text=True)
    assert "Thailand Archaeometallurgy Project" in tap  # tap banner
    assert "Maskarinec" not in tap  # no cross-tenant leakage


def test_multitenant_unknown_host_uses_default_core():
    app = create_app(sites={"tap.test": "tap"}, default_core="ggm")
    app.testing = True
    html = app.test_client().get("/", headers={"Host": "nope.test"}).get_data(as_text=True)
    assert "Maskarinec" in html  # fell back to default core (ggm)


def test_multitenant_healthz_reports_host_core():
    app = create_app(sites={"ggm.test": "ggm", "tap.test": "tap"}, default_core="ggm")
    app.testing = True
    c = app.test_client()
    assert c.get("/healthz", headers={"Host": "tap.test"}).get_json()["core"] == "tap"
    assert c.get("/healthz", headers={"Host": "ggm.test"}).get_json()["core"] == "ggm"


def test_per_page_config_parsed():
    from infrared.config.loader import load_collection

    assert load_collection("tap").display.per_page == [100, 500, 1000]


def test_pale_banner_core_uses_dark_button_text():
    # mmap's pale banner (#f9d88d) must get black button text for legibility.
    html = _html("/about", core="mmap")
    assert "#f9d88d" in html
    assert "color: #000000" in html


# --- result-dependent features (need Solr) ---------------------------------

def _solr_up() -> bool:
    try:
        urllib.request.urlopen(
            "http://localhost:8983/solr/admin/cores?wt=json", timeout=3
        )
        return True
    except Exception:
        return False


solr = pytest.mark.skipif(not _solr_up(), reason="Solr not reachable on :8983")


@solr
def test_table_view_is_sortable_with_row_and_image_popup():
    html = _html("/search?view=table&DTYPE_ss=images")
    assert "sortable" in html  # bootstrap-sortable trigger class
    assert ">Row<" in html  # Row column header
    assert "image-hover-preview" in html  # far-right image popup column
    assert "preview-popup" in html
    assert "/record/" in html  # row number links to the full record


@solr
def test_pagination_format_and_display_switcher():
    html = _html("/search?view=table&per_page=80&page=3&DTYPE_ss=images")
    assert "Previous" in html
    assert "Next" in html
    assert "Page 3" in html
    assert "161" in html  # start row of page 3 at 80/page
    for icon in ("fa-table", "fa-list", "fa-th", "fa-file"):
        assert icon in html


@solr
def test_pagination_only_at_top_not_bottom():
    html = _html("/search?view=list&DTYPE_ss=images")
    # the display switcher (#displays) appears exactly once = controls only on top
    assert html.count('id="displays"') == 1


@solr
def test_facets_collapsed_by_default():
    html = _html("/search")
    assert "facet-toggle" in html
    assert "collapsed" in html  # at least one facet starts collapsed


@solr
def test_active_facet_expands_and_shows_breadcrumb():
    html = _html("/search?SITE_ss=NPW")
    assert "collapse show" in html  # the active facet card is expanded
    assert 'id="breadcrumbs"' in html
    assert "NPW" in html  # active constraint shown as a breadcrumb


@solr
def test_per_page_dropdown_uses_config_values():
    html = _html("/search?DTYPE_ss=images&view=list")
    assert 'aria-label="Records per page"' in html
    assert "100 / page" in html
    assert "1,000 / page" in html
    assert "per_page=500" in html  # an option navigates to that page size


@solr
def test_list_row_number_links_to_record():
    html = _html("/search?view=list&DTYPE_ss=images")
    assert 'class="row-num"' in html
    assert "/record/" in html
