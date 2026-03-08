"""
WekezaOmniOS Runtime Mapper
Phase 3: Maps process state fields across different runtime environments.
"""


SIGNAL_MAP = {
    "linux_to_windows": {
        "SIGTERM": "CTRL_C_EVENT",
        "SIGKILL": "TASKKILL",
        "SIGHUP": "SERVICE_CONTROL_STOP",
    },
    "linux_to_android": {
        "SIGTERM": "SIGTERM",
        "SIGKILL": "SIGKILL",
    },
}

PATH_SEPARATOR = {
    "linux": "/",
    "android": "/",
    "windows": "\\",
}


class RuntimeMapper:
    """
    Translates environment variables, filesystem paths, and OS signals
    between heterogeneous runtime environments.
    """

    def __init__(self, source_os: str = "linux", target_os: str = "linux"):
        self.source_os = source_os
        self.target_os = target_os

    def map_paths(self, paths: list) -> list:
        """Convert a list of filesystem paths to the target OS format."""
        src_sep = PATH_SEPARATOR.get(self.source_os, "/")
        tgt_sep = PATH_SEPARATOR.get(self.target_os, "/")
        return [p.replace(src_sep, tgt_sep) for p in paths]

    def map_signal(self, signal_name: str) -> str:
        """Translate a signal name to its equivalent on the target OS."""
        key = f"{self.source_os}_to_{self.target_os}"
        mapping = SIGNAL_MAP.get(key, {})
        translated = mapping.get(signal_name, signal_name)
        print(f"[RuntimeMapper] {signal_name} -> {translated} ({self.source_os} -> {self.target_os})")
        return translated

    def map_environment(self, env_vars: dict) -> dict:
        """Apply target-OS-specific transformations to environment variables."""
        mapped = dict(env_vars)
        if self.target_os == "windows":
            mapped["OS"] = "Windows_NT"
            mapped["PATH"] = mapped.get("PATH", "").replace("/", "\\")
        elif self.target_os == "android":
            mapped["OS"] = "Android"
        return mapped
class RuntimeMapper:
    """
    Selects the appropriate runtime adapter.
    """

    def __init__(self):

        self.adapters = {}

    def register_adapter(self, os_name, adapter):

        self.adapters[os_name] = adapter

    def get_adapter(self, os_name):

        return self.adapters.get(os_name)
