"""
WekezaOmniOS System-Call Translator
Syscall mapping tables for the Cross-OS Runtime Layer.

This module centralises all OS-to-OS system call translation tables
so they can be imported by the SyscallTranslator without duplication.
"""

# ---------------------------------------------------------------------------
# Windows (Win32 / NT) → Linux syscall equivalents
# ---------------------------------------------------------------------------

WIN32_TO_LINUX = {
    # File I/O
    "NtCreateFile":        "openat",
    "NtReadFile":          "read",
    "NtWriteFile":         "write",
    "NtClose":             "close",
    "NtDeleteFile":        "unlinkat",
    "NtQueryInformationFile": "stat",
    "NtSetInformationFile": "fcntl",

    # Process / thread
    "NtCreateProcess":     "clone",
    "NtCreateThread":      "clone",
    "NtTerminateProcess":  "exit_group",
    "NtTerminateThread":   "exit",
    "NtSuspendThread":     "kill",         # SIGSTOP equivalent
    "NtResumeThread":      "kill",         # SIGCONT equivalent
    "NtWaitForSingleObject": "futex",

    # Memory
    "NtAllocateVirtualMemory": "mmap",
    "NtFreeVirtualMemory":     "munmap",
    "NtProtectVirtualMemory":  "mprotect",
    "NtMapViewOfSection":      "mmap",

    # IPC / sync
    "NtCreateEvent":       "eventfd",
    "NtCreateMutant":      "futex",
    "NtCreateSemaphore":   "semget",
    "NtCreateSection":     "memfd_create",

    # Networking
    "NtDeviceIoControlFile": "ioctl",
    "WSASocket":             "socket",
    "WSAConnect":            "connect",
    "WSARecv":               "recvmsg",
    "WSASend":               "sendmsg",
}

# ---------------------------------------------------------------------------
# Android (Binder / Bionic) → Linux syscall equivalents
# ---------------------------------------------------------------------------

ANDROID_TO_LINUX = {
    # Binder IPC
    "BINDER_WRITE_READ":   "ioctl",
    "BINDER_SET_MAX_THREADS": "prctl",
    "BINDER_THREAD_EXIT":  "exit",
    "BINDER_VERSION":      "ioctl",

    # Bionic libc (subset where name differs from glibc)
    "android_mmap":        "mmap",
    "android_open":        "openat",
    "android_ioctl":       "ioctl",
    "android_recvmsg":     "recvmsg",
    "android_sendmsg":     "sendmsg",

    # ART runtime
    "art_allocate":        "mmap",
    "art_gc":              "madvise",
}

# ---------------------------------------------------------------------------
# macOS (XNU/Mach) → Linux syscall equivalents
# ---------------------------------------------------------------------------

MACOS_TO_LINUX = {
    # Mach messages
    "mach_msg":            "sendmsg",
    "mach_port_allocate":  "memfd_create",
    "mach_port_destroy":   "close",

    # BSD layer
    "open$UNIX2003":       "openat",
    "read$UNIX2003":       "read",
    "write$UNIX2003":      "write",
    "mmap$UNIX2003":       "mmap",
    "munmap$UNIX2003":     "munmap",
    "fork$UNIX2003":       "clone",
    "execve$UNIX2003":     "execve",

    # Dispatch / GCD
    "dispatch_async":      "io_uring_enter",
    "dispatch_sync":       "futex",
}

# ---------------------------------------------------------------------------
# Registry: source OS → translation table
# ---------------------------------------------------------------------------

SYSCALL_TABLES = {
    "windows": WIN32_TO_LINUX,
    "android": ANDROID_TO_LINUX,
    "macos":   MACOS_TO_LINUX,
    "linux":   {},   # identity mapping — no translation needed
}
