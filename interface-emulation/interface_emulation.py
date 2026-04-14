"""
WekezaOmniOS Interface Emulation — Top-level Orchestrator
==========================================================
Wires together all interface-emulation subsystems:
  - Core Kernel Layer  (VirtualFilesystem, ProcessManager, NetworkStack)
  - Command Translator (CommandTranslator)
  - Desktop Manager    (DesktopManager + UI skins)
  - Compatibility Layer (WindowsCompat, LinuxCompat, AndroidCompat)

End-to-end flow:
    1. An app is launched through ProcessManager and logged.
    2. Commands are translated by CommandTranslator.
    3. The UI skin is swapped via DesktopManager.
    4. Binaries are routed to the correct compat module.
"""

import os
import sys

_BASE = os.path.dirname(os.path.abspath(__file__))

# Resolve sibling package paths
for _sub in (
    os.path.join(_BASE, "core-kernel-layer"),
    os.path.join(_BASE, "command-translator"),
    os.path.join(_BASE, "desktop-manager"),
    os.path.join(_BASE, "compatibility-layer", "windows_compat"),
    os.path.join(_BASE, "compatibility-layer", "linux_compat"),
    os.path.join(_BASE, "compatibility-layer", "android_compat"),
):
    if _sub not in sys.path:
        sys.path.insert(0, _sub)

from filesystem import VirtualFilesystem
from process_manager import ProcessManager
from network_stack import NetworkStack
from command_translator import CommandTranslator
from desktop_manager import DesktopManager
from windows_compat import WindowsCompat
from linux_compat import LinuxCompat
from android_compat import AndroidCompat


# ---------------------------------------------------------------------------
# Compat module registry
# ---------------------------------------------------------------------------

_COMPAT_MODULES = {
    "windows": WindowsCompat,
    "linux":   LinuxCompat,
    "android": AndroidCompat,
}


class InterfaceEmulation:
    """
    High-level façade for the Interface Emulation subsystem.

    Instantiate once and use ``launch_app``, ``translate_command``,
    ``switch_ui``, ``load_binary``, and ``status`` to drive the
    interface-emulation layer.
    """

    def __init__(self, host_os: str = "linux", initial_skin: str = "ubuntu"):
        """
        Args:
            host_os (str): Underlying host OS.
            initial_skin (str): UI skin to load on startup.
        """
        print("\n" + "=" * 60)
        print("  WekezaOmniOS Interface Emulation — Starting Up")
        print("=" * 60)

        self.host_os = host_os
        self.filesystem = VirtualFilesystem()
        self.process_mgr = ProcessManager()
        self.network = NetworkStack()
        self.desktop = DesktopManager()
        self._translators: dict[str, CommandTranslator] = {}
        self._compat: dict[str, object] = {}

        # Load initial skin
        self.desktop.load_skin(initial_skin)

        print("\n[InterfaceEmulation] ✅ All sub-systems online.\n")

    # ------------------------------------------------------------------
    # Application management
    # ------------------------------------------------------------------

    def launch_app(self, app_name: str, os_type: str = "linux") -> int:
        """
        Spawns a new process for *app_name* and logs it.

        Args:
            app_name (str): Application to launch.
            os_type (str): Source OS of the application.

        Returns:
            int: PID assigned to the new process.
        """
        print(f"[InterfaceEmulation] Launching app: {app_name} ({os_type})")
        pid = self.process_mgr.spawn(app_name, os_type=os_type)
        return pid

    # ------------------------------------------------------------------
    # Command translation
    # ------------------------------------------------------------------

    def translate_command(
        self, cmd: str, source_os: str = "windows"
    ) -> str:
        """
        Translates *cmd* from *source_os* to its Linux equivalent.

        Args:
            cmd (str): Command to translate.
            source_os (str): Source OS.

        Returns:
            str: Linux equivalent command.
        """
        if source_os not in self._translators:
            self._translators[source_os] = CommandTranslator(source_os)
        return self._translators[source_os].translate(cmd)

    # ------------------------------------------------------------------
    # UI skin switching
    # ------------------------------------------------------------------

    def switch_ui(self, skin_name: str) -> object:
        """
        Switches the active UI skin to *skin_name*.

        Args:
            skin_name (str): Target skin ('windows', 'ubuntu', 'kde', 'macos').

        Returns:
            The new skin object.
        """
        current = self.desktop.current_environment or "none"
        print(
            f"[InterfaceEmulation] Switching UI: {current} → {skin_name}"
        )
        if current != "none":
            return self.desktop.switch_environment(current, skin_name)
        return self.desktop.load_skin(skin_name)

    # ------------------------------------------------------------------
    # Binary loading
    # ------------------------------------------------------------------

    def load_binary(
        self, binary_path: str, os_type: str = "windows"
    ) -> dict:
        """
        Routes binary loading to the appropriate compat module.

        Args:
            binary_path (str): Path to the binary.
            os_type (str): Source OS ('windows', 'linux', 'android').

        Returns:
            dict: Binary metadata from the compat module.
        """
        print(
            f"[InterfaceEmulation] Loading binary: {binary_path} "
            f"(os_type={os_type})"
        )
        if os_type not in self._compat:
            cls = _COMPAT_MODULES.get(os_type.lower())
            if cls is None:
                print(
                    f"[InterfaceEmulation] ⚠️  No compat module for "
                    f"{os_type!r}."
                )
                return {}
            self._compat[os_type] = cls()

        compat = self._compat[os_type]
        if os_type == "windows":
            return compat.load_binary(binary_path)
        elif os_type == "linux":
            return compat.load_binary(binary_path)
        elif os_type == "android":
            return compat.load_apk(binary_path)
        return {}

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def status(self) -> None:
        """Prints a full status summary of all subsystems."""
        print("\n" + "=" * 60)
        print("  [InterfaceEmulation] Status Report")
        print("=" * 60)
        print(f"  Host OS       : {self.host_os}")
        print(f"  Active skin   : {self.desktop.current_environment}")
        mounts = self.filesystem.list_mounts()
        print(f"  Mounts        : {len(mounts)} registered")
        for m in mounts:
            print(f"    {m['source']} → {m['target']} ({m['fs_type']})")
        procs = self.process_mgr.list_processes()
        print(f"  Processes     : {len(procs)} running")
        for p in procs:
            print(
                f"    PID={p['pid']}  {p['name']}  "
                f"[{p['os_type']}]  state={p['state']}"
            )
        ifaces = self.network.list_interfaces()
        print(f"  Interfaces    : {len(ifaces)} registered")
        for i in ifaces:
            print(f"    {i['name']}  {i['ip']}/{i['netmask']}")
        print("=" * 60 + "\n")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ie = InterfaceEmulation(host_os="linux", initial_skin="windows")

    # Core kernel layer
    ie.filesystem.mount("/dev/sda1", "/", "ext4")
    ie.filesystem.mount("/dev/sda2", "/home", "ext4")
    ie.network.add_interface("eth0", "192.168.1.10")

    # Processes
    ie.launch_app("notepad.exe", os_type="windows")
    ie.launch_app("bash", os_type="linux")

    # Command translation
    ie.translate_command("dir", source_os="windows")
    ie.translate_command("copy", source_os="windows")

    # UI switching
    ie.switch_ui("ubuntu")

    # Binary loading
    ie.load_binary("C:\\App\\app.exe", os_type="windows")
    ie.load_binary("/usr/bin/htop", os_type="linux")

    # Full status
    ie.status()
