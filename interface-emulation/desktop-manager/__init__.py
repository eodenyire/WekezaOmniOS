"""
WekezaOmniOS Interface Emulation — Desktop Manager
===================================================
Manages desktop environment switching, workspace persistence, and
skin lifecycle across Windows, Ubuntu, KDE, and macOS environments.
"""

import os
import sys

_BASE = os.path.dirname(os.path.abspath(__file__))
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)

from desktop_manager import DesktopManager

__all__ = ["DesktopManager"]
