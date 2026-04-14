"""
WekezaOmniOS System-Call Translator — package init.
"""
from .syscall_translator import SyscallTranslator
from .syscall_table import SYSCALL_TABLES

__all__ = ["SyscallTranslator", "SYSCALL_TABLES"]
