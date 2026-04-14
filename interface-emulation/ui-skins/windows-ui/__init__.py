"""
WekezaOmniOS Interface Emulation — Windows UI Package
======================================================
Provides Windows 11-style desktop environment components and a
WindowsUI façade that renders a complete desktop scene.
"""

import os
import sys
import importlib.util


def _load_from_here(name: str, filename: str):
    """Loads a submodule from this package's directory by file path."""
    _here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        f"windows_ui.{name}", os.path.join(_here, filename)
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_taskbar_mod     = _load_from_here("taskbar",      "taskbar.py")
_start_menu_mod  = _load_from_here("start_menu",   "start_menu.py")
_file_mgr_mod    = _load_from_here("file_manager", "file_manager.py")
_sys_tray_mod    = _load_from_here("system_tray",  "system_tray.py")

WindowsTaskbar      = _taskbar_mod.WindowsTaskbar
WindowsStartMenu    = _start_menu_mod.WindowsStartMenu
WindowsFileManager  = _file_mgr_mod.WindowsFileManager
WindowsSystemTray   = _sys_tray_mod.WindowsSystemTray


class WindowsUI:
    """
    Façade that assembles the full Windows desktop scene by composing
    all four Windows UI components.
    """

    def __init__(self):
        print("[WindowsUI] 🪟 Loading Windows UI components...")
        self.taskbar = WindowsTaskbar()
        self.start_menu = WindowsStartMenu()
        self.file_manager = WindowsFileManager()
        self.system_tray = WindowsSystemTray()
        print("[WindowsUI] ✅ Windows UI ready.")

    def render_desktop(self) -> str:
        """
        Renders a full Windows desktop scene.

        Returns:
            str: Multi-line description of the Windows desktop.
        """
        print("\n[WindowsUI] Rendering Windows desktop...")
        parts = [
            "=" * 60,
            "  🪟  WekezaOmniOS — Windows Desktop Environment",
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
    "WindowsTaskbar",
    "WindowsStartMenu",
    "WindowsFileManager",
    "WindowsSystemTray",
    "WindowsUI",
]
