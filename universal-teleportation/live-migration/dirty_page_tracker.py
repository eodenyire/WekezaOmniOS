class DirtyPageTracker:

    def __init__(self):

        self.dirty_pages = []

    def mark_dirty(self, page):

        self.dirty_pages.append(page)

    def get_dirty_pages(self, process_id):

        return self.dirty_pages
