"""Minimal example: find the device, verify sample rate, record for a fixed duration."""
from pathlib import Path

from ultramic import wait_for_device, verify_sample_rate, record_continuous

device = wait_for_device(timeout=30)
print(f"Found UltraMic at device index {device}")

if not verify_sample_rate(device, sample_rate=384000):
    raise RuntimeError("Device doesn't support 384kHz")

# Records until Ctrl+C, rotating a new file every 60 seconds
record_continuous(device, output_dir=Path("./examples-output"), file_duration_sec=60)
