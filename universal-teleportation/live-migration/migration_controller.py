"""
WekezaOmniOS Live Migration Controller
Phase 5: Orchestrates pre-copy live migration with minimal downtime.

Algorithm (Pre-Copy):
  1. Initial memory copy while app keeps running.
  2. Track pages dirtied during the copy.
  3. Iteratively copy dirty pages until the delta is small enough.
  4. Brief pause — copy final dirty pages, then resume on target.
"""
from .memory_streamer import MemoryStreamer
from .dirty_page_tracker import DirtyPageTracker
from .migration_state import MigrationState


MAX_DIRTY_ITERATIONS = 5
DIRTY_PAGE_THRESHOLD = 10  # Stop iterating when fewer than this many pages remain dirty


class MigrationController:
    """
    Coordinates the entire live migration sequence for a single process.
    """

    def __init__(self, streamer: MemoryStreamer = None, tracker: DirtyPageTracker = None):
        self.streamer = streamer or MemoryStreamer()
        self.tracker = tracker or DirtyPageTracker()
        self.state = MigrationState()

    def start_migration(self, process_id: int) -> dict:
        """
        Execute the full pre-copy migration pipeline for *process_id*.

        Args:
            process_id: PID of the process to migrate.

        Returns:
            dict with migration result details.
        """
        print(f"[MigrationController] Starting live migration for PID {process_id}")
        self.state.update("COPYING_MEMORY")

        # Step 1: Initial bulk memory copy
        self.streamer.stream_memory(process_id)

        # Step 2: Iteratively synchronise dirty pages
        self.state.update("COPYING_DIRTY_PAGES")
        iterations = 0
        while iterations < MAX_DIRTY_ITERATIONS:
            dirty_pages = self.tracker.get_dirty_pages(process_id)
            if len(dirty_pages) < DIRTY_PAGE_THRESHOLD:
                print(f"[MigrationController] Dirty pages ({len(dirty_pages)}) below threshold — proceeding to final sync.")
                break
            print(f"[MigrationController] Dirty pages remaining: {len(dirty_pages)} (iteration {iterations + 1})")
            self.streamer.stream_pages(dirty_pages)
            self.tracker.clear(process_id)
            iterations += 1

        # Step 3: Final sync (brief pause)
        self.state.update("FINAL_SYNC")
        final_dirty = self.tracker.get_dirty_pages(process_id)
        if final_dirty:
            self.streamer.stream_pages(final_dirty)
            self.tracker.clear(process_id)

        self.state.update("COMPLETE")
        print(f"[MigrationController] Migration complete for PID {process_id} after {iterations + 1} iteration(s).")
        return {
            "process_id": process_id,
            "state": self.state.get_state(),
            "dirty_iterations": iterations + 1,
        }
