"""
WekezaOmniOS Interface Emulation — macOS UI Package
====================================================
macOS-style desktop environment components and a MacOSUI façade.
"""

import os
import sys
import importlib.util


def _load_from_here(name: str, filename: str):
    """Loads a submodule from this package's directory by file path."""
    _here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        f"macos_ui.{name}", os.path.join(_here, filename)
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_taskbar_mod     = _load_from_here("taskbar",      "taskbar.py")
_start_menu_mod  = _load_from_here("start_menu",   "start_menu.py")
_file_mgr_mod    = _load_from_here("file_manager", "file_manager.py")
_sys_tray_mod    = _load_from_here("system_tray",  "system_tray.py")

MacOSTaskbar      = _taskbar_mod.MacOSTaskbar
MacOSStartMenu    = _start_menu_mod.MacOSStartMenu
MacOSFileManager  = _file_mgr_mod.MacOSFileManager
MacOSSystemTray   = _sys_tray_mod.MacOSSystemTray


class MacOSUI:
    """
    Façade that assembles the full macOS desktop scene.
    """

    def __init__(self):
        print("[MacOSUI] 🍎 Loading macOS UI components...")
        self.taskbar = MacOSTaskbar()
        self.start_menu = MacOSStartMenu()
        self.file_manager = MacOSFileManager()
        self.system_tray = MacOSSystemTray()
        print("[MacOSUI] ✅ macOS UI ready.")

    def render_desktop(self) -> str:
        """
        Renders a full macOS desktop scene.

        Returns:
            str: Multi-line description of the macOS desktop.
        """
        print("\n[MacOSUI] Rendering macOS desktop...")
        parts = [
            "=" * 60,
            "  🍎  WekezaOmniOS — macOS Desktop Environment",
            "=" * 60,
            self.taskbar.render(),
            self.start_menu.render(),
            self.file_manager.render(),
            self.system_tray.render(),
            "=" * 60,
        ]
        scene = "\n".join(parts)
        print(scene)
        return scene


__all__ = [
    "MacOSTaskbar",
    "MacOSStartMenu",
    "MacOSFileManager",
    "MacOSSystemTray",
    "MacOSUI",
]
