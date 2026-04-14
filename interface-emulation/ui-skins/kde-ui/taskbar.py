"""
WekezaOmniOS Interface Emulation — KDE Taskbar (Plasma Panel)
=============================================================
Simulates the KDE Plasma panel at the bottom of the screen with the
Application Launcher, taskbar, and system tray.
"""


_DEFAULT_PINNED = [
    "Dolphin", "Firefox", "Konsole", "Kate", "Discover",
]


class KDETaskbar:
    """
    Emulated KDE Plasma bottom panel.
    """

    def __init__(self):
        print("[KDETaskbar] Initialising Plasma panel...")
        self._pinned: list[str] = list(_DEFAULT_PINNED)

    def render(self) -> str:
        """
        Returns a string showing the KDE Plasma bottom panel.

        Returns:
            str: Panel scene.
        """
        pinned_str = "  |  ".join(self._pinned)
        bar = (
            f"[KDE Panel] ❯ Launcher ◀▶  {pinned_str}  "
            f"{'':>6} 🔊  🌐  🔋  🕐 12:00  🗓"
        )
        print(f"[KDETaskbar] {bar}")
        return bar

    def pin_app(self, app_name: str) -> None:
        """Pins *app_name* to the Plasma panel."""
        if app_name not in self._pinned:
            self._pinned.append(app_name)
            print(f"[KDETaskbar] Pinned '{app_name}'.")

    def unpin_app(self, app_name: str) -> None:
        """Unpins *app_name* from the Plasma panel."""
        if app_name in self._pinned:
            self._pinned.remove(app_name)
            print(f"[KDETaskbar] Unpinned '{app_name}'.")
