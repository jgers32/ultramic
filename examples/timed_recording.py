"""Record for a fixed total duration, then stop automatically (no Ctrl+C needed)."""
import time
import threading
from pathlib import Path

from ultramic import wait_for_device, record_continuous

TOTAL_DURATION_SEC = 30

device = wait_for_device()
stop_time = time.monotonic() + TOTAL_DURATION_SEC
stop_flag = lambda: time.monotonic() >= stop_time

record_continuous(
    device,
    output_dir=Path("./examples-output"),
    file_duration_sec=10,
    stop_flag=stop_flag,
)
print("Done recording.")
