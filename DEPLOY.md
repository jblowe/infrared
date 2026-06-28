# Deploying Infrared (containerized, multi-tenant)

This is the generic **container** stack: one small host runs Docker Compose with
three services — a reverse proxy (Caddy), one multi-tenant Flask app, and one
multi-core Solr — behind an AWS **WAF + ALB** that terminates TLS. Caddy routes
by `Host` to the app and serves the per-core image repos as static files.

> - The **actual** deployment runs on a shared multi-app EC2 box where Apache
>   stays the front door and Infrared sits behind it — see **`EC2.md`** and
>   **`docker-compose.ec2.yml`**. This file is the clean/generic reference using
>   `docker-compose.yml`.
> - The single-tenant model (one app per vhost via `INFRARED_CORE`, `app.wsgi`)
>   still works and is documented in the README.

## Architecture

```
Internet → AWS WAF + ALB  (TLS + WAF here; ACM cert)
         → :80 on the EC2/Lightsail host
         → caddy   ── routes by Host ──┐
              ├─ <core>.johnblowe.com  → reverse_proxy web:8000
              └─ /<image-prefix>/*     → static files (/srv/images/<subdir>)
         → web   (one Flask app; core chosen per request from the Host header)
         → solr  (multi-core; internal only)
```

Why this shape:
- **Solr must run 24/7** (stateful JVM) → a single always-on host is the cheapest
  option; serverless doesn't help. Containerizing only makes the host
  reproducible, it doesn't change the cost basis.
- **Images (~90 GB) are a mounted volume**, not in the app image, and are served
  by Caddy (faster, and keeps app containers tiny).

## Host layout (put these on a dedicated EBS volume — snapshot it)

```
/data/solr            Solr data + cores
/data/images/<subdir> image repos, one subdir per core (matches the Caddyfile)
```

Keeping data on its **own EBS volume** means you can detach/reattach it to a
replacement instance and be back in minutes, and back up with cheap incremental
EBS snapshots (e.g. via Data Lifecycle Manager).

## Tenancy: how a request finds its core

`web` runs the app via `wsgi:app` → `create_app()`, which reads
`INFRARED_SITES=/app/configs/sites.toml` and loads every mapped core at startup.
On each request it picks the core from the `Host` header
([configs/sites.toml](configs/sites.toml)); unmatched hosts fall back to `default`.

Each TOML keeps `server = "http://localhost:8983"` for local dev; in the
container, `INFRARED_SOLR_SERVER=http://solr:8983` overrides it (no per-file edits).

## First-time setup

1. **Provision** a small instance (t4g.small / Lightsail 2–4 GB), install Docker + Compose.
2. **Attach** the data EBS volume and mount it; create `/data/solr` and `/data/images/<subdir>`.
3. **Load Solr cores** into `/data/solr` (copy your existing core dirs, or create + index).
4. **Copy image repos** into `/data/images/<core>` (these are the dirs the old
   symlinks pointed at, reorganized one subdir per core).
5. **Point DNS / ALB listener rules** for each hostname at the instance's target
   group (port 80). Keep the WAF associated with the ALB as-is.
6. From the repo on the host:
   ```bash
   docker compose build
   docker compose up -d
   docker compose logs -f
   ```
7. Verify: `curl -H 'Host: tap.johnblowe.com' http://localhost/healthz` → `{"core":"tap"}`.

## The WAF + ALB stay as-is

TLS terminates at the ALB (required for WAF to inspect HTTPS), so the ALB
forwards **plain HTTP to :80**. Just point the target group at this host's port
80 (Caddy). WAF rules, ACM cert, and listener rules are unchanged — only what
listens behind the ALB changed (Apache → Caddy). The ALB **health check** can
target `/healthz` (any host → default core answers).

## Adding a new site

1. `configs/<core>.toml` (+ optional `about/<core>.html`, `static/images/...`).
2. Add the host to `configs/sites.toml`.
3. Add a block to the `Caddyfile` (`import infrared /<prefix> <core>`).
4. Put its images under `/data/images/<core>`.
5. Add the hostname to DNS + the ALB; `docker compose up -d` (rebuild if app code changed).

## Backups

- **Data**: EBS snapshots of the data volume (covers Solr + images).
- **Solr** (optional finer-grained): the Solr backup API or `solr` snapshot → S3.
- **Config/code**: this git repo.

## Single-core container (alternative)

To run one core per container instead of multi-tenant, drop `INFRARED_SITES` and
set `INFRARED_CORE=<core>` on the `web` service (and run one `web` per core,
each routed by its own Caddy block). Multi-tenant is simpler at this scale.

## Local smoke test (no ALB, no containers)

Run just the multi-tenant **app** against a Solr you already have on the host.
This skips Caddy/containers — it only checks that host→core routing and search
work.

### Start the app

Either the Flask dev server (no extra install):

```bash
cd /path/to/infrared
INFRARED_SITES=configs/sites.toml python wsgi.py --port 8000
```

…or the production server (needs gunicorn once: `pip install -e ".[deploy]"`):

```bash
INFRARED_SOLR_SERVER=http://localhost:8983 \
INFRARED_SITES=configs/sites.toml \
gunicorn -b 127.0.0.1:8000 wsgi:app
```

Both read `configs/sites.toml` and pick the core per request from the `Host`
header. `INFRARED_SOLR_SERVER` is optional locally (defaults to each TOML's
`server`, normally `http://localhost:8983`).

### Test with curl (set the Host header)

```bash
curl -H 'Host: ggm.johnblowe.com' http://127.0.0.1:8000/healthz
curl -H 'Host: tap.johnblowe.com' 'http://127.0.0.1:8000/search?view=table&per_page=80'
```

### Test in a browser

**Use `*.localhost` hostnames** — browsers resolve anything ending in `.localhost`
straight to loopback, with no DNS lookup and no `/etc/hosts` edits. The
`run_local.py` launcher below adds a `<core>.localhost` alias for every core, so
just visit:

```
http://tap.localhost:8000/        http://ggm.localhost:8000/
http://mmap-sites.localhost:8000/ http://tbdb.localhost:8000/
```

Two gotchas this avoids:

- **The real `*.johnblowe.com` names don't work in the browser**, even with
  `/etc/hosts` pointing them at `127.0.0.1`: those are live public domains
  (CNAME → your AWS load balancer), and a browser with **Secure DNS / DoH**
  resolves them via public DNS, ignoring `/etc/hosts` — so it connects to AWS
  and hangs. `curl` (OS resolver) honors `/etc/hosts`, which is why curl works
  but the browser doesn't. `*.localhost` sidesteps this entirely.
- **Include the `:8000`.** Without a port the browser uses **port 80**, which on
  this machine is your local **Apache** (`httpd`), not this app. (In the real
  deployment Caddy owns :80 behind the ALB, so there's no port suffix.)

### Easiest: the bundled dev launcher

`scripts/run_local.py` does all of the above — loads `configs/sites.toml`, adds
`<core>.localhost` aliases, and (by default) points `tbdb` at the live `stedt`
core — then serves on `:8000`:

```bash
python scripts/run_local.py            # then browse http://tap.localhost:8000/
python scripts/run_local.py --port 9000 --no-tbdb-stedt
```

### Cores without a matching local Solr core

A site only returns search results if its profile's `[solr] core` exists in your
local Solr; otherwise the page still renders (About, nav, `/healthz`) but search
errors. To exercise a profile against a differently-named local core (e.g. test
`tbdb` against the live `stedt` core, same schema), either edit `core` in the
TOML or use `scripts/run_local.py` (which already does the `tbdb → stedt`
override; see `--no-tbdb-stedt` to disable).

### Stop it

```bash
# Ctrl-C in the foreground, or if backgrounded:
pkill -f wsgi.py        # or: pkill -f run_local.py
```
