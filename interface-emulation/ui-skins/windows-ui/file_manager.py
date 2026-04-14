"""
WekezaOmniOS Interface Emulation — Windows File Manager
========================================================
Simulates a Windows Explorer-style file manager with fake directory
listings and path navigation.
"""


_FAKE_TREE: dict[str, list[str]] = {
    "C:\\Users": ["Public", "Default", "Alice", "Bob"],
    "C:\\Users\\Alice": [
        "Desktop", "Documents", "Downloads", "Music",
        "Pictures", "Videos", "AppData",
    ],
    "C:\\Windows": ["System32", "SysWOW64", "Temp", "Fonts", "explorer.exe"],
    "C:\\Program Files": [
        "Microsoft Office", "Google", "Mozilla Firefox",
        "Windows NT", "Common Files",
    ],
}

_DEFAULT_PATH = "C:\\Users"


class WindowsFileManager:
    """
    Emulated Windows Explorer (file manager) component.

    Maintains a current working path and provides a fake directory
    listing that mirrors a typical Windows installation.
    """

    def __init__(self):
        print("[WindowsFileManager] Initialising file manager...")
        self._path: str = _DEFAULT_PATH

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, path: str = "C:\\Users") -> str:
        """
        Returns a Windows Explorer-style directory listing for *path*.

        Args:
            path (str): Windows path to display.

        Returns:
            str: Explorer listing scene.
        """
        self._path = path
        items = self.list_items()
        rows = "\n".join(f"│  📁  {item}" for item in items)
        view = (
            f"┌─ Windows Explorer — {self._path} ─┐\n"
            f"{rows}\n"
            "└──────────────────────────────────────┘"
        )
        print(f"[WindowsFileManager] Rendered path: {self._path}")
        return view

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self, path: str) -> None:
        """
        Changes the current path.

        Args:
            path (str): New Windows path to navigate to.
        """
        self._path = path
        print(f"[WindowsFileManager] Navigated to {self._path}")

    def list_items(self) -> list[str]:
        """
        Returns a fake directory listing for the current path.

        Returns:
            list[str]: Directory / file names.
        """
        return _FAKE_TREE.get(
            self._path, ["This PC", "Network", "Recycle Bin"]
        )
