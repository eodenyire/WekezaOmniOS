class MigrationController:

    def __init__(self, streamer, tracker):

        self.streamer = streamer
        self.tracker = tracker

    def start_migration(self, process_id):

        print("Starting live migration")

        # Step 1: initial memory copy
        self.streamer.stream_memory(process_id)

        # Step 2: track dirty pages
        dirty_pages = self.tracker.get_dirty_pages(process_id)

        # Step 3: copy dirty pages
        self.streamer.stream_pages(dirty_pages)

        print("Final sync complete")
