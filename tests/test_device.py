import pytest
from unittest.mock import patch
from ultramic.device import find_device, wait_for_device

FAKE_DEVICES = [
    {"name": "Built-in Microphone", "max_input_channels": 1},
    {"name": "UltraMic384K", "max_input_channels": 1},
    {"name": "HDMI Output", "max_input_channels": 0},
]

def test_find_device_zero_channels_excluded():
    devices = [{"name": "UltraMic384K", "max_input_channels": 0}]
    with patch("sounddevice.query_devices", return_value=devices):
        assert find_device("UltraMic") is None


def test_wait_for_device_times_out():
    with patch("ultramic.device.find_device", return_value=None):
        with pytest.raises(TimeoutError):
            wait_for_device(timeout=1, poll_interval=0.1)

def test_find_device_found():
    with patch("sounddevice.query_devices", return_value=FAKE_DEVICES):
        assert find_device("UltraMic") == 1


def test_find_device_not_found():
    with patch("sounddevice.query_devices", return_value=FAKE_DEVICES[:1]):
        assert find_device("UltraMic") is None
