Infrared
========

A configurable [Solr](https://solr.apache.org/) discovery UI — a lightweight,
Blacklight-style search interface (header, breadcrumbs, facets, multiple result
display modes), themable via Bootstrap.

**One app, many cores.** The active Solr core is chosen at run time by the
`INFRARED_CORE` environment variable; each core has a profile in `configs/`.
Switching cores requires no code change.

> **Status:** mid-rewrite from Bottle to Flask. The configuration layer
> (TOML profiles, validation) and app scaffold are in place; the search UI is
> being rebuilt. See `FLASK_REWRITE_PLAN.md` for the roadmap.

Requirements
------------

* Python 3.11 or higher
* [Flask](https://flask.palletsprojects.com/), [pydantic v2](https://docs.pydantic.dev/)
  (and `pysolr`, once the search layer lands)

Install
-------

From the repository root:

```
pip install -e .
```

(or `pip install flask 'pydantic>=2'` for a minimal setup).

Configure a core
----------------

Each Solr core is described by a TOML profile in `configs/`, e.g.
`configs/ggm.toml`. List the available cores by validating one:

```
python -m infrared.cli check-config
```

A profile defines the site branding, Solr coordinates, display defaults, and a
set of **views** (ordered `{solr, label}` lists). Display defaults include
`per_page` — the page-size options offered in the results "per page" dropdown,
e.g. `per_page = [100, 500, 1000]` (the first value is the default). Validate a
profile — TOML syntax and schema errors are reported with location and field
path:

```
python -m infrared.cli check-config ggm
```

About page
----------

Each core gets its own About page — the start page and the **About** nav link
show it in the result pane. It's a plain HTML fragment in `about/`:

* `about/<core>.html` — per-core page (e.g. `about/tap.html`), edit freely.
* `about/default.html` — fallback for any core without its own file.

No templating is involved; just write HTML. (**Start over** clears filters and
goes to the full result list rather than the About page.)

Run (development)
-----------------

Select a core and start the dev server:

```
INFRARED_CORE=ggm python wsgi.py --port 3002
```

It will print something like:

```
 * Serving Flask app 'infrared'
 * Running on http://localhost:3002
```

Then visit http://localhost:3002. Stop the server with `Ctrl-C`. To serve a
different core, change `INFRARED_CORE` and restart.

Deploy (Apache + mod_wsgi)
--------------------------

`app.wsgi` is the WSGI entry point; it builds the Flask app for the active core,
chosen (in priority order) from:

1. `SetEnv INFRARED_CORE <core>` in the vhost,
2. the `INFRARED_CORE` OS environment variable, or
3. the deployment directory name with a trailing `-infrared` stripped
   (a clone in `/home/ubuntu/tap-infrared` defaults to the `tap` core).

So a per-core deployment needs no code edit — name the clone `<core>-infrared`,
or add one `SetEnv` line to the vhost. `infrared.conf` is a ready-to-copy vhost
template; `configs/tap-infrared.conf` and `configs/mmap-infrared.conf` are
concrete examples. Smoke-test the WSGI app without Apache with
`mod_wsgi-express start-server app.wsgi` (set `INFRARED_CORE` first), or with
`INFRARED_CORE=<core> mod_wsgi-express start-server app.wsgi --port 8088`.

Tests
-----

```
python -m pytest
```

Includes parity tests that confirm each `configs/<core>.toml` reproduces its
legacy `configs/config-<core>.py` exactly.
