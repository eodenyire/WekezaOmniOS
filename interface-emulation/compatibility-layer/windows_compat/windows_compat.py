"""
WekezaOmniOS Interface Emulation — Windows Compat Module
=========================================================
Simulates loading Windows executables, translating Windows registry
keys to Linux config paths, mapping Windows paths to Linux paths, and
emulating common Win32 API calls.
"""


# Registry root → Linux config directory mapping
_REGISTRY_MAP: dict[str, str] = {
    "HKLM\\SOFTWARE":           "/etc/omnios/registry/software",
    "HKLM\\SYSTEM":             "/etc/omnios/registry/system",
    "HKCU\\SOFTWARE":           "/home/user/.config/omnios/software",
    "HKCU\\Control Panel":      "/home/user/.config/omnios/control-panel",
    "HKLM\\HARDWARE":           "/proc/omnios/hardware",
}

# Win32 API → POSIX equivalent
_API_MAP: dict[str, str] = {
    "CreateFile":        "open",
    "ReadFile":          "read",
    "WriteFile":         "write",
    "CloseHandle":       "close",
    "CreateProcess":     "fork+exec",
    "TerminateProcess":  "kill",
    "VirtualAlloc":      "mmap",
    "VirtualFree":       "munmap",
    "LoadLibrary":       "dlopen",
    "GetProcAddress":    "dlsym",
    "RegOpenKeyEx":      "open(/etc/omnios/registry/...)",
    "MessageBox":        "zenity --info",
}


class WindowsCompat:
    """
    Compatibility module for Windows binaries and APIs.

    Provides stub implementations of binary loading, path translation,
    registry key mapping, and Win32 API emulation so that the
    interface-emulation layer can represent Windows workloads.
    """

    def __init__(self):
        print("[WindowsCompat] 🪟 Windows compatibility module loaded.")

    # ------------------------------------------------------------------
    # Binary loading
    # ------------------------------------------------------------------

    def load_binary(self, exe_path: str) -> dict:
        """
        Simulates loading a Windows PE executable.

        Args:
            exe_path (str): Path to the .exe file.

        Returns:
            dict: Simulated binary metadata.

        Raises:
            ValueError: If the file does not have a .exe extension.
        """
        if not exe_path.lower().endswith(".exe"):
            raise ValueError(
                f"[WindowsCompat] {exe_path!r} is not a .exe binary."
            )
        info = {
            "path": exe_path,
            "format": "PE32+",
            "arch": "x86_64",
            "subsystem": "Windows GUI",
            "status": "loaded (emulated)",
        }
        print(
            f"[WindowsCompat] Loading PE binary: {exe_path} "
            f"[PE32+, x86_64, Windows GUI]"
        )
        return info

    # ------------------------------------------------------------------
    # Registry translation
    # ------------------------------------------------------------------

    def translate_registry_key(self, win_key: str) -> str:
        """
        Maps a Windows registry key path to a fake Linux config path.

        Args:
            win_key (str): Windows registry key (e.g. 'HKLM\\SOFTWARE\\...').

        Returns:
            str: Linux-equivalent config path.
        """
        for prefix, linux_path in _REGISTRY_MAP.items():
            if win_key.upper().startswith(prefix.upper()):
                remainder = win_key[len(prefix):].replace("\\", "/")
                result = linux_path + remainder
                print(
                    f"[WindowsCompat] Registry: {win_key} → {result}"
                )
                return result
        result = f"/etc/omnios/registry/unknown/{win_key.replace('\\', '/')}"
        print(f"[WindowsCompat] Registry (unmapped): {win_key} → {result}")
        return result

    # ------------------------------------------------------------------
    # Path translation
    # ------------------------------------------------------------------

    def translate_path(self, win_path: str) -> str:
        """
        Converts a Windows filesystem path to a Linux path.

        Examples:
            C:\\Users\\Alice\\file.txt → /home/Alice/file.txt
            D:\\Projects\\app         → /mnt/d/Projects/app

        Args:
            win_path (str): Windows-style path.

        Returns:
            str: Linux-style path.
        """
        path = win_path
        if len(path) >= 2 and path[1] == ":":
            drive = path[0].lower()
            rest = path[2:].replace("\\", "/")
            if drive == "c":
                # Map C:\Users\X → /home/X
                if rest.lower().startswith("/users/"):
                    parts = rest.split("/", 2)
                    user = parts[2].split("/")[0] if len(parts) > 2 else "user"
                    remainder = "/".join(rest.split("/")[3:]) if len(rest.split("/")) > 3 else ""
                    linux_path = f"/home/{user}/{remainder}".rstrip("/")
                else:
                    linux_path = rest or "/"
            else:
                linux_path = f"/mnt/{drive}{rest}"
        else:
            linux_path = win_path.replace("\\", "/")

        print(f"[WindowsCompat] Path: {win_path!r} → {linux_path!r}")
        return linux_path

    # ------------------------------------------------------------------
    # API emulation
    # ------------------------------------------------------------------

    def emulate_api(self, api_call: str, *args) -> str:
        """
        Simulates a Win32 API call.

        Args:
            api_call (str): Win32 API function name.
            *args: Arguments (logged for context).

        Returns:
            str: Linux equivalent operation description.
        """
        linux_equiv = _API_MAP.get(api_call, f"unknown({api_call})")
        print(
            f"[WindowsCompat] API emulated: {api_call}({', '.join(str(a) for a in args)}) "
            f"→ {linux_equiv}"
        )
        return linux_equiv


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    wc = WindowsCompat()
    wc.load_binary("C:\\Program Files\\App\\app.exe")
    wc.translate_registry_key("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion")
    wc.translate_path("C:\\Users\\Alice\\Documents\\file.txt")
    wc.translate_path("D:\\Projects\\OmniOS\\main.py")
    wc.emulate_api("CreateFile", "data.txt", "GENERIC_READ")
    wc.emulate_api("MessageBox", "Hello World")
