"""
WekezaOmniOS Interface Emulation — KDE Start Menu (KRunner / Launcher)
======================================================================
Simulates the KDE Application Launcher and KRunner quick-search.
"""


_APP_LIST = [
    "Dolphin", "Konsole", "Kate", "Firefox", "Thunderbird",
    "KCalc", "Spectacle", "Gwenview", "Okular", "KMail",
    "Plasma Settings", "Discover", "Ark", "KTorrent",
    "LibreOffice", "VLC", "GIMP", "Kdenlive",
]


class KDEStartMenu:
    """
    Emulated KDE Application Launcher / KRunner.
    """

    def __init__(self):
        print("[KDEStartMenu] Initialising Application Launcher...")
        self._apps = list(_APP_LIST)

    def render(self) -> str:
        """
        Returns a string showing the KDE Application Launcher.

        Returns:
            str: Launcher scene.
        """
        favourites = "  ".join(f"[{a}]" for a in self._apps[:6])
        menu = (
            "┌─ KDE Application Launcher ────────────────────────┐\n"
            f"│ Favourites: {favourites}\n"
            "│ All Applications ▶                               │\n"
            "│ [KRunner: Alt+F2 — Run command or search...]     │\n"
            "└──────────────────────────────────────────────────┘"
        )
        print("[KDEStartMenu] Rendered Application Launcher.")
        return menu

    def search(self, query: str) -> list[str]:
        """
        Searches apps by *query* (case-insensitive).

        Args:
            query (str): Search string.

        Returns:
            list[str]: Matching application names.
        """
        results = [a for a in self._apps if query.lower() in a.lower()]
        print(f"[KDEStartMenu] KRunner '{query}' → {len(results)} result(s).")
        return results
