#!/usr/bin/env python
"""Local dev launcher: run the multi-tenant app against your host Solr and browse
every configured core at once.

    python scripts/run_local.py                # http://<core>.localhost:8000/
    python scripts/run_local.py --port 9000

For each host in configs/sites.toml it also registers a ``<core>.localhost``
alias. Browsers resolve ``*.localhost`` to loopback, so there's no need to edit
/etc/hosts and no Secure-DNS/DoH interference (unlike the real *.johnblowe.com
names, which resolve to the AWS load balancer).

By default it points the ``tbdb`` profile at the live ``stedt`` core (same
schema), since there's usually no local ``tbdb`` core; disable with
``--no-tbdb-stedt``.

Dev helper only — production uses gunicorn + Caddy (see DEPLOY.md).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from infrared import create_app  # noqa: E402
from infrared.config.loader import load_sites  # noqa: E402
from infrared.search.repository import SolrRepository  # noqa: E402


def build_app(tbdb_to_stedt: bool = True):
    sites, default = load_sites(REPO_ROOT / "configs" / "sites.toml")
    for host, core in list(sites.items()):
        sites[host.split(".")[0] + ".localhost"] = core  # tap.johnblowe.com -> tap.localhost
    app = create_app(sites=sites, default_core=default)
    if tbdb_to_stedt:
        cols, reps = app.config["COLLECTIONS"], app.config["REPOSITORIES"]
        if "tbdb" in cols:
            cols["tbdb"].solr.core = "stedt"
            reps["tbdb"] = SolrRepository(cols["tbdb"])
    return app


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--debug", action="store_true")
    p.add_argument(
        "--no-tbdb-stedt",
        dest="tbdb_stedt",
        action="store_false",
        help="don't point the tbdb profile at the local stedt core",
    )
    args = p.parse_args()

    app = build_app(tbdb_to_stedt=args.tbdb_stedt)
    cores = ", ".join(sorted(app.config["COLLECTIONS"]))
    print(f"Infrared (multi-tenant dev) → http://{args.host}:{args.port}")
    print(f"  cores: {cores}")
    print(f"  browse e.g. http://tap.localhost:{args.port}/  (use the *.localhost names)")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
