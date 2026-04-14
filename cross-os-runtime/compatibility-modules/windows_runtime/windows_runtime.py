"""
WekezaOmniOS Windows Runtime Module
Translates Windows API calls and application state into the universal
runtime format used by the Cross-OS Runtime Layer.
"""


# Win32 API → POSIX system call table (subset for demo)
WIN32_TO_POSIX = {
    "CreateFile":      "open",
    "ReadFile":        "read",
    "WriteFile":       "write",
    "CloseHandle":     "close",
    "CreateProcess":   "fork+exec",
    "TerminateProcess":"kill",
    "VirtualAlloc":    "mmap",
    "VirtualFree":     "munmap",
    "LoadLibrary":     "dlopen",
    "GetProcAddress":  "dlsym",
}

# NT path prefix that needs stripping for POSIX compatibility
NT_DEVICE_PREFIX = "\\\\?\\"


class WindowsRuntime:
    """
    Compatibility module for Windows applications.

    Provides API translation, path normalisation, and environment
    variable mapping so that a Windows binary's process state can be
    understood and managed by the universal runtime layer.
    """

    OS_NAME = "Windows"

    def __init__(self):
        print(f"[{self.OS_NAME}Runtime] Module loaded.")

    # ------------------------------------------------------------------
    # API translation
    # ------------------------------------------------------------------

    def translate_api_call(self, win32_call):
        """
        Maps a Win32 API call name to its POSIX equivalent.

        Args:
            win32_call (str): Win32 API function name.

        Returns:
            str: The corresponding POSIX call, or the original name if
                 no mapping exists.
        """
        posix_call = WIN32_TO_POSIX.get(win32_call, win32_call)
        print(
            f"[{self.OS_NAME}Runtime] API translation: "
            f"{win32_call} → {posix_call}"
        )
        return posix_call

    # ------------------------------------------------------------------
    # Path normalisation
    # ------------------------------------------------------------------

    def normalise_path(self, win_path):
        """
        Converts a Windows filesystem path to a POSIX-style path.

        Examples:
            C:\\Users\\Alice\\file.txt  →  /c/Users/Alice/file.txt
            \\\\?\\C:\\long\\path       →  /c/long/path

        Args:
            win_path (str): Windows-style path.

        Returns:
            str: POSIX-style equivalent path.
        """
        path = win_path
        if path.startswith(NT_DEVICE_PREFIX):
            path = path[len(NT_DEVICE_PREFIX):]

        # Drive letter  (C:\...)  →  /c/...
        if len(path) >= 2 and path[1] == ":":
            drive = path[0].lower()
            path = "/" + drive + path[2:]

        posix_path = path.replace("\\", "/")
        print(
            f"[{self.OS_NAME}Runtime] Path normalised: "
            f"{win_path!r} → {posix_path!r}"
        )
        return posix_path

    # ------------------------------------------------------------------
    # Environment adaptation
    # ------------------------------------------------------------------

    def adapt_environment(self, env_vars):
        """
        Translates Windows-specific environment variables to their
        cross-platform counterparts.

        Args:
            env_vars (dict): Original Windows environment dictionary.

        Returns:
            dict: Adapted environment dictionary.
        """
        adapted = dict(env_vars)
        # Remap canonical Windows vars to universal equivalents
        if "USERPROFILE" in adapted and "HOME" not in adapted:
            adapted["HOME"] = self.normalise_path(adapted["USERPROFILE"])
        if "APPDATA" in adapted:
            adapted["XDG_CONFIG_HOME"] = self.normalise_path(adapted["APPDATA"])
        if "TEMP" in adapted:
            adapted["TMPDIR"] = self.normalise_path(adapted["TEMP"])

        adapted["OS_TYPE"] = "windows"
        print(f"[{self.OS_NAME}Runtime] Environment adapted.")
        return adapted

    # ------------------------------------------------------------------
    # State translation
    # ------------------------------------------------------------------

    def translate_process_state(self, snapshot):
        """
        Converts a Windows process snapshot into a cross-platform state
        that the runtime engine and sandbox can consume.

        Args:
            snapshot (dict): Raw Windows process state.

        Returns:
            dict: Universal process state.
        """
        state = snapshot.copy()
        state["source_os"] = "windows"

        # Normalise paths inside the snapshot
        if "open_files" in state:
            state["open_files"] = [
                self.normalise_path(p) for p in state["open_files"]
            ]
        if "env" in state:
            state["env"] = self.adapt_environment(state["env"])

        print(f"[{self.OS_NAME}Runtime] Process state translated.")
        return state

    # ------------------------------------------------------------------
    # Dependency resolution placeholder
    # ------------------------------------------------------------------

    def resolve_dependencies(self, dll_list):
        """
        Maps Windows DLL dependencies to cross-platform equivalents or
        marks them for Wine-compatible injection.

        Args:
            dll_list (list[str]): List of required DLL names.

        Returns:
            dict: Mapping of DLL name → resolution strategy.
        """
        strategies = {}
        for dll in dll_list:
            if dll.lower() in ("kernel32.dll", "ntdll.dll", "user32.dll"):
                strategies[dll] = "wine-builtin"
            elif dll.lower().startswith("vcruntime"):
                strategies[dll] = "wine-native"
            else:
                strategies[dll] = "unknown"
            print(
                f"[{self.OS_NAME}Runtime] DLL {dll!r} → {strategies[dll]}"
            )
        return strategies


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    runtime = WindowsRuntime()

    runtime.translate_api_call("CreateFile")
    runtime.translate_api_call("LoadLibrary")

    runtime.normalise_path("C:\\Users\\Alice\\Documents\\report.docx")
    runtime.normalise_path("\\\\?\\D:\\Projects\\OmniOS\\main.py")

    snapshot = {
        "pid": 4001,
        "open_files": ["C:\\Users\\Alice\\data.txt", "D:\\logs\\app.log"],
        "env": {"USERPROFILE": "C:\\Users\\Alice", "TEMP": "C:\\Temp"},
        "app_state": {"window_title": "Notepad"},
    }
    translated = runtime.translate_process_state(snapshot)
    import json
    print(json.dumps(translated, indent=2))
