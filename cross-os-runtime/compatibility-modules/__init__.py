"""
WekezaOmniOS Compatibility Modules
OS-specific runtime adapters for the Cross-OS Runtime Layer.
"""

from .windows_runtime.windows_runtime import WindowsRuntime
from .linux_runtime.linux_runtime import LinuxRuntime
from .android_runtime.android_runtime import AndroidRuntime
from .legacy_mobile_runtime.legacy_mobile_runtime import LegacyMobileRuntime

__all__ = [
    "WindowsRuntime",
    "LinuxRuntime",
    "AndroidRuntime",
    "LegacyMobileRuntime",
]
