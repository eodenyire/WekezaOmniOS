"""
WekezaOmniOS Interface Emulation — Compatibility Layer Tests
=============================================================
pytest tests for WindowsCompat, LinuxCompat, and AndroidCompat.
"""

import os
import sys
import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_BASE, "compatibility-layer", "windows_compat"))
sys.path.insert(0, os.path.join(_BASE, "compatibility-layer", "linux_compat"))
sys.path.insert(0, os.path.join(_BASE, "compatibility-layer", "android_compat"))

from windows_compat import WindowsCompat
from linux_compat import LinuxCompat
from android_compat import AndroidCompat


# ===========================================================================
# WindowsCompat
# ===========================================================================

class TestWindowsCompat:

    def setup_method(self):
        self.wc = WindowsCompat()

    def test_load_binary_exe(self):
        info = self.wc.load_binary("C:\\App\\app.exe")
        assert info["format"] == "PE32+"
        assert info["status"] == "loaded (emulated)"

    def test_load_binary_invalid_extension(self):
        with pytest.raises(ValueError):
            self.wc.load_binary("/usr/bin/notanexe")

    def test_load_binary_path_stored(self):
        info = self.wc.load_binary("C:\\test.exe")
        assert info["path"] == "C:\\test.exe"

    def test_translate_registry_hklm_software(self):
        result = self.wc.translate_registry_key(
            "HKLM\\SOFTWARE\\Microsoft\\Windows"
        )
        assert result.startswith("/etc/omnios/registry/software")

    def test_translate_registry_hkcu_software(self):
        result = self.wc.translate_registry_key("HKCU\\SOFTWARE\\App")
        assert "omnios" in result.lower()

    def test_translate_registry_unknown_key(self):
        result = self.wc.translate_registry_key("HKCR\\exefile")
        assert "omnios" in result.lower()

    def test_translate_path_c_users(self):
        result = self.wc.translate_path("C:\\Users\\Alice\\file.txt")
        assert result.startswith("/home/Alice")

    def test_translate_path_d_drive(self):
        result = self.wc.translate_path("D:\\Projects\\app")
        assert result.startswith("/mnt/d")

    def test_translate_path_backslashes_replaced(self):
        result = self.wc.translate_path("D:\\foo\\bar")
        assert "\\" not in result

    def test_emulate_api_createfile(self):
        result = self.wc.emulate_api("CreateFile", "data.txt")
        assert result == "open"

    def test_emulate_api_loadlibrary(self):
        result = self.wc.emulate_api("LoadLibrary", "kernel32.dll")
        assert result == "dlopen"

    def test_emulate_api_unknown(self):
        result = self.wc.emulate_api("SomeUnknownApi")
        assert "SomeUnknownApi" in result


# ===========================================================================
# LinuxCompat
# ===========================================================================

class TestLinuxCompat:

    def setup_method(self):
        self.lc = LinuxCompat()

    def test_load_binary_elf(self):
        info = self.lc.load_binary("/usr/bin/htop")
        assert info["format"] == "ELF64"
        assert info["status"] == "loaded (native)"

    def test_load_binary_path_stored(self):
        info = self.lc.load_binary("/bin/bash")
        assert info["path"] == "/bin/bash"

    def test_translate_path_identity(self):
        path = "/home/user/data.txt"
        assert self.lc.translate_path(path) == path

    def test_translate_path_root(self):
        assert self.lc.translate_path("/") == "/"

    def test_emulate_syscall_returns_string(self):
        result = self.lc.emulate_syscall("read", 3, "buf", 4096)
        assert isinstance(result, str)
        assert "read" in result

    def test_emulate_syscall_write(self):
        result = self.lc.emulate_syscall("write", 1, "hello", 5)
        assert "write" in result


# ===========================================================================
# AndroidCompat
# ===========================================================================

class TestAndroidCompat:

    def setup_method(self):
        self.ac = AndroidCompat()

    def test_load_apk(self):
        info = self.ac.load_apk("/opt/com.example.app.apk")
        assert "APK" in info["format"]
        assert "loaded" in info["status"]

    def test_load_apk_invalid_extension(self):
        with pytest.raises(ValueError):
            self.ac.load_apk("/opt/notanapk.zip")

    def test_load_apk_path_stored(self):
        info = self.ac.load_apk("/opt/test.apk")
        assert info["path"] == "/opt/test.apk"

    def test_translate_intent_view(self):
        result = self.ac.translate_intent(
            "android.intent.action.VIEW", "https://omnios.dev"
        )
        assert "xdg-open" in result

    def test_translate_intent_main(self):
        result = self.ac.translate_intent("android.intent.action.MAIN")
        assert result == "exec"

    def test_translate_intent_with_data(self):
        result = self.ac.translate_intent(
            "android.intent.action.VIEW", "https://example.com"
        )
        assert result == "xdg-open https://example.com"

    def test_translate_intent_unknown(self):
        result = self.ac.translate_intent("com.custom.action", "")
        assert isinstance(result, str)

    def test_emulate_api_notify(self):
        result = self.ac.emulate_api("NotificationManager.notify", "title")
        assert "notify-send" in result

    def test_emulate_api_unknown(self):
        result = self.ac.emulate_api("CustomAPI.doThing")
        assert isinstance(result, str)
