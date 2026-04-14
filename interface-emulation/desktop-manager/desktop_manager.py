"""
WekezaOmniOS Interface Emulation — Desktop Manager
===================================================
Manages desktop environment skins, workspace persistence, and
environment switching for the interface-emulation subsystem.
"""

import os
import sys

_BASE = os.path.dirname(os.path.abspath(__file__))
_SKINS_DIR = os.path.join(os.path.dirname(_BASE), "ui-skins")

for _sub in (
    os.path.join(_SKINS_DIR, "windows-ui"),
    os.path.join(_SKINS_DIR, "ubuntu-ui"),
    os.path.join(_SKINS_DIR, "kde-ui"),
    os.path.join(_SKINS_DIR, "macos-style"),
):
    if _sub not in sys.path:
        sys.path.insert(0, _sub)

_SKIN_DIRS = {
    "windows": os.path.join(_SKINS_DIR, "windows-ui"),
    "ubuntu":  os.path.join(_SKINS_DIR, "ubuntu-ui"),
    "kde":     os.path.join(_SKINS_DIR, "kde-ui"),
    "macos":   os.path.join(_SKINS_DIR, "macos-style"),
}


class DesktopManager:
    """
    Manages desktop environment skins and workspace state.

    Supports loading, switching, saving, and restoring desktop
    environments at runtime.
    """

    def __init__(self):
        print("\n[DesktopManager] 🖥  Initialising Desktop Manager...")
        self._current_env: str | None = None
        self._workspaces: dict[str, dict] = {}
        self._skin_cache: dict[str, object] = {}
        print(
            f"[DesktopManager] ✅ Desktop Manager ready. "
            f"Environments: {', '.join(self.list_environments())}"
        )

    # ------------------------------------------------------------------
    # Skin management
    # ------------------------------------------------------------------

    def load_skin(self, skin_name: str) -> object:
        """
        Loads and returns the requested UI skin object.

        Args:
            skin_name (str): One of 'windows', 'ubuntu', 'kde', 'macos'.

        Returns:
            WindowsUI | UbuntuUI | KDEUI | MacOSUI: The skin instance.

        Raises:
            ValueError: If *skin_name* is not recognised.
        """
        skin_name = skin_name.lower()
        if skin_name not in _SKIN_DIRS:
            raise ValueError(
                f"[DesktopManager] Unknown skin: {skin_name!r}. "
                f"Available: {list(_SKIN_DIRS)}"
            )

        if skin_name in self._skin_cache:
            print(f"[DesktopManager] Returning cached skin: {skin_name}")
            return self._skin_cache[skin_name]

        print(f"[DesktopManager] Loading skin: {skin_name}...")
        skin_dir = _SKIN_DIRS[skin_name]
        if skin_dir not in sys.path:
            sys.path.insert(0, skin_dir)

        if skin_name == "windows":
            # Import from windows-ui directory
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "windows_ui",
                os.path.join(skin_dir, "__init__.py"),
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            skin = mod.WindowsUI()

        elif skin_name == "ubuntu":
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "ubuntu_ui",
                os.path.join(skin_dir, "__init__.py"),
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            skin = mod.UbuntuUI()

        elif skin_name == "kde":
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "kde_ui",
                os.path.join(skin_dir, "__init__.py"),
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            skin = mod.KDEUI()

        elif skin_name == "macos":
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "macos_ui",
                os.path.join(skin_dir, "__init__.py"),
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            skin = mod.MacOSUI()

        self._skin_cache[skin_name] = skin
        self._current_env = skin_name
        print(f"[DesktopManager] Skin '{skin_name}' loaded and active.")
        return skin

    # ------------------------------------------------------------------
    # Environment switching
    # ------------------------------------------------------------------

    def switch_environment(self, from_env: str, to_env: str) -> object:
        """
        Switches from *from_env* to *to_env*, saving the workspace first.

        Args:
            from_env (str): Currently active environment name.
            to_env (str): Target environment name.

        Returns:
            The new skin object.
        """
        print(
            f"[DesktopManager] Switching environment: "
            f"{from_env} → {to_env}"
        )
        self.save_workspace(from_env)
        skin = self.load_skin(to_env)
        self._current_env = to_env
        print(
            f"[DesktopManager] ✅ Active environment is now: {to_env}"
        )
        return skin

    # ------------------------------------------------------------------
    # Workspace persistence
    # ------------------------------------------------------------------

    def save_workspace(self, env_name: str) -> None:
        """
        Saves the current workspace state for *env_name*.

        Args:
            env_name (str): Environment whose workspace to save.
        """
        self._workspaces[env_name] = {
            "env": env_name,
            "open_apps": [],  # placeholder
            "wallpaper": f"omnios-{env_name}-default.png",
        }
        print(f"[DesktopManager] Workspace saved for: {env_name}")

    def restore_workspace(self, env_name: str) -> dict:
        """
        Restores a previously saved workspace state.

        Args:
            env_name (str): Environment to restore.

        Returns:
            dict: Workspace state dict (empty dict if never saved).
        """
        state = self._workspaces.get(env_name, {})
        print(
            f"[DesktopManager] Restored workspace for: {env_name} "
            f"({len(state)} entries)"
        )
        return state

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def list_environments(self) -> list[str]:
        """Returns list of available environment names."""
        return list(_SKIN_DIRS.keys())

    @property
    def current_environment(self) -> str | None:
        """Returns the name of the currently active environment."""
        return self._current_env


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    dm = DesktopManager()
    print("Environments:", dm.list_environments())
    win = dm.load_skin("windows")
    win.render_desktop()
    dm.switch_environment("windows", "ubuntu")
    dm.save_workspace("ubuntu")
    dm.restore_workspace("windows")
    print("Current env:", dm.current_environment)
