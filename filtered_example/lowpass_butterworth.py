from scipy.signal import butter, lfilter

def low_pass_filter(data, cutoff_freq, fs, order=5):
    nyquist = 0.5 * fs
    norm_cutoff = cutoff_freq / nyquist
    b, a = butter(order, norm_cutoff, btype='low', analog=False)
    filtered_data = lfilter(b, a, data)
    return filtered_data.astype(data.dtype)  # preserve original type