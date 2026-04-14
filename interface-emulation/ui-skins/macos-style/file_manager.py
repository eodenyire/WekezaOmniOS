"""
WekezaOmniOS Interface Emulation — macOS File Manager (Finder)
==============================================================
Simulates the macOS Finder with a column-view sidebar and fake tree.
"""


_FAKE_TREE: dict[str, list[str]] = {
    "/Users/user": [
        "Desktop", "Documents", "Downloads", "Movies",
        "Music", "Pictures", "Public", "Library",
    ],
    "/Users/user/Documents": [
        "Report.pages", "Budget.numbers", "Presentation.key",
        "OmniOS Notes.txt",
    ],
    "/Users/user/Downloads": [
        "macOS-Sonoma.dmg", "archive.zip", "photo.heic",
    ],
    "/": [
        "Applications", "Library", "System", "Users",
        "Volumes", "private", "usr",
    ],
}

_DEFAULT_PATH = "/Users/user"


class MacOSFileManager:
    """
    Emulated macOS Finder file manager component.
    """

    def __init__(self):
        print("[MacOSFileManager] Initialising Finder...")
        self._path: str = _DEFAULT_PATH

    def render(self, path: str = "/Users/user") -> str:
        """
        Returns a Finder-style directory listing for *path*.

        Args:
            path (str): macOS path to display.

        Returns:
            str: Finder scene.
        """
        self._path = path
        items = self.list_items()
        rows = "\n".join(f"│  📄  {item}" for item in items)
        view = (
            f"┌─ Finder — {self._path} ─────────────────────────────┐\n"
            "│ Sidebar: Favourites | iCloud | Locations | Tags     │\n"
            f"{rows}\n"
            "└──────────────────────────────────────────────────────┘"
        )
        print(f"[MacOSFileManager] Rendered path: {self._path}")
        return view

    def navigate(self, path: str) -> None:
        """Navigates to *path*."""
        self._path = path
        print(f"[MacOSFileManager] Navigated to {self._path}")

    def list_items(self) -> list[str]:
        """Returns fake directory entries for the current path."""
        return _FAKE_TREE.get(self._path, ["(empty folder)"])
