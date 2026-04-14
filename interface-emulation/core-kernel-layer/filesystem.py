"""
WekezaOmniOS Interface Emulation — Virtual Filesystem
======================================================
Simulates a Linux-style in-memory filesystem with mount point
management and basic path resolution.
"""


class VirtualFilesystem:
    """
    In-memory simulation of a Linux-style virtual filesystem.

    Tracks mount points and provides path resolution helpers.
    """

    def __init__(self):
        print("[VirtualFilesystem] 🗂  Initialising virtual filesystem...")
        self._mounts: list[dict] = []
        print("[VirtualFilesystem] ✅ Virtual filesystem ready.")

    # ------------------------------------------------------------------
    # Mount management
    # ------------------------------------------------------------------

    def mount(self, source: str, target: str, fs_type: str = "ext4") -> dict:
        """
        Registers a new mount point.

        Args:
            source (str): Device or pseudo-device (e.g. '/dev/sda1').
            target (str): Mount target path (e.g. '/').
            fs_type (str): Filesystem type (default 'ext4').

        Returns:
            dict: The mount entry that was added.
        """
        entry = {"source": source, "target": target, "fs_type": fs_type}
        self._mounts.append(entry)
        print(f"[VirtualFilesystem] Mounted {source} → {target} ({fs_type})")
        return entry

    def unmount(self, target: str) -> None:
        """
        Removes a registered mount point.

        Args:
            target (str): The mount target path to remove.

        Raises:
            KeyError: If no mount point is registered at *target*.
        """
        before = len(self._mounts)
        self._mounts = [m for m in self._mounts if m["target"] != target]
        if len(self._mounts) == before:
            raise KeyError(f"[VirtualFilesystem] No mount found at {target!r}")
        print(f"[VirtualFilesystem] Unmounted {target}")

    # ------------------------------------------------------------------
    # Path helpers
    # ------------------------------------------------------------------

    def exists(self, path: str) -> bool:
        """
        Checks whether *path* is a known mount target or a sub-path of one.

        Args:
            path (str): Path to check.

        Returns:
            bool: True when the path is within any registered mount.
        """
        resolved = self.resolve_path(path)
        for m in self._mounts:
            if resolved == m["target"] or resolved.startswith(
                m["target"].rstrip("/") + "/"
            ):
                return True
        return False

    def resolve_path(self, path: str) -> str:
        """
        Normalises a path: strips trailing slashes and expands ``~``.

        Args:
            path (str): Input path string.

        Returns:
            str: Normalised path.
        """
        if path.startswith("~"):
            path = "/home/user" + path[1:]
        path = path.rstrip("/") or "/"
        return path

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def list_mounts(self) -> list[dict]:
        """
        Returns all registered mount points.

        Returns:
            list[dict]: Each entry has 'source', 'target', and 'fs_type'.
        """
        return list(self._mounts)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    vfs = VirtualFilesystem()
    vfs.mount("/dev/sda1", "/", "ext4")
    vfs.mount("/dev/sda2", "/home", "ext4")
    vfs.mount("tmpfs", "/tmp", "tmpfs")
    print(vfs.list_mounts())
    print(vfs.exists("/home/user/docs"))
    print(vfs.resolve_path("~/Downloads"))
    vfs.unmount("/tmp")
    print(vfs.list_mounts())
