"""
WekezaOmniOS Sandbox — package init.
"""
from .sandbox import Sandbox, SandboxConfig, DEFAULT_ALLOWED_SYSCALLS

__all__ = ["Sandbox", "SandboxConfig", "DEFAULT_ALLOWED_SYSCALLS"]
