"""
WekezaOmniOS UI Compositor
Allows applications from different OS ecosystems to appear together
inside one unified desktop session.

Architecture:
  Each application registers a WindowDescriptor describing its native
  UI properties.  The UICompositor translates those properties into a
  unified layout and emits a composite scene for the display server.
"""

import time
import threading


# ---------------------------------------------------------------------------
# Canonical window states
# ---------------------------------------------------------------------------

WINDOW_STATES = ("normal", "minimised", "maximised", "fullscreen", "hidden")


class WindowDescriptor:
    """
    Describes a top-level window contributed by an application.

    Fields are OS-agnostic: native values are normalised on registration.
    """

    def __init__(self, win_id, app_id, title, os_type,
                 x=0, y=0, width=800, height=600, z_order=0,
                 state="normal"):
        self.win_id   = win_id
        self.app_id   = app_id
        self.title    = title
        self.os_type  = os_type
        self.x        = x
        self.y        = y
        self.width    = width
        self.height   = height
        self.z_order  = z_order   # higher = closer to front
        self.state    = state

    def to_dict(self):
        return {
            "win_id":  self.win_id,
            "app_id":  self.app_id,
            "title":   self.title,
            "os_type": self.os_type,
            "x":       self.x,
            "y":       self.y,
            "width":   self.width,
            "height":  self.height,
            "z_order": self.z_order,
            "state":   self.state,
        }

    def __repr__(self):
        return (
            f"<Window id={self.win_id!r} title={self.title!r} "
            f"os={self.os_type} state={self.state}>"
        )


class UICompositor:
    """
    Composes windows from multiple OS environments into a single desktop.

    Responsibilities:
    - Register and track windows from any supported OS.
    - Translate OS-specific window properties into a canonical format.
    - Manage Z-ordering and focus.
    - Render a composite scene description for the display server.
    """

    def __init__(self, desktop_width=1920, desktop_height=1080):
        self._lock    = threading.Lock()
        self._windows = {}          # win_id -> WindowDescriptor
        self._focus   = None        # currently focused win_id
        self.desktop_width  = desktop_width
        self.desktop_height = desktop_height
        print(
            f"[UICompositor] Initialised. "
            f"Desktop: {desktop_width}×{desktop_height}"
        )

    # ------------------------------------------------------------------
    # Window registration
    # ------------------------------------------------------------------

    def register_window(self, win_id, app_id, title, os_type,
                        x=0, y=0, width=800, height=600,
                        z_order=None, state="normal"):
        """
        Registers a new window from any OS environment.

        Args:
            win_id (str): Unique window identifier.
            app_id (str): Owning application identifier.
            title (str): Window title bar text.
            os_type (str): Source OS ('windows', 'linux', 'android', …).
            x, y (int): Top-left position on the virtual desktop.
            width, height (int): Window dimensions in pixels.
            z_order (int | None): Stacking position; auto-assigned if None.
            state (str): Initial window state (normal, minimised, …).

        Returns:
            WindowDescriptor: The created window descriptor.
        """
        with self._lock:
            if win_id in self._windows:
                print(f"[UICompositor] ⚠️  Window {win_id!r} already registered.")
                return self._windows[win_id]

            if z_order is None:
                z_order = max(
                    (w.z_order for w in self._windows.values()), default=0
                ) + 1

            # Normalise dimensions to fit the virtual desktop
            width  = min(width,  self.desktop_width)
            height = min(height, self.desktop_height)

            desc = WindowDescriptor(
                win_id, app_id, title, os_type,
                x=x, y=y, width=width, height=height,
                z_order=z_order, state=state,
            )
            self._windows[win_id] = desc
            print(
                f"[UICompositor] ✅ Window registered: {desc} "
                f"at ({x},{y}) {width}×{height} z={z_order}"
            )
            return desc

    # ------------------------------------------------------------------
    # Window management
    # ------------------------------------------------------------------

    def move_window(self, win_id, x, y):
        """Moves a window to a new position on the virtual desktop."""
        win = self._get(win_id)
        if win:
            win.x, win.y = x, y
            print(f"[UICompositor] Moved {win_id!r} to ({x}, {y}).")

    def resize_window(self, win_id, width, height):
        """Resizes a window, clamped to desktop dimensions."""
        win = self._get(win_id)
        if win:
            win.width  = min(width,  self.desktop_width)
            win.height = min(height, self.desktop_height)
            print(
                f"[UICompositor] Resized {win_id!r} to "
                f"{win.width}×{win.height}."
            )

    def set_state(self, win_id, state):
        """
        Sets the window state.

        Args:
            win_id (str): Target window identifier.
            state (str): One of WINDOW_STATES.
        """
        if state not in WINDOW_STATES:
            print(f"[UICompositor] ⚠️  Unknown state {state!r}.")
            return
        win = self._get(win_id)
        if win:
            win.state = state
            print(f"[UICompositor] Window {win_id!r} → {state}.")

    def focus(self, win_id):
        """Brings a window to the front and records focus."""
        win = self._get(win_id)
        if win:
            win.z_order = max(
                (w.z_order for w in self._windows.values()), default=0
            ) + 1
            self._focus = win_id
            print(
                f"[UICompositor] 🎯 Focus: {win.title!r} "
                f"(os={win.os_type}, z={win.z_order})"
            )

    def close_window(self, win_id):
        """Removes a window from the compositor."""
        with self._lock:
            win = self._windows.pop(win_id, None)
        if win:
            if self._focus == win_id:
                self._focus = None
            print(f"[UICompositor] ❌ Window {win_id!r} ('{win.title}') closed.")
        else:
            print(f"[UICompositor] ⚠️  Window {win_id!r} not found.")

    # ------------------------------------------------------------------
    # Scene rendering
    # ------------------------------------------------------------------

    def render_scene(self):
        """
        Produces a composite scene description sorted by Z-order.

        Returns:
            dict: Scene metadata and ordered list of window descriptors.
        """
        with self._lock:
            ordered = sorted(
                self._windows.values(),
                key=lambda w: w.z_order,
            )

        scene = {
            "timestamp":       time.strftime("%Y-%m-%dT%H:%M:%S"),
            "desktop_size":    f"{self.desktop_width}×{self.desktop_height}",
            "focused_win":     self._focus,
            "window_count":    len(ordered),
            "windows":         [w.to_dict() for w in ordered],
        }
        print(
            f"[UICompositor] 🖥  Scene rendered: "
            f"{scene['window_count']} window(s)."
        )
        return scene

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def list_windows(self, os_filter=None):
        """
        Lists registered windows, optionally filtered by source OS.

        Args:
            os_filter (str | None): If given, only windows from this OS
                                    are returned.

        Returns:
            list[WindowDescriptor]: Matching windows.
        """
        with self._lock:
            windows = list(self._windows.values())
        if os_filter:
            windows = [w for w in windows if w.os_type == os_filter]
        return windows

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get(self, win_id):
        win = self._windows.get(win_id)
        if not win:
            print(f"[UICompositor] ❌ Window {win_id!r} not found.")
        return win


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json

    compositor = UICompositor(desktop_width=1920, desktop_height=1080)

    # Register windows from three different OS ecosystems
    compositor.register_window(
        "win:notepad", "notepad", "Notepad Classic - C:\\docs\\report.txt",
        "windows", x=100, y=50, width=640, height=480,
    )
    compositor.register_window(
        "win:banking", "com.bank.app", "Mobile Banking Dashboard",
        "android", x=760, y=50, width=360, height=640,
    )
    compositor.register_window(
        "win:htop", "htop", "htop — system monitor",
        "linux", x=100, y=550, width=900, height=400,
    )

    compositor.focus("win:banking")
    compositor.set_state("win:notepad", "minimised")
    compositor.move_window("win:htop", 200, 600)
    compositor.resize_window("win:banking", 400, 700)

    scene = compositor.render_scene()
    print("\n[UICompositor] Scene JSON:")
    print(json.dumps(scene, indent=2))

    print("\n[UICompositor] Android windows only:")
    for w in compositor.list_windows(os_filter="android"):
        print(" ", w)
