import tempfile
import threading
import time
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from ultramic import wait_for_device, verify_sample_rate, record_continuous

pytestmark = pytest.mark.hardware


def test_real_device_found():
    device = wait_for_device(timeout=5)
    assert device is not None


def test_real_device_supports_384k():
    device = wait_for_device(timeout=5)
    assert verify_sample_rate(device, 384000)


def test_records_real_audio():
    device = wait_for_device(timeout=5)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        stop_after_one_file = {"done": False}

        def stop_flag():
            return stop_after_one_file["done"]

        def stopper():
            time.sleep(2)
            stop_after_one_file["done"] = True

        threading.Thread(target=stopper).start()

        record_continuous(device, tmp_path, file_duration_sec=2, stop_flag=stop_flag)

        wav_files = list(tmp_path.glob("*.wav"))
        assert len(wav_files) >= 1

        audio, samplerate = sf.read(wav_files[0])
        assert samplerate == 384000
        assert np.abs(audio).max() > 0.001  # not silent
