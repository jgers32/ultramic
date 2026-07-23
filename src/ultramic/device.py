import time
from typing import Optional

import sounddevice as sd


def find_device(name: str = "UltraMic") -> Optional[int]:
    """Return the PortAudio device index matching `name`, or None."""
    for index, dev in enumerate(sd.query_devices()):
        if name.lower() in dev["name"].lower() and dev["max_input_channels"] > 0:
            return index
    return None


def wait_for_device(name: str = "UltraMic", timeout: int = 30, poll_interval: float = 1.0) -> int:
    """Poll for device enumeration; raise TimeoutError if it never shows up."""
    elapsed = 0.0
    while elapsed < timeout:
        index = find_device(name)
        if index is not None:
            return index
        time.sleep(poll_interval)
        elapsed += poll_interval
    raise TimeoutError(f"{name} not found after {timeout}s")
