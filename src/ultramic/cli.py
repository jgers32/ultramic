import argparse
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from .device import wait_for_device
from .recorder import verify_sample_rate, record_continuous


def main() -> int:
    parser = argparse.ArgumentParser(description="Continuously record from an UltraMic device.")
    parser.add_argument("--audio-dir", type=Path, default=Path("./audio"))
    parser.add_argument("--error-dir", type=Path, default=Path("./errors"))
    parser.add_argument("--sample-rate", type=int, default=384000)
    parser.add_argument("--file-duration", type=int, default=600, help="seconds per rotated file")
    parser.add_argument("--usb-wait-timeout", type=int, default=30)
    args = parser.parse_args()

    args.error_dir.mkdir(parents=True, exist_ok=True)
    log_file = args.error_dir / f"ultramic_errors_{datetime.now():%Y%m%d_%H%M%S}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )

    try:
        device = wait_for_device(timeout=args.usb_wait_timeout)
    except TimeoutError as e:
        logging.error(f"{datetime.now(timezone.utc).isoformat()} ERROR: {e}")
        return 1
    logging.info(f"UltraMic found (device index {device})")

    if not verify_sample_rate(device, args.sample_rate):
        logging.error(
            f"{datetime.now(timezone.utc).isoformat()} ERROR: "
            f"UltraMic cannot record at {args.sample_rate}Hz"
        )
        return 1
    logging.info(
        f"{datetime.now(timezone.utc).isoformat()} UltraMic OK at "
        f"{args.sample_rate}Hz - starting recording"
    )

    try:
        record_continuous(
            device, args.audio_dir,
            sample_rate=args.sample_rate,
            file_duration_sec=args.file_duration,
        )
    except KeyboardInterrupt:
        logging.info("Stopped by user")
        return 0
    except Exception as e:
        logging.error(f"{datetime.now(timezone.utc).isoformat()} ERROR: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
