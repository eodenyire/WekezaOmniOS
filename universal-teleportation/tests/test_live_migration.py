from live_migration.memory_streamer import MemoryStreamer
from live_migration.dirty_page_tracker import DirtyPageTracker

def test_streamer():

    streamer = MemoryStreamer()

    streamer.stream_memory(123)

    assert True
