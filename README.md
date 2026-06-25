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
set of **views** (ordered `{solr, label}` lists). Validate a profile — TOML
syntax and schema errors are reported with location and field path:

```
python -m infrared.cli check-config ggm
```

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

`app.wsgi` is the WSGI entry point; it sets `INFRARED_CORE` and imports the
Flask app. A per-core deployment differs only in that one value (set it in
`app.wsgi` or in the vhost/daemon environment) — no code is copied to switch
cores. See `configs/*.conf` for example vhosts.

Tests
-----

```
python -m pytest
```

Includes parity tests that confirm each `configs/<core>.toml` reproduces its
legacy `configs/config-<core>.py` exactly.
