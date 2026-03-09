"""
WekezaOmniOS Runtime Dispatcher
Phase 7: The "Brain" that selects the correct runtime adapter.
"""
import importlib

class RuntimeDispatcher:
    def __init__(self):
        self.adapters = {
            "ios": "runtime-adapters.apple_adapter.AppleAdapter",
            "android": "runtime-adapters.android_adapter.AndroidAdapter",
            "linux": "runtime-adapters.linux_adapter.LinuxAdapter",
            "windows": "runtime-adapters.windows_adapter.WindowsAdapter",
        }

    def get_adapter(self, target_os):
        """
        Dynamically imports and returns the correct adapter class for the target OS.
        """
        adapter_path = self.adapters.get(target_os.lower())
        if not adapter_path:
            print(f"[Dispatcher] No adapter found for OS: {target_os}")
            return None

        try:
            module_path, class_name = adapter_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            adapter_class = getattr(module, class_name)
            print(f"[Dispatcher] Loaded adapter: {class_name} for {target_os}")
            return adapter_class()
        except (ImportError, AttributeError) as e:
            print(f"[Dispatcher] Error loading adapter for {target_os}: {e}")
            return None

    def dispatch(self, snapshot_metadata, target_os):
        """
        Dispatches the snapshot to the appropriate adapter for translation.
        """
        print(f"[Dispatcher] Dispatching snapshot for target OS: {target_os}")
        adapter = self.get_adapter(target_os)
        if adapter:
            return adapter.translate_runtime(snapshot_metadata)
        
        # If no specific adapter, return the metadata unmodified
        print(f"[Dispatcher] No specific translation applied for {target_os}.")
        return snapshot_metadata

# Example Usage (will be integrated into the Teleportation API)
if __name__ == '__main__':
    # This is a simulation of how the API would use the dispatcher.
    dispatcher = RuntimeDispatcher()
    
    # Mock snapshot metadata from a Windows source
    mock_snapshot = {
        "source_os": "windows",
        "ui_config": {"scaling": "1x"},
        "env": {"DATA_PATH": "C:\\Users\\Developer\\Documents\\MilkAppData"},
        "permissions": [],
        "app_state": {"window_title": "MilkApp v1.0"}
    }

    # 1. Teleport to iOS
    ios_metadata = dispatcher.dispatch(mock_snapshot.copy(), "ios")
    print("--- Translated for iOS ---")
    print(ios_metadata)
    print("\\n")

    # 2. Teleport to Android
    android_metadata = dispatcher.dispatch(mock_snapshot.copy(), "android")
    print("--- Translated for Android ---")
    print(android_metadata)
