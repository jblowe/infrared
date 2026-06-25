"""Apache mod_wsgi entry point.

Per-core deployments differ only in the INFRARED_CORE value below (or set it in
the vhost / daemon environment instead). No code copy needed to switch cores.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

# Select the active collection profile (configs/<core>.toml).
os.environ.setdefault("INFRARED_CORE", "mmap")

from wsgi import app as application  # noqa: E402
