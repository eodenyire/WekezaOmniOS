"""
WekezaOmniOS Syscall Translator
Translates operating system system calls from any supported source OS
into Linux kernel calls used by the Cross-OS Runtime Layer.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from syscall_table import SYSCALL_TABLES


class SyscallTranslator:
    """
    Translates individual system calls from a source OS to the Linux
    kernel call that the universal runtime layer will execute.

    Design:
    - For known source OSes, looks up the call in the prebuilt table.
    - For Linux sources, the call is returned unchanged (identity).
    - Unknown calls are logged and returned unchanged so the runtime
      can decide how to handle them.
    """

    def __init__(self, source_os="linux"):
        """
        Args:
            source_os (str): The OS whose syscalls need translating
                             ('windows', 'android', 'macos', 'linux').
        """
        self.source_os = source_os.lower()
        self._table = SYSCALL_TABLES.get(self.source_os, {})
        print(
            f"[SyscallTranslator] Initialised for source OS: {self.source_os} "
            f"({len(self._table)} mappings loaded)"
        )

    # ------------------------------------------------------------------
    # Core translation
    # ------------------------------------------------------------------

    def translate(self, syscall_name):
        """
        Translates a single system call name.

        Args:
            syscall_name (str): The source-OS system call identifier.

        Returns:
            str: The Linux syscall equivalent, or the original name if
                 no mapping is defined.
        """
        if self.source_os == "linux":
            return syscall_name   # identity — no translation needed

        translated = self._table.get(syscall_name)
        if translated:
            print(
                f"[SyscallTranslator] {self.source_os}: "
                f"{syscall_name!r} → {translated!r}"
            )
            return translated

        print(
            f"[SyscallTranslator] ⚠️  No mapping for {syscall_name!r} "
            f"(source={self.source_os}) — passing through unchanged."
        )
        return syscall_name

    def translate_batch(self, syscall_names):
        """
        Translates a list of system call names in one pass.

        Args:
            syscall_names (list[str]): System call names to translate.

        Returns:
            list[dict]: Each entry has 'source' and 'translated' keys.
        """
        results = []
        for name in syscall_names:
            results.append({
                "source":     name,
                "translated": self.translate(name),
            })
        return results

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def supported_calls(self):
        """
        Returns a sorted list of source OS calls that have known
        translations.

        Returns:
            list[str]: Sorted syscall names with mappings.
        """
        return sorted(self._table.keys())

    def coverage(self):
        """
        Returns the number of syscalls that have explicit translations.

        Returns:
            int: Count of mapped syscalls.
        """
        return len(self._table)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Windows → Linux ===")
    win_translator = SyscallTranslator(source_os="windows")
    calls = ["NtCreateFile", "NtReadFile", "NtAllocateVirtualMemory",
             "NtCreateProcess", "UnknownWinCall"]
    results = win_translator.translate_batch(calls)
    for r in results:
        print(f"  {r['source']:35s} → {r['translated']}")

    print("\n=== Android → Linux ===")
    android_translator = SyscallTranslator(source_os="android")
    android_calls = ["BINDER_WRITE_READ", "art_allocate", "android_open"]
    results = android_translator.translate_batch(android_calls)
    for r in results:
        print(f"  {r['source']:35s} → {r['translated']}")

    print("\n=== macOS → Linux ===")
    mac_translator = SyscallTranslator(source_os="macos")
    mac_calls = ["mach_msg", "dispatch_async", "fork$UNIX2003"]
    results = mac_translator.translate_batch(mac_calls)
    for r in results:
        print(f"  {r['source']:35s} → {r['translated']}")

    print(f"\nWindows coverage: {win_translator.coverage()} calls")
