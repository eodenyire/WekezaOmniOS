class PageBitmap:

    def __init__(self, size):

        self.bitmap = [0] * size

    def mark(self, page):

        self.bitmap[page] = 1

    def get_dirty(self):

        return [i for i, v in enumerate(self.bitmap) if v == 1]
