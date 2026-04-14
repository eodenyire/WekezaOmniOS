"""
WekezaOmniOS Interface Emulation — Command Translator
======================================================
Translates individual or batched shell commands from Windows, macOS,
or cmd source environments into their Linux shell equivalents.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from command_table import COMMAND_TABLES


class CommandTranslator:
    """
    Translates shell commands from a source OS into Linux equivalents.

    For known source OSes, looks up the command in the pre-built table.
    Unknown commands are returned unchanged with a warning.
    """

    def __init__(self, source_os: str = "windows"):
        """
        Args:
            source_os (str): Source OS whose commands need translating
                             ('windows', 'macos', 'cmd').
        """
        self.source_os = source_os.lower()
        self._table: dict[str, str] = COMMAND_TABLES.get(self.source_os, {})
        print(
            f"[CommandTranslator] Initialised for source OS: {self.source_os} "
            f"({len(self._table)} mappings loaded)"
        )

    # ------------------------------------------------------------------
    # Core translation
    # ------------------------------------------------------------------

    def translate(self, cmd: str) -> str:
        """
        Translates a single command.

        Args:
            cmd (str): Source-OS command name.

        Returns:
            str: Linux equivalent, or the original if no mapping exists.
        """
        translated = self._table.get(cmd.lower())
        if translated:
            print(
                f"[CommandTranslator] {self.source_os}: "
                f"{cmd!r} → {translated!r}"
            )
            return translated

        print(
            f"[CommandTranslator] ⚠️  No mapping for {cmd!r} "
            f"(source={self.source_os}) — passing through unchanged."
        )
        return cmd

    def translate_batch(self, cmds: list[str]) -> list[dict]:
        """
        Translates a list of commands in one pass.

        Args:
            cmds (list[str]): Commands to translate.

        Returns:
            list[dict]: Each entry has 'source' and 'translated' keys.
        """
        return [{"source": c, "translated": self.translate(c)} for c in cmds]

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def list_mappings(self) -> dict[str, str]:
        """
        Returns the full command mapping dictionary for the source OS.

        Returns:
            dict[str, str]: Source command → Linux equivalent.
        """
        return dict(self._table)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ct = CommandTranslator(source_os="windows")
    for cmd in ["dir", "copy", "tasklist", "shutdown", "unknown_cmd"]:
        ct.translate(cmd)

    print("\n--- Batch ---")
    results = ct.translate_batch(["dir", "del", "ping"])
    for r in results:
        print(f"  {r['source']:15s} → {r['translated']}")

    print("\n--- macOS ---")
    mac = CommandTranslator(source_os="macos")
    mac.translate("open")
    mac.translate("pbcopy")
