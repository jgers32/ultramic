# ultramic

Simple, dependency-light continuous recording library for UltraMic USB microphones — install with pip, works anywhere.

Built on [sounddevice](https://python-sounddevice.readthedocs.io/) (PortAudio), so it runs the same way on Linux, macOS, and Windows — no platform-specific audio backend required.

## Features

- Automatic device detection by name (no hardcoded device indices)
- Waits for USB enumeration with a configurable timeout
- Verifies the device supports the target sample rate before recording
- Continuous recording with automatic file rotation (new `.wav` every N seconds)
- Simple CLI entry point, plus a Python API for use in your own scripts
- Zero required dependencies beyond `sounddevice`, `soundfile`, and `numpy`

## Installation

```bash
pip install git+https://github.com/yourname/ultramic.git
```

For local development:

```bash
git clone git@github.com:yourname/ultramic.git
cd ultramic
uv venv
source .venv/bin/activate
uv pip install -e ".[dev,viz]"
```

## Quickstart (CLI)

```bash
ultramic-record --audio-dir ./audio --file-duration 600
```

This will:
1. Wait for a device with "UltraMic" in its name to enumerate (default timeout: 30s)
2. Verify it supports 384kHz recording
3. Record continuously, rotating to a new timestamped `.wav` file every 600 seconds
4. Log status and errors to `./errors/`

Run `ultramic-record --help` for all options.

## Quickstart (Python API)

```python
from pathlib import Path
from ultramic import wait_for_device, verify_sample_rate, record_continuous

device = wait_for_device(timeout=30)

if not verify_sample_rate(device, sample_rate=384000):
    raise RuntimeError("Device doesn't support 384kHz")

record_continuous(device, output_dir=Path("./audio"), file_duration_sec=600)
```

See `examples/` for more:
- `examples/list_devices.py` — list all available input devices and their names
- `examples/basic_record.py` — minimal find-device-and-record example
- `examples/timed_recording.py` — record for a fixed total duration and stop automatically

## Visualizing a recording

Generate a waveform, spectrogram, log-scale spectrogram, and mel spectrogram for a recorded file:

```bash
python scripts/visualize.py path/to/recording.wav
```

Saves a combined figure to `./plots/<filename>.png` (use `--plots-dir` to change the output location).

## Testing

```bash
pytest              # unit tests only — no hardware required, safe for CI
pytest -m hardware   # hardware-dependent tests — requires a real UltraMic attached
pytest -v            # verbose output
```

`tests/test_device.py` and `tests/test_recorder.py` mock the audio backend and test pure logic (device matching, timeout handling, sample-rate checks) — these run anywhere, with no hardware needed.

`tests/test_hardware.py` exercises the real device: finding it, verifying its sample rate, and recording actual audio. These are marker-gated and skipped by default since they require physical hardware.

## Platform notes

- **WSL**: the UltraMic must be passed through to WSL with `usbipd bind` / `usbipd attach` before it will be visible to `ultramic`. Without this step, `wait_for_device` will time out as if no device were connected.
- **Sample rate**: UltraMic devices default to 384kHz, well above what most audio tooling assumes (16–48kHz). If you extend the visualization or add feature extraction, double-check that any library defaults (FFT window size, mel filter count, etc.) are adjusted for this — see `scripts/visualize.py` for an example of tuning `n_fft` and `fmax` for high sample rates.

## License

MIT — see [LICENSE](LICENSE).
