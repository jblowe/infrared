"""Infrared command-line entry point."""
from __future__ import annotations

import argparse
import sys

from .config.loader import ConfigError, available_cores, load_collection


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="infrared")
    sub = parser.add_subparsers(dest="cmd", required=True)

    check = sub.add_parser("check-config", help="validate a collection profile")
    check.add_argument("core", nargs="?", help="core name (configs/<core>.toml)")

    args = parser.parse_args(argv)
    if args.cmd == "check-config":
        return _check_config(args.core)
    return 2


def _check_config(core: str | None) -> int:
    if not core:
        cores = available_cores()
        print("available cores:", ", ".join(cores) or "(none)")
        return 1
    try:
        col = load_collection(core)
    except ConfigError as exc:
        print(f"✗ {exc}", file=sys.stderr)
        return 1
    n_fields = sum(len(v) for v in col.views.values())
    print(
        f"✓ {core}: OK — core '{col.solr.core}', "
        f"views: {', '.join(col.views)} ({n_fields} entries)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
