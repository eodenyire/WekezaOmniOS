"""
WekezaOmniOS Interface Emulation — Base Skin
=============================================
Abstract base class that all desktop environment skins must implement.
"""

from abc import ABC, abstractmethod


class BaseSkin(ABC):
    """
    Abstract interface for all WekezaOmniOS desktop environment skins.

    Each concrete skin must implement the five abstract members below
    so the DesktopManager can swap environments without knowing which
    skin is active.
    """

    @property
    @abstractmethod
    def skin_name(self) -> str:
        """Returns the human-readable skin identifier."""

    @abstractmethod
    def render_taskbar(self) -> str:
        """Renders and returns the taskbar/panel as a string."""

    @abstractmethod
    def render_start_menu(self) -> str:
        """Renders and returns the start/launcher menu as a string."""

    @abstractmethod
    def render_file_manager(self, path: str = "/") -> str:
        """
        Renders and returns the file manager view for *path*.

        Args:
            path (str): Directory path to display.
        """

    @abstractmethod
    def render_system_tray(self) -> str:
        """Renders and returns the system tray / notification area."""
