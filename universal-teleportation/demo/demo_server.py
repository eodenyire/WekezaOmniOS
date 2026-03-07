import time
import logging

logging.basicConfig(
    filename="demo_server.log",
    level=logging.INFO,
    format="%(asctime)s [demo_server] %(message)s"
)

def main():
    counter = 0
    while True:
        counter += 1
        logging.info(f"Server tick {counter}")
        print(f"[demo_server] Server tick {counter}")
        time.sleep(5)

if __name__ == "__main__":
    main()
