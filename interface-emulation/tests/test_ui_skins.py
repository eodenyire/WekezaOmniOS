"""
WekezaOmniOS Interface Emulation — UI Skins Tests
==================================================
pytest tests for all four UI skin environments.
"""

import os
import sys
import importlib.util
import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SKINS = os.path.join(_BASE, "ui-skins")


def _load_ui_module(skin_dir: str, mod_name: str):
    """Helper: load a __init__.py from a skin subdirectory."""
    init_path = os.path.join(_SKINS, skin_dir, "__init__.py")
    for subdir in (
        os.path.join(_SKINS, skin_dir),
    ):
        if subdir not in sys.path:
            sys.path.insert(0, subdir)
    spec = importlib.util.spec_from_file_location(mod_name, init_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ===========================================================================
# Windows UI
# ===========================================================================

class TestWindowsUI:

    def setup_method(self):
        mod = _load_ui_module("windows-ui", "windows_ui")
        self.ui = mod.WindowsUI()
        self.taskbar = mod.WindowsTaskbar()
        self.start_menu = mod.WindowsStartMenu()
        self.file_manager = mod.WindowsFileManager()

    def test_render_desktop_nonempty(self):
        result = self.ui.render_desktop()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_desktop_contains_header(self):
        result = self.ui.render_desktop()
        assert "Windows" in result

    def test_taskbar_render(self):
        result = self.taskbar.render()
        assert "Start" in result

    def test_taskbar_pin_app(self):
        self.taskbar.pin_app("Notepad")
        assert "Notepad" in self.taskbar._pinned

    def test_taskbar_pin_duplicate_no_double(self):
        self.taskbar.pin_app("Edge")  # already default
        assert self.taskbar._pinned.count("Edge") == 1

    def test_taskbar_unpin_app(self):
        self.taskbar.pin_app("TestApp")
        self.taskbar.unpin_app("TestApp")
        assert "TestApp" not in self.taskbar._pinned

    def test_start_menu_render(self):
        result = self.start_menu.render()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_start_menu_search_found(self):
        results = self.start_menu.search("note")
        assert any("Notepad" in r for r in results)

    def test_start_menu_search_case_insensitive(self):
        results = self.start_menu.search("NOTEPAD")
        assert len(results) > 0

    def test_start_menu_search_no_match(self):
        results = self.start_menu.search("xyznonexistent")
        assert results == []

    def test_file_manager_render(self):
        result = self.file_manager.render()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_file_manager_navigate(self):
        self.file_manager.navigate("C:\\Windows")
        assert self.file_manager._path == "C:\\Windows"

    def test_file_manager_list_items(self):
        self.file_manager.navigate("C:\\Users")
        items = self.file_manager.list_items()
        assert isinstance(items, list)
        assert len(items) > 0


# ===========================================================================
# Ubuntu UI
# ===========================================================================

class TestUbuntuUI:

    def setup_method(self):
        mod = _load_ui_module("ubuntu-ui", "ubuntu_ui")
        self.ui = mod.UbuntuUI()

    def test_render_desktop_nonempty(self):
        result = self.ui.render_desktop()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_desktop_contains_ubuntu(self):
        result = self.ui.render_desktop()
        assert "Ubuntu" in result


# ===========================================================================
# KDE UI
# ===========================================================================

class TestKDEUI:

    def setup_method(self):
        mod = _load_ui_module("kde-ui", "kde_ui")
        self.ui = mod.KDEUI()

    def test_render_desktop_nonempty(self):
        result = self.ui.render_desktop()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_desktop_contains_kde(self):
        result = self.ui.render_desktop()
        assert "KDE" in result


# ===========================================================================
# macOS UI
# ===========================================================================

class TestMacOSUI:

    def setup_method(self):
        mod = _load_ui_module("macos-style", "macos_ui")
        self.ui = mod.MacOSUI()

    def test_render_desktop_nonempty(self):
        result = self.ui.render_desktop()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_desktop_contains_macos(self):
        result = self.ui.render_desktop()
        assert "macOS" in result
