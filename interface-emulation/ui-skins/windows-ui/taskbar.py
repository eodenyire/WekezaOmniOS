"""
WekezaOmniOS Interface Emulation — Windows Taskbar
===================================================
Simulates the Windows 11 taskbar with a centred Start button,
pinned application icons, a clock, and a system-tray area.
"""


_DEFAULT_PINNED = ["File Explorer", "Edge", "Settings", "Mail", "Calendar"]


class WindowsTaskbar:
    """
    Emulated Windows taskbar component.

    Manages a list of pinned application shortcuts and renders a
    text-based representation of the taskbar strip.
    """

    def __init__(self):
        print("[WindowsTaskbar] Initialising taskbar...")
        self._pinned: list[str] = list(_DEFAULT_PINNED)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self) -> str:
        """
        Returns a string description of the Windows taskbar.

        Returns:
            str: Taskbar scene.
        """
        pinned_str = "  |  ".join(self._pinned)
        bar = (
            f"[Taskbar] ▐ Start ▌  {pinned_str}  "
            f"{'':>10} 🔊  🌐  🔋  🕐 12:00"
        )
        print(f"[WindowsTaskbar] {bar}")
        return bar

    # ------------------------------------------------------------------
    # Pin management
    # ------------------------------------------------------------------

    def pin_app(self, app_name: str) -> None:
        """
        Pins *app_name* to the taskbar.

        Args:
            app_name (str): Application display name.
        """
        if app_name not in self._pinned:
            self._pinned.append(app_name)
            print(f"[WindowsTaskbar] Pinned '{app_name}' to taskbar.")
        else:
            print(f"[WindowsTaskbar] '{app_name}' is already pinned.")

    def unpin_app(self, app_name: str) -> None:
        """
        Unpins *app_name* from the taskbar.

        Args:
            app_name (str): Application display name.
        """
        if app_name in self._pinned:
            self._pinned.remove(app_name)
            print(f"[WindowsTaskbar] Unpinned '{app_name}' from taskbar.")
        else:
            print(f"[WindowsTaskbar] '{app_name}' is not pinned.")
