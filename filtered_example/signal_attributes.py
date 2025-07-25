import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def find_max_frequency(file_path, energy_threshold_ratio=0.01, show_plot=True):
    """
    Finds and plots the maximum significant frequency in an audio file.

    Args:
        file_path (str): Path to the .wav audio file.
        energy_threshold_ratio (float): Fraction of max magnitude considered significant.
        show_plot (bool): Whether to display a frequency spectrum plot.

    Returns:
        float: Maximum significant frequency in Hz.
    """
    fs, data = wavfile.read(file_path)

    # Convert to mono if stereo
    if len(data.shape) == 2:
        data = data.mean(axis=1)

    # Normalize if necessary
    if not np.issubdtype(data.dtype, np.floating):
        data = data / np.max(np.abs(data))

    # Compute FFT
    fft_result = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), d=1/fs)

    # Use only positive frequencies
    pos_freqs = freqs[:len(freqs)//2]
    magnitude = np.abs(fft_result[:len(freqs)//2])

    # Find significant frequencies above threshold
    threshold = energy_threshold_ratio * np.max(magnitude)
    significant_indices = magnitude > threshold

    max_freq = pos_freqs[significant_indices].max() if np.any(significant_indices) else 0.0

    # Plot if enabled
    if show_plot:
        plt.figure(figsize=(10, 5))
        plt.plot(pos_freqs, magnitude)
        plt.axvline(max_freq, color='r', linestyle='--', label=f'Max: {max_freq:.1f} Hz')
        plt.title('Frequency Spectrum')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return max_freq
