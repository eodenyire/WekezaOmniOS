"""
WekezaOmniOS Interface Emulation — macOS Start Menu (Spotlight)
===============================================================
Simulates the macOS Spotlight search and Launchpad application grid.
"""


_APP_LIST = [
    "Finder", "Safari", "Mail", "Calendar", "Notes",
    "Reminders", "Maps", "Photos", "FaceTime", "Messages",
    "Music", "Podcasts", "TV", "App Store", "System Settings",
    "Terminal", "Xcode", "Pages", "Numbers", "Keynote",
]


class MacOSStartMenu:
    """
    Emulated macOS Spotlight search / Launchpad.
    """

    def __init__(self):
        print("[MacOSStartMenu] Initialising Spotlight / Launchpad...")
        self._apps = list(_APP_LIST)

    def render(self) -> str:
        """
        Returns a string showing the macOS Launchpad / Spotlight UI.

        Returns:
            str: Launchpad scene.
        """
        grid = "  ".join(f"[{a}]" for a in self._apps[:6])
        menu = (
            "┌─ Spotlight Search ───────────────────────────────┐\n"
            "│ 🔍 Search for apps, documents, and more...       │\n"
            "├─ Launchpad ──────────────────────────────────────┤\n"
            f"│ {grid}\n"
            "│ [More apps...]                                    │\n"
            "└──────────────────────────────────────────────────┘"
        )
        print("[MacOSStartMenu] Rendered Spotlight / Launchpad.")
        return menu

    def search(self, query: str) -> list[str]:
        """
        Searches Spotlight for *query* (case-insensitive).

        Args:
            query (str): Search string.

        Returns:
            list[str]: Matching application names.
        """
        results = [a for a in self._apps if query.lower() in a.lower()]
        print(
            f"[MacOSStartMenu] Spotlight '{query}' → {len(results)} result(s)."
        )
        return results
