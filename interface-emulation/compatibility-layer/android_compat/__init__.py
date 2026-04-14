"""
WekezaOmniOS Interface Emulation — Android Compat Package
=========================================================
Provides AndroidCompat for APK loading, Android intent translation,
and Android API emulation.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from android_compat import AndroidCompat

__all__ = ["AndroidCompat"]
