"""
WekezaOmniOS Page Bitmap
Phase 5: High-efficiency data structure for tracking dirty memory pages.
"""

class PageBitmap:
    def __init__(self, size):
        self.size = size
        # 0 = clean, 1 = dirty. Bytearray is more memory-efficient than a list.
        self.bitmap = bytearray(size)

    def mark(self, page_index):
        if 0 <= page_index < self.size:
            self.bitmap[page_index] = 1

    def get_dirty(self):
        """Returns a list of indices that need re-transfer."""
        return [i for i, v in enumerate(self.bitmap) if v == 1]

    def clear(self):
        """Resets the bitmap for the next iteration round."""
        self.bitmap = bytearray(self.size)

    def get_dirty_count(self):
        return sum(self.bitmap)
