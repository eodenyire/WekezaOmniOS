"""
WekezaOmniOS Cloud Desktop — Web Platform

Serves the web-based dashboard by mounting the API Gateway's FastAPI app
and adding static-file / HTML page shortcuts.  In production this would be
a separate reverse-proxy tier; here it re-exports the same ASGI app.
"""

import os
import sys

_CLOUD_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CLOUD_DIR not in sys.path:
    sys.path.insert(0, _CLOUD_DIR)

# Re-use the gateway app as the ASGI entry-point
from api_gateway.server import app  # noqa: F401, E402

__all__ = ["app"]
