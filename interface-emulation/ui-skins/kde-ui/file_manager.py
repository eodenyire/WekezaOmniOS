"""
WekezaOmniOS Interface Emulation — KDE File Manager (Dolphin)
=============================================================
Simulates a KDE Dolphin-style file manager with split-pane view.
"""


_FAKE_TREE: dict[str, list[str]] = {
    "/home/user": [
        "Desktop", "Documents", "Downloads", "Music",
        "Pictures", "Videos", "Public", ".kde",
    ],
    "/home/user/Documents": [
        "OmniOS Notes.odt", "Plasma Config.pdf", "Budget.ods",
    ],
    "/": [
        "bin", "boot", "dev", "etc", "home",
        "lib", "mnt", "opt", "proc", "usr", "var",
    ],
}

_DEFAULT_PATH = "/home/user"


class KDEFileManager:
    """
    Emulated Dolphin (KDE) file manager component.
    """

    def __init__(self):
        print("[KDEFileManager] Initialising Dolphin file manager...")
        self._path: str = _DEFAULT_PATH

    def render(self, path: str = "/home/user") -> str:
        """
        Returns a Dolphin-style directory listing for *path*.

        Args:
            path (str): Linux path to display.

        Returns:
            str: File manager scene.
        """
        self._path = path
        items = self.list_items()
        rows = "\n".join(f"│  🗂  {item}" for item in items)
        view = (
            f"┌─ Dolphin — {self._path} ──────────────────────────────┐\n"
            f"{rows}\n"
            "└────────────────────────────────────────────────────────┘"
        )
        print(f"[KDEFileManager] Rendered path: {self._path}")
        return view

    def navigate(self, path: str) -> None:
        """Navigates to *path*."""
        self._path = path
        print(f"[KDEFileManager] Navigated to {self._path}")

    def list_items(self) -> list[str]:
        """Returns fake directory entries for the current path."""
        return _FAKE_TREE.get(self._path, ["(empty directory)"])
