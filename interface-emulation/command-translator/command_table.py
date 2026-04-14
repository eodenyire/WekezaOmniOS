"""
WekezaOmniOS Interface Emulation — Command Tables
==================================================
Static mapping dictionaries that translate shell commands from Windows,
macOS, and cmd source environments to Linux equivalents.
"""

COMMAND_TABLES: dict[str, dict[str, str]] = {
    "windows": {
        "dir":      "ls",
        "copy":     "cp",
        "move":     "mv",
        "del":      "rm",
        "type":     "cat",
        "cls":      "clear",
        "echo":     "echo",
        "rename":   "mv",
        "mkdir":    "mkdir",
        "rmdir":    "rmdir -r",
        "tasklist": "ps aux",
        "taskkill": "kill",
        "ipconfig": "ifconfig",
        "netstat":  "netstat",
        "ping":     "ping",
        "attrib":   "chmod",
        "xcopy":    "rsync",
        "find":     "grep",
        "sort":     "sort",
        "more":     "less",
        "shutdown": "shutdown",
    },
    "macos": {
        "open":       "xdg-open",
        "pbcopy":     "xclip -selection clipboard",
        "pbpaste":    "xclip -selection clipboard -o",
        "say":        "espeak",
        "defaults":   "gsettings",
        "launchctl":  "systemctl",
        "sw_vers":    "lsb_release -a",
        "caffeinate": "caffeine",
    },
}

# cmd is an alias for windows
COMMAND_TABLES["cmd"] = COMMAND_TABLES["windows"]
