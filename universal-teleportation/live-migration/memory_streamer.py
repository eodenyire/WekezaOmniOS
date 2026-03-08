class MemoryStreamer:

    def stream_memory(self, process_id):

        print(f"Streaming memory for process {process_id}")

    def stream_pages(self, pages):

        for page in pages:
            print(f"Transferring page {page}")
