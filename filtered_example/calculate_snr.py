import numpy as np
from scipy.io import wavfile

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def calculate_snr(original_path: str, test_path: str) -> float:
    """
    Calculate the Signal-to-Noise Ratio (SNR) in dB between two audio files.

    Parameters:
        original_path (str): Path to the original unmodified WAV file.
        test_path (str): Path to the modified or decrypted WAV file.

    Returns:
        float: The SNR value in decibels (dB).
    """
    # Read both audio files
    fs_orig, original = wavfile.read(original_path)
    fs_test, test = wavfile.read(test_path)

    # Ensure sample rates match
    if fs_orig != fs_test:
        raise ValueError("Sampling rates do not match.")

    # Match signal lengths
    min_len = min(len(original), len(test))
    original = original[:min_len]
    test = test[:min_len]

    # Convert to float for precision
    original_f = original.astype(np.float64)
    test_f = test.astype(np.float64)

    # Compute noise and powers
    noise = original_f - test_f
    signal_power = np.sum(original_f ** 2)
    noise_power = np.sum(noise ** 2)

    # Avoid divide-by-zero
    snr = 10 * np.log10(signal_power / noise_power) if noise_power != 0 else np.inf
    return snr


def plot_signal_noise(original: np.ndarray, test: np.ndarray, snr: float):
    noise = original.astype(np.float64) - test.astype(np.float64)

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(noise)
    plt.title("Noise (Original - Test)")

    plt.subplot(1, 2, 2)
    signal_power = np.sum(original.astype(np.float64)**2)
    noise_power = np.sum(noise**2)
    plt.bar(["Signal", "Noise"], [signal_power, noise_power])
    plt.title(f"SNR: {snr:.2f} dB")
    plt.tight_layout()
    plt.show()
