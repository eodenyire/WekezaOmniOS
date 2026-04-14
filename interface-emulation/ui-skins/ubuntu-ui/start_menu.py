"""
WekezaOmniOS Interface Emulation — Ubuntu Start Menu (Activities)
=================================================================
Simulates the GNOME Activities overview / application grid.
"""


_APP_LIST = [
    "Files", "Firefox", "Thunderbird", "Text Editor",
    "Terminal", "System Monitor", "Settings", "Software",
    "Calculator", "Calendar", "Contacts", "Clocks",
    "Rhythmbox", "Shotwell", "LibreOffice Writer",
    "LibreOffice Calc", "VLC", "GIMP",
]


class UbuntuStartMenu:
    """
    Emulated GNOME Activities overview / application launcher.
    """

    def __init__(self):
        print("[UbuntuStartMenu] Initialising Activities overview...")
        self._apps = list(_APP_LIST)

    def render(self) -> str:
        """
        Returns a string showing the GNOME Activities overview.

        Returns:
            str: Activities scene.
        """
        grid = "  ".join(f"[{a}]" for a in self._apps[:8])
        menu = (
            "┌─ Activities Overview ─────────────────────────────┐\n"
            f"│ Apps: {grid}\n"
            "│ [Search: Type to search apps and files...]        │\n"
            "│ Workspaces: [ 1 ] [ 2 ] [ 3 ] [ + ]              │\n"
            "└──────────────────────────────────────────────────┘"
        )
        print("[UbuntuStartMenu] Rendered Activities overview.")
        return menu

    def search(self, query: str) -> list[str]:
        """
        Returns apps matching *query* (case-insensitive substring).

        Args:
            query (str): Search string.

        Returns:
            list[str]: Matching application names.
        """
        results = [a for a in self._apps if query.lower() in a.lower()]
        print(
            f"[UbuntuStartMenu] Search '{query}' → {len(results)} result(s)."
        )
        return results
