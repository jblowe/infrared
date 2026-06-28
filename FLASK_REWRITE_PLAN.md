# Infrared: Bottle → Flask Rewrite Plan

Status: **draft for review** — no code written yet.
Date: 2026-06-24

This document proposes a from-scratch rewrite of Infrared as a conventional,
class-oriented Flask application that **replaces** the current Bottle app in this
repo. When complete, the Bottle code is gone from the working tree (recoverable
via git history and a tag).

---

## 1. Goals & guiding principles

1. **Same product, cleaner internals.** Preserve Infrared's UX, theming, facets,
   display modes, and — crucially — its deployment model: *one app, the active
   Solr core selected at deploy time, no code change to switch cores.*
2. **Retire the untyped `data` dict.** Replace the grab-bag that flows
   app → utils → templates with small, typed domain objects consumed by attribute.
3. **Config as data.** Move per-core definitions out of executable `config.py`
   into declarative **TOML**, loaded into validated dataclasses, with clear,
   line-referenced error feedback when the TOML is malformed.
4. **Select the core by environment variable**, not by copying a file.
5. **Few, maintainable templates.** One template per display mode, one per UI
   component, over a shared base layout.
6. **Conventional Flask.** App factory, blueprints, Jinja2, `flask.request`,
   testable units. Smaller and simpler than today.

Non-goals: redesigning the Solr schema; changing what the cores contain;
reworking the visual design beyond what consolidation requires.

---

## 2. What exists today (baseline)

| File | Role | Fate |
|---|---|---|
| `app.py` | Bottle routes; builds `parameters`, mutates `data`, renders | replaced by `app/` package + blueprints |
| `config.py` | `parmz` global bag + `FIELD_DEFINITIONS` (stringly-typed views, `(label, field)` tuples) | replaced by `configs/*.toml` + `Collection` model |
| `utils.py` | `do_solr_query` assembles `data`; paging; `set_controls`; render | logic split into `search/` service + response model |
| `solr_query.py` | thin `solr` lib wrapper; f-string query building | replaced by `SolrRepository` with parameterised queries |
| `top.py` | stray hello-world | deleted |
| `views/*.tpl` (19 Bottle templates) | UI | replaced by ~12 Jinja2 templates |
| `configs/config-*.py` | per-core profiles | converted to `configs/*.toml` |
| `app.wsgi`, `configs/*.conf` | Apache + mod_wsgi deployment | updated for core-by-env-var |

### The `data` dict contract (what templates actually use)

Measured from `views/*.tpl`. The new model must expose equivalents:

| Old `data[...]` key | Used for | New home |
|---|---|---|
| `results` (`.results`, `.facets`, `.numfound`, `.start_row`) | the result set + facets | `SearchResponse.documents`, `.facets`, `.total`, `.start` |
| `content` | alias of `results.results` | `SearchResponse.documents` |
| `single` | one full record | `SearchResponse.document` (single-doc response) |
| `image_field`, `image_prefix` | thumbnail rendering | `Collection.image_field`, `Collection.image_prefix` (template globals) |
| `terms`, `base_string`, `query_string` | breadcrumbs & links | `SearchRequest` (exposes `.terms`, `.query_string()`) |
| `result_fields` | columns to show | `View.fields` |
| `controls`, `controls['page']` | paging / display mode | `SearchRequest.controls` (`page`, `per_page`, `view`) |
| `errors`, `messages` | alerts | `SearchResponse.errors` / `.messages` |
| `back`, `selected_field` | nav state | folded into request/response or dropped if unused |

Branding globals (`TITLE`, `BANNER`, `LOGO`, `NAVBAR`, `BANNER_COLOR`,
`FACET_LABELS`, `FACETS`, `TITLE_FIELD`) become attributes of `Collection`,
injected once as Jinja globals.

---

## 3. Replacement / git strategy (answering "cleanest way")

1. **Settle the dirty tree first.** Commit or stash the current uncommitted
   changes on `main` so the rewrite starts from a known-clean base. *(Needs your
   decision — see Open Questions.)*
2. **Tag the final Bottle state:** `git tag bottle-final` (and optionally push the
   tag). This is the recovery point.
3. **Branch:** `git switch -c flask-rewrite`.
4. **Build incrementally on the branch**, deleting obsolete files in the same
   commits that supersede them, so history reads cleanly.
5. **Merge to `main`** when done (a normal merge keeps the rewrite history; a tag
   already preserves Bottle). After merge, `main` is pure Flask.

No second repo, no `archive/` directory in-tree — git history + the `bottle-final`
tag are the archive.

---

## 4. Target architecture

```
infrared/
├─ wsgi.py                  # entry point: app = create_app()
├─ app.wsgi                 # mod_wsgi shim: sets INFRARED_CORE, imports wsgi.app
├─ pyproject.toml           # deps; replaces requirements.txt
├─ configs/
│  ├─ ggm.toml              # per-core profiles (converted from config-*.py)
│  ├─ mmap.toml
│  └─ tap.toml
├─ infrared/               # the Python package
│  ├─ __init__.py           # create_app(core=None) app factory
│  ├─ config/
│  │  ├─ models.py          # Field, View, Collection (validated dataclasses)
│  │  └─ loader.py          # load_collection(core) -> Collection; TOML + validation
│  ├─ search/
│  │  ├─ request.py         # SearchRequest (parse terms + controls from flask.request)
│  │  ├─ response.py        # SearchResponse / Document / Facet / Pagination
│  │  └─ repository.py      # SolrRepository (connection + parameterised queries)
│  ├─ views/                # Flask blueprints (routes only; thin)
│  │  ├─ catalog.py         # /, /search, /single/<id>
│  │  └─ suggest.py         # /suggest
│  └─ templates/ + static/  # Jinja2 + assets
└─ tests/
```

### 4.1 Domain model (the classes that retire the dicts)

> **Design note (decided during build):** there is **no field registry**. The
> existing config structure is fine — a view simply lists the Solr fields it
> uses, in order, each with its own label. Labels are **per-view** (the same
> Solr field may be labelled differently in different views), duplication across
> views is allowed, and order of appearance = UI order. `_ss`/`_txt` variants
> are treated as plain separate Solr fields (no shadowing logic). See §5.2.

- **`ViewEntry`** — `{solr, label}`. The atom of a view.
- **`Site` / `Solr` / `Display`** — the branding, Solr-coordinate, and
  display-default sections of a profile (pydantic submodels).
- **`Collection`** — the whole per-core profile: `site`, `solr`, `display`, and
  `views` (a dict of view-name → ordered `list[ViewEntry]`). This **is** the
  parsed TOML. Helpers: `view(name)`, `facets`, `facet_labels`, `labels`.
- **`SearchRequest`** — parses query params into `terms` + controls
  (`page`, `per_page`, `view`); rebuilds query strings for links via
  `query_string()` / `with_term()` / `without_term()` / `is_active()`. Replaces
  the `parameters` + `controls` dicts and the manual `parse_qsl` juggling.
- **`SolrRepository`** — wraps **pysolr**; `search(request) -> SearchResponse`,
  `get(id) -> dict | None`. Term values are **escaped** (`solr_escape`), not
  f-string-interpolated (fixes the injection-fragile `{q[0]}:"{q[1]}"`); facet
  selections become `fq` filters, the main query stays `*:*`.
- **`SearchResponse` / `Facet` / `Pagination`** — typed result object:
  `documents`, `total`, `facets`, `pagination`, `errors`, `ok`. This is what
  templates receive — **the replacement for `data`.**

### 4.2 Routes (old → new), as a `catalog` blueprint

| Old | New | Notes |
|---|---|---|
| `/`, `/about` | `GET /`, `GET /about` | empty query → `*:*`; about is a static page, not a fake search |
| `/facet/`, `/search/` | `GET /search` | one handler; `SearchRequest.from_request()` |
| `/single/<term>` | `GET /record/<id>` | typed single-doc `SearchResponse` |
| `/suggest` | `GET /suggest` | JSON; own blueprint |
| `/remove/<term>` | **removed** | dead/broken; facet removal is a link built by `SearchRequest` |
| static routes | Flask `static_folder` + per-core image route | image dir still per-core |

---

## 5. Config: TOML + validation + core selection

### 5.1 Core selection by env var

- `INFRARED_CORE=mmap` selects `configs/mmap.toml`.
- `create_app()` reads `INFRARED_CORE` (overridable via `create_app(core=...)`
  for tests), calls `load_collection(core)`, stores the `Collection` on the app.
- **Under mod_wsgi:** each vhost's `app.wsgi` sets the variable before import:

  ```python
  # app.wsgi  (per-core deployment differs only in this one line)
  import os
  os.environ.setdefault("INFRARED_CORE", "mmap")
  from wsgi import app as application
  ```

  Deploying a different core = a one-line `.wsgi` (or an OS/vhost env var) — no
  copying `config.py`. This preserves the "no code change to switch cores"
  property while removing the file-copy ritual.

### 5.2 TOML shape (as built — see `configs/ggm.toml` for a real one)

```toml
[site]
title = "GGM"
banner = "Gregory G. Maskarinec: Bāhās & Bahīs of Nepal"
banner_color = "#EC5800"
navbar = "navbar-dark"
logo = "vajra.jpg"

[solr]
server = "http://localhost:8983"
core   = "ggm"
facet_limit = 10
facet_mincount = 2

[display]
per_page     = [100, 500, 1000]
title_field  = "title_s"
image_field  = "path_ss"
image_prefix = "/ggm-images"
layouts      = ["search", "facets", "list", "table", "full"]

# Views are ordered lists of {solr, label}. Labels are per-view; duplication
# across views is fine; order = UI order. No registry, no _ss/_txt shadowing.
[views]
facets = [
  { solr = "city_s", label = "City" },
  { solr = "year_s", label = "Year" },
  { solr = "text",   label = "Keyword" },
]
list = [
  { solr = "city_s",  label = "City" },
  { solr = "title_s", label = "Title" },
]
search = [
  { solr = "city_txt", label = "City" },
]
```

The converter (`scripts/convert_configs.py`) produces these verbatim from the
legacy `config-*.py`, tagging suspect entries (the old autosuggest `_s`→`_txt`
artifacts) with `# FIXME` comments — no silent rewrites.

### 5.3 Validation & user feedback (your stated priority)

- Parse with **`tomllib`** (Python 3.11 stdlib). Syntax errors raise
  `TOMLDecodeError` with line/column → surfaced verbatim by `ConfigError`.
- Validate structure with **pydantic v2** models (`ViewEntry`, `Site`, `Solr`,
  `Display`, `Collection`). `extra="forbid"` + per-field error paths give precise
  "bad TOML" feedback.
- `infrared check-config <core>` validates a profile without starting the
  server.

---

## 6. Templates (Jinja2): few and maintainable

Base layout + one partial per UI component + one per display mode:

```
templates/
├─ base.html              # <head>, theming vars, blocks; was head/index shell
├─ search.html            # extends base: searchbar + facets + results dispatch
├─ record.html            # single full record
├─ home.html, about.html  # static-ish pages
├─ components/
│  ├─ _nav.html           # nav + buttons
│  ├─ _searchbar.html     # input_field
│  ├─ _breadcrumbs.html
│  ├─ _facets.html        # leftpane
│  ├─ _pagination.html    # widgets
│  ├─ _alerts.html        # errors/messages
│  ├─ _images.html        # thumbnail block (shared by list/full/record)
│  └─ _footer.html
└─ displays/
   ├─ list.html  table.html  gallery.html  full.html
```

~12 templates vs. today's 19, with the view dispatch driven by
`View.template` instead of the `% if/include` ladder in `content.tpl`.
Branding and `image_*` injected once as Jinja globals from the `Collection`.

---

## 7. Phasing (each phase independently reviewable on `flask-rewrite`)

1. ✅ **Scaffold** — package layout, `create_app`, `pyproject.toml`, `wsgi.py`,
   blueprints; app boots under `INFRARED_CORE`.
2. ✅ **Config model** — `ViewEntry`/`Site`/`Solr`/`Display`/`Collection`, TOML
   loader + validation, `check-config` CLI. **All** `config-*.py` converted to
   TOML; per-core parity tests.
3. ✅ **Search core** — `SolrRepository` (pysolr), `SearchRequest`,
   `SearchResponse`/`Facet`/`Pagination`; verified against live Solr cores.
4. ✅ **Routes + templates** — `catalog` blueprint (`/`, `/search`,
   `/record/<id>`) + the Jinja set; facets, breadcrumbs, pagination, all four
   display modes, single record. (`/suggest` blueprint is a stub — see §9.)
5. ✅ **Deployment** — `app.wsgi` selects the core from vhost `SetEnv` →
   OS env → deployment dir name; vhost confs updated for Flask + mod_wsgi;
   verified live under `mod_wsgi-express` (mod_wsgi 5.0.2 / Python 3.11).
6. ✅ **Delete Bottle** — removed `app.py`, `utils.py`, `solr_query.py`,
   `top.py`, `config.py`, root `views/*.tpl` (19), `configs/config-*.py` (6),
   `requirements.txt`, `start.sh`, the empty `app/` dir, and the now-moot
   `tests/test_config_parity.py`. Tests green (44). Merge `flask-rewrite` →
   `main` is the remaining step (commit + push owned by the user).

---

## 8. Resolved decisions (2026-06-24)

1. **Dirty tree** — cleaned up by the user; untracked files ignored.
2. **Validation** — **pydantic v2**.
3. **Solr client** — **pysolr** (behind `SolrRepository`).
4. **`/remove`** — **removed**; facet removal is a link.
5. **Configs** — convert **all** `config-*.py` to TOML.
6. **Config model** — **no registry**; views are ordered `{solr, label}`;
   labels per-view; duplication allowed; `_ss`/`_txt` are plain separate fields.
7. **Conversion** — **verbatim**; suspect entries flagged as `# FIXME`, never
   silently rewritten.

---

## 9. Progress & handoff notes (resume here)

**Done:** Phases 1–5. On branch `flask-rewrite`; the legacy Bottle files still
exist untouched (deleted in Phase 6). The `bottle-final` tag marks the
pre-rewrite state. Tests: `python -m pytest` → all green (config parity, search
unit tests, Solr-gated integration, route smoke).

**UI parity pass (post-Phase 4):** restored from the Bottle app — fully
**self-contained assets** (local Bootstrap/jQuery/FontAwesome/bootstrap-sortable/
-table, no CDN; Flask `static_folder` → repo `static/`), nav (logo, home, about,
toggle sidebar) + `/about`, Start Over button + breadcrumb trail (no "clear
all"), original pagination line + FontAwesome display switcher (top only),
row-number → full-record links with the gray record bar, sortable table with the
hover image-popup column, and collapsible facets (collapsed by default).
**Per-core theming** is now driven by the config (`Site.banner_color` /
`secondary_color`, with a `contrast_color` filter for legible button text) and
injected in `base.html`; `site-theme.css` holds only color-agnostic rules. New
tests in `tests/test_views.py` (+ request link-builder tests) cover all of this.

**Try it (dev):** `INFRARED_CORE=ggm python wsgi.py --port 4321` →
http://localhost:4321 (cores: ggm, marc, mmap, mmap-sites, mmap-artifacts, tap).
Requires the conda `main` env (Flask, pydantic v2, pysolr) and Solr at :8983.

**Try it (mod_wsgi):** `INFRARED_CORE=ggm mod_wsgi-express start-server app.wsgi
--port 8088` → http://localhost:8088. `app.wsgi` picks the core from vhost
`SetEnv` → OS env → `<core>-infrared` dir name; see `infrared.conf` (template)
and `configs/{tap,mmap}-infrared.conf`.

**Next: Phase 6** — delete Bottle, merge to `main`.

**Open items / findings for the user (not yet actioned):**
- **SEARCH `_txt` fields are unpopulated** — e.g. `title_txt` has 0 docs in the
  `ggm` core, so the search-box dropdown fields return nothing (the working
  catch-all is `text`). Decide whether to repoint each profile's `search` view
  at `text` / the `_s` fields. Config/data, left as-is.
- **`# FIXME` entries** in `configs/mmap.toml` and `configs/mmap-artifacts.toml`
  (old autosuggest `_s`→`_txt` cruft, e.g. `sherd_txtample?_txt`; real field is
  `sherd_sample_s`). Clean by hand when convenient; parity tests track them.
- **`/suggest`** is a stub blueprint. The legacy autosuggest was non-functional
  (NameError). Implement properly or drop in a later pass.
- **Bootstrap is via CDN** in `base.html`; localise the assets in Phase 5/6 if
  offline/production use needs it.
- **`requirements.txt`** still lists Bottle deps; superseded by `pyproject.toml`,
  removed in Phase 6.
