from datetime import datetime
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf


def verify_sample_rate(device: int, sample_rate: int = 384000) -> bool:
    """True if the device can open at the given sample rate."""
    try:
        sd.check_input_settings(device=device, samplerate=sample_rate, channels=1)
        return True
    except Exception:
        return False


def record_continuous(
    device: int,
    output_dir: Path,
    sample_rate: int = 384000,
    file_duration_sec: int = 600,
    block_size: int = 32768,
    stop_flag=None,
) -> None:
    """Record indefinitely, rotating to a new timestamped .wav file every
    `file_duration_sec` seconds. Pass a callable `stop_flag` (returns bool)
    to allow graceful shutdown; otherwise runs until interrupted."""
    output_dir.mkdir(parents=True, exist_ok=True)
    should_stop = stop_flag or (lambda: False)

    while not should_stop():
        filename = output_dir / f"{datetime.now():%Y%m%d_%H%M%S}.wav"
        frames_needed = sample_rate * file_duration_sec
        frames_written = 0

        with sf.SoundFile(filename, mode="w", samplerate=sample_rate, channels=1, subtype="PCM_16") as f:
            with sd.InputStream(device=device, samplerate=sample_rate, channels=1, blocksize=block_size, dtype="int16") as stream:
                while frames_written < frames_needed and not should_stop():
                    block, _ = stream.read(block_size)
                    f.write(block)
                    frames_written += len(block)
