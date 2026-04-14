"""
WekezaOmniOS Interface Emulation — Integration Tests
=====================================================
pytest integration tests for the top-level InterfaceEmulation class.
"""

import os
import sys
import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

from interface_emulation import InterfaceEmulation


class TestInterfaceEmulation:

    def setup_method(self):
        self.ie = InterfaceEmulation(host_os="linux", initial_skin="ubuntu")

    def test_init_creates_instance(self):
        assert self.ie is not None

    def test_host_os_set(self):
        assert self.ie.host_os == "linux"

    def test_initial_skin_loaded(self):
        assert self.ie.desktop.current_environment == "ubuntu"

    def test_launch_app_returns_pid(self):
        pid = self.ie.launch_app("bash", os_type="linux")
        assert isinstance(pid, int)
        assert pid >= 1000

    def test_launch_app_stored_in_process_manager(self):
        pid = self.ie.launch_app("test_app", os_type="windows")
        proc = self.ie.process_mgr.get_process(pid)
        assert proc is not None
        assert proc["name"] == "test_app"

    def test_translate_command_windows(self):
        result = self.ie.translate_command("dir", source_os="windows")
        assert result == "ls"

    def test_translate_command_unknown(self):
        result = self.ie.translate_command("unknowncmd", source_os="windows")
        assert result == "unknowncmd"

    def test_translate_command_macos(self):
        result = self.ie.translate_command("open", source_os="macos")
        assert result == "xdg-open"

    def test_switch_ui_returns_skin(self):
        skin = self.ie.switch_ui("windows")
        assert skin is not None

    def test_switch_ui_updates_current_env(self):
        self.ie.switch_ui("kde")
        assert self.ie.desktop.current_environment == "kde"

    def test_switch_ui_macos(self):
        self.ie.switch_ui("macos")
        assert self.ie.desktop.current_environment == "macos"

    def test_load_binary_windows_exe(self):
        result = self.ie.load_binary("C:\\App\\app.exe", os_type="windows")
        assert isinstance(result, dict)
        assert result.get("format") == "PE32+"

    def test_load_binary_linux_elf(self):
        result = self.ie.load_binary("/usr/bin/bash", os_type="linux")
        assert isinstance(result, dict)
        assert result.get("format") == "ELF64"

    def test_load_binary_android_apk(self):
        result = self.ie.load_binary("/opt/app.apk", os_type="android")
        assert isinstance(result, dict)
        assert "APK" in result.get("format", "")

    def test_load_binary_unknown_os_returns_empty(self):
        result = self.ie.load_binary("/some/binary", os_type="unknown_os")
        assert result == {}

    def test_status_runs_without_error(self, capsys):
        self.ie.status()
        captured = capsys.readouterr()
        assert "Status Report" in captured.out

    def test_filesystem_accessible(self):
        self.ie.filesystem.mount("/dev/sda1", "/", "ext4")
        assert self.ie.filesystem.exists("/")

    def test_network_accessible(self):
        self.ie.network.add_interface("eth0", "10.0.0.1")
        ifaces = self.ie.network.list_interfaces()
        assert len(ifaces) >= 1
