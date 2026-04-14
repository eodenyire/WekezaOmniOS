"""
WekezaOmniOS Interface Emulation — Ubuntu System Tray
======================================================
Simulates the GNOME top-bar notification / system indicators.
"""


_DEFAULT_ICONS = [
    "NetworkManager", "Bluetooth", "Sound",
    "Battery", "Calendar", "UserMenu",
]


class UbuntuSystemTray:
    """
    Emulated GNOME / Ubuntu system tray (top-bar indicators).
    """

    def __init__(self):
        print("[UbuntuSystemTray] Initialising system tray...")
        self._icons: list[str] = list(_DEFAULT_ICONS)

    def render(self) -> str:
        """
        Returns a string representation of the GNOME top bar.

        Returns:
            str: System tray scene.
        """
        icons_str = "  ".join(f"[{i}]" for i in self._icons)
        tray = (
            f"[TopBar] Activities  Applications  Places  "
            f"{icons_str}  🕐 12:00"
        )
        print(f"[UbuntuSystemTray] {tray}")
        return tray

    def add_icon(self, name: str) -> None:
        """Adds *name* to the indicator area."""
        if name not in self._icons:
            self._icons.append(name)
            print(f"[UbuntuSystemTray] Added indicator: {name}")

    def remove_icon(self, name: str) -> None:
        """Removes *name* from the indicator area."""
        if name in self._icons:
            self._icons.remove(name)
            print(f"[UbuntuSystemTray] Removed indicator: {name}")

    def list_icons(self) -> list[str]:
        """Returns current indicator names."""
        return list(self._icons)
