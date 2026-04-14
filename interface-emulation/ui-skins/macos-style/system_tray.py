"""
WekezaOmniOS Interface Emulation — macOS System Tray (Menu Bar Extras)
======================================================================
Simulates the macOS menu bar extras (right side of the menu bar).
"""


_DEFAULT_ICONS = [
    "WiFi", "Bluetooth", "AirDrop",
    "Battery", "TimeMachine", "Spotlight",
]


class MacOSSystemTray:
    """
    Emulated macOS menu bar extras / status items.
    """

    def __init__(self):
        print("[MacOSSystemTray] Initialising menu bar extras...")
        self._icons: list[str] = list(_DEFAULT_ICONS)

    def render(self) -> str:
        """
        Returns a string representation of the macOS menu bar extras.

        Returns:
            str: Menu bar extras scene.
        """
        icons_str = "  ".join(f"[{i}]" for i in self._icons)
        tray = f"[Menu Bar Extras] {icons_str}  🔍 Spotlight  🕐 12:00  Fri"
        print(f"[MacOSSystemTray] {tray}")
        return tray

    def add_icon(self, name: str) -> None:
        """Adds *name* to the menu bar extras."""
        if name not in self._icons:
            self._icons.append(name)
            print(f"[MacOSSystemTray] Added menu bar extra: {name}")

    def remove_icon(self, name: str) -> None:
        """Removes *name* from the menu bar extras."""
        if name in self._icons:
            self._icons.remove(name)
            print(f"[MacOSSystemTray] Removed menu bar extra: {name}")

    def list_icons(self) -> list[str]:
        """Returns current menu bar extra names."""
        return list(self._icons)
