"""
WekezaOmniOS Interface Emulation — Windows Start Menu
======================================================
Simulates the Windows 11 Start menu with a pinned-apps grid, a
recommended-files section, and a fuzzy search capability.
"""


_APP_LIST = [
    "Notepad", "Calculator", "Paint", "File Explorer", "Settings",
    "Task Manager", "Edge", "Mail", "Calendar", "Photos",
    "Camera", "Maps", "Weather", "Clock", "Snipping Tool",
    "Windows Terminal", "Visual Studio Code", "PowerShell",
]


class WindowsStartMenu:
    """
    Emulated Windows Start menu component.

    Renders a simplified text representation of the Windows 11 Start
    menu and supports a case-insensitive substring search.
    """

    def __init__(self):
        print("[WindowsStartMenu] Initialising start menu...")
        self._apps = list(_APP_LIST)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self) -> str:
        """
        Returns a string showing the Windows-style Start menu.

        Returns:
            str: Start menu scene.
        """
        pinned = "  ".join(f"[{a}]" for a in self._apps[:6])
        menu = (
            "┌─ Start Menu ─────────────────────────────────────┐\n"
            f"│ Pinned: {pinned}\n"
            "│ Recommended: Recent documents / frequent apps    │\n"
            "│ [Search bar: Type here to search...]             │\n"
            "└──────────────────────────────────────────────────┘"
        )
        print(f"[WindowsStartMenu] Rendered Start menu.")
        return menu

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, query: str) -> list[str]:
        """
        Returns apps whose names contain *query* (case-insensitive).

        Args:
            query (str): Search string.

        Returns:
            list[str]: Matching application names.
        """
        results = [a for a in self._apps if query.lower() in a.lower()]
        print(
            f"[WindowsStartMenu] Search '{query}' → {len(results)} result(s)."
        )
        return results
