"""Apache mod_wsgi entry point.

One file serves every core. The active collection profile (configs/<core>.toml)
is chosen, in priority order, from:

  1. ``SetEnv INFRARED_CORE <core>`` in the vhost  (passed through the WSGI environ)
  2. the ``INFRARED_CORE`` OS environment variable
  3. the deployment directory name, with a trailing ``-infrared`` stripped
     (so a clone in ``/home/ubuntu/tap-infrared`` defaults to the ``tap`` core)

So a per-core deployment needs no code edit: either name the clone
``<core>-infrared`` or add one ``SetEnv`` line to the vhost. See configs/*.conf.

The Flask app is built lazily on the first request, once the core is known
(``SetEnv`` values are only visible per-request, not at import time).
"""
import os
import sys
import threading

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from infrared import create_app  # noqa: E402

_app = None
_lock = threading.Lock()


def _core_from_dir():
    """Derive the core from the deployment directory name (``<core>-infrared``)."""
    name = os.path.basename(_HERE)
    return name[: -len("-infrared")] if name.endswith("-infrared") else name


def application(environ, start_response):
    global _app
    if _app is None:
        with _lock:
            if _app is None:
                core = (
                    environ.get("INFRARED_CORE")
                    or os.environ.get("INFRARED_CORE")
                    or _core_from_dir()
                )
                _app = create_app(core)
    return _app(environ, start_response)
