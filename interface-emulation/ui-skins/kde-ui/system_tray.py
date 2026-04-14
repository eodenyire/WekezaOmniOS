"""
WekezaOmniOS Interface Emulation — KDE System Tray
===================================================
Simulates the KDE Plasma system-tray notification area.
"""


_DEFAULT_ICONS = [
    "NetworkManager", "Bluetooth", "Volume",
    "Battery", "Clipboard", "Notifications",
]


class KDESystemTray:
    """
    Emulated KDE Plasma system-tray area.
    """

    def __init__(self):
        print("[KDESystemTray] Initialising KDE system tray...")
        self._icons: list[str] = list(_DEFAULT_ICONS)

    def render(self) -> str:
        """
        Returns a string representation of the KDE system tray.

        Returns:
            str: System tray scene.
        """
        icons_str = "  ".join(f"[{i}]" for i in self._icons)
        tray = f"[KDE SysTray] {icons_str}  🕐 12:00  📅"
        print(f"[KDESystemTray] {tray}")
        return tray

    def add_icon(self, name: str) -> None:
        """Adds *name* to the tray."""
        if name not in self._icons:
            self._icons.append(name)
            print(f"[KDESystemTray] Added icon: {name}")

    def remove_icon(self, name: str) -> None:
        """Removes *name* from the tray."""
        if name in self._icons:
            self._icons.remove(name)
            print(f"[KDESystemTray] Removed icon: {name}")

    def list_icons(self) -> list[str]:
        """Returns current tray icon names."""
        return list(self._icons)
