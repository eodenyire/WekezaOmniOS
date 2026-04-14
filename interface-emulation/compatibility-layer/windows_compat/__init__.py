"""
WekezaOmniOS Interface Emulation — Windows Compatibility Package
================================================================
Provides WindowsCompat for .exe loading, registry key mapping,
path translation, and Win32 API emulation.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from windows_compat import WindowsCompat

__all__ = ["WindowsCompat"]
