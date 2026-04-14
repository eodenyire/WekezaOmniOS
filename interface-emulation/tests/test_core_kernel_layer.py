"""
WekezaOmniOS Interface Emulation — Core Kernel Layer Tests
===========================================================
pytest tests for VirtualFilesystem, ProcessManager, and NetworkStack.
"""

import os
import sys
import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_BASE, "core-kernel-layer"))

from filesystem import VirtualFilesystem
from process_manager import ProcessManager
from network_stack import NetworkStack


# ===========================================================================
# VirtualFilesystem
# ===========================================================================

class TestVirtualFilesystem:

    def setup_method(self):
        self.vfs = VirtualFilesystem()

    def test_mount_and_list(self):
        self.vfs.mount("/dev/sda1", "/", "ext4")
        mounts = self.vfs.list_mounts()
        assert len(mounts) == 1
        assert mounts[0]["source"] == "/dev/sda1"
        assert mounts[0]["target"] == "/"
        assert mounts[0]["fs_type"] == "ext4"

    def test_mount_default_fs_type(self):
        self.vfs.mount("/dev/sda2", "/home")
        mounts = self.vfs.list_mounts()
        assert mounts[0]["fs_type"] == "ext4"

    def test_unmount(self):
        self.vfs.mount("/dev/sda1", "/", "ext4")
        self.vfs.unmount("/")
        assert self.vfs.list_mounts() == []

    def test_unmount_nonexistent_raises(self):
        with pytest.raises(KeyError):
            self.vfs.unmount("/nonexistent")

    def test_exists_mounted_path(self):
        self.vfs.mount("/dev/sda1", "/", "ext4")
        assert self.vfs.exists("/")

    def test_exists_subpath_of_mount(self):
        self.vfs.mount("/dev/sda2", "/home", "ext4")
        assert self.vfs.exists("/home/user/docs")

    def test_exists_false_when_no_mount(self):
        assert not self.vfs.exists("/etc")

    def test_resolve_path_trailing_slash(self):
        assert self.vfs.resolve_path("/home/user/") == "/home/user"

    def test_resolve_path_tilde(self):
        assert self.vfs.resolve_path("~/Downloads") == "/home/user/Downloads"

    def test_resolve_path_root(self):
        assert self.vfs.resolve_path("/") == "/"

    def test_list_mounts_multiple(self):
        self.vfs.mount("/dev/sda1", "/", "ext4")
        self.vfs.mount("tmpfs", "/tmp", "tmpfs")
        mounts = self.vfs.list_mounts()
        assert len(mounts) == 2
        targets = {m["target"] for m in mounts}
        assert targets == {"/", "/tmp"}


# ===========================================================================
# ProcessManager
# ===========================================================================

class TestProcessManager:

    def setup_method(self):
        self.pm = ProcessManager()

    def test_spawn_returns_pid(self):
        pid = self.pm.spawn("bash", "linux")
        assert isinstance(pid, int)
        assert pid >= 1000

    def test_spawn_stores_process(self):
        pid = self.pm.spawn("test_proc", "windows", priority=3)
        proc = self.pm.get_process(pid)
        assert proc is not None
        assert proc["name"] == "test_proc"
        assert proc["os_type"] == "windows"
        assert proc["priority"] == 3
        assert proc["state"] == "running"

    def test_spawn_auto_increment(self):
        pid1 = self.pm.spawn("p1")
        pid2 = self.pm.spawn("p2")
        assert pid2 == pid1 + 1

    def test_terminate_removes_process(self):
        pid = self.pm.spawn("proc")
        self.pm.terminate(pid)
        assert self.pm.get_process(pid) is None

    def test_terminate_invalid_raises(self):
        with pytest.raises(ValueError):
            self.pm.terminate(9999)

    def test_suspend_changes_state(self):
        pid = self.pm.spawn("proc")
        self.pm.suspend(pid)
        assert self.pm.get_process(pid)["state"] == "suspended"

    def test_resume_changes_state(self):
        pid = self.pm.spawn("proc")
        self.pm.suspend(pid)
        self.pm.resume(pid)
        assert self.pm.get_process(pid)["state"] == "running"

    def test_suspend_invalid_raises(self):
        with pytest.raises(ValueError):
            self.pm.suspend(9999)

    def test_resume_invalid_raises(self):
        with pytest.raises(ValueError):
            self.pm.resume(9999)

    def test_list_processes(self):
        pid1 = self.pm.spawn("p1")
        pid2 = self.pm.spawn("p2")
        procs = self.pm.list_processes()
        pids = {p["pid"] for p in procs}
        assert pid1 in pids
        assert pid2 in pids

    def test_get_process_none_for_unknown(self):
        assert self.pm.get_process(99999) is None


# ===========================================================================
# NetworkStack
# ===========================================================================

class TestNetworkStack:

    def setup_method(self):
        self.ns = NetworkStack()

    def test_add_interface(self):
        self.ns.add_interface("eth0", "192.168.1.10")
        ifaces = self.ns.list_interfaces()
        assert len(ifaces) == 1
        assert ifaces[0]["name"] == "eth0"
        assert ifaces[0]["ip"] == "192.168.1.10"
        assert ifaces[0]["netmask"] == "255.255.255.0"

    def test_add_interface_custom_netmask(self):
        self.ns.add_interface("lo", "127.0.0.1", "255.0.0.0")
        assert self.ns.list_interfaces()[0]["netmask"] == "255.0.0.0"

    def test_remove_interface(self):
        self.ns.add_interface("eth0", "10.0.0.1")
        self.ns.remove_interface("eth0")
        assert self.ns.list_interfaces() == []

    def test_remove_interface_not_found_raises(self):
        with pytest.raises(KeyError):
            self.ns.remove_interface("eth99")

    def test_list_interfaces_multiple(self):
        self.ns.add_interface("eth0", "10.0.0.1")
        self.ns.add_interface("wlan0", "192.168.0.5")
        assert len(self.ns.list_interfaces()) == 2

    def test_ping_returns_true(self):
        assert self.ns.ping("8.8.8.8") is True

    def test_ping_any_host(self):
        assert self.ns.ping("example.com") is True

    def test_resolve_localhost(self):
        assert self.ns.resolve("localhost") == "127.0.0.1"

    def test_resolve_loopback_ip(self):
        assert self.ns.resolve("127.0.0.1") == "127.0.0.1"

    def test_resolve_external_returns_fake_ip(self):
        ip = self.ns.resolve("example.com")
        assert ip.startswith("10.")

    def test_resolve_deterministic(self):
        assert self.ns.resolve("omnios.dev") == self.ns.resolve("omnios.dev")
