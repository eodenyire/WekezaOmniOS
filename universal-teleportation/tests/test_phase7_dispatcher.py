"""
WekezaOmniOS Phase 7 - Runtime Dispatcher Tests
"""
import unittest
import sys
import os

# Ensure the runtime-adapters directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from runtime_adapters.runtime_dispatcher import RuntimeDispatcher
from runtime_adapters.apple_adapter import AppleAdapter
from runtime_adapters.android_adapter import AndroidAdapter
from runtime_adapters.windows_adapter import WindowsAdapter
from runtime_adapters.linux_adapter import LinuxAdapter
from runtime_adapters.ios_adapter import IOSAdapter

class TestRuntimeDispatcher(unittest.TestCase):

    def setUp(self):
        """Set up a new RuntimeDispatcher for each test."""
        self.dispatcher = RuntimeDispatcher()
        self.snapshot = {
            "process_id": 1234,
            "memory_pages": ["page1", "page2"],
            "env": {"DATA_PATH": "C:\\Users\\Test\\MilkData"},
            "ui_config": {"scaling": "windows_100_percent"},
            "permissions": []
        }

    def test_dispatcher_initialization(self):
        """Test that the dispatcher initializes with the correct adapters."""
        self.assertIn("ios", self.dispatcher._adapters)
        self.assertIn("android", self.dispatcher._adapters)
        self.assertIn("windows", self.dispatcher._adapters)
        self.assertIn("linux", self.dispatcher._adapters)
        self.assertEqual(self.dispatcher._adapters["ios"], self.dispatcher.get_adapter("ios"))

    def test_get_apple_adapter(self):
        """Test retrieving the Apple adapter for 'ios' and 'macos'."""
        adapter_ios = self.dispatcher.get_adapter("ios")
        self.assertIsInstance(adapter_ios, IOSAdapter)
        
        adapter_macos = self.dispatcher.get_adapter("macos")
        self.assertIsInstance(adapter_macos, IOSAdapter)

    def test_get_android_adapter(self):
        """Test retrieving the Android adapter."""
        adapter = self.dispatcher.get_adapter("android")
        self.assertIsInstance(adapter, AndroidAdapter)

    def test_get_windows_adapter(self):
        """Test retrieving the Windows adapter."""
        adapter = self.dispatcher.get_adapter("windows")
        self.assertIsInstance(adapter, WindowsAdapter)

    def test_get_linux_adapter(self):
        """Test retrieving the Linux adapter."""
        adapter = self.dispatcher.get_adapter("linux")
        self.assertIsInstance(adapter, LinuxAdapter)

    def test_get_unknown_adapter(self):
        """Test that an unknown OS returns None."""
        with self.assertRaises(ValueError):
            self.dispatcher.get_adapter("amigaos")

    def test_translate_for_ios(self):
        """Test the full translation flow for iOS."""
        translated_snapshot = self.dispatcher.translate(self.snapshot.copy(), "ios")
        
        # Check UI scaling
        self.assertEqual(translated_snapshot['ui_config']['scaling'], "ios_retina")
        
        # Check path mapping
        self.assertEqual(translated_snapshot['env']['DATA_PATH'], "/var/mobile/Containers/Data/Application/MilkApp")
        
        # Check input driver
        self.assertEqual(translated_snapshot['input_driver'], "ios_touch")

    def test_translate_for_android(self):
        """Test the full translation flow for Android."""
        translated_snapshot = self.dispatcher.translate(self.snapshot.copy(), "android")
        
        # Check permission mapping
        self.assertIn("android.permission.CAMERA", translated_snapshot['permissions'])
        
        # Check filesystem mapping
        self.assertEqual(translated_snapshot['env']['DATA_PATH'], "/storage/emulated/0/MilkApp")

    def test_translate_for_unsupported_os(self):
        """Test that translation for an unsupported OS returns the original snapshot."""
        original_snapshot = self.snapshot.copy()
        translated_snapshot = self.dispatcher.translate(original_snapshot, "freebsd")
        
        # The snapshot should be unchanged
        self.assertDictEqual(original_snapshot, translated_snapshot)

if __name__ == '__main__':
    unittest.main()
