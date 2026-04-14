"""
WekezaOmniOS Interface Emulation — macOS Taskbar (Dock + Menu Bar)
==================================================================
Simulates the macOS Dock at the bottom and the menu bar at the top.
"""


_DEFAULT_DOCK = [
    "Finder", "Safari", "Mail", "Calendar", "Maps",
    "Photos", "FaceTime", "Messages", "Music", "System Settings",
]


class MacOSTaskbar:
    """
    Emulated macOS Dock (bottom) and menu bar (top).
    """

    def __init__(self):
        print("[MacOSTaskbar] Initialising macOS Dock...")
        self._dock: list[str] = list(_DEFAULT_DOCK)

    def render(self) -> str:
        """
        Returns a string showing the macOS Dock and menu bar.

        Returns:
            str: Dock + menu bar scene.
        """
        icons = "  ".join(f"[{a}]" for a in self._dock)
        bar = (
            "[Menu Bar] 🍎 Apple  Finder  File  Edit  View  Go  Window  Help"
            f"{'':>10} 🔊 WiFi 🔋 🕐12:00\n"
            f"[Dock] {icons}"
        )
        print("[MacOSTaskbar] Rendered Dock and menu bar.")
        return bar

    def pin_app(self, app_name: str) -> None:
        """Adds *app_name* to the Dock."""
        if app_name not in self._dock:
            self._dock.append(app_name)
            print(f"[MacOSTaskbar] Added '{app_name}' to Dock.")

    def unpin_app(self, app_name: str) -> None:
        """Removes *app_name* from the Dock."""
        if app_name in self._dock:
            self._dock.remove(app_name)
            print(f"[MacOSTaskbar] Removed '{app_name}' from Dock.")
