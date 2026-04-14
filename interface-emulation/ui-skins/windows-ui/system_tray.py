"""
WekezaOmniOS Interface Emulation — Windows System Tray
=======================================================
Simulates the Windows notification area (system tray) with a managed
set of tray icons.
"""


_DEFAULT_ICONS = ["Network", "Volume", "Battery", "OneDrive", "Antivirus"]


class WindowsSystemTray:
    """
    Emulated Windows system-tray / notification area.
    """

    def __init__(self):
        print("[WindowsSystemTray] Initialising system tray...")
        self._icons: list[str] = list(_DEFAULT_ICONS)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self) -> str:
        """
        Returns a string representation of the system tray.

        Returns:
            str: System tray scene.
        """
        icons_str = "  ".join(f"[{i}]" for i in self._icons)
        tray = f"[SysTray] {icons_str}  | 🕐 12:00 | 📅 Mon"
        print(f"[WindowsSystemTray] {tray}")
        return tray

    # ------------------------------------------------------------------
    # Icon management
    # ------------------------------------------------------------------

    def add_icon(self, name: str) -> None:
        """Adds *name* to the tray."""
        if name not in self._icons:
            self._icons.append(name)
            print(f"[WindowsSystemTray] Added icon: {name}")

    def remove_icon(self, name: str) -> None:
        """Removes *name* from the tray."""
        if name in self._icons:
            self._icons.remove(name)
            print(f"[WindowsSystemTray] Removed icon: {name}")

    def list_icons(self) -> list[str]:
        """Returns the current list of tray icon names."""
        return list(self._icons)
