"""
WekezaOmniOS Dirty Page Tracker
Phase 5: Tracks which memory pages have been modified during migration.

In production this hooks into kernel mechanisms (e.g. soft-dirty PTEs, userfaultfd);
the prototype uses a simple in-memory list per process.
"""
from .page_bitmap import PageBitmap


class DirtyPageTracker:
    """
    Tracks dirty memory pages per process during live migration.
    """

    def __init__(self, bitmap_size: int = 1024):
        self._bitmaps: dict = {}
        self._bitmap_size = bitmap_size

    def _get_bitmap(self, process_id: int) -> PageBitmap:
        if process_id not in self._bitmaps:
            self._bitmaps[process_id] = PageBitmap(self._bitmap_size)
        return self._bitmaps[process_id]

    def mark_dirty(self, process_id: int, page: int) -> None:
        """Mark a specific memory page as dirty for the given process."""
        self._get_bitmap(process_id).mark(page)

    def get_dirty_pages(self, process_id: int) -> list:
        """
        Return the list of dirty page indices for *process_id*.

        For the prototype, pages 0-9 are pre-marked dirty to simulate
        runtime writes during the copy window.
        """
        bitmap = self._get_bitmap(process_id)
        # Simulate runtime writes: mark pages 0-9 on first call
        if not bitmap.get_dirty():
            for i in range(10):
                bitmap.mark(i)
        return bitmap.get_dirty()

    def clear(self, process_id: int) -> None:
        """Reset dirty page tracking for a process after a copy round."""
        if process_id in self._bitmaps:
            del self._bitmaps[process_id]
Phase 5: Monitors memory writes during the pre-copy phase.
"""
from .page_bitmap import PageBitmap

class DirtyPageTracker:
    def __init__(self, total_pages=1000):
        self.bitmap = PageBitmap(total_pages)
        self.is_tracking = False

    def start_tracking(self):
        """Starts monitoring memory writes."""
        print("[Tracker] 🔍 Memory write-watch activated.")
        self.is_tracking = True

    def stop_tracking(self):
        """Deactivates monitoring for the final freeze."""
        self.is_tracking = False

    def mark_dirty(self, page_index):
        """Called by the kernel-hook/ptrace when a memory write occurs."""
        if self.is_tracking:
            self.bitmap.mark(page_index)

    def get_dirty_pages(self, process_id=None):
        """Returns current delta of modified pages."""
        return self.bitmap.get_dirty()
