"""
WekezaOmniOS Dirty Page Tracker
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
