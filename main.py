# This is the designed main PY file that will run the code

# Import declarations here
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
from pydub import AudioSegment
import numpy as np

# Function designed to filter the audio and combine the channels
def filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype="bandpass")
    return filtfilt(b, a, data)


# Function to convert MP3 to WAV dynamically
def convert_to_wav(filepath):
    """Converts an MP3 file to WAV format dynamically."""
    if filepath.endswith(".mp3"):
        wav_filepath = filepath.replace(".mp3", ".wav")
        AudioSegment.from_mp3(filepath).export(wav_filepath, format="wav")
        return wav_filepath
    return filepath  # If already WAV, return the same path


# Function to process a file dynamically
def process_file(filename):
    """Processes the selected audio file and returns data for plotting."""
    filename = convert_to_wav(filename)
    samplerate, data = wavfile.read(filename)

    # Handle stereo data by combining channels
    if len(data.shape) == 2:
        left_channel = data[:, 0]
        right_channel = data[:, 1]
        data = (left_channel + right_channel) / 2
    time = np.linspace(0.0, len(data) / samplerate, len(data), endpoint=False)
    return samplerate, data, time


# Function to calculate spectrum data
def calculate_spectrum(data, samplerate):
    """Calculates the frequency spectrum of the audio."""
    fourier_transform = np.fft.fft(data)
    spectrum = np.abs(fourier_transform)
    freqs = np.fft.fftfreq(len(data), d=1 / samplerate)

    # Only use the positive frequencies
    freqs = freqs[: len(freqs) // 2]
    spectrum = spectrum[: len(spectrum) // 2]
    return freqs, spectrum
