"""
WekezaOmniOS Sandbox
Security isolation layer for the Cross-OS Runtime Layer.

Isolates applications using three complementary mechanisms inspired by
Linux container technologies:
  1. Namespace sets (mount, pid, net, ipc, uts, user)
  2. Seccomp allow-lists (system call filtering)
  3. cgroup resource limits (cpu, memory, blkio)

In this research phase the implementation models the configuration and
audit logic; actual kernel calls would be wired in during OS integration.
"""

import threading
import time


# ---------------------------------------------------------------------------
# Default seccomp allow-list (minimal POSIX subset safe for sandboxed apps)
# ---------------------------------------------------------------------------

DEFAULT_ALLOWED_SYSCALLS = frozenset({
    "read", "write", "open", "openat", "close", "stat", "fstat",
    "lstat", "mmap", "mprotect", "munmap", "brk", "sigreturn",
    "exit", "exit_group", "futex", "clock_gettime", "nanosleep",
    "socket", "connect", "sendmsg", "recvmsg", "bind", "listen",
    "accept", "epoll_wait", "epoll_ctl", "epoll_create1",
    "ioctl", "fcntl", "dup", "dup2", "pipe",
    "select", "poll", "sendfile", "clone", "execve", "wait4",
    "getpid", "getppid", "getuid", "getgid", "geteuid", "getegid",
})

# Syscalls that are always blocked (privileged / dangerous)
BLOCKED_SYSCALLS = frozenset({
    "ptrace", "kexec_load", "init_module", "finit_module",
    "delete_module", "mount", "umount2", "pivot_root", "chroot",
    "reboot", "swapon", "swapoff", "setns", "unshare",
})


class SandboxConfig:
    """Holds the security policy for a single sandboxed process."""

    def __init__(self, pid, name,
                 allowed_syscalls=None,
                 extra_blocked=None,
                 cpu_limit_pct=100,
                 memory_limit_bytes=None,
                 network_isolated=False):
        self.pid               = pid
        self.name              = name
        self.allowed_syscalls  = set(allowed_syscalls or DEFAULT_ALLOWED_SYSCALLS)
        self.blocked_syscalls  = set(BLOCKED_SYSCALLS) | set(extra_blocked or [])
        self.cpu_limit_pct     = cpu_limit_pct
        self.memory_limit_bytes = memory_limit_bytes or (256 * 1024 * 1024)
        self.network_isolated  = network_isolated
        self.created_at        = time.strftime("%Y-%m-%dT%H:%M:%S")

    def to_dict(self):
        return {
            "pid":                  self.pid,
            "name":                 self.name,
            "allowed_syscalls":     sorted(self.allowed_syscalls),
            "blocked_syscalls":     sorted(self.blocked_syscalls),
            "cpu_limit_pct":        self.cpu_limit_pct,
            "memory_limit_bytes":   self.memory_limit_bytes,
            "network_isolated":     self.network_isolated,
            "created_at":           self.created_at,
        }


class Sandbox:
    """
    Security isolation layer for the Cross-OS Runtime Layer.

    Responsibilities:
    - Apply namespace sets per isolated process.
    - Enforce seccomp syscall allow/block lists.
    - Enforce cgroup resource limits.
    - Audit all security events.
    """

    def __init__(self):
        self._lock    = threading.Lock()
        self._configs = {}          # pid -> SandboxConfig
        self._audit   = []          # list of audit log entries
        print("[Sandbox] Initialised.")

    # ------------------------------------------------------------------
    # Isolation entry point
    # ------------------------------------------------------------------

    def isolate(self, pid, name, cpu_limit_pct=80,
                memory_limit_mb=256, network_isolated=True,
                extra_blocked=None):
        """
        Places a process inside a sandboxed container.

        Args:
            pid (int): Process identifier to isolate.
            name (str): Application name (for logging).
            cpu_limit_pct (int): CPU time percentage ceiling (1–100).
            memory_limit_mb (int): RAM ceiling in MiB.
            network_isolated (bool): Whether network access is blocked.
            extra_blocked (list | None): Additional syscalls to block.

        Returns:
            SandboxConfig: The applied security configuration.
        """
        with self._lock:
            config = SandboxConfig(
                pid=pid,
                name=name,
                cpu_limit_pct=cpu_limit_pct,
                memory_limit_bytes=memory_limit_mb * 1024 * 1024,
                network_isolated=network_isolated,
                extra_blocked=extra_blocked,
            )
            self._configs[pid] = config

        self._apply_namespaces(config)
        self._apply_seccomp(config)
        self._apply_cgroups(config)

        self._audit_event(pid, "ISOLATE", f"Sandbox applied to '{name}'.")
        print(
            f"[Sandbox] 🔒 PID {pid} ('{name}') isolated. "
            f"cpu≤{cpu_limit_pct}%, "
            f"mem≤{memory_limit_mb}MiB, "
            f"network={'blocked' if network_isolated else 'allowed'}."
        )
        return config

    # ------------------------------------------------------------------
    # Syscall enforcement
    # ------------------------------------------------------------------

    def check_syscall(self, pid, syscall_name):
        """
        Determines whether a process is allowed to execute a syscall.

        Args:
            pid (int): Process identifier.
            syscall_name (str): System call name to evaluate.

        Returns:
            bool: True if permitted, False if blocked.
        """
        with self._lock:
            config = self._configs.get(pid)

        if config is None:
            # No sandbox configured — allow by default (unsandboxed process)
            return True

        if syscall_name in config.blocked_syscalls:
            self._audit_event(pid, "BLOCK",
                              f"Syscall {syscall_name!r} blocked.")
            print(
                f"[Sandbox] 🚫 PID {pid}: syscall {syscall_name!r} BLOCKED."
            )
            return False

        if syscall_name in config.allowed_syscalls:
            return True

        # Syscall is neither explicitly allowed nor blocked — deny by default
        self._audit_event(pid, "DENY",
                          f"Syscall {syscall_name!r} not in allow-list.")
        print(
            f"[Sandbox] ⚠️  PID {pid}: syscall {syscall_name!r} "
            f"not in allow-list — denied."
        )
        return False

    # ------------------------------------------------------------------
    # Release
    # ------------------------------------------------------------------

    def release(self, pid):
        """
        Removes the sandbox for a terminated process and frees resources.

        Args:
            pid (int): Process identifier.
        """
        with self._lock:
            config = self._configs.pop(pid, None)
        if config:
            self._audit_event(pid, "RELEASE",
                              f"Sandbox released for '{config.name}'.")
            print(f"[Sandbox] 🔓 PID {pid} ('{config.name}') released.")
        else:
            print(f"[Sandbox] ⚠️  PID {pid} has no active sandbox.")

    # ------------------------------------------------------------------
    # Audit log
    # ------------------------------------------------------------------

    def audit_log(self, pid=None):
        """
        Returns recorded security events.

        Args:
            pid (int | None): If given, only events for this PID are
                              returned; otherwise all events are returned.

        Returns:
            list[dict]: Audit log entries.
        """
        with self._lock:
            entries = list(self._audit)
        if pid is not None:
            entries = [e for e in entries if e["pid"] == pid]
        return entries

    # ------------------------------------------------------------------
    # Private kernel interface stubs
    # ------------------------------------------------------------------

    def _apply_namespaces(self, config):
        """
        Configures Linux namespaces for the process.
        (Stub — real implementation calls clone(2) with CLONE_NEW* flags.)
        """
        namespaces = ["pid", "net", "mnt", "ipc", "uts"]
        if config.network_isolated:
            namespaces.append("net:isolated")
        print(
            f"[Sandbox] Namespaces applied for PID {config.pid}: "
            f"{', '.join(namespaces)}"
        )

    def _apply_seccomp(self, config):
        """
        Installs the seccomp BPF filter for the process.
        (Stub — real implementation calls prctl(PR_SET_SECCOMP, ...).)
        """
        print(
            f"[Sandbox] Seccomp filter installed for PID {config.pid}: "
            f"{len(config.allowed_syscalls)} allowed, "
            f"{len(config.blocked_syscalls)} blocked."
        )

    def _apply_cgroups(self, config):
        """
        Creates cgroup entries and writes resource limits.
        (Stub — real implementation writes to /sys/fs/cgroup/.)
        """
        print(
            f"[Sandbox] cgroups configured for PID {config.pid}: "
            f"cpu={config.cpu_limit_pct}%, "
            f"memory={config.memory_limit_bytes // (1024*1024)}MiB."
        )

    def _audit_event(self, pid, event_type, message):
        entry = {
            "timestamp":  time.strftime("%Y-%m-%dT%H:%M:%S"),
            "pid":        pid,
            "event_type": event_type,
            "message":    message,
        }
        with self._lock:
            self._audit.append(entry)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json

    sandbox = Sandbox()

    sandbox.isolate(9001, "notepad.exe",
                    cpu_limit_pct=50, memory_limit_mb=128,
                    network_isolated=True)
    sandbox.isolate(9002, "com.bank.app",
                    cpu_limit_pct=60, memory_limit_mb=256,
                    network_isolated=False)

    print("\n--- Syscall checks ---")
    print(sandbox.check_syscall(9001, "read"))          # allowed
    print(sandbox.check_syscall(9001, "ptrace"))        # blocked
    print(sandbox.check_syscall(9001, "kexec_load"))    # blocked
    print(sandbox.check_syscall(9001, "io_uring_setup")) # not in allow-list

    sandbox.release(9002)

    print("\n--- Audit log for PID 9001 ---")
    print(json.dumps(sandbox.audit_log(pid=9001), indent=2))
