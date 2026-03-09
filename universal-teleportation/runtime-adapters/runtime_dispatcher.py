"""
WekezaOmniOS Runtime Dispatcher
Phase 7: Orchestrates cross-OS teleportation by selecting the correct
runtime adapter for a given source/target OS pair and applying the
necessary state translations before restoration.
"""
from .linux_adapter import LinuxAdapter
from .windows_adapter import WindowsAdapter
from .android_adapter import AndroidAdapter
from .ios_adapter import IOSAdapter
from .dependency_resolver import DependencyResolver
from .runtime_mapper import RuntimeMapper


ADAPTER_MAP = {
    "linux": LinuxAdapter,
    "windows": WindowsAdapter,
    "android": AndroidAdapter,
    "macos": IOSAdapter,
    "ios": IOSAdapter,
}


class RuntimeDispatcher:
    """
    Phase 7: Selects the correct adapter, resolves dependencies, and maps
    runtime state for cross-OS teleportation.
    """

    def __init__(self):
        self.resolver = DependencyResolver()
        self._adapters = {
            "linux": LinuxAdapter(),
            "windows": WindowsAdapter(),
            "android": AndroidAdapter(),
            "macos": IOSAdapter(),
            "ios": IOSAdapter(),
        }

    def translate(self, snapshot, target_os):
        if target_os not in self._adapters:
            return snapshot
        
        adapter = self._adapters[target_os]
        return adapter.translate_process_state(snapshot)


    def get_adapter(self, os_name: str):
        """
        Return the runtime adapter instance for the given OS name.

        Args:
            os_name: Target OS identifier (linux, windows, android, macos, ios).

        Returns:
            Runtime adapter instance.

        Raises:
            ValueError: If the OS is not supported.
        """
        key = os_name.lower()
        adapter = self._adapters.get(key)
        if adapter is None:
            raise ValueError(
                f"[RuntimeDispatcher] Unsupported OS: '{os_name}'. "
                f"Supported: {list(self._adapters.keys())}"
            )
        return adapter

    def dispatch(self, snapshot_data: dict, source_os: str, target_os: str) -> dict:
        """
        Translate snapshot state from source_os to target_os.

        Steps:
            1. Check OS compatibility.
            2. Map runtime paths, signals, and env vars.
            3. Apply target adapter transformations.

        Args:
            snapshot_data: Process snapshot metadata dict.
            source_os: OS the snapshot was captured on.
            target_os: OS where the snapshot will be restored.

        Returns:
            dict: Translated snapshot data ready for restoration.
        """
        print(f"[RuntimeDispatcher] Dispatching {source_os} -> {target_os}")

        # Step 1: Compatibility check
        compatible = self.resolver.check_compatibility(source_os, target_os)
        if not compatible:
            print(
                f"[RuntimeDispatcher] ⚠️  {source_os} -> {target_os} requires "
                "adaptation — applying runtime mapper."
            )

        # Step 2: Map paths, signals, and env vars
        mapper = RuntimeMapper(source_os=source_os, target_os=target_os)
        translated = snapshot_data.copy()
        if "paths" in translated:
            translated["paths"] = mapper.map_paths(translated["paths"])
        if "env_vars" in translated:
            translated["env_vars"] = mapper.map_environment(translated["env_vars"])
        translated["target_os"] = target_os

        # Step 3: Apply target adapter
        adapter = self.get_adapter(target_os)
        translated = adapter.translate_process_state(translated)

        print(f"[RuntimeDispatcher] ✅ State translated for {target_os}.")
        return translated

    def supported_os_list(self) -> list:
        """Return the list of supported target operating systems."""
        return list(self._adapters.keys())
