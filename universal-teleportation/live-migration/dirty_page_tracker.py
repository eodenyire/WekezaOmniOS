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
