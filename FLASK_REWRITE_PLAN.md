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

- **`Field`** — `key`, `solr_field`, `label`, and flags: `facetable`, `sortable`,
  `type` (string/int/image/date…). One source of truth for a field; views and
  facets reference fields by key instead of duplicating `(label, field)` tuples.
- **`View`** — a named display mode (`list`, `table`, `gallery`, `full`) =
  ordered list of `Field`s + a template name. Replaces the `LIST`/`TABLE`/… keys
  of `FIELD_DEFINITIONS` and the near-duplicate `LIST`/`FULL` lists.
- **`Collection`** — the whole per-core profile: branding (title, banner, colours,
  logo), Solr coordinates (`server`, `core`), image config, the `Field` registry,
  the `View`s, the facet set, paging defaults. This **is** the parsed TOML.
- **`SearchRequest`** — parses `flask.request` into `terms` + `controls`
  (`page`, `per_page`, `view`); knows how to rebuild its own query string for
  links/breadcrumbs. Replaces the `parameters` + `controls` dicts and the manual
  `parse_qsl` juggling in `app.py:facet()`.
- **`SolrRepository`** — wraps **pysolr**; `search(request, view) ->
  SearchResponse`, `get(id) -> Document`, `suggest(field, term, limit)`.
  Query terms are passed as parameters, not f-string-interpolated (fixes the
  injection-fragile `{q[0]}:"{q[1]}"`).
- **`SearchResponse`** — typed result object: `documents`, `facets`, `total`,
  `pagination`, `errors`, `messages` (and `document` for single-record).
  This is what templates receive — **the replacement for `data`.**

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

### 5.2 TOML shape (worked from the current mmap config)

```toml
[collection]
title = "MMAP"
banner = "Middle Mekong Archaeology Project"
banner_color = "#f9d88d"
secondary_color = "#002868"
navbar = "navbar-light"
logo = "mmap-logo-pot-and-river.png"

[solr]
server = "http://localhost:8983"
core   = "mmap-sites"
facet_limit = 100
facet_mincount = 2

[display]
row_limits   = [10, 20, 30]
title_field  = "site_name_s"
image_field  = "General_view_THUMBNAILS_ss"
image_prefix = "/mmap-images"

# Field registry: one entry per field, referenced by key elsewhere.
[fields.site_name]   = { solr = "site_name_s",  label = "Site name", facet = true, sort = true }
[fields.site_date]   = { solr = "site_date_s",  label = "Site date", facet = true }
[fields.thumbnails]  = { solr = "General_view_THUMBNAILS_ss", label = "Images", type = "image" }
# ...

[views]
search  = ["siteid", "site_name", "site_date"]      # search handler fields
list    = ["siteid", "site_name", "site_date", ...] # ordered field keys
table   = ["site_name", "site_short", "nrprimrv"]
gallery = ["site_name"]
full    = ["...everything..."]
facets  = ["site_name", "site_date", "gis_code", ...]
```

This kills the duplication: `list`/`full`/`facets` are now just lists of field
*keys*; labels and Solr names live once in `[fields]`.

### 5.3 Validation & user feedback (your stated priority)

- Parse with **`tomllib`** (Python 3.11 stdlib — matches the project env). Syntax
  errors raise `TOMLDecodeError` with line/column → surfaced verbatim.
- Validate structure with **pydantic v2** dataclasses (`Field`, `View`,
  `Collection`). Pydantic gives precise, field-path error messages
  ("`views.list[3]` references unknown field key `foo`"), which is exactly the
  "good feedback on bad TOML" you asked for.
- A `infrared check-config <core>` CLI command validates a profile without
  starting the server — the moral equivalent of `python config.py` testing
  validity today, but with real diagnostics.

*(Confirmed: pydantic v2.)*

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

1. **Scaffold** — package layout, `create_app`, `pyproject.toml`, `wsgi.py`,
   empty blueprints; app boots and serves a hello page under `INFRARED_CORE`.
2. **Config model** — `Field`/`View`/`Collection`, TOML loader + validation,
   `check-config` CLI. Convert **all** `configs/config-*.py` to TOML.
   (Unit-tested against the old `config-*.py` values for parity.)
3. **Search core** — `SolrRepository` (pysolr), `SearchRequest`,
   `SearchResponse`; verify query parity against the live Solr cores.
4. **Routes + templates** — catalog blueprint + the Jinja set; reach feature
   parity with the Bottle UI (facets, all display modes, single record, suggest).
5. **Deployment** — update `app.wsgi`/vhost confs for env-var core selection;
   smoke-test under mod_wsgi.
6. **Delete Bottle** — remove `app.py`, `utils.py`, `solr_query.py`, `top.py`,
   `config.py`, `views/*.tpl`; finalise `pyproject.toml`. Merge to `main`.

---

## 8. Resolved decisions (2026-06-24)

1. **Dirty tree** — cleaned up by the user; remaining untracked files are
   ignored. Rewrite starts from current `main`.
2. **Validation** — **pydantic v2**.
3. **Solr client** — move to **pysolr** (behind `SolrRepository`).
4. **`/remove`** — **removed** entirely; facet removal becomes a link.
5. **Configs** — convert **all** `configs/config-*.py` to TOML.
