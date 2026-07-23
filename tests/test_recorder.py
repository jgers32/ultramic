from unittest.mock import patch, MagicMock
from ultramic.recorder import verify_sample_rate


def test_verify_sample_rate_ok():
    with patch("sounddevice.check_input_settings"):
        assert verify_sample_rate(device=0, sample_rate=384000) is True


def test_verify_sample_rate_fails():
    with patch("sounddevice.check_input_settings", side_effect=Exception("unsupported")):
        assert verify_sample_rate(device=0, sample_rate=384000) is False
