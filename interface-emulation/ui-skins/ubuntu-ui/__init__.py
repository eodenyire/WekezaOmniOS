"""
WekezaOmniOS Interface Emulation — Ubuntu UI Package
=====================================================
Ubuntu (Unity/GNOME) desktop environment components and a UbuntuUI
façade that renders a complete desktop scene.
"""

import os
import sys
import importlib.util


def _load_from_here(name: str, filename: str):
    """Loads a submodule from this package's directory by file path."""
    _here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        f"ubuntu_ui.{name}", os.path.join(_here, filename)
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_taskbar_mod     = _load_from_here("taskbar",      "taskbar.py")
_start_menu_mod  = _load_from_here("start_menu",   "start_menu.py")
_file_mgr_mod    = _load_from_here("file_manager", "file_manager.py")
_sys_tray_mod    = _load_from_here("system_tray",  "system_tray.py")

UbuntuTaskbar      = _taskbar_mod.UbuntuTaskbar
UbuntuStartMenu    = _start_menu_mod.UbuntuStartMenu
UbuntuFileManager  = _file_mgr_mod.UbuntuFileManager
UbuntuSystemTray   = _sys_tray_mod.UbuntuSystemTray


class UbuntuUI:
    """
    Façade that assembles the full Ubuntu desktop scene.
    """

    def __init__(self):
        print("[UbuntuUI] 🐧 Loading Ubuntu UI components...")
        self.taskbar = UbuntuTaskbar()
        self.start_menu = UbuntuStartMenu()
        self.file_manager = UbuntuFileManager()
        self.system_tray = UbuntuSystemTray()
        print("[UbuntuUI] ✅ Ubuntu UI ready.")

    def render_desktop(self) -> str:
        """
        Renders a full Ubuntu desktop scene.

        Returns:
            str: Multi-line description of the Ubuntu desktop.
        """
        print("\n[UbuntuUI] Rendering Ubuntu desktop...")
        parts = [
            "=" * 60,
            "  🐧  WekezaOmniOS — Ubuntu Desktop Environment",
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
    "UbuntuTaskbar",
    "UbuntuStartMenu",
    "UbuntuFileManager",
    "UbuntuSystemTray",
    "UbuntuUI",
]
