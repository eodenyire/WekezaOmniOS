"""
WekezaOmniOS Interface Emulation — Ubuntu Taskbar (Unity Dock)
===============================================================
Simulates the Ubuntu Unity-style launcher dock on the left side of
the screen.
"""


_DEFAULT_DOCK = [
    "Files", "Firefox", "Thunderbird", "LibreOffice",
    "Settings", "Terminal", "Software Center",
]


class UbuntuTaskbar:
    """
    Emulated Ubuntu Unity dock / GNOME taskbar.
    """

    def __init__(self):
        print("[UbuntuTaskbar] Initialising Ubuntu dock...")
        self._dock: list[str] = list(_DEFAULT_DOCK)

    def render(self) -> str:
        """
        Returns a string showing the Unity-style left-side dock.

        Returns:
            str: Dock scene.
        """
        icons = "\n".join(f"  ║  {app}" for app in self._dock)
        bar = (
            "╔═ Ubuntu Dock ═╗\n"
            f"{icons}\n"
            "║  [Show Apps]  ║\n"
            "╚═══════════════╝"
        )
        print("[UbuntuTaskbar] Rendered Ubuntu dock.")
        return bar

    def pin_app(self, app_name: str) -> None:
        """Pins *app_name* to the dock."""
        if app_name not in self._dock:
            self._dock.append(app_name)
            print(f"[UbuntuTaskbar] Pinned '{app_name}' to dock.")

    def unpin_app(self, app_name: str) -> None:
        """Unpins *app_name* from the dock."""
        if app_name in self._dock:
            self._dock.remove(app_name)
            print(f"[UbuntuTaskbar] Unpinned '{app_name}' from dock.")
