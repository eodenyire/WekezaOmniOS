"""
WekezaOmniOS Linux Runtime Module
Provides POSIX-native compatibility support within the Cross-OS Runtime
Layer.  Because the host is typically Linux, this module acts as the
transparent pass-through layer while still normalising metadata for the
universal runtime format.
"""

import os


# POSIX signal number → canonical signal name
SIGNAL_NAMES = {
    1:  "SIGHUP",
    2:  "SIGINT",
    9:  "SIGKILL",
    15: "SIGTERM",
    17: "SIGCHLD",
    18: "SIGCONT",
    19: "SIGSTOP",
}


class LinuxRuntime:
    """
    Compatibility module for Linux/POSIX applications.

    Responsibilities:
    - Verify and normalise POSIX paths.
    - Map Linux signal numbers to canonical names.
    - Pass environment variables through with minimal transformation.
    - Translate process state into the universal runtime format.
    """

    OS_NAME = "Linux"

    def __init__(self):
        print(f"[{self.OS_NAME}Runtime] Module loaded.")

    # ------------------------------------------------------------------
    # Path utilities
    # ------------------------------------------------------------------

    def normalise_path(self, posix_path):
        """
        Resolves and normalises a POSIX filesystem path.

        Args:
            posix_path (str): Potentially relative or redundant path.

        Returns:
            str: Normalised absolute-style path.
        """
        normalised = os.path.normpath(posix_path)
        print(
            f"[{self.OS_NAME}Runtime] Path normalised: "
            f"{posix_path!r} → {normalised!r}"
        )
        return normalised

    # ------------------------------------------------------------------
    # Signal mapping
    # ------------------------------------------------------------------

    def signal_name(self, signal_number):
        """
        Returns the canonical name for a Linux signal number.

        Args:
            signal_number (int): POSIX signal number.

        Returns:
            str: Signal name or 'SIG<N>' for unknown signals.
        """
        name = SIGNAL_NAMES.get(signal_number, f"SIG{signal_number}")
        print(
            f"[{self.OS_NAME}Runtime] Signal {signal_number} → {name}"
        )
        return name

    # ------------------------------------------------------------------
    # Environment adaptation
    # ------------------------------------------------------------------

    def adapt_environment(self, env_vars):
        """
        Ensures the environment carries the universal OS_TYPE marker.

        Args:
            env_vars (dict): Process environment dictionary.

        Returns:
            dict: Adapted environment dictionary.
        """
        adapted = dict(env_vars)
        adapted["OS_TYPE"] = "linux"
        print(f"[{self.OS_NAME}Runtime] Environment adapted.")
        return adapted

    # ------------------------------------------------------------------
    # State translation
    # ------------------------------------------------------------------

    def translate_process_state(self, snapshot):
        """
        Translates a Linux process snapshot into the universal runtime
        format.  Because Linux is the host, most fields pass through
        unchanged; only the universal metadata tag is added.

        Args:
            snapshot (dict): Raw Linux process state.

        Returns:
            dict: Universal process state.
        """
        state = snapshot.copy()
        state["source_os"] = "linux"

        if "open_files" in state:
            state["open_files"] = [
                self.normalise_path(p) for p in state["open_files"]
            ]
        if "env" in state:
            state["env"] = self.adapt_environment(state["env"])

        print(f"[{self.OS_NAME}Runtime] Process state translated.")
        return state

    # ------------------------------------------------------------------
    # Syscall interception placeholder
    # ------------------------------------------------------------------

    def handle_system_calls(self, intercepted_calls):
        """
        Entry point for ptrace-based syscall interception.
        In this phase the method logs each intercepted call and returns
        it unchanged.  A real implementation would apply seccomp
        filters here.

        Args:
            intercepted_calls (list[str]): List of syscall names to process.

        Returns:
            list[str]: The same calls (pass-through for now).
        """
        for call in intercepted_calls:
            print(f"[{self.OS_NAME}Runtime] Intercepted syscall: {call!r}")
        return intercepted_calls


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    runtime = LinuxRuntime()

    runtime.normalise_path("/home/alice/../alice/docs/report.txt")
    runtime.signal_name(15)
    runtime.signal_name(9)

    snapshot = {
        "pid": 5001,
        "open_files": ["/home/alice/data.txt", "/var/log/app.log"],
        "env": {"HOME": "/home/alice", "USER": "alice"},
        "app_state": {"cwd": "/home/alice/projects"},
    }
    import json
    translated = runtime.translate_process_state(snapshot)
    print(json.dumps(translated, indent=2))
