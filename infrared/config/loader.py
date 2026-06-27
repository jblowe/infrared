"""Load and validate a collection profile from ``configs/<core>.toml``.

Selection is by name (the ``INFRARED_CORE`` env var or an explicit ``core``).
Errors are raised as :class:`ConfigError` with messages aimed at whoever is
editing the TOML — TOML syntax errors include line/column, and schema errors
are reported per field path.
"""
from __future__ import annotations

import os
import tomllib
from pathlib import Path

from pydantic import ValidationError

from .models import Collection


class ConfigError(Exception):
    """Raised when a collection profile is missing, unparseable, or invalid."""


def config_dir() -> Path:
    override = os.environ.get("INFRARED_CONFIG_DIR")
    if override:
        return Path(override)
    # infrared/infrared/config/loader.py -> repo root is parents[2]
    return Path(__file__).resolve().parents[2] / "configs"


def available_cores() -> list[str]:
    d = config_dir()
    return sorted(p.stem for p in d.glob("*.toml")) if d.is_dir() else []


def load_collection(core: str) -> Collection:
    if not core:
        raise ConfigError(
            "no core selected; set INFRARED_CORE or pass core=... "
            f"(available: {', '.join(available_cores()) or 'none'})"
        )
    path = config_dir() / f"{core}.toml"
    if not path.is_file():
        cores = available_cores()
        hint = f" available: {', '.join(cores)}" if cores else ""
        raise ConfigError(f"no config for core '{core}' at {path}.{hint}")

    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"{path.name}: invalid TOML: {exc}") from exc

    try:
        return Collection.model_validate(raw)
    except ValidationError as exc:
        raise ConfigError(_format_validation_error(path.name, exc)) from exc


def _format_validation_error(name: str, exc: ValidationError) -> str:
    lines = [f"{name}: {exc.error_count()} configuration error(s):"]
    for err in exc.errors():
        loc = ".".join(str(p) for p in err["loc"]) or "(root)"
        lines.append(f"  - {loc}: {err['msg']}")
    return "\n".join(lines)
