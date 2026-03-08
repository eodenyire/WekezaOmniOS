"""
WekezaOmniOS Migration Controller
Phase 5: Orchestrates iterative pre-copy migration to achieve near-zero downtime.
"""
from .memory_streamer import MemoryStreamer
from .dirty_page_tracker import DirtyPageTracker

class MigrationController:
    def __init__(self, streamer, tracker):
        self.streamer = streamer
        self.tracker = tracker
        self.threshold = 10 # Final sync happens when dirty pages are < 10

    def start_migration(self, process_id):
        print(f"\n[Controller] 🚀 Starting LIVE MIGRATION for PID {process_id}")

        # Step 1: Initial memory copy (Round 0)
        self.tracker.start_tracking()
        self.streamer.stream_memory(process_id)

        # Step 2: Iterative Dirty Page Tracking
        round_count = 1
        while round_count < 5: # Limit rounds to prevent infinite loops
            dirty_pages = self.tracker.get_dirty_pages(process_id)
            print(f"[Controller] Round {round_count}: {len(dirty_pages)} dirty pages found.")
            
            if len(dirty_pages) <= self.threshold:
                break
                
            self.tracker.bitmap.clear() # Reset bitmap for the next round
            self.streamer.stream_pages(dirty_pages)
            round_count += 1

        # Step 3: Final synchronization (The "Brownout" Window)
        print("[Controller] 🧊 Threshold met. Pausing process for final sync...")
        self.tracker.stop_tracking()
        final_pages = self.tracker.get_dirty_pages(process_id)
        self.streamer.stream_pages(final_pages)

        print(f"[Controller] ✅ SUCCESS. PID {process_id} is live on target node.")
        return True
