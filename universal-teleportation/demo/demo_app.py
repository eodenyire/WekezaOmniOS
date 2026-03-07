# 📄 `demo_app.py`

A simple **long-running Python process** for Phase 1.

```python
import time

def main():
    counter = 0
    while True:
        counter += 1
        print(f"[demo_app] WekezaOmniOS Demo Running | Tick {counter}")
        time.sleep(2)

if __name__ == "__main__":
    main()
