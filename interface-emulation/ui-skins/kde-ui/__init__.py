"""
WekezaOmniOS Interface Emulation — KDE UI Package
==================================================
KDE Plasma desktop environment components and a KDEUI façade.
"""

import os
import sys
import importlib.util


def _load_from_here(name: str, filename: str):
    """Loads a submodule from this package's directory by file path."""
    _here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        f"kde_ui.{name}", os.path.join(_here, filename)
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_taskbar_mod     = _load_from_here("taskbar",      "taskbar.py")
_start_menu_mod  = _load_from_here("start_menu",   "start_menu.py")
_file_mgr_mod    = _load_from_here("file_manager", "file_manager.py")
_sys_tray_mod    = _load_from_here("system_tray",  "system_tray.py")

KDETaskbar      = _taskbar_mod.KDETaskbar
KDEStartMenu    = _start_menu_mod.KDEStartMenu
KDEFileManager  = _file_mgr_mod.KDEFileManager
KDESystemTray   = _sys_tray_mod.KDESystemTray


class KDEUI:
    """
    Façade that assembles the full KDE Plasma desktop scene.
    """

    def __init__(self):
        print("[KDEUI] 🔵 Loading KDE Plasma UI components...")
        self.taskbar = KDETaskbar()
        self.start_menu = KDEStartMenu()
        self.file_manager = KDEFileManager()
        self.system_tray = KDESystemTray()
        print("[KDEUI] ✅ KDE Plasma UI ready.")

    def render_desktop(self) -> str:
        """
        Renders a full KDE Plasma desktop scene.

        Returns:
            str: Multi-line description of the KDE desktop.
        """
        print("\n[KDEUI] Rendering KDE Plasma desktop...")
        parts = [
            "=" * 60,
            "  🔵  WekezaOmniOS — KDE Plasma Desktop Environment",
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
    "KDETaskbar",
    "KDEStartMenu",
    "KDEFileManager",
    "KDESystemTray",
    "KDEUI",
]
