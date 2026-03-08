"""
WekezaOmniOS Live Migration Tests
Phase 5: Validates the live migration engine components.
"""
import pytest
from live_migration.memory_streamer import MemoryStreamer
from live_migration.dirty_page_tracker import DirtyPageTracker
from live_migration.migration_state import MigrationState
from live_migration.page_bitmap import PageBitmap
from live_migration.migration_controller import MigrationController


# ---------------------------------------------------------------------------
# MemoryStreamer
# ---------------------------------------------------------------------------

def test_streamer_instantiation():
    """MemoryStreamer can be created."""
    streamer = MemoryStreamer()
    assert streamer is not None


def test_streamer_stream_memory():
    """stream_memory executes without error."""
    streamer = MemoryStreamer()
    streamer.stream_memory(123)
    assert streamer.total_pages_sent == 100


def test_streamer_stream_pages():
    """stream_pages transfers the specified pages."""
    streamer = MemoryStreamer()
    streamer.stream_pages([0, 1, 2])
    assert streamer.total_pages_sent == 3


# ---------------------------------------------------------------------------
# DirtyPageTracker
# ---------------------------------------------------------------------------

def test_dirty_page_tracker_mark_and_get():
    """DirtyPageTracker tracks dirty pages correctly."""
    tracker = DirtyPageTracker()
    tracker.mark_dirty(99, 5)
    tracker.mark_dirty(99, 10)
    dirty = tracker.get_dirty_pages(99)
    assert 5 in dirty
    assert 10 in dirty


def test_dirty_page_tracker_clear():
    """clear() resets the dirty list for a process."""
    tracker = DirtyPageTracker()
    tracker.mark_dirty(42, 0)
    tracker.clear(42)
    # After clear, get_dirty_pages re-simulates a fresh set
    dirty = tracker.get_dirty_pages(42)
    # Should be the simulated initial 10 pages
    assert len(dirty) == 10


# ---------------------------------------------------------------------------
# PageBitmap
# ---------------------------------------------------------------------------

def test_page_bitmap_mark_and_get_dirty():
    """PageBitmap marks pages and returns the correct dirty list."""
    bm = PageBitmap(100)
    bm.mark(5)
    bm.mark(20)
    dirty = bm.get_dirty()
    assert 5 in dirty
    assert 20 in dirty
    assert 0 not in dirty


def test_page_bitmap_clean_state():
    """A newly created PageBitmap has no dirty pages."""
    bm = PageBitmap(50)
    assert bm.get_dirty() == []


# ---------------------------------------------------------------------------
# MigrationState
# ---------------------------------------------------------------------------

def test_migration_state_initial():
    """MigrationState starts as INITIAL."""
    state = MigrationState()
    assert state.get_state() == "INITIAL"


def test_migration_state_transitions():
    """MigrationState transitions correctly through lifecycle."""
    state = MigrationState()
    for s in ["COPYING_MEMORY", "COPYING_DIRTY_PAGES", "FINAL_SYNC", "COMPLETE"]:
        state.update(s)
        assert state.get_state() == s


# ---------------------------------------------------------------------------
# MigrationController (end-to-end)
# ---------------------------------------------------------------------------

def test_migration_controller_full_pipeline():
    """MigrationController completes a migration for a given PID."""
    controller = MigrationController()
    result = controller.start_migration(process_id=1234)
    assert result["process_id"] == 1234
    assert result["state"] == "COMPLETE"
    assert result["dirty_iterations"] >= 1
