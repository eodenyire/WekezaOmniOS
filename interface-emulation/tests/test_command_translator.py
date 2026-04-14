"""
WekezaOmniOS Interface Emulation — Command Translator Tests
============================================================
pytest tests for CommandTranslator.
"""

import os
import sys
import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_BASE, "command-translator"))

from command_translator import CommandTranslator


class TestCommandTranslator:

    def setup_method(self):
        self.ct = CommandTranslator(source_os="windows")

    def test_translate_dir(self):
        assert self.ct.translate("dir") == "ls"

    def test_translate_copy(self):
        assert self.ct.translate("copy") == "cp"

    def test_translate_move(self):
        assert self.ct.translate("move") == "mv"

    def test_translate_del(self):
        assert self.ct.translate("del") == "rm"

    def test_translate_type(self):
        assert self.ct.translate("type") == "cat"

    def test_translate_cls(self):
        assert self.ct.translate("cls") == "clear"

    def test_translate_tasklist(self):
        assert self.ct.translate("tasklist") == "ps aux"

    def test_translate_taskkill(self):
        assert self.ct.translate("taskkill") == "kill"

    def test_translate_ipconfig(self):
        assert self.ct.translate("ipconfig") == "ifconfig"

    def test_translate_shutdown(self):
        assert self.ct.translate("shutdown") == "shutdown"

    def test_translate_unknown_returns_unchanged(self):
        assert self.ct.translate("unknowncmd") == "unknowncmd"

    def test_translate_case_insensitive(self):
        assert self.ct.translate("DIR") == "ls"

    def test_translate_batch(self):
        results = self.ct.translate_batch(["dir", "copy", "move"])
        assert len(results) == 3
        assert results[0] == {"source": "dir", "translated": "ls"}
        assert results[1] == {"source": "copy", "translated": "cp"}
        assert results[2] == {"source": "move", "translated": "mv"}

    def test_translate_batch_with_unknown(self):
        results = self.ct.translate_batch(["dir", "unknowncmd"])
        assert results[1]["translated"] == "unknowncmd"

    def test_list_mappings_returns_dict(self):
        mappings = self.ct.list_mappings()
        assert isinstance(mappings, dict)
        assert "dir" in mappings
        assert mappings["dir"] == "ls"

    def test_list_mappings_copy(self):
        assert self.ct.list_mappings()["copy"] == "cp"

    def test_macos_translator(self):
        mac = CommandTranslator(source_os="macos")
        assert mac.translate("open") == "xdg-open"
        assert mac.translate("pbcopy") == "xclip -selection clipboard"

    def test_cmd_alias_same_as_windows(self):
        cmd_ct = CommandTranslator(source_os="cmd")
        assert cmd_ct.translate("dir") == "ls"

    def test_unknown_os_unknown_cmd_passthrough(self):
        ct = CommandTranslator(source_os="freebsd")
        assert ct.translate("ls") == "ls"
