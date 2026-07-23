import argparse
from pathlib import Path

import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy import signal


def plot_waveform(ax, audio, samplerate):
    print("  Plotting waveform...")
    time = np.linspace(0, len(audio) / samplerate, num=len(audio))
    ax.plot(time, audio, linewidth=0.5)
    ax.set_title("Waveform")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")


def plot_spectrogram(ax, audio, samplerate, log_scale=False):
    label = "log-scale spectrogram" if log_scale else "spectrogram"
    print(f"  Plotting {label}...")
    f, t, Sxx = signal.spectrogram(audio, fs=samplerate)
    Sxx = 10 * np.log10(Sxx + 1e-12)  # dB scale, always log-magnitude
    ax.pcolormesh(t, f, Sxx, shading="gouraud")
    if log_scale:
        ax.set_yscale("log")
        ax.set_ylim(bottom=max(f[1], 1))  # avoid log(0)
    ax.set_title("Log-scale Spectrogram" if log_scale else "Spectrogram")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")

def plot_mel_spectrogram(ax, audio, samplerate, n_mels=128, n_fft=4096, fmax=None):
    print("  Plotting mel spectrogram...")
    try:
        import librosa
        import librosa.display
    except ImportError:
        print("    librosa not installed, skipping (pip install librosa)")
        ax.text(0.5, 0.5, "librosa not installed\n(pip install librosa)",
                ha="center", va="center", transform=ax.transAxes)
        return

    mel = librosa.feature.melspectrogram(
        y=audio.astype(np.float32), sr=samplerate,
        n_mels=n_mels, n_fft=n_fft, fmax=fmax or samplerate / 2,
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)
    librosa.display.specshow(mel_db, sr=samplerate, x_axis="time", y_axis="mel",
                              fmax=fmax or samplerate / 2, ax=ax)
    ax.set_title("Mel Spectrogram")


def main():
    parser = argparse.ArgumentParser(description="Visualize a recorded .wav file.")
    parser.add_argument("wav_path", type=Path)
    parser.add_argument("--plots-dir", type=Path, default=Path("./plots"))
    args = parser.parse_args()

    print(f"Reading {args.wav_path}...")
    audio, samplerate = sf.read(args.wav_path)
    if audio.ndim > 1:
        audio = audio[:, 0]  # take first channel if stereo
    print(f"  {len(audio)} samples at {samplerate} Hz ({len(audio) / samplerate:.1f}s)")

    print("Generating plots:")
    fig, axes = plt.subplots(4, 1, figsize=(10, 12))
    plot_waveform(axes[0], audio, samplerate)
    plot_spectrogram(axes[1], audio, samplerate)
    plot_spectrogram(axes[2], audio, samplerate, log_scale=True)
    plot_mel_spectrogram(axes[3], audio, samplerate)

    fig.suptitle(f"{args.wav_path.name} ({samplerate} Hz)")
    fig.tight_layout()

    args.plots_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.plots_dir / f"{args.wav_path.stem}.png"
    print(f"Saving to {output_path}...")
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Done: {output_path}")


if __name__ == "__main__":
    main()
