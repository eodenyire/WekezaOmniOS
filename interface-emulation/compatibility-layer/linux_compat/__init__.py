"""
WekezaOmniOS Interface Emulation — Linux Compat Package
========================================================
Provides LinuxCompat for ELF binary loading, path handling, and
syscall pass-through logging.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from linux_compat import LinuxCompat

__all__ = ["LinuxCompat"]
