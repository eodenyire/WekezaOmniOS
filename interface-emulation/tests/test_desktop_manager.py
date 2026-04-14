"""
WekezaOmniOS Interface Emulation — Desktop Manager Tests
=========================================================
pytest tests for the DesktopManager.
"""

import os
import sys
import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_BASE, "desktop-manager"))

from desktop_manager import DesktopManager


class TestDesktopManager:

    def setup_method(self):
        self.dm = DesktopManager()

    def test_list_environments_count(self):
        envs = self.dm.list_environments()
        assert len(envs) >= 4

    def test_list_environments_contains_all(self):
        envs = self.dm.list_environments()
        for name in ("windows", "ubuntu", "kde", "macos"):
            assert name in envs

    def test_load_skin_windows(self):
        skin = self.dm.load_skin("windows")
        assert skin is not None
        assert hasattr(skin, "render_desktop")

    def test_load_skin_ubuntu(self):
        skin = self.dm.load_skin("ubuntu")
        assert skin is not None
        assert hasattr(skin, "render_desktop")

    def test_load_skin_kde(self):
        skin = self.dm.load_skin("kde")
        assert skin is not None
        assert hasattr(skin, "render_desktop")

    def test_load_skin_macos(self):
        skin = self.dm.load_skin("macos")
        assert skin is not None
        assert hasattr(skin, "render_desktop")

    def test_load_skin_unknown_raises(self):
        with pytest.raises(ValueError):
            self.dm.load_skin("unknown_os")

    def test_load_skin_sets_current_environment(self):
        self.dm.load_skin("ubuntu")
        assert self.dm.current_environment == "ubuntu"

    def test_load_skin_cached(self):
        skin1 = self.dm.load_skin("windows")
        skin2 = self.dm.load_skin("windows")
        assert skin1 is skin2

    def test_switch_environment(self):
        self.dm.load_skin("windows")
        self.dm.switch_environment("windows", "ubuntu")
        assert self.dm.current_environment == "ubuntu"

    def test_switch_environment_saves_workspace(self):
        self.dm.load_skin("windows")
        self.dm.switch_environment("windows", "ubuntu")
        assert "windows" in self.dm._workspaces

    def test_save_workspace(self):
        self.dm.save_workspace("kde")
        assert "kde" in self.dm._workspaces
        ws = self.dm._workspaces["kde"]
        assert ws["env"] == "kde"

    def test_restore_workspace_saved(self):
        self.dm.save_workspace("macos")
        restored = self.dm.restore_workspace("macos")
        assert restored["env"] == "macos"

    def test_restore_workspace_not_saved_returns_empty(self):
        result = self.dm.restore_workspace("neverset")
        assert result == {}

    def test_current_environment_initially_none(self):
        dm = DesktopManager()
        assert dm.current_environment is None

    def test_render_desktop_after_load(self):
        skin = self.dm.load_skin("windows")
        result = skin.render_desktop()
        assert isinstance(result, str)
        assert len(result) > 0
