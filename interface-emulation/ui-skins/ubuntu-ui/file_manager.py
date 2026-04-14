"""
WekezaOmniOS Interface Emulation — Ubuntu File Manager (Nautilus)
=================================================================
Simulates a GNOME Nautilus-style file manager with Linux home paths.
"""


_FAKE_TREE: dict[str, list[str]] = {
    "/home/user": [
        "Desktop", "Documents", "Downloads", "Music",
        "Pictures", "Videos", "Templates", ".config",
    ],
    "/home/user/Documents": [
        "report.odt", "notes.txt", "budget.ods", "resume.pdf",
    ],
    "/home/user/Downloads": [
        "ubuntu-24.04.iso", "archive.tar.gz", "photo.jpg",
    ],
    "/": [
        "bin", "boot", "dev", "etc", "home",
        "lib", "mnt", "opt", "proc", "root",
        "run", "srv", "sys", "tmp", "usr", "var",
    ],
}

_DEFAULT_PATH = "/home/user"


class UbuntuFileManager:
    """
    Emulated Nautilus (GNOME Files) file manager component.
    """

    def __init__(self):
        print("[UbuntuFileManager] Initialising file manager...")
        self._path: str = _DEFAULT_PATH

    def render(self, path: str = "/home/user") -> str:
        """
        Returns a Nautilus-style directory listing for *path*.

        Args:
            path (str): Linux path to display.

        Returns:
            str: File manager scene.
        """
        self._path = path
        items = self.list_items()
        rows = "\n".join(f"│  📁  {item}" for item in items)
        view = (
            f"┌─ Files — {self._path} ──────────────────────────────┐\n"
            f"{rows}\n"
            "└──────────────────────────────────────────────────────┘"
        )
        print(f"[UbuntuFileManager] Rendered path: {self._path}")
        return view

    def navigate(self, path: str) -> None:
        """Navigates to *path*."""
        self._path = path
        print(f"[UbuntuFileManager] Navigated to {self._path}")

    def list_items(self) -> list[str]:
        """Returns fake directory entries for the current path."""
        return _FAKE_TREE.get(self._path, ["(empty directory)"])
