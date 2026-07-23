"""List all available input devices — useful for confirming what name/index
your UltraMic shows up as before hardcoding anything."""
import sounddevice as sd

for i, dev in enumerate(sd.query_devices()):
    if dev["max_input_channels"] > 0:
        print(f"[{i}] {dev['name']} (inputs: {dev['max_input_channels']})")
